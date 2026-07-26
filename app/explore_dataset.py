import pandas as pd
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset path
DATA_PATH = BASE_DIR / "data" / "raw" / "customer_support_tickets.csv"

# Load dataset
df = pd.read_csv(DATA_PATH)

print("=" * 80)
print("DATASET OVERVIEW")
print("=" * 80)

print(f"\nNumber of rows: {len(df)}")
print(f"Number of columns: {len(df.columns)}")

print("\nColumns:")
print(df.columns.tolist())

print("\n")

print("=" * 80)
print("COLUMN INFORMATION")
print("=" * 80)
print(df.info())

print("\n")

print("=" * 80)
print("FIRST FIVE RECORDS")
print("=" * 80)
print(df.head())

print("\n")

print("=" * 80)
print("MISSING VALUES")
print("=" * 80)
print(df.isnull().sum())

print("\n")

print("=" * 80)
print("QUEUE DISTRIBUTION")
print("=" * 80)

if "queue" in df.columns:
    print(df["queue"].value_counts())

print("\n")

print("=" * 80)
print("PRIORITY DISTRIBUTION")
print("=" * 80)

if "priority" in df.columns:
    print(df["priority"].value_counts())

print("\n")

print("=" * 80)
print("TYPE DISTRIBUTION")
print("=" * 80)

if "type" in df.columns:
    print(df["type"].value_counts())

print("\n")

print("=" * 80)
print("DONE")
print("=" * 80)