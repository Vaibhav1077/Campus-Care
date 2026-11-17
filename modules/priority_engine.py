"""
CampusCare – Transparent rule-based priority engine.

Rules (first-match base, then additive escalation):
1. Category/keyword base priority
2. Age escalation (never more than one step per rule, never Critical from pure-Low base via age)
3. Recurring boost (same block+room+category, 2+ complaints in 90 days)
"""
from datetime import datetime, date
import pandas as pd

THRESHOLDS = {
    "age_medium_days": 7,      # Pending > N days: Low → Medium
    "age_high_days": 14,       # Pending > N days: Medium or below → High
    "age_critical_days": 30,   # Pending > N days: High or below → Critical (only if base >= Medium)
    "recurring_window_days": 90,  # Window to detect recurring issues
    "recurring_min_count": 2,  # Minimum prior complaints to trigger recurring boost
    "overdue_days": 7,         # Pending/In Progress > N days = overdue
}

PRIORITY_ORDER = ["Low", "Medium", "High", "Critical"]

ELECTRICAL_CRITICAL_KEYWORDS = [
    "spark", "sparking", "shock", "fire", "burning", "smoke", "electrocution", "short circuit"
]
PLUMBING_HIGH_KEYWORDS = [
    "flood", "flooding", "no water", "burst", "overflow", "sewage", "blockage"
]


def _priority_index(p: str) -> int:
    try:
        return PRIORITY_ORDER.index(p)
    except ValueError:
        return 0


def _bump_up(priority: str, levels: int = 1) -> str:
    idx = _priority_index(priority)
    new_idx = min(idx + levels, len(PRIORITY_ORDER) - 1)
    return PRIORITY_ORDER[new_idx]


def _days_pending(record: dict) -> int:
    """Days since date_reported. Returns 0 if date is missing or invalid."""
    date_str = str(record.get("date_reported", "")).strip()
    if not date_str or date_str.lower() == "nan":
        return 0
    try:
        reported = datetime.strptime(date_str, "%Y-%m-%d").date()
        return (date.today() - reported).days
    except ValueError:
        return 0


def calculate_priority(record: dict, historical_df: pd.DataFrame) -> tuple[str, str]:
    """
    Calculate priority and return (priority_level, explanation).
    Does NOT auto-assign Critical based solely on age to Low-base complaints.
    """
    category = str(record.get("category", "")).strip()
    description = str(record.get("description", "")).lower()
    status = str(record.get("status", "Pending")).strip()

    reasons = []

    # --- Step 1: Category-based base priority ---
    base_priority = "Low"
    if category == "Electrical":
        if any(kw in description for kw in ELECTRICAL_CRITICAL_KEYWORDS):
            base_priority = "Critical"
            reasons.append(f"Electrical complaint with critical keyword (sparking/shock/fire) → base Critical.")
        else:
            base_priority = "Medium"
            reasons.append("Electrical complaint (general) → base Medium.")
    elif category == "Plumbing":
        if any(kw in description for kw in PLUMBING_HIGH_KEYWORDS):
            base_priority = "High"
            reasons.append(f"Plumbing complaint with severe keyword (flooding/no water) → base High.")
        else:
            base_priority = "Medium"
            reasons.append("Plumbing complaint (general) → base Medium.")
    else:
        base_priority = "Low"
        reasons.append(f"{category} complaint → base Low.")

    current_priority = base_priority

    # --- Step 2: Age escalation (only for Pending/In Progress) ---
    if status in ("Pending", "In Progress"):
        days = _days_pending(record)
        if days > 0:
            reasons.append(f"Complaint has been pending for {days} day(s).")

        age_applied = False

        # Rule: > age_medium_days AND base = Low → bump to Medium
        if (not age_applied
                and days > THRESHOLDS["age_medium_days"]
                and base_priority == "Low"):
            current_priority = _bump_up(current_priority)
            reasons.append(
                f"Pending > {THRESHOLDS['age_medium_days']} days with Low base → escalated to Medium."
            )
            age_applied = True

        # Rule: > age_high_days AND base <= Medium → bump to High
        if (not age_applied
                and days > THRESHOLDS["age_high_days"]
                and _priority_index(base_priority) <= _priority_index("Medium")):
            current_priority = max(
                [current_priority, "High"],
                key=lambda p: _priority_index(p)
            )
            reasons.append(
                f"Pending > {THRESHOLDS['age_high_days']} days with base <= Medium → escalated to High."
            )
            age_applied = True

        # Rule: > age_critical_days AND base >= Medium → bump to Critical
        # ONLY if original base was at least Medium (never Critical from Low base via age)
        if (not age_applied
                and days > THRESHOLDS["age_critical_days"]
                and _priority_index(base_priority) >= _priority_index("Medium")
                and _priority_index(current_priority) <= _priority_index("High")):
            current_priority = "Critical"
            reasons.append(
                f"Pending > {THRESHOLDS['age_critical_days']} days with base >= Medium → escalated to Critical."
            )
            age_applied = True

    # --- Step 3: Recurring boost ---
    if historical_df is not None and not historical_df.empty:
        block = str(record.get("hostel_block", "")).strip()
        room = str(record.get("room_number", "")).strip()
        window = THRESHOLDS["recurring_window_days"]
        min_count = THRESHOLDS["recurring_min_count"]

        try:
            cutoff = pd.Timestamp.today() - pd.Timedelta(days=window)
            hist = historical_df.copy()
            hist["date_reported"] = pd.to_datetime(hist["date_reported"], errors="coerce")
            matches = hist[
                (hist["hostel_block"].astype(str).str.strip() == block) &
                (hist["room_number"].astype(str).str.strip() == room) &
                (hist["category"].astype(str).str.strip() == category) &
                (hist["date_reported"] >= cutoff)
            ]
            if len(matches) >= min_count:
                old_priority = current_priority
                current_priority = _bump_up(current_priority)
                reasons.append(
                    f"Recurring issue: {len(matches)} complaints at {block} room {room} "
                    f"for {category} in last {window} days → bumped from {old_priority} to {current_priority}."
                )
        except Exception:
            pass

    explanation = " | ".join(reasons) if reasons else "Default base priority."
    return current_priority, explanation


def get_overdue_complaints(df: pd.DataFrame) -> pd.DataFrame:
    """Return Pending/In Progress complaints older than overdue_days threshold."""
    if df is None or df.empty:
        return pd.DataFrame(columns=df.columns if df is not None else [])
    threshold = THRESHOLDS["overdue_days"]
    today = pd.Timestamp.today().normalize()
    result = df.copy()
    result = result[result["status"].astype(str).str.strip().isin(["Pending", "In Progress"])]
    result["_date"] = pd.to_datetime(result["date_reported"], errors="coerce")
    result = result[result["_date"].notna()]
    result["_age"] = (today - result["_date"]).dt.days
    result = result[result["_age"] > threshold]
    return result.drop(columns=["_date", "_age"]).reset_index(drop=True)


def get_critical_pending(df: pd.DataFrame) -> pd.DataFrame:
    """Return Critical or High priority Pending/In Progress complaints."""
    if df is None or df.empty:
        return pd.DataFrame(columns=df.columns if df is not None else [])
    result = df[
        df["priority"].astype(str).str.strip().isin(["Critical", "High"]) &
        df["status"].astype(str).str.strip().isin(["Pending", "In Progress"])
    ]
    return result.reset_index(drop=True)
