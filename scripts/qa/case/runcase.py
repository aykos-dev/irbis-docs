"""Create a run, run one case per call, then finish the run's cases after review.

usage (always with the QA venv, for uiautomator2 and Pillow):
  PY=~/.claude/venvs/qa/bin/python; RC=scripts/qa/case/runcase.py
  $PY $RC new    <slug> --build "…" [--backend …] [--scope …]   create qa/<slug>/runs/<YYYY-MM-DD_HHMM>/run.md
                                                               (device, app version and accounts filled in);
                                                               prints the run dir
  $PY $RC run    <run dir> TC-019 [--force]       copy qa/<slug>/cases/scripts/TC-019.py into proof/TC-019/case.py
                                                  and execute it, recording it; writes proof/TC-019/result.json;
                                                  keeps the raw video until `finish`
  $PY $RC finish <run dir> <verdicts.json>        after review: render kept videos (P0/P1 or not Pass), contact
                                                  sheet only for P2/P3 Pass, check each, write run.md rows and
                                                  sections; a case with no result.json (Blocked, Not run, or
                                                  checked inside another case) gets its row from the verdict entry
One case per call: grouping saves little and hides progress.
The app session is shared between calls: a case relaunches the app only if its script does.
A checkpoint that fails blocks the case (status "blocked"); a script or device error is status "error".
"""
import importlib.util
import json
import os
import re
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "rec"))
from casekit import Blocked, Ctx  # noqa: E402
from config import CACHE, QA_ROOT  # noqa: E402
from rec import Rec  # noqa: E402
import gencase  # noqa: E402
import runmd  # noqa: E402

RENDER_WORKERS = 3
VERDICT_KEY = {"Pass": "pass", "Fail": "fail", "Blocked": "blocked", "Not run": "not-run"}


def library(run_dir):
    """qa/<slug>/cases/scripts for a run at qa/<slug>/runs/<run>."""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(run_dir))), "cases", "scripts")


def new(slug, build, backend="—", scope="all cases in the plan"):
    import drv
    if (why := drv.device_ready()):
        sys.exit(why)
    plan = os.path.join(QA_ROOT, slug, "cases", f"Test_{slug}.md")
    if not os.path.exists(plan):
        sys.exit(f"no plan at {plan} — run /qa-plan {slug} first")
    run = time.strftime("%Y-%m-%d_%H%M")
    run_dir = os.path.join(QA_ROOT, slug, "runs", run)
    os.makedirs(os.path.join(run_dir, "proof", "_run"), exist_ok=True)
    model = drv.sh("getprop", "ro.product.model").strip()
    android = drv.sh("getprop", "ro.build.version.release").strip()
    name, code = drv.app_version()
    text = runmd.RUN_TEMPLATE.format(run=run, slug=slug, build=f"{drv.PKG} {name} ({code}) — {build}",
                                     backend=backend, device=f"{model} (Android {android})",
                                     accounts="see Test data; phone numbers masked", tester="owner", scope=scope)
    open(os.path.join(run_dir, "run.md"), "w", encoding="utf-8").write(text)
    print(run_dir)


def prepare(run_dir, tc, force=False):
    """Copy the library script into proof/TC-NNN/case.py (the run's snapshot); refuse a stale one unless forced."""
    import shutil
    lib, case_dir = library(run_dir), os.path.join(run_dir, "proof", tc)
    os.makedirs(case_dir, exist_ok=True)
    src = os.path.join(lib, f"{tc}.py")
    if os.path.exists(src):
        if lib not in sys.path:
            sys.path.insert(0, lib)  # for `from _feature import *`
        want = gencase.script_hash(src)
        if want:
            m = re.search(r'"plan":\s*"([^"]+)"', open(src, encoding="utf-8").read())
            plan = os.path.join(os.path.dirname(lib), m.group(1)) if m else None
            now = gencase.plan_hash(open(plan, encoding="utf-8").read(), tc) if plan and os.path.exists(plan) else None
            if now and now != want and not force:
                sys.exit(f"{tc}: the plan changed since this script was written (hash {want} → {now}); "
                         f"update the script (and its plan_hash) or run with --force")
        shutil.copy(src, os.path.join(case_dir, "case.py"))
    elif not os.path.exists(os.path.join(case_dir, "case.py")):
        sys.exit(f"{tc}: no script — write {src} (gencase.py new …)")
    return case_dir


