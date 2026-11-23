# dc16 (run thread gate v11 note): presD's crossed arms vanished on his navy coat; a 12 px light-slate rim around the plum arm stroke.
# Run AFTER cast.py (cast.py rewrites the pose textures). python3 rimfix_dc16.py
import numpy as np,cv2,glob
from PIL import Image
for f in sorted(glob.glob('/root/dc/tex16/presD_arm_pose_cross*.png')):
    im=np.array(Image.open(f)).astype(np.float32); a=im[...,3]/255
    halo=cv2.dilate((a>0.5).astype(np.uint8),cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(25,25))).astype(np.float32)
    hal=np.clip(cv2.GaussianBlur(halo,(0,0),1.5)-a,0,1); col=np.array([128,134,158],np.float32)
    out=im.copy(); na=a+hal*(1-a)
    out[...,:3]=(im[...,:3]*a[...,None]+col*hal[...,None]*(1-a[...,None]))/np.maximum(na[...,None],1e-4); out[...,3]=na*255
    Image.fromarray(np.clip(out,0,255).astype(np.uint8)).save(f)
