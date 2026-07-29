# 📊 Storytelling using Data Visualization

A production-oriented, interactive teaching application for the **2-credit PGDM-BDA core course** at Goa Institute of Management.

**Instructor:** Dr. Alok Tiwari  
**Institution:** Goa Institute of Management, Goa  
**Course design:** 16 sessions × 75 minutes  
**Application version:** 2.1.0

> All datasets in the application are deterministic and synthetic. They do not represent real students, patients, organisations, or financial records. Healthcare examples are for education only and are not clinical guidance.

## What the app provides

- 16 fully developed course sessions across four modules
- Official PowerPoint decks for all 16 sessions
- A correctly matched PPTX download on every session page
- A central **Course Presentation Library** on the Resources & Tools page
- Stable, shareable page URLs for sessions and practice tools
- Concept, demonstration, lab, quiz, and reflection activities
- Working session-completion tracking for the current browser session
- Previous, roadmap, and next-session controls
- Classroom mode and reduced-motion accessibility preferences
- Deterministic synthetic datasets that remain consistent across reruns
- Chart Selection Engine and Storytelling Framework Builder
- Management case studies, quizzes, downloadable datasets, and story summaries
- Responsive design for desktop, tablet, and mobile-width screens
- Automated tests and GitHub Actions quality checks

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

## Official course presentations

Every session page includes a **Session Presentation** card near the session heading. The card downloads the official editable PPTX corresponding to that page.

The **Resources & Tools** page also contains the Course Presentation Library. Select any of the 16 sessions and download its deck. Only the selected library file is loaded, preserving responsive performance.

The presentations are stored locally in the repository under `assets/session_ppts/`. No API key, paid service, database, secret, or external storage service is required.

The decks are educational course resources. Copyright and attribution to Dr. Alok Tiwari and Goa Institute of Management must be retained.

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/dr-alok-tiwari/storytelling_dataviz_by_dr_alok_tiwari.git
cd storytelling_dataviz_by_dr_alok_tiwari
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

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

## Development installation and quality checks

```bash
pip install -e ".[dev]"
ruff check app.py modules tests --select E9,F63,F7,F82 --ignore E402,F401
pytest
```

The presentation-resource tests verify:

- exact coverage of Sessions 1–16;
- unique paths and download filenames;
- the existence and non-empty size of every deck;
- valid PPTX/OOXML ZIP structure;
- canonical session-title alignment; and
- clean rejection of invalid session numbers.

## Project structure

```text
storytelling_dataviz_by_dr_alok_tiwari/
├── app.py
├── requirements.txt
├── pyproject.toml
├── README.md
├── LICENSE.md
├── .gitignore
├── assets/
│   └── session_ppts/
│       ├── README.md
│       ├── session_01_introduction_why_data_visualization_and_storytelling_matter.pptx
│       ├── ...
│       └── session_16_guest_session_healthcare_data_visualization.pptx
├── .streamlit/
│   └── config.toml
├── .github/
│   └── workflows/
│       └── quality.yml
├── modules/
│   ├── __init__.py
│   ├── ui_components.py
│   ├── session_resources.py
│   ├── data_generators.py
│   ├── home.py
│   ├── lazy_tabs.py
│   ├── sessions_1_8.py
│   ├── sessions_9_16.py
│   ├── quiz_bank.py
│   ├── tools.py
│   └── tools_runtime_patch.py
└── tests/
    ├── test_app_smoke.py
    ├── test_data_generators.py
    ├── test_session_resources.py
    └── test_tools.py
```

## Design and performance decisions

### Shared presentation metadata

`modules/session_resources.py` is the single source of truth for presentation filenames and download metadata. It derives session titles and module assignments from the existing canonical UI mappings, preventing title drift.

### Per-session loading

Each session page reads only its own presentation. The bytes are cached with `st.cache_data` and are not repeatedly read on normal widget reruns.

### Lazy presentation library

The Course Presentation Library displays all 16 entries but loads only the selected presentation for download.

### Native navigation and deterministic data

The application uses `st.navigation` and `st.Page` for stable URLs and browser navigation. Synthetic datasets use fixed random seeds and caching so charts, examples, and downloads remain reproducible.

### Accessibility

The shared visual system provides high-contrast text, responsive typography, minimum control heights, classroom enlargement, reduced-motion support, and system-font fallbacks.

## Streamlit Community Cloud deployment

1. Push the repository to GitHub.
2. Sign in to Streamlit Community Cloud.
3. Select **Create app**.
4. Choose this repository and the target branch.
5. Set the main file path to `app.py`.
6. Deploy.

The PPTX assets are served directly from the deployed repository. No secrets are required.

## Classroom use

- Turn on **Classroom mode** in the sidebar for projection.
- Use a display resolution of at least 1280 × 720.
- Share direct session URLs with students before class.
- Download the session presentation from the card below the session header.
- Use the Course Presentation Library for consolidated access to all decks.
- Remember that completion progress is stored for the current browser session only.

## Data, privacy, and educational use

- The app does not require authentication.
- It does not collect or transmit student responses to an external database.
- Text entries and progress use Streamlit session state and are not durable records.
- Downloaded files are generated or served locally from repository content.
- Do not enter personal, confidential, patient-identifiable, or institutionally restricted information into public deployments.

## License and attribution

Copyright © 2026 Dr. Alok Tiwari. All rights reserved.

Educational use is permitted subject to the conditions in `LICENSE.md`. Attribution to Dr. Alok Tiwari and Goa Institute of Management must be retained in the application and official course presentations.
