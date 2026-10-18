import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': "Seasonal lock beats the forecast: 'Closed for the season · Opens in {Month}'",
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC7 + AC3 — season bar closed this month → Seasonal lock, opensMonth = next non-closed month '
                '(wrapping)',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, onboarding done',
                  "Peak PLACE, season bar: current Tashkent month and the next one 'closed', the other ten "
                  "'possible'",
                  'MILD forecast, no closure/override'],
 'steps': ['set_place season, seed MILD', 'Cold-start, open the place → check: card shown', 'Read the card'],
 'expected': ["Chip reads 'Seasonal lock' and title equals 'Closed for the season · Opens in {month after next}' — "
              'UI tree + screenshot',
              "`place.condition-updated` ends with '· season' and no 'Good weather' line is shown (season beats "
              'forecast) — UI tree',
              'QA event `condition_viewed` {status: seasonal_lock, source: season} — event log'],
 'caption': {'expected': "Chip reads 'Seasonal lock' and title equals 'Closed for the season · O"},
 'focus': 'place.condition'
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = slug0(); m = today().month
    season = ["possible"] * 12
    season[m - 1] = "closed"; season[m % 12] = "closed"
    set_place(slug, hazards=[], season=season)
    c.step(1, "season + seed"); seed(slug)
    c.step(2, "open place")
    t0, tid, shot = view(c, slug, "1_card")
    c.checkpoint("condition card shown", tid == "place.condition", tid)
    c.step(3, "read card")
    want = f"Closed for the season · Opens in {month_name(m + 2)}"
    c.result(1, text_in("place.condition-status") == "Seasonal lock" and tidtext("place.condition-title") == want, f"chip {text_in('place.condition-status')!r}, title {tidtext('place.condition-title')!r}, want {want!r}", [shot])
    up = tidtext("place.condition-updated") or ""
    c.result(2, up.endswith("· season") and not has("Good weather"), f"updated {up!r}", [shot])
    ev = viewed(t0, slug)
    c.result(3, bool(ev) and ev.get("status") == "seasonal_lock" and ev.get("source") == "season", f"event {ev}")
