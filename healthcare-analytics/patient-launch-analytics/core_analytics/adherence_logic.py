"""
core_analytics/adherence_logic.py
-----------------------------------
Flags patients as High or Low adherence based on their visit frequency.

Logic (confidence-tuned):
  - We use visit count as a proxy for medication adherence
  - Patients with more visits are assumed to be more engaged with their care
  - We calculate visits per year (annualized) to normalize for time in system

  Thresholds:
    High Adherence   → >= 3 visits per year  (actively managed)
    Medium Adherence → 1–2 visits per year   (occasional engagement)
    Low Adherence    → < 1 visit per year    (likely lapsed / non-adherent)

  Note: In a real project, this would use Rx fill data and MPR (Medication
  Possession Ratio). This is a visit-frequency proxy for demo purposes.
"""

import pandas as pd
import numpy as np
import sys
sys.path.append("..")
from data_ingestion.load_data import load_raw_data


def flag_adherence(df):
    # Count total visits per patient
    visit_count = df.groupby("patient_id").size().reset_index(name="total_visits")

    # Get the date range for each patient
    date_range = df.groupby("patient_id")["visit_date"].agg(
        first_visit="min",
        last_visit="max"
    ).reset_index()

    # Merge visit count with date range
    patient_data = pd.merge(visit_count, date_range, on="patient_id")

    # Calculate how many years the patient has been in the system
    patient_data["years_in_system"] = (
        (patient_data["last_visit"] - patient_data["first_visit"]).dt.days / 365
    )

    # Avoid division by zero — set minimum to 0.1 years (~36 days)
    patient_data["years_in_system"] = patient_data["years_in_system"].clip(lower=0.1)

    # Annualized visit rate
    patient_data["visits_per_year"] = round(
        patient_data["total_visits"] / patient_data["years_in_system"], 2
    )

    # Apply adherence label
    def assign_adherence(visits_per_year):
        if visits_per_year >= 3:
            return "High"
        elif visits_per_year >= 1:
            return "Medium"
        else:
            return "Low"

    patient_data["adherence_flag"] = patient_data["visits_per_year"].apply(assign_adherence)

    # Summary print
    print("[adherence_logic] Adherence Distribution:")
    print(patient_data["adherence_flag"].value_counts())
    print(f"\nAverage visits/year by segment:")
    print(patient_data.groupby("adherence_flag")["visits_per_year"].mean().round(2))

    return patient_data


if __name__ == "__main__":
    df = load_raw_data()
    result = flag_adherence(df)
    print(result.head(10))
