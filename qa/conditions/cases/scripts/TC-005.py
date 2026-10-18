import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Hazards now lists each place hazard with its level (Raised / Open)',
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC7 + AC2 — hazard levels: rain 12 mm → mudslide/flood Raised, road Open',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, onboarding done',
                  'Peak PLACE with hazards mudslide, flood, road; season open',
                  'Forecast: window day Sun rain 12 mm (≥10 → Caution, < 30), everything else MILD'],
 'steps': ['set_place hazards, seed the fixture',
           "Cold-start, open the place, scroll to 'Hazards now' → check: `place.hazards-now` shown",
           'Read the three rows'],
 'expected': ["`place.hazard.mudslide` and `place.hazard.flood` exist and their `.level` reads 'Raised' — UI tree + "
              'screenshot',
              "`place.hazard.road` exists and its `.level` reads 'Open' — UI tree",
              'The three levels equal the API `GET /v1/places/{id}/condition` hazards (raised, raised, open) and no '
              'row for a hazard the place lacks (`place.hazard.heat`) — API + UI tree'],
 'caption': {'expected': '`place.hazard.mudslide` and `place.hazard.flood` exist and their `.lev'},
 'focus': 'place.hazards-now'
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = slug0(); set_place(slug, hazards=["mudslide", "flood", "road"], season=["possible"] * 12)
    c.step(1, "seed"); seed(slug, sun={"precipitation_sum": 12})
    c.step(2, "open place")
    t0, tid, _ = view(c, slug, "0_open")
    c.checkpoint("hazards list shown", reveal("place.hazards-now"), "no place.hazards-now")
    shot = c.shot("1_hazards", "place.hazards-now")
    c.step(3, "read rows")
    lv = {h: tidtext(f"place.hazard.{h}.level") for h in ("mudslide", "flood", "road")}
    c.result(1, lv["mudslide"] == "Raised" and lv["flood"] == "Raised", f"levels {lv}", [shot])
    c.result(2, lv["road"] == "Open", f"road {lv['road']!r}", [shot])
    api_lv = {h["hazard"]: h["level"] for h in cond(slug)["hazards"]}
    c.result(3, api_lv == {"mudslide": "raised", "flood": "raised", "road": "open"} and not has("place.hazard.heat", exact=True), f"api {api_lv}, heat row {has('place.hazard.heat', exact=True)}", [shot])
