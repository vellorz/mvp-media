# Rick-style facial expression library for the 2D cut-out cast (cast.py / lib.py).
# Built Nov 22 2026 from 868 labelled face changes in 7 of Rick's videos (#03 #04 #10 #12 #14 #22 #24, new-analysis-2 merged.json)
# plus face crops of 2-3 reference frames per expression (research/rick-style-spec/expression-library/).
# STYLE ONLY: every drawing below is our own vector code; no Rick pixels are used anywhere.
#
# How to use (opt-in, so renders already in flight do not change):
#   cast.json, per character:  "library": "all"            -> every LIBRARY face is added to that character
#                              "library": ["smug","panic"] -> only those
#   Faces the character already defines keep their own recipe (expand() never overwrites).
#   Scene code then keys faces by name as before: faces(ch,[(f,'smug'),(f+20,'panic'),...]).
#   lib.face() falls back through ALT when a character lacks a name.
# Face recipe = [eyes, brows, mouth, extras]; extras is a '+'-joined string (e.g. 'sweat+blushR').

import math
try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:   # dc: Blender's python has no PIL; lib.py only needs LIBRARY/expand/alternates
    Image = ImageDraw = ImageFilter = None

CX = 512
CLEAR = (0, 0, 0, 0)
WHITE = (255, 255, 255, 255)
RED_M = (110, 28, 34, 255)          # mouth interior (same as cast.py)
TONGUE = (220, 90, 100, 255)
TEAR = (120, 190, 255, 255)
BLUSH = (246, 150, 160, 150)

# ------------------------------------------------------------------ library
# name: (eyes, brows, mouth, extras)   counts = labelled occurrences in the 7 analysed Rick videos
LIBRARY = {
    # calm / base
    'neutral':      ('dot', 'none', 'line', ''),            # 8, 5 videos
    'deadpan':      ('lid', 'none', 'line', ''),            # 61, 7 videos (Rick's most common face)
    'sleepy':       ('lidlow', 'none', 'line', ''),         # half-closed / tired
    'smug':         ('lid', 'none', 'smirk', ''),           # 26, 6 videos
    'smug_grin':    ('lid', 'none', 'toothy', ''),          # 9, 3 videos
    'skeptical':    ('lid', 'Lraise', 'line', ''),           # 28, 7 videos (one brow up)
    'side_eye':     ('sideR', 'none', 'smirkR', ''),        # 23, 7 videos
    'look_up':      ('ringup', 'Lup', 'o', ''),              # 4, 4 videos
    'look_down':    ('lookdown', 'none', 'line', ''),       # 6, 5 videos
    'determined':   ('lidstern', 'none', 'smirk', ''),      # 2, 2 videos
    # happy
    'smile':        ('dot', 'none', 'smile', ''),           # dot eyes + small smile (12)
    'happy':        ('happy', 'none', 'smile', ''),         # ^^ closed-eye smile, 18, 5 videos
    'content':      ('closed', 'none', 'smile', ''),        # 6, 4 videos
    'laugh':        ('happy', 'Lup', 'laugh', ''),           # 14, 4 videos
    'cry_laugh':    ('happy', 'Lworry', 'toothy', 'tears+blushR'),  # 6 (#14)
    'grin':         ('dot', 'none', 'toothy', ''),          # 20, 6 videos
    'open_smile':   ('dot', 'Lup', 'dsmile', ''),            # open smile, no teeth
    'manic_grin':   ('ring', 'Lup', 'toothy', ''),           # 7, 3 videos
    'wink':         ('wink', 'none', 'smirk', ''),          # 4, 3 videos
    'wink_grin':    ('wink', 'none', 'toothy', ''),         # 5, 3 videos
    'proud':        ('happy', 'none', 'smile', 'blushR'),   # blush cases, 8 in 4 videos
    'cool_shades':  ('dot', 'none', 'toothy', 'shades'),    # 3 (#24)
    'tongue':       ('lid', 'none', 'tongue', ''),          # 1 (#22)
    # surprise / fear
    'surprise':     ('ring', 'Lup', 'o', ''),                # 15, 4 videos
    'shock':        ('pin', 'Lup', 'O', ''),                 # 13, 4 videos
    'startle':      ('tinyw', 'none', 'o', ''),             # wide dot eyes, no brows, 4, 3 videos
    'worried':      ('ring', 'Lworry', 'wavy', ''),          # 13, 5 videos
    'nervous':      ('dot', 'Lworry', 'grit', 'sweat'),      # 10, 5 videos
    'panic':        ('ring', 'Lup', 'grit', 'sweat'),        # 8, 5 videos
    'stunned':      ('pin', 'none', 'wavy', ''),            # 6, 2 videos
    'dazed':        ('spiral', 'none', 'wavy', ''),         # 8, 6 videos
    'hypnotized':   ('hypno', 'none', 'line', ''),          # 3 (#24)
    'hypnotized_lids': ('hypnolid', 'none', 'line', ''),   # #24 f1622
    # sad
    'sad':          ('dot', 'Lworry', 'frown', ''),          # 8, 3 videos
    'sad_tears':    ('lidsad', 'Lworry', 'frown', 'tear1'),
    'sigh':         ('closed', 'Lworry', 'sigh', ''),        # 2, 2 videos
    # cross
    'frown':        ('lid', 'Lflat', 'frown', ''),           # 9, 5 videos
    'annoyed':      ('lid', 'Langry', 'frown', ''),          # 8, 4 videos
    'closed_annoyed': ('closed', 'Langry', 'line', ''),      # -_- 2, 2 videos
    'stern':        ('lidstern', 'Langry', 'line', ''),      # 17, 4 videos
    'angry':        ('dot', 'Langry', 'frown', ''),          # 8, 4 videos
    'angry_squint': ('squint', 'Langryhv', 'grit', ''),      # 7, 3 videos
    'shout':        ('squeeze', 'Langryhv', 'shout', ''),    # 12, 4 videos
    'rage':         ('lidstern', 'Langryhv', 'grit', 'vein+gloom'),   # 6, 3 videos (#03 purple fill, #22 red vein mark)
    'rage_red':     ('rage', 'Langryhv', 'frown', 'redglow'),   # 1 (#24 sheriff)
    'squeeze':      ('squeeze', 'none', 'grit', ''),        # 7, 4 videos
    'wince':        ('onesquint', 'Lworry', 'grit', ''),     # 10, 5 videos
    'squint':       ('squint', 'Lflat', 'line', ''),         # 15, 5 videos (concentrate)
    # sleep / mouth-only
    'asleep':       ('sleep', 'none', 'o', 'zzz'),          # 9, 4 videos
    'whistle':      ('closed', 'none', 'whistleo', ''),     # 3 (#03)
    'blink':        ('closed', 'Lflat', 'line', ''),         # 74 (2 f, auto in lib.finish)
}
# families: what a missing face falls back to (used by lib.face)
FAMILY = {
    'calm': ['deadpan', 'neutral', 'sleepy', 'look_down', 'look_up'],
    'smug': ['smug', 'smug_grin', 'skeptical', 'side_eye', 'determined', 'wink', 'tongue', 'cool_shades'],
    'happy': ['happy', 'smile', 'content', 'laugh', 'cry_laugh', 'grin', 'open_smile', 'manic_grin', 'wink_grin', 'proud', 'cheer'],
    'surprise': ['surprise', 'shock', 'startle', 'wow', 'stunned', 'look_up'],
    'fear': ['worried', 'nervous', 'panic', 'wince', 'dazed', 'hypnotized', 'hypnotized_lids'],
    'sad': ['sad', 'sad_tears', 'sigh', 'frown'],
    'cross': ['annoyed', 'stern', 'angry', 'angry_squint', 'shout', 'rage', 'rage_red', 'squeeze', 'closed_annoyed', 'frown', 'grit', 'squint'],
    'sleep': ['asleep', 'sleepy', 'content'],
}
def alternates(k):
    out = []
    for fam in FAMILY.values():
        if k in fam: out += [a for a in fam if a != k and a not in out]
    return out

