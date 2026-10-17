"""What a case script sees. The script IS the test case: its META is the plan (`gencase.py doc` renders
qa/<slug>/cases/Test_<slug>.md from all scripts), run(c) executes it.

META keys: title, priority (P0–P3), group (Core|Supplementary), requirement ("AC2 — one line"), env,
precondition [..], steps [..], expected [.. "bullet — evidence"], postcondition (optional), focus (testID to crop
screenshots to), caption {expected}.

Evidence: c.shot(name) saves the full screenshot (proof) plus a small crop of META["focus"] (or focus=…) into
proof/_run/review/TC/ — reviewers read ONLY the crop, and only for bullets that are ❌ or — (needs a human).

Example:

    META = {"title": "Check-in succeeds 150 m from a verified spot", "group": "Core", "priority": "P1",
            "env": "Android · auto (adb + mock location) · resources: ACC-A, SPOT-1",
            "plan": "Test_check-in.md", "anchor": "tc-003--p1--…", "source": "AC2",
            "expected": ["Success sheet \\"+50 XP\\" within 5 s — screenshot",
                         "Event `checkin_succeeded` {xp_awarded: 50} — event log"],
            "caption": {"expected": "success sheet with +50 XP"}, "plan_hash": "…"}

    def run(c):
        c.pre("ACC-A signed in, no check-in today at SPOT-1")
        lat, lng = offset(*SPOT_1, metres_north=150)
        fix = c.open_app_at(lat, lng, "150 m north of SPOT-1", 1)
        c.checkpoint("app read the mock location", fix is not None, fix)
        c.step(2, "Open SPOT-1 → Check in"); deep_link("irbis://spots/spot_1"); tap("spot.checkin", exact=True)
        t0 = c.mark()
        ok = wait("+50 XP", 5)
        c.result(1, ok, "success sheet shown" if ok else "no success sheet", [c.shot("2_result")])
        ev = c.wait_event("checkin_succeeded", t0, 5)
        c.result(2, bool(ev and ev.get("xp_awarded") == 50), f"event: {ev}")

checkpoint() that does not hold raises Blocked: the case stops and runcase.py records the reason.
result(n, ok, observed, proof) answers Expected bullet n (1-based); ok=None means a person must judge it.
Everything goes into proof/TC-NNN/result.json; the verdict is decided after review, never by the script alone.
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rec"))
import drv  # noqa: E402

THUMB_W = 360          # review crops: small on purpose (each image read costs tokens)
FOCUS_PAD = 24


class Blocked(Exception):
    pass


class Ctx:
    def __init__(self, case_dir, run_dir, meta, rec):
        self.dir, self.run_dir, self.meta, self.rec = case_dir, run_dir, meta, rec
        self.done, self.results, self.checkpoints, self.notes, self.shots = [], {}, [], [], []

    # --- what was done ---
    def pre(self, text):
        self.done.append(text)

    def setup(self, text):
        self.rec.step(f"Setup: {text}")

    def step(self, n, text):
        self.rec.step(f"{n}: {text}")
        self.done.append(f"{n}. {text}")

    def observe(self, text):
        self.rec.step(f"Observed: {text}")

    def note(self, text):
        self.notes.append(text)

    # --- evidence ---
    def t(self):
        return round(time.time() - self.rec.t0, 1)

    def shot(self, name, focus=None):
        """Full screenshot = proof; a small crop around `focus` (testID) = what a reviewer looks at."""
        focus = focus or self.meta.get("focus")
        box = None
        if focus:
            n = drv.find(focus, exact=True)
            box = n["b"] if n else None
        path = self.rec.shot(name)
        self.shots.append(os.path.basename(path))
        try:
            from PIL import Image
            review = os.path.join(self.run_dir, "proof", "_run", "review", self.meta["tc"])
            os.makedirs(review, exist_ok=True)
            im = Image.open(path)
            if box:
                x1, y1, x2, y2 = box
                im = im.crop((max(0, x1 - FOCUS_PAD), max(0, y1 - FOCUS_PAD),
                              min(im.width, x2 + FOCUS_PAD), min(im.height, y2 + FOCUS_PAD)))
            w = min(THUMB_W, im.width)
            im.resize((w, int(im.height * w / im.width))).save(os.path.join(review, os.path.basename(path)))
        except Exception as e:  # the crop is a convenience; the full screenshot is the proof
            self.note(f"review crop failed: {e}")
        return os.path.basename(path)

    def checkpoint(self, name, ok, seen=None):
        self.checkpoints.append({"name": name, "ok": bool(ok), "seen": str(seen)[:400], "t": self.t()})
        if not ok:
            raise Blocked(f"checkpoint '{name}' did not hold: {str(seen)[:200]}")

    def result(self, n, ok, observed, proof=()):
        self.results[n] = {"ok": ok, "observed": observed, "proof": list(proof), "t": self.t()}

    # --- device helpers bound to this recording ---
    mark = staticmethod(drv.mark)
    wait_event = staticmethod(drv.wait_event)
    no_event = staticmethod(drv.no_event)

    def open_app_at(self, lat, lng, label, step_no, **kw):
        fix = drv.open_app_at(self.rec, lat, lng, label, step_no, **kw)
        self.done.append(f"{step_no}. app opened at {label}")
        return fix

    def data(self):
        return {"done": self.done, "results": {str(k): v for k, v in sorted(self.results.items())},
                "checkpoints": self.checkpoints, "notes": self.notes, "shots": self.shots}
