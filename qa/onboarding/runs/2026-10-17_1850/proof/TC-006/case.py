import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Language step: English preselected, a tap switches the app at once and Continue stays enabled',
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC3 — Onb2 language list',
 'env': 'Android · auto (adb)',
 'precondition': ['First run (reset link), app language English, guest'],
 'steps': ['Reset (app language English) → Language → check: onboarding.language',
           'Read selected state of the three rows and Continue',
           'Tap Русский, read the screen and Continue',
           "Tap O'zbekcha (uz row), read the screen"],
 'expected': ['onboarding.lang-en is selected, lang-uz and lang-ru are not; onboarding.continue is enabled — UI tree + '
              'screenshot',
              'After tapping Русский: lang-ru selected, progress "Шаг 1 из 4" within 2 s, event onboarding_language '
              '{locale: ru}, Continue enabled — UI tree + QA events',
              'After tapping uz: lang-uz selected, progress "1-qadam, jami 4", event onboarding_language {locale: uz} '
              '— UI tree + QA events'],
 'focus': 'onboarding.language',
 'caption': {'expected': 'language list'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.checkpoint("Language shown", first_run_to("language"), "no onboarding.language")
    s0 = c.shot("1_initial")
    c.result(1, selected("onboarding.lang-en") and not selected("onboarding.lang-ru") and not selected("onboarding.lang-uz") and enabled("onboarding.continue"),
             f"en={selected('onboarding.lang-en')} ru={selected('onboarding.lang-ru')} uz={selected('onboarding.lang-uz')} continue={enabled('onboarding.continue')}", [s0])
    c.step(3, "Tap Русский"); t0 = mark()
    tap("onboarding.lang-ru", exact=True)
    ok = wait("Шаг 1 из 4", 2); ev = wait_event("onboarding_language", t0, 3, lambda p: p.get("locale") == "ru")
    c.result(2, ok and selected("onboarding.lang-ru") and bool(ev) and enabled("onboarding.continue"), f"progress ru={ok}, event={ev}", [c.shot("2_ru")])
    c.step(4, "Tap uz"); t0 = mark()
    tap("onboarding.lang-uz", exact=True)
    ok = wait("1-qadam, jami 4", 2); ev = wait_event("onboarding_language", t0, 3, lambda p: p.get("locale") == "uz")
    c.result(3, ok and selected("onboarding.lang-uz") and bool(ev), f"progress uz={ok}, event={ev}", [c.shot("3_uz")])
    deep_link("irbis://debug/lang/en")
