import streamlit as st
import pandas as pd
import plotly.express as px
from graph import agent

st.set_page_config(page_title="ResearchLab AI", page_icon="🧪", layout="centered")

EDUCATION_ORDER = [
    "some high school",
    "high school",
    "some college",
    "associate's degree",
    "bachelor's degree",
    "master's degree",
]

st.title("🧪 ResearchLab AI")
st.caption("Ask a question about student performance. The agent plans the research, analyzes real data, and writes a report.")

examples = [
    "Does family background affect student exam performance?",
    "Does test preparation improve exam scores?",
    "Is there a gender gap in student performance?",
]

choice = st.selectbox("Pick an example question, or type your own below", examples)
question = st.text_input("Your research question", value=choice)

if st.button("Run Research", type="primary"):
    if not question.strip():
        st.warning("Please enter a research question first.")
    else:
        try:
            with st.spinner("The agent is working, this takes a few seconds..."):
                result = agent.invoke({"question": question})
                findings = result["findings"]
                contradictions = result["contradictions"]
                report = result["report"]

            st.header("Results")

            for c in contradictions:
                factor = c["group_column"].title()
                st.warning(
                    f"Contradiction found in {factor}: the leading group is different "
                    "across math, reading and writing, so no single overall claim is safe."
                )

            for f in findings:
                st.subheader(f["group_column"].title())
                st.caption(f"Gap between groups: {f['gap']} points")
                chart_df = pd.DataFrame({
                    "Group": list(f["group_means"].keys()),
                    "Average score": list(f["group_means"].values()),
                })
                order = {"Group": EDUCATION_ORDER} if f["group_column"] == "parental level of education" else {}
                fig = px.bar(chart_df, x="Group", y="Average score", text="Average score", category_orders=order)
                fig.update_layout(yaxis_range=[0, 100], height=320)
                st.plotly_chart(fig)

            st.header("Report")
            st.markdown(report)
            st.download_button("Download report", data=report, file_name="research_report.md", mime="text/markdown")
        except Exception:
            st.error("Something went wrong. Please try again or rephrase your question.")