"""
Output formatter for INVSC — makes compiler output look authentic.
"""

import sys

from .config import COLORS, PASSING_GRADES


BANNER = r"""
  ___  _   _  __     __  ____    ____ 
 |_ _|| \ | | \ \   / / / ___|  / ___|
  | | |  \| |  \ \ / /  \___ \ | |    
  | | | |\  |   \ V /    ___) || |___ 
 |___||_| \_|    \_/    |____/  \____|

  INVariant Scala Compiler v0.1.0
  "Your code is only as good as your invariants."
"""

GRADE_MESSAGES = {
    "alpha": [
        "🎓 Grade: α (Alpha) — First Class Honours",
        "Your tutor would be proud. Compilation successful.",
    ],
    "alpha(-)": [
        "🎓 Grade: α⁻ (Alpha Minus) — First Class Honours (minor blemish)",
        "Nearly flawless. One could quibble, but one shan't. Compilation successful.",
    ],
    "alphabeta": [
        "📝 Grade: αβ (Alpha-Beta) — Upper Second",
        "Acceptable, though one expected better. Compilation successful.",
    ],
    "betaalpha": [
        "📋 Grade: βα (Beta-Alpha) — Upper Second (lower end)",
        "Showing promise, but not enough. COMPILATION REFUSED.",
    ],
    "beta": [
        "😤 Grade: β (Beta) — Lower Second",
        "This is beneath you. COMPILATION REFUSED.",
    ],
    "betagamma": [
        "😡 Grade: βγ (Beta-Gamma) — Lower Second (barely)",
        "Your tutor is composing a strongly worded letter. COMPILATION REFUSED.",
    ],
    "gammabeta": [
        "💀 Grade: γβ (Gamma-Beta) — Third Class (upper end)",
        "Were you even trying? COMPILATION VIOLENTLY REFUSED.",
    ],
    "gamma": [
        "💀 Grade: γ (Gamma) — Third Class",
        "Were you even trying? This is an embarrassment to the university.",
        "COMPILATION VIOLENTLY REFUSED.",
    ],
}


def print_banner():
    """Print the INVSC banner."""
    c = COLORS
    print(f"{c['header']}{BANNER}{c['reset']}")


def print_phase(phase: str):
    """Print a compilation phase."""
    c = COLORS
    print(f"{c['info']}{c['bold']}[INVSC]{c['reset']}{c['info']} {phase}{c['reset']}")


def print_warnings(warnings: list[dict], filename: str):
    """Print warnings in scalac-style format."""
    c = COLORS
    for w in warnings:
        severity = w.get("severity", "warning")
        line = w.get("line")
        msg = w.get("message", "unknown issue")

        if severity == "error":
            color = c["error"]
            tag = "error"
        else:
            color = c["warning"]
            tag = "warning"

        loc = f"{filename}:{line}" if line else filename
        print(f"{c['bold']}{loc}: {color}{tag}: {c['reset']}{msg}")


def print_summary(summary: str):
    """Print the tutor's summary."""
    c = COLORS
    if summary:
        print()
        print(f"{c['bold']}Tutor's remarks:{c['reset']} {summary}")


def print_grade(grade: str):
    """Print the grade with appropriate drama."""
    c = COLORS
    color = c.get(grade, c["reset"])
    messages = GRADE_MESSAGES.get(grade, [f"Grade: {grade}"])

    print()
    print(f"{'─' * 60}")
    for msg in messages:
        print(f"{color}{c['bold']}  {msg}{c['reset']}")
    print(f"{'─' * 60}")
    print()


def print_compilation_result(grade: str, filename: str):
    """Print the final compilation result."""
    c = COLORS
    if grade in PASSING_GRADES:
        print(f"{c['bold']}Compiling {filename}...{c['reset']}")
        print(f"{c['alpha']}✓ Compilation successful.{c['reset']}")
    else:
        print(f"{c['bold']}Compiling {filename}...{c['reset']}")
        print(f"{c['error']}✗ Compilation FAILED. Grade too low.{c['reset']}")
        print(
            f"{c['error']}  invsc: error: "
            f"code does not meet minimum invariant standards (need αβ or above){c['reset']}"
        )


def format_full_output(result: dict, filename: str) -> int:
    """
    Format and print the full INVSC output.
    Returns exit code (0 for pass, 1 for fail).
    """
    print_banner()
    print_phase(f"Analysing {filename}...")
    print_phase("Checking loop invariants and variants...")
    print_phase("Consulting the Oxford examiners board...")
    print()

    # Warnings
    warnings = result.get("warnings", [])
    if warnings:
        print_warnings(warnings, filename)
    else:
        print(f"{COLORS['alpha']}No warnings. Immaculate.{COLORS['reset']}")

    # Summary
    print_summary(result.get("summary", ""))

    # Grade
    grade = result["grade"]
    print_grade(grade)

    # Compile result
    print_compilation_result(grade, filename)

    if grade in PASSING_GRADES:
        return 0
    else:
        return 1
