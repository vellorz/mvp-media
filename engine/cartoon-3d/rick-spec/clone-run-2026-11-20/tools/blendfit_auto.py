#!/usr/bin/env python3
"""blendfit_auto.py - automatic, motion-compensated blend-weight fit for every
dissolve (type contains 'dissolve', len_f > 3) in a video's joins.verified.csv.

Model: I_t ~ (1 - w) A'_t + w B'_t, where A'_t / B'_t are the clean reference
frames A / B warped onto frame t.

  frames      540x960 dumps /root/work/VID/f/NNNN.jpg (frame n 1-based)
  A, B        A = recorded start - 3, B = recorded end + 3 (end = start + len - 1)
  window      t = A-6 .. B+6, clipped to the video and to the neighbouring joins
              (never crosses the previous join's last frame / the next join's
              first frame)
  motion      ECC homography (cv2.findTransformECC, MOTION_HOMOGRAPHY, gauss
              filter 5) on gray 270x480 images, caption band (rows 62-80 % H)
              masked out; A->t is chained outward from A (each t initialised with
              the warp of its neighbour nearer to A), B->t likewise from B;
              fallback: ECC affine, then the neighbour's warp. Warps scaled to
              540x960.
  fit region  central 60 % (x and y 20-80 %) minus the caption band, minus pixels
              that a warp maps from outside the reference frame
  weight      least squares w = <d, y> / <d, d> with d = B' - A', y = I - A'
              (RGB, 0-1), robust: 5 iterations dropping the 20 % pixels with the
              largest |y - w d|; residual = RMS of the kept 80 % (0-255 units);
              contrast = RMS of d over the kept pixels (0-255)
  dissolve    frames with 0.03 < w < 0.97 forming one run of consecutive frames:
              the run that overlaps the recorded blend most (ties: nearest);
              auto start = first frame, auto len = run length
  confidence  'low' when any of: the run is not monotonic (a step down > 0.05),
              the median residual over the run > 0.5 x the median contrast of the
              run (the model explains less than half), the run touches the
              window edge, A or B was clipped to a neighbouring join, another run
              of >= 2 frames reaching 0.1 < w < 0.9 exists in the window (runs that
              only reach 0.03-0.10 / 0.90-0.97 are motion drift of the warps
              outside A..B and are ignored), the 3 frames before A (after B)
              have median |w| (|w-1|) > 0.05 (the reference frame is not clean:
              the picture keeps changing beyond it), or no run.
              Otherwise 'ok'.

CLI  blendfit_auto.py VID [--out CSV] [--strips DIR]
"""
import sys, os, csv, json
import numpy as np
import cv2

ROOT = '/root/work'
REC = '/mnt/project-files/modern-vista-social/research/rick-style-spec/new-analysis/'
CAP0, CAP1 = 0.62, 0.80
LO, HI = 0.03, 0.97
SIDE = 6
OFF = 3
TRIM = 0.20


def load(vid, n):
    im = cv2.imread(os.path.join(ROOT, vid, 'f', '%04d.jpg' % n))
    assert im is not None, (vid, n)
    return im.astype(np.float32) / 255.0


def nframes(vid):
    return len([f for f in os.listdir(os.path.join(ROOT, vid, 'f')) if f.endswith('.jpg')])


def joins(vid):
    rows = list(csv.DictReader(open(REC + vid + '/joins.verified.csv')))
    out = []
    for i, r in enumerate(rows, 1):
        out.append(dict(idx=i, start=int(r['start_frame']), len=int(r['len_f']), type=r['type']))
    return out


_S = np.diag([2.0, 2.0, 1.0]).astype(np.float32)
_Si = np.diag([0.5, 0.5, 1.0]).astype(np.float32)
CRIT = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1e-5)


