# Flat 2D cut-out cast, Rick construction: round cream head, monoline dark outline (~2.3 % of head width), drawn face,
# bean/stick body with one costume cue, flat colour blocks + soft gradient + fabric lines. Our own designs.
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import json, math
T='/root/cc/tex/'; K=(50,28,42,255); SK=(251,244,241,255); OUT=23   # r8 (owner Nov 20: clone Rick's characters): pure white heads like Rick's. r8b (guide v1.3 x.3): dark plum ink, never pure black; 27 px on an 800 px disc = 3.4 % lit side
def new(w,h): im=Image.new('RGBA',(w,h),(0,0,0,0)); return im,ImageDraw.Draw(im)
def dk(c,f=0.75): return tuple(int(v*f) for v in c[:3])+(255,)
CX,CY=512,540
def eyes(d,kind,cy=520,gap=108,glasses=None):   # r8b: centres 27 % of head width apart (216 px of 800)
    for sx in(-1,1):
        x=CX+sx*gap
        if kind=='dot': d.ellipse([x-33,cy-50,x+33,cy+50],fill=K)   # r8b: 100 px tall = 12.5 % of head width
        elif kind=='wide': d.ellipse([x-56,cy-56,x+56,cy+56],fill=(255,255,255,255),outline=K,width=13); d.ellipse([x-20,cy-20,x+20,cy+20],fill=K)
        elif kind=='tiny': d.ellipse([x-14,cy-14,x+14,cy+14],fill=K)
        elif kind=='up': d.ellipse([x-33,cy-62,x+33,cy+38],fill=K)
        elif kind=='side': d.ellipse([x-2,cy-50,x+62,cy+50],fill=K)
        elif kind=='squeeze': d.line([x-40*sx,cy-30,x+34*sx,cy],fill=K,width=19); d.line([x+34*sx,cy,x-40*sx,cy+30],fill=K,width=19)
        elif kind=='half': d.chord([x-38,cy-38,x+38,cy+38],0,180,fill=K); d.line([x-48,cy,x+48,cy],fill=K,width=16)
        elif kind=='happy': d.arc([x-48,cy-24,x+48,cy+54],200,340,fill=K,width=18)
        elif kind=='closed': d.line([x-44,cy+4,x+44,cy+4],fill=K,width=17)
        elif kind=='swirl':
            for rr in (44,28,12): d.arc([x-rr,cy-rr,x+rr,cy+rr],0,300,fill=K,width=8)
        elif kind=='wink':
            if sx<0: d.arc([x-44,cy-20,x+44,cy+30],200,340,fill=K,width=17)
            else: d.ellipse([x-33,cy-50,x+33,cy+50],fill=K)
        if glasses: d.ellipse([x-74,cy-66,x+74,cy+66],outline=glasses,width=12)
    if glasses: d.line([CX-51,cy-6,CX+51,cy-6],fill=glasses,width=11)
def brows(d,kind,cy=405,gap=108):
    for sx in(-1,1):
        x=CX+sx*gap
        if kind=='flat': d.line([x-52,cy,x+52,cy],fill=K,width=30)
        elif kind=='angry': d.line([x-52*sx,cy-24,x+52*sx,cy+20],fill=K,width=32)
        elif kind=='up': d.line([x-52,cy-36,x+52,cy-36],fill=K,width=30)
        elif kind=='worry': d.line([x-52*sx,cy+16,x+52*sx,cy-26],fill=K,width=30)
        elif kind=='raise': yy=cy-(46 if sx>0 else 0); d.line([x-52,yy,x+52,yy-(8 if sx>0 else 0)],fill=K,width=30)
        elif kind=='none': pass
def mouth(d,kind,cy=715,cx=CX):
    R=(110,28,34,255)
    if kind=='line': d.line([cx-52,cy,cx+52,cy],fill=K,width=17)
    elif kind=='smile': d.arc([cx-82,cy-64,cx+82,cy+44],25,155,fill=K,width=17)
    elif kind=='grin': d.chord([cx-96,cy-50,cx+96,cy+70],0,180,fill=(255,255,255,255),outline=K,width=14); d.line([cx-90,cy+8,cx+90,cy+8],fill=K,width=8)
    elif kind=='smirk': d.arc([cx-82,cy-74,cx+62,cy+26],20,110,fill=K,width=17)
    elif kind=='O': d.ellipse([cx-40,cy-48,cx+40,cy+48],fill=R,outline=K,width=13)
    elif kind=='o': d.ellipse([cx-24,cy-26,cx+24,cy+26],fill=R,outline=K,width=12)
    elif kind=='open': d.chord([cx-80,cy-50,cx+80,cy+80],0,180,fill=R,outline=K,width=13); d.rectangle([cx-60,cy+12,cx+60,cy+26],fill=(255,255,255,255))
    elif kind=='wide': d.rounded_rectangle([cx-90,cy-40,cx+90,cy+70],40,fill=R,outline=K,width=13); d.rectangle([cx-70,cy-30,cx+70,cy-14],fill=(255,255,255,255))
    elif kind=='wavy': d.line([(cx-68,cy),(cx-34,cy-16),(cx,cy),(cx+34,cy-16),(cx+68,cy)],fill=K,width=15,joint='curve')
    elif kind=='grit':
        d.rounded_rectangle([cx-98,cy-38,cx+98,cy+38],18,fill=(255,255,255,255),outline=K,width=13)
        for i in range(-2,3): d.line([cx+i*35,cy-38,cx+i*35,cy+38],fill=K,width=8)
    elif kind=='laugh':
        d.chord([cx-108,cy-78,cx+108,cy+98],0,180,fill=R,outline=K,width=13)
        d.rectangle([cx-84,cy+12,cx+84,cy+34],fill=(255,255,255,255)); d.ellipse([cx-38,cy+44,cx+38,cy+84],fill=(220,90,100,255))
    elif kind=='frown': d.arc([cx-78,cy-4,cx+78,cy+88],205,335,fill=K,width=17)
    elif kind=='whistle': d.ellipse([cx-30,cy-30,cx+30,cy+30],fill=R,outline=K,width=12); d.rounded_rectangle([cx-18,cy-10,cx+110,cy+26],10,fill=(200,200,210,255),outline=K,width=10); d.ellipse([cx+80,cy-20,cx+150,cy+46],fill=(200,200,210,255),outline=K,width=10)
