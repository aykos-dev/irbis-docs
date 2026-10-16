"""Blur personal data (a phone number, a name) in a recording before it leaves the machine.
Use it for any recording that shows a real person's data before it leaves this machine. Dev test accounts with
synthetic data (user_1, +998XXXXXXXXX) need no blur.

usage: blur.py <in.mp4> <out.mp4> --template <frame.png>:x0,y0,x1,y1 [--template …]
       blur.py --check <video.mp4> --template …          print the times the text is still found
A template is a box cut from a frame of the same kind of video (extract one with
`ffmpeg -ss T -i video.mp4 -frames:v 1 frame.png`) around the text to hide. Every frame is searched
(normalised cross-correlation, any height, ±4 px sideways) and the matched area is blurred while it is on screen.
The original stays untouched. Run with ~/.claude/venvs/qa/bin/python (numpy, Pillow).
"""
import argparse
import json
import subprocess

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from PIL import Image

THRESHOLD, PAD, FPS_BLUR, FPS_CHECK = 0.72, 8, 4, 5


def probe(path):
    s = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height", "-of", "json", path], capture_output=True,
                                  text=True).stdout)["streams"][0]
    return s["width"], s["height"]


def load(specs):
    out = []
    for spec in specs:
        path, box = spec.rsplit(":", 1)
        x0, y0, x1, y1 = map(int, box.split(","))
        out.append((x0, np.asarray(Image.open(path).convert("L"), dtype=np.float32)[y0:y1, x0:x1]))
    return out


def frames(path, fps, w, h):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps}", "-f", "rawvideo",
                          "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
    i = 0
    while len(buf := p.stdout.read(w * h)) == w * h:
        yield i / fps, np.frombuffer(buf, dtype=np.uint8).reshape(h, w).astype(np.float32)
        i += 1


def find(frame, templates):
    hits = []
    for x0, t in templates:
        th, tw = t.shape
        tz = (t - t.mean()) / (t.std() + 1e-6)
        best = (-1.0, 0, 0)
        for x in range(max(0, x0 - 4), min(frame.shape[1] - tw, x0 + 4) + 1, 2):
            win = sliding_window_view(frame[:, x:x + tw], (th, tw))[::2, 0]
            m, s = win.mean(axis=(1, 2), keepdims=True), win.std(axis=(1, 2), keepdims=True) + 1e-6
            ncc = (((win - m) / s) * tz).mean(axis=(1, 2))
            k = int(ncc.argmax())
            if ncc[k] > best[0]:
                best = (float(ncc[k]), x, k * 2)
        if best[0] >= THRESHOLD:
            hits.append((best[1], best[2], tw, th, best[0]))
    return hits


def detect(path, templates, fps):
    w, h = probe(path)
    return [(t, hit) for t, f in frames(path, fps, w, h) for hit in find(f, templates)]


def blur(src, dst, templates):
    boxes = []
    for t, (x, y, w, h, _) in detect(src, templates, FPS_BLUR):
        b = boxes[-1] if boxes else None
        if b and abs(b[2] - y) <= 4 and abs(b[1] - x) <= 4 and t - b[4] <= 1.5 / FPS_BLUR:
            b[4] = t
        else:
            boxes.append([t, x, y, (w, h), t])
    if not boxes:
        subprocess.run(["cp", src, dst], check=True)
        print("nothing found — copied unchanged")
        return
    graph, last = [], "0:v"
    for i, (t0, x, y, (w, h), t1) in enumerate(boxes):
        a, b = max(0.0, t0 - 0.35), t1 + 0.35
        bx, by, bw, bh = max(0, x - PAD), max(0, y - PAD), w + 2 * PAD, h + 2 * PAD
        graph.append(f"[0:v]crop={bw}:{bh}:{bx}:{by},boxblur=luma_radius=9:luma_power=4:"
                     f"chroma_radius=9:chroma_power=2[b{i}]")
        graph.append(f"[{last}][b{i}]overlay={bx}:{by}:enable='between(t,{a:.2f},{b:.2f})'[v{i}]")
        last = f"v{i}"
        print(f"blur {a:6.2f}–{b:6.2f}s at x={bx} y={by} {bw}x{bh}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", ";".join(graph), "-map", f"[{last}]",
                    "-c:v", "libx264", "-crf", "23", "-pix_fmt", "yuv420p", "-movflags", "+faststart", dst], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--template", action="append", required=True)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    tpl = load(a.template)
    if a.check:
        left = detect(a.paths[0], tpl, FPS_CHECK)
        print("still found:", [(round(t, 1), round(h[4], 2)) for t, h in left] or "none")
    else:
        blur(a.paths[0], a.paths[1], tpl)


if __name__ == "__main__":
    main()
