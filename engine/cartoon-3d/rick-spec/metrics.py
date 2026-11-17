# Per-frame metrics for a video: luma, saturation, edge density, frame diff, histogram distance.
# Usage: python3 metrics.py video.mp4 out.csv   (decodes at 270x480)
import sys,subprocess,numpy as np,cv2
v,out=sys.argv[1],sys.argv[2]; W,H=270,480
p=subprocess.Popen(['ffmpeg','-v','error','-i',v,'-vf',f'scale={W}:{H}','-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
prev=None;prevh=None;rows=[];i=0
while True:
    b=p.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    i+=1; f=np.frombuffer(b,np.uint8).reshape(H,W,3)
    hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV); g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
    e=cv2.Canny(g,80,160); ed=(cv2.dilate(e,np.ones((3,3)))>0).mean()
    h=cv2.calcHist([hsv],[0,1],None,[30,16],[0,180,0,256]); cv2.normalize(h,h)
    diff=float(np.abs(g.astype(int)-prev).mean()) if prev is not None else 0
    hd=float(cv2.compareHist(prevh,h,cv2.HISTCMP_BHATTACHARYYA)) if prevh is not None else 0
    lab=cv2.cvtColor(f,cv2.COLOR_BGR2LAB)
    rows.append((i,round((i-1)/30,3),round(g.mean()/255,3),round(hsv[...,1].mean()/255,3),round(ed,3),round(diff,2),round(hd,3),
                 round(np.percentile(g,2)/255,3),round(np.percentile(g,98)/255,3),round(float(lab[...,1].mean()-128),2),round(float(lab[...,2].mean()-128),2)))
    prev=g.astype(int);prevh=h
open(out,'w').write('frame,t,luma,sat,edge,diff,histd,p2,p98,lab_a,lab_b\n'+'\n'.join(','.join(map(str,r)) for r in rows))
print(v,i)
