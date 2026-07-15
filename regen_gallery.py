import os, re

g = r"C:\Users\lionn\Desktop\trading bot\xcalibur-cuts\gallery"
p = r"C:\Users\lionn\Desktop\trading bot\xcalibur-cuts\index.html"

files = sorted(os.listdir(g))
img_ext = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
vid_ext = {".mp4", ".webm", ".ogg"}

items = []
n = 0
skip = {35, 52, 55, 14, 15, 7, 8, 9, 3}
for f in files:
    ext = os.path.splitext(f)[1].lower()
    n += 1
    if n in skip:
        continue
    if ext in img_ext:
        items.append('<figure class="tile"><span class="tile__num">%d</span><img src="gallery/%s" alt="Xcalibur Cuts haircut" loading="lazy" /></figure>' % (n, f))
    elif ext in vid_ext:
        items.append('<figure class="tile"><span class="tile__num">%d</span><video src="gallery/%s" controls preload="metadata" muted></video></figure>' % (n, f))

grid = "\n        ".join(items)
block = '      <div class="gallery__grid">\n        ' + grid + '\n      </div>'

s = open(p, encoding="utf-8").read()
s2 = re.sub(r'      <div class="gallery__grid">.*?      </div>', block, s, flags=re.S)
open(p, "w", encoding="utf-8").write(s2)
print("gallery items:", len(items))
