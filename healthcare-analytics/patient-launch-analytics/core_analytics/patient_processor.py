"""
core_analytics/patient_processor.py
-------------------------------------
Calculates Treatment Duration for each patient.

Logic:
  - Treatment Duration = Last visit date - First visit date (in days)
  - This tells us how long a patient has been in the system / under care
  - Longer duration = more chronic / complex patient
"""

import pandas as pd
import sys
sys.path.append("..")
from data_ingestion.load_data import load_raw_data


def calculate_treatment_duration(df):
    # Group by patient and find their first and last visit
    patient_timeline = df.groupby("patient_id")["visit_date"].agg(
        first_visit="min",
        last_visit="max"
    ).reset_index()

    # Calculate duration in days
    patient_timeline["treatment_duration_days"] = (
        patient_timeline["last_visit"] - patient_timeline["first_visit"]
    ).dt.days

    # Add a simple label: Short (<90 days), Medium (90–365), Long (365+)
    def label_duration(days):
        if days < 90:
            return "Short-Term"
        elif days < 365:
            return "Medium-Term"
        else:
            return "Long-Term"

    patient_timeline["duration_segment"] = patient_timeline["treatment_duration_days"].apply(label_duration)

    print(f"[patient_processor] Treatment duration calculated for {len(patient_timeline):,} patients")
    print(patient_timeline["duration_segment"].value_counts())
    return patient_timeline


if __name__ == "__main__":
    df = load_raw_data()
    result = calculate_treatment_duration(df)
    print(result.head(10))
