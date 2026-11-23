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
try:   # Blender's Python has no PIL: lib.py only needs expand()/alternates(), the drawing code runs in cast.py
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
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

# =================================================================== ROUND 3 (owner Nov 22 2026, 5:28 PM CT)
# Owner's benchmark review: goatee and king bigger and hanging past the chin; full beard re-benchmarked on Rick's #22 bearded soldier
# (the old ref was a masked robber); sideburns and afro dropped; spiky, curly, cowlick, messy, bowl and bangs redrawn as closer copies of
# Rick (#08 ginger tufts, #02 orange curls, #11/#13 strand rising from a full head of hair, #13 messy spikes, #09 bowl, #06/#12 fringes);
# hats redrawn on Rick's proportions (#23 top hat, #07 cowboy, #03 newsboy, #24 trucker, #03/#23 bowler) and NO hair may show above a
# hat's brim (hair is erased under every hat3d). Approved round-2 items (pencil, chevron, curled, walrus, toothbrush, droop, whitebeard,
# stubbledots, sidepart, topknot, beanie3d) keep their round-2 drawing exactly.
# Tall items need room outside the 1024 square: pads(c) gives (top, bottom) pixels; cast.head() returns a 1024 x (top+1024+bottom)
# texture and lib.char() makes the face card taller by the same ratio, so the head itself stays where it was.
BANNED = {'sideburns', 'afro'}            # owner Nov 22 5:28 PM CT: never use
FHAIR = [n for n in FHAIR if n not in BANNED]
HAIRDO = [n for n in HAIRDO if n not in BANNED]
_fhair_r2, _hairdo_r2, _hairdo_back_r2, _hat3d_r2 = fhair, hairdo, hairdo_back, hat3d
SS3 = 2                                   # new items are drawn at 2x and downsampled (clean edges)
HEADROOM = {'tophat3d': 256, 'cowboy3d': 256, 'bowler3d': 128}
HAIRROOM = {'spiky': 128, 'cowlick': 160, 'curly': 64}
FOOTROOM = {'goatee': 128, 'king': 128, 'fullbeard': 160}

def pads(c):
    """(top, bottom) extra texture pixels a character's head needs; (0, 0) for everyone else (renders in flight are unchanged)"""
    top = HEADROOM.get(c.get('hat3d'), 0) if c.get('hat3d') else HAIRROOM.get(c.get('hairdo'), 0)
    return int(top), int(FOOTROOM.get(c.get('fhair'), 0))

def _cr(pts, n=10, closed=True):
    """Catmull-Rom spline through pts"""
    P = list(pts); out = []
    m = len(P) if closed else len(P) - 1
    for i in range(m):
        p0 = P[i - 1] if (closed or i > 0) else P[i]; p1 = P[i]; p2 = P[(i + 1) % len(P)]; p3 = P[(i + 2) % len(P)] if (closed or i + 2 < len(P)) else p2
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    if not closed: out.append(P[-1])
    return out

class _L:
    """a 2x RGBA drawing layer in head coordinates (y may be negative down to -top), returned at 1x with .done()"""
    def __init__(self, top=0, bottom=0):
        self.oy = top; self.H = 1024 + top + bottom
        self.im = Image.new('RGBA', (1024 * SS3, self.H * SS3), CLEAR); self.d = ImageDraw.Draw(self.im)
    def p(self, pts): return [(x * SS3, (y + self.oy) * SS3) for x, y in pts]
    def b(self, box): x0, y0, x1, y1 = box; return [x0 * SS3, (y0 + self.oy) * SS3, x1 * SS3, (y1 + self.oy) * SS3]
    def mask(self): return Image.new('L', self.im.size, 0)
    def poly(self, pts, fill=None, K=None, w=0, d=None):
        d = d or self.d; q = self.p(pts)
        if fill is not None: d.polygon(q, fill=fill)
        if K is not None and w: self.line(pts + pts[:2], K, w, d=d)
    def line(self, pts, col, w, d=None, caps=True):
        d = d or self.d; q = self.p(pts); W = int(w * SS3)
        d.line(q, fill=col, width=W, joint='curve')
        if caps:
            for x, y in (q[0], q[-1]): d.ellipse([x - W / 2 + 1, y - W / 2 + 1, x + W / 2 - 1, y + W / 2 - 1], fill=col)
    def ell(self, box, fill=None, K=None, w=0, d=None):
        (d or self.d).ellipse(self.b(box), fill=fill, outline=K, width=int(w * SS3))
    def shapes(self, polys, col, K, w, union=True, circles=()):
        """filled shapes with a w-px ink outline. union=True: one silhouette (no inner lines); False: layered, each over the last"""
        items = [('p', s) for s in polys] + [('c', s) for s in circles]
        def ink(kind, s):
            if kind == 'p': self.poly(s, K, K, 2 * w)
            else: x0, y0, x1, y1 = s; self.ell([x0 - w, y0 - w, x1 + w, y1 + w], K)
        def fil(kind, s):
            if kind == 'p': self.poly(s, col)
            else: self.ell(s, col)
        if union:
            for it in items: ink(*it)
            for it in items: fil(*it)
        else:
            for it in items: ink(*it); fil(*it)
    def clipdraw(self, region_polys, fn, region_circles=()):
        """run fn(draw) on a scratch layer and keep only what lands inside the given region (for highlights, shading, strands)"""
        m = self.mask(); md = ImageDraw.Draw(m)
        for s in region_polys: md.polygon(self.p(s), fill=255)
        for s in region_circles: md.ellipse(self.b(s), fill=255)
        lay = Image.new('RGBA', self.im.size, CLEAR); fn(ImageDraw.Draw(lay))
        a = lay.getchannel('A'); from PIL import ImageChops; lay.putalpha(ImageChops.multiply(a, m))
        self.im.alpha_composite(lay)
    def done(self): return self.im.resize((1024, self.H), Image.LANCZOS)

