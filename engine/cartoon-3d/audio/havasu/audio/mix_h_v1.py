# Soundtrack for the London Bridge -> Arizona short: Drew VO (studio clean), synthesized SFX on the picture's events,
# and the original garage bed (synth_h.py) at ONE constant level about 15 dB under the voice (no ducking, no pumping).
# Output: mix.wav (48 kHz stereo, exact film length), stems, cues.md.
import sys, subprocess, numpy as np
sys.path.insert(0, ".")
from dsp import SR, ns, rng, pan, place, fades, dbg, integrated, lp, hp, bp, phase, colored, write_wav, read_wav
import sfx_gen as G

DUR = 2130 / 30
VO_OFF = 0.2
W = lambda s: s + VO_OFF
N = ns(DUR)

def load(path, ch=2):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).astype(float).reshape(-1, ch).T

vo = np.zeros((2, N)); place(vo, load("../voice/voice.wav", 1)[0], VO_OFF)
music = np.zeros((2, N)); m = load("havasu-music.wav"); place(music, m[:, : N], 0.0)
sfx = np.zeros((2, N)); amb = np.zeros((2, N))
cues = []
def ev(t, x, g=1.0, p=0.0, name=""):
    x = np.asarray(x, float)
    place(sfx, pan(x, p) if x.ndim == 1 else x, t, g); cues.append((t, name))
def bed(t0, t1, x, g=1.0, fin=0.25, fout=0.25):
    x = np.asarray(x, float); x = x if x.ndim == 2 else pan(x)
    x = x[:, : ns(t1 - t0)]
    n = x.shape[1]; e = np.ones(n); a, b = ns(fin), ns(fout)
    e[:a] = np.linspace(0, 1, a); e[-b:] *= np.linspace(1, 0, b)
    place(amb, x * e, t0, g)
r = rng(11)

def horn(f1=420, f2=528, dur=0.35):
    t = np.arange(ns(dur)) / SR
    x = np.sign(np.sin(phase(np.full(len(t), f1)))) + np.sign(np.sin(phase(np.full(len(t), f2))))
    return fades(lp(x, 2400) * 0.25, 0.01, 0.05)
def ship_horn(dur=1.6):
    t = np.arange(ns(dur)) / SR
    x = sum(np.sin(phase(np.full(len(t), f))) / (k + 1) for k, f in enumerate([98, 147, 196, 294]))
    e = np.minimum(1, t / 0.12) * np.minimum(1, (dur - t) / 0.3)
    return lp(np.tanh(x * 1.5), 1200) * e * 0.5
def chainsaw(dur=1.5):
    t = np.arange(ns(dur)) / SR
    f = 70 + 80 * np.minimum(1, t / 0.4) + 25 * np.sin(t * 9)
    x = np.sign(np.sin(phase(f))) * (0.6 + 0.4 * np.sin(phase(f * 0.5)))
    x = bp(x + 0.3 * r.standard_normal(len(t)), 120, 4000)
    return fades(x * np.minimum(1, (dur - t) / 0.25) * 0.35, 0.02, 0.1)
def thud(big=1.0):
    t = np.arange(ns(0.8)) / SR
    return (np.sin(phase(55 * (1 + 0.8 * np.exp(-t / 0.03)))) * np.exp(-t / 0.18) * 1.6 + bp(r.standard_normal(len(t)), 300, 3000) * np.exp(-t / 0.03)) * big
def coins(n=7):
    y = np.zeros(ns(0.9))
    for k in range(n):
        c = G.clink(r, bright=1.2); i = ns(0.05 + r.uniform(0, 0.6)); y[i:i + len(c)] += c[: len(y) - i] * r.uniform(0.4, 0.9)
    return y
def stone_clack():
    t = np.arange(ns(0.5)) / SR
    return np.sin(phase(90 * (1 + 0.5 * np.exp(-t / 0.02)))) * np.exp(-t / 0.08) * 1.2 + bp(r.standard_normal(len(t)), 800, 5000) * np.exp(-t / 0.015) * 0.8
def scrape():
    t = np.arange(ns(0.35)) / SR
    return bp(r.standard_normal(len(t)), 600, 3500) * np.sin(np.pi * t / t[-1]) ** 2 * 0.5
def pop():
    t = np.arange(ns(0.15)) / SR
    return np.sin(phase(500 + 1400 * t / 0.15)) * np.exp(-t / 0.03) * 0.6
def rumble(dur, f=45):
    n = ns(dur); t = np.arange(n) / SR
    return lp(r.standard_normal(n), 140) * 2.0 + np.sin(phase(np.full(n, f) + 4 * np.sin(t * 3))) * 0.4
def rush(dur):
    n = ns(dur); t = np.arange(n) / SR
    return bp(colored(n, r, 0.3), 150, 6000) * np.minimum(1, t / 0.3) * np.minimum(1, (dur - t) / 0.6) * 0.9

