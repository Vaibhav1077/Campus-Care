# CampusCare – Dataset Notes

> **Important:** All records in `data/sample_data.csv` are synthetic. They were created to
> demonstrate the application and test its logic. They do not represent real student complaints,
> real hostel incidents, or any field observations. Contact values use placeholder college email
> addresses, not real phone numbers or personal information.

---

## 1. Files

| File | Purpose | Records |
|------|---------|---------|
| `data/data.csv` | Live data file — stores real complaints submitted through the app | 1 real entry (C001) |
| `data/sample_data.csv` | Synthetic demo dataset — used in Demo Mode only | 25 synthetic records (C101–C125) |

The app loads `data/data.csv` by default. Admins can switch to Demo Mode via the sidebar
checkbox to load `sample_data.csv` for testing and demonstration.

---

## 2. CSV Schema

All records follow the 13-column schema defined in `modules/data_manager.py`:

| Column | Type | Description |
|--------|------|-------------|
| `complaint_id` | String | Unique ID, format C001, C002, … |
| `date_reported` | String (YYYY-MM-DD) | Date complaint was submitted |
| `hostel_block` | String | Hostel block name (e.g. A Block) |
| `room_number` | String | Room number within the block |
| `category` | String (enum) | One of: Electrical, Plumbing, Cleaning, Furniture, Internet, Other |
| `description` | String | Free-text complaint description |
| `reported_by` | String | Username or name of the student |
| `contact` | String | Student contact — email used in demo data, never real phone numbers |
| `priority` | String (enum) | One of: Critical, High, Medium, Low |
| `status` | String (enum) | One of: Pending, In Progress, Resolved |
| `assigned_to` | String | Staff member assigned to the complaint (blank if unassigned) |
| `date_resolved` | String (YYYY-MM-DD) | Date resolved — blank if not yet resolved |
| `resolution_notes` | String | Notes added by admin on resolution — blank if pending |

---

## 3. Synthetic Dataset Summary (sample_data.csv)

**25 records — C101 to C125**

### Category distribution
| Category | Count |
|----------|-------|
| Electrical | 5 |
| Plumbing | 5 |
| Cleaning | 4 |
| Internet | 4 |
| Furniture | 4 |
| Other | 3 |

### Status distribution
| Status | Count |
|--------|-------|
| Resolved | 13 |
| In Progress | 6 |
| Pending | 6 |

### Priority distribution
| Priority | Count |
|----------|-------|
| Medium | 10 |
| High | 8 |
| Critical | 4 |
| Low | 3 |

### Hostel blocks covered
A Block, B Block, C Block, D Block, E Block (5 blocks, 4–6 records each)

### Date range
2026-10-01 to 2026-10-25 (25 days, one complaint per day)

---

## 4. Validation Results

Validated programmatically using `modules/validators.py` (`validate_complaint` function):

- ✅ No missing required fields
- ✅ No invalid categories, statuses or priorities
- ✅ All dates in correct YYYY-MM-DD format
- ✅ No duplicate records (same block + room + category + date)
- ✅ All 25 records loaded correctly by `load_data()`

---

## 5. Design Choices

- **Descriptions** are written as a student would naturally phrase them — specific, one or two sentences, without technical jargon.
- **Contact field** uses placeholder email addresses (`studentNN@college.edu`) to avoid exposing any real personal information.
- **Critical records** (C106, C111, C118, C120) represent safety or service-outage scenarios, used to test the priority engine and overdue complaint detection.
- **Recurring issue pattern:** A Block room 101 (Electrical), B Block room 202 (Furniture), and E Block (Plumbing) have multiple related complaints across different rooms, which allows the recurring issues module to detect patterns.
- **Resolution notes** are filled only for Resolved records, consistent with how the admin Manage Complaint page works.

---

## 6. Limitations

- All descriptions, names and contact details are fabricated. They should not be used to draw conclusions about real hostel conditions.
- The dataset does not reflect seasonal patterns, actual complaint frequency, or real resolution times at any institution.
- 25 records is sufficient to demonstrate all application features but is not statistically representative of a real hostel's complaint volume.
- The `reported_by` field uses generic identifiers (`student_01` etc.) because the demo does not have real student usernames registered in the system.