def _lt(c, f=1.35, add=25): return tuple(min(255, int(v * f) + add) for v in c[:3]) + (255,)
def _hc(a, r=400, cx=CX, cy=540):
    """point on the head circle (angle in degrees, 270 = top, y down)"""
    return (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
def _arcpts(a0, a1, r, n=24, cx=CX, cy=540): return [_hc(a0 + (a1 - a0) * i / n, r, cx, cy) for i in range(n + 1)]

# ------------------------------------------------------------------ facial hair, round 3
def fhair_layer(name, col, K, dx=0, top=0, bottom=0):
    """goatee / king / fullbeard on a padded layer (head coords); None for items that keep their round-2 drawing"""
    if name not in ('goatee', 'king', 'fullbeard'): return None
    L = _L(top, bottom); cx = CX + dx; col = tuple(col)[:3] + (255,); dkc = dk_(col, 0.62); hi = _lt(col, 1.3, 40)
    if name == 'goatee':   # Rick #25 samurai: broad dark tuft from under the lip, hanging well past the chin to a split point
        patch = [(cx - 26, 662), (cx + 26, 662), (cx + 12, 700), (cx - 12, 700)]
        g = _cr([(cx - 70, 728), (cx - 20, 716), (cx + 20, 716), (cx + 70, 728), (cx + 78, 800), (cx + 62, 900), (cx + 38, 1000), (cx + 14, 1080), (cx, 1050), (cx - 14, 1082), (cx - 40, 1000), (cx - 64, 900), (cx - 80, 800)], 8)
        L.shapes([patch], col, K, 9); L.shapes([g], col, K, 11)
        L.clipdraw([g], lambda dd: [dd.line(L.p([(cx + x, 760), (cx + x * 0.6, 880), (cx + x * 0.25, 1010)]), fill=hi, width=7 * SS3, joint='curve') for x in (-34, 30)])
        L.clipdraw([g], lambda dd: dd.line(L.p([(cx, 770), (cx + 2, 900), (cx, 1040)]), fill=dkc, width=8 * SS3, joint='curve'))
    elif name == 'king':   # Rick #17 king: thin curled moustache + soul patch + long narrow pointed goatee past the chin
        for sx in (-1, 1):
            L.line([(cx + sx * 10, 566), (cx + sx * 60, 572), (cx + sx * 100, 560), (cx + sx * 116, 536), (cx + sx * 104, 522)], K, 26)
            L.line([(cx + sx * 10, 566), (cx + sx * 60, 572), (cx + sx * 100, 560), (cx + sx * 116, 536), (cx + sx * 104, 522)], col, 12)
        patch = [(cx - 18, 664), (cx + 18, 664), (cx + 6, 698), (cx - 6, 698)]
        g = _cr([(cx - 30, 726), (cx + 30, 726), (cx + 32, 800), (cx + 20, 900), (cx + 8, 1000), (cx - 4, 1086), (cx - 18, 990), (cx - 30, 880), (cx - 34, 790)], 8)
        L.shapes([patch], col, K, 8); L.shapes([g], col, K, 10)
        L.clipdraw([g], lambda dd: dd.line(L.p([(cx + 14, 750), (cx + 8, 880), (cx - 2, 1020)]), fill=hi, width=6 * SS3, joint='curve'))
    elif name == 'fullbeard':   # Rick #22 soldier: no moustache; starts beside the mouth, covers the jaw, hangs a quarter-head below the chin
        r = _random.Random(22)
        topedge = [(150, 700), (260, 694), (400, 700), (CX - 60 + dx, 704), (CX + 60 + dx, 704), (624, 700), (764, 694), (874, 700)]
        side_r = _arcpts(26, 62, 414)
        bottom = []
        for i, x in enumerate(range(760, 250, -34)):
            y = 1040 + 70 * math.sin(math.pi * (x - 250) / 510) + (26 if i % 2 else -8) + r.randint(-6, 6)
            bottom.append((x + r.randint(-6, 6), y))
        side_l = _arcpts(118, 154, 414)
        beard = topedge + side_r + bottom + side_l
        beard = [(x, y) for x, y in beard]
        L.shapes([beard], col, K, 14)
        def tex(dd):
            for _ in range(300):
                x = r.uniform(150, 874); y = r.uniform(690, 1180); ln = r.uniform(30, 64); a = math.radians(90 + r.uniform(-20, 20) + (x - 512) * 0.05)
                c_ = (dk_(col, 0.45) if r.random() < 0.6 else dkc) if r.random() < 0.88 else hi
                dd.line(L.p([(x, y), (x + ln * math.cos(a), y + ln * math.sin(a))]), fill=c_, width=int(r.choice((5, 6, 7)) * SS3))
        L.clipdraw([beard], tex)
    return L.done()

def fhair(im, name, col, K, dx=0):
    """round-2 entry point kept for approved items; round-3 items draw the part of fhair_layer() that fits in the 1024 square"""
    if name in BANNED: return
    if name in ('goatee', 'king', 'fullbeard'):
        im.alpha_composite(fhair_layer(name, col, K, dx).crop((0, 0, 1024, 1024))); return
    _fhair_r2(im, name, col, K, dx)

# ------------------------------------------------------------------ hairstyles, round 3
def _cap(r_out=414, a0=192, a1=348):
    return _arcpts(a0, a1, r_out)

def hair_layer(name, col, K, dx=0, top=0):
    """Rick hairstyles on their own padded layer (head coords). Composited AFTER the face features (hairlines end above the brows),
    erased under any hat. Returns None for approved round-2 styles (sidepart, topknot), which still draw on the head."""
    if name not in ('spiky', 'curly', 'messy', 'cowlick', 'bowl', 'bangs'): return None
    L = _L(top, 0); col = tuple(col)[:3] + (255,); dkc = dk_(col, 0.66); hi = _lt(col, 1.3, 45); r = _random.Random(sum(map(ord, name)))
    W = 22
    def shade(region, cx_=-120):   # Rick's hair carries the head's cel shadow: a darker band on the lower-left
        L.clipdraw([region], lambda dd: dd.ellipse(L.b([CX - 520 + cx_, 300, CX + 120 + cx_, 1100]), fill=dkc))
    if name == 'bowl':   # Rick #09: glossy brown cap, part on the left, fringe sweeping right in one convex curve, sides to the temples
        outer = _cap(416, 190, 350)
        hl = _cr([(884, 452), (866, 360), (812, 292), (716, 262), (600, 268), (500, 288), (418, 300), (392, 262), (318, 252), (232, 286), (172, 360), (150, 452)], 6, closed=False)
        cap = outer + hl
        L.shapes([cap], col, K, W); shade(cap)
        def hls(dd):
            for k, (y0, w_) in enumerate(((176, 14), (206, 10))):
                dd.line(L.p(_cr([(430, y0 + 12), (560, y0 - 8), (690, y0 + 6), (800, y0 + 50)], 6, closed=False)), fill=hi, width=w_ * SS3, joint='curve')
        L.clipdraw([cap], hls)
        L.line([(426, 146), (410, 200), (394, 258)], K, 9)    # part
        L.line([(330, 262), (300, 300), (296, 330)], K, 8)    # strand at the part
    elif name == 'bangs':   # Rick #12 office men / #21: glossy black helmet of hair, fringe straight across the brow line,
                            # sides to the ears, a stack of long white-grey highlight streaks across the crown
        outer = _cap(424, 190, 350)
        fringe = _cr([(888, 470), (872, 380), (836, 300), (740, 270), (620, 268), (500, 274), (380, 284), (270, 300), (196, 330), (168, 400), (150, 470)], 6, closed=False)
        cap = outer + fringe
        L.shapes([cap], col, K, W); shade(cap, -160)
        hl2 = _lt(col, 1.1, 130) if sum(col[:3]) < 200 else hi
        def hls(dd):
            for k in range(5):
                dd.line(L.p(_arcpts(216 + k * 3, 296 - k * 5, 372 - k * 30, 18, CX - 10, 570)), fill=hl2, width=int((12 - k * 1.2) * SS3), joint='curve')
        L.clipdraw([cap], hls)
        L.line(_cr([(820, 300), (790, 250), (760, 230)], 4, closed=False), K, 8)    # fringe tip strand on the long side
    elif name == 'spiky':   # Rick #08 ginger: one hair mass whose top breaks into a few big pointed locks sweeping up and right,
                            # ink lines between the locks, a darker stroke inside each, freckle dots; hairline a row of small points
        outer = _cap(412, 196, 344)
        hl = [(884, 430), (864, 330)]
        for i, x in enumerate(range(800, 180, -62)): hl.append((x, 262 if i % 2 == 0 else 298))
        hl += [(172, 330), (146, 430)]
        cap = outer + hl
        def lock(bl, br, tp):   # a flame lock: base on the cap, body bulging up-left, hollow right edge, sharp tip flicking up and right
            ml = (bl[0] - 30 + (tp[0] - bl[0]) * 0.12, bl[1] + (tp[1] - bl[1]) * 0.62)
            mr = (tp[0] - (tp[0] - br[0]) * 0.45 - 40, tp[1] + (br[1] - tp[1]) * 0.5)
            return (_cr([bl, ml, tp, mr, br, ((bl[0] + br[0]) / 2, (bl[1] + br[1]) / 2 + 50)], 10), bl, ml, tp, br)
        back = [lock((150, 360), (380, 200), (400, -70)), lock((300, 210), (560, 160), (590, -110)), lock((470, 170), (720, 190), (770, -84)),
                lock((640, 210), (880, 340), (930, 10))]
        front = [lock((200, 300), (440, 260), (500, 10)), lock((430, 270), (660, 270), (700, 36))]
        shapes = back + front
        L.shapes([cap], col, K, W)
        for f in back: L.shapes([f[0]], col, K, 14, union=False)
        for f in front: L.shapes([f[0]], col, K, 13, union=False)
        shade(cap)
        for sh_, bl, ml, tp, br in shapes:   # inside each lock: a darker stroke along it, a light sheen near the tip, freckle dots
            mid = ((bl[0] + br[0]) / 2, (bl[1] + br[1]) / 2 + 30)
            def inner(dd, mid=mid, tp=tp, ml=ml):
                dd.line(L.p(_cr([mid, ((mid[0] + tp[0]) / 2 + 14, (mid[1] + tp[1]) / 2 + 6), (tp[0] - (tp[0] - mid[0]) * 0.15, tp[1] + 40)], 6, closed=False)), fill=dkc, width=10 * SS3, joint='curve')
                dd.line(L.p(_cr([((ml[0] + tp[0]) / 2 + 20, (ml[1] + tp[1]) / 2 + 24), (tp[0] - 30, tp[1] + 30)], 4, closed=False)), fill=hi, width=8 * SS3, joint='curve')
                for _ in range(4):
                    x = r.uniform(min(mid[0], tp[0]), max(mid[0], tp[0])); y = r.uniform(tp[1] + 40, mid[1] - 10); dd.ellipse(L.b([x - 5, y - 5, x + 5, y + 5]), fill=dkc)
            L.clipdraw([sh_], inner)
    elif name == 'curly':   # Rick #02: a cloud of round curls, wider than the crown, scalloped fringe, curl strokes inside
        circles = []
        for i in range(9):
            a = 192 + i * 19.5; x, y = _hc(a, 395, CX, 470); rr = 92 if 230 < a < 310 else 80
            circles.append([x - rr, y - rr, x + rr, y + rr])
        for x in range(212, 840, 88): circles.append([x - 58, 200, x + 58, 292])
        for sx in (-1, 1): circles.append([CX + sx * 352 - 56, 270, CX + sx * 352 + 56, 382])
        core = _arcpts(190, 350, 380, 24, CX, 470) + [(840, 260), (184, 260)]
        L.shapes([core], col, K, 18, circles=circles)
        shade(core)
        def curls(dd):
            for bx in circles:
                x0, y0, x1, y1 = bx; cxx, cyy = (x0 + x1) / 2, (y0 + y1) / 2; rr = (x1 - x0) * 0.32
                a0 = r.uniform(150, 220); dd.arc(L.b([cxx - rr, cyy - rr, cxx + rr, cyy + rr]), a0, a0 + 200, fill=dkc, width=8 * SS3)
            for _ in range(10):
                x, y = r.uniform(260, 760), r.uniform(120, 230); rr = r.uniform(18, 30)
                dd.arc(L.b([x - rr, y - rr, x + rr, y + rr]), 200, 340, fill=hi, width=6 * SS3)
        L.clipdraw([core], curls, circles)
    elif name == 'cowlick':   # Rick #11/#13: a full head of side-swept hair with one strand curling up off the crown
        outer = _cap(414, 190, 350)
        hl = _cr([(886, 450), (870, 350), (820, 286), (720, 262), (600, 262), (480, 276), (380, 300), (300, 300), (220, 320), (170, 380), (150, 452)], 6, closed=False)
        cap = outer + hl
        L.shapes([cap], col, K, W); shade(cap)
        L.clipdraw([cap], lambda dd: dd.line(L.p(_cr([(400, 180), (560, 160), (720, 200), (820, 270)], 6, closed=False)), fill=hi, width=12 * SS3, joint='curve'))
        for x0 in (600, 470, 360):   # comb lines sweeping toward the fringe
            L.line(_cr([(x0 + 20, 160), (x0 - 20, 220), (x0 - 70, 286)], 5, closed=False), dkc, 8)
        # the strand: a tapered blade from the crown, bending back and curling at the tip (Rick #11 onion-tip, #13 sprout)
        strand = _cr([(500, 146), (560, 146), (590, 80), (566, 0), (520, -60), (470, -96), (500, -40), (520, 20), (510, 90)], 8)
        L.shapes([strand], col, K, 12, union=False)
        L.line(_cr([(530, 140), (548, 60), (520, -20), (488, -76)], 5, closed=False), dkc, 7)
        small = _cr([(620, 152), (650, 150), (676, 90), (700, 40), (672, 60), (640, 110)], 6)
        L.shapes([small], col, K, 10, union=False)
    elif name == 'messy':   # Rick #13 (glasses dad): short brown mop with thin spikes sticking out every way, a few on the forehead
        outer = _cap(410, 192, 348)
        hl = [(882, 440), (864, 340), (800, 284), (740, 300), (700, 262), (620, 280), (560, 258), (500, 290), (440, 262), (380, 286), (300, 270), (230, 300), (176, 350), (152, 440)]
        cap = outer + hl
        spikes = []
        for a in list(range(198, 346, 15)):
            a2 = a + r.uniform(-4, 4); base = 404; ln = r.uniform(70, 140); dev = r.uniform(-34, 34)
            b0, b1 = _hc(a2 - 3.2, base), _hc(a2 + 3.2, base); tip = _hc(a2 + dev * 0.25, base + ln)
            mid = ((b0[0] + tip[0]) / 2 + dev * 0.4, (b0[1] + tip[1]) / 2)
            spikes.append(_cr([b0, mid, tip, b1], 5))
        for x, ln in ((420, 52), (610, 60), (730, 46)):   # a few strands falling onto the forehead
            spikes.append(_cr([(x - 26, 262), (x + 10, 280), (x + 30, 262 + ln), (x + 26, 262)], 5))
        L.shapes([cap] + spikes, col, K, 14)
        shade(cap)
        for _ in range(7):
            x = r.uniform(260, 760); y = r.uniform(170, 250)
            L.line(_cr([(x, y), (x + r.uniform(-30, 30), y + 30), (x + r.uniform(-40, 40), y + 56)], 4, closed=False), dkc, 7)
    return L.done()

def hairdo(d, name, col, K, dx=0):
    """round-2 entry point (draws on the head): only the approved styles still draw here; round-3 styles come from hair_layer()"""
    if name in BANNED: return
    if name in ('sidepart', 'topknot'): _hairdo_r2(d, name, col, K, dx)
def hairdo_back(d, name, col, K): return   # afro (banned) and old bangs were the only back pieces

# ------------------------------------------------------------------ hats, round 3
def hat3d_layer(name, col, K, tilt=0, dx=0, col2=None, top=0, bottom=0):
    """Rick-proportioned hats on a padded layer (head coords). Returns (layer, brim_y). beanie3d keeps its approved round-2 drawing."""
    if name == 'beanie3d':
        lay = _hat3d_r2(name, col, K, tilt, dx, col2); out = Image.new('RGBA', (1024, 1024 + top + bottom), CLEAR); out.alpha_composite(lay, (0, top)); return out, 330
    L = _L(top, bottom); col = tuple(col)[:3] + (255,); sh = dk_(col, 0.84 if sum(col[:3]) > 600 else 0.7); hi = _lt(col, 1.15, 30); W = 20
    c2 = tuple(col2 or (245, 245, 245))[:3] + (255,); band = dk_(col, 0.35) if sum(col[:3]) > 200 else (20, 20, 24, 255)
    if name == 'tophat3d':   # Rick #23: tall crown flaring slightly toward the top, black band, brim curled up at both sides, low on the head
        by = 236; band = (26, 22, 28, 255)
        brim = _cr([(52, by - 52), (180, by - 2), (512, by + 20), (844, by - 2), (972, by - 52), (960, by), (830, by + 46), (512, by + 66), (194, by + 46), (64, by)], 6)
        L.shapes([brim], col, K, W)
        L.clipdraw([brim], lambda dd: dd.line(L.p(_cr([(70, by - 10), (200, by + 34), (512, by + 54), (824, by + 34), (954, by - 10)], 6, closed=False)), fill=band, width=18 * SS3, joint='curve'))
        crown = [(266, by + 14), (236, -150), (788, -150), (758, by + 14)]
        L.poly(crown, col, K, W)
        L.clipdraw([crown], lambda dd: dd.polygon(L.p([(690, by + 40), (676, -160), (800, -160), (800, by + 40)]), fill=sh))
        L.clipdraw([crown], lambda dd: dd.polygon(L.p(_cr([(230, by - 66), (512, by - 50), (794, by - 66)], 6, closed=False) + [(794, by + 30), (230, by + 30)]), fill=band))
        L.line(_cr([(266, by + 10), (512, by + 28), (758, by + 10)], 6, closed=False), K, W)
        L.ell([236, -184, 788, -116], hi, K, W)                            # top
        L.line([(306, by - 70), (290, -110)], _lt(col, 1.0, 60), 10)       # highlight stripe
    elif name == 'cowboy3d':   # Rick #07: pinched crown, very wide thin brim curling up at both sides
        by = 210
        brim = _cr([(20, 120), (120, 200), (300, by + 32), (512, by + 44), (724, by + 32), (904, 200), (1004, 120), (990, 170), (880, 250), (700, by + 74), (512, by + 84), (324, by + 74), (144, 250), (34, 170)], 6)
        L.shapes([brim], sh, K, W)
        L.clipdraw([brim], lambda dd: dd.line(L.p(_cr([(60, 150), (300, by + 36), (512, by + 48), (724, by + 36), (964, 150)], 6, closed=False)), fill=col, width=22 * SS3, joint='curve'))
        crown = _cr([(300, by + 40), (300, 60), (330, -110), (420, -170), (512, -126), (604, -170), (694, -110), (724, 60), (724, by + 40), (512, by + 56)], 8)
        L.shapes([crown], col, K, W)
        L.clipdraw([crown], lambda dd: dd.polygon(L.p([(620, -200), (760, -200), (760, by + 60), (650, by + 60)]), fill=sh))
        L.clipdraw([crown], lambda dd: dd.polygon(L.p(_cr([(280, by - 20), (512, by - 4), (744, by - 20)], 6, closed=False) + _cr([(744, by + 44), (512, by + 60), (280, by + 44)], 6, closed=False)), fill=dk_(col, 0.45)))
        L.line(_cr([(512, -120), (500, -40), (512, 40)], 5, closed=False), sh, 10)   # front crease
    elif name == 'bowler3d':   # Rick #03/#23: round dome, brim with both sides curled up, sheen on the dome
        by = 240
        brim = _cr([(120, by - 40), (240, by + 6), (512, by + 26), (784, by + 6), (904, by - 40), (900, by + 6), (780, by + 56), (512, by + 74), (244, by + 56), (124, by + 6)], 6)
        L.shapes([brim], sh, K, W)
        dome = _cr([(222, by + 10), (230, 60), (330, -60), (512, -100), (694, -60), (794, 60), (802, by + 10), (512, by + 30)], 8)
        L.shapes([dome], col, K, W)
        L.clipdraw([dome], lambda dd: dd.polygon(L.p(_cr([(200, by - 40), (512, by - 22), (824, by - 40)], 6, closed=False) + [(824, by + 60), (200, by + 60)]), fill=dk_(col, 0.55) if sum(col[:3]) > 150 else (70, 66, 74, 255)))
        L.clipdraw([dome], lambda dd: dd.line(L.p(_cr([(300, 120), (360, -10), (470, -70)], 6, closed=False)), fill=_lt(col, 1.6, 90), width=16 * SS3, joint='curve'))
    elif name == 'flatcap3d':   # Rick #03 newsboy: puffy crown wider than the head, panels from a top button, short peak over the brows
        by = 268
        crown = _cr([(118, by + 20), (130, 160), (250, 60), (512, 28), (790, 56), (910, 150), (912, by + 16), (512, by)], 8)
        L.shapes([crown], col, K, W)
        def stripes(dd):
            if col2 is not None:
                for k in range(-9, 10):
                    dd.line(L.p(_cr([(560, 40), (560 + k * 30, 120), (512 + k * 52, by + 20)], 6, closed=False)), fill=c2, width=11 * SS3, joint='curve')
            else:
                for k in (-3, -1, 1, 3): dd.line(L.p(_cr([(560, 40), (560 + k * 40, 130), (512 + k * 90, by + 20)], 6, closed=False)), fill=sh, width=8 * SS3, joint='curve')
            dd.polygon(L.p([(118, 180), (118, by + 30), (420, by + 30)]), fill=sh)
        L.clipdraw([crown], stripes)
        L.ell([538, 24, 586, 60], col, K, 9)
        peak = _cr([(270, by - 6), (512, by + 6), (760, by - 6), (730, by + 30), (512, by + 44), (296, by + 30)], 6)
        L.shapes([peak], dk_(col, 0.55), K, 14)
    elif name == 'trucker':   # Rick #24: rounded crown, white front panels with a centre seam and trim, curved peak seen from below
        by = 262
        crown = _cr([(126, by + 20), (150, 140), (300, 52), (512, 30), (724, 52), (874, 140), (898, by + 20), (512, by)], 8)
        L.shapes([crown], col, K, W)
        front = _cr([(240, by + 6), (270, 120), (400, 50), (512, 40), (624, 50), (754, 120), (784, by + 6), (512, by - 6)], 8)
        L.shapes([front], c2, K, 12)
        L.clipdraw([front], lambda dd: dd.line(L.p(_cr([(250, by - 4), (290, 140), (512, 60), (734, 140), (774, by - 4)], 6, closed=False)), fill=col, width=14 * SS3, joint='curve'))
        L.line(_cr([(512, 44), (506, 150), (512, by - 6)], 5, closed=False), dk_(c2, 0.6), 8)
        L.ell([492, 20, 532, 52], col, K, 8)
        peak = _cr([(200, by + 8), (512, by + 4), (824, by + 8), (790, by + 40), (512, by + 50), (234, by + 40)], 6)
        L.shapes([peak], col, K, 14)
        L.clipdraw([peak], lambda dd: dd.polygon(L.p([(200, by + 26), (824, by + 26), (824, by + 60), (200, by + 60)]), fill=sh))
    else:
        return None, 0
    lay = L.done().rotate(-tilt, resample=Image.BICUBIC, center=(CX, by + top), translate=(int(dx), 0))
    return lay, by

def hat3d(name, col, K, tilt=0, dx=0, col2=None):
    """round-2 entry point: a 1024 layer (anything above the square is cut). cast.head() uses hat3d_layer() with headroom instead."""
    lay, _ = hat3d_layer(name, col, K, tilt, dx, col2)
    return lay

def hat_region(hat, margin=26):
    """L mask, 255 where something under the hat must not show: above the hat's lower edge (+margin), column by column;
    columns the hat does not reach use the hat's lowest edge. Rick never shows hair above a brim."""
    W, H = hat.size; a = hat.getchannel('A').point(lambda v: 255 if v > 40 else 0)
    m = Image.new('L', (W, H), 0); bb = a.getbbox()
    if not bb: return m
    try:
        import numpy as np
        A = np.array(a) > 0; anyc = A.any(0); low = np.where(anyc, H - 1 - np.argmax(A[::-1], 0), -1).tolist()
    except Exception:
        px = a.load(); low = []
        for x in range(W):
            yy = -1
            for y in range(H - 1, -1, -1):
                if px[x, y]: yy = y; break
            low.append(yy)
    md = ImageDraw.Draw(m)
    for x in range(W): md.line([(x, 0), (x, (low[x] if low[x] >= 0 else bb[3]) + margin)], fill=255)
    return m

def erase_under_hat(lay, region, top=0):
    """clear lay wherever region (same width, at least as tall) is set, and keep what is left inside the head outline (+10 px):
    under a hat Rick shows hair only as a patch hugging the side of the head (#03 newsboy, #23 top hat), never sticking out"""
    from PIL import ImageChops
    r = region.crop((0, 0) + lay.size); keep = Image.new('L', lay.size, 0); ImageDraw.Draw(keep).ellipse([102, 130 + top, 922, 950 + top], fill=255)
    out = lay.copy(); out.putalpha(ImageChops.multiply(ImageChops.multiply(lay.getchannel('A'), ImageChops.invert(r)), keep)); return out

def restore_under_hat(im, pre, region):
    """on the 1024 head: hair drawn after `pre` is undone inside the hat region (the head disc comes back, back hair outside it goes)"""
    disc = Image.new('L', (1024, 1024), 0); ImageDraw.Draw(disc).ellipse([112, 140, 912, 940], fill=255)
    from PIL import ImageChops
    r = region.crop((0, 0, 1024, 1024))
    im.paste(pre, (0, 0), ImageChops.multiply(r, disc))
    im.paste(Image.new('RGBA', (1024, 1024), CLEAR), (0, 0), ImageChops.multiply(r, ImageChops.invert(disc)))

# ------------------------------------------------------------------ more turn variety (owner liked the turned faces: "add more")
# Per-face tokens in the extras string, so one character can look left in one shot and right in the next:
#   turnL / turnR / front    face slides to that side (round 2)
#   mouthL / mouthR / mouthC lopsided mouth on that side, overriding the character's mouth_side
#   tiltL / tiltR            whole head tipped ~8 degrees (Rick #22 headband man, #01 grin, #03 newsboy, #21 ranger), hat and hair with it
#   lookL / lookR            turn + mouth on the same side in one token (the common Rick pose)
def mouth_side(c, ex=''):
    ks = (ex or '').split('+'); m = c.get('mouth_side', 0)
    if 'mouthL' in ks or 'lookL' in ks: m = -1
    if 'mouthR' in ks or 'lookR' in ks: m = 1
    if 'mouthC' in ks: m = 0
    return m
def head_tilt(c, ex=''):
    ks = (ex or '').split('+'); t = c.get('head_tilt', 0)
    if 'tiltL' in ks: t = 8
    if 'tiltR' in ks: t = -8
    return t
_turn_dx_r2 = turn_dx
def turn_dx(c, ex=''):
    ks = (ex or '').split('+')
    if 'lookL' in ks: return -62
    if 'lookR' in ks: return 62
    return _turn_dx_r2(c, ex)
TOKENS = {'turnL', 'turnR', 'front', 'mouthL', 'mouthR', 'mouthC', 'tiltL', 'tiltR', 'lookL', 'lookR'}

# ------------------------------------------------------------------ growing library (owner Nov 22 2026, 5:52 PM CT)
# "the expression library page [should] keep accumulating new facial expressions ... a constant feedback loop that expands the library".
# Builders add faces WITHOUT editing this file: library_extra.json next to this file, {"faces": {name: [eyes, brows, mouth, extras]},
# "family": {name: family}, "log": [...]} using any eyes/brows/mouth/extras kind already defined here (or in cast.py).
# New drawing primitives (a new eye shape, hair, hat) still go in this file, in a dated section like ROUND 3 above.
# How-to and checklist: research/rick-style-spec/expression-library/CONTRIBUTING.md (project files).
def _load_extra():
    import json, os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'library_extra.json')
    if not os.path.exists(p): return
    try: E = json.load(open(p))
    except Exception as e: print('library_extra.json unreadable:', e); return
    for k, v in E.get('faces', {}).items():
        if k not in LIBRARY: LIBRARY[k] = tuple((list(v) + [''] * 4)[:4])
    for k, v in E.get('family', {}).items():
        for fam, members in FAMILY.items():
            if fam == v and k not in members: members.append(k) if isinstance(members, list) else None
