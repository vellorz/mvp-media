# Measure a dissolve's opacity curve around a known midpoint: fit incoming weight a(t) for each frame
# as a linear blend of an anchor before and after. Usage: dissolve_curve.py video.mp4 mid1 mid2 ...
import sys,subprocess,numpy as np
v=sys.argv[1]; mids=[int(x) for x in sys.argv[2:]]; W,H=54,96
raw=subprocess.run(['ffmpeg','-v','error','-i',v,'-vf',f'scale={W}:{H}:flags=area,gblur=sigma=1.5','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
F=np.frombuffer(raw,np.uint8).reshape(-1,H,W,3).astype(np.float32)
def fit(A,B,M):
    d=(B-A).ravel(); return float(((M-A).ravel()*d).sum()/(d*d).sum())
out=[]
for m in mids:
    best=None
    for R in (8,10,12,14):
        A=F[m-1-R];B=F[m-1+R]; al=[fit(A,B,F[m-1+k]) for k in range(-R,R+1)]
        al=np.clip(al,0,1); fr=list(range(m-R,m+R+1))
        a05=[f for f,a in zip(fr,al) if 0.05<a<0.95]; a1090=[f for f,a in zip(fr,al) if 0.1<=a<=0.9]
        err=np.mean([np.abs(F[m-1+k]-(A+fit(A,B,F[m-1+k])*(B-A))).mean() for k in range(-R,R+1)])/ (np.abs(A-B).mean()+1e-6)
        if best is None or err<best[0]: best=(err,R,a05,a1090,al)
    err,R,a05,a1090,al=best
    span=(min(a05),max(a05)) if a05 else None; core=len(a1090)
    print(f"mid {m}: visible {span[0] if span else '-'}-{span[1] if span else '-'} ({(span[1]-span[0]+1) if span else 0} f), 10-90% core {core} f, fit err {err:.2f}")
