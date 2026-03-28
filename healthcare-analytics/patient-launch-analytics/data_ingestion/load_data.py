"""
data_ingestion/load_data.py
----------------------------
Loads the raw diagnoses CSV and does basic cleaning.
This is the first step in the pipeline — everything else reads from here.
"""

import pandas as pd

def load_raw_data(filepath=None):
    if filepath is None:
        import os
        filepath = os.path.join(os.path.dirname(__file__), "C:\\Users\\srinithya\\Desktop\\NITHYA\\Data Analysis Project\\Srinithya\\individual git projects\\Exploratory Data Analysis\\patient_launch_analytics\\data\\diagnoses.csv")
    # Read the CSV file
    df = pd.read_csv(filepath)

    # Convert visit_date to a proper date column
    df["visit_date"] = pd.to_datetime(df["visit_date"])

    # Drop rows where patient_id or visit_date is missing
    df = df.dropna(subset=["patient_id", "visit_date"])

    # Strip whitespace from text columns just in case
    df["primary_diagnosis"] = df["primary_diagnosis"].str.strip()

    print(f"[load_data] Loaded {len(df):,} records | {df['patient_id'].nunique():,} unique patients")
    return df


# Quick test — run this file directly to confirm data loads OK
if __name__ == "__main__":
    data = load_raw_data()
    print(data.head())
    print(data.dtypes)
