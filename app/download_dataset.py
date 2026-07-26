from datasets import load_dataset
import pandas as pd
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

# Create data/raw if it doesn't exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

print("Downloading dataset...")

# Download dataset
dataset = load_dataset("Tobi-Bueck/customer-support-tickets")

print(dataset)

# Save train split
train_df = dataset["train"].to_pandas()

output_file = RAW_DATA_DIR / "customer_support_tickets.csv"
train_df.to_csv(output_file, index=False)

print(f"\nDataset downloaded successfully!")
print(f"Saved to: {output_file}")

print("\nFirst 5 rows:")
print(train_df.head())