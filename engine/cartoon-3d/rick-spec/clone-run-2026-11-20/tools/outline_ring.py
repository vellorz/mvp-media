#!/usr/bin/env python3
"""outline_ring.py - fully automatic ring measurement of a character's head
OUTLINE width (stroke width of the ink line around the head fill).

Only human input: a rough head box (x0,y0,x1,y1, full-res 1080x1920 pixels).

Method (frozen; see FROZEN PARAMETERS below; frozen 2026-11-19 after the sanity test)
 1. Frame: exact frame n (1-based) decoded by ffmpeg at full resolution,
    cached under /root/work/ring/frames/VID/full_NNNN.png.
 2. Fill segmentation (same principle as strict_design.head_measure, re-implemented
    here, not imported, so that strict_design.py stays untouched):
    search window = box grown by 20 % each side; reference = central half of the
    box; luma threshold thr = (P90(centre luma) + 40) / 2; chroma gate: Lab (a,b)
    within 25 of the median chroma of the bright centre pixels; 3-px erosion,
    connected component with most centre pixels, regrown 3 px inside the raw
    mask, holes filled, then a 5x5 morphological opening (removes 1-2 px
    antialias spurs that would tilt the contour normals).
 3. Contour = outer contour of the fill, smoothed along its arc (Gaussian,
    sigma 4 points) to get tangents; outward normal = tangent rotated 90 deg,
    sign from the contour orientation.
 4. N = 72 scans: for each polar angle 0,5,...,355 deg about the fill centroid,
    the contour point whose polar angle is nearest (ties: the outermost one).
    The scan samples luma (Rec.709) bilinearly at 1-px steps along the outward
    normal from t = -6 (inside) to t = +40 (outside); t = 0 is the contour pixel.
 5. A scan is CLEAN only if all hold (no manual exclusions):
    a. every sample lies inside the frame and outside the caption band
       (rows 62-80 % H);
    b. the inside samples t = -6..-2 lie in the fill mask; fill luma Lf = their
       median;
    c. dark run: midpoint mid = (Lf + Ld)/2 with Ld = darkest luma of the run,
       solved by fixed-point iteration (start: Ld = min over t = -1..40); the
       run = the first maximal stretch of samples < mid at t >= -1;
    d. the run starts at t <= 3 (within 3 px of the fill edge);
    e. the run does not reach t = 40, and the 4 samples right after the run are
       all >= mid (the line has a non-dark far side: rejects hair, hats, dark
       clothes, dark background, merged shapes);
    f. contrast Lf - Ld >= 50 (a real ink line, not soft shading);
    g. the run is dark ink: Ld <= 0.55 * Lf; the median of the run core (run
       minus its 1-px ends, runs >= 5 px) is <= Ld + 0.35*(mid - Ld) (a mid-dark
       region bounded by a thin line is not an ink stroke); and at most 1 core
       sample is above Ld + 0.6*(mid - Ld) (a light bump inside = two objects);
    h. colour consistency (runs >= 4 px): fewer than 3 core samples further than
       35 (RGB) from the run's median colour (orange/brown hair, skin shadow,
       coloured objects inside the run);
    i. geometry (added in the sanity test): the scan point lies on the real fill
       edge (within 2 px; points on a convex-hull bridge over eyebrows, hair
       notches, mouth are rejected); not at a corner of the fill (turning angle
       > 35 deg over +/- 6 % of the fill width); not in the chin/neck sector
       (outward normal within 40 deg of straight down: the chin line merges
       with collars/necks/beards).
    Scan points: the polar-angle search runs on the densified convex hull of the
    fill, normals from the hull smoothed along its arc (sigma 4 px).
    KNOWN LIMIT: hair, caps or collars drawn in the same near-black as the ink and
    ending on a light background pass every test (they look exactly like a thick
    outline: dark edges, ~30-40 luma plateau, light far side). They inflate single
    scans; the median is robust only while they are a minority of the clean scans.
    Width = number of samples in the run (px, perpendicular to the edge).
 6. Statistics over clean scans: n, median, IQR (P25,P75), P10, P90; lit/shaded:
    plane fit L = a + b x + c y over the eroded fill; scans whose contour point
    lies on the +grad side of the centroid are LIT, the others SHADED.
    outer head width = fill width (widest row of the fill) + 2 * median;
    ratio = median / fill width.  status "unreadable" if clean < 8 of 72.
 7. Determinism: 3 extra runs with the box jittered by 8 px on every side
    (pattern J1 = all sides out, J2 = all sides in, J3 = left/top in, right/bottom
    out); |jitter median - base median| must be <= 1 px for all three, else
    "unstable".

CLI
  outline_ring.py VID N x0 y0 x1 y1 [--debug out.png] [--json]
Library: measure(img, box, debug=None), measure_with_jitter(img, box, debug=None)
"""
import os, sys, json, math, subprocess, tempfile
import numpy as np
import cv2
from scipy import ndimage as ndi

