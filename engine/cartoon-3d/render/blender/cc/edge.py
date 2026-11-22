import sys
from PIL import Image
import numpy as np
from scipy import ndimage
for f in sys.argv[1:]:
    a=np.asarray(Image.open(f).convert('RGB').resize((180,320)),dtype=float).mean(2)
    gx=ndimage.sobel(a,1); gy=ndimage.sobel(a,0); m=np.hypot(gx,gy)
    print(f.split('/')[-1], round((m>60).mean()*100,1))
