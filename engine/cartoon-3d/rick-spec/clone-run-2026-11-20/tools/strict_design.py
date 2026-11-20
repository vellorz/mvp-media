#!/usr/bin/env python3
"""strict_design.py - strict, reproducible per-shot design measurements.

Implements the binding definitions in
new-analysis/_agent-prompts/verify-definitions.md.

All caption/head measures run on FULL-RES 1080x1920 frames extracted by ffmpeg
(exact frame index via the select filter, frame n is 1-based).
Camera runs on the 540x960 frame dumps /root/work/VID/f/NNNN.jpg.

CLI
  strict_design.py extract VID N [N ...]            -> cache full-res PNGs
  strict_design.py cap     VID N [--debug out.png]  -> caption cap height
  strict_design.py head    VID N x0 y0 x1 y1 [--debug out.png] [--exclude left,right,top]
      (full-res bbox; --exclude marks a scan unclean after the analyst SAW in
       the debug image that it lies on hair/shadow/another object; the tool
       never accepts a typed-in number)
  strict_design.py zoom    VID OUT.png N:x0,y0,x1,y1 [N:x0,y0,x1,y1 ...]
      (4x crops centred on every scan start point, for the visual check)
  strict_design.py camera  VID A B [--series]
  strict_design.py luma    VID N

Library: cap_height(img), head_measure(img, bbox), camera(vid, a, b),
mean_luma(img), get_frame(vid, n).

Analyst conventions used with this tool (first applied to #22 and #24)
- Choose the LARGEST real head by looking (never a far crowd if a nearer
  character exists); measure several candidates and keep the largest fill.
- Always view the debug image AND the zoom crops. Mark a scan --exclude when
  you SEE that it: lies on dark or coloured headwear (cap band, helmet rim,
  hat brim), on hair (incl. the corner of a hairline/sideburn notch), on a
  helmet cheek flap, on an adjacent character's outline, or on a caption.
  A top scan on a LIGHT headband/cap underside line (light on both sides of
  the stroke) is kept. Never type a number in.
- A caption whose only ascender is 'f' (or that reads 'no ascender') is
  replaced by the nearest caption event inside the shot that has a capital or
  h,t,l,k,b,d.

Method details (fixed, do not tune per frame)
- Luma = Rec.709 on gamma-encoded RGB (0.2126 R + 0.7152 G + 0.0722 B).
- cap_height: band 62-80 % H. Glyph = connected component of luma > 128
  (midpoint of white fill ~250 and outline ~10) whose 1-px..6-px surrounding
  ring is >= 70 % dark (luma < 100), whose mean HSV saturation is <= 40 and
  whose median luma is >= 215 (caption white is pure and neutral). Height 12-110 px. Line = glyphs whose bottom is within
  the dominant bottom cluster (+/- 6 px) or that straddle it (descenders).
  Marks (< 0.55 x median height: dots, commas, apostrophes) are dropped.
  Baseline = last row whose glyph-fill pixel count is >= 40 % of the peak
  row of the line's fill profile (the x-band carries most fill); descenders (bottom > baseline + 6 px) are excluded from
  the height classes.
  x-height ref = height of the shortest non-descender glyph (after dropping
  marks < 0.55 x median). Ascender/capital class = non-descender glyphs taller
  than 1.15 x x-height ref (if every glyph is an ascender the frame reads as
  'no ascender' and a neighbouring caption is used). cap height = median of the tallest third
  (ceil(n/3)) of the non-descender glyphs, restricted to the ascender class.
  If the ascender class is empty -> "no ascender".
  Note: 'f' has a round top that overshoots h/d/t/capitals by ~3 px; the
  definitions list capitals and h,t,l,k,b,d, so a caption whose only
  ascender is 'f' should be replaced by a neighbouring caption (caller's job,
  the glyph identity is not known to the tool).
  Height = last fill row - first fill row + 1 (white-fill only).
- head_measure: bbox = approximate head box (full-res px), supplied by eye.
  Fill = bright (luma > fill_thr) pixels whose Lab chroma (a*, b*) is within
  25 of the median chroma of the bright bbox-centre pixels, eroded 3 px
  (7x7) before labelling and grown back 3 px inside the raw mask; the component with the largest overlap with the
  central 50 % of the bbox, searched inside the bbox grown by 20 %; holes
  (eyes, mouth) filled. fill_thr = 0.5*(p90 luma inside bbox centre + 40).
  If the fill touches the grown-box border the result is flagged 'leak'.
  Fill width = widest row of the filled component (global).
  Cheek scan row = widest row within the 30-80 % band of the fill height.
  Scans (3 lines averaged, 1 px apart, perpendicular to the edge):
    left cheek / right cheek: horizontal, on the widest fill row;
    top: vertical, on the fill's centre column; each starts 12 px inside the
    fill edge and runs outward.
  Per scan: L_fill = median luma of the 10 px from 12 to 3 px inside the
  edge; the outward window starts 2 px inside the edge; L_dark = min luma in the
  first 40 % of the outward window; mid = (L_fill + L_dark) / 2; outline =
  count of contiguous pixels with luma < mid from the first crossing.
  Clean only if: L_fill >= fill_thr; contrast L_fill - L_dark >= 60; the run starts <= 6 px
  outside the fill edge; for runs >= 4 px, fewer than 3 inner run pixels
  differ by > 35 (RGB distance) from the run's median colour (an ink line is
  one colour; brown hair / coloured shadow / another object is not); the dark run ends inside the
  window; within 6 px after the run the luma rises back above mid
  (otherwise the line touches hair / shadow / a dark object); the run does not
  reach the frame edge; run <= 12 % of fill width (outline is ~2-5 % of head width; longer runs
  are hats/hair/shadow).
  Outline = median of clean scans; < 2 clean -> "unreadable".
  Outer width = fill width + left cheek run + right cheek run (outer edge of
  each run measured from the fill edge) when both cheek scans are clean, else fill width + 2 x outline median
  ("derived"), else fill width only.
- camera: 540 w frames. Per pair (n, n+1): Shi-Tomasi points (max 1500,
  q 0.005, min dist 7) outside the caption band (rows 62-80 % H), LK pyramidal
  flow with forward-backward check (< 0.7 px). Pass 1 RANSAC similarity
  (estimateAffinePartial2D, thr 1.0 px) on all points; outliers with residual
  > 1.5 px are rasterised, dilated 25 px, and the LARGEST connected blob is the
  moving foreground object; pass 2 refits on points outside that blob and
  outside the caption band. Background speed = median displacement magnitude
  of the pass-2 model evaluated at its RANSAC inlier points (captures pan +
  zoom + roll where the background actually is; no extrapolation to corners). Cross-checks: |median flow| of points in the top third and of points
  in the outer 15 % side strips (pass-2 inliers not required).
  Speed series value for pair (n,n+1) is assigned to frame n+1.
  fast move = run of speed > 2 px/f, >= 3 frames, runs merged when < 5 frames
  apart. all moves = fast moves + drifts, where drifts = pieces of the
  (> 0.3 px/f, merged when < 5 f apart) mask left after removing the fast
  moves, each piece >= 8 frames counting once. static run = consecutive frames
  with speed < 0.3; longest reported in frames; static_gt45 = longest > 45.
"""
import os, sys, json, math, subprocess, tempfile
import numpy as np
import cv2
from scipy import ndimage as ndi

