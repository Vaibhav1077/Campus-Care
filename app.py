"""
CampusCare – Smart Campus Maintenance & Complaint Management System
Role-based redesign: Student and Admin views.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go

from modules import auth, theme
from modules.data_manager import (
    load_data, add_complaint, update_complaint, get_complaint, export_csv, CSV_COLUMNS
)
from modules.priority_engine import (
    calculate_priority, get_overdue_complaints, get_critical_pending
)
from modules.analytics import (
    summary_stats, category_distribution, status_distribution,
    recurring_issues
)
from modules.validators import VALID_CATEGORIES, VALID_STATUSES, VALID_PRIORITIES

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
WORKSPACE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(WORKSPACE, "data", "data.csv")
SAMPLE_PATH = os.path.join(WORKSPACE, "data", "sample_data.csv")

# ---------------------------------------------------------------------------
# Page config — must be first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="CampusCare",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject CSS on every render
st.markdown(theme.get_css(), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Login gate
# ---------------------------------------------------------------------------
if not auth.is_authenticated():
    # Centered login layout
    left, mid, right = st.columns([1, 2, 1])
    with mid:
        login_html = theme.card(
            f"""
            <h2 style="color:{theme.DARK_GREEN}; margin-top:0;">🏫 CampusCare Login</h2>
            <p style="color:{theme.CHARCOAL};">Smart Campus Maintenance &amp; Complaint Management</p>
            """
        )
        st.markdown(login_html, unsafe_allow_html=True)

        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", key="login_btn"):
            if username and password:
                ok, role = auth.login(username, password)
                if ok:
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
            else:
                st.error("Please enter both username and password.")

        st.markdown(
            f"""
            <div style="margin-top:16px; padding:10px; background:{theme.BEIGE};
                        border-radius:8px; font-size:0.85em; color:{theme.CHARCOAL};">
            <strong>Demo credentials</strong><br>
            Student &nbsp;→&nbsp; <code>student</code> / <code>student123</code><br>
            Admin &nbsp;&nbsp;→&nbsp; <code>admin</code> / <code>admin123</code>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.stop()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
role = auth.get_current_role()
user = auth.get_current_user()

