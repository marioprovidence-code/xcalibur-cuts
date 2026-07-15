import os, subprocess, imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
G = r"C:\Users\lionn\Desktop\trading bot\xcalibur-cuts\gallery"
tmp = os.path.join(G, "_tmp_compress")
os.makedirs(tmp, exist_ok=True)

for f in os.listdir(G):
    if not f.lower().endswith(".mp4"):
        continue
    src = os.path.join(G, f)
    dst = os.path.join(tmp, f)
    before = os.path.getsize(src)
    cmd = [
        FF, "-y", "-i", src,
        "-vf", "scale='min(720,iw)':-2",
        "-c:v", "libx264", "-crf", "28", "-preset", "medium",
        "-c:a", "aac", "-b:a", "96k",
        "-movflags", "+faststart", dst,
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    after = os.path.getsize(dst)
    # only replace if compression actually helped
    if after < before:
        os.replace(dst, src)
        print("OK  %-28s %.1fMB -> %.1fMB" % (f, before/1e6, after/1e6))
    else:
        os.remove(dst)
        print("SKIP %-28s (no savings)" % f)

import shutil
shutil.rmtree(tmp, ignore_errors=True)
