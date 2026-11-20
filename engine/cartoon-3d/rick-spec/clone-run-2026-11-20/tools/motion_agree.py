#!/usr/bin/env python3
"""motion_agree.py VID -> agreement_motion.json : measurer A (merged.json) vs blind measurer B (measurerB_motion.json).
Tolerances = definitions_v3 sections 1-4 and 8. A field is compared when BOTH measurers give a value; fields where only one
gives a value are counted separately ('one_sided') and reported, never silently dropped. Per-field rates are reported."""
import sys, json, re
from collections import defaultdict
vid = sys.argv[1]; N = f'/mnt/project-files/modern-vista-social/research/rick-style-spec/new-analysis-2/{vid}/'
A = json.load(open(N+'merged.json')); B = json.load(open(N+'measurerB_motion.json'))
S = defaultdict(lambda: [0, 0, 0]); miss = []   # field -> [ok, compared, one_sided]
def cmp(cat, f, a, b, ok_fn, ident):
    k = cat+'.'+f
    if a is None and b is None: return
    if a is None or b is None: S[k][2] += 1; return
    try: ok = bool(ok_fn(a, b))
    except Exception: ok = False
    S[k][1] += 1; S[k][0] += ok
    if not ok: miss.append(dict(field=k, item=ident, A=a, B=b))
tol = lambda t: (lambda a, b: abs(a-b) <= t)
nc = lambda s: re.sub(r'\s*\(.*', '', str(s).lower()).strip()
same = lambda a, b: nc(a) == nc(b)
for b in B.get('actions', []):
    a = A['actions'][b['id']]; ident = f"action {b['id']} {a['character']} {a['class']} f{a['start_f']}-{a['end_f']}"
    S['actions.found'][1] += 1; S['actions.found'][0] += bool(b.get('found'))
    if not b.get('found'): miss.append(dict(field='actions.found', item=ident, A=True, B=False)); continue
    t = 1 if (a['end_f']-a['start_f']+1) <= 10 else 2
    cmp('actions', 'start_f', a.get('start_f'), b.get('start_f'), tol(t), ident); cmp('actions', 'end_f', a.get('end_f'), b.get('end_f'), tol(t), ident)
    for f in ('anticipation_f', 'travel_f', 'overshoot_f', 'settle_f'): cmp('actions', f, a.get(f), b.get(f), tol(1), ident)
    cmp('actions', 'motion_type', a.get('motion_type'), b.get('motion_type'), same, ident)
    for f in ('elbow_deg', 'knee_deg'): cmp('actions', f, a.get(f), b.get(f), tol(10), ident)
    cmp('actions', 'torso_tilt_deg', a.get('torso_tilt_deg'), b.get('torso_tilt_deg'), tol(5), ident)
    cmp('actions', 'cadence_f', a.get('cadence_f'), b.get('cadence_f'), tol(1), ident)
    cmp('actions', 'poses_per_step', a.get('poses_per_step'), b.get('poses_per_step'), lambda x, y: x == y, ident)
    cmp('actions', 'stride_H', a.get('stride_H'), b.get('stride_H'), tol(0.15), ident); cmp('actions', 'bob_pct_H', a.get('bob_pct_H'), b.get('bob_pct_H'), tol(3), ident)
for b in B.get('characters', []):
    a = A['characters'][b['id']]; ident = f"char {b['id']} {a['label'][:40]} f{a.get('measure_frame')}"; H = a.get('H_px')
    cmp('characters', 'H_px', H, b.get('H_px'), lambda x, y: abs(x-y) <= max(2, 0.03*x), ident)   # v2 head-fill tolerance 3 %
    cmp('characters', 'head_aspect', a.get('head_aspect'), b.get('head_aspect'), tol(0.08), ident)
    for f in ('torso_h_H', 'torso_w_H', 'leg_len_H', 'total_h_H'): cmp('characters', f, a.get(f), b.get(f), tol(0.08), ident)
    cmp('characters', 'arm_thick_px', a.get('arm_thick_px'), b.get('arm_thick_px'), tol(1.5), ident)
    for f in ('hand_pct_H', 'foot_pct_H', 'eye_size_pct_H', 'eye_spacing_pct_H'): cmp('characters', f, a.get(f), b.get(f), tol(3), ident)
    cmp('characters', 'outline_px', a.get('outline_px'), b.get('outline_px'), tol(1.5), ident)
    cmp('characters', 'arm_class', a.get('arm_class'), b.get('arm_class'), same, ident); cmp('characters', 'leg_class', a.get('leg_class'), b.get('leg_class'), same, ident)
    cmp('characters', 'fingers', a.get('fingers'), b.get('fingers'), lambda x, y: bool(x) == bool(y), ident)
for b in B.get('assets', []):
    a = A['assets'][b['id']]; ident = f"asset {b['id']} {a['object'][:40]} f{a['start_f']}-{a['end_f']}"
    S['assets.found'][1] += 1; S['assets.found'][0] += bool(b.get('found'))
    if not b.get('found'): miss.append(dict(field='assets.found', item=ident, A=True, B=False)); continue
    t = 1 if (a['end_f']-a['start_f']+1) <= 10 else 2
    cmp('assets', 'start_f', a.get('start_f'), b.get('start_f'), tol(t), ident); cmp('assets', 'end_f', a.get('end_f'), b.get('end_f'), tol(t), ident)
    cmp('assets', 'class', a.get('class'), b.get('class'), same, ident); cmp('assets', 'easing', a.get('easing'), b.get('easing'), same, ident)
    cmp('assets', 'overshoot', a.get('overshoot'), b.get('overshoot'), lambda x, y: bool(x) == bool(y), ident)
    cmp('assets', 'bounces', a.get('bounces'), b.get('bounces'), lambda x, y: x == y, ident)
    cmp('assets', 'rot_deg_per_f', a.get('rot_deg_per_f'), b.get('rot_deg_per_f'), lambda x, y: abs(x-y) <= 0.15*max(abs(x), abs(y), 1e-9), ident)
    cmp('assets', 'blur', a.get('blur'), b.get('blur'), lambda x, y: bool(x) == bool(y), ident); cmp('assets', 'on_twos', a.get('on_twos'), b.get('on_twos'), lambda x, y: bool(x) == bool(y), ident)
    cmp('assets', 'loop_f', a.get('loop_f'), b.get('loop_f'), tol(1), ident)
cats = defaultdict(lambda: [0, 0, 0])
for k, v in S.items():
    c = k.split('.')[0]
    for i in range(3): cats[c][i] += v[i]
out = dict(video=vid, fields={k: dict(ok=v[0], compared=v[1], one_sided=v[2], rate=round(100*v[0]/v[1], 1) if v[1] else None) for k, v in sorted(S.items())},
           categories={k: dict(ok=v[0], compared=v[1], one_sided=v[2], rate=round(100*v[0]/v[1], 1) if v[1] else None) for k, v in cats.items()}, misses=miss)
json.dump(out, open(N+'agreement_motion.json', 'w'), indent=1)
print(vid); [print(f"  {k:32s} {v['ok']:4d}/{v['compared']:4d} {v['rate']}  one-sided {v['one_sided']}") for k, v in out['fields'].items()]
[print(' CAT', k, v) for k, v in out['categories'].items()]