def expand(C):
    """add LIBRARY faces to every character whose cast.json entry has "library" (never overwrites a face it already has)"""
    for n, c in C.items():
        want = c.get('library')
        if not want: continue
        names = list(LIBRARY) if want == 'all' else list(want)
        f = c.setdefault('faces', {})
        for k in names:
            if k in LIBRARY and k not in f:
                e, b, m, x = LIBRARY[k]; f[k] = [e, b, m] + ([x] if x else [])
    return C

# ------------------------------------------------------------------ eyes
EYES = {'lid', 'lidlow', 'lidstern', 'lidsad', 'ring', 'ringup', 'pin', 'tinyw', 'sideR', 'sideL', 'lookdown',
        'squint', 'onesquint', 'sleep', 'spiral', 'hypno', 'hypnolid', 'rage'}
def _dot(d, x, cy, K, dx=0, dy=0, w=33, h=50): d.ellipse([x + dx - w, cy + dy - h, x + dx + w, cy + dy + h], fill=K)
def _cut_above(d, pts): d.polygon(pts, fill=CLEAR)
def eyes(d, kind, K, cy=520, gap=108):
    for sx in (-1, 1):
        x = CX + sx * gap; ins = -sx   # ins: direction toward the face centre
        if kind in ('lid', 'lidlow'):
            # Rick's half-lid: the dot cut flat by a lid line a little wider than the dot
            ly = cy - 8 if kind == 'lid' else cy + 14
            _dot(d, x, cy, K); _cut_above(d, [(x - 60, cy - 80), (x + 60, cy - 80), (x + 60, ly), (x - 60, ly)])
            d.line([x - 48, ly, x + 48, ly], fill=K, width=16)
        elif kind in ('lidstern', 'lidsad'):
            hi, lo = (cy - 34, cy + 4)
            yin, yout = (lo, hi) if kind == 'lidstern' else (hi, lo)   # stern: inner end low (cross); sad: inner end high
            xi, xo = x + ins * 48, x - ins * 48
            _dot(d, x, cy, K)
            _cut_above(d, [(xi, cy - 90), (xo, cy - 90), (xo, yout), (xi, yin)])
            d.line([xi, yin, xo, yout], fill=K, width=16)
        elif kind in ('ring', 'ringup'):
            d.ellipse([x - 54, cy - 58, x + 54, cy + 58], fill=WHITE, outline=K, width=12)
            py = cy - 24 if kind == 'ringup' else cy
            d.ellipse([x - 14, py - 15, x + 14, py + 15], fill=K)
        elif kind == 'pin':     # shock: big whites, pin pupils
            d.ellipse([x - 62, cy - 66, x + 62, cy + 66], fill=WHITE, outline=K, width=12)
            d.ellipse([x - 8, cy - 8, x + 8, cy + 8], fill=K)
        elif kind == 'tinyw':   # startle: small round dots, a little apart
            d.ellipse([x + sx * 8 - 24, cy - 24, x + sx * 8 + 24, cy + 24], fill=K)
        elif kind in ('sideR', 'sideL'):
            dx = 26 if kind == 'sideR' else -26
            _dot(d, x, cy, K, dx=dx); _cut_above(d, [(x - 80, cy - 80), (x + 80, cy - 80), (x + 80, cy - 10), (x - 80, cy - 10)])
            d.line([x - 48, cy - 10, x + 48, cy - 10], fill=K, width=16)
        elif kind == 'lookdown':
            _dot(d, x, cy, K, dy=22, h=40); _cut_above(d, [(x - 60, cy - 80), (x + 60, cy - 80), (x + 60, cy - 2), (x - 60, cy - 2)])
            d.line([x - 48, cy - 2, x + 48, cy - 2], fill=K, width=16)
        elif kind == 'squint':  # short thick dash, ends turned down
            d.line([(x - 44, cy + 10), (x - 30, cy - 2), (x + 30, cy - 2), (x + 44, cy + 10)], fill=K, width=18, joint='curve')
        elif kind == 'onesquint':
            if sx < 0:
                d.line([x - 40 * sx, cy - 28, x + 34 * sx, cy], fill=K, width=18); d.line([x + 34 * sx, cy, x - 40 * sx, cy + 28], fill=K, width=18)
            else: _dot(d, x, cy, K, w=30, h=44)
        elif kind == 'sleep':   # '= =' double lids
            d.line([x - 46, cy - 6, x + 46, cy - 6], fill=K, width=14); d.line([x - 40, cy + 22, x + 40, cy + 22], fill=K, width=12)
        elif kind == 'spiral':
            pts = []
            for i in range(0, 64):
                a = i * 0.36 * sx; r = 4 + i * 0.78
                pts.append((x + r * math.cos(a), cy + r * math.sin(a)))
            d.line(pts, fill=K, width=9, joint='curve')
        elif kind in ('hypno', 'hypnolid'):   # #24: white ring eyes with a red curved-arrow sign reflection; 'hypnolid' = heavy lids
            RD = (226, 70, 40, 255)
            d.ellipse([x - 62, cy - 62, x + 62, cy + 62], fill=WHITE, outline=K, width=13)
            d.arc([x - 34, cy - 34, x + 34, cy + 34], 200, 520, fill=RD, width=10)
            d.polygon([(x - 40, cy - 2), (x - 22, cy - 26), (x - 12, cy + 2)], fill=RD)
            if kind == 'hypnolid':
                _cut_above(d, [(x - 70, cy - 80), (x + 70, cy - 80), (x + 70, cy - 4), (x - 70, cy - 4)])
                d.arc([x - 62, cy - 62, x + 62, cy + 62], 180, 360, fill=CLEAR, width=14)
                d.line([x - 62, cy - 4, x + 62, cy - 4], fill=K, width=14)
        elif kind == 'rage':    # red glowing eyes
            d.ellipse([x - 44, cy - 34, x + 44, cy + 34], fill=(255, 120, 60, 120))
            d.ellipse([x - 34, cy - 26, x + 34, cy + 26], fill=(225, 30, 30, 255))
            d.ellipse([x - 12, cy - 10, x + 12, cy + 10], fill=(255, 230, 120, 255))

