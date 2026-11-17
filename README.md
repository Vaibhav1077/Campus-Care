# 🏫 CampusCare – Smart Campus Maintenance & Complaint Management System

CampusCare is a Streamlit-based complaint management system built for hostel maintenance staff at NIT Jamshedpur. It provides a structured digital interface to track, prioritize, and resolve maintenance issues systematically, replacing informal reporting channels with a centralized, searchable record of every complaint from submission through resolution.

## Problem Hypothesis

> **Note: The following is a hypothesis, not a verified finding. It will be tested against fieldwork.**

Hostel maintenance complaint tracking at NIT Jamshedpur may currently rely on informal channels such as verbal reports or messaging apps, which likely causes delays and lost complaints that go unresolved. A structured digital system could improve resolution time and accountability for maintenance staff. This remains an assumption pending fieldwork confirmation.

## Features

- 📊 Dashboard with KPI metrics and 4 interactive charts
- 📋 Complaint management (add, view, edit, delete, search, filter, export)
- ⚙️ Smart Priority Engine with transparent rule-based scoring and explanations
- 🔁 Recurring Issue Detection to identify chronic problem locations
- ⏳ Pending Complaint Monitor with overdue alerts and age tracking
- 🧪 Demo mode with synthetic data for stakeholder demonstrations

## Technology Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Backend logic |
| Streamlit | ≥1.32 | Web UI |
| Pandas | ≥2.1 | Data processing |
| Plotly | ≥5.19 | Interactive charts |
| Pytest | ≥8.0 | Testing |
| CSV | — | Data storage |

## Project Structure

```
CampusCare/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md
├── .gitignore
├── data/
│   ├── data.csv              # Real complaint records (empty until fieldwork)
│   └── sample_data.csv       # Synthetic demo data (clearly labelled)
├── modules/
│   ├── validators.py         # Input validation and ID generation
│   ├── data_manager.py       # CSV read/write with atomic writes
│   ├── priority_engine.py    # Rule-based priority calculation
│   └── analytics.py          # Statistics and trend analysis
├── tests/
│   └── test_campuscare.py    # Pytest test suite
├── docs/
│   ├── research.md           # Problem research and literature review
│   ├── fieldwork.md          # Fieldwork template (to be completed)
│   └── reflection.md         # Personal reflection (to be written by student)
├── evidence/                 # Field photos and evidence
└── ai-chats/                 # AI conversation logs
```

## Installation

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run app.py
```

> App opens at http://localhost:8501 by default.

## CSV Format

All complaint records in `data/data.csv` use the following 13-column schema:

| Column | Description |
|--------|-------------|
| complaint_id | Unique ID (C001, C002, ...) |
| date_reported | Date in YYYY-MM-DD format |
| hostel_block | Hostel block identifier (e.g. A, B, C) |
| room_number | Room number or location |
| category | One of: Electrical, Plumbing, Cleaning, Furniture, Internet, Other |
| description | Detailed description of the issue |
| reported_by | Name of the person reporting |
| contact | Contact number of reporter |
| priority | One of: Critical, High, Medium, Low |
| status | One of: Pending, In Progress, Resolved |
| assigned_to | Staff member assigned to resolve |
| date_resolved | Resolution date in YYYY-MM-DD format (blank if unresolved) |
| resolution_notes | Notes on how the issue was resolved |

## Testing

```bash
python -m pytest tests/test_campuscare.py -v
```

Test coverage includes: ID generation, input validation, duplicate detection, CSV operations, priority calculation, age escalation, analytics, overdue detection.

## Known Limitations

- CSV storage is not suitable for concurrent writes from multiple users.
- No authentication or role-based access control.
- Priority engine uses rule-based heuristics, not machine learning.
- Real fieldwork data has not yet been collected; `data.csv` is currently empty.
- Not deployed — runs locally only.

## Output Screenshots

> Screenshots to be added after field visit.

## Demo Video

> Demo video link: [To be added]