_load_extra()

# ------------------------------------------------------------------ ADDED BY VIDEOS: 2026-11-22, Washington DC Thanksgiving (dc9)
# kepi3d: 1860s forage cap (Union blue / Confederate grey / postal brown), rule 334(b) addition.
# Rick refs: 15_022_0 (blue kepi, gold emblem, peak low over the brows) and 02_006_0 (blue peaked cap with badge), both in
# research/rick-style-spec/expression-library/round2|round3/ref-crops; side by side: additions/2026-11-22_washington-dc_kepi3d.jpg.
# Drawn like the round-2 hats (lit top ellipse, shaded far side, curved band, peak seen from below), then tilted. The caller squashes it
# to the top 60 % of the head like the head's other hats (DC cast.py), which keeps the brim above the brows.
HAT_PERIOD = ['kepi3d']
def hat3d_period(name, col, K, tilt=0, dx=0):
    if name not in HAT_PERIOD: return None
    lay = Image.new('RGBA', (1024, 1024), CLEAR); d = ImageDraw.Draw(lay)
    col = tuple(col)[:3] + (255,); sh = dk_(col, 0.72); hi = tuple(min(255, int(v * 1.25) + 25) for v in col[:3]) + (255,); W = 22; bd = dk_(col, 0.55)
    crown = [(230, 380), (270, 80), (800, 50), (812, 380)]
    d.polygon(crown, fill=col); d.polygon([(690, 58), (800, 50), (812, 380), (700, 380)], fill=sh)
    d.ellipse([262, 22, 808, 112], fill=hi, outline=K, width=W)
    d.line(crown + [crown[0]], fill=K, width=W, joint='curve')
    d.rectangle([222, 318, 820, 384], fill=bd); d.chord([222, 344, 820, 424], 0, 180, fill=bd); d.arc([222, 344, 820, 424], 0, 180, fill=K, width=12); d.line([222, 318, 820, 318], fill=K, width=10)
    d.chord([160, 370, 660, 520], 0, 180, fill=(24, 22, 26, 255), outline=K, width=W); d.arc([200, 380, 600, 470], 20, 90, fill=(80, 80, 90, 255), width=10)
    d.ellipse([470, 330, 520, 380], fill=(214, 180, 80, 255), outline=K, width=8)   # plain brass button, no insignia
    lay = lay.resize((1106, 1106), Image.LANCZOS).crop((41, 0, 1065, 1024)); lay = lay.rotate(-tilt, resample=Image.BICUBIC, center=(CX, 300))
    out = Image.new('RGBA', (1024, 1024), CLEAR); out.alpha_composite(lay, (int(dx), int(abs(tilt) * 4))); return out
