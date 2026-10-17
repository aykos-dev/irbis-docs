"""run.md rows and case sections from proof/<id>/result.json + the reviewed verdict.
Every case gets a Table row; only non-Pass cases get a section (Pass details stay in proof/<id>/result.json).

Used by runcase.py finish. Replaces a case's existing row/section when the case is re-run.
verdict entry: {"verdict": "Pass|Fail|Blocked|Not run", "line": "what happened, one line",
                "conclusion": "…", "extra": "…", "caption": "actual, one line (video)",
                "actual": {"2": "override text for bullet 2"}, "ok": {"2": true}}
  ("ok"/"actual" override the script's reading after review; the script's own values stay in result.json)
a case that was not executed (no result.json) needs "title" and "reason" (why, or which case's proof covers it).
"""
import json
import os
import re

MARK = {True: "✅", False: "❌", None: "—"}


def mmss(t):
    return f"t={int(t // 60):02d}:{int(t % 60):02d}" if t is not None else ""


def proof_refs(tc, r, video_kept):
    refs = [f"proof/{tc}/{p}" for p in r.get("proof", [])]
    if video_kept and r.get("t") is not None:
        refs.append(f"video.mp4 {mmss(r['t'])}")
    return ", ".join(refs) or "no proof"


def section(res, v, video_kept):
    m, tc = res["meta"], res["meta"]["tc"]
    head = (f"**Group:** {m.get('group', '—')} · **Priority:** {m.get('priority', '—')} · **Env:** {m.get('env', '—')}\n"
            f"**Case:** {m['title']} · [→ {m.get('plan', '')}](../../cases/{m.get('plan', '')}#{m.get('anchor') or tc.lower()})")
    lines = [f'<a id="{tc.lower()}"></a>', f"### {tc} · {v['verdict']} · {m['title']}", head]
    if res.get("stub"):
        lines.append(f"**{'Reason' if v['verdict'] in ('Blocked', 'Not run') else 'Proof'}:** {v.get('reason', '—')}")
        if v.get("conclusion"):
            lines.append(f"**Conclusion:** {v['conclusion']}")
        return "\n".join(lines)
    if v["verdict"] in ("Blocked", "Not run"):
        lines.append(f"**Reason:** {v.get('reason') or res.get('reason') or '—'}")
        files = sorted(f for f in os.listdir(res["_dir"]) if not f.startswith(".") and f != "result.json")
        if files:
            lines.append("**Proof:** " + ", ".join(f"proof/{tc}/{f}" for f in files))
        return "\n".join(lines)
    lines.append("**Done:** " + " → ".join(res["done"]))
    lines.append(f"**Expected** (source: {m.get('source', '—')}):")
    lines += [f"{i}. {e}" for i, e in enumerate(m["expected"], 1)]
    lines.append("**Actual:**")
    for i in range(1, len(m["expected"]) + 1):
        r = res["results"].get(str(i), {"ok": None, "observed": "not checked", "proof": []})
        obs = v.get("actual", {}).get(str(i), r["observed"])
        ok = v.get("ok", {}).get(str(i), r["ok"])
        lines.append(f"{i}. {MARK[ok]} {obs} — {proof_refs(tc, r, video_kept)}")
    lines.append(f"**Conclusion:** {v.get('conclusion', '—')}")
    if v.get("extra"):
        lines.append(f"**Extra:** {v['extra']}")
    return "\n".join(lines)


def row(res, v):
    m, tc = res["meta"], res["meta"]["tc"]
    if res.get("stub"):
        return f"| [{tc}](#{tc.lower()}) | {m['title']} | {v['verdict']} | {v.get('line', '—')} | {v.get('reason', '—')} | — |"
    bad = [i for i, r in sorted(res["results"].items()) if v.get("ok", {}).get(i, r["ok"]) is False]
    issue = (v.get("reason") or res.get("reason") or "—") if v["verdict"] in ("Blocked", "Not run") else \
        ("❌ " + ", ".join(bad) if bad else "—")
    link = f"[{tc}](#{tc.lower()})" if v["verdict"] != "Pass" else tc
    return f"| {link} | {m['title']} | {v['verdict']} | {v.get('line', '—')} | {issue} | [proof/{tc}/](proof/{tc}/) |"


def _replace_block(text, heading, tc, new, end_marker):
    """Replace the case's block inside a section, or append it before end_marker."""
    start = text.index(heading)
    stop = text.find(end_marker, start + len(heading))
    stop = len(text) if stop < 0 else stop
    body = text[start:stop]
    pat = re.compile(rf'(<a id="{re.escape(tc.lower())}"></a>\n)?### {re.escape(tc)} · .*?(?=\n<a id=|\n### (?:TC|STD)-|\Z)', re.S)
    if new is None:  # a Pass: no section (drop one left by an earlier non-Pass run of the same case)
        body = pat.sub("", body, count=1)
    else:
        body = pat.sub(lambda _: new, body, count=1) if pat.search(body) else body.rstrip("\n") + "\n\n" + new + "\n\n"
    return text[:start] + body + text[stop:]


def write(run_md, items):
    """items: list of (result dict, verdict dict, video_kept)."""
    text = open(run_md, encoding="utf-8").read()
    for res, v, kept in items:
        tc = res["meta"]["tc"]
        r = row(res, v)
        rows = re.compile(rf"^\| \[?{re.escape(tc)}\]?.*$", re.M)
        if rows.search(text):
            text = rows.sub(lambda _: r, text, count=1)
        else:
            j = text.index("## Table")
            nxt = text.find("\n## ", j + 5)
            nxt = len(text) if nxt < 0 else nxt
            block = text[j:nxt].rstrip("\n")
            if "| TC |" not in block:
                block += "\n| TC | Case | Verdict | What happened | Issue / note | Proof |\n|---|---|---|---|---|---|"
            text = text[:j] + block + "\n" + r + "\n" + text[nxt:]
        sec = None if v["verdict"] == "Pass" else section(res, v, kept)
        text = _replace_block(text, "## Cases", tc, sec, "\n## Additional observations")
    open(run_md, "w", encoding="utf-8").write(text)


def load(case_dir):
    res = json.load(open(os.path.join(case_dir, "result.json"), encoding="utf-8"))
    res["_dir"] = case_dir
    return res


def stub(tc, v, plan):
    """A case that was not executed: row and section from the verdict entry alone."""
    return {"stub": True, "meta": {"tc": tc, "title": v.get("title", tc), "plan": plan or "",
                                   "priority": v.get("priority", "—"), "group": v.get("group", "—"),
                                   "env": v.get("env", "—"), "anchor": tc.lower()}, "results": {}}


RUN_TEMPLATE = """# Run {run} — {slug}
**Status:** in progress
**Build:** {build}
**Backend:** {backend}
**Device:** {device}
**Accounts:** {accounts}
**Tester:** Claude (auto) + {tester} (manual)
**Scope:** {scope}
**Blocked reasons:** —
**Plan:** ../../cases/Test_{slug}.md

## Results

## Defects

## Table
| TC | Case | Verdict | What happened | Issue / note | Proof |
|---|---|---|---|---|---|

## Cases
_Only cases that did not pass; Pass details are in proof/<id>/result.json._

## Additional observations

## Follow-ups
"""
