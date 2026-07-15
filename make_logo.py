from PIL import Image, ImageEnhance, ImageOps

src = r"C:\Users\lionn\Desktop\trading bot\xcalibur-cuts\logo.png"
out = r"C:\Users\lionn\Desktop\trading bot\xcalibur-cuts\logo-vintage.png"

img = Image.open(src).convert("RGB")

# Square crop (center)
w, h = img.size
side = min(w, h)
left = (w - side) // 2
top = (h - side) // 2
img = img.crop((left, top, left + side, top + side))
img = img.resize((512, 512), Image.LANCZOS)

# Vintage: desaturate, warm sepia/gold tone, soft contrast, vignette
img = ImageEnhance.Color(img).enhance(0.15)
img = ImageEnhance.Contrast(img).enhance(1.05)
img = ImageEnhance.Brightness(img).enhance(0.97)

# Tint toward gold (#c9a14a)
tint = Image.new("RGB", img.size, (201, 161, 74))
img = Image.blend(img, tint, 0.45)

# Vignette
mask = Image.new("L", img.size, 0)
mask_data = mask.load()
import math
cx, cy = 256, 256
maxd = math.sqrt(cx * cx + cy * cy)
for y in range(512):
    for x in range(512):
        d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        mask_data[x, y] = int(255 * max(0, min(1, (maxd - d) / maxd + 0.25)))
dark = Image.new("RGB", img.size, (20, 16, 8))
img = Image.composite(img, dark, mask)

# Slight grain/retro feel via reduced sharpness
img = ImageEnhance.Sharpness(img).enhance(0.9)

img.save(out)
print("saved", out)
