import time
from drv import *  # noqa
from _std import screen, untranslated  # noqa

# Owner (2026-10-17): font-scale and layout/scroll checks removed from QA — translation only.
META = {"title": "Copy is translated", "priority": "P2", "group": "Standards",
        "requirement": "engineering-standards §12 — i18n", "env": "Android · auto (adb)",
        "precondition": ["screen reachable"],
        "steps": ["Russian — open the screen", "Uzbek — open the screen"],
        "expected": ["No English catalog string left on screen in Russian or Uzbek — UI tree"],
        "caption": {"expected": "translated"}}


def run(c):
    open_screen, root = screen(c)
    left = {}
    try:
        for n, lang in enumerate(("ru", "uz"), 1):
            c.step(n, f"{lang} — open the screen")
            deep_link(f"irbis://debug/lang/{lang}")  # in-app language (prefs.locale); lands on Debug
            c.checkpoint(f"screen opened ({lang})", open_screen(c), root)
            time.sleep(1)
            left[lang] = untranslated([nd["text"] for nd in nodes() if nd["text"]])
            c.shot(lang, focus=root)
        c.result(1, not any(left.values()), f"untranslated: {left}")
    finally:
        deep_link("irbis://debug/lang/en")
