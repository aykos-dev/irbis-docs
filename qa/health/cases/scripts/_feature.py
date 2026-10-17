"""health feature: PLAN (rendered into Test_health.md), SCREENS (for the standards suite), shared helpers."""
import json
import os
import subprocess
import time
import urllib.error
import urllib.request

from drv import PKG, deep_link, has, nodes, relaunch, sh, wait  # noqa: F401

from config import DOCS  # noqa: E402

API_DIR = os.path.join(os.path.dirname(DOCS), "irbis-api")
HEALTH_URL = "http://localhost:3000/health"
PORT = "tcp:3000"


def api_health():
    """(http status, body dict) from the Mac's side, or (None, None) when the API is not listening."""
    try:
        with urllib.request.urlopen(HEALTH_URL, timeout=5) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")
    except (urllib.error.URLError, OSError):
        return None, None


def db(running):
    """Start or stop the Postgres container the API uses, then wait until /health agrees (≤ 20 s)."""
    subprocess.run(["docker", "compose", "start" if running else "stop", "db"], cwd=API_DIR,
                   capture_output=True, text=True)
    want = "up" if running else "down"
    end = time.time() + 20
    while time.time() < end:
        _, body = api_health()
        if body and body.get("db") == want:
            return body
        time.sleep(0.5)
    return api_health()[1]


def reverse(on):
    """Forward the phone's localhost:3000 to the Mac's API (or remove the forward)."""
    if on:
        subprocess.run(["adb", "reverse", PORT, PORT], capture_output=True)
    else:
        subprocess.run(["adb", "reverse", "--remove", PORT], capture_output=True)


def card_texts():
    """All visible texts on screen, in order (for asserting copy)."""
    return [n["text"] for n in nodes() if n["text"]]


def app_locale(code):
    sh("cmd", "locale", "set-app-locales", PKG, "--locales", code)


PLAN = {
    "spec": "features/health.md",
    "resources": [("Android", "emulator pixel-8a emulating the S25 Ultra (session.py up), or the phone; devRelease APK"),
                  ("Backend", "irbis-api `npm run start:dev` on :3000 + Postgres container `db`; `adb reverse tcp:3000 tcp:3000`")],
    "test_data": [("API-UP", "API + DB running", "`curl localhost:3000/health` → status ok"),
                  ("DB-DOWN", "DB stopped, API running", "`docker compose stop db` (irbis-api)"),
                  ("API-GONE", "API unreachable from the device", "`adb reverse --remove tcp:3000`")],
}


def open_status(c=None):
    """Status is a dev/staging Debug screen since `auth` (AC10): cold start, then the deep link."""
    reverse(True)
    relaunch()
    time.sleep(1)
    deep_link("irbis://debug/status")
    return wait("health.status-card", 15, exact=True) and wait("health.api-chip", 8, exact=True)


SCREENS = {"status": {"open": open_status, "root": "health.status-card"}}
