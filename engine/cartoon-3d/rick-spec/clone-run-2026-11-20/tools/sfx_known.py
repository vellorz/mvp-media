#!/usr/bin/env python3
"""sfx_known.py BED.wav VO.wav OUTDIR SEED - known-answer mix: our own bed + narration at Rick's measured gap (16 dB), plus 20 synthetic SFX of known time/level/class. Writes mix.wav, music_true.wav (bed+sfx), truth.json"""
import sys, json, os, numpy as np, soundfile as sf
bedp, vop, out, seed = sys.argv[1:5]; rng = np.random.default_rng(int(seed)); os.makedirs(out, exist_ok=True)
b, sr = sf.read(bedp, always_2d=True); v, sr2 = sf.read(vop, always_2d=True); b = b.mean(1); v = v.mean(1)
if sr2 != sr:
    import librosa; v = librosa.resample(v, orig_sr=sr2, target_sr=sr)
n = min(len(b), len(v), sr*58); b = b[:n]; v = v[:n]
rms = lambda x: np.sqrt(np.mean(x**2)+1e-14)
v = v/rms(v)*10**(-17/20); b = b/rms(b)*10**(-33/20)     # VO about 16 dB over the bed
def env(x, a=0.004, d=0.08):
    t = np.arange(len(x))/sr; return x*np.minimum(t/a, 1)*np.exp(-np.maximum(t-a, 0)/d)
def make(cl):
    if cl == 'low thud': L = int(.18*sr); t = np.arange(L)/sr; return env(np.sin(2*np.pi*(90*t-60*t*t)), d=0.05)
    if cl == 'bright click/pop': L = int(.06*sr); return env(rng.standard_normal(L)*1.0, a=0.001, d=0.012) - 0  # wideband click
    if cl == 'noise sweep/whoosh':
        L = int(.5*sr); x = rng.standard_normal(L); from scipy import signal
        f0 = np.linspace(500, 5000, L); ph = np.cumsum(2*np.pi*f0/sr); x = signal.lfilter(*signal.butter(2, [400/(sr/2), 8000/(sr/2)], 'band'), x)*(0.6+0.4*np.sin(ph)); w = np.sin(np.pi*np.arange(L)/L)**1.2; return x*w
    L = int(.15*sr); t = np.arange(L)/sr; return env(np.sin(2*np.pi*900*t)+0.5*np.sin(2*np.pi*1350*t), d=0.04)   # mid hit
classes = ['low thud', 'bright click/pop', 'noise sweep/whoosh', 'mid hit']*5; rng.shuffle(classes)
times = np.sort(rng.uniform(2, 56, 20))
for i in range(1, 20):
    if times[i]-times[i-1] < 0.6: times[i] = times[i-1]+0.6+rng.uniform(0, .3)
sfx = np.zeros(n); truth = []
for t0, cl in zip(times, classes):
    s = make(cl); i0 = int(t0*sr); s = s[:n-i0]
    # local bed level (2 s median of 100 ms windows)
    seg = b[max(i0-sr, 0):i0+sr]; w = [10*np.log10(np.mean(seg[k:k+sr//10]**2)+1e-14) for k in range(0, len(seg)-sr//10, sr//20)]; B = float(np.median(w))
    over = float(rng.uniform(8, 16)); k100 = sr//10; pk = max(10*np.log10(np.mean(s[k:k+k100]**2)+1e-14) for k in range(0, max(len(s)-k100, 1), sr//100)) if len(s) > k100 else 10*np.log10(np.mean(np.pad(s, (0, k100-len(s)))**2)+1e-14)
    s = s*10**((B+over-pk)/20); sfx[i0:i0+len(s)] += s; truth.append(dict(t=round(float(t0), 3), over_bed_dB=round(over, 1), **{'class': cl}))
music = b+sfx; mix = v+music; pk = np.abs(mix).max(); g = 0.8/pk
sf.write(out+'/mix.wav', np.stack([mix*g, mix*g], 1), sr); sf.write(out+'/music_true.wav', music*g, sr); json.dump(dict(events=truth), open(out+'/truth.json', 'w'), indent=1); print(len(truth))
