# CampusCare – Final Submission Checklist

Use this checklist before submitting the assignment. Statuses are based on the actual repository contents as of the current date.

---

## Step 1 – Research

| Item | File | Status |
|------|------|--------|
| Problem statement (5 lines) | `docs/research.md` | ✅ Complete |
| Two existing solutions with limitations | `docs/research.md` | ✅ Complete |
| Why existing solutions are insufficient | `docs/research.md` | ✅ Complete |
| Two verified academic sources with notes | `docs/research.md` | ✅ Complete |
| Why CampusCare is needed | `docs/research.md` | ✅ Complete |

---

## Step 2 – Fieldwork

| Item | File | Status |
|------|------|--------|
| Interview questionnaire (10 questions) | `fieldwork/interview_questionnaire.md` | ✅ Complete |
| Interview notes template | `fieldwork/interview_notes.md` | ✅ Complete (template ready) |
| **Actual interview conducted and filled** | `fieldwork/interview_notes.md` | ⏳ Pending — must be done by you |
| Field observation template | `fieldwork/observation_notes.md` | ✅ Complete (template ready) |
| **Actual observations filled in** | `fieldwork/observation_notes.md` | ✅ Partial — photos documented; observer name, block, room pending |
| Complaint dataset (20+ records) | `data/data.csv` | ✅ Complete (26 records) |
| Dataset clearly labelled as synthetic | `docs/data-notes.md` | ✅ Complete |
| Data analysis document | `fieldwork/data_analysis.md` | ✅ Complete |
| Evidence directory | `fieldwork/evidence/` | ✅ Created |
| Real photographs added to evidence | `fieldwork/evidence/` | ✅ Complete — 2 photos added (2026-11-18) |

---

## Step 3 – Build

| Item | File / Location | Status |
|------|----------------|--------|
| Working Streamlit application | `app.py` | ✅ Complete |
| Student login and portal | `app.py` | ✅ Complete |
| Admin login and portal | `app.py` | ✅ Complete |
| Complaint submission with validation | `app.py` | ✅ Complete |
| Unique complaint ID generation | `modules/validators.py` | ✅ Complete |
| Priority engine integrated | `modules/priority_engine.py`, `app.py` | ✅ Complete |
| Admin dashboard with charts | `app.py` | ✅ Complete |
| Filter and search on complaints | `app.py` | ✅ Complete |
| CSV persistence and data integrity | `modules/data_manager.py` | ✅ Complete |
| Automated tests (pytest) | `tests/test_campuscare.py` | ✅ Complete (20 tests) |
| README.md with all required sections | `README.md` | ✅ Complete |
| **Application screenshots** | Not present | ⏳ Pending — take and add after running the app |

---

## Step 4 – Reflection

| Item | File | Status |
|------|------|--------|
| Reflection document | `reflection.md` | ✅ Complete |

---

## Submission Extras

| Item | Status | Notes |
|------|--------|-------|
| GitHub repository with commits | ✅ Complete | https://github.com/Vaibhav1077/Campus-Care |
| **3 recent commits pushed to GitHub** | ⏳ Pending — network was blocked; run `git push origin master` |
| AI conversation export (if required) | 🔍 Needs verification | Check your assignment instructions — if required, export your AI chat history from the tool used |
| Demo video | ⏳ Pending — record yourself | Run the app, show student and admin login, submit a complaint, update status |

---

## How to Push Pending Commits

Run this once your internet connection to GitHub is working:

```powershell
cd "c:\Users\iamva\OneDrive\Desktop\CampusCare"
git push origin master
```

This will push commits: `d3ee42f`, `ea19628`, `43e3e7d`

---

## How to Run the Application for Screenshots

```powershell
cd "c:\Users\iamva\OneDrive\Desktop\CampusCare"
python3.14 -m streamlit run app.py
```

Then open **http://localhost:8501** and take screenshots of:
1. Login page
2. Student — Submit Complaint form
3. Student — My Complaints page
4. Admin — Dashboard with charts
5. Admin — All Complaints with filters
6. Admin — Manage Complaint page

---

*Checklist version: 1.0 — CampusCare Step 4*