# ------------------------------------------------------------------ brows
BROWS = {'angryhv', 'raiseL', 'short', 'Lflat', 'Langry', 'Lworry', 'Lup', 'Lraise', 'Langryhv'}
# Library brows ('L' kinds): Rick draws short thick brow strokes on the skin just above the eyes, never on the hair or hat band.
# The rig's own brows sit at y 405 (300 after the feature lift) and get lost on the hairline, so library faces use these, 40 px lower.
def _lbrow(d, kind, K, cy, gap):
    for sx in (-1, 1):
        x = CX + sx * gap; ins = -sx
        if kind == 'Lflat': d.line([x - 40, cy, x + 40, cy], fill=K, width=24)
        elif kind == 'Lup': d.line([x - 40, cy - 22, x + 40, cy - 22], fill=K, width=24)
        elif kind == 'Langry': d.line([x - ins * 42, cy - 16, x + ins * 42, cy + 14], fill=K, width=26)
        elif kind == 'Langryhv': d.line([x - ins * 46, cy - 22, x + ins * 40, cy + 20], fill=K, width=32)
        elif kind == 'Lworry': d.line([x - ins * 42, cy + 12, x + ins * 42, cy - 18], fill=K, width=24)
        elif kind == 'Lraise':
            yy = cy - (30 if sx > 0 else 0); d.line([x - 40, yy, x + 40, yy - (8 if sx > 0 else 0)], fill=K, width=24)
