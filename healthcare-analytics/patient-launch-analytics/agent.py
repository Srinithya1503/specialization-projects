import pandas as pd

# =========================
# LOAD DATA (STRICT SCHEMA)
# =========================
def load_data():
    ta = pd.read_csv("powerbi_exports/ta_summary_export.csv")

    adherence = pd.read_csv("powerbi_exports/adherence_export.csv")
    duration = pd.read_csv("powerbi_exports/duration_export.csv")

    return ta, adherence, duration


# =========================
# METRICS ENGINE (NO TRUST)
# =========================
def compute_metrics(ta, adherence, duration):

    # -------- THERAPEUTIC AREA --------
    total_patients = ta["unique_patients"].sum()

    ta["calc_patient_pct"] = (ta["unique_patients"] / total_patients) * 100

    top3 = ta.sort_values("unique_patients", ascending=False).head(3)
    top3_share = (top3["unique_patients"].sum() / total_patients) * 100

    hypertension_pct = ta.loc[
        ta["condition"] == "hypertension", "calc_patient_pct"
    ].values[0]

    # -------- ADHERENCE --------
    adh_counts = adherence["adherence_flag"].value_counts().reset_index()
    adh_counts.columns = ["category", "patients"]

    total_adh = adh_counts["patients"].sum()
    adh_counts["pct"] = (adh_counts["patients"] / total_adh) * 100

    low = adh_counts.loc[adh_counts["category"] == "Low", "pct"].values[0]
    high = adh_counts.loc[adh_counts["category"] == "High", "pct"].values[0]
    medium = adh_counts.loc[adh_counts["category"] == "Medium", "pct"].values[0]

    adh_delta = abs(low - high)
    adh_ratio = max(low, high) / min(low, high)

    # -------- DURATION --------
    dur_counts = duration["duration_segment"].value_counts().reset_index()
    dur_counts.columns = ["category", "patients"]

    total_dur = dur_counts["patients"].sum()
    dur_counts["pct"] = (dur_counts["patients"] / total_dur) * 100

    long = dur_counts.loc[dur_counts["category"] == "Long-Term", "pct"].values[0]
    short = dur_counts.loc[dur_counts["category"] == "Short-Term", "pct"].values[0]

    dur_delta = long - short
    dur_ratio = long / short if short != 0 else 0

    return {
        "total_patients": total_patients,
        "ta": ta,
        "top3_share": top3_share,
        "hypertension_pct": hypertension_pct,
        "adh": adh_counts,
        "dur": dur_counts,
        "low": low,
        "high": high,
        "medium": medium,
        "adh_delta": adh_delta,
        "adh_ratio": adh_ratio,
        "long": long,
        "short": short,
        "dur_delta": dur_delta,
        "dur_ratio": dur_ratio
    }


# =========================
# VALIDATION LAYER (STRICT)
# =========================
def validate(m):

    ta_sum = m["ta"]["calc_patient_pct"].sum()
    adh_sum = m["adh"]["pct"].sum()
    dur_sum = m["dur"]["pct"].sum()

    assert 99 <= ta_sum <= 101, f"TA % ERROR: {ta_sum}"
    assert 99 <= adh_sum <= 101, f"Adherence % ERROR: {adh_sum}"
    assert 99 <= dur_sum <= 101, f"Duration % ERROR: {dur_sum}"

    assert m["top3_share"] <= 100, "Top3 share invalid"

    print("✅ VALIDATION PASSED")


# =========================
# INSIGHT ENGINE (NUMERIC)
# =========================
def generate_insights(m):

    insights = f"""
KEY NUMERIC INSIGHTS

1. Market Concentration
   - Top 3 TA Share: {m['top3_share']:.2f}%
   - Hypertension Share: {m['hypertension_pct']:.2f}%
   - Contribution Ratio: {m['top3_share']/m['hypertension_pct']:.2f}x

2. Adherence Balance
   - Low: {m['low']:.2f}%
   - High: {m['high']:.2f}%
   - Medium: {m['medium']:.2f}%
   - Delta (Low vs High): {m['adh_delta']:.2f}%
   - Ratio: {m['adh_ratio']:.2f}x

3. Duration Strength
   - Long-Term: {m['long']:.2f}%
   - Short-Term: {m['short']:.2f}%
   - Delta: {m['dur_delta']:.2f}%
   - Ratio: {m['dur_ratio']:.2f}x
"""

    return insights


# =========================
# STRATEGY ENGINE
# =========================
def generate_strategy(m):

    strategy = f"""
PRIORITIZED STRATEGY

PRIMARY:
→ Hypertension + Long-Term + Low Adherence
→ Reason:
   - Largest TA ({m['hypertension_pct']:.2f}%)
   - Strong LTV ({m['long']:.2f}% long-term)
   - Conversion pool ({m['low']:.2f}% low adherence)

SECONDARY:
→ Top 3 TA + High Adherence
→ Reason:
   - Scale ({m['top3_share']:.2f}%)
   - Retention base ({m['high']:.2f}%)

TERTIARY:
→ Short-Term Patients
→ Reason:
   - Conversion into long-term ({m['short']:.2f}% base)
"""

    return strategy


# =========================
# KPI LAYER
# =========================
def generate_kpis(m):

    return f"""
KPI FRAMEWORK

MARKET:
- Total Patients: {m['total_patients']}
- Hypertension Share: {m['hypertension_pct']:.2f}%
- Top 3 TA Share: {m['top3_share']:.2f}%

ADHERENCE:
- Low: {m['low']:.2f}%
- Medium: {m['medium']:.2f}%
- High: {m['high']:.2f}%
- Delta: {m['adh_delta']:.2f}%
- Ratio: {m['adh_ratio']:.2f}x

DURATION:
- Long-Term: {m['long']:.2f}%
- Short-Term: {m['short']:.2f}%
- Delta: {m['dur_delta']:.2f}%
- Ratio: {m['dur_ratio']:.2f}x

COMMERCIAL:
- Switch Opportunity = Low Adherence
- Retention Driver = Long-Term
- Growth Focus = Top 3 TA
"""


# =========================
# FINAL REPORT
# =========================
def generate_report(m):

    return f"""
🚀 FINAL EXECUTIVE REPORT (AUDIT SAFE)

{generate_insights(m)}

{generate_strategy(m)}

{generate_kpis(m)}
"""


# =========================
# RUN
# =========================
def run():
    print("🚀 Running PRODUCTION AGENT...")

    ta, adherence, duration = load_data()

    metrics = compute_metrics(ta, adherence, duration)

    validate(metrics)

    report = generate_report(metrics)

    print(report)


if __name__ == "__main__":
    run()