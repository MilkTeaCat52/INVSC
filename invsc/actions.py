"""
Grade actions — the fun stuff that happens based on your grade.
"""

import subprocess
import sys
import time
import random

from .config import COLORS


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


def action_alpha_beta():
    """Mild approval for alpha-beta."""
    c = COLORS
    print(f"{c['alpha-beta']}{c['bold']}")
    print("  ┌──────────────────────────────────────────────────┐")
    print("  │                                                  │")
    print("  │   📝  ALPHA-BETA — UPPER SECOND                 │")
    print("  │                                                  │")
    print("  │   Adequate. Your tutor expected more,            │")
    print("  │   but will not send a stern letter.              │")
    print("  │                                                  │")
    print("  └──────────────────────────────────────────────────┘")
    print(f"{c['reset']}")

    _try_say("Upper second. Adequate, though one expected better from you.")


def action_beta():
    """Disappointment for beta — refuses to compile."""
    c = COLORS
    print(f"{c['beta']}{c['bold']}")
    print("  ┌──────────────────────────────────────────────────┐")
    print("  │                                                  │")
    print("  │   😤  BETA — LOWER SECOND                       │")
    print("  │                                                  │")
    print("  │   Your tutor is writing a strongly worded        │")
    print("  │   letter to your Director of Studies.            │")
    print("  │                                                  │")
    print("  │   COMPILATION DENIED.                            │")
    print("  │                                                  │")
    print("  └──────────────────────────────────────────────────┘")
    print(f"{c['reset']}")

    _try_say("Beta. Lower second. This is beneath you. Compilation denied.")


def action_gamma():
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


def run_grade_action(grade: str):
    """Run the appropriate action for the given grade."""
    actions = {
        "alpha": action_alpha,
        "alpha-beta": action_alpha_beta,
        "beta": action_beta,
        "gamma": action_gamma,
    }

    action = actions.get(grade)
    if action:
        action()


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
