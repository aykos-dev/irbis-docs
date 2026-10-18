import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Rule boundaries seen on the card: wind 34/35, gusts 59/60, rain 19/20 mm, chance 59/60 %, max 34/35 °C, '
          'min -9/-10 °C',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC2 — thresholds are inclusive (≥ / ≤); Go below, Caution/Not now at the value',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, onboarding done',
                  'Peak PLACE, no hazards, season open; each fixture changes one field on Sun (window-safe) and '
                  'leaves the rest MILD'],
 'steps': ['For each pair seed the below-value fixture, cold-start and read the chip; seed the at-value fixture, '
           'cold-start and read the chip'],
 'expected': ["Wind 34 → 'Go', 35 → 'Caution' — chip",
              "Gusts 59 → 'Go', 60 → 'Not now' — chip",
              "Precipitation 19 mm → 'Go', 20 mm → 'Not now' — chip",
              "Rain chance 59 % → 'Go', 60 % → 'Caution' — chip",
              "Max temperature 34 → 'Go', 35 → 'Caution' — chip",
              "Min temperature -9 → 'Go', -10 → 'Caution' — chip"],
 'caption': {'expected': "Wind 34 → 'Go', 35 → 'Caution' — chip"},
 'focus': 'place.condition-status'
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = slug0(); set_place(slug, hazards=[], season=["possible"] * 12)
    pairs = [("wind_speed_10m_max", 34, "Go", 35, "Caution"), ("wind_gusts_10m_max", 59, "Go", 60, "Not now"),
             ("precipitation_sum", 19, "Go", 20, "Not now"), ("precipitation_probability_max", 59, "Go", 60, "Caution"),
             ("temperature_2m_max", 34, "Go", 35, "Caution"), ("temperature_2m_min", -9, "Go", -10, "Caution")]
    for n, (f, lo, elo, hi, ehi) in enumerate(pairs, 1):
        c.step(n, f"{f}: {lo} then {hi}")
        got = []
        for v in (lo, hi):
            seed(slug, sun={f: v})
            view(c, slug, f"{n}_{f}_{v}")
            got.append(text_in("place.condition-status"))
        shot = c.shot(f"{n}_last", "place.condition-status")
        c.result(n, got == [elo, ehi], f"{f}: {lo}→{got[0]!r}, {hi}→{got[1]!r}", [shot])