def extras(d,kind):
    if 'sweat' in kind: d.polygon([(800,320),(770,400),(830,400)],fill=(120,190,255,255)); d.ellipse([768,372,832,436],fill=(120,190,255,255),outline=K,width=8)
    if 'blush' in kind: pass   # r8: Rick's faces carry no blush
    if 'puff' in kind:
        for x in(300,724): d.ellipse([x-80,600,x+80,740],fill=(250,180,170,170))
    if 'tear' in kind: d.ellipse([370,580,410,640],fill=(120,190,255,255),outline=K,width=6)
    if 'angryfill' in kind: pass
C=json.load(open('/root/cc/src/cast.json'))
def head(name,fk):
    c=C[name]; e,b,m=c['faces'][fk][:3]; ex=c['faces'][fk][3] if len(c['faces'][fk])>3 else ''
    im,d=new(1024,1024); hair=tuple(c.get('hair',(60,40,30)))+(255,)
    hs=c.get('hairstyle','short')
    if hs=='bun': d.ellipse([382,40,642,280],fill=hair,outline=K,width=OUT)
    if hs=='long': d.rounded_rectangle([100,260,924,980],200,fill=hair,outline=K,width=OUT)
    if hs=='mullet': d.rounded_rectangle([170,320,854,1010],140,fill=hair,outline=K,width=OUT)   # back hair, crown to shoulders
    if hs=='tied': d.rounded_rectangle([150,250,874,1000],180,fill=hair,outline=K,width=OUT)   # cc: long hair falling behind the shoulders
    if hs=='white': d.rounded_rectangle([130,300,894,860],200,fill=hair,outline=K,width=OUT)   # cc: old man's white hair at the sides
    if hs=='perm':
        for a in range(0,360,30): x=CX+380*math.cos(math.radians(a)); y=500+360*math.sin(math.radians(a))*0.95; d.ellipse([x-120,y-120,x+120,y+120],fill=hair,outline=K,width=OUT)
    skin=tuple(c.get('skin',SK[:3]))+(255,)
    # r8b (guide v1.3 x.3): ink 3.4 % of head width toward the light (upper right), 6 % away from it and under the chin
    d.ellipse([112,140,912,940],fill=K); d.ellipse([112+48,140+27,912-27,940-48],fill=skin)
    head_shade(im,skin); d=ImageDraw.Draw(im)
    # r9 (RENDER_SPEC_v1.4 A: eyes centred ~69 % up the head): hair and hats are drawn on their own layer and squashed to the top 40 % of the
    # head (x0.6 from the top), the face features on a layer moved up 105 px (eyes at 65.6 % up)
    if 'angryfill' in ex: 
        ov=Image.new('RGBA',(1024,1024),(0,0,0,0)); od=ImageDraw.Draw(ov); od.ellipse([130,158,894,922],fill=(170,60,170,120)); im.alpha_composite(ov); d=ImageDraw.Draw(im)
    if hs in('short','bald','bun','mullet','tied','white'):   # r9: hairlines raised with the features (hair ends ~285, brows at 300)
        if hs=='short': d.chord([150,150,874,420],180,360,fill=hair,outline=K,width=OUT)
        if hs=='bun': d.chord([150,150,874,410],180,360,fill=hair,outline=K,width=OUT)
        if hs=='bald':
            for sx in(-1,1): d.chord([CX+sx*390-100,300,CX+sx*390+100,580],90 if sx>0 else 270,270 if sx>0 else 450,fill=hair)
        if hs=='mullet': d.chord([150,150,874,420],180,360,fill=hair,outline=K,width=OUT)
        if hs=='tied': d.chord([150,150,874,420],180,360,fill=hair,outline=K,width=OUT)
        if hs=='white': d.chord([200,160,824,380],180,360,fill=hair,outline=K,width=OUT)
    base=im; im,d=new(1024,1024)   # hats on their own layer, squashed x0.6 from the top (peaks end <= 245)
    hat=c.get('hat')
    if hat=='cop':
        d.chord([140,60,884,400],180,360,fill=(28,36,70,255),outline=K,width=OUT); d.rectangle([150,230,874,300],fill=(28,36,70,255),outline=K,width=OUT)
        d.chord([180,270,844,400],0,180,fill=(20,20,26,255),outline=K,width=OUT)   # peak; r8b (round-7 C4: brows were drawn on the dark peak): peak ends at y 400, brows sit below it
        d.polygon([(CX,130),(CX+44,175),(CX+30,225),(CX-30,225),(CX-44,175)],fill=(214,180,80,255),outline=K)  # plain shield, no text
    if hat=='flatcap': d.chord([150,140,874,480],180,360,fill=(90,90,96,255),outline=K,width=OUT); d.chord([200,300,760,400],0,180,fill=(70,70,76,255),outline=K,width=OUT)
    if hat=='ladyhat': d.ellipse([60,250,964,380],fill=(150,40,60,255),outline=K,width=OUT); d.chord([230,90,794,420],180,360,fill=(150,40,60,255),outline=K,width=OUT); d.ellipse([680,150,780,250],fill=(240,200,80,255),outline=K,width=10)
    if hat=='beanie': d.chord([140,110,884,460],180,360,fill=tuple(c['scarf'])+(255,),outline=K,width=OUT); d.ellipse([462,60,562,160],fill=(250,250,250,255),outline=K,width=12)
    if hat=='fedora': d.ellipse([90,300,934,400],fill=(80,60,44,255),outline=K,width=OUT); d.rounded_rectangle([250,90,774,350],60,fill=(80,60,44,255),outline=K,width=OUT); d.rectangle([250,280,774,330],fill=(40,30,24,255))
    if hat=='capotain':   # cc: Pilgrim's tall felt hat (tapered crown, flat brim, plain band; no buckle: buckles are a later myth)
        hc=tuple(c.get('hatc',(40,34,36)))+(255,)
        d.ellipse([70,300,954,420],fill=hc,outline=K,width=OUT); d.polygon([(250,360),(300,0),(724,0),(774,360)],fill=hc,outline=K); d.line([(250,360),(300,0),(724,0),(774,360)],fill=K,width=OUT)
        d.rectangle([262,270,762,330],fill=dk(hc,0.6),outline=K,width=10)
    if hat=='knit': d.chord([140,110,884,460],180,360,fill=tuple(c.get('hatc',(150,40,40)))+(255,),outline=K,width=OUT); d.rectangle([150,330,874,400],fill=dk(tuple(c.get('hatc',(150,40,40))),0.75)+(255,) if False else (120,32,32,255),outline=K,width=10)
    if hat=='tricorn':
        hc=(40,34,40,255); d.chord([200,100,824,420],180,360,fill=hc,outline=K,width=OUT)
        d.polygon([(40,380),(512,250),(984,380),(512,330)],fill=hc,outline=K); d.line([(40,380),(512,250),(984,380),(512,330),(40,380)],fill=K,width=OUT)
        d.line([(80,372),(512,262),(944,372)],fill=(200,170,90,255),width=10)
    if hat=='sunhat': hc=(236,214,150,255); d.ellipse([20,300,1004,420],fill=hc,outline=K,width=OUT); d.chord([230,90,794,420],180,360,fill=hc,outline=K,width=OUT); d.rectangle([236,300,788,340],fill=(60,110,150,255))
    if hat=='cap': hc=tuple(c.get('hatc',(40,90,140)))+(255,); d.chord([150,120,874,440],180,360,fill=hc,outline=K,width=OUT); d.chord([420,330,980,420],180,360,fill=hc,outline=K,width=OUT)
    top=im.resize((1024,int(1024*0.6)),Image.LANCZOS); im=base; im.alpha_composite(top,(0,0)); top=None
    feat,d=new(1024,1024)
    eyes(d,e,glasses=(tuple(c['glasses'])+(255,)) if c.get('glasses') else None); brows(d,b if hat not in('cop','flatcap','fedora','beanie','ladyhat','capotain','tricorn','knit','cap','sunhat') or b!='up' else 'flat'); mouth(d,m)
    if c.get('mustache'):   # r8: Rick's bushy two-lobe mustache
        mc=tuple(c['mustache'])+(255,)
        for sx in(-1,1): d.ellipse([CX+sx*80-95,605,CX+sx*80+95,705],fill=mc,outline=K,width=12)
        d.ellipse([CX-70,610,CX+70,690],fill=mc)
    if c.get('nose',True): d.arc([CX-30,560,CX+30,640],-30,200,fill=K,width=10)
    extras(d,ex)
    im.alpha_composite(feat.crop((0,105,1024,1024)),(0,0))
    return im
