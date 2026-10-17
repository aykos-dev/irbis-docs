import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Safety opens its empty state; Language opens the language sheet",
 "priority": "P2",
 "group": "Supplementary",
 "requirement": "AC2 — Safety empty state, Language row",
 "env": "Android · auto (adb)",
 "precondition": [
  "Guest Profile open"
 ],
 "steps": [
  "Tap Safety & SOS → check: empty.safety within 5 s",
  "Back; tap Language → check: profile.language-sheet"
 ],
 "expected": [
  "empty.safety visible after tapping profile.safety — UI tree + screenshot",
  "profile.language-sheet lists profile.language-en, profile.language-ru, profile.language-uz — UI tree"
 ],
 "focus": "profile.guest",
 "caption": {
  "expected": "Safety empty state and language sheet"
 }
}


def run(c):
    c.pre("guest Profile")
    c.checkpoint("guest Profile shown", ensure_guest(), "no profile.guest")
    c.step(1, "Tap Safety & SOS")
    tap("profile.safety", exact=True)
    ok1 = wait("empty.safety", 5, exact=True)
    s1 = c.shot("1_safety", focus="empty.safety")
    c.result(1, ok1, "empty.safety shown" if ok1 else "not shown", [s1])
    back()
    c.checkpoint("back on guest Profile", wait("profile.guest", 5, exact=True), "no profile.guest")
    c.step(2, "Tap Language")
    tap("profile.language", exact=True)
    ok2 = wait("profile.language-sheet", 5, exact=True)
    opts = [has(f"profile.language-{k}", exact=True) for k in ("en", "ru", "uz")]
    s2 = c.shot("2_language", focus="profile.language-sheet")
    c.result(2, ok2 and all(opts), f"sheet {ok2}, options en/ru/uz {opts}", [s2])
    back()
