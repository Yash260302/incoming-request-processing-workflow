import re
from typing import Dict, Any


class EntityExtractor:
    """
    Regex and heuristic entity extractor for customer support requests.
    Extracts customer info, product/software names, quantities, deadlines, error codes, and priority markers.
    """

    def extract_entities(self, text: str) -> Dict[str, Any]:
        entities = {}

        # Email address extraction
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        if email_match:
            entities["customer_email"] = email_match.group(0)

        # Account / Ticket / Order ID extraction
        account_match = re.search(r'(?:account|id|order|ticket|ref|invoice)\s*#?\s*([A-Z0-9-]{4,15})', text, re.IGNORECASE)
        if account_match:
            entities["account_or_ticket_id"] = account_match.group(1)

        # User count / seats extraction (e.g. "10 users", "5 seats", "for 20 licenses")
        quantity_match = re.search(r'(\d+)\s*(?:users|seats|licenses|members|accounts|copies)', text, re.IGNORECASE)
        if quantity_match:
            entities["user_count"] = int(quantity_match.group(1))

        # Software / Product name extraction
        software_keywords = [
            "Premium Edition", "Enterprise", "Pro Edition", "Office 365", "Salesforce",
            "Jira", "Slack", "Database", "Windows Server", "CRM", "Docker", "Kubernetes"
        ]
        found_software = []
        for sw in software_keywords:
            if sw.lower() in text.lower():
                found_software.append(sw)
        if found_software:
            entities["software_or_product"] = ", ".join(found_software)

        # Monetary value extraction (€50, $30, etc.)
        money_match = re.findall(r'[\$€£]\s*\d+(?:\.\d{2})?|\d+\s*(?:EUR|USD|GBP|euros|dollars)', text, re.IGNORECASE)
        if money_match:
            entities["amounts_mentioned"] = money_match

        # Deadline / Date extraction (e.g. "by next Monday", "by 4/30", "within 2 days")
        deadline_match = re.search(r'by\s+([A-Za-z0-9/\s,-]+?)(?=\.|\n|$)', text, re.IGNORECASE)
        if deadline_match:
            entities["deadline"] = deadline_match.group(1).strip()

        # Urgency keywords
        urgency_keywords = ["urgent", "asap", "immediately", "critical", "down", "outage", "emergency", "unacceptable"]
        detected_urgency_words = [word for word in urgency_keywords if word in text.lower()]
        if detected_urgency_words:
            entities["urgency_signals"] = detected_detected = list(set(detected_urgency_words))

        return entities
