"""
GPT client for INVSC — sends code to the OpenAI API for invariant checking.

Uses a two-pass approach:
  Pass 1 (Analysis): Ask GPT to trace through the code step-by-step,
                      understand the logic, and analyse each loop's invariants/variants.
  Pass 2 (Judgement): Given the analysis, produce the final structured JSON verdict.

This dramatically improves accuracy because GPT reasons about correctness
before committing to a grade, rather than jumping to conclusions.
"""

import json
from openai import OpenAI

from .config import OPENAI_API_KEY, OPENAI_MODEL, PROMPT_FILE, ALL_GRADES


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


ANALYSIS_SYSTEM = (
    "You are INVSC, the INVariant Scala Compiler — an expert in formal "
    "verification and Hoare logic. You must carefully and accurately analyse "
    "Scala code. Do NOT rush to judgement. Trace through the code mentally "
    "step by step."
)

ANALYSIS_PROMPT = """\
I need you to carefully analyse the following Scala program's loop invariants and variants.

For EACH loop in the program, do the following step-by-step:
1. Identify the loop and what it computes.
2. Trace through 2-3 iterations with concrete values to understand the behavior.
3. Read the annotated invariant. Check: is it true before the loop starts? \
Is it maintained by each iteration? Is it true when the loop exits?
4. Read the annotated variant. Check: is it a non-negative integer expression? \
Does it strictly decrease on every iteration? Does reaching 0 (or below) imply termination?
5. Conclude whether each invariant and variant is CORRECT or INCORRECT, with justification.

Be precise. Do not hallucinate issues. If an invariant uses informal notation \
(e.g. "[The actual number we're guessing]" to refer to an unknown value), \
interpret it charitably — it may be referring to a value that exists at runtime \
but isn't directly named in scope. Variants that depend on external unknowns \
are acceptable as long as they decrease.

Here is the program:

```scala
{source_code}
```

Provide your detailed step-by-step analysis. Do NOT output JSON yet.
"""

JUDGEMENT_SYSTEM = (
    "You are INVSC, the INVariant Scala Compiler. Based on the analysis provided, "
    "you produce a final JSON verdict. You respond ONLY in valid JSON. "
    "No markdown fences, no extra text."
)

JUDGEMENT_PROMPT = """\
Based on your analysis above, now produce the final verdict.

Use the following grading scale (Oxford system):
- alpha: Flawless. All loops have correct invariants and variants.
- alpha(-): Near-flawless, only trivial nitpicks (e.g. informal notation).
- alphabeta: Good but with minor issues in one or two annotations.
- betaalpha: Decent, but some invariants/variants have notable problems.
- beta: Significant missing or incorrect annotations.
- betagamma: Poor effort, many missing annotations.
- gammabeta: Very poor, barely any correct annotations.
- gamma: No effort on invariants/variants whatsoever. Disgraceful.

IMPORTANT: If your analysis concluded the invariants and variants are correct, \
you MUST grade alpha or alpha(-). Do NOT contradict your own analysis.

Respond in this JSON format ONLY:
{
  "grade": "alpha|alpha(-)|alphabeta|betaalpha|beta|betagamma|gammabeta|gamma",
  "summary": "A brief overall summary (1-2 sentences, in the tone of an Oxford tutor)",
  "warnings": [
    {
      "line": <line_number_or_null>,
      "severity": "warning|error",
      "message": "description of the issue"
    }
  ]
}
"""


def query_gpt(source_code: str, api_key: str | None = None, model: str | None = None) -> dict:
    """
    Send the source code to GPT for invariant checking using two-pass approach.

    Pass 1: Deep analysis with chain-of-thought reasoning
    Pass 2: Structured JSON judgement based on the analysis

    Returns a dict with keys: grade, summary, warnings, analysis
    """
    key = api_key or OPENAI_API_KEY
    mdl = model or OPENAI_MODEL

    if not key:
        raise GPTError(
            "No OpenAI API key found. Set OPENAI_API_KEY environment variable "
            "or pass --api-key flag."
        )

    client = OpenAI(api_key=key)

    # --- Pass 1: Analysis ---
    analysis_prompt = ANALYSIS_PROMPT.format(source_code=source_code)

    analysis_response = client.chat.completions.create(
        model=mdl,
        messages=[
            {"role": "system", "content": ANALYSIS_SYSTEM},
            {"role": "user", "content": analysis_prompt},
        ],
        temperature=0.2,
    )

    analysis = analysis_response.choices[0].message.content.strip()

    # --- Pass 2: Judgement (with analysis as context) ---
    judgement_response = client.chat.completions.create(
        model=mdl,
        messages=[
            {"role": "system", "content": JUDGEMENT_SYSTEM},
            {"role": "user", "content": analysis_prompt},
            {"role": "assistant", "content": analysis},
            {"role": "user", "content": JUDGEMENT_PROMPT},
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )

    raw = judgement_response.choices[0].message.content.strip()

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
    result["grade"] = result["grade"].strip().lower().replace(" ", "")

    # Handle common GPT variations
    grade_aliases = {
        "alpha-": "alpha(-)",
        "alpha_minus": "alpha(-)",
        "alpha_beta": "alphabeta",
        "alpha-beta": "alphabeta",
        "beta_alpha": "betaalpha",
        "beta-alpha": "betaalpha",
        "beta_gamma": "betagamma",
        "beta-gamma": "betagamma",
        "gamma_beta": "gammabeta",
        "gamma-beta": "gammabeta",
    }
    result["grade"] = grade_aliases.get(result["grade"], result["grade"])

    valid_grades = set(ALL_GRADES)
    if result["grade"] not in valid_grades:
        raise GPTError(
            f"GPT returned unknown grade '{result['grade']}'. "
            f"Expected one of: {valid_grades}\nRaw response:\n{raw}"
        )

    # Attach the analysis for debugging / verbose output
    result["analysis"] = analysis

    return result
