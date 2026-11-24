# Painted textures for the Nuremberg Christkindlesmarkt short (fri-nuremberg). PIL only, our own designs (generic painters from the Cape Cod paint_cc.py; every Nuremberg texture below is new). Output /root/nb/tex/
# Reuses only the generic painter helpers of the Black Friday paint.py (wash, strokes, paintdetail, sky): no BF texture is reused.
import sys; sys.path.insert(0,'/root/nb/src')
import paint as P
P.T='/root/nb/tex/'; T=P.T
import numpy as np, random, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from paint import wash, strokes, paintdetail, noise, jl, jr, mul, text, font, FS, FSN, FM, INK
FSI='/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf'
def full(): return Image.new('L',(1,1),255)
def det(im,base,seed,dens=1.0,K=1): return paintdetail(im,Image.new('L',im.size,255),base,seed,K,dens=dens)
# ---------------- ground ----------------
def sand(name='sand',base=(222,196,150),seed=1,W=1024,H=1024,ripples=True):
    im=wash(W,H,base,0.10,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    if ripples:
        for k in range(70):
            y=r.uniform(0,H); x0=r.uniform(-200,W); L=r.uniform(120,380); amp=r.uniform(3,7)
            pts=[(x0+t,y+amp*math.sin(t/18+k)) for t in range(0,int(L),8)]
            d.line(pts,fill=mul(base,0.82),width=3); d.line([(x,y_+3) for x,y_ in pts],fill=mul(base,1.08),width=2)
    for _ in range(2600):   # shell grit and pebbles
        x,y=r.uniform(0,W),r.uniform(0,H); s=r.uniform(1,3.2); c=r.choice([mul(base,0.6),mul(base,1.12),(150,140,128),(236,226,210)])
        d.ellipse([x-s,y-s,x+s,y+s],fill=c)
    im=strokes(im,1600,mul(base,0.86),seed+3,6,20,2,60); im.save(T+name+'.png')
def water(name='water',base=(52,108,128),seed=2,W=1024,H=1024,foam=0.0):
    im=wash(W,H,base,0.12,seed); d=ImageDraw.Draw(im,'RGBA'); r=random.Random(seed)
    for _ in range(900):   # painted wave strokes: dark troughs, light crests
        x,y=r.uniform(0,W),r.uniform(0,H); L=r.uniform(14,60); c=mul(base,r.uniform(0.62,0.8))+(170,)
        d.arc([x,y,x+L,y+L*0.3],190,350,fill=c,width=3)
    for _ in range(700):
        x,y=r.uniform(0,W),r.uniform(0,H); L=r.uniform(10,40); c=mul(base,r.uniform(1.25,1.6))+(150,)
        d.arc([x,y,x+L,y+L*0.28],200,340,fill=c,width=2)
    if foam:
        for _ in range(int(500*foam)):
            x,y=r.uniform(0,W),r.uniform(0,H); s=r.uniform(4,16); d.ellipse([x-s,y-s*0.5,x+s,y+s*0.5],fill=(240,244,240,r.randint(120,220)))
    im=det(im.convert('RGB'),base,seed+50,0.7); im.save(T+name+'.png')
def planks(name,base,seed,W=1024,H=1024,pw=86,nails=True,vertical=False):
    im=wash(W,H,base,0.06,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for j in range(0,H,pw):
        c=mul(base,r.uniform(0.84,1.12)); d.rectangle([0,j,W,j+pw-4],fill=c); jl(d,[(0,j),(W,j)],6,mul(base,0.36),j)
        x=r.uniform(0,W); jl(d,[(x,j),(x,j+pw)],5,mul(base,0.36),j+1)
        for k in range(9):   # wood grain
            yy=j+r.uniform(8,pw-10); xx=r.uniform(-100,W); L=r.uniform(80,300)
            d.line([(xx+t,yy+2*math.sin(t/30+k)) for t in range(0,int(L),10)],fill=mul(c,0.74),width=2)
        for k in range(2): kx,ky=r.uniform(0,W),j+r.uniform(18,pw-22); d.ellipse([kx-12,ky-6,kx+12,ky+6],outline=mul(c,0.6),width=3)
        if nails:
            for xx in (x-20,x+20): d.ellipse([xx-4,j+pw/2-4,xx+4,j+pw/2+4],fill=mul(base,0.3))
    im=det(im,base,seed+900)
    if vertical: im=im.rotate(90)
    im.save(T+name+'.png')
def shingles(name='shingle',base=(150,146,138),seed=7,W=1024,H=1024):
    im=wash(W,H,base,0.08,seed); d=ImageDraw.Draw(im); r=random.Random(seed); rh=64
    for j in range(0,H,rh):
        x=-r.uniform(0,60)
        while x<W:
            w=r.uniform(40,90); c=mul(base,r.uniform(0.82,1.14)); d.rectangle([x,j,x+w,j+rh+10],fill=c,outline=mul(base,0.42),width=3)
            for k in range(3): xx=x+r.uniform(5,w-5); d.line([xx,j+6,xx+r.uniform(-2,2),j+rh],fill=mul(c,0.78),width=2)
            x+=w
        d.line([0,j+rh+8,W,j+rh+8],fill=mul(base,0.4),width=5)
    det(im,base,seed+900).save(T+name+'.png')
def stone(name,base,seed,W=1024,H=1024,carve=None):
    im=wash(W,H,base,0.14,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for _ in range(3000):
        x,y=r.uniform(0,W),r.uniform(0,H); s=r.uniform(1,4); d.ellipse([x-s,y-s,x+s,y+s],fill=r.choice([mul(base,0.65),mul(base,1.2),(236,232,226),(70,66,64)]))
    for k in range(14): jl(d,[(r.uniform(0,W),r.uniform(0,H)) for _ in range(4)],3,mul(base,0.55),k,6)
    im=strokes(im,1400,mul(base,0.8),seed+4,6,22,2,70)
    if carve:
        f=font(FS,300); d=ImageDraw.Draw(im)
        text(d,(W/2+6,H*0.56+8),carve,f,mul(base,1.25)); text(d,(W/2,H*0.56),carve,f,mul(base,0.45))
    det(im,base,seed+900).save(T+name+'.png')
def sky(name,top,bot,seed,clouds,cloud,W=1024,H=2048):
    """P.sky made tileable: each cloud is also drawn one width left and right, so the 5x-repeated dome shows no cut cloud edges"""
    from PIL import ImageFilter
    y=np.linspace(0,1,H)[:,None,None]; a=np.array(top,np.float32)*(1-y**0.8)+np.array(bot,np.float32)*(y**0.8); a=np.repeat(a,W,1)
    im=Image.fromarray(a.astype(np.uint8)).convert('RGBA'); r=random.Random(seed)
    for k in range(clouds):
        cx,cy=r.uniform(0,W),r.uniform(H*0.12,H*0.55); s=r.uniform(50,120)
        blob=Image.new('RGBA',(W,H),(0,0,0,0)); bd=ImageDraw.Draw(blob)
        for q in range(9):
            ox,oy=r.uniform(-2.2,2.2)*s,r.uniform(-0.5,0.3)*s; rr=s*r.uniform(0.5,0.9)
            for sh in (-W,0,W): bd.ellipse([cx+ox-rr+sh,cy+oy-rr,cx+ox+rr+sh,cy+oy+rr*0.8],fill=cloud+(255,))
        im=Image.alpha_composite(im,blob)
        big=Image.new('L',(W*3,H)); al=blob.split()[3]
        for i in range(3): big.paste(al,(i*W,0))
        e=big.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(7)).crop((W,0,2*W,H))
        ol=Image.new('RGBA',(W,H),(70,74,96,0)); ol.putalpha(e.point(lambda v:200 if v>40 else 0)); im=Image.alpha_composite(im,ol)
    im.convert('RGB').save(T+name+'.png')
def dunes_far(name,W=4096,H=900,seed=11,base=(214,186,138),grass=(122,134,70),water_=(60,110,136)):
    """far shore card: low dunes with beach grass and a strip of sea, alpha above the dune line"""
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); r=random.Random(seed)
    yline=[H*0.42+70*math.sin(x/260+seed)+40*math.sin(x/97) for x in range(0,W+8,8)]
    d.polygon([(0,H)]+[(i*8,y) for i,y in enumerate(yline)]+[(W,H)],fill=base+(255,))
    for i,y in enumerate(yline[::3]):
        x=i*24
        for k in range(r.randint(2,5)):
            gx=x+r.uniform(-10,10); d.line([gx,y+6,gx+r.uniform(-14,14),y-r.uniform(20,60)],fill=mul(grass,r.uniform(0.8,1.2))+(255,),width=4)
    a=np.asarray(im).copy(); m=a[...,3]>0
    n=(noise(W,H,8,seed)-0.5)*40; a[...,:3]=np.where(m[...,None],np.clip(a[...,:3]+n[...,None],0,255),a[...,:3]); im=Image.fromarray(a.astype(np.uint8))
    d=ImageDraw.Draw(im); jl(d,[(i*8,y) for i,y in enumerate(yline)],5,(110,84,60),seed,1.5)
    im.save(T+name+'.png')
def treeline(name,W=4096,H=1200,seed=12,base=(54,84,62)):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); r=random.Random(seed); x=0
    while x<W:   # scrub pines and oaks: stacked ink-edged blobs
        h=r.uniform(H*0.45,H*0.95); w=r.uniform(110,220); c=mul(base,r.uniform(0.75,1.2))
        d.rectangle([x+w/2-10,H-h*0.35,x+w/2+10,H],fill=(84,62,46,255),outline=(46,30,30,255),width=4)
        for k in range(6):
            cy=H-h+k*h*0.11; rr=w*(0.35+0.08*k)*r.uniform(0.8,1.1)
            d.ellipse([x+w/2-rr,cy-rr*0.8,x+w/2+rr,cy+rr*0.8],fill=mul(c,1-0.05*k)+(255,),outline=(46,34,40,255),width=5)
        x+=w*r.uniform(0.45,0.8)
    d.rectangle([0,H*0.86,W,H],fill=mul(base,0.7)+(255,))
    a=np.asarray(im).copy(); m=a[...,3]>0; n=(noise(W,H,6,seed)-0.5)*18; a[...,:3]=np.where(m[...,None],np.clip(a[...,:3]+n[...,None],0,255),a[...,:3])
    Image.fromarray(a.astype(np.uint8)).save(T+name+'.png')
