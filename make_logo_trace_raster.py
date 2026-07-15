import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SRC = r"C:\Users\lionn\Desktop\trading bot\xcalibur-cuts\logo.png"
OUT_PNG = r"C:\Users\lionn\Desktop\trading bot\xcalibur-cuts\logo-trace.png"
OUT_JPG = r"C:\Users\lionn\Desktop\trading bot\xcalibur-cuts\logo-trace.jpeg"

img = Image.open(SRC).convert("L")
w, h = img.size
side = min(w, h)
img = img.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2))
R = 170
img = img.resize((R, R), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.8))
a = np.asarray(img, dtype=np.float32)
p = np.pad(a, 1, mode="edge")
gx = (p[1:-1, 2:] - p[1:-1, :-2]) + 2 * (p[2:, 2:] - p[2:, :-2]) + (p[:-2, 2:] - p[:-2, :-2])
gy = (p[2:, 1:-1] - p[:-2, 1:-1]) + 2 * (p[2:, 2:] - p[:-2, :-2]) + (p[2:, :-2] - p[:-2, 2:])
mag = np.sqrt(gx ** 2 + gy ** 2)
mag = mag / (mag.max() + 1e-6)
TH = 0.34

S = 512
sx = S / (R - 1)
sy = S / (R - 1)
base = Image.new("RGB", (S, S), (12, 10, 8))
d = ImageDraw.Draw(base)
# hexagon frame
hexp = [(120, 18), (187, 58), (187, 182), (120, 222), (53, 182), (53, 58)]
d.line(hexp + [hexp[0]], fill=(201, 161, 74), width=3)

H, W = mag.shape
for i in range(H - 1):
    for j in range(W - 1):
        tl, tr = mag[i, j], mag[i, j + 1]
        br, bl = mag[i + 1, j + 1], mag[i + 1, j]
        c = (1 if tl >= TH else 0) * 8 + (1 if tr >= TH else 0) * 4 + \
            (1 if br >= TH else 0) * 2 + (1 if bl >= TH else 0) * 1
        if c == 0 or c == 15:
            continue
        def pt(e):
            if e == 'a': return (j + (TH - tl) / (tr - tl + 1e-9)) * sx, i * sy
            if e == 'b': return (j + 1) * sx, (i + (TH - tr) / (br - tr + 1e-9)) * sy
            if e == 'c': return (j + (TH - bl) / (br - bl + 1e-9)) * sx, (i + 1) * sy
            if e == 'd': return j * sx, (i + (TH - tl) / (bl - tl + 1e-9)) * sy
        table = {1: [('d', 'c')], 2: [('c', 'b')], 3: [('d', 'b')], 4: [('a', 'b')],
                 5: [('a', 'd'), ('c', 'b')], 6: [('a', 'c')], 7: [('a', 'd')],
                 8: [('d', 'a')], 9: [('a', 'c')], 10: [('d', 'a'), ('c', 'b')],
                 11: [('a', 'b')], 12: [('d', 'b')], 13: [('c', 'b')], 14: [('d', 'c')]}
        for e1, e2 in table[c]:
            x1, y1 = pt(e1); x2, y2 = pt(e2)
            d.line([(x1, y1), (x2, y2)], fill=(201, 161, 74), width=1)

base = base.filter(ImageFilter.GaussianBlur(0.6))
base.save(OUT_PNG)
base.convert("RGB").save(OUT_JPG, "JPEG", quality=95)
print("saved raster trace")