# ---- cuts: soft whooshes on the big place changes ----
for t in [2.58, 5.1, 190 / 30, 697 / 30, 760 / 30, 958 / 30, 1012 / 30, 1070 / 30, 1239 / 30, 1626 / 30, 1797 / 30, 1927 / 30]:
    ev(t - 0.18, G.whoosh(0.45, r, peak=0.18), 0.35, r.uniform(-0.3, 0.3), "whoosh")
ev(190 / 30, G.whoosh(0.7, r, peak=0.05, f_lo=600, f_hi=5000), 0.5, 0, "flash")
# ---- ambience beds ----
bed(0, 6.4, G.breeze(6.5, r, 0.8), 0.35)
bed(6.33, 23.3, G.applause(17, r, people=0) * 0 + G.breeze(17, r, 0.3), 0.15)
city = np.zeros(ns(22));
for k in range(8): city += np.pad(G.babble(21.5, r, r.uniform(110, 220), r.uniform(0.9, 1.1)), (0, ns(22) - ns(21.5)))[: ns(22)] * 0.25
bed(6.33, 23.3, city, 0.18); bed(25.33, 31.93, city[: ns(7)], 0.15)
bed(10.33, 15.1, rumble(4.8), 0.3)
bed(31.93, 33.73, G.water_bed(1.9, r, 1.2), 0.5)
bed(33.73, 35.67, rumble(2.0, 38), 0.7)
bed(35.67, 51.3, G.breeze(15.7, r, 0.7), 0.3)
bed(51.3, 64.3, G.water_bed(13, r, 0.6), 0.25)
crowd2 = np.zeros(ns(6));
for k in range(6): crowd2 += G.babble(6, r, r.uniform(110, 240), r.uniform(0.9, 1.1)) * 0.25
bed(54.2, 59.9, crowd2, 0.16)
# ---- events ----
for t, p in [(W(11.6), -0.2), (W(12.2), 0.3), (W(12.6), 0.0)]: ev(t, horn(r.uniform(380, 460), r.uniform(500, 560)), 0.45, p, "honk")
ev(W(13.1), G.bubbles(2.0, r, 14), 0.5, 0.2, "bubbles")
for k in range(6): ev(W(16.24) + r.uniform(0, 0.25), G.whoa(r), 0.35, r.uniform(-0.6, 0.6), "gasp")
for h in [W(17.72), W(18.52), W(18.98)]: ev(h, G.hammer_hit(r, 1.0), 0.7, 0.2, "hammer")
ev(W(21.68), chainsaw(1.6), 0.45, 0.1, "chainsaw")
for k in range(4): ev(W(21.8) + r.uniform(0, 0.3), G.whoa(r), 0.25, r.uniform(-0.6, 0.6), "gasp")
ev(W(27.1), thud(1.0), 0.9, 0, "bag thud"); ev(W(27.1) + 0.02, coins(), 0.4, 0.1, "coins")
for k in range(5): ev(28.0 + k * 0.62, G.hammer_hit(r, 0.5), 0.18, -0.4, "chisel")
ev(W(32.2), ship_horn(1.6), 0.5, 0, "ship horn")
for k, b in enumerate([35.9, 36.04, 36.2, 36.36, 36.55, 36.74, 36.96, 37.18, 37.44]): ev(W(b), stone_clack(), 0.6, -0.6 + k * 0.15, "stone")
for k in range(5): ev(W(39.7) + r.uniform(0, 0.3), G.hurrah(r, r.uniform(110, 170), r.uniform(0.95, 1.05)), 0.3, r.uniform(-0.5, 0.5), "hurrah")
ev(W(44.6), G.whoosh(1.9, r, peak=0.9, f_lo=200, f_hi=900), 0.25, 0.4, "tumbleweed")
for k in range(10): ev(46.6 + k * 0.42 + r.uniform(0, 0.1), scrape(), 0.35, r.uniform(-0.5, 0.5), "dig")
ev(W(50.5), rush(2.4), 0.7, 0, "flood"); ev(W(50.75), G.splash_big(r), 0.45, 0, "splash")
ev(W(61.0), pop(), 0.5, -0.2, "bubble in"); ev(W(62.86), pop(), 0.6, -0.2, "bubble pop")

# ---- mix: VO as recorded, bed at a constant level 15 dB under the voice, SFX under the voice ----
L_vo = integrated(vo)
music *= dbg(L_vo - 15.0 - integrated(music))
sfx *= dbg(-3.0); amb *= dbg(-6.0)
mix = vo + music + sfx + amb
g = dbg(-14.0 - integrated(mix)); mix *= g
pk = np.abs(mix).max()
if pk > dbg(-1.5): mix = np.tanh(mix / dbg(-1.5)) * dbg(-1.5)
write_wav("mix.wav", mix[:, :N]); write_wav("stem_vo.wav", vo * g); write_wav("stem_music.wav", music * g); write_wav("stem_sfx.wav", (sfx + amb) * g)
print("VO", round(L_vo, 1), "music rel", round(integrated(music) - L_vo, 1), "mix", round(integrated(mix), 1), "peak", round(20 * np.log10(np.abs(mix).max()), 2))
open("cues.md", "w").write("# cues\n" + "\n".join(f"- {t:6.2f}s {n}" for t, n in sorted(cues)))
