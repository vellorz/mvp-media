"""Round 5 proposal sheets (no Blender): 2D composites that mirror lib.char() geometry, for the owner review page.
python3 r5sheet.py r5demo.json OUTDIR   -> turn strips, gesture cards, a few animated GIFs. No Rick pixels."""
import sys, json, math, os
from PIL import Image, ImageDraw, ImageFont
import expressions as X, cast
D = X.expand(json.load(open(sys.argv[1]))); cast.C.update(D); OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
GEO = {'tall': (0.966, 0.141, 0.86), 'short': (0.966, 0.156, 0.86), 'round': (0.966, 0.165, 0.86)}   # lib.GEO
BSY = 0.91; HS = 0.43 / 0.586; ARM_W, ARM_H, ARM_OFF = 0.744, 0.558, 0.242; PX = 900   # px per metre on the sheet
_cache = {}
def tex(key, fn):
    if key not in _cache: _cache[key] = fn()
    return _cache[key]
def card(canvas, im, w, h, cx, cz, ox, oz):
    """paste a texture as a plane w x h metres centred at (cx, cz) world, canvas origin (ox px, oz px = ground line)"""
    W, H = max(1, int(w * PX)), max(1, int(h * PX)); t = im.resize((W, H), Image.LANCZOS)
    canvas.alpha_composite(t, (int(ox + cx * PX - W / 2), int(oz - cz * PX - H / 2)))
def figure(name, face, arms=('arm', 'arm'), size=(1100, 1500)):
    c = cast.C[name]; top, shx, shz = GEO[c['body']]; q = BSY; top = -0.04 + (top + 0.04) * q; shz = -0.04 + (shz + 0.04) * q
    cv = Image.new('RGBA', size, (0, 0, 0, 0)); ox, oz = size[0] / 2, size[1] - 40
    card(cv, tex((name, 'body'), lambda: cast.body(name)), 0.8, 1.1 * q, 0, -0.04 + 0.55 * q, ox, oz)
    for sx, k in zip((-1, 1), arms):
        if k == 'arm':
            im = tex((name, 'arm'), lambda: cast.arm(name))
            if sx < 0: im = im.transpose(Image.FLIP_LEFT_RIGHT)
            # rest card hangs at -8 deg about the shoulder (lib.char)
            big = Image.new('RGBA', (im.width, im.height * 2), (0, 0, 0, 0)); big.alpha_composite(im, (0, im.height - 40))
            big = big.rotate(8 * sx, resample=Image.BICUBIC, center=(im.width / 2, im.height))
            card(cv, big, ARM_W * q, ARM_H * 2 * q * (im.height * 2) / (im.height * 2), sx * shx, shz + (ARM_H * q) - ARM_H * q, ox, oz)
        else:
            p = k.replace('arm_pose_', ''); mix, over = 1.0, 0.0
            if p.endswith('_m'): p, mix = p[:-2], 0.5
            elif p.endswith('_o'): p, over = p[:-2], 9.0
            im = tex((name, k), lambda: cast.pose_arm(name, p, mix=mix, over=over))
            if sx < 0: im = im.transpose(Image.FLIP_LEFT_RIGHT)
            card(cv, im, 1200 * ARM_W / 1200 * q, 1800 * ARM_W / 1200 * q, sx * shx, shz + (ARM_H / 2 - ARM_OFF - 40 * ARM_W / 1200) * q - 0 * q + (0), ox, oz)
    pt, pb = X.pads(c); hd = tex((name, face), lambda: cast.head(name, face))
    hw = 0.75 * HS; hh = hw * (1024 + pt + pb) / 1024
    card(cv, hd, hw, hh, 0, top + 0.2535 * HS + 0.75 * HS * (pt - pb) / 2048, ox, oz)
    return cv
def label(im, txt, sub=''):
    out = Image.new('RGBA', (im.width, im.height + 92), (247, 244, 238, 255)); out.alpha_composite(im, (0, 92)); d = ImageDraw.Draw(out)
    try: F = ImageFont.truetype('DejaVuSans-Bold.ttf', 34); G = ImageFont.truetype('DejaVuSans.ttf', 26)
    except OSError: F = G = ImageFont.load_default()
    d.text((14, 8), txt, fill=(40, 28, 40, 255), font=F); d.text((14, 52), sub, fill=(110, 96, 110, 255), font=G)
    return out
def crop_head(im): return im.crop((290, 230, 810, 790))
def row(ims, gap=8, bg=(247, 244, 238, 255)):
    W = sum(i.width for i in ims) + gap * (len(ims) - 1); H = max(i.height for i in ims); o = Image.new('RGBA', (W, H), bg); x = 0
    for i in ims: o.alpha_composite(i, (x, 0)); x += i.width + gap
    return o
def save(im, n, scale=0.5): im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS); im.convert('RGB').save(os.path.join(OUT, n), quality=88); return n
SPEC = json.load(open(sys.argv[1].replace('.json', '_sheet.json')))
for name, base in SPEC['turn_strips']:
    # all seven levels, then the planned transitions
    lv = [label(crop_head(figure(name, X.turn_name(base, l))), {-3: 'L3', -2: 'L2', -1: 'L1', 0: 'F', 1: 'R1', 2: 'R2', 3: 'R3'}[l], {0: 'front', 1: 'slight', 2: '3/4', 3: 'strong 3/4'}[abs(l)]) for l in range(-3, 4)]
    save(row(lv), f'levels_{name}_{base}.jpg')
import importlib.util
def plan(frm, to, holds=None):   # same as lib.turn_plan (lib needs bpy)
    if frm == to: return []
    if abs(to - frm) == 1: return [(0, to)]
    if frm * to < 0: return [(0, 0), (2 if abs(frm) + abs(to) >= 4 else 1, to)]
    step = 1 if to > frm else -1; lv = list(range(frm + step, to + step, step)); out = []; o = 0
    for i, l in enumerate(lv):
        out.append((o, l)); o += (holds[i] if holds and i < len(holds) else (2 if i == len(lv) - 2 else 1))
    return out
for name, base, frm, to in SPEC['transitions']:
    fr = []; p = plan(frm, to); end = p[-1][0] + 4; cur = frm; seq = []
    for f in range(-3, end):
        for o, l in p:
            if o == f: cur = l
        seq.append((f, cur))
    tiles = [label(crop_head(figure(name, X.turn_name(base, l))), f'frame {f + 4}', {-3: 'L3', -2: 'L2', -1: 'L1', 0: 'F', 1: 'R1', 2: 'R2', 3: 'R3'}[l]) for f, l in seq]
    save(row(tiles, 4), f'turn_{name}_{base}_{frm}_{to}.jpg', 0.42)
    g = [t.convert('RGB').resize((t.width // 2, t.height // 2)) for t in tiles]
    g[0].save(os.path.join(OUT, f'turn_{name}_{base}_{frm}_{to}.gif'), save_all=True, append_images=g[1:] + [g[-1]] * 20, duration=33, loop=0)
for name, face, sets in SPEC['gestures']:
    for title, sub, arms in sets:
        save(label(figure(name, face, tuple(arms)), title, sub), f'pose_{name}_{title}.jpg', 0.5)
print('done', OUT)
