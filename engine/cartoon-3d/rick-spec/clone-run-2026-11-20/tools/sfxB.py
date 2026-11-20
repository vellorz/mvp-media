#!/usr/bin/env python3
"""sfxB.py MUSIC_STEM.wav OUT.json  - Tool B (definitions v3 s9 + amendment v3.2). scipy only, native sample rate, own framing. Shares no code with sfxA."""
import sys, json, numpy as np, soundfile as sf
from scipy import signal, ndimage
x, sr = sf.read(sys.argv[1], always_2d=True); x = x.mean(1)
hop = int(round(sr*0.005)); win = int(round(sr*0.02)); nfr = (len(x)-win)//hop
idx = np.arange(win)[None, :]+hop*np.arange(nfr)[:, None]; fr = x[idx]*np.hanning(win)[None, :]; SP = np.abs(np.fft.rfft(fr, axis=1))**2; fq = np.fft.rfftfreq(win, 1/sr); dt = hop/sr
pw = SP.sum(1)+1e-14; w = int(round(0.1/dt)); c = np.cumsum(np.concatenate([[0], pw])); L = 10*np.log10((c[w:]-c[:-w])/w)      # window starting at frame i
h = int(round(2.0/dt)); bed = ndimage.median_filter(L, size=2*h+1, mode='nearest'); ov = L-bed
lab, n = ndimage.label(ov >= 6); ev = []
lev = 10*np.log10(pw); g = np.convolve(lev, np.ones(2)/2, 'same')
for r in range(1, n+1):
    ii = np.where(lab == r)[0]; a = max(ii[0]-2, 2); b = min(ii[-1]+w, len(g)-1); d = g[a:b+1]-g[a-2:b-1]; o = a+int(np.argmax(d))-1
    ev.append((o, float(ov[ii].max()), (ii[int(np.argmax(ov[ii]))]+w/2)*dt+win/2/sr))
env = lev-ndimage.uniform_filter1d(lev, 2*h); ac = signal.correlate(env, env, mode='full', method='fft')[len(env)-1:]; lo, hi = int(2/dt), min(int(26/dt), len(ac)-2); P = (lo+int(np.argmax(ac[lo:hi])))*dt
out = []
for o, mx, tp in ev:
    reps = 0; avail = 0
    for k in range(-6, 7):
        q = o+int(round(k*P/dt))
        if k == 0 or q < 5 or q >= len(ov)-5: continue
        avail += 1
        if ov[max(q-w+4, 0):q+5].max() >= max(mx-3, 5): reps += 1
    spec = SP[o:o+w].mean(0); base = np.median(SP[max(o-h//2, 0):o+h//2:5], 0); ex = np.clip(spec-base, 0, None); cen = float((ex*fq).sum()/(ex.sum()+1e-14))
    seg = lev[o:o+int(2/dt)]; pk = int(np.argmax(seg[:24])); j = pk
    while j < len(seg)-1 and seg[j] > seg[pk]-10: j += 1
    dur = (j-pk)*dt*1000; t = o*dt+win/2/sr
    cl = 'low thud' if cen < 400 else ('bright click/pop' if cen > 2000 and dur < 120 else ('noise sweep/whoosh' if dur >= 200 else 'mid hit'))
    if not (avail >= 2 and reps >= max(2, 0.6*avail)): out.append(dict(t=round(float(t), 3), t_peak=round(float(tp), 3), frame=int(round(t*30))+1, over_bed_dB=round(mx, 1), dur_ms=int(dur), centroid_hz=int(cen), loop_repeats=reps, **{'class': cl}))
json.dump(dict(tool='sfxB', loop_period_s=round(float(P), 3), n_runs=len(ev), events=out), open(sys.argv[2], 'w'), indent=1); print(sys.argv[1], 'events', len(out), 'of runs', len(ev), 'loopP', round(float(P), 3))
