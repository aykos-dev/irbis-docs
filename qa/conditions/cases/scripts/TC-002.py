import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Closure beats a mild forecast: Not now, admin text (uz fallback in English), worried Irbis',
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC7 + AC3 — closure → Not now, source closure, admin text in app locale with uz fallback, mascot',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, onboarding done',
                  'Peak PLACE with MILD forecast',
                  "Admin closure created via API: official, reason uz 'QA Yopiq: toshqin', no ru/en text"],
 'steps': ['Seed MILD, create the closure through the admin API',
           'Cold-start, open the place → check: card shown',
           'Read the card'],
 'expected': ["Chip reads 'Not now', title 'Not now this weekend', `place.condition-mascot` present — UI tree + "
              'screenshot',
              "`place.condition-updated` ends with '· closure' — UI tree",
              "`place.condition-reason.1` equals the uz text 'QA Yopiq: toshqin' (no en text → uz fallback) and "
              "there is no reason.2 and no 'Good weather' line — UI tree",
              'QA event `condition_viewed` {status: not_now, source: closure} — event log'],
 'caption': {'expected': "Chip reads 'Not now', title 'Not now this weekend', `place.condition-m"},
 'focus': 'place.condition'
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = slug0(); set_place(slug, hazards=[], season=["possible"] * 12)
    c.step(1, "seed + closure"); seed(slug); closure(slug, "QA Yopiq: toshqin")
    c.step(2, "open place")
    t0, tid, shot = view(c, slug, "1_card")
    c.checkpoint("condition card shown", tid == "place.condition", tid)
    c.step(3, "read card")
    c.result(1, text_in("place.condition-status") == "Not now" and tidtext("place.condition-title") == "Not now this weekend" and has("place.condition-mascot", exact=True), f"chip {text_in('place.condition-status')!r}, mascot {has('place.condition-mascot', exact=True)}", [shot])
    up = tidtext("place.condition-updated") or ""
    c.result(2, up.endswith("· closure"), f"updated {up!r}", [shot])
    r1 = tidtext("place.condition-reason.1") or ""
    c.result(3, r1 == "QA Yopiq: toshqin" and not has("place.condition-reason.2", exact=True) and not has("Good weather"), f"reason.1 {r1!r}", [shot])
    ev = viewed(t0, slug)
    c.result(4, bool(ev) and ev.get("status") == "not_now" and ev.get("source") == "closure", f"event {ev}")
