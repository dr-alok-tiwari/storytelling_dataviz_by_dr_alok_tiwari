"""Deterministic synthetic datasets used across the course.

Each generator owns its random seed and is cached independently. This ensures a
chart, model answer, and downloadable dataset remain consistent across Streamlit
reruns and across students using the same application version.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st


def _rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


@st.cache_data(show_spinner=False)
def retail_sales(seed: int = 101) -> pd.DataFrame:
    """Return a two-year retail series with an intentional teaching narrative.

    Year 1 rises by exactly 50% from January to December and peaks in
    November, matching the action-title exercises used in Sessions 1 and 8.
    """
    rng = _rng(seed)
    months = pd.date_range("2023-01-01", periods=24, freq="MS")
    revenue = np.array(
        [
            110.0, 116.0, 123.0, 129.0, 136.0, 142.0,
            148.0, 153.0, 158.0, 164.0, 172.0, 165.0,
            121.0, 128.0, 135.0, 142.0, 150.0, 157.0,
            163.0, 169.0, 175.0, 181.0, 190.0, 184.0,
        ]
    )
    return pd.DataFrame(
        {
            "month": months,
            "revenue_lakhs": revenue,
            "units_sold": (revenue * 4.2 + rng.normal(0, 12, 24)).astype(int).clip(300),
            "region": rng.choice(["North", "South", "East", "West"], 24),
        }
    )


@st.cache_data(show_spinner=False)
def regional_sales(seed: int = 18) -> pd.DataFrame:
    rng = _rng(seed)
    regions = ["North", "South", "East", "West", "Central"]
    categories = ["Electronics", "Apparel", "FMCG", "Furniture", "Sports"]
    rows: list[dict[str, object]] = []
    for region in regions:
        for category in categories:
            rows.append(
                {
                    "region": region,
                    "category": category,
                    "sales": int(rng.integers(40, 200)),
                    "target": int(rng.integers(80, 180)),
                    "growth_pct": round(float(rng.uniform(-15, 35)), 1),
                }
            )
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def marketing_campaign() -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "channel": ["Email", "Social", "SEO", "PPC", "Influencer", "Print", "TV"],
            "spend_lakhs": [12, 18, 8, 22, 15, 30, 45],
            "leads": [340, 620, 290, 780, 410, 180, 520],
            "conversions": [68, 112, 58, 134, 82, 24, 63],
            "revenue_lakhs": [34, 56, 29, 67, 41, 12, 31],
        }
    )
    df["cpl"] = (df["spend_lakhs"] * 100_000 / df["leads"]).round(0)
    df["roi"] = (
        (df["revenue_lakhs"] - df["spend_lakhs"]) / df["spend_lakhs"] * 100
    ).round(1)
    return df


@st.cache_data(show_spinner=False)
def customer_satisfaction(seed: int = 303) -> pd.DataFrame:
    rng = _rng(seed)
    n = 400
    departments = rng.choice(["Sales", "Support", "Delivery", "Billing", "Returns"], n)
    means = {"Sales": 7.8, "Support": 6.4, "Delivery": 7.2, "Billing": 5.9, "Returns": 6.8}
    scores = [
        round(float(np.clip(rng.normal(means[department], 1.2), 1, 10)), 1)
        for department in departments
    ]
    return pd.DataFrame(
        {
            "department": departments,
            "nps_score": scores,
            "wait_minutes": (rng.exponential(5, n) + 1).round(1).clip(1, 60),
        }
    )


@st.cache_data(show_spinner=False)
def operations_delays(seed: int = 404) -> pd.DataFrame:
    rng = _rng(seed)
    dates = pd.date_range("2023-01-01", periods=52, freq="W")
    base_delay = 4 + rng.normal(0, 1, 52)
    trend = np.linspace(0, -1.5, 52)
    return pd.DataFrame(
        {
            "week": dates,
            "avg_delay_hrs": (base_delay + trend).clip(1).round(2),
            "shipments": rng.integers(200, 600, 52),
            "on_time_pct": (rng.beta(8, 2, 52) * 100).round(1),
        }
    )


@st.cache_data(show_spinner=False)
def financial_expenses(seed: int = 505) -> pd.DataFrame:
    rng = _rng(seed)
    quarters = ["Q1-22", "Q2-22", "Q3-22", "Q4-22", "Q1-23", "Q2-23", "Q3-23", "Q4-23"]
    base = {
        "Salaries": 120,
        "Marketing": 45,
        "Logistics": 38,
        "Technology": 28,
        "Admin": 22,
        "R&D": 18,
    }
    rows: list[dict[str, object]] = []
    for index, quarter in enumerate(quarters):
        for category, amount in base.items():
            growth = 1 + (index * 0.015) + rng.uniform(-0.05, 0.05)
            rows.append(
                {
                    "quarter": quarter,
                    "category": category,
                    "amount_lakhs": round(amount * growth, 1),
                }
            )
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def healthcare_patient_flow(seed: int = 606) -> pd.DataFrame:
    rng = _rng(seed)
    n = 300
    probabilities = np.array(
        [
            0.01,
            0.01,
            0.01,
            0.01,
            0.01,
            0.02,
            0.04,
            0.07,
            0.09,
            0.08,
            0.07,
            0.06,
            0.06,
            0.06,
            0.06,
            0.07,
            0.07,
            0.06,
            0.05,
            0.04,
            0.04,
            0.03,
            0.02,
            0.01,
        ]
    )
    hours = rng.choice(range(24), n, p=probabilities)
    departments = rng.choice(
        ["Emergency", "OPD", "ICU", "Surgery", "Radiology"],
        n,
        p=[0.35, 0.30, 0.12, 0.13, 0.10],
    )
    wait = np.where(
        departments == "Emergency",
        rng.exponential(20, n).clip(5, 120),
        rng.exponential(35, n).clip(5, 180),
    )
    return pd.DataFrame(
        {
            "hour": hours,
            "department": departments,
            "wait_minutes": wait.round(1),
            "severity": rng.choice(
                ["Low", "Medium", "High", "Critical"],
                n,
                p=[0.4, 0.35, 0.18, 0.07],
            ),
        }
    )


@st.cache_data(show_spinner=False)
def bed_occupancy(seed: int = 707) -> pd.DataFrame:
    rng = _rng(seed)
    dates = pd.date_range("2023-01-01", periods=90)
    wards = ["General", "ICU", "Maternity", "Paediatrics", "Ortho"]
    capacity = {"General": 120, "ICU": 24, "Maternity": 40, "Paediatrics": 35, "Ortho": 50}
    rows: list[dict[str, object]] = []
    for date in dates:
        for ward in wards:
            sampled_pct = float(np.clip(rng.beta(7, 2) * 100, 40, 100))
            occupied = min(capacity[ward], int(round(capacity[ward] * sampled_pct / 100)))
            actual_pct = occupied / capacity[ward] * 100
            rows.append(
                {
                    "date": date,
                    "ward": ward,
                    "capacity": capacity[ward],
                    "occupied": occupied,
                    "occupancy_pct": round(actual_pct, 1),
                }
            )
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def time_series_revenue(seed: int = 808) -> pd.DataFrame:
    rng = _rng(seed)
    dates = pd.date_range("2020-01-01", periods=48, freq="MS")
    trend = np.linspace(100, 180, 48)
    seasonal = 20 * np.sin(np.linspace(0, 8 * np.pi, 48))
    noise = rng.normal(0, 6, 48)
    covid_dip = np.where((dates >= "2020-03-01") & (dates <= "2021-03-01"), -25, 0)
    revenue = (trend + seasonal + noise + covid_dip).clip(40)
    df = pd.DataFrame({"month": dates, "revenue": revenue.round(1)})
    df["yoy_growth"] = (df["revenue"].pct_change(12) * 100).round(1)
    return df


@st.cache_data(show_spinner=False)
def student_performance(seed: int = 909) -> pd.DataFrame:
    rng = _rng(seed)
    n = 120
    quiz = rng.integers(35, 100, n)
    project = rng.integers(40, 100, n)
    attendance = rng.uniform(55, 100, n).round(1)
    weighted_score = 0.35 * quiz + 0.45 * project + 0.20 * attendance
    grades = pd.cut(
        weighted_score,
        bins=[-np.inf, 59.99, 69.99, 79.99, np.inf],
        labels=["D", "C", "B", "A"],
    ).astype(str)
    return pd.DataFrame(
        {
            "student_id": range(1, n + 1),
            "program": rng.choice(["BDA", "HCM", "Finance", "Marketing", "Operations"], n),
            "quiz_score": quiz,
            "project_score": project,
            "attendance_pct": attendance,
            "final_grade": grades,
        }
    )


@st.cache_data(show_spinner=False)
def scatter_sales_spend(seed: int = 1001) -> pd.DataFrame:
    rng = _rng(seed)
    n = 80
    spend = rng.uniform(5, 100, n)
    revenue = 3.2 * spend + rng.normal(0, 15, n) + 20
    return pd.DataFrame(
        {
            "marketing_spend": spend.round(1),
            "revenue": revenue.clip(10).round(1),
            "channel": rng.choice(["Online", "Offline", "Both"], n),
        }
    )


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
    """Return a defensive copy of a named synthetic dataset."""
    if name not in DATASETS:
        raise KeyError(f"Unknown dataset: {name}")
    return DATASETS[name]().copy(deep=True)
