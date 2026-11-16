# concat the 2K chunks, blend the dissolve frames (base chunk frame * (1-a) + over layer png * a), encode, mux the mix
import json, subprocess, sys, os, numpy as np
from PIL import Image
from scipy import ndimage
D = sys.argv[1] if len(sys.argv) > 1 else "/home/user/cart2/out/c2/final20"; W, H = 1440, 2560
segs = sorted(f for f in os.listdir(D) if f.startswith("seg_") and f.endswith(".mp4") and ".tmp" not in f)
assert len(segs) == 22, segs
with open(D + "/concat.txt", "w") as f:
    for s in segs: f.write(f"file '{D}/{s}'\n")
dis = {n: a for n, a in json.load(open(D + "/dissolves.json"))}
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-f", "concat", "-safe", "0", "-i", D + "/concat.txt", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                        "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", D + "/video_noaudio.mp4"], stdin=subprocess.PIPE)
n = 0; blended = 0; edges = []
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    if n in dis:
        a = dis[n]; base = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32)
        op = next(p for p in (f"{D}/over0/over_{n:04d}.png", f"{D}/over1/over_{n:04d}.png", f"{D}/over/over_{n:04d}.png") if os.path.exists(p))
        ov = np.asarray(Image.open(op).convert("RGB").resize((W, H)), np.float32)
        buf = np.clip(base * (1 - a) + ov * a + 0.5, 0, 255).astype(np.uint8).tobytes(); blended += 1
    sm = np.asarray(Image.frombuffer("RGB", (W, H), buf).resize((180, 320)), np.float32).mean(2)
    m = np.hypot(ndimage.sobel(sm, 1), ndimage.sobel(sm, 0)); edges.append(float((m > 60).mean() * 100))
    enc.stdin.write(buf); n += 1
enc.stdin.close(); enc.wait(); dec.wait()
print("frames", n, "blended", blended, "of", len(dis), "edge avg %.2f min %.1f median %.1f" % (np.mean(edges), np.min(edges), np.median(edges)))
json.dump(edges, open(D + "/edges.json", "w"))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", D + "/video_noaudio.mp4", "-i", "/home/user/chicago/audio/mix_v2.wav", "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", D + "/chicago_final_2k.mp4"], check=True)
print("muxed")
