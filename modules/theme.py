"""
CampusCare – Color palette constants and CSS helpers.
"""

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
CREAM = "#F7F4EC"
WHITE = "#FFFFFF"
DARK_GREEN = "#244C3A"
SAGE_GREEN = "#A8B9A0"
BEIGE = "#E8DDC8"
CHARCOAL = "#252A26"


def get_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ── Hide Streamlit chrome ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
.viewerBadge_container__1QSob { display: none !important; }

/* ── Global ── */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #F7F4EC !important;
    font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif !important;
    color: #252A26 !important;
}
.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 2rem !important;
    max-width: 1200px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1b3828 0%, #244C3A 50%, #1b3828 100%) !important;
    border-right: none !important;
    box-shadow: 4px 0 20px rgba(0,0,0,0.15) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}
[data-testid="stSidebar"] * {
    color: rgba(255,255,255,0.85) !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] strong,
[data-testid="stSidebar"] b {
    color: #ffffff !important;
}
[data-testid="stSidebar"] hr {
    border: none !important;
    border-top: 1px solid rgba(168,185,160,0.3) !important;
    margin: 10px 0 !important;
}

/* Sidebar radio — hide dots, style as nav links */
[data-testid="stSidebar"] .stRadio > label {
    display: none !important;
}
[data-testid="stSidebar"] .stRadio > div {
    gap: 2px !important;
}
[data-testid="stSidebar"] .stRadio div[data-baseweb="radio"] {
    background: transparent !important;
    border-radius: 8px !important;
    padding: 2px 0 !important;
    transition: background 0.2s !important;
}
[data-testid="stSidebar"] .stRadio div[data-baseweb="radio"]:hover {
    background: rgba(255,255,255,0.08) !important;
}
[data-testid="stSidebar"] .stRadio div[data-baseweb="radio"] > div:first-child {
    display: none !important;
}
[data-testid="stSidebar"] .stRadio div[data-baseweb="radio"] label {
    padding: 10px 16px !important;
    border-radius: 8px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    width: 100% !important;
    display: block !important;
    color: rgba(255,255,255,0.78) !important;
}
[data-testid="stSidebar"] .stRadio div[data-baseweb="radio"][aria-checked="true"] {
    background: rgba(168,185,160,0.22) !important;
    border-left: 3px solid #A8B9A0 !important;
}
[data-testid="stSidebar"] .stRadio div[data-baseweb="radio"][aria-checked="true"] label {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* Sidebar checkbox */
[data-testid="stSidebar"] .stCheckbox label {
    color: rgba(255,255,255,0.78) !important;
    font-size: 0.85rem !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #244C3A 0%, #2d6349 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.6rem !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.03em !important;
    box-shadow: 0 2px 10px rgba(36,76,58,0.3) !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1b3828 0%, #244C3A 100%) !important;
    box-shadow: 0 4px 16px rgba(36,76,58,0.4) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}
.stDownloadButton > button {
    background: #A8B9A0 !important;
    color: #252A26 !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: 600 !important;
    padding: 0.4rem 1.2rem !important;
}
.stDownloadButton > button:hover {
    background: #8fa68a !important;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: #ffffff !important;
    border-radius: 12px !important;
    padding: 18px 20px 14px 20px !important;
    box-shadow: 0 2px 14px rgba(0,0,0,0.06) !important;
    border: 1px solid #ede9df !important;
    border-left: 4px solid #244C3A !important;
}
[data-testid="stMetricValue"] {
    color: #244C3A !important;
    font-size: 2.1rem !important;
    font-weight: 700 !important;
    line-height: 1.2 !important;
}
[data-testid="stMetricLabel"] {
    color: #777 !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}

/* ── DataFrames ── */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 14px rgba(0,0,0,0.06) !important;
    border: 1px solid #ede9df !important;
}
.stDataFrame thead tr th {
    background-color: #244C3A !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
    padding: 10px 14px !important;
}
.stDataFrame tbody tr:nth-child(even) {
    background-color: #fafaf7 !important;
}
.stDataFrame tbody tr:hover {
    background-color: #eef2ee !important;
}

/* ── Form inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border: 1.5px solid #d8d4ca !important;
    border-radius: 8px !important;
    background: #ffffff !important;
    font-size: 0.9rem !important;
    color: #252A26 !important;
    padding: 8px 12px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #244C3A !important;
    box-shadow: 0 0 0 3px rgba(36,76,58,0.12) !important;
    outline: none !important;
}
.stSelectbox > div > div {
    border-radius: 8px !important;
    border: 1.5px solid #d8d4ca !important;
    background: #ffffff !important;
}
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stDateInput label {
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    color: #444 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
    margin-bottom: 4px !important;
}

/* ── Headings ── */
h1 {
    color: #244C3A !important;
    font-weight: 700 !important;
    font-size: 1.75rem !important;
    margin-bottom: 0.3rem !important;
    letter-spacing: -0.02em !important;
}
h2 {
    color: #244C3A !important;
    font-weight: 600 !important;
    font-size: 1.3rem !important;
}
h3 {
    color: #244C3A !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
}

/* ── Alerts / notifications ── */
.stAlert {
    border-radius: 10px !important;
    font-size: 0.88rem !important;
}
[data-testid="stNotification"] {
    border-radius: 10px !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid #e5e0d6 !important;
    margin: 1rem 0 !important;
}

/* ── Info/Success/Error boxes ── */
.stSuccess { background: #e8f5e9 !important; border-left: 4px solid #244C3A !important; border-radius: 8px !important; }
.stError   { background: #fdecea !important; border-left: 4px solid #c0392b !important; border-radius: 8px !important; }
.stWarning { background: #fff8e1 !important; border-left: 4px solid #f39c12 !important; border-radius: 8px !important; }
.stInfo    { background: #e8f4fd !important; border-left: 4px solid #2980b9 !important; border-radius: 8px !important; }

/* ── Card class ── */
.card {
    background: #ffffff;
    border-radius: 14px;
    padding: 24px 28px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    margin-bottom: 20px;
    border: 1px solid #ede9df;
}

/* ── Badges ── */
.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.75em;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.badge-pending    { background: #FFF8E1; color: #E65100; border: 1px solid #FFB300; }
.badge-inprogress { background: #E3F2FD; color: #1565C0; border: 1px solid #1565C0; }
.badge-resolved   { background: #E8F5E9; color: #1B5E20; border: 1px solid #2E7D32; }
.badge-critical   { background: #FFEBEE; color: #B71C1C; border: 1px solid #C62828; }

/* ── Form container ── */
[data-testid="stForm"] {
    background: #ffffff !important;
    border-radius: 14px !important;
    padding: 24px !important;
    border: 1px solid #ede9df !important;
    box-shadow: 0 2px 14px rgba(0,0,0,0.06) !important;
}

/* ── Plotly charts ── */
.js-plotly-plot .plotly {
    border-radius: 12px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F7F4EC; }
::-webkit-scrollbar-thumb { background: #A8B9A0; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #244C3A; }
</style>
"""


def card(content_html: str) -> str:
    return f'<div class="card">{content_html}</div>'


def status_badge(status: str) -> str:
    s = status.strip().lower().replace("-", "").replace(" ", "")
    if s == "pending":
        css = "badge-pending"
    elif s in ("inprogress", "in progress"):
        css = "badge-inprogress"
    elif s == "resolved":
        css = "badge-resolved"
    elif s == "critical":
        css = "badge-critical"
    else:
        css = "badge-pending"
    return f'<span class="badge {css}">{status}</span>'


def page_header(title: str, subtitle: str = "") -> str:
    sub_html = f'<p style="color:#666;font-size:0.9rem;margin:4px 0 0 0;font-weight:400;">{subtitle}</p>' if subtitle else ""
    return f"""
<div style="margin-bottom:1.5rem;">
  <h1 style="margin:0;padding:0;border:none;">{title}</h1>
  {sub_html}
  <div style="height:3px;width:60px;background:linear-gradient(90deg,#244C3A,#A8B9A0);
              border-radius:2px;margin-top:8px;"></div>
</div>
"""
