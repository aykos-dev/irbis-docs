"""Device helpers for Irbis QA case and repro scripts (Android over adb). The recorder is rec.py;
Rec is re-exported here so a script can import everything from drv.

Speed rules: no fixed sleeps — wait for the next state (UI text, testID, QA event) with a timeout.
UI dumps go through uiautomator2 when importable (QA venv, ~0.3 s), else one `adb exec-out` call (~0.7 s).
Run scripts with ~/.claude/venvs/qa/bin/python.

Finding elements: RN `testID` shows up as the node's resource-id, so `tap("spots.checkin-button", exact=True)`
is the stable way to reach an element; visible text is the fallback (it changes with the locale).

A bug's script lives in qa/<slug>/bugs/D{n}_{name}/others/repro{__variant}.py and passes the bug folder to Rec:
  FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  r = Rec(FOLDER, variant); r.start(); r.step("Step 1: …"); r.shot("01_home"); r.stop(TITLE)
then, after looking at the evidence: rec.py render FOLDER [--variant V] --verdict … ; rec.py check FOLDER.

Location: mockloop.sh re-sends the point in POINT_FILE every second; point() changes it.
Device conditions (network, font scale, dark mode, rotation) are restored by `session.py down`.
"""
import atexit
import html
import os
import re
import subprocess
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import CACHE, CFG  # noqa: E402
from events import parse  # noqa: E402
from rec import Rec  # noqa: E402,F401  (re-export)

POINT_FILE = os.environ.get("QA_POINT", f"{CACHE}/point.txt")
PKG = CFG["package"]
POLL_S = 0.2


# ---------- adb ----------
def sh(*args):
    return subprocess.run(["adb", "shell", *args], capture_output=True, text=True).stdout


def locked():
    return "isKeyguardShowing=true" in sh("dumpsys", "window")


def device_ready():
    """None when a device is attached and unlocked, else the reason."""
    if subprocess.run(["adb", "get-state"], capture_output=True, text=True).stdout.strip() != "device":
        return "no Android device on adb — connect the phone (adb devices) and retry"
    if locked():
        return "the phone is locked — unlock it and retry"
    return None


# ---------- UI ----------
_u2 = None


def _device():
    global _u2
    if _u2 is None:
        try:
            import uiautomator2
            _u2 = uiautomator2.connect()
        except Exception:  # not in the venv, or the agent failed: fall back to adb
            _u2 = False
    return _u2


def _xml():
    d = _device()
    if d:
        try:
            return d.dump_hierarchy()
        except Exception:
            pass
    return subprocess.run(["adb", "exec-out", "uiautomator", "dump", "/dev/tty"],
                          capture_output=True, text=True).stdout


def nodes():
    out = []
    for m in re.finditer(r"<node [^>]*>", _xml()):
        n = m.group(0)
        get = lambda k: html.unescape((re.search(" " + k + r'="([^"]*)"', n) or [None, ""])[1])  # noqa: E731
        b = re.findall(r"\d+", get("bounds"))
        if len(b) != 4:
            continue
        x1, y1, x2, y2 = map(int, b)
        rid = get("resource-id")
        out.append({"text": get("text"), "desc": get("content-desc"), "rid": rid.split(":id/")[-1],
                    "x": (x1 + x2) // 2, "y": (y1 + y2) // 2, "y1": y1, "b": (x1, y1, x2, y2), "cls": get("class"),
                    "enabled": get("enabled"), "selected": get("selected"), "checked": get("checked"),
                    "focused": get("focused")})
    return out


def find(needle, exact=False, ns=None):
    """First node whose text, content-desc or testID matches."""
    for n in ns if ns is not None else nodes():
        for v in (n["text"], n["desc"], n["rid"]):
            if (v == needle) if exact else (needle and needle in v):
                return n
    return None


def has(needle, exact=False):
    return find(needle, exact) is not None


def wait(needle, timeout=20, exact=False):
    """True as soon as a node with this text / content-desc / testID is on screen."""
    end = time.time() + timeout
    while True:
        if has(needle, exact):
            return True
        if time.time() > end:
            return False
        time.sleep(POLL_S)


def wait_any(needles, timeout=20):
    """The first of several texts / testIDs that appears, or None."""
    end = time.time() + timeout
    while True:
        ns = nodes()
        for nd in needles:
            if find(nd, ns=ns):
                return nd
        if time.time() > end:
            return None
        time.sleep(POLL_S)


def wait_gone(needle, timeout=20):
    end = time.time() + timeout
    while time.time() < end:
        if not has(needle):
            return True
        time.sleep(POLL_S)
    return False


def tap(needle, exact=False, timeout=10):
    end = time.time() + timeout
    while True:
        n = find(needle, exact)
        if n:
            sh("input", "tap", str(n["x"]), str(n["y"]))
            return n
        if time.time() > end:
            raise RuntimeError(f"not found: {needle}")
        time.sleep(POLL_S)