def brows(d, kind, K, cy=405, gap=108):
    if kind.startswith('L'): return _lbrow(d, kind, K, cy + 40, gap)
    for sx in (-1, 1):
        x = CX + sx * gap
        if kind == 'angryhv': d.line([x - 58 * sx, cy - 34, x + 46 * sx, cy + 30], fill=K, width=38)
        elif kind == 'raiseL':
            yy = cy - (46 if sx < 0 else 0); d.line([x - 52, yy - (8 if sx < 0 else 0), x + 52, yy], fill=K, width=30)
        elif kind == 'short': d.line([x - 30, cy - 40, x + 30, cy - 40], fill=K, width=26)

# ------------------------------------------------------------------ mouths
MOUTHS = {'toothy', 'shout', 'tongue', 'sigh', 'dsmile', 'smirkR', 'snarl', 'whistleo'}
def mouth(d, kind, K, cy=715, cx=CX):
    if kind == 'toothy':    # Rick's grin: flat top, round bottom, tooth grid
        d.chord([cx - 104, cy - 66, cx + 104, cy + 78], 0, 180, fill=WHITE, outline=K, width=14)
        d.line([cx - 96, cy + 22, cx + 96, cy + 22], fill=K, width=7)
        for i in (-2, -1, 0, 1, 2): d.line([cx + i * 34, cy + 6, cx + i * 34, cy + 66 - abs(i) * 10], fill=K, width=6)
    elif kind == 'shout':
        d.ellipse([cx - 92, cy - 52, cx + 92, cy + 104], fill=RED_M, outline=K, width=14)
        d.chord([cx - 70, cy - 44, cx + 70, cy + 4], 180, 360, fill=WHITE)
        d.chord([cx - 50, cy + 50, cx + 50, cy + 104], 180, 360, fill=TONGUE)
    elif kind == 'tongue':
        d.arc([cx - 82, cy - 64, cx + 82, cy + 44], 25, 155, fill=K, width=17)
        d.chord([cx - 10, cy + 10, cx + 58, cy + 86], 0, 180, fill=TONGUE, outline=K, width=10)
    elif kind == 'sigh': d.ellipse([cx - 44, cy - 18, cx + 44, cy + 26], fill=RED_M, outline=K, width=12)
    elif kind == 'dsmile': d.chord([cx - 84, cy - 44, cx + 84, cy + 74], 0, 180, fill=RED_M, outline=K, width=14)
    elif kind == 'smirkR': d.arc([cx - 62, cy - 74, cx + 82, cy + 26], 70, 160, fill=K, width=17)
    elif kind == 'snarl':
        d.polygon([(cx - 96, cy - 20), (cx + 96, cy - 44), (cx + 96, cy + 30), (cx - 96, cy + 20)], fill=WHITE, outline=K)
        d.line([(cx - 96, cy - 20), (cx + 96, cy - 44), (cx + 96, cy + 30), (cx - 96, cy + 20), (cx - 96, cy - 20)], fill=K, width=12)
        for i in (-1, 0, 1): d.line([cx + i * 46, cy - 30 - i * 6, cx + i * 46, cy + 24], fill=K, width=7)
    elif kind == 'whistleo': d.ellipse([cx + 10, cy - 22, cx + 54, cy + 22], fill=RED_M, outline=K, width=12)

# ------------------------------------------------------------------ extras (feature layer, drawn after the face)
def extras(d, kind, K):
    if not kind: return
    ks = kind.split('+')
    if 'sweat2' in ks:   # second drop, upper left
        d.polygon([(250, 300), (226, 356), (274, 356)], fill=TEAR); d.ellipse([224, 336, 276, 388], fill=TEAR, outline=K, width=7)
    if 'tears' in ks:    # cry-laugh: chains of drops from the outer eye corners
        for sx in (-1, 1):
            x0 = CX + sx * 168
            for i, (dy, r) in enumerate(((560, 16), (604, 20), (656, 24))):
                d.ellipse([x0 + sx * i * 10 - r, dy - r, x0 + sx * i * 10 + r, dy + r], fill=TEAR, outline=K, width=6)
    if 'tear1' in ks: d.ellipse([CX - 128 - 18, 580, CX - 128 + 18, 636], fill=TEAR, outline=K, width=6)
    if 'blushR' in ks:
        for sx in (-1, 1):
            x = CX + sx * 190
            d.ellipse([x - 62, 610, x + 62, 660], fill=BLUSH)
            for j in (-1, 0, 1): d.line([x + j * 24 - 8, 646, x + j * 24 + 8, 624], fill=(220, 100, 120, 255), width=6)
    if 'vein' in ks:     # red anger mark, upper right of the head
        vx, vy = 760, 300
        for a in (45, 135, 225, 315):
            ox, oy = vx + 26 * math.cos(math.radians(a)), vy + 26 * math.sin(math.radians(a))
            d.arc([ox - 26, oy - 26, ox + 26, oy + 26], a + 90, a + 270, fill=(214, 30, 40, 255), width=12)
    if 'zzz' in ks:
        for i, (zx, zy, s) in enumerate(((700, 360, 40), (770, 290, 52), (850, 210, 64))):
            d.line([(zx, zy), (zx + s, zy), (zx, zy + s), (zx + s, zy + s)], fill=K, width=12)
    if 'shades' in ks:
        for sx in (-1, 1):   # #24: two round black lenses on a thin bridge
            x = CX + sx * 108
            d.ellipse([x - 66, 456, x + 66, 588], fill=(22, 20, 26, 255), outline=K, width=10)
            d.arc([x - 44, 478, x + 30, 552], 200, 250, fill=(150, 150, 170, 255), width=8)
        d.line([CX - 44, 500, CX + 44, 500], fill=K, width=12)

