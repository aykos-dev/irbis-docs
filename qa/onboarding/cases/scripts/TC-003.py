import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Meet Irbis: Get started opens Language; the chip shows EN and switches the language',
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC2 — Onb1 buttons and language chip',
 'env': 'Android · auto (adb)',
 'precondition': ['First run (reset link), app language English, guest'],
 'steps': ['Reset → Meet Irbis → check: onboarding.welcome',
           'Read the chip (onboarding.lang-chip)',
           'Tap the chip, choose Русский in the sheet',
           'Tap the chip, choose English',
           'Tap Get started'],
 'expected': ['Chip text is EN; texts "Get started" and "I already have an account" are on screen — UI tree + '
              'screenshot',
              'After picking Русский the chip text is RU and "Начать" shows without reopening the screen (≤ 2 s) — UI '
              'tree + screenshot',
              'After picking English the chip is EN again, "Get started" returns — UI tree',
              'Get started → onboarding.language is shown; event onboarding_step {step: language} — UI tree + QA '
              'events'],
 'focus': 'onboarding.lang-chip',
 'caption': {'expected': 'chip EN → RU'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.checkpoint("Meet Irbis shown", first_run_to("welcome"), "no onboarding.welcome")
    chip = find("onboarding.lang-chip", exact=True)
    shot = c.shot("1_welcome")
    txt = chip and (chip["text"] or chip["desc"])
    c.result(1, bool(chip and "EN" in (chip["text"] + chip["desc"])) and has("Get started") and has("I already have an account"), f"chip text/desc: {txt!r}", [shot])
    c.step(2, "Chip → Русский")
    tap("onboarding.lang-chip", exact=True)
    c.checkpoint("language sheet open", wait("profile.language-sheet", 5, exact=True), "no sheet")
    tap("profile.language-ru", exact=True)
    ok = wait("Начать", 3)
    chip = find("onboarding.lang-chip", exact=True)
    c.result(2, ok and bool(chip and "RU" in (chip["text"] + chip["desc"])), f"Начать={ok}, chip RU={bool(chip and 'RU' in (chip['text'] + chip['desc']))}", [c.shot("2_ru")])
    c.step(3, "Chip → English")
    wait_gone("profile.language-sheet", 3)
    tap("onboarding.lang-chip", exact=True); wait("profile.language-sheet", 5, exact=True)
    tap("profile.language-en", exact=True)
    ok = wait("Get started", 3); chip = find("onboarding.lang-chip", exact=True)
    c.result(3, ok and bool(chip and "EN" in (chip["text"] + chip["desc"])), f"Get started={ok}", [c.shot("3_en")])
    c.step(4, "Get started"); t0 = mark()
    tap("onboarding.get-started", exact=True)
    ok = wait("onboarding.language", 10, exact=True)
    ev = wait_event("onboarding_step", t0, 5, lambda p: p.get("step") == "language")
    c.result(4, ok and bool(ev), f"language screen={ok}, event={ev}", [c.shot("4_language")])
