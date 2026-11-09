"""synth2.py (steady-level beds, gentle internal pump only) <name> -> <name>-music.wav : original UK garage / house beds, composed in code (we own them), bar lines placed on each video's payoff line."""
import sys, subprocess, numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100
rng = np.random.default_rng(7)
NOTE = {n: i for i, n in enumerate(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])}
def hz(n, o): return 440 * 2 ** ((NOTE[n] + 12 * (o + 1) - 69) / 12)
def midi_hz(m): return 440 * 2 ** ((m - 69) / 12)
def lp(x, f, o=2): return sosfilt(butter(o, min(f, SR / 2 - 100), 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def env(n, a, d):  # attack/exp-decay envelope, seconds
    t = np.arange(n) / SR; e = np.exp(-t / d); k = int(a * SR)
    if k: e[:k] *= np.linspace(0, 1, k)
    return e
def saw(f, n, harm=24):  # band-limited saw, slight analog drift
    t = np.arange(n) / SR; out = np.zeros(n)
    for h in range(1, harm + 1):
        if f * h > 9000: break
        out += np.sin(2 * np.pi * f * h * t + h) / h
    return out

# ---------------- drums ----------------
def kick(punch=1.0):
    n = int(.42 * SR); t = np.arange(n) / SR
    f = 46 + 120 * np.exp(-t * 32); ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 6.5); click = hp(rng.standard_normal(n), 2500) * np.exp(-t * 300) * .25
    return np.tanh((body + click) * 1.6 * punch)
def clap():
    n = int(.35 * SR); t = np.arange(n) / SR; x = bp(rng.standard_normal(n), 900, 6000); e = np.zeros(n)
    for d in (0, .011, .022): e += (t >= d) * np.exp(-np.clip(t - d, 0, None) * (90 if d < .02 else 18))
    tone = np.sin(2 * np.pi * 210 * t) * np.exp(-t * 40) * .3
    return x * e * .55 + tone
def hat(open_=False):
    n = int((.32 if open_ else .06) * SR); t = np.arange(n) / SR
    x = hp(rng.standard_normal(n), 7000, 4); return x * np.exp(-t * (11 if open_ else 70)) * (.32 if open_ else .3)
def shaker():
    n = int(.08 * SR); t = np.arange(n) / SR
    return bp(rng.standard_normal(n), 5000, 12000) * np.sin(np.pi * t / t[-1]) ** 2 * .16
def rim():
    n = int(.08 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1700 * t) * .5 + bp(rng.standard_normal(n), 2000, 6000)) * np.exp(-t * 80) * .35

# ---------------- tonal ----------------
def stab(chord, dur, bright):  # detuned saw chord, house organ-ish
    n = int(dur * SR); x = np.zeros(n)
    for m in chord:
        for det in (-.07, .07): x += saw(midi_hz(m + det), n, 14)
    x = lp(x, bright) * env(n, .004, dur * .45)
    return x / max(1, len(chord)) * .5
def pad(chord, dur, bright):
    n = int(dur * SR); x = np.zeros(n); t = np.arange(n) / SR
    for m in chord:
        for det in (-.12, 0, .12): x += saw(midi_hz(m + det), n, 10)
    a = np.minimum(1, t / .25) * np.minimum(1, (dur - t) / .2).clip(0)
    return lp(x, bright) * a / len(chord) * .22
def sub(m, dur):
    n = int(dur * SR); t = np.arange(n) / SR; f = midi_hz(m)
    x = np.sin(2 * np.pi * f * t) + .25 * np.sin(4 * np.pi * f * t) + .12 * np.sign(np.sin(2 * np.pi * f * t))
    return np.tanh(lp(x, 400) * 1.4) * env(n, .005, dur * .9) * .55
def pluck(m, dur):
    n = int(dur * SR); x = saw(midi_hz(m), n, 18) + .5 * saw(midi_hz(m + 12.05), n, 10)
    return lp(x, 3200) * env(n, .002, .12) * .22
def riser(dur):
    n = int(dur * SR); t = np.arange(n) / SR; out = np.zeros(n); x = rng.standard_normal(n); step = 2205
    for i, k in enumerate(range(0, n, step)):
        fr = i * step / n; lo = 300 + 6000 * fr ** 2; seg = x[k:k + step]
        out[k:k + len(seg)] = bp(seg, lo, lo * 2.2)
    tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / dur) ** 2) / SR) * .15
    return (out * .5 + tone) * (t / dur) ** 2
