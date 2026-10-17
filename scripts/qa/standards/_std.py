"""Helpers for the standards suite (STD-*): one script per engineering-standards check, run on any screen a feature
lists in its _feature.SCREENS = {"name": {"open": fn(c) -> bool, "root": "<testID of the screen's main area>"}}.
Run as `runcase.py run <run dir> STD-DARK@<screen>`."""
import glob
import json
import os
import re

from config import DOCS

APP_I18N = os.path.join(os.path.dirname(DOCS), "irbis-app", "src", "shared", "i18n")
ALLOW = {"IRBIS", "Irbis", "API", "dev", "staging"}


def screen(c):
    import _feature
    s = _feature.SCREENS[c.meta["screen"]]
    return s["open"], s["root"]


def english_strings():
    """Every English catalog value as a regex (interpolations %{x} match anything)."""
    out = []
    for f in glob.glob(os.path.join(APP_I18N, "en", "*.json")):
        def walk(v):
            if isinstance(v, dict):
                for x in v.values():
                    walk(x)
            elif isinstance(v, str) and re.search(r"[A-Za-z]{3,}", v):
                out.append(re.compile("^" + re.sub(r"%\\\{\w+\\\}", ".*", re.escape(v)) + "$"))
        walk(json.load(open(f, encoding="utf-8")))
    return out


def untranslated(texts):
    """On-screen texts that are exactly an English catalog string (or contain no letters of the locale)."""
    en = english_strings()
    return [t for t in texts if t not in ALLOW and not re.fullmatch(r"v\d+(\.\d+)*", t) and any(p.match(t) for p in en)]


def composite(paths, out, width=360):
    """Side-by-side image of several review crops — one image for a reviewer to read instead of several."""
    from PIL import Image
    ims = [Image.open(p) for p in paths if os.path.exists(p)]
    if not ims:
        return None
    ims = [i.resize((width, int(i.height * width / i.width))) for i in ims]
    s = Image.new("RGB", (width * len(ims) + 8 * (len(ims) - 1), max(i.height for i in ims)), "white")
    x = 0
    for i in ims:
        s.paste(i, (x, 0))
        x += width + 8
    s.save(out)
    return out
