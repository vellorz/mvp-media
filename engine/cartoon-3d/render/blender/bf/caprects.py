# caption rectangles (fractions of W,H, y from the bottom like world_to_camera_view) for t7probe: python3 caprects.py
import sys; sys.argv=['post.py','/nonexistent','/tmp/x.mp4','1.0']; sys.path.insert(0,'/root/bf/src')
import post as P, json, numpy as np
out=[]
for a,txt,b in P.CAPS:
    lay,_=P.cap_layer(txt); al=np.asarray(lay)[...,3]; ys,xs=np.nonzero(al>40)
    out.append(dict(a=a,b=b,txt=txt,x0=xs.min()/P.W,x1=(xs.max()+1)/P.W,y0=1-(ys.max()+1)/P.H,y1=1-ys.min()/P.H))
json.dump(out,open('/root/bf/bridge/caprects.json','w'),indent=0); print('CAPRECTS',len(out),'box bottom %H',round((1-min(o['y0'] for o in out))*100,2),'top',round((1-max(o['y1'] for o in out))*100,2))
