"""
Grade actions — the fun stuff that happens based on your grade.
"""

import subprocess
import sys
import time
import random
import webbrowser
from urllib.parse import quote

from .config import COLORS


# Email template for gammabeta / gamma shaming
SHAME_EMAIL_RECIPIENT = "gavinlowe2@gmail.com"
SHAME_EMAIL_SUBJECT = "INVSC Formal Complaint — Inadequate Loop Invariants"
SHAME_EMAIL_BODY = """\
Dear Gavin,

I am writing to formally bring to your attention a matter of grave academic concern.

The student in question submitted the following file for compilation:

    {filename}

Upon rigorous inspection by the Invariant Scala Compiler (INVSC), the code was awarded \
a grade of {grade}, which falls well below the minimum standard expected of any \
self-respecting member of this university.

The compiler's remarks were as follows:

    "{summary}"

The Examination Schools have been notified. I trust you will take appropriate action.

Yours in disappointment,
The Invariant Scala Compiler
"""


def action_alpha():
    """Reward for alpha: play a triumphant fanfare."""
    c = COLORS
    print(f"{c['alpha']}{c['bold']}")
    print("  ╔══════════════════════════════════════════════════╗")
    print("  ║                                                  ║")
    print("  ║   🏆  ALPHA — FIRST CLASS HONOURS  🏆           ║")
    print("  ║                                                  ║")
    print("  ║   The Examination Schools are pleased.           ║")
    print("  ║   You may proceed to All Souls.                  ║")
    print("  ║                                                  ║")
    print("  ╚══════════════════════════════════════════════════╝")
    print(f"{c['reset']}")

    _try_say("Congratulations. First class honours. The examiners are satisfied.")


def action_alpha_minus():
    """Near-perfect, trivial nitpicks."""
    c = COLORS
    print(f"{c['alpha(-)']}{c['bold']}")
    print("  ╔══════════════════════════════════════════════════╗")
    print("  ║                                                  ║")
    print("  ║   🎓  ALPHA MINUS — FIRST CLASS (near miss)  🎓 ║")
    print("  ║                                                  ║")
    print("  ║   The Examination Schools are nearly pleased.    ║")
    print("  ║   A minor blemish on an otherwise fine effort.   ║")
    print("  ║                                                  ║")
    print("  ╚══════════════════════════════════════════════════╝")
    print(f"{c['reset']}")

    _try_say("Alpha minus. Nearly flawless. One could quibble, but one shan't.")


def action_alphabeta():
    """Mild approval for alphabeta."""
    c = COLORS
    print(f"{c['alphabeta']}{c['bold']}")
    print("  ┌──────────────────────────────────────────────────┐")
    print("  │                                                  │")
    print("  │   📝  ALPHA-BETA — UPPER SECOND                 │")
    print("  │                                                  │")
    print("  │   Adequate. The compiler expected more,          │")
    print("  │   but will not send a stern letter.              │")
    print("  │                                                  │")
    print("  └──────────────────────────────────────────────────┘")
    print(f"{c['reset']}")

    _try_say("Alpha beta. Adequate, though one expected better from you.")


def action_betaalpha():
    """Borderline — not quite good enough."""
    c = COLORS
    print(f"{c['betaalpha']}{c['bold']}")
    print("  ┌──────────────────────────────────────────────────┐")
    print("  │                                                  │")
    print("  │   📋  BETA-ALPHA — UPPER SECOND (lower end)     │")
    print("  │                                                  │")
    print("  │   Showing promise, but not enough.               │")
    print("  │   The compiler sighs audibly.                    │")
    print("  │                                                  │")
    print("  │   COMPILATION DENIED.                            │")
    print("  │                                                  │")
    print("  └──────────────────────────────────────────────────┘")
    print(f"{c['reset']}")

    _try_say("Beta alpha. Showing promise, but not enough. Compilation denied.")


def action_beta():
    """Disappointment for beta — refuses to compile."""
    c = COLORS
    print(f"{c['beta']}{c['bold']}")
    print("  ┌──────────────────────────────────────────────────┐")
    print("  │                                                  │")
    print("  │   😤  BETA — LOWER SECOND                       │")
    print("  │                                                  │")
    print("  │   The compiler is writing a strongly worded      │")
    print("  │   letter to your Director of Studies.            │")
    print("  │                                                  │")
    print("  │   COMPILATION DENIED.                            │")
    print("  │                                                  │")
    print("  └──────────────────────────────────────────────────┘")
    print(f"{c['reset']}")

    _try_say("Beta. Lower second. This is beneath you. Compilation denied.")


