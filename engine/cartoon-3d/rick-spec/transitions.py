# Detect hard cuts and cross-dissolves via linear-blend fit on heavily downscaled frames.
# Usage: python3 transitions.py video.mp4 out.csv
import sys,subprocess,numpy as np,cv2
v,out=sys.argv[1],sys.argv[2]; W,H=36,64
raw=subprocess.run(['ffmpeg','-v','error','-i',v,'-vf',f'scale={W}:{H}:flags=area','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
F=np.frombuffer(raw,np.uint8).reshape(-1,H,W,3).astype(np.float32); N=len(F)
res=[]
for L in [2,4,6,8,10,12,14,16,20]:
    for s in range(1,N-L-1):
        A=F[s-1];B=F[s+L]; dAB=np.abs(A-B).mean()
        if dAB<18: continue
        mids=F[s:s+L]; d=(B-A).ravel(); dd=(d*d).sum()
        alphas=[];err=[]
        for M in mids:
            a=float(((M-A).ravel()*d).sum()/dd); alphas.append(a)
            err.append(np.abs(M-(A+a*(B-A))).mean())
        al=np.array(alphas); mono=np.all(np.diff(al)>-0.08) and al[0]<0.45 and al[-1]>0.55
        if not mono: continue
        e=np.mean(err); 
        # endpoints should be stable neighbours (not mid-transition)
        eA=np.abs(F[s-2]-A).mean() if s>=2 else 0; eB=np.abs(F[min(s+L+1,N-1)]-B).mean()
        score=dAB/(e+1)
        if score>3.0 and e<0.35*dAB: res.append((s,L,round(dAB,1),round(e,1),round(score,2),round(eA,1),round(eB,1)))
# non-max suppression by score
res.sort(key=lambda r:-r[4]); taken=[];keep=[]
for r in res:
    a,b=r[0],r[0]+r[1]
    if any(not(b<x-2 or a>y+2) for x,y in taken): continue
    taken.append((a,b)); keep.append(r)
keep.sort()
raw2=subprocess.run(['ffmpeg','-v','error','-i',v,'-vf','scale=72:128:flags=area','-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True).stdout
G=np.frombuffer(raw2,np.uint8).reshape(-1,128,72,3)
def hd(a,b):
    h=[cv2.calcHist([cv2.cvtColor(x,cv2.COLOR_BGR2HSV)],[0,1,2],None,[12,6,6],[0,180,0,256,0,256]) for x in (a,b)]
    [cv2.normalize(x,x) for x in h]; return cv2.compareHist(h[0],h[1],cv2.HISTCMP_BHATTACHARYYA)
# calibrated on #14 every-frame ground truth (Nov 17): keep if colour-histogram change across the window >=0.37 and blend score >=4
keep=[r+(round(hd(G[max(r[0]-1,0)],G[min(r[0]+r[1],len(G)-1)]),3),) for r in keep]
keep=[r for r in keep if r[7]>=0.37 and r[4]>=4]
open(out,'w').write('start_frame,len_f,dAB,blend_err,score,preA,postB,histd\n'+'\n'.join(','.join(map(str,[r[0]+1]+list(r[1:]))) for r in keep))
print(v.split('/')[-1][:2],len(keep),[(r[0]+1,r[1]) for r in keep])
