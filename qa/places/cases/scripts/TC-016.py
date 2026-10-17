import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'No match shows the empty state; Reset filters clears everything',
 'priority': 'P0',
 'group': 'Core',
 'requirement': "AC5 — 'No places match these filters' + Reset filters",
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, location granted + mock at Tashkent centre',
                  'Explore loaded',
                  'A filter combination that the API says has 0 places (picked at run time)'],
 'steps': ['Find a combination: type Cave with difficulty 5 (verify total 0 with the API → check)',
           'Apply it in the app',
           'Tap explore.filter.reset'],
 'expected': ["explore.empty shows with the text 'No places match these filters' and the 'Reset filters' button; QA "
              'event explore_filters_applied count 0 — UI tree + screenshot + QA event',
              'After Reset: explore.empty is gone, header back to 71, Type / Difficulty / Distance chips show no '
              'value (defaults) — UI tree + screenshot'],
 'focus': 'explore.empty',
 'caption': {'expected': "explore.empty shows with the text 'No places match these fil"}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    st, d = places(types=["cave"], difficultyMin=5, difficultyMax=5)
    c.checkpoint("API says 0 places for cave + difficulty 5", st == 200 and d["total"] == 0, d.get("total"))
    c.checkpoint("Explore loaded", explore_ready(), "no list")
    t0 = mark()
    c.step(1, "apply cave + difficulty 5-5")
    apply_filters(types=["cave"], dmin=5, dmax=5)
    ev = wait_event("explore_filters_applied", t0, 10)
    wait("explore.empty", 8, exact=True)
    c.result(1, has("explore.empty", exact=True) and has("No places match these filters") and has("Reset filters") and bool(ev) and ev.get("count") == 0,
             f"empty shown {has('explore.empty', exact=True)}, event {ev}", [c.shot("1_empty")])
    c.step(2, "Reset filters"); tap("explore.filter.reset", exact=True)
    wait("explore.count", 10, exact=True)
    chips = [text_of(f"explore.filter.{k}") or "" for k in ("type", "difficulty", "distance")]
    c.result(2, not has("explore.empty", exact=True) and count_in_header() == 71 and not any(("·" in x or "–" in x or "≤" in x) for x in chips),
             f"header {count_in_header()}, chips {chips}", [c.shot("2_reset", "explore.sheet")])
