# Patient-Centric Launch Analytics & Therapeutic Area Dashboard

## Project Purpose
Analyze longitudinal patient records to support a biopharmaceutical product launch.
Key metrics: Patient Adherence, Treatment Duration, and Therapeutic Area (TA) Concentration.

## Repository Structure

```
patient_launch_analytics/
│
├── data/
│   └── diagnoses.csv               ← Raw patient records (100k patients, 15 conditions)
│
├── data_ingestion/
│   └── load_data.py                ← Loads and does basic cleaning of raw CSV
│
├── core_analytics/
│   ├── patient_processor.py        ← Calculates Treatment Duration per patient
│   ├── market_metrics.py           ← Aggregates Patient Volume per Condition
│   └── adherence_logic.py          ← Flags High vs Low Medication Adherence
│
├── powerbi_exports/
│   ├── ta_summary_export.csv       ← TA concentration table for Power BI
│   ├── adherence_export.csv        ← Adherence flags per patient for Power BI
│   └── duration_export.csv         ← Treatment duration per patient for Power BI
│
├── run_pipeline.py                 ← Master script: runs everything end to end
└── README.md
```

## How to Run

```bash
# Install dependencies
pip install pandas numpy

# Run the full pipeline
python run_pipeline.py
```

## Dataset
Source: [Kaggle - Patient Records 100k Patients 15 Conditions](https://www.kaggle.com/datasets/sergionefedov/patient-records-100k-patients-15-conditions)

## Key Outputs
- `powerbi_exports/ta_summary_export.csv` — Market share by condition
- `powerbi_exports/adherence_export.csv` — Adherence flags per patient
- `powerbi_exports/duration_export.csv` — Treatment duration per patient


## 📊 Pipeline Results ( data — 274,592 records, 100K patients)

**Treatment Duration:**  63K patients are Long-Term (365+ days), showing a heavily chronic population — ideal for launch targeting.

**Market Metrics — Top 5 by Patient Volume:**

| Condition | Unique Patients | Visit Share |
|---|---|---|
| Hypertension | 39,702 | 22.0% |
| Obesity | 34,725 | 19.1% |
| Hyperlipidemia | 31,018 | 16.9% |
| Chronic Kidney Disease | 13,991 | 8.9% |
| Osteoarthritis | 9,847 | 5.2% |

**Adherence Split:** 35% Low · 35% High · 30% Medium — a nearly even 3-way split, which is analytically interesting.

---

## 🎯 3 Client-Ready Strategic Insights

**Insight 1 — Hypertension + Hyperlipidemia = Your Beachhead Market**
Hypertension (40K patients, 22% of all visits) and Hyperlipidemia (31K patients, 16.9%) together account for nearly 40% of the total patient population. Any cardiovascular drug launch targeting comorbid Hypertension-Hyperlipidemia has an addressable population of ~25K+ overlapping patients already in treatment — the foundation for a strong launch case.

**Insight 2 — Chronic Kidney Disease Is the High-Value Underserved Gap**
CKD has 14K patients but generates a disproportionately high visit volume per patient — signaling disease severity and repeat care needs. With limited approved therapeutic options relative to disease burden, CKD represents the highest unmet need per patient and the strongest clinical differentiation argument for a launch narrative.

**Insight 3 — 35K Low-Adherence Patients Are a Commercial Opportunity, Not a Problem**
The adherence analysis flags 35,239 patients as Low (< 1 visit/year). In a launch context, this is your switch + re-engagement cohort. A drug with better tolerability or a simpler dosing profile can be positioned directly against this gap — quantified as 35% of the total patient base showing evidence of treatment dropout.

----