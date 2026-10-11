"""data/contributions.json -> activity-chart.svg (animated monthly bar chart)"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "data" / "contributions.json", ROOT / "activity-chart.svg"
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
MN = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
W, H, LEFT, TOP, BASE = 860, 240, 50, 60, 190


def build(data):
    items = sorted(data["monthly"].items())[-12:]
    peak = max(max(v for _, v in items), 1)
    slot = (W - LEFT - 30) / len(items)
    bw = slot * 0.55
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>',
         f'<text x="{LEFT}" y="30" font-family="{FONT}" font-size="14" fill="#c9d1d9">monthly activity</text>',
         f'<text x="{W-30}" y="30" text-anchor="end" font-family="{FONT}" font-size="11" fill="#8b949e">peak {peak}</text>',
         f'<line x1="{LEFT}" y1="{BASE}" x2="{W-30}" y2="{BASE}" stroke="#30363d"/>']
    for i, (k, v) in enumerate(items):
        h = (BASE - TOP) * v / peak
        x = LEFT + i * slot + (slot - bw) / 2
        hot = v == peak
        col = "#69f0a0" if hot else "#26a641" if v else "#161b22"
        hh = max(h, 2)
        dl = i * 0.12
        o.append(f'<rect x="{x:.1f}" y="{BASE}" width="{bw:.1f}" height="0" rx="3" fill="{col}">'
                 f'<animate attributeName="height" from="0" to="{hh:.1f}" dur=".6s" begin="{dl:.2f}s" fill="freeze"/>'
                 f'<animate attributeName="y" from="{BASE}" to="{BASE-hh:.1f}" dur=".6s" begin="{dl:.2f}s" fill="freeze"/>'
                 f'<title>{v} in {MN[int(k[5:7])-1]} {k[:4]}</title></rect>')
        o.append(f'<text x="{x+bw/2:.1f}" y="{BASE-hh-6:.1f}" text-anchor="middle" font-family="{FONT}" font-size="10" '
                 f'fill="#c9d1d9" opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".3s" begin="{dl+.6:.2f}s" fill="freeze"/>{v}</text>')
        o.append(f'<text x="{x+bw/2:.1f}" y="{BASE+18}" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#8b949e">{MN[int(k[5:7])-1]}</text>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    OUT.write_text(build(json.loads(SRC.read_text(encoding="utf-8"))), encoding="utf-8")
    print("Wrote", OUT.name)
