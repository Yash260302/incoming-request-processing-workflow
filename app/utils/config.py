from pathlib import Path


class Config:
    """
    Central configuration for the Incoming Request Processing Workflow.
    """

    # ---------------------------------------------------------
    # Project Root
    # ---------------------------------------------------------

    PROJECT_ROOT = Path(__file__).resolve().parents[2]

    # ---------------------------------------------------------
    # Data
    # ---------------------------------------------------------

    DATA_DIR = PROJECT_ROOT / "data"

    RAW_DATA_DIR = DATA_DIR / "raw"

    PROCESSED_DATA_DIR = DATA_DIR / "processed"

    SAMPLE_DATA_DIR = DATA_DIR / "samples"

    RAW_DATASET = RAW_DATA_DIR / "customer_support_tickets.csv"

    PROCESSED_DATASET = (
        PROCESSED_DATA_DIR /
        "processed_customer_support_tickets.csv"
    )

    # ---------------------------------------------------------
    # Outputs
    # ---------------------------------------------------------

    OUTPUT_DIR = PROJECT_ROOT / "outputs"

    REPORTS_DIR = OUTPUT_DIR / "reports"

    LOGS_DIR = OUTPUT_DIR / "logs"

    PREDICTIONS_DIR = OUTPUT_DIR / "predictions"

    # ---------------------------------------------------------
    # Models
    # ---------------------------------------------------------

    MODEL_DIR = PROJECT_ROOT / "models"

    CLASSIFIER_DIR = MODEL_DIR / "classifier"

    ENTITY_DIR = MODEL_DIR / "entity_extractor"

    RESPONSE_DIR = MODEL_DIR / "response_generator"

    # ---------------------------------------------------------
    # AI Configuration
    # ---------------------------------------------------------

    DEFAULT_LLM = "gpt-5.5"

    DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    CONFIDENCE_THRESHOLD = 0.80

    MAX_RESPONSE_TOKENS = 800