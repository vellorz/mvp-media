# 1981 store interior seen through the opening doors (S16): warm lit aisles, shelves of gift boxes, hanging lamps, cast-style ink lines.
from PIL import Image, ImageDraw
import random
T='/root/bf/tex/'; K=(46,34,30); r=random.Random(5)
W,H=1024,800
im=Image.new('RGB',(W,H),(255,226,170)); d=ImageDraw.Draw(im)
for y in range(H):
    t=y/H; d.line([0,y,W,y],fill=(int(255-30*t),int(232-60*t),int(180-70*t)))
d.rectangle([0,H-170,W,H],fill=(170,110,70)); d.line([0,H-170,W,H-170],fill=K,width=6)
for x in range(0,W,96): d.line([x,H-170,x-60,H],fill=(140,90,56),width=4)
for row,y0 in enumerate([200,380]):
    for sx in range(0,W,256):
        d.rectangle([sx+16,y0,sx+240,y0+150],fill=(130,84,52),outline=K,width=6)
        x=sx+28
        while x<sx+228:
            w=r.randint(28,52); h=r.randint(50,120); c=r.choice([(200,40,40),(40,110,70),(240,200,60),(60,90,170),(230,140,160)])
            d.rectangle([x,y0+146-h,x+w,y0+146],fill=c,outline=K,width=4); d.line([x+w//2,y0+146-h,x+w//2,y0+146],fill=(250,240,220),width=5); x+=w+6
for x in range(96,W,192):
    d.line([x,0,x,70],fill=K,width=5); d.pieslice([x-46,50,x+46,120],180,360,fill=(250,240,200),outline=K,width=5)
d.rectangle([W//2-180,H-330,W//2+180,H-200],fill=(200,40,40),outline=K,width=8)
for i in range(6): d.rectangle([W//2-160+i*58,H-310,W//2-120+i*58,H-220],fill=(250,236,90),outline=K,width=4)
im.save(T+'storeint.png'); print('STOREINT_OK')
