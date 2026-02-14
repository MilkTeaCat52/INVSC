"""
GPT client for INVSC — sends code to the OpenAI API for invariant checking.
"""

import json
from openai import OpenAI

from .config import OPENAI_API_KEY, OPENAI_MODEL, PROMPT_FILE


class GPTError(Exception):
    """Raised when GPT returns something we can't parse."""
    pass


def load_prompt_template() -> str:
    """Load the prompt template from disk."""
    return PROMPT_FILE.read_text(encoding="utf-8")


def build_prompt(source_code: str) -> str:
    """Build the full prompt by appending the source code to the template."""
    template = load_prompt_template()
    return template + source_code


def query_gpt(source_code: str, api_key: str | None = None, model: str | None = None) -> dict:
    """
    Send the source code to GPT for invariant checking.

    Returns a dict with keys: grade, summary, warnings
    """
    key = api_key or OPENAI_API_KEY
    mdl = model or OPENAI_MODEL

    if not key:
        raise GPTError(
            "No OpenAI API key found. Set OPENAI_API_KEY environment variable "
            "or pass --api-key flag."
        )

    client = OpenAI(api_key=key)

    prompt = build_prompt(source_code)

    response = client.chat.completions.create(
        model=mdl,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are INVSC, the INVariant Scala Compiler. "
                    "You respond ONLY in valid JSON. No markdown fences, no extra text."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content.strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError as e:
        raise GPTError(f"GPT returned invalid JSON: {e}\nRaw response:\n{raw}")

    # Validate expected keys
    if "grade" not in result:
        raise GPTError(f"GPT response missing 'grade' field:\n{raw}")
    if "warnings" not in result:
        result["warnings"] = []
    if "summary" not in result:
        result["summary"] = ""

    # Normalize grade
    result["grade"] = result["grade"].strip().lower()

    valid_grades = {"alpha", "alpha-beta", "beta", "gamma"}
    if result["grade"] not in valid_grades:
        raise GPTError(
            f"GPT returned unknown grade '{result['grade']}'. "
            f"Expected one of: {valid_grades}\nRaw response:\n{raw}"
        )

    return result
