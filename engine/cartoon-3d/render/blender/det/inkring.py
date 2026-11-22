# Rule 308 ink sampler, method as written in the rule: darkest 2 % of head-ring pixels per shot.
# Heads = large near-white low-saturation blobs (face cards); ring = band 3-25 px (2K) outside each blob.
# python3 inkring.py VIDEO.mp4 [STEP]
import sys, json, subprocess, numpy as np, cv2
V=sys.argv[1]; STEP=int(sys.argv[2]) if len(sys.argv)>2 else 12
SH=json.load(open('/root/det/bridge/shots.json')); W,H=1440,2560
p=subprocess.Popen(['ffmpeg','-v','error','-i',V,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
f=0; ink={}; nh={}
while True:
    b=p.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    if f%STEP==0:
        x=np.frombuffer(b,np.uint8).reshape(H,W,3); hsv=cv2.cvtColor(x,cv2.COLOR_RGB2HSV)
        face=((hsv[...,2]>215)&(hsv[...,1]<45)).astype(np.uint8); face[int(0.62*H):int(0.75*H)]=0
        face=cv2.morphologyEx(face,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
        n,lab,st,_=cv2.connectedComponentsWithStats(face)
        shot=[k for k,(a,e) in SH.items() if a<=f<=e][-1]
        for i in range(1,n):
            x0,y0,w,h,a=st[i]
            if a<1500 or a>0.25*W*H: continue
            if not (0.6<w/h<1.6) or a/(w*h)<0.55: continue   # roundish card
            m=(lab==i).astype(np.uint8)
            ring=(cv2.dilate(m,np.ones((51,51),np.uint8))>0)&~(cv2.dilate(m,np.ones((7,7),np.uint8))>0)
            px=x[ring].astype(np.float32); Y=px@np.float32([0.299,0.587,0.114])
            k=max(5,int(0.02*len(Y))); d=px[np.argsort(Y)[:k]]
            ink.setdefault(shot,[]).append(np.median(d,0)); nh[shot]=nh.get(shot,0)+1
    f+=1
bad=0; out={}
for s in SH:
    if s not in ink: print('INKRING',s,'no heads found'); continue
    r,g,b_=np.median(np.array(ink[s]),0); mx,mn=max(r,g,b_),min(r,g,b_); sat=(mx-mn)/max(mx,1)
    ok=40<=r<=75 and 20<=g<=55 and 40<=b_<=65 and sat<=0.5; bad+=not ok; out[s]=[int(r),int(g),int(b_),round(sat,2),ok]
    print('INKRING',s,'heads',nh[s],'rgb',(int(r),int(g),int(b_)),'sat',round(sat,2),'ok' if ok else 'OUT')
print('INKRING_OUT',bad)
