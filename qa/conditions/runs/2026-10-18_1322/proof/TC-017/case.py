import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Precedence on the card: override beats closure beats forecast; ending the override brings the closure '
          'back',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC3 — override > closure > season > forecast; creating/ending recomputes at once; override text '
                "with uz fallback, source 'Irbis team'",
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, onboarding done',
                  'Peak PLACE, MILD forecast, season open',
                  "Closure (uz 'QA Yopiq') active, then override Caution (uz 'QA Ehtiyot bo`ling') created via admin "
                  'API'],
 'steps': ['Seed MILD + closure + override Caution → cold-start, open the place → check: card shown',
           'End the override via admin API → cold-start, open the place'],
 'expected': ["With override: chip 'Caution', title 'Caution this weekend', updated ends '· Irbis team', reason.1 "
              'equals the override uz text — UI tree + screenshot',
              "After ending the override: chip 'Not now', updated ends '· closure', reason.1 equals the closure text "
              '— UI tree + screenshot'],
 'caption': {'expected': "With override: chip 'Caution', title 'Caution this weekend', updated e"},
 'focus': 'place.condition'
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = slug0(); set_place(slug, hazards=[], season=["possible"] * 12)
    c.step(1, "seed, closure, override"); seed(slug); closure(slug, "QA Yopiq"); o = override(slug, "caution", "QA Ehtiyot boling")
    t0, tid, shot = view(c, slug, "1_override")
    c.checkpoint("condition card shown", tid == "place.condition", tid)
    reveal("place.condition-reason.1")
    up = tidtext("place.condition-updated") or ""
    c.result(1, text_in("place.condition-status") == "Caution" and tidtext("place.condition-title") == "Caution this weekend" and up.endswith("· Irbis team") and tidtext("place.condition-reason.1") == "QA Ehtiyot boling", f"chip {text_in('place.condition-status')!r}, updated {up!r}, reason {tidtext('place.condition-reason.1')!r}", [shot])
    c.step(2, "end override")
    st, _, _ = api("POST", f"/v1/admin/overrides/{o['id']}/end", None, admin())
    c.checkpoint("override ended", st == 200, st)
    t0, tid, shot = view(c, slug, "2_closure")
    reveal("place.condition-reason.1")
    up = tidtext("place.condition-updated") or ""
    c.result(2, text_in("place.condition-status") == "Not now" and up.endswith("· closure") and tidtext("place.condition-reason.1") == "QA Yopiq", f"chip {text_in('place.condition-status')!r}, updated {up!r}, reason {tidtext('place.condition-reason.1')!r}", [shot])
