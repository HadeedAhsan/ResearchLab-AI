import os
import re
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

DEFAULT_MODEL = "openai/gpt-oss-120b"

GROUP_COLUMNS = [
    "gender",
    "race/ethnicity",
    "parental level of education",
    "lunch",
    "test preparation course",
]


class MissingKeyError(RuntimeError):
    """GROQ_API_KEY is not set."""


class OutOfScopeError(ValueError):
    """The question is not about this dataset."""


class PlanError(ValueError):
    """The model did not return a usable plan."""


_client = None


def get_client():
    global _client
    if _client is None:
        key = os.getenv("GROQ_API_KEY")
        if not key:
            raise MissingKeyError("GROQ_API_KEY is not set.")
        _client = Groq(api_key=key)
    return _client


def ask_llm(prompt):
    response = get_client().chat.completions.create(
        model=os.getenv("GROQ_MODEL", DEFAULT_MODEL),
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def make_plan(question):
    prompt = f"""You are a research planner for an education dataset of student exam scores.
Available factors: {GROUP_COLUMNS}
Research question: {question}

Pick the 2 to 4 factors most relevant to the question.
If the question is not about student performance, or none of the factors are relevant, return an empty list.
Reply with JSON only, in exactly this format:
{{"tasks": [{{"group_column": "lunch", "reason": "short reason"}}]}}"""

    for _ in range(2):
        text = ask_llm(prompt) or ""
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            continue
        try:
            plan = json.loads(match.group(0))
        except json.JSONDecodeError:
            continue

        raw_tasks = plan.get("tasks")
        if raw_tasks == []:
            raise OutOfScopeError("No relevant factors for this question.")

        tasks, seen = [], set()
        for t in raw_tasks or []:
            col = t.get("group_column") if isinstance(t, dict) else None
            if col in GROUP_COLUMNS and col not in seen:
                seen.add(col)
                tasks.append({"group_column": col, "reason": t.get("reason", "")})
        if tasks:
            return tasks

    raise PlanError("The model did not return a usable research plan.")


if __name__ == "__main__":
    question = "Does family background affect student exam performance?"
    for task in make_plan(question):
        print(task)
