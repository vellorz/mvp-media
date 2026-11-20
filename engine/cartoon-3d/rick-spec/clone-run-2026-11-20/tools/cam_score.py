import sys, json
def score(truth, stats):
    mv = stats['shots'][0]['moves']; ok = tot = 0; miss = []
    for t in truth['moves']:
        best = None
        for m in mv:
            ov = min(m['end_f'], t['end_f']) - max(m['start_f'], t['start_f'])
            if ov > 0 and (best is None or ov > best[0]): best = (ov, m)
        fields = ['found', 'start', 'end', 'type', 'size', 'ease']; tot += len(fields)
        if best is None: miss.append((t, 'not found')); continue
        m = best[1]; ok += 1
        c1 = abs(m['start_f']-t['start_f']) <= 2; c2 = abs(m['end_f']-t['end_f']) <= 2; c3 = m['type'] == t['type']
        if t['type'] in ('push-in', 'pull-out'): c4 = abs(m['scale']/t['amount']-1) <= 0.01
        elif t['type'] == 'pan': c4 = abs(m['pan_pct']-t['amount']) <= 0.5
        else: c4 = abs(m['tilt_pct']-t['amount']) <= 0.5
        c5 = m['ease'] == t['ease']
        for c, n in zip((c1, c2, c3, c4, c5), fields[1:]):
            ok += c
            if not c: miss.append((t['start_f'], t['end_f'], t['type'], t['ease'], round(t['amount'], 3), n, m['start_f'], m['end_f'], m['type'], m['scale'], m['pan_pct'], m['tilt_pct'], m['ease']))
    extra = len(mv) - len(truth['moves'])
    return ok, tot, miss, extra
if __name__ == '__main__':
    O = T = 0
    for d in sys.argv[2:]:
        ok, tot, miss, extra = score(json.load(open(d+'/truth.json')), json.load(open(d+f'/stats{sys.argv[1]}.json'))); O += ok; T += tot
        print(d, ok, tot, 'extra moves', extra); [print('   MISS', m) for m in miss]
    print('TOOL', sys.argv[1], O, T, round(100*O/T, 1))
