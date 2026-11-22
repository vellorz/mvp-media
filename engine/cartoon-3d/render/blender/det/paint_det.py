# Painted textures for the Detroit Thanksgiving short (mon-detroit). Own textures; helper functions from the BF paint.py.
import numpy as np, random, math
from PIL import Image, ImageDraw, ImageFilter
import paint as P
from paint import T, INK, wash, strokes, jl, jr, mul, text, font, FS, FSN, paintdetail, noise
def fin(im,base,seed,name,dens=1.0):
    im=strokes(im,500,mul(base,0.78),seed,6,20,2,40); im=paintdetail(im,Image.new('L',im.size,255),base,seed+900,1,dens=dens); im.save(T+name+'.png')
# ---------- sky + Detroit 1934 skyline (generic art-deco towers, no real-building copies) ----------
def skyline34(name,W=4096,H=1500,seed=31):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); r=random.Random(seed); far=(150,156,172)
    x=0
    while x<W:
        w=r.uniform(140,320); h=r.uniform(260,700); c=mul(far,r.uniform(0.9,1.08))
        d.rectangle([x,H-h,x+w,H],fill=c); jr(d,x,H-h,x+w,H,3,mul(far,0.6),int(x))
        for yy in range(int(H-h+30),H-20,44):
            for xx in range(int(x+16),int(x+w-16),32): d.rectangle([xx,yy,xx+14,yy+22],fill=mul(c,0.8))
        x+=w+r.uniform(-20,30)
    for cx,h,w in [(W*0.3,1250,260),(W*0.55,1400,300),(W*0.78,1100,240)]:   # stepped deco towers
        c=(128,120,130); y=H-h
        for k in range(5):
            ww=w*(1-k*0.16); hh=h*(0.55 if k==0 else 0.11); d.rectangle([cx-ww/2,y if k else H-h*0.55,cx+ww/2,H if k==0 else y+hh],fill=mul(c,1+k*0.03)); jr(d,cx-ww/2,y if k else H-h*0.55,cx+ww/2,H if k==0 else y+hh,4,mul(c,0.55),k)
            if k==0: y=H-h*0.55
            y-=hh if k else 0
        d.polygon([(cx-24,H-h),(cx+24,H-h),(cx,H-h-120)],fill=c)
        for yy in range(int(H-h*0.55)+30,H-30,52):
            for xx in range(int(cx-w/2+20),int(cx+w/2-20),36): d.rectangle([xx,yy,xx+12,yy+30],fill=(96,90,104))
    im.save(T+name+'.png')
