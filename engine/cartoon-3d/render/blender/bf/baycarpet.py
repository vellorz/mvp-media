# r8b (round-7 payoff/visual: bay floor flat, Laplacian 19.7 < 75): painted Rick-style patterned carpet for the payoff window bay
from PIL import Image, ImageDraw, ImageFilter
import random, numpy as np
W=1024; im=Image.new('RGB',(W,W),(132,30,40)); d=ImageDraw.Draw(im); rr=random.Random(7)
for y in range(0,W,128):
    for x in range(0,W,128):
        cx,cy=x+64,y+64; d.polygon([(cx,cy-54),(cx+54,cy),(cx,cy+54),(cx-54,cy)],fill=(176,52,58),outline=(236,196,110),width=6)
        d.ellipse([cx-14,cy-14,cx+14,cy+14],fill=(236,196,110)); d.ellipse([cx-6,cy-6,cx+6,cy+6],fill=(40,70,60))
        for sx,sy in((0,0),(128,0),(0,128),(128,128)): d.ellipse([x+sx-8,y+sy-8,x+sx+8,y+sy+8],fill=(40,70,60))
a=np.asarray(im).astype(np.float32); n=np.random.RandomState(3).normal(0,9,(W,W,1)); a=np.clip(a+n,0,255)   # pile grain
Image.fromarray(a.astype(np.uint8)).save('/root/bf/tex/baycarpet.png'); print('CARPET_OK')