ROOT = '/root/work'
CACHE = '/root/work/strict'
W, H = 1080, 1920


# ---------------------------------------------------------------- frames
def _cache_path(vid, n):
    return os.path.join(CACHE, vid, 'full_%04d.png' % n)


def extract(vid, ns):
    ns = sorted(set(int(n) for n in ns))
    todo = [n for n in ns if not os.path.exists(_cache_path(vid, n))]
    if not todo:
        return
    os.makedirs(os.path.join(CACHE, vid), exist_ok=True)
    expr = '+'.join('eq(n\\,%d)' % (n - 1) for n in todo)
    tdir = tempfile.mkdtemp(dir=os.path.join(CACHE, vid))   # private dir: safe for parallel calls
    tmp = os.path.join(tdir, '_tmp_%03d.png')
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', os.path.join(ROOT, 'vid', vid + '.mp4'),
                    '-vf', "select='%s'" % expr, '-vsync', '0', '-start_number', '0', tmp], check=True)
    for i, n in enumerate(todo):
        os.replace(tmp % i, _cache_path(vid, n))
    os.rmdir(tdir)


def get_frame(vid, n):
    p = _cache_path(vid, n)
    if not os.path.exists(p):
        extract(vid, [n])
    img = cv2.imread(p)
    assert img is not None and img.shape[:2] == (H, W), p
    return img


