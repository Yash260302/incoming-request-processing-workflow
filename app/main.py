import sys
from pathlib import Path

# Ensure root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app.services.dataset_manager import DatasetManager
from app.services.champion_model import ChampionModel
from app.services.priority_model import PriorityModel
from app.services.type_model import TypeModel
from workflows.workflow_engine import WorkflowEngine
from app.utils.logger import Logger


def main():
    logger = Logger.get_logger()
    logger.info("=" * 80)
    logger.info("STARTING INCOMING REQUEST PROCESSING WORKFLOW POC INITIALIZATION")
    logger.info("=" * 80)

    dataset_mgr = DatasetManager()
    df = dataset_mgr.load_dataset()
    dataset_mgr.validate_dataset()
    dataset_mgr.statistics()

    # 1. Train Queue / Intent Champion Model
    logger.info("\n--- 1. Training Queue Model ---")
    champion = ChampionModel()
    champion.train(df)

    # 2. Train Priority Model
    logger.info("\n--- 2. Training Priority Model ---")
    priority = PriorityModel()
    priority.train(df)

    # 3. Train Ticket Type Model
    logger.info("\n--- 3. Training Ticket Type Model ---")
    ticket_type_model = TypeModel()
    ticket_type_model.train(df)

    # 4. End-to-End Workflow Execution Test
    logger.info("\n--- 4. Running Sample Workflow Test ---")
    engine = WorkflowEngine()

    test_tickets = [
        {
            "subject": "Broken item – need refund",
            "body": "I received a damaged gadget yesterday, and customer service hasn't responded. This is unacceptable!"
        },
        {
            "subject": "System Outage – URGENT",
            "body": "Our servers are down and customers can't login. This is critical!"
        },
        {
            "subject": "Install new software license",
            "body": "Hello, I need to upgrade to Premium Edition for 10 more users by next Monday."
        }
    ]

    for ticket in test_tickets:
        logger.info(f"\nProcessing Ticket: '{ticket['subject']}'")
        res = engine.process_request(ticket["subject"], ticket["body"])
        logger.info(f" -> Queue: {res['queue']} | Priority: {res['priority']} | Type: {res['type']}")
        logger.info(f" -> Branch: {res['branch']} | Status: {res['status']}")

    logger.info("=" * 80)
    logger.info("POC PIPELINE INITIALIZATION & MODEL TRAINING COMPLETE!")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()