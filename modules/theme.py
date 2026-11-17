"""
CampusCare - design system.

Identity: "maintenance signage". A deep petrol-and-ink palette (calm, trustworthy,
institutional) with one safety-yellow accent used only to mark "where you are"
(active nav item, current step in a tracker). Everything else stays quiet.

Type: Bricolage Grotesque for headings and big numbers, Public Sans for UI text.

All helpers return HTML strings WITHOUT indentation or blank lines, because
Markdown treats indented / blank-line-separated HTML as code blocks.
All user-supplied values are escaped through esc().
"""
import html

# ---------------------------------------------------------------------------
# Tokens (kept as module constants so app.py / charts can reuse them)
# ---------------------------------------------------------------------------
INK = "#121A22"
INK_SOFT = "#1B2733"
PETROL = "#0E6A7A"
PETROL_DARK = "#0A4F5C"
PETROL_TINT = "#E3F1F3"
SIGNAL = "#F2C230"
BG = "#F2F4F5"
SURFACE = "#FFFFFF"
LINE = "#DDE3E6"
TEXT = "#18222B"
MUTED = "#66757F"

PENDING = "#B7791F"
PROGRESS = "#2563C9"
RESOLVED = "#1F8A5B"
CRITICAL = "#C93636"
HIGH = "#D9692B"
MEDIUM = "#B08A1E"
LOW = "#5F7380"

CHART_COLORS = [PETROL, "#2563C9", "#D9692B", "#1F8A5B", "#8B5CF6", "#B08A1E", "#C93636", "#5F7380"]


def esc(value) -> str:
    """HTML-escape any value; None / NaN become an empty string."""
    if value is None:
        return ""
    if isinstance(value, float) and value != value:
        return ""
    return html.escape(str(value))


# ---------------------------------------------------------------------------
# Icons (inline SVG, stroke based, one consistent set)
# ---------------------------------------------------------------------------
_ICONS = {
    "inbox": '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.46 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "repeat": '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
}


def icon(name: str, size: int = 20, color: str = "currentColor") -> str:
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
        f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'{_ICONS.get(name, "")}</svg>'
    )


def logo_mark(size: int = 34) -> str:
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 40 40" aria-hidden="true">'
        f'<rect width="40" height="40" rx="10" fill="{PETROL}"/>'
        f'<path d="M10 19.5 20 11l10 8.5V30a1 1 0 0 1-1 1H11a1 1 0 0 1-1-1z" fill="none" stroke="#fff" stroke-width="2.2" stroke-linejoin="round"/>'
        f'<path d="m15.5 21.5 3.2 3.2 5.8-6" fill="none" stroke="{SIGNAL}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
        f'</svg>'
    )


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
def get_css() -> str:
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700&family=Public+Sans:wght@400;500;600;700&display=swap');

:root {{
  --ink:{INK}; --ink-soft:{INK_SOFT}; --petrol:{PETROL}; --petrol-dark:{PETROL_DARK}; --petrol-tint:{PETROL_TINT};
  --signal:{SIGNAL}; --bg:{BG}; --surface:{SURFACE}; --line:{LINE}; --text:{TEXT}; --muted:{MUTED};
  --font-ui:'Public Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;
  --font-display:'Bricolage Grotesque', 'Public Sans', system-ui, sans-serif;
}}

/* ---- Streamlit chrome ---- */
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {{ display:none !important; }}
header[data-testid="stHeader"] {{ background:transparent !important; }}

html, body, .stApp, [data-testid="stAppViewContainer"] {{
  background:var(--bg) !important; color:var(--text) !important; font-family:var(--font-ui) !important;
}}
.block-container {{ padding:2rem 2.5rem 3rem !important; max-width:1240px !important; }}
@media (max-width:760px) {{ .block-container {{ padding:1.2rem 1rem 2.5rem !important; }} }}

