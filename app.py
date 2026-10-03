import streamlit as st
import pandas as pd
import plotly.express as px
from graph import agent


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ResearchLab AI",
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

    </style>
    """,
    unsafe_allow_html=True,
)


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

examples = [
    "Does family background affect student exam performance?",
    "Does test preparation improve exam scores?",
    "Is there a gender gap in student performance?",
]


# =========================================================
# SESSION STATE
# =========================================================

if "question" not in st.session_state:
    st.session_state.question = ""


# =========================================================
# HERO
# =========================================================

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


# =========================================================
# START RESEARCH
# =========================================================

st.markdown("## 🔎 Start Your Research")

st.markdown(
    '<p class="section-description">'
    'Choose a question below or enter your own research question.'
    '</p>',
    unsafe_allow_html=True,
)


# =========================================================
# QUICK QUESTIONS
# =========================================================

st.markdown(
    '<div class="eyebrow">Quick Questions</div>',
    unsafe_allow_html=True,
)

cols = st.columns(3)

for i, example in enumerate(examples):
    with cols[i]:
        if st.button(
            example,
            key=f"quick_question_{i}",
            use_container_width=True,
        ):
            st.session_state.question = example


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# RESEARCH QUESTION
# =========================================================

st.markdown(
    '<div class="eyebrow">Your Research Question</div>',
    unsafe_allow_html=True,
)

question = st.text_input(
    "Research question",
    key="question",
    placeholder="e.g. Does test preparation improve exam scores?",
    label_visibility="collapsed",
)


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# RUN RESEARCH
# =========================================================

run_research = st.button(
    "🔍 Run Research",
    type="primary",
    use_container_width=True,
)


# =========================================================
# RESEARCH
# =========================================================

if run_research:

    if not st.session_state.question.strip():

        st.warning(
            "Please enter a research question first."
        )

    else:

        try:

            with st.spinner(
                "🧠 ResearchLab AI is analyzing your question..."
            ):

                result = agent.invoke(
                    {
                        "question": st.session_state.question
                    }
                )

                findings = result["findings"]
                contradictions = result["contradictions"]
                report = result["report"]


            # =================================================
            # RESULTS
            # =================================================

            st.markdown("## 📊 Research Results")

            st.markdown(
                '<p class="section-description">'
                'Insights discovered from the research analysis.'
                '</p>',
                unsafe_allow_html=True,
            )


            # =================================================
            # CONTRADICTIONS
            # =================================================

            for c in contradictions:

                factor = c["group_column"].title()

                st.warning(
                    f"⚠️ Contradiction found in {factor}: "
                    "the leading group is different across math, "
                    "reading and writing, so no single overall "
                    "claim is safe."
                )


            # =================================================
            # FINDINGS
            # =================================================

            for f in findings:

                factor = f["group_column"].title()

                st.markdown(
                    f"### {factor}"
                )

                st.markdown(
                    f"**Difference between groups: "
                    f"{f['gap']} points**"
                )


                chart_df = pd.DataFrame(
                    {
                        "Group": list(
                            f["group_means"].keys()
                        ),
                        "Average score": list(
                            f["group_means"].values()
                        ),
                    }
                )


                order = (
                    {"Group": EDUCATION_ORDER}
                    if f["group_column"]
                    == "parental level of education"
                    else {}
                )


                # ---------------------------------------------
                # CHART
                # ---------------------------------------------

                fig = px.bar(
                    chart_df,
                    x="Group",
                    y="Average score",
                    text="Average score",
                    category_orders=order,
                )


                fig.update_layout(
                    yaxis_range=[0, 100],
                    height=340,
                    margin=dict(
                        l=20,
                        r=20,
                        t=20,
                        b=20,
                    ),
                    plot_bgcolor="#f4f5f7",
                    paper_bgcolor="#f4f5f7",
                    font=dict(
                        color="#111827"
                    ),
                    xaxis=dict(
                        tickfont=dict(
                            color="black"
                        )
                    ),
                )


                fig.update_traces(
                    textposition="outside",
                    cliponaxis=False,
                )


                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={
                        "displayModeBar": False
                    },
                )


                st.markdown("---")


            # =================================================
            # REPORT
            # =================================================

            st.markdown("## 📄 Research Report")

            st.markdown(
                '<p class="section-description">'
                'A complete summary generated from the research findings.'
                '</p>',
                unsafe_allow_html=True,
            )


            # Report is now displayed without the extra box

            st.markdown(report)


            st.download_button(
                "⬇️ Download Research Report",
                data=report,
                file_name="research_report.md",
                mime="text/markdown",
                use_container_width=True,
            )


        except Exception as e:

            st.error(
                "Something went wrong while running the research."
            )

            st.caption(
                f"Error details: {e}"
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