# ---- round 3 (rule 193): Rick-style construction ----
# slim column garment (narrower than the head), long coat/robe to the shins, hard cel shadow on the left third,
# light rim on the right, ink detail (collar, placket, buttons, belt + buckle, hem band, fold lines),
# stick legs with small shoes; thin sleeves with a cuff and a small hand. Drawn at 2x and downsampled (clean edges).
SS=2; BOUT=17   # round 4: body outline as heavy as the head's (verifier: thin body outlines vs heads)
def lt(c,f=1.12): return tuple(min(255,int(v*f)) for v in c[:3])+(255,)
GB={'tall':(98,175,215),'short':(98,180,222),'round':(98,200,238)}   # r8b: one build for all (guide v1.3 x.3: torso 1.00 H, legs 1.25-1.3 H, total 3.2-3.35 H); kinds differ in width only   # top px, shoulder half-width, hem half-width
HEMY={'tall':528,'short':528,'round':528}   # r8b: torso 430 px = 1.00 H (head 0.43 m), legs 528->1074 = 1.27 H   # r6 (round-5: legs 0.64-0.90 H, Rick 0.93-1.31): shorter torso, longer legs   # round 5 (B1/B2): torso ~0.86 H tall (H = head disc ~560 px), legs ~0.85 H visible
WK={'tall':0.74,'short':0.745,'round':0.72}
def _sil(kind):
    y0,w0,w1=GB[kind]; y1=HEMY[kind]; pts=[]
    k_=WK[kind]; w0=int(w0*k_); w1=int(w1*k_)   # r9 (RENDER_SPEC_v1.4 A: torso width 0.73-0.89 H): widths x0.72-0.745
    w1=int(w1*0.74); rr=int(0.36*2*w1)   # r6: hem narrower than the middle (Rick: widest at mid-torso)   # rounded bottom: corner radius >= 0.35 of the torso width (Rick bean)
    BG_=int(62*k_)
    yb=y1-rr*0.55   # sides end here, then a half-ellipse closes the bottom
    for i in range(0,11): t=i/10; pts.append((400-(w1+(w0-w1)*t)-BG_*math.sin(math.pi*t), yb+(y0+70-yb)*t))
    for i in range(0,13): a=math.radians(180+i*7.5); pts.append((400-w0+70+70*math.cos(a)*1.0, y0+70+70*math.sin(a)))
    pts.append((400-w0+70,y0)); pts.append((400+w0-70,y0))
    for i in range(0,13): a=math.radians(270+i*7.5); pts.append((400+w0-70+70*math.cos(a), y0+70+70*math.sin(a)))
    for i in range(0,11): t=i/10; pts.append((400+(w0+(w1-w0)*t)+BG_*math.sin(math.pi*t), y0+70+(yb-y0-70)*t))
    for i in range(1,24): a=math.pi*i/24; pts.append((400+w1*math.cos(a), yb+rr*0.55*math.sin(a)))
    return pts,y0,w0,w1,y1