with st.sidebar:
    st.markdown(
        f"""
        <div style="padding:12px 0 4px 0;">
            <span style="font-size:1.3em; font-weight:700;">🏫 CampusCare</span><br>
            <span style="font-size:0.8em; opacity:0.8;">Smart Campus Maintenance</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.12); border-radius:8px;
                    padding:8px 12px; margin:8px 0 12px 0; font-size:0.85em;">
            👤 <strong>{user}</strong><br>
            <span style="opacity:0.75; text-transform:capitalize;">{role}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    if role == "student":
        page = st.radio(
            "Navigation",
            ["📝 Submit Complaint", "📋 My Complaints", "🔍 Complaint Status", "ℹ️ Help & Info"],
            label_visibility="collapsed",
        )
        use_demo = False
    else:
        page = st.radio(
            "Navigation",
            ["📊 Dashboard", "📋 All Complaints", "⚙️ Manage Complaint",
             "🚨 Priority & Overdue", "🔄 Recurring Issues"],
            label_visibility="collapsed",
        )
        st.divider()
        use_demo = st.checkbox("🧪 Use Demo Data", value=False)

    st.divider()
    if st.button("🚪 Logout"):
        auth.logout()
        st.rerun()

# ---------------------------------------------------------------------------
# Data source
# ---------------------------------------------------------------------------
data_path = SAMPLE_PATH if use_demo else DATA_PATH

if use_demo:
    st.warning("⚠️ Viewing synthetic demo data", icon="⚠️")


@st.cache_data(ttl=5)
def _load(path: str) -> pd.DataFrame:
    return load_data(path)


df = _load(data_path)


# ===========================================================================
# STUDENT PAGES
# ===========================================================================

# ---------------------------------------------------------------------------
# Student — Submit Complaint
# ---------------------------------------------------------------------------
if page == "📝 Submit Complaint":
    st.title("📝 Submit a New Complaint")

    with st.form("submit_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        name = col1.text_input("Your Name *")
        contact = col2.text_input("Contact (phone / email)")

        col3, col4 = st.columns(2)
        hostel_block = col3.text_input("Hostel Block *")
        room_number = col4.text_input("Room Number *")

        category = st.selectbox(
            "Category *",
            ["Electrical", "Plumbing", "Furniture", "Cleaning",
             "Internet", "AC/Heating", "Other"],
        )
        description = st.text_area("Description *", height=120,
                                   placeholder="Describe the issue in detail…")

        submitted = st.form_submit_button("Submit Complaint")

    if submitted:
        errors = []
        if not name.strip():
            errors.append("Name is required.")
        if not hostel_block.strip():
            errors.append("Hostel Block is required.")
        if not room_number.strip():
            errors.append("Room Number is required.")
        if not description.strip():
            errors.append("Description is required.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            complaint_id = "CC-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            # Map AC/Heating and other non-standard categories to "Other" for validation
            mapped_category = category if category in VALID_CATEGORIES else "Other"
            record = {
                "complaint_id": complaint_id,
                "date_reported": datetime.date.today().isoformat(),
                "hostel_block": hostel_block.strip(),
                "room_number": room_number.strip(),
                "category": mapped_category,
                "description": description.strip(),
                "reported_by": auth.get_current_user(),
                "contact": contact.strip(),
                "priority": "Medium",
                "status": "Pending",
                "assigned_to": "",
                "date_resolved": "",
                "resolution_notes": "",
            }
            ok, msg = add_complaint(record, DATA_PATH)
            if ok:
                st.success(f"✅ Complaint submitted! ID: **{complaint_id}**")
                st.cache_data.clear()
            else:
                st.error(f"Submission failed: {msg}")


# ---------------------------------------------------------------------------
# Student — My Complaints
# ---------------------------------------------------------------------------
elif page == "📋 My Complaints":
    st.title("📋 My Complaints")

    my_df = df[df["reported_by"].astype(str) == auth.get_current_user()].copy()
    st.metric("Your Complaints", len(my_df))

    if my_df.empty:
        st.info("No complaints submitted yet.")
    else:
        display_cols = [
            "complaint_id", "date_reported", "hostel_block", "room_number",
            "category", "priority", "status",
        ]
        st.dataframe(my_df[display_cols], use_container_width=True, hide_index=True)


# ---------------------------------------------------------------------------
# Student — Complaint Status
# ---------------------------------------------------------------------------
elif page == "🔍 Complaint Status":
    st.title("🔍 Complaint Status")

    my_df = df[df["reported_by"].astype(str) == auth.get_current_user()].copy()

    if my_df.empty:
        st.info("You have no complaints on record.")
    else:
        complaint_ids = my_df["complaint_id"].tolist()
        selected_id = st.selectbox("Select Complaint ID", complaint_ids)
        rec = get_complaint(selected_id, my_df)
        if rec:
            badge = theme.status_badge(str(rec.get("status", "Pending")))
            card_html = theme.card(
                f"""
                <h3 style="margin-top:0; color:{theme.DARK_GREEN};">
                    {rec.get('complaint_id')} &nbsp; {badge}
                </h3>
                <table style="width:100%; border-collapse:collapse; font-size:0.92em;">
                  <tr><td style="padding:4px 8px; color:#666; width:160px;"><strong>Date Reported</strong></td>
                      <td style="padding:4px 8px;">{rec.get('date_reported','')}</td></tr>
                  <tr style="background:#fafafa;">
                      <td style="padding:4px 8px;"><strong>Hostel / Room</strong></td>
                      <td style="padding:4px 8px;">{rec.get('hostel_block','')} / {rec.get('room_number','')}</td></tr>
                  <tr><td style="padding:4px 8px;"><strong>Category</strong></td>
                      <td style="padding:4px 8px;">{rec.get('category','')}</td></tr>
                  <tr style="background:#fafafa;">
                      <td style="padding:4px 8px;"><strong>Priority</strong></td>
                      <td style="padding:4px 8px;">{rec.get('priority','')}</td></tr>
                  <tr><td style="padding:4px 8px;"><strong>Assigned To</strong></td>
                      <td style="padding:4px 8px;">{rec.get('assigned_to','') or '—'}</td></tr>
                  <tr style="background:#fafafa;">
                      <td style="padding:4px 8px;"><strong>Date Resolved</strong></td>
                      <td style="padding:4px 8px;">{rec.get('date_resolved','') or '—'}</td></tr>
                  <tr><td style="padding:4px 8px; vertical-align:top;"><strong>Description</strong></td>
                      <td style="padding:4px 8px;">{rec.get('description','')}</td></tr>
                  <tr style="background:#fafafa;">
                      <td style="padding:4px 8px; vertical-align:top;"><strong>Resolution Notes</strong></td>
                      <td style="padding:4px 8px;">{rec.get('resolution_notes','') or '—'}</td></tr>
                </table>
                """
            )
            st.markdown(card_html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Student — Help & Info
# ---------------------------------------------------------------------------
elif page == "ℹ️ Help & Info":
    st.title("ℹ️ Help & Information")

    st.markdown(
        theme.card(
            f"""
            <h3 style="color:{theme.DARK_GREEN}; margin-top:0;">How to Submit a Complaint</h3>
            <ol style="line-height:1.8;">
              <li>Go to <strong>Submit Complaint</strong> from the sidebar.</li>
              <li>Fill in your name, hostel block, room number, category, and a clear description.</li>
              <li>Click <strong>Submit Complaint</strong>. You will receive a unique Complaint ID.</li>
              <li>Use <strong>Complaint Status</strong> to track progress using your Complaint ID.</li>
            </ol>
            """
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        theme.card(
            f"""
            <h3 style="color:{theme.DARK_GREEN}; margin-top:0;">Categories</h3>
            <table style="width:100%; border-collapse:collapse; font-size:0.92em;">
              <tr style="background:{theme.BEIGE};">
                  <th style="padding:6px 10px; text-align:left;">Category</th>
                  <th style="padding:6px 10px; text-align:left;">Examples</th>
              </tr>
              <tr><td style="padding:6px 10px;">Electrical</td>
                  <td style="padding:6px 10px;">Power cuts, socket issues, flickering lights</td></tr>
              <tr style="background:#fafafa;"><td style="padding:6px 10px;">Plumbing</td>
                  <td style="padding:6px 10px;">Leaking taps, blocked drains, no water supply</td></tr>
              <tr><td style="padding:6px 10px;">Furniture</td>
                  <td style="padding:6px 10px;">Broken chairs, damaged wardrobes, missing tables</td></tr>
              <tr style="background:#fafafa;"><td style="padding:6px 10px;">Cleaning</td>
                  <td style="padding:6px 10px;">Dusty rooms, overflowing bins, pest issues</td></tr>
              <tr><td style="padding:6px 10px;">Internet</td>
                  <td style="padding:6px 10px;">No WiFi, slow connection, router faults</td></tr>
              <tr style="background:#fafafa;"><td style="padding:6px 10px;">AC/Heating</td>
                  <td style="padding:6px 10px;">AC not cooling, heater not working</td></tr>
              <tr><td style="padding:6px 10px;">Other</td>
                  <td style="padding:6px 10px;">Any issue not covered above</td></tr>
            </table>
            """
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        theme.card(
            f"""
            <h3 style="color:{theme.DARK_GREEN}; margin-top:0;">Expected Resolution Times</h3>
            <table style="width:100%; border-collapse:collapse; font-size:0.92em;">
              <tr style="background:{theme.BEIGE};">
                  <th style="padding:6px 10px; text-align:left;">Priority</th>
                  <th style="padding:6px 10px; text-align:left;">Target Resolution</th>
              </tr>
              <tr><td style="padding:6px 10px;">Critical</td><td style="padding:6px 10px;">Same day</td></tr>
              <tr style="background:#fafafa;"><td style="padding:6px 10px;">High</td>
                  <td style="padding:6px 10px;">Within 24 hours</td></tr>
              <tr><td style="padding:6px 10px;">Medium</td><td style="padding:6px 10px;">Within 3 days</td></tr>
              <tr style="background:#fafafa;"><td style="padding:6px 10px;">Low</td>
                  <td style="padding:6px 10px;">Within 7 days</td></tr>
            </table>
            """
        ),
        unsafe_allow_html=True,
    )


# ===========================================================================
# ADMIN PAGES
# ===========================================================================

# ---------------------------------------------------------------------------
# Admin — Dashboard
# ---------------------------------------------------------------------------
elif page == "📊 Dashboard":
    st.title("📊 Dashboard")

    stats = summary_stats(df)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Complaints", stats["total"])
    c2.metric("Pending", stats["pending"])
    c3.metric("In Progress", stats["in_progress"])
    c4.metric("Resolved", stats["resolved"])
    c5.metric("Critical", stats["critical"])

    if df.empty:
        st.info("No complaint data yet. Add complaints or switch to Demo Data to see charts.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            cat_df = category_distribution(df)
            if not cat_df.empty:
                fig = px.bar(
                    cat_df, x="category", y="count",
                    title="Complaints by Category",
                    color="category",
                    color_discrete_sequence=[
                        theme.DARK_GREEN, theme.SAGE_GREEN, theme.BEIGE,
                        "#7a9e8a", "#b8c9b0", "#d4c4a0",
                    ],
                )
                fig.update_layout(
                    paper_bgcolor=theme.CREAM,
                    plot_bgcolor=theme.CREAM,
                    font_color=theme.CHARCOAL,
                    showlegend=False,
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            stat_df = status_distribution(df)
            if not stat_df.empty:
                fig = px.pie(
                    stat_df, names="status", values="count",
                    title="Status Distribution",
                    hole=0.4,
                    color_discrete_sequence=[
                        theme.DARK_GREEN, theme.SAGE_GREEN, theme.BEIGE,
                    ],
                )
                fig.update_layout(
                    paper_bgcolor=theme.CREAM,
                    font_color=theme.CHARCOAL,
                )
                st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------------------
# Admin — All Complaints
# ---------------------------------------------------------------------------
elif page == "📋 All Complaints":
    st.title("📋 All Complaints")

    with st.sidebar:
        st.markdown("### Filters")
        blocks = ["All"] + sorted(df["hostel_block"].dropna().unique().tolist()) if not df.empty else ["All"]
        f_block = st.selectbox("Hostel Block", blocks, key="ab_block")
        f_cat = st.selectbox("Category", ["All"] + VALID_CATEGORIES, key="ab_cat")
        f_pri = st.selectbox("Priority", ["All"] + VALID_PRIORITIES, key="ab_pri")
        f_status = st.selectbox("Status", ["All"] + VALID_STATUSES, key="ab_status")

    view_df = df.copy()
    if f_block != "All":
        view_df = view_df[view_df["hostel_block"] == f_block]
    if f_cat != "All":
        view_df = view_df[view_df["category"] == f_cat]
    if f_pri != "All":
        view_df = view_df[view_df["priority"] == f_pri]
    if f_status != "All":
        view_df = view_df[view_df["status"] == f_status]

    st.metric("Showing", len(view_df))

    if view_df.empty:
        st.info("No complaints match the selected filters.")
    else:
        st.dataframe(view_df, use_container_width=True, hide_index=True)
        csv_str = export_csv(view_df, {})
        st.download_button(
            "⬇️ Download CSV",
            csv_str,
            "complaints_export.csv",
            "text/csv",
        )


# ---------------------------------------------------------------------------
# Admin — Manage Complaint
# ---------------------------------------------------------------------------
elif page == "⚙️ Manage Complaint":
    st.title("⚙️ Manage Complaint")

    if df.empty:
        st.info("No complaints to manage.")
    else:
        complaint_ids = df["complaint_id"].tolist()
        selected_id = st.selectbox("Select Complaint ID", complaint_ids, key="mgmt_id")
        rec = get_complaint(selected_id, df)

        if rec:
            badge = theme.status_badge(str(rec.get("status", "Pending")))
            st.markdown(
                theme.card(
                    f"""
                    <strong>{rec.get('complaint_id')}</strong> &nbsp; {badge} <br>
                    <small style="color:#666;">
                        {rec.get('hostel_block','')} / Room {rec.get('room_number','')} &nbsp;|&nbsp;
                        {rec.get('category','')} &nbsp;|&nbsp;
                        Reported: {rec.get('date_reported','')}
                    </small><br><br>
                    <em>{rec.get('description','')}</em>
                    """
                ),
                unsafe_allow_html=True,
            )

            with st.form("manage_form"):
                col1, col2 = st.columns(2)
                current_status = str(rec.get("status", "Pending"))
                status_idx = VALID_STATUSES.index(current_status) if current_status in VALID_STATUSES else 0
                new_status = col1.selectbox("Status", VALID_STATUSES, index=status_idx)

                assigned_to = col2.text_input(
                    "Assigned To", value=str(rec.get("assigned_to", "") or "")
                )

                resolution_notes = st.text_area(
                    "Resolution Notes", value=str(rec.get("resolution_notes", "") or "")
                )

                date_resolved_val = rec.get("date_resolved", "") or ""
                try:
                    dr_default = datetime.date.fromisoformat(str(date_resolved_val)) if date_resolved_val else datetime.date.today()
                except ValueError:
                    dr_default = datetime.date.today()

                date_resolved = st.date_input("Date Resolved (optional)", value=dr_default)

                save_btn = st.form_submit_button("💾 Save Changes")

            if save_btn:
                updates = {
                    "status": new_status,
                    "assigned_to": assigned_to,
                    "resolution_notes": resolution_notes,
                    "date_resolved": str(date_resolved) if new_status == "Resolved" else "",
                }
                if use_demo:
                    st.warning("Demo mode: cannot edit demo data.")
                else:
                    ok, msg = update_complaint(selected_id, updates, DATA_PATH)
                    if ok:
                        st.success(msg)
                        st.cache_data.clear()
                    else:
                        st.error(msg)


# ---------------------------------------------------------------------------
# Admin — Priority & Overdue
# ---------------------------------------------------------------------------
elif page == "🚨 Priority & Overdue":
    st.title("🚨 Priority & Overdue Complaints")

    critical_df = get_critical_pending(df)
    overdue_df = get_overdue_complaints(df)

    st.subheader("Critical / High Priority — Pending or In Progress")
    if critical_df.empty:
        st.success("No critical or high-priority pending complaints.")
    else:
        display_cols = [c for c in
                        ["complaint_id", "date_reported", "hostel_block", "room_number",
                         "category", "priority", "status", "assigned_to"]
                        if c in critical_df.columns]
        st.dataframe(critical_df[display_cols], use_container_width=True, hide_index=True)

    st.subheader("Overdue Complaints")
    if overdue_df.empty:
        st.success("No overdue complaints.")
    else:
        display_cols = [c for c in
                        ["complaint_id", "date_reported", "hostel_block", "room_number",
                         "category", "priority", "status", "assigned_to"]
                        if c in overdue_df.columns]
        st.dataframe(overdue_df[display_cols], use_container_width=True, hide_index=True)


# ---------------------------------------------------------------------------
# Admin — Recurring Issues
# ---------------------------------------------------------------------------
elif page == "🔄 Recurring Issues":
    st.title("🔄 Recurring Issues")

    recur_df = recurring_issues(df)

    if recur_df.empty:
        st.info("No recurring issues detected. Add more complaint records to see patterns.")
    else:
        for _, row in recur_df.iterrows():
            level = "🚩" if row["count"] >= 3 else "⚠️"
            card_html = theme.card(
                f"""
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <div>
                    <strong style="color:{theme.DARK_GREEN};">
                      {level} {row['hostel_block']} — Room {row['room_number']}
                    </strong><br>
                    <span style="font-size:0.9em; color:#666;">Category: {row['category']}</span>
                  </div>
                  <div style="font-size:1.6em; font-weight:700; color:{theme.DARK_GREEN};">
                    {row['count']} complaints
                  </div>
                </div>
                """
            )
            st.markdown(card_html, unsafe_allow_html=True)
