# CampusCare

A role-based campus maintenance complaint management system built with Python and Streamlit.

## Problem Being Solved

Students living in campus hostels have no structured way to report maintenance issues such as electrical faults, plumbing failures, or broken furniture. Without a formal system, complaints are made verbally or by text message and often get lost or go unresolved for weeks. CampusCare gives students a self-service portal to submit and track their complaints while giving admin and maintenance staff a prioritised, searchable queue with built-in analytics. This reduces follow-up overhead for both students and staff and ensures critical issues surface automatically.

## Features

### Student Portal
- Submit maintenance complaints with hostel block, room number, category, and description
- Automatic unique complaint ID generation
- Automatic priority classification (Critical / High / Medium / Low) using rule-based engine
- View and search personal complaint history
- Track complaint status (Pending → In Progress → Resolved) with a visual stepper
- Filter complaints by status and category

### Admin Portal
- View all complaints with search and multi-filter (block, category, priority, status)
- Dashboard with KPI metrics: total, pending, in-progress, resolved, critical, overdue
- Charts: complaints by category, status distribution, hostel-block distribution
- Update complaint status, priority, assigned staff, and resolution notes
- Priority & Overdue queue — identifies Critical/High and overdue complaints
- Recurring Issues detector — surfaces locations with repeated same-category complaints
- Analytics page with monthly trend, priority breakdown, block and category charts
- Export complaints as CSV

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.14 |
| UI Framework | Streamlit |
| Data Processing | pandas |
| Charts | Plotly |
| Persistence | CSV (file-based) |
| Testing | pytest |

## Setup Instructions

```bash
git clone https://github.com/Vaibhav1077/Campus-Care.git
cd Campus-Care
pip install -r requirements.txt
```

## Run Command

```bash
python3.14 -m streamlit run app.py
```

Then open: http://localhost:8501

## Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| Student | student | student123 |
| Admin | admin | admin123 |

## Project Structure

```
CampusCare/
├── app.py                  # Main Streamlit application and page router
├── requirements.txt        # Python dependencies
├── data/
│   ├── data.csv            # Live complaint records
│   └── sample_data.csv     # Read-only synthetic demo dataset
├── modules/
│   ├── auth.py             # Login / logout / session management
│   ├── data_manager.py     # CSV read/write, complaint CRUD
│   ├── priority_engine.py  # Rule-based priority classification
│   ├── analytics.py        # Aggregation and reporting functions
│   ├── validators.py       # Field validation and duplicate detection
│   └── theme.py            # Design tokens, CSS, and HTML component helpers
├── tests/
│   └── test_campuscare.py  # pytest test suite
├── docs/                   # Research and fieldwork notes
└── fieldwork/              # Interview notes and observation records
```

## Data Schema

Complaints are stored in `data/data.csv` with 13 columns:

| Column | Type | Description |
|--------|------|-------------|
| complaint_id | string | Unique identifier (e.g. C001 or CC-20241215120000) |
| date_reported | date | ISO 8601 date the complaint was submitted |
| hostel_block | string | Hostel block name (e.g. A Block, F Block) |
| room_number | string | Room number within the block |
| category | string | Issue category (Electrical, Plumbing, Furniture, Cleaning, Internet, AC/Heating, Other) |
| description | string | Free-text description of the problem |
| reported_by | string | Username of the student who submitted |
| contact | string | Student phone or email for follow-up |
| priority | string | Assigned priority: Critical, High, Medium, or Low |
| status | string | Workflow status: Pending, In Progress, or Resolved |
| assigned_to | string | Name of the staff member handling the complaint |
| date_resolved | date | ISO 8601 date the complaint was resolved (empty if open) |
| resolution_notes | string | Notes recorded when resolving the complaint |

## Demo Video

▶️ [Watch the 3-minute demo on Google Drive](https://drive.google.com/drive/folders/1H4cnVCVzivzDjqjciYaMRTr2qkkFRKid?usp=drive_link)

The demo covers student login, complaint submission, admin dashboard, priority engine, and status update workflow.

## Screenshots

### Login Page
![Login](evidence/screenshot/Screenshot%202026-11-18%20110130.png)

### Submit Complaint (Student)
![Submit Complaint](evidence/screenshot/Screenshot%202026-11-18%20110151.png)

### My Complaints (Student)
![My Complaints](evidence/screenshot/Screenshot%202026-11-18%20110221.png)

### Admin Dashboard
![Admin Dashboard](evidence/screenshot/Screenshot%202026-11-18%20110227.png)

### All Complaints with Filters (Admin)
![All Complaints](evidence/screenshot/Screenshot%202026-11-18%20110248.png)

### Manage Complaint (Admin)
![Manage Complaint](evidence/screenshot/Screenshot%202026-11-18%20110259.png)

## Known Limitations

- No real authentication — credentials are hardcoded in modules/auth.py; not production-safe
- Single-file CSV backend — not suitable for concurrent multi-user writes
- No email or push notifications when complaint status changes
- No file/image upload for attaching evidence to complaints
