"""Runtime corrections and lightweight chart helpers.

This module keeps the original teaching modules stable while applying small,
process-wide corrections during application startup. It also replaces Plotly's
statsmodels-backed OLS option with an equivalent NumPy line fit, avoiding a large
scientific dependency for a handful of simple teaching charts.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules import tools
from modules.data_generators import regional_sales, time_series_revenue

_ORIGINAL_GET_RECOMMENDATION = tools.get_recommendation
_ORIGINAL_EXAMPLE_FIGURE = tools._example_figure
_ORIGINAL_PX_SCATTER = px.scatter
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


def _data_frame_from_scatter_args(args: tuple[Any, ...], kwargs: dict[str, Any]) -> pd.DataFrame | None:
    data_frame = kwargs.get("data_frame")
    if isinstance(data_frame, pd.DataFrame):
        return data_frame
    if args and isinstance(args[0], pd.DataFrame):
        return args[0]
    return None


def _scatter_with_numpy_ols(*args: Any, **kwargs: Any) -> go.Figure:
    """Render ``trendline='ols'`` with NumPy instead of statsmodels.

    The application uses OLS only for simple linear teaching examples with named
    numeric columns. All other Plotly Express scatter behaviour is delegated to
    the original implementation unchanged.
    """

    if kwargs.get("trendline") != "ols":
        return _ORIGINAL_PX_SCATTER(*args, **kwargs)

    scatter_kwargs = dict(kwargs)
    scatter_kwargs.pop("trendline", None)
    scatter_kwargs.pop("trendline_options", None)
    scatter_kwargs.pop("trendline_scope", None)
    requested_line_color = scatter_kwargs.pop("trendline_color_override", None)

    figure = _ORIGINAL_PX_SCATTER(*args, **scatter_kwargs)
    data_frame = _data_frame_from_scatter_args(args, kwargs)
    x_name = kwargs.get("x")
    y_name = kwargs.get("y")
    color_name = kwargs.get("color")

    if (
        data_frame is None
        or not isinstance(x_name, str)
        or not isinstance(y_name, str)
        or x_name not in data_frame.columns
        or y_name not in data_frame.columns
    ):
        return figure

    marker_colors: dict[str, Any] = {}
    for trace in figure.data:
        trace_name = str(getattr(trace, "name", ""))
        marker = getattr(trace, "marker", None)
        marker_color = getattr(marker, "color", None) if marker is not None else None
        if trace_name and marker_color is not None:
            marker_colors[trace_name] = marker_color

    if isinstance(color_name, str) and color_name in data_frame.columns:
        groups = data_frame.groupby(color_name, sort=False, dropna=False, observed=True)
    else:
        groups = [(None, data_frame)]

    for group_name, group in groups:
        numeric = group[[x_name, y_name]].apply(pd.to_numeric, errors="coerce").dropna()
        if len(numeric) < 2 or numeric[x_name].nunique() < 2:
            continue

        slope, intercept = np.polyfit(numeric[x_name].to_numpy(), numeric[y_name].to_numpy(), 1)
        x_line = np.array([numeric[x_name].min(), numeric[x_name].max()], dtype=float)
        y_line = slope * x_line + intercept

        group_label = None if group_name is None else str(group_name)
        line_color = requested_line_color or marker_colors.get(group_label or "")
        line_style: dict[str, Any] = {"width": 2.2, "dash": "dash"}
        if line_color is not None:
            line_style["color"] = line_color

        figure.add_trace(
            go.Scatter(
                x=x_line,
                y=y_line,
                mode="lines",
                name="Linear trend" if group_label is None else f"{group_label} trend",
                legendgroup=group_label,
                showlegend=False,
                hovertemplate="Linear trend<extra></extra>",
                line=line_style,
            )
        )

    return figure


def install() -> None:
    """Install chart corrections once per Python process."""
    global _INSTALLED
    if _INSTALLED:
        return
    tools.get_recommendation = _get_recommendation
    tools._example_figure = _example_figure
    px.scatter = _scatter_with_numpy_ols
    _INSTALLED = True