def pre(im, kind):
    """head-layer effects drawn before hair/hat/features (head disc 112..912 x 140..940)"""
    ks = (kind or '').split('+')
    if 'redglow' in ks:
        ov = Image.new('RGBA', im.size, CLEAR); ImageDraw.Draw(ov).ellipse([200, 280, 824, 760], fill=(255, 60, 40, 95))
        ov = ov.filter(ImageFilter.GaussianBlur(60)); m = Image.new('L', im.size, 0); ImageDraw.Draw(m).ellipse([160, 167, 885, 892], fill=255)  # inside the ink only
        from PIL import ImageChops
        ov.putalpha(ImageChops.multiply(ov.getchannel('A'), m)); im.alpha_composite(ov)
    if 'gloom' not in ks: return
    ov = Image.new('RGBA', im.size, CLEAR); od = ImageDraw.Draw(ov)
    m = Image.new('L', im.size, 0); md = ImageDraw.Draw(m)
    md.rectangle([0, 470, 1024, 1024], fill=255)   # #03 f515-521: purple fill rising from the chin
    m = m.filter(ImageFilter.GaussianBlur(26))
    from PIL import ImageChops
    sk = Image.new('L', im.size, 0); ImageDraw.Draw(sk).ellipse([160, 167, 885, 892], fill=255); m = ImageChops.multiply(m, sk)   # inside the ink only
    od.rectangle([0, 0, 1024, 1024], fill=(120, 50, 150, 170))
    from PIL import ImageChops
    ov.putalpha(ImageChops.multiply(ov.getchannel('A'), m)); im.alpha_composite(ov)

# =================================================================== round 2 (owner Nov 22 5:11 PM CT)
# Off-centre mouths and turned faces, Rick-style facial hair, hairstyles and perspective hats.
# Studied on 394 head crops sampled every 2.5 s from all 24 Rick videos (research/rick-style-spec/expression-library/round2/).
# All coordinates below are FINAL head-texture coordinates (head disc 112..912 x 140..940, centre 512,540).
import random as _random

def turn_dx(c, ex=''):
    """horizontal shift of eyes/nose/mouth: Rick turns a head by sliding the whole face toward the side it faces (8-12 % of head width)"""
    t = c.get('turn', 0)
    ks = (ex or '').split('+')
    if 'turnL' in ks: t = -1
    if 'turnR' in ks: t = 1
    if 'front' in ks: t = 0
    return int(round(t * 62))

MOUTH_TILT = 9      # degrees: one corner higher than the other
MOUTH_SHIFT = 46    # px past the turn shift: the mouth sits off the face's centre line
def mouth_layer(draw_fn, kind, side, cy=715):
    """draw a mouth on its own layer and give it Rick's lopsided set: shifted toward `side`, tilted so that side's corner rides up"""
    lay = Image.new('RGBA', (1024, 1024), CLEAR); d = ImageDraw.Draw(lay)
    draw_fn(d, kind, cy=cy, cx=CX)
    if not side: return lay
    if kind in ('O', 'o', 'sigh', 'shout', 'whistleo'): ang = 0      # round mouths only shift
    else: ang = MOUTH_TILT * side
    lay = lay.rotate(ang, resample=Image.BICUBIC, center=(CX, cy))
    out = Image.new('RGBA', (1024, 1024), CLEAR); out.alpha_composite(lay, (int(MOUTH_SHIFT * side), 0))
    return out

