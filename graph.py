from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from planner import make_plan
from analysis_tools import load_data, compare_groups, find_contradictions
from reporter import write_report


class ResearchState(TypedDict):
    question: str
    plan: list
    findings: list
    contradictions: list
    report: str


def planner_step(state: ResearchState):
    return {"plan": make_plan(state["question"])}


def analyze_step(state: ResearchState):
    df = load_data()
    findings = []
    for task in state["plan"]:
        result = compare_groups(df, task["group_column"])
        result["reason"] = task["reason"]
        findings.append(result)
    return {"findings": findings}


def contradiction_step(state: ResearchState):
    df = load_data()
    contradictions = []
    for task in state["plan"]:
        result = find_contradictions(df, task["group_column"])
        if result["contradiction"]:
            contradictions.append(result)
    return {"contradictions": contradictions}


def report_step(state: ResearchState):
    return {"report": write_report(state["question"], state["findings"], state["contradictions"])}


builder = StateGraph(ResearchState)
builder.add_node("planner_step", planner_step)
builder.add_node("analyze_step", analyze_step)
builder.add_node("contradiction_step", contradiction_step)
builder.add_node("report_step", report_step)

builder.add_edge(START, "planner_step")
builder.add_edge("planner_step", "analyze_step")
builder.add_edge("analyze_step", "contradiction_step")
builder.add_edge("contradiction_step", "report_step")
builder.add_edge("report_step", END)

agent = builder.compile()


if __name__ == "__main__":
    result = agent.invoke({"question": "Is there a gender gap in student performance?"})
    print("PLAN:", [t["group_column"] for t in result["plan"]])
    print()
    print("CONTRADICTIONS:", result["contradictions"])