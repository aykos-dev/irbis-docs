import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Card shows at most 3 reason lines, worst first (Thunderstorm leads)',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC7 + AC2 — up to 3 reasons, worst first, from templates',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, onboarding done',
                  'Peak PLACE, no hazards; Sun: weather code 95, wind 40, rain chance 70 %, max 36 °C (four '
                  'triggers); Sat MILD'],
 'steps': ['Seed the four-trigger fixture',
           'Cold-start, open the place → check: card shown',
           'Read the reason lines'],
 'expected': ["Chip 'Not now' with worried Irbis (`place.condition-mascot`) — UI tree + screenshot",
              "`place.condition-reason.1` = 'Thunderstorm on Sunday'; reasons 2 and 3 exist; "
              '`place.condition-reason.4` is absent — UI tree',
              'Reasons 2 and 3 are template lines of triggered rules (Strong wind / Rain likely / Heat) — UI tree'],
 'caption': {'expected': "Chip 'Not now' with worried Irbis (`place.condition-mascot`) — UI tree"},
 'focus': 'place.condition'
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = slug0(); set_place(slug, hazards=[], season=["possible"] * 12)
    c.step(1, "seed"); seed(slug, sun={"weather_code": 95, "wind_speed_10m_max": 40, "precipitation_probability_max": 70, "temperature_2m_max": 36})
    c.step(2, "open place")
    t0, tid, shot = view(c, slug, "1_card")
    c.checkpoint("condition card shown", tid == "place.condition", tid)
    c.step(3, "read reasons")
    c.result(1, text_in("place.condition-status") == "Not now" and has("place.condition-mascot", exact=True), f"chip {text_in('place.condition-status')!r}", [shot])
    r = [tidtext(f"place.condition-reason.{i}") for i in (1, 2, 3)]
    c.result(2, r[0] == "Thunderstorm on Sunday" and all(r) and not has("place.condition-reason.4", exact=True), f"reasons {r}", [shot])
    c.result(3, all(x and (x.startswith("Strong wind on Sunday") or x.startswith("Rain likely on Sunday") or x.startswith("Heat on Sunday")) for x in r[1:]), f"reasons 2-3 {r[1:]}", [shot])
