import os
from PIL import Image

apk = r"C:\Users\lionn\Desktop\trading bot\xcalibur-cuts\android-app\apk"
src = Image.open(r"C:\Users\lionn\Desktop\trading bot\xcalibur-cuts\logo-trace.png").convert("RGBA")
BG = (12, 10, 8, 255)
dpi = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}

for name, size in dpi.items():
    d = os.path.join(apk, "res", "mipmap-" + name)
    os.makedirs(d, exist_ok=True)
    canvas = Image.new("RGBA", (size, size), BG)
    pad = int(size * 0.16)
    s = size - 2 * pad
    l = src.resize((s, s), Image.LANCZOS)
    canvas.paste(l, ((size - s) // 2, (size - s) // 2), l)
    canvas.save(os.path.join(d, "ic_launcher.png"))
print("icons generated:", list(dpi))
