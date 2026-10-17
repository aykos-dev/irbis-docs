import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Type filter Peaks + Lakes: chip value, list and map refetch, QA event',
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC5 — type multi-select, active chip shows value',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, location granted + mock at Tashkent centre', 'Explore loaded with 71 places, no filter'],
 'steps': ['Tap the Type chip → check: explore.filter-sheet.type', 'Select Peaks and Lakes', 'Tap Apply'],
 'expected': ["Type chip text reads 'Peaks · Lakes' — UI tree + screenshot",
              "Header count equals the API total for types=peak,lake (45) and the first card slug equals the API's "
              'first item — UI tree + API response',
              'QA event explore_filters_applied {types: [peak, lake], count: 45} — QA event'],
 'focus': 'explore.filter.type',
 'caption': {'expected': "Type chip text reads 'Peaks · Lakes'"}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.checkpoint("Explore loaded", explore_ready(), "no list")
    t0 = mark()
    c.step(1, "open Type sheet"); tap("explore.filter.type", exact=True)
    c.checkpoint("Type sheet", wait("explore.filter-sheet.type", 5, exact=True), "no sheet")
    c.step(2, "select Peaks and Lakes")
    for t in ("peak", "lake"): tap(f"explore.filter-option.type-{t}", exact=True)
    c.step(3, "Apply"); tap("explore.filter.apply", exact=True)
    ev = wait_event("explore_filters_applied", t0, 10)
    time.sleep(0.5)
    chip = text_of("explore.filter.type") or ""
    c.result(1, "Peaks · Lakes" in chip, f"chip text {chip!r}", [c.shot("1_chip", "explore.filter.type")])
    st, d = places(limit=200, lat=TASHKENT[0], lng=TASHKENT[1], types=["peak", "lake"])
    first = d["items"][0]["slug"]
    c.result(2, count_in_header() == d["total"] == 45 and has("explore.card." + first, exact=True), f"header {count_in_header()}, api total {d['total']}, first card present {has('explore.card.' + first, exact=True)}", [c.shot("2_list", "explore.sheet")])
    c.result(3, bool(ev) and sorted(ev.get("types", [])) == ["lake", "peak"] and ev.get("count") == 45, f"event {ev}")