# shared-rig hook (det cast.py goes through hat3d_layer for every hat3d): period hats come out squashed to the top 60 % of the head,
# exactly as DC's cast.py draws them, on the padded layer so hair under them is erased like under every other hat
_hat3d_layer_r3 = hat3d_layer
def hat3d_layer(name, col, K, tilt=0, dx=0, col2=None, top=0, bottom=0):
    if name in HAT_PERIOD:
        lay = hat3d_period(name, col, K, tilt, dx).resize((1024, int(1024 * 0.6)), Image.LANCZOS)
        out = Image.new('RGBA', (1024, 1024 + top + bottom), CLEAR); out.alpha_composite(lay, (0, top)); return out, 300
    return _hat3d_layer_r3(name, col, K, tilt, dx, col2, top, bottom)

# =================================================================== ROUND 4 PROPOSAL (Nov 23 2026, coordinator's Cape Cod vs Rick #10/#14 check)
# Measured on 360 Rick heads (24 videos, frames every 2.5 s) with the same detector run on our library heads:
#   skin: Rick's heads are near-white TINTED BY THE SCENE: per-video median runs from cool blue-white (#05, #21, #24) to peach
#         (#07 252,226,198; #09 246,231,205; #25 253,236,217) and pink (#10 233,204,206; #14 241,227,227); all-video median 243,231,228.
#   lidded/wide eyes: Rick 0.19 of head width wide, ours 0.13  (x1.45);  brows: Rick 0.19 long x 0.058 thick, ours 0.11-0.12 x 0.03-0.05 (x1.6);
#   eye spacing about equal (Rick 0.27-0.28, ours 0.30); walrus moustache about equal (ours 0.42 vs Rick median 0.34 over all moustaches).
# Opt-in so renders in flight are unchanged: cast.json per character  "feat_scale": "rick"  and  "skin": "rick_warm" | "rick_pink" | ...
SKIN = {'rick_neutral': (245, 233, 229), 'rick_warm': (250, 231, 208), 'rick_pink': (240, 216, 214), 'rick_cool': (238, 238, 246), 'rig_white': (251, 244, 241)}
def skin_rgb(v, default):
    if isinstance(v, str): return SKIN.get(v, default)[:3]
    return tuple(v)[:3] if v else tuple(default)[:3]
