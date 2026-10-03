"""Neofetch-style info card. STATIC=1 emits a frozen frame."""
import os
STATIC = os.environ.get("STATIC") == "1"
ROWS = [
    ("Now", "Final-year CSE student, Lucknow"),
    ("Role", "MERN Stack Developer"),
    ("Stack", "React · Node.js · Express · MongoDB"),
    ("DSA", "Java"),
    ("Built", "MedKart (pharmacy mgmt), PrepSense (RAG study bot)"),
    ("Learning", "Advanced MERN · AI / RAG / LLMs"),
    ("Outside", "photography · editing · travel · mountains"),
    ("Contact", "in/abhi9rai"),
]
W, LH = 490, 26
H = 70 + len(ROWS) * LH + 24
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
     'font-family="ui-monospace,Menlo,Consolas,monospace" font-size="13">',
     '<style>.r{opacity:%s;animation:f .5s ease-out forwards}'
     '@keyframes f{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}'
     '.k{fill:#58a6ff;font-weight:bold}.v{fill:#c9d1d9}.d{fill:#8b949e}</style>' % ("1" if STATIC else "0"),
     f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117"/>',
     '<circle cx="20" cy="18" r="6" fill="#ff5f56"/><circle cx="40" cy="18" r="6" fill="#ffbd2e"/>'
     '<circle cx="60" cy="18" r="6" fill="#27c93f"/>',
     f'<text x="{W//2}" y="22" text-anchor="middle" class="d">abhinav@github: ~</text>',
     '<text x="20" y="52" class="v"><tspan fill="#3fb950">abhinav@github</tspan> ~ $ neofetch</text>']
for i, (k, v) in enumerate(ROWS):
    y = 82 + i * LH
    delay = 0 if STATIC else round(0.4 + i * 0.25, 2)
    o.append(f'<g class="r" style="animation-delay:{delay}s"><text x="20" y="{y+14}" class="k">{k}</text>'
             f'<text x="100" y="{y+14}" class="v">{v}</text></g>')
o.append("</svg>")
open("info-card.svg", "w").write("\n".join(o))
print("wrote info-card.svg")