ROOT = '/root/work'
CACHE = '/root/work/ring/frames'
W, H = 1080, 1920
CAP0, CAP1 = 0.62, 0.80

# FROZEN PARAMETERS
N_SCANS = 72
T_IN, T_OUT = 6, 40
START_MAX = 3          # run must start within 3 px of the fill edge
FAR_MIN = 4            # >= 4 px back above the midpoint after the run
CONTRAST_MIN = 50
DARK_REL = 0.55        # Ld <= DARK_REL * Lf
RUN_FLAT = 0.6         # samples inside the run above Ld + RUN_FLAT*(mid-Ld) ...
CORE_REL = 0.35        # median of the run core must be <= Ld + 0.35*(mid-Ld)
RUN_BUMP_MAX = 1       # ... at most this many (outside the 1-px edges)
MIN_CLEAN = 8
COL_DIST = 35          # colour distance (RGB) from the run median ...
COL_N = 3              # ... for at least this many samples = colour change
IMGF = None
BRIDGE_MAX = 2.0       # scan point must be within 2 px of the real fill contour
CORNER_ARC = 0.06      # arc (fraction of fill width) for the corner test ...
CHIN_NY = 0.766        # normals within 40 deg of straight down: chin joins neck/collar, skipped
CORNER_MAX = 35.0
FAR_FILL_TEST = False  # tried and switched off: it also rejects light walls/sky/headbands (lost 4 of 15 heads)
FAR_FILL_DIST = 30.0   # far side within this RGB distance of the fill colour = another head      # ... turning angle above this = corner, scan rejected
JITTER = 8
JIT_PATTERNS = [(-1, -1, 1, 1), (1, 1, -1, -1), (1, 1, 1, 1)]   # sign per side (x0,y0,x1,y1)


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
    tdir = tempfile.mkdtemp(dir=os.path.join(CACHE, vid))
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


# ---------------------------------------------------------------- fill
def segment_fill(img, L, box):
    x0, y0, x1, y1 = [int(v) for v in box]
    hh, ww = L.shape
    gx, gy = int(0.2 * (x1 - x0)), int(0.2 * (y1 - y0))
    X0, Y0, X1, Y1 = max(0, x0 - gx), max(0, y0 - gy), min(ww, x1 + gx), min(hh, y1 + gy)
    sub = L[Y0:Y1, X0:X1]
    cx0, cx1 = x0 + (x1 - x0) // 4 - X0, x1 - (x1 - x0) // 4 - X0
    cy0, cy1 = y0 + (y1 - y0) // 4 - Y0, y1 - (y1 - y0) // 4 - Y0
    p90 = float(np.percentile(sub[cy0:cy1, cx0:cx1], 90))
    thr = 0.5 * (p90 + 40)
    labc = cv2.cvtColor(img[Y0:Y1, X0:X1], cv2.COLOR_BGR2LAB).astype(np.float32)
    ab = labc[..., 1:]
    cmask = sub[cy0:cy1, cx0:cx1] > thr
    ref = np.median(ab[cy0:cy1, cx0:cx1][cmask], 0) if cmask.any() else np.array([128, 128], np.float32)
    chroma_ok = np.linalg.norm(ab - ref, axis=2) < 25
    bright_raw = (sub > thr) & chroma_ok
    bright = ndi.binary_erosion(bright_raw, structure=np.ones((7, 7), bool))
    lab, n = ndi.label(bright)
    if n == 0:
        return None
    cen = lab[cy0:cy1, cx0:cx1]
    counts = np.bincount(cen.ravel(), minlength=n + 1)
    counts[0] = 0
    if counts.max() == 0:
        return None
    k = int(counts.argmax())
    comp = ndi.binary_dilation(lab == k, structure=np.ones((7, 7), bool)) & bright_raw
    comp = ndi.binary_fill_holes(comp)
    comp = ndi.binary_opening(comp, structure=np.ones((5, 5), bool))
    lab2, n2 = ndi.label(comp)
    if n2 == 0:
        return None
    sizes = np.bincount(lab2.ravel()); sizes[0] = 0
    comp = lab2 == int(sizes.argmax())
    leak = bool(comp[0, :].any() or comp[-1, :].any() or comp[:, 0].any() or comp[:, -1].any())
    full = np.zeros((hh, ww), bool)
    full[Y0:Y1, X0:X1] = comp
    return dict(mask=full, thr=thr, win=(X0, Y0, X1, Y1), leak=leak)


