# CampusCare – Smart Campus Maintenance & Complaint Management System

A lightweight complaint tracking and maintenance management tool designed for
hostel staff at NIT Jamshedpur.

## Problem Statement

Hostel maintenance complaints at NIT Jamshedpur are currently managed through
informal channels (WhatsApp messages, verbal reports), making it difficult for
staff to prioritise, track, and close issues systematically.

## Stack

| Tool | Purpose |
|------|---------|
| Python 3.11+ | Core language |
| Streamlit | Web UI |
| Pandas | Data manipulation |
| CSV | Lightweight data store |
| Plotly | Charts and dashboards |
| Pytest | Automated tests |

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure

```
CampusCare/
├── app.py               # Streamlit entry point
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   ├── data.csv         # Real fieldwork data (populated after visits)
│   └── sample_data.csv  # Synthetic data for testing only
├── modules/             # Feature modules (populated during development)
├── tests/               # Pytest test suite
├── docs/
│   ├── research.md      # Problem research and literature
│   ├── fieldwork.md     # Field visit notes and observations
│   └── reflection.md    # Personal reflection (written by student)
├── evidence/            # Photos and supporting evidence from field visits
└── ai-chats/            # Logs of AI-assisted sessions (assignment requirement)
```

## Status

- [x] Repository initialised
- [x] Research document drafted
- [x] Fieldwork template prepared
- [ ] Field visit completed
- [ ] Real data collected
- [ ] Application built
- [ ] Tests written

## Assignment Context

24-hour take-home project — NIT Jamshedpur.
