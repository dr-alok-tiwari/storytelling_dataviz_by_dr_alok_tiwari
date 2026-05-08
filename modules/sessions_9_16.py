"""
sessions_9_16.py
Teaching content for Sessions 9–16 (Modules 3 & 4).
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from modules.ui_components import (
    callout_insight, callout_manager, callout_mistake, callout_action,
    session_header, reflection_box, PRIMARY, ACCENT, SUCCESS, DANGER, WARNING
)
from modules.data_generators import (
    scatter_sales_spend, time_series_revenue, healthcare_patient_flow,
    bed_occupancy, regional_sales, financial_expenses, marketing_campaign,
    operations_delays, retail_sales
)
from modules.quiz_bank import QUIZ_BANK

rng = np.random.default_rng(13)


def render_quiz(session_num: int):
    qs = [q for q in QUIZ_BANK if q["session"] == session_num]
    if not qs:
        st.info("Quiz questions for this session are in the Quiz Zone.")
        return
    st.markdown(f"### 📝 Session {session_num} Quiz — {len(qs)} Questions")
    for i, q in enumerate(qs):
        with st.container():
            st.markdown(f"---\n**Q{i+1}. `[{q['type']}]` {q['q']}**")
            choice = st.radio(
                "Select your answer:",
                q["options"],
                key=f"quiz_s{session_num}_q{i}",
                index=0,
            )
            col_btn, col_score = st.columns([1, 4])
            with col_btn:
                reveal = st.button("🔍 Reveal Answer", key=f"ans_s{session_num}_q{i}")
            if reveal:
                if choice is None:
                    st.warning("Please select an option first.")
                elif choice == q["answer"]:
                    st.success(f"✅ **Correct!** — {q['explanation']}")
                else:
                    st.error(f"❌ **Correct answer:** {q['answer']}\n\n{q['explanation']}")
    st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION 9
# ══════════════════════════════════════════════════════════════════════════════
def session_9():
    session_header(9)
    tab_c, tab_d, tab_l, tab_q, tab_r = st.tabs(
        ["📖 Concept", "📊 Demo", "🔬 Lab", "❓ Quiz", "🪞 Reflect"])

    with tab_c:
        st.subheader("From Correlation to Insight")
        st.write("""
        Scatter plots reveal relationships between two quantitative variables.
        They are indispensable for hypothesis generation — but dangerous if
        the analyst skips from correlation to causation without business reasoning.
        """)
        callout_mistake("Correlation ≠ Causation. A scatter plot showing a positive relationship between marketing spend and revenue does not prove that spending more will increase revenue — both might be driven by seasonal factors.", "The Causation Trap")
        
        st.subheader("What a Scatter Plot Can Tell You")
        scatter_insights = {
            "Direction": "Positive (both rise), Negative (one rises, other falls), None",
            "Strength": "Tight cluster = strong; loose scatter = weak",
            "Shape": "Linear, curved, step-function",
            "Outliers": "Points far from the cluster — investigate these first",
            "Clusters": "Two separate groups within the data — may need segmentation"
        }
        for key, val in scatter_insights.items():
            st.markdown(f"**{key}:** {val}")

        callout_insight("The most valuable scatter plots in business have a third dimension — color the dots by a categorical variable (e.g., channel, region) to reveal if the relationship holds uniformly or differs by segment.", "Third Dimension")

        st.subheader("Building an Insight from a Scatter Plot")
        steps = [
            "Observe the overall pattern (direction, strength)",
            "Name the outliers — which brands/products/periods?",
            "Check if the pattern holds across sub-groups",
            "Frame a business hypothesis: 'Channels with X tend to show Y'",
            "Recommend investigation or action"
        ]
        for i, step in enumerate(steps, 1):
            st.markdown(f"{i}. {step}")

    with tab_d:
        df = scatter_sales_spend()
        color_var = st.radio("Color by:", ["None", "channel"], horizontal=True, key="s9_color")
        add_trend = st.checkbox("Add trend line", value=True, key="s9_trend")
        fig = px.scatter(df, x="marketing_spend", y="revenue",
                         color="channel" if color_var == "channel" else None,
                         title="Marketing Spend vs Revenue — Positive Association",
                         trendline="ols" if add_trend else None,
                         labels={"marketing_spend": "Marketing Spend (₹L)", "revenue": "Revenue (₹L)"})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        callout_manager("Which channel shows the strongest slope? Which has outliers that could be investigated? These questions drive strategy.", "Managerial Meaning")

        st.subheader("Correlation Matrix Heat Map")
        df2 = marketing_campaign()[["spend_lakhs","leads","conversions","revenue_lakhs","roi"]]
        corr = df2.corr().round(2)
        fig2 = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r",
                         zmin=-1, zmax=1, title="Correlation Matrix — Marketing Metrics")
        fig2.update_layout(height=350)
        st.plotly_chart(fig2, use_container_width=True)
        callout_insight("Dark blue = strong positive correlation. Dark red = strong negative. Explore why strong correlations exist before building strategy on them.", "Reading the Matrix")

    with tab_l:
        st.subheader("Lab: Describe the Relationship")
        df3 = scatter_sales_spend()
        x_var = st.selectbox("X-axis:", ["marketing_spend"], key="s9_x")
        y_var = st.selectbox("Y-axis:", ["revenue"], key="s9_y")
        fig3 = px.scatter(df3, x=x_var, y=y_var, color="channel",
                          trendline="ols", height=350)
        st.plotly_chart(fig3, use_container_width=True)
        st.text_input("Describe the direction and strength of the relationship:", key="s9_lab_obs")
        st.text_input("Name one business hypothesis this relationship suggests:", key="s9_lab_hyp")
        st.text_input("What additional data would you need to test causation?", key="s9_lab_causal")

    with tab_q:
        render_quiz(9)

    with tab_r:
        reflection_box(
            "In your domain, name two variables that are likely correlated but where the relationship is probably explained by a third (confounding) variable. "
            "What experiment would isolate the true causal effect?",
            key="refl_s9"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION 10
# ══════════════════════════════════════════════════════════════════════════════
def session_10():
    session_header(10)
    tab_c, tab_d, tab_l, tab_q, tab_r = st.tabs(
        ["📖 Concept", "📊 Demo", "🔬 Lab", "❓ Quiz", "🪞 Reflect"])

    with tab_c:
        st.subheader("Time Is a Privileged Dimension")
        st.write("""
        Time series visualization is different from other charts because the
        ordering of the x-axis is not arbitrary — it reflects a causal sequence.
        Earlier events can affect later ones. Trends, cycles, and shocks are all
        readable in the same visual if the chart is well-designed.
        """)
        ts_charts = pd.DataFrame({
            "Chart": ["Line chart", "Area chart", "Bar chart (time)", "Slope chart", "Heat map (calendar)"],
            "Best For": [
                "Single or multiple continuous series over time",
                "Volume or cumulative value over time — single series",
                "Monthly/quarterly comparisons, few periods",
                "Before-after change across categories",
                "Patterns within a day/week/year structure"
            ],
            "Key Rule": [
                "Connect the dots only if there are no gaps",
                "Use filled area only for a single series (stacking can mislead)",
                "Do not connect bars with a line unless there is a trend to show",
                "Use for exactly two time points",
                "Ideal for revealing cyclical patterns (e.g., hourly demand)"
            ]
        })
        st.dataframe(ts_charts, use_container_width=True, hide_index=True)
        callout_insight("Annotation is essential in time series. Every anomaly, event, or change in trend should be labeled directly on the chart — not in a footnote.", "Annotation Rule")
        callout_mistake("Irregular time intervals on the x-axis (plotting Jan, March, Sept, Dec as evenly spaced) create a visual acceleration that does not exist in the data.", "Irregular Intervals")

    with tab_d:
        df = time_series_revenue()
        df["month_str"] = df["month"].dt.strftime("%b %Y")
        chart_type = st.radio("Chart type:", ["Line", "Area", "Annotated Line"], horizontal=True, key="s10_ct")
        rolling = st.checkbox("Add 3-month rolling average", key="s10_roll")
        fig = go.Figure()
        if rolling:
            df["rolling"] = df["revenue"].rolling(3).mean()
        if chart_type == "Line":
            fig.add_trace(go.Scatter(x=df["month"], y=df["revenue"], mode="lines",
                                      name="Revenue", line=dict(color=PRIMARY)))
        elif chart_type == "Area":
            fig.add_trace(go.Scatter(x=df["month"], y=df["revenue"], mode="lines",
                                      fill="tozeroy", name="Revenue",
                                      line=dict(color=PRIMARY), fillcolor="rgba(27,79,138,0.15)"))
        else:
            fig.add_trace(go.Scatter(x=df["month"], y=df["revenue"], mode="lines",
                                      name="Revenue", line=dict(color=PRIMARY)))
            fig.add_annotation(x="2020-04-01", y=df[df["month"] == "2020-04-01"]["revenue"].values[0],
                                text="COVID-19\nDisruption", showarrow=True,
                                arrowhead=2, ax=50, ay=-40, font=dict(color=DANGER))
            fig.add_annotation(x="2021-06-01", y=df[df["month"] == "2021-06-01"]["revenue"].values[0],
                                text="Recovery\nBegins", showarrow=True,
                                arrowhead=2, ax=-50, ay=-40, font=dict(color=SUCCESS))
        if rolling and "rolling" in df.columns:
            fig.add_trace(go.Scatter(x=df["month"], y=df["rolling"], mode="lines",
                                      name="3M Rolling Avg", line=dict(color=ACCENT, dash="dash")))
        fig.update_layout(title="Revenue 2020–2023 — Recovery Post-COVID Visible", height=380,
                          xaxis_title="Month", yaxis_title="Revenue (₹L)")
        st.plotly_chart(fig, use_container_width=True)
        callout_manager("The rolling average smooths noise — revealing the underlying trend. Annotation tells the reader WHY the trend broke.", "Managerial Meaning")

    with tab_l:
        st.subheader("Lab: Build Your Time Story")
        df2 = retail_sales()
        df2["month_str"] = df2["month"].dt.strftime("%b %Y")
        show_ma = st.checkbox("Show 3-month moving average", key="s10_lab_ma")
        highlight_max = st.checkbox("Highlight peak month", key="s10_lab_hl")
        if show_ma:
            df2["ma3"] = df2["revenue_lakhs"].rolling(3).mean()
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df2["month"], y=df2["revenue_lakhs"],
                                   mode="lines+markers", name="Revenue",
                                   line=dict(color=PRIMARY, width=2),
                                   marker=dict(size=5)))
        if show_ma:
            fig2.add_trace(go.Scatter(x=df2["month"], y=df2["ma3"],
                                       name="3M MA", line=dict(color=ACCENT, dash="dash")))
        if highlight_max:
            peak_row = df2.loc[df2["revenue_lakhs"].idxmax()]
            fig2.add_annotation(x=peak_row["month"], y=peak_row["revenue_lakhs"],
                                 text=f"Peak: ₹{peak_row['revenue_lakhs']}L",
                                 showarrow=True, arrowhead=2, ax=0, ay=-40,
                                 font=dict(color=DANGER))
        fig2.update_layout(height=340, title="Revenue Trend — Build Your Story",
                            xaxis_title="Month", yaxis_title="Revenue (₹L)")
        st.plotly_chart(fig2, use_container_width=True)
        st.text_input("Write the story title for this chart:", key="s10_lab_title")
        st.text_area("What is the main managerial insight? What action does it suggest?", key="s10_lab_insight", height=70)

    with tab_q:
        render_quiz(10)

    with tab_r:
        reflection_box(
            "Think of a business metric you track regularly. What would its time series reveal that a single monthly report does not? "
            "What event or context annotation would make it more useful?",
            key="refl_s10"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION 11
# ══════════════════════════════════════════════════════════════════════════════
def session_11():
    session_header(11)
    tab_c, tab_d, tab_l, tab_q, tab_r = st.tabs(
        ["📖 Concept", "📊 Demo", "🔬 Lab", "❓ Quiz", "🪞 Reflect"])

    with tab_c:
        st.subheader("What Makes a Dashboard Work?")
        st.write("""
        A dashboard is not a collection of charts — it is a focused information
        environment designed around a specific decision. Everything on the page
        should answer the question: what does the audience need to decide, and
        right now?
        """)
        callout_insight("Design principle: define the primary decision question before choosing a single chart. If you cannot state the decision in one sentence, the dashboard will not have a clear story.", "Decision-First Design")

        principles = {
            "Hierarchy of attention": "Most critical information top-left; supporting detail below",
            "F-pattern reading": "Users scan top-left to right, then down the left — place KPIs there",
            "Signal before noise": "The headline insight should be visible without scrolling",
            "Minimal chrome": "Borders, shadows, gradients are noise unless they encode information",
            "Consistent encoding": "Same chart type for same question across the dashboard",
            "Progressive detail": "Summary → drill-down, not all detail at once"
        }
        for p, desc in principles.items():
            st.markdown(f"**{p}:** {desc}")

        callout_mistake("A dashboard with 20 KPI cards and 12 charts is a data dump dressed as a dashboard. If everything is equally visible, nothing is important.", "Dashboard Overload")
        callout_action("Limit an executive dashboard to 1 headline insight, 3–4 KPIs, and 2–3 supporting charts. Operations dashboards can go deeper, but still need a decision hierarchy.", "Dashboard Sizing Rule")

    with tab_d:
        st.subheader("Sample Executive Dashboard — Sales Performance")
        df = regional_sales()
        df2 = retail_sales()
        total_sales = df["sales"].sum()
        top_region = df.groupby("region")["sales"].sum().idxmax()
        avg_growth = df["growth_pct"].mean()
        target_hit = (df["sales"] >= df["target"]).mean() * 100

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Sales", f"₹{total_sales}L", f"+{avg_growth:.1f}% avg growth")
        col2.metric("Top Region", top_region, "Leads 5 regions")
        col3.metric("Target Achievement", f"{target_hit:.0f}%", "of categories on track")
        col4.metric("Active Categories", "5", "Across all regions")

        col_a, col_b = st.columns([1.4, 1])
        with col_a:
            ts = df2[["month", "revenue_lakhs"]].copy()
            ts["ma3"] = ts["revenue_lakhs"].rolling(3).mean()
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=ts["month"], y=ts["revenue_lakhs"],
                                       mode="lines", name="Revenue",
                                       line=dict(color=PRIMARY, width=2),
                                       fill="tozeroy", fillcolor="rgba(27,79,138,0.1)"))
            fig1.add_trace(go.Scatter(x=ts["month"], y=ts["ma3"],
                                       mode="lines", name="Trend",
                                       line=dict(color=ACCENT, dash="dash", width=1.5)))
            fig1.update_layout(title="Revenue Trending Upward — Momentum Holding",
                                height=280, margin=dict(t=40, b=20),
                                legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig1, use_container_width=True)
        with col_b:
            by_r = df.groupby("region")["sales"].sum().reset_index().sort_values("sales", ascending=True)
            fig2 = go.Figure(go.Bar(x=by_r["sales"], y=by_r["region"], orientation="h",
                                     marker_color=[DANGER if r == top_region else "#BDC3C7"
                                                   for r in by_r["region"]]))
            fig2.update_layout(title="North Leads — Invest Further",
                                height=280, margin=dict(t=40, b=20),
                                xaxis_title="Sales (₹L)")
            st.plotly_chart(fig2, use_container_width=True)

        callout_manager("This dashboard answers one question at a glance: are we on track, and where should we focus? KPIs give the headline; charts provide the supporting evidence.", "Managerial Meaning")

    with tab_l:
        st.subheader("Lab: Design a Healthcare Dashboard")
        st.write("Use the hospital patient flow data to build a ward-level operations dashboard.")
        df3 = bed_occupancy()
        selected_wards = st.multiselect("Select wards:", df3["ward"].unique().tolist(),
                                         default=["General", "ICU"], key="s11_wards")
        sub = df3[df3["ward"].isin(selected_wards)] if selected_wards else df3

        col1, col2 = st.columns(2)
        with col1:
            avg_occ = sub.groupby("ward")["occupancy_pct"].mean().reset_index()
            for _, row in avg_occ.iterrows():
                col1.metric(f"{row['ward']} Avg Occupancy", f"{row['occupancy_pct']:.1f}%",
                             "⚠️ High" if row["occupancy_pct"] > 85 else "Normal")
        with col2:
            recent = sub[sub["date"] >= sub["date"].max() - pd.Timedelta(days=30)]
            trend = recent.groupby(["date", "ward"])["occupancy_pct"].mean().reset_index()
            fig3 = px.line(trend, x="date", y="occupancy_pct", color="ward",
                            title="30-Day Occupancy Trend", height=250)
            fig3.add_hline(y=85, line_dash="dash", line_color=DANGER,
                            annotation_text="85% Alert Threshold")
            fig3.update_layout(margin=dict(t=40, b=20))
            col2.plotly_chart(fig3, use_container_width=True)

        st.text_input("Write the headline insight for your dashboard:", key="s11_headline")
        st.text_area("What operational decision does this dashboard support?", key="s11_decision", height=60)

    with tab_q:
        render_quiz(11)

    with tab_r:
        reflection_box(
            "Think about a dashboard you use or have seen. What is the primary decision it supports? "
            "Is that decision immediately visible, or is it buried under too much detail?",
            key="refl_s11"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION 12
# ══════════════════════════════════════════════════════════════════════════════
def session_12():
    session_header(12)
    tab_c, tab_d, tab_l, tab_q, tab_r = st.tabs(
        ["📖 Concept", "📊 Demo", "🔬 Lab", "❓ Quiz", "🪞 Reflect"])

    with tab_c:
        st.subheader("The Three Levels of Chart Titles")
        st.write("""
        A chart title is not a label — it is the first sentence of your story.
        Most analysts write descriptive titles; the best analysts write action-oriented titles.
        """)
        title_types = pd.DataFrame({
            "Type": ["Descriptive", "Analytical", "Action-Oriented"],
            "Example": [
                "Q3 Sales Data",
                "North Region Had Highest Q3 Sales",
                "Invest More in North Region — 34% Higher Returns vs Average"
            ],
            "When Appropriate": [
                "Exploratory dashboards where all context is needed",
                "Briefings where the audience draws their own conclusions",
                "Executive presentations and strategy documents — most business contexts"
            ]
        })
        st.dataframe(title_types, use_container_width=True, hide_index=True)
        callout_action("Default to action-oriented titles for any chart shown to a decision-maker. Descriptive titles are for data exploration tools, not business communication.", "Title Rule")

        st.subheader("Annotation: Adding the 'Why'")
        st.write("""
        Annotation connects a data observation to a business explanation.
        The best annotations answer three questions: what (the data fact),
        why (the cause), and so what (the implication).
        """)
        annotation_types = {
            "Reference line": "Shows a target, threshold, or benchmark",
            "Callout box": "Explains an anomaly or critical data point",
            "Highlight region": "Shades a period of interest (e.g., lockdown period)",
            "Data label": "Shows the exact value for a key point",
            "Arrow + text": "Directs attention to the most important data point"
        }
        for t, d in annotation_types.items():
            st.markdown(f"**{t}** — {d}")

        callout_insight("A well-annotated chart is self-contained. The reader does not need to hear the analyst speak to understand what happened, why it happened, and what to do about it.", "Self-Contained Chart")

    with tab_d:
        st.subheader("Interactive Title Lab")
        df = retail_sales()
        df["month_str"] = df["month"].dt.strftime("%b %Y")
        title_level = st.radio("Chart title type:", ["Descriptive", "Analytical", "Action-Oriented"],
                                horizontal=True, key="s12_title")
        add_annotation = st.checkbox("Add annotations", key="s12_ann")
        add_target = st.checkbox("Add target line (₹150L)", key="s12_target")
        titles = {
            "Descriptive": "Monthly Revenue",
            "Analytical": "Revenue Rose 40% Over 24 Months",
            "Action-Oriented": "Revenue Growth Accelerating — Scale Operations to Meet Demand"
        }
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["month"], y=df["revenue_lakhs"],
                                  mode="lines+markers", line=dict(color=PRIMARY, width=2.5),
                                  marker=dict(size=5), name="Revenue"))
        if add_target:
            fig.add_hline(y=150, line_dash="dot", line_color=ACCENT,
                           annotation_text="₹150L Target", annotation_position="right")
        if add_annotation:
            peak = df.loc[df["revenue_lakhs"].idxmax()]
            fig.add_annotation(x=peak["month"], y=peak["revenue_lakhs"],
                                text=f"Peak: ₹{peak['revenue_lakhs']}L", showarrow=True,
                                arrowhead=2, ax=0, ay=-40, font=dict(color=DANGER))
        fig.update_layout(title=titles[title_level], height=380,
                          xaxis_title="Month", yaxis_title="Revenue (₹L)")
        st.plotly_chart(fig, use_container_width=True)
        callout_manager(f"Title type used: **{title_level}**. Notice how the action-oriented title pre-answers the 'so what?' question before the reader even looks at the data.", "Managerial Meaning")

    with tab_l:
        st.subheader("Lab: Rewrite This Title")
        bad_titles = [
            ("Sales Data 2023", "Marketing campaign performance over 12 months, with a 45% spike in November due to Diwali promotion."),
            ("Patient Count", "ICU occupancy exceeded 90% every weekend in Q3, with average stay 3.2 days."),
            ("Cost Analysis", "Technology spend doubled in 2023 while all other costs grew by only 8%."),
        ]
        for i, (bad, context) in enumerate(bad_titles):
            st.markdown(f"**Bad title {i+1}:** *'{bad}'*")
            st.caption(f"Context: {context}")
            st.text_input(f"Your rewritten action-oriented title:", key=f"s12_title_{i}")
            if st.button(f"Show model title {i+1}", key=f"s12_model_{i}"):
                models = [
                    "Diwali Campaign Drove 45% Sales Spike in Nov — Replicate in 2024",
                    "ICU at Breaking Point Every Weekend in Q3 — Immediate Staffing Review Needed",
                    "Technology Is Now the Fastest-Growing Cost Driver — Review Vendor Contracts"
                ]
                st.success(f"Model: {models[i]}")
            st.markdown("")

    with tab_q:
        render_quiz(12)

    with tab_r:
        reflection_box(
            "Rewrite three descriptive titles from your most recent presentation as action-oriented titles. "
            "Which one required the deepest understanding of the data to write correctly?",
            key="refl_s12"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION 13
# ══════════════════════════════════════════════════════════════════════════════
def session_13():
    session_header(13)
    tab_c, tab_d, tab_l, tab_q, tab_r = st.tabs(
        ["📖 Concept", "📊 Demo", "🔬 Lab", "❓ Quiz", "🪞 Reflect"])

    with tab_c:
        st.subheader("The Anatomy of a Misleading Chart")
        st.write("""
        Some visualization errors are accidental — carelessness with axes or
        defaults. Others are deliberate — a truncated axis or a cherry-picked
        time window chosen to support a predetermined conclusion. Both do damage.
        """)
        pitfalls = {
            "Truncated axis": "Exaggerates small differences on bar charts",
            "Cherry-picked time window": "Selecting start/end dates that flatter the trend",
            "Dual y-axis deception": "Implying correlation between unrelated variables",
            "Area chart for multiple series": "Upper layers look larger than they are",
            "Chartjunk": "Decorations that add noise and reduce trust",
            "Missing denominator": "Rising absolute numbers hide declining rates",
            "Survivorship bias": "Only showing the successful outcomes (the 'winners')",
            "Inappropriate aggregation": "Averaging out the variation that matters most",
            "Misleading bubble size": "Area vs radius: radius = sqrt(value), not value",
            "Base rate neglect": "Impressive growth from a tiny base looks huge as %"
        }
        for pitfall, desc in pitfalls.items():
            st.markdown(f"🔴 **{pitfall}** — {desc}")

        callout_action("The ethical test: if a competitor's analyst saw this chart, would they say it represents the data fairly? If not, it needs redesign.", "The Fairness Test")

    with tab_d:
        st.subheader("Misleading Chart Clinic")
        clinic_cases = {
            "Dual Y-Axis Danger": "dual",
            "Cherry-Picked Time Window": "cherry",
            "Missing Denominator": "denominator",
        }
        case = st.selectbox("Select case:", list(clinic_cases.keys()), key="s13_case")
        if case == "Dual Y-Axis Danger":
            x = pd.date_range("2020-01", periods=24, freq="MS")
            y1 = 200 + np.arange(24) * 5 + rng.normal(0, 10, 24)
            y2 = 1000 + np.arange(24) * 100 + rng.normal(0, 200, 24)
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=x, y=y1, name="Ice Cream Sales", line=dict(color=PRIMARY)), secondary_y=False)
            fig.add_trace(go.Scatter(x=x, y=y2, name="Drowning Incidents", line=dict(color=DANGER)), secondary_y=True)
            fig.update_layout(title="Ice Cream Sales PERFECTLY Predict Drowning! (Misleading Dual Axis)",
                               height=350)
            st.plotly_chart(fig, use_container_width=True)
            callout_mistake("Both series rise due to a common cause: summer heat. The dual y-axis can make ANY two upward trends look correlated. Always check the confounding variable.", "Problem")
        elif case == "Cherry-Picked Time Window":
            ts = time_series_revenue()
            col1, col2 = st.columns(2)
            with col1:
                cherry = ts[(ts["month"] >= "2021-04-01") & (ts["month"] <= "2023-01-01")]
                fig1 = px.line(cherry, x="month", y="revenue",
                               title="Revenue Has Never Been Stronger! (Cherry-Picked Window)",
                               color_discrete_sequence=[SUCCESS])
                fig1.update_layout(height=280)
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                fig2 = px.line(ts, x="month", y="revenue",
                               title="Full Picture: Growth After COVID Dip (Full Window)",
                               color_discrete_sequence=[PRIMARY])
                fig2.add_vrect(x0="2020-03-01", x1="2021-03-01",
                               fillcolor=DANGER, opacity=0.1,
                               annotation_text="COVID Disruption")
                fig2.update_layout(height=280)
                st.plotly_chart(fig2, use_container_width=True)
            callout_mistake("Starting the chart after the COVID dip hides the fact that growth is partly recovery. The full time window tells a more honest story.", "Problem")
        else:
            col1, col2 = st.columns(2)
            years = [2019, 2020, 2021, 2022, 2023]
            complaints = [120, 180, 240, 200, 220]
            customers = [1000, 2000, 4000, 5000, 5500]
            with col1:
                fig1 = px.bar(x=years, y=complaints, color_discrete_sequence=[DANGER],
                               title="Complaints Are Rising! (Absolute Numbers Only)")
                fig1.update_layout(height=280, xaxis_title="Year", yaxis_title="Complaints")
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                rates = [c/cust*100 for c, cust in zip(complaints, customers)]
                fig2 = px.bar(x=years, y=rates, color_discrete_sequence=[SUCCESS],
                               title="Complaint Rate Is Actually Falling (Rate per 100 Customers)")
                fig2.update_layout(height=280, xaxis_title="Year", yaxis_title="Complaints per 100")
                st.plotly_chart(fig2, use_container_width=True)
            callout_insight("The complaint rate halved even as absolute numbers rose — because the customer base grew 5.5×. Always show rates when the denominator changes significantly.", "The Denominator Matters")

    with tab_l:
        st.subheader("Lab: Identify the Pitfall")
        st.write("For each scenario, identify the visualization pitfall and propose the fix.")
        scenarios = [
            "A startup shows revenue growth of 400% — from ₹10L to ₹50L.",
            "A chart compares Q4 performance across 5 years but omits 2020 because it was 'unusual'.",
            "A bar chart's y-axis starts at 95 to show that Division A (96) outperforms Division B (98).",
        ]
        for i, scenario in enumerate(scenarios):
            st.markdown(f"**Scenario {i+1}:** {scenario}")
            col1, col2 = st.columns(2)
            col1.text_input("Pitfall:", key=f"s13_pitfall_{i}")
            col2.text_input("Fix:", key=f"s13_fix_{i}")
            if st.button(f"Model answer {i+1}", key=f"s13_ans_{i}"):
                models = [
                    ("Base rate neglect — 400% sounds huge but from ₹10L is trivial in absolute terms.",
                     "Show both absolute and % change. Add market context."),
                    ("Cherry-picking / survivorship bias — omitting bad years distorts the trend.",
                     "Include all years. Annotate 2020 with context rather than removing it."),
                    ("Truncated axis — starting at 95 makes a 2% difference look like 100%.",
                     "Start y-axis at 0. Add a note that both divisions exceed 95% target."),
                ]
                st.success(f"Pitfall: {models[i][0]}\n\nFix: {models[i][1]}")
            st.markdown("")

    with tab_q:
        render_quiz(13)

    with tab_r:
        reflection_box(
            "Recall a chart or data presentation that surprised you with a conclusion. "
            "In hindsight, was there a pitfall — cherry-picked window, missing denominator, or misleading axis? "
            "What would the honest version have shown?",
            key="refl_s13"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION 14
# ══════════════════════════════════════════════════════════════════════════════
def session_14():
    session_header(14)
    tab_c, tab_d, tab_l, tab_q, tab_r = st.tabs(
        ["📖 Concept", "📊 Demo", "🔬 Lab", "❓ Quiz", "🪞 Reflect"])

    with tab_c:
        st.subheader("Visualizing Strategy: From Data to Decision")
        st.write("""
        Strategy communication is different from operational reporting.
        The audience is smaller, the decisions are larger, and the tolerance for
        data density is lower. A well-constructed strategic visual story
        compresses months of analysis into a single slide that makes a decision obvious.
        """)
        callout_insight("McKinsey's 'SCR' framework: Situation → Complication → Resolution. Every strategic visual story follows this arc — and every chart should advance one of these three stages.", "SCR Framework")

        strategy_charts = pd.DataFrame({
            "Strategic Question": [
                "Where are we vs target?",
                "Where should we invest?",
                "What is driving our performance?",
                "How do we compare to competitors?",
                "What will happen if we act / don't act?"
            ],
            "Recommended Visual": [
                "Bullet chart or performance gap bar",
                "Portfolio bubble chart (growth vs share)",
                "Waterfall chart (contribution analysis)",
                "Slope chart or indexed line comparison",
                "Scenario fan chart or before/after comparison"
            ]
        })
        st.dataframe(strategy_charts, use_container_width=True, hide_index=True)

        callout_mistake("Showing 15 slides of supporting analysis before the recommendation is the opposite of strategic. Senior leaders want the conclusion first, evidence second.", "Pyramid Principle")
        callout_action("Use Barbara Minto's Pyramid Principle: Lead with the recommendation. Follow with 3 supporting insights. Follow each with the data. Never bury the conclusion at the end.", "Structure Rule")

    with tab_d:
        st.subheader("Performance Gap Visualization")
        df = regional_sales()
        by_region = df.groupby("region")[["sales", "target"]].sum().reset_index()
        by_region["gap"] = by_region["sales"] - by_region["target"]
        by_region["color"] = by_region["gap"].apply(lambda x: SUCCESS if x >= 0 else DANGER)
        fig = go.Figure()
        for _, row in by_region.iterrows():
            fig.add_trace(go.Bar(x=[row["region"]], y=[row["gap"]],
                                  marker_color=row["color"], showlegend=False,
                                  name=row["region"]))
        fig.add_hline(y=0, line_color="black", line_width=1)
        fig.update_layout(title="Sales vs Target Gap by Region — 2 of 5 Regions Below Target",
                           height=320, yaxis_title="Gap vs Target (₹L)")
        st.plotly_chart(fig, use_container_width=True)
        callout_manager("This diverging gap chart answers 'who is on track?' in 3 seconds. Color instantly signals pass/fail. The manager can go straight to action.", "Managerial Meaning")

        st.subheader("Waterfall: Attribution of Performance")
        cats = list(df.groupby("category")["sales"].sum().index)
        base = df["sales"].sum() / len(cats)
        contribs = [(df[df["category"] == c]["sales"].sum() - base) for c in cats]
        fig2 = go.Figure(go.Waterfall(
            name="Contribution",
            orientation="v",
            measure=["relative"] * len(cats) + ["total"],
            x=cats + ["Total"],
            y=contribs + [sum(contribs)],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        fig2.update_layout(title="Category Contribution to Sales (Above/Below Average)",
                            height=330)
        st.plotly_chart(fig2, use_container_width=True)

    with tab_l:
        st.subheader("Lab: Tell a Strategic Story in 3 Charts")
        st.write("Use the datasets below to construct a 3-chart strategy story for a management presentation.")
        df_r = regional_sales()
        df_m = marketing_campaign()
        df_f = financial_expenses().groupby("category")["amount_lakhs"].sum().reset_index()

        st.markdown("**Chart 1: Where are we?**")
        fig1 = px.bar(df_r.groupby("region")["sales"].sum().reset_index().sort_values("sales", ascending=False),
                      x="region", y="sales", title="Chart 1: Regional Sales Snapshot",
                      color_discrete_sequence=[PRIMARY])
        fig1.update_layout(height=250)
        st.plotly_chart(fig1, use_container_width=True)
        st.text_input("Chart 1 action title:", key="s14_t1")

        st.markdown("**Chart 2: Where should we invest?**")
        fig2 = px.scatter(df_m, x="spend_lakhs", y="roi", size="revenue_lakhs", color="channel",
                           title="Chart 2: ROI vs Spend by Channel — Identify High-Return Channels")
        fig2.update_layout(height=280)
        st.plotly_chart(fig2, use_container_width=True)
        st.text_input("Chart 2 action title:", key="s14_t2")

        st.markdown("**Chart 3: What is the cost risk?**")
        fig3 = px.bar(df_f.sort_values("amount_lakhs", ascending=False),
                      x="category", y="amount_lakhs",
                      title="Chart 3: Cost Structure — Where Is the Risk?",
                      color_discrete_sequence=[DANGER if i == 0 else "#BDC3C7" for i in range(len(df_f))])
        fig3.update_layout(height=250)
        st.plotly_chart(fig3, use_container_width=True)
        st.text_input("Chart 3 action title:", key="s14_t3")
        st.text_area("Write the 3-sentence strategic recommendation that ties these charts together:", key="s14_rec", height=80)

    with tab_q:
        render_quiz(14)

    with tab_r:
        reflection_box(
            "Think of the most important strategic decision you have witnessed or participated in. "
            "What three charts would have made the evidence undeniable and the decision obvious?",
            key="refl_s14"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION 15
# ══════════════════════════════════════════════════════════════════════════════
def session_15():
    session_header(15)
    st.subheader("🔧 Integrated Storytelling Workshop")
    st.write("""
    This session is your capstone lab. You will select a business problem,
    explore data, build a complete visual story from context to recommendation,
    and export a narrative summary.
    """)

    st.markdown("---")
    st.markdown("### Step 1: Choose Your Business Domain")
    domain = st.selectbox("Business domain:", [
        "Retail Sales Strategy", "Marketing ROI Optimization",
        "Operations Efficiency Improvement", "Healthcare Resource Planning",
        "Financial Cost Control"
    ], key="s15_domain")

    domain_datasets = {
        "Retail Sales Strategy": retail_sales(),
        "Marketing ROI Optimization": marketing_campaign(),
        "Operations Efficiency Improvement": operations_delays(),
        "Healthcare Resource Planning": bed_occupancy(),
        "Financial Cost Control": financial_expenses(),
    }
    df = domain_datasets[domain]

    st.markdown("### Step 2: Define the Business Question")
    biz_q = st.text_input("State your business question in one sentence:", key="s15_q")

    st.markdown("### Step 3: Explore the Data")
    with st.expander("View raw dataset"):
        st.dataframe(df.head(30), use_container_width=True)

    st.markdown("### Step 4: Select Charts and Build Your Story")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Chart 1: Context / Overview**")
        if domain == "Retail Sales Strategy":
            ts = df.rename(columns={"revenue_lakhs": "value"}) if "revenue_lakhs" in df.columns else df
            fig1 = px.line(df, x="month", y="revenue_lakhs", title="Revenue Over Time",
                           color_discrete_sequence=[PRIMARY]) if "revenue_lakhs" in df.columns else go.Figure()
        elif domain == "Marketing ROI Optimization":
            fig1 = px.bar(df.sort_values("roi", ascending=False), x="channel", y="roi",
                          title="ROI by Channel", color_discrete_sequence=[PRIMARY])
        elif domain == "Operations Efficiency Improvement":
            fig1 = px.line(df, x="week", y="avg_delay_hrs", title="Delivery Delay Trend",
                           color_discrete_sequence=[PRIMARY])
        elif domain == "Healthcare Resource Planning":
            avg_occ = df.groupby("ward")["occupancy_pct"].mean().reset_index()
            fig1 = px.bar(avg_occ.sort_values("occupancy_pct", ascending=False),
                          x="ward", y="occupancy_pct", title="Avg Occupancy by Ward",
                          color_discrete_sequence=[PRIMARY])
        else:
            agg = df.groupby("category")["amount_lakhs"].sum().reset_index()
            fig1 = px.bar(agg.sort_values("amount_lakhs", ascending=False),
                          x="category", y="amount_lakhs", title="Total Spend by Category",
                          color_discrete_sequence=[PRIMARY])
        fig1.update_layout(height=270, margin=dict(t=40, b=20))
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("**Chart 2: Key Insight**")
        if domain == "Marketing ROI Optimization":
            fig2 = px.scatter(df, x="spend_lakhs", y="revenue_lakhs", size="conversions",
                               color="channel", title="Spend vs Revenue by Channel")
        elif domain == "Retail Sales Strategy":
            df["ma"] = df["revenue_lakhs"].rolling(3).mean()
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=df["month"], y=df["revenue_lakhs"], mode="lines", name="Revenue", line=dict(color=PRIMARY)))
            fig2.add_trace(go.Scatter(x=df["month"], y=df["ma"], mode="lines", name="3M MA", line=dict(color=ACCENT, dash="dash")))
            fig2.update_layout(title="Revenue with Trend Line")
        elif domain == "Operations Efficiency Improvement":
            fig2 = px.scatter(df, x="shipments", y="avg_delay_hrs",
                               title="Do More Shipments → More Delays?", trendline="ols")
        elif domain == "Healthcare Resource Planning":
            recent = df.groupby(["date", "ward"])["occupancy_pct"].mean().reset_index()
            fig2 = px.line(recent.tail(200), x="date", y="occupancy_pct", color="ward",
                            title="Occupancy Trend by Ward")
            fig2.add_hline(y=85, line_dash="dash", line_color=DANGER,
                            annotation_text="Alert Threshold")
        else:
            fig2 = px.bar(df, x="quarter", y="amount_lakhs", color="category",
                           title="Cost Trend by Category Over Time")
        fig2.update_layout(height=270, margin=dict(t=40, b=20))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Step 5: Build Your Narrative")
    context = st.text_area("Context (What is the situation?):", key="s15_context", height=50)
    insight = st.text_area("Insight (What pattern does the data show?):", key="s15_insight", height=50)
    implication = st.text_area("Implication (What does this mean for the business?):", key="s15_impl", height=50)
    recommendation = st.text_area("Recommendation (What should be done, and by when?):", key="s15_rec", height=60)

    st.markdown("### Step 6: Export Your Story")
    if st.button("Generate Story Summary", key="s15_export"):
        summary = f"""
