# r4 (text T1 r3): per-shot camera tilt so every face whose box meets the caption column clears the 71.7 % caption band
import json,sys
d=json.load(open('/root/det/bridge/faceboxes.json'));sh=json.load(open('/root/det/bridge/shots.json'))
old=json.load(open('/root/det/src/tilt.json')) if len(sys.argv)>1 else {}
out={}
for S,(a,b) in sh.items():
    if S=='S21': continue
    need=0
    for f in range(a,b+1):
        for q in d.get(str(f),[]):
            if q[2]>0.37 and q[0]<0.63 and q[1]<0.735: need=max(need,q[3]-0.665)
    v=round(old.get(S,0)+max(0,need),3)
    if v: out[S]=v
print(out); json.dump(out,open('/root/det/src/tilt.json','w'))
