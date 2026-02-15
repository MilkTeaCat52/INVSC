"""
Scala compilation step — calls scalac after INVSC approves the code.
"""

import subprocess
import shutil
import sys
from pathlib import Path
import os

from .config import COLORS


def real_compile(source_path: Path, out_dir:Path | None = None , compiler:str | None = None) -> int:
    """
    Run the Scala compiler (fsc or scalac) on the source file.
    Returns the compiler's exit code.
    """
    c = COLORS
    ext = source_path.suffix.lower()

    if ext != ".scala":
        print(f"{c['warning']}invsc: warning: '{source_path.name}' is not a .scala file. "
              f"Invariant check passed but skipping compilation of {source_path.name}.{c['reset']}")
        return 0
    
    if compiler is not None:
        # Check whether compiler is on path
        if shutil.which(compiler):
            # Check whether compiler is a valid Scala compiler
            if compiler in ["fsc", "scalac"]:
                print(f"{c['info']}[INVSC] Using {compiler} for compilation.{c['reset']}")
            else:
                print(f"{c['warning']}invsc: note: {compiler} was not recognised as a valid Scala compiler. Falling back on default compilers.{c['reset']}")
                compiler = None
        else:
            print(f"{c['warning']}invsc: note: {compiler} was not found in PATH. Falling back on default compilers.{c['reset']}")
            compiler = None

    if compiler is None:
        # Try fsc then scalac
        for candidate in ["fsc", "scalac"]:
            if shutil.which(candidate):
                compiler = candidate
                print(f"{c['info']}[INVSC] Compiler not specified. Defaulting to {compiler} for compilation.{c['reset']}")
                break

    if compiler is None:
        print(f"{c['warning']}invsc: note: none of 'fsc' or 'scalac' found in PATH. "
              f"Invariant check passed but cannot compile {source_path.name}.{c['reset']}")
        print(f"{c['info']}  hint: install Scala via https://www.scala-lang.org/download/{c['reset']}")
        return 0

    if out_dir is None:
        print(f"{c['info']}[INVSC] Output directory not specified. Defaulting to parent of source file.{c['reset']}")
        out_dir = source_path.parent

    # Build command
    if compiler == "fsc":
        # Fast Scala Compiler: fsc [-d outdir] file.scala      
        cmd = ["fsc", "-d", str(out_dir), str(source_path)]  
    elif compiler == "scalac":
        # Scala Compiler: scalac [-d outdir] file.scala
        cmd = ["scalac", "-d", str(out_dir), str(source_path)]


    print(f"{c['info']}[INVSC] Compiling: {' '.join(cmd)}{c['reset']}")

    try:
        # Create output directory if it doesn't exist
        out_dir.mkdir(parents=True, exist_ok=True)

        windows = os.name == "nt"

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, shell=windows)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        if result.returncode == 0:
            print(f"{c['alpha']}[INVSC] {compiler} finished successfully.{c['reset']}")
        else:
            print(f"{c['error']}[INVSC] {compiler} exited with code {result.returncode}.{c['reset']}")

        return result.returncode
    except subprocess.TimeoutExpired:
        print(f"{c['error']}invsc: error: compilation timed out (120s){c['reset']}")
        return 1
    except Exception as e:
        print(f"{c['error']}invsc: error: compilation failed: {e}{c['reset']}")
        return 1


def real_run(source_path: Path, extra_args: list[str] | None = None) -> int:
    """
    Run the Scala command on the source file.
    Returns the compiler's exit code.
    """
    c = COLORS
    ext = source_path.suffix.lower()

    if ext != ".scala":
        print(f"{c['warning']}invsc: warning: '{source_path.name}' is not a .scala file. "
              f"Invariant check passed but skipping compilation of {source_path.name}.{c['reset']}")
        return 0
    

    # Check if scala is on path
    if shutil.which("scala"):
        # Scala 3 CLI: scala compile file.scala
        cmd = ["scala", str(source_path)]
    else:
        print(f"{c['warning']}invsc: note: 'scala' was not found in PATH. "
              f"Invariant check passed but cannot compile {source_path.name}.{c['reset']}")
        print(f"{c['info']}  hint: install Scala via https://www.scala-lang.org/download/{c['reset']}")        
        return 0

    if extra_args:
        cmd.extend(extra_args)

    print(f"{c['info']}[INVSC] Compiling: {' '.join(cmd)}{c['reset']}")

    try:
        windows = os.name == "nt"

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, shell = windows)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        if result.returncode == 0:
            print(f"{c['alpha']}[INVSC] scala finished successfully.{c['reset']}")
        else:
            print(f"{c['error']}[INVSC] scala exited with code {result.returncode}.{c['reset']}")

        return result.returncode
    except subprocess.TimeoutExpired:
        print(f"{c['error']}invsc: error: compilation timed out (120s){c['reset']}")
        return 1
    except Exception as e:
        print(f"{c['error']}invsc: error: compilation failed: {e}{c['reset']}")
        return 1

