# Painted textures for "Black Friday" (Philadelphia). PIL only. Output /root/bf/tex/
import numpy as np, random, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont
T='/root/bf/tex/'; INK=(46,34,30)
FS='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'; FSN='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FM='/home/user/mvp-media/engine/cartoon-3d/project/public/havasu/fonts/Montserrat.ttf'
def font(p,s):
    f=ImageFont.truetype(p,s)
    if p==FM:
        try: f.set_variation_by_name('Black')
        except Exception: pass
    return f
def noise(w,h,s,seed):
    r=np.random.RandomState(seed); a=r.rand(max(2,h//s),max(2,w//s))
    return np.asarray(Image.fromarray((a*255).astype(np.uint8)).resize((w,h),Image.BICUBIC),np.float32)/255
def wash(w,h,rgb,amp=0.08,seed=0,grad=0.0):
    n=noise(w,h,64,seed)*0.6+noise(w,h,16,seed+1)*0.3+noise(w,h,4,seed+2)*0.1
    g=np.linspace(1+grad,1-grad,h)[:,None]
    a=np.array(rgb,np.float32)[None,None,:]*(1+(n[...,None]-0.5)*2*amp)*g[...,None]
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def strokes(im,n,col,seed,lmin=8,lmax=30,wid=2,alpha=60,ang=None):
    r=random.Random(seed); ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    for _ in range(n):
        x,y=r.uniform(0,im.width),r.uniform(0,im.height); L=r.uniform(lmin,lmax)
        a=(ang if ang is not None else r.uniform(0,math.pi))+r.uniform(-0.2,0.2)
        d.line([x,y,x+L*math.cos(a),y+L*math.sin(a)],fill=col+(alpha,),width=wid)
    return Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB')
def jl(d,pts,w=3,col=INK,seed=0,j=1.2):
    r=random.Random(seed); d.line([(x+r.uniform(-j,j),y+r.uniform(-j,j)) for x,y in pts],fill=col,width=w,joint='curve')
def jr(d,x0,y0,x1,y1,w=3,col=INK,seed=0,fill=None):
    if fill: d.rectangle([x0,y0,x1,y1],fill=fill)
    jl(d,[(x0,y0),(x1,y0),(x1,y1),(x0,y1),(x0,y0)],w,col,seed)
def mul(c,k): return tuple(max(0,min(255,int(v*k))) for v in c[:3])
def text(d,xy,s,f,fill,anchor='mm',stroke=0,sf=INK): d.text(xy,s,font=f,fill=fill,anchor=anchor,stroke_width=stroke,stroke_fill=sf)
# ---------------- brick building facade with a shop front ----------------
SHOPS=[('HATS',(150,40,40),(240,220,170)),('TOYS',(40,90,140),(250,220,90)),('DRUGS',(30,100,70),(240,240,230)),('DINER',(170,60,40),(250,240,200)),
       ('RADIO & TV',(60,60,90),(250,200,90)),('SHOES',(110,70,40),(245,230,190)),('BAKERY',(200,120,60),(255,245,220)),('JEWELERS',(40,40,40),(230,200,110))]
def facade(name,wall,shop,seed,W=1024,H=1536,floors=3,cols=3,era=1950,xmas=True):
    r=random.Random(seed); im=wash(W,H,wall,0.08,seed,0.06); d=ImageDraw.Draw(im)
    # bricks
    bh=18; bw=46
    for j in range(H//bh):
        off=(j%2)*bw//2
        for i in range(-1,W//bw+1):
            c=mul(wall,r.uniform(0.86,1.1)); x=i*bw+off; y=j*bh
            d.rectangle([x+1,y+1,x+bw-2,y+bh-2],fill=c)
    d=ImageDraw.Draw(im)
    gf=int(H*0.36); top=H-gf  # ground floor height
    fh=(top-90)//floors
    for f in range(floors):
        for c in range(cols):
            cx=W*(c+0.5)/cols; y0=70+f*fh+fh*0.16; y1=y0+fh*0.62; wv=W/cols*0.26
            d.rectangle([cx-wv-10,y0-14,cx+wv+10,y0],fill=mul(wall,1.25)); jr(d,cx-wv-10,y0-14,cx+wv+10,y0,2,seed=f*5+c)  # lintel
            kind=r.choice(['dark','shade','curtain','lit','lit','person','plant'])
            glass=(44,52,66) if kind!='lit' else (250,214,140)
            d.rectangle([cx-wv,y0,cx+wv,y1],fill=glass)
            if kind=='shade': d.rectangle([cx-wv,y0,cx+wv,y0+(y1-y0)*r.uniform(0.3,0.6)],fill=(226,206,160))
            if kind=='curtain':
                for sx in(-1,1): d.polygon([(cx+sx*wv,y0),(cx+sx*wv*0.2,y0),(cx+sx*wv,y1)],fill=(190,70,60))
            if kind=='person':
                d.ellipse([cx-24,y0+40,cx+24,y0+88],fill=(240,236,226),outline=INK,width=3); d.rectangle([cx-30,y0+88,cx+30,y1],fill=(80,90,120))
            if kind=='plant': d.ellipse([cx-wv*0.8,y1-40,cx+wv*0.8,y1+10],fill=(80,130,70),outline=INK,width=2)
            d.line([cx,y0,cx,y1],fill=(220,210,190),width=6); d.line([cx-wv,(y0+y1)/2,cx+wv,(y0+y1)/2],fill=(220,210,190),width=6)
            jr(d,cx-wv,y0,cx+wv,y1,3,seed=f*7+c)
            d.rectangle([cx-wv-12,y1,cx+wv+12,y1+12],fill=mul(wall,1.3)); jl(d,[(cx-wv-12,y1+12),(cx+wv+12,y1+12)],2,seed=f+c)
    # cornice
    d.rectangle([0,0,W,46],fill=mul(wall,0.7));
    for i in range(0,W,32): d.rectangle([i+4,46,i+20,62],fill=mul(wall,0.6))
    jl(d,[(0,46),(W,46)],3,seed=seed)
    # ground floor shop
    sname,sc_,sfg=shop
    d.rectangle([0,top,W,H],fill=mul(sc_,0.9)); jl(d,[(0,top),(W,top)],4,seed=seed+1)
    d.rectangle([30,top+20,W-30,top+130],fill=sc_); jr(d,30,top+20,W-30,top+130,4,seed=seed+2)
    fsz=96 if len(sname)<8 else 70
    text(d,(W/2,top+76),sname,font(FS,fsz),sfg,stroke=3)
    # windows + door
    dw=170; dx=W/2-dw/2
    for (a,b) in [(40,dx-20),(dx+dw+20,W-40)]:
        d.rectangle([a,top+160,b,H-60],fill=(60,72,86))
        # display goods
        for k in range(int((b-a)//90)):
            gx=a+30+k*90+r.uniform(-8,8); gy=H-60
            kind=r.choice(['box','box','hat','round','tall'])
            col=r.choice([(200,60,50),(60,120,180),(230,190,60),(90,150,90),(220,220,210),(160,90,160)])
            if kind=='box': h_=r.uniform(60,120); d.rectangle([gx-34,gy-h_,gx+34,gy],fill=col,outline=INK,width=3); d.line([gx,gy-h_,gx,gy],fill=(250,240,200),width=6); d.line([gx-34,gy-h_/2,gx+34,gy-h_/2],fill=(250,240,200),width=6)
            elif kind=='hat': d.ellipse([gx-44,gy-30,gx+44,gy-6],fill=col,outline=INK,width=3); d.rectangle([gx-26,gy-74,gx+26,gy-22],fill=col,outline=INK,width=3)
            elif kind=='round': d.ellipse([gx-34,gy-70,gx+34,gy],fill=col,outline=INK,width=3)
            else: d.rectangle([gx-18,gy-150,gx+18,gy],fill=col,outline=INK,width=3); d.ellipse([gx-24,gy-180,gx+24,gy-136],fill=mul(col,1.2),outline=INK,width=3)
        if xmas:  # Thanksgiving / holiday dressing: price cards + garland
            for k in range(int((b-a)//120)):
                px=a+40+k*120; d.rectangle([px,top+190,px+70,top+236],fill=(250,246,230)); jr(d,px,top+190,px+70,top+236,2,seed=k)
                text(d,(px+35,top+213),r.choice(['$1.98','$2.49','$4.95','$0.99','SALE']),font(FSN,22),(170,30,30))
            for x in range(int(a),int(b),24): d.ellipse([x,top+150+8*math.sin(x/30),x+26,top+176+8*math.sin(x/30)],fill=(60,120,60),outline=(30,70,30))
        d.line([a,top+160,b,H-60],fill=(150,170,190),width=3)  # glass glint
        jr(d,a,top+160,b,H-60,5,seed=int(a))
    d.rectangle([dx,top+160,dx+dw,H],fill=(96,62,40)); d.rectangle([dx+20,top+190,dx+dw-20,top+440],fill=(70,84,100)); jr(d,dx,top+160,dx+dw,H,5,seed=9)
    d.ellipse([dx+dw-40,top+460,dx+dw-24,top+476],fill=(220,180,60))
    d.rectangle([0,H-60,W,H],fill=(130,120,110)); jl(d,[(0,H-60),(W,H-60)],3)
    im=strokes(im,600,mul(wall,0.7),seed,6,22,2,45)
    im.filter(ImageFilter.GaussianBlur(0.5)).save(T+name+'.png')
def dept_store(name,era=1950,W=2048,H=1536,seed=40,banner=None):
    wall=(214,196,166) if era<1970 else (206,190,170)
    r=random.Random(seed); im=wash(W,H,wall,0.06,seed,0.05); d=ImageDraw.Draw(im)
    for j in range(H//40):  # stone courses
        jl(d,[(0,j*40),(W,j*40)],2,mul(wall,0.75),seed+j,0.8)
        for i in range(0,W,160): x=i+(j%2)*80; jl(d,[(x,j*40),(x,j*40+40)],2,mul(wall,0.75),seed+i,0.6)
    top=int(H*0.42)
    for f in range(2):
        for c in range(8):
            x0=60+c*245; y0=90+f*260
            d.rectangle([x0,y0,x0+150,y0+200],fill=(56,64,80) if r.random()<0.6 else (248,214,146))
            for k in range(1,3): d.line([x0+k*50,y0,x0+k*50,y0+200],fill=wall,width=5)
            d.line([x0,y0+100,x0+150,y0+100],fill=wall,width=5); jr(d,x0,y0,x0+150,y0+200,3,seed=c+f*9)
            d.rectangle([x0-10,y0+200,x0+160,y0+214],fill=mul(wall,1.15))
    # name band
    d.rectangle([0,top-120,W,top-10],fill=(30,60,50)); jr(d,0,top-120,W,top-10,4)
    text(d,(W/2,top-64),'HARTWELL & SONS' if era<1970 else 'HARTWELL\'S',font(FS,84),(236,206,120),stroke=2)
    # ground floor display windows (big)
    for c in range(4):
        x0=40+c*510; d.rectangle([x0,top+20,x0+430,H-70],fill=(70,82,96)); jr(d,x0,top+20,x0+430,H-70,6,seed=c)
        d.rectangle([x0,top+20,x0+430,top+70],fill=(160,40,40) if era<1970 else (30,30,30)); 
        for k in range(0,430,40): d.polygon([(x0+k,top+70),(x0+k+40,top+70),(x0+k+20,top+100)],fill=(160,40,40) if era<1970 else (30,30,30))
    d.rectangle([0,H-70,W,H],fill=(120,110,100))
    if banner: pass
    im=strokes(im,900,mul(wall,0.7),seed,6,24,2,40); im.filter(ImageFilter.GaussianBlur(0.5)).save(T+name+'.png')
def asphalt(W=2048,H=2048,seed=50):
    im=wash(W,H,(84,82,86),0.10,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for _ in range(140):  # cracks + patches + oil
        x,y=r.uniform(0,W),r.uniform(0,H)
        if r.random()<0.4: d.ellipse([x,y,x+r.uniform(40,140),y+r.uniform(20,70)],fill=(64,62,66))
        else: jl(d,[(x,y),(x+r.uniform(-60,60),y+r.uniform(20,80)),(x+r.uniform(-90,90),y+r.uniform(60,140))],2,(54,52,56),int(x))
    # trolley rails (two pairs), lane dashes, crosswalk at both ends
    for cx in (W*0.36,W*0.64):
        for o in (-38,38): d.line([cx+o,0,cx+o,H],fill=(150,150,156),width=8); d.line([cx+o+5,0,cx+o+5,H],fill=(60,58,60),width=3)
        for y in range(0,H,40): d.rectangle([cx-48,y,cx+48,y+8],fill=(70,66,64))
    for y in range(0,H,160): d.rectangle([W/2-8,y,W/2+8,y+90],fill=(236,220,150))
    for sx in(0.08,0.92): d.line([W*sx,0,W*sx,H],fill=(220,220,210),width=10)
    for y0 in (40,H-260):
        for x in range(int(W*0.1),int(W*0.9),110): d.rectangle([x,y0,x+70,y0+220],fill=(232,230,220)); jr(d,x,y0,x+70,y0+220,2,(120,118,112),x)
    for k in range(5): x,y=r.uniform(200,W-200),r.uniform(300,H-300); d.ellipse([x,y,x+90,y+90],fill=(60,58,62),outline=(30,30,30),width=4); d.line([x+10,y+45,x+80,y+45],fill=(40,40,40),width=3)
    for k in range(6): x,y=r.uniform(0,W),r.uniform(0,H); d.ellipse([x,y,x+r.uniform(80,200),y+r.uniform(30,70)],fill=(70,80,96))  # puddles
    strokes(im,2500,(110,108,112),seed,4,16,2,50).save(T+'asphalt.png')
def sidewalk(W=1024,H=1024,seed=52):
    base=(196,188,176); im=wash(W,H,base,0.07,seed); d=ImageDraw.Draw(im); r=random.Random(seed); S=170
    for j in range(H//S+1):
        for i in range(W//S+1):
            jr(d,i*S,j*S,i*S+S,j*S+S,3,(130,124,116),i*13+j,fill=mul(base,r.uniform(0.92,1.06)))
            if r.random()<0.25: jl(d,[(i*S+r.uniform(10,80),j*S+10),(i*S+r.uniform(60,150),j*S+r.uniform(80,160))],2,(120,112,104),i+j)
    for _ in range(60): x,y=r.uniform(0,W),r.uniform(0,H); d.ellipse([x,y,x+8,y+8],fill=(150,144,138))
    for _ in range(10): x,y=r.uniform(0,W),r.uniform(0,H); d.polygon([(x,y),(x+26,y+8),(x+10,y+22)],fill=(190,120,50))  # leaves
    strokes(im,900,(150,144,136),seed,5,18,2,45).save(T+'sidewalk.png')
def sky(name,top,bot,W=1024,H=2048,seed=17,clouds=7,cloud=(250,244,236)):
    y=np.linspace(0,1,H)[:,None,None]; a=np.array(top,np.float32)*(1-y**0.8)+np.array(bot,np.float32)*(y**0.8); a=np.repeat(a,W,1)
    im=Image.fromarray(a.astype(np.uint8)).convert('RGBA'); r=random.Random(seed)
    for k in range(clouds):
        cx,cy=r.uniform(0,W),r.uniform(H*0.12,H*0.55); s=r.uniform(50,120)
        blob=Image.new('RGBA',(W,H),(0,0,0,0)); bd=ImageDraw.Draw(blob)
        for q in range(9):
            ox,oy=r.uniform(-2.2,2.2)*s,r.uniform(-0.5,0.3)*s; rr=s*r.uniform(0.5,0.9)
            bd.ellipse([cx+ox-rr,cy+oy-rr,cx+ox+rr,cy+oy+rr*0.8],fill=cloud+(255,))
        im=Image.alpha_composite(im,blob)
        e=blob.filter(ImageFilter.FIND_EDGES); im=Image.alpha_composite(im,Image.fromarray((np.asarray(e)*np.array([0,0,0,0.5])).astype(np.uint8)))
    im.convert('RGB').save(T+name+'.png')
def skyline(name,era=1950,W=4096,H=1400,seed=19,night=False):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); r=random.Random(seed)
    far=(150,160,176) if not night else (60,64,110); near=(120,128,146) if not night else (44,46,90)
    x=0
    while x<W:
        w=r.uniform(120,300); h=r.uniform(300,800); c=mul(far,r.uniform(0.92,1.08))
        d.rectangle([x,H-h,x+w,H],fill=c); jr(d,x,H-h,x+w,H,3,mul(far,0.6),int(x))
        for yy in range(int(H-h+30),H-20,46):
            for xx in range(int(x+18),int(x+w-18),34): d.rectangle([xx,yy,xx+16,yy+24],fill=(250,224,150) if (night and r.random()<0.5) else mul(c,0.8))
        x+=w+r.uniform(-20,30)
    # City Hall tower silhouette (tower + clock + statue) in the middle
    cx=W*0.52; c=near
    d.rectangle([cx-180,H-560,cx+180,H],fill=c); d.rectangle([cx-110,H-980,cx+110,H-560],fill=c)
    d.polygon([(cx-110,H-980),(cx+110,H-980),(cx+70,H-1160),(cx-70,H-1160)],fill=c); d.rectangle([cx-50,H-1250,cx+50,H-1160],fill=c)
    d.ellipse([cx-30,H-1330,cx+30,H-1250],fill=c); d.ellipse([cx-60,H-900,cx+60,H-780],fill=(240,230,200)); d.ellipse([cx-60,H-900,cx+60,H-780],outline=mul(c,0.5),width=6)
    d.line([cx,H-840,cx,H-880],fill=INK,width=6); d.line([cx,H-840,cx+30,H-840],fill=INK,width=6)
    jr(d,cx-110,H-980,cx+110,H-560,4,mul(c,0.55),3); jr(d,cx-180,H-560,cx+180,H,4,mul(c,0.55),4)
    im.save(T+name+'.png')
def chalkboard(name,state):  # state 0 roster, 1 cancelled, 2..5 BLACK FRIDAY writing progress
    W,H=1536,1024; im=wash(W,H,(46,62,54),0.10,60); d=ImageDraw.Draw(im)
    for _ in range(300): x,y=random.uniform(0,W),random.uniform(0,H); d.line([x,y,x+random.uniform(20,90),y+random.uniform(-6,6)],fill=(70,86,78),width=3)
    ch=(232,232,220); f=font(FSN,60); f2=font(FSN,44)
    text(d,(W/2,90),'DUTY ROSTER - FRI. NOV. 24',f,ch)
    names=['SGT. KELLY','OFC. RUIZ','OFC. BROWN','OFC. MOSS','OFC. DUNN','OFC. LEE']
    for i,n in enumerate(names):
        y=200+i*80; text(d,(300,y),n,f2,ch,'lm'); text(d,(760,y),'DAY OFF',f2,ch,'lm')
        if state>=1: d.line([750,y,980,y],fill=(250,120,110),width=6); text(d,(1030,y),'12 HR',f2,(250,200,120),'lm')
    if state>=1: 
        st=Image.new('RGBA',(700,200),(0,0,0,0)); sd=ImageDraw.Draw(st); sd.rectangle([6,6,694,194],outline=(220,60,50),width=12); text(sd,(350,100),'CANCELLED',font(FS,86),(220,60,50))
        st=st.rotate(10,expand=True,resample=Image.BICUBIC); stamp=st
    if state>=2:
        d.rectangle([60,620,W-60,H-60],fill=(46,62,54)); s='BLACK FRIDAY'; n=min(len(s),int(len(s)*(state-1)/4)); 
        fb=font(FS,150); x0=W/2-d.textlength(s,font=fb)/2   # letters appear left to right where the chalk is
        if n>0: text(d,(x0,880),s[:n],fb,(250,250,240),'lm',0)
    if state>=1: im.paste(stamp,(720,250),stamp)   # stamp stays on the roster through the chalk writing
    d.rectangle([0,0,W,H],outline=(120,86,54),width=40); im.save(T+name+'.png')
def banner(name,txt='BIG FRIDAY!',sub='NOV. 24 - 1961 - SHOP DOWNTOWN',W=2048,H=512):
    im=Image.new('RGB',(W,H),(250,236,90)); d=ImageDraw.Draw(im)
    for x in range(0,W,64): d.rectangle([x,0,x+32,H],fill=(246,224,70))
    d.rectangle([20,20,W-20,H-20],outline=(200,40,40),width=18)
    text(d,(W/2,H*0.42),txt,font(FS,210),(200,40,40),stroke=6,sf=(255,255,255)); text(d,(W/2,H*0.82),sub,font(FSN,60),(40,40,90))
    for k in range(10): x=random.uniform(80,W-80); y=random.uniform(30,H-30); d.polygon([(x,y-26),(x+8,y-8),(x+28,y-8),(x+12,y+4),(x+18,y+24),(x,y+12),(x-18,y+24),(x-12,y+4),(x-28,y-8),(x-8,y-8)],fill=(240,120,40))
    im.save(T+name+'.png')
FRI={1962:23,1966:25,1968:29,1969:28,1970:27,1971:26,1981:27}
def newspaper(name,head,sub,year,size=1.0,W=1024,H=1400,seed=70):
    im=wash(W,H,(238,232,214),0.04,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    text(d,(W/2,70),'THE PHILADELPHIA DAILY' if 'TOWN' not in sub else sub.split('|')[1],font(FS,56),INK)
    d.line([40,110,W-40,110],fill=INK,width=4); text(d,(W/2,135),f'FRIDAY, NOVEMBER {FRI[year]}, {year}     5 CENTS',font(FSN,24),INK); d.line([40,158,W-40,158],fill=INK,width=2)
    fs=int(130*size); fh=font(FS,fs)
    while d.textlength(head,font=fh)>W-60: fs-=6; fh=font(FS,fs)
    text(d,(W/2,170+fs*0.6),head,fh,INK)
    y=200+fs*1.2; text(d,(W/2,y),sub.split('|')[0],font(FS,40),(60,50,46))
    y+=50; d.rectangle([60,y,W/2-20,y+380],fill=(170,164,150)); jr(d,60,y,W/2-20,y+380,3)
    # photo: crowd silhouettes
    for k in range(12): cx=80+k*36; d.ellipse([cx,y+200,cx+30,y+230],fill=(90,86,80)); d.rectangle([cx,y+230,cx+30,y+380],fill=(90,86,80))
    for col in range(2):
        x0=W/2+20 if col==0 else 60; ys=y if col==0 else y+400
        for k in range(26 if col==0 else 14): d.line([x0,ys+k*16,x0+(W/2-80)*r.uniform(0.8,1),ys+k*16],fill=(120,114,104),width=6)
    im.save(T+name+'.png')
def ledger(name,state,W=1536,H=1024,seed=80):  # state 0: red entries only; 1..4: black total being written; 
    im=wash(W,H,(240,234,214),0.04,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for y in range(80,H,40): d.line([0,y,W,y],fill=(170,200,220),width=2)
    for x in (120,W/2-40,W/2,W-260): d.line([x,0,x,H],fill=(220,140,140),width=3)
    d.line([W/2-4,0,W/2-4,H],fill=(160,150,130),width=10)  # spine
    text(d,(W*0.25,40),'NOVEMBER',font(FS,40),(60,50,46)); text(d,(W*0.75,40),'FRIDAY',font(FS,40),(60,50,46))
    hand=font(FS,30)
    for k in range(18):
        y=100+k*40
        d.text((140,y),r.choice(['rent','wages','stock','coal','lights','window','ads','tax','freight']),font=hand,fill=(50,46,60))
        d.text((W/2-200,y),f'({r.randint(12,980)}.{r.randint(10,99)})',font=hand,fill=(196,30,30))
    for k in range(int(state*4.5)):
        y=100+k*40; d.text((W/2+40,y),r.choice(['sales','gifts','toys','coats','hats']),font=hand,fill=(50,46,60)); d.text((W-240,y),f'{r.randint(200,4000)}.{r.randint(10,99)}',font=hand,fill=(20,20,26))
    if state>=4:
        d.line([W/2+40,H-120,W-60,H-120],fill=(20,20,26),width=5); d.text((W/2+60,H-100),'TOTAL',font=font(FS,44),fill=(20,20,26)); d.text((W-330,H-100),'+ 18,240.00',font=font(FS,44),fill=(20,20,26))
    d.line([140,H-120,W/2-60,H-120],fill=(196,30,30),width=5); d.text((150,H-100),'TOTAL',font=font(FS,44),fill=(196,30,30)); d.text((W/2-330,H-100),'(9,410.00)',font=font(FS,44),fill=(196,30,30))
    im.save(T+name+'.png')
def wallpaper(name,base,motif,W=1024,H=1024,seed=90):
    im=wash(W,H,base,0.05,seed); d=ImageDraw.Draw(im)
    for j in range(0,H,128):
        for i in range(0,W,128):
            x=i+(64 if (j//128)%2 else 0); y=j
            d.ellipse([x+40,y+40,x+88,y+88],outline=motif,width=4); d.line([x+64,y+20,x+64,y+108],fill=motif,width=3); d.line([x+20,y+64,x+108,y+64],fill=motif,width=3)
    d.rectangle([0,H-260,W,H],fill=mul(base,0.6));
    for x in range(0,W,128): jr(d,x+10,H-240,x+118,H-30,3,mul(base,0.4),x)
    d.rectangle([0,H-280,W,H-260],fill=mul(base,0.45)); strokes(im,500,mul(base,0.8),seed,6,22,2,40).save(T+name+'.png')
def woodfloor(name='wood',W=1024,H=1024,seed=95,base=(150,100,62)):
    im=wash(W,H,base,0.06,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for j in range(0,W,64):
        c=mul(base,r.uniform(0.85,1.12)); d.rectangle([j,0,j+62,H],fill=c); jl(d,[(j,0),(j,H)],3,mul(base,0.5),j)
        y=r.uniform(0,H); jl(d,[(j,y),(j+62,y)],3,mul(base,0.5),j+1)
        for k in range(4): yy=r.uniform(0,H); d.arc([j+10,yy,j+50,yy+80],200,340,fill=mul(base,0.7),width=2)
    im.save(T+name+'.png')
def newsstand_sign(name,town):
    W,H=1024,256; im=Image.new('RGB',(W,H),(40,70,120)); d=ImageDraw.Draw(im); d.rectangle([10,10,W-10,H-10],outline=(240,220,150),width=10)
    sz=96
    while d.textlength(town+' NEWS',font=font(FS,sz))>W-120: sz-=4
    text(d,(W/2,H/2),town+' NEWS',font(FS,sz),(250,236,180),stroke=3); im.save(T+name+'.png')
def poster_frame_display(name):  # store window back wall 1981 with gift boxes painted (poster added as 3D frame)
    wallpaper(name,(120,40,46),(160,70,72),seed=97)
if __name__=='__main__':
    walls=[(160,70,56),(140,62,52),(176,96,70),(120,60,54),(168,84,62),(150,92,80),(130,74,60),(182,110,84)]
    for i in range(8): facade(f'fac{i}',walls[i],SHOPS[i],100+i)
    for i in range(4): facade(f'fac81_{i}',walls[i+2],SHOPS[(i+3)%8],200+i,era=1981,xmas=True)
    dept_store('dept50',1950); dept_store('dept81',1981,seed=41)
    asphalt(); sidewalk()
    sky('sky_day',(96,146,200),(240,218,180)); sky('sky_dawn',(80,90,170),(252,196,150),seed=21,cloud=(252,214,196)); sky('sky_grey',(120,140,170),(226,214,196),seed=23,clouds=10)
    skyline('skyline50'); skyline('skyline_dawn',night=True)
    for s in range(6): chalkboard(f'board{s}',s)
    banner('banner')
    newspaper('paper62','BLACK FRIDAY','Shoppers jam Center City',1962,0.7,seed=71)
    newspaper('paper66','BLACK FRIDAY!','Worst traffic yet, police say',1966,1.0,seed=72)
    newspaper('paper70','BLACK FRIDAY!!','Crowds break all records',1970,1.4,seed=73)
    for i,t in enumerate(['PITTSBURGH','BALTIMORE','TRENTON','BOSTON']): newspaper(f'town{i}','BLACK FRIDAY',f'Crowds downtown|THE {t} TIMES',1968+i,1.0,seed=74+i); newsstand_sign(f'stand{i}',t)
    newspaper('paper81','RED TO BLACK!','Why stores call it Black Friday',1981,1.0,seed=79)
    for s in range(5): ledger(f'ledger{s}',s)
    wallpaper('precinct',(110,140,120),(90,116,100),seed=91); wallpaper('office',(176,150,110),(150,120,84),seed=92); wallpaper('office81',(150,120,96),(196,160,110),seed=93)
    woodfloor(); woodfloor('lino',base=(120,128,120),seed=96); poster_frame_display('window81')
    print('PAINT_OK')
