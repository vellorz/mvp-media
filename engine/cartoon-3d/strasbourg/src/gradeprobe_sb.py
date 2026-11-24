# rule 355 graded-frame face probe (Strasbourg). Reads skinprobe_sb.py output (still path, root, x, y), grades each shot's stills with the
# gradelib_sb chain (solve on that shot's stills -> apply -> finish -> floor -> vignette), reads a 5x5 median at each cheek point,
# drops points that are not skin in the raw still (hair, occluders), then trims the shot's R/B tint (G 0.88-1.06, B 0.88-1.22; R is left alone because lit faces clip at R=1.0) until the shot median
# sits in the band (G/R 0.92 +-0.03, B/R 0.86 +-0.035, inside rule 355's 0.04). python3 gradeprobe_sb.py PTS.txt OUT_PREFIX
import os, sys, json, numpy as np
os.environ.setdefault('GRADE_K','0.25'); sys.path.insert(0,os.path.dirname(__file__))
import gradelib_sb as G
from PIL import Image
pts=[l.split() for l in open(sys.argv[1]) if l.strip()]; OUT=sys.argv[2]
by={}
for fp,root,x,y in pts:
    n=os.path.basename(fp).split('_')[1]; by.setdefault(n,{}).setdefault(fp,[]).append((root,float(x),float(y)))
def grade(raw,p,n): return G.vig(G.floor_(G.finish(G.apply(raw,p))),G.VIG[n])
def read(img,x,y):
    h,w=img.shape[:2]; cx,cy=int(x*w),int(y*h); return np.median(img[max(0,cy-2):cy+3,max(0,cx-2):cx+3].reshape(-1,3),0)
def isskin(c): return c[0]>=c[1]>=c[2]-0.02 and G.gray(c[None,None])[0,0]>0.25 and (c[0]-c[2])/max(c[0],1e-4)<0.45
def run(n,tint):
    ims={fp:np.asarray(Image.open(fp).convert('RGB'),np.float32)/255 for fp in by[n]}
    smp=[v[::2,::2] for v in ims.values()]; b=G.solve(smp,tint,G.LT[n],G.VIG[n]); p=b[1]
    rows=[]
    for fp,im in ims.items():
        o=grade(im,p,n)
        for root,x,y in by[n][fp]:
            r_=read(im,x,y)
            if not isskin(r_): rows.append((os.path.basename(fp),root,None,None,'not-skin (hair/occluded)')); continue
            c=read(o,x,y); rows.append((os.path.basename(fp),root,round(float(c[1]/c[0]),3),round(float(c[2]/c[0]),3),''))
    ok=[r for r in rows if r[2] is not None]
    gr=float(np.median([r[2] for r in ok])) if ok else None; br=float(np.median([r[3] for r in ok])) if ok else None
    return gr,br,rows,b
TINTS={}; rep=[]
for n in sorted(by):
    t=list(G.TINT[n]); hist=[]
    for it in range(8):
        used=tuple(t); gr,br,rows,b=run(n,used); hist.append((tuple(round(v,3) for v in t),gr,br))
        if gr is None: break
        dg=0 if abs(gr-0.92)<=0.03 else gr/0.92; db=0 if abs(br-0.86)<=0.035 else 0.86/br
        if not dg and not db: break
        if dg: t[1]=min(max(t[1]/dg,0.88),1.06)   # v2: trim G, not R: bright day faces are already clipped at R=1.0, so an R gain changed nothing
        if db: t[2]=min(max(t[2]*db,0.88),1.22)
    TINTS[n]=[round(v,4) for v in used]   # the tint the reported numbers were measured with
    fin=('PASS' if gr is not None and abs(gr-0.92)<=0.04 and abs(br-0.86)<=0.04 else ('NO FACE' if gr is None else 'FAIL'))
    rep.append(f'{n}  tint {TINTS[n]}  graded median G/R {gr if gr is None else round(gr,3)}  B/R {br if br is None else round(br,3)}  n={sum(1 for r in rows if r[2] is not None)}  {fin}')
    for r in rows: rep.append(f'    {r[0]} {r[1]} {r[2]} {r[3]} {r[4]}')
    print(rep[-len(rows)-1],flush=True)
json.dump(TINTS,open(OUT+'_tints.json','w'),indent=1); open(OUT+'.txt','w').write('\n'.join(rep)+'\n'); print('GRADEPROBE_DONE')
