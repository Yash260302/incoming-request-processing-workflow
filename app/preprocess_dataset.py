import pandas as pd
from pathlib import Path

# -------------------------------------------------------------------
# Project Paths
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw" / "customer_support_tickets.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = PROCESSED_DIR / "processed_customer_support_tickets.csv"

# -------------------------------------------------------------------
# Load Dataset
# -------------------------------------------------------------------

print("Loading dataset...")

df = pd.read_csv(RAW_DATA)

print(f"Loaded {len(df)} records")

# -------------------------------------------------------------------
# Handle Missing Values
# -------------------------------------------------------------------

df["subject"] = df["subject"].fillna("")
df["body"] = df["body"].fillna("")

# -------------------------------------------------------------------
# Merge Subject + Body
# -------------------------------------------------------------------

df["request_text"] = (
    "Subject: "
    + df["subject"]
    + "\n\nBody:\n"
    + df["body"]
)

# Map Priority levels if numeric (1=Low, 2=Medium, 3=Critical/High)
if df["priority"].dtype in ['int64', 'float64']:
    priority_map = {1: "Low", 2: "Medium", 3: "High"}
    df["priority"] = df["priority"].map(priority_map).fillna("Medium")

df["priority"] = df["priority"].astype(str)

required_columns = [
    "subject",
    "body",
    "request_text",
    "queue",
    "priority",
    "type",
    "language",
    "answer"
]

processed_df = df[[c for c in required_columns if c in df.columns]].copy()

# -------------------------------------------------------------------
# Remove Empty Requests
# -------------------------------------------------------------------

processed_df = processed_df[
    processed_df["request_text"].str.strip() != ""
]

# -------------------------------------------------------------------
# Save Processed Dataset
# -------------------------------------------------------------------

processed_df.to_csv(OUTPUT_FILE, index=False)

print("\nProcessing Complete!")

print(f"Processed Records : {len(processed_df)}")

print(f"Saved To : {OUTPUT_FILE}")

print("\nPreview:\n")

print(processed_df.head())