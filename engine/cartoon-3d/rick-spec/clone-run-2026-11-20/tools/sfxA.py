#!/usr/bin/env python3
"""sfxA.py MUSIC_STEM.wav OUT.json  - Tool A (definitions v3 s9 + amendment v3.2). librosa STFT at 22.05 kHz."""
import sys, json, numpy as np, librosa, soundfile as sf, warnings; warnings.filterwarnings('ignore')
y, sr = sf.read(sys.argv[1], always_2d=True); y = y.mean(1); SR = sr
HOP = int(round(SR*0.01)); NF = 2048; S = np.abs(librosa.stft(y, n_fft=NF, hop_length=HOP, center=False))**2; F = librosa.fft_frequencies(sr=SR, n_fft=NF); dt = HOP/SR
p = S.sum(0)+1e-14; N = len(p); W = int(round(0.1/dt))
L = 10*np.log10(np.convolve(p, np.ones(W)/W, 'valid'))          # L[i] = level of the 100 ms window starting at frame i
H = int(round(2.0/dt)); bed = np.array([np.median(L[max(i-H, 0):i+H:4]) for i in range(len(L))]); over = L-bed
# loop period: autocorrelation of detrended 10 ms level
e = 10*np.log10(p); e = e-np.convolve(e, np.ones(2*H)/(2*H), 'same'); ac = np.correlate(e, e, 'full')[N-1:]; lo, hi = int(2/dt), min(int(26/dt), N-2)
P = float((lo+int(np.argmax(ac[lo:hi])))*dt)
ev = []; i = 0
while i < len(over):
    if over[i] >= 6:
        j = i
        while j+1 < len(over) and over[j+1] >= 6: j += 1
        a = max(i-1, 1); b = min(j+W, N-1); d = 10*np.log10(p[a:b+1])-10*np.log10(p[a-1:b]); o = a+int(np.argmax(d))   # onset = steepest 10 ms rise
        ev.append(dict(i=o, t=o*dt+NF/2/SR, tp=(i+int(np.argmax(over[i:j+1]))+W/2)*dt+NF/2/SR, over=float(over[i:j+1].max()), run=(i, j))); i = j+1
    else: i += 1
out = []
for x in ev:
    o = x['i']; reps = 0; avail = 0
    for k in range(-6, 7):
        q = o+int(round(k*P/dt))
        if k == 0 or q < 3 or q >= len(over)-3: continue
        avail += 1
        if over[max(q-W+2, 0):q+3].max() >= max(x['over']-3, 5): reps += 1
    spec = S[:, o:o+W].mean(1); a0 = max(o-H//2, 0); base = np.median(S[:, a0:o+H//2:3], 1); ex = np.clip(spec-base, 0, None); cen = float((ex*F).sum()/(ex.sum()+1e-14))
    lv = 10*np.log10(p[o:o+int(2/dt)]); pk = int(np.argmax(lv[:12])); j = pk
    while j < len(lv)-1 and lv[j] > lv[pk]-10: j += 1
    dur = (j-pk)*dt*1000
    cl = 'low thud' if cen < 400 else ('bright click/pop' if cen > 2000 and dur < 120 else ('noise sweep/whoosh' if dur >= 200 else 'mid hit'))
    rec = dict(t=round(x['t'], 3), t_peak=round(x['tp'], 3), frame=int(round(x['t']*30))+1, over_bed_dB=round(x['over'], 1), dur_ms=int(dur), centroid_hz=int(cen), loop_repeats=reps, **{'class': cl})
    rec['loop_avail'] = avail
    if not (avail >= 2 and reps >= max(2, 0.6*avail)): out.append(rec)
json.dump(dict(tool='sfxA', loop_period_s=round(P, 3), n_runs=len(ev), events=out), open(sys.argv[2], 'w'), indent=1); print(sys.argv[1], 'events', len(out), 'of runs', len(ev), 'loopP', round(P, 3))
