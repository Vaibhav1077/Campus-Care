"""
CampusCare – Color palette constants and CSS helpers.
"""

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
CREAM = "#F7F4EC"       # main background
WHITE = "#FFFFFF"       # cards
DARK_GREEN = "#244C3A"  # primary
SAGE_GREEN = "#A8B9A0"  # secondary
BEIGE = "#E8DDC8"       # accent
CHARCOAL = "#252A26"    # text


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

def get_css() -> str:
    """Return a CSS string for injection via st.markdown(..., unsafe_allow_html=True)."""
    return f"""
<style>
/* ---- Global background ---- */
html, body, [data-testid="stAppViewContainer"], .stApp {{
    background-color: {CREAM} !important;
    color: {CHARCOAL} !important;
}}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {{
    background-color: {DARK_GREEN} !important;
}}
[data-testid="stSidebar"] * {{
    color: {WHITE} !important;
}}
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stCheckbox label {{
    color: {WHITE} !important;
}}
[data-testid="stSidebar"] hr {{
    border-color: {SAGE_GREEN} !important;
}}

/* ---- Card ---- */
.card {{
    background-color: {WHITE};
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    margin-bottom: 16px;
}}

/* ---- Buttons ---- */
.stButton > button {{
    background-color: {DARK_GREEN} !important;
    color: {WHITE} !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 0.4rem 1.2rem !important;
    font-weight: 600 !important;
}}
.stButton > button:hover {{
    background-color: {SAGE_GREEN} !important;
    color: {CHARCOAL} !important;
}}

/* ---- Download button ---- */
.stDownloadButton > button {{
    background-color: {SAGE_GREEN} !important;
    color: {CHARCOAL} !important;
    border-radius: 8px !important;
    border: none !important;
}}

/* ---- Input fields ---- */
input[type="text"], input[type="password"],
textarea, .stTextInput input, .stTextArea textarea {{
    border: 1.5px solid {SAGE_GREEN} !important;
    border-radius: 8px !important;
}}

/* ---- Metric boxes ---- */
[data-testid="metric-container"] {{
    background-color: {WHITE};
    border-radius: 10px;
    padding: 12px 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
}}

/* ---- DataFrames / tables ---- */
.stDataFrame {{
    border-radius: 10px;
    overflow: hidden;
}}
.stDataFrame th {{
    background-color: {DARK_GREEN} !important;
    color: {WHITE} !important;
}}

/* ---- Headings ---- */
h1, h2, h3, h4, h5 {{
    color: {DARK_GREEN} !important;
}}

/* ---- Status badges ---- */
.badge {{
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.82em;
    font-weight: 600;
    letter-spacing: 0.03em;
}}
.badge-pending    {{ background-color: #FFF3CD; color: #856404; }}
.badge-inprogress {{ background-color: #CCE5FF; color: #004085; }}
.badge-resolved   {{ background-color: #D4EDDA; color: #155724; }}
.badge-critical   {{ background-color: #F8D7DA; color: #721C24; }}
</style>
"""


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------

def card(content_html: str) -> str:
    """Wrap content in a styled card div."""
    return f'<div class="card">{content_html}</div>'


def status_badge(status: str) -> str:
    """Return an HTML <span> with the appropriate badge class."""
    s = status.strip().lower().replace("-", "").replace(" ", "")
    if s == "pending":
        css_class = "badge-pending"
    elif s in ("inprogress", "in progress"):
        css_class = "badge-inprogress"
    elif s == "resolved":
        css_class = "badge-resolved"
    elif s == "critical":
        css_class = "badge-critical"
    else:
        css_class = "badge-pending"
    return f'<span class="badge {css_class}">{status}</span>'
