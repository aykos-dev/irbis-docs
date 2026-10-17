import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Difficulty range 1–3 and distance chips (≤ 50 / ≤ 100 / ≤ 150 / Any)',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC5 — difficulty range, distance options, default Any',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, location granted + mock at Tashkent centre', 'Explore loaded, no filter'],
 'steps': ['Note the Distance chip before touching it',
           'Difficulty 1 to 3 → Apply',
           'Distance ≤ 50 km → Apply; then ≤ 100; then ≤ 150; then Any (each Apply)'],
 'expected': ['Untouched Distance chip is the default state (value Any) — UI tree + screenshot',
              "Difficulty chip reads 'Difficulty 1–3'; header = API total for difficultyMin=1&difficultyMax=3; event "
              'explore_filters_applied {difficultyMin: 1, difficultyMax: 3} — UI tree + API response + QA event',
              "For each of 50 / 100 / 150 the chip reads '≤ N km' and the header equals the API total for "
              'maxDistanceKm=N (a place exactly on N km stays in); Any returns 71 — UI tree + API response + QA '
              'event maxKm'],
 'focus': 'explore.filter.distance',
 'caption': {'expected': 'Untouched Distance chip is the default state (value Any)'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.checkpoint("Explore loaded", explore_ready(), "no list")
    c.result(1, "≤" not in (text_of("explore.filter.distance") or ""), f"distance chip {text_of('explore.filter.distance')!r}", [c.shot("1_default", "explore.filter.distance")])
    t0 = mark()
    c.step(1, "difficulty 1-3"); apply_filters(dmin=1, dmax=3)
    ev = wait_event("explore_filters_applied", t0, 10)
    st, d = places(limit=200, lat=TASHKENT[0], lng=TASHKENT[1], difficultyMin=1, difficultyMax=3)
    chip = text_of("explore.filter.difficulty") or ""
    c.result(2, "Difficulty 1–3" in chip and count_in_header() == d["total"] and bool(ev) and ev.get("difficultyMin") == 1 and ev.get("difficultyMax") == 3,
             f"chip {chip!r}, header {count_in_header()}, api {d['total']}, event {ev}", [c.shot("2_diff", "explore.filter.difficulty")])
    obs, ok = [], True
    for km in (50, 100, 150, 0):
        t0 = mark()
        c.step(3, f"distance {km or 'Any'}")
        apply_filters(km=km)
        ev = wait_event("explore_filters_applied", t0, 10)
        s, dd = places(limit=200, lat=TASHKENT[0], lng=TASHKENT[1], difficultyMin=1, difficultyMax=3, **({"maxDistanceKm": km} if km else {}))
        chip = text_of("explore.filter.distance") or ""
        good = (km == 0 or f"≤ {km} km" in chip) and count_in_header() == dd["total"] and bool(ev)
        ok &= good
        obs.append(f"{km or 'Any'}: chip {chip!r}, header {count_in_header()}, api {dd['total']}, event maxKm {ev and ev.get('maxKm')}")
    c.result(3, ok, "; ".join(obs), [c.shot("3_distance", "explore.filter.distance")])
