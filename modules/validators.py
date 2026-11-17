"""
CampusCare – Input validation and ID generation.
"""
import re
from datetime import datetime
import pandas as pd

VALID_CATEGORIES = ["Electrical", "Plumbing", "Cleaning", "Furniture", "Internet", "Other"]
VALID_STATUSES = ["Pending", "In Progress", "Resolved"]
VALID_PRIORITIES = ["Critical", "High", "Medium", "Low"]
REQUIRED_FIELDS = [
    "date_reported", "hostel_block", "room_number", "category",
    "description", "reported_by", "priority", "status"
]


def validate_complaint(record: dict) -> tuple[bool, list[str]]:
    """Validate a complaint record. Returns (is_valid, list_of_errors)."""
    errors = []

    # Required fields
    for field in REQUIRED_FIELDS:
        value = record.get(field, "")
        if not value or str(value).strip() == "":
            errors.append(f"Required field '{field}' is missing or empty.")

    # Date format
    date_reported = record.get("date_reported", "")
    if date_reported and str(date_reported).strip():
        try:
            datetime.strptime(str(date_reported).strip(), "%Y-%m-%d")
        except ValueError:
            errors.append(f"'date_reported' must be in YYYY-MM-DD format, got '{date_reported}'.")

    date_resolved = record.get("date_resolved", "")
    if date_resolved and str(date_resolved).strip() and str(date_resolved).strip().lower() != "nan":
        try:
            datetime.strptime(str(date_resolved).strip(), "%Y-%m-%d")
        except ValueError:
            errors.append(f"'date_resolved' must be in YYYY-MM-DD format, got '{date_resolved}'.")

    # Category
    category = record.get("category", "")
    if category and str(category).strip() not in VALID_CATEGORIES:
        errors.append(f"Invalid category '{category}'. Must be one of: {', '.join(VALID_CATEGORIES)}.")

    # Status
    status = record.get("status", "")
    if status and str(status).strip() not in VALID_STATUSES:
        errors.append(f"Invalid status '{status}'. Must be one of: {', '.join(VALID_STATUSES)}.")

    # Priority
    priority = record.get("priority", "")
    if priority and str(priority).strip() not in VALID_PRIORITIES:
        errors.append(f"Invalid priority '{priority}'. Must be one of: {', '.join(VALID_PRIORITIES)}.")

    # Room number non-empty
    room_number = record.get("room_number", "")
    if room_number and not str(room_number).strip():
        errors.append("'room_number' must not be empty.")

    return len(errors) == 0, errors


def generate_complaint_id(existing_ids: list[str]) -> str:
    """Generate next complaint ID in C001, C002, ... format, ensuring uniqueness."""
    max_num = 0
    for cid in existing_ids:
        cid_str = str(cid).strip()
        if re.match(r'^C(\d+)$', cid_str):
            num = int(cid_str[1:])
            if num > max_num:
                max_num = num
    return f"C{max_num + 1:03d}"


def detect_duplicate(new_record: dict, existing: pd.DataFrame) -> bool:
    """Return True if a complaint with same block+room+category+date already exists."""
    if existing is None or existing.empty:
        return False
    mask = (
        (existing["hostel_block"].astype(str).str.strip() == str(new_record.get("hostel_block", "")).strip()) &
        (existing["room_number"].astype(str).str.strip() == str(new_record.get("room_number", "")).strip()) &
        (existing["category"].astype(str).str.strip() == str(new_record.get("category", "")).strip()) &
        (existing["date_reported"].astype(str).str.strip() == str(new_record.get("date_reported", "")).strip())
    )
    return bool(mask.any())
