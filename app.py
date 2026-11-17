"""
CampusCare – Smart Campus Maintenance & Complaint Management System
NIT Jamshedpur Hostel
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from modules.data_manager import (
    load_data, save_data, add_complaint, update_complaint,
    delete_complaint, get_complaint, export_csv, CSV_COLUMNS
)
from modules.priority_engine import (
    calculate_priority, get_overdue_complaints, get_critical_pending, THRESHOLDS
)
from modules.analytics import (
    summary_stats, category_distribution, priority_distribution,
    status_distribution, complaint_trend, recurring_issues, top_locations,
    avg_resolution_by_category
)
from modules.validators import VALID_CATEGORIES, VALID_STATUSES, VALID_PRIORITIES

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
WORKSPACE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(WORKSPACE, "data", "data.csv")
SAMPLE_PATH = os.path.join(WORKSPACE, "data", "sample_data.csv")

COLOR_STATUS = {"Pending": "🔴", "In Progress": "🟡", "Resolved": "🟢"}
COLOR_PRIORITY = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="CampusCare",
    page_icon="🏫",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🏫 CampusCare")
    st.caption("Smart Campus Maintenance\n& Complaint Management")
    st.divider()

    page = st.radio(
        "Navigation",
        ["📊 Dashboard", "📋 Complaints", "⚙️ Priority Engine", "🔁 Recurring Issues", "⏳ Pending Monitor"],
        label_visibility="collapsed"
    )

    st.divider()
    use_demo = st.toggle("🧪 Load Demo Data", value=False)
    if use_demo:
        st.warning("Demo mode: showing synthetic data only.")

data_path = SAMPLE_PATH if use_demo else DATA_PATH

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
@st.cache_data(ttl=5)
def load(path):
    return load_data(path)

df = load(data_path)

if use_demo:
    st.warning("⚠️ Demo data active — these are synthetic records for demonstration only.")

# ===========================================================================
# PAGE: DASHBOARD
# ===========================================================================
if page == "📊 Dashboard":
    st.title("📊 Dashboard")
    stats = summary_stats(df)

    # Overdue alert
    if stats["overdue"] > 0:
        st.error(f"🚨 {stats['overdue']} complaint(s) are overdue (pending > {THRESHOLDS['overdue_days']} days). Please review immediately.")

    # KPI Cards
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    c1.metric("Total", stats["total"])
    c2.metric("Pending", stats["pending"])
    c3.metric("In Progress", stats["in_progress"])
    c4.metric("Resolved", stats["resolved"])
    c5.metric("Critical", stats["critical"])
    c6.metric("Overdue", stats["overdue"])
    c7.metric("Avg Resolution (days)", stats["avg_resolution_days"])

    if df.empty:
        st.info("No complaint data yet. Add complaints or switch to Demo Data to see charts.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            cat_df = category_distribution(df)
            if not cat_df.empty:
                fig = px.bar(cat_df, x="category", y="count", title="Complaints by Category",
                             color="category", color_discrete_sequence=px.colors.qualitative.Set2)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            pri_df = priority_distribution(df)
            if not pri_df.empty:
                fig = px.pie(pri_df, names="priority", values="count", title="Priority Distribution",
                             color_discrete_sequence=px.colors.qualitative.Set2)
                st.plotly_chart(fig, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            stat_df = status_distribution(df)
            if not stat_df.empty:
                fig = px.pie(stat_df, names="status", values="count", title="Status Distribution",
                             hole=0.4, color_discrete_sequence=px.colors.qualitative.Plotly)
                st.plotly_chart(fig, use_container_width=True)

        with col4:
            trend_df = complaint_trend(df)
            if not trend_df.empty:
                fig = px.line(trend_df, x="week", y="count", title="Weekly Complaint Trend",
                              markers=True)
                st.plotly_chart(fig, use_container_width=True)

# ===========================================================================
# PAGE: COMPLAINTS
# ===========================================================================
elif page == "📋 Complaints":
    st.title("📋 Complaint Management")
    tab1, tab2, tab3, tab4 = st.tabs(["View All", "Add New", "Edit / Update", "Delete"])

    # --- View All ---
    with tab1:
        st.subheader("All Complaints")
        if df.empty:
            st.info("No complaints recorded yet.")
        else:
            col1, col2, col3, col4 = st.columns(4)
            f_status = col1.selectbox("Status", ["All"] + VALID_STATUSES, key="vs")
            f_cat = col2.selectbox("Category", ["All"] + VALID_CATEGORIES, key="vc")
            f_pri = col3.selectbox("Priority", ["All"] + VALID_PRIORITIES, key="vp")
            f_block = col4.selectbox("Block", ["All"] + sorted(df["hostel_block"].dropna().unique().tolist()), key="vb")

            search = st.text_input("🔍 Search in description", key="vsearch")

            view_df = df.copy()
            if f_status != "All":
                view_df = view_df[view_df["status"] == f_status]
            if f_cat != "All":
                view_df = view_df[view_df["category"] == f_cat]
            if f_pri != "All":
                view_df = view_df[view_df["priority"] == f_pri]
            if f_block != "All":
                view_df = view_df[view_df["hostel_block"] == f_block]
            if search:
                view_df = view_df[view_df["description"].astype(str).str.contains(search, case=False, na=False)]

            st.write(f"Showing {len(view_df)} of {len(df)} complaint(s)")

            # Color-coded status badges
            display_df = view_df.copy()
            display_df["Status"] = display_df["status"].map(lambda s: f"{COLOR_STATUS.get(s, '')} {s}")
            display_df["Priority"] = display_df["priority"].map(lambda p: f"{COLOR_PRIORITY.get(p, '')} {p}")

            st.dataframe(
                display_df[["complaint_id", "date_reported", "hostel_block", "room_number",
                             "category", "description", "Priority", "Status", "assigned_to"]],
                use_container_width=True, hide_index=True
            )

            csv_str = export_csv(view_df, {})
            st.download_button("⬇️ Export to CSV", csv_str, "complaints_export.csv", "text/csv")

    # --- Add New ---
    with tab2:
        st.subheader("Add New Complaint")
        with st.form("add_form"):
            col1, col2 = st.columns(2)
            block = col1.text_input("Hostel Block *")
            room = col2.text_input("Room Number / Location *")
            col3, col4 = st.columns(2)
            category = col3.selectbox("Category *", VALID_CATEGORIES)
            date_rep = col4.date_input("Date Reported *", value=date.today())
            description = st.text_area("Description *", height=100)
            col5, col6 = st.columns(2)
            reported_by = col5.text_input("Reported By *")
            contact = col6.text_input("Contact")
            col7, col8 = st.columns(2)
            assigned_to = col7.text_input("Assigned Staff")
            status = col8.selectbox("Status", VALID_STATUSES)

            # Priority suggestion
            if block and room and category and description:
                temp_record = {
                    "hostel_block": block, "room_number": room,
                    "category": category, "description": description,
                    "date_reported": str(date_rep), "status": status
                }
                suggested_priority, explanation = calculate_priority(temp_record, df)
            else:
                suggested_priority, explanation = "Low", "Fill all fields for smart suggestion."

            priority = st.selectbox(
                f"Priority (suggested: {suggested_priority})",
                VALID_PRIORITIES,
                index=VALID_PRIORITIES.index(suggested_priority)
            )
            st.caption(f"🤖 Priority reasoning: {explanation}")

            submitted = st.form_submit_button("Submit Complaint")

        if submitted:
            record = {
                "date_reported": str(date_rep),
                "hostel_block": block,
                "room_number": room,
                "category": category,
                "description": description,
                "reported_by": reported_by,
                "contact": contact,
                "priority": priority,
                "status": status,
                "assigned_to": assigned_to,
                "date_resolved": "",
                "resolution_notes": "",
            }
            if not use_demo:
                ok, msg = add_complaint(record, DATA_PATH)
                if ok:
                    st.success(msg)
                    st.cache_data.clear()
                else:
                    st.error(msg)
            else:
                st.warning("Demo mode active — cannot add complaints to demo data. Switch off demo toggle first.")

    # --- Edit / Update ---
    with tab3:
        st.subheader("Edit / Update Complaint")
        if df.empty:
            st.info("No complaints to edit.")
        else:
            complaint_ids = df["complaint_id"].tolist()
            selected_id = st.selectbox("Select Complaint ID", complaint_ids, key="edit_id")
            rec = get_complaint(selected_id, df)
            if rec:
                with st.form("edit_form"):
                    col1, col2 = st.columns(2)
                    new_status = col1.selectbox("Status", VALID_STATUSES,
                                                index=VALID_STATUSES.index(str(rec.get("status", "Pending"))) if str(rec.get("status", "Pending")) in VALID_STATUSES else 0)
                    new_priority = col2.selectbox("Priority", VALID_PRIORITIES,
                                                  index=VALID_PRIORITIES.index(str(rec.get("priority", "Low"))) if str(rec.get("priority", "Low")) in VALID_PRIORITIES else 3)
                    new_assigned = st.text_input("Assigned To", value=str(rec.get("assigned_to", "") or ""))
                    new_resolved = st.text_input("Date Resolved (YYYY-MM-DD)", value=str(rec.get("date_resolved", "") or ""))
                    new_notes = st.text_area("Resolution Notes", value=str(rec.get("resolution_notes", "") or ""))
                    update_btn = st.form_submit_button("Update")

                if update_btn:
                    updates = {
                        "status": new_status, "priority": new_priority,
                        "assigned_to": new_assigned, "date_resolved": new_resolved,
                        "resolution_notes": new_notes
                    }
                    if not use_demo:
                        ok, msg = update_complaint(selected_id, updates, DATA_PATH)
                        if ok:
                            st.success(msg)
                            st.cache_data.clear()
                        else:
                            st.error(msg)
                    else:
                        st.warning("Demo mode: cannot edit demo data.")

    # --- Delete ---
    with tab4:
        st.subheader("Delete Complaint")
        if df.empty:
            st.info("No complaints to delete.")
        else:
            del_id = st.selectbox("Select Complaint ID to Delete", df["complaint_id"].tolist(), key="del_id")
            rec = get_complaint(del_id, df)
            if rec:
                st.write("**Preview:**")
                st.json({k: v for k, v in rec.items() if v and str(v) != "nan"})
                confirm = st.text_input('Type "DELETE" to confirm')
                if st.button("🗑️ Delete Permanently"):
                    if confirm == "DELETE":
                        if not use_demo:
                            ok, msg = delete_complaint(del_id, DATA_PATH)
                            if ok:
                                st.success(msg)
                                st.cache_data.clear()
                            else:
                                st.error(msg)
                        else:
                            st.warning("Demo mode: cannot delete demo data.")
                    else:
                        st.error('Please type "DELETE" exactly to confirm deletion.')

# ===========================================================================
# PAGE: PRIORITY ENGINE
# ===========================================================================
elif page == "⚙️ Priority Engine":
    st.title("⚙️ Smart Priority Engine")

    st.subheader("Test Priority Calculation")
    with st.form("priority_form"):
        col1, col2, col3 = st.columns(3)
        t_block = col1.text_input("Hostel Block")
        t_room = col2.text_input("Room Number")
        t_cat = col3.selectbox("Category", VALID_CATEGORIES)
        t_desc = st.text_area("Description")
        col4, col5 = st.columns(2)
        t_date = col4.date_input("Date Reported", value=date.today())
        t_status = col5.selectbox("Current Status", VALID_STATUSES)
        calc_btn = st.form_submit_button("Calculate Priority")

    if calc_btn and t_desc:
        test_rec = {
            "hostel_block": t_block, "room_number": t_room,
            "category": t_cat, "description": t_desc,
            "date_reported": str(t_date), "status": t_status
        }
        result_priority, result_explanation = calculate_priority(test_rec, df)
        st.success(f"**Calculated Priority: {COLOR_PRIORITY.get(result_priority, '')} {result_priority}**")
        st.info(f"**Reasoning:** {result_explanation}")

    st.divider()
    st.subheader("Current Critical / High Pending Complaints")
    critical_df = get_critical_pending(df)
    if critical_df.empty:
        st.info("No critical or high-priority pending complaints at this time.")
    else:
        st.dataframe(critical_df[["complaint_id", "date_reported", "hostel_block", "room_number",
                                  "category", "description", "priority", "status", "assigned_to"]],
                     use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Configurable Thresholds")
    st.json(THRESHOLDS)

# ===========================================================================
# PAGE: RECURRING ISSUES
# ===========================================================================
elif page == "🔁 Recurring Issues":
    st.title("🔁 Recurring Issue Detection")

    recur_df = recurring_issues(df)
    if recur_df.empty:
        st.info("No recurring issues detected. Add more complaint records to see patterns.")
    else:
        st.write(f"**{len(recur_df)} recurring location+category pair(s) found.**")

        # Flag if 3+ issues in same location
        flag_df = recur_df[recur_df["count"] >= 3]
        if not flag_df.empty:
            for _, row in flag_df.iterrows():
                st.error(f"🚩 Attention: {row['hostel_block']} Room {row['room_number']} has {row['count']} {row['category']} complaints!")

        st.dataframe(recur_df, use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("Top Problem Locations")
        loc_df = top_locations(df)
        if not loc_df.empty:
            fig = px.bar(loc_df, x="hostel_block", y="count", title="Complaints by Block",
                         color="hostel_block", color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig, use_container_width=True)

# ===========================================================================
# PAGE: PENDING MONITOR
# ===========================================================================
elif page == "⏳ Pending Monitor":
    st.title("⏳ Pending Complaint Monitor")

    open_df = df[df["status"].astype(str).str.strip().isin(["Pending", "In Progress"])].copy()

    if open_df.empty:
        st.info("No open complaints. All issues are resolved!")
    else:
        today = pd.Timestamp.today().normalize()
        open_df["_date"] = pd.to_datetime(open_df["date_reported"], errors="coerce")
        open_df["age_days"] = (today - open_df["_date"]).dt.days.fillna(0).astype(int)

        # Priority filter
        f_pri = st.selectbox("Filter by Priority", ["All"] + VALID_PRIORITIES, key="pm_pri")
        if f_pri != "All":
            open_df = open_df[open_df["priority"] == f_pri]

        # Color coding
        def row_color(age):
            if age > 7:
                return "🔴"
            elif age >= 5:
                return "🟠"
            else:
                return "🟢"

        open_df["Age Status"] = open_df["age_days"].apply(row_color)
        open_df["Overdue"] = open_df["age_days"].apply(lambda d: "Yes" if d > 7 else "No")

        st.dataframe(
            open_df[["Age Status", "complaint_id", "date_reported", "age_days", "Overdue",
                      "hostel_block", "room_number", "category", "priority", "status", "assigned_to"]],
            use_container_width=True, hide_index=True
        )

        st.divider()
        st.subheader("Unresolved High-Priority Summary")
        high_df = df[
            df["priority"].astype(str).str.strip().isin(["Critical", "High"]) &
            df["status"].astype(str).str.strip().isin(["Pending", "In Progress"])
        ]
        if high_df.empty:
            st.success("No unresolved Critical or High priority complaints.")
        else:
            st.warning(f"{len(high_df)} unresolved Critical/High priority complaint(s) require attention.")
            st.dataframe(high_df[["complaint_id", "date_reported", "hostel_block", "room_number",
                                   "category", "priority", "status"]],
                         use_container_width=True, hide_index=True)
