from typing import Dict, Any


class ResponseGenerator:
    """
    Drafts tailored outbound email responses based on the request branch, extracted entities, and knowledge retrieval.
    """

    def generate_response(self, branch: str, entities: Dict[str, Any], kb_result: Dict[str, Any] = None) -> str:
        if branch == "Complaint / Escalation":
            return (
                "Dear Valued Customer,\n\n"
                "We sincerely apologize for the experience you encountered. Your issue has been escalated with HIGH PRIORITY "
                "to our Senior Support Management team. Case ticket has been logged in our system and assigned a 2-hour manager follow-up.\n\n"
                "A dedicated specialist will contact you shortly to resolve this matter and process any eligible refund/replacement.\n\n"
                "Best regards,\n"
                "Customer Support Escalation Team"
            )

        elif branch == "Technical Incident":
            return (
                "URGENT TICKET ACKNOWLEDGEMENT:\n\n"
                "Hello,\n\n"
                "We have received your incident report regarding system issues/outage. Our technical operations and engineering teams "
                "have been alerted immediately via emergency alerts. Automated resolution has been paused to ensure human engineer intervention.\n\n"
                "We are actively working on resolving this issue and will update you shortly.\n\n"
                "Sincerely,\n"
                "Technical Operations Team"
            )

        elif branch == "Service Request":
            software = entities.get("software_or_product", "requested product/license")
            seats = entities.get("user_count", "specified")
            deadline = entities.get("deadline", "requested timeframe")
            
            return (
                f"Hello,\n\n"
                f"Thank you for submitting your service request. We have captured your request details:\n"
                f" - Service / Software: {software}\n"
                f" - Quantity / Seats: {seats}\n"
                f" - Target Timeline: {deadline}\n\n"
                f"Your request has been routed to our Sales & Provisioning team. A 24-hour SLA timer has been set.\n\n"
                f"Best regards,\n"
                f"IT & Sales Service Desk"
            )

        else: # General Inquiry / Other
            if kb_result and kb_result.get("answer"):
                faq_answer = kb_result["answer"]
            else:
                faq_answer = "Thank you for reaching out to us. We have received your inquiry and marked your ticket as resolved."
            
            return (
                f"Hi there,\n\n"
                f"{faq_answer}\n\n"
                f"If you have any further questions, feel free to reply to this email.\n\n"
                f"Warm regards,\n"
                f"Customer Care Team"
            )
