import os
import re
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

GROUP_COLUMNS = [
    "gender",
    "race/ethnicity",
    "parental level of education",
    "lunch",
    "test preparation course",
]


def ask_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def make_plan(question):
    prompt = f"""You are a research planner for an education dataset of student exam scores.
Available factors: {GROUP_COLUMNS}
Research question: {question}

Pick the 2 to 4 factors most relevant to the question.
Reply with JSON only, in exactly this format:
{{"tasks": [{{"group_column": "lunch", "reason": "short reason"}}]}}"""

    text = ask_llm(prompt)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    plan = json.loads(match.group(0))
    return [t for t in plan["tasks"] if t["group_column"] in GROUP_COLUMNS]


if __name__ == "__main__":
    question = "Does family background affect student exam performance?"
    for task in make_plan(question):
        print(task)