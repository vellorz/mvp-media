# Detroit post probe (rule 321): black-share (317), ink sampler (308), poster brightness (320), on a finished video or on raw frames.
# python3 postprobe.py VIDEO.mp4 [STEP]
import sys, json, subprocess, numpy as np, cv2
V=sys.argv[1]; STEP=int(sys.argv[2]) if len(sys.argv)>2 else 6
SH=json.load(open('/root/det/bridge/shots.json')); PQ=json.load(open('/root/det/bridge/posterquad.json'))
W,H=720,1280
TOTAL=int(subprocess.run(['ffprobe','-v','error','-count_packets','-select_streams','v:0','-show_entries','stream=nb_read_packets','-of','csv=p=0',V],capture_output=True,text=True).stdout.strip())   # r3 (payoff verifier round 2): rule 320 is judged on the TRUE last 10 frames, not every 6th
p=subprocess.Popen(['ffmpeg','-v','error','-i',V,'-vf',f'scale={W}:{H}','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
f=0; black=[]; ink={}; post=[]
k5=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
while True:
    b=p.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    LASTN=(f>=TOTAL-10)
    if f%STEP==0 or (LASTN and str(f) in PQ):
        x=np.frombuffer(b,np.uint8).reshape(H,W,3).astype(np.float32)/255; Y=x[...,0]*0.299+x[...,1]*0.587+x[...,2]*0.114
        dark=(Y<0.07).astype(np.uint8); flat=cv2.morphologyEx(dark,cv2.MORPH_OPEN,k5)   # thin ink lines removed, flat dark areas kept
        cap=np.zeros_like(flat); cap[int(0.62*H):int(0.75*H)]=1; flat=flat*(1-cap)   # caption band outlines excluded
        shot=([n for n,(a,e) in SH.items() if a<=f<=e] or [list(SH)[-1]])[0]
        black.append((f,shot,float(flat.mean())))
        # ink: thin dark structures (black-hat) that are dark and not grey-neutral black text
        bh=cv2.morphologyEx((Y*255).astype(np.uint8),cv2.MORPH_BLACKHAT,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)))
        m=(bh>60)&(Y<0.30); m[int(0.62*H):int(0.75*H)]=False
        if m.sum()>200: ink.setdefault(shot,[]).append(np.median(x[m],0)*255)
        if str(f) in PQ:
            q=np.float32([[a*W,(1-c)*H] for a,c in PQ[str(f)]]); mk=np.zeros((H,W),np.uint8); cv2.fillConvexPoly(mk,q.astype(np.int32),1)
            inner=cv2.erode(mk,np.ones((9,9),np.uint8)).astype(bool); ring=(cv2.dilate(mk,np.ones((41,41),np.uint8))>0)&~(mk>0)
            post.append((f,float(Y[inner].mean()),float(Y[~(mk>0)&~ring].mean()),float(np.percentile(Y[inner],98)),float(Y[ring].mean())))
    f+=1
bad=[b for b in black if b[2]>0.03]
print('BLACKSHARE max',round(max(b[2] for b in black)*100,2),'% frames over 3 %:',len(bad),[(b[0],b[1],round(b[2]*100,1)) for b in bad[:12]])
allbad=0
for s,v in ink.items():
    r,g,b_=np.median(np.array(v),0); mx,mn=max(r,g,b_),min(r,g,b_); sat=(mx-mn)/max(mx,1)
    ok=40<=r<=75 and 20<=g<=55 and 40<=b_<=65 and sat<=0.5; allbad+=not ok
    print('INK',s,'rgb',(int(r),int(g),int(b_)),'sat',round(sat,2),'ok' if ok else 'OUT')
print('INK_OUT',allbad)
if post:
    last=[a for a in post if a[0]>=TOTAL-10]; pm=np.mean([a[1] for a in last]); rm=np.mean([a[2] for a in last]); p98=np.max([a[3] for a in last]); gm=np.mean([a[4] for a in last])
    print('POSTER last frames: poster mean',round(pm,3),'rest',round(rm,3),'poster p98',round(p98,3),'frame ring',round(gm,3),'PASS' if pm>=rm and p98<=0.95 else 'FAIL')
