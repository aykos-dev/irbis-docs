"""Case library for a feature: one script per case, kept beside the plan and reused by every run and retest.

Library:  qa/<slug>/cases/scripts/
            _feature.py   shared points, accounts and helpers of this feature (optional; scripts `from _feature import *`)
            TC-NNN.py     META (with plan_hash) + run(c)
A run copies the script it executes into proof/TC-NNN/case.py, so the proof always shows the exact script.

usage:
  gencase.py new   <plan.md> TC-NNN [TC-…]     write skeletons for cases that have no script
  gencase.py check <plan.md>                   ok / stale (the case text changed) / missing / orphan
  gencase.py hash  <plan.md> TC-NNN            the case's current plan hash

Plan format (qa/<slug>/cases/Test_<slug>.md):
  ### ★ TC-NNN · P1 · title  … **Requirement:** … **Env:** … **Precondition:** … **Steps:** …
  **Expected result** (…): - bullet — evidence …   (until the next heading)
plan_hash = sha1 of the case text, whitespace-normalised, first 10 hex — a script goes stale exactly when the
plan's wording of that case changes.
"""
import argparse
import hashlib
import json
import os
import re
import sys


def lib_dir(plan):
    return os.path.join(os.path.dirname(os.path.abspath(plan)), "scripts")


def case_text(doc, tc):
    m = re.search(rf"^### (?:★ )?{tc} · .*?(?=^#{{2,3}} |\Z)", doc, re.M | re.S)
    return m.group(0) if m else None


def plan_hash(plan_doc, tc):
    text = case_text(plan_doc, tc)
    if text is None:
        return None
    text = re.sub(r"^### (?:★ )?", "### ", text)
    text = re.sub(r"^---\s*\n", "", text, flags=re.M)
    return hashlib.sha1(" ".join(text.split()).encode()).hexdigest()[:10]


def anchor(heading):
    h = re.sub(r"[^\w\- ]", "", heading.lower())
    return h.replace(" ", "-")


def parse_case(text, tc):
    head = re.match(rf"^### (?:★ )?(({tc}) · (P\d) · (.+))$", text, re.M)
    get = lambda k: (re.search(rf"^\**{k}:\**\s*(.+?)\s*$", text, re.M) or [None, ""])[1]  # noqa: E731
    exp_i = text.find("**Expected result")
    exp = [l[2:].strip() for l in text[exp_i:].splitlines() if l.startswith("- ")] if exp_i >= 0 else []
    post = text.find("**Postcondition")
    if post > exp_i >= 0:
        exp = [l[2:].strip() for l in text[exp_i:post].splitlines() if l.startswith("- ")]
    steps_i = text.find("**Steps:**")
    steps = [l.strip() for l in text[steps_i:exp_i if exp_i > 0 else None].splitlines()[1:]
             if re.match(r"\s*\d+\.", l)] if steps_i >= 0 else []
    pm = re.search(r"\*\*Precondition:\*\*(.*?)(?=\n\*\*Steps|\n\*\*Expected|\Z)", text, re.S)
    pre = " ".join(l.strip().lstrip("- ").strip() for l in pm.group(1).splitlines() if l.strip()) if pm else ""
    req = get("Requirement")
    return {"title": head.group(4), "priority": head.group(3), "env": get("Env"),
            "source": req.split(" — ")[0] if req else "", "anchor": anchor(head.group(1)), "expected": exp,
            "steps": steps, "pre": pre}


SKELETON = '''import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
try:
    from _feature import *  # noqa  (shared points/accounts/helpers of this feature)
except ImportError:
    pass

META = {meta}


def run(c):
    c.pre({pre!r})
{body}
'''


def skeleton(info, plan_name, phash):
    meta = {"title": info["title"], "group": "Core" if info["priority"] in ("P0", "P1") else "Supplementary",
            "priority": info["priority"] or "P2", "env": info["env"], "plan": plan_name, "anchor": info["anchor"],
            "source": info["source"], "expected": info["expected"],
            "caption": {"expected": (info["expected"] or [""])[0].split(" — ")[0][:80]}, "plan_hash": phash}
    body = [f"    # {s}" for s in info["steps"]]
    for i, e in enumerate(info["expected"], 1):
        body.append(f"    # Expected {i}: {e}")
        body.append(f"    c.result({i}, None, 'TODO', [])")
    return SKELETON.format(meta=json.dumps(meta, ensure_ascii=False, indent=1), pre=info["pre"],
                           body="\n".join(body) or "    pass")


def script_hash(path):
    m = re.search(r'"plan_hash":\s*"([0-9a-f]+)"', open(path, encoding="utf-8").read())
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["new", "check", "hash"])
    ap.add_argument("plan")
    ap.add_argument("tcs", nargs="*")
    a = ap.parse_args()
    plan_doc = open(a.plan, encoding="utf-8").read()
    lib = lib_dir(a.plan)
    plan_name = os.path.basename(a.plan)
    all_tcs = sorted(set(re.findall(r"^### (?:★ )?(TC-\d{3})", plan_doc, re.M)))
    if a.cmd == "hash":
        for tc in a.tcs:
            print(tc, plan_hash(plan_doc, tc))
        return
    if a.cmd == "check":
        have = {f[:-3] for f in os.listdir(lib) if re.match(r"TC-\d{3}\.py$", f)} if os.path.isdir(lib) else set()
        rows = {"ok": [], "stale": [], "missing": [], "orphan": sorted(have - set(all_tcs))}
        for tc in all_tcs:
            if tc not in have:
                rows["missing"].append(tc)
            elif script_hash(os.path.join(lib, f"{tc}.py")) != plan_hash(plan_doc, tc):
                rows["stale"].append(tc)
            else:
                rows["ok"].append(tc)
        for k, v in rows.items():
            print(f"{k:8s} {len(v):3d}  {' '.join(v)}")
        return
    os.makedirs(lib, exist_ok=True)
    for tc in a.tcs:
        path = os.path.join(lib, f"{tc}.py")
        if os.path.exists(path):
            print(tc, "exists — not overwritten")
            continue
        text = case_text(plan_doc, tc)
        if text is None:
            sys.exit(f"{tc}: not found in {a.plan}")
        open(path, "w", encoding="utf-8").write(skeleton(parse_case(text, tc), plan_name, plan_hash(plan_doc, tc)))
        print(tc, "skeleton written", path)


if __name__ == "__main__":
    main()