def type_text(text):
    """Type into the focused field (adb input text: spaces as %s, shell metacharacters escaped)."""
    safe = re.sub(r"([\\'\"`$&|;<>()])", r"\\\1", text).replace(" ", "%s")
    sh("input", "text", safe)


def swipe(x1, y1, x2, y2, ms=300):
    sh("input", "swipe", str(x1), str(y1), str(x2), str(y2), str(ms))


def scroll_down():
    w, h = screen_size()
    swipe(w // 2, int(h * 0.75), w // 2, int(h * 0.3))


def screen_size():
    m = re.search(r"(\d+)x(\d+)", sh("wm", "size"))
    return (int(m.group(1)), int(m.group(2))) if m else (1080, 2400)


def overlaps(a, b):
    """Two nodes' bounds intersect (e.g. an input hidden behind the keyboard or a toast over a button)."""
    ax1, ay1, ax2, ay2 = a["b"]
    bx1, by1, bx2, by2 = b["b"]
    return ax1 < bx2 and bx1 < ax2 and ay1 < by2 and by1 < ay2


def keyboard_shown():
    return "mInputShown=true" in sh("dumpsys", "input_method")


def keyboard_top():
    """Y of the keyboard's top edge in screen pixels, or None when it is hidden."""
    if not keyboard_shown():
        return None
    m = re.search(r"touchableRegion=SkRegion\(\(\d+,(\d+),\d+,\d+\)\)", sh("dumpsys", "window", "InputMethod"))
    return int(m.group(1)) if m else None


# ---------- QA events (IRBIS_QA lines in logcat, dev/staging builds) ----------
class EventStream:
    """Reads `adb logcat` in the background; wait_event() returns as soon as an event arrives."""

    def __init__(self):
        self.events, self.lock = [], threading.Lock()
        self.proc = subprocess.Popen(["adb", "logcat", "-v", "time"], stdout=subprocess.PIPE,
                                     stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, text=True, errors="replace")
        atexit.register(self.proc.kill)  # an orphaned logcat would hold the caller's pipe open
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        for line in self.proc.stdout:
            ev = parse(line)
            if ev:
                with self.lock:
                    self.events.append((time.time(), ev[1], ev[2]))

    def since(self, t0, name=None):
        with self.lock:
            return [(t, n, p) for t, n, p in self.events if t >= t0 and (name is None or n == name)]


_stream = None


def events():
    global _stream
    if _stream is None:
        _stream = EventStream()
        time.sleep(0.5)
    return _stream


def mark():
    """A point in time to wait for events after (call it before the action)."""
    events()
    return time.time()


def wait_event(name, since, timeout=20, pred=None):
    """Props of the first `name` event after `since` matching pred(props), or None."""
    end = time.time() + timeout
    while True:
        for _, n, p in events().since(since, name):
            if pred is None or pred(p):
                return p
        if time.time() > end:
            return None
        time.sleep(POLL_S)


def no_event(name, since, window):
    """True when `name` did NOT occur within `window` seconds after `since` (waits out the window)."""
    end = since + window
    while time.time() < end:
        if events().since(since, name):
            return False
        time.sleep(POLL_S)
    return not events().since(since, name)


def crashed():
    """Fatal JS/native crash lines of the app in logcat (cleared when the recording started)."""
    log = subprocess.run(["adb", "logcat", "-d", "-v", "time", "-b", "crash,main"], capture_output=True,
                         text=True).stdout
    return [l for l in log.splitlines() if PKG in l and ("FATAL EXCEPTION" in l or "Fatal" in l)]


# ---------- location (mock) ----------
def point(lat, lng, acc=10, age=0):
    with open(POINT_FILE, "w") as f:
        f.write(f"{lat} {lng} {acc} {age}\n")
    time.sleep(1.2)  # mockloop.sh re-sends every second


def warm_cache(seconds=4):
    """Open Google Maps so Play Services caches the mock fix (needed on a real phone with Location Accuracy off)."""
    sh("monkey", "-p", "com.google.android.apps.maps", "-c", "android.intent.category.LAUNCHER", "1")
    time.sleep(seconds)


def decline_accuracy_prompt(rec=None, timeout=3):
    """Google 'Location Accuracy' resolution dialog appears because that setting is off for the mock."""
    if wait("No thanks", timeout=timeout):
        if rec:
            rec.step("Test setup: decline Google 'Location Accuracy' prompt (setting is off so the mock location is used)")
        tap("No thanks")
        wait_gone("No thanks", timeout=3)
        return True
    return False


def distance_m(lat1, lng1, lat2, lng2):
    """Haversine distance in metres — for choosing mock points at exact distances (BVA: 199 / 200 / 201 m)."""
    from math import asin, cos, radians, sin, sqrt
    p1, p2 = radians(lat1), radians(lat2)
    a = sin((p2 - p1) / 2) ** 2 + cos(p1) * cos(p2) * sin(radians(lng2 - lng1) / 2) ** 2
    return 2 * 6371008.8 * asin(sqrt(a))


def offset(lat, lng, metres_north=0.0, metres_east=0.0):
    """A point `metres_north` / `metres_east` away from (lat, lng)."""
    from math import cos, degrees, radians
    dlat = degrees(metres_north / 6371008.8)
    dlng = degrees(metres_east / (6371008.8 * cos(radians(lat))))
    return round(lat + dlat, 7), round(lng + dlng, 7)


# ---------- app ----------
def activity():
    return f"{PKG}/{CFG['activity']}"  # ".MainActivity" (relative) or a full class name


def launch():
    """Bring the app to the front (am start; monkey as a fallback)."""
    out = sh("am", "start", "-n", activity())
    if "Error" in out:
        sh("monkey", "-p", PKG, "-c", "android.intent.category.LAUNCHER", "1")


def relaunch():
    sh("am", "force-stop", PKG)
    launch()


def deep_link(url):
    sh("am", "start", "-a", "android.intent.action.VIEW", "-d", url, PKG)


def home_key():
    sh("input", "keyevent", "3")


def back():
    sh("input", "keyevent", "4")


def app_version():
    out = sh("dumpsys", "package", PKG)
    name = (re.search(r"versionName=(\S+)", out) or [None, "?"])[1]
    code = (re.search(r"versionCode=(\d+)", out) or [None, "?"])[1]
    return name, code


def open_app_at(rec, lat, lng, label, step_no, acc=10, age=0, expect=None, retries=1, warm=True):
    """Cold start at a mock place; returns the app's location event props (None if never seen).
    Waits for the app's own reading of the mock point instead of fixed sleeps; re-warms Maps once if needed."""
    point(lat, lng, acc, age)
    rec.step(f"Setup: phone location = {label}")
    fix = None
    for attempt in range(retries + 1):
        if warm:
            warm_cache(4 if attempt == 0 else 6)
        t0 = mark()
        if attempt == 0:
            rec.step(f"Step {step_no}: Open the app")
        relaunch()
        decline_accuracy_prompt(rec, timeout=4)
        fix = wait_event(CFG["location_event"], t0, timeout=20, pred=lambda p: p.get("is_mocked", True))
        if fix:
            break
    if expect:
        wait(expect, timeout=20)
    return fix


def background_and_return(rec, step_no, new_point=None, label=None, away_s=3):
    rec.step(f"Step {step_no}: Send the app to the background (Home button)")
    home_key()
    if new_point:
        point(*new_point)
        rec.step(f"Step {step_no + 1}: The phone moves to {label}")
        warm_cache()
        step_no += 1
    else:
        time.sleep(away_s)
    rec.step(f"Step {step_no + 1}: Return to the app")
    launch()
    decline_accuracy_prompt(rec, timeout=2)
    return step_no + 2


def process_death(rec=None, step_no=None):
    """Background the app, let Android kill its process, return — state must be restored (standards: restore)."""
    if rec:
        rec.step(f"Step {step_no}: Background the app and let Android kill its process")
    home_key()
    time.sleep(1)
    sh("am", "kill", PKG)
    time.sleep(1)
    launch()


# ---------- device conditions (engineering-standards checks; session.py down restores them) ----------
def set_network(wifi=None, data=None):
    """Offline = set_network(False, False). Wait for the app's offline banner after this."""
    if wifi is not None:
        sh("svc", "wifi", "enable" if wifi else "disable")
    if data is not None:
        sh("svc", "data", "enable" if data else "disable")
    time.sleep(2)


def font_scale(scale):
    """1.0 normal; 1.3 large; 2.0 largest accessibility size on most devices."""
    sh("settings", "put", "system", "font_scale", str(scale))
    time.sleep(1.5)


def dark_mode(on):
    sh("cmd", "uimode", "night", "yes" if on else "no")
    time.sleep(1.5)


def rotate(landscape):
    sh("settings", "put", "system", "accelerometer_rotation", "0")
    sh("settings", "put", "system", "user_rotation", "1" if landscape else "0")
    time.sleep(1.5)


def permission(name, grant):
    """e.g. permission('android.permission.ACCESS_FINE_LOCATION', False). Revoking restarts the app process."""
    sh("pm", "grant" if grant else "revoke", PKG, name)


def reset_permission(name):
    """Back to 'ask every time' so the app shows its rationale + system prompt again."""
    sh("pm", "revoke", PKG, name)
    sh("pm", "clear-permission-flags", PKG, name, "user-set", "user-fixed")
