from planner import make_plan
from analysis_tools import load_data, compare_groups


def run_research(question):
    df = load_data()
    plan = make_plan(question)
    findings = []
    for task in plan:
        result = compare_groups(df, task["group_column"])
        result["reason"] = task["reason"]
        findings.append(result)
    return findings


if __name__ == "__main__":
    question = "Does family background affect student exam performance?"
    for finding in run_research(question):
        print(finding)
        print()