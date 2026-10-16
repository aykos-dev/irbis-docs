"""Burn step captions from steps.tsv under a raw scrcpy recording (caption strip below the screen).
usage: <python with Pillow> caption.py <raw.mp4> <steps.tsv> <out.mp4> "<title>"
steps.tsv: "<seconds from record start>\t<caption>" per line, last line "<total>\tEND".
rec.py render calls this; run it by hand only to re-caption a raw file.
"""
import json
import os
import subprocess
import sys
import tempfile
import textwrap

from PIL import Image, ImageDraw, ImageFont

FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
STRIP_H = 300
RED, GREEN, GREY, AMBER = (255, 95, 95), (90, 220, 120), (170, 170, 170), (255, 190, 70)
# first matching prefix wins: specific verdicts before the bare "Result:" / "Natija:"
COLORS = {"Result: FIXED": GREEN, "Result: PASS": GREEN, "Result: NOT FIXED": RED, "Result: FAIL": RED,
          "Result:": AMBER, "Actual": RED, "Expected": GREEN, "Test setup": GREY, "Setup": GREY}


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height", "-of", "json", path], capture_output=True, text=True).stdout
    s = json.loads(out)["streams"][0]
    return s["width"], s["height"]


def strip(path, w, title, caption):
    img = Image.new("RGB", (w, STRIP_H), (18, 18, 18))
    d = ImageDraw.Draw(img)
    f_title = ImageFont.truetype(FONT_B, 22)
    f_text = ImageFont.truetype(FONT, 27)
    f_text_b = ImageFont.truetype(FONT_B, 27)
    d.text((18, 14), title, font=f_title, fill=(140, 140, 140))
    color = next((c for k, c in COLORS.items() if caption.startswith(k)), (255, 255, 255))
    head, _, rest = caption.partition(":")
    lines = textwrap.wrap(caption, width=max(20, w // 15))
    y = 56
    for i, line in enumerate(lines[:7]):
        font = f_text_b if i == 0 and rest else f_text
        d.text((18, y), line, font=font, fill=color)
        y += 34
    img.save(path)


def main():
    raw, steps, out, title = sys.argv[1:5]
    w, h = probe(raw)
    rows = [l.rstrip("\n").split("\t", 1) for l in open(steps, encoding="utf-8")]
    rows = [(float(t), c) for t, c in rows]
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                "default=nw=1:nk=1", raw], capture_output=True, text=True).stdout)
    # scrcpy writes no frames while the screen is static, so the file can end before the last step;
    # clone the last frame up to END so the final captions stay visible
    end_t = rows[-1][0]
    pad = max(0.0, round(end_t - dur + 0.5, 2))
    caps_dir = tempfile.mkdtemp(prefix="caps")
    os.makedirs(caps_dir, exist_ok=True)
    inputs, filters, prev = ["-i", raw], [f"[0:v]tpad=stop_mode=clone:stop_duration={pad},fps=30,pad={w}:{h + STRIP_H}:0:0:color=0x121212[v0]"], "v0"
    for i, (t, c) in enumerate(rows[:-1]):
        end = rows[i + 1][0]
        p = f"{caps_dir}/{i:02d}.png"
        strip(p, w, title, c)
        inputs += ["-loop", "1", "-i", p]
        nxt = f"v{i + 1}"
        filters.append(f"[{prev}][{i + 1}:v]overlay=0:{h}:shortest=1:enable='between(t,{t},{end})'[{nxt}]")
        prev = nxt
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filters), "-map", f"[{prev}]",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "26", "-preset", "veryfast",
           "-t", str(max(dur, end_t)), out]
    subprocess.run(cmd, check=True)
    for f in os.listdir(caps_dir):
        os.remove(f"{caps_dir}/{f}")
    os.rmdir(caps_dir)
    print("ok", out)


main()
