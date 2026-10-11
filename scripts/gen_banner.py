"""Animated growth banner -> banner.svg (pure SMIL, no JS, works inside GitHub READMEs)"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "banner.svg"

# EDIT ME: your growth path, left to right
MILESTONES = ["Java", "Spring Boot", "Microservices", "PTA @ Cognizant", "Full-time ▸"]

W, H = 860, 240
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
Y0, Y1 = 192, 120          # curve start / end height


def build():
    n = len(MILESTONES)
    xs = [60 + i * (W - 120) / (n - 1) for i in range(n)]
    ys = [Y0 - (Y0 - Y1) * (i / (n - 1)) ** 1.4 for i in range(n)]
    d = f"M{xs[0]:.1f},{ys[0]:.1f}"
    for i in range(1, n):
        mx = (xs[i - 1] + xs[i]) / 2
        d += f" C{mx:.1f},{ys[i-1]:.1f} {mx:.1f},{ys[i]:.1f} {xs[i]:.1f},{ys[i]:.1f}"
    area = d + f" L{xs[-1]:.1f},{H-30} L{xs[0]:.1f},{H-30} Z"

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs>'
         '<linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#26a641"/>'
         '<stop offset="1" stop-color="#69f0a0"/></linearGradient>'
         '<linearGradient id="a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#39d353" stop-opacity=".25"/>'
         '<stop offset="1" stop-color="#39d353" stop-opacity="0"/></linearGradient>'
         '<clipPath id="t1"><rect x="30" y="20" height="30" width="0">'
         '<animate attributeName="width" from="0" to="520" dur="2s" begin="0.3s" fill="freeze"/></rect></clipPath>'
         '<clipPath id="t2"><rect x="30" y="52" height="34" width="0">'
         '<animate attributeName="width" from="0" to="420" dur="1.4s" begin="2.3s" fill="freeze"/></rect></clipPath>'
         '</defs>',
         f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>',
         f'<text x="30" y="42" font-family="{FONT}" font-size="14" fill="#39d353" clip-path="url(#t1)">'
         'shivendra@github ~ $ <tspan fill="#c9d1d9">./grow.sh --backend --deepfake</tspan></text>',
         f'<text x="30" y="78" font-family="{FONT}" font-size="26" font-weight="700" fill="#e6edf3" clip-path="url(#t2)">'
         'Shivendra Pandey</text>',
         f'<text x="30" y="100" font-family="{FONT}" font-size="12" fill="#8b949e" opacity="0">'
         'Java + Spring Boot by day, deepfake detection by curiosity'
         '<animate attributeName="opacity" from="0" to="1" dur="0.8s" begin="3.7s" fill="freeze"/></text>',
         f'<rect x="{30+8.6*30}" y="64" width="12" height="3" fill="#39d353" opacity="0">'
         '<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.01;.5;.51;1" dur="1s" begin="3.7s" repeatCount="indefinite"/></rect>',
         f'<path d="{area}" fill="url(#a)" opacity="0">'
         '<animate attributeName="opacity" from="0" to="1" dur="1.5s" begin="2.5s" fill="freeze"/></path>',
         f'<path d="{d}" pathLength="1" fill="none" stroke="url(#g)" stroke-width="3" stroke-linecap="round" '
         'stroke-dasharray="1" stroke-dashoffset="1">'
         '<animate attributeName="stroke-dashoffset" from="1" to="0" dur="3s" begin="1s" fill="freeze"/></path>']
    for i, (x, y, label) in enumerate(zip(xs, ys, MILESTONES)):
        t = 1 + 3 * i / (n - 1)
        last = i == n - 1
        o.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".4s" begin="{t:.2f}s" fill="freeze"/>'
                 f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#0d1117" stroke="#39d353" stroke-width="2.5"/>'
                 + (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="none" stroke="#69f0a0">'
                    '<animate attributeName="r" values="6;16" dur="1.6s" repeatCount="indefinite"/>'
                    '<animate attributeName="opacity" values=".8;0" dur="1.6s" repeatCount="indefinite"/></circle>' if last else "")
                 + f'<text x="{x:.1f}" y="{y+26:.1f}" text-anchor="middle" font-family="{FONT}" font-size="11" '
                 f'fill="{"#69f0a0" if last else "#8b949e"}">{label}</text></g>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    OUT.write_text(build(), encoding="utf-8")
    print("Wrote", OUT.name)
