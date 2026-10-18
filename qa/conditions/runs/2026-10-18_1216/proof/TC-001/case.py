import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Place shows the Go card for a mild weekend: chip, title, age + source, good-weather reason',
 'priority': 'P0',
 'group': 'Core',
 'requirement': "AC7 + AC2 — Go this weekend, 'Updated {relative} · {source}', GOOD_WEATHER line",
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, onboarding done',
                  'Peak PLACE, forecast fixture MILD for the weekend window (24°/12°, wind 10 km/h, rain 10 %, code '
                  '1), no closure/override, season not closed'],
 'steps': ['Seed the MILD forecast and recompute the place',
           'Cold-start the app and open the place (deep link) → check: a condition card testID shows within 15 s',
           'Read the card'],
 'expected': ["Chip `place.condition-status` reads 'Go' and `place.condition-title` reads 'Go this weekend' — UI "
              'tree + screenshot',
              "`place.condition-updated` matches 'Updated just now · forecast' (or 'N min ago') — UI tree",
              "`place.condition-reason.1` matches 'Good weather on Saturday|Sunday, wind up to 10 km/h' and there is "
              'no reason.2 and no worried Irbis (`place.condition-mascot`) — UI tree',
              'QA event `condition_viewed` {slug, status: go, source: forecast, ageMin ≤ 2} — event log'],
 'caption': {'expected': "Chip `place.condition-status` reads 'Go' and `place.condition-title` r"},
 'focus': 'place.condition'
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = slug0(); set_place(slug, hazards=[], season=["possible"] * 12)
    c.step(1, "seed MILD"); seed(slug)
    c.step(2, "open place")
    t0, tid, shot = view(c, slug, "1_card")
    c.checkpoint("condition card shown", tid == "place.condition", tid)
    c.step(3, "read card")
    import re
    c.result(1, text_in("place.condition-status") == "Go" and tidtext("place.condition-title") == "Go this weekend", f"chip {text_in('place.condition-status')!r}, title {tidtext('place.condition-title')!r}", [shot])
    up = tidtext("place.condition-updated") or ""
    c.result(2, re.fullmatch(r"Updated (just now|\d+ min ago) · forecast", up) is not None, f"updated {up!r}", [shot])
    r1 = tidtext("place.condition-reason.1") or ""
    c.result(3, re.fullmatch(r"Good weather on (Saturday|Sunday), wind up to 10 km/h", r1) is not None and not has("place.condition-reason.2", exact=True) and not has("place.condition-mascot", exact=True), f"reason.1 {r1!r}, reason.2 {has('place.condition-reason.2', exact=True)}, mascot {has('place.condition-mascot', exact=True)}", [shot])
    ev = viewed(t0, slug)
    c.result(4, bool(ev) and ev.get("status") == "go" and ev.get("source") == "forecast" and (ev.get("ageMin") or 0) <= 2, f"event {ev}")
