"""
run_pipeline.py
----------------
Master script — runs the full analytics pipeline end to end.
Outputs 3 CSV files ready for Power BI import.

Run from the root of the project:
    python run_pipeline.py
"""

import sys
import os

# Make sure sub-modules can find each other
sys.path.append(os.path.dirname(__file__))

from data_ingestion.load_data import load_raw_data
from core_analytics.patient_processor import calculate_treatment_duration
from core_analytics.market_metrics import aggregate_by_condition
from core_analytics.adherence_logic import flag_adherence

# ── Step 1: Load raw data ──────────────────────────────────────────────────────
print("\n" + "="*60)
print("STEP 1: Loading Raw Data")
print("="*60)
df = load_raw_data()

# ── Step 2: Treatment Duration ─────────────────────────────────────────────────
print("\n" + "="*60)
print("STEP 2: Calculating Treatment Duration")
print("="*60)
duration_df = calculate_treatment_duration(df)

# ── Step 3: Market Metrics ─────────────────────────────────────────────────────
print("\n" + "="*60)
print("STEP 3: Aggregating Patient Volume per Condition")
print("="*60)
market_df = aggregate_by_condition(df)

# ── Step 4: Adherence Flagging ─────────────────────────────────────────────────
print("\n" + "="*60)
print("STEP 4: Flagging Patient Adherence")
print("="*60)
adherence_df = flag_adherence(df)

# ── Step 5: Export to Power BI CSVs ───────────────────────────────────────────
print("\n" + "="*60)
print("STEP 5: Exporting to powerbi_exports/")
print("="*60)

os.makedirs("powerbi_exports", exist_ok=True)

duration_df.to_csv("powerbi_exports/duration_export.csv", index=False)
market_df.to_csv("powerbi_exports/ta_summary_export.csv", index=False)
adherence_df.to_csv("powerbi_exports/adherence_export.csv", index=False)

print("  ✔ powerbi_exports/duration_export.csv")
print("  ✔ powerbi_exports/ta_summary_export.csv")
print("  ✔ powerbi_exports/adherence_export.csv")

print("\n" + "="*60)
print("Pipeline Complete. Files ready for Power BI.")
print("="*60 + "\n")
