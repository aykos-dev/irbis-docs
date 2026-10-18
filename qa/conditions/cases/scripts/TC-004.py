import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Weather card: per window day temps, wind + rain chance of the worst day, Open-Meteo credit',
 'priority': 'P0',
 'group': 'Core',
 'requirement': "AC7 + AC2 — 'Weather this weekend', '{day} {max}° / {min}°', worst-day wind and rain, credit; "
                'window = coming weekend (Sunday → Sun only)',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, onboarding done',
                  'Peak PLACE, no hazards, season open',
                  'Forecast: Sat 27°/14°; Sun 31°/18°, wind 40 km/h (Caution WIND), rain chance 45 %; Sat wind 10, '
                  'rain 10 %. Worst day = Sun'],
 'steps': ['Seed the fixture',
           'Cold-start, open the place, scroll to the weather card → check: `place.weather` shown',
           'Read the card'],
 'expected': ['For each day of the window (Sat+Sun, or Sun only when today is Sunday in Tashkent) '
              "`place.weather-day.<sat|sun>` shows '{Sat|Sun} {max}° / {min}°' (27°/14°, 31°/18°); "
              '`place.weather-day.sat` is absent when the window is Sun only — UI tree + screenshot',
              "`place.weather-summary` contains 'Wind 40 km/h' and 'Rain 45%' (worst day = Sun) — UI tree",
              "'Weather data by Open-Meteo.com' is shown — UI tree"],
 'caption': {'expected': 'For each day of the window (Sat+Sun, or Sun only when today is Sunday '},
 'focus': 'place.weather'
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = slug0(); set_place(slug, hazards=[], season=["possible"] * 12)
    c.step(1, "seed"); seed(slug, sat={"temperature_2m_max": 27, "temperature_2m_min": 14}, sun={"temperature_2m_max": 31, "temperature_2m_min": 18, "wind_speed_10m_max": 40, "precipitation_probability_max": 45})
    c.step(2, "open place")
    t0, tid, _ = view(c, slug, "0_open")
    ok = reveal("place.weather")
    c.checkpoint("weather card shown", ok, "no place.weather")
    shot = c.shot("1_weather", "place.weather")
    c.step(3, "read card")
    w = window(); exp = {"sat": "Sat 27° / 14°", "sun": "Sun 31° / 18°"}
    got = {d: tidtext(f"place.weather-day.{d}") for d in ("sat", "sun")}
    okd = all((got[d] is not None and exp[d] in got[d]) if d in w else got[d] is None for d in ("sat", "sun"))
    c.result(1, okd, f"window {sorted(w)}, got {got}", [shot])
    sm = tidtext("place.weather-summary") or ""
    c.result(2, "Wind 40 km/h" in sm and "Rain 45%" in sm, f"summary {sm!r}", [shot])
    c.result(3, has("Weather data by Open-Meteo.com"), "credit text present" if has("Weather data by Open-Meteo.com") else "credit missing", [shot])
