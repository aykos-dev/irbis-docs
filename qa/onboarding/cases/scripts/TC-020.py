import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Language chosen on Onb2 stays after ✕',
 'priority': 'P1',
 'group': 'Supplementary',
 'requirement': 'AC3 — language saved at once and kept after ✕',
 'env': 'Android · auto (adb)',
 'precondition': ['First run (reset link), app language English, guest'],
 'steps': ["Reset → Language → tap O'zbek (uz) → ✕ → tabs", 'Cold start'],
 'expected': ['Tabs are in Uzbek (nav.tab-profile content-desc "Profil") after ✕ — UI tree',
              'Still Uzbek after the cold start — UI tree'],
 'focus': 'nav.tab-profile',
 'caption': {'expected': 'tabs in Uzbek'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    c.checkpoint("Language shown", first_run_to("language"), "no onboarding.language")
    tap("onboarding.lang-uz", exact=True); time.sleep(0.5); tap("onboarding.close", exact=True)
    ok = wait(TABS, 10, exact=True); tab = find(TABS, exact=True)
    c.result(1, ok and bool(tab and "Profil" in (tab["desc"], tab["text"])), f"tab {tab and (tab['desc'] or tab['text'])!r}", [c.shot("1_uz")])
    relaunch(); wait(TABS, 20, exact=True); tab = find(TABS, exact=True)
    c.result(2, bool(tab and "Profil" in (tab["desc"], tab["text"])), f"tab {tab and (tab['desc'] or tab['text'])!r}", [c.shot("2_cold")])
    deep_link("irbis://debug/lang/en")
