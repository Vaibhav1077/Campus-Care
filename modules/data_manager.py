"""
CampusCare – CSV data management with atomic writes.
"""
import os
import tempfile
import shutil
from datetime import datetime
import pandas as pd
from modules.validators import validate_complaint, generate_complaint_id, detect_duplicate

CSV_COLUMNS = [
    "complaint_id", "date_reported", "hostel_block", "room_number",
    "category", "description", "reported_by", "contact",
    "priority", "status", "assigned_to", "date_resolved", "resolution_notes"
]


def load_data(path: str) -> pd.DataFrame:
    """Read CSV safely. Returns empty DataFrame with correct columns if file is empty or missing."""
    if not os.path.exists(path):
        return pd.DataFrame(columns=CSV_COLUMNS)
    try:
        df = pd.read_csv(path, dtype=str)
        # Ensure all expected columns exist
        for col in CSV_COLUMNS:
            if col not in df.columns:
                df[col] = ""
        df = df[CSV_COLUMNS]
        # Drop rows that are entirely NaN (blank lines)
        df = df.dropna(how="all").reset_index(drop=True)
        return df
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        return pd.DataFrame(columns=CSV_COLUMNS)


def save_data(df: pd.DataFrame, path: str) -> None:
    """Atomic write: write to temp file then rename."""
    dir_name = os.path.dirname(os.path.abspath(path))
    os.makedirs(dir_name, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
    try:
        with os.fdopen(fd, 'w', newline='', encoding='utf-8') as f:
            df.to_csv(f, index=False)
        shutil.move(tmp_path, path)
    except Exception:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise


def add_complaint(record: dict, path: str) -> tuple[bool, str]:
    """Validate, check duplicate, append complaint. Returns (success, message)."""
    df = load_data(path)

    # Generate ID if not provided
    if not record.get("complaint_id") or str(record.get("complaint_id", "")).strip() == "":
        record["complaint_id"] = generate_complaint_id(df["complaint_id"].tolist())

    is_valid, errors = validate_complaint(record)
    if not is_valid:
        return False, "Validation failed: " + "; ".join(errors)

    if detect_duplicate(record, df):
        return False, "Duplicate complaint detected: same block, room, category and date already exists."

    new_row = {col: record.get(col, "") for col in CSV_COLUMNS}
    new_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(new_df, path)
    return True, f"Complaint {record['complaint_id']} added successfully."


def update_complaint(complaint_id: str, updates: dict, path: str) -> tuple[bool, str]:
    """Update fields of an existing complaint."""
    df = load_data(path)
    mask = df["complaint_id"].astype(str).str.strip() == str(complaint_id).strip()
    if not mask.any():
        return False, f"Complaint '{complaint_id}' not found."
    for key, value in updates.items():
        if key in CSV_COLUMNS and key != "complaint_id":
            df.loc[mask, key] = value
    save_data(df, path)
    return True, f"Complaint '{complaint_id}' updated successfully."


def delete_complaint(complaint_id: str, path: str) -> tuple[bool, str]:
    """Delete a complaint by ID."""
    df = load_data(path)
    mask = df["complaint_id"].astype(str).str.strip() == str(complaint_id).strip()
    if not mask.any():
        return False, f"Complaint '{complaint_id}' not found."
    df = df[~mask].reset_index(drop=True)
    save_data(df, path)
    return True, f"Complaint '{complaint_id}' deleted."


def get_complaint(complaint_id: str, df: pd.DataFrame) -> dict | None:
    """Return a complaint record as dict, or None if not found."""
    mask = df["complaint_id"].astype(str).str.strip() == str(complaint_id).strip()
    matches = df[mask]
    if matches.empty:
        return None
    return matches.iloc[0].to_dict()


def export_csv(df: pd.DataFrame, filters: dict) -> str:
    """Apply filters and return CSV string for download."""
    filtered = df.copy()
    for col, value in filters.items():
        if value and value != "All" and col in filtered.columns:
            filtered = filtered[filtered[col].astype(str).str.strip() == str(value).strip()]
    return filtered.to_csv(index=False)