def grass_card(name,seed,W=512,H=512,col=(150,150,80)):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); r=random.Random(seed)
    for _ in range(46):
        x=W/2+r.gauss(0,W*0.13); h=r.uniform(H*0.45,H*0.95); bend=r.uniform(-90,90)
        pts=[(x+bend*(t**2),H-h*t) for t in [i/10 for i in range(11)]]
        c=mul(col,r.uniform(0.7,1.25)); d.line(pts,fill=(60,56,40,255),width=11,joint='curve'); d.line(pts,fill=c+(255,),width=6,joint='curve')
    im.save(T+name+'.png')
def card_text(name,lines,bg,fg,W=1024,H=512,f=None,border=None,seed=5,wood=True):
    im=wash(W,H,bg,0.08,seed)
    if wood:
        d=ImageDraw.Draw(im); r=random.Random(seed)
        for k in range(30): yy=r.uniform(0,H); d.line([(t,yy+3*math.sin(t/40+k)) for t in range(0,W,12)],fill=mul(bg,0.8),width=2)
    d=ImageDraw.Draw(im)
    if border: d.rectangle([14,14,W-14,H-14],outline=border,width=16)
    n=len(lines)
    for i,(s,sz) in enumerate(lines):
        ft=font(f or FS,sz)
        while d.textlength(s,font=ft)>W-110: sz-=4; ft=font(f or FS,sz)
        text(d,(W/2,H*(i+0.5)/n+ (8 if n==1 else 0)),s,ft,fg,stroke=2,sf=mul(fg,0.6))
    det(im,bg,seed+900,0.6).save(T+name+'.png')
