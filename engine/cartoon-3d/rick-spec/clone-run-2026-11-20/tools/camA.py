#!/usr/bin/env python3
"""camA.py VIDEO OUT.csv  - Tool A (definitions v3 s5): Shi-Tomasi + pyramidal LK + RANSAC similarity. Per frame pair: tx,ty (% W per frame), scale, rot(deg)."""
import sys, subprocess, numpy as np, cv2
v, out = sys.argv[1], sys.argv[2]; W, H = 540, 960
p = subprocess.Popen(['ffmpeg','-v','error','-i',v,'-vf',f'scale={W}:{H}:flags=area','-f','rawvideo','-pix_fmt','gray','-'], stdout=subprocess.PIPE)
mask = np.full((H, W), 255, np.uint8); mask[int(.655*H):int(.745*H), :] = 0
prev = None; rows = []; i = 0
while True:
    b = p.stdout.read(W*H)
    if len(b) < W*H: break
    i += 1; g = np.frombuffer(b, np.uint8).reshape(H, W)
    if prev is not None:
        tx = ty = 0.0; s = 1.0; r = 0.0; n = 0; inl = 0
        pts = cv2.goodFeaturesToTrack(prev, 600, 0.01, 8, mask=mask)
        if pts is not None and len(pts) >= 12:
            nxt, st, err = cv2.calcOpticalFlowPyrLK(prev, g, pts, None, winSize=(21, 21), maxLevel=3)
            ok = st.ravel() == 1
            # exclude points landing in caption band
            a0 = pts[ok].reshape(-1, 2); a1 = nxt[ok].reshape(-1, 2)
            keep = ~((a1[:, 1] > .655*H) & (a1[:, 1] < .745*H)); a0 = a0[keep]; a1 = a1[keep]; n = len(a0)
            if n >= 12:
                M, inm = cv2.estimateAffinePartial2D(a0, a1, method=cv2.RANSAC, ransacReprojThreshold=1.5, maxIters=3000, confidence=0.995)
                if M is not None:
                    s = float(np.hypot(M[0, 0], M[1, 0])); r = float(np.degrees(np.arctan2(M[1, 0], M[0, 0])))
                    # translation of the frame centre
                    c = np.array([W/2, H/2]); c2 = M[:, :2] @ c + M[:, 2]
                    tx = float((c2[0]-c[0])/W*100); ty = float((c2[1]-c[1])/W*100); inl = int(inm.sum())
        rows.append((i, round(tx, 4), round(ty, 4), round(s, 5), round(r, 4), n, inl))
    else:
        rows.append((i, 0, 0, 1, 0, 0, 0))
    prev = g
open(out, 'w').write('frame,tx,ty,scale,rot,npts,inliers\n' + '\n'.join(','.join(map(str, r)) for r in rows)); print(v, i)
