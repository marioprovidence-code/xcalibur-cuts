import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = r"C:\Users\lionn\Desktop\trading bot\xcalibur-cuts\og-image.png"
W, H = 1200, 630
BG = (12, 10, 8)
GOLD = (201, 161, 74)
GOLD_L = (230, 197, 116)

# Base
img = Image.new("RGB", (W, H), BG)
arr = np.asarray(img, dtype=np.float32)

# Radial gold glow (center-right)
ys, xs = np.mgrid[0:H, 0:W]
cx, cy = 760, 315
d = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2)
glow = np.clip(1 - d / 900, 0, 1) ** 2
for i, c in enumerate(GOLD):
    arr[:, :, i] = np.clip(arr[:, :, i] + glow * c * 0.32, 0, 255)
img = Image.fromarray(arr.astype(np.uint8))

d = ImageDraw.Draw(img)

# Logo (dark base matches BG, so it blends)
logo = Image.open(r"C:\Users\lionn\Desktop\trading bot\xcalibur-cuts\logo-trace.png").convert("RGB")
lh = 420
lw = int(logo.width * lh / logo.height)
logo = logo.resize((lw, lh), Image.LANCZOS)
img.paste(logo, (70, (H - lh) // 2))

# Fonts
def font(sz, bold=True):
    cand = [
        r"C:\Windows\Fonts\timesbd.ttf" if bold else r"C:\Windows\Fonts\times.ttf",
        r"C:\Windows\Fonts\georgia.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for f in cand:
        try:
            return ImageFont.truetype(f, sz)
        except Exception:
            pass
    return ImageFont.load_default()

# Text block on the right
tx = 560
title_f = font(88)
sub_f = font(34, bold=False)
slog_f = font(40, bold=False)

d.text((tx, 150), "XCALIBUR CUTS", font=title_f, fill=GOLD)
d.text((tx, 250), "BARBER  SALON", font=sub_f, fill=GOLD_L)
d.text((tx, 320), "Where Quality Meets Precision", font=slog_f, fill=GOLD_L)
d.text((tx, 400), "Gasparillo  ·  Book via WhatsApp & Setmore", font=font(28, False), fill=(180, 176, 168))

# Gold frame
frame = Image.new("RGB", (W, H), (0, 0, 0))
fd = ImageDraw.Draw(frame)
fd.rectangle([18, 18, W - 19, H - 19], outline=GOLD, width=3)
img = Image.composite(img, frame, frame.convert("L"))

img.save(OUT)
print("saved", OUT, img.size)
