"""Turn source-prepped.png into a self-typing, monochrome ASCII SVG."""
import os
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source-prepped.png"
OUT = ROOT / "avi-ascii.svg"

RAMP = " .`:-=+*cs#%@"      # bright (sparse) -> dark (dense)
COLS = 110                  # characters per row
CHAR_W = 5.5                # px per character
CHAR_H = 11.0               # px per row (monospace glyphs are ~2x taller than wide)
FONT_SIZE = 10
FILL = "#c9d1d9"            # one light-gray colour
BG = "#0d1117"
ROW_DELAY = 0.07            # seconds between rows
ROW_DUR = 0.45              # seconds for one row to wipe in
STATIC = os.environ.get("STATIC") == "1"


def load_cropped():
    img = Image.open(SRC).convert("L")
    a = np.array(img)
    ys, xs = np.where(a < 245)              # everything that isn't background white
    pad = 12
    box = (max(xs.min() - pad, 0), max(ys.min() - pad, 0),
           min(xs.max() + pad, img.width), min(ys.max() + pad, img.height))
    return img.crop(box)


def to_rows(img):
    w, h = img.size
    rows = max(1, round(COLS * (h / w) * (CHAR_W / CHAR_H)))
    small = img.resize((COLS, rows), Image.LANCZOS)
    a = np.array(small).astype(float) / 255.0
    fg = a[a < 0.96]                         # stretch levels using subject pixels only
    lo, hi = np.percentile(fg, 2), np.percentile(fg, 98)
    a = np.clip((a - lo) / (hi - lo), 0, 1)
    a = a ** 0.95                            # tuned so face detail survives against dark hair and gray hoodie
    idx = np.clip(((1 - a) * (len(RAMP) - 1)).round().astype(int), 0, len(RAMP) - 1)
    return ["".join(RAMP[i] for i in row).rstrip() for row in idx]


def build_svg(lines):
    pad = 12
    W = COLS * CHAR_W + pad * 2
    H = len(lines) * CHAR_H + pad * 2
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
           f'viewBox="0 0 {W:.0f} {H:.0f}">',
           f'<rect width="100%" height="100%" rx="8" fill="{BG}"/>', "<defs>"]
    if not STATIC:
        for i in range(len(lines)):
            b = i * ROW_DELAY
            out.append(
                f'<clipPath id="c{i}"><rect x="{pad}" y="{pad + i * CHAR_H:.1f}" width="0" '
                f'height="{CHAR_H}"><animate attributeName="width" from="0" to="{COLS * CHAR_W}" '
                f'begin="{b:.2f}s" dur="{ROW_DUR}s" fill="freeze"/></rect></clipPath>')
    out.append("</defs>")
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        y = pad + (i + 1) * CHAR_H - 2.5
        clip = "" if STATIC else f' clip-path="url(#c{i})"'
        out.append(
            f'<text x="{pad}" y="{y:.1f}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
            f'font-size="{FONT_SIZE}" fill="{FILL}" xml:space="preserve" '
            f'textLength="{len(line) * CHAR_W:.1f}" lengthAdjust="spacing"{clip}>{escape(line)}</text>')
        if not STATIC:   # block cursor riding the wipe edge
            b = i * ROW_DELAY
            out.append(
                f'<rect x="{pad}" y="{pad + i * CHAR_H + 1:.1f}" width="{CHAR_W}" height="{CHAR_H - 2}" '
                f'fill="{FILL}" opacity="0"><animate attributeName="x" from="{pad}" to="{pad + COLS * CHAR_W}" '
                f'begin="{b:.2f}s" dur="{ROW_DUR}s" fill="freeze"/>'
                f'<animate attributeName="opacity" values="0.9;0.9;0" keyTimes="0;0.95;1" '
                f'begin="{b:.2f}s" dur="{ROW_DUR}s" fill="freeze"/></rect>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    lines = to_rows(load_cropped())
    OUT.write_text(build_svg(lines), encoding="utf-8")
    print(f"Wrote {OUT.name}: {COLS} x {len(lines)} characters")
