import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
from _feature import *  # noqa

META = {'title': 'Seed difficulty and required level bands (boundary elevations)',
 'priority': 'P1',
 'group': 'Variants',
 'requirement': 'AC1 — <1500→1, 1500–2499→2, 2500–3199→3, 3200–3799→4, ≥3800→5; level 1/2/3/5/7',
 'env': 'API · auto (no device)',
 'precondition': ['Seeded LOCAL dev DB (71 rows)'],
 'steps': ['For every row compute the expected difficulty from elevation_m and the expected required level from the '
           'difficulty',
           'Report the elevations closest to each boundary (1499/1500, 2499/2500, 3199/3200, 3799/3800)'],
 'expected': ['0 rows where difficulty ≠ band(elevation_m) — SQL',
              '0 rows where required_level ≠ map(difficulty) with 1→1, 2→2, 3→3, 4→5, 5→7 — SQL',
              'Nearest rows to each boundary (below / at-or-above) listed with their difficulty so a reviewer sees '
              'the band edge is honoured — SQL (observed text)'],
 'caption': {'expected': '0 rows where difficulty ≠ band(elevation_m)'}
}


def run(c):
    c.pre(" · ".join(META["precondition"]))
    band = "case when elevation_m < 1500 then 1 when elevation_m < 2500 then 2 when elevation_m < 3200 then 3 when elevation_m < 3800 then 4 else 5 end"
    lvl = "case difficulty when 1 then 1 when 2 then 2 when 3 then 3 when 4 then 5 else 7 end"
    c.step(1, "compare difficulty with band(elevation)")
    b1 = count_where(f"difficulty <> ({band})")
    c.result(1, b1 == 0, f"rows with wrong difficulty: {b1}")
    c.step(2, "compare required_level with map(difficulty)")
    b2 = count_where(f"required_level <> ({lvl})")
    c.result(2, b2 == 0, f"rows with wrong level: {b2}")
    edges = []
    for e in (1500, 2500, 3200, 3800):
        lo = sql(f"select elevation_m || ' m → d' || difficulty from places where elevation_m < {e} order by elevation_m desc limit 1")
        hi = sql(f"select elevation_m || ' m → d' || difficulty from places where elevation_m >= {e} order by elevation_m limit 1")
        edges.append(f"{e}: below {lo or 'n/a'}, at/above {hi or 'n/a'}")
    c.result(3, True, "; ".join(edges))
