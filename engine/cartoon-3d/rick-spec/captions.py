# Measure burned-in caption geometry: white fill with black outline, every 10th frame, full res.
# Usage: captions.py video.mp4 -> prints share of sampled frames with a caption, median top/bottom y (% H), cap-box height px, width % W, centre x %.
import sys,subprocess,numpy as np,cv2,statistics as st
v=sys.argv[1]; W,H=1080,1920
p=subprocess.Popen(['ffmpeg','-v','error','-i',v,'-vf','select=not(mod(n\\,10)),scale=1080:1920','-vsync','0','-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
res=[];n=0
while True:
    b=p.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    n+=1; f=np.frombuffer(b,np.uint8).reshape(H,W,3)
    band=f[int(.55*H):int(.85*H)]
    white=(band.min(axis=2)>232).astype(np.uint8)
    dark=(band.max(axis=2)<45).astype(np.uint8)
    darkn=cv2.dilate(dark,np.ones((9,9),np.uint8))
    tw=white&darkn
    # keep white pixels near dark outline; row profile
    rows=np.where(tw.sum(1)>6)[0]
    if len(rows)<20: continue
    # largest contiguous run
    runs=np.split(rows,np.where(np.diff(rows)>4)[0]+1); r=max(runs,key=len)
    if len(r)<25 or len(r)>140: continue
    cols=np.where(tw[r[0]:r[-1]+1].sum(0)>0)[0]
    y0=r[0]+int(.55*H); y1=r[-1]+int(.55*H)
    res.append((y0,y1,y1-y0,cols.min(),cols.max()))
if res:
    print(v.split('/')[-1][:2],'frames',n,'with_caption',round(len(res)/n,2),'top%',round(st.median(r[0] for r in res)/H*100,1),'bottom%',round(st.median(r[1] for r in res)/H*100,1),'box_h_px',st.median(r[2] for r in res),'width%W med',round(st.median((r[4]-r[3])/W for r in res)*100,1),'max',round(max((r[4]-r[3])/W for r in res)*100,1),'centre%',round(st.median((r[3]+r[4])/2/W for r in res)*100,1))
else: print(v,'none')
