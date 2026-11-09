# Soundtrack for the Eiffel Tower short: Drew VO take a, synthesized SFX on the picture's events, the original garage
# bed (synth_e.py 'eiffel') at ONE constant level ~20 dB under the voice. Same chain/levels the owner approved on r2.
import sys, subprocess, numpy as np
sys.path.insert(0, ".")
from dsp import SR, ns, rng, pan, place, fades, dbg, integrated, lp, hp, bp, phase, colored, write_wav
import sfx_gen as G
DUR = 1962 / 30; VO_OFF = 0.2; W = lambda s: s + VO_OFF; N = ns(DUR)
def load(path, ch=2):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).astype(float).reshape(-1, ch).T
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "../voice/a.wav", "-af",
  "highpass=f=90,deesser=i=0.4,acompressor=threshold=-22dB:ratio=4:attack=5:release=90:makeup=4dB,alimiter=limit=0.89:attack=3:release=40",
  "voice_proc.wav"], check=True)
vo = np.zeros((2, N)); place(vo, load("voice_proc.wav", 1)[0], VO_OFF)
music = np.zeros((2, N)); m = load("eiffel-music.wav"); place(music, m[:, :N], 0.0)
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
for t in [4.58, 8.28, 13.58, 20.88, 25.26, 31.32, 40.48, 46.88, 51.98, 56.1]:
    ev(W(t) - 0.18, G.whoosh(0.45, r, peak=0.18), 0.32, r.uniform(-0.3, 0.3), "whoosh (cut)")
ev(0.0, thud(0.4), 0.5, 0, "sub thump")
for k, h in enumerate([W(2.7), W(3.2), W(3.62)]): ev(h, G.hammer_hit(r, 1.0), 0.7, -0.2 + 0.2 * k, "sledgehammer")
ev(W(4.58), G.whoosh(0.7, r, peak=0.05, f_lo=600, f_hi=5000), 0.5, 0, "flash")
ev(W(6.4), G.applause(1.6, r, people=24) if hasattr(G, "applause") else paper(), 0.35, 0, "fair crowd")
ev(W(11.9), paper(0.5), 0.6, 0.1, "letter up"); ev(W(13.2), stamp(), 0.6, 0.2, "wax seal")
ev(W(17.8), pop(), 0.5, 0, "why?")
ev(W(22.3), paper(0.35), 0.6, -0.1, "calendar flip"); ev(W(24.56), stamp(), 0.7, 0, "come down")
for h in [W(28.26), W(28.6), W(28.95)]: ev(h, G.hammer_hit(r, 0.6), 0.5, 0.3, "bolt")
ev(W(30.16), falling(0.8), 0.5, 0, "drop"); ev(W(30.16) + 0.8, thud(0.6), 0.6, 0, "ball lands")
ev(W(33.0), zap(0.6), 0.5, 0, "radio on"); ev(W(33.0), ding(), 0.4, 0, "radio ding")
ev(W(36.3), beeps(1.2), 0.5, -0.3, "morse (french)")
ev(W(40.6), marching(5.4), 0.5, -0.4, "column march")
ev(W(42.12), static(3.8), 0.55, 0.2, "jamming static")
ev(W(46.1), thud(0.5), 0.5, -0.2, "column stops")
ev(W(47.66), beeps(1.4), 0.5, 0.2, "coded message"); ev(W(50.32), stamp(), 0.55, 0, "H-21")
ev(W(56.78), thud(0.45), 0.45, 0, "paint tons")
ev(W(59.2), G.whoosh(0.6, r, peak=0.2), 0.4, 0, "to poster"); ev(W(60.0), thud(0.5), 0.45, 0, "poster lands")
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