h1,h2,h3,h4 {{ font-family:var(--font-display) !important; color:var(--ink) !important; letter-spacing:-0.01em; }}
p, label, span, div {{ font-family:var(--font-ui); }}
:focus-visible {{ outline:2px solid var(--petrol) !important; outline-offset:2px; }}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {{ background:var(--ink) !important; border-right:none !important; }}
[data-testid="stSidebar"] > div:first-child {{ padding-top:0 !important; }}
[data-testid="stSidebar"] * {{ color:#C9D3DA; }}
[data-testid="stSidebar"] hr {{ border:none !important; border-top:1px solid rgba(255,255,255,.09) !important; margin:14px 0 !important; }}
[data-testid="stSidebar"] div[role="radiogroup"] {{ gap:2px !important; }}
[data-testid="stSidebar"] div[role="radiogroup"] > label {{
  position:relative; padding:10px 14px 10px 16px !important; border-radius:8px; margin:0 !important;
  cursor:pointer; transition:background .15s; width:100%;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {{ display:none !important; }}
[data-testid="stSidebar"] div[role="radiogroup"] > label p {{ font-size:.92rem !important; font-weight:500 !important; color:#C9D3DA !important; }}
[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {{ background:rgba(255,255,255,.06); }}
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {{ background:rgba(255,255,255,.09); }}
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p {{ color:#fff !important; font-weight:600 !important; }}
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked)::before {{
  content:""; position:absolute; left:0; top:9px; bottom:9px; width:3px; border-radius:2px; background:var(--signal);
}}
[data-testid="stSidebar"] .stCheckbox p {{ font-size:.85rem !important; color:#9FB0BB !important; }}
[data-testid="stSidebar"] .stButton > button {{
  background:transparent !important; color:#C9D3DA !important; border:1px solid rgba(255,255,255,.16) !important;
  box-shadow:none !important; width:100%; font-weight:500 !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{ background:rgba(255,255,255,.07) !important; transform:none !important; }}

.sb-brand {{ display:flex; align-items:center; gap:11px; padding:26px 18px 18px; }}
.sb-brand b {{ font-family:var(--font-display); font-size:1.3rem; color:#fff !important; letter-spacing:-.02em; font-weight:600; }}
.sb-brand small {{ display:block; font-size:.74rem; color:#7F919D !important; margin-top:1px; }}
.sb-user {{ margin:6px 12px 14px; padding:12px; border-radius:10px; background:rgba(255,255,255,.05); display:flex; gap:11px; align-items:center; }}
.sb-avatar {{ width:36px; height:36px; border-radius:9px; background:var(--petrol); color:#fff !important; display:flex; align-items:center;
  justify-content:center; font-family:var(--font-display); font-weight:600; flex-shrink:0; }}
.sb-user b {{ color:#fff !important; font-size:.9rem; display:block; line-height:1.2; }}
.sb-user span {{ font-size:.76rem; color:#8CA0AC !important; }}

/* ---- Buttons ---- */
.stButton > button, [data-testid="stFormSubmitButton"] > button, .stDownloadButton > button {{
  background:var(--petrol) !important; color:#fff !important; border:none !important; border-radius:8px !important;
  padding:.55rem 1.3rem !important; font-weight:600 !important; font-size:.9rem !important;
  transition:background .15s, box-shadow .15s !important; box-shadow:none !important;
}}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover, .stDownloadButton > button:hover {{
  background:var(--petrol-dark) !important; box-shadow:0 2px 8px rgba(14,106,122,.3) !important;
}}
.stButton > button p, [data-testid="stFormSubmitButton"] > button p, .stDownloadButton > button p {{ color:#fff !important; font-weight:600 !important; }}
.stButton > button:active {{ transform:translateY(1px); }}

/* ---- Inputs ---- */
.stTextInput input, .stTextArea textarea, .stDateInput input, .stNumberInput input {{
  background:#fff !important; border:1px solid #C9D3D9 !important; border-radius:8px !important; color:var(--text) !important; font-size:.92rem !important;
}}
.stTextInput input:focus, .stTextArea textarea:focus {{ border-color:var(--petrol) !important; box-shadow:0 0 0 3px rgba(14,106,122,.15) !important; }}
div[data-baseweb="select"] > div {{ background:#fff !important; border:1px solid #C9D3D9 !important; border-radius:8px !important; }}
.stTextInput label p, .stTextArea label p, .stSelectbox label p, .stDateInput label p, .stCheckbox label p {{
  font-size:.84rem !important; font-weight:600 !important; color:#33414B !important;
}}
[data-testid="stForm"] {{ background:#fff !important; border:1px solid var(--line) !important; border-radius:12px !important; padding:1.6rem !important; }}

/* ---- Alerts ---- */
[data-testid="stAlert"] {{ border-radius:10px !important; }}

/* ---- Components ---- */
.pg-head {{ margin:0 0 1.6rem; }}
.pg-head h1 {{ font-size:2rem !important; font-weight:600 !important; margin:0 !important; padding:0 !important; line-height:1.15; }}
.pg-head p {{ color:var(--muted); font-size:.95rem; margin:.45rem 0 0; max-width:62ch; }}

.sec-title {{ font-family:var(--font-display); font-size:1.12rem; font-weight:600; color:var(--ink); margin:1.8rem 0 .8rem; display:flex; align-items:baseline; gap:10px; }}
.sec-title span {{ font-family:var(--font-ui); font-size:.82rem; color:var(--muted); font-weight:400; }}

.card {{ background:#fff; border:1px solid var(--line); border-radius:12px; padding:1.3rem 1.5rem; margin-bottom:1rem; }}
.card h3 {{ font-size:1.05rem !important; margin:0 0 .7rem !important; }}

.kpi-grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(170px, 1fr)); gap:14px; margin-bottom:.4rem; }}
.kpi {{ background:#fff; border:1px solid var(--line); border-radius:12px; padding:1rem 1.2rem 1.05rem; position:relative; }}
.kpi .k-label {{ font-size:.84rem; color:var(--muted); font-weight:500; }}
.kpi .k-value {{ font-family:var(--font-display); font-size:2.3rem; font-weight:600; color:var(--ink); line-height:1.1; margin-top:.35rem; letter-spacing:-.02em; }}
.kpi .k-hint {{ font-size:.78rem; color:var(--muted); margin-top:.3rem; }}
.kpi.warn .k-value {{ color:{CRITICAL}; }}
.kpi.warn::before {{ content:""; position:absolute; left:0; top:14px; bottom:14px; width:3px; background:{CRITICAL}; border-radius:0 2px 2px 0; }}

/* badges */
.badge {{ display:inline-flex; align-items:center; gap:6px; padding:3px 10px 3px 8px; border-radius:6px; font-size:.78rem; font-weight:600; white-space:nowrap; }}
.badge::before {{ content:""; width:7px; height:7px; border-radius:50%; background:currentColor; }}
.b-pending {{ background:#FBF1DE; color:{PENDING}; }}
.b-inprogress {{ background:#E3EDFB; color:{PROGRESS}; }}
.b-resolved {{ background:#DFF2E8; color:{RESOLVED}; }}
.p-critical {{ background:#FBE5E5; color:{CRITICAL}; }}
.p-high {{ background:#FBEADF; color:{HIGH}; }}
.p-medium {{ background:#F6EFD6; color:{MEDIUM}; }}
.p-low {{ background:#E8EDF0; color:{LOW}; }}

/* tables */
.tbl-wrap {{ background:#fff; border:1px solid var(--line); border-radius:12px; overflow-x:auto; }}
table.tbl {{ width:100%; border-collapse:collapse; font-size:.88rem; min-width:640px; }}
table.tbl th {{ text-align:left; font-weight:600; font-size:.8rem; color:var(--muted); padding:.8rem 1rem; background:#F8FAFA; border-bottom:1px solid var(--line); white-space:nowrap; }}
table.tbl td {{ padding:.8rem 1rem; border-bottom:1px solid #EEF1F3; color:var(--text); vertical-align:middle; }}
table.tbl tr:last-child td {{ border-bottom:none; }}
table.tbl tbody tr:hover td {{ background:#F6FAFA; }}
table.tbl td.id {{ font-weight:600; color:var(--petrol-dark); white-space:nowrap; }}
table.tbl td.muted {{ color:var(--muted); }}
table.tbl td.wrap {{ max-width:320px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
.tbl-foot {{ font-size:.82rem; color:var(--muted); margin:.55rem .2rem 0; }}

/* detail list */
.kv {{ display:grid; grid-template-columns:150px 1fr; gap:.65rem 1rem; font-size:.92rem; }}
.kv dt {{ color:var(--muted); }} .kv dd {{ margin:0; color:var(--text); }}
@media (max-width:600px) {{ .kv {{ grid-template-columns:1fr; gap:.1rem; }} .kv dd {{ margin-bottom:.6rem; }} }}

/* stepper */
.stepper {{ display:flex; align-items:flex-start; margin:.3rem 0 .2rem; }}
.step {{ flex:1; position:relative; text-align:center; font-size:.82rem; color:var(--muted); }}
.step .dot {{ width:28px; height:28px; border-radius:50%; margin:0 auto 8px; display:flex; align-items:center; justify-content:center;
  background:#fff; border:2px solid #C9D3D9; font-weight:700; font-size:.78rem; position:relative; z-index:1; color:var(--muted); }}
.step::before {{ content:""; position:absolute; top:13px; left:-50%; width:100%; height:2px; background:#D5DDE1; }}
.step:first-child::before {{ display:none; }}
.step.done .dot {{ background:var(--petrol); border-color:var(--petrol); color:#fff; }}
.step.done::before, .step.current::before {{ background:var(--petrol); }}
.step.current .dot {{ border-color:var(--ink); background:var(--signal); color:var(--ink); }}
.step.current, .step.done {{ color:var(--ink); font-weight:600; }}

/* complaint list item */
.item {{ background:#fff; border:1px solid var(--line); border-radius:12px; padding:1rem 1.2rem; margin-bottom:.7rem; }}
.item-top {{ display:flex; justify-content:space-between; gap:10px; align-items:flex-start; flex-wrap:wrap; }}
.item-top b {{ color:var(--ink); }}
.item-meta {{ font-size:.82rem; color:var(--muted); margin-top:2px; }}
.item p {{ margin:.55rem 0 .2rem; font-size:.9rem; color:#33414B; }}

/* empty state */
.empty {{ background:#fff; border:1px dashed #BCC8CF; border-radius:12px; padding:2.4rem 1.5rem; text-align:center; }}
.empty .e-ic {{ width:46px; height:46px; border-radius:12px; background:var(--petrol-tint); color:var(--petrol); display:inline-flex; align-items:center; justify-content:center; }}
.empty h4 {{ font-size:1.05rem !important; margin:.9rem 0 .3rem !important; }}
.empty p {{ color:var(--muted); font-size:.9rem; margin:0 auto; max-width:46ch; }}

.callout {{ border-radius:10px; padding:.9rem 1.1rem; font-size:.9rem; background:var(--petrol-tint); color:var(--petrol-dark); border:1px solid #C5E0E5; margin-bottom:1rem; }}
.callout.ok {{ background:#DFF2E8; color:#17613F; border-color:#BDE3CF; }}

/* login */
.login-brand {{ background:var(--ink); border-radius:16px; padding:3rem 2.6rem; min-height:600px; display:flex; flex-direction:column; justify-content:space-between; }}
.login-brand h2 {{ color:#fff !important; font-size:2.3rem !important; line-height:1.15; font-weight:600 !important; margin:2.2rem 0 1rem !important; max-width:15ch; }}
.login-brand p {{ color:#9FB0BB; max-width:40ch; line-height:1.65; font-size:.98rem; margin:0; }}
.login-brand ul {{ list-style:none; padding:0; margin:0; display:grid; gap:12px; }}
.login-brand li {{ color:#C9D3DA; font-size:.92rem; display:flex; gap:12px; align-items:center; }}
.login-brand li i {{ width:8px; height:8px; border-radius:2px; background:var(--signal); flex-shrink:0; }}
.demo-box {{ margin-top:1.4rem; padding:.9rem 1.1rem; border:1px solid var(--line); border-radius:10px; background:#fff; font-size:.84rem; color:var(--muted); }}
.demo-box code {{ background:#EEF3F4; padding:2px 7px; border-radius:5px; color:var(--petrol-dark); font-size:.82rem; }}
@media (max-width:900px) {{ .login-brand {{ min-height:0; padding:2rem 1.5rem; gap:2rem; }} }}

@media (prefers-reduced-motion: no-preference) {{
  .stepper .step.current .dot {{ animation:pulse 2.2s ease-out infinite; }}
}}
@keyframes pulse {{ 0% {{ box-shadow:0 0 0 0 rgba(242,194,48,.55); }} 70% {{ box-shadow:0 0 0 9px rgba(242,194,48,0); }} 100% {{ box-shadow:0 0 0 0 rgba(242,194,48,0); }} }}

::-webkit-scrollbar {{ width:8px; height:8px; }} ::-webkit-scrollbar-thumb {{ background:#C3CED4; border-radius:4px; }}
</style>
"""


# ---------------------------------------------------------------------------
# HTML component helpers
# ---------------------------------------------------------------------------
def page_header(title: str, subtitle: str = "") -> str:
    sub = f"<p>{esc(subtitle)}</p>" if subtitle else ""
    return f'<div class="pg-head"><h1>{esc(title)}</h1>{sub}</div>'


def section_title(title: str, note: str = "") -> str:
    n = f"<span>{esc(note)}</span>" if note else ""
    return f'<div class="sec-title">{esc(title)}{n}</div>'


def card(content_html: str) -> str:
    return f'<div class="card">{content_html}</div>'


def kpi(label: str, value, hint: str = "", warn: bool = False) -> str:
    h = f'<div class="k-hint">{esc(hint)}</div>' if hint else ""
    cls = "kpi warn" if warn else "kpi"
    return f'<div class="{cls}"><div class="k-label">{esc(label)}</div><div class="k-value">{esc(value)}</div>{h}</div>'


def kpi_grid(items) -> str:
    """items: list of kpi() strings."""
    return f'<div class="kpi-grid">{"".join(items)}</div>'


def status_badge(status: str) -> str:
    s = str(status).strip().lower().replace("-", "").replace(" ", "")
    css = {"pending": "b-pending", "inprogress": "b-inprogress", "resolved": "b-resolved"}.get(s, "b-pending")
    return f'<span class="badge {css}">{esc(status)}</span>'


def priority_badge(priority: str) -> str:
    p = str(priority).strip().lower()
    css = {"critical": "p-critical", "high": "p-high", "medium": "p-medium", "low": "p-low"}.get(p, "p-low")
    return f'<span class="badge {css}">{esc(priority)}</span>'


STEPS = ["Pending", "In Progress", "Resolved"]


def stepper(status: str) -> str:
    cur = STEPS.index(status) if status in STEPS else 0
    parts = []
    for i, label in enumerate(STEPS):
        if status == "Resolved" or i < cur:
            cls, mark = "done", "&#10003;"
        elif i == cur:
            cls, mark = "current", str(i + 1)
        else:
            cls, mark = "todo", str(i + 1)
        parts.append(f'<div class="step {cls}"><div class="dot">{mark}</div>{label}</div>')
    return f'<div class="stepper">{"".join(parts)}</div>'


def empty_state(title: str, text: str, icon_name: str = "inbox") -> str:
    return (
        f'<div class="empty"><span class="e-ic">{icon(icon_name, 22)}</span>'
        f"<h4>{esc(title)}</h4><p>{esc(text)}</p></div>"
    )


def callout(text: str, ok: bool = False) -> str:
    return f'<div class="callout{" ok" if ok else ""}">{text}</div>'


def detail_list(pairs) -> str:
    """pairs: list of (label, html_or_text, is_html)."""
    rows = []
    for label, value, *rest in pairs:
        is_html = bool(rest and rest[0])
        shown = value if is_html else (esc(value) or "&mdash;")
        rows.append(f"<dt>{esc(label)}</dt><dd>{shown}</dd>")
    return f'<dl class="kv">{"".join(rows)}</dl>'


def complaint_item(rec, extra_html: str = "") -> str:
    desc = esc(rec.get("description", ""))
    if len(desc) > 140:
        desc = desc[:140].rstrip() + "..."
    return (
        '<div class="item"><div class="item-top"><div>'
        f'<b>{esc(rec.get("category", ""))}</b> &nbsp;<span class="item-meta">{esc(rec.get("complaint_id", ""))}</span>'
        f'<div class="item-meta">{esc(rec.get("hostel_block", ""))}, room {esc(rec.get("room_number", ""))} &middot; reported {esc(rec.get("date_reported", ""))}</div>'
        f'</div><div>{priority_badge(rec.get("priority", ""))} {status_badge(rec.get("status", ""))}</div></div>'
        f"<p>{desc}</p>{extra_html}</div>"
    )


def table(df, columns) -> str:
    """columns: list of (field, header, kind). kind: id|status|priority|text|muted|wrap"""
    head = "".join(f"<th>{esc(h)}</th>" for _, h, _ in columns)
    body = []
    for _, row in df.iterrows():
        cells = []
        for field, _, kind in columns:
            v = row.get(field, "")
            if kind == "status":
                cells.append(f"<td>{status_badge(v)}</td>")
            elif kind == "priority":
                cells.append(f"<td>{priority_badge(v)}</td>")
            elif kind in ("id", "muted", "wrap"):
                cells.append(f'<td class="{kind}">{esc(v) or "&mdash;"}</td>')
            else:
                cells.append(f'<td>{esc(v) or "&mdash;"}</td>')
        body.append(f'<tr>{"".join(cells)}</tr>')
    return f'<div class="tbl-wrap"><table class="tbl"><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def style_fig(fig, height: int = 300):
    """Apply the shared Plotly look."""
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=8, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Public Sans, sans-serif", color=TEXT, size=12),
        showlegend=False,
        hoverlabel=dict(font_family="Public Sans, sans-serif"),
    )
    fig.update_xaxes(showgrid=False, linecolor=LINE, tickfont=dict(color=MUTED), title=None)
    fig.update_yaxes(gridcolor="#E9EEF0", zeroline=False, tickfont=dict(color=MUTED), title=None)
    return fig
