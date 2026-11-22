# Round-2 benchmark sheet (owner Nov 22 5:11 PM CT): off-centre mouths and turned faces, Rick-style facial hair, hairstyles and
# perspective hats, each beside Rick reference crops. Usage: python3 benchsheet.py <refs.json> <ref_dir> <out.jpg>
#   refs.json = {item: [crop_name, ...]}; crops are read from <ref_dir>/<name>.png (Rick crops stay in project files, never in this repo)
import sys, json, os
sys.path.insert(0, '/root/det/src')
import cast, expressions as X
from PIL import Image, ImageDraw, ImageFont

BG = (236, 230, 218); INK = (40, 30, 40)
def font(sz):
    try: return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', sz)
    except Exception: return ImageFont.load_default()

def demo(item):
    """a test character showing one round-2 item; returns (cast.json entry, face key)"""
    base = dict(cast.C['xlib_man']); base.pop('hairdo', None)
    base.update(turn=0.5, mouth_side=1)
    if item in X.FHAIR:
        base.update(fhair=item, fhaircol={'whitebeard': [240, 240, 240], 'walrus': [120, 70, 40], 'fullbeard': [110, 66, 36], 'stubbledots': [80, 70, 80]}.get(item, [34, 28, 30]))
        if item == 'whitebeard': base.update(hairdo='cowlick', hair=[230, 230, 230])
    elif item in X.HAIRDO:
        base.update(hairdo=item, hair={'spiky': [220, 110, 40], 'curly': [210, 110, 50], 'bowl': [120, 70, 40], 'messy': [70, 46, 30]}.get(item, [32, 30, 36]))
    elif item in X.HAT3D:
        base.update(hat3d=item, hat_tilt={'trucker': 12, 'bowler3d': -6, 'tophat3d': 5, 'cowboy3d': -5, 'flatcap3d': -8, 'beanie3d': 6}[item],
                    hatcol={'trucker': [200, 40, 40], 'bowler3d': [40, 40, 48], 'tophat3d': [30, 30, 34], 'cowboy3d': [180, 140, 80], 'flatcap3d': [90, 90, 96], 'beanie3d': [70, 100, 70]}[item], hatcol2=[245, 245, 245])
        if item == 'trucker': base['faces'] = dict(base['faces']); base['faces']['cool_shades'] = ['dot', 'none', 'toothy', 'shades']
    cast.C['_bench'] = base
    return 'cool_shades' if item == 'trucker' else 'smug'

SECTIONS = [('Facial hair (proposed 326a options, owner to pick)', X.FHAIR), ('Hairstyles (proposed, owner to pick)', X.HAIRDO), ('Hats in perspective, tilted', X.HAT3D)]
def main(refs, rdir, out):
    F1, F2, F3 = font(22), font(16), font(30)
    cw, chh, cols = 3 * 170 + 30, 230, 3
    rows = 2 + sum((len(v) + cols - 1) // cols for _, v in SECTIONS)
    H = 80 + rows * chh + 60 * (len(SECTIONS) + 1)
    sh = Image.new('RGB', (cols * cw + 20, H), BG); d = ImageDraw.Draw(sh)
    d.text((20, 20), "Rick benchmark: off-centre mouths, facial hair, hair, angled hats", fill=INK, font=F3)
    d.text((20, 56), 'each cell: ours | Rick A | Rick B (style only; our own drawings)', fill=(90, 80, 90), font=F2)
    y = 90
    # turned faces + off-centre mouths: one character, six faces, turn and mouth side alternate
    d.text((20, y), 'Turned faces and off-centre, lopsided mouths (every face in the library can carry them)', fill=INK, font=F1); y += 34
    for j, (fk, t, ms) in enumerate([('smug', 0.6, 1), ('grin', -0.5, -1), ('laugh', 0.4, 1), ('frown', -0.6, -1), ('surprise', 0.5, 1), ('side_eye', 0.8, 1)]):
        b = dict(cast.C['xlib_man']); b.update(turn=t, mouth_side=ms); cast.C['_bench'] = b
        h = cast.head('_bench', fk).resize((160, 160), Image.LANCZOS); sh.paste(h, (20 + j * 170, y), h)
        d.text((24 + j * 170, y + 162), f'{fk} turn {t:+.1f}', fill=INK, font=F2)
    y += 190
    d.text((20, y), 'Rick:', fill=(160, 40, 40), font=F1)
    for j, r in enumerate(refs.get('turn', [])[:4]):
        im = Image.open(os.path.join(rdir, r + '.png')).convert('RGB').resize((160, 160)); sh.paste(im, (100 + j * 170, y))
        d.rectangle([100 + j * 170, y, 260 + j * 170, y + 160], outline=(160, 40, 40), width=3)
    y += 200
    for title, items in SECTIONS:
        d.text((20, y), title, fill=INK, font=F1); y += 34
        for i, it in enumerate(items):
            x0 = 10 + (i % cols) * cw; y0 = y + (i // cols) * chh
            fk = demo(it); h = cast.head('_bench', fk).resize((160, 160), Image.LANCZOS)
            d.rounded_rectangle([x0, y0, x0 + cw - 20, y0 + chh - 12], 12, fill=(250, 247, 240), outline=(200, 190, 180), width=2)
            sh.paste(h, (x0 + 8, y0 + 30), h); d.text((x0 + 10, y0 + 6), it, fill=INK, font=F1)
            rs = refs.get(it, [])
            for j, r in enumerate(rs[:2]):
                im = Image.open(os.path.join(rdir, r + '.png')).convert('RGB').resize((160, 160)); sh.paste(im, (x0 + 8 + (j + 1) * 170, y0 + 30))
                d.rectangle([x0 + 8 + (j + 1) * 170, y0 + 30, x0 + 168 + (j + 1) * 170, y0 + 190], outline=(160, 40, 40), width=3)
            if not rs: d.text((x0 + 190, y0 + 100), '[INFERRED] no clear Rick frame', fill=(150, 60, 60), font=F2)
        y += ((len(items) + cols - 1) // cols) * chh + 20
    sh = sh.crop((0, 0, sh.width, y + 10)); sh.save(out, quality=92); print('BENCH_OK', out)

if __name__ == '__main__':
    main(json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3])
