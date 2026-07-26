import sys
from pathlib import Path

# Force UTF-8 stdout encoding for Windows console
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ensure root directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from workflows.workflow_engine import WorkflowEngine
from app.utils.logger import Logger


def run_validation():
    logger = Logger.get_logger()
    logger.info("=" * 80)
    logger.info("VALIDATING INCOMING REQUEST PROCESSING WORKFLOW - 5 SCENARIOS")
    logger.info("=" * 80)

    engine = WorkflowEngine()

    scenarios = [
        {
            "name": "Scenario 1: Product Complaint",
            "subject": "Broken item – need refund",
            "body": "I received a damaged gadget yesterday, and customer service hasn't responded. This is unacceptable!"
        },
        {
            "name": "Scenario 2: Billing Inquiry",
            "subject": "Invoice discrepancy",
            "body": "I was charged €50 instead of €30 on my last statement. Can you explain the extra fees?"
        },
        {
            "name": "Scenario 3: Service Request",
            "subject": "Install new software license",
            "body": "Hello, I need to upgrade to Premium Edition for 10 more users by next Monday."
        },
        {
            "name": "Scenario 4: Technical Outage Incident",
            "subject": "System Outage – URGENT",
            "body": "Our servers are down and customers can't login. This is critical!"
        },
        {
            "name": "Scenario 5: Casual Inquiry",
            "subject": "Hours of operation",
            "body": "Hi, just wanted to know if you're open on weekends."
        }
    ]

    for sc in scenarios:
        print("\n" + "=" * 70)
        print(f"📌 {sc['name']}")
        print("=" * 70)
        print(f"Input Subject : {sc['subject']}")
        print(f"Input Body    : {sc['body']}")

        res = engine.process_request(sc["subject"], sc["body"])

        print(f"\n🔮 CLASSIFICATION & INFERENCE:")
        print(f"   Queue (Department) : {res['queue']}")
        print(f"   Priority / Urgency : {res['priority']}")
        print(f"   Ticket Type        : {res['type']}")
        print(f"   Confidence Score   : {res['confidence'] * 100:.1f}%")

        print(f"\n🌿 WORKFLOW ROUTING:")
        print(f"   Branch Taken       : {res['branch']}")
        print(f"   Status             : {res['status']}")
        print(f"   SLA Timer          : {res['sla_timer']}")

        print(f"\n⚙️ EXECUTED ACTIONS:")
        for action in res["actions"]:
            print(f"   • {action}")

        if res["extracted_entities"]:
            print(f"\n🔎 EXTRACTED ENTITIES:")
            for k, v in res["extracted_entities"].items():
                print(f"   • {k}: {v}")

        print(f"\n✉️ DRAFTED RESPONSE:")
        print("--------------------------------------------------")
        print(res["response"])
        print("--------------------------------------------------")

    print("\n" + "=" * 80)
    print("✅ VALIDATION OF ALL 5 SCENARIOS COMPLETED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    run_validation()
