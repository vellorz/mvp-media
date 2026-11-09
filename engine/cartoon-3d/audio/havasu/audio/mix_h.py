# Soundtrack for the London Bridge -> Arizona short: Drew VO (studio clean), synthesized SFX on the picture's events,
# and the original garage bed (synth_h.py) at ONE constant level about 15 dB under the voice (no ducking, no pumping).
# Output: mix.wav (48 kHz stereo, exact film length), stems, cues.md.
import sys, subprocess, numpy as np
sys.path.insert(0, ".")
from dsp import SR, ns, rng, pan, place, fades, dbg, integrated, lp, hp, bp, phase, colored, write_wav, read_wav
import sfx_gen as G

DUR = 1985 / 30
VO_OFF = 0.2
W = lambda s: s + VO_OFF
N = ns(DUR)

def load(path, ch=2):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).astype(float).reshape(-1, ch).T

subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "../voice2/c.wav", "-af",
  "highpass=f=90,deesser=i=0.4,acompressor=threshold=-22dB:ratio=4:attack=5:release=90:makeup=4dB,alimiter=limit=0.89:attack=3:release=40",
  "voice_proc.wav"], check=True)
vo = np.zeros((2, N)); place(vo, load("voice_proc.wav", 1)[0], VO_OFF)
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

# ---- round 2 events (new voice: voice2/c.words.json; film time = word time + 0.2). Sparse like the reference:
# ~1 per 4 s, clustered at the hook, the act change and the payoff; whooshes only on place changes.
ev(0.0, rumble(0.5, 40) * np.exp(-np.arange(ns(0.5)) / SR / 0.15), 0.5, 0, "sub thump")
ev(W(1.38), coins(9), 0.55, 0.1, "coins (price)")
for t in [5.8, 20.04, 22.16, 30.46, 32.28]:
    ev(W(t) - 0.18, G.whoosh(0.45, r, peak=0.18), 0.35, r.uniform(-0.3, 0.3), "whoosh")
ev(W(5.8), G.whoosh(0.7, r, peak=0.05, f_lo=600, f_hi=5000), 0.5, 0, "flash")
ev(W(8.3), G.bubbles(2.0, r, 14), 0.5, 0.2, "bubbles (sinking)")
for t, p in [(W(11.62), -0.2), (W(12.0), 0.3), (W(12.3), 0.0)]: ev(t, horn(r.uniform(380, 460), r.uniform(500, 560)), 0.45, p, "honk")
for h in [W(15.2), W(15.78), W(16.28)]: ev(h, G.hammer_hit(r, 1.0), 0.7, 0.2, "hammer")
ev(W(18.62), chainsaw(1.6), 0.45, 0.1, "chainsaw")
ev(W(26.32), thud(1.0), 0.9, 0, "bag thud"); ev(W(26.32) + 0.02, coins(), 0.4, 0.1, "coins")
ev(W(30.7), ship_horn(1.6), 0.5, 0, "ship horn")
for k, b in enumerate([34.08, 34.4, 34.76, 35.14, 35.4]): ev(W(b), stone_clack(), 0.6, -0.6 + k * 0.3, "stone")
ev(W(39.6), G.whoosh(1.9, r, peak=0.9, f_lo=200, f_hi=900), 0.25, 0.4, "tumbleweed")
for k in range(4): ev(W(42.44) + k * 0.35 + r.uniform(0, 0.05), scrape(), 0.35, r.uniform(-0.5, 0.5), "dig")
ev(W(44.1), rush(2.4), 0.7, 0, "flood"); ev(W(44.35), G.splash_big(r), 0.45, 0, "splash")
ev(W(58.2), pop(), 0.5, -0.2, "bubble in"); ev(W(60.32), pop(), 0.6, -0.2, "bubble pop")
ev(W(61.02), thud(0.5), 0.45, 0, "poster lands")

# ---- mix, matched to the measured reference: the voice IS the mix (voice alone ~ -14 LUFS), music + SFX bed ~20 dB
# under it at one constant level (no ducking), SFX ~10 dB under the voice and capped so no hit spikes. No ambience beds.
L_vo = integrated(vo)
music *= dbg(L_vo - 20.0 - integrated(music))
sfx_pk = np.abs(sfx).max(); vo_pk = np.abs(vo).max()
sfx *= vo_pk * dbg(-9.0) / sfx_pk                     # loudest hit peaks 9 dB under the voice peak
ceil = vo_pk * dbg(-9.0); sfx = np.tanh(sfx / ceil) * ceil
mix = vo + music + sfx
g = dbg(-13.6 - integrated(mix)); mix *= g
lim = dbg(-2.0)
if np.abs(mix).max() > lim: mix = np.tanh(mix / lim) * lim
write_wav("mix.wav", mix[:, :N]); write_wav("stem_vo.wav", vo * g); write_wav("stem_music.wav", music * g); write_wav("stem_sfx.wav", sfx * g)
print("VO", round(L_vo, 1), "music rel", round(integrated(music) - L_vo, 1), "mix", round(integrated(mix), 1), "peak", round(20 * np.log10(np.abs(mix).max()), 2))
open("cues.md", "w").write("# cues\n" + "\n".join(f"- {t:6.2f}s {n}" for t, n in sorted(cues)))