def impact():
    n = int(2.2 * SR); t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-t * 9)) / SR) * np.exp(-t * 2.2)
    crash = hp(rng.standard_normal(n), 3000) * np.exp(-t * 2.8) * .35
    return np.tanh(boom * 1.3) * .8 + crash

# ---------------- arrangement ----------------
TRACKS = {
  # Pisa short: sunny Italian house in D; lift on "By 1990" (film 38.44 s), end stab after "frame"
  'pisa': dict(dur=69.33, bpm=123.9, t0=-0.306, style='house', drop=1, lift=20, end_bar=35,
      prog=[[62, 66, 69, 73, 76], [59, 62, 66, 69, 73], [55, 59, 62, 66], [57, 61, 64, 66]],  # Dmaj9 Bm9 Gmaj7 A6
      bass=[38, 35, 31, 33], lead=[78, 81, 83, 86, 83, 81, 78, 74]),
  # Eiffel Tower short: bright Parisian UK garage in F; lift on "radio" (film 33.2 s), end stab after "frame"
  'eiffel': dict(dur=65.4, bpm=125.49, t0=-1.226, style='garage', drop=1, lift=18, end_bar=34,
      prog=[[65, 69, 72, 76, 79], [62, 65, 69, 72, 76], [58, 62, 65, 69], [60, 64, 67, 69]],  # Fmaj9 Dm9 Bbmaj7 C6
      bass=[41, 38, 34, 36], lead=[77, 79, 81, 84, 81, 79, 77, 72]),
  # London Bridge -> Arizona cartoon short: warm nostalgic UK garage, steady bed; lift on "stood proudly" (37.93 s), end stab after the last line
  'havasu': dict(dur=66.2, bpm=129.92, t0=-0.857, style='garage', drop=1, lift=17, end_bar=36,
      prog=[[63, 67, 70, 74, 77], [60, 63, 67, 70, 74], [56, 60, 63, 67], [58, 62, 65, 67]],  # Ebmaj9 Cm9 Abmaj7 Bb6
      bass=[39, 36, 32, 34], lead=[75, 77, 79, 82, 79, 77, 75, 72]),
  # Portofino: sunny Italo-disco, octave bass, arps; full from bar 1, steady level throughout
  'portofino': dict(dur=14.4, bpm=118, t0=.05, style='italo', drop=1, end_bar=7,
      prog=[[57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 65], [52, 55, 59, 62]],  # Am7 Fmaj7 G7 Em7
      bass=[45, 41, 43, 40], lead=[76, 72, 69, 72, 74, 71, 67, 71]),
  # Kirkjufell: airy UK garage, pads + 2-step, steady
  'kirkjufell': dict(dur=13.5, bpm=132, t0=.05, style='garage', drop=1, end_bar=7,
      prog=[[62, 66, 69, 73], [59, 62, 66, 69], [55, 59, 62, 66], [57, 61, 64, 69]],  # Dmaj7 Bm7 Gmaj7 A
      bass=[38, 35, 31, 33], lead=[78, 81, 76, 73, 74, 76, 78, 81]),

  # Antibes: bright Riviera 2-step garage; full lift on "Antibes." (20.77 s)
  'antibes': dict(dur=26.6, bpm=139.3, t0=.1, style='garage', drop=12, end_bar=14,
      prog=[[65, 69, 72, 76, 79], [64, 67, 71, 74], [62, 65, 69, 72, 76], [60, 64, 67, 71]],  # Fmaj9 Em7 Dm9 Cmaj7
      bass=[41, 40, 38, 36], lead=[76, 79, 81, 84, 81, 79, 76, 74]),
  # Menton: bouncy major house; lift on "Menton." (14.88 s)
  'menton': dict(dur=20.9, bpm=129.9, t0=.1, style='house', drop=8, end_bar=10,
      prog=[[60, 64, 67, 69, 74], [57, 60, 64, 67, 71], [62, 65, 69, 72, 76], [55, 59, 62, 65, 69]],  # C6/9 Am9 Dm9 G13
      bass=[36, 33, 38, 31], lead=[72, 74, 76, 79, 76, 74, 72, 69]),
  # Zermatt: dark minor half-time until "Today, Zermatt" (bar 7), lifts, full peak on "Zermatt." (bar 13)
  'zermatt': dict(dur=29.1, bpm=137.6, t0=.1, style='dark', drop=13, lift=7, end_bar=15,
      prog=[[60, 63, 67, 70], [56, 60, 63, 67], [53, 56, 60, 63], [55, 59, 62, 65]],  # Cm7 Abmaj7 Fm7 G7
      prog_lift=[[63, 67, 70, 74], [58, 62, 65, 69], [60, 63, 67, 70], [56, 60, 63, 67, 70]],  # Ebmaj7 Bbmaj7 Cm7 Abmaj9
      bass=[36, 32, 29, 31], bass_lift=[39, 34, 36, 32], lead=[75, 74, 72, 70, 72, 74, 75, 79]),
}

