"""
quiz_bank.py  — Expanded quiz bank: 5+ questions per session (80+ total).
All questions: index=None so no option is pre-selected.
Types: MCQ, TrueFalse, Scenario
"""

QUIZ_BANK = [

    # ══════════════════════════════════════════════════════════════════════
    #  SESSION 1 — Why Visualization Matters
    # ══════════════════════════════════════════════════════════════════════
    {
        "session": 1, "clo": "CLO1", "type": "MCQ",
        "q": "A manager scans a 200-row table to find quarterly sales trends. What is the PRIMARY limitation?",
        "options": ["Too many decimal places", "Tables cannot reveal trends over time", "Data is unsorted", "Colors are absent"],
        "answer": "Tables cannot reveal trends over time",
        "explanation": "Tables are designed for precise look-up, not pattern recognition. A line chart immediately surfaces trends, outliers, and seasonality that rows of numbers hide."
    },
    {
        "session": 1, "clo": "CLO1", "type": "MCQ",
        "q": "Data storytelling in business combines which three elements?",
        "options": ["Tables, dashboards, and reports", "Data, visuals, and narrative", "Charts, colors, and fonts", "Excel, PowerPoint, and Tableau"],
        "answer": "Data, visuals, and narrative",
        "explanation": "Effective data storytelling requires all three: data (evidence), visuals (encoding), and narrative (context + so-what). Any missing element weakens the story."
    },
    {
        "session": 1, "clo": "CLO1", "type": "TrueFalse",
        "q": "A well-designed chart completely eliminates the need for any written or spoken explanation.",
        "options": ["True", "False"],
        "answer": "False",
        "explanation": "Even the best chart benefits from a clear title, annotation, and verbal context. Charts are one layer — they work best alongside narrative, not instead of it."
    },
    {
        "session": 1, "clo": "CLO1", "type": "Scenario",
        "q": "A VP presents 14 slides with 3 charts each. The audience leaves confused, with no clear action. What is most likely the core problem?",
        "options": ["Not enough data was presented", "Too many charts without a connecting narrative or recommendation", "The charts used the wrong software", "The audience was not technical enough"],
        "answer": "Too many charts without a connecting narrative or recommendation",
        "explanation": "Data dumping — showing all available data without a story thread — overwhelms rather than informs. The fix: one key message, then 3-5 supporting visuals with a clear recommendation."
    },
    {
        "session": 1, "clo": "CLO1", "type": "MCQ",
        "q": "In the DIKW hierarchy applied to visualization, what does a good chart help a manager do?",
        "options": ["Collect more raw data", "Compress the journey from data to a wise decision", "Replace analytical thinking", "Present more numbers per slide"],
        "answer": "Compress the journey from data to a wise decision",
        "explanation": "DIKW: Data → Information → Knowledge → Wisdom. Good visualization accelerates this progression, helping managers reach actionable understanding quickly."
    },
    {
        "session": 1, "clo": "CLO1", "type": "MCQ",
        "q": "Approximately how many bits per second does the human visual system transmit to the brain?",
        "options": ["1,000 bps", "100,000 bps", "10,000,000 bps", "1,000,000,000 bps"],
        "answer": "10,000,000 bps",
        "explanation": "The visual system transmits roughly 10 million bits per second — more than all other senses combined. Charts exploit this high-bandwidth channel; tables do not."
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SESSION 2 — Mapping Data to Visual Forms
    # ══════════════════════════════════════════════════════════════════════
    {
        "session": 2, "clo": "CLO2", "type": "MCQ",
        "q": "You need to compare exact sales figures across 8 product categories for one month. Best chart?",
        "options": ["Pie chart", "Bar chart", "Scatter plot", "Heat map"],
        "answer": "Bar chart",
        "explanation": "Bar charts encode quantities as bar length — the most accurately perceived channel for comparing discrete categories. Pie charts become unreadable beyond 5 slices."
    },
    {
        "session": 2, "clo": "CLO2", "type": "MCQ",
        "q": "According to Cleveland & McGill (1984), which visual encoding channel is MOST accurately perceived?",
        "options": ["Color hue", "Area", "Position along a common scale", "Angle"],
        "answer": "Position along a common scale",
        "explanation": "Empirical research confirms that humans most accurately judge position on a common axis. Color hue, area, and angle are progressively weaker encodings for quantitative comparisons."
    },
    {
        "session": 2, "clo": "CLO2", "type": "MCQ",
        "q": "A scatter plot primarily encodes data using which two channels?",
        "options": ["Color and size", "X-position and Y-position", "Length and angle", "Area and texture"],
        "answer": "X-position and Y-position",
        "explanation": "Scatter plots exploit the most accurate encoding channel (position) for both variables, making them ideal for exploring relationships between two quantitative variables."
    },
    {
        "session": 2, "clo": "CLO2", "type": "TrueFalse",
        "q": "For showing how revenue changed over 24 months, a bar chart is always preferable to a line chart.",
        "options": ["True", "False"],
        "answer": "False",
        "explanation": "Line charts are superior for continuous time-series data because they emphasize slope and trend (rate of change). Bar charts are better for comparing discrete amounts across categories."
    },
    {
        "session": 2, "clo": "CLO2", "type": "Scenario",
        "q": "A team wants to show the relationship between employee training hours and sales performance across 80 employees. What chart is most appropriate?",
        "options": ["Stacked bar chart", "Pie chart", "Scatter plot", "Box plot"],
        "answer": "Scatter plot",
        "explanation": "With two continuous variables (training hours, sales performance) and individual data points, a scatter plot is ideal. You can add color to encode a third variable (e.g., department)."
    },
    {
        "session": 2, "clo": "CLO2", "type": "MCQ",
        "q": "Which data type is best visualized using a histogram?",
        "options": ["Nominal categories like product names", "Continuous quantitative data like patient ages", "Ranked survey responses", "Binary yes/no outcomes"],
        "answer": "Continuous quantitative data like patient ages",
        "explanation": "Histograms show the frequency distribution of continuous data — the shape, spread, skew, and presence of multiple modes. They require interval or ratio data, not categories."
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SESSION 3 — Axes, Scales & Coordinate Systems
    # ══════════════════════════════════════════════════════════════════════
    {
        "session": 3, "clo": "CLO2", "type": "MCQ",
        "q": "A bar chart's y-axis starts at 50 instead of 0. What is the likely visual effect?",
        "options": ["Chart becomes easier to read", "Small differences appear much larger than they really are", "Data becomes more accurate", "Trend lines are clearer"],
        "answer": "Small differences appear much larger than they really are",
        "explanation": "Truncating a bar chart axis removes the reference baseline. A 10% actual difference can look like 200% — a classic misleading technique used to exaggerate growth or decline."
    },
    {
        "session": 3, "clo": "CLO2", "type": "TrueFalse",
        "q": "For a line chart of stock prices, it is acceptable NOT to start the y-axis at zero.",
        "options": ["True", "False"],
        "answer": "True",
        "explanation": "Line charts encode change in slope, not bar length. Zooming in on the relevant range is often the right call. The zero-baseline rule applies strictly to bar/column charts."
    },
    {
        "session": 3, "clo": "CLO2", "type": "MCQ",
        "q": "Data spans from ₹500 to ₹5,000,000. Which axis scale prevents small values from being invisible?",
        "options": ["Linear scale", "Logarithmic scale", "Percentage scale", "Inverted scale"],
        "answer": "Logarithmic scale",
        "explanation": "A log scale spaces orders of magnitude evenly (10, 100, 1,000, 10,000), making data that spans multiple magnitudes visible and comparable across the full range."
    },
    {
        "session": 3, "clo": "CLO2", "type": "Scenario",
        "q": "A TV news chart shows party vote shares of 32%, 31%, 30%, 29% using a bar chart with y-axis from 28% to 33%. What is the problem?",
        "options": ["Too many parties are shown", "The truncated axis makes a near-tie look like a landslide", "The chart should use a line instead", "The axis labels are missing units"],
        "answer": "The truncated axis makes a near-tie look like a landslide",
        "explanation": "A 3-percentage-point range looks like one party dominates another. Starting at 0% shows all four parties with nearly equal support — the truthful story. This technique is common in political media."
    },
    {
        "session": 3, "clo": "CLO2", "type": "MCQ",
        "q": "Dual y-axes on a chart (one scale per line) are generally considered problematic because:",
        "options": ["They look old-fashioned", "The reader can falsely perceive any two unrelated variables as correlated", "They require two chart types", "They cannot be exported to PDF"],
        "answer": "The reader can falsely perceive any two unrelated variables as correlated",
        "explanation": "By independently scaling two axes, a dual-axis chart can make any two completely unrelated time series appear to move together. This is a common misleading technique."
    },
    {
        "session": 3, "clo": "CLO2", "type": "TrueFalse",
        "q": "Using a square root scale on an axis is a legitimate choice when data is right-skewed but does not span multiple orders of magnitude.",
        "options": ["True", "False"],
        "answer": "True",
        "explanation": "Square root transformations are useful for moderately skewed data (e.g., income distributions, city population). They compress large values less aggressively than log scales."
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SESSION 4 — Color, Emphasis & Attention
    # ══════════════════════════════════════════════════════════════════════
    {
        "session": 4, "clo": "CLO2", "type": "MCQ",
        "q": "Which color palette is most appropriate for showing profit/loss deviation from a zero baseline?",
        "options": ["Sequential (light-to-dark blue)", "Diverging (red–white–blue)", "Categorical (distinct hues)", "Rainbow (spectrum)"],
        "answer": "Diverging (red–white–blue)",
        "explanation": "Diverging palettes have a neutral midpoint (white or light) and saturate toward two distinct hues on either end. They are ideal for data with a meaningful zero — profits vs losses, above vs below target."
    },
    {
        "session": 4, "clo": "CLO2", "type": "TrueFalse",
        "q": "A rainbow (spectrum) color palette is a scientifically valid choice for encoding ordered quantitative data.",
        "options": ["True", "False"],
        "answer": "False",
        "explanation": "Rainbow palettes impose artificial categorical boundaries through perceptual steps in the spectrum. They are also unreadable for ~8% of men with red-green color blindness. Use sequential or diverging palettes instead."
    },
    {
        "session": 4, "clo": "CLO2", "type": "MCQ",
        "q": "Pre-attentive processing is relevant to visualization because:",
        "options": ["It requires focused concentration to decode charts", "The brain detects color differences in under 250 ms before conscious attention", "Colors must be bold to be perceived", "It only works with bar charts"],
        "answer": "The brain detects color differences in under 250 ms before conscious attention",
        "explanation": "Pre-attentive features (color, shape, size, orientation) are processed instantly by the visual cortex. A single colored bar in a grey chart directs the eye in milliseconds — before the reader starts reading."
    },
    {
        "session": 4, "clo": "CLO2", "type": "Scenario",
        "q": "A heat map uses red-green coloring to show high vs low performance. What immediate problem does this create?",
        "options": ["Red and green clash visually for everyone", "8% of men cannot distinguish red from green — key insights are invisible", "Green should always mean 'stop'", "Red maps only work in financial charts"],
        "answer": "8% of men cannot distinguish red from green — key insights are invisible",
        "explanation": "Red-green color blindness (deuteranopia/protanopia) is the most common form, affecting ~8% of men. The entire signal disappears for these readers. Use blue-orange instead."
    },
    {
        "session": 4, "clo": "CLO2", "type": "MCQ",
        "q": "You want to highlight the single highest-revenue region in a bar chart while graying out the others. This technique is called:",
        "options": ["Rainbow encoding", "Accent color (pop) technique", "Sequential scaling", "Saturation mapping"],
        "answer": "Accent color (pop) technique",
        "explanation": "Using one standout color (typically red, orange, or your brand primary) against neutral grey bars directs the eye instantly to the most important value without distraction."
    },
    {
        "session": 4, "clo": "CLO2", "type": "TrueFalse",
        "q": "If a chart cannot be read in greyscale, it relies too heavily on color and likely needs redesign.",
        "options": ["True", "False"],
        "answer": "True",
        "explanation": "Greyscale testing is a standard accessibility check. If critical information disappears when color is removed, the chart has a redundancy failure — add shape, pattern, or direct labels as backup channels."
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SESSION 5 — Visualizing Amounts
    # ══════════════════════════════════════════════════════════════════════
    {
        "session": 5, "clo": "CLO2", "type": "MCQ",
        "q": "You are ranking 15 sales regions by revenue. The category names are long. Best chart?",
        "options": ["Vertical bar chart", "Horizontal bar chart", "Pie chart", "Radar chart"],
        "answer": "Horizontal bar chart",
        "explanation": "Horizontal bars allow long labels to run left-to-right without rotation or truncation. They are also easier to rank visually when there are more than 8 categories."
    },
    {
        "session": 5, "clo": "CLO2", "type": "TrueFalse",
        "q": "Sorting bars in descending order (highest at top/left) always improves the readability of a bar chart.",
        "options": ["True", "False"],
        "answer": "True",
        "explanation": "Sorted order allows the reader to instantly identify the top and bottom performers. An unsorted bar chart forces the eye to scan randomly and reconstruct a ranking mentally."
    },
    {
        "session": 5, "clo": "CLO2", "type": "MCQ",
        "q": "Edward Tufte's 'data-ink ratio' principle says a well-designed chart should:",
        "options": ["Use as many colors as possible", "Maximize the proportion of ink that encodes data, removing decorative elements", "Always include a 3D perspective", "Have a dark background for visual impact"],
        "answer": "Maximize the proportion of ink that encodes data, removing decorative elements",
        "explanation": "Tufte's principle: every drop of ink should earn its place by encoding data. Gridlines, shadows, 3D effects, and decorative borders are 'chartjunk' that reduces the data-ink ratio."
    },
    {
        "session": 5, "clo": "CLO2", "type": "Scenario",
        "q": "A grouped bar chart shows revenue for 5 products across 6 regions, creating 30 bars in one chart. What is the problem and the fix?",
        "options": ["No problem — more data is always better", "30 bars create visual clutter; split into a small multiple or faceted view by region", "Use a single stacked bar instead", "Add a 3D perspective to separate the groups"],
        "answer": "30 bars create visual clutter; split into a small multiple or faceted view by region",
        "explanation": "Grouped bars become unreadable beyond 3–4 groups per cluster. Small multiples (one chart per region) preserve comparison while maintaining clarity — each chart stays uncluttered."
    },
    {
        "session": 5, "clo": "CLO2", "type": "MCQ",
        "q": "A lollipop chart is primarily an improvement over a bar chart in which situation?",
        "options": ["When data is categorical", "When there are many ranked items and the bar width adds unnecessary visual weight", "When the data includes negative values", "When comparing parts of a whole"],
        "answer": "When there are many ranked items and the bar width adds unnecessary visual weight",
        "explanation": "Lollipop charts (dot + thin stem) reduce ink without losing the ranked comparison. They are particularly effective for long ranked lists (15+ items) where bar width creates a dense wall of color."
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SESSION 6 — Distributions & Variation
    # ══════════════════════════════════════════════════════════════════════
    {
        "session": 6, "clo": "CLO2", "type": "MCQ",
        "q": "A hospital reports 'average wait time: 15 minutes.' Why is this a potentially misleading statistic?",
        "options": ["It uses the wrong unit of time", "The mean hides the distribution — 90% may wait 5 min while 10% wait 2 hours", "Averages are only valid for normally distributed data", "The sample size is too small"],
        "answer": "The mean hides the distribution — 90% may wait 5 min while 10% wait 2 hours",
        "explanation": "The mean collapses a full distribution into one number. A bimodal or right-skewed distribution can produce an average that doesn't represent any real experience. Always show the distribution."
    },
    {
        "session": 6, "clo": "CLO2", "type": "MCQ",
        "q": "A box plot shows the interquartile range (IQR). What does this represent?",
        "options": ["The range between the minimum and maximum", "The middle 50% of the data (25th to 75th percentile)", "The standard deviation multiplied by 1.5", "The confidence interval of the mean"],
        "answer": "The middle 50% of the data (25th to 75th percentile)",
        "explanation": "The IQR is the box in a box plot — from Q1 (25th percentile) to Q3 (75th percentile). It captures the 'central bulk' of the data and is resistant to outliers, unlike range."
    },
    {
        "session": 6, "clo": "CLO2", "type": "TrueFalse",
        "q": "A violin plot is superior to a box plot when the shape of the distribution (e.g., bimodality) is important.",
        "options": ["True", "False"],
        "answer": "True",
        "explanation": "Violin plots add kernel density estimation around the box plot, revealing whether the distribution is unimodal, bimodal, or skewed — information a box plot hides by design."
    },
    {
        "session": 6, "clo": "CLO2", "type": "Scenario",
        "q": "Two stores each have mean customer satisfaction of 7.2/10. Store A's scores cluster tightly around 7. Store B has many 9s and many 4s. What chart reveals this difference best?",
        "options": ["Bar chart of means", "Pie chart of score categories", "Violin or box plot of the score distributions", "Single KPI card showing 7.2"],
        "answer": "Violin or box plot of the score distributions",
        "explanation": "The means are identical, but the distributions are completely different. A violin/box plot immediately reveals Store B's bimodal distribution — some delighted customers, some very unhappy. This demands a different management response."
    },
    {
        "session": 6, "clo": "CLO2", "type": "MCQ",
        "q": "For a dataset with 12 data points, which visualization is most appropriate for showing the full distribution?",
        "options": ["Histogram (20 bins)", "Box plot with outlier points shown", "Strip plot (jitter plot) showing each point", "Density plot"],
        "answer": "Strip plot (jitter plot) showing each point",
        "explanation": "With only 12 points, showing every individual value is honest and informative. Histograms and density plots need far more data to produce meaningful shapes — they will mislead with n=12."
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SESSION 7 — Proportions & Composition
    # ══════════════════════════════════════════════════════════════════════
    {
        "session": 7, "clo": "CLO2", "type": "MCQ",
        "q": "A pie chart has 11 slices. The key problem is:",
        "options": ["Pie charts can only use 10 colors", "Human perception cannot accurately compare more than ~5 angles or areas", "Pie charts must sum to exactly 100", "The chart requires 3D rendering"],
        "answer": "Human perception cannot accurately compare more than ~5 angles or areas",
        "explanation": "Beyond 5–6 slices, angle comparison breaks down entirely. Readers end up guessing or relying on data labels alone — at which point the chart is a decorated table, not a visualization."
    },
    {
        "session": 7, "clo": "CLO2", "type": "TrueFalse",
        "q": "A 100% stacked bar chart is well-suited to show how the MIX of cost categories changes over multiple quarters.",
        "options": ["True", "False"],
        "answer": "True",
        "explanation": "100% stacked bars normalize all bars to 100%, making proportion changes visible across time or groups. This is ideal for tracking budget mix drift — e.g., salaries growing as a share of total costs."
    },
    {
        "session": 7, "clo": "CLO2", "type": "MCQ",
        "q": "A treemap is most appropriate when:",
        "options": ["Showing trend over time", "Showing hierarchical composition where parent-child relationships matter", "Comparing two continuous variables", "Showing a single proportion"],
        "answer": "Showing hierarchical composition where parent-child relationships matter",
        "explanation": "Treemaps encode area proportionally within nested rectangles, making them ideal for hierarchical data — e.g., total costs → departments → line items. Each level shows composition at that level."
    },
    {
        "session": 7, "clo": "CLO2", "type": "Scenario",
        "q": "A CFO wants to see how the marketing budget (₹12 Cr) breaks down into sub-items AND how each sub-item performed vs last year. Which chart best handles both questions?",
        "options": ["A single pie chart", "A waterfall chart showing the budget build", "A grouped bar chart: this year vs last year per category", "A 3D donut chart"],
        "answer": "A grouped bar chart: this year vs last year per category",
        "explanation": "Grouped bars allow direct comparison (this year vs last year) per category. A pie chart cannot show change over time. A waterfall shows build-up, not comparison. The CFO's question has two parts — the grouped bar handles both."
    },
    {
        "session": 7, "clo": "CLO2", "type": "MCQ",
        "q": "A waterfall chart is most useful for:",
        "options": ["Showing a distribution of values", "Explaining how a starting value reaches a final total through incremental additions and subtractions", "Comparing proportions across 10 categories", "Mapping geographic sales data"],
        "answer": "Explaining how a starting value reaches a final total through incremental additions and subtractions",
        "explanation": "Waterfall charts show the stepwise journey: starting value → each positive/negative component → ending value. Classic uses: P&L bridges, budget vs actuals, headcount changes."
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SESSION 8 — Chart Critique & Redesign
    # ══════════════════════════════════════════════════════════════════════
    {
        "session": 8, "clo": "CLO2", "type": "MCQ",
        "q": "The FIRST question to ask when critiquing a chart is:",
        "options": ["Is the color palette accessible?", "What business question is this chart trying to answer?", "Does the chart use 3D effects?", "How many data points are shown?"],
        "answer": "What business question is this chart trying to answer?",
        "explanation": "Chart critique always begins with purpose. If you don't know what decision the chart supports, you cannot evaluate whether it succeeds. Every design choice should be judged against this question."
    },
    {
        "session": 8, "clo": "CLO2", "type": "TrueFalse",
        "q": "A 3D bar chart is acceptable when the data is complex and needs to stand out in a presentation.",
        "options": ["True", "False"],
        "answer": "False",
        "explanation": "3D perspective effects distort bar heights — bars at the front appear shorter than identical bars at the back. This is perceptual distortion, not enhancement. 3D should never be used on charts that encode quantity."
    },
    {
        "session": 8, "clo": "CLO2", "type": "MCQ",
        "q": "A 'spaghetti chart' with 12 lines of equal visual weight can be fixed most effectively by:",
        "options": ["Adding more colors", "Highlighting the key line and fading others to light grey", "Using a 3D view", "Converting to a scatter plot"],
        "answer": "Highlighting the key line and fading others to light grey",
        "explanation": "Accent-and-fade: one bold colored line for the subject of interest, all others in light grey for context. This provides comparison without competition — the key line becomes instantly traceable."
    },
    {
        "session": 8, "clo": "CLO2", "type": "Scenario",
        "q": "A news headline says 'Sales up 40%!' The chart shows bars from 95 to 100. What has happened?",
        "options": ["The data is correct and the headline is accurate", "The truncated y-axis makes a 5% increase look like a 40% increase visually", "The chart is drawn incorrectly", "The headline is in a different currency"],
        "answer": "The truncated y-axis makes a 5% increase look like a 40% increase visually",
        "explanation": "Starting bars at 95 instead of 0 compresses the full scale into a tiny visual range. The bar that was 100 looks 4× taller than 95 — a 400% visual exaggeration of a 5.3% actual difference."
    },
    {
        "session": 8, "clo": "CLO2", "type": "MCQ",
        "q": "An irregular time axis (Jan, Mar, Apr, Sep, Dec) on a line chart creates which specific distortion?",
        "options": ["The line colors look wrong", "Equal visual slopes represent unequal time gaps — trend appears smoother or steeper than reality", "The legend disappears", "Plotly cannot render irregular intervals"],
        "answer": "Equal visual slopes represent unequal time gaps — trend appears smoother or steeper than reality",
        "explanation": "Line charts imply constant time intervals through visual slope. Irregular intervals collapse or stretch real time, making a slow change look like sudden acceleration or vice versa."
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SESSION 9 — Relationships & Insight
    # ══════════════════════════════════════════════════════════════════════
    {
        "session": 9, "clo": "CLO3", "type": "MCQ",
        "q": "A scatter plot shows a strong positive correlation (r = 0.92) between ice cream sales and drowning incidents. The correct interpretation is:",
        "options": ["Ice cream causes drowning — restrict sales", "Both variables are driven by a common cause (summer heat), not each other", "The correlation is a measurement error", "The relationship needs to be shown on a bar chart"],
        "answer": "Both variables are driven by a common cause (summer heat), not each other",
        "explanation": "Classic confounding: summer heat increases both ice cream sales and swimming activity (which increases drowning risk). Correlation ≠ Causation. Always ask: what third variable could explain both?"
    },
    {
        "session": 9, "clo": "CLO3", "type": "MCQ",
        "q": "In a scatter plot, a tight cluster of points around a straight trend line indicates:",
        "options": ["Weak correlation", "A strong linear relationship between the two variables", "Outliers are present", "The data was incorrectly collected"],
        "answer": "A strong linear relationship between the two variables",
        "explanation": "Tightness of the scatter around the trend line measures strength of correlation. A perfect line would mean r = 1.0. Loose scatter means the two variables are weakly related."
    },
    {
        "session": 9, "clo": "CLO3", "type": "TrueFalse",
        "q": "Adding color (a third variable) to a scatter plot can reveal whether a relationship holds uniformly across sub-groups.",
        "options": ["True", "False"],
        "answer": "True",
        "explanation": "Coloring scatter points by a categorical variable (e.g., region, channel) can reveal Simpson's Paradox — where a relationship exists overall but reverses or disappears within sub-groups."
    },
    {
        "session": 9, "clo": "CLO3", "type": "Scenario",
        "q": "A correlation matrix shows spend–revenue r=0.85 but spend–profit r=0.12. What is the business implication?",
        "options": ["The data has errors", "Spending more drives revenue but has weak impact on profit — costs are likely rising proportionally", "Revenue and profit are always correlated", "The matrix is upside down"],
        "answer": "Spending more drives revenue but has weak impact on profit — costs are likely rising proportionally",
        "explanation": "High spend-revenue correlation with low spend-profit correlation suggests the additional revenue is being consumed by the cost of generating it. The ROI conversation needs to shift to margin, not top line."
    },
    {
        "session": 9, "clo": "CLO3", "type": "MCQ",
        "q": "Which step should come AFTER observing an interesting correlation in a scatter plot?",
        "options": ["Immediately issue a business recommendation", "Frame a business hypothesis and seek causal validation before recommending action", "Remove the outliers and recalculate", "Convert to a bar chart for clarity"],
        "answer": "Frame a business hypothesis and seek causal validation before recommending action",
        "explanation": "Correlation is a starting point, not a conclusion. The next step is forming a causal hypothesis and validating it through experimentation, domain knowledge, or causal modeling — not acting directly on the correlation."
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SESSION 10 — Time Series & Change
    # ══════════════════════════════════════════════════════════════════════
    {
        "session": 10, "clo": "CLO3", "type": "MCQ",
        "q": "A rolling average is added to a time series chart primarily to:",
        "options": ["Add more data points", "Smooth out short-term noise and reveal the underlying trend", "Make the chart look more professional", "Replace missing values"],
        "answer": "Smooth out short-term noise and reveal the underlying trend",
        "explanation": "Rolling (moving) averages reduce week-to-week or month-to-month volatility, letting the reader see the underlying direction (upward, downward, flat, cyclical) without being distracted by noise."
    },
    {
        "session": 10, "clo": "CLO3", "type": "TrueFalse",
        "q": "Annotating a specific data point in a time series (e.g., 'Price hike in April') adds noise and should be avoided.",
        "options": ["True", "False"],
        "answer": "False",
        "explanation": "Contextual annotations are one of the most powerful storytelling tools in time series charts. A labeled event (policy change, product launch, market shock) transforms a chart from data display to explanation."
    },
    {
        "session": 10, "clo": "CLO3", "type": "MCQ",
        "q": "A slope chart is best suited for:",
        "options": ["Showing distributions within one time period", "Comparing two time points for multiple entities simultaneously", "Tracking daily stock price movements", "Showing correlation between two variables"],
        "answer": "Comparing two time points for multiple entities simultaneously",
        "explanation": "Slope charts (before–after charts) show direction and magnitude of change for multiple categories between two points. They are particularly readable when many lines would clutter a full time series."
    },
    {
        "session": 10, "clo": "CLO3", "type": "Scenario",
        "q": "Monthly sales data shows a sharp spike every December and a trough every February. How should this be handled in reporting?",
        "options": ["Remove December and February as outliers", "Report seasonally adjusted figures and explicitly label the seasonal pattern", "Use a logarithmic scale to flatten the spikes", "Switch to annual totals to hide the pattern"],
        "answer": "Report seasonally adjusted figures and explicitly label the seasonal pattern",
        "explanation": "Seasonal patterns are real business signals, not errors. Seasonally adjusted trends isolate underlying growth from expected cyclicality, while the raw data with seasonal labels tells the complete story."
    },
    {
        "session": 10, "clo": "CLO3", "type": "MCQ",
        "q": "Which chart type is most useful for showing how much of a change in total revenue came from volume increase vs price increase?",
        "options": ["Line chart", "Waterfall chart", "Heat map", "Scatter plot"],
        "answer": "Waterfall chart",
        "explanation": "A waterfall chart decomposes a total change into its contributing parts — perfect for revenue bridges (e.g., Volume +₹20Cr, Price -₹5Cr, Mix +₹8Cr = Net +₹23Cr). It shows both the components and the total."
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SESSION 11 — Dashboard Storytelling
    # ══════════════════════════════════════════════════════════════════════
    {
        "session": 11, "clo": "CLO3", "type": "MCQ",
        "q": "The primary purpose of a business dashboard is to:",
        "options": ["Display every available metric in real time", "Support a specific decision by showing the most relevant metrics at a glance", "Demonstrate technical capability to stakeholders", "Replace all written reports"],
        "answer": "Support a specific decision by showing the most relevant metrics at a glance",
        "explanation": "Dashboards succeed when designed around a specific audience and decision. A dashboard that shows everything is a dashboard that shows nothing — the decision-first principle drives metric selection."
    },
    {
        "session": 11, "clo": "CLO3", "type": "TrueFalse",
        "q": "Eye-tracking research shows that readers of left-to-right text naturally scan dashboards in an F-shaped pattern.",
        "options": ["True", "False"],
        "answer": "True",
        "explanation": "Nielsen Group eye-tracking studies show users scan web and dashboard content in an F-pattern: full first row, partial second row, then a left-column sweep. Place the most critical KPIs in the top-left."
    },
    {
        "session": 11, "clo": "CLO3", "type": "MCQ",
        "q": "Which dashboard layout principle places the single most important KPI in the top-left position?",
        "options": ["Visual hierarchy based on F-pattern scanning", "The grid-first layout rule", "Responsive design principle", "The three-click rule"],
        "answer": "Visual hierarchy based on F-pattern scanning",
        "explanation": "Because of F-pattern scanning, the top-left gets the most attention. Placing your primary KPI (e.g., NPS, revenue vs target) there ensures the most important number is seen first — every time."
    },
    {
        "session": 11, "clo": "CLO3", "type": "Scenario",
        "q": "A sales dashboard has 22 KPI cards, 8 charts, 3 filters, and a news feed widget. An executive says it is 'overwhelming and unhelpful.' What is the core issue?",
        "options": ["The charts use the wrong colors", "The dashboard lacks an audience and decision focus — it is a data dump in dashboard form", "The dashboard needs more data", "The filters are not working correctly"],
        "answer": "The dashboard lacks an audience and decision focus — it is a data dump in dashboard form",
        "explanation": "A dashboard should answer 'what do I need to decide today?' For an executive, that might be 3–5 KPIs with drill-down available. 22 cards impose cognitive overload. Design for the decision, not the data."
    },
    {
        "session": 11, "clo": "CLO3", "type": "MCQ",
        "q": "Sparklines on a dashboard are small charts that show:",
        "options": ["Pie chart proportions", "Trend over time within a single cell or KPI card", "Real-time streaming data", "Correlation between two variables"],
        "answer": "Trend over time within a single cell or KPI card",
        "explanation": "Sparklines (popularized by Tufte) pack a temporal trend into a tiny inline chart — often a line or bar — displayed next to a KPI value. They add context (is this improving or declining?) without consuming space."
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SESSION 12 — Annotation, Titles & Narrative Flow
    # ══════════════════════════════════════════════════════════════════════
    {
        "session": 12, "clo": "CLO3", "type": "MCQ",
        "q": "What distinguishes a 'descriptive title' from an 'insight title' in data visualization?",
        "options": ["Descriptive titles are longer", "An insight title states the key finding or recommendation; a descriptive title merely labels the chart", "Insight titles must include numbers", "Descriptive titles are used for internal reports only"],
        "answer": "An insight title states the key finding or recommendation; a descriptive title merely labels the chart",
        "explanation": "Descriptive: 'Sales by Region Q3.' Insight: 'North Region Underperforms All Others by >20% — Investigate Distribution.' The insight title does the analysis; the descriptive title does not."
    },
    {
        "session": 12, "clo": "CLO3", "type": "TrueFalse",
        "q": "Annotating every single data point with its value improves readability by making the chart more informative.",
        "options": ["True", "False"],
        "answer": "False",
        "explanation": "Over-labelling creates visual noise that crowds out the pattern. Label only the key values — the highest, lowest, or inflection points that support your narrative. Let the chart's shape communicate the rest."
    },
    {
        "session": 12, "clo": "CLO3", "type": "MCQ",
        "q": "In the SCR (Situation-Complication-Resolution) storytelling framework, what does the 'Complication' step establish?",
        "options": ["The baseline data context", "The tension or problem that makes the status quo unsustainable", "The recommended course of action", "The chart legend"],
        "answer": "The tension or problem that makes the status quo unsustainable",
        "explanation": "SCR is a narrative structure: Situation (here is where we are), Complication (here is why that's a problem), Resolution (here is what we should do). The complication creates the urgency that makes the recommendation compelling."
    },
    {
        "session": 12, "clo": "CLO3", "type": "Scenario",
        "q": "A chart title reads 'Revenue Trend 2022–2024.' How can this be improved?",
        "options": ["Add more years to the title", "Change it to 'Revenue Growth Has Stalled Since Q2 2023 — Action Required'", "Use a larger font", "Add the chart number"],
        "answer": "Change it to 'Revenue Growth Has Stalled Since Q2 2023 — Action Required'",
        "explanation": "The improved title states what the data shows (growth stalled), when (since Q2 2023), and why it matters (action required). This is the difference between labelling a chart and writing a headline."
    },
    {
        "session": 12, "clo": "CLO3", "type": "MCQ",
        "q": "A subtitle below a chart title should serve to:",
        "options": ["Repeat the title in different words", "Provide one additional layer of context — the 'so what' or key caveat not in the main title", "List data sources", "Replace the y-axis label"],
        "answer": "Provide one additional layer of context — the 'so what' or key caveat not in the main title",
        "explanation": "Title → Subtitle → Caption is a three-layer annotation hierarchy. Subtitles add the qualifying context: 'Based on n=1,200 customers | Regional outliers excluded.' They do not repeat — they extend."
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SESSION 13 — Pitfalls in Data Storytelling
    # ══════════════════════════════════════════════════════════════════════
    {
        "session": 13, "clo": "CLO4", "type": "MCQ",
        "q": "Cherry-picking in data storytelling means:",
        "options": ["Using fruit industry data as examples", "Selecting only the data points that support a predetermined conclusion while ignoring contradictory evidence", "Choosing the best visual design", "Picking the highest value to feature prominently"],
        "answer": "Selecting only the data points that support a predetermined conclusion while ignoring contradictory evidence",
        "explanation": "Cherry-picking is selective reporting — it produces technically accurate but misleading analyses. The ethical standard is to present data that challenges your hypothesis alongside data that supports it."
    },
    {
        "session": 13, "clo": "CLO4", "type": "TrueFalse",
        "q": "Reporting a percentage increase without stating the base value (e.g., '200% growth!') can be misleading.",
        "options": ["True", "False"],
        "answer": "True",
        "explanation": "200% growth from ₹1L to ₹3L is very different from 200% growth from ₹100Cr to ₹300Cr. Always state the base value when reporting percentage changes — the denominator defines context."
    },
    {
        "session": 13, "clo": "CLO4", "type": "MCQ",
        "q": "A dual y-axis chart shows revenue (left axis, ₹ Crores) and NPS score (right axis, 0–100) on the same chart. The main risk is:",
        "options": ["The legend is confusing", "Readers may infer that revenue and NPS are causally related when the visual overlap is a scale artifact", "The two lines cannot be different colors", "The chart cannot be printed"],
        "answer": "Readers may infer that revenue and NPS are causally related when the visual overlap is a scale artifact",
        "explanation": "Dual-axis charts allow the analyst to manually scale either axis until the two lines appear to move together. This manufactured convergence implies relationship where none may exist. Use two separate charts with a text link."
    },
    {
        "session": 13, "clo": "CLO4", "type": "Scenario",
        "q": "An e-commerce report shows 'conversion rate improved from 2.0% to 2.6%.' The headline claims 'Conversion Up 30%!' Is this misleading?",
        "options": ["Yes — a 0.6 percentage point change sounds much smaller than 30%", "No — 30% is mathematically correct and not misleading", "It depends on whether the metric is revenue or volume", "It depends on the chart type used"],
        "answer": "No — 30% is mathematically correct and not misleading",
        "explanation": "2.6/2.0 = 1.30 — a 30% relative increase. This is mathematically accurate. However, communicators should present both: '30% relative improvement (from 2.0% to 2.6% absolute).' Context prevents misinterpretation."
    },
    {
        "session": 13, "clo": "CLO4", "type": "MCQ",
        "q": "Which technique is most often used to make a gradual decline look like a stable plateau?",
        "options": ["Removing outliers", "Shortening the time window shown — cutting off the period where the decline began", "Switching from line to bar chart", "Using log scale"],
        "answer": "Shortening the time window shown — cutting off the period where the decline began",
        "explanation": "Temporal cherry-picking: if performance peaked 2 years ago and has declined since, starting the chart's time axis at the peak hides the full picture. Always show the full relevant history."
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SESSION 14 — Strategy Communication
    # ══════════════════════════════════════════════════════════════════════
    {
        "session": 14, "clo": "CLO4", "type": "MCQ",
        "q": "A 'gap chart' in strategy communication is used to show:",
        "options": ["Missing data in a time series", "The distance between current performance and target — making the challenge visible", "Negative values on a bar chart", "The difference between two correlation coefficients"],
        "answer": "The distance between current performance and target — making the challenge visible",
        "explanation": "Gap charts visualize the aspirational gap: where we are today vs where we need to be. They give strategy narratives a clear focal point — the gap is the problem to solve."
    },
    {
        "session": 14, "clo": "CLO4", "type": "TrueFalse",
        "q": "For a board-level strategy presentation, showing 3 highly focused charts is almost always more effective than 15 detailed analytical charts.",
        "options": ["True", "False"],
        "answer": "True",
        "explanation": "Senior audiences have limited time and want decisions, not analyses. Three carefully chosen charts — each answering one strategic question — will be remembered and acted upon. Fifteen charts create cognitive overload."
    },
    {
        "session": 14, "clo": "CLO4", "type": "MCQ",
        "q": "The SCR framework stands for:",
        "options": ["Summary, Context, Results", "Situation, Complication, Resolution", "Strategy, Chart, Recommendation", "Scale, Color, Range"],
        "answer": "Situation, Complication, Resolution",
        "explanation": "SCR is a narrative structure derived from McKinsey's communication methodology. Situation sets the context, Complication creates urgency, Resolution provides the actionable answer."
    },
    {
        "session": 14, "clo": "CLO4", "type": "Scenario",
        "q": "A strategy deck opens with 8 slides of market background before stating the problem. An MD falls asleep on slide 4. The fix is:",
        "options": ["Add more animations", "Apply SCR: lead with the Situation (one slide), Complication (one slide), then Resolution (main argument)", "Use a darker theme", "Include more data sources"],
        "answer": "Apply SCR: lead with the Situation (one slide), Complication (one slide), then Resolution (main argument)",
        "explanation": "Executive audiences want the punchline first, not last. SCR frontloads the key message: 'Our market share is declining (Situation). Competitors are winning on digital (Complication). We must launch an app by Q3 (Resolution).'"
    },
    {
        "session": 14, "clo": "CLO4", "type": "MCQ",
        "q": "A bubble chart adds which additional encoding dimension beyond a standard scatter plot?",
        "options": ["Color intensity", "A third quantitative variable encoded as bubble area", "Time as the Z-axis", "Correlation coefficient as bubble shape"],
        "answer": "A third quantitative variable encoded as bubble area",
        "explanation": "Bubble charts use x-position, y-position (like scatter), plus bubble area to encode a third variable. Classic example: BCG Matrix (Market Share × Market Growth × Revenue as bubble size)."
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SESSION 15 — Integrated Workshop
    # ══════════════════════════════════════════════════════════════════════
    {
        "session": 15, "clo": "CLO4", "type": "MCQ",
        "q": "In an end-to-end storytelling workflow, which step MUST come before selecting chart types?",
        "options": ["Writing the title", "Defining the audience and the decision they need to make", "Cleaning the data", "Choosing the color palette"],
        "answer": "Defining the audience and the decision they need to make",
        "explanation": "Audience and decision define everything: which metrics matter, which chart types are appropriate, what level of detail to include, and what the recommendation should be. Skip this step and the analysis may be technically correct but communication-ally useless."
    },
    {
        "session": 15, "clo": "CLO4", "type": "TrueFalse",
        "q": "A data story for a field sales team should use the same charts and narrative structure as a data story for the CFO.",
        "options": ["True", "False"],
        "answer": "False",
        "explanation": "Audience drives everything. Field teams need operational, actionable detail (by territory, by customer, daily/weekly). The CFO needs aggregated strategic signals (margin, portfolio trends, forecast confidence). Same data, completely different story."
    },
    {
        "session": 15, "clo": "CLO4", "type": "MCQ",
        "q": "What is the purpose of a 'storyboard' before building a data presentation?",
        "options": ["To create animated transitions between slides", "To sketch the sequence of charts and narrative frames before any chart is built", "To export charts to a PDF format", "To define the color scheme"],
        "answer": "To sketch the sequence of charts and narrative frames before any chart is built",
        "explanation": "Storyboarding (even on paper) lets you test the narrative logic before investing in chart building. The test: can someone follow your argument from frame 1 to the last frame without data? If yes, the story is structurally sound."
    },
    {
        "session": 15, "clo": "CLO4", "type": "Scenario",
        "q": "After completing a full data story, you test it with a colleague who says 'so what?' after the last slide. What does this indicate?",
        "options": ["The data is wrong", "The story lacks a clear recommendation or call to action", "The colleague is not interested in data", "The charts need more detail"],
        "answer": "The story lacks a clear recommendation or call to action",
        "explanation": "A data story without a 'so what' is an analysis, not a story. Every data story must end with a specific, actionable recommendation. If the listener asks 'so what?', the Resolution in SCR is missing."
    },
    {
        "session": 15, "clo": "CLO4", "type": "MCQ",
        "q": "Which of the following is the most important criterion for selecting which charts to include in a final presentation?",
        "options": ["The charts that took the longest to build", "The charts that most directly support the recommendation", "The charts that show the most data", "The charts with the most visual complexity"],
        "answer": "The charts that most directly support the recommendation",
        "explanation": "Ruthless selection: only include charts that earn their place by supporting the recommendation. Charts that are interesting but don't move the argument forward should be moved to an appendix."
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SESSION 16 — Healthcare Data Visualization
    # ══════════════════════════════════════════════════════════════════════
    {
        "session": 16, "clo": "CLO4", "type": "MCQ",
        "q": "In healthcare dashboards, which metric best signals the overall operational health of an emergency department?",
        "options": ["Total number of doctors on roster", "Door-to-doctor time (patient arrival to first clinical contact)", "Number of parking spaces", "Average salary of nurses"],
        "answer": "Door-to-doctor time (patient arrival to first clinical contact)",
        "explanation": "Door-to-doctor time is a high-signal composite metric — it reflects ED staffing, triage efficiency, bed availability, and queue management simultaneously. It is the most widely used ED performance indicator globally."
    },
    {
        "session": 16, "clo": "CLO4", "type": "TrueFalse",
        "q": "A heat map of hourly patient arrivals by day of week is a useful tool for hospital shift scheduling decisions.",
        "options": ["True", "False"],
        "answer": "True",
        "explanation": "Arrival heat maps reveal peak load patterns (e.g., Monday mornings, Friday evenings) that should drive staffing schedules. Without this visualization, shifts are assigned on intuition rather than evidence."
    },
    {
        "session": 16, "clo": "CLO4", "type": "MCQ",
        "q": "Bed occupancy rate consistently above 95% in a hospital ward indicates:",
        "options": ["Excellent efficiency — near-full capacity utilization", "A system near critical failure — no buffer for surge, infection control risks increase", "That the hospital needs fewer beds", "That patient discharge rates are too high"],
        "answer": "A system near critical failure — no buffer for surge, infection control risks increase",
        "explanation": "WHO and NHS guidelines suggest 85% as a safe occupancy ceiling. Above 95%, there is no buffer for emergency admissions, cross-infection risk rises, and patient safety deteriorates. The visualization must flag this as a danger zone."
    },
    {
        "session": 16, "clo": "CLO4", "type": "Scenario",
        "q": "A hospital administrator wants to compare patient satisfaction across 12 wards and also see score distributions. What chart combination is most informative?",
        "options": ["12 separate pie charts", "A bar chart of mean scores only", "A box plot or violin plot per ward showing median, spread, and outliers", "A single KPI card with the hospital average"],
        "answer": "A box plot or violin plot per ward showing median, spread, and outliers",
        "explanation": "Box/violin plots per ward enable multi-dimensional comparison: median (central tendency), IQR (consistency), whiskers (extreme cases), and outlier points (individual incidents). The mean alone hides wards with bimodal satisfaction."
    },
    {
        "session": 16, "clo": "CLO4", "type": "MCQ",
        "q": "Why is a Gantt-style chart useful for tracking patient journey (admission to discharge)?",
        "options": ["It shows proportions of diagnosis types", "It maps each patient's timeline across stages — identifying bottlenecks where time is lost", "It replaces electronic health records", "It visualizes medication dosages"],
        "answer": "It maps each patient's timeline across stages — identifying bottlenecks where time is lost",
        "explanation": "A patient-flow Gantt chart shows each care stage (triage → assessment → treatment → discharge) as a horizontal bar. Unusually long bars at any stage immediately reveal systemic delays — the starting point for process improvement."
    },

]
