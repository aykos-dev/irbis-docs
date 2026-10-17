import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'First run: Splash for 1.5 s, then Meet Irbis',
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC1 — Splash 1.5 s then Meet Irbis',
 'env': 'Android · auto (adb)',
 'precondition': ['First run (reset link), app language English, guest'],
 'steps': ['Open irbis://debug/onboarding/reset and watch the QA events → check: onboarding.welcome within 10 s'],
 'expected': ['Event onboarding_step {step: splash} then {step: welcome}, 1.0–2.5 s apart (1.5 s nominal, adb/log '
              'jitter) — QA events (timestamps)',
              'onboarding.welcome is on screen and onboarding.splash is gone — UI tree + screenshot'],
 'focus': 'onboarding.welcome',
 'caption': {'expected': 'Meet Irbis after splash'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    deep_link("irbis://debug/lang/en"); time.sleep(1)
    t0 = mark()
    c.step(1, "Open the reset link")
    deep_link("irbis://debug/onboarding/reset")
    c.checkpoint("Meet Irbis shown within 10 s", wait("onboarding.welcome", 10, exact=True), "no onboarding.welcome")
    spl = wait_event("onboarding_step", t0, 5, lambda p: p.get("step") == "splash")
    wel = wait_event("onboarding_step", t0, 5, lambda p: p.get("step") == "welcome")
    from drv import events
    ts = {p.get("step"): t for t, n, p in events().since(t0, "onboarding_step")}
    dt = (ts.get("welcome", 0) - ts.get("splash", 0)) if "splash" in ts and "welcome" in ts else None
    c.result(1, dt is not None and 1.0 <= dt <= 2.5, f"splash→welcome {dt if dt is None else round(dt, 2)} s; events {sorted(ts)}")
    shot = c.shot("1_welcome")
    c.result(2, has("onboarding.welcome", exact=True) and not has("onboarding.splash", exact=True), "welcome shown, splash gone", [shot])