# ------------------------------------------------------------------ facial hair (fhair)
FHAIR = ['pencil', 'chevron', 'curled', 'walrus', 'toothbrush', 'droop', 'goatee', 'king', 'fullbeard', 'whitebeard', 'stubbledots', 'sideburns']
def fhair(im, name, col, K, dx=0):
    d = ImageDraw.Draw(im); cx = CX + dx; col = tuple(col)[:3] + (255,); hi = tuple(min(255, int(v * 1.35) + 20) for v in col[:3]) + (255,)
    if name == 'pencil':      # thin line, tips lifted (#05, #23 bowtie men)
        for sx in (-1, 1): d.line([(cx + sx * 8, 568), (cx + sx * 60, 566), (cx + sx * 96, 552)], fill=col, width=15, joint='curve')
    elif name == 'chevron':   # thick push-broom, wider at the bottom, combed notches (#07 cowboy, #11, #24 sheriff)
        pts = [(cx - 96, 540), (cx + 96, 540), (cx + 128, 604), (cx - 128, 604)]
        d.polygon(pts, fill=col); d.line(pts + [pts[0]], fill=K, width=10, joint='curve')
        for x in (-70, -24, 24, 70): d.line([cx + x, 584, cx + x + (6 if x > 0 else -6), 604], fill=K, width=7)
    elif name == 'curled':    # handlebar with curls at the tips (#23 top-hat tycoon)
        for sx in (-1, 1):
            d.chord([cx + sx * 70 - 76, 528, cx + sx * 70 + 76, 612], 180, 360, fill=col)
            d.ellipse([cx + sx * 70 - 76, 540, cx + sx * 70 + 76, 600], fill=col, outline=K, width=9)
            ex_ = cx + sx * 150; d.arc([ex_ - 34, 520, ex_ + 34, 588], 90 if sx > 0 else 0, 360 if sx > 0 else 270, fill=K, width=14)
        d.ellipse([cx - 44, 534, cx + 44, 590], fill=col)
    elif name == 'walrus':    # two rounded lobes drooping over the lip, fringe lines (#04 captain)
        for sx in (-1, 1):
            d.ellipse([cx + sx * 66 - 88, 528, cx + sx * 66 + 88, 628], fill=col, outline=K, width=11)
        d.ellipse([cx - 60, 534, cx + 60, 616], fill=col)
        for x in (-110, -66, -22, 22, 66, 110): d.line([cx + x, 590, cx + x * 1.06, 622], fill=dk_(col), width=8)
    elif name == 'toothbrush':
        d.rounded_rectangle([cx - 46, 542, cx + 46, 590], 12, fill=col, outline=K, width=9)
    elif name == 'droop':     # thin long ends hanging past the mouth (#14 emperor)
        for sx in (-1, 1): d.line([(cx + sx * 10, 566), (cx + sx * 70, 572), (cx + sx * 104, 612), (cx + sx * 110, 690)], fill=col, width=14, joint='curve')
    elif name in ('goatee', 'king'):   # small chin tuft (#17 king, #25 samurai)
        d.polygon([(cx - 40, 760), (cx + 40, 760), (cx + 8, 850), (cx - 6, 852)], fill=col); d.line([(cx - 40, 760), (cx - 6, 852), (cx + 8, 850), (cx + 40, 760)], fill=K, width=8)
        if name == 'king':
            for sx in (-1, 1): d.line([(cx + sx * 10, 566), (cx + sx * 70, 570), (cx + sx * 92, 556)], fill=col, width=12, joint='curve')
    elif name == 'fullbeard':  # hugs the jaw: high at the sideburns, dips under the mouth, mouth stays on skin (#13, #22)
        m = Image.new('L', (1024, 1024), 0); md = ImageDraw.Draw(m)
        md.ellipse([118, 146, 906, 990], fill=255)
        top = [(0, 0), (1024, 0), (1024, 640)] + [(x, 640 + 110 * math.sin(math.pi * (x - 112) / 800) ** 2) for x in range(912, 111, -40)] + [(0, 640)]
        md.polygon(top, fill=0)
        lay = Image.new('RGBA', (1024, 1024), col); dd = ImageDraw.Draw(lay)
        for x in range(170, 860, 52): dd.arc([x - 26, 820 + (x % 3) * 24, x + 26, 870 + (x % 3) * 24], 20, 160, fill=dk_(col), width=7)
        im.paste(lay, (0, 0), m); d = ImageDraw.Draw(im)
        # Rick #22: the beard hangs past the chin outline onto the chest, textured with short strokes
        bib = [(cx - 300, 760), (cx - 230, 930), (cx - 120, 1010), (cx, 1022), (cx + 120, 1010), (cx + 230, 930), (cx + 300, 760)]
        d.polygon(bib, fill=col); d.line(bib, fill=K, width=14, joint='curve')
        for i, x in enumerate(range(-220, 240, 44)): d.line([cx + x, 860 + (i % 2) * 30, cx + x * 0.9, 930 + (i % 2) * 30], fill=dk_(col), width=8)
        d.line([(x, 640 + 110 * math.sin(math.pi * (x - 112) / 800) ** 2) for x in range(150, 880, 20)], fill=K, width=10, joint='curve')
        d.arc([118, 146, 906, 990], 18, 162, fill=K, width=16)
        for sx in (-1, 1): d.line([(cx + sx * 8, 566), (cx + sx * 70, 570), (cx + sx * 110, 600)], fill=col, width=26, joint='curve')
    elif name == 'whitebeard':  # long pointed beard (#17 wizard)
        pts = [(cx - 230, 600), (cx - 120, 840), (cx, 1010), (cx + 120, 840), (cx + 230, 600), (cx + 120, 700), (cx, 720), (cx - 120, 700)]
        d.polygon(pts, fill=col); d.line(pts + [pts[0]], fill=K, width=11, joint='curve')
        for x in (-80, 0, 80): d.line([cx + x, 760, cx + x * 0.5, 940], fill=dk_(col), width=6)
    elif name == 'stubbledots':  # dotted stubble on the jaw (#14 emperor, #17)
        r = _random.Random(7)
        for _ in range(110):
            a = r.uniform(0.15, 0.85) * math.pi; rr = r.uniform(250, 370)
            x, y = cx + rr * math.cos(a) * 1.0, 560 + rr * math.sin(a) * 0.9
            if y > 900: continue
            d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=col)
    elif name == 'sideburns':
        for sx in (-1, 1): d.polygon([(CX + sx * 370, 300), (CX + sx * 395, 330), (CX + sx * 380, 560), (CX + sx * 330, 540), (CX + sx * 330, 300)], fill=col)
