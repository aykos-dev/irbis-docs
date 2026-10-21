import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Forecast older than 6 h keeps the last status and shows its age',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': "AC4 + AC7 — stale (> 6 h) keeps status; 'Updated 7 h ago'. The time is set in the DB, not waited",
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, onboarding done',
                  'Peak PLACE with a Caution forecast (Sun wind 40); place_conditions.computed_at set to 7 h ago in '
                  'the LOCAL DB'],
 'steps': ['Seed Caution with computed_at 7 h back', 'Cold-start, open the place → check: card shown'],
 'expected': ["Chip still reads 'Caution' (status kept) and `place.condition-updated` reads 'Updated 7 h ago · "
              "forecast' — UI tree + screenshot",
              'QA event `condition_viewed` {status: caution, ageMin between 415 and 425} — event log'],
 'caption': {'expected': "Chip still reads 'Caution' (status kept) and `place.condition-updated`"},
 'focus': 'place.condition'
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = slug0(); set_place(slug, hazards=[], season=["possible"] * 12)
    c.step(1, "seed stale"); seed(slug, sun={"wind_speed_10m_max": 40}, stale_h=7)
    c.step(2, "open place")
    t0, tid, shot = view(c, slug, "1_stale")
    c.checkpoint("condition card shown", tid == "place.condition", tid)
    up = tidtext("place.condition-updated") or ""
    c.result(1, text_in("place.condition-status") == "Caution" and up == "Updated 7 h ago · forecast", f"chip {text_in('place.condition-status')!r}, updated {up!r}", [shot])
    ev = viewed(t0, slug)
    c.result(2, bool(ev) and ev.get("status") == "caution" and 415 <= (ev.get("ageMin") or 0) <= 425, f"event {ev}")