def render(name):
    P = TRACKS[name]; dur = P['dur']; N = int((dur + 2.5) * SR)
    L = np.zeros(N); R = np.zeros(N); verb_send = np.zeros(N); duck = np.ones(N)
    beat = 60 / P['bpm']; bar = beat * 4; s16 = beat / 4; t0 = P['t0']
    def put(buf, x, t, g=1.0):
        i = int(t * SR)
        if i >= N or i + len(x) <= 0: return
        if i < 0: x = x[-i:]; i = 0
        j = min(N, i + len(x)); buf[i:j] += x[:j - i] * g
    def stereo(x, t, g=1.0, pan=0.0, send=0.0):
        put(L, x, t, g * (1 - pan) ** .5 if pan > 0 else g); put(R, x, t, g * (1 + pan) ** .5 if pan < 0 else g)
        if send: put(verb_send, x, t, g * send)
    def sidechain(t, depth=.18, length=None):
        depth = min(depth, .18)
        length = length or beat * .85; n = int(length * SR); i = int(t * SR); j = min(N, i + n)
        if i < 0: return
        if i < N: duck[i:j] = np.minimum(duck[i:j], 1 - depth * np.exp(-np.arange(j - i) / SR / (length * .35)))
    swing = (0 if P['style'] == 'italo' else .17) * s16
    def st(b, k):  # time of 16th step k in bar b, swung
        return t0 + b * bar + k * s16 + (swing if k % 2 else 0)
    nbars = int(np.ceil((dur - t0) / bar)) + 1
    music = np.zeros(N)  # tonal bus (gets sidechained)
    def tput(x, t, g=1.0): put(music, x, t, g)
    drop, end_bar, style = P['drop'], P['end_bar'], P['style']
    lift = P.get('lift', 0)
    # pre-roll: impact at 0 so the very first frame hits
    stereo(impact(), 0.0, .35, send=.3)
    for b in range(nbars):
        bt = t0 + b * bar
        if bt > dur + .5: break
        dark = style == 'dark' and b < lift
        prog = P['prog_lift'] if (style == 'dark' and b >= lift) else P['prog']
        bassl = P['bass_lift'] if (style == 'dark' and b >= lift) else P['bass']
        ch = prog[b % 4]; bn = bassl[b % 4]
        full = b >= drop
        outro = b >= end_bar
        bright = 2200 if b < drop else 5200
        if dark: bright = 1300
        if outro:
            if b == end_bar:  # final stab + boom on the downbeat, then tails
                stereo(stab(ch, bar * 1.5, 3500), bt, .9, send=.7); stereo(kick(1.1), bt, .9); stereo(impact(), bt, .5, send=.4)
                tput(sub(bn, bar * 1.2), bt, .9)
            continue
        # drums
        if style == 'italo':
            for k in (0, 4, 8, 12): stereo(kick(.9), st(b, k), .85); sidechain(st(b, k))
            for k in (4, 12): stereo(clap(), st(b, k), .5, send=.35)
            for k in (2, 6, 10, 14): stereo(hat(True), st(b, k), .34, pan=.25)
            for k in range(0, 16, 2): tput(sub(bn + (12 if (k // 2) % 2 else 0), s16 * 1.7), st(b, k), .75)
            for k in range(16):
                arp = ch[k % len(ch)] + 12
                x = pluck(arp, s16 * 1.2); tput(x, st(b, k), .55); put(verb_send, x, st(b, k), .5)
            tput(pad(ch, bar, 2600), bt, .6); put(verb_send, pad(ch, bar, 2600), bt, .3)
            if b + 1 == end_bar: stereo(riser(bar), bt, .35)
            continue
        if style == 'house':
            for k in (0, 4, 8, 12): stereo(kick(), st(b, k), .9); sidechain(st(b, k))
            for k in (4, 12): stereo(clap(), st(b, k), .55, send=.25)
            for k in range(16): stereo(hat(k % 4 == 2), st(b, k), (.5 if k % 4 == 2 else .28) * (1.0 if full else .8), pan=.25)
            for k in (3, 7, 11, 15): stereo(shaker(), st(b, k), .9, pan=-.3)
        elif style == 'garage' or (style == 'dark' and not dark):
            for k in (0, 10) if b % 2 == 0 else (0, 7, 10): stereo(kick(), st(b, k), .9); sidechain(st(b, k))
            for k in (4, 12): stereo(clap(), st(b, k), .55, send=.3)
            for k in range(16): stereo(hat(k in (2, 6, 10, 14)), st(b, k), (.42 if k in (2, 6, 10, 14) else .26) * (1 if full else .75), pan=.25)
            for k in (5, 13): stereo(rim(), st(b, k), .6, pan=-.35, send=.2)
        else:  # dark half-time: kick on 1, clap on 3, sparse hats
            stereo(kick(.9), st(b, 0), .85); sidechain(st(b, 0), .6, beat * 1.6)
            if b % 2: stereo(kick(.8), st(b, 10), .6)
            stereo(clap(), st(b, 8), .45, send=.6)
            for k in (2, 6, 10, 14): stereo(hat(), st(b, k), .22, pan=.3)
        # bass
        if dark:
            tput(sub(bn, bar * .98), bt, .8)
        else:
            pat = [(0, 3), (3, 2), (6, 3), (10, 2), (12, 2), (14, 2)] if style != 'house' else [(2, 2), (6, 2), (10, 2), (14, 2)]
            for k, ln in pat:
                m = bn + (12 if (style != 'house' and k in (6, 14)) else 0)
                tput(sub(m, ln * s16 * 1.1), st(b, k), .85)
        # chords
        if dark:
            tput(pad(ch, bar, bright), bt, 1.0); put(verb_send, pad(ch, bar, bright), bt, .5)
        else:
            hits = (3, 6, 10, 13) if style != 'house' else (2, 6, 10, 14)
            for k in hits:
                x = stab(ch, s16 * 2.2, bright); tput(x, st(b, k), .9); put(verb_send, x, st(b, k), .45)
            if full: tput(pad(ch, bar, 3000), bt, .7)
        # hook pluck on the drop and lift sections
        if full or (style == 'dark' and b >= lift):
            ld = P['lead']
            for i, k in enumerate((0, 3, 6, 8, 10, 11, 14, 15) if b % 2 == 0 else (0, 2, 6, 8, 10, 13, 14, 15)):
                x = pluck(ld[(i + b) % len(ld)], s16 * 1.5); tput(x, st(b, k), .9); put(verb_send, x, st(b, k), .6)
        # riser into the drop (and into the lift)
        if b + 1 in (drop, lift) and b + 1 > 0:
            stereo(riser(bar), bt, .3)
        if b in (drop, lift) and b > 0:
            stereo(impact(), bt, .3, send=.3)
    # reverb (decorrelated stereo)
    def ir(seed):
        r = np.random.default_rng(seed); n = int(1.6 * SR); t = np.arange(n) / SR
        return lp(r.standard_normal(n) * np.exp(-t * 3.2), 6000)
    wl = fftconvolve(verb_send, ir(1))[:N] * .09; wr = fftconvolve(verb_send, ir(2))[:N] * .09
    music *= duck
    L += music + wl; R += music + wr
    out = np.stack([L, R], 1)[:int((dur) * SR)]
    fade = int(.6 * SR); out[-fade:] *= np.linspace(1, 0, fade)[:, None]
    out = np.tanh(out * 1.2) / 1.2
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-',
                    '-af', 'loudnorm=I=-16:TP=-1.5:LRA=7', '-ar', '48000', f'{name}-music.wav'],
                   input=out.astype(np.float32).tobytes(), check=True)
    print(name, 'bpm', P['bpm'], 'drop at', round(t0 + drop * bar, 2), 's, end stab at', round(t0 + end_bar * bar, 2), 's')

for n in sys.argv[1:]: render(n)
