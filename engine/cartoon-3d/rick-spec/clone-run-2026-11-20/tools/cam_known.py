#!/usr/bin/env python3
"""cam_known.py FRAME.jpg OUTDIR SEED - synthetic known-answer clip: scripted pans/pushes/holds with eases over a real still, moving FG card, x264 re-encode. Writes clip.mp4 + truth.json"""
import sys, json, os, subprocess, numpy as np, cv2
src, out, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]); os.makedirs(out, exist_ok=True); rng = np.random.default_rng(seed)
im = cv2.imread(src); W, H = 1080, 1920; big = cv2.resize(im, (W*2, H*2), interpolation=cv2.INTER_CUBIC)
def ease(kind, u):
    if kind == 'linear': return u
    if kind == 'ease-in': return u**2.2
    if kind == 'ease-out': return 1-(1-u)**2.2
    return 0.5-0.5*np.cos(np.pi*u)
# script: segments (hold | move)
segs = []; f = 1; kinds = ['push-in', 'pan', 'pull-out', 'tilt', 'pan', 'push-in']; rng.shuffle(kinds)
eases = ['ease-in', 'ease-out', 'ease-in-out', 'linear', 'ease-in-out', 'ease-out']; rng.shuffle(eases)
for kd, es in zip(kinds, eases):
    hl = int(rng.integers(8, 20)); segs.append(('hold', f, f+hl-1, None, None, None)); f += hl
    ml = int(rng.integers(10, 36))
    if kd == 'push-in': amt = float(rng.uniform(1.08, 1.35))
    elif kd == 'pull-out': amt = float(1/rng.uniform(1.08, 1.30))
    else: amt = float(rng.choice([-1, 1])*rng.uniform(4, 12))  # % W
    segs.append(('move', f, f+ml-1, kd, es, amt)); f += ml
segs.append(('hold', f, f+11, None, None, None)); N = f+11
cx, cy, z = W*1.0, H*1.0, 1.0; state = []; zat = {}
for typ, a, b, kd, es, amt in segs:
    zat[a] = z
    for n in range(a, b+1):
        if typ == 'move':
            u0 = ease(es, (n-a)/(b-a+1)); u1 = ease(es, (n-a+1)/(b-a+1))
            if kd in ('push-in', 'pull-out'): z *= amt**(u1-u0)
            elif kd == 'pan': cx -= amt/100*W*(u1-u0)*2/z   # content shift in px of source (2x canvas): frame-space shift = amt % W
            else: cy -= amt/100*W*(u1-u0)*2/z
        state.append((cx, cy, z))
vw = cv2.VideoWriter(out+'/raw.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, (W, H))
card = np.zeros((260, 200, 3), np.uint8); card[:] = (40, 200, 250); cv2.circle(card, (100, 90), 70, (255, 255, 255), -1); cv2.circle(card, (100, 90), 70, (20, 20, 40), 8)
for n, (cx, cy, z) in enumerate(state):
    w2, h2 = W*2/z/2*1.0, H*2/z/2*1.0   # half-size of the source window (base window = W x H in 2x canvas => shows half the canvas at z=1)
    M = np.float32([[W/(2*w2), 0, W/2 - cx*W/(2*w2)], [0, H/(2*h2), H/2 - cy*H/(2*h2)]])
    fr = cv2.warpAffine(big, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    x = int(120 + (n*9) % 700); y = int(700 + 120*np.sin(n/7.0)); fr[y:y+260, x:x+200] = card   # moving FG card (not camera)
    cv2.putText(fr, 'word %d' % (n//9), (380, 1370), cv2.FONT_HERSHEY_SIMPLEX, 2.2, (255, 255, 255), 8)
    vw.write(fr)
vw.release()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out+'/raw.avi', '-c:v', 'libx264', '-b:v', '4500k', '-pix_fmt', 'yuv420p', out+'/clip.mp4']); os.remove(out+'/raw.avi')
truth = [dict(start_f=a, end_f=b, type=kd, ease=es, amount=amt) for typ, a, b, kd, es, amt in segs if typ == 'move']  # pair index: motion between frame n and n+1 is recorded at frame n+1
json.dump(dict(n=N, moves=truth), open(out+'/truth.json', 'w'), indent=1); print(N, truth)
