# Flat 2D cut-out cast, Rick construction: round cream head, monoline dark outline (~2.3 % of head width), drawn face,
# bean/stick body with one costume cue, flat colour blocks + soft gradient + fabric lines. Our own designs.
from PIL import Image, ImageDraw, ImageFilter
import json, math
T='/root/bf/tex/'; K=(30,22,20,255); SK=(252,246,236,255); OUT=19   # 19 px on an 800 px disc = 2.4 %
def new(w,h): im=Image.new('RGBA',(w,h),(0,0,0,0)); return im,ImageDraw.Draw(im)
def dk(c,f=0.75): return tuple(int(v*f) for v in c[:3])+(255,)
CX,CY=512,540
def eyes(d,kind,cy=520,gap=125,glasses=None):
    for sx in(-1,1):
        x=CX+sx*gap
        if kind=='dot': d.ellipse([x-24,cy-32,x+24,cy+32],fill=K)
        elif kind=='wide': d.ellipse([x-56,cy-56,x+56,cy+56],fill=(255,255,255,255),outline=K,width=13); d.ellipse([x-20,cy-20,x+20,cy+20],fill=K)
        elif kind=='tiny': d.ellipse([x-14,cy-14,x+14,cy+14],fill=K)
        elif kind=='up': d.ellipse([x-24,cy-44,x+24,cy+22],fill=K)
        elif kind=='side': d.ellipse([x-6,cy-30,x+42,cy+30],fill=K)
        elif kind=='squeeze': d.line([x-40*sx,cy-30,x+34*sx,cy],fill=K,width=19); d.line([x+34*sx,cy,x-40*sx,cy+30],fill=K,width=19)
        elif kind=='half': d.chord([x-38,cy-38,x+38,cy+38],0,180,fill=K); d.line([x-48,cy,x+48,cy],fill=K,width=16)
        elif kind=='happy': d.arc([x-48,cy-24,x+48,cy+54],200,340,fill=K,width=18)
        elif kind=='closed': d.line([x-44,cy+4,x+44,cy+4],fill=K,width=17)
        elif kind=='swirl':
            for rr in (44,28,12): d.arc([x-rr,cy-rr,x+rr,cy+rr],0,300,fill=K,width=8)
        elif kind=='wink':
            if sx<0: d.arc([x-44,cy-20,x+44,cy+30],200,340,fill=K,width=17)
            else: d.ellipse([x-24,cy-32,x+24,cy+32],fill=K)
        if glasses: d.ellipse([x-74,cy-66,x+74,cy+66],outline=glasses,width=12)
    if glasses: d.line([CX-51,cy-6,CX+51,cy-6],fill=glasses,width=11)
def brows(d,kind,cy=405,gap=125):
    for sx in(-1,1):
        x=CX+sx*gap
        if kind=='flat': d.line([x-52,cy,x+52,cy],fill=K,width=20)
        elif kind=='angry': d.line([x-52*sx,cy-24,x+52*sx,cy+20],fill=K,width=22)
        elif kind=='up': d.line([x-52,cy-36,x+52,cy-36],fill=K,width=19)
        elif kind=='worry': d.line([x-52*sx,cy+16,x+52*sx,cy-26],fill=K,width=20)
        elif kind=='raise': yy=cy-(46 if sx>0 else 0); d.line([x-52,yy,x+52,yy-(8 if sx>0 else 0)],fill=K,width=20)
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
    if 'blush' in kind:
        for x in(330,694): d.ellipse([x-60,612,x+60,662],fill=(240,120,130,150))
    if 'puff' in kind:
        for x in(300,724): d.ellipse([x-80,600,x+80,740],fill=(250,180,170,170))
    if 'tear' in kind: d.ellipse([370,580,410,640],fill=(120,190,255,255),outline=K,width=6)
    if 'angryfill' in kind: pass
