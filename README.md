# CampusCare

A campus facility complaint management system built with Python and Streamlit.

## Features

- **Complaint Submission** — Students can submit facility issues with category and description
- **Status Tracking** — Track the lifecycle of each complaint (Pending → In Progress → Resolved)
- **Priority Engine** — Automatically assigns priority (High/Medium/Low) based on category and keywords
- **Analytics Dashboard** — Visual breakdown of complaints by category, status, and priority
- **Admin Panel** — View, filter, and update complaint statuses

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.x |
| UI Framework | Streamlit |
| Data Processing | pandas |
| Persistence | CSV (file-based) |

## Installation

```bash
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

## CSV Data Format

Complaints are stored in `data/data.csv` with the following columns:

| Column | Description |
|--------|-------------|
| `complaint_id` | Unique identifier (auto-generated) |
| `name` | Reporter's name |
| `category` | Issue category (e.g., Maintenance, Cleanliness, Safety) |
| `description` | Detailed description of the issue |
| `status` | Current status: Pending, In Progress, or Resolved |
| `priority` | Auto-assigned priority: High, Medium, or Low |
| `timestamp` | Date and time the complaint was submitted |

## Limitations

- No user authentication — anyone can view or modify complaints
- Single-user CSV backend — not suitable for concurrent multi-user access
- No real-time updates — page refresh required to see changes
- No email/notification system for status updates

## Demo

[ Insert 3-minute demo video/GIF link here ]