RICK_SCALE = (1.4, 1.6, 1.3)       # eyes, brows, mouth
def feat_scale(c):
    v = c.get('feat_scale')
    if not v: return None
    if v == 'rick': return RICK_SCALE
    return tuple((list(v) + [1, 1, 1])[:3])
# feature boxes in face-layer coordinates (before the 105 px lift): (centre x, centre y, half size)
EYE_BOXES = [(CX - 108, 520, 110), (CX + 108, 520, 110)]
BROW_BOXES = [(CX - 108, 405, 100), (CX + 108, 405, 100)]   # about the old brow line, so bigger brows grow down, away from the hairline
MOUTH_BOXES = [(CX, 715, 170)]
def scaled(dst, drawfn, boxes, f):
    """draw with drawfn on a scratch layer, then scale each box's content about its own centre (feature spacing unchanged)"""
    lay = Image.new('RGBA', (1024, 1024), CLEAR); drawfn(ImageDraw.Draw(lay))
    if abs(f - 1) < 1e-3: dst.alpha_composite(lay); return
    for bx, by, r in boxes:
        cr = lay.crop((bx - r, by - r, bx + r, by + r)); n = int(2 * r * f); cr = cr.resize((n, n), Image.LANCZOS)
        dst.alpha_composite(cr, (int(bx - n / 2), int(by - n / 2)))
