"""Minimal test runner (no pytest required).

    python tests/run_tests.py

Discovers `test_*.py` in this directory, runs every `test_*` callable, and
reports pass/fail.  Exits non-zero if any test fails.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
import traceback

HERE = pathlib.Path(__file__).resolve().parent
SKILL = HERE.parent
sys.path.insert(0, str(SKILL / "scripts"))


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    files = sorted(HERE.glob("test_*.py"))
    n_pass = n_fail = 0
    for f in files:
        mod = load(f)
        for name in sorted(dir(mod)):
            if not name.startswith("test_"):
                continue
            fn = getattr(mod, name)
            if not callable(fn):
                continue
            try:
                fn()
                print(f"PASS  {f.name}::{name}")
                n_pass += 1
            except Exception as e:  # noqa: BLE001
                print(f"FAIL  {f.name}::{name}: {e}")
                traceback.print_exc()
                n_fail += 1
    print(f"\n{n_pass} passed, {n_fail} failed")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