def small_gray(im):
    g = cv2.cvtColor((im * 255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
    return cv2.resize(g, (270, 480), interpolation=cv2.INTER_AREA).astype(np.float32)


def ecc_mask():
    m = np.ones((480, 270), np.uint8)
    m[int(CAP0 * 480):int(CAP1 * 480)] = 0
    return m


def ecc(tmpl_g, inp_g, H0):
    m = ecc_mask()
    try:
        _, H = cv2.findTransformECC(tmpl_g, inp_g, H0.copy(), cv2.MOTION_HOMOGRAPHY, CRIT, m, 5)
        return H, 'H'
    except cv2.error:
        pass
    try:
        A0 = H0[:2].copy()
        _, A = cv2.findTransformECC(tmpl_g, inp_g, A0, cv2.MOTION_AFFINE, CRIT, m, 5)
        return np.vstack([A, [0, 0, 1]]).astype(np.float32), 'A'
    except cv2.error:
        return H0.copy(), 'prev'


def chain(ref, ts, G):
    """warps (small scale) ref->t for all t in ts, chained outward from ref"""
    Hs = {ref: (np.eye(3, dtype=np.float32), 'id')}
    for direction in (1, -1):
        prev = ref
        t = ref + direction
        while t in ts:
            H, how = ecc(G[t], G[ref], Hs[prev][0])
            Hs[t] = (H, how)
            prev = t
            t += direction
    return Hs


def warp(im, Hsmall):
    H = _S @ Hsmall @ _Si
    h, w = im.shape[:2]
    out = cv2.warpPerspective(im, H, (w, h), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_CONSTANT, borderValue=-1)
    valid = (out[..., 0] >= 0)
    return out, valid


def fit_w(I, Aw, Bw, mask):
    d = (Bw - Aw)[mask]
    y = (I - Aw)[mask]
    keep = np.ones(len(d), bool)
    w = 0.0
    for _ in range(5):
        dd, yy = d[keep], y[keep]
        den = float((dd * dd).sum())
        if den < 1e-9:
            return None, None, None
        w = float((dd * yy).sum() / den)
        r = np.abs(y - w * d).sum(1)
        thr = np.quantile(r, 1 - TRIM)
        keep = r <= thr
    res = float(np.sqrt(((y[keep] - w * d[keep]) ** 2).mean()) * 255)
    con = float(np.sqrt((d[keep] ** 2).mean()) * 255)
    return w, res, con


def fit_join(vid, J, prev_end, next_start, N):
    s, L = J['start'], J['len']
    e = s + L - 1
    A, B = s - OFF, e + OFF
    lo_lim, hi_lim = max(1, prev_end + 1), min(N, next_start - 1)
    clipped = False
    if A < lo_lim:
        A, clipped = lo_lim, True
    if B > hi_lim:
        B, clipped = hi_lim, True
    t0, t1 = max(lo_lim, A - SIDE), min(hi_lim, B + SIDE)
    ts = list(range(t0, t1 + 1))
    F = {t: load(vid, t) for t in ts}
    G = {t: small_gray(F[t]) for t in ts}
    HA = chain(A, set(ts), G)
    HB = chain(B, set(ts), G)
    h, w_ = F[A].shape[:2]
    region = np.zeros((h, w_), bool)
    region[int(0.2 * h):int(0.8 * h), int(0.2 * w_):int(0.8 * w_)] = True
    region[int(CAP0 * h):int(CAP1 * h)] = False
    rows = []
    for t in ts:
        Aw, va = warp(F[A], HA[t][0])
        Bw, vb = warp(F[B], HB[t][0])
        m = region & va & vb
        wt, res, con = fit_w(F[t], Aw, Bw, m)
        rows.append(dict(t=t, w=wt, res=res, con=con, howA=HA[t][1], howB=HB[t][1]))
    # dissolve run
    inr = [r['w'] is not None and LO < r['w'] < HI for r in rows]
    runs, i = [], 0
    while i < len(rows):
        if inr[i]:
            j = i
            while j + 1 < len(rows) and inr[j + 1]:
                j += 1
            runs.append((rows[i]['t'], rows[j]['t']))
            i = j + 1
        else:
            i += 1
    out = dict(idx=J['idx'], type=J['type'], rec_start=s, rec_len=L, A=A, B=B, window=[t0, t1], clipped=clipped,
               series=[[r['t'], None if r['w'] is None else round(r['w'], 3), None if r['res'] is None else round(r['res'], 2),
                        None if r['con'] is None else round(r['con'], 2), r['howA'] + r['howB']] for r in rows],
               runs=runs)
    if not runs:
        out.update(auto_start=None, auto_len=None, residual=None, flag='low', why='no frame with 0.03<w<0.97')
        return out
    def ov(r):
        return (max(0, min(r[1], e) - max(r[0], s) + 1), -min(abs(r[0] - s), abs(r[1] - e)))
    run = max(runs, key=ov)
    rr = [r for r in rows if run[0] <= r['t'] <= run[1]]
    ws = [r['w'] for r in rr]
    mono = all(ws[k + 1] >= ws[k] - 0.05 for k in range(len(ws) - 1))
    resid = float(np.median([r['res'] for r in rr]))
    con = float(np.median([r['con'] for r in rr]))
    why = []
    if not mono:
        why.append('not monotonic')
    if resid > 0.5 * con:
        why.append('residual high (%.1f vs contrast %.1f)' % (resid, con))
    if run[0] == t0 or run[1] == t1:
        why.append('run touches window edge')
    if clipped:
        why.append('A/B clipped to neighbouring join')
    wa = [r['w'] for r in rows if A - 3 <= r['t'] < A and r['w'] is not None]
    wb = [r['w'] for r in rows if B < r['t'] <= B + 3 and r['w'] is not None]
    if wa and abs(float(np.median(wa))) > 0.05:
        why.append('frame A not clean (median w before A = %.2f)' % float(np.median(wa)))
    if wb and abs(float(np.median(wb)) - 1) > 0.05:
        why.append('frame B not clean (median w after B = %.2f)' % float(np.median(wb)))
    others = [r for r in runs if r != run and r[1] - r[0] >= 1 and
              max(min(abs(x['w']), abs(1 - x['w'])) for x in rows if r[0] <= x['t'] <= r[1]) > 0.10]
    if others:
        why.append('another run of >= 2 frames with w 0.1-0.9 in window')
    out.update(auto_start=run[0], auto_len=run[1] - run[0] + 1, residual=round(resid, 2), contrast=round(con, 2),
               monotonic=mono, flag='low' if why else 'ok', why='; '.join(why))
    return out


def strip(vid, J, path):
    s, L = J['rec_start'], J['rec_len']
    e = s + L - 1
    t0 = min(s, J['auto_start'] or s) - 4
    t1 = max(e, (J['auto_start'] or s) + (J['auto_len'] or L) - 1) + 4
    wmap = {t: w for t, w, *_ in J['series']}
    tiles = []
    N = nframes(vid)
    for t in range(max(1, t0), min(N, t1) + 1):
        im = (load(vid, t) * 255).astype(np.uint8)
        im = cv2.resize(im, (180, 320), interpolation=cv2.INTER_AREA)
        inrec = s <= t <= e
        inauto = J['auto_start'] is not None and J['auto_start'] <= t < J['auto_start'] + J['auto_len']
        col = (0, 255, 0) if inauto and inrec else (0, 255, 255) if inrec else (255, 0, 255) if inauto else (128, 128, 128)
        cv2.rectangle(im, (0, 0), (179, 319), col, 3)
        w = wmap.get(t)
        cv2.putText(im, '%d' % t, (6, 22), 0, 0.65, (0, 0, 0), 4); cv2.putText(im, '%d' % t, (6, 22), 0, 0.65, (255, 255, 255), 2)
        txt = 'w %.2f' % w if w is not None else 'w -'
        cv2.putText(im, txt, (6, 310), 0, 0.6, (0, 0, 0), 4); cv2.putText(im, txt, (6, 310), 0, 0.6, (255, 255, 255), 2)
        tiles.append(im)
    rows = [np.hstack(tiles[i:i + 8] + [np.zeros((320, 180, 3), np.uint8)] * (8 - len(tiles[i:i + 8]))) for i in range(0, len(tiles), 8)]
    cv2.imwrite(path, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])


def main(argv):
    vid = argv[0]
    out_csv = argv[argv.index('--out') + 1] if '--out' in argv else '/root/work/ring/out/%s_joins_blendfit_auto.csv' % vid
    sdir = argv[argv.index('--strips') + 1] if '--strips' in argv else '/root/work/ring/strips'
    os.makedirs(sdir, exist_ok=True)
    N = nframes(vid)
    Js = joins(vid)
    res = []
    for k, J in enumerate(Js):
        if 'dissolve' not in J['type'].lower() or J['len'] <= 3:
            continue
        pe = Js[k - 1]['start'] + max(Js[k - 1]['len'], 1) - 1 if k > 0 else 0
        ns = Js[k + 1]['start'] if k + 1 < len(Js) else N + 1
        r = fit_join(vid, J, pe, ns, N)
        ds = None if r['auto_start'] is None else r['auto_start'] - r['rec_start']
        dl = None if r['auto_len'] is None else r['auto_len'] - r['rec_len']
        r['differs_gt2'] = 'yes' if (ds is None or abs(ds) > 2 or abs(dl) > 2) else 'no'
        if r['differs_gt2'] == 'yes':
            p = os.path.join(sdir, '%s_join%02d_f%d.jpg' % (vid[:2], r['idx'], r['rec_start']))
            strip(vid, r, p)
            r['strip'] = os.path.basename(p)
        res.append(r)
        print(r['idx'], r['rec_start'], r['rec_len'], '->', r['auto_start'], r['auto_len'], r.get('residual'), r.get('contrast'),
              r['flag'], r['why'], r['differs_gt2'], [x[1] for x in r['series']], flush=True)
    with open(out_csv, 'w', newline='') as f:
        wr = csv.writer(f)
        wr.writerow(['join_index', 'recorded_start', 'recorded_len', 'auto_start', 'auto_len', 'residual', 'flag', 'differs_gt2',
                     'contrast', 'why', 'type'])
        for r in res:
            wr.writerow([r['idx'], r['rec_start'], r['rec_len'], r['auto_start'], r['auto_len'], r.get('residual'), r['flag'],
                         r['differs_gt2'], r.get('contrast'), r['why'], r['type']])
    json.dump(res, open(out_csv.replace('.csv', '.json'), 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1:])
