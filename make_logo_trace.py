import math, json
import numpy as np
from PIL import Image, ImageFilter

SRC = r"C:\Users\lionn\Desktop\trading bot\xcalibur-cuts\logo.png"
OUT = r"C:\Users\lionn\Desktop\trading bot\xcalibur-cuts\logo-trace.svg"

# ---- 1. Load + square crop + resize ----
img = Image.open(SRC).convert("L")
w, h = img.size
side = min(w, h)
img = img.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2))
R = 170
img = img.resize((R, R), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.8))

# ---- 2. Edges via Sobel (numpy) ----
a = np.asarray(img, dtype=np.float32)
p = np.pad(a, 1, mode="edge")
gx = (p[1:-1, 2:] - p[1:-1, :-2]) * 1.0 + (p[2:, 2:] - p[2:, :-2]) * 2.0 + (p[:-2, 2:] - p[:-2, :-2]) * 1.0
gy = (p[2:, 1:-1] - p[:-2, 1:-1]) * 1.0 + (p[2:, 2:] - p[:-2, :-2]) * 2.0 + (p[2:, :-2] - p[:-2, 2:]) * 1.0
mag = np.sqrt(gx ** 2 + gy ** 2)
mag = mag / (mag.max() + 1e-6)

# ---- 3. Marching squares -> segments ----
TH = 0.34
H, W = mag.shape
# edge interpolation points: a=top, b=right, c=bottom, d=left
segs = []
for i in range(H - 1):
    for j in range(W - 1):
        tl, tr = mag[i, j], mag[i, j + 1]
        br, bl = mag[i + 1, j + 1], mag[i + 1, j]
        c = (1 if tl >= TH else 0) * 8 + (1 if tr >= TH else 0) * 4 + \
            (1 if br >= TH else 0) * 2 + (1 if bl >= TH else 0) * 1
        if c == 0 or c == 15:
            continue
        def pt(edge):
            if edge == 'a':
                return (j + (TH - tl) / (tr - tl + 1e-9), i)
            if edge == 'b':
                return (j + 1, i + (TH - tr) / (br - tr + 1e-9))
            if edge == 'c':
                return (j + (TH - bl) / (br - bl + 1e-9), i + 1)
            if edge == 'd':
                return (j, i + (TH - tl) / (bl - tl + 1e-9))
        table = {1: [('d', 'c')], 2: [('c', 'b')], 3: [('d', 'b')], 4: [('a', 'b')],
                 5: [('a', 'd'), ('c', 'b')], 6: [('a', 'c')], 7: [('a', 'd')],
                 8: [('d', 'a')], 9: [('a', 'c')], 10: [('d', 'a'), ('c', 'b')],
                 11: [('a', 'b')], 12: [('d', 'b')], 13: [('c', 'b')], 14: [('d', 'c')]}
        for e1, e2 in table[c]:
            segs.append((pt(e1), pt(e2)))

# ---- 4. Link segments into polylines ----
def key(p):
    return (round(p[0], 1), round(p[1], 1))

adj = {}
for idx, (p1, p2) in enumerate(segs):
    k1, k2 = key(p1), key(p2)
    adj.setdefault(k1, []).append((k2, idx))
    adj.setdefault(k2, []).append((k1, idx))

used = [False] * len(segs)
polylines = []
for s in range(len(segs)):
    if used[s]:
        continue
    p1, p2 = segs[s]
    used[s] = True
    chain = [p1, p2]
    # extend forward from p2
    cur = key(p2)
    while True:
        nxt = None
        for (other, si) in adj.get(cur, []):
            if not used[si]:
                nxt = (other, si); break
        if nxt is None:
            break
        other, si = nxt
        used[si] = True
        chain.append(other)
        cur = other
    # extend backward from p1
    cur = key(p1)
    while True:
        nxt = None
        for (other, si) in adj.get(cur, []):
            if not used[si]:
                nxt = (other, si); break
        if nxt is None:
            break
        other, si = nxt
        used[si] = True
        chain.insert(0, other)
        cur = other
    if len(chain) >= 4:
        polylines.append(chain)

# sort by length desc, keep top N for file size
polylines.sort(key=len, reverse=True)
polylines = polylines[:240]

# ---- 5. Scale to viewBox 240 ----
sx = 240.0 / (W - 1)
sy = 240.0 / (H - 1)

def fmt(p):
    return "%.1f %.1f" % (p[0] * sx, p[1] * sy)

paths = []
for pl in polylines:
    d = "M " + " L ".join(fmt(p) for p in pl)
    paths.append(d)

# ---- 6. Emit SVG (gold wireframe, draw-on + pulse + scan) ----
svg = []
svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" role="img" aria-label="Xcalibur Cuts traced wireframe logo">')
svg.append('''  <defs>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="1.6" result="b" />
      <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
    </filter>
    <linearGradient id="scanGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#e6c574" stop-opacity="0" />
      <stop offset="50%" stop-color="#e6c574" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#e6c574" stop-opacity="0" />
    </linearGradient>
    <style>
      :root { --gold:#c9a14a; --goldL:#e6c574; }
      .ln { fill:none; stroke:var(--gold); stroke-width:1.4; stroke-linecap:round; stroke-linejoin:round;
            filter:url(#glow); stroke-dasharray:1; stroke-dashoffset:1; animation:draw 2.6s ease forwards; }
      .scan { fill:url(#scanGrad); opacity:0; animation:scan 3.6s 2.6s linear infinite; }
      @keyframes draw { to { stroke-dashoffset:0; } }
      @keyframes scan { 0%{transform:translateY(14px);opacity:0;} 10%{opacity:.8;} 90%{opacity:.8;} 100%{transform:translateY(216px);opacity:0;} }
      @media (prefers-reduced-motion: reduce) { .ln{stroke-dashoffset:0;animation:none;} .scan{display:none;} }
    </style>
  </defs>''')

# hexagon frame for branding cohesion
svg.append('  <path class="ln" style="animation-delay:.1s" pathLength="1" d="M120 18 L187 58 L187 182 L120 222 L53 182 L53 58 Z" />')

for i, d in enumerate(paths):
    delay = 0.2 + (i % 24) * 0.06
    svg.append('  <path class="ln" style="animation-delay:%.2fs" pathLength="1" d="%s" />' % (delay, d))

svg.append('  <rect class="scan" x="34" y="0" width="172" height="2.5" rx="1.2" />')
svg.append('</svg>')

open(OUT, "w", encoding="utf-8").write("\n".join(svg))
print("paths:", len(paths), "segments:", len(segs))