def _S(p): return [(x*SS,y*SS) for x,y in p]
def _hw(y,y0,w0,w1,y1): return w0+(w1-w0)*max(0,min(1,(y-y0-70)/(y1-y0-70)))
def body(name,stride=0):
    c=C[name]; kind=c.get('body','tall'); R=tuple(c['coat'])+(255,); cue=c.get('cue')
    W,H=800*SS,1100*SS; im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    legc=dk(tuple(c.get('legs',(40,36,40))),0.8); shoe=(34,26,22,255)
    pts,y0,w0,w1,y1=_sil(kind); s=lambda v:int(v*SS)
    # legs (thin sticks) + small shoes; stride poses spread the feet, one lifted
    # r8 (Rick clone): legs are one dark noodle line each (6.5 % of head width, no taper), knee bowed outward ~156 deg, small dark stub feet <= 0.12 H
    # r8b (guide v1.3 x.3): one smooth noodle curve per leg (no knee joint), 5.5 % H thick; foot oval ~15 % H wide
    LW=24
    for sx in(-1,1):
        x=400+sx*62; fx=x+sx*20+(sx*60 if stride else 0); lift=(70 if (stride==1 and sx<0) or (stride==2 and sx>0) else 0); fy=1056-lift
        y_0=y1-60; cx_=(x+fx)/2+sx*30; cy_=(y_0+fy)/2
        P=[((1-t)**2*x+2*(1-t)*t*cx_+t*t*fx,(1-t)**2*y_0+2*(1-t)*t*cy_+t*t*fy) for t in [i/24 for i in range(25)]]
        d.line(_S(P),fill=K,width=s(LW),joint='curve')
        for p_ in (P[0],P[-1]): d.ellipse([s(p_[0]-LW/2),s(p_[1]-LW/2),s(p_[0]+LW/2),s(p_[1]+LW/2)],fill=K)
        d.ellipse([s(fx-30+sx*16),s(fy-14),s(fx+34+sx*16),s(fy+18)],fill=K)
    # garment base
    gm=Image.new('L',(W,H),0); ImageDraw.Draw(gm).polygon(_S(pts),fill=255)
    base=Image.new('RGBA',(W,H),R); im.paste(base,(0,0),gm); d=ImageDraw.Draw(im)
    L=[]   # detail layer drawn clipped to the garment
    det=Image.new('RGBA',(W,H),(0,0,0,0)); dd=ImageDraw.Draw(det)
    shade=dk(R,0.74); rim=lt(R,1.16); line2=dk(R,0.52)
    # hard cel shadow: left third, slightly curved edge (light from the upper right, Rick-style)
    sh=[(400-260,0)]+[(400-60-int(40*math.sin(math.pi*t)), int(1100*t)) for t in [i/20 for i in range(21)]]+[(400-260,1100)]
    dd.polygon(_S(sh),fill=shade)
    dd.polygon(_S([(400+w0-16,y0+40),(400+w0+30,y0+40),(400+w0+30+(w1-w0)*0.5+40,(y0+y1)/2),(400+w1+40,y1),(400+w1-22,y1),(400+(w0+w1)/2+24-19,(y0+y1)/2)]),fill=rim)   # rim follows the bulge
    hemh=34 if cue not in('apron',) else 0
    if hemh: dd.polygon(_S([(0,y1-hemh-40),(800,y1-hemh-40),(800,y1+60),(0,y1+60)]),fill=dk(R,0.6))
    beltY=y0+int((y1-y0)*0.46)
    def belt(col=(30,24,22,255),buck=(214,180,80,255)):
        dd.rectangle([0,s(beltY),W,s(beltY+42)],fill=col); dd.line([0,s(beltY),W,s(beltY)],fill=K,width=s(6)); dd.line([0,s(beltY+42),W,s(beltY+42)],fill=K,width=s(6))
        dd.rectangle([s(372),s(beltY-6),s(428),s(beltY+48)],fill=buck,outline=K,width=s(6)); dd.rectangle([s(388),s(beltY+8),s(412),s(beltY+34)],fill=col)
    def placket(x=400,top=None,bot=None): dd.line([s(x),s(top or y0+30),s(x),s(bot or y1)],fill=K,width=s(7))
    def buttons(xs,ys,col=(214,180,80,255),r=13):
        for x in xs:
            for y in ys: dd.ellipse([s(x-r),s(y-r),s(x+r),s(y+r)],fill=col,outline=K,width=s(5)); dd.ellipse([s(x-r+5),s(y-r+4),s(x-r+11),s(y-r+10)],fill=(255,250,230,255))
    def folds(n=4,ytop=None):
        yt=ytop or beltY+60
        for k in range(n):
            x=400-int(_hw(y1,y0,w0,w1,y1)*0.7)+k*int(_hw(y1,y0,w0,w1,y1)*1.4/(n-1)) if n>1 else 400
            dd.line(_S([(x,y1-30),(x+6,y1-110),(x-4,yt+80)]),fill=line2,width=s(5),joint='curve')
        dd.arc([s(330),s(beltY+50),s(470),s(beltY+120)],20,160,fill=line2,width=s(5))
    def lapels(col,shirt=(248,246,238,255),depth=230):
        dd.polygon(_S([(400-90,y0-10),(400,y0+depth),(400+90,y0-10)]),fill=shirt)
        for sx in(-1,1): dd.polygon(_S([(400+sx*92,y0-12),(400+sx*20,y0+depth-10),(400+sx*70,y0+depth-60),(400+sx*150,y0+60)]),fill=col,outline=K,width=s(7))
    def collar(col,h=46):
        dd.rounded_rectangle([s(400-120),s(y0-10),s(400+120),s(y0+h)],s(18),fill=col,outline=K,width=s(7))
    if cue=='cop':
        collar(dk(R,0.8)); placket(); belt(); buttons((360,440),[y0+110,y0+190,beltY+90,beltY+170])
        for sx in(-1,1): dd.rounded_rectangle([s(400+sx*w0-60-(0 if sx>0 else -0)),s(y0+8),s(400+sx*w0+(-10 if sx>0 else 60)),s(y0+44)],s(10),fill=dk(R,0.6),outline=K,width=s(6))
        dd.polygon(_S([(278,y0+120),(318,y0+100),(340,y0+150),(300,y0+178),(268,y0+150)]),fill=(214,180,80,255),outline=K)
        dd.line(_S([(282,y0+128),(330,y0+140)]),fill=dk((214,180,80),0.6),width=s(4))
        folds(4)
    elif cue=='bowtie':
        lapels(dk(R,0.7)); placket(400,y0+230); buttons((400,),[y0+290,beltY+30],col=(70,46,30,255),r=12)
        dd.polygon(_S([(338,y0+30),(400,y0+58),(462,y0+30),(462,y0+100),(400,y0+72),(338,y0+100)]),fill=(170,30,40,255),outline=K,width=s(6)); dd.ellipse([s(388),s(y0+52),s(412),s(y0+80)],fill=(140,20,30,255),outline=K,width=s(5))
        for sx in(-1,1): dd.rectangle([s(400+sx*150-55),s(beltY+60),s(400+sx*150+55),s(beltY+82)],fill=dk(R,0.65),outline=K,width=s(5))
        dd.polygon(_S([(470,y0+150),(520,y0+150),(510,y0+178),(480,y0+178)]),fill=(240,236,226,255),outline=K,width=s(4))
        folds(3)
    elif cue=='blazer':
        lapels(dk(R,0.72),shirt=(250,248,244,255)); placket(400,y0+230); buttons((400,),[y0+280,beltY+20],col=(230,200,110,255))
        dd.line(_S([(400,y0+234),(400,y0+120)]),fill=(200,190,180,255),width=s(4))
        belt(col=(28,24,26,255),buck=(230,200,110,255)); folds(3)
    elif cue=='stripes':
        dd.polygon(_S([(400-110,y0),(400+110,y0),(400+90,y1),(400-90,y1)]),fill=(236,234,228,255))
        for y in range(y0+40,y1,56): dd.line([s(300),s(y),s(500),s(y)],fill=(40,40,48,255),width=s(22))
        for sx in(-1,1): dd.line(_S([(400+sx*112,y0),(400+sx*92,y1)]),fill=K,width=s(7))
        buttons((300,),[y0+200,beltY+40],col=(60,60,66,255),r=11); folds(3)
    elif cue=='pearls':
        collar(lt(R,1.08),36); placket(400,y0+40,beltY); buttons((400,),[y0+120,y0+200,y0+280],col=(246,240,226,255),r=11)
        belt(col=dk(R,0.55),buck=(230,210,150,255))
        for k in range(5): x=400-150+k*75; dd.line(_S([(x,beltY+60),(x+(k-2)*22,y1)]),fill=line2,width=s(5))
        for k in range(11): dd.ellipse([s(310+k*18-9),s(y0+50+abs(k-5)*7-9),s(310+k*18+9),s(y0+50+abs(k-5)*7+9)],fill=(252,250,244,255),outline=K,width=s(3))
    elif cue=='camera':
        lapels(dk(R,0.7),shirt=(250,240,200,255)); placket(400,y0+230); buttons((400,),[y0+290,beltY+40],col=(90,60,30,255),r=12)
        dd.line(_S([(290,y0+10),(470,y0+330)]),fill=(50,40,32,255),width=s(18)); dd.line(_S([(290,y0+10),(470,y0+330)]),fill=K,width=s(4))
        dd.rounded_rectangle([s(420),s(y0+300),s(540),s(y0+380)],s(10),fill=(40,40,44,255),outline=K,width=s(7)); dd.ellipse([s(456),s(y0+312),s(512),s(y0+368)],fill=(120,140,170,255),outline=K,width=s(5))
        for sx in(-1,1): dd.rectangle([s(400+sx*150-50),s(beltY+40),s(400+sx*150+50),s(beltY+62)],fill=dk(R,0.65),outline=K,width=s(5))
        folds(3)
    elif cue=='scarf':
        placket(); buttons((370,430),[y0+140,y0+230,beltY+40,beltY+130],col=(230,220,190,255),r=12)
        belt(col=dk(R,0.55),buck=(200,190,170,255)); folds(4)
    elif cue=='apron':
        collar(dk(R,0.8)); placket(); buttons((400,),[y0+110,y0+190,y0+270,beltY+60],col=(90,70,50,255),r=11)
        dd.line(_S([(260,y0+10),(560,beltY+40)]),fill=(110,84,52,255),width=s(26)); dd.line(_S([(260,y0+10),(560,beltY+40)]),fill=K,width=s(5))
        dd.rounded_rectangle([s(430),s(beltY+20),s(650),s(beltY+190)],s(16),fill=(214,196,150,255),outline=K,width=s(8)); dd.line([s(430),s(beltY+60),s(650),s(beltY+60)],fill=K,width=s(6))
        for k in range(3): dd.rectangle([s(450+k*55),s(beltY+5),s(495+k*55),s(beltY+40)],fill=(240,236,222,255),outline=K,width=s(4))
        folds(3)
    elif cue=='pilgrim':   # cc: doublet buttoned down the front, plain white falling collar, breeches band at the hem
        placket(); buttons((400,),[y0+120,y0+180,y0+240,beltY+20,beltY+80,beltY+140],col=dk(R,0.55),r=11)
        dd.rectangle([0,s(beltY),W,s(beltY+26)],fill=dk(R,0.6)); dd.line([0,s(beltY),W,s(beltY)],fill=K,width=s(5))
        folds(3)
    elif cue=='sailor':   # cc: loose undyed shirt, open neck, coloured sash
        dd.polygon(_S([(400-70,y0-10),(400,y0+120),(400+70,y0-10)]),fill=(246,236,214,255)); dd.line(_S([(400-70,y0-10),(400,y0+120),(400+70,y0-10)]),fill=K,width=s(6))
        dd.rectangle([0,s(beltY),W,s(beltY+46)],fill=tuple(c.get('sash',(170,50,40)))+(255,)); dd.line([0,s(beltY),W,s(beltY)],fill=K,width=s(5)); dd.line([0,s(beltY+46),W,s(beltY+46)],fill=K,width=s(5))
        dd.polygon(_S([(470,beltY+40),(510,beltY+150),(450,beltY+150)]),fill=tuple(c.get('sash',(170,50,40)))+(255,),outline=K)
        folds(3)
    elif cue=='mantle':   # cc: deerskin mantle tied over one shoulder, fringed hem; plain, no costume clichés
        sk=(184,140,92,255)
        dd.polygon(_S([(100,y0-20),(330,y0-20),(700,y1+40),(100,y1+40)]),fill=sk)
        dd.line(_S([(330,y0-20),(700,y1+40)]),fill=K,width=s(7)); dd.line(_S([(120,y0+10),(300,y0+10)]),fill=dk(sk,0.6),width=s(6))
        for k in range(14): x=140+k*38; dd.line([s(x),s(y1-10),s(x+4),s(y1+40)],fill=dk(sk,0.62),width=s(6))
        dd.ellipse([s(290),s(y0-10),s(340),s(y0+40)],fill=(200,190,160,255),outline=K,width=s(5))   # shell tie at the shoulder
        for k in range(3): dd.line(_S([(200+k*90,y0+120+k*60),(160+k*90,y1-60)]),fill=dk(sk,0.78),width=s(5))
    elif cue=='coat18':   # cc: 1740s long coat with big turned cuffs, white neck cloth
        lapels(dk(R,0.78),shirt=(246,242,232,255),depth=160); placket(400,y0+160)
        buttons((360,440),[y0+190,y0+250,beltY+20,beltY+80],col=(214,190,120,255),r=11)
        for sx in(-1,1): dd.rectangle([s(400+sx*150-45),s(beltY+60),s(400+sx*150+45),s(beltY+90)],fill=dk(R,0.65),outline=K,width=s(5))
        folds(4)
    elif cue=='vest':
        dd.polygon(_S([(400-100,y0),(400+100,y0),(400+80,y1),(400-80,y1)]),fill=(240,238,232,255))
        for sx in(-1,1): dd.polygon(_S([(400+sx*100,y0-10),(400+sx*20,y0+260),(400+sx*20,y1),(400+sx*260,y1),(400+sx*260,y0-10)]),fill=dk(R,0.8),outline=K,width=s(7))
        for y in range(y0+80,y1,70): dd.line([0,s(y),s(380),s(y)],fill=K,width=s(4)); dd.line([s(420),s(y),W,s(y)],fill=K,width=s(4))
        folds(3)
    # clip detail to the garment, paste
    clip=Image.new('RGBA',(W,H),(0,0,0,0)); clip.paste(det,(0,0),Image.composite(det.split()[3],Image.new('L',(W,H),0),gm))
    im.alpha_composite(clip); d=ImageDraw.Draw(im)
    if cue=='pilgrim':   # cc: plain white falling collar over the shoulders
        d.chord([s(400-215),s(y0-70),s(400+215),s(y0+150)],0,180,fill=(248,246,238,255),outline=K,width=s(8)); d.line([s(400),s(y0+40),s(400),s(y0+148)],fill=K,width=s(6))
    if cue=='scarf':   # scarf sits over the coat and the shoulder line
        sc=tuple(c['scarf'])+(255,)
        d.rounded_rectangle([s(400-150),s(y0-24),s(400+150),s(y0+56)],s(30),fill=sc,outline=K,width=s(BOUT-4))
        d.rounded_rectangle([s(450),s(y0+30),s(520),s(y0+330)],s(16),fill=sc,outline=K,width=s(BOUT-4))
        for yy in (y0+110,y0+190): d.line([s(452),s(yy),s(518),s(yy)],fill=(250,250,250,255),width=s(16))
        for k in range(5): d.line([s(458+k*14),s(y0+330),s(458+k*14),s(y0+362)],fill=sc,width=s(6))
    d.line(_S(pts+[pts[0]]),fill=K,width=s(BOUT),joint='curve')
    return im.resize((800,1100),Image.LANCZOS)