C=json.load(open('/root/bf/src/cast.json'))
def head(name,fk):
    c=C[name]; e,b,m=c['faces'][fk][:3]; ex=c['faces'][fk][3] if len(c['faces'][fk])>3 else ''
    im,d=new(1024,1024); hair=tuple(c.get('hair',(60,40,30)))+(255,)
    hs=c.get('hairstyle','short')
    if hs=='bun': d.ellipse([382,40,642,280],fill=hair,outline=K,width=OUT)
    if hs=='long': d.rounded_rectangle([100,260,924,980],200,fill=hair,outline=K,width=OUT)
    if hs=='mullet': d.rounded_rectangle([170,320,854,1010],140,fill=hair,outline=K,width=OUT)   # back hair, crown to shoulders
    if hs=='perm':
        for a in range(0,360,30): x=CX+380*math.cos(math.radians(a)); y=500+360*math.sin(math.radians(a))*0.95; d.ellipse([x-120,y-120,x+120,y+120],fill=hair,outline=K,width=OUT)
    skin=tuple(c.get('skin',SK[:3]))+(255,)
    d.ellipse([112,140,912,940],fill=skin,outline=K,width=OUT)
    if 'angryfill' in ex: 
        ov=Image.new('RGBA',(1024,1024),(0,0,0,0)); od=ImageDraw.Draw(ov); od.ellipse([130,158,894,922],fill=(170,60,170,120)); im.alpha_composite(ov); d=ImageDraw.Draw(im)
    if hs in('short','bald','bun','mullet'):
        if hs=='short': d.chord([150,150,874,560],180,360,fill=hair,outline=K,width=OUT)
        if hs=='bun': d.chord([150,150,874,520],180,360,fill=hair,outline=K,width=OUT)
        if hs=='bald':
            for sx in(-1,1): d.chord([CX+sx*390-100,400,CX+sx*390+100,680],90 if sx>0 else 270,270 if sx>0 else 450,fill=hair)
        if hs=='mullet': d.chord([150,150,874,540],180,360,fill=hair,outline=K,width=OUT)
    hat=c.get('hat')
    if hat=='cop':
        d.chord([140,90,884,470],180,360,fill=(28,36,70,255),outline=K,width=OUT); d.rectangle([150,280,874,360],fill=(28,36,70,255),outline=K,width=OUT)
        d.chord([180,320,844,470],0,180,fill=(20,20,26,255),outline=K,width=OUT)   # peak
        d.polygon([(CX,170),(CX+44,220),(CX+30,290),(CX-30,290),(CX-44,220)],fill=(214,180,80,255),outline=K)  # plain shield, no text
    if hat=='flatcap': d.chord([150,140,874,520],180,360,fill=(90,90,96,255),outline=K,width=OUT); d.chord([200,330,760,470],0,180,fill=(70,70,76,255),outline=K,width=OUT)
    if hat=='ladyhat': d.ellipse([60,250,964,380],fill=(150,40,60,255),outline=K,width=OUT); d.chord([230,90,794,420],180,360,fill=(150,40,60,255),outline=K,width=OUT); d.ellipse([680,150,780,250],fill=(240,200,80,255),outline=K,width=10)
    if hat=='beanie': d.chord([140,110,884,520],180,360,fill=tuple(c['scarf'])+(255,),outline=K,width=OUT); d.ellipse([462,60,562,160],fill=(250,250,250,255),outline=K,width=12)
    if hat=='fedora': d.ellipse([90,300,934,400],fill=(80,60,44,255),outline=K,width=OUT); d.rounded_rectangle([250,90,774,350],60,fill=(80,60,44,255),outline=K,width=OUT); d.rectangle([250,280,774,330],fill=(40,30,24,255))
    eyes(d,e,glasses=(tuple(c['glasses'])+(255,)) if c.get('glasses') else None); brows(d,b if hat not in('cop','flatcap','fedora','beanie','ladyhat') or b!='up' else 'flat'); mouth(d,m)
    if c.get('mustache'): d.chord([CX-120,640,CX+120,720],180,360,fill=tuple(c['mustache'])+(255,),outline=K,width=10)
    if c.get('nose',True): d.arc([CX-30,560,CX+30,640],-30,200,fill=K,width=10)
    extras(d,ex)
    return im
