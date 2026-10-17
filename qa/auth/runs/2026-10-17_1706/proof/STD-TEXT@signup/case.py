import os, sys, time
from drv import *  # noqa
from _std import composite, screen, untranslated  # noqa

META = {"title": "Copy is translated and layout survives long text", "priority": "P2", "group": "Standards",
        "requirement": "engineering-standards §12/§13 — i18n, +40% text, largest font", "env": "Android · auto (adb)",
        "precondition": ["screen reachable"],
        "steps": ["Russian, font 1.15 — open the screen", "Uzbek, font 1.15 — open the screen",
                  "English, font 2.0 — open the screen"],
        "expected": ["No English catalog string left on screen in Russian or Uzbek — UI tree",
                     "Nothing clipped or overflowing its container in any of the three — one composite crop (human)"],
        "caption": {"expected": "translated, nothing overflows"}}


def run(c):
    open_screen, root = screen(c)
    prev = sh("settings", "get", "system", "font_scale").strip() or "1.0"
    left, crops = {}, []
    try:
        for n, (lang, font) in enumerate((("ru", 1.15), ("uz", 1.15), ("en", 2.0)), 1):
            c.step(n, f"{lang}, font {font} — open the screen")
            font_scale(font)
            sh("cmd", "locale", "set-app-locales", PKG, "--locales", lang)
            c.checkpoint(f"screen opened ({lang})", open_screen(c), root)
            time.sleep(1)
            if lang != "en":
                left[lang] = untranslated([nd["text"] for nd in nodes() if nd["text"]])
            shot = c.shot(f"{lang}_font{font}", focus=root)
            crops.append(os.path.join(c.run_dir, "proof", "_run", "review", c.meta["tc"], shot))
        c.result(1, not any(left.values()), f"untranslated: {left}")
        comp = composite(crops, os.path.join(c.run_dir, "proof", "_run", "review", c.meta["tc"], "_composite.png"))
        c.result(2, None, f"judge {os.path.basename(comp) if comp else 'the crops'}: ru · uz · en@2.0 side by side",
                 [os.path.basename(p) for p in crops])
    finally:
        sh("cmd", "locale", "set-app-locales", PKG, "--locales", "en")
        font_scale(prev)