def dk_(c, f=0.7): return tuple(int(v * f) for v in c[:3]) + (255,)

# ------------------------------------------------------------------ hairstyles (hairdo)
HAIRDO = ['sidepart', 'spiky', 'curly', 'messy', 'cowlick', 'topknot', 'bowl', 'afro', 'bangs']
def hairdo_back(d, name, col, K):
    col = tuple(col)[:3] + (255,)
    if name == 'afro': d.ellipse([70, 50, 954, 700], fill=col, outline=K, width=26)
    if name == 'bangs': d.rounded_rectangle([92, 170, 932, 800], 260, fill=col, outline=K, width=26)
def hairdo(d, name, col, K, dx=0):
    col = tuple(col)[:3] + (255,); hl = tuple(min(255, int(v * 1.5) + 40) for v in col[:3]) + (255,)
    if name == 'sidepart':   # slick helmet with a side-swept fringe and highlight streaks (#12, #21, #25)
        d.chord([140, 136, 884, 470], 180, 360, fill=col, outline=K, width=26)
        d.pieslice([120, 150, 760, 560], 180, 300, fill=col, outline=K, width=22)
        for i in range(3): d.arc([260 + i * 60, 170 + i * 10, 760 + i * 30, 420], 200, 250, fill=hl, width=10)
    elif name == 'spiky':    # a few tall flame tufts leaning one way (#08 ginger, #11 quiff)
        tufts = [(250, 40, 170), (380, 10, 210), (510, 0, 250), (640, 20, 230), (770, 60, 190)]
        for x, lean, h in tufts:
            pts = [(x - 80, 270), (x + lean - 10, 250 - h), (x + 30, 190), (x + 80, 270)]
            d.polygon(pts, fill=col); d.line(pts, fill=K, width=16, joint='curve')
        d.chord([150, 120, 874, 420], 180, 360, fill=col, outline=K, width=26)
    elif name == 'curly':    # bubbles along the crown (#02 orange curls)
        for x in range(180, 860, 84):
            d.ellipse([x - 62, 120 + (x % 3) * 12, x + 62, 244 + (x % 3) * 12], fill=col, outline=K, width=16)
        for x in range(220, 820, 110): d.ellipse([x - 70, 70, x + 70, 200], fill=col, outline=K, width=16)
        d.chord([160, 150, 864, 380], 180, 360, fill=col)
    elif name == 'messy':    # short dark mop, jagged fringe (#21, #22 headband men)
        d.chord([140, 130, 884, 440], 180, 360, fill=col, outline=K, width=26)
        pts = [(160, 285)] + [(200 + i * 70, 285 + (40 if i % 2 else 0)) for i in range(10)] + [(864, 285), (864, 200), (160, 200)]
        d.polygon(pts, fill=col); d.line(pts[:12], fill=K, width=14, joint='curve')
    elif name == 'cowlick':  # bare crown, one curled strand (#11, #13 kid)
        d.arc([CX - 20, 40, CX + 120, 170], 120, 330, fill=K, width=16)
        d.arc([CX - 60, 70, CX + 60, 170], 180, 300, fill=K, width=14)
    elif name == 'topknot':  # samurai chonmage: shaved crown band, tied knot on top (#25)
        d.chord([180, 150, 844, 360], 180, 360, fill=col, outline=K, width=22)
        d.rounded_rectangle([CX - 40, 40, CX + 40, 170], 30, fill=col, outline=K, width=16); d.line([CX - 44, 140, CX + 44, 140], fill=(200, 50, 50, 255), width=14)
    elif name == 'bowl':     # brown bowl cut with a straight fringe and side panels (#09 boy)
        d.chord([132, 130, 892, 520], 180, 360, fill=col, outline=K, width=26)
        for sx in (-1, 1): d.rounded_rectangle([CX + sx * 345 - 50, 300, CX + sx * 345 + 50, 500], 30, fill=col, outline=K, width=18)
        d.rectangle([150, 300, 874, 330], fill=col); d.line([180, 330, 844, 330], fill=K, width=14)
    elif name == 'afro':
        for x in range(200, 840, 80): d.arc([x - 50, 110, x + 50, 210], 180, 360, fill=dk_(col), width=8)
    elif name == 'bangs':    # woman: dark bob with a heavy fringe over one eye (#06)
        d.chord([140, 136, 884, 470], 180, 360, fill=col, outline=K, width=26)
        d.polygon([(180, 300), (700, 260), (760, 420), (520, 360), (300, 420)], fill=col); d.line([(300, 420), (520, 360), (760, 420)], fill=K, width=14)

