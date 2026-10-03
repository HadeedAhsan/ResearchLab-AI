# 🧪 ResearchLab AI

An autonomous AI research agent for the education domain. Ask a question about student performance and the agent plans the research, analyzes real data, detects contradictions, and writes a structured report.

## What it does

1. **Plans** the research by choosing the most relevant factors for your question
2. **Analyzes** a dataset of 1000 students with real statistics (group averages and significance tests)
3. **Detects contradictions** when the leading group changes between math, reading and writing
4. **Writes a report** with summary, findings, contradictions, hypotheses and limitations

The AI only writes about numbers computed by Python, so results are not made up.

## AI skills used

- Agentic AI: a LangGraph agent with planning, analysis, contradiction detection and reporting steps
- AI workflows: each stage is a node in a connected graph that shares state
- Gen AI: Groq LLM for planning and report writing

## Tech stack

Python, LangGraph, Groq API, Pandas, SciPy, Plotly, Streamlit

## Run it locally

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a .env file in the project folder:

```
GROQ_API_KEY=your_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

Then start the app:

```
streamlit run app.py
```

## Project structure

- app.py: Streamlit interface
- graph.py: LangGraph agent
- planner.py: question to research plan
- analysis_tools.py: statistics and contradiction detection
- reporter.py: report writing
- data/students.csv: Students Performance dataset from Kaggle

## Team

Add your team name and member names here.

## Live demo

Add your Streamlit link here after deployment.