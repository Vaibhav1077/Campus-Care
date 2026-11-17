# CampusCare – Data Analysis

> ⚠️ **All statistics in this document are derived from the synthetic dataset in `data/data.csv`.**
> Records C002–C026 are fabricated for testing purposes.
> Record C001 is a real entry submitted through the application.
> No statistics here represent actual hostel conditions or real student data.

All counts below were calculated by running `fieldwork_validate.py` against the live CSV file.

---

## 1. Dataset Overview

| Metric | Value |
|--------|-------|
| Total records | 26 |
| Columns (schema fields) | 13 |
| ID range | C001 – C026 |
| Date range | 2026-10-01 to 2026-11-17 |
| Hostel blocks covered | 6 (A, B, C, D, E, F) |
| Duplicate IDs | 0 |
| Validation errors | 0 |

---

## 2. Complaint Count by Category

| Category | Count | Percentage |
|----------|-------|------------|
| Electrical | 6 | 23.1% |
| Plumbing | 5 | 19.2% |
| Cleaning | 4 | 15.4% |
| Internet | 4 | 15.4% |
| Furniture | 4 | 15.4% |
| Other | 3 | 11.5% |
| **Total** | **26** | **100%** |

**Most common type:** Electrical (6 complaints, 23.1%)

---

## 3. Complaint Count by Status

| Status | Count | Percentage |
|--------|-------|------------|
| Resolved | 13 | 50.0% |
| Pending | 7 | 26.9% |
| In Progress | 6 | 23.1% |
| **Total** | **26** | **100%** |

- Half the complaints have been resolved.
- 7 complaints are still pending with no staff assigned.
- 6 are actively being worked on.

---

## 4. Priority Distribution

| Priority | Count | Percentage |
|----------|-------|------------|
| Medium | 11 | 42.3% |
| High | 8 | 30.8% |
| Critical | 4 | 15.4% |
| Low | 3 | 11.5% |
| **Total** | **26** | **100%** |

- 4 Critical complaints exist in the dataset — all 4 are Resolved, consistent with the expectation that critical issues are handled immediately.
- 8 High-priority complaints are present; some remain Pending or In Progress, which is a scenario the priority engine is designed to flag.

---

## 5. Hostel Block Distribution

| Hostel Block | Count |
|--------------|-------|
| A Block | 6 |
| B Block | 5 |
| C Block | 5 |
| D Block | 5 |
| E Block | 4 |
| F Block | 1 |
| **Total** | **26** |

A Block has the highest number of complaints in this dataset (6), spread across multiple categories and rooms. This is a synthetic distribution and does not reflect real usage patterns.

---

## 6. Resolution Quality Check

| Check | Result |
|-------|--------|
| Resolved records with resolution notes | 13 / 13 (100%) |
| Pending records with no staff assigned | 0 / 7 — all have been pre-assigned in the demo data to test admin view |
| Critical complaints all resolved | 4 / 4 (100%) |

---

## 7. Observations from the Synthetic Dataset

These are observations about the dataset's design, not findings from real fieldwork:

1. **Electrical complaints are most common** in this dataset, which reflects common hostel maintenance scenarios (fans, lights, sockets, extension boards).

2. **All Critical complaints are pre-resolved** to demonstrate the resolution workflow — in a real system, critical issues should be resolved same-day and this pattern would be a positive quality indicator.

3. **The dataset tests the priority engine** — 4 High-priority complaints are left Pending or In Progress to trigger the "Priority & Overdue" admin view.

4. **Recurring issue detection** can be tested using this data — multiple Electrical complaints in A Block and multiple Plumbing complaints in E Block appear across different rooms, which the analytics module can detect as block-level patterns.

5. **Resolution notes are consistent** — every Resolved record has a non-empty resolution note, which is the expected workflow when an admin marks a complaint as resolved.

6. **Contact field** uses placeholder college email addresses, not real phone numbers, ensuring no personal data is exposed.

---

## 8. How This Data Helps Maintenance Staff

If this were real data, a warden or admin using CampusCare could:

- See immediately that **7 complaints are still pending** and prioritise the 2 High-priority ones among them.
- Use the **Priority & Overdue** page to identify any High or Critical complaint that has been open too long without assignment.
- Use the **Recurring Issues** page to identify that A Block has accumulated 6 complaints — possibly indicating an older electrical installation that needs attention.
- Filter by hostel block on the **All Complaints** page to focus only on their assigned block.
- Track the **50% resolution rate** over the month and compare it to future months to assess improvement.

---

## 9. Validation Command

To re-run validation and reproduce these statistics:

```powershell
cd "c:\Users\iamva\OneDrive\Desktop\CampusCare"
python3.14 fieldwork_validate.py
```

The script uses `modules/validators.py` and `modules/data_manager.py` from the existing application — the same code that the app itself uses to load and validate data.

---

*Generated from: `data/data.csv` — 26 records (C001–C026)*
*Analysis script: `fieldwork_validate.py`*
*Dataset type: Synthetic (C002–C026) + 1 real entry (C001)*
