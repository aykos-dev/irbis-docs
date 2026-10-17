import os, sys
from drv import *  # noqa
from _std import screen  # noqa

META = {"title": "Dark mode uses the night tokens", "priority": "P3", "group": "Standards",
        "requirement": "engineering-standards §5/§8 — light + dark from tokens", "env": "Android · auto (adb)",
        "precondition": ["screen reachable"], "steps": ["Dark mode on", "Open the screen"],
        "expected": ["Screen background is the night token #131D22 — screenshot (pixel check)"],
        "caption": {"expected": "night background"}}
NIGHT = (0x13, 0x1D, 0x22)


def run(c):
    open_screen, root = screen(c)
    c.step(1, "Dark mode on")
    dark_mode(True)
    try:
        c.step(2, "Open the screen")
        c.checkpoint("screen opened", open_screen(c), root)
        shot = c.shot("dark", focus=root)
        from PIL import Image
        im = Image.open(os.path.join(c.dir, shot)).convert("RGB")
        px = im.getpixel((6, im.height // 2))
        c.result(1, all(abs(a - b) <= 12 for a, b in zip(px, NIGHT)), f"background pixel {px} vs #131D22", [shot])
    finally:
        dark_mode(False)
