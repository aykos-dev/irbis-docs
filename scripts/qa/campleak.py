#!/usr/bin/env python3
"""Privacy check over campbot JSONL logs: which bot received which secret, and whether any
non-describer saw a Crocodile word before the turn's result. Usage: campleak.py <bot log dir>"""
import json, os, sys

d = sys.argv[1]
for f in sorted(os.listdir(d)):
    if not f.endswith(".jsonl"):
        continue
    deals, seat, leaks = [], None, []
    open_words = {}  # word -> turnNo, from public results (fine to see)
    for line in open(os.path.join(d, f)):
        r = json.loads(line)
        m = r["msg"]
        if r["dir"] != "in" or not isinstance(m, dict):
            continue
        if m.get("type") == "welcome":
            seat = m["seatId"]
        if m.get("type") == "deal":
            deals.append((m.get("game"), m.get("round"), m["secret"]))
        if m.get("type") == "game":
            p = m.get("public", {})
            raw = json.dumps(p)
            if m.get("game") == "croc" and p.get("phase") in ("ready", "running") and "word" in raw:
                leaks.append(("croc word in public while running", p.get("turnNo")))
            if m.get("game") == "mafia" and not p.get("ended"):
                for o in p.get("out", []):
                    pass  # roleId of out seats is public by design when revealOut
                if "roles" in raw:
                    leaks.append(("mafia roles before ended", m.get("round")))
    croc = [x for x in deals if x[0] == "croc"]
    maf = [x for x in deals if x[0] == "mafia"]
    print(f"{f[:-6]:8} seat={seat} mafia_deals={len(maf)} croc_deals={len(croc)} leaks={leaks}")