def body(name,stride=0):
    # stride 0 = standing; 1/2 = walk poses (legs spread, one foot lifted, alternating) for rule 162
    c=C[name]; im,d=new(800,1100); R=tuple(c['coat'])+(255,); kind=c.get('body','tall')
    legc=tuple(c.get('legs',(40,36,40)))+(255,)
    for sx in(-1,1):
        x=400+sx*92; fx=x+(sx*70 if stride else 0); lift=(70 if (stride==1 and sx<0) or (stride==2 and sx>0) else 0)
        fy=1012-lift
        d.line([x,760,fx,fy],fill=legc,width=34); d.line([x,760,fx,fy],fill=K,width=6)
        d.ellipse([fx-78+sx*28,fy-26,fx+62+sx*28,fy+48],fill=(36,28,24,255),outline=K,width=13)
    if kind=='tall': pts=[(250,50),(550,50),(640,820),(160,820)]
    elif kind=='short': pts=[(220,140),(580,140),(640,800),(160,800)]
    else: pts=None
    if pts: d.polygon(pts,fill=R)
    else: d.ellipse([130,70,670,860],fill=R)
    # soft gradient (light from the right) + fabric lines
    ov=Image.new('RGBA',im.size,(0,0,0,0)); od=ImageDraw.Draw(ov)
    for i in range(40): od.rectangle([i*20,0,i*20+20,1100],fill=(20,10,30,int(max(0,70-i*3.2))))
    a=im.split()[3]; im=Image.alpha_composite(im,Image.composite(ov,Image.new('RGBA',im.size,(0,0,0,0)),a)); d=ImageDraw.Draw(im)
    for k in range(6): d.line([300+k*40,120,280+k*44,800],fill=dk(R,0.86),width=4)
    if pts: d.line(pts+[pts[0]],fill=K,width=OUT,joint='curve')
    else: d.ellipse([130,70,670,860],outline=K,width=OUT)
    cue=c.get('cue')
    if cue=='cop':
        for i in range(4): d.ellipse([385,170+i*140,415,200+i*140],fill=(220,186,80,255),outline=K,width=6)
        d.rectangle([180,600,620,650],fill=(30,26,24,255),outline=K,width=8); d.rectangle([370,596,430,654],fill=(214,180,80,255),outline=K,width=6)
        d.polygon([(300,230),(340,200),(360,250),(330,280)],fill=(214,180,80,255),outline=K)  # plain star-less badge
    if cue=='bowtie': d.polygon([(330,70),(400,105),(470,70),(470,150),(400,115),(330,150)],fill=(170,30,40,255),outline=K); d.line([400,150,400,800],fill=dk(R,0.6),width=10)
    if cue=='blazer':
        d.polygon([(250,50),(400,320),(550,50)],fill=(250,250,245,255),outline=K); d.line([400,320,400,820],fill=K,width=10)
        for sx in(-1,1): d.ellipse([400+sx*280-90,30,400+sx*280+90,150],fill=R,outline=K,width=OUT)  # shoulder pads
    if cue=='stripes':
        for y in range(120,800,70): d.line([200,y,600,y],fill=(240,240,240,255),width=26)
        d.polygon(pts,outline=K,width=OUT) if pts else None
    if cue=='scarf': d.rounded_rectangle([230,40,570,130],30,fill=tuple(c['scarf'])+(255,),outline=K,width=12); d.rectangle([460,110,530,380],fill=tuple(c['scarf'])+(255,),outline=K,width=10)
    if cue=='apron': d.polygon([(290,260),(510,260),(550,790),(250,790)],fill=(246,240,228,255),outline=K)
    if cue=='camera': d.line([300,60,500,300],fill=K,width=8)
    if cue=='pearls':
        for k in range(9): d.ellipse([290+k*26,90+abs(k-4)*8,312+k*26,112+abs(k-4)*8],fill=(250,250,240,255),outline=K,width=4)
    if cue=='vest': d.polygon([(300,100),(400,300),(500,100),(520,780),(280,780)],fill=dk(R,0.7),outline=K)
    return im
