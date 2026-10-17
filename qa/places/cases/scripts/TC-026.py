import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Locale fallback: Uzbek name and description shown in Russian',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC7 + AC4 — name / description in the app locale, fallback uz',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest, app language Russian (`irbis://debug/lang/ru`)',
                  'A place with only name_uz and description_uz (ru/en null), plus a second place with name_en set'],
 'steps': ['Open Explore in Russian and find the first card of the uz-only place',
           'Open its Place',
           'Switch to English and open the place whose name_en is set'],
 'expected': ['Russian UI: the card and place.name show the Uzbek name (name_uz) — UI tree + screenshot',
              'place.description shows the Uzbek description text — UI tree + screenshot',
              'English UI: the card for the place with name_en shows the English name, not name_uz — UI tree + '
              'screenshot'],
 'focus': 'place.name',
 'caption': {'expected': 'Russian UI: the card and place.name show the Uzbek name (nam'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    slug = pick("type='peak' and difficulty=1")
    slug_en = pick("type='lake'")
    set_place(slug, description_uz="QA tavsif: faqat o'zbekcha matn.")
    set_place(slug_en, name_en="QA English Lake")
    nm_uz = sql(f"select name_uz from places where slug='{slug}'")
    deep_link("irbis://debug/lang/ru"); time.sleep(1)
    c.step(1, "open the place in Russian")
    c.checkpoint("Place opened", open_place_link(slug), "no place.screen")
    c.result(1, text_of("place.name") == nm_uz, f"place.name {text_of('place.name')!r} vs name_uz {nm_uz!r}", [c.shot("1_ru_name")])
    c.result(2, "QA tavsif" in screen_text(), "description text in uz while UI is ru", [c.shot("2_ru_desc", "place.description")])
    deep_link("irbis://debug/lang/en"); time.sleep(1)
    c.step(3, "open the en-named place in English")
    c.checkpoint("Place opened", open_place_link(slug_en), "no place.screen")
    c.result(3, text_of("place.name") == "QA English Lake", f"place.name {text_of('place.name')!r}", [c.shot("3_en_name")])
    deep_link("irbis://debug/lang/en")
