#!/usr/bin/env python3
"""Driver: outline_ring.py on every shot of one video.
Box/frame per shot from the record's strict_evidence/headsNN.json (the head the
strict pass measured); shots from design_fields_strict.json. If the recorded
frame is unreadable/unstable, the same head is tracked (normalised
cross-correlation of the box crop, search +/- 1 box size) to the frames at 25 %
and 75 % of the shot and measured there."""
import sys, os, json, glob, shutil
import numpy as np, cv2
sys.path.insert(0, '/root/work/tools')
import outline_ring as o

B = '/mnt/project-files/modern-vista-social/research/rick-style-spec/new-analysis/'
vid = sys.argv[1]
rec = B + vid + '/'
d = json.load(open(rec + 'design_fields_strict.json'))
hp = glob.glob(rec + 'strict_evidence/heads%s.json' % vid[:2])[0]
heads = json.load(open(hp))
DBG = '/root/work/ring/dbg/'


def track(img0, box, img1):
    x0, y0, x1, y1 = box
    g0 = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY); g1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    tpl = g0[max(0, y0):y1, max(0, x0):x1]
    w, h = x1 - x0, y1 - y0
    X0, Y0 = max(0, x0 - w), max(0, y0 - h)
    X1, Y1 = min(o.W, x1 + w), min(o.H, y1 + h)
    srch = g1[Y0:Y1, X0:X1]
    if srch.shape[0] < tpl.shape[0] or srch.shape[1] < tpl.shape[1]:
        return None, 0.0
    r = cv2.matchTemplate(srch, tpl, cv2.TM_CCOEFF_NORMED)
    _, mx, _, loc = cv2.minMaxLoc(r)
    nx0, ny0 = X0 + loc[0], Y0 + loc[1]
    return [int(nx0), int(ny0), int(nx0 + tpl.shape[1]), int(ny0 + tpl.shape[0])], float(mx)


def summarize(r):
    keys = ['fill_w_px', 'head_fill_pctW', 'clean_scans', 'median_px', 'iqr_px', 'p10_px', 'p90_px', 'lit_median_px',
            'shaded_median_px', 'lit_n', 'shaded_n', 'ratio_to_fill', 'outer_w_px', 'outer_pctW', 'jitter_medians',
            'status', 'leak', 'fill_luma_gradient_mag', 'widths', 'reject_counts']
    return {k: r.get(k) for k in keys}


shots_out = []
for s in d['shots']:
    k = s['shot']
    h = heads.get(str(k))
    base = dict(shot=k, start_f=s['start_f'], end_f=s['end_f'],
                strict_outline_px=s.get('outline_px'), strict_scans_px=s.get('outline_scans_px'),
                strict_fill_pctW=s.get('head_fill_pctW'))
    if not h or not h.get('bbox'):
        base.update(frame=(h or {}).get('frame', s['frame']), box=None,
                    status='no character' if s.get('outline_px') == 'no character' else 'no box (record: %s)' % s.get('outline_px'),
                    note=(h or {}).get('note'))
        shots_out.append(base); continue
    f0, box = int(h['frame']), [int(v) for v in h['bbox']]
    a, b = s['start_f'], s['end_f']
    f25, f75 = int(round(a + 0.25 * (b - a))), int(round(a + 0.75 * (b - a)))
    o.extract(vid, [f0, f25, f75])
    img0 = o.get_frame(vid, f0)
    r = o.measure_with_jitter(img0, box, DBG + '%s_s%d_f%d.png' % (vid[:2], k, f0))
    tries = [dict(frame=f0, box=box, **summarize(r))]
    chosen = tries[0]
    if r['status'] != 'ok':
        for f in (f25, f75):
            if f == f0:
                continue
            img = o.get_frame(vid, f)
            nb, sc = track(img0, box, img)
            if nb is None or sc < 0.5:
                tries.append(dict(frame=f, box=nb, track_score=round(sc, 3), status='track failed'))
                continue
            rr = o.measure_with_jitter(img, nb, DBG + '%s_s%d_f%d.png' % (vid[:2], k, f))
            t = dict(frame=f, box=nb, track_score=round(sc, 3), **summarize(rr))
            tries.append(t)
            if rr['status'] == 'ok' and chosen['status'] != 'ok':
                chosen = t
    out = dict(base)
    out.update(frame=chosen['frame'], box=chosen['box'], note=h.get('note'))
    for kk in ['fill_w_px', 'head_fill_pctW', 'clean_scans', 'median_px', 'iqr_px', 'p10_px', 'p90_px', 'lit_median_px',
               'shaded_median_px', 'lit_n', 'shaded_n', 'ratio_to_fill', 'outer_w_px', 'outer_pctW', 'jitter_medians', 'status']:
        out[kk] = chosen.get(kk)
    out['debug_png'] = 'ring_evidence/%s_s%d_f%d.png' % (vid[:2], k, chosen['frame'])
    out['tries'] = tries
    shots_out.append(out)
    print(k, chosen['frame'], out['status'], out['fill_w_px'], out['clean_scans'], out['median_px'], out['iqr_px'],
          out['lit_median_px'], out['shaded_median_px'], out['jitter_medians'], '| strict', s.get('outline_px'),
          '| tries', [(t['frame'], t['status'], t.get('median_px')) for t in tries], flush=True)

res = dict(video=vid, tool='outline_ring.py', tool_params=dict(N=o.N_SCANS, t_in=o.T_IN, t_out=o.T_OUT, start_max=o.START_MAX,
           far_min=o.FAR_MIN, contrast_min=o.CONTRAST_MIN, dark_rel=o.DARK_REL, col_dist=o.COL_DIST, corner_max=o.CORNER_MAX,
           chin_ny=o.CHIN_NY, min_clean=o.MIN_CLEAN, jitter_px=o.JITTER, jitter_patterns=o.JIT_PATTERNS),
           head_source=os.path.relpath(hp, rec), shots=shots_out)
os.makedirs('/root/work/ring/out', exist_ok=True)
json.dump(res, open('/root/work/ring/out/%s_outline_ring.json' % vid, 'w'), indent=1, default=float)
