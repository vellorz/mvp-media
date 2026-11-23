"""Round 6 (coordinated motion) preview sheets, no Blender: 2D composites that mirror lib.char() geometry plus lib.combo()'s lean pivot,
head pivot and stride cards, frame by frame from motion.frames() (the same plan lib.combo bakes). No Rick pixels.
python3 m6sheet.py r5demo.json OUTDIR [combo ...]   -> per combo: strip (every frame, labelled) + animated GIF + key-frame card."""
import sys, json, math, os
from PIL import Image, ImageDraw, ImageFont
import expressions as X, cast, motion as MO
D = X.expand(json.load(open(sys.argv[1]))); cast.C.update(D); OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
ONLY = sys.argv[3:]
GEO = {'tall': (0.966, 0.141, 0.86), 'short': (0.966, 0.156, 0.86), 'round': (0.966, 0.165, 0.86)}   # lib.GEO
BSY = 0.91; HS = 0.43 / 0.586; ARM_W, ARM_H, ARM_OFF = 0.744, 0.558, 0.242; PX = 700
_cache = {}
def tex(key, fn):
    if key not in _cache: _cache[key] = fn()
    return _cache[key]
def card(canvas, im, w, h, cx, cz, ox, oz, rot=0.0, piv=None):
    W, H = max(1, int(w * PX)), max(1, int(h * PX)); t = im.resize((W, H), Image.LANCZOS)
    x, y = int(ox + cx * PX - W / 2), int(oz - cz * PX - H / 2)
    if rot and piv is not None:   # rotate the card about a world pivot (px on canvas)
        lay = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); lay.alpha_composite(t, (x, y))
        lay = lay.rotate(rot, resample=Image.BICUBIC, center=piv); canvas.alpha_composite(lay); return
    canvas.alpha_composite(t, (x, y))
def arm_img(name, k):
    if k == 'hang':
        im = tex((name, 'arm'), lambda: cast.arm(name)); return im, 'rest'
    p = k; mix, over = 1.0, 0.0
    if p.endswith('_m'): p, mix = p[:-2], 0.5
    elif p.endswith('_o'): p, over = p[:-2], 9.0
    return tex((name, k), lambda: cast.pose_arm(name, p, mix=mix, over=over)), 'pose'
def figure(name, s, size=(900, 1250)):
    """lib.combo hierarchy in 2D: legs card on the feet pivot; torso card, arms and head on the hip pivot (lean); squash/hop on the feet"""
    c = cast.C[name]; top, shx, shz = GEO[c['body']]; q = BSY; top = -0.04 + (top + 0.04) * q; shz = -0.04 + (shz + 0.04) * q
    ox, oz = size[0] / 2, size[1] - 60
    zc = -0.04 + 0.55 * q; zh = -0.04 + 1.1 * q * (1 - cast.HIP_ROW / 1100)
    stride = {'body': 0, 'bodyw1': 1, 'bodyw2': 2}.get(s['legs'], 0)
    legs = Image.new('RGBA', size, (0, 0, 0, 0)); upper = Image.new('RGBA', size, (0, 0, 0, 0))
    behind = Image.new('RGBA', size, (0, 0, 0, 0))
    def fxs(anchor):
        return [e for e in s.get('fx', []) if e[1] == anchor]
    def fxim(k, side): return tex(('fx', k, side), lambda: cast.fx(k) if side > 0 else cast.fx(k).transpose(Image.FLIP_LEFT_RIGHT))
    if s['legs'].startswith('run'):   # round 7 run legs (cast.run_legs, both facings)
        lg = s['legs']; card(legs, tex((name, lg), lambda: cast.run_legs(name, int(lg[-1]), 1 if lg[3] == 'R' else -1)), 0.8, 1.1 * q, 0, zc, ox, oz)
    else:
        card(legs, tex((name, 'legs', stride), lambda: cast.split_body(name, stride)[1]), 0.8, 1.1 * q, 0, zc, ox, oz)
    for k, _a, dx, dz, sz, sd in fxs('behind'): card(behind, fxim(k, sd), sz, sz, dx, zh + dz, ox, oz)
    card(upper, tex((name, 'top'), lambda: cast.split_body(name, 0)[0]), 0.8, 1.1 * q, 0, zc, ox, oz)
    for sx in (-1, 1):
        im, kind = arm_img(name, s['arms'][sx])
        if sx < 0: im = im.transpose(Image.FLIP_LEFT_RIGHT)
        if kind == 'rest':
            big = Image.new('RGBA', (im.width, im.height * 2), (0, 0, 0, 0)); big.alpha_composite(im, (0, im.height - 40))
            big = big.rotate(8 * sx, resample=Image.BICUBIC, center=(im.width / 2, im.height))
            card(upper, big, ARM_W * q, ARM_H * 2 * q, sx * shx, shz, ox, oz)
        else:
            card(upper, im, cast.POSE_W * ARM_W / 1200 * q, cast.POSE_H * ARM_W / 1200 * q, sx * shx, shz + (ARM_H / 2 - ARM_OFF - 40 * ARM_W / 1200) * q, ox, oz)
    k = X.turn_name(s['face'], s['lv']) if s['lv'] is not None else s['face']
    if k not in c['faces']: k = s['face'] if s['face'] in c['faces'] else list(c['faces'])[0]
    pt, pb = X.pads(c); hd = tex((name, 'h', k), lambda: cast.head(name, k))
    hw = 0.75 * HS; hh = hw * (1024 + pt + pb) / 1024
    hz = top - s['hdy']
    for k, _a, dx, dz, sz, sd in fxs('torso'): card(upper, fxim(k, sd), sz, sz, dx, zh + dz, ox, oz)
    if fxs('head'):
        hl = Image.new('RGBA', size, (0, 0, 0, 0)); card(hl, hd, hw, hh, 0, hz + 0.2535 * HS + 0.75 * HS * (pt - pb) / 2048, ox, oz)
        for k, _a, dx, dz, sz, sd in fxs('head'): card(hl, fxim(k, sd), sz, sz, dx, hz + dz, ox, oz)
        if s['htilt']: hl = hl.rotate(-s['htilt'], resample=Image.BICUBIC, center=(ox, oz - hz * PX))
        upper.alpha_composite(hl)
    else:
        card(upper, hd, hw, hh, 0, hz + 0.2535 * HS + 0.75 * HS * (pt - pb) / 2048, ox, oz, rot=-s['htilt'], piv=(ox, oz - hz * PX))
    if s['lean']:
        upper = upper.rotate(-s['lean'], resample=Image.BICUBIC, center=(ox, oz - zh * PX))
        behind = behind.rotate(-s['lean'], resample=Image.BICUBIC, center=(ox, oz - zh * PX))
    cv = behind; cv.alpha_composite(legs); cv.alpha_composite(upper)
    for k, _a, dx, dz, sz, sd in fxs('feet'): card(cv, fxim(k, sd), sz, sz, dx, dz, ox, oz)
    if s['squash'] or s['hop']:
        sc_x, sc_y = 1 + s['squash'] * 0.6, 1 - s['squash']
        t = cv.resize((int(cv.width * sc_x), int(cv.height * sc_y)), Image.LANCZOS); cv2 = Image.new('RGBA', size, (0, 0, 0, 0))
        cv2.alpha_composite(t, (int(ox - ox * sc_x), int(oz - oz * sc_y - s['hop'] * PX))); cv = cv2
    return cv