def action_betagamma():
    """Even worse than beta."""
    c = COLORS
    print(f"{c['betagamma']}{c['bold']}")
    print("  ┌──────────────────────────────────────────────────┐")
    print("  │                                                  │")
    print("  │   😡  BETA-GAMMA — barely passable              │")
    print("  │                                                  │")
    print("  │   The compiler has given up on the letter        │")
    print("  │   and is now speaking directly to the Dean.      │")
    print("  │                                                  │")
    print("  │   COMPILATION DENIED.                            │")
    print("  │                                                  │")
    print("  └──────────────────────────────────────────────────┘")
    print(f"{c['reset']}")

    _try_say("Beta gamma. Barely passable. Compilation denied.")


def action_gammabeta(filename: str = "", summary: str = ""):
    """Very poor."""
    c = COLORS
    print(f"{c['gammabeta']}{c['bold']}")
    print("  ╔══════════════════════════════════════════════════╗")
    print("  ║                                                  ║")
    print("  ║   💀  GAMMA-BETA — approaching disgrace         ║")
    print("  ║                                                  ║")
    print("  ║   The Examination Schools are concerned.         ║")
    print("  ║   Your college is considering rustication.       ║")
    print("  ║                                                  ║")
    print("  ║   COMPILATION VIOLENTLY DENIED.                  ║")
    print("  ║                                                  ║")
    print("  ╚══════════════════════════════════════════════════╝")
    print(f"{c['reset']}")

    _try_say("Gamma beta. Approaching disgrace. Compilation violently denied.")
    _open_shame_email("gammabeta", filename, summary)


def action_gamma(filename: str = "", summary: str = ""):
    """Maximum shame for gamma."""
    c = COLORS
    print(f"{c['gamma']}{c['bold']}")
    print("  ╔══════════════════════════════════════════════════╗")
    print("  ║                                                  ║")
    print("  ║   💀  GAMMA — THIRD CLASS  💀                   ║")
    print("  ║                                                  ║")
    print("  ║   The Examination Schools are appalled.          ║")
    print("  ║   Your college has been notified.                ║")
    print("  ║   Please reconsider your life choices.           ║")
    print("  ║                                                  ║")
    print("  ║   COMPILATION VIOLENTLY DENIED.                  ║")
    print("  ║                                                  ║")
    print("  ╚══════════════════════════════════════════════════╝")
    print(f"{c['reset']}")

    # Dramatic pause
    print(f"\n{c['gamma']}  Deleting your code in 3...", end="", flush=True)
    time.sleep(1)
    print(" 2...", end="", flush=True)
    time.sleep(1)
    print(" 1...", end="", flush=True)
    time.sleep(1)
    print(f"\n  Just kidding. But you should feel bad.{c['reset']}\n")

    _try_say(
        "Gamma. Third class. The Examination Schools are appalled. "
        "Your college has been notified. Compilation violently denied."
    )
    _open_shame_email("gamma", filename, summary)


def run_grade_action(grade: str, filename: str = "", summary: str = ""):
    """Run the appropriate action for the given grade."""
    actions = {
        "alpha": action_alpha,
        "alpha(-)": action_alpha_minus,
        "alphabeta": action_alphabeta,
        "betaalpha": action_betaalpha,
        "beta": action_beta,
        "betagamma": action_betagamma,
        "gammabeta": action_gammabeta,
        "gamma": action_gamma,
    }

    action = actions.get(grade)
    if action:
        if grade in ("gammabeta", "gamma"):
            action(filename=filename, summary=summary)
        else:
            action()


def _open_shame_email(grade: str, filename: str, summary: str):
    """Open the default mail client with a pre-filled shame email."""
    body = SHAME_EMAIL_BODY.format(
        filename=filename or "<unknown>",
        grade=grade,
        summary=summary or "No further comment.",
    )
    mailto_url = (
        f"mailto:{quote(SHAME_EMAIL_RECIPIENT)}"
        f"?subject={quote(SHAME_EMAIL_SUBJECT)}"
        f"&body={quote(body)}"
    )
    try:
        webbrowser.open(mailto_url)
    except Exception:
        pass  # Silently fail if no mail client available


def _try_say(text: str):
    """Try to use macOS 'say' command for dramatic effect."""
    try:
        subprocess.Popen(
            ["say", "-v", "Daniel", text],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (FileNotFoundError, OSError):
        pass  # Not on macOS or 'say' not available
