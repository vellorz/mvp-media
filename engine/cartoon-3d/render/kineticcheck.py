#!/usr/bin/env python3
"""Kinetic camera check (rules 384-388, 393; Gemini R01-R05, R09). 2026-11-26.
Usage: python3 kineticcheck.py VIDEO [--json]
Subpixel phase correlation (parabolic peak) between consecutive frames on the top-half ROI
at 540x960; speeds reported in px/frame at 1080 wide (x1.333 for the 1440 master).
Same measurer as research/rick-style-spec/new-analysis-7-gemini/spotcheck/kin.py, so values
compare directly with the Rick numbers there. Guidance-level gates, not 99 % rules.
Caution: a flat sky in the top half can under-read motion; confirm a LOW by eye."""
import sys, subprocess, json
import numpy as np
W, H = 540, 960
FLOORS = dict(move=80.0, burst=8.0, p90=18.0, maxhold_s=6.0, hook=40.0)
TARGETS = "Rick 01-19: move 85 %, burst (>=20 px/f) 12-25 % (median 17), p90 >=25, typical longest still <2 s, state change every 1.6-3.5 s, hook >=40 px/f by 2.5 s"
def sub(c, i, n):
    a, b, cc = c[(i - 1) % n], c[i], c[(i + 1) % n]; d = a - 2 * b + cc
    return 0.0 if d == 0 else 0.5 * (a - cc) / d
def measure(v):
    p = subprocess.Popen(['ffmpeg', '-v', 'quiet', '-i', v, '-vf', f'scale={W}:{H},format=gray',
                          '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    win = np.outer(np.hanning(H // 2 - 40), np.hanning(W - 40))
    prev = prevF = None; sp = []; dif = []
    while True:
        buf = p.stdout.read(W * H)
        if len(buf) < W * H: break
        f = np.frombuffer(buf, np.uint8).reshape(H, W).astype(np.float32)
        roi = f[20:H // 2 - 20, 20:W - 20]; roi = (roi - roi.mean()) * win
        F = np.fft.fft2(roi)
        if prevF is not None:
            R = F * np.conj(prevF); R /= np.abs(R) + 1e-6; c = np.fft.ifft2(R).real
            y, x = np.unravel_index(np.argmax(c), c.shape); h, w = c.shape
            yy = y + sub(c[:, x], y, h); xx = x + sub(c[y, :], x, w)
            if yy > h / 2: yy -= h
            if xx > w / 2: xx -= w
            sp.append(2 * float(np.hypot(xx, yy))); dif.append(float(np.abs(f - prev).mean()))
        prev, prevF = f, F
    return np.array(sp), np.array(dif)
def main():
    v = sys.argv[1]; sp, dif = measure(v); n = len(sp)
    run = best = 0
    for s in sp < 0.54:
        run = run + 1 if s else 0; best = max(best, run)
    jumps = [i + 1 for i in range(1, n - 1) if dif[i] > 25 and dif[i] > 4 * max(dif[i - 1], dif[i + 1], 1)
             and sp[i - 1] < 20 and sp[i + 1] < 20]
    fast = sp >= 20
    events = sorted(set([i for i in range(1, n) if fast[i] and not fast[i - 1]] + jumps))
    gaps = np.diff([0] + events + [n]) / 30.0 if n else np.array([0])
    r = dict(video=v, frames=n,
             move=round(float((sp >= 0.54).mean() * 100), 1), glide=round(float((sp >= 2).mean() * 100), 1),
             burst=round(float(fast.mean() * 100), 1), median=round(float(np.median(sp)), 2),
             p90=round(float(np.percentile(sp, 90)), 1), maxhold_s=round(best / 30, 2),
             hook=round(float(sp[15:90].max()) if n > 90 else 0.0, 1),
             maxgap_s=round(float(gaps.max()), 2), median_gap_s=round(float(np.median(gaps)), 2),
             isolated_jumps=len(jumps), jump_frames=jumps[:30])
    st = {k: ("PASS" if (r[k] <= FLOORS[k] if k == "maxhold_s" else r[k] >= FLOORS[k]) else "LOW")
          for k in FLOORS}
    st["maxgap_s"] = "INFO"  # lower bound: dissolves not detected; rule 387 is checked on the shot list
    r["status"] = st
    if "--json" in sys.argv: print(json.dumps(r)); return
    print("KINETIC", " ".join(f"{k}={r[k]}({st.get(k,'-')})" for k in
          ("move", "burst", "p90", "maxhold_s", "hook", "maxgap_s")), f"median={r['median']} jumps={r['isolated_jumps']}")
    print("gap lower bound: only fast bursts and frame jumps count as state changes; dissolves are not detected")
    print(TARGETS)
    if r["isolated_jumps"]: print("isolated frame jumps (planned cut? else pop/orphan key, rule 77/393):", r["jump_frames"])
if __name__ == "__main__":
    main()
