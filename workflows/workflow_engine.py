import uuid
from datetime import datetime, timedelta
from typing import Dict, Any

from app.services.inference.unified_predictor import UnifiedPredictor
from app.services.entity_extractor import EntityExtractor
from app.services.knowledge_base import KnowledgeBase
from workflows.response_generator import ResponseGenerator
from workflows.audit_logger import AuditLogger
from app.utils.logger import Logger


class WorkflowEngine:
    """
    Central Workflow Engine orchestrating multi-branch request processing logic.
    """

    def __init__(self):
        self.logger = Logger.get_logger()
        self.predictor = UnifiedPredictor()
        self.entity_extractor = EntityExtractor()
        self.knowledge_base = KnowledgeBase()
        self.response_generator = ResponseGenerator()
        self.audit_logger = AuditLogger()

    def process_request(self, subject: str, body: str, raw_text: str = None) -> Dict[str, Any]:
        if not raw_text:
            raw_text = f"{subject or ''} {body or ''}".strip()

        request_id = f"REQ-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.now()

        # Step 1: Predict Queue, Priority, Type & Confidence
        prediction = self.predictor.predict(raw_text)
        queue = prediction["queue"]
        priority = prediction["priority"]
        ticket_type = prediction["type"]
        confidence = prediction["overall_confidence"]
        is_low_confidence = prediction["is_low_confidence"]

        # Step 2: Entity Extraction
        entities = self.entity_extractor.extract_entities(raw_text)

        # Step 3: Knowledge Base Lookup
        kb_result = self.knowledge_base.query(raw_text)

        # Step 4: Branch Determination Logic
        raw_lower = raw_text.lower()
        branch = "General Inquiry"
        status = "Resolved"
        actions = []
        sla_timer = "N/A"

        # Explicit signal heuristics overriding general default queue
        has_outage_signal = any(w in raw_lower for w in ["outage", "server down", "cannot login", "system down", "critical outage"])
        has_complaint_signal = any(w in raw_lower for w in ["damaged", "broken", "unacceptable", "refund", "complaint", "faulty"])
        has_service_signal = any(w in raw_lower for w in ["install", "upgrade", "license", "seats", "provision"])

        if has_outage_signal or (ticket_type.lower() == "incident" and has_complaint_signal):
            branch = "Technical Incident"
            priority = "High"
            status = "In Progress (Incident Active)"
            actions = [
                "1) Urgent flag assigned (Critical/High priority).",
                "2) Emergency alert dispatched to Supervisor and Technical Analysts via Slack/Email.",
                "3) Urgent acknowledgement email drafted and queued.",
                "4) Automated resolution PAUSED (Human-in-the-loop mandated)."
            ]
            sla_timer = f"Immediate Alert (Target: {(now + timedelta(hours=1)).strftime('%H:%M EST')})"

        elif has_service_signal:
            branch = "Service Request"
            priority = "Medium"
            status = "Routed to Operations"
            actions = [
                f"1) Extracted details: Software='{entities.get('software_or_product', 'N/A')}', Seats='{entities.get('user_count', 'N/A')}', Deadline='{entities.get('deadline', 'N/A')}'.",
                f"2) Routed request ticket to [{queue}] team.",
                "3) Auto-acknowledgement email generated and sent to customer.",
                "4) 24-Hour SLA provisioning timer created."
            ]
            sla_timer = f"24-Hour SLA Timer (Deadline: {(now + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M')})"

        elif kb_result or any(w in raw_lower for w in ["hours", "open", "weekend", "question", "inquiry", "info", "information"]):
            branch = "General Inquiry"
            priority = "Low"
            status = "Resolved"
            actions = [
                f"1) Query matched against Knowledge Base FAQ: '{kb_result['matched_category'] if kb_result else 'General FAQ'}'.",
                "2) Auto-generated factual reply.",
                "3) Outbound email dispatched to customer.",
                "4) Ticket marked as RESOLVED in system."
            ]
            sla_timer = "Auto-Closed"

        elif has_complaint_signal or "complaint" in queue.lower() or priority.lower() in ["high", "critical", "3"]:
            branch = "Complaint / Escalation"
            priority = "High"
            status = "Escalated to Management"
            actions = [
                "1) Drafted formal apology email with refund & replacement info.",
                "2) Escalated ticket to Senior Support Manager.",
                "3) Logged case in CRM database with High Priority tag.",
                "4) Set 2-Hour SLA follow-up reminder."
            ]
            sla_timer = f"2-Hour Manager Follow-up (Deadline: {(now + timedelta(hours=2)).strftime('%H:%M EST')})"

        elif has_service_signal:
            branch = "Service Request"
            priority = "Medium"
            status = "Routed to Operations"
            actions = [
                f"1) Extracted details: Software='{entities.get('software_or_product', 'N/A')}', Seats='{entities.get('user_count', 'N/A')}', Deadline='{entities.get('deadline', 'N/A')}'.",
                f"2) Routed request ticket to [{queue}] team.",
                "3) Auto-acknowledgement email generated and sent to customer.",
                "4) 24-Hour SLA provisioning timer created."
            ]
            sla_timer = f"24-Hour SLA Timer (Deadline: {(now + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M')})"

        elif kb_result or any(w in raw_lower for w in ["hours", "open", "weekend", "question", "inquiry", "info", "information"]):
            branch = "General Inquiry"
            priority = "Low"
            status = "Resolved"
            actions = [
                f"1) Query matched against Knowledge Base FAQ: '{kb_result['matched_category'] if kb_result else 'General FAQ'}'.",
                "2) Auto-generated factual reply.",
                "3) Outbound email dispatched to customer.",
                "4) Ticket marked as RESOLVED in system."
            ]
            sla_timer = "Auto-Closed"

        else:
            branch = "General Inquiry"
            status = "Resolved"
            actions = [
                f"1) Query matched against Knowledge Base FAQ: '{kb_result['matched_category'] if kb_result else 'General FAQ'}'.",
                "2) Auto-generated factual reply.",
                "3) Outbound email dispatched to customer.",
                "4) Ticket marked as RESOLVED in system."
            ]
            sla_timer = "Auto-Closed"

        # Append Low-Confidence Human-in-the-loop notice if confidence score is low
        if is_low_confidence:
            actions.append("⚠️ LOW CONFIDENCE ALERT: Model confidence < 35%. Flagged for human agent verification.")
            if status == "Resolved":
                status = "Pending Agent Verification"

        # Step 5: Response Generation
        response_draft = self.response_generator.generate_response(branch, entities, kb_result)

        # Step 6: Assemble Execution Result & Record Audit Log
        result = {
            "request_id": request_id,
            "timestamp": now.isoformat(),
            "subject": subject or "N/A",
            "body": body or raw_text,
            "raw_text": raw_text,
            "queue": queue,
            "priority": priority,
            "type": ticket_type,
            "confidence": confidence,
            "is_low_confidence": is_low_confidence,
            "branch": branch,
            "actions": actions,
            "extracted_entities": entities,
            "kb_result": kb_result,
            "response": response_draft,
            "status": status,
            "sla_timer": sla_timer
        }

        self.audit_logger.log_execution(result)
        return result
