from typing import Optional, Dict, Any


class KnowledgeBase:
    """
    RAG / FAQ Knowledge Retrieval Engine for auto-generating responses for general inquiries and standard support tickets.
    """

    FAQ_DATABASE = [
        {
            "keywords": ["hours", "open", "weekend", "operating hours", "business hours", "schedule"],
            "category": "Hours of Operation",
            "answer": "Our customer support and operational hours are Monday to Friday, 8:00 AM – 8:00 PM EST. On weekends, our automated service handles requests, and emergency technical support remains active 24/7."
        },
        {
            "keywords": ["invoice", "charge", "charged", "extra fee", "discrepancy", "bill", "payment"],
            "category": "Billing & Invoices",
            "answer": "Invoice charges reflect standard base subscriptions plus any prorated user license additions made during the prior billing cycle. You can view itemized billing breakdowns in your account dashboard under Settings > Billing."
        },
        {
            "keywords": ["refund", "damaged", "broken", "return", "faulty", "replacement"],
            "category": "Refund & Product Replacement",
            "answer": "We deeply apologize for damaged items or order issues. Our standard policy offers full refunds or zero-cost expedited replacements within 30 days of receipt. Our customer escalation team will process this immediately."
        },
        {
            "keywords": ["license", "upgrade", "seats", "install", "software license", "provision"],
            "category": "Software Licensing & Provisioning",
            "answer": "Software upgrades and additional user license seats are provisioned within 24 business hours. Our Sales and IT Provisioning team will issue updated license keys and send onboarding instructions."
        },
        {
            "keywords": ["outage", "server down", "cannot login", "system down", "critical", "incident"],
            "category": "System Outage & Technical Support",
            "answer": "We have detected a high-priority technical incident. Our engineering team is currently investigating server connectivity and working towards full restoration. SLA updates will be posted hourly."
        }
    ]

    def query(self, text: str) -> Optional[Dict[str, Any]]:
        text_lower = text.lower()
        best_match = None
        max_matches = 0

        for entry in self.FAQ_DATABASE:
            matches = sum(1 for kw in entry["keywords"] if kw in text_lower)
            if matches > max_matches:
                max_matches = matches
                best_match = entry

        if best_match and max_matches > 0:
            return {
                "matched_category": best_match["category"],
                "answer": best_match["answer"],
                "relevance_score": min(1.0, round(max_matches * 0.35, 2))
            }
        return None
