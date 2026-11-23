# rule 308/341 ink sampler (Detroit inkring.py method) on stills: darkest 2 % of the ring band around each face card. Scales the band to the image size.
import sys, numpy as np, cv2
from PIL import Image
for p in sys.argv[1:]:
    x=np.asarray(Image.open(p).convert('RGB')); H,W=x.shape[:2]; k_=W/1440
    hsv=cv2.cvtColor(x,cv2.COLOR_RGB2HSV); face=((hsv[...,2]>205)&(hsv[...,1]<50)).astype(np.uint8)
    face=cv2.morphologyEx(face,cv2.MORPH_OPEN,np.ones((5,5),np.uint8)); n,lab,st,_=cv2.connectedComponentsWithStats(face); res=[]
    for i in range(1,n):
        x0,y0,w,h,a=st[i]
        if a<1500*k_*k_ or a>0.25*W*H or not (0.6<w/h<1.6) or a/(w*h)<0.55: continue
        m=(lab==i).astype(np.uint8); o=max(3,int(51*k_))|1; ii=max(3,int(7*k_))|1
        ring=(cv2.dilate(m,np.ones((o,o),np.uint8))>0)&~(cv2.dilate(m,np.ones((ii,ii),np.uint8))>0)
        px=x[ring].astype(np.float32); Y=px@np.float32([0.299,0.587,0.114]); kk=max(5,int(0.02*len(Y))); res.append(np.median(px[np.argsort(Y)[:kk]],0))
    if not res: print('INK',p.split('/')[-1],'no heads'); continue
    r,g,b=np.median(np.array(res),0); mx,mn=max(r,g,b),min(r,g,b); sat=(mx-mn)/max(mx,1)
    ok=40<=r<=75 and 20<=g<=55 and 40<=b<=65 and sat<=0.5
    print('INK',p.split('/')[-1],'heads',len(res),'rgb',(int(r),int(g),int(b)),'sat',round(sat,2),'ok' if ok else 'OUT')
