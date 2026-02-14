"""
Main CLI entry point for INVSC — INVariant Scala Compiler.
"""

import argparse
import sys
from pathlib import Path

from .config import COLORS, PASSING_GRADES
from .gpt_client import query_gpt, GPTError
from .formatter import format_full_output, print_banner, print_phase
from .compiler import real_compile
from .actions import run_grade_action


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="invsc",
        description="INVSC — INVariant Scala Compiler. "
                    "The Scala compiler that judges your code like an Oxford tutor.",
        epilog="Your code is only as good as your invariants.",
    )

    parser.add_argument(
        "source",
        type=str,
        help="Scala source file to compile (e.g., Main.scala)",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="OpenAI API key (or set OPENAI_API_KEY env var)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="OpenAI model to use (default: gpt-4o)",
    )
    parser.add_argument(
        "--no-compile",
        action="store_true",
        help="Only run invariant checking, skip actual Scala compilation",
    )
    parser.add_argument(
        "--no-action",
        action="store_true",
        help="Skip grade actions (no sound, no drama)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON result instead of formatted output",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force compilation even if grade is below alpha-beta (live dangerously)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show GPT's detailed analysis (chain-of-thought reasoning)",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    c = COLORS

    source_path = Path(args.source)

    # Check file exists
    if not source_path.exists():
        print(f"{c['error']}invsc: error: no such file: '{args.source}'{c['reset']}", file=sys.stderr)
        sys.exit(1)

    if not source_path.is_file():
        print(f"{c['error']}invsc: error: '{args.source}' is not a file{c['reset']}", file=sys.stderr)
        sys.exit(1)

    # Check it's a Scala file
    if source_path.suffix.lower() != ".scala":
        print(f"{c['warning']}invsc: warning: '{args.source}' is not a .scala file{c['reset']}", file=sys.stderr)

    # Read source code
    try:
        source_code = source_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"{c['error']}invsc: error: cannot read '{args.source}': {e}{c['reset']}", file=sys.stderr)
        sys.exit(1)

    if not source_code.strip():
        print(f"{c['error']}invsc: error: '{args.source}' is empty{c['reset']}", file=sys.stderr)
        sys.exit(1)

    # Query GPT
    try:
        result = query_gpt(source_code, api_key=args.api_key, model=args.model)
    except GPTError as e:
        print(f"{c['error']}invsc: error: {e}{c['reset']}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"{c['error']}invsc: internal error: {e}{c['reset']}", file=sys.stderr)
        sys.exit(1)

    # Output results
    if args.json:
        import json
        print(json.dumps(result, indent=2))
        exit_code = 0 if result["grade"] in PASSING_GRADES else 1
    else:
        # Show verbose analysis if requested
        if args.verbose and "analysis" in result:
            print(f"{c['info']}{'─' * 60}{c['reset']}")
            print(f"{c['bold']}GPT Analysis (chain-of-thought):{c['reset']}")
            print(f"{c['info']}{'─' * 60}{c['reset']}")
            print(result["analysis"])
            print(f"{c['info']}{'─' * 60}{c['reset']}")
            print()

        exit_code = format_full_output(result, args.source)

    # Grade actions
    if not args.no_action:
        run_grade_action(result["grade"])

    # Actual Scala compilation
    grade = result["grade"]
    should_compile = grade in PASSING_GRADES or args.force

    if args.force and grade not in PASSING_GRADES:
        print(f"\n{c['warning']}invsc: warning: --force flag used. "
              f"Compiling despite shameful grade. Your tutor will hear about this.{c['reset']}")

    if should_compile and not args.no_compile:
        print()
        compile_exit = real_compile(source_path)
        if compile_exit != 0:
            exit_code = compile_exit

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
