#!/usr/bin/env python3
"""camstats.py CAM.csv JOINS.csv OUT.json  - moves/holds per shot from a per-frame camera track (definitions v3 s5)."""
import sys, json, numpy as np, csv
K = 50.0; THR = 0.05; MINLEN = 4; BRIDGE = 2
def load_cam(p):
    r = list(csv.DictReader(open(p))); return {k: np.array([float(x[k]) for x in r]) for k in ('tx', 'ty', 'scale')}
def load_joins(p):
    J = []
    for x in csv.DictReader(open(p)):
        try: J.append((int(float(x['start_frame'])), int(float(x['len_f']))))
        except Exception: pass
    return sorted(J)
def med3(x):
    y = x.copy(); y[1:-1] = np.median(np.stack([x[:-2], x[1:-1], x[2:]]), 0); return y
def analyse(cam, joins, N=None):
    tx, ty, sc = med3(cam['tx']), med3(cam['ty']), med3(cam['scale']); N = len(tx)
    speed = np.sqrt(tx**2 + ty**2 + (K*(sc-1))**2)
    # shots: frames (1-based) between joins; frames inside a blend and the pair straddling a cut are excluded
    excl = np.zeros(N+2, bool); bounds = [1]
    for s, L in joins:
        a, b = s-1, s+max(L, 1)     # pair indexes touching the join
        excl[max(a, 1):min(b, N)+1] = True; bounds.append(s + L//2)
    bounds.append(N+1); shots = []
    for i in range(len(bounds)-1):
        a, b = bounds[i], bounds[i+1]-1
        idx = np.array([f for f in range(a, b+1) if not excl[f] and f >= 2]);
        if len(idx) == 0: shots.append(dict(start=a, end=b, frames=0, hold_share=None, longest_hold=0, moves=[])); continue
        mv = speed[idx-1] >= THR
        # bridge short still gaps
        runs = []; j = 0
        while j < len(mv):
            if mv[j]:
                k = j
                while k+1 < len(mv) and (mv[k+1] or (not mv[k+1] and any(mv[k+1:k+2+BRIDGE]) and (k+1+BRIDGE) < len(mv) and mv[k+1:k+2+BRIDGE].sum() > 0 and (idx[min(k+1+BRIDGE, len(idx)-1)] - idx[k]) <= BRIDGE+1+0)): k += 1
                while not mv[k]: k -= 1
                runs.append((j, k)); j = k+1
            else: j += 1
        moves = []; movmask = np.zeros(len(mv), bool)
        for j, k in runs:
            if k-j+1 < MINLEN: continue
            movmask[j:k+1] = True; f = idx[j:k+1]
            S = float(np.prod(sc[f-1])); PX = float(np.sum(tx[f-1])); PY = float(np.sum(ty[f-1]))
            sp = np.convolve(speed[f-1], np.ones(3)/3, 'same'); p = float(np.argmax(sp)/max(len(sp)-1, 1))
            c = np.cumsum(speed[f-1]); c = np.concatenate([[0], c])/c[-1]; u = np.linspace(0, 1, len(c))
            tmpl = {'linear': u, 'ease-in': u**2.2, 'ease-out': 1-(1-u)**2.2, 'ease-in-out': 0.5-0.5*np.cos(np.pi*u)}
            errs = {k: float(np.sqrt(np.mean((c-v)**2))) for k, v in tmpl.items()}; ease = min(errs, key=errs.get); cv = errs[ease]
            comps = []
            if S >= 1.03: comps.append('push-in')
            if S <= 0.97: comps.append('pull-out')
            if abs(PX) >= 2: comps.append('pan')
            if abs(PY) >= 2: comps.append('tilt')
            typ = 'drift' if not comps else (comps[0] if len(comps) == 1 else 'compound:' + '+'.join(comps))
            moves.append(dict(start_f=int(f[0]), end_f=int(f[-1]), length_f=int(len(f)), type=typ, scale=round(S, 4), pan_pct=round(PX, 2), tilt_pct=round(PY, 2), peak_pos=round(p, 2), cv=round(cv, 2), ease=ease, peak_speed=round(float(sp.max()), 3), mean_speed=round(float(sp.mean()), 3)))
        still = ~movmask; lh = 0; c = 0
        for q in still:
            c = c+1 if q else 0; lh = max(lh, c)
        shots.append(dict(start=int(a), end=int(b), frames=int(len(idx)), hold_share=round(float(still.mean()), 3), longest_hold=int(lh), moves=moves))
    return dict(n_frames=int(N), moving_share=round(float(np.mean(speed[1:] >= THR)), 3), shots=shots)
if __name__ == '__main__':
    res = analyse(load_cam(sys.argv[1]), load_joins(sys.argv[2])); json.dump(res, open(sys.argv[3], 'w'), indent=1)
    print(sys.argv[1], 'shots', len(res['shots']), 'moves', sum(len(s['moves']) for s in res['shots']), 'moving_share', res['moving_share'])
