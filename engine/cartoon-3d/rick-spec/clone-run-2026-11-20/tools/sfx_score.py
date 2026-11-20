import sys, json
def score(truthp, detp, verbose=True):
    T = json.load(open(truthp))['events']; D = json.load(open(detp))['events']; used = set(); ok = tot = 0; miss = []
    for t in T:
        sw = t['class'] == 'noise sweep/whoosh'; key = (lambda d: abs(d['t_peak']-(t['t']+0.25))) if sw else (lambda d: abs(d['t']-t['t'])); tolm = 0.12 if sw else 0.05
        m = [(key(d), i) for i, d in enumerate(D) if key(d) <= tolm and i not in used]; tot += 4
        if not m: miss.append(('notfound', t)); continue
        _, i = min(m); used.add(i); d = D[i]; c = [True, key(d) <= (0.1 if sw else 0.0334), abs(d['over_bed_dB']-t['over_bed_dB']) <= 1.5, d['class'] == t['class']]; ok += sum(c)
        if not all(c): miss.append((t, d['t'], d['over_bed_dB'], d['class']))
    fp = [d for i, d in enumerate(D) if i not in used]
    if verbose:
        print(detp, ok, tot, 'false positives', len(fp)); [print('  MISS', m) for m in miss]; [print('  FP', d['t'], d['over_bed_dB'], d['class'], d.get('loop_repeats')) for d in fp]
    return ok, tot, len(fp)
if __name__ == '__main__': score(sys.argv[1], sys.argv[2])
