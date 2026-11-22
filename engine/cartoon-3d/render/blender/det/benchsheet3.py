# Round-3 benchmark sheet (owner Nov 22 5:28 PM CT review of round 2): redrawn goatee/king/full beard, redrawn hairstyles, hats with no hair
# above the brim, and more turned / lopsided / tilted faces, each beside Rick reference crops.
# Usage: python3 benchsheet3.py <ref_dir> <out.jpg>   (crops <ref_dir>/<name>.png stay in project files, never in this repo)
import sys, os
sys.path.insert(0, '/root/det/src')
import cast, expressions as X
from PIL import Image, ImageDraw, ImageFont

BG = (236, 230, 218); INK = (40, 30, 40); RED = (160, 40, 40); GRN = (50, 110, 60)
def font(sz):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', sz)
    except Exception: return ImageFont.load_default()
F1, F2, F3 = font(22), font(16), font(32)

def head(cfg, fk, S):
    b = dict(cast.C['xlib_man']); b.pop('hairdo', None); b.update(cfg); cast.C['_bench'] = b
    h = cast.head('_bench', fk); pt, pb = X.pads(b); k = S / 1024
    return h.resize((S, int(h.height * k)), Image.LANCZOS), int((pt + 540) * k)

def put_head(sh, cfg, fk, x, cy, S):
    h, oy = head(cfg, fk, S); sh.paste(h, (x, cy - oy), h)

def put_ref(sh, d, rdir, name, x, y, S):
    im = Image.open(os.path.join(rdir, name + '.png')).convert('RGB').resize((S, S), Image.LANCZOS); sh.paste(im, (x, y))
    d.rectangle([x, y, x + S, y + S], outline=RED, width=3)

HAIRS = {'bowl': [120, 70, 40], 'bangs': [34, 28, 36], 'spiky': [220, 110, 40], 'curly': [190, 85, 45], 'cowlick': [120, 72, 42], 'messy': [96, 62, 38],
         'sidepart': [32, 30, 36], 'topknot': [32, 30, 36]}
TURNS = [  # (label, cfg, face)
    ('lookR smug', dict(hairdo='bowl', hair=HAIRS['bowl']), 'smug', 'lookR'),
    ('lookL grin', dict(hairdo='messy', hair=HAIRS['messy']), 'grin', 'lookL'),
    ('tiltL side_eye', dict(hairdo='bangs', hair=HAIRS['bangs']), 'side_eye', 'lookR+tiltL'),
    ('tiltR angry', dict(hairdo='spiky', hair=HAIRS['spiky']), 'angry', 'lookL+tiltR'),
    ('mouthR laugh', dict(hairdo='curly', hair=HAIRS['curly']), 'laugh', 'turnL+mouthR'),
    ('lookR newsboy', dict(hat3d='flatcap3d', hatcol=[50, 80, 150], hatcol2=[235, 235, 240], hat_tilt=-8, hairdo='bowl', hair=HAIRS['bowl']), 'deadpan', 'lookR+tiltR'),
    ('lookL cowlick', dict(hairdo='cowlick', hair=HAIRS['cowlick']), 'happy', 'lookL'),
    ('tiltL goatee', dict(hairdo='sidepart', hair=HAIRS['sidepart'], fhair='goatee', fhaircol=[30, 26, 30]), 'skeptical', 'lookR+tiltL'),
    ('lookR bowler', dict(hat3d='bowler3d', hatcol=[40, 40, 48], hat_tilt=-7, hairdo='messy', hair=HAIRS['messy']), 'stern', 'lookR'),
    ('lookL trucker', dict(hat3d='trucker', hatcol=[205, 50, 50], hatcol2=[245, 245, 245], hat_tilt=10, hairdo='bowl', hair=HAIRS['bowl']), 'smug_grin', 'lookL+tiltR'),
    ('mouthL worried', dict(hairdo='bangs', hair=[90, 56, 34]), 'worried', 'turnR+mouthL'),
    ('lookR tophat', dict(hat3d='tophat3d', hatcol=[240, 236, 228], hat_tilt=5, hairdo='bowl', hair=[60, 40, 30], fhair='curled', fhaircol=[40, 30, 30]), 'happy', 'lookR'),
]
TURN_REFS = ['01_004_0', '22_009_0', '05_011_0', '25_014_0', '03_001_0', '24_006_1', '22_020_1', '09_018_0', '21_017_1', '05_005_0', '16_007_0', '25_024_1']
FH = [('goatee', dict(fhair='goatee', fhaircol=[30, 26, 30], hairdo='sidepart', hair=[30, 26, 30]), 'open_smile', ['25_006_0', '25_007_0']),
      ('king', dict(fhair='king', fhaircol=[120, 70, 40], hairdo='bowl', hair=[120, 70, 40]), 'content', ['17_001_1', '17_017_0']),
      ('fullbeard', dict(fhair='fullbeard', fhaircol=[96, 58, 34], hairdo='bangs', hair=[30, 26, 30]), 'laugh', ['22_005_0', '22_020_0'])]
HD = [('bowl', 'grin', ['09_010_0', '09_018_0']), ('bangs', 'smug', ['12_018_0', '12_020_0']), ('spiky', 'surprise', ['08_020_0', '08_017_1']),
      ('curly', 'happy', ['02_008_1', '22_027_0']), ('cowlick', 'grin', ['11_016_0', '13_005_0']), ('messy', 'smug', ['13_019_1', '13_020_0'])]
