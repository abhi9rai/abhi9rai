"""source-prepped.png -> monochrome ASCII SVG that 'types' in row by row, once."""
import sys, html, numpy as np
from PIL import Image

RAMP = " .`:-=+*cs#%@"          # bright (sparse) -> dark (dense)
COLS = 100
src = sys.argv[1] if len(sys.argv) > 1 else "source-prepped.png"
img = Image.open(src).convert("L")
rows = max(1, int(COLS * img.height / img.width * 0.5))   # chars are ~2x taller than wide
a = np.array(img.resize((COLS, rows)), dtype=float) / 255
CW, CH = 3.7, 7.4
W, H = int(COLS * CW), int(rows * CH) + 8

o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
     'font-family="ui-monospace,Menlo,Consolas,monospace" font-size="7.4" xml:space="preserve">',
     '<style>text{fill:#c9d1d9;white-space:pre}</style>', '<defs>']
for r in range(rows):
    t0 = round(r * 0.06, 2)
    o.append(f'<clipPath id="c{r}"><rect x="0" y="{r*CH:.1f}" width="0" height="{CH+1:.1f}">'
             f'<animate attributeName="width" from="0" to="{W}" begin="{t0}s" dur="0.6s" fill="freeze"/>'
             f'</rect></clipPath>')
o.append('</defs>')
for r in range(rows):
    line = "".join(RAMP[min(int((1 - v) * (len(RAMP) - 1) + 0.5), len(RAMP) - 1)] for v in a[r])
    if line.strip():
        o.append(f'<text x="0" y="{(r+1)*CH:.1f}" clip-path="url(#c{r})" textLength="{W}" '
                 f'lengthAdjust="spacing">{html.escape(line)}</text>')
o.append("</svg>")
open("avi-ascii.svg", "w").write("\n".join(o))
print("wrote avi-ascii.svg", COLS, "x", rows)
