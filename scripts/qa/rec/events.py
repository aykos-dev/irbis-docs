"""Print the app's QA events from `adb logcat -d -v time`.

The app (dev/staging builds only) logs one line per event through src/shared/utils/qaLog.ts:
    IRBIS_QA {"event": "checkin_succeeded", "xp_awarded": 50}
Names and non-personal props only — never tokens, phone numbers or precise coordinates.

usage: adb logcat -d -v time | python3 -I events.py [name_filter]
output: "<time> <event> {props}" per line
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import CFG  # noqa: E402

TAG = CFG["event_tag"] + " "


def parse(line):
    """(time, name, props) from one logcat line, or None."""
    i = line.find(TAG)
    if i < 0:
        return None
    try:
        payload = json.loads(line[i + len(TAG):].strip())
    except ValueError:
        return None
    name = payload.pop("event", "")
    return line[6:18], name, payload


if __name__ == "__main__":
    needle = sys.argv[1] if len(sys.argv) > 1 else ""
    for line in sys.stdin:
        ev = parse(line)
        if ev and needle in ev[1]:
            print(ev[0], ev[1], json.dumps(ev[2], ensure_ascii=False))
