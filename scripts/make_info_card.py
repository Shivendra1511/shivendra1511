"""Neofetch-style info card SVG. Edit ROWS with your own story."""
import os
from pathlib import Path
from xml.sax.saxutils import escape

from config import HANDLE

OUT = Path(__file__).resolve().parent.parent / "info-card.svg"
STATIC = os.environ.get("STATIC") == "1"

# (key, value) - edit freely
ROWS = [
    ("Role",     "Backend Engineer"),
    ("Now",      "PTA Intern @ Cognizant (full-time pending)"),
    ("Stack",    "Java · Spring Boot · Microservices · REST"),
    ("Also",     "Python · ML · Computer Vision"),
    ("Project",  "deepfake-detection-usingRestnet18-MTCNN"),
    ("Training", "Vehicle Telematics & Fleet Management"),
    ("Connect",  "linkedin.com/in/shivendra-pandey-403721342"),
]

W, H = 560, 60 + 34 * len(ROWS) + 70
BG, FG, KEY, ACC = "#0d1117", "#c9d1d9", "#58a6ff", "#3fb950"
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def build():
    anim = "" if STATIC else """
<style>
.l{opacity:0;animation:in .5s ease-out forwards}
@keyframes in{from{opacity:0;transform:translateX(-12px)}to{opacity:1;transform:none}}
</style>"""
    cls = "" if STATIC else ' class="l"'
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{anim}',
         f'<rect width="{W}" height="{H}" rx="10" fill="{BG}"/>',
         f'<rect width="{W}" height="32" rx="10" fill="#161b22"/><rect y="20" width="{W}" height="12" fill="#161b22"/>',
         '<circle cx="18" cy="16" r="6" fill="#ff5f56"/><circle cx="38" cy="16" r="6" fill="#ffbd2e"/>'
         '<circle cx="58" cy="16" r="6" fill="#27c93f"/>',
         f'<text x="{W/2}" y="21" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#8b949e">{escape(HANDLE)}@github: ~</text>']
    d = 0.0

    def line(y, inner):
        nonlocal d
        style = "" if STATIC else f' style="animation-delay:{d:.2f}s"'
        d += 0.25
        o.append(f'<text x="28" y="{y}" font-family="{FONT}" font-size="15" fill="{FG}" xml:space="preserve"{cls}{style}>{inner}</text>')

    line(68, f'<tspan fill="{ACC}" font-weight="bold">{escape(HANDLE)}</tspan><tspan fill="#8b949e">@</tspan><tspan fill="{ACC}" font-weight="bold">github</tspan>')
    line(88, '<tspan fill="#30363d">' + "-" * 28 + "</tspan>")
    y = 118
    for k, v in ROWS:
        line(y, f'<tspan fill="{KEY}" font-weight="bold">{escape(k)}</tspan><tspan fill="#8b949e">: </tspan>{escape(v)}')
        y += 30
    # colour swatches, like neofetch
    sw = ["#f85149", "#d29922", "#3fb950", "#58a6ff", "#bc8cff", "#39c5cf", "#c9d1d9"]
    for i, c in enumerate(sw):
        o.append(f'<rect x="{28 + i * 26}" y="{y + 6}" width="22" height="14" rx="2" fill="{c}"{cls}'
                 f'{"" if STATIC else f" style=\"animation-delay:{d:.2f}s\""}/>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    OUT.write_text(build(), encoding="utf-8")
    print("Wrote", OUT.name)
