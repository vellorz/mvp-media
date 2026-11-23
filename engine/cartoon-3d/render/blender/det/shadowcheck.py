"""Rule 367 probe, part 2 (no Blender): python3 shadowcheck.py PAIRS.json FRAMEDIR [limit_pct=10]
For each overlapping blob pair from lib.shadow_pairs() (r11b), sample the rendered frame (f_###.png) in a 7x5 px window at M (centre
of the overlap) and at A / B (M mirrored through each blob's centre = that blob's darkness alone at the same falloff). Darkness d = 1 - L / Lfloor (Lfloor = 90th percentile luminance of the floor in the same rows, +-120 px).
FAIL when the overlap is lighter than the darker single blob by more than limit_pct % of that blob's darkness (a hole where the
shadows cross; correct stacking is at least as dark as either), or when the overlap darkness jumps by more than limit_pct points from one frame to the next (flicker)."""
import sys, json, numpy as np
from PIL import Image
P = json.load(open(sys.argv[1])); D = sys.argv[2]; LIM = float(sys.argv[3]) if len(sys.argv) > 3 else 10.0
SINGLE_MAX, PAIR_MAX, STD_MAX = 0.6, 0.75, 18.0
cache = {}; bad = 0; occl = 0; prev = {}; worst = 0.0; rows = []
def lum(f):
    if f not in cache:
        cache.clear()   # r11c (DC thread: OOM on 346 2K frames): keep only the current frame; pairs come sorted by frame
        try: cache[f] = np.asarray(Image.open(f'{D}/f_{f:03d}.png').convert('L')).astype(float)
        except FileNotFoundError: cache[f] = None
    return cache[f]
def samp(a, p):
    x, y = int(p[0]), int(p[1]); h, w = a.shape
    if not (3 <= x < w - 3 and 2 <= y < h - 2): return None
    w_ = a[y - 2:y + 3, x - 3:x + 4]; return w_.mean(), w_.std()
for e in P:
    a = lum(e['f'])
    if a is None: continue
    y = int(e['M'][1]); x0 = int(min(e['A'][0], e['B'][0])) - 120; x1 = int(max(e['A'][0], e['B'][0])) + 120
    band = a[max(0, y - 3):y + 4, max(0, x0):min(a.shape[1], x1)]
    if band.size == 0: continue
    fl = np.percentile(band, 90)
    hid = e.get('hidden', [False] * 3)
    if hid[1] or (hid[0] and hid[2]):   # r11c: the overlap (or both references) behind furniture: not a shadow sample
        rows.append((e['f'], e['a'], e['b'], '-', '-', '-', '-', '-', 'hidden')); occl += 1; continue
    vals = [samp(a, e[k]) for k in ('A', 'M', 'B')]
    if None in vals or fl <= 0: continue
    dA, dM, dB = [max(0.0, 1 - v[0] / fl) for v in vals]
    # r11b occlusion filter: a single blob is never darker than ~0.5 and two stacked never than ~0.75, and a window crossing ink has a
    # high spread; such a sample is a character's leg / body / ink, not floor, and is left out (reported as 'occl').
    okA = dA <= SINGLE_MAX and vals[0][1] <= STD_MAX and not hid[0]; okB = dB <= SINGLE_MAX and vals[2][1] <= STD_MAX and not hid[2]
    if dM > PAIR_MAX or vals[1][1] > STD_MAX or not (okA or okB):
        rows.append((e['f'], e['a'], e['b'], round(dA, 3), round(dM, 3), round(dB, 3), '-', '-', 'occl')); occl += 1; continue
    ref = max(d for d, ok in ((dA, okA), (dB, okB)) if ok); short = (ref - dM) / ref * 100 if ref > 0.02 else 0.0
    k = (e['a'], e['b']); jump = abs(dM - prev[k][1]) * 100 if k in prev and prev[k][0] == e['f'] - 1 else 0.0
    prev[k] = (e['f'], dM); worst = max(worst, short)
    st = 'FAIL' if (short > LIM or jump > LIM) else 'ok'
    if st == 'FAIL': bad += 1
    rows.append((e['f'], e['a'], e['b'], round(dA, 3), round(dM, 3), round(dB, 3), round(short, 1), round(jump, 1), st))
for r in rows: print('SHADOWCHECK', *r)
print('SHADOWCHECK_PAIRS', len(rows), 'OCCLUDED', occl, 'FAILS', bad, 'worst_between_shortfall_pct', round(worst, 1)); sys.exit(1 if bad else 0)
