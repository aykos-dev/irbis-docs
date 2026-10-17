import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Filters last for the session (tab switch, Place and Back) but not across a restart',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC5 + AC7 — filters kept; Back keeps filters and list position',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, location granted + mock at Tashkent centre', 'Explore loaded'],
 'steps': ['Apply Type = Lakes',
           'Open another tab and return to Explore',
           'Scroll the list down by 3 swipes, remember the first visible card slug, open a card, tap Back',
           'Force-stop and relaunch the app, open Explore'],
 'expected': ["After the tab round trip the Type chip still reads 'Lakes' and the header is 11 — UI tree + "
              'screenshot',
              'After Place → Back the chip is unchanged and the first visible card is the same slug as before '
              'opening (position kept) — UI tree + screenshot',
              'After a cold restart the chip has no value and the header is 71 (session only) — UI tree + '
              'screenshot'],
 'focus': 'explore.sheet',
 'caption': {'expected': "After the tab round trip the Type chip still reads 'Lakes' a"}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    from drv import scroll_down
    c.checkpoint("Explore loaded", explore_ready(), "no list")
    apply_filters(types=["lake"])
    c.step(1, "tab round trip")
    tap("nav.tab-profile", exact=True); wait("profile.guest", 10, exact=True)
    open_explore()
    chip = text_of("explore.filter.type") or ""
    c.result(1, "Lakes" in chip and count_in_header() == 11, f"chip {chip!r}, header {count_in_header()}", [c.shot("1_kept", "explore.filter.type")])
    c.step(2, "scroll, open card, Back")
    for _ in range(3): scroll_down()
    cards = [n["rid"] for n in nodes() if n["rid"].startswith("explore.card.")]
    c.checkpoint("cards visible after scrolling", bool(cards), cards)
    before = cards[0]
    tap(before, exact=True); wait("place.screen", 10, exact=True)
    tap("place.back", exact=True); wait("explore.count", 10, exact=True)
    after = [n["rid"] for n in nodes() if n["rid"].startswith("explore.card.")]
    c.result(2, "Lakes" in (text_of("explore.filter.type") or "") and bool(after) and after[0] == before, f"first card before {before}, after {after[:1]}, chip {text_of('explore.filter.type')!r}", [c.shot("2_back", "explore.sheet")])
    c.step(3, "cold restart")
    relaunch(); wait("nav.tab-explore", 20, exact=True); open_explore()
    c.result(3, "Lakes" not in (text_of("explore.filter.type") or "") and count_in_header() == 71, f"chip {text_of('explore.filter.type')!r}, header {count_in_header()}", [c.shot("3_restart", "explore.filter.type")])
