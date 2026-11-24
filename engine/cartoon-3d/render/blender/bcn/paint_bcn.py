# Painted textures for the Barcelona short (sat-barcelona). PIL only, our own designs. Output /root/cc/tex/ (= /root/bcn/tex)
# Reuses only the generic painter helpers of the Black Friday paint.py and the Cape Cod paint_cc.py (wash, strokes, paintdetail, sky,
# grass/tree card painters); every texture here is drawn new for this video.
import sys; sys.path.insert(0,'/root/cc/src')
import paint as P
P.T='/root/cc/tex/'; T=P.T
import paint_cc as PC
PC.T=T
import numpy as np, random, math
from PIL import Image, ImageDraw, ImageFilter
from paint import wash, strokes, paintdetail, noise, jl, jr, mul, text, font, FS, FSN, INK
FSI='/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf'
FSR='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
def det(im,base,seed,dens=1.0,K=1): return paintdetail(im,Image.new('L',im.size,255),base,seed,K,dens=dens)

# ---------------- 1899 Barcelona facades: stucco, tall shuttered windows, wrought-iron balconies ----------------
def facade(name,wall,seed,night=False,shop=None,W=1024,H=1536,floors=4,cols=3):
    r=random.Random(seed); im=wash(W,H,wall,0.07,seed,0.05); d=ImageDraw.Draw(im)
    for j in range(0,H,64): d.line([0,j,W,j],fill=mul(wall,0.9),width=2)        # rusticated stucco courses
    gf=int(H*0.30); top=H-gf; fh=(top-110)//floors
    shut=r.choice([(70,110,90),(60,96,110),(110,80,60),(70,96,70)])
    for f in range(floors):
        for c in range(cols):
            cx=W*(c+0.5)/cols; y0=100+f*fh+fh*0.12; y1=y0+fh*0.70; wv=W/cols*0.17
            lit=night and r.random()<0.55
            d.rectangle([cx-wv-14,y0-22,cx+wv+14,y0],fill=mul(wall,1.18)); jr(d,cx-wv-14,y0-22,cx+wv+14,y0,2,seed=f*5+c)
            d.rectangle([cx-wv,y0,cx+wv,y1],fill=(250,206,120) if lit else ((34,36,48) if night else (52,58,70)))
            if lit and r.random()<0.4: d.ellipse([cx-18,y0+fh*0.2,cx+18,y0+fh*0.2+36],fill=(70,50,40)); d.rectangle([cx-24,y0+fh*0.2+34,cx+24,y1],fill=(70,50,40))
            d.line([cx,y0,cx,y1],fill=mul(wall,1.1),width=5)
            ss=r.choice([0,0.5,1.0])                                               # shutters: closed, half, open
            for sx in(-1,1):
                xa=cx+sx*wv; xb=cx+sx*(wv+wv*0.75*(1-ss)) if ss<1 else cx+sx*wv
                if ss<1:
                    d.rectangle([min(xa,xb),y0,max(xa,xb),y1],fill=shut)
                    for k in range(int((y1-y0)//14)): d.line([min(xa,xb),y0+k*14,max(xa,xb),y0+k*14],fill=mul(shut,0.7),width=3)
                    jr(d,min(xa,xb),y0,max(xa,xb),y1,3,seed=f*11+c+sx)
            jr(d,cx-wv,y0,cx+wv,y1,3,seed=f*7+c)
            if f<floors-1:                                                         # balcony: slab + iron railing with curls
                by=y1+4; d.rectangle([cx-wv-30,by,cx+wv+30,by+14],fill=mul(wall,0.8)); jr(d,cx-wv-30,by,cx+wv+30,by+14,2,seed=c)
                d.line([cx-wv-26,by-70,cx+wv+26,by-70],fill=(36,32,36),width=6)
                for x in range(int(cx-wv-24),int(cx+wv+26),18):
                    d.line([x,by-70,x,by],fill=(36,32,36),width=4)
                for x in range(int(cx-wv-10),int(cx+wv+10),36): d.arc([x,by-62,x+26,by-36],0,360,fill=(36,32,36),width=3)
                if r.random()<0.35:                                                # a pot of geraniums
                    d.rectangle([cx+wv-20,by-28,cx+wv+8,by],fill=(170,90,60)); d.ellipse([cx+wv-30,by-54,cx+wv+18,by-24],fill=(70,120,60)); d.ellipse([cx+wv-18,by-56,cx+wv-4,by-42],fill=(210,50,50))
    d.rectangle([0,0,W,60],fill=mul(wall,0.72))
    for i in range(0,W,40): d.rectangle([i+6,60,i+26,80],fill=mul(wall,0.62))
    jl(d,[(0,60),(W,60)],3,seed=seed)
    # ground floor: arched openings (shop or gate)
    d.rectangle([0,top,W,H],fill=mul(wall,0.82)); jl(d,[(0,top),(W,top)],4,seed=seed+1)
    for c in range(cols):
        cx=W*(c+0.5)/cols; aw=W/cols*0.34
        glass=(250,210,130) if (night and c!=1) else ((40,42,54) if night else (70,80,92))
        d.rectangle([cx-aw,top+110,cx+aw,H-30],fill=glass); d.pieslice([cx-aw,top+40,cx+aw,top+180],180,360,fill=glass)
        d.arc([cx-aw,top+40,cx+aw,top+180],180,360,fill=INK,width=5); jl(d,[(cx-aw,top+110),(cx-aw,H-30)],5,seed=c); jl(d,[(cx+aw,top+110),(cx+aw,H-30)],5,seed=c+3)
        for k in range(1,4): d.line([cx-aw,top+110+k*(gf-140)/4,cx+aw,top+110+k*(gf-140)/4],fill=mul(glass,0.6),width=4)
        d.line([cx,top+110,cx,H-30],fill=mul(glass,0.6),width=4)
    d.rectangle([0,H-30,W,H],fill=(150,140,126))
    im=strokes(im,700,mul(wall,0.75),seed,6,22,2,40)
    im=det(im,wall,seed+900,0.7); im.save(T+name+'.png')

def paving(name='paving',base=(196,178,150),seed=3,W=1024,H=1024):
    """Rambla promenade: packed sandy ground with grit and a few flagstones"""
    im=wash(W,H,base,0.10,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for _ in range(3200):
        x,y=r.uniform(0,W),r.uniform(0,H); s=r.uniform(1,3); d.ellipse([x-s,y-s,x+s,y+s],fill=r.choice([mul(base,0.7),mul(base,1.12),(150,140,128)]))
    for k in range(24): jl(d,[(r.uniform(0,W),r.uniform(0,H)) for _ in range(3)],2,mul(base,0.75),k,5)
    im=strokes(im,1200,mul(base,0.85),seed+3,6,20,2,50); im.save(T+name+'.png')
def setts(name='setts',base=(132,124,118),seed=4,W=1024,H=1024):
    """carriageway: granite setts in rows"""
    im=wash(W,H,base,0.08,seed); d=ImageDraw.Draw(im); r=random.Random(seed); bh=48
    for j in range(H//bh+1):
        off=(j%2)*36
        for i in range(-1,W//72+1):
            x=i*72+off; y=j*bh; c=mul(base,r.uniform(0.82,1.15)); d.rounded_rectangle([x+3,y+3,x+69,y+bh-3],8,fill=c,outline=mul(base,0.55),width=3)
            d.line([x+10,y+8,x+40,y+8],fill=mul(c,1.18),width=3)
    im.save(T+name+'.png')
def plane_tree(name='planetree',W=1024,H=2048,seed=12,base=(96,130,70)):
    """London plane of the Rambla: mottled cream-grey-olive trunk, a big rounded canopy of ink-edged leaf clumps (alpha card)"""
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); r=random.Random(seed)
    tx=W/2; d.polygon([(tx-50,H),(tx-36,H*0.42),(tx+36,H*0.42),(tx+52,H)],fill=(186,180,150,255))
    for _ in range(90):
        y=r.uniform(H*0.44,H-20); x=tx+r.uniform(-40,40); s=r.uniform(10,24); d.ellipse([x-s,y-s*1.4,x+s,y+s*1.4],fill=r.choice([(140,140,104,255),(206,200,170,255),(120,118,86,255)]))
    jl(d,[(tx-50,H),(tx-36,H*0.42)],6,(50,40,44),1); jl(d,[(tx+52,H),(tx+36,H*0.42)],6,(50,40,44),2)
    for k in range(4): a=-0.9+k*0.6; d.line([tx,H*0.48,tx+math.sin(a)*300,H*0.30],fill=(170,164,134,255),width=26); jl(d,[(tx,H*0.48),(tx+math.sin(a)*300,H*0.30)],4,(50,40,44),k)
    for k in range(34):
        a=r.uniform(0,2*math.pi); rr=r.uniform(0,1)**0.6; cx=tx+math.cos(a)*rr*400; cy=H*0.25+math.sin(a)*rr*300; s=r.uniform(90,170)
        c=mul(base,r.uniform(0.78,1.2)); d.ellipse([cx-s,cy-s*0.8,cx+s,cy+s*0.8],fill=c+(255,),outline=(46,40,40,255),width=6)
        d.arc([cx-s*0.7,cy-s*0.6,cx+s*0.5,cy+s*0.3],200,320,fill=mul(c,1.25)+(255,),width=8)
    a=np.asarray(im).copy(); m=a[...,3]>0; n=(noise(W,H,8,seed)-0.5)*26; a[...,:3]=np.where(m[...,None],np.clip(a[...,:3]+n[...,None],0,255),a[...,:3])
    Image.fromarray(a.astype(np.uint8)).save(T+name+'.png')
def hills(name='hills_far',W=4096,H=900,seed=14,base=(110,130,96)):
    """far card: Collserola hills with a hilltop and scattered villas (generic, no landmark)"""
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); r=random.Random(seed)
    yl=[H*0.40+120*math.sin(x/700+1.1)+50*math.sin(x/230)-160*math.exp(-((x-W*0.62)/500)**2) for x in range(0,W+8,8)]
    d.polygon([(0,H)]+[(i*8,y) for i,y in enumerate(yl)]+[(W,H)],fill=base+(255,))
    for _ in range(260):
        x=r.uniform(0,W); y=yl[int(x/8)]+r.uniform(20,H*0.5); s=r.uniform(14,34); d.ellipse([x-s,y-s*0.7,x+s,y+s*0.7],fill=mul(base,r.uniform(0.7,0.95))+(255,))
    for _ in range(40):
        x=r.uniform(0,W); y=yl[int(x/8)]+r.uniform(60,H*0.45); d.rectangle([x-14,y-12,x+14,y+10],fill=(236,222,196,255)); d.polygon([(x-18,y-12),(x,y-26),(x+18,y-12)],fill=(170,80,60,255))
    jl(d,[(i*8,y) for i,y in enumerate(yl)],5,(70,74,70),seed,1.5)
    a=np.asarray(im).copy(); m=a[...,3]>0; n=(noise(W,H,8,seed)-0.5)*24; a[...,:3]=np.where(m[...,None],np.clip(a[...,:3]+n[...,None],0,255),a[...,:3])
    Image.fromarray(a.astype(np.uint8)).save(T+name+'.png')
def city_far(name='city_far',W=4096,H=900,seed=15):
    """far card behind the velodrome: low town roofs, chimneys, a few bell towers (generic)"""
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); r=random.Random(seed); x=0
    while x<W:
        w=r.uniform(80,200); h=r.uniform(H*0.18,H*0.42); c=r.choice([(226,206,170),(214,186,150),(230,216,190),(200,170,140)])
        d.rectangle([x,H-h,x+w,H],fill=c+(255,),outline=(70,60,60,255),width=4); d.polygon([(x-6,H-h),(x+w/2,H-h-30),(x+w+6,H-h)],fill=(176,90,66,255),outline=(70,60,60,255))
        for k in range(int(w//40)): d.rectangle([x+12+k*40,H-h+30,x+28+k*40,H-h+56],fill=(70,70,84,255))
        if r.random()<0.06: d.rectangle([x+w/2-20,H-h-200,x+w/2+20,H-h],fill=(206,186,150,255),outline=(70,60,60,255),width=4); d.polygon([(x+w/2-26,H-h-200),(x+w/2,H-h-260),(x+w/2+26,H-h-200)],fill=(150,80,60,255))
        x+=w*r.uniform(0.85,1.05)
    im.save(T+name+'.png')
# ---------------- interiors ----------------
def plaster(name,base,dado,seed,W=1024,H=1024,stripe=None):
    im=wash(W,H,base,0.07,seed,0.04); d=ImageDraw.Draw(im); r=random.Random(seed); dy=int(H*0.62)
    d.rectangle([0,dy,W,H],fill=dado)
    for x in range(0,W,128): d.rectangle([x+10,dy+40,x+118,H-40],outline=mul(dado,0.7),width=5)
    d.rectangle([0,dy-16,W,dy],fill=mul(dado,1.15)); jl(d,[(0,dy-16),(W,dy-16)],3,seed=seed); jl(d,[(0,dy),(W,dy)],3,seed=seed+1)
    if stripe:
        for x in range(0,W,64): d.line([x,0,x,dy-16],fill=stripe,width=10)
    for k in range(10): jl(d,[(r.uniform(0,W),r.uniform(0,dy)) for _ in range(3)],2,mul(base,0.82),k,4)
    im=strokes(im,900,mul(base,0.82),seed+5,6,20,2,40); det(im,base,seed+900,0.6).save(T+name+'.png')
def typecase(name='typecase',W=1024,H=768,seed=41):
    """compositor's type case: wooden drawers of little lead letters"""
    base=(150,104,64); im=wash(W,H,base,0.06,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for j in range(6):
        for i in range(10):
            x0=40+i*94; y0=40+j*114; d.rectangle([x0,y0,x0+86,y0+104],fill=mul(base,0.55),outline=INK,width=4)
            for _ in range(14): x=x0+r.uniform(10,76); y=y0+r.uniform(10,94); d.rectangle([x-4,y-6,x+4,y+6],fill=(120,120,128))
    det(im,base,seed+900,0.5).save(T+name+'.png')
def clockface(name='clock9',W=512,H=512):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.ellipse([16,16,W-16,H-16],fill=(150,100,60,255),outline=INK,width=14); d.ellipse([56,56,W-56,H-56],fill=(246,238,214,255),outline=INK,width=6)
    for k in range(12):
        a=k*math.pi/6; d.line([W/2+170*math.sin(a),H/2-170*math.cos(a),W/2+190*math.sin(a),H/2-190*math.cos(a)],fill=INK,width=10)
    d.line([W/2,H/2,W/2-120,H/2],fill=INK,width=18); d.line([W/2,H/2,W/2,H/2-170],fill=INK,width=12); d.ellipse([W/2-16,H/2-16,W/2+16,H/2+16],fill=INK)   # nine o'clock
    im.save(T+name+'.png')
def sign(name,txt,bg,fg,W=2048,H=384,sz=170,border=(214,180,90),f=FS):
    im=wash(W,H,bg,0.06,7); d=ImageDraw.Draw(im); d.rectangle([16,16,W-16,H-16],outline=border,width=18); d.rectangle([44,44,W-44,H-44],outline=mul(border,0.7),width=6)
    while d.textlength(txt,font=font(f,sz))>W-200: sz-=6
    text(d,(W/2,H/2+6),txt,font(f,sz),fg,stroke=3,sf=mul(fg,0.5)); det(im,bg,9,0.4).save(T+name+'.png')
def paper_ad(name='paper_ad',W=1024,H=1400,seed=70,hl=False):
    """our own drawing of a page of a sports weekly, 1899: masthead, columns, and the small notice (paraphrased, not a facsimile)"""
    pb=(238,230,206); im=wash(W,H,pb,0.04,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    text(d,(W/2,86),'LOS DEPORTES',font(FS,104),INK); d.line([40,150,W-40,150],fill=INK,width=5)
    text(d,(W/2,176),'BARCELONA  ·  22 OCTUBRE 1899',font(FSN,26),INK); d.line([40,200,W-40,200],fill=INK,width=2)
    for col in range(3):
        x0=50+col*318
        for k in range(48):
            y=232+k*24
            if col==1 and 560<y<1000: continue
            d.line([x0,y,x0+290*r.uniform(0.8,1.0),y],fill=(120,112,100),width=7)
    bx0,by0,bx1,by1=350,560,688,1000
    d.rectangle([bx0,by0,bx1,by1],fill=(246,240,222),outline=INK,width=5)
    text(d,((bx0+bx1)/2,by0+44),'FOOT-BALL',font(FS,46),INK)
    lines=['Nuestro amigo','Mr. Kans Kamper,','de la Sociedad','de Deportes, ruega','a cuantos sientan','aficiones por el','foot-ball, pasen','por esta redacción','martes y viernes','de 9 a 11 noche.']
    for i,s in enumerate(lines): text(d,((bx0+bx1)/2,by0+100+i*36),s,font(FSR,27),INK)
    if hl: d.ellipse([bx0+20,by0+122,bx1-20,by0+170],outline=(196,40,36),width=8)
    im=det(im,pb,seed+900,0.3); im.save(T+name+'.png')
def chalk_score(name,txt,W=1024,H=640,seed=72):
    base=(40,52,46); im=wash(W,H,base,0.10,seed); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,H],outline=(130,90,56),width=40)
    text(d,(W/2,H*0.24),'BARCELONA  -  ENGLISH',font(FSN,58),(226,226,214)); d.line([120,H*0.36,W-120,H*0.36],fill=(200,200,190),width=5)
    text(d,(W/2,H*0.66),txt,font(FSN,220),(240,240,230))
    strokes(im,400,(200,200,190),seed,6,30,3,30).save(T+name+'.png')
def track(name='track',base=(204,192,170),seed=60,W=1024,H=1024):
    """cement cycle track with joints and tyre streaks"""
    im=wash(W,H,base,0.07,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for y in range(0,H,256): d.line([0,y,W,y],fill=mul(base,0.7),width=4)
    for _ in range(60): y=r.uniform(0,H); d.line([0,y,W,y+r.uniform(-6,6)],fill=mul(base,0.86),width=r.randint(2,5))
    for _ in range(2200): x,y=r.uniform(0,W),r.uniform(0,H); s=r.uniform(1,2.4); d.ellipse([x-s,y-s,x+s,y+s],fill=r.choice([mul(base,0.75),mul(base,1.1)]))
    det(im,base,seed+900,0.6).save(T+name+'.png')
def turf(name='turf',base=(128,150,72),seed=61,W=1024,H=1024):
    """worn winter grass with sandy patches"""
    im=wash(W,H,base,0.12,seed); d=ImageDraw.Draw(im,'RGBA'); r=random.Random(seed)
    for _ in range(26): x,y=r.uniform(0,W),r.uniform(0,H); s=r.uniform(30,120); d.ellipse([x-s,y-s*0.6,x+s,y+s*0.6],fill=(170,150,104,90))
    for _ in range(6000):
        x,y=r.uniform(0,W),r.uniform(0,H); c=mul(base,r.uniform(0.65,1.3)); d.line([x,y,x+r.uniform(-3,3),y-r.uniform(5,12)],fill=c+(220,),width=2)
    im.save(T+name+'.png')
def fenceboards(name='fence',base=(170,130,84),seed=62,W=1024,H=512):
    im=wash(W,H,base,0.06,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for x in range(0,W,64): c=mul(base,r.uniform(0.85,1.12)); d.rectangle([x,0,x+60,H],fill=c); jl(d,[(x,0),(x,H)],5,mul(base,0.4),x)
    d.rectangle([0,H*0.15,W,H*0.22],fill=mul(base,0.7)); d.rectangle([0,H*0.78,W,H*0.85],fill=mul(base,0.7))
    det(im,base,seed+900,0.5).save(T+name+'.png')
def crowd(name,W=2048,H=1024,seed=63,rows=7,day=True):
    """packed crowd on stands: rows of small bean figures (white heads, dark ink, hats, coats in mixed colours), Rick crowd idea (#22 f1353)"""
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); r=random.Random(seed); rh=H/rows
    for j in range(rows):
        y=(j+0.85)*rh; d.rectangle([0,y-6,W,y+rh*0.2],fill=(120,96,70,255) if day else (90,70,56,255))
        x=r.uniform(-20,10)
        while x<W:
            s=rh*r.uniform(0.30,0.36); coat=r.choice([(60,60,70),(110,70,50),(150,140,120),(70,90,110),(130,50,46),(90,100,70),(200,190,170)])
            d.rounded_rectangle([x-s*0.7,y-s*1.1,x+s*0.7,y+s*0.4],int(s*0.4),fill=coat+(255,),outline=(50,28,42,255),width=4)
            hy=y-s*1.55; d.ellipse([x-s*0.62,hy-s*0.62,x+s*0.62,hy+s*0.62],fill=(250,236,220,255),outline=(50,28,42,255),width=4)
            d.ellipse([x-s*0.24,hy-s*0.1,x-s*0.12,hy+s*0.1],fill=(50,28,42,255)); d.ellipse([x+s*0.12,hy-s*0.1,x+s*0.24,hy+s*0.1],fill=(50,28,42,255))
            if r.random()<0.5: d.arc([x-s*0.3,hy,x+s*0.3,hy+s*0.4],20,160,fill=(50,28,42,255),width=4)
            hat=r.random()
            if hat<0.35: d.rectangle([x-s*0.6,hy-s*0.75,x+s*0.6,hy-s*0.55],fill=(40,36,40,255)); d.ellipse([x-s*0.45,hy-s*1.05,x+s*0.45,hy-s*0.55],fill=(40,36,40,255))
            elif hat<0.55: d.ellipse([x-s*0.75,hy-s*0.72,x+s*0.75,hy-s*0.5],fill=(232,214,160,255),outline=(50,28,42,255),width=3); d.rectangle([x-s*0.45,hy-s*0.95,x+s*0.45,hy-s*0.62],fill=(232,214,160,255))
            if r.random()<0.12: d.line([x+s*0.6,y-s*0.8,x+s*1.0,y-s*2.4],fill=(50,28,42,255),width=8); d.ellipse([x+s*0.85,y-s*2.65,x+s*1.15,y-s*2.35],fill=(50,28,42,255))   # raised arm
            x+=s*r.uniform(1.25,1.6)
    im.save(T+name+'.png')
def kiosk_panel(name='kioskpanel',W=1024,H=1024,seed=64):
    """the newsstand's front: green painted iron with racks of folded papers and magazines (no real titles)"""
    base=(46,94,72); im=wash(W,H,base,0.06,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for j in range(4):
        y0=60+j*230
        d.rectangle([30,y0+180,W-30,y0+196],fill=mul(base,0.6))
        x=40
        while x<W-140:
            w=r.uniform(110,150); c=r.choice([(236,228,206),(240,200,80),(200,70,60),(90,140,190),(236,236,236),(120,180,120)])
            d.rectangle([x,y0,x+w,y0+180],fill=c,outline=INK,width=4); d.rectangle([x+10,y0+12,x+w-10,y0+44],fill=mul(c,0.55))
            for k in range(5): d.line([x+12,y0+64+k*20,x+w-14,y0+64+k*20],fill=mul(c,0.7),width=5)
            x+=w+10
    det(im,base,seed+900,0.5).save(T+name+'.png')
def stadium_seats(name='seats',W=1024,H=1024,seed=65):
    base=(150,150,156); im=wash(W,H,base,0.06,seed); d=ImageDraw.Draw(im)
    for j in range(0,H,64): d.rectangle([0,j,W,j+20],fill=mul(base,0.7)); d.line([0,j,W,j],fill=INK,width=3)
    im.save(T+name+'.png')
if __name__=='__main__':
    walls=[(214,180,128),(226,204,164),(206,160,130),(196,186,150),(222,190,150),(210,170,120)]
    for i,w in enumerate(walls): facade(f'fac{i}',w,300+i,night=False); facade(f'facN{i}',mul(w,0.62),300+i,night=True)
    paving(); paving('pavingN',(120,108,96),5); setts(); setts('settsN',(80,76,74),6)
    plane_tree(); plane_tree('planetreeN',base=(52,74,52),seed=13); hills(); city_far()
    PC.sky('sky_night',(18,26,70),(70,60,110),31,5,(70,70,110)); PC.sky('sky_bcn',(92,150,206),(246,222,186),32,7,(252,246,236)); PC.sky('sky_pm',(110,150,200),(250,214,170),33,6,(252,240,226))
    plaster('wall_news',(226,212,180),(120,80,52),40,stripe=(214,198,162)); plaster('wall_gym',(150,176,150),(110,76,50),41)
    P.woodfloor('floor_news',seed=96,base=(140,96,60)); P.woodfloor('floor_gym',seed=97,base=(176,128,80))
    typecase(); clockface(); paper_ad(); paper_ad('paper_ad_hl',hl=True)
    sign('sign_deportes','LOS DEPORTES',(36,40,52),(244,226,170)); sign('sign_gym','GIMNASIO',(110,40,36),(250,236,200))
    sign('sign_prensa','PRENSA',(40,84,64),(250,238,196),W=1536,H=384)
    chalk_score('score01','0 - 1'); track(); turf(); fenceboards()
    crowd('crowd_small',rows=4,seed=66); crowd('crowd_big',rows=9,seed=67); kiosk_panel(); stadium_seats()
    PC.grass_card('grass0',1); PC.grass_card('grass1',2,col=(130,150,70)); PC.grass_card('grass2',3,col=(160,150,90))
    print('PAINT_OK')
# r3 (stills: S18 crowd read as grey stripes): big-figure crowd, two rows per card, bright mixed shirts, seat colour behind (no dark gaps), many raised arms
def crowd_xl(name='crowd_xl',W=2048,H=1024,seed=66,rows=2):
    im=Image.new('RGBA',(W,H),(178,150,112,255)); d=ImageDraw.Draw(im); r=random.Random(seed); rh=H/rows
    for j in range(rows):
        y=(j+0.92)*rh; d.rectangle([0,y-10,W,y+rh*0.08],fill=(150,120,86,255))
        x=r.uniform(-30,10)
        while x<W:
            s=rh*r.uniform(0.27,0.31); coat=r.choice([(214,70,56),(240,196,60),(70,130,196),(80,160,90),(236,132,50),(240,236,226),(150,90,170),(60,170,170)])
            if r.random()<0.35: d.line([x-s*0.6,y-s*0.8,x-s*1.0,y-s*2.5],fill=(50,28,42,255),width=10); d.ellipse([x-s*1.18,y-s*2.75,x-s*0.82,y-s*2.39],fill=(50,28,42,255))
            if r.random()<0.35: d.line([x+s*0.6,y-s*0.8,x+s*1.0,y-s*2.5],fill=(50,28,42,255),width=10); d.ellipse([x+s*0.82,y-s*2.75,x+s*1.18,y-s*2.39],fill=(50,28,42,255))
            d.rounded_rectangle([x-s*0.72,y-s*1.15,x+s*0.72,y+s*0.3],int(s*0.4),fill=coat+(255,),outline=(50,28,42,255),width=6)
            hy=y-s*1.6; d.ellipse([x-s*0.64,hy-s*0.64,x+s*0.64,hy+s*0.64],fill=(252,238,222,255),outline=(50,28,42,255),width=6)
            d.ellipse([x-s*0.26,hy-s*0.12,x-s*0.1,hy+s*0.12],fill=(50,28,42,255)); d.ellipse([x+s*0.1,hy-s*0.12,x+s*0.26,hy+s*0.12],fill=(50,28,42,255))
            d.chord([x-s*0.32,hy+s*0.05,x+s*0.32,hy+s*0.45],0,180,fill=(120,40,50,255))
            x+=s*r.uniform(1.35,1.6)
    im.save(T+name+'.png')
