# Painted textures for the Cape Cod Pilgrims short (tue-cape-cod). PIL only, our own designs. Output /root/cc/tex/
# Reuses only the generic painter helpers of the Black Friday paint.py (wash, strokes, paintdetail, sky): no BF texture is reused.
import sys; sys.path.insert(0,'/root/cc/src')
import paint as P
P.T='/root/cc/tex/'; T=P.T
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
if __name__=='__main__':
    sand('sand',(222,196,150),1); sand('sand_wet',(176,150,116),4); sand('sand_dawn',(214,176,150),5)
    water('water',(52,110,128),2); water('water_storm',(64,92,106),3,foam=1.0); water('water_dawn',(96,104,140),6); water('water_bay',(60,122,140),8)
    planks('hull',(112,72,44),20); planks('deck',(170,128,86),21); planks('cabin',(128,86,54),22,vertical=True); planks('cabin_floor',(110,74,48),23)
    planks('wharf',(150,120,90),24); planks('barricade',(116,90,64),25,nails=False)
    shingles('shingle',(156,150,140),7); shingles('shingle_trim',(236,230,218),8)
    stone('granite',(150,146,140),40); stone('rock1620',(142,138,132),41,carve='1620'); stone('rock',(138,134,128),42)
    sky('sky_cape',(92,150,206),(246,224,186),17,7,(252,246,236)); sky('sky_storm',(84,98,120),(186,190,196),23,11,(206,210,214)); sky('sky_dawn',(110,110,170),(252,196,160),21,6,(252,214,196)); sky('sky_1741',(110,160,206),(244,226,196),27,8,(252,246,236))
    dunes_far('dunes_far',seed=11); dunes_far('shore_far',seed=13,base=(196,174,136)); treeline('trees',W=8192,H=640,seed=12); treeline('trees_dawn',W=8192,H=600,seed=14,base=(70,76,84))
    for i in range(3): grass_card(f'grass{i}',60+i)
    card_text('sign_route',[('1.  CAPE COD',150),('2.  PLYMOUTH',150)],(196,170,130),(60,40,30),W=1024,H=512,border=(90,64,44))
    card_text('sign_cornhill',[('CORN HILL',170)],(120,90,60),(244,232,200),W=1024,H=384,border=(70,50,36))
    card_text('sign_encounter',[('FIRST ENCOUNTER',120),('BEACH',120)],(40,84,70),(244,236,210),W=1024,H=512,border=(236,228,200),wood=False)
    card_text('sign_gallery',[('PRINTS & POSTERS',110)],(32,64,96),(246,236,210),W=1024,H=256,border=(236,228,200),wood=False)
    chart('chart'); compact('compact0',signed=0); compact('compact1',signed=4); compact('compact2',signed=10); journal('journal')
    basket(); corn(); sail(); deerskin(); fx_cards(); glow()
    print('PAINT_OK')
