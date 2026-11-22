# Expression library sheet (rules 329/330): every LIBRARY face on a man and a woman of the rig, beside 2 Rick reference crops,
# plus a page of whole characters (body + arms + head) wearing library faces beside whole Rick frames.
# Usage: python3 exprsheet.py <picks.json> <out_dir>
#   picks.json = {"picks": {name: [ref_png, ref_png]}, "evidence": {name: "text"}, "inferred": {name: "why"}, "whole": [[name, face], ...], "whole_refs": [png, ...]}
# Rick crops live only in project files (research/rick-style-spec/expression-library/), never in this repo.
import sys, json, math
sys.path.insert(0, '/root/det/src')
import cast, expressions as X
from PIL import Image, ImageDraw, ImageFont

BG = (236, 230, 218); INK = (40, 30, 40)
def font(sz):
    for f in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        try: return ImageFont.truetype(f, sz)
        except Exception: pass
    return ImageFont.load_default()

# lib.py geometry (metres): body card 0.8 x 1.001 centred z 0.4605; head card 0.55 centred z 1.061; arm pivots (+-shx, 0.779), arm card 0.677 x 0.508, 0.22 below
GEO = {'tall': 0.141, 'short': 0.156, 'round': 0.165}
def whole(name, fk, S=420):
    c = cast.C[name]; shx = GEO[c.get('body', 'tall')]
    W, H = int(1.5 * S), int(1.45 * S); im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    def put(card, cx, cz, w, h, rot=0):
        t = card.resize((int(w * S), int(h * S)), Image.LANCZOS)
        if rot: t = t.rotate(rot, resample=Image.BICUBIC, expand=False)
        im.alpha_composite(t, (int(W / 2 + cx * S - t.width / 2), int(H - 0.05 * S - cz * S - t.height / 2)))
    put(cast.body(name), 0, 0.4605, 0.8, 1.001)
    a = cast.arm(name)
    for sx in (-1, 1):
        card = a if sx > 0 else a.transpose(Image.FLIP_LEFT_RIGHT)
        put(card, sx * shx, 0.779 - 0.22, 0.677, 0.508, rot=8 * sx)
    put(cast.head(name, fk), 0, 1.061, 0.55, 0.55)
    return im

def page_grid(names, picks, evid, inferred, title, out):
    F1, F2, F3 = font(26), font(17), font(30)
    cw, chh = 4 * 190 + 30, 262; cols = 2; rows = (len(names) + 1) // 2
    sh = Image.new('RGB', (cols * cw + 20, rows * chh + 90), BG); d = ImageDraw.Draw(sh)
    d.text((20, 20), title, fill=INK, font=F3)
    d.text((20, 58), 'each row: our man | our woman | Rick reference A | Rick reference B   (style match only, our own drawings)', fill=(90, 80, 90), font=F2)
    for i, n in enumerate(names):
        x0 = 10 + (i % cols) * cw; y0 = 90 + (i // cols) * chh
        d.rounded_rectangle([x0, y0, x0 + cw - 20, y0 + chh - 10], 14, fill=(250, 247, 240), outline=(200, 190, 180), width=2)
        for j, who in enumerate(('xlib_man', 'xlib_woman')):
            h = cast.head(who, n).resize((180, 180), Image.LANCZOS); sh.paste(h, (x0 + 8 + j * 190, y0 + 40), h)
        for j, p in enumerate(picks.get(n, [])[:2]):
            r = Image.open(p).convert('RGB').resize((180, 180), Image.LANCZOS); sh.paste(r, (x0 + 8 + (2 + j) * 190, y0 + 40))
            d.rectangle([x0 + 8 + (2 + j) * 190, y0 + 40, x0 + 188 + (2 + j) * 190, y0 + 220], outline=(160, 40, 40), width=3)
        e, b, m, x = X.LIBRARY[n]
        d.text((x0 + 10, y0 + 8), n, fill=INK, font=F1)
        d.text((x0 + 250, y0 + 12), f'eyes {e} / brows {b} / mouth {m}' + (f' / {x}' if x else ''), fill=(90, 80, 90), font=F2)
        tag = evid.get(n, '') + ('   [INFERRED: ' + inferred[n] + ']' if n in inferred else '')
        d.text((x0 + 10, y0 + 226), tag[:95], fill=(150, 60, 60) if n in inferred else (60, 110, 60), font=F2)
    sh.save(out, quality=92)

def page_whole(whole_list, refs, out):
    F1, F3 = font(24), font(30)
    n = len(whole_list); S = 420; cw = int(1.5 * S)
    sh = Image.new('RGB', (max(n * cw + 40, 3 * 430 + 40), 700 + 820), BG); d = ImageDraw.Draw(sh)
    d.text((20, 20), 'Whole characters wearing library faces (rule 329: whole bodies, arms included)', fill=INK, font=F3)
    for i, (name, fk) in enumerate(whole_list):
        im = whole(name, fk, S); sh.paste(im, (20 + i * cw, 70), im)
        d.text((40 + i * cw, 70 + im.height), f'{name}: {fk}', fill=INK, font=F1)
    d.text((20, 720), 'Rick reference frames (whole characters, same faces)', fill=INK, font=F3)
    for j, p in enumerate(refs[:6]):
        r = Image.open(p).convert('RGB'); r = r.resize((int(r.width * 760 / r.height), 760), Image.LANCZOS)
        sh.paste(r, (20 + j * (r.width + 10), 760))
    sh.save(out, quality=92)

if __name__ == '__main__':
    P = json.load(open(sys.argv[1])); od = sys.argv[2]
    names = [n for n in X.LIBRARY]
    third = (len(names) + 2) // 3
    for k in range(3):
        page_grid(names[k * third:(k + 1) * third], P['picks'], P.get('evidence', {}), P.get('inferred', {}),
                  f'Rick-style expression library, page {k + 1} of 3 ({len(names)} faces)', f'{od}/expressions_p{k + 1}.jpg')
    page_whole(P['whole'], P['whole_refs'], f'{od}/expressions_whole.jpg')
    print('SHEET_OK', len(names))
