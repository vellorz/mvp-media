# rule 308/341 ink probe using exact face discs (facebox_dc.py json): darkest 30 % of the outline band (0.94-1.04 of the disc radius) per head.
# python3 inkdisc.py FACEBOX.json IMG... (image names SNN_FFFF.png)
import sys, json, numpy as np
from PIL import Image
FB=json.load(open(sys.argv[1])); allp=[]
for p in sys.argv[2:]:
    f=str(int(p.split('_')[-1].split('.')[0].rstrip('_'))) if not p.endswith('_.png') else None
    x=np.asarray(Image.open(p).convert('RGB')).astype(np.float32); H,W=x.shape[:2]; res=[]
    for b in FB.get(f,[]):
        cx,cy=(b[0]+b[2])/2*W,(b[1]+b[3])/2*H; r=(b[2]-b[0])/2*W
        if r<20 or cx-r<0 or cx+r>W or cy-r<0 or cy+r>H: continue
        yy,xx=np.mgrid[0:H,0:W]; d=np.hypot(xx-cx,yy-cy)/r
        band=(d>0.94)&(d<1.04)&(yy>cy)   # lower half: no hats or hair
        px=x[band]; Y=px@np.float32([0.299,0.587,0.114]); k=max(5,int(0.3*len(Y))); res.append(np.median(px[np.argsort(Y)[:k]],0))
    if not res: print('INK',p.split('/')[-1],'no heads'); continue
    r_,g,b_=np.median(np.array(res),0); mx,mn=max(r_,g,b_),min(r_,g,b_); sat=(mx-mn)/max(mx,1)
    ok=40<=r_<=75 and 20<=g<=55 and 40<=b_<=65 and sat<=0.5; allp.append(ok)
    print('INK',p.split('/')[-1],'heads',len(res),'rgb',(int(r_),int(g),int(b_)),'sat',round(sat,2),'ok' if ok else 'OUT')
print('INK_OUT',allp.count(False),'of',len(allp))
