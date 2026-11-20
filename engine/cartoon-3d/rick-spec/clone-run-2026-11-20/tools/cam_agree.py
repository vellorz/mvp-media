#!/usr/bin/env python3
"""cam_agree.py STATS_A.json STATS_B.json -> agreement per definitions v3 s5 (+v3.1)"""
import sys, json
def agree(A, B):
    f_ok = f_tot = 0; miss = []; per = {}
    def add(k, c, info=None):
        nonlocal f_ok, f_tot
        f_tot += 1; f_ok += bool(c); p = per.setdefault(k, [0, 0]); p[1] += 1; p[0] += bool(c)
        if not c: miss.append((k, info))
    for sa, sb in zip(A['shots'], B['shots']):
        if sa['hold_share'] is None: continue
        add('hold_share', abs(sa['hold_share']-sb['hold_share']) <= 0.05, (sa['start'], sa['hold_share'], sb['hold_share']))
        add('n_moves', len(sa['moves']) == len(sb['moves']), (sa['start'], len(sa['moves']), len(sb['moves'])))
        used = set()
        for ma in sa['moves']:
            best = None
            for j, mb in enumerate(sb['moves']):
                ov = min(ma['end_f'], mb['end_f'])-max(ma['start_f'], mb['start_f'])
                if j not in used and ov > 0 and (best is None or ov > best[0]): best = (ov, j, mb)
            if best is None: continue
            used.add(best[1]); mb = best[2]; tag = (ma['start_f'], ma['end_f'], mb['start_f'], mb['end_f'])
            add('start', abs(ma['start_f']-mb['start_f']) <= 2, tag); add('end', abs(ma['end_f']-mb['end_f']) <= 2, tag); add('type', ma['type'] == mb['type'], tag+(ma['type'], mb['type']))
            add('scale', abs(ma['scale']/mb['scale']-1) <= 0.015, tag+(ma['scale'], mb['scale'])); add('pan', abs(ma['pan_pct']-mb['pan_pct']) <= 1, tag+(ma['pan_pct'], mb['pan_pct'])); add('tilt', abs(ma['tilt_pct']-mb['tilt_pct']) <= 1, tag+(ma['tilt_pct'], mb['tilt_pct'])); add('ease', ma['ease'] == mb['ease'], tag+(ma['ease'], mb['ease']))
    return dict(ok=f_ok, total=f_tot, rate=round(100*f_ok/max(f_tot, 1), 2), per_field=per, misses=miss)
if __name__ == '__main__':
    r = agree(json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))); print(sys.argv[1].split('/')[-2], r['ok'], r['total'], r['rate'], {k: f'{v[0]}/{v[1]}' for k, v in r['per_field'].items()})
    if len(sys.argv) > 3: json.dump(r, open(sys.argv[3], 'w'), indent=1)
