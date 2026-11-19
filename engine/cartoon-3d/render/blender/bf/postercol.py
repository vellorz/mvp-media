# r5: how far is the rendered poster from the shop file? rectify the projected poster quad, fit render = a*file + b per channel
import sys, numpy as np, cv2
from PIL import Image
im=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(np.float32); H,W=im.shape[:2]
q=eval(sys.argv[2]); P=np.asarray(Image.open('/root/bf/poster_2k.png').convert('RGB').resize((400,600))).astype(np.float32)
src=np.float32([[x*W,(1-y)*H] for x,y in q]); dst=np.float32([[0,600],[400,600],[400,0],[0,0]])
R=cv2.warpPerspective(im,cv2.getPerspectiveTransform(src,dst),(400,600))[20:-20,20:-20]; F=P[20:-20,20:-20]
print('render mean',R.reshape(-1,3).mean(0).round(1),'file mean',F.reshape(-1,3).mean(0).round(1))
for c in range(3):
    a,b=np.polyfit(F[...,c].ravel(),R[...,c].ravel(),1); print('ch',c,'gain',round(a,3),'offset',round(b,1))
print('corr',round(np.corrcoef(R.ravel(),F.ravel())[0,1],3))
