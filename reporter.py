import json
from planner import ask_llm


def write_report(question, findings, contradictions=None):
    contradictions = contradictions or []
    prompt = f"""You are an education research analyst.
Research question: {question}

Statistical results from a dataset of 1000 students (use only these numbers, do not invent any):
{json.dumps(findings, indent=2)}

Contradictions detected across subjects (top group differs between math, reading and writing):
{json.dumps(contradictions, indent=2)}

Write a clear report in Markdown with exactly these sections:
## Summary
## Key Findings
## Contradictions
## Hypotheses
## Limitations

Rules:
- Summary: 2 to 3 sentences in plain language.
- Key Findings: one short bullet per factor with the group averages, the gap and the effect_size label (negligible, small, medium or large). Copy gap values exactly as given, never round or change them.
- Contradictions: if the list above is empty, write: No contradictions detected across subjects. Otherwise explain each one in plain language, naming which group leads in which subject, and warn that a single overall claim would be misleading.
- Hypotheses: 2 to 3 testable hypotheses that could explain the findings, including one that could explain any contradiction.
- Limitations: mention that this shows association and not cause, and that the dataset is limited.
- Where p_value is 0.0, write p < 0.0001.
- Keep the whole report easy to read for a non-expert."""
    return ask_llm(prompt)