def arm(name,prop=None,straight=None):
    # r8b (guide v1.3 x.3, rule 253 reversed): ONE smooth noodle stroke, no elbow joint, 5.5 % of head width thick (38 px; head 0.43 m = 694 arm px),
    # ending in a plain round mitten 12 % of head width (83 px), no thumb, no fingers. Drawn straight here; noodle() curves it.
    c=C[name]
    im=Image.new('RGBA',(400,900),(0,0,0,0)); d=ImageDraw.Draw(im)
    def mitt(): d.ellipse([158,670,242,754],fill=K)
    mitt()
    if prop=='bag': d.rectangle([90,760,310,890],fill=(200,170,120,255),outline=K,width=11); d.arc([140,700,260,820],180,360,fill=K,width=9); d.rectangle([150,790,250,830],fill=(200,40,40,255)); d.line([100,800,300,800],fill=dk((200,170,120),0.7),width=4)
    if prop=='box': d.rectangle([100,740,300,880],fill=(60,120,180,255),outline=K,width=11); d.line([200,740,200,880],fill=(250,230,120,255),width=16); d.line([100,810,300,810],fill=(250,230,120,255),width=16); d.polygon([(100,740),(140,740),(100,780)],fill=(40,96,150,255))
    if prop=='chalk': d.rectangle([186,740,214,800],fill=(250,250,250,255),outline=K,width=6)
    if prop=='pen': d.line([200,720,200,880],fill=(20,20,24,255),width=16); d.polygon([(192,880),(208,880),(200,900)],fill=K)
    if prop=='redpen': d.line([200,720,200,880],fill=(196,30,30,255),width=16); d.polygon([(192,880),(208,880),(200,900)],fill=K)
    if prop=='megaphone': d.polygon([(180,720),(220,720),(330,890),(70,890)],fill=(236,230,220,255),outline=K); d.ellipse([70,860,330,900],fill=(60,60,64,255),outline=K,width=8); d.line([200,724,200,860],fill=(200,190,176,255),width=6)
    if prop=='pennant': d.line([200,600,200,120],fill=(120,80,40,255),width=12); d.polygon([(200,120),(390,180),(200,250)],fill=tuple(c.get('scarf',(40,60,140)))+(255,),outline=K)
    if prop=='camera': d.rounded_rectangle([110,720,290,840],20,fill=(40,40,44,255),outline=K,width=12); d.ellipse([160,740,240,820],fill=(120,140,170,255),outline=K,width=8)
    if prop=='paper': d.rectangle([60,640,340,860],fill=(238,232,214,255),outline=K,width=10); d.text((80,660),'BLACK\nFRIDAY',fill=K)
    if prop=='musket': d.line([200,860,200,60],fill=(90,64,44,255),width=26); d.line([200,860,200,60],fill=K,width=6); d.line([200,300,200,60],fill=(70,70,76,255),width=14); d.polygon([(178,860),(222,860),(236,900),(164,900)],fill=(90,64,44,255),outline=K); mitt()
    if prop=='shovel': d.line([200,860,200,200],fill=(130,96,60,255),width=18); d.line([200,860,200,200],fill=K,width=4); d.polygon([(150,860),(250,860),(240,900),(160,900)],fill=(120,120,126,255),outline=K); d.rectangle([170,180,230,210],fill=(130,96,60,255),outline=K,width=6); mitt()
    if prop=='spyglass': d.rounded_rectangle([170,560,230,760],12,fill=(170,130,60,255),outline=K,width=8); d.rectangle([178,560,222,600],fill=(90,70,40,255)); mitt()
    if prop=='quill': d.line([200,720,240,520],fill=(246,244,238,255),width=22); d.line([200,720,240,520],fill=K,width=4); d.line([200,720,196,780],fill=K,width=6); mitt()
    if prop=='bow': d.arc([60,100,340,900],300,60,fill=(120,84,50,255),width=18); d.line([200,120,200,880],fill=(230,222,200,255),width=4); mitt()
    if prop=='cane': d.line([200,720,200,900],fill=(90,60,40,255),width=18); d.arc([150,660,250,760],180,360,fill=(90,60,40,255),width=18); mitt()
    if prop=='basket': d.rounded_rectangle([90,740,310,890],30,fill=(170,128,70,255),outline=K,width=10); [d.line([100,770+k*36,300,770+k*36],fill=(120,84,44,255),width=5) for k in range(3)]; [d.ellipse([110+k*36,712,150+k*36,752],fill=[(214,170,60,255),(190,60,40,255),(120,60,110,255)][k%3],outline=K,width=5) for k in range(6)]; d.arc([110,640,290,800],180,360,fill=K,width=10); mitt()
    if prop=='oar': d.line([200,900,200,100],fill=(150,110,70,255),width=20); d.line([200,900,200,100],fill=K,width=4); mitt()
    if prop=='lantern': d.line([200,700,200,760],fill=K,width=6); d.rounded_rectangle([150,760,250,880],12,fill=(255,214,120,255),outline=K,width=9); d.rectangle([140,750,260,770],fill=(60,50,44,255)); mitt()
    if prop=='phone': d.rounded_rectangle([160,640,240,780],12,fill=(40,40,48,255),outline=K,width=8); mitt()
    if prop in ('box','bag','paper','megaphone','camera'): mitt()   # the mitten sits over the prop so it is held, not floating
    return noodle(im,BEND.get(prop,18) if straight is None else straight)