def luma709(img):
    b, g, r = [img[..., i].astype(np.float32) for i in range(3)]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def mean_luma(img):
    return float(luma709(img).mean() / 255.0)


# ---------------------------------------------------------------- caption
def cap_height(img, debug=None):
    h, w = img.shape[:2]
    y0, y1 = int(0.62 * h), int(0.80 * h)
    band = img[y0:y1]
    L = luma709(band)
    hsv = cv2.cvtColor(band, cv2.COLOR_BGR2HSV)
    sat = hsv[..., 1].astype(np.float32)
    bright = (L > 128).astype(np.uint8)
    dark = L < 100
    n, lab, st, cen = cv2.connectedComponentsWithStats(bright, 8)
    glyphs = []
    for i in range(1, n):
        x, y, bw, bh, area = st[i]
        if bh < 12 or bh > 110 or bw > 400 or area < 40:
            continue
        if x == 0 or y == 0 or x + bw >= w or y + bh >= band.shape[0]:
            continue
        m = (lab[max(0, y - 8):y + bh + 8, max(0, x - 8):x + bw + 8] == i).astype(np.uint8)
        d6 = cv2.dilate(m, np.ones((13, 13), np.uint8))
        d1 = cv2.dilate(m, np.ones((3, 3), np.uint8))
        ring = (d6 > 0) & (d1 == 0)
        dk = dark[max(0, y - 8):y + bh + 8, max(0, x - 8):x + bw + 8][ring]
        if dk.size == 0 or dk.mean() < 0.70:
            continue
        pix = lab == i
        if sat[pix].mean() > 40 or np.median(L[pix]) < 215:
            continue
        glyphs.append(dict(id=i, x=int(x), top=int(y + y0), bot=int(y + y0 + bh - 1), h=int(bh), w=int(bw), area=int(area)))
    res = dict(glyph_count=0, cap_height_px=None, baseline_y=None, baseline_pct=None, status='no caption')
    if len(glyphs) < 1:
        _cap_debug(img, debug, glyphs, res)
        return res
    # dominant line: cluster bottoms
    bots = np.array([g['bot'] for g in glyphs])
    best = max(bots, key=lambda b: ((np.abs(bots - b) <= 6).sum(), -abs(b - 0.716 * h)))
    line = [g for g in glyphs if abs(g['bot'] - best) <= 6 or (g['top'] < best - 10 and g['bot'] > best and g['bot'] - best <= 30)]
    # drop tiny marks (dots, commas, apostrophes)
    medh = np.median([g['h'] for g in line])
    letters = [g for g in line if g['h'] >= 0.55 * medh]
    if not letters:
        letters = line
    # baseline from the row profile of the glyph fill: last row whose white
    # count is >= 40 % of the peak row (the x-band carries most of the fill;
    # descenders and commas add little below the baseline)
    rc = np.zeros(h, np.int64)
    for g in line:
        m = (lab[g['top'] - y0:g['bot'] - y0 + 1, g['x']:g['x'] + g['w']] == g['id'])
        rc[g['top']:g['bot'] + 1] += m.sum(1)
    base = int(np.where(rc >= 0.4 * rc.max())[0].max())
    nondesc = [g for g in letters if g['bot'] <= base + 6]
    for g in line:
        g['cls'] = 'desc' if g['bot'] > base + 6 else 'x'
    res.update(glyph_count=len(line), baseline_y=base, baseline_pct=round(100.0 * base / h, 2))
    if not nondesc:
        res['status'] = 'no glyphs'
        _cap_debug(img, debug, line, res)
        return res
    hs = np.array([g['h'] for g in nondesc])
    xref = float(hs.min())
    asc = [g for g in nondesc if g['h'] > 1.15 * xref]
    for g in asc:
        g['cls'] = 'asc'
    res['x_height_ref_px'] = int(xref)
    if not asc:
        res['status'] = 'no ascender'
        _cap_debug(img, debug, line, res)
        return res
    k = int(math.ceil(len(nondesc) / 3.0))
    top = sorted(nondesc, key=lambda g: -g['h'])[:k]
    top = [g for g in top if g in asc]
    res['cap_height_px'] = float(np.median([g['h'] for g in top]))
    res['tallest_third_heights'] = [g['h'] for g in top]
    res['ascender_count'] = len(asc)
    res['status'] = 'ok'
    _cap_debug(img, debug, line, res)
    return res


