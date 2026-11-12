import sys, subprocess, numpy as np
from scipy import ndimage
for f in sys.argv[1:]:
    raw = subprocess.run(["ffmpeg","-v","error","-i",f,"-vf","scale=180:320:flags=bicubic","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
    a = np.frombuffer(raw,np.uint8).reshape(-1,320,180,3).astype(np.float32).mean(3); e=[]
    for x in a: m=np.hypot(ndimage.sobel(x,1),ndimage.sobel(x,0)); e.append((m>60).mean()*100)
    print(f.split('/')[-1], len(e), round(float(np.mean(e)),2))
