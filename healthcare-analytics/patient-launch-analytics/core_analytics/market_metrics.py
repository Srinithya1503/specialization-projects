"""
core_analytics/market_metrics.py
----------------------------------
Aggregates the 100k records into Patient Volume per Condition.
This simulates a Market Share / Therapeutic Area Concentration analysis.

Output columns:
  - condition: the primary diagnosis
  - total_visits: how many times this condition appeared as primary
  - unique_patients: how many distinct patients have this as a primary diagnosis
  - visit_share_pct: what % of all visits this condition represents
  - patient_share_pct: what % of all unique patients this condition touches
"""

import pandas as pd
import sys
sys.path.append("..")
from data_ingestion.load_data import load_raw_data


def aggregate_by_condition(df):
    # Count visits per condition
    visit_counts = df.groupby("primary_diagnosis").size().reset_index(name="total_visits")

    # Count unique patients per condition
    patient_counts = df.groupby("primary_diagnosis")["patient_id"].nunique().reset_index()
    patient_counts.columns = ["primary_diagnosis", "unique_patients"]

    # Merge both together
    summary = pd.merge(visit_counts, patient_counts, on="primary_diagnosis")

    # Calculate percentage share columns
    summary["visit_share_pct"] = round(summary["total_visits"] / summary["total_visits"].sum() * 100, 2)
    summary["patient_share_pct"] = round(summary["unique_patients"] / df["patient_id"].nunique() * 100, 2)

    # Sort by patient volume descending
    summary = summary.sort_values("unique_patients", ascending=False).reset_index(drop=True)

    # Rename for readability
    summary.rename(columns={"primary_diagnosis": "condition"}, inplace=True)

    print(f"[market_metrics] Summary across {len(summary)} conditions:")
    print(summary.to_string(index=False))
    return summary


if __name__ == "__main__":
    df = load_raw_data()
    result = aggregate_by_condition(df)
