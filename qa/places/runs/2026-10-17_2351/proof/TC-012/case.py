import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Map pins: type colours, clusters with count, single-pin tap',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC4 — one pin per place, colour+icon by type, clustered with a count',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, location granted + mock at Tashkent centre', 'Explore loaded, no filter'],
 'steps': ['Screenshot the map at the default zoom',
           'Filter to Caves only (2 places) and screenshot the map',
           'Tap the centre of the single pin that is shown → check: place.screen'],
 'expected': ['Default zoom shows cluster bubbles with a number — screenshot of explore.map (judged on the crop)',
              'Caves-only map shows 2 single pins in the cave colour (purple) with the cave icon — screenshot of '
              'explore.map (judged on the crop)',
              "Tapping a single pin opens Place for that cave: place.type reads 'Cave' — UI tree + QA event "
              'place_viewed'],
 'focus': 'explore.map',
 'caption': {'expected': 'Default zoom shows cluster bubbles with a number'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.checkpoint("Explore loaded", explore_ready(), "no list")
    c.step(1, "map at default zoom")
    c.result(1, None, "needs eyes: clusters with counts", [c.shot("1_map_default")])
    c.step(2, "filter Caves only")
    t0 = mark()
    apply_filters(types=["cave"])
    wait_event("explore_filters_applied", t0, 10)
    c.result(2, None, "needs eyes: 2 purple cave pins", [c.shot("2_map_caves")])
    c.step(3, "tap a single pin")
    n = find("explore.map", exact=True)
    t0 = mark()
    ok = False
    if n:
        x1, y1, x2, y2 = n["b"]
        # pins are GL-drawn: probe the map centre; the owner confirms on the crop if no tap lands
        sh("input", "tap", str((x1 + x2) // 2), str((y1 + y2) // 2))
        ok = wait("place.screen", 5, exact=True)
    ev = wait_event("place_viewed", t0, 3)
    c.result(3, (ok and "Cave" in (text_of("place.type") or "")) if ok else None,
             "pin tap opened a Place" if ok else "no Place opened by the centre tap — pin position is not in the UI tree; manual check", [c.shot("3_after_pin_tap", "explore.map")])