def mouth_set(lay, kind, side, cy=715):
    """Rick's lopsided set for an already drawn mouth layer (same as mouth_layer)"""
    if not side: return lay
    ang = 0 if kind in ('O', 'o', 'sigh', 'shout', 'whistleo') else MOUTH_TILT * side
    lay = lay.rotate(ang, resample=Image.BICUBIC, center=(CX, cy))
    out = Image.new('RGBA', (1024, 1024), CLEAR); out.alpha_composite(lay, (int(MOUTH_SHIFT * side), 0)); return out

# =================================================================== ROUND 5 PROPOSAL (Nov 23 2026, owner asks; awaits owner approval)
# Owner, Nov 23 2026: "when someone has a facial expression that is angled, it remains angled for the whole duration of that said scene ...
# Rick has a great tendency to have a couple of frames where it transitions from an angled facial reference to ... a slightly less angled
# reference, or maybe a symmetrical reference."  Evidence: research/rick-style-spec/face-turns-arms/ (project files).
# Graded turn levels: the face slides toward the side it faces by a level, in units of the round-2 turn (62 px = 7.75 % of the 800 px disc).
#   level 0 front, 1 slight (5 % of disc width), 2 three-quarter (10 %), 3 strong three-quarter (16 %); lookL/lookR stay 7.75 % [level 3 INFERRED
#   from 4 Rick events: #22 f376-379, #24 f414-416, #10 f257-260, #22 f1459-1463].  Negative = left, positive = right.
# Tokens: tq-3 .. tq3 in a face's extras string.  cast.json "turns": "all" or [face names] adds variants name@L3..name@R3 (opt-in).
TURN_UNITS = {0: 0.0, 1: 0.65, 2: 1.3, 3: 2.05}   # = 5 %, 10 %, 16 % of the disc width (Rick measured 6-16 % on #12 f1438-1445, #14 f1255-1260)
def turn_level(ex=''):
    for k in (ex or '').split('+'):
        if k.startswith('tq'):
            try: return max(-3, min(3, int(k[2:])))
            except ValueError: return None
    return None
