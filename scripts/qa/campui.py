#!/usr/bin/env python3
"""Tiny multi-device UI CLI for the Campfire QA pass (wraps rec/drv.py; run with the QA venv python).

  campui.py <serial|A|B> ids                 # compact node list: testID | text | enabled
  campui.py <dev> texts                      # visible texts, one line
  campui.py <dev> tap <needle> [exact]       # tap by testID / text / content-desc
  campui.py <dev> wait <needle> [timeout]    # exit 1 if not shown in time
  campui.py <dev> hold <needle> <ms>         # press and hold (hold-to-reveal cards, long-press)
  campui.py <dev> shot <png path>            # screenshot
A = emulator-5554 (host), B = emulator-5556 (joiner); override with CAMP_A / CAMP_B.
"""
import os
import subprocess
import sys

ALIAS = {"A": os.environ.get("CAMP_A", "emulator-5554"), "B": os.environ.get("CAMP_B", "emulator-5556")}
serial = ALIAS.get(sys.argv[1], sys.argv[1])
os.environ["ANDROID_SERIAL"] = serial
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "rec"))
import drv  # noqa: E402

cmd, args = sys.argv[2], sys.argv[3:]
if cmd == "ids":
    for n in drv.nodes():
        # app testIDs contain a dot; system UI ids (status bar) do not
        if "." in n["rid"] or (not n["rid"] and (n["text"] or n["desc"])):
            en = "" if n["enabled"] == "true" else " [disabled]"
            print(f'{n["rid"]} | {n["text"] or n["desc"]}{en} @{n["x"]},{n["y"]}')
elif cmd in ("scan", "find"):
    # scan: scroll top→bottom printing each app node once; find <needle>: scroll until it shows, then tap
    w, h = drv.screen_size()
    for _ in range(6):
        drv.sh("input", "swipe", str(w // 2), str(h // 4), str(w // 2), str(h * 3 // 4), "150")
    seen, stale = [], 0
    for _ in range(15):
        ns = drv.nodes()
        if cmd == "find":
            n = drv.find(args[0], exact=True, ns=ns)
            if n and h * 0.12 < n["y"] < h * 0.88:
                drv.sh("input", "tap", str(n["x"]), str(n["y"]))
                print(f"tapped {args[0]}")
                sys.exit(0)
        new = 0
        for n in ns:
            if "." in n["rid"] or (not n["rid"] and n["text"]):
                key = f'{n["rid"]} | {n["text"] or n["desc"]}{"" if n["enabled"] == "true" else " [disabled]"}'
                if key not in seen and "nav." not in key:
                    seen.append(key)
                    new += 1
        stale = stale + 1 if new == 0 else 0
        if stale >= 2:
            break
        drv.sh("input", "swipe", str(w // 2), str(h * 7 // 10), str(w // 2), str(h * 3 // 10), "400")
    if cmd == "find":
        sys.exit(f"not found: {args[0]}")
    print("\n".join(seen))
elif cmd == "texts":
    print(" · ".join(n["text"] or n["desc"] for n in drv.nodes() if (n["text"] or n["desc"])))
elif cmd == "tap":
    n = drv.tap(args[0], exact=len(args) > 1)
    print(f'tapped {n["rid"] or n["text"]}')
elif cmd == "wait":
    ok = drv.wait(args[0], timeout=float(args[1]) if len(args) > 1 else 20)
    print("shown" if ok else "NOT shown")
    sys.exit(0 if ok else 1)
elif cmd == "hold":
    n = drv.find(args[0])
    if not n:
        sys.exit(f"not found: {args[0]}")
    drv.sh("input", "swipe", str(n["x"]), str(n["y"]), str(n["x"]), str(n["y"]), args[1])
    print("held")
elif cmd == "shot":
    with open(args[0], "wb") as f:
        f.write(subprocess.run(["adb", "-s", serial, "exec-out", "screencap", "-p"], capture_output=True).stdout)
    print(args[0])
else:
    sys.exit(f"unknown {cmd}")
