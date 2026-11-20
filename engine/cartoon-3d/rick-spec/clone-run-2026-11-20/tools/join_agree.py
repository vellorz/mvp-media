#!/usr/bin/env python3
"""join_agree.py VID -> compares joins.agentA.csv with measurerB_joins.json (raw, before adjudication); captions too."""
import sys, json, csv, re
vid = sys.argv[1]; N = f'/mnt/project-files/modern-vista-social/research/rick-style-spec/new-analysis-2/{vid}/'
A = [(int(r['start_frame']), int(r['len_f']), r['type']) for r in csv.DictReader(open(N+'joins.agentA.csv'))]; Bj = json.load(open(N+'measurerB_joins.json'))
B = [(j['first_blend_frame'], j['len_f'], j['type']) for j in Bj['joins']]; used = set(); rows = []; ok = tot = 0
def kind(t): return 'cut' if 'cut' in t else ('dissolve' if 'dissolve' in t else t)
for a in A:
    m = [(abs(a[0]-b[0]), i) for i, b in enumerate(B) if i not in used and abs(a[0]-b[0]) <= 8]
    if not m: rows.append((a, None)); tot += 4; continue
    _, i = min(m); used.add(i); b = B[i]; c = [True, abs(a[0]-b[0]) <= 2, abs(a[1]-b[1]) <= 2, kind(a[2]) == kind(b[2])]; ok += sum(c); tot += 4; rows.append((a, b, c))
for i, b in enumerate(B):
    if i not in used: rows.append((None, b)); tot += 4
ca = json.load(open(N+'merged.json'))['caption_events']; cb = Bj['captions']; norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
cu = set(); cok = ctot = 0; cmiss = []
for a in ca:
    m = [(abs(a['on']-b['on']), i) for i, b in enumerate(cb) if i not in cu and abs(a['on']-b['on']) <= 3]
    ctot += 3
    if not m: cmiss.append(('A only', a)); continue
    _, i = min(m); cu.add(i); b = cb[i]; c = [True, abs(a['on']-b['on']) <= 1, norm(a['text']) == norm(b['text'])]; cok += sum(c)
    if not all(c): cmiss.append((a, b))
for i, b in enumerate(cb):
    if i not in cu: ctot += 3; cmiss.append(('B only', b))
res = dict(video=vid, joins=dict(ok=ok, total=tot, rate=round(100*ok/tot, 2), rows=rows), captions=dict(nA=len(ca), nB=len(cb), ok=cok, total=ctot, rate=round(100*cok/ctot, 2), misses=cmiss))
json.dump(res, open(N+'agreement_joins_captions.json', 'w'), indent=1, default=str)
print(vid, 'JOINS', ok, tot, res['joins']['rate']); [print('  ', r) for r in rows if r[0] is None or r[1] is None or not all(r[2])]
print('CAPTIONS', len(ca), len(cb), cok, ctot, res['captions']['rate']); [print('  ', m) for m in cmiss[:12]]