def _cap_debug(img, path, glyphs, res):
    if not path:
        return
    h = img.shape[0]
    y0, y1 = int(0.62 * h), int(0.80 * h)
    vis = img[y0:y1].copy()
    col = {'asc': (0, 0, 255), 'x': (0, 200, 0), 'desc': (255, 0, 0)}
    for g in glyphs:
        cv2.rectangle(vis, (g['x'], g['top'] - y0), (g['x'] + g['w'] - 1, g['bot'] - y0), col.get(g.get('cls'), (0, 255, 255)), 1)
    if res.get('baseline_y'):
        cv2.line(vis, (0, res['baseline_y'] - y0), (vis.shape[1], res['baseline_y'] - y0), (255, 0, 255), 1)
    cv2.putText(vis, 'cap %s base %s' % (res.get('cap_height_px'), res.get('baseline_y')), (10, 30), 0, 1, (0, 255, 255), 2)
    cv2.imwrite(path, vis)


# ---------------------------------------------------------------- head
def _profile(L, x, y, dx, dy, inside, outside):
    """3-line averaged profile from inside the fill going outward along (dx,dy)."""
    hh, ww = L.shape
    px, py = (-dy, dx)  # perpendicular offset for the 3 parallel lines
    vals, edge_hit = [], False
    for t in range(-inside, outside):
        acc = []
        for o in (-1, 0, 1):
            xx, yy = x + dx * t + px * o, y + dy * t + py * o
            if 0 <= xx < ww and 0 <= yy < hh:
                acc.append(L[yy, xx])
        if len(acc) < 3:
            edge_hit = True
            break
        vals.append(np.mean(acc))
    return np.array(vals, np.float32), edge_hit


def _measure_scan(L, x, y, dx, dy, fillw, img=None, fill_thr=0):
    inside = 12
    outside = int(max(30, min(120, 0.35 * fillw)))
    prof, edge_hit = _profile(L, x, y, dx, dy, inside, outside)
    out = dict(x=int(x), y=int(y), dx=dx, dy=dy, clean=False, px=None, why='')
    if len(prof) < inside + 10:
        out['why'] = 'frame edge'
        return out
    Lf = float(np.median(prof[:inside - 2]))
    win = prof[inside - 2:]
    head_part = win[:max(6, int(0.4 * len(win)))]
    Ld = float(head_part.min())
    mid = 0.5 * (Lf + Ld)
    out.update(L_fill=round(Lf, 1), L_dark=round(Ld, 1), mid=round(mid, 1))
    below = np.where(win < mid)[0]
    if Lf < fill_thr:
        out['why'] = 'inside of scan is not head fill'
        return out
    if Lf - Ld < 60:
        out['why'] = 'low contrast'
        return out
    s = int(below[0])
    e = s
    while e + 1 < len(win) and win[e + 1] < mid:
        e += 1
    run = e - s + 1
    out['px'] = int(run)
    out['run_start'] = int(s - 2)   # t of first dark px; scan origin t=0 is the fill edge pixel
    out['outer_t'] = int(e - 2)     # t of last dark px
    if s - 2 > 6:
        out['why'] = 'dark run starts > 6 px outside the fill edge'
        return out
    if e + 1 >= len(win):
        out['why'] = 'run hits window end' + (' / frame edge' if edge_hit else '')
        return out
    after = win[e + 1:e + 7]
    if after.max() <= mid:
        out['why'] = 'no rise after run (touches dark object/hair/shadow)'
        return out
    if img is not None and run >= 4:
        # colour-consistency: an ink line is one colour; hair/shadow/other
        # dark objects inside the run show up as a colour change.
        cols = []
        for t in range(s - 2, e - 1):
            xx, yy = x + dx * t, y + dy * t
            cols.append(img[yy, xx].astype(np.float32))
        cols = np.array(cols)
        core = cols[1:-1] if len(cols) > 3 else cols   # skip the 1-px ringing edges
        med = np.median(core, 0)
        dist = np.linalg.norm(core - med, axis=1)
        out['run_rgb_median'] = [int(v) for v in med[::-1]]
        if (dist > 35).sum() >= 3:
            out['why'] = 'colour change inside run (hair/shadow/other object)'
            return out
    if run > 0.12 * fillw:
        out['why'] = 'run too long'
        return out
    out['clean'] = True
    return out


