"""
sessions_1_8.py — Sessions 1–8, Modules 1 & 2.
No footer() calls — footer is rendered once in app.py.
Each session: Concept | Demo | Lab | Quiz | Reflect
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from modules.ui_components import (
    callout_insight, callout_manager, callout_mistake, callout_action,
    session_header, reflection_box,
    PRIMARY, ACCENT, SUCCESS, DANGER, WARNING
)
from modules.data_generators import (
    retail_sales, regional_sales, customer_satisfaction,
    scatter_sales_spend, financial_expenses, marketing_campaign
)
from modules.quiz_bank import QUIZ_BANK

rng = np.random.default_rng(7)


# ── Shared quiz renderer (no pre-selection, Reveal Answer button) ─────────────
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
                index=0,          # ← no option pre-selected
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
#  SESSION 1 — Why Visualization Matters
# ══════════════════════════════════════════════════════════════════════════════
def session_1():
    session_header(1)
    tab_c, tab_d, tab_l, tab_q, tab_r = st.tabs(
        ["📖 Concept", "📊 Demo", "🔬 Lab", "❓ Quiz", "🪞 Reflect"])

    with tab_c:
        st.subheader("The Problem with Raw Numbers")
        st.write("""
        Managers today are drowning in data — dashboards, spreadsheets, monthly reports.
        Yet most decisions still rely on gut feel, not because data is missing, but because
        it is not communicated well. Visualization bridges that gap.
        """)
        callout_insight(
            "A number without context is nearly meaningless. ₹4.2 Cr revenue — good or bad? "
            "Compared to what? Over which period? For which segment? Visualization supplies context instantly.",
            "Why Visualization Matters"
        )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📋 Same data as a table")
            df = pd.DataFrame({
                "Month": ["Jan","Feb","Mar","Apr","May","Jun"],
                "Sales (₹L)": [112, 98, 134, 156, 141, 168]
            })
            st.dataframe(df, use_container_width=True)
            st.caption("*Trend? You need to compute it mentally.*")
        with col2:
            st.markdown("#### 📈 Same data as a chart")
            df["Month"] = pd.Categorical(df["Month"],
                categories=["Jan","Feb","Mar","Apr","May","Jun"], ordered=True)
            fig = px.line(df, x="Month", y="Sales (₹L)", markers=True,
                          color_discrete_sequence=[PRIMARY])
            fig.update_layout(margin=dict(t=10, b=10), height=220)
            st.plotly_chart(fig, use_container_width=True)
            st.caption("*Upward trend with a dip in Feb — visible in 2 seconds.*")
        callout_manager(
            "The chart takes 2 seconds; the table takes 20 — and still hides the upward trend.",
            "Managerial Meaning"
        )

        st.subheader("What Is Data Storytelling?")
        st.write("""
        Data storytelling combines **data** (evidence), **visuals** (encoding), and
        **narrative** (context + so-what). Miss any one and the story breaks down.
        An analysis without narrative is an essay without a conclusion.
        """)
        cols = st.columns(3)
        icons = ["🔢", "📊", "📝"]
        labels = ["Data", "Visuals", "Narrative"]
        descs = ["Evidence: numbers, measurements, facts",
                 "Encoding: charts, graphs, dashboards",
                 "Context: why it matters, what to do"]
        for col, icon, label, desc in zip(cols, icons, labels, descs):
            col.markdown(f"""
            <div style='background:#EAF4FF;border-radius:10px;padding:14px;text-align:center;'>
            <div style='font-size:2rem;'>{icon}</div>
            <strong>{label}</strong><br>
            <span style='font-size:0.83rem;color:#555;'>{desc}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("#### 💡 Five reasons executives ignore data presentations")
        reasons = [
            ("Too many charts, no clear message", "Data dump overwhelming the key insight"),
            ("Data shown without a business question", "The 'so what?' is never answered"),
            ("Charts require heavy verbal explanation", "Good charts should stand alone"),
            ("No recommendation — just observations", "Analysts describe; managers decide"),
            ("Visual design adds noise, not clarity", "Chartjunk obscures the signal"),
        ]
        for reason, detail in reasons:
            with st.expander(f"❌ {reason}"):
                st.write(detail)

        callout_action(
            "Your job as an analyst is not to show all the data — it is to select the right data, "
            "encode it clearly, and make the decision obvious.",
            "Action Recommendation"
        )

        st.subheader("The DIKW Pyramid")
        st.write("""
        Data → Information → Knowledge → Wisdom is the classic hierarchy.
        A well-designed chart compresses this journey, helping a manager move from
        raw numbers to a defensible decision in minutes, not hours.
        """)

        # DIKW pyramid visual
        pyramid_fig = go.Figure(go.Funnel(
            y=["Data (raw numbers)", "Information (organized)", "Knowledge (patterns)", "Wisdom (decisions)"],
            x=[100, 75, 50, 25],
            textinfo="label",
            marker={"color": ["#BDC3C7","#7FB3D3","#2E86C1",PRIMARY]},
        ))
        pyramid_fig.update_layout(height=250, margin=dict(t=10,b=10), showlegend=False)
        st.plotly_chart(pyramid_fig, use_container_width=True)

    with tab_d:
        st.subheader("Table vs Chart: Side-by-Side")
        df = retail_sales()[["month","revenue_lakhs"]].head(12)
        df["month_str"] = df["month"].dt.strftime("%b %Y")
        col1, col2 = st.columns([1, 1.5])
        with col1:
            st.dataframe(df[["month_str","revenue_lakhs"]].rename(
                columns={"month_str":"Month","revenue_lakhs":"Revenue (₹L)"}),
                use_container_width=True, height=380)
        with col2:
            fig = px.line(df, x="month_str", y="revenue_lakhs",
                          title="Revenue Grows Through the Year — Peak in Nov",
                          markers=True, color_discrete_sequence=[PRIMARY])
            fig.update_layout(xaxis_title="Month", yaxis_title="Revenue (₹L)", height=380)
            st.plotly_chart(fig, use_container_width=True)
        callout_insight(
            "The peak, the dip, and the trend are all visible instantly. "
            "The table forces you to compute — the chart shows.",
            "Observe"
        )

        st.subheader("Anatomy of a Well-Designed Chart")
        anatomy_data = {
            "Element": ["Title", "Subtitle", "Axis labels", "Annotations", "Legend", "Source line"],
            "Purpose": [
                "States the insight or finding (not just the topic)",
                "Adds qualifying context or methodology note",
                "Label every axis with variable name + unit",
                "Highlight the key data points with text callouts",
                "Explains color/shape coding (eliminate if chart is self-explanatory)",
                "Credits the data source — essential for credibility"
            ]
        }
        st.dataframe(pd.DataFrame(anatomy_data), use_container_width=True, hide_index=True)

        st.subheader("Interactive: What Makes a Good Story?")
        q_story = st.radio("A good data story must include:", [
            "A) All available data, no matter how much",
            "B) Exactly three charts",
            "C) Data + Visuals + Narrative leading to a clear recommendation",
            "D) Only charts, no text explanation"
        ], index=0, key="s1_demo_q")
        if st.button("Check answer", key="s1_demo_check"):
            if q_story and "C)" in q_story:
                st.success("✅ Correct! All three components are needed — missing any one weakens the story.")
            elif q_story:
                st.error("❌ The answer is C — data + visuals + narrative, leading to a recommendation.")

    with tab_l:
        st.subheader("Activity 1: Convert a Data Dump to a Story")
        st.write("You have been given 6 months of sales data. Your task: turn it into a data story.")
        df_lab = pd.DataFrame({
            "Month": ["Jan","Feb","Mar","Apr","May","Jun"],
            "Online (₹L)": [45, 41, 58, 72, 68, 89],
            "Offline (₹L)": [67, 63, 76, 84, 73, 79]
        })
        st.dataframe(df_lab, use_container_width=True)

        st.markdown("**Step 1:** What is the single most important trend in this data?")
        t1 = st.text_input("Your observation:", key="s1_lab_t1")

        st.markdown("**Step 2:** Who is the audience — a Sales VP or a Store Manager?")
        audience = st.radio("", ["Sales VP (strategic, quarterly view)",
                                  "Store Manager (operational, daily/weekly)"], key="s1_aud", index=0)

        st.markdown("**Step 3:** Write an action-oriented chart title.")
        t2 = st.text_input("Your title:", key="s1_lab_t2")

        st.markdown("**Step 4:** What is your recommendation in one sentence?")
        t3 = st.text_area("Recommendation:", key="s1_lab_t3", height=60)

        if st.button("Show model answers", key="s1_model"):
            st.success("""
**Observation:** Online sales are growing faster than offline (+98% vs +18% over 6 months).

**Sales VP title:** 'Online Channel Growing 5× Faster Than Offline — Digital-First Pivot Validated'

**Recommendation:** Accelerate digital marketing investment; the online channel is approaching parity with offline and should exceed it by August at current trajectory.
            """)

        st.markdown("---")
        st.subheader("Activity 2: Spot the Story Gap")
        st.write("Below are two presentations. Which one is a data story vs a data dump? Why?")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Presentation A**")
            st.markdown("""
- Slide 1: Revenue by month (12 charts)
- Slide 2: Revenue by product (15 bars)
- Slide 3: Revenue by region (map)
- Slide 4: Revenue by channel (pie)
- Slide 5: Thank you!
            """)
        with col2:
            st.markdown("**Presentation B**")
            st.markdown("""
- Slide 1: Our digital revenue is declining (the problem)
- Slide 2: Mobile users have dropped 35% since August
- Slide 3: Competitor X gained that share
- Slide 4: Recommendation: Relaunch mobile app by Q2
            """)
        answer_gap = st.radio("Which is a data story?", ["Presentation A", "Presentation B"],
                               index=0, key="s1_gap")
        if answer_gap == "Presentation B":
            st.success("✅ Correct! Presentation B has a problem → evidence → recommendation structure. "
                       "Presentation A is a data dump — all data, no narrative.")
        elif answer_gap == "Presentation A":
            st.error("❌ Presentation A shows all data but has no narrative thread or recommendation. "
                     "Presentation B follows the SCR structure.")

        st.download_button("⬇ Download sample dataset (CSV)",
                           df_lab.to_csv(index=False).encode(),
                           "session1_sales.csv", "text/csv")

    with tab_q:
        render_quiz(1)

    with tab_r:
        reflection_box(
            "Think of the last time a data presentation failed to convince your audience. "
            "What was missing — data, visual, or narrative? How would you redesign it?",
            key="refl_s1"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION 2 — Mapping Data to Visual Forms
# ══════════════════════════════════════════════════════════════════════════════
def session_2():
    session_header(2)
    tab_c, tab_d, tab_l, tab_q, tab_r = st.tabs(
        ["📖 Concept", "📊 Demo", "🔬 Lab", "❓ Quiz", "🪞 Reflect"])

    with tab_c:
        st.subheader("Visual Encoding Channels")
        st.write("""
        Data is abstract — numbers and categories with no inherent visual form.
        Visualization maps abstract data onto visual properties that our perceptual
        system decodes. These properties are called **encoding channels**.
        """)
        channels = [
            ("🥇", "Position (x/y axis)", "Most accurate for quantitative data", "#1B4F8A"),
            ("🥈", "Length (bar height)", "Very accurate — basis of bar charts", "#2471A3"),
            ("🥉", "Angle (pie slices)", "Less accurate — basis of pie charts", "#2E86C1"),
            ("4️⃣", "Area (bubble size)", "Difficult to compare precisely", "#5DADE2"),
            ("5️⃣", "Color hue", "Good for categories, not quantities", "#85C1E9"),
            ("6️⃣", "Color intensity", "Works for ordered/sequential data", "#AED6F1"),
            ("7️⃣", "Shape", "Good for categories, not rank", "#D6EAF8"),
            ("8️⃣", "Texture", "Weak — last resort only", "#EBF5FB"),
        ]
        cols = st.columns(2)
        for i, (rank, ch, desc, color) in enumerate(channels):
            cols[i % 2].markdown(
                f"<div style='background:{color}20;border-left:4px solid {color};"
                f"border-radius:6px;padding:8px 12px;margin:4px 0;'>"
                f"<strong>{rank} {ch}</strong><br>"
                f"<span style='font-size:0.85rem;color:#555;'>{desc}</span></div>",
                unsafe_allow_html=True
            )
        callout_insight(
            "Cleveland & McGill (1984) established this hierarchy empirically. "
            "Whenever possible, encode the most important variable using position.",
            "Research Finding"
        )

        st.subheader("Data Types → Chart Families")
        data_chart = pd.DataFrame({
            "Data Type": ["Categorical (Nominal)", "Categorical (Ordinal)",
                           "Quantitative (Continuous)", "Quantitative (Discrete)",
                           "Temporal (Time)", "Relational (Two vars)"],
            "Examples": ["Product type, Region", "Rating 1–5, Size S/M/L",
                          "Revenue, Temperature", "Count, Units",
                          "Monthly sales, Trends", "Spend vs Revenue"],
            "Best Charts": ["Bar, Dot plot, Treemap", "Bar (sorted), Heatmap",
                             "Histogram, Box, Density", "Bar, Dot, Lollipop",
                             "Line, Area, Slope", "Scatter, Bubble"],
            "Avoid": ["Pie >5 cats", "Line chart", "Bar chart", "Histogram",
                       "Bar chart for trends", "Stacked bar"]
        })
        st.dataframe(data_chart, use_container_width=True, hide_index=True)
        callout_mistake(
            "Choosing a chart because it looks impressive rather than because it matches "
            "your data type is the most common beginner error in business analytics.",
            "Common Mistake"
        )

        st.subheader("Quick Reference: Question → Chart")
        qmap = {
            "How much?": ["Bar chart", "Dot plot", "Lollipop"],
            "How did it change?": ["Line chart", "Area chart", "Slope chart"],
            "How is it distributed?": ["Histogram", "Box plot", "Violin"],
            "How does it relate?": ["Scatter plot", "Bubble chart", "Heat map"],
            "What is its composition?": ["Stacked bar", "Treemap", "Pie (≤5)"],
            "How far from target?": ["Bullet chart", "Diverging bar", "Gap chart"],
        }
        for question, charts in qmap.items():
            st.markdown(f"**{question}** → {', '.join(charts)}")

    with tab_d:
        st.subheader("Interactive Chart Gallery")
        df = regional_sales()
        chart_type = st.selectbox("Explore a chart type:",
            ["Bar Chart", "Dot Plot", "Scatter Plot", "Heat Map",
             "Histogram", "Box Plot"])
        if chart_type == "Bar Chart":
            by_region = df.groupby("region")["sales"].sum().reset_index().sort_values("sales", ascending=True)
            fig = px.bar(by_region, x="sales", y="region", orientation="h",
                         title="Total Sales by Region — sorted for easy ranking",
                         color_discrete_sequence=[PRIMARY])
            fig.update_layout(height=320)
            st.plotly_chart(fig, use_container_width=True)
            callout_manager("Horizontal bars work better than vertical when labels are long. "
                             "Sorted descending (highest at top) enables instant rank reading.", "Managerial Meaning")
        elif chart_type == "Dot Plot":
            by_region = df.groupby("region")["sales"].sum().reset_index().sort_values("sales")
            fig = go.Figure(go.Scatter(x=by_region["sales"], y=by_region["region"],
                                       mode="markers", marker=dict(size=14, color=PRIMARY)))
            fig.update_layout(title="Dot Plot — Cleaner ink, same information as bar",
                               height=300, xaxis_title="Sales (₹L)")
            st.plotly_chart(fig, use_container_width=True)
            callout_insight("Dot plots use less ink than bar charts. Particularly useful for "
                             "long ranked lists where bar area adds visual weight without adding information.", "Key Insight")
        elif chart_type == "Scatter Plot":
            df2 = scatter_sales_spend()
            fig = px.scatter(df2, x="marketing_spend", y="revenue", color="channel",
                             title="Marketing Spend vs Revenue — Positive Association",
                             trendline="ols",
                             labels={"marketing_spend": "Marketing Spend (₹L)",
                                     "revenue": "Revenue (₹L)"})
            fig.update_layout(height=380)
            st.plotly_chart(fig, use_container_width=True)
            callout_manager("Scatter plots reveal relationships. Add a trend line to make the "
                             "direction explicit. Color by channel shows if the pattern holds uniformly.", "Managerial Meaning")
        elif chart_type == "Heat Map":
            pivot = df.pivot_table(index="category", columns="region", values="sales", aggfunc="sum")
            fig = px.imshow(pivot, color_continuous_scale="Blues", text_auto=True,
                            title="Sales Heat Map — Category × Region",
                            aspect="auto")
            fig.update_layout(height=380)
            st.plotly_chart(fig, use_container_width=True)
            callout_insight("Dark cells draw attention instantly — no need to scan rows and columns "
                             "comparing numbers. The pattern is pre-attentive.", "Key Insight")
        elif chart_type == "Histogram":
            df3 = customer_satisfaction()
            fig = px.histogram(df3, x="nps_score", nbins=20,
                               title="Distribution of NPS Scores — Is It Bimodal?",
                               color_discrete_sequence=[PRIMARY])
            fig.update_layout(height=340)
            st.plotly_chart(fig, use_container_width=True)
            callout_insight("The histogram shape (symmetric, skewed, bimodal) is the first "
                             "thing to observe. A bimodal shape suggests two distinct groups in the data.", "Key Insight")
        else:
            df4 = customer_satisfaction()
            fig = px.box(df4, x="department", y="nps_score", color="department",
                         title="NPS by Department — Median, IQR, Outliers",
                         points="outliers")
            fig.update_layout(height=360, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            callout_manager("The box plot shows median (central line), IQR (box), range (whiskers), "
                             "and outliers (dots). Far more information than a bar of averages.", "Managerial Meaning")

    with tab_l:
        st.subheader("Activity 1: Match Data to Chart")
        st.write("For each scenario, pick the most appropriate chart type.")
        scenarios = [
            ("Monthly revenue over 3 years — show the trend",
             ["Line chart", "Pie chart", "Scatter plot", "Box plot"], "Line chart"),
            ("Budget allocation across 5 departments — show proportions",
             ["Pie chart (≤5 categories)", "Histogram", "Box plot", "Scatter plot"],
             "Pie chart (≤5 categories)"),
            ("Distribution of customer ages in a retail store",
             ["Histogram", "Bar chart", "Line chart", "Stacked area"], "Histogram"),
            ("Relationship between advertising spend and store footfall",
             ["Scatter plot", "Pie chart", "Stacked bar", "Histogram"], "Scatter plot"),
            ("Comparing Q1 revenue for 10 product lines — ranked",
             ["Horizontal sorted bar", "3D pie", "Violin plot", "Calendar heat map"],
             "Horizontal sorted bar"),
        ]
        for i, (scenario, options, correct) in enumerate(scenarios):
            st.markdown(f"**Scenario {i+1}:** {scenario}")
            choice = st.radio("", options, key=f"s2_lab_{i}", horizontal=True, index=0)
            if st.button("Check ✓", key=f"s2_check_{i}"):
                if choice == correct:
                    st.success(f"✅ Correct! **{correct}** is the best choice here.")
                elif choice is None:
                    st.warning("Please select an option.")
                else:
                    st.error(f"❌ Best answer: **{correct}**")
            st.markdown("")

        st.markdown("---")
        st.subheader("Activity 2: Identify the Encoding Channel")
        st.write("Name the primary encoding channel used in each chart:")
        enc_scenarios = [
            ("A bar chart comparing sales across 6 regions", "Bar length (Length channel)"),
            ("A scatter plot showing spend vs revenue", "X-position and Y-position (Position channel)"),
            ("A heat map of sales intensity by region × category", "Color intensity (sequential)"),
            ("A pie chart showing market share of 4 brands", "Angle (area)"),
        ]
        for i, (sce, ans) in enumerate(enc_scenarios):
            st.markdown(f"**{i+1}. {sce}**")
            user_ans = st.text_input("Channel:", key=f"s2_enc_{i}")
            with st.expander("See answer"):
                st.info(f"**{ans}**")
            st.markdown("")

    with tab_q:
        render_quiz(2)

    with tab_r:
        reflection_box(
            "Look at any chart you have seen in the last week — in a newspaper, presentation, or report. "
            "What encoding channels does it use? Are they the most accurate choice for that data type?",
            key="refl_s2"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION 3 — Axes, Scales & Coordinate Systems
# ══════════════════════════════════════════════════════════════════════════════
def session_3():
    session_header(3)
    tab_c, tab_d, tab_l, tab_q, tab_r = st.tabs(
        ["📖 Concept", "📊 Demo", "🔬 Lab", "❓ Quiz", "🪞 Reflect"])

    with tab_c:
        st.subheader("Why Axes Matter More Than You Think")
        st.write("""
        The axis is the backbone of almost every chart. It defines the reference frame
        against which the reader interprets the data. Tamper with it — deliberately or
        carelessly — and you change the story completely without touching a single data point.
        """)
        callout_mistake(
            "Starting a bar chart y-axis at any value other than zero is one of the most common "
            "forms of visual misleading in business presentations. A 5% sales increase can be made "
            "to look like a 500% increase just by changing where the axis starts.",
            "The Truncated Axis Problem"
        )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### ❌ Truncated axis — misleading")
            df = pd.DataFrame({"Q": ["Q1","Q2","Q3","Q4"], "Rev": [152,158,155,162]})
            fig = go.Figure(go.Bar(x=df["Q"], y=df["Rev"], marker_color=DANGER))
            fig.update_yaxes(range=[148, 170])
            fig.update_layout(height=230, margin=dict(t=20,b=10),
                               title="Revenue SKYROCKETING!")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.markdown("#### ✅ Honest axis — accurate")
            fig2 = go.Figure(go.Bar(x=df["Q"], y=df["Rev"], marker_color=PRIMARY))
            fig2.update_yaxes(range=[0, 200])
            fig2.update_layout(height=230, margin=dict(t=20,b=10),
                                title="Revenue Stable (~6.5% growth)")
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Bar vs Line Chart — Different Rules")
        rules = pd.DataFrame({
            "Chart Type": ["Bar Chart", "Line Chart"],
            "Encoding": ["Bar LENGTH (from zero baseline)", "SLOPE (rate of change)"],
            "Zero Baseline?": ["Always — missing baseline distorts length", "Not always — zooming in reveals slope better"],
            "Analogy": ["A ruler must start at zero to measure length", "A thermometer starts at the relevant temperature range"]
        })
        st.dataframe(rules, use_container_width=True, hide_index=True)

        st.subheader("Linear vs Logarithmic Scale")
        st.write("""
        A **linear scale** spaces values evenly: 10, 20, 30, 40.
        A **logarithmic scale** spaces orders of magnitude evenly: 10, 100, 1,000, 10,000.
        Use log scales when data spans multiple orders of magnitude — otherwise small values become invisible.
        """)
        col1, col2 = st.columns(2)
        x = [1, 10, 100, 1000, 10000]
        with col1:
            fig = px.line(x=x, y=x, markers=True, title="Linear — small values invisible")
            fig.update_layout(height=240, margin=dict(t=30,b=10))
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig2 = px.line(x=x, y=x, log_y=True, markers=True,
                           title="Log — all magnitudes readable")
            fig2.update_layout(height=240, margin=dict(t=30,b=10))
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Dual Y-Axis — Handle with Care")
        callout_mistake(
            "Dual y-axis charts (two different scales on the same chart) allow the analyst to "
            "manually scale either axis until two unrelated variables appear to move together. "
            "This manufactured correlation is one of the most deceptive techniques in business reporting.",
            "Dual Axis Danger"
        )

    with tab_d:
        st.subheader("Interactive: Drag the Axis Start")
        st.write("Drag the slider to change where the y-axis starts. Observe how the story changes.")
        df = pd.DataFrame({
            "Quarter": ["Q1","Q2","Q3","Q4"],
            "Revenue": [152, 158, 155, 162]
        })
        y_min = st.slider("Y-axis starts at:", 0, 150, 0, step=10, key="axis_slider")
        pct_distortion = round((162-152) / (162-y_min) * 100, 1) if y_min < 162 else 0
        fig = go.Figure(go.Bar(x=df["Quarter"], y=df["Revenue"], marker_color=PRIMARY))
        fig.update_yaxes(range=[y_min, 175])
        fig.update_layout(title=f"Revenue by Quarter (Y-axis starts at {y_min})",
                           height=360, margin=dict(t=40,b=20))
        st.plotly_chart(fig, use_container_width=True)

        if y_min > 100:
            st.metric("Visual exaggeration factor", f"{pct_distortion:.0f}×",
                       delta=f"Actual difference: ₹{162-152}L only")
            callout_mistake(
                f"With y-axis at {y_min}, the difference LOOKS enormous — "
                f"but the actual range is only ₹{162-152}L (6.5% growth). "
                "This is textbook truncated-axis distortion.",
                "Visual Lie Detected"
            )
        else:
            callout_manager(
                "With y-axis from 0: the actual variation is small — about 6.5% growth over 4 quarters. "
                "This is the honest story. The business is stable, not 'skyrocketing'.",
                "Honest Reading"
            )

        st.subheader("Dual Y-Axis Demo — Manufactured Correlation")
        months = list(range(1,13))
        revenue = [100 + i*3 + rng.normal(0,5) for i in months]
        temperature = [15 + i*2 + rng.normal(0,3) for i in months]
        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig2.add_trace(go.Scatter(x=months, y=revenue, name="Revenue (₹L)",
                                    line=dict(color=PRIMARY, width=2.5)), secondary_y=False)
        fig2.add_trace(go.Scatter(x=months, y=temperature, name="Temperature (°C)",
                                    line=dict(color=DANGER, width=2.5)), secondary_y=True)
        fig2.update_layout(title="Revenue & Temperature 'Move Together'? (Dual axis illusion)",
                            height=350)
        st.plotly_chart(fig2, use_container_width=True)
        callout_mistake(
            "Temperature and revenue are completely unrelated — but they appear to move together "
            "because we scaled the y-axes to overlap. This is a common technique in misleading reports.",
            "Dual Axis Illusion"
        )

    with tab_l:
        st.subheader("Activity 1: Fix the Broken Chart")
        st.write("Examine the chart below. Identify the problem and describe the fix.")
        df_bad = pd.DataFrame({"Product": ["A","B","C","D"], "Sales": [9810,9880,9850,9920]})
        fig_bad = go.Figure(go.Bar(x=df_bad["Product"], y=df_bad["Sales"],
                                    marker_color=[DANGER, DANGER, DANGER, SUCCESS]))
        fig_bad.update_yaxes(range=[9800, 9930])
        fig_bad.update_layout(title="Product D Has DRAMATICALLY Higher Sales!", height=300)
        st.plotly_chart(fig_bad, use_container_width=True)

        st.text_area("What is wrong? How would you fix it?", key="s3_lab_fix", height=80)
        if st.button("Show model answer", key="s3_fix_btn"):
            st.success(
                "**Problem:** Y-axis starts at 9800, making a <1% actual difference look like 100%.\n\n"
                "**Fix:** Start at 0. Actual range: 9810–9920 — all products are nearly identical. "
                "The correct insight: 'Sales highly consistent across all products.'"
            )
            fig_fix = go.Figure(go.Bar(x=df_bad["Product"], y=df_bad["Sales"],
                                        marker_color=PRIMARY))
            fig_fix.update_yaxes(range=[0, 10500])
            fig_fix.update_layout(title="All Products Perform Consistently (range: ₹9,810–9,920)", height=300)
            st.plotly_chart(fig_fix, use_container_width=True)

        st.markdown("---")
        st.subheader("Activity 2: Choose the Right Scale")
        scale_data = [
            ("Revenue data: ₹500 to ₹550 over 12 months — highlight subtle growth",
             ["Linear, zoomed to ₹480–570", "Log scale", "Start at 0, linear", "Square root scale"],
             "Linear, zoomed to ₹480–570",
             "This is a line chart (slope matters), so zooming in is acceptable. "
             "Starting at 0 would compress all variation into the top 10% of the chart."),
            ("Company valuations ranging from ₹50L (startup) to ₹5,000Cr (conglomerate)",
             ["Linear scale from 0", "Log scale", "Percentage scale", "Inverted scale"],
             "Log scale",
             "Data spanning 4 orders of magnitude (50L → 5000Cr) will have all small values "
             "invisible on a linear scale. Log scale makes all values readable."),
        ]
        for i, (sce, opts, correct, expl) in enumerate(scale_data):
            st.markdown(f"**Scenario {i+1}:** {sce}")
            ans = st.radio("", opts, key=f"s3_scale_{i}", horizontal=True, index=0)
            if st.button(f"Check ✓", key=f"s3_scale_check_{i}"):
                if ans == correct:
                    st.success(f"✅ {correct} — {expl}")
                elif ans is None:
                    st.warning("Please select an option.")
                else:
                    st.error(f"❌ Best: **{correct}** — {expl}")

    with tab_q:
        render_quiz(3)

    with tab_r:
        reflection_box(
            "Find a chart in any business news source or annual report. "
            "Examine its axes carefully. Is the scale honest? What story does the current axis tell "
            "vs what the honest axis would show?",
            key="refl_s3"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION 4 — Color, Emphasis & Attention
# ══════════════════════════════════════════════════════════════════════════════
def session_4():
    session_header(4)
    tab_c, tab_d, tab_l, tab_q, tab_r = st.tabs(
        ["📖 Concept", "📊 Demo", "🔬 Lab", "❓ Quiz", "🪞 Reflect"])

    with tab_c:
        st.subheader("Color Is Not Decoration")
        st.write("""
        Color in charts is a data encoding channel — not a styling tool.
        Every color choice should answer one question: does this help the reader
        decode the data faster and more accurately? If not, remove it.
        """)
        callout_insight(
            "Pre-attentive processing: the brain detects isolated color differences "
            "in under 250 ms — before conscious attention kicks in. "
            "Use this biological fact to direct the eye to what matters.",
            "Pre-Attentive Processing"
        )

        st.subheader("Three Types of Color Palette")
        pal_data = pd.DataFrame({
            "Palette Type": ["Sequential", "Diverging", "Categorical"],
            "When to Use": [
                "Ordered data — low to high (e.g., sales intensity, temperature, density)",
                "Data with a meaningful midpoint (e.g., profit/loss, above/below target)",
                "Unordered categories (e.g., product type, region, brand)"
            ],
            "Example Colors": [
                "Light blue → Dark blue (single hue gradient)",
                "Red ← zero → Blue (two-hue diverging)",
                "Blue, Orange, Green, Red (distinct, colorblind-safe)"
            ],
            "Avoid": [
                "Using for categorical data", "Using for data without a midpoint",
                "Using for ordered data"
            ]
        })
        st.dataframe(pal_data, use_container_width=True, hide_index=True)

        callout_mistake(
            "Using a rainbow (spectrum) palette for quantitative data is scientifically indefensible — "
            "it imposes false categorical boundaries and is uninterpretable to color-blind readers.",
            "Rainbow Palette Warning"
        )

        st.subheader("Designing for Color Blindness")
        st.write("""
        About **8% of men** and **0.5% of women** have color vision deficiency.
        Red-green color blindness (the most common form) makes red and green look identical.
        Design principles:
        - Use **blue-orange** or **blue-red** instead of red-green
        - Add **shape or pattern** as a redundant encoding channel
        - Test with a **greyscale export** — if the chart is unreadable, redesign it
        - Ensure sufficient **luminance contrast** between all elements
        """)
        callout_action(
            "If your chart cannot be read in greyscale, it relies too heavily on color. "
            "Always test a greyscale version before publishing.",
            "Greyscale Test"
        )

        st.subheader("The Accent Color Technique")
        st.write("""
        The most powerful color trick: **one standout color + grey**.
        Use your brand primary (or red) on the one bar/line that matters.
        Everything else goes grey. The eye goes exactly where you direct it.
        Result: no legend needed — the key finding is self-labelling.
        """)

    with tab_d:
        st.subheader("Accent vs Rainbow vs Grey")
        df = regional_sales().groupby("region")["sales"].sum().reset_index().sort_values("sales", ascending=False)
        mode = st.radio("Color mode:", ["Accent (Recommended)", "Rainbow (Avoid)", "All Same", "Greyscale"], horizontal=True)

        if mode == "Accent (Recommended)":
            colors = [DANGER if i == 0 else "#BDC3C7" for i in range(len(df))]
            title = f"{df.iloc[0]['region']} Leads — Invest Here First"
        elif mode == "Rainbow (Avoid)":
            colors = px.colors.qualitative.Plotly[:len(df)]
            title = "Regional Sales (Rainbow — Which bar matters?)"
        elif mode == "All Same":
            colors = [PRIMARY] * len(df)
            title = "Regional Sales (All same — reader must scan)"
        else:
            colors = ["#888888"] * len(df)
            title = "Greyscale — completely accessible, but no accent"

        fig = go.Figure(go.Bar(x=df["region"], y=df["sales"], marker_color=colors))
        fig.update_layout(title=title, height=330, yaxis_title="Sales (₹L)")
        st.plotly_chart(fig, use_container_width=True)
        if mode == "Accent (Recommended)":
            callout_manager(
                "The single red accent directs attention in <250ms. No legend needed. "
                "The grey bars provide reference context without visual competition.",
                "Why Accent Works"
            )

        st.subheader("Sequential Palette for Continuous Data")
        df2 = regional_sales().pivot_table(index="category", columns="region", values="sales")
        scale_choice = st.selectbox("Color scale:", ["Blues", "Greens", "RdBu_r", "Viridis", "Plasma"])
        fig2 = px.imshow(df2, color_continuous_scale=scale_choice,
                         text_auto=True, aspect="auto",
                         title="Sales Intensity — Which scale is most readable?")
        fig2.update_layout(height=340)
        st.plotly_chart(fig2, use_container_width=True)
        callout_insight(
            "Blues (sequential, single-hue) is most intuitive: 'darker = more.' "
            "RdBu_r (diverging) is best if there's a meaningful midpoint. "
            "Viridis/Plasma are colorblind-safe sequential options.",
            "Scale Selection Guide"
        )

    with tab_l:
        st.subheader("Activity 1: Choose the Right Palette")
        pal_q = [
            ("Patient wait times by ward — ranging from 3 minutes to 120 minutes",
             ["Sequential (light → dark)", "Diverging (red–white–blue)", "Categorical (distinct hues)"],
             "Sequential (light → dark)",
             "Wait time is ordered continuous data — longer wait = darker color is instantly intuitive."),
            ("Hospital wards performing above vs below 30-minute wait time target",
             ["Sequential (light → dark)", "Diverging (red–white–blue)", "Categorical (distinct hues)"],
             "Diverging (red–white–blue)",
             "The target is the meaningful midpoint. Above target = blue (good), below = red (bad). "
             "Diverging palettes are built for exactly this case."),
            ("Revenue breakdown by 6 product categories — no ordering or ranking intended",
             ["Sequential (light → dark)", "Diverging (red–white–blue)", "Categorical (distinct hues)"],
             "Categorical (distinct hues)",
             "Product categories have no inherent order. Categorical palettes assign distinct hues "
             "to each — important: stay colorblind-safe (e.g., Okabe-Ito, ColorBrewer Set2)."),
        ]
        for i, (q, opts, correct, expl) in enumerate(pal_q):
            st.markdown(f"**Scenario {i+1}:** {q}")
            ans = st.radio("Best palette:", opts, key=f"s4_pal_{i}", index=0)
            if st.button("Check ✓", key=f"s4_check_{i}"):
                if ans == correct:
                    st.success(f"✅ {correct} — {expl}")
                elif ans is None:
                    st.warning("Please select an option.")
                else:
                    st.error(f"❌ Best: **{correct}** — {expl}")
            st.markdown("")

        st.markdown("---")
        st.subheader("Activity 2: Redesign the Color Story")
        df3 = financial_expenses().groupby("category")["amount_lakhs"].sum().reset_index().sort_values("amount_lakhs", ascending=False)
        pal_choice = st.radio("Choose palette for this cost chart:",
                               ["Random colors", "All same blue", "Accent on highest cost"],
                               horizontal=True, key="s4_pal_act")
        if pal_choice == "Random colors":
            cols = px.colors.qualitative.Set3[:len(df3)]
        elif pal_choice == "All same blue":
            cols = [PRIMARY] * len(df3)
        else:
            cols = [DANGER if i == 0 else "#BDC3C7" for i in range(len(df3))]
        fig3 = go.Figure(go.Bar(x=df3["category"], y=df3["amount_lakhs"], marker_color=cols))
        fig3.update_layout(height=300, yaxis_title="Total Spend (₹L)",
                            title="Which color choice tells the clearest story?")
        st.plotly_chart(fig3, use_container_width=True)
        st.text_input("Write an action-oriented title for the 'accent on highest' version:",
                       key="s4_title_lab")
        if st.button("See model title", key="s4_model"):
            top_cat = df3.iloc[0]["category"]
            st.success(
                f"Model: '{top_cat} Accounts for the Largest Share of Costs — "
                f"A 10% Reduction Would Save ₹{df3.iloc[0]['amount_lakhs']*0.1:.0f}L'"
            )

    with tab_q:
        render_quiz(4)

    with tab_r:
        reflection_box(
            "Open any report from your work or studies. Identify one chart where the color choice "
            "could be improved. Describe the change you would make and the expected impact on readability.",
            key="refl_s4"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION 5 — Visualizing Amounts
# ══════════════════════════════════════════════════════════════════════════════
def session_5():
    session_header(5)
    tab_c, tab_d, tab_l, tab_q, tab_r = st.tabs(
        ["📖 Concept", "📊 Demo", "🔬 Lab", "❓ Quiz", "🪞 Reflect"])

    with tab_c:
        st.subheader("The Amount Chart Family")
        st.write("""
        Comparing amounts across categories is among the most common tasks in business analysis.
        The chart family for this job encodes quantity as bar length or dot position —
        the most accurate perceptual channels. Choosing the wrong family (pie chart for comparison,
        line chart for unordered categories) immediately weakens the story.
        """)
        chart_table = pd.DataFrame({
            "Chart": ["Vertical bar", "Horizontal bar", "Dot plot", "Lollipop",
                       "Grouped bar", "Stacked bar", "Small multiples"],
            "Best For": [
                "≤12 categories, time-based categories",
                "Long labels, many categories (>8)",
                "Long ranked lists, reducing visual clutter",
                "Ranked list, stylistic dot alternative",
                "Comparing sub-groups within categories (≤3 groups)",
                "Composition + comparison simultaneously",
                "Same chart for many groups (no clutter)"
            ],
            "Avoid When": [
                "Many categories (>12) — use horizontal",
                "Showing trend over time — use line",
                "Only 3–4 items — a bar is simpler",
                "Large datasets where dots overlap",
                "More than 3–4 groups per cluster",
                "More than 4–5 stack segments",
                "Only 2–3 groups — use grouped bar"
            ]
        })
        st.dataframe(chart_table, use_container_width=True, hide_index=True)
        callout_insight(
            "For comparing amounts, ALWAYS sort the bars. Ranked order (largest at top/left) "
            "reduces reading time from ~10 seconds to ~1 second for any audience.",
            "The Sorting Rule"
        )
        callout_mistake(
            "A 3D bar chart adds perspective distortion — bars at the back appear shorter. "
            "3D never adds information and always adds visual error. Never use it.",
            "3D Bar Chart: Never"
        )

        st.subheader("Data-Ink Ratio (Tufte's Principle)")
        st.write("""
        **Data-ink ratio = data ink ÷ total ink.**
        The higher the ratio, the better the chart. Every gridline, border, shadow,
        and decorative element that doesn't encode data is "chartjunk" and should be removed.
        """)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**❌ Low data-ink ratio**")
            st.markdown("""
- Heavy grey gridlines every 10 units
- 3D perspective effect
- Background image of bar graphs
- Drop shadows on every bar
- Decorative border around chart area
- 6 different colors (no encoding logic)
            """)
        with col2:
            st.markdown("**✅ High data-ink ratio**")
            st.markdown("""
- No gridlines (or light, minimal ones)
- Flat 2D bars
- White / transparent background
- No shadows
- Thin axis lines only
- One accent color + grey
            """)

    with tab_d:
        df = regional_sales().groupby("region")["sales"].sum().reset_index().sort_values("sales", ascending=False)
        chart_choice = st.radio("Compare chart styles:",
            ["Bar — Unsorted", "Bar — Sorted", "Dot Plot", "Lollipop", "Grouped Bar"],
            horizontal=True, key="s5_demo")

        if chart_choice == "Bar — Unsorted":
            df_unsorted = df.sample(frac=1, random_state=3)
            fig = px.bar(df_unsorted, x="region", y="sales",
                         title="Sales by Region (Unsorted — reader must rank mentally)",
                         color_discrete_sequence=["#95A5A6"])
        elif chart_choice == "Bar — Sorted":
            fig = px.bar(df, x="region", y="sales",
                         title="North Region Leads — immediately clear when sorted",
                         color_discrete_sequence=[PRIMARY])
        elif chart_choice == "Dot Plot":
            df_s = df.sort_values("sales")
            fig = go.Figure(go.Scatter(x=df_s["sales"], y=df_s["region"], mode="markers",
                                        marker=dict(size=16, color=PRIMARY)))
            fig.update_layout(title="Dot Plot — Same data, far less ink", xaxis_title="Sales (₹L)")
        elif chart_choice == "Lollipop":
            df_s = df.sort_values("sales")
            fig = go.Figure()
            for _, row in df_s.iterrows():
                fig.add_shape(type="line", x0=0, x1=row["sales"],
                               y0=row["region"], y1=row["region"],
                               line=dict(color="#BDC3C7", width=2))
            fig.add_trace(go.Scatter(x=df_s["sales"], y=df_s["region"], mode="markers",
                                      marker=dict(size=14, color=PRIMARY)))
            fig.update_layout(title="Lollipop — Minimum ink, maximum clarity", xaxis_title="Sales (₹L)")
        else:
            df2 = regional_sales().groupby(["region","category"])["sales"].sum().reset_index()
            top_cats = df2.groupby("category")["sales"].sum().nlargest(3).index
            df2 = df2[df2["category"].isin(top_cats)]
            fig = px.bar(df2, x="region", y="sales", color="category", barmode="group",
                         title="Grouped Bar — Compare categories within each region")

        fig.update_layout(height=340)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Small Multiples — Scale Without Clutter")
        df3 = regional_sales()
        top_cats = df3.groupby("category")["sales"].sum().nlargest(4).index.tolist()
        df3 = df3[df3["category"].isin(top_cats)]
        region_agg = df3.groupby(["region","category"])["sales"].sum().reset_index()
        fig_sm = px.bar(region_agg, x="category", y="sales", facet_col="region",
                         color_discrete_sequence=[PRIMARY],
                         title="Small Multiples — One Chart Per Region, Same Scale")
        fig_sm.update_layout(height=320)
        st.plotly_chart(fig_sm, use_container_width=True)
        callout_insight(
            "Small multiples use the same axis scale across all panels — "
            "so cross-panel comparison is accurate. This is Tufte's most powerful layout pattern.",
            "Small Multiples"
        )

    with tab_l:
        st.subheader("Activity 1: Build an Amount Story")
        df_m = regional_sales()
        metric = st.selectbox("Metric:", ["sales","target","growth_pct"], key="s5_metric")
        sort_order = st.radio("Sort order:", ["Descending","Ascending","Alphabetical"],
                               horizontal=True, key="s5_sort")
        highlight = st.checkbox("Highlight top performer", key="s5_hl")
        chart_style = st.radio("Chart style:", ["Bar","Dot","Lollipop"], horizontal=True, key="s5_style")

        agg = df_m.groupby("region")[metric].sum().reset_index()
        if sort_order == "Descending":
            agg = agg.sort_values(metric, ascending=False)
        elif sort_order == "Ascending":
            agg = agg.sort_values(metric, ascending=True)
        else:
            agg = agg.sort_values("region")

        colors = ([DANGER] + ["#BDC3C7"]*(len(agg)-1)) if highlight else [PRIMARY]*len(agg)

        if chart_style == "Bar":
            fig = go.Figure(go.Bar(x=agg["region"], y=agg[metric], marker_color=colors))
        elif chart_style == "Dot":
            fig = go.Figure(go.Scatter(x=agg[metric], y=agg["region"],
                                        mode="markers", marker=dict(size=16, color=colors)))
            fig.update_layout(xaxis_title=metric)
        else:
            fig = go.Figure()
            for j, row in agg.iterrows():
                fig.add_shape(type="line", x0=0, x1=row[metric],
                               y0=row["region"], y1=row["region"],
                               line=dict(color="#CCC", width=2))
            fig.add_trace(go.Scatter(x=agg[metric], y=agg["region"], mode="markers",
                                      marker=dict(size=14, color=colors)))
            fig.update_layout(xaxis_title=metric)

        fig.update_layout(title=f"Regional {metric.replace('_',' ').title()}", height=330)
        st.plotly_chart(fig, use_container_width=True)
        title_input = st.text_input("Write an action-oriented title:", key="s5_title")
        if title_input:
            callout_insight(f"Your title: '{title_input}' — Does it tell the reader what to DO, not just what the chart shows?", "Title Check")

        st.markdown("---")
        st.subheader("Activity 2: Chartjunk Hunt")
        st.write("Below is a 'heavily designed' chart. List every element that reduces the data-ink ratio.")
        junk_items = ["3D perspective on bars", "Rainbow colors (no encoding logic)",
                       "Background gradient image", "Bold gridlines every unit",
                       "Drop shadows on each bar", "Decorative border + logo watermark",
                       "Data labels on every bar (not just key values)"]
        st.multiselect("Select the chartjunk elements:", junk_items, key="s5_junk")
        if st.button("See all answers", key="s5_junk_reveal"):
            st.success("All items above are chartjunk — each adds ink without adding data. "
                        "Tufte's principle: every drop of ink must earn its place by encoding data.")

    with tab_q:
        render_quiz(5)

    with tab_r:
        reflection_box(
            "In your last business report or presentation, were your charts sorted? "
            "What insight would be immediately visible if bars were sorted and one was highlighted?",
            key="refl_s5"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION 6 — Distributions & Variation
# ══════════════════════════════════════════════════════════════════════════════
def session_6():
    session_header(6)
    tab_c, tab_d, tab_l, tab_q, tab_r = st.tabs(
        ["📖 Concept", "📊 Demo", "🔬 Lab", "❓ Quiz", "🪞 Reflect"])

    with tab_c:
        st.subheader("Why Averages Lie")
        st.write("""
        A hospital reports average patient wait time of 20 minutes — until you learn that
        90% wait 5 minutes and 10% wait 2 hours. The average conceals the distribution
        that drives actual experience, satisfaction, and safety.
        """)
        callout_insight(
            "Distribution is the truth. A mean is a convenient fiction. "
            "In business, the shape, spread, and tail behavior of data is usually "
            "more valuable than the central tendency alone.",
            "The Distribution Principle"
        )

        # Show how same mean can mask completely different distributions
        st.subheader("Same Mean, Completely Different Story")
        col1, col2, col3 = st.columns(3)
        x_normal = rng.normal(50, 5, 200)
        x_bimodal = np.concatenate([rng.normal(35, 5, 100), rng.normal(65, 5, 100)])
        x_skewed = rng.exponential(10, 200) + 30
        for col, data, label in zip([col1,col2,col3],
                                     [x_normal, x_bimodal, x_skewed],
                                     ["Symmetric (mean=50)", "Bimodal (mean≈50)", "Right-skewed (mean≈50)"]):
            fig = px.histogram(pd.DataFrame({"x":data}), x="x", nbins=20,
                                color_discrete_sequence=[PRIMARY])
            fig.add_vline(x=np.mean(data), line_dash="dash", line_color=DANGER,
                          annotation_text=f"Mean={np.mean(data):.0f}")
            fig.update_layout(height=200, margin=dict(t=20,b=10,l=10,r=10),
                               title=label, showlegend=False,
                               xaxis_title="", yaxis_title="")
            col.plotly_chart(fig, use_container_width=True)
        callout_mistake(
            "All three distributions have nearly identical means — but they represent completely "
            "different business realities. A bar chart of averages cannot distinguish them.",
            "Mean-Only Reporting is Insufficient"
        )

        st.subheader("Distribution Chart Family")
        distrib = pd.DataFrame({
            "Chart": ["Histogram", "Box plot", "Violin plot", "Strip plot", "Density plot", "ECDF"],
            "Shows": [
                "Frequency of values in bins — overall shape",
                "Median, IQR, min, max, outliers",
                "Distribution shape + box plot summary overlaid",
                "Every individual data point",
                "Smoothed probability density curve",
                "Cumulative probability — what % of values are ≤ X?"
            ],
            "Best For": [
                "Large datasets, seeing shape & skew (n > 50)",
                "Comparing distributions across groups",
                "When shape matters, not just summary stats",
                "Small datasets (n < 50) — show all points",
                "Comparing smooth shapes between groups",
                "Distribution comparisons for multiple groups"
            ]
        })
        st.dataframe(distrib, use_container_width=True, hide_index=True)

    with tab_d:
        df = customer_satisfaction()
        dept = st.multiselect("Select departments:", df["department"].unique().tolist(),
                               default=["Sales","Support","Delivery"], key="s6_dept")
        filtered = df[df["department"].isin(dept)] if dept else df
        chart_type = st.radio("Chart type:",
            ["Histogram","Box Plot","Violin","Strip Plot","ECDF"],
            horizontal=True, key="s6_chart")

        if chart_type == "Histogram":
            fig = px.histogram(filtered, x="nps_score", color="department",
                               nbins=20, barmode="overlay", opacity=0.7,
                               title="NPS Score Distribution by Department")
        elif chart_type == "Box Plot":
            fig = px.box(filtered, x="department", y="nps_score", color="department",
                         title="NPS — Median and Spread by Department",
                         points="outliers", notched=True)
        elif chart_type == "Violin":
            fig = px.violin(filtered, x="department", y="nps_score", color="department",
                            box=True, title="Full Distribution Shape — Violin Plot")
        elif chart_type == "Strip Plot":
            fig = px.strip(filtered, x="department", y="nps_score", color="department",
                           title="Every Data Point Visible — Strip Plot")
        else:
            fig = px.ecdf(filtered, x="nps_score", color="department",
                          title="ECDF — What % of customers score ≤ X?")

        fig.update_layout(height=400, showlegend=chart_type in ["Histogram","ECDF"])
        st.plotly_chart(fig, use_container_width=True)

        callout_manager(
            "Which department has the lowest median? Which has the most outliers? "
            "A bar chart of averages hides both. The distribution shows where management intervention is needed.",
            "Managerial Meaning"
        )

        # Live summary stats
        if dept:
            st.subheader("Quick Stats")
            stat_cols = st.columns(len(dept))
            for col, d in zip(stat_cols, dept):
                s = df[df["department"] == d]["nps_score"].describe()
                col.markdown(f"""
                **{d}**
                - Median: {s['50%']:.1f}
                - IQR: {s['25%']:.1f}–{s['75%']:.1f}
                - Min/Max: {s['min']:.0f}/{s['max']:.0f}
                """)

    with tab_l:
        st.subheader("Activity 1: Diagnose the Distribution")
        df2 = customer_satisfaction()
        dept_a = st.selectbox("Department A:", df2["department"].unique(), key="s6_da", index=0)
        dept_b = st.selectbox("Department B:", df2["department"].unique(), key="s6_db", index=1)
        sub = df2[df2["department"].isin([dept_a, dept_b])]

        fig2 = px.violin(sub, x="department", y="nps_score", color="department",
                         box=True, points="all",
                         title=f"Comparing {dept_a} vs {dept_b} — Full Distribution")
        fig2.update_layout(height=360, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

        col1, col2 = st.columns(2)
        for col, dept in zip([col1, col2], [dept_a, dept_b]):
            stats = df2[df2["department"] == dept]["nps_score"].describe()
            skew_val = df2[df2["department"] == dept]["nps_score"].skew()
            col.markdown(f"""
            **{dept}** statistics:
            - Mean: {stats['mean']:.1f} | Median: {stats['50%']:.1f}
            - IQR: {stats['25%']:.1f} – {stats['75%']:.1f}
            - Skewness: {skew_val:.2f}
            - n = {int(stats['count'])}
            """)

        st.text_area("Management recommendation based on the comparison:", key="s6_lab_rec", height=80)
        if st.button("See model recommendation", key="s6_model"):
            st.success(
                "Focus on the department with lower MEDIAN and higher SPREAD (wide IQR). "
                "High variance means inconsistent service delivery — investigate process variation "
                "before trying to raise the average. "
                "If one distribution is bimodal, you likely have two distinct customer cohorts needing different service strategies."
            )

        st.markdown("---")
        st.subheader("Activity 2: When to Use Which Chart")
        dist_q = [
            ("You have 8 data points — customer delivery times in hours",
             ["Histogram", "Box plot", "Strip plot (jitter)"],
             "Strip plot (jitter)",
             "With only 8 points, show all of them. Histogram bins become meaningless at n=8."),
            ("You are comparing NPS distributions for 5 departments and want to show shape",
             ["Violin plot", "Box plot", "Bar chart of means"],
             "Violin plot",
             "Violins show the full distribution shape (unimodal, bimodal, skewed) AND the median/IQR."),
        ]
        for i, (q, opts, correct, expl) in enumerate(dist_q):
            st.markdown(f"**{i+1}. {q}**")
            ans = st.radio("Best chart:", opts, key=f"s6_dist_{i}", index=0)
            if st.button("Check ✓", key=f"s6_dist_check_{i}"):
                if ans == correct:
                    st.success(f"✅ **{correct}** — {expl}")
                elif ans is None:
                    st.warning("Please select an option.")
                else:
                    st.error(f"❌ Best: **{correct}** — {expl}")

    with tab_q:
        render_quiz(6)

    with tab_r:
        reflection_box(
            "In your organization, where is a mean or average being used that might be hiding "
            "a problematic distribution? What chart would reveal the true story?",
            key="refl_s6"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION 7 — Proportions & Composition
# ══════════════════════════════════════════════════════════════════════════════
def session_7():
    session_header(7)
    tab_c, tab_d, tab_l, tab_q, tab_r = st.tabs(
        ["📖 Concept", "📊 Demo", "🔬 Lab", "❓ Quiz", "🪞 Reflect"])

    with tab_c:
        st.subheader("Parts of a Whole")
        st.write("""
        Composition charts answer: what fraction of the total does each part represent?
        They are about relative size — share, proportion, percentage.
        The most common mistake is reaching for a pie chart regardless of how many categories exist.
        """)
        comp_table = pd.DataFrame({
            "Chart": ["Pie", "Donut", "Stacked bar", "100% Stacked bar",
                       "Treemap", "Waterfall", "Mosaic (Marimekko)"],
            "Best For": [
                "≤5 categories, one dominant segment",
                "Same as pie, slightly cleaner center space",
                "Composition over time / across groups",
                "Change in proportions over time",
                "Hierarchical composition (parent > child)",
                "How a start value builds to a total",
                "Two categorical variables, proportional area"
            ],
            "Limit": [
                "Do not use >5 slices",
                "Do not use >5 slices",
                ">5 stack segments become unreadable",
                ">5 segments", "Works up to 20+ items",
                "Best for 6–10 components",
                "Needs careful labelling"
            ]
        })
        st.dataframe(comp_table, use_container_width=True, hide_index=True)

        callout_mistake(
            "A pie chart with 10+ slices is a visual disaster. "
            "Readers cannot compare angles or areas for more than 5–6 slices. "
            "Switch to a sorted horizontal bar chart immediately.",
            "The 12-Slice Pie Problem"
        )
        callout_insight(
            "A 100% stacked bar chart is the most powerful composition chart for business — "
            "it shows how the MIX of categories changes over time or across groups, not just totals.",
            "100% Stacked Bar Advantage"
        )

        st.subheader("When Pie Charts Are Actually Fine")
        st.write("""
        Pie charts are acceptable when:
        1. You have ≤5 categories
        2. One segment is clearly dominant (e.g., 70% market share)
        3. The exact percentages don't matter — only the dominance
        4. Your audience is non-technical and the chart is supplementary
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**✅ Acceptable pie (2 slices)**")
            fig = px.pie(values=[68, 32], names=["Digital", "Offline"],
                         color_discrete_sequence=[PRIMARY, "#BDC3C7"])
            fig.update_layout(height=220, margin=dict(t=10,b=10))
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Dominant segment is immediately clear.")
        with col2:
            st.markdown("**❌ Unacceptable pie (8 slices)**")
            vals = [25,18,15,12,10,8,7,5]
            nms = [f"Cat {i}" for i in range(1,9)]
            fig2 = px.pie(values=vals, names=nms)
            fig2.update_layout(height=220, margin=dict(t=10,b=10))
            st.plotly_chart(fig2, use_container_width=True)
            st.caption("Can you rank Cat 4 vs Cat 5 accurately? Unlikely.")

    with tab_d:
        df = financial_expenses()
        quarters = df["quarter"].unique().tolist()
        selected_q = st.multiselect("Select quarters:", quarters, default=quarters[-4:], key="s7_q")
        sub = df[df["quarter"].isin(selected_q)] if selected_q else df
        mode = st.radio("Chart type:",
            ["Pie (single quarter)","Stacked Bar","100% Stacked","Treemap","Waterfall"],
            horizontal=True, key="s7_mode")

        if mode == "Pie (single quarter)":
            q_choice = st.selectbox("Quarter:", selected_q if selected_q else quarters, key="s7_pie_q")
            pie_df = sub[sub["quarter"] == q_choice]
            fig = px.pie(pie_df, names="category", values="amount_lakhs",
                         title=f"Cost Composition — {q_choice}",
                         color_discrete_sequence=px.colors.qualitative.Set2)
        elif mode == "Stacked Bar":
            fig = px.bar(sub, x="quarter", y="amount_lakhs", color="category",
                         title="Cost Stack — How Total Spend Has Grown")
        elif mode == "100% Stacked":
            fig = px.bar(sub, x="quarter", y="amount_lakhs", color="category",
                         barnorm="percent",
                         title="Cost Mix — Proportions Across Quarters")
        elif mode == "Treemap":
            latest = df[df["quarter"] == df["quarter"].iloc[-1]]
            fig = px.treemap(latest, path=["category"], values="amount_lakhs",
                             title=f"Cost Treemap — {df['quarter'].iloc[-1]}")
        else:
            # Waterfall
            cat_totals = df.groupby("category")["amount_lakhs"].sum().sort_values(ascending=False)
            total = cat_totals.sum()
            wf = pd.DataFrame({"category": cat_totals.index.tolist() + ["Total"],
                                "amount": cat_totals.values.tolist() + [total],
                                "type": ["relative"]*len(cat_totals) + ["total"]})
            fig = go.Figure(go.Waterfall(
                x=wf["category"], y=wf["amount"],
                measure=wf["type"],
                connector={"line": {"color": "grey"}},
                increasing={"marker": {"color": PRIMARY}},
                totals={"marker": {"color": ACCENT}},
            ))
            fig.update_layout(title="Cost Waterfall — How Each Category Builds to Total Spend",
                               showlegend=False)

        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        callout_manager(
            "100% stacked bar: does the cost MIX change across quarters, or just the total? "
            "This is a different strategic question than 'how much did we spend?'",
            "Managerial Meaning"
        )

    with tab_l:
        st.subheader("Activity 1: Build a Budget Story")
        df2 = financial_expenses()
        cat_choice = st.multiselect("Focus categories:",
            df2["category"].unique(), default=["Salaries","Marketing"], key="s7_cats")
        chart_mode = st.radio("View as:", ["Grouped bars","100% stacked","Treemap"], horizontal=True, key="s7_lab_mode")
        sub2 = df2[df2["category"].isin(cat_choice)] if cat_choice else df2

        if chart_mode == "Grouped bars":
            fig2 = px.bar(sub2, x="quarter", y="amount_lakhs", color="category",
                          barmode="group", title="Cost Trend by Category")
        elif chart_mode == "100% stacked":
            fig2 = px.bar(sub2, x="quarter", y="amount_lakhs", color="category",
                          barnorm="percent", title="Category Mix over Time")
        else:
            latest2 = df2[df2["quarter"] == df2["quarter"].iloc[-1]]
            latest2 = latest2[latest2["category"].isin(cat_choice)] if cat_choice else latest2
            fig2 = px.treemap(latest2, path=["category"], values="amount_lakhs")

        fig2.update_layout(height=320)
        st.plotly_chart(fig2, use_container_width=True)
        st.text_input("Write an insight title for this chart:", key="s7_insight_title")
        st.text_area("Managerial recommendation:", key="s7_rec", height=60)

        st.markdown("---")
        st.subheader("Activity 2: Pie or Bar?")
        q_pie = [
            ("7 product categories — compare market share",
             ["Pie chart", "Sorted horizontal bar chart"],
             "Sorted horizontal bar chart",
             "7 slices exceed the 5-slice limit for readable pie charts. A bar chart enables accurate rank comparison."),
            ("4 payment methods — show which dominates at a glance (informal slide)",
             ["Pie chart", "Sorted horizontal bar chart"],
             "Pie chart",
             "4 categories is within the acceptable range, especially if one clearly dominates. Context matters."),
        ]
        for i, (q, opts, correct, expl) in enumerate(q_pie):
            st.markdown(f"**{i+1}.** {q}")
            ans = st.radio("", opts, key=f"s7_pie_{i}", horizontal=True, index=0)
            if st.button("Check ✓", key=f"s7_pie_check_{i}"):
                if ans == correct:
                    st.success(f"✅ **{correct}** — {expl}")
                elif ans is None:
                    st.warning("Please select an option.")
                else:
                    st.error(f"❌ Best: **{correct}** — {expl}")

        st.download_button("⬇ Download expense data",
                           df2.to_csv(index=False).encode(), "session7_expenses.csv", "text/csv")

    with tab_q:
        render_quiz(7)

    with tab_r:
        reflection_box(
            "Look at a dashboard or report you use regularly. Where are pie charts used? "
            "Could a sorted bar or 100% stacked bar tell the story more clearly?",
            key="refl_s7"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  SESSION 8 — Chart Critique & Redesign
# ══════════════════════════════════════════════════════════════════════════════
def session_8():
    session_header(8)
    tab_c, tab_d, tab_l, tab_q, tab_r = st.tabs(
        ["📖 Concept", "📊 Demo", "🔬 Lab", "❓ Quiz", "🪞 Reflect"])

    with tab_c:
        st.subheader("Chart Critique as a Professional Skill")
        st.write("""
        Before creating charts, analysts must be able to diagnose weak ones.
        Chart critique is not about finding fault — it is about identifying
        the gap between what a chart shows and what its audience needs to decide.
        """)
        callout_insight(
            "A chart critique always starts with purpose: "
            "'What business question is this trying to answer?' "
            "If the chart fails to answer that question clearly and honestly, it needs redesign.",
            "Starting Point"
        )

        problems = {
            "Truncated y-axis": "Bar chart doesn't start at zero → exaggerates differences",
            "Wrong chart type": "Pie with 12 slices, or line for unordered categories",
            "3D distortion": "3D skews area/angle perception — front bars appear shorter",
            "Color overload": "Every bar a different color with no encoding logic",
            "Dual-axis illusion": "Two y-axes manufactured to imply false correlation",
            "Over-labelling": "Every point labeled → visual noise drowns the trend",
            "Irregular time scale": "Unequal intervals make flat trends look like acceleration",
            "Spaghetti chart": "10+ lines, equal visual weight — impossible to follow",
            "Missing zero context": "Rate of change looks large due to compressed axis",
            "Cherry-picked window": "Time axis starts at the peak to hide prior decline"
        }
        for problem, desc in problems.items():
            with st.expander(f"🔴 {problem}"):
                st.write(desc)

        callout_action(
            "5-step redesign protocol:\n"
            "1. Identify the business question\n"
            "2. Find the problematic encoding\n"
            "3. Choose the correct chart type\n"
            "4. Fix scale, color, and annotation\n"
            "5. Rewrite the title as an insight",
            "Redesign Protocol"
        )

    with tab_d:
        st.subheader("Before-After Redesign Clinic")
        case = st.selectbox("Select redesign case:", [
            "3D Pie → Sorted Bar",
            "Truncated Axis → Honest Axis",
            "Spaghetti Line → Highlighted Line",
            "Rainbow Colors → Accent Color",
            "Wrong Chart Type → Right Chart Type"
        ], key="s8_case")

        categories = ["Product A","Product B","Product C","Product D","Product E"]
        values = [35, 25, 20, 12, 8]
        col1, col2 = st.columns(2)

        if case == "3D Pie → Sorted Bar":
            with col1:
                st.markdown("❌ **Before: 3D Pie**")
                fig_b = go.Figure(go.Pie(labels=categories, values=values, pull=[0.1]*5))
                fig_b.update_layout(height=290, title="Sales Mix (Hard to Compare)")
                st.plotly_chart(fig_b, use_container_width=True)
                callout_mistake("Can you rank Products C vs D accurately? Most people cannot.", "Problem")
            with col2:
                st.markdown("✅ **After: Sorted Horizontal Bar**")
                df_s = pd.DataFrame({"Product":categories,"Share":values}).sort_values("Share", ascending=True)
                colors = [DANGER if p == "Product A" else "#BDC3C7" for p in df_s["Product"]]
                fig_a = go.Figure(go.Bar(x=df_s["Share"], y=df_s["Product"],
                                          orientation="h", marker_color=colors))
                fig_a.update_layout(height=290, title="Product A Dominates — 35% of Sales",
                                     xaxis_title="Market Share (%)")
                st.plotly_chart(fig_a, use_container_width=True)
                callout_insight("Rank order is instantly readable. The title states the finding.", "Fix")

        elif case == "Truncated Axis → Honest Axis":
            revenue = [152,158,155,162,159,165]
            quarters = [f"Q{i+1}" for i in range(6)]
            with col1:
                st.markdown("❌ **Before: Truncated Axis**")
                fig_b = go.Figure(go.Bar(x=quarters, y=revenue, marker_color=DANGER))
                fig_b.update_yaxes(range=[148,170])
                fig_b.update_layout(height=290, title="Revenue EXPLODING Upward!")
                st.plotly_chart(fig_b, use_container_width=True)
            with col2:
                st.markdown("✅ **After: Zero Baseline**")
                fig_a = go.Figure(go.Bar(x=quarters, y=revenue, marker_color=PRIMARY))
                fig_a.update_yaxes(range=[0,200])
                fig_a.update_layout(height=290, title="Revenue Gradually Growing (+8.5%)")
                st.plotly_chart(fig_a, use_container_width=True)

        elif case == "Spaghetti Line → Highlighted Line":
            months = list(range(1,13))
            lines_data = {f"Line {i}": rng.normal(100+i*2, 15, 12).tolist() for i in range(8)}
            lines_data["Key Product"] = [90,95,100,110,125,140,138,145,155,160,170,182]
            with col1:
                st.markdown("❌ **Before: 9 Equal-Weight Lines**")
                fig_b = go.Figure()
                for name, vals in lines_data.items():
                    fig_b.add_trace(go.Scatter(x=months, y=vals, name=name, mode="lines"))
                fig_b.update_layout(height=290, title="Which product matters? (Unreadable)", showlegend=False)
                st.plotly_chart(fig_b, use_container_width=True)
            with col2:
                st.markdown("✅ **After: Accent + Fade**")
                fig_a = go.Figure()
                for name, vals in lines_data.items():
                    if name == "Key Product":
                        fig_a.add_trace(go.Scatter(x=months, y=vals, name=name,
                                                    mode="lines+markers",
                                                    line=dict(color=DANGER, width=3)))
                    else:
                        fig_a.add_trace(go.Scatter(x=months, y=vals, showlegend=False,
                                                    mode="lines",
                                                    line=dict(color="#E0E0E0", width=1)))
                fig_a.add_annotation(x=12, y=182, text="Key Product: +102%",
                                     showarrow=True, arrowhead=2, ax=-60, ay=-30,
                                     font=dict(color=DANGER, size=12))
                fig_a.update_layout(height=290, title="Key Product Outperforms All — 102% Growth")
                st.plotly_chart(fig_a, use_container_width=True)

        elif case == "Rainbow Colors → Accent Color":
            df_r = regional_sales().groupby("region")["sales"].sum().reset_index().sort_values("sales", ascending=False)
            with col1:
                st.markdown("❌ **Before: Rainbow**")
                fig_b = px.bar(df_r, x="region", y="sales",
                                color="region", title="Which region should we invest in?")
                fig_b.update_layout(height=290, showlegend=False)
                st.plotly_chart(fig_b, use_container_width=True)
            with col2:
                st.markdown("✅ **After: Accent + Grey**")
                acc_colors = [DANGER if i==0 else "#BDC3C7" for i in range(len(df_r))]
                fig_a = go.Figure(go.Bar(x=df_r["region"], y=df_r["sales"], marker_color=acc_colors))
                fig_a.update_layout(height=290,
                                     title=f"{df_r.iloc[0]['region']} Leads — Double Down Here")
                st.plotly_chart(fig_a, use_container_width=True)

        else:  # Wrong chart type
            df_trend = retail_sales()[["month","revenue_lakhs"]].head(12)
            df_trend["month_str"] = df_trend["month"].dt.strftime("%b")
            with col1:
                st.markdown("❌ **Before: Bar for Continuous Time Series**")
                fig_b = px.bar(df_trend, x="month_str", y="revenue_lakhs",
                                title="Revenue by Month (Bar — hides the trend)")
                fig_b.update_layout(height=290)
                st.plotly_chart(fig_b, use_container_width=True)
            with col2:
                st.markdown("✅ **After: Line for Continuous Time Series**")
                fig_a = px.line(df_trend, x="month_str", y="revenue_lakhs",
                                 markers=True, color_discrete_sequence=[PRIMARY],
                                 title="Revenue Growing Consistently — 50% YTD Increase")
                fig_a.update_layout(height=290)
                st.plotly_chart(fig_a, use_container_width=True)

    with tab_l:
        st.subheader("Activity 1: Critique Worksheet")
        df3 = financial_expenses().groupby("category")["amount_lakhs"].sum().reset_index()
        fig_crit = px.pie(df3, names="category", values="amount_lakhs",
                           title="Cost Breakdown")
        fig_crit.update_traces(pull=[0.05]*len(df3), textposition="inside")
        fig_crit.update_layout(height=320)
        st.plotly_chart(fig_crit, use_container_width=True)

        st.markdown("**Complete the critique:**")
        st.text_input("1. Business question this chart tries to answer:", key="s8_q1")
        st.text_input("2. Main design problem:", key="s8_q2")
        st.text_input("3. Better chart type:", key="s8_q3")
        st.text_input("4. Action-oriented title for the redesigned chart:", key="s8_q4")
        st.text_area("5. What would a manager do differently after seeing the redesigned version?", key="s8_q5", height=60)

        if st.button("Show model answers", key="s8_model"):
            top = df3.sort_values("amount_lakhs", ascending=False).iloc[0]["category"]
            st.success(f"""
**1.** Which cost category dominates our expense structure?

**2.** Pie with 6 segments — angle comparison fails beyond 5 slices; dominant category unclear at a glance.

**3.** Sorted horizontal bar chart (descending).

**4.** '{top} Is the Largest Cost Driver — Cut by 10% to Save ₹{df3.sort_values('amount_lakhs',ascending=False).iloc[0]['amount_lakhs']*0.1:.0f}L'

**5.** The manager can immediately see which category to investigate for cost reduction — without mentally comparing slice areas.
            """)

        st.markdown("---")
        st.subheader("Activity 2: Redesign Challenge")
        st.write("Describe (in words) your redesign for the chart above.")
        redesign_steps = ["Identify the business question", "Choose chart type",
                           "Fix the axis/scale", "Redesign the color", "Rewrite the title"]
        for step in redesign_steps:
            st.text_input(f"Step: {step}", key=f"s8_redesign_{step.replace(' ','_')}")

    with tab_q:
        render_quiz(8)

    with tab_r:
        reflection_box(
            "Find a weak chart in any published report. "
            "Apply the 5-step redesign protocol. What is the single most impactful change?",
            key="refl_s8"
        )
