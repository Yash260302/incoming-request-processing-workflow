import unittest
import sys
from pathlib import Path

# Ensure root directory is in sys.path
BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.entity_extractor import EntityExtractor
from app.services.knowledge_base import KnowledgeBase
from workflows.workflow_engine import WorkflowEngine
from workflows.audit_logger import AuditLogger


class TestWorkflowComponents(unittest.TestCase):

    def setUp(self):
        self.extractor = EntityExtractor()
        self.kb = KnowledgeBase()
        self.engine = WorkflowEngine()
        self.logger = AuditLogger()

    def test_entity_extractor(self):
        text = "Hello, I need to upgrade to Premium Edition for 10 users by next Monday. Email: user@example.com"
        entities = self.extractor.extract_entities(text)

        self.assertEqual(entities.get("customer_email"), "user@example.com")
        self.assertEqual(entities.get("user_count"), 10)
        self.assertIn("Premium Edition", entities.get("software_or_product", ""))

    def test_knowledge_base_match(self):
        query_text = "What are your hours of operation on weekends?"
        match = self.kb.query(query_text)

        self.assertIsNotNone(match)
        self.assertEqual(match["matched_category"], "Hours of Operation")
        self.assertIn("8:00 AM", match["answer"])

    def test_workflow_engine_complaint_branch(self):
        subject = "Broken item – need refund"
        body = "I received a damaged product. Customer service hasn't responded!"
        result = self.engine.process_request(subject, body)

        self.assertIn(result["branch"], ["Complaint / Escalation", "Technical Incident"])
        self.assertTrue(len(result["actions"]) > 0)
        self.assertIn("apologize", result["response"].lower())

    def test_audit_logger(self):
        record = {
            "request_id": "TEST-REQ-001",
            "subject": "Unit Test Subject",
            "queue": "Technical Support",
            "priority": "High",
            "type": "Incident",
            "confidence": 0.95,
            "branch": "Technical Incident",
            "actions": ["Action 1"],
            "extracted_entities": {},
            "response": "Test Response",
            "status": "In Progress"
        }
        self.logger.log_execution(record)
        logs = self.logger.get_recent_logs(limit=5)
        self.assertTrue(any(l["request_id"] == "TEST-REQ-001" for l in logs))


if __name__ == "__main__":
    unittest.main()
