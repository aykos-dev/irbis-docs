import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa  (shared points/accounts/helpers of this feature)
except ImportError:
    pass

META = {
 "title": "Dark mode uses the night tokens",
 "group": "Supplementary",
 "priority": "P3",
 "env": "Android · auto (adb) · resources: API-UP",
 "plan": "Test_health.md",
 "anchor": "tc-008--p3--dark-mode-uses-the-night-tokens",
 "source": "standards §5/§8",
 "expected": [
  "Background is the Night token (#131D22) and cards #1C2A30; text readable; chips keep colour + icon + label — screenshot"
 ],
 "caption": {
  "expected": "Background is the Night token (#131D22) and cards #1C2A30; text readable; chips "
 },
 "plan_hash": "c1be9ec784"
}


def run(c):
    c.pre('API-UP')
    reverse(True)
    c.step(1, "Dark mode on, cold start")
    dark_mode(True)
    try:
        relaunch()
        c.checkpoint("status shown", wait("API is up", 15), card_texts()[:6])
        shot = c.shot("1_dark")
        from PIL import Image
        im = Image.open(os.path.join(c.dir, shot)).convert("RGB")
        bg = im.getpixel((10, im.height // 2))
        night = all(abs(a - b) <= 12 for a, b in zip(bg, (0x13, 0x1D, 0x22)))
        c.result(1, night, f"background pixel {bg} vs #131D22", [shot])
    finally:
        dark_mode(False)
