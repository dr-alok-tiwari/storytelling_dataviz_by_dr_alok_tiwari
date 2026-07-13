# 📊 Storytelling using Data Visualization

A production-oriented, interactive teaching application for the **2-credit PGDM-BDA core course** at Goa Institute of Management.

**Instructor:** Dr. Alok Tiwari  
**Institution:** Goa Institute of Management, Goa  
**Course design:** 16 sessions × 75 minutes  
**Application version:** 2.0.0

> All datasets in the application are deterministic and synthetic. They do not represent real students, patients, organisations, or financial records. Healthcare examples are for education only and are not clinical guidance.

---

## What the app provides

- 16 fully developed course sessions across four modules
- Stable, shareable page URLs for every session and practice tool
- Concept, demonstration, lab, quiz, and reflection activities
- Working session-completion tracking for the current browser session
- Previous, roadmap, and next-session controls
- Classroom mode for larger projected text and controls
- Reduced-motion accessibility preference
- Deterministic synthetic datasets that remain consistent across reruns
- Chart Selection Engine with coverage for every input combination
- Storytelling Framework Builder with validation and text export
- Six management case studies with data-derived headlines
- Stable quiz state when filters change
- Downloadable CSV datasets and story summaries
- Responsive design for desktop, tablet, and mobile-width screens
- Automated tests and GitHub Actions quality checks

---

## Course modules

| Module | Sessions | Theme |
|---|---:|---|
| Module 1 | 1–4 | Foundations of data visualization |
| Module 2 | 5–8 | Dashboard design and visual communication |
| Module 3 | 9–12 | Storytelling with data |
| Module 4 | 13–16 | Business, strategy, and healthcare applications |

Each standard session follows this structure:

1. **Concept** — principles and managerial context
2. **Demo** — interactive worked examples
3. **Lab** — guided application activity
4. **Quiz** — formative assessment with explanations
5. **Reflect** — personal application and session completion

---

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/dr-alok-tiwari/storytelling_dataviz_by_dr_alok_tiwari.git
cd storytelling_dataviz_by_dr_alok_tiwari
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed by Streamlit, normally `http://localhost:8501`.

---

## Development installation

To install testing and linting tools:

```bash
pip install -e ".[dev]"
```

Run quality checks:

```bash
ruff check app.py modules/data_generators.py modules/home.py modules/tools.py modules/tools_runtime_patch.py modules/ui_components.py tests --select E9,F63,F7,F82 --ignore E402,F401
pytest
```

The test suite checks:

- application smoke rendering;
- deterministic dataset generation;
- correct year-on-year growth calculations;
- occupancy reconciliation;
- cost-per-lead units;
- score-derived student grades;
- full Chart Selection Engine input coverage.

---

## Project structure

```text
storytelling_dataviz_by_dr_alok_tiwari/
├── app.py                         # Application router and shared shell
├── requirements.txt              # Streamlit Cloud dependencies
├── pyproject.toml                 # Package, lint, and test configuration
├── README.md
├── LICENSE.md
├── .gitignore
├── .streamlit/
│   └── config.toml                # Theme, accessibility, and server settings
├── .github/
│   └── workflows/
│       └── quality.yml            # CI lint and test workflow
├── modules/
│   ├── __init__.py
│   ├── ui_components.py           # Design system and shared components
│   ├── data_generators.py         # Deterministic synthetic datasets
│   ├── home.py                    # Landing page and roadmap
│   ├── sessions_1_8.py            # Modules 1 and 2
│   ├── sessions_9_16.py           # Modules 3 and 4
│   ├── quiz_bank.py               # Question bank
│   ├── tools.py                   # Chart, story, case, quiz, and resource tools
│   └── tools_runtime_patch.py     # Exact recommendation/example alignment
└── tests/
    ├── test_app_smoke.py
    ├── test_data_generators.py
    └── test_tools.py
```

---

## Production design decisions

### Native navigation

The application uses `st.navigation` and `st.Page` rather than a custom button router. This provides:

- stable URLs;
- browser navigation support;
- grouped course modules;
- a cleaner responsive navigation experience;
- less dependence on undocumented Streamlit DOM selectors.

### Deterministic data

Each dataset uses its own fixed random seed and `st.cache_data`. Therefore:

- charts do not unexpectedly change after widget interactions;
- model answers remain aligned with examples;
- downloads match the displayed chart;
- students see reproducible classroom results.

### Accessible visual system

The committed `.streamlit/config.toml` and shared CSS provide:

- 17 px base typography;
- higher-contrast sidebar text;
- responsive heading sizes;
- minimum control heights;
- classroom enlargement mode;
- reduced-motion support;
- system-font fallbacks without an external font dependency.

### Honest educational outputs

Management case headlines and key findings are derived from the current deterministic dataset instead of being hard-coded. This prevents the narrative from contradicting the displayed evidence.

---

## Streamlit Community Cloud deployment

1. Push the repository to GitHub.
2. Sign in to Streamlit Community Cloud.
3. Select **Create app**.
4. Choose this repository and the target branch.
5. Set the main file path to:

```text
app.py
```

6. Deploy.

No API keys, secrets, paid services, or external data files are required.

---

## Classroom use

For projection:

- turn on **Classroom mode** in the sidebar;
- use a display resolution of at least 1280 × 720;
- keep the browser at normal zoom unless the physical room requires additional enlargement;
- share the direct session URL with students before class;
- remind students that completion progress is stored for the current browser session only.

---

## Data and privacy

- The app does not require authentication.
- It does not collect or transmit student responses to an external database.
- Text entries and progress use Streamlit session state and are not durable records.
- Downloaded files are generated locally from synthetic educational content.
- Do not enter personal, confidential, patient-identifiable, or institutionally restricted information into public deployments.

---

## License and attribution

Copyright © 2026 Dr. Alok Tiwari. All rights reserved.

Educational use is permitted subject to the conditions in [LICENSE.md](LICENSE.md). Attribution to Dr. Alok Tiwari and Goa Institute of Management must be retained.
