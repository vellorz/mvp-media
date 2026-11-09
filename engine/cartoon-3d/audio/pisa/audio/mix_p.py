# Soundtrack for the Leaning Tower of Pisa short: Drew VO take a, synthesized SFX on the picture's events, the original garage
# bed (synth_p.py 'pisa') at ONE constant level ~20 dB under the voice. Same chain/levels the owner approved on r2.
import sys, subprocess, numpy as np
sys.path.insert(0, ".")
from dsp import SR, ns, rng, pan, place, fades, dbg, integrated, lp, hp, bp, phase, colored, write_wav
import sfx_gen as G
DUR = 2080 / 30; VO_OFF = 0.2; W = lambda s: s + VO_OFF; N = ns(DUR)
def load(path, ch=2):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).astype(float).reshape(-1, ch).T
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "../voice/a.wav", "-af",
  "highpass=f=90,deesser=i=0.4,acompressor=threshold=-22dB:ratio=4:attack=5:release=90:makeup=4dB,alimiter=limit=0.89:attack=3:release=40",
  "voice_proc.wav"], check=True)
vo = np.zeros((2, N)); place(vo, load("voice_proc.wav", 1)[0], VO_OFF)
music = np.zeros((2, N)); m = load("pisa-music.wav"); place(music, m[:, :N], 0.0)
sfx = np.zeros((2, N)); cues = []
def ev(t, x, g=1.0, p=0.0, name=""):
    x = np.asarray(x, float); place(sfx, pan(x, p) if x.ndim == 1 else x, t, g); cues.append((t, name))
r = rng(21)
def thud(big=1.0):
    t = np.arange(ns(0.8)) / SR
    return (np.sin(phase(55 * (1 + 0.8 * np.exp(-t / 0.03)))) * np.exp(-t / 0.18) * 1.6 + bp(r.standard_normal(len(t)), 300, 3000) * np.exp(-t / 0.03)) * big
def pop():
    t = np.arange(ns(0.15)) / SR; return np.sin(phase(500 + 1400 * t / 0.15)) * np.exp(-t / 0.03) * 0.6
def paper(dur=0.4):
    t = np.arange(ns(dur)) / SR; x = bp(r.standard_normal(len(t)), 1500, 7000)
    return x * (0.4 + 0.6 * np.abs(np.sin(t * 60))) * np.sin(np.pi * t / t[-1]) * 0.4
def stamp():
    t = np.arange(ns(0.3)) / SR
    return np.sin(phase(140 * (1 + np.exp(-t / 0.01)))) * np.exp(-t / 0.05) + bp(r.standard_normal(len(t)), 500, 4000) * np.exp(-t / 0.01) * 0.6
def ding(f=1320):
    t = np.arange(ns(1.0)) / SR; return (np.sin(phase(np.full(len(t), f))) + 0.4 * np.sin(phase(np.full(len(t), f * 2.76)))) * np.exp(-t / 0.35) * 0.35
def falling(dur=0.9):
    t = np.arange(ns(dur)) / SR; return np.sin(phase(1800 - 1300 * t / dur)) * 0.25 * np.minimum(1, t / 0.05)
def zap(dur=0.6):
    t = np.arange(ns(dur)) / SR; f = 600 + 400 * np.sin(t * 40)
    return lp(np.sign(np.sin(phase(f))) * 0.3, 3000) * np.exp(-t / 0.3)
def static(dur):
    n = ns(dur); t = np.arange(n) / SR; x = bp(r.standard_normal(n), 800, 6000) * (0.5 + 0.5 * (r.random(n) > 0.6))
    return lp(x, 5000) * np.minimum(1, t / 0.1) * np.minimum(1, (dur - t) / 0.2) * 0.35
def beeps(dur=1.4):  # morse
    y = np.zeros(ns(dur)); k = 0.0
    for d in [0.06, 0.18, 0.06, 0.06, 0.18, 0.18, 0.06]:
        t = np.arange(ns(d)) / SR; s = np.sin(phase(np.full(len(t), 880))) * 0.3; i = ns(k); y[i:i + len(s)] += s[: len(y) - i]; k += d + 0.07
    return y
def marching(dur):
    y = np.zeros(ns(dur)); k = 0.0
    while k < dur - 0.2:
        b = G.boot(r, 0.7) if hasattr(G, "boot") else thud(0.2); i = ns(k); y[i:i + len(b)] += b[: len(y) - i] * 0.5; k += 0.55
    return y
