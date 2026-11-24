# raw (ungraded) face medians per shot from skinprobe output dirs: python3 skinraw_bcn.py DIR [DIR...] -> prints JSON {shot:[G/R,B/R,nfaces]}
VMIN=0.30   # rule 355 says value > 0.50; night shots (S01, S09) have lit faces at 0.3-0.5, so the probe reaches down to 0.30
import sys, json, numpy as np
from PIL import Image
def faces(img,bl):
    out=[]
    for b in bl:
        h,w=img.shape[:2]; yy,xx=np.mgrid[0:h,0:w]; m=((xx-b['x'])**2+(yy-(b['y']+0.1*b['r']))**2)<(0.6*b['r'])**2
        px=img[m]; mx=px.max(1); mn=px.min(1); s=(mx-mn)/np.maximum(mx,1e-4)
        hue=np.degrees(np.arctan2(np.sqrt(3)*(px[:,1]-px[:,2]),2*px[:,0]-px[:,1]-px[:,2]))%360
        k=(hue>=2)&(hue<=42)&(s<0.40)&(mx>VMIN)
        if k.sum()<20: continue
        q=px[k]; out.append((float(np.median(q[:,1]/q[:,0])),float(np.median(q[:,2]/q[:,0]))))
    return out
res={}
for D in sys.argv[1:]:
    bx=json.load(open(f'{D}/faceboxes.json'))
    for k,bl in bx.items():
        img=np.asarray(Image.open(f'{D}/{k}.png').convert('RGB'),np.float32)/255
        res.setdefault(k[:3],[]).extend(faces(img,bl))
out={s:[round(float(np.median([x[0] for x in v])),3),round(float(np.median([x[1] for x in v])),3),len(v)] for s,v in sorted(res.items()) if v}
print(json.dumps(out))