def font(n, b=False):
    try: return ImageFont.truetype('DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf', n)
    except OSError: return ImageFont.load_default()
def tile(im, txt, sub, moving):
    out = Image.new('RGBA', (im.width, im.height + 86), (247, 244, 238, 255)); out.alpha_composite(im, (0, 86)); d = ImageDraw.Draw(out)
    d.text((10, 6), txt, fill=(40, 28, 40, 255), font=font(30, True)); d.text((10, 46), sub, fill=(110, 96, 110, 255), font=font(22))
    x = im.width - 10
    for part in ('fx', 'legs', 'torso', 'arms', 'head'):
        on = part in moving; w = 22 * len(part) // 2 + 18; x -= w
        d.rounded_rectangle([x, 8, x + w - 6, 38], 8, fill=(214, 110, 60, 255) if on else (226, 220, 210, 255)); d.text((x + 6, 11), part, fill=(255, 255, 255, 255) if on else (150, 140, 140, 255), font=font(18))
    return out
def row(ims, gap=6, bg=(247, 244, 238, 255)):
    W = sum(i.width for i in ims) + gap * (len(ims) - 1); H = max(i.height for i in ims); o = Image.new('RGBA', (W, H), bg); x = 0
    for i in ims: o.alpha_composite(i, (x, 0)); x += i.width + gap
    return o
def grid(ims, cols, gap=6, bg=(247, 244, 238, 255)):
    rows = [row(ims[i:i + cols], gap, bg) for i in range(0, len(ims), cols)]
    W = max(r.width for r in rows); H = sum(r.height for r in rows) + gap * (len(rows) - 1); o = Image.new('RGBA', (W, H), bg); y = 0
    for r in rows: o.alpha_composite(r, (0, y)); y += r.height + gap
    return o
SPEC = json.load(open(sys.argv[1].replace('.json', '_m6.json')))
LV = {-3: 'L3', -2: 'L2', -1: 'L1', 0: 'F', 1: 'R1', 2: 'R2', 3: 'R3', None: '-'}
made = []
for item in SPEC['combos']:
    cname, who, face, side, frm = item['combo'], item['char'], item['face'], item.get('side', 1), item.get('frm', 0)
    if ONLY and cname not in ONLY: continue
    seq = MO.frames(cname, side, face, frm, item.get('face2'), pre=2, post=6)
    mv = dict(MO.moving_parts(seq)); tiles = []
    for s in seq:
        arms = '/'.join(s['arms'][sx] for sx in (-1, 1))
        sub = f"{LV[s['lv']]} {arms}" + (f" lean{s['lean']:+.0f}" if s['lean'] else '') + (' ' + s['legs'] if s['legs'] != 'body' else '')
        tiles.append(tile(figure(who, s), f"f{s['f']:+d}", sub, mv.get(s['f'], set())))
    small = [t.resize((t.width * 2 // 5, t.height * 2 // 5), Image.LANCZOS) for t in tiles]
    g = grid(small, 8); g.convert('RGB').save(os.path.join(OUT, f'combo_{cname}_{who}.jpg'), quality=86)
    gi = [t.convert('RGB').resize((t.width // 3, t.height // 3)) for t in tiles]
    gi[0].save(os.path.join(OUT, f'combo_{cname}_{who}.gif'), save_all=True, append_images=gi[1:] + [gi[-1]] * 18, duration=33, loop=0)
    made.append(cname)
print('done', OUT, len(made), made)
