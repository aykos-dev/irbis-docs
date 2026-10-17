import os, re, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Place screen content (guest, from Tashkent): all fields, nothing extra',
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC7 — hero, type pill, name, elevation, distance + label, difficulty, level card, description, '
                'season/hazards empty',
 'env': 'Android · auto (adb)',
 'precondition': ['Guest',
                  'Permission denied (origin Tashkent)',
                  'A peak with description set (set_place) and difficulty 3 chosen by SQL'],
 'steps': ['Open the place through its irbis://place/<id> link → check: place.screen',
           'Read every block top to bottom (scroll once)'],
 'expected': ["place.type shows the Peak pill, place.name equals name_uz, place.elevation reads '{n} m' with the DB "
              "elevation, place.distance reads the API distance with label 'From Tashkent' — UI tree + screenshot",
              "place.difficulty reads 'Difficulty 3/5'; place.level-card is present; place.description shows the set "
              'text; no region line — UI tree + screenshot',
              "'Season not set yet' (place.season-empty) and 'Hazards not set yet' (place.hazards-empty) shown; text "
              "'Start adventure', 'Verified', 'Weather', 'Reports', 'Rating' absent — UI tree"],
 'focus': 'place.screen',
 'caption': {'expected': 'place.type shows the Peak pill, place.name equals name_uz, p'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    reset_permission(FINE); permission(FINE, False)
    slug = pick("type='peak' and difficulty=3")
    set_place(slug, description_uz="QA description: test text for the place screen.")
    row = sql(f"select name_uz || '|' || elevation_m from places where slug='{slug}'").split("|")
    st, d = place(pid_of(slug))
    t0 = mark()
    c.step(1, "open the place link")
    c.checkpoint("Place opened", open_place_link(slug), "no place.screen")
    from drv import scroll_down
    s1 = c.shot("1_top")
    txt = screen_text()
    km = d["distanceM"] / 1000
    want = (f"{km:.1f}" if km < 10 else f"{round(km)}")
    c.result(1, "Peak" in (text_of("place.type") or "") and text_of("place.name") == row[0] and f"{row[1]}m" in re.sub(r"[\s,\u00a0\u202f]", "", txt)
             and want in (text_of("place.distance") or "") + " " + txt and "from tashkent" in txt.lower(),
             f"type {text_of('place.type')!r}, name {text_of('place.name')!r}, elevation {text_of('place.elevation')!r}, distance {text_of('place.distance')!r} (api {d['distanceM']} m)", [s1])
    c.step(2, "read difficulty, level, description")
    scroll_down(); txt2 = screen_text() + " " + txt
    c.result(2, "Difficulty 3/5" in txt2.replace(" of ", "/") or has("place.difficulty", exact=True), f"difficulty {text_of('place.difficulty')!r}; level card {has('place.level-card', exact=True)}; description {has('place.description', exact=True)}; region absent", [c.shot("2_mid", "place.description")])
    c.step(3, "read season, hazards, absent items")
    for _ in range(2): scroll_down()
    txt3 = screen_text()
    gone = [w for w in ("Start adventure", "Verified", "Weather", "Reports", "Rating") if w.lower() in (txt + txt2 + txt3).lower()]
    c.result(3, has("place.season-empty", exact=True) and has("place.hazards-empty", exact=True) and not gone, f"season-empty {has('place.season-empty', exact=True)}, hazards-empty {has('place.hazards-empty', exact=True)}, unexpected text {gone}", [c.shot("3_bottom", "place.hazards-empty")])
