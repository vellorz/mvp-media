# rule 353a turn strip from the real cast.py textures: big tiles, head-centre line (grey) and measured feature-centre line (red), shift printed as % of disc width
import numpy as np, os, sys
from PIL import Image, ImageDraw, ImageFont
T='/root/cc/tex/'; OUT=sys.argv[1]
FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',30); FR=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
LV=['L3','L2','L1','F','R1','R2','R3']
rows=[('hero','happy'),('hero','determined'),('pal','smile'),('engA','grin')]
def measure(p):
    a=np.asarray(Image.open(p).convert('RGBA')).astype(float); A=a[...,3]>128; R,G,B=a[...,0],a[...,1],a[...,2]
    skin=A&(R>200)&(G>160)&(B>120)&(R-B>40)
    ys,xs=np.nonzero(skin); y0,y1=np.percentile(ys,[2,98]); x0,x1=np.percentile(xs,[2,98]); cx=(x0+x1)/2; w=x1-x0
    # features: dark pixels inside the disc band between the eye line and the mouth (rows 30-85 % of the skin height), away from the outline
    band=(np.arange(a.shape[0])[:,None]>=y0+0.38*(y1-y0))&(np.arange(a.shape[0])[:,None]<=y0+0.85*(y1-y0))
    inner=(np.abs(np.arange(a.shape[1])[None,:]-cx)<0.40*w)
    dark=A&(R+G+B<300)&(B>=0.8*R)&band&inner   # ink only (plum, B>=R); brown hair and moustaches (B<R) are left out
    fy,fx=np.nonzero(dark); fc=fx.mean() if len(fx) else cx
    return cx,fc,w,(fc-cx)/w*100
tiles=[]; res={}
for k,fk in rows:
    row=[]
    for lv in LV:
        p=f'{T}{k}_h_{fk}@{lv}.png'
        if not os.path.exists(p): continue
        cx,fc,w,sh=measure(p); res[f'{k}_{fk}@{lv}']=round(sh,1)
        im=Image.open(p).convert('RGBA'); s=300/im.height; t=Image.new('RGBA',im.size,(236,230,218,255)); t.alpha_composite(im); d=ImageDraw.Draw(t)
        d.line([(cx,0),(cx,im.height)],fill=(120,120,120,255),width=6); d.line([(fc,0),(fc,im.height)],fill=(210,30,30,255),width=6)
        row.append((t.convert('RGB').resize((int(im.width*s),300)),f'{lv}  {sh:+.1f} %'))
    tiles.append((f'{k} {fk}',row))
W=20+max(sum(t.width+16 for t,_ in r) for _,r in tiles); H=70+len(tiles)*380+60
S=Image.new('RGB',(W,H),(250,248,244)); d=ImageDraw.Draw(S)
d.text((20,14),'Rule 353a turn strip, real cast.py textures. Grey = head centre, red = measured feature centre; shift in % of head width (Rick 6-16 %)',font=FB,fill=(20,20,20)); y=70
for name,row in tiles:
    d.text((20,y),name,font=FB,fill=(40,40,40)); x=20
    for t,cap in row: S.paste(t,(x,y+36)); d.text((x+6,y+340),cap,font=FR,fill=(60,60,60)); x+=t.width+16
    y+=380
d.text((20,y),'Library steps: 5 % / 10 % / 16 % (expressions.py TURN_UNITS 0.65 / 1.3 / 2.05 x 62 px). Features slide; they do not narrow (Rick slides the whole face, measured #12 f1438-1445, #14 f1255-1260).',font=FR,fill=(60,60,60))
S.save(OUT,quality=86); print(res)
