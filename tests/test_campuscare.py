"""
CampusCare – Pytest test suite.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
import pandas as pd
from datetime import date, timedelta

from modules.validators import (
    validate_complaint, generate_complaint_id, detect_duplicate,
    VALID_CATEGORIES, VALID_STATUSES, VALID_PRIORITIES
)
from modules.data_manager import (
    load_data, save_data, add_complaint, update_complaint,
    delete_complaint, get_complaint, CSV_COLUMNS
)
from modules.priority_engine import (
    calculate_priority, get_overdue_complaints, get_critical_pending, THRESHOLDS
)
from modules.analytics import summary_stats, recurring_issues


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_complaint(**overrides):
    base = {
        "complaint_id": "C001",
        "date_reported": str(date.today()),
        "hostel_block": "A",
        "room_number": "101",
        "category": "Plumbing",
        "description": "Leaking tap in bathroom",
        "reported_by": "John Doe",
        "contact": "9876543210",
        "priority": "Medium",
        "status": "Pending",
        "assigned_to": "",
        "date_resolved": "",
        "resolution_notes": "",
    }
    base.update(overrides)
    return base


def make_df(*records):
    rows = [make_complaint(**r) for r in records]
    return pd.DataFrame(rows, columns=CSV_COLUMNS)


# ---------------------------------------------------------------------------
# validators.py
# ---------------------------------------------------------------------------

class TestGenerateId:
    def test_generate_id_empty(self):
        cid = generate_complaint_id([])
        assert cid == "C001"

    def test_generate_id_sequence(self):
        existing = [f"C{i:03d}" for i in range(1, 21)]
        cid = generate_complaint_id(existing)
        assert cid == "C021"


class TestValidateComplaint:
    def test_validate_valid_complaint(self):
        rec = make_complaint()
        ok, errors = validate_complaint(rec)
        assert ok is True
        assert errors == []

    def test_validate_missing_field(self):
        rec = make_complaint(description="")
        ok, errors = validate_complaint(rec)
        assert ok is False
        assert any("description" in e for e in errors)

    def test_validate_bad_date(self):
        rec = make_complaint(date_reported="15-06-2024")
        ok, errors = validate_complaint(rec)
        assert ok is False
        assert any("date_reported" in e for e in errors)

    def test_validate_bad_category(self):
        rec = make_complaint(category="Roofing")
        ok, errors = validate_complaint(rec)
        assert ok is False
        assert any("category" in e for e in errors)


class TestDuplicateDetection:
    def test_duplicate_detection(self):
        existing = make_df({"hostel_block": "B", "room_number": "202",
                            "category": "Electrical", "date_reported": "2024-06-01"})
        new_rec = make_complaint(hostel_block="B", room_number="202",
                                 category="Electrical", date_reported="2024-06-01")
        assert detect_duplicate(new_rec, existing) is True

    def test_no_duplicate_different_date(self):
        existing = make_df({"hostel_block": "B", "room_number": "202",
                            "category": "Electrical", "date_reported": "2024-06-01"})
        new_rec = make_complaint(hostel_block="B", room_number="202",
                                 category="Electrical", date_reported="2024-06-02")
        assert detect_duplicate(new_rec, existing) is False


# ---------------------------------------------------------------------------
# data_manager.py
# ---------------------------------------------------------------------------

class TestDataManager:
    def test_load_empty_csv(self, tmp_path):
        path = str(tmp_path / "test.csv")
        df = load_data(path)
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == CSV_COLUMNS
        assert len(df) == 0

    def test_add_complaint_creates_file(self, tmp_path):
        path = str(tmp_path / "test.csv")
        rec = make_complaint(complaint_id="")
        ok, msg = add_complaint(rec, path)
        assert ok is True, msg
        df = load_data(path)
        assert len(df) == 1
        assert df.iloc[0]["complaint_id"] == "C001"

    def test_update_complaint(self, tmp_path):
        path = str(tmp_path / "test.csv")
        rec = make_complaint(complaint_id="C001")
        add_complaint(rec, path)
        ok, msg = update_complaint("C001", {"status": "Resolved"}, path)
        assert ok is True, msg
        df = load_data(path)
        assert df.iloc[0]["status"] == "Resolved"

    def test_delete_complaint(self, tmp_path):
        path = str(tmp_path / "test.csv")
        rec = make_complaint(complaint_id="C001")
        add_complaint(rec, path)
        ok, msg = delete_complaint("C001", path)
        assert ok is True, msg
        df = load_data(path)
        assert len(df) == 0


# ---------------------------------------------------------------------------
# priority_engine.py
# ---------------------------------------------------------------------------

class TestPriorityEngine:
    def _empty_df(self):
        return pd.DataFrame(columns=CSV_COLUMNS)

    def test_priority_electrical_spark(self):
        rec = make_complaint(category="Electrical", description="sparking from socket",
                             date_reported=str(date.today()))
        priority, explanation = calculate_priority(rec, self._empty_df())
        assert priority == "Critical"

    def test_priority_age_escalation(self):
        # Low base (Cleaning) + 15 days pending → should escalate to Medium, not Critical
        old_date = str(date.today() - timedelta(days=15))
        rec = make_complaint(category="Cleaning", description="room not cleaned",
                             date_reported=old_date, status="Pending")
        priority, explanation = calculate_priority(rec, self._empty_df())
        # Low base + 15 days: age_medium rule (>7d, Low→Medium) fires first. NOT Critical.
        assert priority in ("Medium", "High"), f"Got {priority}: {explanation}"
        assert priority != "Critical"

    def test_priority_no_escalation_on_low_base(self):
        # Low base complaint at 35 days should stay at High max (never Critical from low base)
        old_date = str(date.today() - timedelta(days=35))
        rec = make_complaint(category="Furniture", description="broken chair",
                             date_reported=old_date, status="Pending")
        priority, explanation = calculate_priority(rec, self._empty_df())
        # Low base → escalate step by step: >7d→Medium, then age rules have fired once.
        # Rule: never Critical from pure-Low base via age alone.
        assert priority != "Critical", f"Should not be Critical for low-base: {explanation}"

    def test_overdue_complaints(self):
        old_date = str(date.today() - timedelta(days=10))
        recent_date = str(date.today() - timedelta(days=2))
        df = make_df(
            {"complaint_id": "C001", "date_reported": old_date, "status": "Pending"},
            {"complaint_id": "C002", "date_reported": recent_date, "status": "Pending"},
        )
        overdue = get_overdue_complaints(df)
        ids = overdue["complaint_id"].tolist()
        assert "C001" in ids
        assert "C002" not in ids

    def test_priority_plumbing_no_supply(self):
        # Critical plumbing keyword 'no water' should yield Critical or High
        rec = make_complaint(
            category="Plumbing",
            description="no water supply in bathroom since morning",
            date_reported=str(date.today()),
            status="Pending"
        )
        priority, explanation = calculate_priority(rec, self._empty_df())
        assert priority in ("Critical", "High"), f"Expected Critical or High, got {priority}: {explanation}"

    def test_priority_cleaning_low(self):
        # Cleaning complaint with non-urgent description should get Medium or Low
        rec = make_complaint(
            category="Cleaning",
            description="floor needs sweeping",
            date_reported=str(date.today()),
            status="Pending"
        )
        priority, explanation = calculate_priority(rec, self._empty_df())
        assert priority in ("Medium", "Low"), f"Expected Medium or Low, got {priority}: {explanation}"


# ---------------------------------------------------------------------------
# analytics.py
# ---------------------------------------------------------------------------

class TestAnalytics:
    def test_summary_stats_empty(self):
        df = pd.DataFrame(columns=CSV_COLUMNS)
        stats = summary_stats(df)
        assert stats["total"] == 0
        assert stats["pending"] == 0
        assert stats["avg_resolution_days"] == 0.0

    def test_recurring_issues_detected(self):
        df = make_df(
            {"complaint_id": "C001", "hostel_block": "A", "room_number": "101", "category": "Plumbing"},
            {"complaint_id": "C002", "hostel_block": "A", "room_number": "101", "category": "Plumbing"},
            {"complaint_id": "C003", "hostel_block": "B", "room_number": "202", "category": "Electrical"},
        )
        result = recurring_issues(df)
        assert len(result) == 1
        row = result.iloc[0]
        assert row["hostel_block"] == "A"
        assert row["room_number"] == "101"
        assert row["category"] == "Plumbing"
        assert row["count"] == 2
