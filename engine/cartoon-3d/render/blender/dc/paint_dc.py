# Painted textures for the Washington DC Thanksgiving short (thu-washington-dc). PIL only, our own designs. Output /root/dc/tex/
# Reuses only the generic painter helpers of the Black Friday paint.py (wash, strokes, paintdetail, sky, wallpaper, woodfloor, facade): no BF texture is reused.
import sys; sys.path.insert(0,'/root/dc/src')
import paint as P
P.T='/root/dc/tex/'; T=P.T
import numpy as np, random, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from paint import wash, strokes, paintdetail, noise, jl, jr, mul, text, font, FS, FSN, FM, INK
FSI='/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf'; FSR='/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'
def det(im,base,seed,dens=1.0,K=1): return paintdetail(im,Image.new('L',im.size,255),base,seed,K,dens=dens)
def planks(name,base,seed,W=1024,H=1024,pw=86,vertical=False):
    im=wash(W,H,base,0.06,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for j in range(0,H,pw):
        c=mul(base,r.uniform(0.84,1.12)); d.rectangle([0,j,W,j+pw-4],fill=c); jl(d,[(0,j),(W,j)],6,mul(base,0.36),j)
        x=r.uniform(0,W); jl(d,[(x,j),(x,j+pw)],5,mul(base,0.36),j+1)
        for k in range(9):
            yy=j+r.uniform(8,pw-10); xx=r.uniform(-100,W); L=r.uniform(80,300)
            d.line([(xx+t,yy+2*math.sin(t/30+k)) for t in range(0,int(L),10)],fill=mul(c,0.74),width=2)
    im=det(im,base,seed+900)
    if vertical: im=im.rotate(90)
    im.save(T+name+'.png')
def plaster(name,base,seed,W=1024,H=1024,wainscot=None):
    im=wash(W,H,base,0.10,seed); im=strokes(im,1600,mul(base,0.82),seed,10,40,3,70); im=strokes(im,500,mul(base,1.12),seed+1,10,30,3,60)
    d=ImageDraw.Draw(im); r=random.Random(seed)
    for k in range(10): jl(d,[(r.uniform(0,W),r.uniform(0,H)) for _ in range(3)],2,mul(base,0.7),k,5)
    if wainscot:
        d.rectangle([0,H-300,W,H],fill=wainscot)
        for x in range(0,W,170): jr(d,x+14,H-280,x+156,H-34,6,mul(wainscot,0.45),x)
        d.rectangle([0,H-322,W,H-300],fill=mul(wainscot,0.7)); jl(d,[(0,H-322),(W,H-322)],5,mul(wainscot,0.35),3)
    det(im,base,seed+900).save(T+name+'.png')
def brick(name,base,seed,W=1024,H=1024):
    im=wash(W,H,base,0.08,seed); d=ImageDraw.Draw(im); r=random.Random(seed); bh,bw=32,84
    for j in range(H//bh+1):
        off=(j%2)*bw//2
        for i in range(-1,W//bw+2):
            c=mul(base,r.uniform(0.82,1.12)); x=i*bw+off; y=j*bh; d.rectangle([x+3,y+3,x+bw-3,y+bh-3],fill=c)
    det(im,base,seed+900).save(T+name+'.png')
def cobble(name='cobble',base=(150,140,128),seed=3,W=1024,H=1024):
    im=wash(W,H,mul(base,0.6),0.06,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for j in range(0,H,46):
        x=-r.uniform(0,40)
        while x<W:
            w=r.uniform(50,80); c=mul(base,r.uniform(0.8,1.15)); d.rounded_rectangle([x+4,j+4,x+w-4,j+42],12,fill=c,outline=mul(base,0.45),width=3); x+=w
    for _ in range(26):   # fallen leaves
        x,y=r.uniform(0,W),r.uniform(0,H); c=r.choice([(214,120,40),(190,70,40),(226,170,60)]); d.ellipse([x-9,y-5,x+9,y+5],fill=c,outline=INK,width=2)
    det(im,base,seed+900).save(T+name+'.png')
def carpet(name,base,motif,seed,W=1024,H=1024):
    im=wash(W,H,base,0.06,seed); d=ImageDraw.Draw(im)
    for j in range(0,H,128):
        for i in range(0,W,128):
            cx,cy=i+64+(64 if (j//128)%2 else 0),j+64; d.polygon([(cx,cy-36),(cx+36,cy),(cx,cy+36),(cx-36,cy)],fill=motif,outline=mul(base,0.5)); d.ellipse([cx-8,cy-8,cx+8,cy+8],fill=mul(motif,1.2))
    d.rectangle([20,20,W-20,H-20],outline=mul(motif,0.8),width=24)
    det(im,base,seed+900).save(T+name+'.png')
def sky(name,top,bot,seed,clouds,cloud,W=1024,H=2048):
    y=np.linspace(0,1,H)[:,None,None]; a=np.array(top,np.float32)*(1-y**0.8)+np.array(bot,np.float32)*(y**0.8); a=np.repeat(a,W,1)
    im=Image.fromarray(a.astype(np.uint8)).convert('RGBA'); r=random.Random(seed)
    for k in range(clouds):
        cx,cy=r.uniform(0,W),r.uniform(H*0.12,H*0.55); s=r.uniform(50,120)
        blob=Image.new('RGBA',(W,H),(0,0,0,0)); bd=ImageDraw.Draw(blob)
        for q in range(9):
            ox,oy=r.uniform(-2.2,2.2)*s,r.uniform(-0.5,0.3)*s; rr=s*r.uniform(0.5,0.9)
            for sh in (-W,0,W): bd.ellipse([cx+ox-rr+sh,cy+oy-rr,cx+ox+rr+sh,cy+oy+rr*0.8],fill=cloud+(255,))
        im=Image.alpha_composite(im,blob)
        e=blob.split()[3].filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(7)); ol=Image.new('RGBA',(W,H),(70,74,96,0)); ol.putalpha(e.point(lambda v:200 if v>40 else 0)); im=Image.alpha_composite(im,ol)
    im.convert('RGB').save(T+name+'.png')
# ---------------- window views (painted cards seen through window openings) ----------------
def view_rooftops(name,skyc,night=False,seed=5,W=1024,H=1024,dome=False,glow=False):
    y=np.linspace(0,1,H)[:,None,None]; a=np.array(skyc[0],np.float32)*(1-y)+np.array(skyc[1],np.float32)*y
    im=Image.fromarray(np.repeat(a,W,1).astype(np.uint8)); d=ImageDraw.Draw(im); r=random.Random(seed)
    if night:
        for _ in range(60): x,y_=r.uniform(0,W),r.uniform(0,H*0.5); d.ellipse([x-2,y_-2,x+2,y_+2],fill=(250,246,220))
        d.ellipse([W*0.72,H*0.12,W*0.72+90,H*0.12+90],fill=(250,240,200),outline=INK,width=5)
    if glow:   # distant war glow on the horizon (no battle shown)
        g=Image.new('RGBA',(W,H),(0,0,0,0)); gd=ImageDraw.Draw(g); gd.ellipse([-200,H*0.5,W*0.7,H*0.95],fill=(230,90,50,140)); g=g.filter(ImageFilter.GaussianBlur(60)); im=Image.alpha_composite(im.convert('RGBA'),g).convert('RGB'); d=ImageDraw.Draw(im)
        for k in range(5): x=r.uniform(0,W*0.6); d.ellipse([x-70,H*0.5-60,x+70,H*0.5+40],fill=(120,110,120),outline=INK,width=4)
    if dome:   # generic domed capitol under scaffolding (1860s), far off; no logo
        cx,base_=W*0.62,H*0.70; c=(214,212,204) if not night else (120,120,150)
        d.rectangle([cx-260,base_-120,cx+260,base_],fill=c,outline=INK,width=5)
        for k in range(9): x=cx-230+k*57; d.rectangle([x,base_-110,x+18,base_-10],fill=mul(c,0.85),outline=INK,width=2)
        d.rectangle([cx-120,base_-210,cx+120,base_-120],fill=c,outline=INK,width=5); d.chord([cx-130,base_-360,cx+130,base_-60],180,360,fill=mul(c,0.9),outline=INK,width=5)
        for k in range(8): x=cx-120+k*34; d.line([x,base_-330,x,base_-180],fill=(120,90,60),width=4)
        for k in range(5): y_=base_-320+k*32; d.line([cx-125,y_,cx+125,y_],fill=(120,90,60),width=3)
        d.line([cx+150,base_-120,cx+150,base_-420],fill=(90,70,50),width=8); d.line([cx+150,base_-410,cx+20,base_-380],fill=(90,70,50),width=6)   # crane
    for k in range(14):   # rooftops
        x=k*W/12-r.uniform(0,40); w=r.uniform(90,160); h=r.uniform(120,300); c=r.choice([(150,80,60),(170,100,70),(130,90,80),(160,130,110)])
        if night: c=mul(c,0.45)
        d.rectangle([x,H-h,x+w,H],fill=c,outline=INK,width=4); d.polygon([(x-10,H-h),(x+w/2,H-h-50),(x+w+10,H-h)],fill=mul(c,0.7),outline=INK)
        d.rectangle([x+w*0.7,H-h-60,x+w*0.7+22,H-h-10],fill=mul(c,0.8),outline=INK,width=3)
        for yy in range(int(H-h+30),H-20,60):
            for xx in range(int(x+14),int(x+w-24),40): d.rectangle([xx,yy,xx+20,yy+30],fill=(250,214,130) if (night and r.random()<0.5) else mul(c,0.6),outline=INK,width=2)
    det(im,skyc[1],seed+900,0.5).save(T+name+'.png')
# ---------------- props and paper ----------------
def letter(name,seed,W=768,H=1024,lines=16,head=None,ink=(40,40,70)):
    im=wash(W,H,(240,232,210),0.05,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    if head: text(d,(W/2,90),head,font(FSI,52),ink)
    y=170 if head else 90
    for k in range(lines):
        x=70; L=r.uniform(0.7,1.0)*(W-140)
        pts=[(x+t,y+6*math.sin(t/14+k)+r.uniform(-2,2)) for t in range(0,int(L),6)]
        d.line(pts,fill=ink,width=5,joint='curve'); y+=52
    d.line([W*0.55,y+20,W-80,y+10],fill=ink,width=6)
    det(im,(240,232,210),seed+900,0.4).save(T+name+'.png')
def envelope(name,seed,W=768,H=512):
    im=wash(W,H,(236,226,200),0.05,seed); d=ImageDraw.Draw(im)
    d.line([(0,0),(W/2,H*0.55),(W,0)],fill=mul((236,226,200),0.6),width=8); d.ellipse([W/2-50,H*0.55-50,W/2+50,H*0.55+50],fill=(170,30,40),outline=INK,width=6)
    d.rectangle([4,4,W-4,H-4],outline=mul((236,226,200),0.5),width=8)
    det(im,(236,226,200),seed+900,0.4).save(T+name+'.png')
def magazine(name,seed=11,W=768,H=1024):
    base=(232,214,180); im=wash(W,H,base,0.06,seed); d=ImageDraw.Draw(im)
    d.rectangle([24,24,W-24,H-24],outline=(120,40,60),width=14)
    text(d,(W/2,130),"LADY'S BOOK",font(FSR,96),(120,40,60)); text(d,(W/2,210),'NOVEMBER',font(FS,44),INK)
    d.ellipse([W/2-210,280,W/2+210,760],fill=(214,190,160),outline=INK,width=8)   # oval fashion plate: a dress silhouette
    d.polygon([(W/2-40,380),(W/2+40,380),(W/2+150,720),(W/2-150,720)],fill=(150,60,90),outline=INK); d.ellipse([W/2-40,310,W/2+40,390],fill=(250,244,236),outline=INK,width=6)
    text(d,(W/2,850),'A NATIONAL',font(FS,60),INK); text(d,(W/2,920),'THANKSGIVING',font(FS,60),INK)
    det(im,base,seed+900,0.5).save(T+name+'.png')
def page_print(name,seed=12,W=768,H=1024):
    im=wash(W,H,(238,232,214),0.04,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    text(d,(W/2,90),'ONE DAY OF',font(FS,78),INK); text(d,(W/2,180),'THANKS',font(FS,96),INK); d.line([60,250,W-60,250],fill=INK,width=5)
    for col in range(2):
        x0=60+col*(W/2-30)
        for k in range(26): d.line([x0,290+k*26,x0+(W/2-110)*r.uniform(0.75,1),290+k*26],fill=(110,104,96),width=8)
    im.save(T+name+'.png')
def states_board(name,W=2048,H=1024,seed=21):
    base=(120,86,60); im=wash(W,H,base,0.08,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    text(d,(W/2,70),'THANKSGIVING DAYS',font(FS,84),(244,232,200),stroke=4,sf=INK)
    cols,rows=7,3; days=[8,15,29,22,27,None,26,1,20,6,None,18,24,13,30,3,10,None,17,5,12]
    for j in range(rows):
        for i in range(cols):
            x=90+i*(W-180)/cols; y=150+j*285; w=(W-180)/cols-26; h=255; k=j*cols+i
            d.rectangle([x,y,x+w,y+h],fill=(244,238,222),outline=INK,width=6); d.rectangle([x,y,x+w,y+48],fill=(170,40,40),outline=INK,width=6)
            d.ellipse([x+w/2-14,y-12,x+w/2+14,y+16],fill=(200,190,170),outline=INK,width=4)
            for a in range(4):
                for b in range(5): text(d,(x+28+b*(w-50)/4,y+80+a*44),str(1+a*7+b),font(FSN,24),(90,84,76))
            dd=days[k]
            if dd is None: d.line([x+20,y+60,x+w-20,y+h-20],fill=(170,30,30),width=12); d.line([x+w-20,y+60,x+20,y+h-20],fill=(170,30,30),width=12)
            else:
                a,b=(dd-1)//7%4,(dd-1)%5; cx,cy=x+28+b*(w-50)/4,y+80+a*44; d.ellipse([cx-30,cy-24,cx+30,cy+24],outline=(200,30,30),width=7)
    det(im,base,seed+900,0.6).save(T+name+'.png')
def landmap(name,half=None,W=2048,H=1280,seed=31):
    base=(226,208,166); im=wash(W,H,base,0.08,seed,0.04); d=ImageDraw.Draw(im); r=random.Random(seed)
    sea=(150,180,176); d.rectangle([0,0,W,H],fill=sea)
    pts=[]
    for i in range(64):
        a=2*math.pi*i/64; rx,ry=W*0.43,H*0.36; k=1+0.08*math.sin(5*a+1)+0.05*math.cos(9*a)
        pts.append((W/2+rx*k*math.cos(a),H*0.52+ry*k*math.sin(a)*(0.8 if math.sin(a)>0 else 1.0)))
    d.polygon(pts,fill=base,outline=INK); jl(d,pts+[pts[0]],7,INK,3)
    for k in range(16):   # state lines (generic), rivers
        x=W*0.12+k*W*0.05; jl(d,[(x+r.uniform(-20,20),H*0.2),(x+r.uniform(-40,40),H*0.8)],3,mul(base,0.6),k,8)
    jl(d,[(W*0.45,H*0.2),(W*0.5,H*0.5),(W*0.48,H*0.86)],8,(90,130,170),5,10)
    text(d,(W/2,H*0.42),'THE UNITED STATES',font(FS,80),mul(base,0.45)); im=strokes(im,900,mul(base,0.8),seed,8,30,2,50)
    im=det(im,base,seed+900,0.6)
    if half:   # torn halves: the land split in two (left/right with a jagged tear)
        m=Image.new('L',(W,H),0); md=ImageDraw.Draw(m); tear=[(W*0.5+r.uniform(-50,50),y) for y in range(0,H+40,40)]
        md.polygon(([(0,0)]+tear+[(0,H)]) if half=='L' else ([(W,0)]+tear+[(W,H)]),fill=255)
        out=Image.new('RGBA',(W,H),(0,0,0,0)); out.paste(im,(0,0),m); im=out
    im.save(T+name+'.png')
def proclamation(name,W=1024,H=1400,seed=41,stamped=False):
    base=(240,232,206); im=wash(W,H,base,0.05,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    d.rectangle([30,30,W-30,H-30],outline=(120,90,50),width=12)
    text(d,(W/2,140),'PROCLAMATION',font(FS,96),INK); text(d,(W/2,240),'A DAY OF THANKSGIVING',font(FS,56),INK)
    text(d,(W/2,320),'the last Thursday of November',font(FSI,48),(70,50,40)); d.line([140,370,W-140,370],fill=INK,width=4)
    for k in range(14): d.line([110,430+k*48,110+(W-220)*r.uniform(0.7,1.0),430+k*48],fill=(110,100,90),width=9)
    if stamped:
        d.ellipse([W-380,H-380,W-120,H-120],outline=(180,30,40),width=16); text(d,(W-250,H-250),'YES',font(FS,96),(180,30,40))
    d.line([140,H-170,520,H-190],fill=(40,40,70),width=8)
    det(im,base,seed+900,0.4).save(T+name+'.png')
def deskcal(name,day,month='SEPT',W=512,H=640,seed=50):
    base=(246,242,232); im=wash(W,H,base,0.04,seed); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,150],fill=(170,40,40)); text(d,(W/2,78),month,font(FS,80),(250,240,220))
    text(d,(W/2,400),str(day),font(FS,300),INK); d.rectangle([4,4,W-4,H-4],outline=INK,width=8)
    im.save(T+name+'.png')
def yearcal(name,year,W=512,H=640,seed=51):
    base=(246,242,232); im=wash(W,H,base,0.04,seed); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,150],fill=(60,70,110)); text(d,(W/2,78),'NOV',font(FS,80),(250,240,220))
    text(d,(W/2,360),str(year),font(FS,170),INK); d.rectangle([4,4,W-4,H-4],outline=INK,width=8)
    im.save(T+name+'.png')
def bookshelf(name,seed=60,W=1024,H=1024):
    base=(96,64,44); im=wash(W,H,base,0.06,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for j in range(4):
        y1=(j+1)*H/4-14; d.rectangle([0,y1,W,y1+14],fill=mul(base,0.7),outline=INK,width=3); x=10
        while x<W-20:
            w=r.uniform(26,60); h=r.uniform(150,220); c=r.choice([(140,40,40),(40,70,110),(60,100,60),(150,120,60),(110,60,90),(200,180,140)])
            if r.random()<0.12: d.polygon([(x,y1),(x+w,y1),(x+w+40,y1-h*0.9),(x+40,y1-h*0.9)],fill=c,outline=INK); x+=w+40; continue
            d.rectangle([x,y1-h,x+w,y1],fill=c,outline=INK,width=3); d.line([x+5,y1-h+20,x+w-5,y1-h+20],fill=(220,190,110),width=3); x+=w+2
    det(im,base,seed+900,0.6).save(T+name+'.png')
def pigeonholes(name,seed=61,W=1536,H=1024):
    base=(130,96,64); im=wash(W,H,base,0.06,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for j in range(6):
        for i in range(10):
            x,y=20+i*150,20+j*166; d.rectangle([x,y,x+140,y+156],fill=mul(base,0.45),outline=INK,width=5)
            for k in range(r.randint(1,5)): yy=y+150-k*20; d.rectangle([x+10,yy-30,x+130,yy],fill=r.choice([(240,232,210),(232,222,196),(246,240,226)]),outline=INK,width=3)
    det(im,base,seed+900,0.6).save(T+name+'.png')
def lamb(name='lamb',W=512,H=512):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); K_=(50,28,42,255)
    for sx in(-1,1):
        for dx in(-1,1): d.line([W/2+sx*70+dx*20,330,W/2+sx*70+dx*20,450],fill=K_,width=22)
    for k in range(11): a=2*math.pi*k/11; d.ellipse([W/2+150*math.cos(a)-70,260+80*math.sin(a)-70,W/2+150*math.cos(a)+70,260+80*math.sin(a)+70],fill=(250,248,244,255),outline=K_,width=12)
    d.ellipse([W/2-150,180,W/2+150,340],fill=(250,248,244,255))
    d.ellipse([W/2+120,140,W/2+250,270],fill=(60,50,56,255),outline=K_,width=10); d.ellipse([W/2+190,180,W/2+215,205],fill=(255,255,255,255)); d.ellipse([W/2+198,188,W/2+210,200],fill=K_)
    d.ellipse([W/2+100,150,W/2+150,190],fill=(60,50,56,255),outline=K_,width=8)
    im.save(T+name+'.png')
def turkey(name='turkey',W=768,H=512):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); K_=(50,28,42,255)
    d.ellipse([60,380,W-60,480],fill=(246,244,238,255),outline=K_,width=10)
    d.ellipse([170,160,W-170,440],fill=(190,110,50,255),outline=K_,width=12); d.ellipse([240,200,W-300,330],fill=(220,150,80,255))
    for sx in(-1,1): d.ellipse([W/2+sx*230-60,330,W/2+sx*230+60,420],fill=(180,100,46,255),outline=K_,width=10); d.ellipse([W/2+sx*300-22,330,W/2+sx*300+22,374],fill=(250,248,240,255),outline=K_,width=6)
    im.save(T+name+'.png')
def leaf_fx(name='fx_leaves',W=512,H=512,seed=7):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); r=random.Random(seed)
    for _ in range(14):
        x,y=r.uniform(40,W-40),r.uniform(40,H-40); a=r.uniform(0,6.28); c=r.choice([(214,120,40),(190,70,40),(226,170,60)])
        pts=[(x+28*math.cos(a+t),y+16*math.sin(a+t)*(1 if t<3.14 else 0.6)) for t in [i*0.5 for i in range(13)]]
        d.polygon(pts,fill=c+(255,),outline=(50,28,42,255))
    im.save(T+name+'.png')
def tree_fall(name,seed,W=768,H=1024):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); r=random.Random(seed); K_=(50,28,42,255)
    d.polygon([(W/2-34,H),(W/2+34,H),(W/2+18,H*0.45),(W/2-18,H*0.45)],fill=(90,64,46,255),outline=K_)
    for _ in range(26):
        x,y=W/2+r.gauss(0,170),H*0.32+r.gauss(0,140); rr=r.uniform(70,130); c=r.choice([(214,120,40),(190,80,40),(226,170,60),(170,60,36)])
        d.ellipse([x-rr,y-rr*0.8,x+rr,y+rr*0.8],fill=c+(255,),outline=K_,width=8)
    im.save(T+name+'.png')
def rowhouses(name,seed,W=2048,H=1536):
    walls=[(160,74,56),(176,100,72),(140,80,66),(190,140,110)]; im=Image.new('RGB',(W,H)); r=random.Random(seed)
    x=0; d=ImageDraw.Draw(im)
    while x<W:
        w=int(r.uniform(420,560)); c=r.choice(walls); P.facade('_tmpf',c,P.SHOPS[0],seed+x,W=1024,H=1536,floors=3,cols=3,era=1860,xmas=False)
        f=Image.open(T+'_tmpf.png').resize((w,H)); im.paste(f,(x,0)); x+=w
    det(im,(160,90,70),seed+900,0.5).save(T+name+'.png')
def sign(name,txt,bg,fg,W=1024,H=256,border=None,f=None,sz=120):
    im=wash(W,H,bg,0.06,5); d=ImageDraw.Draw(im)
    if border: d.rectangle([12,12,W-12,H-12],outline=border,width=14)
    ft=font(f or FS,sz)
    while d.textlength(txt,font=ft)>W-90: sz-=4; ft=font(f or FS,sz)
    text(d,(W/2,H/2+6),txt,ft,fg,stroke=2,sf=mul(fg,0.6)); det(im,bg,9,0.5).save(T+name+'.png')
def cloth(name,base,seed,check=None,W=1024,H=1024):
    im=wash(W,H,base,0.05,seed); d=ImageDraw.Draw(im)
    if check:
        for i in range(0,W,128): d.rectangle([i,0,i+48,H],fill=check+(0,))
        ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
        for i in range(0,W,128): od.rectangle([i,0,i+48,H],fill=check+(90,)); od.rectangle([0,i,W,i+48],fill=check+(90,))
        im=Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB')
    im=strokes(im,800,mul(base,0.85),seed,10,40,2,50); det(im,base,seed+900,0.5).save(T+name+'.png')
def framed_letter(name,W=768,H=1024):
    letter('_fl',77,W,H,14,head='Dear Sir,')
    im=Image.open(T+'_fl.png'); d=ImageDraw.Draw(im); d.rectangle([0,0,W,H],outline=(150,110,50),width=40); im.save(T+name+'.png')
def poster(src,name='poster'):
    im=Image.open(src).convert('RGB'); im.save(T+name+'.png'); im.resize((im.width//2,im.height//2),Image.LANCZOS).save('/root/dc/poster_2k.png')
def fx_cards():
    # smoke puff, splash, sand spray, sparkle: flat FX cards (Rick flat FX 12-27 f)
    for nm,col,seed in (('fx_smoke',(236,232,226),1),('fx_splash',(230,244,248),2),('fx_dust',(230,214,180),3),('fx_paper',(250,246,234),4)):
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
if __name__=='__main__':
    P.wallpaper('wp_office',(70,96,74),(196,170,100),seed=91)
    P.wallpaper('wp_pres',(214,200,168),(150,60,60),seed=92)
    P.wallpaper('wp_today',(196,150,104),(236,214,170),seed=93)
    P.wallpaper('wp_hall',(150,60,52),(214,176,110),seed=94)
    plaster('plaster_clerk',(206,190,150),21,wainscot=(120,86,58)); plaster('plaster_print',(190,176,150),22,wainscot=(90,70,56))
    P.woodfloor('floor_office',seed=95,base=(140,92,58)); P.woodfloor('floor_clerk',seed=96,base=(150,110,72)); P.woodfloor('floor_today',seed=97,base=(170,120,76))
    planks('desk',(120,76,46),31); planks('deskdark',(84,52,34),32); planks('crate',(170,130,86),33)
    brick('brick_print',(150,80,60),34); cobble(); carpet('carpet_pres',(120,40,46),(214,176,110),35); carpet('carpet_today',(70,90,110),(200,170,120),36)
    sky('sky_fall',(110,150,200),(250,214,170),17,6,(252,244,232)); sky('sky_today',(96,150,206),(246,224,190),18,7,(252,248,240))
    view_rooftops('win_phil',((130,170,210),(246,222,186)),seed=5); view_rooftops('win_phil_night',((24,30,70),(70,60,110)),night=True,seed=5)
    view_rooftops('win_wash',((140,176,212),(246,226,190)),seed=6,dome=True); view_rooftops('win_war',((30,30,60),(90,50,70)),night=True,seed=6,dome=True,glow=True)
    view_rooftops('win_today',((110,160,210),(250,226,190)),seed=8)
    view_rooftops('street_far',((120,160,206),(250,214,170)),seed=9,dome=True)
    for i in range(6): letter(f'letter{i}',100+i)
    letter('letter_hero',120,head='Dear Sir,'); envelope('env',121); magazine('magazine'); page_print('page_print')
    states_board('states_board'); landmap('map_land'); landmap('map_L',half='L'); landmap('map_R',half='R')
    proclamation('procl'); proclamation('procl_yes',stamped=True)
    for i,dd in enumerate([28,29,30,1,2,3]): deskcal(f'dcal{i}',dd,'SEPT' if dd>=28 else 'OCT')
    for y in (1846,1850,1854,1858,1861,1863): yearcal(f'ycal{y}',y)
    bookshelf('shelf'); pigeonholes('pigeon'); lamb(); turkey(); leaf_fx(); tree_fall('tree0',1); tree_fall('tree1',2)
    rowhouses('rows',70)
    sign('sign_print',"LADY'S BOOK  PRINT ROOM",(40,60,90),(244,232,200),border=(214,190,120))
    sign('banner_thanks','GIVE THANKS',(150,40,40),(250,236,200),W=2048,H=384,border=(214,176,110),sz=200)
    sign('sign_mail','U.S. MAIL',(60,70,100),(244,232,200),border=(214,190,120))
    cloth('cloth_hall',(240,234,220),40); cloth('cloth_today',(236,228,214),41,check=(170,60,50)); cloth('sackcloth',(196,170,120),42)
    framed_letter('framed_letter')
    fx_cards(); glow()
    print('PAINT_OK')