def head_measure(img, bbox, debug=None, exclude=()):
    x0, y0, x1, y1 = [int(v) for v in bbox]
    hh, ww = img.shape[:2]
    L = luma709(img)
    gx, gy = int(0.2 * (x1 - x0)), int(0.2 * (y1 - y0))
    X0, Y0, X1, Y1 = max(0, x0 - gx), max(0, y0 - gy), min(ww, x1 + gx), min(hh, y1 + gy)
    sub = L[Y0:Y1, X0:X1]
    cx0, cx1 = x0 + (x1 - x0) // 4 - X0, x1 - (x1 - x0) // 4 - X0
    cy0, cy1 = y0 + (y1 - y0) // 4 - Y0, y1 - (y1 - y0) // 4 - Y0
    p90 = float(np.percentile(sub[cy0:cy1, cx0:cx1], 90))
    thr = 0.5 * (p90 + 40)
    # colour gate: fill = bright AND chroma (a*, b*) within 25 of the median
    # chroma of the bright centre pixels (keeps red cap bands, coloured hats
    # and saturated backgrounds out of the head fill)
    labc = cv2.cvtColor(img[Y0:Y1, X0:X1], cv2.COLOR_BGR2LAB).astype(np.float32)
    ab = labc[..., 1:]
    cmask = sub[cy0:cy1, cx0:cx1] > thr
    ref = np.median(ab[cy0:cy1, cx0:cx1][cmask], 0) if cmask.any() else np.array([128, 128], np.float32)
    chroma_ok = np.linalg.norm(ab - ref, axis=2) < 25
    bright_raw = (sub > thr) & chroma_ok
    # erode 3 px before labelling so thin bright bridges (cap seams, antialias
    # gaps in an outline) do not join the face to a white cap/helmet; the
    # chosen component is grown back by 3 px inside the raw mask
    bright = ndi.binary_erosion(bright_raw, structure=np.ones((7, 7), bool))
    lab, n = ndi.label(bright)
    if n == 0:
        return dict(status='no fill found')
    cen = lab[cy0:cy1, cx0:cx1]
    counts = np.bincount(cen.ravel(), minlength=n + 1)
    counts[0] = 0
    k = int(counts.argmax())
    comp = ndi.binary_dilation(lab == k, structure=np.ones((7, 7), bool)) & bright_raw
    comp = ndi.binary_fill_holes(comp)
    leak = bool(comp[0, :].any() or comp[-1, :].any() or comp[:, 0].any() or comp[:, -1].any())
    rows = np.where(comp.any(1))[0]
    best_w, best_r, lr = -1, None, None
    widths = []
    for r in rows:
        xs = np.where(comp[r])[0]
        widths.append((xs[-1] - xs[0] + 1, r, xs[0], xs[-1]))
    widths.sort(key=lambda t: -t[0])
    # widest row: take the median row among rows within 1 px of max width
    fw = widths[0][0]                       # fill-only width = global widest row
    gr = widths[0][1]
    # cheek scan row: widest row inside the 30-80 % band of the fill height
    # (keeps the scan off helmet/hat rims and off the chin)
    r0, r1 = rows[0], rows[-1]
    lo, hi = r0 + 0.30 * (r1 - r0), r0 + 0.80 * (r1 - r0)
    band = [t for t in widths if lo <= t[1] <= hi] or widths
    mxb = max(t[0] for t in band)
    cand = sorted([t for t in band if t[0] >= mxb - 1], key=lambda t: t[1])
    cw, r, xl, xr = cand[len(cand) // 2]
    cols = np.where(comp.any(0))[0]
    ccol = int(round(np.mean(np.where(comp)[1])))
    toprow = int(np.where(comp[:, ccol])[0][0]) if comp[:, ccol].any() else int(rows[0])
    R, XL, XR, CC, TR = r + Y0, xl + X0, xr + X0, ccol + X0, toprow + Y0
    scans = {
        'left': _measure_scan(L, XL, R, -1, 0, fw, img, thr),
        'right': _measure_scan(L, XR, R, 1, 0, fw, img, thr),
        'top': _measure_scan(L, CC, TR, 0, -1, fw, img, thr),
    }
    for k in exclude:
        scans[k]['clean'] = False
        scans[k]['why'] = 'excluded by analyst on visual check (' + scans[k]['why'] + ')'
    clean = [s['px'] for s in scans.values() if s['clean']]
    res = dict(bbox=[x0, y0, x1, y1], fill_thr=round(thr, 1), fill_px=int(fw),
               fill_pctW=round(100.0 * fw / ww, 2), widest_row_y=int(gr + Y0),
               cheek_row_y=int(R), cheek_row_fill_px=int(cw),
               fill_x=[int(XL), int(XR)], leak=leak,
               scans_px=[s['px'] if s['clean'] else None for s in scans.values()],
               scans=scans)
    if len(clean) >= 2:
        res['outline_px'] = float(np.median(clean))
    else:
        res['outline_px'] = 'unreadable'
    sl, sr = scans['left'], scans['right']
    if sl['clean'] and sr['clean']:
        outer = fw + (sl['outer_t'] + 1) + (sr['outer_t'] + 1)
        res['outer_method'] = 'fill width + left and right cheek runs'
    elif isinstance(res['outline_px'], float):
        outer = fw + 2 * res['outline_px']
        res['outer_method'] = 'derived fill+2*outline'
    else:
        outer = fw
        res['outer_method'] = 'fill only (outline unreadable)'
    res['outer_px'] = int(round(outer))
    res['outer_pctW'] = round(100.0 * outer / ww, 2)
    res['status'] = 'leak' if leak else 'ok'
    if debug:
        vis = img.copy()
        m = np.zeros(L.shape, np.uint8)
        m[Y0:Y1, X0:X1] = comp.astype(np.uint8)
        cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(vis, cnts, -1, (0, 255, 0), 1)
        cv2.rectangle(vis, (x0, y0), (x1, y1), (255, 255, 0), 2)
        cv2.rectangle(vis, (X0, Y0), (X1 - 1, Y1 - 1), (255, 0, 255), 1)
        for name, s in scans.items():
            c = (0, 0, 255) if s['clean'] else (0, 165, 255)
            t_end = s.get('outer_t', 30) or 30
            p0 = (s['x'], s['y'])
            p1 = (s['x'] + s['dx'] * (t_end + 1), s['y'] + s['dy'] * (t_end + 1))
            cv2.line(vis, p0, p1, c, 1)
            cv2.putText(vis, '%s %s' % (name, s['px']), (p1[0] + 4, p1[1] - 4), 0, 0.7, c, 2)
        pad = 40
        cy = vis[max(0, Y0 - pad):min(hh, Y1 + pad), max(0, X0 - pad):min(ww, X1 + pad)]
        sc = max(1, int(700 / max(cy.shape[:2])))
        cy = cv2.resize(cy, None, fx=sc, fy=sc, interpolation=cv2.INTER_NEAREST)
        cv2.putText(cy, 'fill %d outer %d ol %s' % (fw, res['outer_px'], res['outline_px']), (10, 30), 0, 0.9, (0, 255, 255), 2)
        cv2.imwrite(debug, cy)
    return res


# ---------------------------------------------------------------- camera
def _small(vid, n):
    p = os.path.join(ROOT, vid, 'f', '%04d.jpg' % n)
    im = cv2.imread(p, cv2.IMREAD_GRAYSCALE)
    assert im is not None, p
    return im


def _pair_motion(g0, g1):
    h, w = g0.shape
    cy0, cy1 = int(0.62 * h), int(0.80 * h)
    mask = np.full((h, w), 255, np.uint8)
    mask[cy0:cy1] = 0
    p0 = cv2.goodFeaturesToTrack(g0, 1500, 0.005, 7, mask=mask)
    out = dict(speed=None, top=None, sides=None, n=0, fg_frac=0.0)
    if p0 is None or len(p0) < 12:
        return out
    lk = dict(winSize=(21, 21), maxLevel=4, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))
    p1, s1, _ = cv2.calcOpticalFlowPyrLK(g0, g1, p0, None, **lk)
    pb, s2, _ = cv2.calcOpticalFlowPyrLK(g1, g0, p1, None, **lk)
    ok = (s1.ravel() == 1) & (s2.ravel() == 1) & (np.linalg.norm((pb - p0).reshape(-1, 2), axis=1) < 0.7)
    a, b = p0.reshape(-1, 2)[ok], p1.reshape(-1, 2)[ok]
    if len(a) < 12:
        return out
    flow = b - a
    top = a[:, 1] < h / 3
    side = (a[:, 0] < 0.15 * w) | (a[:, 0] > 0.85 * w)
    out['top'] = float(np.linalg.norm(np.median(flow[top], 0))) if top.sum() >= 5 else None
    out['sides'] = float(np.linalg.norm(np.median(flow[side], 0))) if side.sum() >= 5 else None
    M, inl = cv2.estimateAffinePartial2D(a, b, method=cv2.RANSAC, ransacReprojThreshold=1.0, maxIters=3000, confidence=0.995)
    if M is None:
        return out
    res = np.linalg.norm(a @ M[:, :2].T + M[:, 2] - b, axis=1)
    outl = res > 1.5
    keep = np.ones(len(a), bool)
    if outl.sum() >= 6:
        fg = np.zeros((h, w), np.uint8)
        for x, y in a[outl].astype(int):
            fg[min(h - 1, max(0, y)), min(w - 1, max(0, x))] = 255
        fg = cv2.dilate(fg, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (51, 51)))
        n, lab, st, _ = cv2.connectedComponentsWithStats(fg)
        if n > 1:
            big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
            inside = lab[np.clip(a[:, 1].astype(int), 0, h - 1), np.clip(a[:, 0].astype(int), 0, w - 1)] == big
            keep = ~inside
            out['fg_frac'] = float(st[big, cv2.CC_STAT_AREA]) / (h * w)
    pts = a
    if keep.sum() >= 12:
        M2, in2 = cv2.estimateAffinePartial2D(a[keep], b[keep], method=cv2.RANSAC, ransacReprojThreshold=1.0, maxIters=3000, confidence=0.995)
        if M2 is not None:
            M = M2
            pts = a[keep][in2.ravel() == 1]
    else:
        pts = a[inl.ravel() == 1]
    if len(pts) < 6:
        pts = a
    d = pts @ M[:, :2].T + M[:, 2] - pts
    out['speed'] = float(np.median(np.linalg.norm(d, axis=1)))
    out['n'] = int(len(pts))
    return out