def squish(dur=0.5):
    t = np.arange(ns(dur)) / SR; return bp(r.standard_normal(len(t)), 300, 2500) * (0.5 + 0.5 * np.sin(t * 40)) * np.sin(np.pi * t / t[-1]) * 0.5
def drill(dur):
    t = np.arange(ns(dur)) / SR; f = 95 + 6 * np.sin(t * 7)
    return bp(np.sign(np.sin(phase(f))) * 0.5 + 0.4 * r.standard_normal(len(t)), 150, 3000) * np.minimum(1, t / 0.2) * np.minimum(1, (dur - t) / 0.3) * 0.3
def creak(dur=1.6):
    return G.creak(dur, r) if hasattr(G, "creak") else thud(0.3)
for t in [4.72, 7.3, 12.22, 16.48, 22.42, 27.82, 34.96, 38.24, 41.06, 44.74, 48.92, 53.6, 55.56, 58.96]:
    ev(W(t) - 0.18, G.whoosh(0.45, r, peak=0.18), 0.32, r.uniform(-0.3, 0.3), "whoosh (cut)")
ev(0.0, thud(0.4), 0.5, 0, "sub thump")
ev(W(3.7), creak(1.4), 0.5, 0.2, "tower creak (falling over)")
ev(W(7.3), G.whoosh(0.7, r, peak=0.05, f_lo=600, f_hi=5000), 0.5, 0, "flash")
ev(W(8.34), creak(1.6), 0.55, -0.2, "starts leaning"); ev(W(8.62), paper(0.35), 0.5, 0.3, "calendar 1178")
ev(W(15.4), squish(0.9), 0.7, 0, "sponge squish")
for g, tt in enumerate([17.64, 18.34, 19.02]): ev(W(tt) - 0.3, marching(1.6), 0.45, -0.5 + 0.5 * g, "army march")
ev(W(19.8), thud(0.35), 0.5, 0.2, "tools dropped"); ev(W(21.26), paper(0.35), 0.6, -0.1, "calendar 1272")
ev(W(25.9), thud(0.3), 0.4, 0, "soil packs")
for tt in [31.86, 32.6, 33.14, 34.02, 34.6]: ev(W(tt), thud(0.5), 0.5, r.uniform(-0.3, 0.3), "floor lands")
ev(W(37.62), pop(), 0.7, 0.2, "banana pop")
ev(W(39.46), ding(1100), 0.45, 0, "5.5 degrees")
for k in range(10): ev(W(41.52) + k * (W(43.38) - W(41.52)) / 10, thud(0.25), 0.4, r.uniform(-0.4, 0.4), "lead block")
ev(W(45.12), drill(3.6), 0.5, -0.2, "drills")
ev(W(49.3), creak(2.2), 0.55, 0, "settles back"); ev(W(50.4), pop(), 0.5, 0.2, "45 cm tag"); ev(W(52.2), paper(0.35), 0.5, 0.2, "1838 tag")
ev(W(54.36), stamp(), 0.6, 0, "STOP")
ev(W(59.66), ding(1320), 0.4, 0, "2001")
ev(W(63.68), G.whoosh(0.6, r, peak=0.2), 0.4, 0, "to poster"); ev(W(64.4), thud(0.5), 0.45, 0, "poster lands")
L_vo = integrated(vo)
music *= dbg(L_vo - 20.0 - integrated(music))
vo_pk = np.abs(vo).max(); sfx *= vo_pk * dbg(-9.0) / np.abs(sfx).max()
ceil = vo_pk * dbg(-9.0); sfx = np.tanh(sfx / ceil) * ceil
mix = vo + music + sfx; g = dbg(-13.6 - integrated(mix)); mix *= g
lim = dbg(-2.0)
if np.abs(mix).max() > lim: mix = np.tanh(mix / lim) * lim
write_wav("mix.wav", mix[:, :N]); write_wav("stem_vo.wav", vo * g); write_wav("stem_music.wav", music * g); write_wav("stem_sfx.wav", sfx * g)
print("VO", round(L_vo, 1), "music rel", round(integrated(music) - L_vo, 1), "mix", round(integrated(mix), 1), "peak", round(20 * np.log10(np.abs(mix).max()), 2))
open("cues.md", "w").write("# cues\n" + "\n".join(f"- {t:6.2f}s {n}" for t, n in sorted(cues)))