HATS = [('tophat3d', dict(hat3d='tophat3d', hatcol=[240, 236, 228], hat_tilt=5, hairdo='bowl', hair=[60, 40, 30], fhair='curled', fhaircol=[40, 30, 30]), 'happy', ['23_009_1', '23_010_0']),
        ('cowboy3d', dict(hat3d='cowboy3d', hatcol=[205, 170, 110], hat_tilt=-4, hairdo='messy', hair=HAIRS['messy'], fhair='chevron', fhaircol=[34, 28, 30]), 'deadpan', ['07_009_0', '07_010_0']),
        ('flatcap3d', dict(hat3d='flatcap3d', hatcol=[50, 80, 150], hatcol2=[235, 235, 240], hat_tilt=-8, hairdo='bowl', hair=HAIRS['bowl']), 'smug', ['03_001_0', '03_023_0']),
        ('trucker', dict(hat3d='trucker', hatcol=[205, 50, 50], hatcol2=[245, 245, 245], hat_tilt=10, hairdo='bowl', hair=HAIRS['bowl']), 'smug_grin', ['24_008_1', '24_015_0']),
        ('bowler3d', dict(hat3d='bowler3d', hatcol=[40, 40, 48], hat_tilt=-7, hairdo='spiky', hair=HAIRS['spiky']), 'stern', ['03_006_0', '23_011_0'])]

def with_tok(cfg, fk, tok):
    # put a per-face token on a throwaway face key
    b = dict(cfg); faces = dict(cast.C['xlib_man'].get('faces', {})); rec = list(cast.C['xlib_man']['faces'][fk]) if fk in cast.C['xlib_man']['faces'] else None
    return b, rec

def main(rdir, out):
    S = 200; cw = 3 * (S + 12) + 16; cols = 3; chh = int(S * 1.55) + 44
    W = cols * cw + 20
    blocks_h = 90 + (2 * int(S * 1.5) + 60) + (2 * (S + 30) + 40) + 3 * 60 + 60 + 60 \
        + (1 * chh) + 120 + (2 * chh) + 60 + (2 * chh) + 60 + 140
    sh = Image.new('RGB', (W, blocks_h), BG); d = ImageDraw.Draw(sh)
    d.text((20, 18), 'Rick benchmark, round 3: redrawn beards, hair and hats, more turned faces', fill=INK, font=F3)
    d.text((20, 58), 'ours first, then Rick frames in red frames (style only; every drawing is our own code)', fill=(90, 80, 90), font=F2)
    y = 96
    # A. turned faces
    d.text((20, y), 'Turned faces, lopsided mouths and head tilts (new per-face tokens: lookL/lookR, mouthL/mouthR, tiltL/tiltR)', fill=INK, font=F1); y += 36
    lib = X.LIBRARY
    for i, (lab, cfg, fk, tok) in enumerate(TURNS):
        e, b_, m, xx = lib[fk]; c = dict(cfg); c['faces'] = {fk: [e, b_, m, (xx + '+' if xx else '') + tok]}; c['library'] = []
        x = 20 + (i % 6) * (W - 40) // 6; cy = y + int(S * 0.62) + (i // 6) * int(S * 1.5)
        b = dict(cast.C['xlib_man']); b.pop('hairdo', None); b.update(c); cast.C['_bench'] = b
        h = cast.head('_bench', fk); pt, pb = X.pads(b); k = S / 1024; h = h.resize((S, int(h.height * k)), Image.LANCZOS)
        sh.paste(h, (x, cy - int((pt + 540) * k)), h); d.text((x + 6, cy + int(S * 0.5)), lab, fill=INK, font=F2)
    y += 2 * int(S * 1.5) + 20
    d.text((20, y), 'Rick:', fill=RED, font=F1); y += 32
    for j, r in enumerate(TURN_REFS):
        put_ref(sh, d, rdir, r, 20 + (j % 6) * (W - 40) // 6, y + (j // 6) * (S + 30), S)
    y += 2 * (S + 30) + 30
    def section(title, items, note=None):
        nonlocal y
        d.text((20, y), title, fill=INK, font=F1); y += 34
        if note: d.text((20, y), note, fill=GRN, font=F2); y += 26
        for i, (name, cfg, fk, refs) in enumerate(items):
            x0 = 10 + (i % cols) * cw; y0 = y + (i // cols) * chh
            d.rounded_rectangle([x0, y0, x0 + cw - 12, y0 + chh - 10], 12, fill=(250, 247, 240), outline=(200, 190, 180), width=2)
            d.text((x0 + 10, y0 + 6), name, fill=INK, font=F1)
            put_head(sh, cfg, fk, x0 + 8, y0 + 36 + int(S * 0.75), S)
            for j, r in enumerate(refs[:2]): put_ref(sh, d, rdir, r, x0 + 8 + (j + 1) * (S + 12), y0 + 36 + int(S * 0.75) - S // 2, S)
        y += ((len(items) + cols - 1) // cols) * chh + 16
    section('Facial hair, redrawn: goatee and king hang past the chin; full beard benchmarked on Rick\'s bearded soldier', FH,
            'Approved and unchanged: pencil, chevron, curled, walrus, toothbrush, droop, whitebeard, stubbledots.   Removed: sideburns.')
    section('Hairstyles, redrawn as closer copies of Rick', [(n, dict(hairdo=n, hair=HAIRS[n]), fk, refs) for n, fk, refs in HD],
            'Approved and unchanged: sidepart, topknot.   Removed: afro.')
    section('Hats, redrawn: each one is worn over a full head of hair, and nothing shows above the brim', HATS,
            'Approved and unchanged: beanie3d.')
    sh = sh.crop((0, 0, W, y + 10)); sh.save(out, quality=92); print('BENCH3_OK', out)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
