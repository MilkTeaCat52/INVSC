"""
Configuration for INVSC.
"""

import os
from pathlib import Path

# OpenAI API config
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("INVSC_MODEL", "gpt-4o")

# Path to the prompt template
PROMPT_FILE = Path(__file__).parent / "prompt.txt"

# Oxford grading scale (ordered best to worst)
# alpha        — First-class: flawless
# alpha(-)     — First-class minus: near-flawless, trivial nitpicks
# alphabeta    — Upper second plus: good with minor issues
# betaalpha    — Upper second: decent but some problems
# beta         — Lower second: significant issues
# betagamma    — Lower second minus: poor effort
# gammabeta    — Third-class plus: very poor
# gamma        — Third-class: disgraceful

ALL_GRADES = [
    "alpha", "alpha(-)", "alphabeta", "betaalpha",
    "beta", "betagamma", "gammabeta", "gamma",
]
PASSING_GRADES = {"alpha", "alpha(-)", "alphabeta"}
FAILING_GRADES = {"betaalpha", "beta", "betagamma", "gammabeta", "gamma"}

# Colors for terminal output
COLORS = {
    "alpha": "\033[92m",         # bright green
    "alpha(-)": "\033[92m",      # bright green
    "alphabeta": "\033[93m",     # yellow
    "betaalpha": "\033[93m",     # yellow
    "beta": "\033[91m",          # red
    "betagamma": "\033[91m",     # red
    "gammabeta": "\033[95m",     # magenta
    "gamma": "\033[95m",         # magenta (shame)
    "reset": "\033[0m",
    "bold": "\033[1m",
    "warning": "\033[93m",
    "error": "\033[91m",
    "info": "\033[94m",
    "header": "\033[96m",
}