VISUAL STORY SUMMARY
====================
Domain: {domain}
Business Question: {biz_q}

CONTEXT
{context if context else '[Not filled in]'}

INSIGHT
{insight if insight else '[Not filled in]'}

IMPLICATION
{implication if implication else '[Not filled in]'}

RECOMMENDATION
{recommendation if recommendation else '[Not filled in]'}

Generated in: Storytelling using Data Visualization — PGDM-BDA
Goa Institute of Management | Dr. Alok Tiwari
"""
        st.download_button("⬇ Download Story Summary (TXT)", summary.encode(),
                           f"visual_story_{domain.replace(' ','_')}.txt", "text/plain")
        callout_action("Your story is ready. Review: does each section flow naturally to the next? Does the recommendation follow logically from the insight?", "Final Check")

    reflection_box(
        "What was the hardest part of this workshop — choosing the right chart, "
        "writing the insight, or connecting it to a recommendation? "
        "That friction is where your growth as a data storyteller is happening.",
        key="refl_s15"
    )


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION 16
# ══════════════════════════════════════════════════════════════════════════════
def session_16():
    session_header(16)
    tab_c, tab_d, tab_l, tab_q, tab_r = st.tabs(
        ["📖 Concept", "📊 Demo", "🔬 Lab", "❓ Quiz", "🪞 Reflect"])

    with tab_c:
        st.subheader("Healthcare Data: Unique Challenges")
        st.write("""
        Healthcare data visualization carries special responsibilities.
        Patient safety decisions, resource allocation, and public health
        communication all depend on charts being honest, interpretable,
        and appropriately caveated.
        """)
        callout_insight("Healthcare dashboards serve two distinct audiences: clinical staff (need operational granularity) and administrators (need strategic aggregates). Design differently for each.", "Audience Segmentation")
        hc_charts = pd.DataFrame({
            "Healthcare Use Case": [
                "Patient flow and wait times",
                "Bed occupancy and capacity",
                "Mortality and complication rates",
                "Epidemic/disease spread",
                "Resource utilization",
                "Staff performance"
            ],
            "Recommended Visual": [
                "Heat map (hour × day) or gantt-style timeline",
                "Bullet chart or gauge with threshold line",
                "Control chart (SPC) — distinguish noise from signal",
                "Choropleth map or epidemic curve",
                "Stacked utilization bar with over-capacity highlight",
                "Box plot or dot plot (anonymous)"
            ],
            "Key Risk": [
                "Aggregating across very different patient types",
                "Occupancy averages hide daily peak crises",
                "Small denominators make rates unstable (use confidence intervals)",
                "Lag in reporting creates false calm before peak",
                "Averages hide equipment failures or maintenance gaps",
                "Individual identification from drill-down data (privacy)"
            ]
        })
        st.dataframe(hc_charts, use_container_width=True, hide_index=True)
        callout_mistake("Showing only average length of stay across a ward hides the distribution of complex vs routine cases. A bimodal distribution requires completely different interventions.", "The Average LOS Problem")

    with tab_d:
        st.subheader("Hospital Operational Dashboard")
        df_bed = bed_occupancy()
        df_pf = healthcare_patient_flow()

        col1, col2, col3, col4 = st.columns(4)
        avg_occ = df_bed["occupancy_pct"].mean()
        icu_occ = df_bed[df_bed["ward"] == "ICU"]["occupancy_pct"].mean()
        critical_pct = (df_pf["severity"] == "Critical").mean() * 100
        avg_wait = df_pf["wait_minutes"].mean()
        col1.metric("Overall Occupancy", f"{avg_occ:.1f}%", "⚠️ High" if avg_occ > 80 else "Normal")
        col2.metric("ICU Occupancy", f"{icu_occ:.1f}%", "🔴 Critical" if icu_occ > 85 else "Monitor")
        col3.metric("Critical Patients", f"{critical_pct:.1f}%", "of all admissions")
        col4.metric("Avg Wait Time", f"{avg_wait:.0f} min", "Across departments")

        col_a, col_b = st.columns([1.3, 1])
        with col_a:
            pivot = df_pf.groupby(["hour", "department"])["wait_minutes"].mean().reset_index()
            pivot_wide = pivot.pivot(index="department", columns="hour", values="wait_minutes")
            fig1 = px.imshow(pivot_wide, color_continuous_scale="Reds",
                              title="Average Wait Time by Dept × Hour of Day",
                              labels=dict(x="Hour", y="Department", color="Wait (min)"),
                              aspect="auto")
            fig1.update_layout(height=300, margin=dict(t=40, b=20))
            col_a.plotly_chart(fig1, use_container_width=True)
        with col_b:
            ward_occ = df_bed.groupby("ward")["occupancy_pct"].mean().reset_index().sort_values("occupancy_pct", ascending=False)
            colors = [DANGER if v > 85 else ACCENT if v > 75 else PRIMARY for v in ward_occ["occupancy_pct"]]
            fig2 = go.Figure(go.Bar(x=ward_occ["occupancy_pct"], y=ward_occ["ward"],
                                     orientation="h", marker_color=colors))
            fig2.add_vline(x=85, line_dash="dot", line_color=DANGER,
                            annotation_text="85% Alert")
            fig2.update_layout(title="Ward Occupancy vs Threshold", height=300,
                                margin=dict(t=40, b=20), xaxis_title="Occupancy (%)")
            col_b.plotly_chart(fig2, use_container_width=True)

        callout_manager("The heat map immediately shows peak demand hours for each department. The ward chart flags which wards are above the alert threshold. Together they drive staffing decisions.", "Managerial Meaning")

    with tab_l:
        st.subheader("Lab: Build the Healthcare Story")
        df_pf2 = healthcare_patient_flow()
        dept_focus = st.selectbox("Focus department:", df_pf2["department"].unique(), key="s16_dept")
        sub = df_pf2[df_pf2["department"] == dept_focus]
        col1, col2 = st.columns(2)
        with col1:
            fig_hist = px.histogram(sub, x="wait_minutes", nbins=20,
                                     title=f"Wait Time Distribution — {dept_focus}",
                                     color_discrete_sequence=[PRIMARY])
            fig_hist.update_layout(height=270)
            col1.plotly_chart(fig_hist, use_container_width=True)
        with col2:
            fig_sev = px.bar(sub["severity"].value_counts().reset_index(),
                              x="severity", y="count", color="severity",
                              title=f"Severity Mix — {dept_focus}",
                              color_discrete_map={"Low": SUCCESS, "Medium": ACCENT,
                                                   "High": WARNING if True else ACCENT,
                                                   "Critical": DANGER})
            fig_sev.update_layout(height=270, showlegend=False)
            col2.plotly_chart(fig_sev, use_container_width=True)
        stats = sub["wait_minutes"].describe()
        st.markdown(f"**{dept_focus} wait statistics** — Median: {stats['50%']:.0f} min | P75: {stats['75%']:.0f} min | Max: {stats['max']:.0f} min | Critical cases: {(sub['severity']=='Critical').sum()}")
        st.text_area("What is the priority action for this department based on the data?", key="s16_lab_rec", height=60)
        if st.button("Model recommendation", key="s16_model"):
            median_w = stats["50%"]
            crit = (sub["severity"] == "Critical").mean() * 100
            st.success(f"For {dept_focus}: Median wait is {median_w:.0f} minutes with {crit:.0f}% critical patients. Priority action depends on severity mix — if critical patients are waiting over 30 minutes, triage process review is urgent. If waits are driven by volume, consider parallel track protocols.")
        st.download_button("⬇ Download patient flow data", df_pf2.to_csv(index=False).encode(),
                           "session16_patient_flow.csv", "text/csv")

    with tab_q:
        render_quiz(16)

    with tab_r:
        reflection_box(
            "Healthcare visualization has lives at stake. What additional design constraints — "
            "beyond clarity and honesty — should a healthcare dashboard designer follow? "
            "Think about privacy, uncertainty, and alert fatigue.",
            key="refl_s16"
        )

