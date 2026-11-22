# helper textures for the Detroit build: glow, pool, ceiling, facade sides, painted crowd card, radio grille, wood
import numpy as np, random, math
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import T, INK, wash, jl, jr, mul, paintdetail, strokes
def radial(name,rgb,W=512,soft=1.0):
    y,x=np.mgrid[0:W,0:W]/(W-1)*2-1; r=np.sqrt(x*x+y*y); a=np.clip(1-r,0,1)**(2*soft)
    im=np.zeros((W,W,4),np.uint8); im[...,:3]=rgb; im[...,3]=(a*255).astype(np.uint8); Image.fromarray(im).save(T+name+'.png')
radial('glow',(255,255,255)); radial('pool',(255,214,150),soft=0.8)
im=wash(1024,1024,(236,230,214),0.05,7); d=ImageDraw.Draw(im)
for i in range(0,1024,256): jl(d,[(i,0),(i,1024)],5,(170,160,140),i); jl(d,[(0,i),(1024,i)],5,(170,160,140),i+1)
paintdetail(im,Image.new('L',im.size,255),(236,230,214),9,1).save(T+'ceiltile.png')
for i in range(6):
    f=Image.open(T+f'dfac{i}.png').convert('RGB'); c=f.crop((0,60,f.width,int(f.height*0.55))).resize((1024,1024)); c.save(T+f'side_dfac{i}.png')
# painted crowd card (far bleacher rows): small heads + hats + coats in rows, flat colours, ink dots
W,H=2048,1024; im=wash(W,H,(150,112,76),0.08,11); d=ImageDraw.Draw(im); r=random.Random(5)
for row in range(9):
    y=H-60-row*110; d.rectangle([0,y+40,W,y+70],fill=(110,80,56))
    x=r.uniform(0,30)
    while x<W:
        c=r.choice([(60,60,70),(120,90,60),(90,40,40),(60,90,70),(150,130,100),(40,50,80),(170,60,50)]); s=r.uniform(26,34)
        d.rounded_rectangle([x-s*0.9,y-10,x+s*0.9,y+60],12,fill=c,outline=(50,28,42),width=4)
        d.ellipse([x-s*0.6,y-s*1.2-10,x+s*0.6,y-10],fill=(251,244,241),outline=(50,28,42),width=4)
        if r.random()<0.6: d.rectangle([x-s*0.7,y-s*1.25-14,x+s*0.7,y-s*1.0-10],fill=r.choice([(80,60,44),(60,60,66),(150,40,50)]),outline=(50,28,42),width=3)
        d.ellipse([x-8,y-s*0.75-10,x-3,y-s*0.6-10],fill=(50,28,42)); d.ellipse([x+3,y-s*0.75-10,x+8,y-s*0.6-10],fill=(50,28,42))
        if r.random()<0.25: d.polygon([(x+s,y-20),(x+s+50,y-40),(x+s,y-60)],fill=r.choice([(200,60,40),(240,200,60),(60,90,160)]),outline=(50,28,42))
        x+=s*2+r.uniform(2,12)
paintdetail(im,Image.new('L',im.size,255),(150,112,76),13,1,neutral=True,dens=0.5).save(T+'crowdcard.png')
# radio grille cloth with a lit dial
im=wash(512,768,(120,80,50),0.06,15); d=ImageDraw.Draw(im)
d.ellipse([96,80,416,400],fill=(180,150,110),outline=INK,width=10)
for k in range(9): d.line([110,110+k*34,402,110+k*34],fill=(150,120,86),width=6)
d.rounded_rectangle([140,470,372,560],20,fill=(250,220,140),outline=INK,width=8)
for k in range(9): d.line([160+k*24,490,160+k*24,540],fill=(110,80,50),width=3)
d.line([256,480,276,550],fill=(200,30,30),width=6)
for x in (170,342): d.ellipse([x-36,610,x+36,682],fill=(80,56,36),outline=INK,width=8)
paintdetail(im,Image.new('L',im.size,255),(120,80,50),17,1,neutral=True,dens=0.5).save(T+'radiofront.png')
P.woodfloor('wood',seed=81,base=(120,80,52))
print('PAINT2_OK')
