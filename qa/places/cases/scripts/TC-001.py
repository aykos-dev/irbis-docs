import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Seed imports 71 places and is idempotent',
 'priority': 'P0',
 'group': 'Core',
 'requirement': 'AC1 — 71 rows, upsert by slug, type counts',
 'env': 'API · auto (no device)',
 'precondition': ['LOCAL dev DB migrated (places_init)', 'API repo on feat/places'],
 'steps': ['Run `npm run db:seed` in irbis-api → check: exit code 0',
           'Count rows in `places`',
           'Run `npm run db:seed` a second time → check: exit code 0',
           'Count rows again and count per type'],
 'expected': ['After the first run `select count(*) from places` = 71 — SQL',
              'After the second run the count is still 71 and `count(distinct slug)` = 71 — SQL',
              'Rows per type: peak 34, waterfall 22, lake 11, cave 2, canyon 2, camping 0, trail 0 — SQL'],
 'caption': {'expected': 'After the first run `select count(*) from places` = 71'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    import subprocess
    api_dir = os.path.join(os.path.dirname(DOCS), "irbis-api")
    def seed():
        r = subprocess.run(["npm", "run", "db:seed", "--silent"], cwd=api_dir, capture_output=True, text=True, timeout=240)
        return r.returncode
    c.step(1, "npm run db:seed (1st)")
    c.checkpoint("seed exit 0 (1st)", seed() == 0, "non-zero exit")
    n1 = count_where("true")
    c.step(2, "count rows")
    c.result(1, n1 == 71, f"count after 1st seed = {n1}")
    c.step(3, "npm run db:seed (2nd)")
    c.checkpoint("seed exit 0 (2nd)", seed() == 0, "non-zero exit")
    n2, d2 = count_where("true"), int(sql("select count(distinct slug) from places"))
    c.step(4, "count rows and types")
    c.result(2, n2 == 71 and d2 == 71, f"count {n2}, distinct slugs {d2}")
    per = {t: count_where(f"type='{t}'") for t in TYPES}
    exp = {**{t: 0 for t in TYPES}, **SEED_COUNTS}
    c.result(3, per == exp, f"per type {per}")
