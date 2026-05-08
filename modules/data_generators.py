"""
data_generators.py
Synthetic but realistic datasets for all course modules.
No external files required — everything is generated in memory.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)


def retail_sales():
    months = pd.date_range("2023-01-01", periods=24, freq="MS")
    base = 120 + np.linspace(0, 40, 24)
    seasonal = 15 * np.sin(np.linspace(0, 4 * np.pi, 24))
    noise = rng.normal(0, 5, 24)
    sales = (base + seasonal + noise).clip(80)
    return pd.DataFrame({
        "month": months,
        "revenue_lakhs": sales.round(1),
        "units_sold": (sales * 4.2 + rng.normal(0, 20, 24)).astype(int).clip(300),
        "region": rng.choice(["North", "South", "East", "West"], 24)
    })


def regional_sales():
    regions = ["North", "South", "East", "West", "Central"]
    categories = ["Electronics", "Apparel", "FMCG", "Furniture", "Sports"]
    rows = []
    for r in regions:
        for c in categories:
            rows.append({
                "region": r,
                "category": c,
                "sales": int(rng.integers(40, 200)),
                "target": int(rng.integers(80, 180)),
                "growth_pct": round(float(rng.uniform(-15, 35)), 1)
            })
    return pd.DataFrame(rows)


def marketing_campaign():
    campaigns = ["Email", "Social", "SEO", "PPC", "Influencer", "Print", "TV"]
    df = pd.DataFrame({
        "channel": campaigns,
        "spend_lakhs": [12, 18, 8, 22, 15, 30, 45],
        "leads": [340, 620, 290, 780, 410, 180, 520],
        "conversions": [68, 112, 58, 134, 82, 24, 63],
        "revenue_lakhs": [34, 56, 29, 67, 41, 12, 31],
    })
    df["cpl"] = (df["spend_lakhs"] * 100 / df["leads"]).round(2)
    df["roi"] = ((df["revenue_lakhs"] - df["spend_lakhs"]) / df["spend_lakhs"] * 100).round(1)
    return df


def customer_satisfaction():
    n = 400
    departments = rng.choice(["Sales", "Support", "Delivery", "Billing", "Returns"], n)
    scores = []
    means = {"Sales": 7.8, "Support": 6.4, "Delivery": 7.2, "Billing": 5.9, "Returns": 6.8}
    for d in departments:
        scores.append(round(float(np.clip(rng.normal(means[d], 1.2), 1, 10)), 1))
    return pd.DataFrame({"department": departments, "nps_score": scores,
                         "wait_minutes": (rng.exponential(5, n) + 1).round(1).clip(1, 60)})


def operations_delays():
    dates = pd.date_range("2023-01-01", periods=52, freq="W")
    base_delay = 4 + rng.normal(0, 1, 52)
    trend = np.linspace(0, -1.5, 52)
    df = pd.DataFrame({
        "week": dates,
        "avg_delay_hrs": (base_delay + trend).clip(1).round(2),
        "shipments": rng.integers(200, 600, 52),
        "on_time_pct": (rng.beta(8, 2, 52) * 100).round(1)
    })
    return df


def financial_expenses():
    quarters = ["Q1-22", "Q2-22", "Q3-22", "Q4-22", "Q1-23", "Q2-23", "Q3-23", "Q4-23"]
    categories = ["Salaries", "Marketing", "Logistics", "Technology", "Admin", "R&D"]
    rows = []
    base = {"Salaries": 120, "Marketing": 45, "Logistics": 38, "Technology": 28, "Admin": 22, "R&D": 18}
    for i, q in enumerate(quarters):
        for cat, b in base.items():
            growth = 1 + (i * 0.015) + rng.uniform(-0.05, 0.05)
            rows.append({"quarter": q, "category": cat, "amount_lakhs": round(b * growth, 1)})
    return pd.DataFrame(rows)


def healthcare_patient_flow():
    n = 300
    hours = rng.choice(range(24), n, p=np.array([
        0.01, 0.01, 0.01, 0.01, 0.01, 0.02, 0.04, 0.07, 0.09,
        0.08, 0.07, 0.06, 0.06, 0.06, 0.06, 0.07, 0.07, 0.06,
        0.05, 0.04, 0.04, 0.03, 0.02, 0.01
    ]))
    departments = rng.choice(["Emergency", "OPD", "ICU", "Surgery", "Radiology"], n,
                              p=[0.35, 0.30, 0.12, 0.13, 0.10])
    wait = np.where(departments == "Emergency",
                    rng.exponential(20, n).clip(5, 120),
                    rng.exponential(35, n).clip(5, 180))
    return pd.DataFrame({"hour": hours, "department": departments,
                         "wait_minutes": wait.round(1),
                         "severity": rng.choice(["Low", "Medium", "High", "Critical"], n,
                                                  p=[0.4, 0.35, 0.18, 0.07])})


def bed_occupancy():
    dates = pd.date_range("2023-01-01", periods=90)
    wards = ["General", "ICU", "Maternity", "Paediatrics", "Ortho"]
    cap = {"General": 120, "ICU": 24, "Maternity": 40, "Paediatrics": 35, "Ortho": 50}
    rows = []
    for d in dates:
        for w in wards:
            occ_pct = np.clip(rng.beta(7, 2) * 100, 40, 100)
            rows.append({"date": d, "ward": w, "capacity": cap[w],
                         "occupied": int(cap[w] * occ_pct / 100),
                         "occupancy_pct": round(occ_pct, 1)})
    return pd.DataFrame(rows)


def time_series_revenue():
    dates = pd.date_range("2020-01-01", periods=48, freq="MS")
    trend = np.linspace(100, 180, 48)
    seasonal = 20 * np.sin(np.linspace(0, 8 * np.pi, 48))
    noise = rng.normal(0, 6, 48)
    covid_dip = np.where((dates >= "2020-03-01") & (dates <= "2021-03-01"), -25, 0)
    revenue = (trend + seasonal + noise + covid_dip).clip(40)
    return pd.DataFrame({"month": dates, "revenue": revenue.round(1),
                         "yoy_growth": np.concatenate([[np.nan] * 12,
                                                        np.diff(revenue.reshape(-1, 12).mean(1)).repeat(12)])})


def student_performance():
    n = 120
    programs = rng.choice(["BDA", "HCM", "Finance", "Marketing", "Operations"], n)
    return pd.DataFrame({
        "student_id": range(1, n + 1),
        "program": programs,
        "quiz_score": rng.integers(35, 100, n),
        "project_score": rng.integers(40, 100, n),
        "attendance_pct": rng.uniform(55, 100, n).round(1),
        "final_grade": rng.choice(["A", "B", "C", "D"], n, p=[0.25, 0.40, 0.25, 0.10])
    })


def scatter_sales_spend():
    n = 80
    spend = rng.uniform(5, 100, n)
    revenue = 3.2 * spend + rng.normal(0, 15, n) + 20
    return pd.DataFrame({
        "marketing_spend": spend.round(1),
        "revenue": revenue.clip(10).round(1),
        "channel": rng.choice(["Online", "Offline", "Both"], n)
    })


DATASETS = {
    "Retail Sales (Time Series)": retail_sales,
    "Regional Sales Performance": regional_sales,
    "Marketing Campaign ROI": marketing_campaign,
    "Customer Satisfaction": customer_satisfaction,
    "Operations Delays": operations_delays,
    "Financial Expenses": financial_expenses,
    "Healthcare Patient Flow": healthcare_patient_flow,
    "Hospital Bed Occupancy": bed_occupancy,
    "Revenue Trend (Multi-year)": time_series_revenue,
    "Student Performance": student_performance,
    "Marketing Spend vs Revenue": scatter_sales_spend,
}


def get_dataset(name: str) -> pd.DataFrame:
    return DATASETS[name]()
