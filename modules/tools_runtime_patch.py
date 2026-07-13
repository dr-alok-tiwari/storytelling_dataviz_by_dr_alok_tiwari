"""Small runtime corrections for legacy chart-engine example rendering.

The main tools module remains stable for the other teaching utilities. This layer
ensures that every chart recommendation is illustrated by the same chart family
that is named in the recommendation.
"""

from __future__ import annotations

from dataclasses import replace

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules import tools
from modules.data_generators import regional_sales, time_series_revenue

_ORIGINAL_GET_RECOMMENDATION = tools.get_recommendation
_ORIGINAL_EXAMPLE_FIGURE = tools._example_figure
_INSTALLED = False


def _get_recommendation(data_type: str, question: str, audience: str, category_count: int = 5):
    recommendation = _ORIGINAL_GET_RECOMMENDATION(data_type, question, audience, category_count)
    if data_type.lower() == "geospatial" and recommendation.primary == "Choropleth map":
        return replace(
            recommendation,
            primary="Proportional-symbol map",
            alternatives=("Choropleth map for regional rates", "Ranked bar chart alongside the map"),
        )
    return recommendation


def _example_figure(recommendation, data_type: str, question: str) -> go.Figure:
    primary = recommendation.primary

    if primary == "Calendar or period heat map":
        df = time_series_revenue().copy()
        df["year"] = df["month"].dt.year
        df["month_name"] = df["month"].dt.strftime("%b")
        month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        matrix = df.pivot(index="year", columns="month_name", values="revenue").reindex(columns=month_order)
        figure = px.imshow(
            matrix,
            text_auto=".0f",
            aspect="auto",
            color_continuous_scale="Blues",
            labels={"x": "Month", "y": "Year", "color": "Revenue"},
        )
        figure.update_layout(title="Revenue concentration by month and year")

    elif primary == "Grouped or faceted bar chart":
        df = regional_sales().groupby(["region", "category"], as_index=False)["sales"].sum()
        leading_categories = df.groupby("category")["sales"].sum().nlargest(3).index.tolist()
        figure = px.bar(
            df[df["category"].isin(leading_categories)],
            x="region",
            y="sales",
            color="category",
            barmode="group",
        )
        figure.update_layout(title="Top product categories compared within each region")

    elif primary == "Adjacency matrix":
        labels = ["Website", "Store", "Cart", "Purchase", "Exit"]
        matrix = np.array(
            [
                [0, 0, 60, 0, 40],
                [0, 0, 35, 0, 15],
                [0, 0, 0, 55, 40],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ]
        )
        figure = px.imshow(
            pd.DataFrame(matrix, index=labels, columns=labels),
            text_auto=True,
            color_continuous_scale="Blues",
            labels={"x": "Destination", "y": "Source", "color": "Flow"},
        )
        figure.update_layout(title="Customer-journey adjacency matrix")

    else:
        return _ORIGINAL_EXAMPLE_FIGURE(recommendation, data_type, question)

    figure.update_layout(height=420, margin={"t": 60, "r": 25, "b": 45, "l": 55})
    return figure


def install() -> None:
    """Install chart-engine corrections once per Python process."""
    global _INSTALLED
    if _INSTALLED:
        return
    tools.get_recommendation = _get_recommendation
    tools._example_figure = _example_figure
    _INSTALLED = True