# ---------- stadium: grass field with yard lines, wooden bleachers, stadium wall, scoreboard ----------
def field(name='field',W=2048,H=2048,seed=41):
    base=(92,140,70); im=wash(W,H,base,0.10,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for j in range(0,H,128): d.rectangle([0,j,W,j+64],fill=mul(base,1.06))      # mowing bands
    for j in range(0,H,256): d.rectangle([0,j-6,W,j+6],fill=(236,234,222))         # yard lines (every 5 yd)
    for j in range(0,H,51):
        for x in (W*0.33,W*0.66): d.rectangle([x-12,j-2,x+12,j+2],fill=(230,228,214))
    for _ in range(90): x,y=r.uniform(0,W),r.uniform(0,H); d.ellipse([x,y,x+r.uniform(30,110),y+r.uniform(14,40)],fill=(120,110,80))   # worn patches (late season)
    im=strokes(im,4000,(60,110,50),seed,4,14,2,70,ang=math.pi/2); fin(im,(80,126,62),seed,name)
def bleacher(name='bleacher',W=1024,H=1024,seed=43):
    base=(150,112,76); im=wash(W,H,base,0.08,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for j in range(0,H,64):
        c=mul(base,r.uniform(0.88,1.1)); d.rectangle([0,j,W,j+40],fill=c); d.rectangle([0,j+40,W,j+64],fill=mul(base,0.55)); jl(d,[(0,j+40),(W,j+40)],4,mul(base,0.35),j)
        for k in range(6): x=r.uniform(0,W); d.arc([x,j+6,x+50,j+34],200,340,fill=mul(base,0.7),width=2)
        for x in range(0,W,170): d.ellipse([x+r.uniform(0,10),j+16,x+12,j+26],fill=(80,70,60))   # bolts
    fin(im,base,seed,name)
def stadwall(name='stadwall',W=1024,H=1024,seed=45):
    base=(176,160,140); im=wash(W,H,base,0.07,seed); d=ImageDraw.Draw(im)
    for j in range(0,H,40):
        off=(j//40%2)*48
        for i in range(-1,W//96+1): jr(d,i*96+off,j,i*96+off+96,j+40,3,mul(base,0.6),i+j,fill=mul(base,random.Random(i*7+j).uniform(0.9,1.08)))
    d.rectangle([0,0,W,90],fill=(60,80,110)); d.rectangle([0,90,W,104],fill=(220,190,90))
    fin(im,base,seed,name)
def scoreboard(name,home,vis,qtr='FINAL',W=1536,H=768,seed=47):
    im=Image.new('RGB',(W,H),(36,44,40)); d=ImageDraw.Draw(im)
    d.rectangle([14,14,W-14,H-14],outline=(220,190,90),width=16)
    text(d,(W*0.27,110),'HOME',font(FS,96),(240,232,200)); text(d,(W*0.73,110),'VISITORS',font(FS,96),(240,232,200))
    for x,v in ((W*0.27,home),(W*0.73,vis)):
        d.rectangle([x-230,190,x+230,560],fill=(20,22,20)); jr(d,x-230,190,x+230,560,6,(220,190,90),int(x))
        text(d,(x,380),str(v),font(FSN,300),(250,240,200))
    text(d,(W/2,650),qtr,font(FSN,90),(250,200,80))
    paintdetail(im,Image.new('L',im.size,255),(50,56,52),seed,1,neutral=True,dens=0.4).save(T+name+'.png')
def ticketbooth(name,sold=False,W=1024,H=1024,seed=49):
    base=(200,70,56); im=wash(W,H,base,0.07,seed); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,150],fill=(240,224,180)); jr(d,0,0,W,150,6,INK,1); text(d,(W/2,78),'TICKETS',font(FS,110),(160,30,30))
    for k in range(0,W,64): d.rectangle([k,150,k+32,190],fill=(240,224,180))
    d.rectangle([260,330,764,700],fill=(70,84,96)); jr(d,260,330,764,700,8,INK,2); d.rectangle([380,640,644,700],fill=(110,80,60))
    if sold:
        d.polygon([(120,420),(904,380),(920,580),(136,620)],fill=(250,240,200),outline=INK); text(d,(520,500),'SOLD OUT',font(FS,112),(190,30,30))
    for y in range(760,H,48): d.line([0,y,W,y],fill=mul(base,0.7),width=6)
    fin(im,base,seed,name,0.7)
# ---------- interiors ----------
def studio(name='studiowall',W=1024,H=1024,seed=51):   # acoustic tiles + wainscot
    base=(170,150,120); im=wash(W,H,base,0.06,seed); d=ImageDraw.Draw(im)
    for j in range(0,H-260,96):
        for i in range(0,W,96):
            jr(d,i+4,j+4,i+92,j+92,4,mul(base,0.55),i+j,fill=mul(base,random.Random(i+j*3).uniform(0.92,1.08)))
            for a in range(3):
                for b in range(3): d.ellipse([i+20+a*26,j+20+b*26,i+28+a*26,j+28+b*26],fill=mul(base,0.6))
    d.rectangle([0,H-260,W,H],fill=(110,74,50))
    for x in range(0,W,128): jr(d,x+10,H-240,x+118,H-30,6,(60,40,28),x)
    d.rectangle([0,H-284,W,H-260],fill=(80,52,36))
    fin(im,base,seed,name)
def usmap(name,lit,W=2048,H=1280,seed=53):
    """stylised continental US (hand-drawn outline, no borders) with 94 station bulbs; lit = how many are on, filled east to west and back"""
    im=wash(W,H,(214,200,160),0.06,seed); d=ImageDraw.Draw(im)
    jr(d,20,20,W-20,H-20,14,(110,74,50),1)
    pts=[(0.08,0.18),(0.30,0.16),(0.48,0.17),(0.58,0.20),(0.62,0.28),(0.66,0.22),(0.72,0.26),(0.80,0.20),(0.90,0.12),(0.93,0.20),(0.88,0.30),(0.86,0.42),(0.82,0.52),
         (0.84,0.60),(0.80,0.72),(0.84,0.88),(0.80,0.90),(0.74,0.76),(0.62,0.74),(0.54,0.80),(0.46,0.92),(0.40,0.80),(0.32,0.74),(0.22,0.70),(0.12,0.62),(0.07,0.48),(0.06,0.32)]
    P_=[(x*W,y*H) for x,y in pts]; d.polygon(P_,fill=(196,206,160)); jl(d,P_+[P_[0]],8,(80,70,50),3,2.0)
    r=random.Random(seed); bulbs=[]
    from matplotlib.path import Path as MP
    mp=MP(P_)
    while len(bulbs)<94:
        x,y=r.uniform(0.07*W,0.92*W),r.uniform(0.16*H,0.9*H)
        if mp.contains_point((x,y)) and all((x-a)**2+(y-b)**2>48**2 for a,b in bulbs): bulbs.append((x,y))
    det=(0.60*W,0.27*H); bulbs.sort(key=lambda p:(p[0]-det[0])**2+(p[1]-det[1])**2)
    for i,(x,y) in enumerate(bulbs):
        on=i<lit; c=(255,214,90) if on else (110,100,80)
        if on: d.ellipse([x-26,y-26,x+26,y+26],fill=(255,240,180))
        d.ellipse([x-14,y-14,x+14,y+14],fill=c,outline=INK,width=4)
    d.ellipse([det[0]-30,det[1]-30,det[0]+30,det[1]+30],fill=(200,40,40),outline=INK,width=6); d.polygon([(det[0],det[1]-80),(det[0]+16,det[1]-30),(det[0]-16,det[1]-30)],fill=(80,70,60))
    text(d,(W/2,H-70),'COAST TO COAST',font(FS,80),(110,40,30))
    im.save(T+name+'.png')
def calendar(name,top,big,sub='',circle=False,grey=False,W=768,H=1024,seed=55):
    base=(246,240,226) if not grey else (196,192,184); im=wash(W,H,base,0.03,seed); d=ImageDraw.Draw(im)
    def fit(t,f0,mw,p=FS):
        z=f0
        while d.textlength(t,font=font(p,z))>mw: z-=4
        return font(p,z)
    d.rectangle([0,0,W,200],fill=(170,40,40) if not grey else (110,104,100)); text(d,(W/2,110),top,fit(top,92,W-70),(250,240,220))
    text(d,(W/2,470),big,fit(big,330,W-80,FSN),(40,34,30) if not grey else (90,86,80)); text(d,(W/2,760),sub,font(FS,70),(140,40,40) if not grey else (80,76,72))
    if circle: d.ellipse([W/2-260,300,W/2+260,640],outline=(210,30,30),width=22)
    for k in range(5): d.ellipse([60+k*150,20,90+k*150,50],fill=(230,230,230),outline=INK,width=4)
    jr(d,0,0,W,H,8,INK,2); im.save(T+name+'.png')
def newspaper34(name,head,sub,date,W=1024,H=1400,seed=57):
    im=wash(W,H,(238,232,214),0.04,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    text(d,(W/2,70),'THE MOTOR CITY EVENING POST',font(FS,50),INK); d.line([40,110,W-40,110],fill=INK,width=4)
    text(d,(W/2,135),date+'     3 CENTS',font(FSN,24),INK); d.line([40,158,W-40,158],fill=INK,width=2)
    fs=150; fh=font(FS,fs)
    while d.textlength(head,font=fh)>W-60: fs-=6; fh=font(FS,fs)
    text(d,(W/2,170+fs*0.6),head,fh,INK); y=200+fs*1.2; text(d,(W/2,y),sub,font(FS,40),(60,50,46))
    y+=50; d.rectangle([60,y,W/2-20,y+380],fill=(170,164,150)); jr(d,60,y,W/2-20,y+380,3)
    d.ellipse([140,y+120,330,y+250],outline=(90,86,80),width=10); d.line([235,y+120,235,y+250],fill=(90,86,80),width=6)   # baseball drawing
    for col in range(2):
        x0=W/2+20 if col==0 else 60; ys=y if col==0 else y+400
        for k in range(26 if col==0 else 14): d.line([x0,ys+k*16,x0+(W/2-80)*r.uniform(0.8,1),ys+k*16],fill=(120,114,104),width=6)
    im.save(T+name+'.png')
def lionsbanner(name,n=5,W=2048,H=512):
    """a sign painter's banner: the word LIONS appears letter by letter (n letters). Plain lettering, no emblem."""
    im=Image.new('RGB',(W,H),(236,226,196)); d=ImageDraw.Draw(im)
    d.rectangle([24,24,W-24,H-24],outline=(60,80,120),width=20)
    full='LIONS'; f=font(FS,300); tw=d.textlength(full,font=f); x=W/2-tw/2
    for i,ch in enumerate(full[:n]):
        d.text((x,H/2),ch,font=f,fill=(60,80,120),anchor='lm'); x+=d.textlength(ch,font=f)
    paintdetail(im,Image.new('L',im.size,255),(220,210,180),61,1,neutral=True,dens=0.4).save(T+name+'.png')
def onair(name,on):
    W,H=768,256; im=Image.new('RGB',(W,H),(200,40,36) if on else (90,40,38)); d=ImageDraw.Draw(im)
    d.rectangle([10,10,W-10,H-10],outline=INK,width=14); text(d,(W/2,H/2),'ON AIR',font(FS,140),(255,240,200) if on else (150,110,100))
    im.save(T+name+'.png')
def tvfield(name,W=1280,H=720,seed=63):   # modern TV picture: generic green field, tiny white and dark dots, no logos or graphics
    im=wash(W,H,(70,150,70),0.08,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for x in range(0,W,110): d.line([x,0,x-200,H],fill=(236,236,226),width=5)
    for k in range(22):
        x,y=r.uniform(100,W-100),r.uniform(160,H-120); c=(240,240,240) if k%2 else (50,60,90)
        d.ellipse([x-12,y-30,x+12,y-6],fill=c); d.rectangle([x-12,y-6,x+12,y+26],fill=c)
    d.ellipse([W*0.52,H*0.4,W*0.52+26,H*0.4+16],fill=(130,70,40))
    d.rectangle([0,0,W,90],fill=(40,60,110)); d.rectangle([0,90,W,110],fill=(30,30,40))   # crowd band
    for k in range(400): x,y=r.uniform(0,W),r.uniform(0,90); d.ellipse([x,y,x+6,y+6],fill=r.choice([(240,220,200),(200,80,60),(80,100,160),(250,250,250)]))
    im.save(T+name+'.png')
def modernwall(name,base,W=1024,H=1024,seed=65):   # painted plaster above white shiplap wainscot
    im=wash(W,H,base,0.06,seed); d=ImageDraw.Draw(im)
    for _ in range(9): x,y=random.Random(_).uniform(0,W),random.Random(_+50).uniform(0,H-300); d.ellipse([x,y,x+260,y+180],fill=mul(base,1.03))
    d.rectangle([0,H-300,W,H],fill=(236,232,222))
    for x in range(0,W,64): jl(d,[(x,H-300),(x,H)],5,(170,164,150),x)
    d.rectangle([0,H-318,W,H-300],fill=(250,248,240)); jl(d,[(0,H-318),(W,H-318)],5,(150,144,130),2)
    fin(im,base,seed,name,1.2)
def rug(name,c1,c2,W=1024,H=1024,seed=67):
    im=wash(W,H,c1,0.06,seed); d=ImageDraw.Draw(im)
    for k in range(6): m=60+k*70; jr(d,m,m,W-m,H-m,14,c2 if k%2==0 else mul(c1,0.7),k)
    for x in range(120,W-120,80):
        for y in range(120,H-120,80): d.polygon([(x,y-22),(x+22,y),(x,y+22),(x-22,y)],fill=mul(c2,1.1))
    fin(im,c1,seed,name)
if __name__=='__main__':
    walls=[(150,70,56),(132,66,58),(170,100,72),(120,64,60),(160,90,66),(140,96,84)]
    SH=P.SHOPS; picks=[SH[3],SH[4],SH[1],SH[5],SH[6],SH[2]]
    for i in range(6): P.facade(f'dfac{i}',walls[i],picks[i],300+i,era=1934,xmas=False)
    P.sky('dsky',(110,140,184),(236,214,184),seed=33,clouds=9); P.sky('dsky_grey',(130,146,170),(230,216,196),seed=35,clouds=11)
    skyline34('dskyline')
    P.sidewalk(seed=58); import os; os.replace(T+'sidewalk.png',T+'dsidewalk.png')
    P.asphalt(seed=59); os.replace(T+'asphalt.png',T+'dasphalt.png')
    field(); bleacher(); stadwall()
    scoreboard('score0',0,0,'1ST QTR'); scoreboard('score1',16,19,'FINAL')
    ticketbooth('booth0'); ticketbooth('booth1',sold=True)
    studio(); P.wallpaper('dining',(150,110,90),(190,150,110),seed=69); P.wallpaper('office34',(96,120,100),(120,150,120),seed=71)
    P.woodfloor('dwood',seed=73,base=(140,92,58)); P.woodfloor('dwood2',seed=74,base=(176,130,86))
    for n in (0,10,30,60,94): usmap(f'map{n}',n)
    calendar('cal1934','NOVEMBER 1934','29','THANKSGIVING',circle=True)
    for y in range(1935,1946):
        war=1939<=y<=1944
        calendar(f'cal{y}',f'THANKSGIVING {y}','NO GAME' if war else 'GAME DAY','' ,grey=war,seed=55+y)
    calendar('cal2026','THANKSGIVING 2026','GAME DAY','',seed=99)
    newspaper34('paperTigers','TIGERS WIN PENNANT','Whole town goes baseball crazy','SEPTEMBER 1934')
    for n in range(6): lionsbanner(f'lions{n}',n)
    onair('onair0',False); onair('onair1',True); tvfield('tvfield')
    modernwall('livwall',(120,150,170)); rug('rug34',(150,60,50),(220,180,110)); rug('rugM',(200,190,170),(110,130,150),seed=68)
    print('PAINT_DET_OK')