# r7 (owner Nov 19: forearms stuck out sideways and swung across faces): natural hang 18 deg; 'armS' = straight card for raised and gripping arms
BEND={'musket':0,'shovel':6,'spyglass':25,'quill':30,'bow':4,'cane':10,'basket':22,'oar':0,'lantern':18,'phone':28,'pennant':0,'megaphone':15,'paper':20,'bag':20,'box':25,'camera':25,'chalk':30,'pen':30,'redpen':30}
AW=38
NBOW=110   # r4: control-point offset in px (sagitta = NBOW/2)
def noodle(hand,deg,ey=330):
    # the hand (with its prop) swings outward by deg about a point 330 px down; the arm is one quadratic curve from the shoulder to the hand
    W,H=hand.size; out=Image.new('RGBA',(W*3,H),(0,0,0,0)); X=W*3//2
    lay=Image.new('RGBA',(W*3,H),(0,0,0,0)); lay.paste(hand,(W,0),hand)
    if deg: lay=lay.rotate(deg,resample=Image.BICUBIC,center=(X,ey))   # PIL rotates counter-clockwise: the hand swings to +x (outward)
    a=math.radians(deg); hx=X+(712-ey)*math.sin(a); hy=ey+(712-ey)*math.cos(a)
    sx0,sy0=X,40; cxp,cyp=X,(sy0+hy)/2+40   # control point straight below the shoulder: leaves the shoulder down, bends smoothly into the hand
    # r4 (visual verifier r3, must-have 3: every arm read as a straight stick; guide x.3: 85 of 113 Rick arms are curved noodles):
    # bow the curve sideways so the arm reads as a soft noodle (~35-40 deg total turn, sagitta ~55 px on a 670 px arm), elbow side outward
    mx_,my_=(sx0+hx)/2,(sy0+hy)/2; dx_,dy_=hx-sx0,hy-sy0; ln_=math.hypot(dx_,dy_) or 1
    nx_,ny_=dy_/ln_,-dx_/ln_
    if nx_<0: nx_,ny_=-nx_,-ny_
    cxp,cyp=mx_+nx_*NBOW,my_+ny_*NBOW
    P=[((1-t)**2*sx0+2*(1-t)*t*cxp+t*t*hx,(1-t)**2*sy0+2*(1-t)*t*cyp+t*t*hy) for t in [i/40 for i in range(41)]]
    big=Image.new('RGBA',(W*3*SS,H*SS),(0,0,0,0)); bd=ImageDraw.Draw(big)
    bd.line([(x*SS,y*SS) for x,y in P],fill=K,width=AW*SS,joint='curve')
    for x,y in (P[0],P[-1]): bd.ellipse([(x-AW/2)*SS,(y-AW/2)*SS,(x+AW/2)*SS,(y+AW/2)*SS],fill=K)
    out.alpha_composite(big.resize((W*3,H),Image.LANCZOS)); out.alpha_composite(lay)
    return out
