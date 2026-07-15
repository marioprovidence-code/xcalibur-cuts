from PIL import Image, ImageFilter, ImageOps

src = r"C:\Users\lionn\Desktop\trading bot\xcalibur-cuts\logo.png"
out_png = r"C:\Users\lionn\Desktop\trading bot\xcalibur-cuts\logo-wire.png"
out_jpg = r"C:\Users\lionn\Desktop\trading bot\xcalibur-cuts\logo-wire.jpeg"

# Square center crop, large for crisp edges
img = Image.open(src).convert("RGB")
w, h = img.size
side = min(w, h)
left = (w - side) // 2
top = (h - side) // 2
img = img.crop((left, top, left + side, top + side))
img = img.resize((640, 640), Image.LANCZOS)

# Grayscale + edge detection (wireframe / robot look)
gray = img.convert("L")
edges = gray.filter(ImageFilter.FIND_EDGES)
edges = edges.filter(ImageFilter.SMOOTH_MORE)

ex = edges.load()
gold = (201, 161, 74)
out = Image.new("RGB", img.size, (8, 7, 5))
ox = out.load()
W, H = img.size
for y in range(H):
    for x in range(W):
        v = ex[x, y]
        # boost contrast, keep faint structure for a "wire" feel
        f = max(0, (v - 30)) / 225.0
        ox[x, y] = (
            int(gold[0] * f),
            int(gold[1] * f),
            int(gold[2] * f),
        )

# Subtle glow: screen the edges lightly over the dark base
glow = out.filter(ImageFilter.GaussianBlur(1.2))
out = Image.blend(out, glow, 0.5)
out = ImageOps.autocontrast(out, cutoff=0)

out.save(out_png)
out.convert("RGB").save(out_jpg, "JPEG", quality=95)
print("saved", out_png, "and", out_jpg)