def load_case(case_dir):
    spec = importlib.util.spec_from_file_location("case_" + os.path.basename(case_dir).replace("-", "_"),
                                                  os.path.join(case_dir, "case.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def proposed(meta, data, status):
    if status != "done":
        return "Blocked" if status == "blocked" else "Not run"
    oks = [data["results"].get(str(i), {}).get("ok") for i in range(1, len(meta["expected"]) + 1)]
    if any(o is False for o in oks):
        return "Fail"
    return "Pass" if all(o is True for o in oks) else "Not run"


def run(run_dir, tcs, force=False):
    if len(tcs) != 1:
        sys.exit("one case per call — runcase.py run <run dir> TC-NNN")
    if not os.path.exists(os.path.join(CACHE, "session.json")):
        print("warning: no device session open (session.py up) — DND, show taps and mock are not managed", flush=True)
    tc = tcs[0]
    case_dir = prepare(run_dir, tc, force)
    mod = load_case(case_dir)
    meta = dict(mod.META, tc=tc)
    rec = Rec(case_dir, layout="case", title=f"{tc} · {meta['title']}")
    rec.start()
    c = Ctx(case_dir, run_dir, meta, rec)
    t0, status, reason = time.time(), "done", None
    try:
        mod.run(c)
    except Blocked as e:
        status, reason = "blocked", str(e)
    except Exception as e:  # a script or device error is not a verdict
        status, reason = "error", f"{type(e).__name__}: {e} @ line {traceback.extract_tb(e.__traceback__)[-1].lineno}"
    finally:
        ev = rec.stop(rec.title)
    data = c.data()
    res = {"meta": meta, "status": status, "reason": reason, "proposed": proposed(meta, data, status),
           "duration_s": round(time.time() - t0, 1), "events": len(ev), **data}
    json.dump(res, open(os.path.join(case_dir, "result.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    oks = "".join({True: "✅", False: "❌", None: "—"}[data["results"].get(str(i), {}).get("ok")]
                  for i in range(1, len(meta["expected"]) + 1))
    print(f"{tc} · {res['proposed']:8s} · {oks} · {res['duration_s']:5.1f}s" + (f" · {reason}" if reason else ""),
          flush=True)


def finish(run_dir, verdicts_path):
    verdicts = json.load(open(verdicts_path, encoding="utf-8"))
    items, jobs = [], []
    plan = next((runmd.load(os.path.join(run_dir, "proof", t))["meta"]["plan"] for t in verdicts
                 if os.path.exists(os.path.join(run_dir, "proof", t, "result.json"))), None)
    for tc, v in verdicts.items():
        case_dir = os.path.join(run_dir, "proof", tc)
        if not os.path.exists(os.path.join(case_dir, "result.json")):  # not executed
            items.append((runmd.stub(tc, v, plan), v, False))
            continue
        res = runmd.load(case_dir)
        rec = Rec.load(case_dir)
        keep = res["meta"].get("priority") in ("P0", "P1") or v["verdict"] != "Pass"
        items.append((res, v, keep))
        jobs.append((rec, keep, v, res))

    def work(job):
        rec, keep, v, res = job
        if rec.status != "stopped":
            return f"{res['meta']['tc']}: already {rec.status}"
        if keep:
            rec.render(VERDICT_KEY[v["verdict"]], res["meta"].get("caption", {}).get("expected"), v.get("caption"))
            return f"{res['meta']['tc']}: rendered, check " + ("OK" if rec.check() else "PROBLEMS")
        rec.sheet_only()
        return f"{res['meta']['tc']}: sheet only"

    with ThreadPoolExecutor(RENDER_WORKERS) as pool:
        for line in pool.map(work, jobs):
            print(line, flush=True)
    runmd.write(os.path.join(run_dir, "run.md"), items)
    print(f"run.md: {len(items)} rows and sections written", flush=True)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--force"]
    if len(args) < 2 or args[0] not in ("new", "run", "finish"):
        sys.exit(__doc__)
    if args[0] == "new":
        import argparse
        ap = argparse.ArgumentParser()
        ap.add_argument("cmd")
        ap.add_argument("slug")
        ap.add_argument("--build", required=True)
        ap.add_argument("--backend", default="—")
        ap.add_argument("--scope", default="all cases in the plan")
        a = ap.parse_args(args)
        new(a.slug, a.build, a.backend, a.scope)
    elif args[0] == "run":
        run(args[1], args[2:], "--force" in sys.argv)
    else:
        finish(args[1], args[2])
