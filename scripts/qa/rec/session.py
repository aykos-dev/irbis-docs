"""Device session for QA runs: set the phone up before the first recording and put it back afterwards.

usage: session.py up [--mock] [--no-dnd]   record the current values, then: Show taps on, Do Not Disturb = total
                                           silence; with --mock also mock location (shell appop, gps/network/fused
                                           test providers, Google Location Accuracy off, mockloop.sh running)
       session.py down                     restore every value recorded by `up` (also network, font scale, dark
                                           mode and rotation that cases changed), stop mockloop, print the cleanup
                                           table (Markdown) for the run's / bugs' session notes
       session.py status
State: ~/.cache/irbis-qa/session.json.
"""
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import CACHE  # noqa: E402
from drv import device_ready, has, nodes, sh, tap  # noqa: E402

STATE = f"{CACHE}/session.json"
MOCKLOOP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mockloop.sh")
PROVIDERS = ("gps", "network", "fused")
ZEN = {"0": "off", "1": "priority", "2": "none", "3": "alarms"}
SETTINGS = (("system", "font_scale"), ("system", "accelerometer_rotation"), ("system", "user_rotation"),
            ("system", "show_touches"), ("global", "zen_mode"), ("global", "wifi_on"), ("global", "mobile_data"))


def accuracy_switch(want=None):
    """Read (and with want=True/False set) Settings → Location → Location services → Location Accuracy.
    Works with the device UI in English."""
    sh("am", "start", "-a", "android.settings.LOCATION_SOURCE_SETTINGS")
    time.sleep(2)
    if has("Location services"):
        tap("Location services")
        time.sleep(2)
    if has("Location Accuracy", exact=True):
        tap("Location Accuracy", exact=True)
        time.sleep(2.5)
    sw = [n for n in nodes() if "Switch" in n["cls"]]
    if not (has("Improve Location Accuracy") and sw):
        sh("input", "keyevent", "3")
        return None
    state = sw[0]["checked"] == "true"
    if want is not None and state != want:
        sh("input", "tap", str(sw[0]["x"]), str(sw[0]["y"]))
        time.sleep(2)
        state = [n for n in nodes() if "Switch" in n["cls"]][0]["checked"] == "true"
    sh("input", "keyevent", "3")
    return state


def get(ns, key):
    return sh("settings", "get", ns, key).strip()


def up(mock, dnd):
    if (why := device_ready()):
        sys.exit(why)
    if os.path.exists(STATE):
        sys.exit(f"a session is already open ({STATE}); run `session.py down` first")
    st = {"mock": mock, "dnd": dnd, "started": time.strftime("%Y-%m-%d %H:%M"),
          "settings": {f"{ns}/{k}": get(ns, k) for ns, k in SETTINGS},
          "night": sh("cmd", "uimode", "night").strip()}
    sh("settings", "put", "system", "show_touches", "1")
    if dnd:
        sh("cmd", "notification", "set_dnd", "none")
    if mock:
        st["mock_appop"] = sh("appops", "get", "com.android.shell", "android:mock_location").split(";")[0].split(":")[-1].strip()
        st["accuracy"] = accuracy_switch()
        if st["accuracy"]:
            accuracy_switch(False)
        sh("appops", "set", "com.android.shell", "android:mock_location", "allow")
        for p in PROVIDERS:
            sh("cmd", "location", "providers", "add-test-provider", p)
            sh("cmd", "location", "providers", "set-test-provider-enabled", p, "true")
        log = open(f"{CACHE}/mockloop.log", "w")
        st["mockloop_pid"] = subprocess.Popen(["bash", MOCKLOOP], stdout=log, stderr=subprocess.STDOUT,
                                              start_new_session=True).pid
    json.dump(st, open(STATE, "w"), indent=1)
    status()


def down():
    if not os.path.exists(STATE):
        sys.exit("no open session")
    st = json.load(open(STATE))
    rows = []
    if st.get("mock"):
        try:
            os.killpg(st["mockloop_pid"], 15)
        except ProcessLookupError:
            pass
        for p in PROVIDERS:
            sh("cmd", "location", "providers", "remove-test-provider", p)
        sh("appops", "set", "com.android.shell", "android:mock_location", st.get("mock_appop") or "default")
        rows.append(("Mock loop, test providers", "Stopped and removed"))
        rows.append(("`mock_location` appop for shell", f"`{st.get('mock_appop') or 'default'}` (as before)"))
        if st.get("accuracy") is None:
            rows.append(("Google Location Accuracy", "⚠️ could not be read at `up` — check it by hand"))
        else:
            now = accuracy_switch(st["accuracy"])
            rows.append(("Google Location Accuracy", f"{'On' if st['accuracy'] else 'Off'} (as before)"
                         if now == st["accuracy"] else "⚠️ could not be restored — set it by hand"))
    before = st.get("settings", {})
    wifi, data = before.get("global/wifi_on"), before.get("global/mobile_data")
    if wifi in ("0", "1", "2"):
        sh("svc", "wifi", "disable" if wifi == "0" else "enable")
    if data in ("0", "1"):
        sh("svc", "data", "enable" if data == "1" else "disable")
    for key, val in before.items():
        ns, k = key.split("/")
        if k in ("wifi_on", "mobile_data", "zen_mode"):
            continue
        if val in ("", "null"):
            sh("settings", "delete", ns, k)
        else:
            sh("settings", "put", ns, k, val)
    if st.get("night"):
        mode = "yes" if "yes" in st["night"] else "auto" if "auto" in st["night"] else "no"
        sh("cmd", "uimode", "night", mode)
    rows.append(("Network, font scale, rotation, show taps, dark mode", "Restored to the values before the session"))
    if st.get("dnd"):
        zen = before.get("global/zen_mode", "0")
        sh("cmd", "notification", "set_dnd", ZEN.get(zen, "off"))
        now = get("global", "zen_mode")
        rows.append(("Do Not Disturb", f"{ZEN.get(now, now)} (as before)" if now == zen
                     else f"⚠️ is {ZEN.get(now, now)}, was {ZEN.get(zen)}"))
    os.remove(STATE)
    print("| Item | State after the session |\n|---|---|")
    for k, v in rows:
        print(f"| {k} | {v} |")
    print("| Test data (spots, check-ins, profile edits) | add rows for what this session created or deleted |")


def status():
    if not os.path.exists(STATE):
        print("no open session")
        return
    print(json.dumps(json.load(open(STATE)), indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "up":
        up("--mock" in sys.argv, "--no-dnd" not in sys.argv)
    elif cmd == "down":
        down()
    else:
        status()
