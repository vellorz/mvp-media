#!/usr/bin/env python3
"""camB.py VIDEO OUT.csv  - Tool B (definitions v3 s5): dense Farneback flow at 270x480 + robust iteratively-reweighted similarity fit. No shared code with camA."""
import sys, subprocess, numpy as np, cv2
v, out = sys.argv[1], sys.argv[2]; W, H = 270, 480
p = subprocess.Popen(['ffmpeg','-v','error','-i',v,'-vf',f'scale={W}:{H}:flags=bicubic','-f','rawvideo','-pix_fmt','gray','-'], stdout=subprocess.PIPE)
ys, xs = np.mgrid[0:H:4, 0:W:4]; valid = ~((ys > .655*H) & (ys < .745*H))
X = (xs - W/2.0)[valid].astype(np.float64); Y = (ys - H/2.0)[valid].astype(np.float64)
def fit(u, v_):
    # model: u = a*X - b*Y + tx ; v = b*X + a*Y + ty   (a = s*cos - 1, b = s*sin)
    w = np.ones_like(u); par = np.zeros(4)
    for it in range(12):
        A = np.zeros((4, 4)); B = np.zeros(4)
        r1 = np.stack([X, -Y, np.ones_like(X), np.zeros_like(X)], 1); r2 = np.stack([Y, X, np.zeros_like(X), np.ones_like(X)], 1)
        A = (r1*w[:, None]).T @ r1 + (r2*w[:, None]).T @ r2; B = (r1*w[:, None]).T @ u + (r2*w[:, None]).T @ v_
        try: par = np.linalg.solve(A + 1e-9*np.eye(4), B)
        except Exception: break
        res = np.hypot(u - r1 @ par, v_ - r2 @ par); sc = max(1.4826*np.median(res), 0.05)
        w = 1.0/(1.0 + (res/(2.0*sc))**2)**2   # steep redescender
    return par, float(np.mean(res < 3*sc))
prev = None; rows = []; i = 0
while True:
    b = p.stdout.read(W*H)
    if len(b) < W*H: break
    i += 1; g = np.frombuffer(b, np.uint8).reshape(H, W)
    if prev is not None:
        fl = cv2.calcOpticalFlowFarneback(prev, g, None, 0.5, 4, 21, 3, 7, 1.5, 0)
        gx = cv2.Sobel(prev, cv2.CV_32F, 1, 0); gy = cv2.Sobel(prev, cv2.CV_32F, 0, 1); tex = (np.hypot(gx, gy)[::4, ::4])[valid] > 12
        u = fl[::4, ::4, 0][valid].astype(np.float64); v_ = fl[::4, ::4, 1][valid].astype(np.float64)
        if tex.sum() > 80:
            Xs, Ys = X, Y; X_, Y_ = X[tex], Y[tex]
            globals()['X'], globals()['Y'] = X_, Y_
            par, inl = fit(u[tex], v_[tex])
            globals()['X'], globals()['Y'] = Xs, Ys
            a, bb, tx, ty = par; s = float(np.hypot(1+a, bb)); r = float(np.degrees(np.arctan2(bb, 1+a)))
            rows.append((i, round(tx/W*100, 4), round(ty/W*100, 4), round(s, 5), round(r, 4), int(tex.sum()), round(inl, 3)))
        else: rows.append((i, 0, 0, 1, 0, int(tex.sum()), 0))
    else: rows.append((i, 0, 0, 1, 0, 0, 0))
    prev = g
open(out, 'w').write('frame,tx,ty,scale,rot,npts,inliers\n' + '\n'.join(','.join(map(str, r)) for r in rows)); print(v, i)
