# Expression-library targets (coordinator Nov 22, proposed rule from 'Build Rick-style facial expression library'):
# >=14 distinct faces per video, >=4 per featured character, >=5 distinct faces in any 12 s window. blink is not counted. Reads bridge/faces.json.
import json,sys,collections
D=json.load(open('/root/dc/bridge/faces.json')); SH=json.load(open('/root/dc/bridge/shots.json')); END=2086; W=360
FEAT=sys.argv[1].split(',') if len(sys.argv)>1 else []
ev=[]   # (frame, kind, face) visible events, clipped to the character's shot range
for c in D:
    a,b=SH[c['shot']]; seq=[(f,k.replace('_ta','').replace('_tb','')) for f,k in c['faces'] if k!='blink' and not k.startswith('talk')]   # dc14: angle variants count as their base expression   # lip shapes are not expressions
    for i,(f,k) in enumerate(seq):
        nf=seq[i+1][0] if i+1<len(seq) else b
        if nf>=a and f<=b: ev.append((max(f,a),min(nf,b),c['kind'],k))
allf=set(e[3] for e in ev); per=collections.defaultdict(set)
for e in ev: per[e[2]].add(e[3])
worst=(99,0)
for t in range(0,END-W+1,15):
    n=len(set(e[3] for e in ev if e[0]<t+W and e[1]>t))
    if n<worst[0]: worst=(n,t)
print('DISTINCT',len(allf),sorted(allf))
for k in sorted(per,key=lambda k:-len(per[k])): print(f'  {k:8s} {len(per[k]):2d} {"FEATURED" if k in FEAT else ""} {sorted(per[k])}')
print('MIN12S',worst[0],'at frame',worst[1])
ok=len(allf)>=14 and worst[0]>=5 and all(len(per[k])>=4 for k in FEAT)
print('FACECHECK','PASS' if ok else 'FAIL')
