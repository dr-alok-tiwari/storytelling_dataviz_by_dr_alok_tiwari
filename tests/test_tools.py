import plotly.express as px

from modules.data_generators import scatter_sales_spend
from modules.tools import get_recommendation


def test_recommendation_engine_covers_all_inputs():
    data_types = ["Categorical", "Numerical", "Time series", "Geospatial", "Relational", "Hierarchical"]
    questions = ["Compare", "Rank", "Show trend", "Show distribution", "Show relationship", "Show composition", "Show deviation"]
    audiences = ["Executive", "Analyst", "Operations manager", "Healthcare manager", "Customer / public"]

    for data_type in data_types:
        for question in questions:
            for audience in audiences:
                recommendation = get_recommendation(data_type, question, audience, category_count=7)
                assert recommendation.primary
                assert recommendation.alternatives
                assert recommendation.rationale
                assert recommendation.avoid


def test_many_category_composition_does_not_recommend_pie():
    recommendation = get_recommendation("Categorical", "Show composition", "Executive", category_count=12)
    assert "pie" not in recommendation.primary.lower()


def test_plotly_ols_trendline_dependency_is_available():
    frame = scatter_sales_spend()
    figure = px.scatter(
        frame,
        x="marketing_spend",
        y="revenue",
        color="channel",
        trendline="ols",
    )
    assert figure.data
