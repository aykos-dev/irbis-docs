import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Deep link irbis://place/<id> opens Place from a cold start; an unknown id is handled',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC7 — deep link opens Place; error state',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, onboarding done', 'App force-stopped'],
 'steps': ['Force-stop, then open irbis://place/<id of a seeded peak>',
           'Open irbis://place/00000000-0000-4000-8000-000000000000',
           'Tap Back / the on-screen back action'],
 'expected': ['The seeded place opens with place.name equal to its name_uz and QA event place_viewed {slug} — UI '
              'tree + QA event',
              'The unknown id shows an error / not-found state (place.not-found or place.error), no crash, no '
              'place.name — UI tree + screenshot (wording is an open question)',
              'Back leaves the error state to a tab screen without a crash — UI tree'],
 'focus': 'place.screen',
 'caption': {'expected': 'The seeded place opens with place.name equal to its name_uz '}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = pick("type='peak'")
    nm = sql(f"select name_uz from places where slug='{slug}'")
    sh("am", "force-stop", PKG); time.sleep(1)
    t0 = mark()
    c.step(1, "cold deep link")
    ok = open_place_link(slug)
    ev = wait_event("place_viewed", t0, 10)
    c.result(1, ok and text_of("place.name") == nm and bool(ev) and ev.get("slug") == slug, f"name {text_of('place.name')!r}, event {ev}", [c.shot("1_link")])
    c.step(2, "unknown id")
    deep_link("irbis://place/00000000-0000-4000-8000-000000000000")
    st = wait_any(["place.not-found", "place.error", "place.offline"], 12)
    c.result(2, st == "place.not-found" and has("This place isn't available") and has("place.not-found-back", exact=True) and not has("place.name", exact=True) and not crashed(), f"state {st!r}, text {has('This place isn' + chr(39) + 't available')}", [c.shot("2_notfound", "place.screen")])
    c.step(3, "Back")
    tap("place.not-found-back", exact=True) if has("place.not-found-back", exact=True) else tap("place.back", exact=True)
    c.result(3, wait_any(["nav.tab-explore", "nav.tab-profile"], 10) is not None and not crashed(), "tab bar visible, no crash")
