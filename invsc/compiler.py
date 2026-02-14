"""
Scala compilation step — calls scalac after INVSC approves the code.
"""

import subprocess
import shutil
import sys
from pathlib import Path

from .config import COLORS


def real_compile(source_path: Path, extra_args: list[str] | None = None) -> int:
    """
    Run the Scala compiler (scalac) on the source file.
    Returns the compiler's exit code.
    """
    c = COLORS
    ext = source_path.suffix.lower()

    if ext != ".scala":
        print(f"{c['warning']}invsc: warning: '{source_path.name}' is not a .scala file. "
              f"Invariant check passed but skipping compilation.{c['reset']}")
        return 0

    # Try scalac first, then scala (Scala 3 CLI can also compile)
    compiler = None
    for candidate in ["scalac", "scala"]:
        if shutil.which(candidate):
            compiler = candidate
            break

    if compiler is None:
        print(f"{c['warning']}invsc: note: neither 'scalac' nor 'scala' found in PATH. "
              f"Invariant check passed but cannot compile.{c['reset']}")
        print(f"{c['info']}  hint: install Scala via https://www.scala-lang.org/download/{c['reset']}")
        return 0

    # Build command
    if compiler == "scalac":
        # Classic scalac: scalac [-d outdir] file.scala
        out_dir = source_path.parent / "out"
        cmd = ["scalac", "-d", str(out_dir), str(source_path)]
    else:
        # Scala 3 CLI: scala compile file.scala
        cmd = ["scala", "compile", str(source_path)]

    if extra_args:
        cmd.extend(extra_args)

    print(f"{c['info']}[INVSC] Compiling: {' '.join(cmd)}{c['reset']}")

    try:
        # Create output directory if using scalac
        if compiler == "scalac":
            out_dir.mkdir(parents=True, exist_ok=True)

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        if result.returncode == 0:
            print(f"{c['alpha']}[INVSC] scalac finished successfully.{c['reset']}")
        else:
            print(f"{c['error']}[INVSC] scalac exited with code {result.returncode}.{c['reset']}")

        return result.returncode
    except subprocess.TimeoutExpired:
        print(f"{c['error']}invsc: error: compilation timed out (120s){c['reset']}")
        return 1
    except Exception as e:
        print(f"{c['error']}invsc: error: compilation failed: {e}{c['reset']}")
        return 1
