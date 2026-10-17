import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Experience: nothing preselected, Continue disabled until a pick, quiz card is static',
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC4 — Onb3',
 'env': 'Android · auto (adb)',
 'precondition': ['First run (reset link), app language English, guest'],
 'steps': ['Reset → Language → Continue → check: onboarding.experience',
           'Read tiles and Continue',
           'Tap the orange quiz card text',
           'Tap Weekend hiker',
           'Tap Experienced'],
 'expected': ['onboarding.exp-beginner / exp-weekend / exp-experienced all unselected and onboarding.continue disabled '
              '— UI tree + screenshot',
              'Quiz card text "Everyone starts as a Wanderer." is on screen; tapping it changes nothing (still on '
              'onboarding.experience, Continue still disabled, no event) — UI tree',
              'After Weekend hiker: it is selected, the other two are not, Continue enabled — UI tree',
              'After Experienced: only exp-experienced selected (single choice), Continue enabled — UI tree'],
 'focus': 'onboarding.experience',
 'caption': {'expected': 'three tiles'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.checkpoint("Experience shown", first_run_to("experience"), "no onboarding.experience")
    ids = ["onboarding.exp-beginner", "onboarding.exp-weekend", "onboarding.exp-experienced"]
    c.result(1, not any(selected(i) for i in ids) and all(has(i, exact=True) for i in ids) and not enabled("onboarding.continue"),
             f"selected {[selected(i) for i in ids]}, continue enabled={enabled('onboarding.continue')}", [c.shot("1_initial")])
    c.step(3, "Tap the quiz card"); t0 = mark()
    card = find("Everyone starts as a Wanderer.")
    if card: tap("Everyone starts as a Wanderer.")
    time.sleep(1)
    c.result(2, bool(card) and has("onboarding.experience", exact=True) and not enabled("onboarding.continue") and not events().since(t0, "onboarding_step"),
             f"card found={bool(card)}", [c.shot("2_card")])
    c.step(4, "Weekend hiker"); tap(ids[1], exact=True)
    c.result(3, selected(ids[1]) and not selected(ids[0]) and not selected(ids[2]) and enabled("onboarding.continue"), f"selected {[selected(i) for i in ids]}", [c.shot("3_weekend")])
    c.step(5, "Experienced"); tap(ids[2], exact=True)
    c.result(4, selected(ids[2]) and not selected(ids[1]) and enabled("onboarding.continue"), f"selected {[selected(i) for i in ids]}", [c.shot("4_experienced")])
