#!/usr/bin/python3
"""run_tests.py — RUN greenery own pytest suite and print a parseable summary.

Invoked via the `/mayhem/greenery-tests` ELF launcher (NOT directly), so the verify-repo
sabotage oracle can neuter the launcher and prove the test oracle is behavioral.

greenery ships its tests as `greenery/*_test.py` modules (bound_test, charclass_test, conc_test,
fsm_test, multiplier_test, mult_test, parse_test, pattern_test, rxelems_test) — known-answer cases
asserting regex parsing, reduction, FSM equivalence, charclass algebra, multiplier arithmetic, and
Pattern set operations EXACTLY. A no-op / "exit(0)" / behavior-altering patch to greenery cannot
pass it.

It runs the real suite, writes a JUnit XML, parses the counts, and prints one line:

    RUNTESTS tests=<n> passed=<p> failed=<f> skipped=<s>

Exit 0 iff failed == 0. mayhem/test.sh parses that line into a CTRF report.
"""
from __future__ import annotations

import os
import sys
import xml.etree.ElementTree as ET

import pytest

SRC = os.environ.get("SRC", "/mayhem")
XML = "/tmp/greenery-junit.xml"
TESTS_DIR = "greenery"


def main() -> int:
    os.chdir(SRC)
    pytest.main(["-q", "-p", "no:cacheprovider", TESTS_DIR, "--junitxml", XML])

    root = ET.parse(XML).getroot()
    suites = root.findall("testsuite") or ([root] if root.tag == "testsuite" else [])
    if not suites:
        print("RUNTESTS tests=0 passed=0 failed=1 skipped=0")
        return 1

    tests = failed = skipped = 0
    for s in suites:
        tests += int(s.get("tests", 0))
        failed += int(s.get("failures", 0)) + int(s.get("errors", 0))
        skipped += int(s.get("skipped", 0))
    passed = tests - failed - skipped

    print(f"RUNTESTS tests={tests} passed={passed} failed={failed} skipped={skipped}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
