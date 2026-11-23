# dc14 rule 350 probe: sagitta of the arm stroke centre line on every arm texture, as % of the shoulder-to-hand chord. PASS >= 6 %.
import sys, glob, numpy as np, math
from PIL import Image
T=sys.argv[1] if len(sys.argv)>1 else '/root/dc/tex/'
res=[]
for p in sorted(glob.glob(T+'*_arm*.png')):
    if p.endswith('_L.png'): continue
    a=np.asarray(Image.open(p).convert('RGBA')).astype(int)
    ink=(a[...,3]>200)&(a[...,:3].sum(-1)<200)
    ys=np.where(ink.any(1))[0]
    # stroke rows: from the shoulder cap to 70 px above the lowest ink row of the arm column (mitten + prop excluded)
    pts=[]
    for y in range(60,620):
        xs=np.where(ink[y])[0]
        if len(xs)==0: continue
        # the arm run is the run nearest the previous centre
        runs=np.split(xs,np.where(np.diff(xs)>1)[0]+1); cs=[(r[0]+r[-1])/2 for r in runs if 20<=len(r)<=120]
        if not cs: continue
        c=cs[0] if not pts else min(cs,key=lambda v:abs(v-pts[-1][0]))
        if pts and abs(c-pts[-1][0])>12: continue
        pts.append((c,y))
    if len(pts)<100: res.append((p,None)); continue
    P=np.array(pts,float); A,B=P[0],P[-1]; L=np.linalg.norm(B-A); n=np.array([B[1]-A[1],-(B[0]-A[0])])/L
    d=(P-A)@n; s=float(np.max(np.abs(d)))/L*100
    res.append((p,round(s,1)))
bad=[r for r in res if r[1] is None or r[1]<6]
for p,s in res: print('ARMCURVE',p.split('/')[-1],s)
print('ARMCURVE_MIN',min(s for _,s in res if s is not None),'N',len(res),'FAIL',len(bad))
