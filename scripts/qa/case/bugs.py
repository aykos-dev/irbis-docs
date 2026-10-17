"""Defect bookkeeping across features.

usage:
  bugs.py next  <slug>        the next defect number for a feature (D1, D2 … continue across runs, never reused)
  bugs.py index               rebuild qa/BUGS.md (every defect of every feature)
  bugs.py open                list the open defects (Open / Not fixed) as `<slug>/D{n}` — the input /qa-retest takes
  bugs.py find  <ref>         path of a defect folder from `check-in/D3`, `D3` (if unique) or a path

A defect file is qa/<slug>/bugs/D{n}_{name}/D{n}_{name}.md; its header table carries `| Status | … |` and
`| Severity | … |`, the first heading is `# D{n} · {one line}`.
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rec"))
from config import QA_ROOT  # noqa: E402

def defects():
    out = []
    for path in sorted(glob.glob(os.path.join(QA_ROOT, "*", "bugs", "D*_*", "D*_*.md"))):
        folder = os.path.dirname(path)
        slug = os.path.basename(os.path.dirname(os.path.dirname(folder)))
        text = open(path, encoding="utf-8").read()
        num = int(re.match(r"D(\d+)_", os.path.basename(folder)).group(1))
        title = (re.search(r"^# D\d+ · (.+)$", text, re.M) or [None, os.path.basename(folder)])[1]
        cell = lambda k: (re.search(rf"^\| {k} \| (.+?) \|\s*$", text, re.M) or [None, "—"])[1].strip()  # noqa: E731
        out.append({"slug": slug, "n": num, "ref": f"{slug}/D{num}", "title": title, "status": cell("Status"),
                    "severity": cell("Severity"), "cases": cell("Cases"), "path": path, "folder": folder})
    return out


def is_open(d):
    s = d["status"].lstrip("✅❌ *").lower()
    return s.startswith("open") or s.startswith("not fixed")


def sev_key(d):
    m = re.match(r"(\d)", d["severity"])
    return (int(m.group(1)) if m else 9, d["slug"], d["n"])


def index():
    ds = defects()
    rel = lambda p, base: os.path.relpath(p, base)  # noqa: E731
    lines = ["# Defects — all features", "",
             "Built by `scripts/qa/case/bugs.py index`. Open first, then by severity. "
             "Retest open ones with `/qa-retest open`.", "",
             "| Ref | Severity | Defect | Status |", "|---|---|---|---|"]
    for d in sorted(ds, key=lambda d: (not is_open(d), *sev_key(d))):
        lines.append(f"| [{d['ref']}]({rel(d['path'], QA_ROOT)}) | {d['severity']} | {d['title']} | {d['status']} |")
    open(os.path.join(QA_ROOT, "BUGS.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"indexed {len(ds)} defects ({sum(is_open(d) for d in ds)} open)")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "open"
    ds = defects()
    if cmd == "next":
        slug = sys.argv[2]
        print("D" + str(max([d["n"] for d in ds if d["slug"] == slug] or [0]) + 1))
    elif cmd == "index":
        index()
    elif cmd == "open":
        for d in sorted((d for d in ds if is_open(d)), key=sev_key):
            print(f"{d['ref']}\t{d['severity']}\t{d['title']}")
    elif cmd == "find":
        ref = sys.argv[2].rstrip("/")
        if os.path.isdir(ref):
            print(os.path.abspath(ref))
            return
        hits = [d for d in ds if d["ref"] == ref or f"D{d['n']}" == ref or os.path.basename(d["folder"]) == ref]
        if len(hits) != 1:
            sys.exit(f"{ref}: {'not found' if not hits else 'ambiguous — use <slug>/D{n}: ' + ', '.join(h['ref'] for h in hits)}")
        print(hits[0]["folder"], "\t", hits[0]["cases"])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