# ------------------------------------------------------------------ perspective hats (hat3d), drawn upright then tilted
HAT3D = ['trucker', 'bowler3d', 'tophat3d', 'cowboy3d', 'flatcap3d', 'beanie3d']
def hat3d(name, col, K, tilt=0, dx=0, col2=None):
    """returns a 1024 RGBA layer. Rick's hats are small 3D props: the brim is an ellipse seen from slightly below and to one side,
    the band curves with it, the crown carries a lit and a shaded side, and the whole hat sits tilted (#24 cool-shades trucker, #03 bowler)."""
    lay = Image.new('RGBA', (1024, 1024), CLEAR); d = ImageDraw.Draw(lay)
    col = tuple(col)[:3] + (255,); sh = dk_(col, 0.72); hi = tuple(min(255, int(v * 1.25) + 25) for v in col[:3]) + (255,)
    W = 22
    if name == 'trucker':   # mesh-back cap, white front panel, brim jutting toward the facing side
        c2 = tuple(col2 or (245, 245, 245))[:3] + (255,)
        d.chord([150, 60, 874, 420], 180, 360, fill=col, outline=K, width=W)
        d.chord([300, 70, 724, 400], 180, 360, fill=c2, outline=K, width=16)
        d.line([CX, 70, CX, 240], fill=dk_(c2), width=8); d.ellipse([CX - 22, 52, CX + 22, 92], fill=col, outline=K, width=8)
        d.polygon([(250, 236), (780, 236), (900, 300), (700, 330), (300, 300)], fill=sh); d.line([(250, 236), (780, 236), (900, 300), (700, 330), (300, 300), (250, 236)], fill=K, width=W, joint='curve')
        d.rectangle([150, 214, 874, 240], fill=dk_(col, 0.5))
    elif name == 'bowler3d':
        d.ellipse([150, 230, 874, 320], fill=sh, outline=K, width=W)
        d.chord([210, 40, 814, 470], 180, 360, fill=col, outline=K, width=W)
        d.rectangle([222, 206, 802, 250], fill=dk_(col, 0.45)); d.line([222, 250, 802, 250], fill=K, width=12)
        d.arc([300, 70, 720, 360], 200, 250, fill=hi, width=16)
    elif name == 'tophat3d':
        d.ellipse([150, 270, 874, 350], fill=sh, outline=K, width=W)
        d.rectangle([270, 40, 754, 300], fill=col); d.rectangle([700, 60, 750, 290], fill=sh)
        d.line([270, 40, 270, 300], fill=K, width=W); d.line([754, 40, 754, 300], fill=K, width=W)
        d.rectangle([272, 220, 752, 280], fill=dk_(col, 0.45))
        d.ellipse([270, 10, 754, 80], fill=hi, outline=K, width=W)
    elif name == 'cowboy3d':
        d.ellipse([40, 210, 984, 340], fill=sh, outline=K, width=W)
        d.arc([40, 150, 200, 300], 90, 200, fill=K, width=W); d.arc([824, 150, 984, 300], 340, 90, fill=K, width=W)
        d.chord([250, 40, 774, 420], 180, 360, fill=col, outline=K, width=W); d.line([CX - 60, 60, CX, 100, CX + 60, 60], fill=sh, width=14)
        d.rectangle([262, 200, 762, 240], fill=dk_(col, 0.45))
    elif name == 'flatcap3d':
        d.chord([140, 100, 884, 440], 180, 360, fill=col, outline=K, width=W)
        d.polygon([(220, 250), (820, 250), (860, 300), (180, 300)], fill=sh); d.line([(220, 250), (820, 250), (860, 300), (180, 300), (220, 250)], fill=K, width=16)
        for x in (330, 460, 590, 720): d.arc([x - 120, 110, x + 120, 330], 220, 300, fill=sh, width=8)
    elif name == 'beanie3d':
        d.chord([140, 60, 884, 470], 180, 360, fill=col, outline=K, width=W)
        d.rounded_rectangle([140, 200, 884, 280], 30, fill=sh, outline=K, width=16)
        for x in range(200, 840, 50): d.line([x, 205, x, 275], fill=dk_(col, 0.55), width=6)
    # Rick's hats sit low and big on the crown (brim about a third of the way down the head): scale 1.08 about the crown, drop 40 px
    lay = lay.resize((1106, 1106), Image.LANCZOS).crop((41, 0, 1065, 1024))
    lay = lay.rotate(-tilt, resample=Image.BICUBIC, center=(CX, 300))
    out = Image.new('RGBA', (1024, 1024), CLEAR); out.alpha_composite(lay, (int(dx), 40))
    return out
