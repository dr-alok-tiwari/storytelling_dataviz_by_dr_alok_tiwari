# 📊 Storytelling using Data Visualization
### Interactive Teaching App
**Goa Institute of Management | Dr. Alok Tiwari**

---

## Overview

This is a fully self-contained, classroom-ready Streamlit application for the
2-credit PGDM-BDA core course *Storytelling using Data Visualization*. It covers
all 16 sessions (75 minutes each) across four modules, requiring no external
data files, API keys, or paid tools.

---

## Quick Start

### 1. Clone or copy the project

```bash
# If using git
git clone <your-repo-url>
cd dataviz_app

# Or simply unzip the folder and cd into it
cd dataviz_app
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

---

## Project Structure

```
dataviz_app/
│
├── app.py                    ← Main entry point & sidebar router
├── requirements.txt          ← Python dependencies
├── README.md                 ← This file
│
└── modules/
    ├── __init__.py
    ├── ui_components.py      ← CSS, color palette, callout helpers, footer
    ├── data_generators.py    ← 11 synthetic in-memory datasets
    ├── home.py               ← Landing page & Course Roadmap
    ├── sessions_1_8.py       ← Sessions 1–8 (Modules 1 & 2)
    ├── sessions_9_16.py      ← Sessions 9–16 (Modules 3 & 4)
    ├── quiz_bank.py          ← 50+ quiz questions (MCQ, T/F, scenario)
    └── tools.py              ← Chart Engine, Story Builder, Cases, Quiz Zone, Resources
```

---

## Course Modules

| Module | Sessions | Theme |
|--------|----------|-------|
| 1 | 1–4  | Foundations of Data Visualization |
| 2 | 5–8  | Dashboard Design & Visual Communication |
| 3 | 9–12 | Storytelling with Data |
| 4 | 13–16 | Business & Strategy Applications |

---

## Features

- **16 fully developed session pages** — each with Concept, Demo, Lab, Quiz, and Reflection tabs
- **Chart Selection Engine** — recommends chart types by data type, question, and audience
- **Storytelling Framework Builder** — 8-step narrative builder with text export
- **Business Case Library** — 6 cases (Sales, Marketing, Operations, Finance, Healthcare, Strategy)
- **Quiz Zone** — 50+ questions with instant answer reveal and CLO tagging
- **Misleading Chart Clinic** — before/after redesign examples built into Session 8 & 13
- **Final Integrated Workshop** — end-to-end visual story build (Session 15)
- **Healthcare Dashboard** — purpose-built session for HCM/healthcare analytics students (Session 16)
- **Session progress tracker** — sidebar checkboxes with completion bar
- **Downloadable outputs** — CSV datasets and storyboard summaries

---

## Technology Stack

| Library | Purpose |
|---------|---------|
| streamlit ≥ 1.32 | UI framework |
| pandas ≥ 2.0 | Data manipulation |
| numpy ≥ 1.24 | Numerical generation |
| plotly ≥ 5.18 | Interactive charts |
| altair ≥ 5.0 | Declarative charts |
| matplotlib ≥ 3.7 | Static figures |
| scikit-learn ≥ 1.3 | Illustrative ML examples |

No API keys. No paid services. No external data files.

---

## Classroom Usage Notes

- **Projection mode:** use wide layout (already set) at 1280×720 or higher
- **Font size:** increase browser zoom to 110–125% for rear-row visibility
- **Session flow:** each session is designed for a 75-minute class:
  - 10 min — Concept tab (instructor-led)
  - 20 min — Demo tab (live walkthrough)
  - 20 min — Lab tab (student activity)
  - 10 min — Quiz tab (discussion)
  - 10 min — Reflection tab + summary
  - 5 min  — Wrap-up / questions
- **Progress tracking:** students check the session-complete box at the end; progress shows in sidebar

---

## Suggested Improvements (Future Versions)

1. Add st-aggrid for richer data tables in the workshop
2. Integrate Lottie animations for concept introductions
3. Add a PDF export button for storyboard summaries
4. Connect an optional Google Sheets import for live classroom data
5. Add a leaderboard for quiz scores using st.session_state
6. Build a peer-critique mode where students submit redesigns
7. Add a dark/light theme toggle
8. Package as a Docker container for zero-install classroom deployment

---

## License & Attribution

Developed for academic use at Goa Institute of Management (GIM), Panaji, Goa.
All datasets are synthetically generated and do not represent any real individuals
or organizations.

**Instructor:** Dr. Alok Tiwari, Assistant Professor — Big Data Analytics, GIM
