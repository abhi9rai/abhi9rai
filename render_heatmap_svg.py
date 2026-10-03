"""Render data/contributions.json as an animated 53x7 heatmap SVG."""
import json, datetime as dt

D = json.load(open("data/contributions.json"))
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
CELL, GAP, LEFT, TOP = 12, 3, 34, 44
STEP = CELL + GAP
days = [(dt.date.fromisoformat(d["date"]), d) for d in D["days"]]
first = days[0][0]
start = first - dt.timedelta(days=(first.weekday() + 1) % 7)   # back to Sunday
W, H = 860, TOP + 7 * STEP + 52

o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
     f'font-family="ui-monospace,Menlo,Consolas,monospace">',
     '<style>.c{opacity:0;animation:p .45s ease-out forwards}'
     '@keyframes p{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:none}}'
     '.t{fill:#8b949e;font-size:11px}.h{fill:#c9d1d9;font-size:13px}</style>',
     f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117"/>',
     f'<text x="{LEFT}" y="22" class="h">$ ./contributions.sh --user {D["user"]}</text>']

last_m = None
for d, rec in days:
    col, row = (d - start).days // 7, (d.weekday() + 1) % 7
    x, y = LEFT + col * STEP, TOP + row * STEP
    if row == 0 and d.month != last_m and (d.day <= 7 or last_m is None):
        o.append(f'<text x="{x}" y="{TOP-8}" class="t">{d.strftime("%b")}</text>')
        last_m = d.month
    delay = round((col + row) * 0.018, 3)
    tip = f'{rec["count"]} on {d.isoformat()}'
    o.append(f'<rect class="c" style="animation-delay:{delay}s" x="{x}" y="{y}" width="{CELL}" '
             f'height="{CELL}" rx="3" fill="{PALETTE[min(rec["level"],4)]}"><title>{tip}</title></rect>')

for r, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    o.append(f'<text x="2" y="{TOP + r*STEP + 10}" class="t">{name}</text>')

fy = TOP + 7 * STEP + 22
b = D["best_day"]
o.append(f'<text x="{LEFT}" y="{fy}" class="h">{D["total"]:,} contributions in the last year</text>')
o.append(f'<text x="{LEFT}" y="{fy+18}" class="t">streak {D["current_streak"]}d · longest {D["longest_streak"]}d · '
         f'best day {b["count"]} ({b["date"]})</text>')
lx = W - 180
o.append(f'<text x="{lx-34}" y="{fy+8}" class="t">Less</text>')
for i, c in enumerate(PALETTE):
    o.append(f'<rect x="{lx+i*17}" y="{fy-2}" width="12" height="12" rx="3" fill="{c}"/>')
o.append(f'<text x="{lx+5*17+4}" y="{fy+8}" class="t">More</text></svg>')
open("contrib-heatmap.svg", "w").write("\n".join(o))
print("wrote contrib-heatmap.svg")