# ---------------------------------------------------------------- scans
def _sample(L, xs, ys):
    return cv2.remap(L, xs.astype(np.float32).reshape(1, -1), ys.astype(np.float32).reshape(1, -1),
                     cv2.INTER_LINEAR).ravel()


def _scan(L, mask, px, py, nx, ny):
    ts = np.arange(-T_IN, T_OUT + 1)
    xs, ys = px + nx * ts, py + ny * ts
    out = dict(x=float(px), y=float(py), nx=float(nx), ny=float(ny), clean=False, px=None, why='')
    if xs.min() < 0 or ys.min() < 0 or xs.max() > W - 1 or ys.max() > H - 1:
        out['why'] = 'leaves frame'
        return out
    if ((ys >= CAP0 * H) & (ys <= CAP1 * H)).any():
        out['why'] = 'caption band'
        return out
    inside = [(int(round(xs[i])), int(round(ys[i]))) for i in range(0, T_IN - 1)]   # t=-6..-2
    if not all(mask[y, x] for x, y in inside):
        out['why'] = 'inside not fill'
        return out
    prof = _sample(L, xs, ys)
    Lf = float(np.median(prof[:T_IN - 1]))
    o = T_IN - 1                         # index of t=-1
    win = prof[o:]                       # t=-1..40
    Ld = float(win.min())
    run = None
    for _ in range(8):
        mid = 0.5 * (Lf + Ld)
        below = np.where(win < mid)[0]
        if below.size == 0:
            run = None
            break
        s = int(below[0]); e = s
        while e + 1 < len(win) and win[e + 1] < mid:
            e += 1
        nLd = float(win[s:e + 1].min())
        if run == (s, e) and abs(nLd - Ld) < 1e-3:
            break
        run = (s, e); Ld = nLd
    if run is None:
        out['why'] = 'no dark run'
        return out
    s, e = run
    mid = 0.5 * (Lf + Ld)
    ts_ = s - 1                          # t of first dark sample
    te_ = e - 1
    out.update(Lf=round(Lf, 1), Ld=round(Ld, 1), mid=round(mid, 1), t_start=int(ts_), t_end=int(te_),
               px=int(e - s + 1), prof=[round(float(v), 1) for v in prof])
    if ts_ > START_MAX:
        out['why'] = 'run starts > 3 px out'
        return out
    if e + FAR_MIN >= len(win):
        out['why'] = 'run reaches scan end / no far side'
        return out
    if (win[e + 1:e + 1 + FAR_MIN] < mid).any():
        out['why'] = 'far side dark (< 4 px light)'
        return out
    # far side = another head fill (adjacent character: two outlines merged)
    tf = np.arange(te_ + 2, te_ + 2 + FAR_MIN)
    fcol = np.stack([_sample(IMGF[..., ch], px + nx * tf, py + ny * tf) for ch in range(3)], 1)
    ti = np.arange(-T_IN, -1)
    icol = np.median(np.stack([_sample(IMGF[..., ch], px + nx * ti, py + ny * ti) for ch in range(3)], 1), 0)
    if FAR_FILL_TEST and np.linalg.norm(np.median(fcol, 0) - icol) < FAR_FILL_DIST:
        out['why'] = 'far side looks like head fill (adjacent character)'
        return out
    if Lf - Ld < CONTRAST_MIN:
        out['why'] = 'low contrast'
        return out
    if Ld > DARK_REL * Lf:
        out['why'] = 'run not dark ink'
        return out
    if e - s + 1 >= 4:
        # colour consistency: an ink line is one colour; hair, skin shadow or
        # another coloured object inside the run shows as a colour change
        ts_run = np.arange(ts_ + 1, te_)          # skip the 1-px edges
        cx, cy = px + nx * ts_run, py + ny * ts_run
        cols = np.stack([_sample(IMGF[..., ch], cx, cy) for ch in range(3)], 1)
        med = np.median(cols, 0)
        if (np.linalg.norm(cols - med, axis=1) > COL_DIST).sum() >= COL_N:
            out['why'] = 'colour change inside run'
            return out
    core = win[s + 1:e]                  # skip 1-px edges
    if core.size >= 3 and float(np.median(core)) > Ld + CORE_REL * (mid - Ld):
        out['why'] = 'run core not ink-dark (mid-dark region bounded by a line)'
        return out
    if core.size and (core > Ld + RUN_FLAT * (mid - Ld)).sum() > RUN_BUMP_MAX:
        out['why'] = 'light bump inside run (two objects)'
        return out
    out['clean'] = True
    return out


