"""data/contributions.json -> contrib-heatmap.svg (animated 53x7 grid)"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "data" / "contributions.json", ROOT / "contrib-heatmap.svg"

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
CELL, GAP, LEFT, TOP = 12, 3, 40, 52
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def level_of(d):
    lv = d["level"]
    return 5 if lv == 4 and d["count"] >= 15 else lv     # neon top end for big days


def build(data):
    days = data["days"]
    first = date.fromisoformat(days[0]["date"])
    offset = (first.weekday() + 1) % 7            # GitHub weeks start on Sunday
    weeks = (len(days) + offset + 6) // 7
    W = LEFT + weeks * (CELL + GAP) + 20
    H = TOP + 7 * (CELL + GAP) + 62
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         "<style>.c{opacity:0;animation:s .55s ease-out forwards}"
         "@keyframes s{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:none}}</style>",
         f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117"/>']
    last_month = -1
    for i, d in enumerate(days):
        w, dow = divmod(i + offset, 7)
        x, y = LEFT + w * (CELL + GAP), TOP + dow * (CELL + GAP)
        m = int(d["date"][5:7]) - 1
        if dow == 0 and m != last_month and w < weeks - 2:
            o.append(f'<text x="{x}" y="{TOP - 10}" font-family="{FONT}" font-size="10" fill="#8b949e">{MONTHS[m]}</text>')
            last_month = m
        delay = (w + dow) * 0.025
        o.append(f'<rect class="c" style="animation-delay:{delay:.2f}s" x="{x}" y="{y}" width="{CELL}" '
                 f'height="{CELL}" rx="3" fill="{PALETTE[level_of(d)]}"><title>{d["count"]} on {d["date"]}</title></rect>')
    for dow, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        o.append(f'<text x="8" y="{TOP + dow * (CELL + GAP) + 10}" font-family="{FONT}" font-size="10" fill="#8b949e">{name}</text>')
    o.append(f'<text x="{LEFT}" y="26" font-family="{FONT}" font-size="14" fill="#c9d1d9">'
             f'{data["total"]:,} contributions in the last year</text>')
    fy = H - 28
    o.append(f'<text x="{LEFT}" y="{fy + 10}" font-family="{FONT}" font-size="11" fill="#8b949e">'
             f'current streak {data["current_streak"]}d · longest {data["longest_streak"]}d · '
             f'best day {data["best_day"]["count"]}</text>')
    lx = W - 20 - (len(PALETTE) * (CELL + 3)) - 70
    o.append(f'<text x="{lx}" y="{fy + 10}" font-family="{FONT}" font-size="10" fill="#8b949e">Less</text>')
    for i, c in enumerate(PALETTE):
        o.append(f'<rect x="{lx + 32 + i * (CELL + 3)}" y="{fy}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>')
    o.append(f'<text x="{lx + 36 + len(PALETTE) * (CELL + 3)}" y="{fy + 10}" font-family="{FONT}" font-size="10" fill="#8b949e">More</text>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    OUT.write_text(build(json.loads(SRC.read_text(encoding="utf-8"))), encoding="utf-8")
    print("Wrote", OUT.name)
