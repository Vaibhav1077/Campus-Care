"""
CampusCare - Smart Campus Maintenance & Complaint Management System.
Role-based UI: Student portal and Admin / Maintenance portal.

Only the presentation layer changed. All data access, authentication, priority
and analytics logic still comes from the existing modules.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import datetime
import streamlit as st
import pandas as pd
import plotly.express as px

from modules import auth, theme
from modules.theme import esc
from modules.data_manager import (
    load_data, add_complaint, update_complaint, get_complaint, export_csv,
)
from modules.priority_engine import get_overdue_complaints, get_critical_pending
from modules.analytics import (
    summary_stats, category_distribution, status_distribution, recurring_issues,
)
from modules.validators import VALID_CATEGORIES, VALID_STATUSES, VALID_PRIORITIES

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(WORKSPACE, "data", "data.csv")
SAMPLE_PATH = os.path.join(WORKSPACE, "data", "sample_data.csv")

STUDENT_PAGES = ["Home", "Submit Complaint", "My Complaints", "Track Complaint", "History", "Help"]
ADMIN_PAGES = ["Dashboard", "All Complaints", "Manage Complaint", "Priority & Overdue",
               "Recurring Issues", "Analytics"]
FORM_CATEGORIES = ["Electrical", "Plumbing", "Furniture", "Cleaning", "Internet", "AC/Heating", "Other"]

st.set_page_config(page_title="CampusCare", page_icon="🏫", layout="wide", initial_sidebar_state="expanded")
st.markdown(theme.get_css(), unsafe_allow_html=True)


def html(s: str):
    st.markdown(s, unsafe_allow_html=True)


# ===========================================================================
# Login
# ===========================================================================
if not auth.is_authenticated():
    html("<style>.block-container{max-width:1100px !important; padding-top:2rem !important;}</style>")
    left, right = st.columns([1.1, 1], gap="large")

    with left:
        html(
            '<div class="login-brand"><div>'
            f'{theme.logo_mark(40)}'
            "<h2>Report it. Track it. Get it fixed.</h2>"
            "<p>CampusCare connects students and the maintenance team so hostel issues are seen, assigned and resolved without chasing anyone.</p>"
            "</div><ul>"
            "<li><i></i>Raise a complaint in under a minute</li>"
            "<li><i></i>See exactly where your request stands</li>"
            "<li><i></i>Maintenance teams work from one prioritised queue</li>"
            "</ul></div>"
        )

    with right:
        html('<div style="height:2.5rem"></div>')
        html('<h2 style="font-size:1.8rem;margin:0 0 .3rem;">Sign in</h2>'
             '<p style="color:#66757F;margin:0 0 1.4rem;">Use your CampusCare account to continue.</p>')
        username = st.text_input("Username", key="login_username", placeholder="Your username")
        password = st.text_input("Password", type="password", key="login_password", placeholder="Your password")
        if st.button("Sign in", key="login_btn", use_container_width=True):
            if username and password:
                with st.spinner("Signing you in..."):
                    ok, _role = auth.login(username, password)
                if ok:
                    st.rerun()
                else:
                    st.error("That username and password don't match. Check them and try again.")
            else:
                st.error("Enter both your username and password.")
        html(
            '<div class="demo-box"><b style="color:#18222B">Demo accounts</b><br>'
            "Student: <code>student</code> / <code>student123</code><br>"
            "Admin: <code>admin</code> / <code>admin123</code></div>"
        )
    st.stop()

# ===========================================================================
# Session, sidebar
# ===========================================================================
role = auth.get_current_role()
user = auth.get_current_user() or "user"
pages = STUDENT_PAGES if role == "student" else ADMIN_PAGES


def goto(page: str, **state):
    """Callback used by buttons to jump to another page (optionally preselecting a record)."""
    st.session_state["nav"] = page
    for k, v in state.items():
        st.session_state[k] = v


if st.session_state.get("nav") not in pages:
    st.session_state["nav"] = pages[0]

with st.sidebar:
    html(
        f'<div class="sb-brand">{theme.logo_mark(34)}<div><b>CampusCare</b>'
        f'<small>{"Student portal" if role == "student" else "Maintenance portal"}</small></div></div>'
        f'<div class="sb-user"><div class="sb-avatar">{esc(user[:1].upper())}</div>'
        f'<div><b>{esc(user)}</b><span>{"Student" if role == "student" else "Administrator"}</span></div></div>'
    )
    st.radio("Navigation", pages, key="nav", label_visibility="collapsed")

    use_demo = False
    if role != "student":
        st.divider()
        use_demo = st.checkbox("Use demo data", value=False, help="Switch to the synthetic sample dataset (read-only).")
    st.divider()
    if st.button("Log out", key="logout_btn"):
        auth.logout()
        for k in ("nav", "track_id", "mgmt_id"):
            st.session_state.pop(k, None)
        st.rerun()

page = st.session_state["nav"]
data_path = SAMPLE_PATH if use_demo else DATA_PATH

# ===========================================================================
# Data
# ===========================================================================
@st.cache_data(ttl=5)
def _load(path: str) -> pd.DataFrame:
    return load_data(path)


try:
    df = _load(data_path)
except Exception as exc:  # surfaced as a proper error state instead of a stack trace
    html(theme.page_header("Something went wrong", "We couldn't load the complaint records."))
    html(theme.empty_state("Complaint data is unavailable", f"Check that the data file exists and is readable. Details: {exc}", "alert"))
    st.stop()

if use_demo:
    html(theme.callout("You are viewing synthetic demo data. Changes are disabled."))


# ===========================================================================
# Shared helpers
# ===========================================================================
def my_complaints() -> pd.DataFrame:
    if df.empty:
        return df.copy()
    out = df[df["reported_by"].astype(str) == user].copy()
    return sort_recent(out)


def sort_recent(d: pd.DataFrame) -> pd.DataFrame:
    if d.empty:
        return d
    d = d.copy()
    d["_d"] = pd.to_datetime(d["date_reported"], errors="coerce")
    return d.sort_values("_d", ascending=False).drop(columns="_d")


def greeting() -> str:
    h = datetime.datetime.now().hour
    return "Good morning" if h < 12 else "Good afternoon" if h < 17 else "Good evening"


def paged_table(d: pd.DataFrame, columns, key: str, size: int = 10):
    """Render a styled table with simple pagination."""
    total = len(d)
    pages_n = max(1, -(-total // size))
    if pages_n > 1:
        cur = st.number_input("Page", 1, pages_n, 1, key=f"{key}_page")
    else:
        cur = 1
    start = (cur - 1) * size
    html(theme.table(d.iloc[start:start + size], columns))
    html(f'<div class="tbl-foot">Showing {start + 1}-{min(start + size, total)} of {total}</div>')


def option_label(row) -> str:
    return f'{row["complaint_id"]}  |  {row["category"]}  |  {row["hostel_block"]} {row["room_number"]}'


def pick_complaint(d: pd.DataFrame, key: str):
    """Selectbox over complaint ids with a readable label; returns the id."""
    ids = d["complaint_id"].tolist()
    labels = {r["complaint_id"]: option_label(r) for _, r in d.iterrows()}
    if st.session_state.get(key) not in ids:
        st.session_state.pop(key, None)
    return st.selectbox("Complaint", ids, key=key, format_func=lambda i: labels.get(i, i))


# ===========================================================================
# STUDENT PAGES
# ===========================================================================
def student_home():
    mine = my_complaints()
    html(theme.page_header(f"{greeting()}, {user.title()}", "Here's where your maintenance requests stand."))

    total = len(mine)
    open_df = mine[mine["status"] != "Resolved"] if total else mine
    prog = int((mine["status"] == "In Progress").sum()) if total else 0
    res = int((mine["status"] == "Resolved").sum()) if total else 0
    html(theme.kpi_grid([
        theme.kpi("Total submitted", total),
        theme.kpi("Open", len(open_df), "Waiting or being worked on"),
        theme.kpi("In progress", prog),
        theme.kpi("Resolved", res),
    ]))

    c1, c2 = st.columns([1.7, 1], gap="large")
    with c1:
        html(theme.section_title("Open complaints", "Most recent first"))
        if open_df.empty:
            html(theme.empty_state(
                "Nothing open right now" if total else "No complaints yet",
                "Everything you reported has been resolved." if total else "When something breaks in your room or block, report it here and we'll track it for you.",
                "check" if total else "inbox"))
        else:
            for _, rec in open_df.head(4).iterrows():
                html(theme.complaint_item(rec, theme.stepper(str(rec["status"]))))
                st.button("View details", key=f"home_{rec['complaint_id']}", on_click=goto,
                          args=("Track Complaint",), kwargs={"track_id": rec["complaint_id"]})
    with c2:
        html(theme.section_title("Need something fixed?"))
        html(theme.card("<p style='margin:0 0 .9rem;color:#66757F;font-size:.92rem'>Describe the problem and we'll route it to the right team.</p>"))
        st.button("Submit a complaint", key="home_submit", on_click=goto, args=("Submit Complaint",), use_container_width=True)


def student_submit():
    html(theme.page_header("Submit a complaint", "Tell us what's wrong and where. The more specific you are, the faster we can fix it."))
    c1, c2 = st.columns([1.8, 1], gap="large")
    with c1:
        with st.form("submit_form", clear_on_submit=True):
            a, b = st.columns(2)
            name = a.text_input("Your name *")
            contact = b.text_input("Contact (phone or email)")
            a, b = st.columns(2)
            hostel_block = a.text_input("Hostel block *")
            room_number = b.text_input("Room number *")
            category = st.selectbox("Category *", FORM_CATEGORIES)
            description = st.text_area("What's the problem? *", height=130,
                                       placeholder="For example: the ceiling fan makes a loud noise and stops after a few minutes.")
            submitted = st.form_submit_button("Submit complaint")

        if submitted:
            errors = []
            if not name.strip():
                errors.append("Enter your name.")
            if not hostel_block.strip():
                errors.append("Enter your hostel block.")
            if not room_number.strip():
                errors.append("Enter your room number.")
            if not description.strip():
                errors.append("Describe the problem.")
            if errors:
                for e in errors:
                    st.error(e)
            else:
                complaint_id = "CC-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                mapped = category if category in VALID_CATEGORIES else "Other"
                record = {
                    "complaint_id": complaint_id,
                    "date_reported": datetime.date.today().isoformat(),
                    "hostel_block": hostel_block.strip(),
                    "room_number": room_number.strip(),
                    "category": mapped,
                    "description": description.strip(),
                    "reported_by": user,
                    "contact": contact.strip(),
                    "priority": "Medium",
                    "status": "Pending",
                    "assigned_to": "",
                    "date_resolved": "",
                    "resolution_notes": "",
                }
                with st.spinner("Submitting your complaint..."):
                    ok, msg = add_complaint(record, DATA_PATH)
                if ok:
                    st.cache_data.clear()
                    html(theme.callout(f"Complaint submitted. Your reference is <b>{esc(complaint_id)}</b>. Use Track Complaint to follow it.", ok=True))
                else:
                    st.error(f"We couldn't submit your complaint: {msg}")
    with c2:
        html(theme.card(
            "<h3>What happens next</h3>"
            "<p style='color:#66757F;font-size:.9rem;margin:0 0 .8rem'>Target resolution times by priority:</p>"
            f"{theme.priority_badge('Critical')} <span style='font-size:.88rem'>Same day</span><br><div style='height:6px'></div>"
            f"{theme.priority_badge('High')} <span style='font-size:.88rem'>Within 24 hours</span><br><div style='height:6px'></div>"
            f"{theme.priority_badge('Medium')} <span style='font-size:.88rem'>Within 3 days</span><br><div style='height:6px'></div>"
            f"{theme.priority_badge('Low')} <span style='font-size:.88rem'>Within 7 days</span>"
        ))


def student_my_complaints():
    mine = my_complaints()
    html(theme.page_header("My complaints", "Everything you've reported, in one place."))
    if mine.empty:
        html(theme.empty_state("No complaints yet", "Complaints you submit will appear here.", "inbox"))
        st.button("Submit a complaint", on_click=goto, args=("Submit Complaint",))
        return
    a, b, c = st.columns([2, 1, 1])
    q = a.text_input("Search", placeholder="Search by ID, category or description", key="my_q")
    f_status = b.selectbox("Status", ["All"] + VALID_STATUSES, key="my_status")
    f_cat = c.selectbox("Category", ["All"] + sorted(mine["category"].dropna().unique().tolist()), key="my_cat")
    v = mine
    if q:
        mask = v[["complaint_id", "category", "description"]].astype(str).apply(
            lambda col: col.str.contains(q, case=False, na=False)).any(axis=1)
        v = v[mask]
    if f_status != "All":
        v = v[v["status"] == f_status]
    if f_cat != "All":
        v = v[v["category"] == f_cat]
    html('<div style="height:.6rem"></div>')
    if v.empty:
        html(theme.empty_state("No matches", "Try a different search or clear the filters.", "search"))
        return
    cols = [("complaint_id", "Reference", "id"), ("date_reported", "Reported", "muted"), ("category", "Category", "text"),
            ("hostel_block", "Block", "text"), ("room_number", "Room", "text"),
            ("priority", "Priority", "priority"), ("status", "Status", "status")]
    paged_table(v, cols, "my")
    html('<div style="height:.8rem"></div>')
    sel = pick_complaint(v, "track_id")
    st.button("Track this complaint", on_click=goto, args=("Track Complaint",), key="my_track")


def student_track():
    mine = my_complaints()
    html(theme.page_header("Track a complaint", "See the current status, who is handling it and any resolution notes."))
    if mine.empty:
        html(theme.empty_state("Nothing to track yet", "Submit a complaint and you'll be able to follow it here.", "inbox"))
        return
    cid = pick_complaint(mine, "track_id")
    rec = get_complaint(cid, mine)
    if not rec:
        html(theme.empty_state("Complaint not found", "It may have been removed. Pick another from the list.", "alert"))
        return
    status = str(rec.get("status", "Pending"))
    html(theme.card(
        f'<div class="item-top"><h3 style="margin:0">{esc(rec.get("complaint_id"))}</h3>'
        f'<div>{theme.priority_badge(rec.get("priority", ""))} {theme.status_badge(status)}</div></div>'
        f'<div style="margin:1.3rem 0 .4rem">{theme.stepper(status)}</div>'
    ))
    resolved = str(rec.get("date_resolved", "") or "")
    html(theme.card("<h3>Details</h3>" + theme.detail_list([
        ("Category", rec.get("category", "")),
        ("Location", f'{rec.get("hostel_block", "")}, room {rec.get("room_number", "")}'),
        ("Reported on", rec.get("date_reported", "")),
        ("Assigned to", rec.get("assigned_to", "")),
        ("Resolved on", resolved),
        ("Description", rec.get("description", "")),
        ("Resolution notes", rec.get("resolution_notes", "")),
    ])))


def student_history():
    mine = my_complaints()
    html(theme.page_header("History", "Complaints that have been resolved."))
    done = mine[mine["status"] == "Resolved"] if not mine.empty else mine
    if done.empty:
        html(theme.empty_state("No resolved complaints yet", "Once a complaint is resolved it moves here with its resolution notes.", "clock"))
        return
    cols = [("complaint_id", "Reference", "id"), ("category", "Category", "text"), ("date_reported", "Reported", "muted"),
            ("date_resolved", "Resolved", "muted"), ("assigned_to", "Handled by", "text"), ("resolution_notes", "Resolution", "wrap")]
    paged_table(done, cols, "hist")


def student_help():
    html(theme.page_header("Help", "How CampusCare works."))
    html(theme.card(
        "<h3>Submitting and following a complaint</h3>"
        "<ol style='line-height:1.9;margin:0;padding-left:1.2rem;color:#33414B'>"
        "<li>Open <b>Submit Complaint</b> and fill in your location, category and a clear description.</li>"
        "<li>You get a reference number straight away.</li>"
        "<li>Open <b>Track Complaint</b> to see its status, the assigned staff member and resolution notes.</li>"
        "</ol>"))
    rows = [("Electrical", "Power cuts, socket issues, flickering lights"), ("Plumbing", "Leaking taps, blocked drains, no water"),
            ("Furniture", "Broken chairs, damaged wardrobes"), ("Cleaning", "Overflowing bins, pest issues"),
            ("Internet", "No Wi-Fi, slow connection, router faults"), ("AC/Heating", "AC not cooling, heater not working"),
            ("Other", "Anything not covered above")]
    body = "".join(f"<tr><td class='id'>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in rows)
    html(theme.card("<h3>Categories</h3>"
                    f'<div class="tbl-wrap" style="border:none"><table class="tbl" style="min-width:0"><tbody>{body}</tbody></table></div>'))


# ===========================================================================
# ADMIN PAGES
# ===========================================================================
def admin_dashboard():
    html(theme.page_header("Dashboard", "Live overview of campus complaints."))
    if df.empty:
        html(theme.empty_state("No complaints recorded yet", "Once students submit complaints, this dashboard fills in automatically.", "inbox"))
        return
    s = summary_stats(df)
    overdue = len(get_overdue_complaints(df))
    rate = f'{round(s["resolved"] / s["total"] * 100)}%' if s["total"] else "0%"
    html(theme.kpi_grid([
        theme.kpi("Total complaints", s["total"]),
        theme.kpi("Pending", s["pending"]),
        theme.kpi("In progress", s["in_progress"]),
        theme.kpi("Resolved", s["resolved"], f"{rate} resolution rate"),
        theme.kpi("Critical", s["critical"], warn=s["critical"] > 0),
        theme.kpi("Overdue", overdue, warn=overdue > 0),
    ]))
    c1, c2 = st.columns([1.5, 1], gap="large")
    with c1:
        html(theme.section_title("Complaints by category"))
        cat = category_distribution(df)
        if not cat.empty:
            fig = px.bar(cat.sort_values("count"), x="count", y="category", orientation="h", color_discrete_sequence=[theme.PETROL])
            fig.update_traces(marker_cornerradius=4)
            st.plotly_chart(theme.style_fig(fig, 320), use_container_width=True, config={"displayModeBar": False})
    with c2:
        html(theme.section_title("Status"))
        stt = status_distribution(df)
        if not stt.empty:
            cmap = {"Pending": theme.PENDING, "In Progress": theme.PROGRESS, "Resolved": theme.RESOLVED}
            fig = px.pie(stt, names="status", values="count", hole=0.62, color="status", color_discrete_map=cmap)
            fig.update_traces(textinfo="value", sort=False)
            st.plotly_chart(theme.style_fig(fig, 320).update_layout(showlegend=True, legend=dict(orientation="h", y=-0.05)),
                            use_container_width=True, config={"displayModeBar": False})
    html(theme.section_title("Latest complaints"))
    cols = [("complaint_id", "Reference", "id"), ("date_reported", "Reported", "muted"), ("category", "Category", "text"),
            ("hostel_block", "Block", "text"), ("priority", "Priority", "priority"), ("status", "Status", "status")]
    html(theme.table(sort_recent(df).head(6), cols))


def admin_all():
    html(theme.page_header("All complaints", "Search, filter and export every complaint."))
    if df.empty:
        html(theme.empty_state("No complaints recorded yet", "Complaints will be listed here as they come in.", "inbox"))
        return
    q = st.text_input("Search", placeholder="Search by ID, room, reporter or description", key="all_q")
    a, b, c, d = st.columns(4)
    blocks = ["All"] + sorted(df["hostel_block"].dropna().astype(str).unique().tolist())
    f_block = a.selectbox("Hostel block", blocks, key="ab_block")
    f_cat = b.selectbox("Category", ["All"] + VALID_CATEGORIES, key="ab_cat")
    f_pri = c.selectbox("Priority", ["All"] + VALID_PRIORITIES, key="ab_pri")
    f_status = d.selectbox("Status", ["All"] + VALID_STATUSES, key="ab_status")
    v = df.copy()
    if q:
        mask = v[["complaint_id", "room_number", "reported_by", "description"]].astype(str).apply(
            lambda col: col.str.contains(q, case=False, na=False)).any(axis=1)
        v = v[mask]
    if f_block != "All":
        v = v[v["hostel_block"].astype(str) == f_block]
    if f_cat != "All":
        v = v[v["category"] == f_cat]
    if f_pri != "All":
        v = v[v["priority"] == f_pri]
    if f_status != "All":
        v = v[v["status"] == f_status]
    v = sort_recent(v)
    html('<div style="height:.6rem"></div>')
    if v.empty:
        html(theme.empty_state("No complaints match", "Try removing a filter or changing your search.", "search"))
        return
    cols = [("complaint_id", "Reference", "id"), ("date_reported", "Reported", "muted"), ("hostel_block", "Block", "text"),
            ("room_number", "Room", "text"), ("category", "Category", "text"), ("priority", "Priority", "priority"),
            ("status", "Status", "status"), ("assigned_to", "Assigned to", "text")]
    paged_table(v, cols, "all", size=12)
    html('<div style="height:.8rem"></div>')
    a, b = st.columns([3, 1])
    with a:
        pick_complaint(v, "mgmt_id")
    with b:
        html('<div style="height:1.75rem"></div>')
        st.button("Open in Manage", on_click=goto, args=("Manage Complaint",), key="open_mgmt", use_container_width=True)
    st.download_button("Download CSV", export_csv(v, {}), "complaints_export.csv", "text/csv")


def admin_manage():
    html(theme.page_header("Manage complaint", "Update status and priority, assign staff and record the resolution."))
    if df.empty:
        html(theme.empty_state("No complaints to manage", "Complaints will appear here once students submit them.", "inbox"))
        return
    cid = pick_complaint(sort_recent(df), "mgmt_id")
    rec = get_complaint(cid, df)
    if not rec:
        html(theme.empty_state("Complaint not found", "Pick another complaint from the list.", "alert"))
        return
    status = str(rec.get("status", "Pending"))
    html(theme.card(
        f'<div class="item-top"><div><h3 style="margin:0 0 .2rem">{esc(rec.get("complaint_id"))}</h3>'
        f'<div class="item-meta">{esc(rec.get("hostel_block"))}, room {esc(rec.get("room_number"))} &middot; {esc(rec.get("category"))} &middot; '
        f'reported {esc(rec.get("date_reported"))} by {esc(rec.get("reported_by"))}</div></div>'
        f'<div>{theme.priority_badge(rec.get("priority", ""))} {theme.status_badge(status)}</div></div>'
        f'<p style="margin:.9rem 0 0;color:#33414B">{esc(rec.get("description"))}</p>'
    ))
    with st.form("manage_form"):
        a, b, c = st.columns(3)
        s_idx = VALID_STATUSES.index(status) if status in VALID_STATUSES else 0
        cur_pri = str(rec.get("priority", "Medium"))
        p_idx = VALID_PRIORITIES.index(cur_pri) if cur_pri in VALID_PRIORITIES else 0
        new_status = a.selectbox("Status", VALID_STATUSES, index=s_idx)
        new_priority = b.selectbox("Priority", VALID_PRIORITIES, index=p_idx)
        assigned_to = c.text_input("Assigned to", value=str(rec.get("assigned_to", "") or ""), placeholder="Staff member name")
        notes = st.text_area("Resolution notes", value=str(rec.get("resolution_notes", "") or ""),
                             placeholder="What was done, or what is still needed?")
        raw = rec.get("date_resolved", "") or ""
        try:
            default_d = datetime.date.fromisoformat(str(raw)) if raw else datetime.date.today()
        except ValueError:
            default_d = datetime.date.today()
        date_resolved = st.date_input("Date resolved (used when status is Resolved)", value=default_d)
        save = st.form_submit_button("Save changes")
    if save:
        if use_demo:
            st.warning("Demo data is read-only. Turn off demo data to save changes.")
        else:
            updates = {
                "status": new_status,
                "priority": new_priority,
                "assigned_to": assigned_to,
                "resolution_notes": notes,
                "date_resolved": str(date_resolved) if new_status == "Resolved" else "",
            }
            with st.spinner("Saving..."):
                ok, msg = update_complaint(cid, updates, DATA_PATH)
            if ok:
                st.cache_data.clear()
                st.success(msg or "Changes saved.")
            else:
                st.error(f"We couldn't save the changes: {msg}")


def admin_priority():
    html(theme.page_header("Priority & overdue", "What needs attention first."))
    if df.empty:
        html(theme.empty_state("No complaints recorded yet", "Priority queues build up as complaints arrive.", "inbox"))
        return
    open_df = df[df["status"] != "Resolved"]
    counts = open_df["priority"].value_counts()
    html(theme.kpi_grid([theme.kpi(f"{p} (open)", int(counts.get(p, 0)), warn=(p in ("Critical",) and counts.get(p, 0) > 0))
                         for p in VALID_PRIORITIES]))
    cols = [("complaint_id", "Reference", "id"), ("date_reported", "Reported", "muted"), ("hostel_block", "Block", "text"),
            ("room_number", "Room", "text"), ("category", "Category", "text"), ("priority", "Priority", "priority"),
            ("status", "Status", "status"), ("assigned_to", "Assigned to", "text")]
    crit = get_critical_pending(df)
    html(theme.section_title("Critical and high priority", "Pending or in progress"))
    if crit.empty:
        html(theme.empty_state("Nothing urgent", "There are no critical or high-priority complaints open.", "check"))
    else:
        paged_table(crit, [c for c in cols if c[0] in crit.columns], "crit", size=8)
    over = get_overdue_complaints(df)
    html(theme.section_title("Overdue", "Past the target resolution time"))
    if over.empty:
        html(theme.empty_state("No overdue complaints", "Everything is within its target resolution time.", "check"))
    else:
        paged_table(over, [c for c in cols if c[0] in over.columns], "over", size=8)
    html('<div style="height:.5rem"></div>')
    st.button("Go to Manage Complaint", on_click=goto, args=("Manage Complaint",), key="prio_manage")


def admin_recurring():
    html(theme.page_header("Recurring issues", "Locations with repeated complaints that probably need a lasting fix."))
    rec = recurring_issues(df) if not df.empty else pd.DataFrame()
    if rec.empty:
        html(theme.empty_state("No recurring issues detected", "A location appears here when the same category is reported there more than once.", "repeat"))
        return
    html(theme.kpi_grid([theme.kpi("Locations affected", len(rec)),
                         theme.kpi("Reported 3+ times", int((rec["count"] >= 3).sum()), warn=bool((rec["count"] >= 3).any()))]))
    html(theme.section_title("Repeat locations"))
    for _, r in rec.iterrows():
        sev = theme.priority_badge("High" if r["count"] >= 3 else "Medium")
        html(theme.card(
            f'<div class="item-top"><div><b style="color:#121A22">{esc(r["hostel_block"])}, room {esc(r["room_number"])}</b>'
            f'<div class="item-meta">{esc(r["category"])}</div></div>'
            f'<div style="text-align:right">{sev}<div style="font-family:var(--font-display);font-size:1.5rem;font-weight:600;margin-top:.3rem">{esc(r["count"])} complaints</div></div></div>'
        ))


def admin_analytics():
    html(theme.page_header("Analytics", "Trends and patterns, calculated from your complaint records."))
    if df.empty:
        html(theme.empty_state("No data to analyse yet", "Charts appear once complaints have been recorded.", "inbox"))
        return
    d = df.copy()
    d["_rep"] = pd.to_datetime(d["date_reported"], errors="coerce")
    d["_res"] = pd.to_datetime(d["date_resolved"], errors="coerce")
    days = (d["_res"] - d["_rep"]).dt.days.dropna()
    avg = f"{days.mean():.1f} days" if len(days) else "No data"
    s = summary_stats(df)
    rate = f'{round(s["resolved"] / s["total"] * 100)}%' if s["total"] else "0%"
    html(theme.kpi_grid([
        theme.kpi("Resolution rate", rate),
        theme.kpi("Average time to resolve", avg, f"Across {len(days)} resolved complaints" if len(days) else ""),
        theme.kpi("Overdue now", len(get_overdue_complaints(df)), warn=len(get_overdue_complaints(df)) > 0),
        theme.kpi("Recurring locations", len(recurring_issues(df))),
    ]))
    c1, c2 = st.columns(2, gap="large")
    with c1:
        html(theme.section_title("Complaints per month"))
        m = d.dropna(subset=["_rep"]).assign(month=lambda x: x["_rep"].dt.to_period("M").astype(str)).groupby("month").size().reset_index(name="count")
        if m.empty:
            html(theme.empty_state("No dated complaints", "Monthly trends need valid report dates.", "clock"))
        else:
            fig = px.area(m, x="month", y="count", color_discrete_sequence=[theme.PETROL], markers=True)
            st.plotly_chart(theme.style_fig(fig, 300), use_container_width=True, config={"displayModeBar": False})
    with c2:
        html(theme.section_title("Open complaints by priority"))
        pr = d[d["status"] != "Resolved"]["priority"].value_counts().reindex(VALID_PRIORITIES).fillna(0).reset_index()
        pr.columns = ["priority", "count"]
        cmap = {"Critical": theme.CRITICAL, "High": theme.HIGH, "Medium": theme.MEDIUM, "Low": theme.LOW}
        fig = px.bar(pr, x="priority", y="count", color="priority", color_discrete_map=cmap)
        fig.update_traces(marker_cornerradius=4)
        st.plotly_chart(theme.style_fig(fig, 300), use_container_width=True, config={"displayModeBar": False})
    c3, c4 = st.columns(2, gap="large")
    with c3:
        html(theme.section_title("Complaints by hostel block"))
        hb = d["hostel_block"].astype(str).value_counts().head(10).reset_index()
        hb.columns = ["block", "count"]
        fig = px.bar(hb.sort_values("count"), x="count", y="block", orientation="h", color_discrete_sequence=[theme.PROGRESS])
        fig.update_traces(marker_cornerradius=4)
        st.plotly_chart(theme.style_fig(fig, 300), use_container_width=True, config={"displayModeBar": False})
    with c4:
        html(theme.section_title("Complaints by category"))
        cat = category_distribution(df)
        fig = px.bar(cat.sort_values("count"), x="count", y="category", orientation="h", color_discrete_sequence=[theme.PETROL])
        fig.update_traces(marker_cornerradius=4)
        st.plotly_chart(theme.style_fig(fig, 300), use_container_width=True, config={"displayModeBar": False})
    st.download_button("Download full report (CSV)", export_csv(df, {}), "campuscare_report.csv", "text/csv")


# ===========================================================================
# Router
# ===========================================================================
ROUTES = {
    "Home": student_home, "Submit Complaint": student_submit, "My Complaints": student_my_complaints,
    "Track Complaint": student_track, "History": student_history, "Help": student_help,
    "Dashboard": admin_dashboard, "All Complaints": admin_all, "Manage Complaint": admin_manage,
    "Priority & Overdue": admin_priority, "Recurring Issues": admin_recurring, "Analytics": admin_analytics,
}
ROUTES[page]()