def measure(img, box, debug=None, L=None):
    global IMGF
    if L is None:
        L = luma709(img)
    IMGF = img.astype(np.float32)
    seg = segment_fill(img, L, box)
    if seg is None:
        return dict(status='no fill', box=list(map(int, box)))
    mask = seg['mask']
    ys, xs = np.nonzero(mask)
    cxm, cym = float(xs.mean()), float(ys.mean())
    # fill width = widest row
    rmin = np.full(H, 10 ** 6); rmax = np.full(H, -1)
    np.minimum.at(rmin, ys, xs); np.maximum.at(rmax, ys, xs)
    wid = np.where(rmax >= 0, rmax - rmin + 1, 0)
    fill_w = int(wid.max())
    # luma gradient of the fill (plane fit on the eroded fill)
    er = ndi.binary_erosion(mask, structure=np.ones((7, 7), bool))
    ey, ex = np.nonzero(er if er.sum() > 50 else mask)
    A = np.c_[np.ones(len(ex)), ex - cxm, ey - cym]
    coef, *_ = np.linalg.lstsq(A, L[ey, ex].astype(np.float64), rcond=None)
    g = np.array([coef[1], coef[2]])
    gmag = float(np.linalg.norm(g))
    # contour
    m8 = mask.astype(np.uint8)
    cnts, _ = cv2.findContours(m8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cnts, key=cv2.contourArea)[:, 0, :].astype(np.float64)
    if len(c) < 40:
        return dict(status='no fill', box=list(map(int, box)))
    # convex hull of the fill, densified to 1-px steps: features that cut into
    # the fill from its edge (eyebrows, hair notches, mouth) are bridged, and a
    # scan placed on a bridge is rejected by the inside-is-fill test
    c0 = np.c_[ndi.gaussian_filter1d(c[:, 0], 2, mode='wrap'), ndi.gaussian_filter1d(c[:, 1], 2, mode='wrap')]
    kc = max(3, int(round(CORNER_ARC * fill_w)))
    d1 = c0 - np.roll(c0, kc, 0)
    d2 = np.roll(c0, -kc, 0) - c0
    turn = np.degrees(np.abs(np.arctan2(d1[:, 0] * d2[:, 1] - d1[:, 1] * d2[:, 0], (d1 * d2).sum(1))))
    hull = cv2.convexHull(c.astype(np.float32))[:, 0, :].astype(np.float64)
    pts = []
    for i in range(len(hull)):
        a, b = hull[i], hull[(i + 1) % len(hull)]
        n = max(1, int(math.ceil(np.hypot(*(b - a)))))
        for k in range(n):
            pts.append(a + (b - a) * k / n)
    c = np.array(pts)
    cs = np.c_[ndi.gaussian_filter1d(c[:, 0], 4, mode='wrap'), ndi.gaussian_filter1d(c[:, 1], 4, mode='wrap')]
    tg = np.roll(cs, -2, 0) - np.roll(cs, 2, 0)
    tg /= np.linalg.norm(tg, axis=1, keepdims=True) + 1e-9
    nrm = np.c_[tg[:, 1], -tg[:, 0]]
    # orientation: outward normal should point away from the centroid on average
    if (((c - [cxm, cym]) * nrm).sum(1)).mean() < 0:
        nrm = -nrm
    ang = np.degrees(np.arctan2(c[:, 1] - cym, c[:, 0] - cxm)) % 360
    rad = np.hypot(c[:, 0] - cxm, c[:, 1] - cym)
    c0 = c0  # true (lightly smoothed) contour, used for the bridge and corner tests
    scans = []
    for k in range(N_SCANS):
        th = 5.0 * k
        d = np.abs((ang - th + 180) % 360 - 180)
        cand = np.where(d <= d.min() + 1e-6)[0]
        if d.min() > 2.5:
            # no contour point within this sector (non-star shape); nearest anyway
            pass
        i = int(cand[np.argmax(rad[cand])])
        dd = np.hypot(c0[:, 0] - c[i, 0], c0[:, 1] - c[i, 1])
        j = int(dd.argmin())
        if dd[j] > BRIDGE_MAX:
            sc = dict(x=float(c[i, 0]), y=float(c[i, 1]), nx=float(nrm[i, 0]), ny=float(nrm[i, 1]), clean=False, px=None,
                      why='on hull bridge (not fill edge)')
        elif nrm[i, 1] > CHIN_NY:
            sc = dict(x=float(c[i, 0]), y=float(c[i, 1]), nx=float(nrm[i, 0]), ny=float(nrm[i, 1]), clean=False, px=None,
                      why='chin/neck sector')
        elif turn[j] > CORNER_MAX:
            sc = dict(x=float(c[i, 0]), y=float(c[i, 1]), nx=float(nrm[i, 0]), ny=float(nrm[i, 1]), clean=False, px=None,
                      why='corner of the fill')
        else:
            sc = _scan(L, mask, c[i, 0], c[i, 1], nrm[i, 0], nrm[i, 1])
        sc['angle'] = th
        side = (c[i, 0] - cxm) * g[0] + (c[i, 1] - cym) * g[1]
        sc['half'] = 'lit' if side > 0 else 'shaded'
        scans.append(sc)
    clean = [s for s in scans if s['clean']]
    wv = np.array([s['px'] for s in clean], float)
    res = dict(box=list(map(int, box)), fill_thr=round(seg['thr'], 1), leak=seg['leak'],
               fill_w_px=fill_w, head_fill_pctW=round(100.0 * fill_w / W, 2),
               fill_centroid=[round(cxm, 1), round(cym, 1)],
               fill_luma_gradient=[round(float(g[0]), 3), round(float(g[1]), 3)], fill_luma_gradient_mag=round(gmag, 3),
               clean_scans=int(len(clean)), widths=[int(v) for v in wv],
               reject_counts={})
    for s in scans:
        if not s['clean']:
            res['reject_counts'][s['why']] = res['reject_counts'].get(s['why'], 0) + 1
    if len(clean) >= 1:
        res.update(median_px=float(np.median(wv)),
                   iqr_px=[float(np.percentile(wv, 25)), float(np.percentile(wv, 75))],
                   p10_px=float(np.percentile(wv, 10)), p90_px=float(np.percentile(wv, 90)))
        lit = [s['px'] for s in clean if s['half'] == 'lit']
        sh = [s['px'] for s in clean if s['half'] == 'shaded']
        res['lit_n'], res['shaded_n'] = len(lit), len(sh)
        res['lit_median_px'] = float(np.median(lit)) if lit else None
        res['shaded_median_px'] = float(np.median(sh)) if sh else None
        res['outer_w_px'] = float(fill_w + 2 * res['median_px'])
        res['outer_pctW'] = round(100.0 * res['outer_w_px'] / W, 2)
        res['ratio_to_fill'] = round(res['median_px'] / fill_w, 4)
    res['status'] = 'ok' if len(clean) >= MIN_CLEAN else 'unreadable'
    res['scans'] = scans
    if debug:
        draw_debug(img, mask, seg['win'], box, scans, res, debug)
    return res


