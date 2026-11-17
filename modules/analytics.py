"""
CampusCare – Analytics and reporting functions.
All functions handle empty DataFrames gracefully.
"""
import pandas as pd
from datetime import datetime
from modules.priority_engine import THRESHOLDS


def summary_stats(df: pd.DataFrame) -> dict:
    """Return summary KPI statistics."""
    empty = {
        "total": 0, "pending": 0, "in_progress": 0, "resolved": 0,
        "critical": 0, "overdue": 0, "avg_resolution_days": 0.0
    }
    if df is None or df.empty:
        return empty

    total = len(df)
    pending = int((df["status"].astype(str).str.strip() == "Pending").sum())
    in_progress = int((df["status"].astype(str).str.strip() == "In Progress").sum())
    resolved = int((df["status"].astype(str).str.strip() == "Resolved").sum())
    critical = int((df["priority"].astype(str).str.strip() == "Critical").sum())

    # Overdue: Pending/In Progress older than threshold
    today = pd.Timestamp.today().normalize()
    threshold = THRESHOLDS["overdue_days"]
    open_df = df[df["status"].astype(str).str.strip().isin(["Pending", "In Progress"])].copy()
    open_df["_date"] = pd.to_datetime(open_df["date_reported"], errors="coerce")
    overdue = int((open_df["_date"].notna() & ((today - open_df["_date"]).dt.days > threshold)).sum())

    # Average resolution time
    resolved_df = df[df["status"].astype(str).str.strip() == "Resolved"].copy()
    resolved_df["_start"] = pd.to_datetime(resolved_df["date_reported"], errors="coerce")
    resolved_df["_end"] = pd.to_datetime(resolved_df["date_resolved"], errors="coerce")
    valid = resolved_df[resolved_df["_start"].notna() & resolved_df["_end"].notna()]
    if not valid.empty:
        avg_days = float(((valid["_end"] - valid["_start"]).dt.days).mean())
    else:
        avg_days = 0.0

    return {
        "total": total, "pending": pending, "in_progress": in_progress,
        "resolved": resolved, "critical": critical, "overdue": overdue,
        "avg_resolution_days": round(avg_days, 1)
    }


def category_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Complaints per category."""
    if df is None or df.empty:
        return pd.DataFrame(columns=["category", "count"])
    result = df.groupby("category").size().reset_index(name="count")
    return result.sort_values("count", ascending=False).reset_index(drop=True)


def priority_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Complaints per priority level."""
    if df is None or df.empty:
        return pd.DataFrame(columns=["priority", "count"])
    result = df.groupby("priority").size().reset_index(name="count")
    return result.reset_index(drop=True)


def status_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Complaints per status."""
    if df is None or df.empty:
        return pd.DataFrame(columns=["status", "count"])
    result = df.groupby("status").size().reset_index(name="count")
    return result.reset_index(drop=True)


def complaint_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Complaints per week (ISO week)."""
    if df is None or df.empty:
        return pd.DataFrame(columns=["week", "count"])
    temp = df.copy()
    temp["_date"] = pd.to_datetime(temp["date_reported"], errors="coerce")
    temp = temp[temp["_date"].notna()]
    if temp.empty:
        return pd.DataFrame(columns=["week", "count"])
    temp["week"] = temp["_date"].dt.to_period("W").dt.start_time
    result = temp.groupby("week").size().reset_index(name="count")
    return result.sort_values("week").reset_index(drop=True)


def recurring_issues(df: pd.DataFrame) -> pd.DataFrame:
    """Location+category pairs with 2+ complaints, sorted by count descending."""
    if df is None or df.empty:
        return pd.DataFrame(columns=["hostel_block", "room_number", "category", "count"])
    result = (
        df.groupby(["hostel_block", "room_number", "category"])
        .size()
        .reset_index(name="count")
    )
    result = result[result["count"] >= 2]
    return result.sort_values("count", ascending=False).reset_index(drop=True)


def top_locations(df: pd.DataFrame) -> pd.DataFrame:
    """Hostel blocks with most complaints."""
    if df is None or df.empty:
        return pd.DataFrame(columns=["hostel_block", "count"])
    result = df.groupby("hostel_block").size().reset_index(name="count")
    return result.sort_values("count", ascending=False).reset_index(drop=True)


def avg_resolution_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Average resolution days per category (resolved complaints only)."""
    if df is None or df.empty:
        return pd.DataFrame(columns=["category", "avg_days"])
    resolved = df[df["status"].astype(str).str.strip() == "Resolved"].copy()
    if resolved.empty:
        return pd.DataFrame(columns=["category", "avg_days"])
    resolved["_start"] = pd.to_datetime(resolved["date_reported"], errors="coerce")
    resolved["_end"] = pd.to_datetime(resolved["date_resolved"], errors="coerce")
    valid = resolved[resolved["_start"].notna() & resolved["_end"].notna()].copy()
    if valid.empty:
        return pd.DataFrame(columns=["category", "avg_days"])
    valid["days"] = (valid["_end"] - valid["_start"]).dt.days
    result = valid.groupby("category")["days"].mean().reset_index()
    result.columns = ["category", "avg_days"]
    result["avg_days"] = result["avg_days"].round(1)
    return result.sort_values("avg_days", ascending=False).reset_index(drop=True)
