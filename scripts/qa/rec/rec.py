"""Screen recorder for Irbis QA (Android, scrcpy) — one tool for case videos, bug videos and retests.

Two phases, so the verdict on the video is written only after a person has looked at the evidence:
  1. record:  start -> step "<caption>" ... -> shot <name> ... -> stop
              stop keeps the raw recording and writes the step times and the analytics events.
  2. finish:  render [--verdict V --expected "..." --actual "..."]  burns the captions, adds the verdict
              captions at the end, deletes the raw file;  check  validates the result and extracts the
              verdict frame for review;  prune  drops a case video that is not kept (P2/P3 Pass).

Layouts:
  bug   qa/<slug>/bugs/D{n}_{name}/            video/{folder}{__variant}.mp4
                                     image/{shot}{__variant}.png
                                     others/steps{__variant}.tsv, events{__variant}.txt, .rec{__variant}.json
  case  qa/<slug>/runs/{run}/proof/TC-NNN/  video.mp4, video_steps.tsv, video_sheet.png, events.txt, {step}_{what}.png

CLI:   rec.py start <folder> [--layout bug|case] [--variant V] [--title "..."]
       rec.py step <folder> [--variant V] "<caption>"
       rec.py shot <folder> [--variant V] <name>
       rec.py stop <folder> [--variant V]
       rec.py render <folder> [--variant V] [--verdict fixed|not-fixed|pass|fail|blocked|not-run]
                     [--expected "..."] [--actual "..."]
       rec.py check <folder> [--variant V]
       rec.py prune <folder> [--variant V]
Python: from rec import Rec;  r = Rec(folder, variant, layout="bug"); r.start(); r.step(...); r.stop(title)
"""
import argparse
import json
import os
import re
import signal
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from config import VENV_PY as PY_PIL  # noqa: E402
EVENTS = os.environ.get("REC_EVENTS")            # regex over "time name {props}" lines; unset = every event
START_TIMEOUT_S = 15
HOLD_S = {"expected": 5.0, "result": 6.0}
SHEET_EVERY_S, SHEET_COLUMNS, SHEET_TILE_W = 2, 8, 180

WORDS = {
    "en": {"expected": "Expected", "result": "Result",
           "fixed": "FIXED", "not-fixed": "NOT FIXED", "pass": "PASS", "fail": "FAIL",
           "blocked": "BLOCKED", "not-run": "NOT RUN"},
}