def draw_debug(img, mask, win, box, scans, res, path):
    X0, Y0, X1, Y1 = win
    pad = 50
    a0, b0 = max(0, X0 - pad), max(0, Y0 - pad)
    a1, b1 = min(W, X1 + pad), min(H, Y1 + pad)
    crop = img[b0:b1, a0:a1].copy()
    sc = max(2, int(math.ceil(900 / max(crop.shape[:2]))))
    sc = min(sc, 8)
    vis = cv2.resize(crop, None, fx=sc, fy=sc, interpolation=cv2.INTER_NEAREST)
    m = (mask[b0:b1, a0:a1]).astype(np.uint8)
    cnts, _ = cv2.findContours(cv2.resize(m, None, fx=sc, fy=sc, interpolation=cv2.INTER_NEAREST),
                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(vis, cnts, -1, (255, 255, 0), 1)
    for s in scans:
        P = lambda t: (int(round((s['x'] + s['nx'] * t - a0 + 0.5) * sc)), int(round((s['y'] + s['ny'] * t - b0 + 0.5) * sc)))
        if s['clean']:
            cv2.line(vis, P(s['t_start'] - 0.5), P(s['t_end'] + 0.5), (0, 255, 0), max(1, sc // 3))
        else:
            te = s.get('t_end')
            te = T_OUT if te is None else min(te, T_OUT)
            cv2.line(vis, P(0), P(te + 0.5), (0, 0, 255), 1)
    txt = 'fill %s clean %s med %s %s' % (res.get('fill_w_px'), res.get('clean_scans'), res.get('median_px'), res.get('status'))
    cv2.putText(vis, txt, (10, 30), 0, 0.9, (0, 0, 0), 4)
    cv2.putText(vis, txt, (10, 30), 0, 0.9, (0, 255, 255), 2)
    cv2.imwrite(path, vis)


def jitter_boxes(box):
    x0, y0, x1, y1 = box
    out = []
    for p in JIT_PATTERNS:
        out.append([x0 + p[0] * JITTER, y0 + p[1] * JITTER, x1 + p[2] * JITTER, y1 + p[3] * JITTER])
    return out


def measure_with_jitter(img, box, debug=None):
    L = luma709(img)
    res = measure(img, box, debug, L)
    jm = []
    for jb in jitter_boxes(box):
        r = measure(img, jb, None, L)
        jm.append(r.get('median_px'))
    res['jitter_boxes'] = jitter_boxes(box)
    res['jitter_medians'] = jm
    res['jitter_clean'] = None
    if res['status'] == 'ok':
        bad = [m for m in jm if m is None or abs(m - res['median_px']) > 1.0]
        if bad:
            res['status'] = 'unstable'
    return res


def strip_scans(res):
    r = dict(res)
    r.pop('scans', None)
    return r


if __name__ == '__main__':
    a = sys.argv[1:]
    dbg = None
    if '--debug' in a:
        i = a.index('--debug'); dbg = a[i + 1]; del a[i:i + 2]
    js = '--json' in a
    a = [x for x in a if x != '--json']
    vid, n = a[0], int(a[1]); box = [int(v) for v in a[2:6]]
    r = measure_with_jitter(get_frame(vid, n), box, dbg)
    if js:
        print(json.dumps(r, default=float, indent=1))
    else:
        print(json.dumps(strip_scans(r), default=float))
