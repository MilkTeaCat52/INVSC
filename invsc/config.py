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

# Oxford grading thresholds
# Alpha (α)   — First-class: excellent invariants, variants, and annotations
# Alpha-Beta  — Upper second: good but minor issues
# Beta (β)    — Lower second: passable but notable issues
# Gamma (γ)   — Third-class: poor annotations, does not compile
PASSING_GRADES = {"alpha", "alpha-beta"}
FAILING_GRADES = {"beta", "gamma"}

# Colors for terminal output
COLORS = {
    "alpha": "\033[92m",       # bright green
    "alpha-beta": "\033[93m",  # yellow
    "beta": "\033[91m",        # red
    "gamma": "\033[95m",       # magenta (shame)
    "reset": "\033[0m",
    "bold": "\033[1m",
    "warning": "\033[93m",
    "error": "\033[91m",
    "info": "\033[94m",
    "header": "\033[96m",
}
