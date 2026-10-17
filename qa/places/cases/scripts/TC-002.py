import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Seed name cleaning and slug rules',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': "AC1 — strip '(… m)', slug = kebab + elevation, ru/en null",
 'env': 'API · auto (no device)',
 'precondition': ['Seeded LOCAL dev DB (71 rows)'],
 'steps': ["Query the row 'Chuquraq' with the parenthesised name `Chuquraq (27 m.) (Kelin Ko'ylak)` and 'Qorangur' "
           '(2943 m. in source, elevation 2941)',
           'Check every row: no `(… m)` height left in name_uz, slug = lowercase ASCII + `-` + elevation, slugs '
           'unique, name_ru / name_en / region null'],
 'expected': ["name_uz of the Chuquraq row is exactly `Chuquraq (Kelin Ko'ylak)` (the second parenthesis stays) — "
              'SQL',
              'Qorangur row: name_uz `Qorangur`, slug `qorangur-2941` — SQL',
              'Over all 71 rows: 0 names matching `\\(\\s*\\d+\\s*m\\.?\\s*\\)`, 0 slugs not matching '
              '`^[a-z0-9]+(-[a-z0-9]+)*-<elevation>$`, 71 distinct slugs, 0 non-null name_ru/name_en/region, 0 '
              'non-empty season/hazards — SQL'],
 'caption': {'expected': "name_uz of the Chuquraq row is exactly `Chuquraq (Kelin Ko'y"}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    import re
    c.step(1, "read Chuquraq + Qorangur rows")
    ch = sql("select name_uz from places where name_uz like 'Chuquraq (Kelin%'")
    c.result(1, ch == "Chuquraq (Kelin Ko'ylak)", f"Chuquraq row name_uz = {ch!r}")
    q = sql("select name_uz || '|' || slug from places where slug like 'qorangur-%'")
    c.result(2, q == "Qorangur|qorangur-2941", f"Qorangur row = {q!r}")
    c.step(2, "scan all rows")
    rows = [r.split("|") for r in sql("select name_uz || '|' || slug || '|' || elevation_m from places").splitlines()]
    bad_name = [r[1] for r in rows if re.search(r"\(\s*\d+\s*m\.?\s*\)", r[0])]
    bad_slug = [r[1] for r in rows if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*-" + r[2], r[1])]
    extra = count_where("name_ru is not null or name_en is not null or region is not null or cardinality(season) > 0 or cardinality(hazards) > 0")
    c.result(3, len(rows) == 71 and not bad_name and not bad_slug and len({r[1] for r in rows}) == 71 and extra == 0,
             f"rows {len(rows)}, height-in-name {len(bad_name)}, bad slugs {bad_slug[:3]}, rows with ru/en/region/season/hazards {extra}")