class Rec:
    def __init__(self, folder, variant=None, layout="bug", lang=None, title=None):
        self.folder = os.path.abspath(folder)
        self.variant = variant
        self.layout = layout
        self.lang = "en"
        self.title = title
        sfx = f"__{variant}" if variant else ""
        self.sfx = sfx
        f = self.folder
        if layout == "bug":
            name = os.path.basename(f)
            self.video_dir, self.image_dir, self.others_dir = f"{f}/video", f"{f}/image", f"{f}/others"
            self.video = f"{self.video_dir}/{name}{sfx}.mp4"
            self.raw = f"{self.video_dir}/.raw{sfx}.mp4"
            self.steps_path = f"{self.others_dir}/steps{sfx}.tsv"
            self.events_path = f"{self.others_dir}/events{sfx}.txt"
            self.state_path = f"{self.others_dir}/.rec{sfx}.json"
            self.check_frame = f"{self.others_dir}/.check{sfx}.png"
            self.sheet = None
        else:
            self.video_dir = self.image_dir = self.others_dir = f
            self.video = f"{f}/video{sfx}.mp4"
            self.raw = f"{f}/.raw{sfx}.mp4"
            self.steps_path = f"{f}/video_steps{sfx}.tsv"
            self.events_path = f"{f}/events{sfx}.txt"
            self.state_path = f"{f}/.rec{sfx}.json"
            self.check_frame = f"{f}/.check{sfx}.png"
            self.sheet = f"{f}/video_sheet{sfx}.png"
        self.t0, self.pid, self.steps, self.status, self.end, self._proc = None, None, [], "new", None, None

    # ---------- state (lets every CLI call pick up where the last one stopped) ----------
    def save(self):
        os.makedirs(os.path.dirname(self.state_path), exist_ok=True)
        keep = {k: getattr(self, k) for k in ("layout", "lang", "title", "t0", "pid", "steps", "status", "end",
                                               "variant")}
        with open(self.state_path, "w", encoding="utf-8") as fh:
            json.dump(keep, fh, ensure_ascii=False, indent=1)

    @classmethod
    def load(cls, folder, variant=None):
        sfx = f"__{variant}" if variant else ""
        for path in (f"{folder}/others/.rec{sfx}.json", f"{folder}/.rec{sfx}.json"):
            if os.path.exists(path):
                st = json.load(open(path, encoding="utf-8"))
                r = cls(folder, variant, st["layout"], st["lang"], st["title"])
                for k in ("t0", "pid", "steps", "status", "end"):
                    setattr(r, k, st[k])
                return r
        sys.exit(f"no recording state in {folder} (variant {variant!r})")

    # ---------- phase 1: record ----------
    def start(self):
        if subprocess.run(["adb", "get-state"], capture_output=True, text=True).stdout.strip() != "device":
            sys.exit("no Android device on adb — connect the phone (adb devices) and retry")
        if "isKeyguardShowing=true" in subprocess.run(["adb", "shell", "dumpsys", "window"], capture_output=True,
                                                           text=True).stdout:
            sys.exit("the phone is locked — unlock it (PIN) and retry")
        for d in (self.video_dir, self.image_dir, self.others_dir):
            os.makedirs(d, exist_ok=True)
        if os.path.exists(self.raw):
            os.remove(self.raw)
        subprocess.run(["adb", "logcat", "-c"])
        log = open(f"{self.raw}.log", "w")
        proc = subprocess.Popen(["scrcpy", "--no-window", "--no-audio", "--no-control", "--max-size=1280", "--video-bit-rate=6M", f"--record={self.raw}"],
                                stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        # scrcpy's log is block-buffered into the file, so "Recording started" shows up only at exit; the raw
        # file growing is the reliable sign that the first frame (video time 0) has arrived
        end = time.time() + START_TIMEOUT_S
        while time.time() < end and not (os.path.exists(self.raw) and os.path.getsize(self.raw) > 0):
            if proc.poll() is not None:
                sys.exit("scrcpy exited: " + open(f"{self.raw}.log").read()[-400:])
            time.sleep(0.05)
        if not (os.path.exists(self.raw) and os.path.getsize(self.raw) > 0):
            sys.exit(f"scrcpy wrote nothing in {START_TIMEOUT_S}s: " + open(f"{self.raw}.log").read()[-400:])
        self._proc = proc  # kept when the recording is driven from this process (Python scripts); CLI calls lose it
        self.pid, self.t0, self.steps, self.status = proc.pid, time.time(), [], "recording"
        self.save()

    def step(self, caption):
        t = round(time.time() - self.t0, 2)
        self.steps.append([t, caption])
        self.save()
        print(f"[{t:6.1f}s] {caption}", flush=True)

    def shot(self, name):
        path = f"{self.image_dir}/{name}{self.sfx}.png"
        with open(path, "wb") as fh:
            fh.write(subprocess.run(["adb", "exec-out", "screencap", "-p"], capture_output=True).stdout)
        return path

    def stop(self, title=None):
        time.sleep(1.5)
        self.end = round(time.time() - self.t0, 2)
        self.title = title or self.title or os.path.basename(self.folder)
        try:
            os.killpg(self.pid, signal.SIGINT)
        except ProcessLookupError:
            pass
        proc = getattr(self, "_proc", None)
        if proc is not None:  # our own child: wait() reaps it (a kill-0 probe would see the zombie for 30 s)
            try:
                proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                proc.kill()
        else:
            for _ in range(150):
                try:
                    os.kill(self.pid, 0)
                    time.sleep(0.2)
                except ProcessLookupError:
                    break
        log = subprocess.run(["adb", "logcat", "-d", "-v", "time"], capture_output=True, text=True).stdout
        ev = subprocess.run([sys.executable, f"{BASE}/events.py", ""], input=log,
                            capture_output=True, text=True).stdout.splitlines()
        keep = [l for l in ev if not EVENTS or re.search(EVENTS, l)]
        with open(self.events_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(keep) + ("\n" if keep else ""))
        self.status = "stopped"
        self.save()
        self._write_steps(self.steps, self.end)
        print(f"stopped: raw kept at {self.raw}. Review the screenshots and {self.events_path}, then: "
              f"rec.py render {self.folder}{' --variant ' + self.variant if self.variant else ''} --verdict …")
        return keep

    # ---------- phase 2: finish ----------
    def _write_steps(self, steps, end):
        with open(self.steps_path, "w", encoding="utf-8") as fh:
            for t, c in steps:
                fh.write(f"{t}\t{c}\n")
            fh.write(f"{end}\tEND\n")

    def render(self, verdict=None, expected=None, actual=None):
        if not os.path.exists(self.raw):
            sys.exit(f"no raw recording at {self.raw} (already rendered? re-record to change captions)")
        w = WORDS[self.lang]
        steps, t = [list(s) for s in self.steps], self.end
        if expected:
            steps.append([t, f"{w['expected']}: {expected}"])
            t = round(t + HOLD_S["expected"], 2)
        if verdict:
            steps.append([t, f"{w['result']}: {w[verdict]}" + (f" — {actual}" if actual else "")])
            t = round(t + HOLD_S["result"], 2)
        self._write_steps(steps, t)
        subprocess.run([PY_PIL, f"{BASE}/caption.py", self.raw, self.steps_path, self.video, self.title], check=True)
        if self.sheet:
            rows = max(1, -(-int(t / SHEET_EVERY_S + 1) // SHEET_COLUMNS))
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", self.video, "-vf",
                            f"fps=1/{SHEET_EVERY_S},scale={SHEET_TILE_W}:-2,tile={SHEET_COLUMNS}x{rows}",
                            "-frames:v", "1", self.sheet], check=True)
        os.remove(self.raw)
        if os.path.exists(f"{self.raw}.log"):
            os.remove(f"{self.raw}.log")
        self.steps, self.end, self.status = steps, t, "rendered"
        self.save()
        print("rendered", self.video)

    def check(self):
        """Validate the finished video; extract the frame of the last caption for a human look."""
        problems = []
        if not os.path.exists(self.video):
            problems.append(f"missing {self.video}")
        for d in {self.video_dir, self.image_dir, self.others_dir}:
            for f in os.listdir(d):
                if f.startswith(" ") or f.startswith(".raw") or (f.endswith(".mp4") and f.startswith(".")):
                    problems.append(f"stray file {d}/{f!r}")
        if not problems:
            dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                        "default=nw=1:nk=1", self.video], capture_output=True, text=True).stdout)
            if dur < self.end - 0.5 or dur > self.end + 5.0:  # cut short, or a long dead tail
                problems.append(f"duration {dur:.1f}s, steps say {self.end:.1f}s")
            last = self.steps[-1][0] if self.steps else 0
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(min(last + 1.0, dur - 0.1)), "-i",
                            self.video, "-frames:v", "1", self.check_frame], check=True)
        print("check:", "OK" if not problems else "PROBLEMS", *problems, sep="\n  ")
        if not problems:
            print(f"  look at {self.check_frame}: the screen must show what the last caption says "
                  f"({self.steps[-1][1][:80] if self.steps else ''})")
        return not problems

    def sheet_only(self):
        """A video that is not kept (P2/P3 Pass): contact sheet straight from the raw file, then drop the raw."""
        if not os.path.exists(self.raw):
            sys.exit(f"no raw recording at {self.raw}")
        if self.sheet:
            rows = max(1, -(-int(self.end / SHEET_EVERY_S + 1) // SHEET_COLUMNS))
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", self.raw, "-vf",
                            f"fps=1/{SHEET_EVERY_S},scale={SHEET_TILE_W}:-2,tile={SHEET_COLUMNS}x{rows}",
                            "-frames:v", "1", self.sheet], check=True)
        os.remove(self.raw)
        if os.path.exists(f"{self.raw}.log"):
            os.remove(f"{self.raw}.log")
        self.status = "sheet-only"
        self.save()
        print("sheet only", self.sheet)

    def prune(self):
        if os.path.exists(self.video):
            os.remove(self.video)
        print("pruned", self.video, "(sheet and steps kept)")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["start", "step", "shot", "stop", "render", "check", "prune"])
    ap.add_argument("folder")
    ap.add_argument("arg", nargs="?")
    ap.add_argument("--variant")
    ap.add_argument("--layout", choices=["bug", "case"], default="bug")
    ap.add_argument("--title")
    ap.add_argument("--verdict", choices=list(WORDS["en"])[2:])
    ap.add_argument("--expected")
    ap.add_argument("--actual")
    a = ap.parse_args()
    if a.cmd == "start":
        Rec(a.folder, a.variant, a.layout, None, a.title).start()
        return
    r = Rec.load(a.folder, a.variant)
    if a.cmd == "step":
        r.step(a.arg)
    elif a.cmd == "shot":
        print(r.shot(a.arg))
    elif a.cmd == "stop":
        r.stop(a.title)
    elif a.cmd == "render":
        r.render(a.verdict, a.expected, a.actual)
    elif a.cmd == "check":
        sys.exit(0 if r.check() else 1)
    elif a.cmd == "prune":
        r.prune()


if __name__ == "__main__":
    main()