def chart(name,W=1536,H=1536,seed=30):
    """captain's sea chart: our own drawing of the coast from Cape Cod to the Hudson, dotted course, labels"""
    base=(226,206,160); im=wash(W,H,base,0.10,seed,0.05); d=ImageDraw.Draw(im); r=random.Random(seed)
    sea=(166,190,176)
    # land: north-west mass with the hooked Cape, plus Long Island strip and the Hudson mouth to the south-west
    land=[(0,0),(W*0.78,0),(W*0.74,H*0.20),(W*0.60,H*0.30),(W*0.58,H*0.40),(W*0.70,H*0.44),(W*0.86,H*0.40),(W*0.92,H*0.30),(W*0.86,H*0.24),(W*0.90,H*0.18),(W*0.97,H*0.26),(W*0.97,H*0.48),(W*0.70,H*0.54),(W*0.50,H*0.56),(W*0.30,H*0.64),(W*0.18,H*0.74),(W*0.14,H*0.86),(0,H*0.9)]
    d.rectangle([0,0,W,H],fill=sea); d.polygon(land,fill=(214,190,140),outline=INK); jl(d,land+[land[0]],6,INK,seed,2.0)
    li=[(W*0.10,H*0.95),(W*0.40,H*0.80),(W*0.44,H*0.82),(W*0.14,H*0.98)]; d.polygon(li,fill=(214,190,140)); jl(d,li+[li[0]],5,INK,seed+1,2.0)
    jl(d,[(W*0.12,H*0.88),(W*0.10,H*0.70),(W*0.06,H*0.52),(W*0.04,H*0.30)],9,(120,150,160),seed+2,3.0)   # the Hudson
    for k in range(40): x,y=r.uniform(0,W*0.6),r.uniform(0,H*0.5); d.line([x,y,x+12,y-8],fill=mul((214,190,140),0.75),width=3)  # hatching
    # course: from the open Atlantic (right) toward the Hudson, bent back to the Cape tip
    crs=[(W*0.98,H*0.86),(W*0.80,H*0.74),(W*0.66,H*0.66),(W*0.56,H*0.64)]; ret=[(W*0.56,H*0.64),(W*0.64,H*0.60),(W*0.80,H*0.52),(W*0.90,H*0.34),(W*0.88,H*0.22)]
    for seg in (crs,ret):
        for i in range(len(seg)-1):
            (x0,y0),(x1,y1)=seg[i],seg[i+1]; L=math.hypot(x1-x0,y1-y0); n=int(L/26)
            for k in range(0,n,2): t0,t1=k/n,(k+1)/n; d.line([x0+(x1-x0)*t0,y0+(y1-y0)*t0,x0+(x1-x0)*t1,y0+(y1-y0)*t1],fill=(170,40,34),width=9)
    x,y=W*0.56,H*0.64; d.line([x-26,y-26,x+26,y+26],fill=(170,40,34),width=12); d.line([x-26,y+26,x+26,y-26],fill=(170,40,34),width=12)
    fl=font(FSI,64); text(d,(W*0.26,H*0.60),'HUDSON RIVER',fl,(60,40,30)); text(d,(W*0.80,H*0.14),'CAPE COD',fl,(60,40,30)); text(d,(W*0.72,H*0.90),'ATLANTIC',font(FSI,70),(70,90,96))
    # compass rose
    cx,cy,R_=W*0.28,H*0.26,120
    for a in range(0,360,45):
        L=R_ if a%90==0 else R_*0.6; x1,y1=cx+L*math.sin(math.radians(a)),cy-L*math.cos(math.radians(a))
        d.polygon([(x1,y1),(cx+16*math.cos(math.radians(a)),cy+16*math.sin(math.radians(a))),(cx-16*math.cos(math.radians(a)),cy-16*math.sin(math.radians(a)))],fill=(170,40,34) if a==0 else INK)
    d.ellipse([cx-R_*0.7,cy-R_*0.7,cx+R_*0.7,cy+R_*0.7],outline=INK,width=4)
    d.rectangle([12,12,W-12,H-12],outline=(110,80,52),width=20)
    det(im,base,seed+900,0.5).save(T+name+'.png')
