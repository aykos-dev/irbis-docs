"""Repro of D{n} — re-records the bug video. Copy to qa/<slug>/bugs/D{n}_{name}/others/repro.py.
A retest copies it to others/repro__retest-YYYY-MM-DD.py and sets VARIANT = "retest-YYYY-MM-DD".

Run:   ~/.claude/venvs/qa/bin/python others/repro.py
Then, after looking at image/ and others/events.txt yourself:
       python3 scripts/qa/rec/rec.py render <bug folder> [--variant V] --verdict fail|fixed|not-fixed|blocked \
               --expected "…" --actual "…"
       python3 scripts/qa/rec/rec.py check <bug folder> [--variant V]   (Read the frame it names)
Captions: "Setup:" for state that is not part of the bug, "Step n:" with the SAME numbers as the bug's
Steps to Reproduce, "Observed:" neutral (no verdict — render adds Expected / Result after review).
Secrets: phone and OTP come from IRBIS_QA_PHONE / IRBIS_QA_OTP env vars, never written here.
"""
import os
import sys

FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))           # the bug folder
DOCS = os.path.abspath(os.path.join(FOLDER, *[".."] * 4))                       # irbis-docs
sys.path.insert(0, os.path.join(DOCS, "scripts", "qa", "rec"))
from drv import *  # noqa: E402,F403

VARIANT = None                                    # "retest-YYYY-MM-DD" for a retest
TITLE = "D{n} · {what goes wrong, one line}"

r = Rec(FOLDER, VARIANT)                          # noqa: F405
r.start()
try:
    r.step("Setup: {account state, permission, location — what is not part of the bug}")
    # fix = open_app_at(r, LAT, LNG, "label", 1)
    r.step("Step 1: …")
    # tap("spot.checkin-button", exact=True)
    r.shot("01_…")
    r.step("Observed: …")
finally:
    r.stop(TITLE)                                 # keeps the raw file; prints the render command
