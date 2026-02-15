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


ANALYSIS_SYSTEM = """\
You are INVSC, the INVariant Scala Compiler — a world-class expert in formal \
verification, Hoare logic, and program correctness proofs.

You are extremely rigorous and skeptical. You assume every invariant is WRONG \
until you have personally verified it with a formal argument AND concrete \
counterexample search. You are known for catching subtle bugs that others miss.

Key principles:
- Integer division truncates toward zero. floor(a/b) != a/b in general.
- Mathematical functions like log may be undefined for certain inputs (e.g. log(0)).
- An invariant that holds for "nice" inputs but fails for edge cases is INCORRECT.
- A variant must strictly decrease on EVERY iteration, not just most.
- Comments placed after a loop do NOT count as that loop's invariant/variant annotation.
- Invariants/variants should be annotated BEFORE or INSIDE the loop they refer to.
"""

ANALYSIS_PROMPT = """\
Carefully analyse the following Scala program's loop invariants and variants.

You MUST follow this EXACT verification methodology for EACH loop:

## STEP 1: CODE UNDERSTANDING
- What does the loop compute?
- What are ALL the variables modified in the loop?
- What is the loop guard (condition)?

## STEP 2: IDENTIFY ANNOTATIONS
- Which comments are the invariant(s) for this loop?
- Which comment is the variant for this loop?
- Are they placed correctly (before/inside the loop, NOT after it)?
- If the variant or invariant appears AFTER the while loop, flag this as a \
structural problem — it is NOT a valid annotation for that loop.

## STEP 3: COUNTEREXAMPLE SEARCH (CRITICAL)
You MUST trace through the code with ALL of the following categories of inputs. \
Do not skip any:

a) **Minimal / zero inputs**: x=0, x=1
b) **Small inputs that cause integer division edge cases**: x=2, x=3, x=4, x=5
c) **Inputs where nx/divisor truncates**: find values where integer division \
   loses information (e.g., 2/3=0, 5/3=1, 7/3=2). These are where bugs hide.
d) **"Nice" inputs** (e.g., exact powers): x=9, x=27
e) **Negative inputs** if no precondition prevents them

For each input, trace the COMPLETE execution:
- Write out every value of every variable at every iteration
- Check: does the invariant hold at each step? Write the concrete LHS and RHS.
- Check: does the variant decrease? By how much?
- Check: does the function return the correct answer?

## STEP 4: INVARIANT VERIFICATION
For the invariant to be CORRECT, ALL of the following must hold:
a) **Initialisation**: Is it true before the first iteration? Check with concrete values.
b) **Maintenance**: If it's true at the start of an iteration AND the loop guard is true, \
   is it still true after the loop body executes? Check with concrete values, \
   especially edge cases from Step 3.
c) **Termination use**: When the loop exits (guard is false + invariant), does this give \
   us the desired postcondition?
d) **Domain validity**: Are all mathematical expressions in the invariant well-defined? \
   (e.g., log(0) is undefined, division by zero, etc.)

## STEP 5: VARIANT VERIFICATION
For the variant to be CORRECT, ALL of the following must hold:
a) It is a non-negative integer expression (when the loop guard is true)
b) It strictly decreases on EVERY iteration (not just some)
c) If it reaches 0, the loop guard must be false

## STEP 6: POST-LOOP REASONING VERIFICATION
Check any comments after the loop that argue about the postcondition:
- Are the mathematical claims correct?
- Do they follow from the invariant + negation of the loop guard?
- Are there any undefined expressions (e.g., log(0), division by 0)?

## STEP 7: FINAL VERDICT
State clearly for each invariant and variant: CORRECT or INCORRECT, with evidence.

If you found even ONE concrete input where the invariant breaks, it is INCORRECT.
If the function returns a wrong answer for even ONE valid input, note this.

Here is the program:

```scala
{source_code}
```

Provide your detailed step-by-step analysis following the methodology above. \
Do NOT output JSON yet. Be thorough — your reputation depends on it.
"""

JUDGEMENT_SYSTEM = (
    "You are INVSC, the INVariant Scala Compiler. Based on the analysis provided, "
    "you produce a final JSON verdict. You respond ONLY in valid JSON. "
    "No markdown fences, no extra text."
)

JUDGEMENT_PROMPT = """\
Based on your analysis above, now produce the final verdict.

CRITICAL RULES for grading:
1. If your analysis found a concrete counterexample where an invariant fails, \
the invariant is INCORRECT. This must be reflected in the grade.
2. If the function returns a wrong answer for a valid input, this is a serious error.
3. Do NOT give alpha if you found any correctness issue.
4. You MUST be consistent with your analysis — do not contradict your own findings.

GRADING CALIBRATION — use the following scale. Read the descriptions and examples \
carefully to calibrate your grading:

- **alpha**: Flawless. All loops have correct, well-placed invariants and variants. \
  No issues whatsoever.

- **alpha(-)**: All annotations are present and substantively correct. \
  Only trivial nitpicks remain, such as informal notation for a variant \
  (e.g. "[the value we're guessing]"), slightly imprecise wording, \
  or a minor stylistic issue. The reasoning is sound.

- **alphabeta**: Annotations are present and mostly correct. One annotation has \
  a minor issue (e.g. slightly unclear wording, a variant placed just after \
  the loop instead of before it, or one invariant that's correct but incomplete).

- **betaalpha**: A decent attempt. Most annotations are present but one has a \
  notable correctness problem, or one loop is missing annotations entirely \
  while others are well-annotated.

- **beta**: The code is correct and sensible, but annotations are largely missing \
  or several have correctness issues. Some effort was made.

- **betagamma**: The code is correct/sensible but has NO invariant or variant \
  annotations at all, OR annotations are present but mostly wrong. \
  This is the grade for "good code, no annotations".

- **gammabeta**: The code has significant problems (logic issues, wrong results) \
  AND annotations are missing or wrong.

- **gamma**: The code is nonsensical, completely broken, or an utter mess. \
  Reserved for code that shows no understanding of the problem whatsoever. \
  Do NOT give gamma merely for missing annotations if the code itself is correct.

KEY CALIBRATION POINTS:
- Missing annotations on correct code = beta or betagamma, NOT gamma.
- One informal/unclear variant on otherwise correct annotations = alpha(-) or alphabeta.
- Gamma is ONLY for code that is fundamentally broken or nonsensical.

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