def _runs(mask):
    runs, i, n = [], 0, len(mask)
    while i < n:
        if mask[i]:
            j = i
            while j + 1 < n and mask[j + 1]:
                j += 1
            runs.append([i, j])
            i = j + 1
        else:
            i += 1
    return runs


def _merge(runs, gap):
    out = []
    for r in runs:
        if out and r[0] - out[-1][1] - 1 < gap:
            out[-1][1] = r[1]
        else:
            out.append(list(r))
    return out


def camera(vid, a, b):
    frames = list(range(a, b + 1))
    g = {n: _small(vid, n) for n in frames}
    series = []
    for n in frames[:-1]:
        m = _pair_motion(g[n], g[n + 1])
        m['frame'] = n + 1
        series.append(m)
    sp = np.array([m['speed'] if m['speed'] is not None else np.nan for m in series])
    # NaN (no texture) treated as unknown -> carry previous value
    for i in range(len(sp)):
        if np.isnan(sp[i]):
            sp[i] = sp[i - 1] if i else 0.0
    fast = [r for r in _merge(_runs(sp > 2.0), 5)]
    fast = [r for r in fast if r[1] - r[0] + 1 >= 3]
    # drifts: frames > 0.3 px/f (runs merged when < 5 f apart) that are not
    # inside a fast move; each remaining piece >= 8 f is one drift move.
    moving = np.zeros(len(sp), bool)
    for r in _merge(_runs(sp > 0.3), 5):
        moving[r[0]:r[1] + 1] = True
    for f in fast:
        moving[f[0]:f[1] + 1] = False
    drifts = [r for r in _runs(moving) if r[1] - r[0] + 1 >= 8]
    n_all = len(fast) + len(drifts)
    seg = sorted([(r, 'fast') for r in fast] + [(r, 'drift') for r in drifts])
    stat = _runs(sp < 0.3)
    longest = max([r[1] - r[0] + 1 for r in stat], default=0)
    off = a + 1
    return dict(a=a, b=b, n_pairs=len(series),
                speed=[round(float(v), 3) for v in sp],
                top=[None if m['top'] is None else round(m['top'], 3) for m in series],
                sides=[None if m['sides'] is None else round(m['sides'], 3) for m in series],
                fast_moves=len(fast), fast_runs=[[r[0] + off, r[1] + off] for r in fast],
                all_moves=n_all, all_runs=[[r[0] + off, r[1] + off, k] for r, k in seg],
                longest_static_f=int(longest), static_gt45=bool(longest > 45),
                median_speed=round(float(np.median(sp)), 3) if len(sp) else None,
                median_top=_nmed([m['top'] for m in series]),
                median_sides=_nmed([m['sides'] for m in series]))