def elbow(im,dx,ey=330,wy=640):
    # round 5 (B4): never a dead-straight arm. Shear the forearm sideways so the elbow reads at ~165 deg (Rick hanging arms 155-175)
    if not dx: return im
    a=np.asarray(im); out=np.zeros_like(a); H=a.shape[0]
    for y in range(H):
        sh=0 if y<ey else int(round(dx*min(1.0,(y-ey)/(wy-ey))))
        if sh: out[y,sh:]=a[y,:-sh]
        else: out[y]=a[y]
    return Image.fromarray(out)
def head_shade(im,skin):
    # Rick heads: soft cel shadow crescent on the lower-left of the face disc
    m=Image.new('L',im.size,0); md=ImageDraw.Draw(m); md.ellipse([160,167,885,892],fill=255); md.ellipse([200,107,945,852],fill=0)
    m=m.filter(ImageFilter.GaussianBlur(10))
    cl=Image.new('L',im.size,0); ImageDraw.Draw(cl).ellipse([160,167,885,892],fill=255)   # r8b: shade stays inside the ink
    from PIL import ImageChops; m=ImageChops.multiply(m,cl)
    sh=Image.new('RGBA',im.size,dk(skin,0.88)); im.paste(sh,(0,0),m)
if __name__=='__main__':
    out={}
    for n,c in C.items():
        for fk in c['faces']: head(n,fk).save(f'{T}{n}_h_{fk}.png')
        body(n).save(f'{T}{n}_body.png'); body(n,1).save(f'{T}{n}_bodyw1.png'); body(n,2).save(f'{T}{n}_bodyw2.png')
        for p in c.get('props',[None]): arm(n,p).save(f'{T}{n}_arm{"_"+p if p else ""}.png')
        arm(n).save(f'{T}{n}_arm.png'); arm(n,straight=4).save(f'{T}{n}_armS.png')
        # r7 (rule 272): left arms get their own mirrored texture, never a negative object scale (the PC GPU drew a mirrored card as a black box)
        import glob as _g
        for fp in _g.glob(f'{T}{n}_arm*.png'):
            if fp.endswith('_L.png'): continue
            Image.open(fp).transpose(Image.FLIP_LEFT_RIGHT).save(fp[:-4]+'_L.png')
    # preview
    pv=Image.new('RGBA',(300*len(C),700),(236,230,218,255))
    for i,n in enumerate(C):
        b=Image.open(f'{T}{n}_body.png').resize((240,330)); h=Image.open(f'{T}{n}_h_{list(C[n]["faces"])[0]}.png').resize((260,260))
        pv.alpha_composite(b,(i*300+30,330)); pv.alpha_composite(h,(i*300+20,110))
    pv.convert('RGB').save('/root/cc/cast_preview.jpg')
    faces=[]
    for n,c in C.items():
        for fk in c['faces']: faces.append(Image.open(f'{T}{n}_h_{fk}.png').resize((128,128)))
    sh=Image.new('RGBA',(128*16,128*((len(faces)+15)//16)),(236,230,218,255))
    for i,f in enumerate(faces): sh.alpha_composite(f,((i%16)*128,(i//16)*128))
    sh.convert('RGB').save('/root/cc/faces_sheet.jpg'); print('CAST_OK',len(faces),'faces')
