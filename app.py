import html
import inspect
import os
import re
import time

import pandas as pd
import plotly.express as px
import streamlit as st

from analysis_tools import load_data
from graph import agent
from planner import MissingKeyError, OutOfScopeError, PlanError


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ResearchLab-AI",
    page_icon="🧪",
    layout="wide",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ================= PAGE ================= */

    .stApp {
        background-color: #f4f5f7;
        color: #111827;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ================= REMOVE TOP NAVBAR ================= */

    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
    }


    /* ================= HERO ================= */

    .hero-container {
        background: #172554;
        padding: 40px 45px;
        border-radius: 24px;
        margin-bottom: 38px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.18);
    }

    .hero-container h1 {
        color: white !important;
        font-size: 42px !important;
        font-weight: 800 !important;
        margin: 0 !important;
    }

    .hero-description {
        color: white !important;
        font-size: 17px;
        line-height: 1.6;
        margin-top: 10px;
        max-width: 780px;
    }


    /* ================= SECTION TITLES ================= */

    h2, h3 {
        color: #111827 !important;
    }

    .section-description {
        color: #111827;
        font-size: 15px;
        margin-bottom: 20px;
    }


    /* ================= SMALL LABELS ================= */

    .eyebrow {
        color: #172554;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }


    /* ================= QUICK QUESTIONS ================= */

    div.stButton > button {
        background-color: white;
        color: #111827;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        min-height: 52px;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background-color: #172554;
        color: white;
        border-color: #172554;
    }


    /* ================= RESEARCH INPUT ================= */

    .stTextInput input {
        background-color: white !important;
        color: #111827 !important;
        border: 1px solid #94a3b8 !important;
        border-radius: 12px !important;
        min-height: 50px !important;
        padding: 12px 15px !important;
        font-size: 15px !important;
    }

    .stTextInput input::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }


    /* ================= PRIMARY BUTTON ================= */

    div.stButton > button[kind="primary"] {
        background-color: #172554 !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        min-height: 52px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #0f172a !important;
        color: white !important;
    }


    /* ================= CONTRADICTION ================= */

    .stAlert {
        background-color: #172554 !important;
        color: white !important;
        border-radius: 14px !important;
        border: none !important;
    }

    .stAlert p {
        color: white !important;
    }


    /* ================= REPORT ================= */

    .report-content {
        background-color: white;
        color: #111827;
        padding: 28px;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
    }

    .report-content p,
    .report-content li,
    .report-content h1,
    .report-content h2,
    .report-content h3 {
        color: #111827 !important;
    }


    /* ================= DOWNLOAD BUTTON ================= */

    .stDownloadButton button {
        background-color: #172554 !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        min-height: 48px !important;
        font-weight: 700 !important;
    }


    /* ================= FOOTER ================= */

    .footer-text {
        color: #111827;
        text-align: center;
        font-size: 13px;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #cbd5e1;
    }


    /* ================= BUTTON TEXT ================= */

    div.stButton > button p,
    .stFormSubmitButton button p {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }

    div.stButton > button:hover p {
        color: white !important;
    }


    /* ================= FORM ================= */

    [data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }

    .stFormSubmitButton button,
    [data-testid="stFormSubmitButton"] button {
        background-color: #172554 !important;
        border: none !important;
        border-radius: 12px !important;
        min-height: 52px !important;
        font-weight: 700 !important;
    }

    .stFormSubmitButton button p,
    [data-testid="stFormSubmitButton"] button p {
        color: white !important;
        font-size: 16px !important;
    }


    /* ================= HOW IT WORKS ================= */

    .step-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin: 6px 0 26px 0;
    }

    @media (max-width: 900px) {
        .step-grid { grid-template-columns: repeat(2, 1fr); }
    }

    @media (max-width: 560px) {
        .step-grid { grid-template-columns: 1fr; }
    }

    .step-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 18px;
    }

    .step-num {
        display: inline-block;
        background: #172554;
        color: white;
        border-radius: 999px;
        width: 26px;
        height: 26px;
        line-height: 26px;
        text-align: center;
        font-size: 13px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .step-title {
        color: #111827;
        font-weight: 800;
        font-size: 15px;
        margin-bottom: 4px;
    }

    .step-text {
        color: #374151;
        font-size: 13.5px;
        line-height: 1.5;
    }


    /* ================= RESULT CARDS ================= */

    .metric-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 16px 18px;
        height: 100%;
    }

    .metric-title {
        color: #172554;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric-value {
        color: #111827;
        font-size: 30px;
        font-weight: 800;
        margin: 4px 0 0 0;
    }

    .metric-sub {
        color: #6b7280;
        font-size: 12.5px;
        margin-bottom: 10px;
    }

    .metric-tag {
        display: inline-block;
        background: #e0e7ff;
        color: #172554;
        border-radius: 999px;
        padding: 2px 10px;
        font-size: 12px;
        font-weight: 700;
        margin: 0 6px 6px 0;
    }

    .metric-tag.muted {
        background: #f1f5f9;
        color: #475569;
    }

    .metric-why {
        color: #374151;
        font-size: 13px;
        line-height: 1.45;
        margin-top: 4px;
    }


    /* ================= NOTICES ================= */

    .notice {
        border-radius: 14px;
        padding: 14px 18px;
        font-size: 14.5px;
        line-height: 1.5;
        margin: 8px 0 14px 0;
    }

    .notice.info {
        background: #e0e7ff;
        color: #172554;
    }

    .notice.error {
        background: #fee2e2;
        color: #7f1d1d;
    }



    /* ================= BUTTONS (uniform look) ================= */

    div.stButton,
    .stDownloadButton {
        margin-bottom: 4px;
    }

    button[data-testid^="stBaseButton"] {
        border-radius: 12px !important;
        min-height: 52px !important;
        height: auto !important;
        padding: 0.6rem 1.1rem !important;
        transition: transform .18s ease, box-shadow .18s ease,
                    background-color .18s ease, border-color .18s ease !important;
    }

    button[data-testid="stBaseButton-secondary"] {
        background-color: white !important;
        color: #111827 !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05) !important;
    }

    button[data-testid="stBaseButton-secondary"]:hover {
        background-color: #172554 !important;
        border-color: #172554 !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(23, 37, 84, 0.18) !important;
    }

    button[data-testid="stBaseButton-secondary"]:hover p {
        color: white !important;
    }

    .stDownloadButton button[data-testid^="stBaseButton"] {
        background-color: #172554 !important;
        border: none !important;
    }

    .stDownloadButton button p {
        color: white !important;
    }

    .stDownloadButton button:hover {
        background-color: #0f172a !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(23, 37, 84, 0.25) !important;
    }


    /* ================= TEXT INPUT ================= */

    [data-testid="stTextInputRootElement"] {
        background: white !important;
        border: 1px solid #94a3b8 !important;
        border-radius: 12px !important;
        min-height: 52px !important;
        height: auto !important;
        overflow: hidden !important;
        transition: border-color .15s ease, box-shadow .15s ease;
    }

    [data-testid="stTextInputRootElement"]:focus-within {
        border-color: #172554 !important;
        box-shadow: 0 0 0 3px rgba(23, 37, 84, 0.15) !important;
    }

    [data-testid="stTextInputRootElement"] > div,
    [data-testid="stTextInputRootElement"] [data-baseweb="base-input"],
    [data-testid="stTextInputRootElement"] [data-baseweb="input"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        height: auto !important;
        min-height: 50px !important;
    }

    .stTextInput input {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        min-height: 50px !important;
        padding: 12px 16px !important;
    }


    /* ================= CARDS ================= */

    .step-grid {
        gap: 16px;
        margin: 10px 0 22px 0;
    }

    .step-card {
        padding: 22px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
        transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    }

    .step-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 30px rgba(23, 37, 84, 0.12);
        border-color: #c7d2fe;
    }

    .step-title {
        margin-bottom: 6px;
    }

    .tip-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin: 4px 0 32px 0;
    }

    @media (max-width: 900px) {
        .tip-grid { grid-template-columns: 1fr; }
    }

    .tip-card {
        background: #eef2ff;
        border: 1px solid #dbe4ff;
        border-radius: 16px;
        padding: 18px 22px;
        transition: transform .18s ease, box-shadow .18s ease;
    }

    .tip-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 24px rgba(23, 37, 84, 0.10);
    }

    .tip-title {
        color: #172554;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }

    .tip-text {
        color: #1f2937;
        font-size: 14px;
        line-height: 1.55;
    }

    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 18px;
        margin: 14px 0 18px 0;
    }

    .metric-card {
        position: relative;
        overflow: hidden;
        height: auto;
        padding: 24px 26px 20px 26px;
        border-radius: 18px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
        transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    }

    .metric-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: #172554;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 30px rgba(23, 37, 84, 0.14);
        border-color: #c7d2fe;
    }

    .metric-value {
        font-size: 34px;
        margin: 6px 0 2px 0;
    }

    .metric-sub {
        margin-bottom: 14px;
    }

    .metric-tag {
        padding: 4px 12px;
        margin: 0 8px 8px 0;
    }

    .metric-why {
        margin-top: 8px;
        padding-top: 12px;
        border-top: 1px solid #eef2f7;
        font-size: 13.5px;
    }

    .hint {
        background: white;
        border: 1px dashed #cbd5e1;
        border-radius: 14px;
        padding: 12px 18px;
        color: #475569;
        font-size: 13.5px;
        line-height: 1.55;
        margin: 4px 0 24px 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit Cloud: copy secrets into the environment so planner.py can read them
try:
    for _name in ("GROQ_API_KEY", "GROQ_MODEL"):
        if _name in st.secrets and not os.getenv(_name):
            os.environ[_name] = st.secrets[_name]
except Exception:
    pass


# =========================================================
# HELPERS
# =========================================================

def stretch(fn):
    """Full width kwarg that works on old and new Streamlit."""
    if "width" in inspect.signature(fn).parameters:
        return {"width": "stretch"}
    return {"use_container_width": True}


def notice(kind, text):
    st.markdown(
        f'<div class="notice {kind}">{html.escape(text)}</div>',
        unsafe_allow_html=True,
    )


@st.cache_data
def get_df():
    return load_data()


# =========================================================
# DATA
# =========================================================

EDUCATION_ORDER = [
    "some high school",
    "high school",
    "some college",
    "associate's degree",
    "bachelor's degree",
    "master's degree",
]

FACTOR_LABELS = {
    "gender": "Gender",
    "race/ethnicity": "Race/Ethnicity",
    "parental level of education": "Parental education",
    "lunch": "Lunch type",
    "test preparation course": "Test preparation",
}

COLUMN_GUIDE = [
    ("gender", "Student gender (female or male)"),
    ("race/ethnicity", "Anonymised group A to E as given in the dataset"),
    ("parental level of education", "Highest education level of a parent"),
    ("lunch", "Standard or free/reduced lunch (often used as a proxy for family income)"),
    ("test preparation course", "Whether the student completed a prep course"),
    ("math / reading / writing score", "Exam scores from 0 to 100"),
    ("average score", "Mean of the three scores, calculated by the app"),
]

QUICK = [
    ("Family background and scores", "Does family background affect student exam performance?"),
    ("Does test prep help?", "Does test preparation improve exam scores?"),
    ("Is there a gender gap?", "Is there a gender gap in student performance?"),
]

EXAMPLES = [q for _, q in QUICK]

MORE_QUESTIONS = EXAMPLES + [
    "Does lunch type relate to exam scores?",
    "Does parental education matter for student results?",
    "Do exam scores differ across race/ethnicity groups?",
]

STEP_TEXT = {
    "planner_step": lambda s: "Plan ready. The agent will look at: "
    + ", ".join(FACTOR_LABELS.get(t["group_column"], t["group_column"]) for t in s["plan"])
    + ".",
    "analyze_step": lambda s: f"Compared groups and ran significance tests on {len(s['findings'])} factor(s).",
    "contradiction_step": lambda s: (
        "No contradictions across subjects."
        if not s["contradictions"]
        else f"Found {len(s['contradictions'])} contradiction(s) across subjects."
    ),
    "report_step": lambda s: "Report written.",
}

NEXT_LABEL = {
    "planner_step": "Analyzing student data...",
    "analyze_step": "Checking for contradictions...",
    "contradiction_step": "Writing the report...",
    "report_step": "Research complete",
}


# =========================================================
# SESSION STATE
# =========================================================

_defaults = {
    "question": "",
    "pending": False,
    "result": None,
    "history": [],
    "view": "home",
    "flash": None,
}
for _key, _value in _defaults.items():
    if _key not in st.session_state:
        st.session_state[_key] = _value


def pick_question(q):
    st.session_state.question = q
    st.session_state.pending = True


def submit_form():
    st.session_state.pending = True


def go_home():
    st.session_state.view = "home"


def load_history(i):
    item = st.session_state.history[i]
    st.session_state.result = item
    st.session_state.question = item["question"]
    st.session_state.view = "results"


def clear_history():
    st.session_state.history = []


# =========================================================
# RUN THE AGENT
# =========================================================

def run_research(question):
    """Returns True on success. On failure stores a flash message and returns False."""
    state = {"question": question}
    start = time.time()

    try:
        with st.status("Planning the research...", expanded=True) as status:
            for update in agent.stream({"question": question}, stream_mode="updates"):
                for node, data in update.items():
                    state.update(data)
                    st.write("✅ " + STEP_TEXT[node](state))
                    status.update(label=NEXT_LABEL[node])
            status.update(label="Research complete", state="complete", expanded=False)
    except MissingKeyError:
        st.session_state.flash = (
            "error",
            "No Groq API key found. Add GROQ_API_KEY to your .env file "
            "(or to Streamlit secrets when deployed), then restart the app.",
            "",
        )
        return False
    except OutOfScopeError:
        st.session_state.flash = (
            "info",
            "That question does not look like it is about this dataset. Try asking "
            "about exam scores and a factor like gender, lunch, parental education, "
            "race/ethnicity or test preparation.",
            "",
        )
        return False
    except PlanError:
        st.session_state.flash = (
            "error",
            "The AI could not build a research plan for that question. Try rephrasing it.",
            "",
        )
        return False
    except Exception as e:
        st.session_state.flash = (
            "error",
            "Something went wrong while running the research.",
            f"Error details: {e}",
        )
        return False

    result = {
        "question": question,
        "plan": state["plan"],
        "findings": state["findings"],
        "contradictions": state["contradictions"],
        "report": state["report"],
        "seconds": round(time.time() - start, 1),
    }
    st.session_state.result = result
    st.session_state.view = "results"
    history = [h for h in st.session_state.history if h["question"] != question]
    history.insert(0, result)
    st.session_state.history = history[:8]
    return True


# =========================================================
# PAGE PIECES
# =========================================================

def render_hero():
    st.markdown(
        """
        <div class="hero-container">
            <h1>🧪 ResearchLab AI</h1>
            <p class="hero-description">
                Turn your research question into meaningful insights.
                ResearchLab AI plans the research, analyzes real student data,
                identifies patterns and contradictions, and generates a report.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home_button():
    col, _ = st.columns([1, 4])
    with col:
        st.button("🏠 Home", key="home_btn", on_click=go_home, **stretch(st.button))


def render_how_it_works():
    st.markdown("## How this page works")
    st.markdown(
        '<div class="step-grid">'
        '<div class="step-card"><div class="step-num">1</div>'
        '<div class="step-title">Ask a question</div>'
        '<div class="step-text">Tap a quick question or type your own about student exam scores.</div></div>'
        '<div class="step-card"><div class="step-num">2</div>'
        '<div class="step-title">The agent plans</div>'
        '<div class="step-text">It picks which factors to study, like parental education, lunch or test prep.</div></div>'
        '<div class="step-card"><div class="step-num">3</div>'
        '<div class="step-title">Python analyzes</div>'
        '<div class="step-text">Group averages, significance tests and a check for contradictions across subjects.</div></div>'
        '<div class="step-card"><div class="step-num">4</div>'
        '<div class="step-title">Read and download</div>'
        '<div class="step-text">See charts in Results, the written Report, and the Data and Method tab.</div></div>'
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="tip-grid">'
        '<div class="tip-card"><div class="tip-title">Try asking</div>'
        '<div class="tip-text">Does test prep improve scores? Is there a gender gap?</div></div>'
        '<div class="tip-card"><div class="tip-title">It can look at</div>'
        '<div class="tip-text">Gender, race/ethnicity, parental education, lunch type and test prep.</div></div>'
        '<div class="tip-card"><div class="tip-title">Keep in mind</div>'
        '<div class="tip-text">Shows patterns, not causes. One dataset of 1,000 students.</div></div>'
        "</div>",
        unsafe_allow_html=True,
    )


def render_ask(show_quick, flash=None):
    if show_quick:
        st.markdown("## 🔎 Start Your Research")
        st.markdown(
            '<p class="section-description">'
            "Choose a question below or enter your own research question."
            "</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="eyebrow">Quick Questions (tap to run instantly)</div>',
            unsafe_allow_html=True,
        )
        cols = st.columns(3)
        for i, (label, question) in enumerate(QUICK):
            with cols[i]:
                st.button(
                    label,
                    key=f"quick_question_{i}",
                    on_click=pick_question,
                    args=(question,),
                    help=question,
                    **stretch(st.button),
                )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div class="eyebrow">Or write your own question</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="eyebrow">Ask a new question</div>',
            unsafe_allow_html=True,
        )

    with st.form("research_form"):
        st.text_input(
            "Research question",
            key="question",
            placeholder="e.g. Does test preparation improve exam scores?",
            label_visibility="collapsed",
        )
        st.form_submit_button(
            "🔍 Run Research",
            type="primary",
            on_click=submit_form,
            **stretch(st.form_submit_button),
        )

    if flash:
        notice(flash[0], flash[1])
        if flash[2]:
            st.caption(flash[2])


def render_history_buttons(prefix, limit=8):
    for i, past in enumerate(st.session_state.history[:limit]):
        st.button(
            past["question"],
            key=f"{prefix}_{i}",
            on_click=load_history,
            args=(i,),
            help="Reopen this result",
            **stretch(st.button),
        )


def style_fig(fig):
    fig.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor="#f4f5f7",
        paper_bgcolor="#f4f5f7",
        font=dict(color="#111827"),
        legend=dict(orientation="h", y=1.12, title_text=""),
    )
    fig.update_xaxes(tickfont=dict(color="#111827"), title_font=dict(color="#111827"))
    fig.update_yaxes(
        tickfont=dict(color="#111827"),
        title_font=dict(color="#111827"),
        gridcolor="#e2e8f0",
    )
    return fig


def metric_card(f):
    label = FACTOR_LABELS.get(f["group_column"], f["group_column"].title())
    p = "p < 0.0001" if f["p_value"] == 0 else f"p = {f['p_value']}"
    sig = "Significant" if f["significant"] else "Not significant"
    effect = f.get("effect_size", "")
    tags = f'<span class="metric-tag">{sig}</span><span class="metric-tag muted">{p}</span>'
    if effect:
        tags += f'<span class="metric-tag muted">{effect} effect</span>'
    why = html.escape(f.get("reason", ""))
    return (
        '<div class="metric-card">'
        f'<div class="metric-title">{html.escape(label)}</div>'
        f'<div class="metric-value">{f["gap"]} pts</div>'
        '<div class="metric-sub">gap between top and bottom group</div>'
        f"{tags}"
        f'<div class="metric-why">{why}</div>'
        "</div>"
    )


def bar_chart(f, zoom):
    sizes = f.get("group_sizes", {})
    rows = []
    for group, mean in f["group_means"].items():
        n = sizes.get(str(group))
        rows.append(
            {
                "Group": f"{group} (n={n})" if n else str(group),
                "Raw": str(group),
                "Average score": mean,
            }
        )
    if f["group_column"] == "parental level of education":
        rows.sort(
            key=lambda r: EDUCATION_ORDER.index(r["Raw"])
            if r["Raw"] in EDUCATION_ORDER
            else 99
        )

    df = pd.DataFrame(rows)
    hi, lo = df["Average score"].max(), df["Average score"].min()
    df["Role"] = [
        "Highest" if m == hi else "Lowest" if m == lo else "Other"
        for m in df["Average score"]
    ]

    fig = px.bar(
        df,
        x="Group",
        y="Average score",
        color="Role",
        text="Average score",
        category_orders={"Group": df["Group"].tolist(), "Role": ["Highest", "Other", "Lowest"]},
        color_discrete_map={"Highest": "#172554", "Other": "#93c5fd", "Lowest": "#f59e0b"},
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        yaxis_range=[max(0, lo - 8), min(100, hi + 6)] if zoom else [0, 100]
    )
    return style_fig(fig)


def subject_chart(c):
    rows = []
    for subject, groups in c["means_by_subject"].items():
        for group, mean in groups.items():
            rows.append(
                {
                    "Group": group,
                    "Subject": subject.replace(" score", "").title(),
                    "Average score": mean,
                }
            )
    fig = px.bar(
        pd.DataFrame(rows),
        x="Group",
        y="Average score",
        color="Subject",
        barmode="group",
        text="Average score",
        color_discrete_sequence=["#172554", "#3b82f6", "#93c5fd"],
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(yaxis_range=[0, 100])
    return style_fig(fig)


def findings_csv(findings):
    rows = []
    for f in findings:
        for group, mean in f["group_means"].items():
            rows.append(
                {
                    "factor": f["group_column"],
                    "group": group,
                    "students": f.get("group_sizes", {}).get(str(group)),
                    "average_score": mean,
                    "factor_gap": f["gap"],
                    "p_value": f["p_value"],
                    "significant": f["significant"],
                    "eta_squared": f.get("eta_squared"),
                    "effect_size": f.get("effect_size"),
                }
            )
    return pd.DataFrame(rows).to_csv(index=False)


def render_results(res):
    findings = res["findings"]
    contradictions = res["contradictions"]

    st.caption(f"Question asked: {res['question']}  ·  finished in {res['seconds']}s")

    # ---- summary cards ----
    st.markdown(
        '<div class="card-grid">' + "".join(metric_card(f) for f in findings) + "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hint"><b>How to read this:</b> the gap is the highest group average '
        "minus the lowest. A p value under 0.05 means the difference is unlikely to be chance. "
        "Effect size shows how big it is in practice.</div>",
        unsafe_allow_html=True,
    )

    # ---- contradictions ----
    st.markdown("### Contradictions across subjects")
    if contradictions:
        for c in contradictions:
            label = FACTOR_LABELS.get(c["group_column"], c["group_column"].title())
            st.warning(
                f"⚠️ Contradiction found in {label}: the leading group is "
                "different across math, reading and writing, so no single "
                "overall claim is safe."
            )
            st.plotly_chart(
                subject_chart(c),
                key=f"subject_{c['group_column']}",
                config={"displayModeBar": False},
                **stretch(st.plotly_chart),
            )
            leaders = "  ·  ".join(
                f"{s.replace(' score', '').title()}: {info['top_group']} leads ({info['top_score']})"
                for s, info in c["by_subject"].items()
            )
            st.caption(leaders)
    else:
        notice(
            "info",
            "No contradictions. For every factor checked, the same group leads "
            "in math, reading and writing.",
        )

    # ---- group charts ----
    st.markdown("### Group averages")
    zoom = st.toggle(
        "Zoom chart axis to the data range",
        value=False,
        help="Makes small gaps easier to see. The axis will not start at zero.",
    )
    for f in findings:
        label = FACTOR_LABELS.get(f["group_column"], f["group_column"].title())
        st.markdown(f"**{label}**")
        st.plotly_chart(
            bar_chart(f, zoom),
            key=f"bars_{f['group_column']}",
            config={"displayModeBar": False},
            **stretch(st.plotly_chart),
        )
    if zoom:
        st.caption("Note: the axis does not start at zero, so gaps look bigger than they are.")


def render_report(res):
    report = res["report"]
    st.markdown(re.sub(r"(?m)^## ", "### ", report))

    left, right = st.columns(2)
    with left:
        st.download_button(
            "⬇️ Download report (.md)",
            data=report,
            file_name="research_report.md",
            mime="text/markdown",
            **stretch(st.download_button),
        )
    with right:
        st.download_button(
            "⬇️ Download numbers (.csv)",
            data=findings_csv(res["findings"]),
            file_name="research_numbers.csv",
            mime="text/csv",
            **stretch(st.download_button),
        )
    with st.expander("Copy report as text"):
        st.code(report, language="markdown")


def render_data_tab(res):
    df = get_df()
    st.markdown("### The dataset")
    st.caption(f"{len(df)} students. First 25 rows shown.")
    st.dataframe(df.head(25), hide_index=True, **stretch(st.dataframe))

    st.markdown("### What each column means")
    st.dataframe(
        pd.DataFrame(COLUMN_GUIDE, columns=["Column", "Meaning"]),
        hide_index=True,
        **stretch(st.dataframe),
    )

    st.markdown("### How the analysis works")
    st.markdown(
        """
- **Planning:** the AI picks 2 to 4 factors that match your question.
- **Group comparison:** a t test for two groups, one way ANOVA for more than two. This gives the p value.
- **Effect size:** eta squared, shown as negligible, small, medium or large.
- **Contradictions:** flagged when the top group is not the same in math, reading and writing.
- **Report:** the AI writes only from the numbers Python calculated.
- **Limits:** results show association, not cause. One dataset, 1,000 students.
        """
    )

    st.markdown("### Research plan the agent chose")
    for t in res["plan"]:
        label = FACTOR_LABELS.get(t["group_column"], t["group_column"])
        st.markdown(f"**{label}**: {t.get('reason') or 'no reason given'}")



# =========================================================
# MAIN FLOW
# =========================================================

running = st.session_state.pending
st.session_state.pending = False
flash = st.session_state.flash
st.session_state.flash = None

on_home = st.session_state.view == "home" and not running

render_hero()

if on_home:
    render_how_it_works()
    render_ask(True, flash)
    if st.session_state.history:
        st.markdown('<div class="eyebrow">Recent questions</div>', unsafe_allow_html=True)
        render_history_buttons("recent", limit=5)
        st.button("Clear history", key="clear_history", on_click=clear_history)
else:
    render_home_button()
    render_ask(False, flash)

if running:
    q = st.session_state.question.strip()
    if not q:
        st.session_state.flash = ("info", "Please enter a research question first.", "")
        st.rerun()
    elif not run_research(q):
        st.rerun()

res = st.session_state.result

if st.session_state.view == "results" and res and not on_home:
    st.markdown("## Research Results")
    tab_results, tab_report, tab_data = st.tabs(
        ["Results", "Report", "Data and Method"]
    )
    with tab_results:
        render_results(res)
    with tab_report:
        render_report(res)
    with tab_data:
        render_data_tab(res)

    st.markdown("## 💡 Ask something else")
    options = [q for q in MORE_QUESTIONS if q != res["question"]][:3]
    follow_cols = st.columns(len(options))
    for i, q in enumerate(options):
        with follow_cols[i]:
            st.button(
                q,
                key=f"follow_{i}",
                on_click=pick_question,
                args=(q,),
                help=q,
                **stretch(st.button),
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <p class="footer-text">
        🧪 ResearchLab AI · AI-powered research and data analysis
    </p>
    """,
    unsafe_allow_html=True,
)