def arm(name,prop=None):
    c=C[name]; im,d=new(400,900); R=tuple(c['coat'])+(255,); skin=tuple(c.get('skin',SK[:3]))+(255,)
    d.rounded_rectangle([150,20,250,330],48,fill=R,outline=K,width=OUT); d.line([200,300,200,690],fill=K,width=30)
    d.ellipse([148,672,252,776],fill=skin,outline=K,width=15)
    if prop=='whistle': pass
    if prop=='bag': d.rectangle([90,760,310,890],fill=(200,170,120,255),outline=K,width=13); d.arc([140,700,260,820],180,360,fill=K,width=10); d.rectangle([150,790,250,830],fill=(200,40,40,255))
    if prop=='box': d.rectangle([100,740,300,880],fill=(60,120,180,255),outline=K,width=13); d.line([200,740,200,880],fill=(250,230,120,255),width=16); d.line([100,810,300,810],fill=(250,230,120,255),width=16)
    if prop=='chalk': d.rectangle([186,740,214,800],fill=(250,250,250,255),outline=K,width=6)
    if prop=='pen': d.line([200,720,200,880],fill=(20,20,24,255),width=16); d.polygon([(192,880),(208,880),(200,900)],fill=K)
    if prop=='redpen': d.line([200,720,200,880],fill=(196,30,30,255),width=16); d.polygon([(192,880),(208,880),(200,900)],fill=K)
    if prop=='megaphone': d.polygon([(180,720),(220,720),(330,890),(70,890)],fill=(236,230,220,255),outline=K); d.ellipse([70,860,330,900],fill=(60,60,64,255),outline=K,width=8)
    if prop=='pennant': d.line([200,600,200,120],fill=(120,80,40,255),width=12); d.polygon([(200,120),(390,180),(200,250)],fill=tuple(c.get('scarf',(40,60,140)))+(255,),outline=K)
    if prop=='camera': d.rounded_rectangle([110,720,290,840],20,fill=(40,40,44,255),outline=K,width=12); d.ellipse([160,740,240,820],fill=(120,140,170,255),outline=K,width=8)
    if prop=='paper': d.rectangle([60,640,340,860],fill=(238,232,214,255),outline=K,width=10); d.text((80,660),'BLACK\nFRIDAY',fill=K)
    return im
if __name__=='__main__':
    out={}
    for n,c in C.items():
        for fk in c['faces']: head(n,fk).save(f'{T}{n}_h_{fk}.png')
        body(n).save(f'{T}{n}_body.png'); body(n,1).save(f'{T}{n}_bodyw1.png'); body(n,2).save(f'{T}{n}_bodyw2.png')
        for p in c.get('props',[None]): arm(n,p).save(f'{T}{n}_arm{"_"+p if p else ""}.png')
        arm(n).save(f'{T}{n}_arm.png')
    # preview
    pv=Image.new('RGBA',(300*len(C),700),(236,230,218,255))
    for i,n in enumerate(C):
        b=Image.open(f'{T}{n}_body.png').resize((240,330)); h=Image.open(f'{T}{n}_h_{list(C[n]["faces"])[0]}.png').resize((260,260))
        pv.alpha_composite(b,(i*300+30,330)); pv.alpha_composite(h,(i*300+20,110))
    pv.convert('RGB').save('/root/bf/cast_preview.jpg')
    faces=[]
    for n,c in C.items():
        for fk in c['faces']: faces.append(Image.open(f'{T}{n}_h_{fk}.png').resize((128,128)))
    sh=Image.new('RGBA',(128*16,128*((len(faces)+15)//16)),(236,230,218,255))
    for i,f in enumerate(faces): sh.alpha_composite(f,((i%16)*128,(i//16)*128))
    sh.convert('RGB').save('/root/bf/faces_sheet.jpg'); print('CAST_OK',len(faces),'faces')