def _nmed(v):
    v = [x for x in v if x is not None]
    return round(float(np.median(v)), 3) if v else None


# ---------------------------------------------------------------- cli
def _default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.bool_):
        return bool(o)
    raise TypeError(type(o))


def main(argv):
    cmd, vid = argv[0], argv[1]
    dbg = None
    if '--debug' in argv:
        i = argv.index('--debug')
        dbg = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    if cmd == 'extract':
        extract(vid, [int(x) for x in argv[2:]])
        print('ok')
    elif cmd == 'cap':
        print(json.dumps(cap_height(get_frame(vid, int(argv[2])), dbg), default=_default))
    elif cmd == 'head':
        exc = ()
        if '--exclude' in argv:
            exc = tuple(argv[argv.index('--exclude') + 1].split(','))
        r = head_measure(get_frame(vid, int(argv[2])), [int(x) for x in argv[3:7]], dbg, exc)
        print(json.dumps(r, default=_default))
    elif cmd == 'camera':
        r = camera(vid, int(argv[2]), int(argv[3]))
        if '--series' not in argv:
            for k in ('speed', 'top', 'sides'):
                r.pop(k)
        print(json.dumps(r, default=_default))
    elif cmd == 'zoom':
        out, specs = argv[2], argv[3:]
        tiles = []
        for sp in specs:
            n, b = sp.split(':')
            im = get_frame(vid, int(n))
            r = head_measure(im, [int(x) for x in b.split(',')])
            for k, sc in r.get('scans', {}).items():
                x, y = sc['x'], sc['y']
                c = im[max(0, y - 30):y + 30, max(0, x - 30):x + 30].copy()
                if c.size == 0:
                    continue
                c = cv2.resize(c, (240, 240), interpolation=cv2.INTER_NEAREST)
                cv2.putText(c, 'f%s %s %s' % (n, k, sc['px'] if sc['clean'] else 'x'), (3, 14), 0, 0.45, (0, 0, 255), 1)
                cv2.circle(c, (120, 120), 3, (0, 255, 0), -1)
                tiles.append(c)
        blank = np.zeros((240, 240, 3), np.uint8)
        rows = [np.hstack(tiles[i:i + 6] + [blank] * (6 - len(tiles[i:i + 6]))) for i in range(0, len(tiles), 6)]
        cv2.imwrite(out, np.vstack(rows))
        print(out)
    elif cmd == 'luma':
        print(round(mean_luma(get_frame(vid, int(argv[2]))), 4))


if __name__ == '__main__':
    main(sys.argv[1:])
