import numpy as np
import pandas as pd

from modules.data_generators import (
    bed_occupancy,
    get_dataset,
    marketing_campaign,
    retail_sales,
    student_performance,
    time_series_revenue,
)


def test_generators_are_deterministic():
    pd.testing.assert_frame_equal(retail_sales(), retail_sales())
    pd.testing.assert_frame_equal(get_dataset("Retail Sales (Time Series)"), retail_sales())


def test_yoy_growth_is_twelve_month_percentage_change():
    df = time_series_revenue()
    expected = (df["revenue"].pct_change(12) * 100).round(1)
    pd.testing.assert_series_equal(df["yoy_growth"], expected, check_names=False)


def test_bed_occupancy_reconciles_with_capacity():
    df = bed_occupancy()
    calculated = (df["occupied"] / df["capacity"] * 100).round(1)
    assert np.allclose(calculated, df["occupancy_pct"])
    assert (df["occupied"] <= df["capacity"]).all()


def test_cost_per_lead_is_in_rupees():
    df = marketing_campaign()
    expected = (df["spend_lakhs"] * 100_000 / df["leads"]).round(0)
    pd.testing.assert_series_equal(df["cpl"], expected, check_names=False)


def test_student_grade_is_derived_from_scores():
    df = student_performance()
    weighted = 0.35 * df["quiz_score"] + 0.45 * df["project_score"] + 0.20 * df["attendance_pct"]
    expected = pd.cut(
        weighted,
        bins=[-np.inf, 59.99, 69.99, 79.99, np.inf],
        labels=["D", "C", "B", "A"],
    ).astype(str)
    pd.testing.assert_series_equal(df["final_grade"], expected, check_names=False)