def compact(name,W=1024,H=1400,seed=31,signed=0):
    """the deal on paper: opening words of the 1620 compact (public domain text), signature lines filling in"""
    base=(236,222,184); im=wash(W,H,base,0.08,seed,0.06); d=ImageDraw.Draw(im); r=random.Random(seed)
    f1=font(FSI,58); f2=font(FSI,40)
    text(d,(W/2,120),'In the name of God, Amen.',f1,(50,36,30))
    y=220
    for ln in ['We whose names are underwritten','... do by these presents solemnly','and mutually, in the presence of God','and one of another, covenant and','combine ourselves together into','a civil body politic ...','Cape Cod, the 11th of November']:
        text(d,(W/2,y),ln,f2,(60,44,36)); y+=66
    for k in range(10):   # signature lines
        x=90+(k%2)*450; yy=760+(k//2)*120; d.line([x,yy,x+380,yy],fill=(120,100,80),width=3)
        if k<signed:
            pts=[(x+10+t*36,yy-14-14*math.sin(t*1.7+k)) for t in range(10)]; d.line(pts,fill=(40,30,40),width=6,joint='curve')
    det(im,base,seed+900,0.4).save(T+name+'.png')
def journal(name,W=1536,H=1024,seed=32):
    """an open journal: two pages of hand script about corn, arrows and Plymouth; no rock anywhere"""
    base=(236,224,190); im=wash(W,H,base,0.08,seed,0.05); d=ImageDraw.Draw(im); r=random.Random(seed)
    d.line([W/2,0,W/2,H],fill=(150,120,90),width=10)
    f=font(FSI,46); L=[['Novemb. ... we found','corn in a basket ...','took it, meaning to','pay them again ...'],['Decemb. ... arrows came','flying amongst us ...','none hurt ...','then to Plymouth ...']]
    for p in range(2):
        for i,s in enumerate(L[p]):
            x0=80+p*W/2; y=140+i*190; d.text((x0,y),s,font=f,fill=(50,40,40))
            for k in range(2): yy=y+80+k*45; d.line([x0,yy,x0+r.uniform(380,600),yy],fill=(120,110,110),width=3)
    det(im,base,seed+900,0.4).save(T+name+'.png')
def basket(name='basket',W=512,H=512,seed=33,base=(170,128,70)):
    im=wash(W,H,base,0.06,seed); d=ImageDraw.Draw(im)
    for j in range(0,H,26):
        for i in range(0,W,40): o=(j//26)%2*20; d.rounded_rectangle([i+o,j+2,i+o+36,j+24],8,fill=mul(base,1.1 if (i//40+j//26)%2 else 0.86),outline=mul(base,0.5),width=3)
    det(im,base,seed+900,0.5).save(T+name+'.png')
def corn(name='corn',W=512,H=512,seed=34):
    im=Image.new('RGB',(W,H),(140,70,40)); d=ImageDraw.Draw(im); r=random.Random(seed)
    for j in range(0,H,22):
        for i in range(0,W,22): c=r.choice([(214,170,60),(190,60,40),(120,60,110),(236,210,140),(220,140,50)]); d.ellipse([i+2,j+2,i+20,j+20],fill=c,outline=(90,50,40),width=2)
    det(im,(190,120,60),seed+900,0.4).save(T+name+'.png')
def sail(name='sail',base=(232,220,192),seed=35,W=1024,H=1024):
    im=wash(W,H,base,0.08,seed,0.04); d=ImageDraw.Draw(im)
    for x in range(0,W,128): d.line([x,0,x,H],fill=mul(base,0.82),width=4)   # canvas panel seams
    for y in range(0,H,256): d.line([0,y,W,y],fill=mul(base,0.86),width=3)
    for _ in range(40): x,y=random.uniform(0,W),random.uniform(0,H); d.ellipse([x-30,y-20,x+30,y+20],fill=mul(base,0.93))   # weather stains
    det(im,base,seed+900,0.7).save(T+name+'.png')
def deerskin(name='deerskin',base=(156,112,72),seed=36,W=512,H=512):
    im=wash(W,H,base,0.12,seed); im=strokes(im,500,mul(base,0.8),seed,8,30,3,90); det(im,base,seed+900,0.8).save(T+name+'.png')
def fx_cards():
    # smoke puff, splash, sand spray, sparkle: flat FX cards (Rick flat FX 12-27 f)
    for nm,col,seed in (('fx_smoke',(236,232,226),1),('fx_splash',(230,244,248),2),('fx_sand',(230,206,160),3)):
        W=H=512; im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); r=random.Random(seed)
        for k in range(9):
            a=r.uniform(0,2*math.pi); rr=r.uniform(60,150); x=W/2+math.cos(a)*r.uniform(0,110); y=H/2+math.sin(a)*r.uniform(0,90)
            if nm=='fx_splash': y=H*0.55-abs(math.sin(a))*r.uniform(0,160)
            d.ellipse([x-rr*0.6,y-rr*0.5,x+rr*0.6,y+rr*0.5],fill=col+(255,),outline=(70,60,70,255),width=9)
        for k in range(9):
            a=r.uniform(0,2*math.pi); rr=r.uniform(40,120); x=W/2+math.cos(a)*r.uniform(0,90); y=H/2+math.sin(a)*r.uniform(0,70)
            if nm=='fx_splash': y=H*0.55-abs(math.sin(a))*r.uniform(0,150)
            d.ellipse([x-rr*0.55,y-rr*0.45,x+rr*0.55,y+rr*0.45],fill=col+(255,))
        im.save(T+nm+'.png')
    W=H=256; im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    for a in range(0,360,45): d.line([128,128,128+110*math.cos(math.radians(a)),128+110*math.sin(math.radians(a))],fill=(255,240,190,255),width=14 if a%90==0 else 8)
    im.save(T+'fx_spark.png')
def glow(name='glow',W=256,H=256):
    yy,xx=np.mgrid[0:H,0:W]; r=np.sqrt((xx-W/2)**2+(yy-H/2)**2)/(W/2); a=np.clip(1-r,0,1)**2
    im=np.zeros((H,W,4),np.uint8); im[...,:3]=255; im[...,3]=(a*255).astype(np.uint8); Image.fromarray(im).save(T+name+'.png')
def interior_wall(name,base,seed):
    planks(name,base,seed,vertical=True)

# ======================= Nuremberg (fri-nuremberg) textures, all new =======================
def cobble(name='cobble',base=(118,112,110),seed=60,W=1024,H=1024,snow=0.0):
    im=wash(W,H,mul(base,0.55),0.06,seed); d=ImageDraw.Draw(im); r=random.Random(seed); s_=42
    for j in range(0,H+s_,s_):
        off=(j//s_%2)*s_/2
        for i in range(-1,W//s_+2):
            x=i*s_+off+r.uniform(-4,4); y=j+r.uniform(-3,3); c=mul(base,r.uniform(0.8,1.15))
            d.rounded_rectangle([x+3,y+3,x+s_-3,y+s_-3],10,fill=c); d.arc([x+6,y+6,x+s_-6,y+s_-6],200,300,fill=mul(c,1.2),width=3)
    if snow:
        sn=Image.new('L',(W,H),0); sd=ImageDraw.Draw(sn)
        for _ in range(int(900*snow)): x,y=r.uniform(0,W),r.uniform(0,H); rr=r.uniform(8,40); sd.ellipse([x-rr,y-rr*0.6,x+rr,y+rr*0.6],fill=255)
        sn=sn.filter(ImageFilter.GaussianBlur(3)); im=Image.composite(Image.new('RGB',(W,H),(236,240,248)),im,sn)
    det(im,base,seed+900,0.7).save(T+name+'.png')
def snowfield(name='snow',base=(232,236,246),seed=61,W=1024,H=1024):
    im=wash(W,H,base,0.05,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for k in range(60):
        y=r.uniform(0,H); x0=r.uniform(-200,W); L=r.uniform(120,380)
        pts=[(x0+t,y+5*math.sin(t/30+k)) for t in range(0,int(L),8)]; d.line(pts,fill=(206,214,232),width=4)
    for _ in range(800): x,y=r.uniform(0,W),r.uniform(0,H); d.ellipse([x-1.5,y-1.5,x+1.5,y+1.5],fill=(255,255,255))
    im.save(T+name+'.png')
def timber(name,wall,beam,seed,W=1024,H=1536,floors=3,lit=0.5,gable=True,snowroof=False):
    """Franconian half-timbered townhouse front (Fachwerk): beams in an X/K pattern, small-paned windows, our own drawing"""
    r=random.Random(seed); im=wash(W,H,wall,0.07,seed,0.05); d=ImageDraw.Draw(im); bw=30
    top=200 if gable else 40; gf=int(H*0.30); fh=(H-gf-top)//floors
    if gable:
        sky=Image.new('RGBA',(W,H),(0,0,0,0)); sdr=ImageDraw.Draw(sky)
        d.polygon([(0,0),(W*0.5-40,0),(0,top+60)],fill=(0,0,0)); d.polygon([(W,0),(W*0.5+40,0),(W,top+60)],fill=(0,0,0))
    for f in range(floors+1):
        y=top+f*fh; d.rectangle([0,y-bw//2,W,y+bw//2],fill=beam); jl(d,[(0,y-bw//2),(W,y-bw//2)],4,INK,f)
    for f in range(floors):
        y0=top+f*fh; y1=y0+fh
        for c in range(4):
            x0=c*W/4; x1=x0+W/4; d.rectangle([x0-bw//2,y0,x0+bw//2,y1],fill=beam)
            if c in(0,3):
                d.line([(x0+10,y1-10),(x1-10,y0+fh*0.45)],fill=beam,width=bw-6) if c==0 else d.line([(x1-10,y1-10),(x0+10,y0+fh*0.45)],fill=beam,width=bw-6)
            else:
                cx=(x0+x1)/2; wv=W/4*0.30; wy0=y0+fh*0.22; wy1=y0+fh*0.74
                on=r.random()<lit; gl=(252,206,120) if on else (52,60,78)
                d.rectangle([cx-wv-14,wy0-14,cx+wv+14,wy1+14],fill=beam); d.rectangle([cx-wv,wy0,cx+wv,wy1],fill=gl)
                for k in (1,2): d.line([cx-wv,wy0+(wy1-wy0)*k/3,cx+wv,wy0+(wy1-wy0)*k/3],fill=beam,width=6)
                d.line([cx,wy0,cx,wy1],fill=beam,width=8); jr(d,cx-wv,wy0,cx+wv,wy1,3,seed=f*7+c)
                d.rectangle([cx-wv-20,wy1+10,cx+wv+20,wy1+30],fill=mul(beam,1.2))
                if on and r.random()<0.6: d.polygon([(cx-26,wy1-4),(cx,wy1-50),(cx+26,wy1-4)],fill=(60,120,70))   # small Advent tree in the window
        d.rectangle([W-bw//2,y0,W,y1],fill=beam)
    # ground floor: arched door and shop window
    gy=H-gf; d.rectangle([0,gy,W,H],fill=mul(wall,0.86)); d.rectangle([0,gy-bw//2,W,gy+bw//2],fill=beam)
    d.rounded_rectangle([W*0.12,gy+gf*0.25,W*0.36,H],60,fill=(90,56,36)); jr(d,W*0.12,gy+gf*0.25,W*0.36,H,3,seed=seed)
    d.rectangle([W*0.48,gy+gf*0.2,W*0.88,gy+gf*0.75],fill=(252,214,140) if r.random()<0.8 else (60,66,80)); jr(d,W*0.48,gy+gf*0.2,W*0.88,gy+gf*0.75,3,seed=seed+1)
    im=det(im,wall,seed+900,0.5)
    if gable:
        a=Image.new('L',(W,H),255); ad=ImageDraw.Draw(a); ad.polygon([(0,0),(W*0.5,0),(0,top+60)],fill=0); ad.polygon([(W,0),(W*0.5,0),(W,top+60)],fill=0)
        im=im.convert('RGBA'); im.putalpha(a)
        d=ImageDraw.Draw(im); d.line([(0,top+60),(W*0.5,0),(W,top+60)],fill=INK,width=14)
    im.save(T+name+'.png')
def stall_roof(name='stall_roof',W=1024,H=512,seed=62,a=(200,40,46),b=(246,242,234)):
    im=Image.new('RGB',(W,H),b); d=ImageDraw.Draw(im); n=8
    for k in range(n):
        if k%2==0: d.rectangle([k*W/n,0,(k+1)*W/n,H],fill=a)
    for k in range(n+1): d.line([k*W/n,0,k*W/n,H],fill=mul(a,0.6),width=3)
    for k in range(n): d.arc([k*W/n,H-70,(k+1)*W/n,H+30],0,180,fill=mul(a,0.6),width=6)
    det(im,a,seed,0.4).save(T+name+'.png')
def stall_front(name,txt,seed,W=1024,H=512,col=(150,104,64)):
    im=wash(W,H,col,0.06,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for k in range(0,W,90): d.rectangle([k,0,k+86,H],fill=mul(col,r.uniform(0.85,1.1))); d.line([k,0,k,H],fill=mul(col,0.5),width=4)
    d.rectangle([60,40,W-60,170],fill=(250,244,228)); d.rectangle([60,40,W-60,170],outline=(40,30,26),width=8)
    ft=font(FS,96)
    while d.textlength(txt,font=ft)>W-180: ft=font(FS,ft.size-4)
    text(d,(W/2,106),txt,ft,(150,36,40))
    for k in range(14):   # goods on the counter: gingerbread hearts, candles, ornaments
        x=80+k*62; y=300+r.uniform(-14,14); kind=k%3
        if kind==0: d.polygon([(x,y),(x-24,y-24),(x-12,y-40),(x,y-28),(x+12,y-40),(x+24,y-24)],fill=(150,90,40),outline=(40,30,26)); d.line([x-14,y-24,x+14,y-24],fill=(250,250,250),width=4)
        elif kind==1: d.ellipse([x-20,y-40,x+20,y],fill=r.choice([(200,40,46),(214,180,60),(60,110,170)]),outline=(40,30,26),width=4)
        else: d.rectangle([x-8,y-50,x+8,y],fill=(240,230,200),outline=(40,30,26),width=3); d.ellipse([x-5,y-64,x+5,y-50],fill=(255,200,90))
    im.save(T+name+'.png')
def sky_dusk(name='sky_dusk',W=1024,H=2048,seed=63):
    yy=np.linspace(0,1,H)[:,None]; top=np.array([30,44,96]); mid=np.array([70,90,160]); bot=np.array([236,150,120])
    c=np.where(yy<0.6, top+(mid-top)*(yy/0.6), mid+(bot-mid)*((yy-0.6)/0.4)); im=np.broadcast_to(c[:,None,:],(H,W,3)).astype(np.uint8).copy()
    img=Image.fromarray(im); d=ImageDraw.Draw(img); r=random.Random(seed)
    for _ in range(140): x,y=r.uniform(0,W),r.uniform(0,H*0.5); s_=r.uniform(1,3); d.ellipse([x-s_,y-s_,x+s_,y+s_],fill=(250,246,220))
    for k in range(5):
        x=r.uniform(0,W); y=r.uniform(H*0.35,H*0.7); w=r.uniform(160,380)
        d.ellipse([x-w,y-28,x+w,y+28],fill=(120,110,170)); d.ellipse([x-w*0.7,y-50,x+w*0.5,y+10],fill=(140,124,180))
    img.save(T+name+'.png')
def church_stone(name='church',base=(176,120,96),seed=64):
    stone(name,base,seed)
def bentbox_note(name,state,W=1400,H=900,seed=65):
    """underside of the bentwood box: the ink inscription; state 'blob' (third digit smudged), 'two' / 'seven' (hover ghosts), 'reveal' (7 traced)"""
    base=(222,186,132); im=wash(W,H,base,0.08,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for k in range(40): y=r.uniform(0,H); d.line([(t,y+4*math.sin(t/60+k)) for t in range(0,W,14)],fill=mul(base,0.86),width=3)   # pine grain
    ink=(46,36,40); ft=font(FSI,74)
    for i,ln in enumerate(['Regina Susanna Harßdörfferin von der','Jungfrau Susanna Eleonora Elbsin zum','Kindles marck überschickt']):
        d.text((90,140+i*130),ln,font=ft,fill=ink)
    fy=font(FSI,150); x0=420; y0=560
    for k,ch in enumerate('16?8'):
        if ch!='?': d.text((x0+k*120,y0),ch,font=fy,fill=ink)
    gx=x0+2*120+40; gy=y0+90
    if state in('two','seven'):
        g=Image.new('RGBA',(W,H),(0,0,0,0)); gd=ImageDraw.Draw(g); gd.text((x0+2*120,y0),'2' if state=='two' else '7',font=fy,fill=(200,40,40,200)); im=Image.alpha_composite(im.convert('RGBA'),g).convert('RGB'); d=ImageDraw.Draw(im)
    if state!='reveal':
        for k in range(16): a=r.uniform(0,2*math.pi); rr=r.uniform(20,62); d.ellipse([gx+math.cos(a)*rr*0.8-rr*0.6,gy+math.sin(a)*rr*0.7-rr*0.5,gx+math.cos(a)*rr*0.8+rr*0.6,gy+math.sin(a)*rr*0.7+rr*0.5],fill=ink)
        if state in('two','seven'):
            g=Image.new('RGBA',(W,H),(0,0,0,0)); gd=ImageDraw.Draw(g); gd.text((x0+2*120,y0),'2' if state=='two' else '7',font=fy,fill=(220,50,50,170),stroke_width=4,stroke_fill=(255,255,255,200)); im=Image.alpha_composite(im.convert('RGBA'),g).convert('RGB')
    else:
        for k in range(16): a=r.uniform(0,2*math.pi); rr=r.uniform(20,62); d.ellipse([gx+math.cos(a)*rr*0.8-rr*0.6,gy+math.sin(a)*rr*0.7-rr*0.5,gx+math.cos(a)*rr*0.8+rr*0.6,gy+math.sin(a)*rr*0.7+rr*0.5],fill=(80,66,70))
        d.text((x0+2*120,y0),'7',font=fy,fill=(240,200,60),stroke_width=6,stroke_fill=ink)
    im.save(T+name+'.png')
def boxlid(name='boxlid',W=1024,H=640,seed=66):
    base=(214,170,110); im=wash(W,H,base,0.06,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    d.ellipse([20,20,W-20,H-20],fill=(226,190,130),outline=(70,46,30),width=14)
    for k in range(7):   # painted folk flowers (tulips and daisies)
        a=2*math.pi*k/7; x=W/2+math.cos(a)*300; y=H/2+math.sin(a)*170; c=r.choice([(200,46,56),(60,110,170),(236,190,60)])
        for p in range(6): b=2*math.pi*p/6; d.ellipse([x+math.cos(b)*26-20,y+math.sin(b)*26-20,x+math.cos(b)*26+20,y+math.sin(b)*26+20],fill=c,outline=(60,40,30),width=4)
        d.ellipse([x-12,y-12,x+12,y+12],fill=(250,230,120))
    d.polygon([(W/2,H/2-90),(W/2-60,H/2+40),(W/2+60,H/2+40)],fill=(70,120,70),outline=(40,30,26)); d.ellipse([W/2-50,H/2-150,W/2+50,H/2-50],fill=(200,46,56),outline=(40,30,26),width=6)
    im.save(T+name+'.png')
def banner_txt(name,txt,sub,W=2048,H=420,bg=(200,40,46),fg=(252,240,200)):
    im=wash(W,H,bg,0.06,67); d=ImageDraw.Draw(im)
    d.rectangle([20,20,W-20,H-20],outline=fg,width=14)
    for k in range(0,W,128): d.polygon([(k,H),(k+64,H-50),(k+128,H)],fill=mul(bg,0.8))
    text(d,(W/2,H*0.42),txt,font(FS,190),fg,stroke=3,sf=mul(bg,0.5)); text(d,(W/2,H*0.80),sub,font(FS,64),fg)
    im.save(T+name+'.png')
def ledger_page(name='ledger_page',W=1536,H=1024,seed=68):
    base=(236,224,196); im=wash(W,H,base,0.06,seed); d=ImageDraw.Draw(im)
    d.line([W/2,0,W/2,H],fill=(160,130,100),width=10)
    ft=font(FS,62); fi=font(FSI,54); ink=(50,40,44)
    text(d,(W*0.25,110),'St. Johannis',ft,ink); text(d,(W*0.25,190),'Grab No. 54',font(FS,84),(150,36,40))
    for i,ln in enumerate(['Georg Sebastian Elbs','Eleonora Elbs, geb. Kraus','Susanna Eleonora Elbs']): d.text((70,300+i*120),ln,font=fi,fill=ink)
    d.ellipse([110,690,190,770],outline=(200,150,40),width=12); d.ellipse([150,690,230,770],outline=(200,150,40),width=12)
    d.text((260,690),'getraut 1651',font=fi,fill=ink)
    for k in range(12): d.line([W/2+60,140+k*70,W-70,140+k*70],fill=(180,166,140),width=3)
    for k in range(9): d.text((W/2+70,100+k*70),'— — —  — —',font=fi,fill=(120,110,100))
    det(im,base,seed+900,0.4).save(T+name+'.png')
def shelf_books(name='shelf_books',W=1024,H=1024,seed=69):
    im=wash(W,H,(90,60,40),0.05,seed); d=ImageDraw.Draw(im); r=random.Random(seed); rows=4; rh=H/rows
    for j in range(rows):
        y1=(j+1)*rh-20; x=10
        while x<W-30:
            w=r.uniform(34,70); h=r.uniform(rh*0.6,rh*0.86); c=r.choice([(110,40,36),(60,70,50),(140,100,60),(50,50,70),(120,90,50)])
            d.rectangle([x,y1-h,x+w,y1],fill=c,outline=(30,22,20),width=4); d.rectangle([x+6,y1-h+20,x+w-6,y1-h+40],fill=(214,180,90))
            x+=w+2
        d.rectangle([0,y1,W,y1+20],fill=(120,84,52)); d.line([0,y1,W,y1],fill=(30,22,20),width=5)
    im.save(T+name+'.png')
def sandstone_plate(name,txt,seed,W=1024,H=640):
    base=(180,140,110); im=wash(W,H,base,0.12,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for _ in range(1500): x,y=r.uniform(0,W),r.uniform(0,H); s_=r.uniform(1,3); d.ellipse([x-s_,y-s_,x+s_,y+s_],fill=r.choice([mul(base,0.7),mul(base,1.15)]))
    br=(150,110,50); d.rounded_rectangle([W*0.22,H*0.18,W*0.78,H*0.82],30,fill=br,outline=(70,50,30),width=12)   # bronze epitaph plate
    d.rounded_rectangle([W*0.26,H*0.24,W*0.74,H*0.76],20,outline=(200,160,80),width=6)
    if txt: text(d,(W/2,H/2),txt,font(FS,120),(250,226,150),stroke=3,sf=(70,50,30))
    det(im,base,seed+900,0.5).save(T+name+'.png')
def museum_wall(name='museum_wall',base=(208,196,178),seed=70):
    im=wash(1024,1024,base,0.05,seed); d=ImageDraw.Draw(im)
    d.rectangle([0,760,1024,1024],fill=mul(base,0.8)); d.line([0,760,1024,760],fill=mul(base,0.5),width=8)
    for k in range(0,1024,256): d.rectangle([k+20,800,k+236,990],outline=mul(base,0.6),width=6)
    det(im,base,seed+900,0.4).save(T+name+'.png')
def office_wall(name='office_wall',base=(214,226,232),seed=71):
    im=wash(1024,1024,base,0.05,seed); d=ImageDraw.Draw(im)
    for k in range(0,1024,64): d.line([k,0,k,1024],fill=mul(base,0.94),width=18)
    det(im,base,seed+900,0.4).save(T+name+'.png')
def parquet(name='parquet',base=(150,104,66),seed=72):
    im=wash(1024,1024,base,0.06,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for j in range(0,1024,64):
        for i in range(0,1024,192):
            x=i+(j//64%2)*96; c=mul(base,r.uniform(0.85,1.12)); d.rectangle([x,j,x+190,j+62],fill=c,outline=mul(base,0.55),width=3)
    det(im,base,seed+900,0.5).save(T+name+'.png')
def photo_print(name,W=768,H=1024,seed=73):
    im=Image.new('RGB',(W,H),(246,244,238)); d=ImageDraw.Draw(im); g=(120,120,124)
    d.rectangle([40,40,W-40,H-220],fill=(150,146,140)); r=random.Random(seed)
    for k in range(20): a=r.uniform(0,2*math.pi); rr=r.uniform(50,150); x=W/2+math.cos(a)*rr*0.6; y=(H-180)/2+math.sin(a)*rr*0.5; d.ellipse([x-rr*0.6,y-rr*0.5,x+rr*0.6,y+rr*0.5],fill=(40,36,40))
    text(d,(W/2,H-120),'?',font(FS,140),(200,40,40))
    im.save(T+name+'.png')
def cake_side(name='cake_side',W=1024,H=256):
    im=Image.new('RGB',(W,H),(246,232,220)); d=ImageDraw.Draw(im)
    for k in range(0,W,64): d.chord([k,-40,k+64,60],0,180,fill=(250,250,250),outline=(200,180,170),width=3)
    d.rectangle([0,H*0.55,W,H*0.68],fill=(200,46,56))
    for k in range(0,W,96): d.ellipse([k+30,H*0.75,k+60,H*0.88],fill=(214,180,60))
    im.save(T+name+'.png')
def snowflake_card(name='fx_snow',W=128,H=128):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); d.ellipse([28,28,100,100],fill=(255,255,255,235)); im.save(T+name+'.png')
def steam_card(name='fx_steam',W=256,H=512):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    for k in range(4): y=H-60-k*110; d.ellipse([W/2-60+k*8*(-1)**k,y-60,W/2+60+k*8*(-1)**k,y+50],fill=(250,250,250,150-k*25))
    im.save(T+name+'.png')
if __name__=='__main__':
    cobble('cobble',(118,112,110),60,snow=0.22); cobble('cobble_old',(130,118,100),74,snow=0.8); snowfield('snow')
    for i,(w,b) in enumerate([((236,222,196),(110,60,40)),((226,200,170),(90,50,36)),((240,232,214),(120,70,44)),((222,210,190),(80,52,40)),((236,214,180),(100,64,44))]):
        timber(f'house{i}',w,b,80+i,lit=0.6)
        timber(f'house_old{i}',mul(w,0.94),b,90+i,lit=0.35)
    stall_roof('stall_roof'); stall_roof('stall_roof_g',a=(46,110,70))
    stall_front('stall_lebk','LEBKUCHEN',101); stall_front('stall_glueh','GLÜHWEIN',102,col=(130,80,50)); stall_front('stall_stars','STERNE',103); stall_front('stall_prints','KUNSTDRUCKE',104,col=(120,84,56))
    stall_front('stall_old1','KINDLES MARCK',105,col=(120,90,60)); stall_front('stall_old2','SCHACHTELN',106,col=(110,80,56))
    sky_dusk(); sky('sky_winter',(120,150,196),(226,226,236),17,7,(244,244,250)); church_stone('church',(176,122,98),64); stone('sandstone',(180,142,112),75)
    bentbox_note('boxnote_blob','blob'); bentbox_note('boxnote_two','two'); bentbox_note('boxnote_seven','seven'); bentbox_note('boxnote_reveal','reveal'); boxlid()
    banner_txt('banner400','400 JAHRE','CHRISTKINDLESMARKT  1628 – 2028'); banner_txt('banner350','350 JAHRE','CHRISTKINDLESMARKT  1678 – 2028')
    ledger_page(); shelf_books(); sandstone_plate('grave54','54',76); sandstone_plate('grave_a','',77); sandstone_plate('grave_b','',78)
    museum_wall(); office_wall(); parquet(); planks('wood',(150,110,74),79); planks('table',(170,126,84),81); photo_print('photo_blob'); cake_side()
    card_text('sign_prints',[('KUNSTDRUCKE · PRINTS',100)],(32,64,96),(246,236,210),W=1024,H=256,border=(236,228,200),wood=False)
    card_text('sign_archive',[('STADTARCHIV',120)],(60,60,70),(240,236,226),W=1024,H=256,border=(200,196,186),wood=False)
    card_text('sign_museum',[('MUSEUM',120)],(110,30,36),(246,236,210),W=1024,H=256,border=(236,228,200),wood=False)
    card_text('label_box',[('Spanschachtel',70),('Kindles-Marck',70)],(244,240,230),(40,36,40),W=768,H=384,border=(40,36,40),wood=False)
    fx_cards(); glow(); snowflake_card(); steam_card()
    print('PAINT_OK')
