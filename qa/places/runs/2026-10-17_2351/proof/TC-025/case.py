import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Season bar, hazards list and region line when set',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': "AC7 — 12 months J–D, today's month marked, legend; hazards list; region only if set",
 'env': 'Android · auto (adb)',
 'precondition': ['Guest',
                  "One local place set to: region 'Tashkent region', season Best for Apr–Oct, Possible Mar and Nov, "
                  'Closed Dec–Feb, hazards flood + road'],
 'steps': ['Open the place via its link and scroll to the season bar',
           'Read the bar, the legend, the hazards and the region line'],
 'expected': ["The region line 'Tashkent region' is shown — UI tree + screenshot",
              'place.season shows 12 months (place.season-1 … place.season-12), the legend Best / Possible / Closed, '
              "and place.season-today marks this month (month number = today's) — UI tree + screenshot",
              'place.hazards lists Flood and Road (place.hazard-flood, place.hazard-road); place.season-empty and '
              'place.hazards-empty are absent — UI tree + screenshot'],
 'focus': 'place.season',
 'caption': {'expected': "The region line 'Tashkent region' is shown"}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    import datetime
    slug = pick("type='lake'")
    seas = ["closed", "closed", "possible", "best", "best", "best", "best", "best", "best", "best", "possible", "closed"]
    set_place(slug, region="Tashkent region", season=seas, hazards=["flood", "road"])
    c.step(1, "open the place")
    c.checkpoint("Place opened", open_place_link(slug), "no place.screen")
    c.result(1, has("Tashkent region"), "region line text present", [c.shot("1_region")])
    from drv import scroll_down
    for _ in range(3):
        if has("place.season", exact=True): break
        scroll_down()
    c.step(2, "read season bar")
    months = [m for m in range(1, 13) if has(f"place.season-{m}", exact=True)]
    leg = [w for w in ("Best", "Possible", "Closed") if has(w)]
    today = find("place.season-today", exact=True)
    c.result(2, months == list(range(1, 13)) and leg == ["Best", "Possible", "Closed"] and today is not None,
             f"months {len(months)}, legend {leg}, today marker {bool(today)} (today is month {datetime.date.today().month})", [c.shot("2_season", "place.season")])
    for _ in range(2): scroll_down()
    c.step(3, "read hazards")
    c.result(3, has("place.hazard-flood", exact=True) and has("place.hazard-road", exact=True) and not has("place.season-empty", exact=True) and not has("place.hazards-empty", exact=True),
             f"flood {has('place.hazard-flood', exact=True)}, road {has('place.hazard-road', exact=True)}", [c.shot("3_hazards", "place.hazards")])
