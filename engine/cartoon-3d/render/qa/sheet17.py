import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from scipy import ndimage
def edge(p):
    a=np.asarray(Image.open(p).convert('RGB').resize((180,320)),dtype=float).mean(2)
    return (np.hypot(ndimage.sobel(a,1),ndimage.sobel(a,0))>60).mean()*100
out=sys.argv[1]; items=[x.split('=') for x in sys.argv[2:]]
W,H,cols=540,960,4; rows=(len(items)+cols-1)//cols
sh=Image.new('RGB',(W*cols,(H+70)*rows),'white'); d=ImageDraw.Draw(sh)
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
for i,(p,lab) in enumerate(items):
    x,y=(i%cols)*W,(i//cols)*(H+70)
    d.text((x+10,y+8),f"{i+1}. {lab}",fill='black',font=f); d.text((x+10,y+38),f"frame {p.split('x_')[1][:-4]}, edge {edge(p):.0f}%",fill='#444',font=f)
    sh.paste(Image.open(p),(x,y+70))
sh.save(out,quality=88)