_turn_dx_r4 = turn_dx
def turn_dx(c, ex=''):
    lv = turn_level(ex)
    if lv is None: return _turn_dx_r4(c, ex)
    return int(round((1 if lv > 0 else -1) * TURN_UNITS[abs(lv)] * 62))
_mouth_side_r4 = mouth_side
def mouth_side(c, ex=''):
    lv = turn_level(ex)
    if lv is None: return _mouth_side_r4(c, ex)
    return 0 if lv == 0 else (1 if lv > 0 else -1)   # Rick: the mouth rides toward the turned side from the slight level on
TOKENS = TOKENS | {f'tq{i}' for i in range(-3, 4)}
def turn_name(base, lv):
    return f"{base}@F" if lv == 0 else f"{base}@{'L' if lv < 0 else 'R'}{abs(lv)}"
_expand_r4 = expand
def expand(C):
    C = _expand_r4(C)
    for n, c in C.items():
        want = c.get('turns')
        if not want: continue
        f = c.setdefault('faces', {})
        bases = [k for k in list(f) if '@' not in k and not k.startswith('talk') and k != 'blink'] if want == 'all' else [k for k in want if k in f]
        for k in bases:
            e, b, m = f[k][:3]; ex = f[k][3] if len(f[k]) > 3 else ''
            ex = '+'.join(t for t in ex.split('+') if t and t not in ('lookL', 'lookR', 'turnL', 'turnR', 'front', 'mouthL', 'mouthR', 'mouthC'))
            for lv in (-3, -2, -1, 0, 1, 2, 3):
                nm = turn_name(k, lv)
                if nm not in f: f[nm] = [e, b, m, (ex + '+' if ex else '') + f'tq{lv}']
        if c.get('blink_turns', True) and 'blink' in f:   # blinks keep the head angle they interrupt
            e, b, m = f['blink'][:3]
            for lv in (-3, -2, -1, 0, 1, 2, 3):
                nm = turn_name('blink', lv)
                if nm not in f: f[nm] = [e, b, m, f'tq{lv}']
    return C
