# Flat 2D cut-out cast, Rick construction: round cream head, monoline dark outline (~2.3 % of head width), drawn face,
# bean/stick body with one costume cue, flat colour blocks + soft gradient + fabric lines. Our own designs.
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import json, math
import expressions as X   # Rick-style expression library (opt-in per character via cast.json "library")
T='/root/cc/tex/'; K=(50,28,42,255); SK=(251,244,241,255); OUT=23   # r8 (owner Nov 20: clone Rick's characters): pure white heads like Rick's. r8b (guide v1.3 x.3): dark plum ink, never pure black; 27 px on an 800 px disc = 3.4 % lit side
def new(w,h): im=Image.new('RGBA',(w,h),(0,0,0,0)); return im,ImageDraw.Draw(im)
def dk(c,f=0.75): return tuple(int(v*f) for v in c[:3])+(255,)
CX,CY=512,540
def eyes(d,kind,cy=520,gap=108,glasses=None):   # r8b: centres 27 % of head width apart (216 px of 800)
    if kind in X.EYES:
        X.eyes(d,kind,K,cy,gap); kind='_lib'
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
    if kind in X.BROWS: return X.brows(d,kind,K,cy,gap)
    for sx in(-1,1):
        x=CX+sx*gap
        if kind=='flat': d.line([x-52,cy,x+52,cy],fill=K,width=30)
        elif kind=='angry': d.line([x-52*sx,cy-24,x+52*sx,cy+20],fill=K,width=32)
        elif kind=='up': d.line([x-52,cy-36,x+52,cy-36],fill=K,width=30)
        elif kind=='worry': d.line([x-52*sx,cy+16,x+52*sx,cy-26],fill=K,width=30)
        elif kind=='raise': yy=cy-(46 if sx>0 else 0); d.line([x-52,yy,x+52,yy-(8 if sx>0 else 0)],fill=K,width=30)
        elif kind=='none': pass
def mouth(d,kind,cy=715,cx=CX):
    if kind in X.MOUTHS: return X.mouth(d,kind,K,cy,cx)
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
    X.extras(d,kind,K)   # library extras: tears, tear1, blushR, vein, zzz, shades, sweat2
C=X.expand(json.load(open('/root/cc/src/cast.json')))
def head(name,fk):
    c=C[name]; e,b,m=c['faces'][fk][:3]; ex=c['faces'][fk][3] if len(c['faces'][fk])>3 else ''
    im,d=new(1024,1024); hair=tuple(c.get('hair',(60,40,30)))+(255,)
    hs=c.get('hairstyle','short')
    HD=c.get('hairdo'); TD=X.turn_dx(c,ex); PT,PB=X.pads(c)   # library round 3: PT/PB = extra texture rows for tall hats, hair and beards
    #   # library round 2: Rick hairstyles; TD = face slide toward the turned side
    if HD: hs='_hairdo'; X.hairdo_back(d,HD,hair,K)
    if hs=='bun': d.ellipse([382,40,642,280],fill=hair,outline=K,width=OUT)
    if hs=='long': d.rounded_rectangle([100,260,924,980],200,fill=hair,outline=K,width=OUT)
    if hs=='mullet': d.rounded_rectangle([170,320,854,1010],140,fill=hair,outline=K,width=OUT)   # back hair, crown to shoulders
    if hs=='tied': d.rounded_rectangle([150,250,874,1000],180,fill=hair,outline=K,width=OUT)   # cc: long hair falling behind the shoulders
    if hs=='white': d.rounded_rectangle([130,300,894,860],200,fill=hair,outline=K,width=OUT)   # cc: old man's white hair at the sides
    if hs=='perm':
        for a in range(0,360,30): x=CX+380*math.cos(math.radians(a)); y=500+360*math.sin(math.radians(a))*0.95; d.ellipse([x-120,y-120,x+120,y+120],fill=hair,outline=K,width=OUT)
    skin=tuple(X.skin_rgb(c.get('skin'),SK[:3]))+(255,)   # library round 4: 'skin' may name a Rick skin preset (X.SKIN)
    # r8b (guide v1.3 x.3): ink 3.4 % of head width toward the light (upper right), 6 % away from it and under the chin
    d.ellipse([112,140,912,940],fill=K); d.ellipse([112+48,140+27,912-27,940-48],fill=skin)
    head_shade(im,skin); d=ImageDraw.Draw(im)
    # r9 (RENDER_SPEC_v1.4 A: eyes centred ~69 % up the head): hair and hats are drawn on their own layer and squashed to the top 40 % of the
    # head (x0.6 from the top), the face features on a layer moved up 105 px (eyes at 65.6 % up)
    if 'angryfill' in ex: 
        ov=Image.new('RGBA',(1024,1024),(0,0,0,0)); od=ImageDraw.Draw(ov); od.ellipse([130,158,894,922],fill=(170,60,170,120)); im.alpha_composite(ov); d=ImageDraw.Draw(im)
    if 'gloom' in ex or 'redglow' in ex: X.pre(im,ex); d=ImageDraw.Draw(im)   # library: rage gloom on the head top
    PRE=im.copy() if c.get('hat3d') else None   # library round 3: head before any front hair, to undo hair under a hat
    if hs in('short','bald','bun','mullet','tied','white'):   # r9: hairlines raised with the features (hair ends ~285, brows at 300)
        if hs=='short': d.chord([150,150,874,420],180,360,fill=hair,outline=K,width=OUT)
        if hs=='bun': d.chord([150,150,874,410],180,360,fill=hair,outline=K,width=OUT)
        if hs=='bald':
            for sx in(-1,1): d.chord([CX+sx*390-100,300,CX+sx*390+100,580],90 if sx>0 else 270,270 if sx>0 else 450,fill=hair)
        if hs=='mullet': d.chord([150,150,874,420],180,360,fill=hair,outline=K,width=OUT)
        if hs=='tied': d.chord([150,150,874,420],180,360,fill=hair,outline=K,width=OUT)
        if hs=='white': d.chord([200,160,824,380],180,360,fill=hair,outline=K,width=OUT)
    if HD: X.hairdo(d,HD,hair,K,dx=TD//3)
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
    top=im.resize((1024,int(1024*0.6)),Image.LANCZOS); im=base
    if c.get('hat_tilt') or TD:   # library round 2: hats sit tilted and slide a little with the turn (Rick #24 trucker, #03 bowler)
        tl=Image.new('RGBA',(1024,1024),(0,0,0,0)); tl.alpha_composite(top,(0,0)); top=tl.rotate(-c.get('hat_tilt',0),resample=Image.BICUBIC,center=(CX,180),translate=(TD//2,0))
    im.alpha_composite(top,(0,0)); top=None
    HAT=None
    if c.get('hat3d'):   # library round 3: Rick-proportioned hat on a padded layer, composited last; hair above its brim removed
        HAT,_by=X.hat3d_layer(c['hat3d'],c.get('hatcol',(80,60,44)),K,tilt=c.get('hat_tilt',0),dx=TD//2,col2=c.get('hatcol2'),top=PT,bottom=PB)
        HREG=X.hat_region(HAT); X.restore_under_hat(im,PRE,HREG.crop((0,PT,1024,PT+1024)))
    if c.get('fhair'): X.fhair(im,c['fhair'],c.get('fhaircol',c.get('hair',(60,40,30))),K,dx=TD)   # library round 2: Rick facial hair (326a revision pending owner pick)
    feat,d=new(1024,1024)
    FS=X.feat_scale(c)   # library round 4 (owner OK 00:20Z Nov 23): Rick-sized eyes / brows / mouth
    _gl=(tuple(c['glasses'])+(255,)) if c.get('glasses') else None; _bk=b if hat not in('cop','flatcap','fedora','beanie','ladyhat','capotain','tricorn','knit','cap','sunhat') or b!='up' else 'flat'
    if FS:
        X.scaled(feat,lambda dd: eyes(dd,e,glasses=_gl),X.EYE_BOXES,FS[0]); X.scaled(feat,lambda dd: brows(dd,_bk),X.BROW_BOXES,FS[1]); d=ImageDraw.Draw(feat)
    else:
        eyes(d,e,glasses=_gl); brows(d,_bk)
    MSIDE=X.mouth_side(c,ex)   # library round 3: per-face mouthL/mouthR/lookL/lookR tokens override mouth_side
    if FS:
        _ml,_md=new(1024,1024); X.scaled(_ml,lambda dd: mouth(dd,m),X.MOUTH_BOXES,FS[2]); feat.alpha_composite(X.mouth_set(_ml,m,MSIDE)); d=ImageDraw.Draw(feat)
    elif MSIDE: feat.alpha_composite(X.mouth_layer(mouth,m,MSIDE)); d=ImageDraw.Draw(feat)   # library round 2: Rick's off-centre, lopsided mouths
    else: mouth(d,m)
    if c.get('mustache'):   # r8: Rick's bushy two-lobe mustache
        mc=tuple(c['mustache'])+(255,)
        for sx in(-1,1): d.ellipse([CX+sx*80-95,605,CX+sx*80+95,705],fill=mc,outline=K,width=12)
        d.ellipse([CX-70,610,CX+70,690],fill=mc)
    if c.get('stache_small'):   # 326a D2 (from Detroit r5): one slim rounded mustache, narrower than the mouth
        mc=tuple(c['stache_small'])+(255,); d.rounded_rectangle([CX-105,628,CX+105,672],22,fill=mc,outline=K,width=10)
    if c.get('stubble'):   # 326a D3: light jaw shadow, no outline
        ov=Image.new('RGBA',(1024,1024),(0,0,0,0)); od=ImageDraw.Draw(ov); od.chord([CX-330,520,CX+330,860],0,180,fill=tuple(c['stubble'])+(42,)); feat.alpha_composite(ov); d=ImageDraw.Draw(feat)
    if c.get('nose',True): d.arc([CX-30,560,CX+30,640],-30,200,fill=K,width=10)
    extras(d,ex)
    im.alpha_composite(feat.crop((0,105,1024,1024)),(TD,0))
    HL=X.hair_layer(HD,hair,K,dx=TD//2,top=PT) if HD else None
    FL=X.fhair_layer(c['fhair'],c.get('fhaircol',c.get('hair',(60,40,30))),K,dx=TD,top=PT,bottom=PB) if c.get('fhair') else None
    TILT=X.head_tilt(c,ex)
    if not (PT or PB or HL or HAT or TILT): return im
    # library round 3: final texture is 1024 x (PT+1024+PB); lib.char() sizes the face card to match (head stays in place)
    out=Image.new('RGBA',(1024,PT+1024+PB),(0,0,0,0)); out.alpha_composite(im,(0,PT))
    if FL is not None and PB: out.alpha_composite(FL.crop((0,PT+1024,1024,PT+1024+PB)),(0,PT+1024))
    if HL is not None:
        if HAT is not None: HL=X.erase_under_hat(HL,HREG,PT)
        out.alpha_composite(HL,(0,0))
    if HAT is not None: out.alpha_composite(HAT,(0,0))
    if TILT: out=out.rotate(TILT,resample=Image.BICUBIC,center=(512,PT+540))   # tiltL/tiltR tokens tip the whole head
    return out
# ---- round 3 (rule 193): Rick-style construction ----
# slim column garment (narrower than the head), long coat/robe to the shins, hard cel shadow on the left third,
# light rim on the right, ink detail (collar, placket, buttons, belt + buckle, hem band, fold lines),
# stick legs with small shoes; thin sleeves with a cuff and a small hand. Drawn at 2x and downsampled (clean edges).
SS=2; BOUT=17   # round 4: body outline as heavy as the head's (verifier: thin body outlines vs heads)
def lt(c,f=1.12): return tuple(min(255,int(v*f)) for v in c[:3])+(255,)
GB={'tall':(98,175,215),'short':(98,180,222),'round':(98,200,238)}   # r8b: one build for all (guide v1.3 x.3: torso 1.00 H, legs 1.25-1.3 H, total 3.2-3.35 H); kinds differ in width only   # top px, shoulder half-width, hem half-width
HEMY={'tall':545,'short':545,'round':545}   # r6det (rule 329, Rick f606/f771: torso ~1.05 H capsule): hem lower   # r8b: torso 430 px = 1.00 H (head 0.43 m), legs 528->1074 = 1.27 H   # r6 (round-5: legs 0.64-0.90 H, Rick 0.93-1.31): shorter torso, longer legs   # round 5 (B1/B2): torso ~0.86 H tall (H = head disc ~560 px), legs ~0.85 H visible
WK={'tall':0.775,'short':0.78,'round':0.69}   # bcn: rule 336 (DC 09eca41) torso width <= 0.85 H   # r6det (rule 329, Rick f606: torso ~0.85-0.9 H wide): was 0.72-0.745
def _sil(kind):
    y0,w0,w1=GB[kind]; y1=HEMY[kind]; pts=[]
    k_=WK[kind]; w0=int(w0*k_); w1=int(w1*k_)   # r9 (RENDER_SPEC_v1.4 A: torso width 0.73-0.89 H): widths x0.72-0.745
    w1=int(w0*0.90); rr=int(0.36*2*w1)   # bcn: rule 336a hem narrower than the middle (DC 09eca41)   # r6det (rule 329): Rick's bean is widest near the hem (pear), sides near-straight   # r6det (rule 329): near-straight sides like Rick's capsule torso (was hem x0.74 = egg)   # r6: hem narrower than the middle (Rick: widest at mid-torso)   # rounded bottom: corner radius >= 0.35 of the torso width (Rick bean)
    BG_=int(46*k_)   # rule 336a: widest row mid-torso   # r6det: small side bulge (was 62)
    R_=int(w0*0.85)   # r7det (rule 329, Rick f606: capsule top is fully rounded and sits behind the head, no square shoulders): was 70
    yb=y1-rr*0.55   # sides end here, then a half-ellipse closes the bottom
    for i in range(0,11): t=i/10; pts.append((400-(w1+(w0-w1)*t)-BG_*math.sin(math.pi*t), yb+(y0+R_-yb)*t))
    for i in range(0,13): a=math.radians(180+i*7.5); pts.append((400-w0+R_+R_*math.cos(a), y0+R_+R_*math.sin(a)))
    pts.append((400-w0+R_,y0)); pts.append((400+w0-R_,y0))
    for i in range(0,13): a=math.radians(270+i*7.5); pts.append((400+w0-R_+R_*math.cos(a), y0+R_+R_*math.sin(a)))
    for i in range(0,11): t=i/10; pts.append((400+(w0+(w1-w0)*t)+BG_*math.sin(math.pi*t), y0+R_+(yb-y0-R_)*t))
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
    LW=30   # rule 336a limb width (DC 09eca41)   # r6det (rule 329, Rick legs 6-7.5 % H filled tubes): ink tube 34 px with a trouser fill inside
    for sx in(-1,1):
        x=400+sx*62; fx=x+sx*20+(sx*60 if stride else 0); lift=(70 if (stride==1 and sx<0) or (stride==2 and sx>0) else 0); fy=1056-lift
        y_0=y1-60; cx_=(x+fx)/2+sx*30; cy_=(y_0+fy)/2
        P=[((1-t)**2*x+2*(1-t)*t*cx_+t*t*fx,(1-t)**2*y_0+2*(1-t)*t*cy_+t*t*fy) for t in [i/24 for i in range(25)]]
        d.line(_S(P),fill=K,width=s(LW),joint='curve')
        d.line(_S(P),fill=legc,width=s(LW-14),joint='curve')   # r6det: filled tube (trouser colour) inside the ink
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
    elif cue=='kit1899':   # bcn: 1899 football shirt: long sleeves, lace-up neck, no badge, no stripes, no number (no club kit)
        dd.polygon(_S([(400-70,y0-10),(400,y0+70),(400+70,y0-10)]),fill=dk(R,0.8)); dd.line(_S([(400-70,y0-10),(400,y0+70),(400+70,y0-10)]),fill=K,width=s(6))
        dd.line([s(400),s(y0+70),s(400),s(y0+190)],fill=K,width=s(6))
        for k in range(3): yy=y0+90+k*34; dd.line(_S([(384,yy),(416,yy+20)]),fill=(120,96,70,255),width=s(5)); dd.line(_S([(416,yy),(384,yy+20)]),fill=(120,96,70,255),width=s(5))
        dd.rectangle([0,s(y1-120),W,s(y1-96)],fill=dk(R,0.86))   # shirt tucked into the knickerbockers
        folds(3)
    elif cue=='vest':
        dd.polygon(_S([(400-100,y0),(400+100,y0),(400+80,y1),(400-80,y1)]),fill=(240,238,232,255))
        for sx in(-1,1): dd.polygon(_S([(400+sx*100,y0-10),(400+sx*20,y0+260),(400+sx*20,y1),(400+sx*260,y1),(400+sx*260,y0-10)]),fill=dk(R,0.8),outline=K,width=s(7))
        for y in range(y0+80,y1,70): dd.line([0,s(y),s(380),s(y)],fill=K,width=s(4)); dd.line([s(420),s(y),W,s(y)],fill=K,width=s(4))
        folds(3)
    # clip detail to the garment, paste
    clip=Image.new('RGBA',(W,H),(0,0,0,0)); clip.paste(det,(0,0),Image.composite(det.split()[3],Image.new('L',(W,H),0),gm))
    im.alpha_composite(clip); d=ImageDraw.Draw(im)
    if cue=='pilgrim':   # cc: plain white falling collar over the shoulders
        cw_=min(215,w0-45)   # r4 (castcheck shoulder join, Detroit b54a72c): the collar stays inside the torso outline so the arm grows out of the side
        d.chord([s(400-cw_),s(y0-70),s(400+cw_),s(y0+150)],0,180,fill=(248,246,238,255),outline=K,width=s(8)); d.line([s(400),s(y0+40),s(400),s(y0+148)],fill=K,width=s(6))
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
    def mitt(): d.ellipse([150,662,250,762],fill=K)   # r6det: mitten 100 px (was 84)
    mitt()
    if prop=='bag': d.rectangle([90,760,310,890],fill=(200,170,120,255),outline=K,width=11); d.arc([140,700,260,820],180,360,fill=K,width=9); d.rectangle([150,790,250,830],fill=(200,40,40,255)); d.line([100,800,300,800],fill=dk((200,170,120),0.7),width=4)
    if prop=='box': d.rectangle([100,740,300,880],fill=(60,120,180,255),outline=K,width=11); d.line([200,740,200,880],fill=(250,230,120,255),width=16); d.line([100,810,300,810],fill=(250,230,120,255),width=16); d.polygon([(100,740),(140,740),(100,780)],fill=(40,96,150,255))
    if prop=='chalk': d.rectangle([186,740,214,800],fill=(250,250,250,255),outline=K,width=6)
    if prop=='pen': d.line([200,720,200,880],fill=(20,20,24,255),width=16); d.polygon([(192,880),(208,880),(200,900)],fill=K)
    if prop=='redpen': d.line([200,720,200,880],fill=(196,30,30,255),width=16); d.polygon([(192,880),(208,880),(200,900)],fill=K)
    if prop=='megaphone': d.polygon([(180,720),(220,720),(330,890),(70,890)],fill=(236,230,220,255),outline=K); d.ellipse([70,860,330,900],fill=(60,60,64,255),outline=K,width=8); d.line([200,724,200,860],fill=(200,190,176,255),width=6)
    if prop=='pennant': d.line([200,600,200,120],fill=(120,80,40,255),width=12); d.polygon([(200,120),(390,180),(200,250)],fill=tuple(c.get('scarf',(40,60,140)))+(255,),outline=K)
    if prop=='camera': d.rounded_rectangle([110,720,290,840],20,fill=(40,40,44,255),outline=K,width=12); d.ellipse([160,740,240,820],fill=(120,140,170,255),outline=K,width=8)
    if prop=='paper':   # bcn r2 (shots r1: read as an ID card): a folded broadsheet hanging from the mitten by its top edge: masthead, headline, photo, columns
        P=[(40,700),(360,712),(352,898),(32,890)]
        d.polygon(P,fill=(240,234,216,255)); d.line(P+[P[0]],fill=K,width=9)
        d.polygon([(52,722),(348,733),(347,768),(51,757)],fill=(40,36,40,255))
        for k in range(4): d.line([(80+k*66,740+k*2),(118+k*66,741+k*2)],fill=(240,234,216,255),width=8)
        d.polygon([(48,778),(178,782),(176,846),(46,842)],fill=(150,140,128,255))
        for k in range(5):
            d.line([(196,784+k*21),(340,788+k*21)],fill=(120,112,104,255),width=7)
        for k in range(2): d.line([(46,858+k*16),(176,862+k*16)],fill=(120,112,104,255),width=7)
        d.line([(188,772),(186,892)],fill=(170,160,148,255),width=4); mitt()
    if prop=='musket': d.line([200,860,200,60],fill=(90,64,44,255),width=26); d.line([200,860,200,60],fill=K,width=6); d.line([200,300,200,60],fill=(70,70,76,255),width=14); d.polygon([(178,860),(222,860),(236,900),(164,900)],fill=(90,64,44,255),outline=K); mitt()
    if prop=='shovel': d.line([200,860,200,200],fill=(130,96,60,255),width=18); d.line([200,860,200,200],fill=K,width=4); d.polygon([(150,860),(250,860),(240,900),(160,900)],fill=(120,120,126,255),outline=K); d.rectangle([170,180,230,210],fill=(130,96,60,255),outline=K,width=6); mitt()
    if prop=='spyglass': d.rounded_rectangle([170,560,230,760],12,fill=(170,130,60,255),outline=K,width=8); d.rectangle([178,560,222,600],fill=(90,70,40,255)); mitt()
    if prop=='quill': d.line([200,720,240,520],fill=(246,244,238,255),width=22); d.line([200,720,240,520],fill=K,width=4); d.line([200,720,196,780],fill=K,width=6); mitt()
    if prop=='bow': d.arc([60,100,340,900],300,60,fill=(120,84,50,255),width=18); d.line([200,120,200,880],fill=(230,222,200,255),width=4); mitt()
    if prop=='cane': d.line([200,720,200,900],fill=(90,60,40,255),width=18); d.arc([150,660,250,760],180,360,fill=(90,60,40,255),width=18); mitt()
    if prop=='basket': d.rounded_rectangle([90,740,310,890],30,fill=(170,128,70,255),outline=K,width=10); [d.line([100,770+k*36,300,770+k*36],fill=(120,84,44,255),width=5) for k in range(3)]; [d.ellipse([110+k*36,712,150+k*36,752],fill=[(214,170,60,255),(190,60,40,255),(120,60,110,255)][k%3],outline=K,width=5) for k in range(6)]; d.arc([110,640,290,800],180,360,fill=K,width=10); mitt()
    if prop=='oar': d.line([200,900,200,100],fill=(150,110,70,255),width=20); d.line([200,900,200,100],fill=K,width=4); mitt()
    if prop=='lantern': d.line([200,700,200,760],fill=K,width=6); d.rounded_rectangle([150,760,250,880],12,fill=(255,214,120,255),outline=K,width=9); d.rectangle([140,750,260,770],fill=(60,50,44,255)); mitt()
    if prop=='ball':   # bcn: 1899 leather football held in the mitten (r2: fits inside the 900 px arm canvas; was cut at the bottom)
        d.ellipse([86,646,314,874],fill=(150,96,52,255),outline=K,width=12); d.arc([86,680,314,850],200,340,fill=dk((150,96,52),0.6),width=8)
        d.line([200,658,200,862],fill=dk((150,96,52),0.6),width=7); d.arc([126,648,274,874],100,260,fill=dk((150,96,52),0.6),width=7)
        for k in range(4): d.line([186,728+k*20,214,728+k*20],fill=(240,226,190,255),width=6)
        d.ellipse([126,684,170,720],fill=(196,146,96,255)); mitt()
    if prop=='dumbbell':   # bcn r2 (shots r1: read as black dots): iron dumbbell side on, stacked grey plates on a long bar, held at the middle
        G=(108,110,118,255); GD=(78,80,88,255)
        d.line([20,712,380,712],fill=(150,150,158,255),width=22); d.line([20,712,380,712],fill=K,width=4)
        for x0,w in ((24,34),(60,30),(310,30),(342,34)):
            d.rounded_rectangle([x0,(712-95 if w==34 else 712-80),x0+w,(712+95 if w==34 else 712+80)],8,fill=(G if w==34 else GD),outline=K,width=8)
        mitt()
    if prop=='suitcase':   # bcn: leather travel case hanging from the mitten by its handle (r2: whole case inside the canvas)
        d.arc([150,680,250,770],180,360,fill=K,width=14); d.rounded_rectangle([40,725,360,880],16,fill=(120,72,40,255),outline=K,width=12)
        d.line([40,772,360,772],fill=dk((120,72,40),0.6),width=8)
        for x in(90,310): d.rectangle([x-14,715,x+14,880],fill=(90,54,30,255),outline=K,width=5)
    if prop=='phone': d.rounded_rectangle([160,640,240,780],12,fill=(40,40,48,255),outline=K,width=8); mitt()
    if prop in ('box','bag','paper','megaphone','camera'): mitt()   # the mitten sits over the prop so it is held, not floating
    return noodle(im,BEND.get(prop,18) if straight is None else straight)
# r7 (owner Nov 19: forearms stuck out sideways and swung across faces): natural hang 18 deg; 'armS' = straight card for raised and gripping arms
BEND={'suitcase':0,'ball':10,'dumbbell':8,'musket':0,'shovel':6,'spyglass':25,'quill':30,'bow':4,'cane':10,'basket':22,'oar':0,'lantern':18,'phone':28,'pennant':0,'megaphone':15,'paper':20,'bag':20,'box':25,'camera':25,'chalk':30,'pen':30,'redpen':30}
AW=50   # rule 336a (DC 09eca41)   # r4 (rule 329, from Detroit e1ed5d1: Rick arms 5.5-6 % H): was 38
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

# ---- ROUND 5 PROPOSAL (Nov 23 2026, owner: "arms ... slightly bent downwards, and they are raised from down to up ... a basic repetitive
# motion ... repeated for all of the characters"; awaits owner approval). Rick arm-gesture library: whole-arm POSE drawings swapped as
# snaps (1-2 f) with an optional 1-frame in-between, instead of rotating one bent card about the shoulder.
# Evidence (144 labelled Rick arm actions, 20 checked frame by frame): research/rick-style-spec/face-turns-arms/ (project files).
# Each pose = (upper-arm angle, forearm angle) in degrees, 0 = straight down, 90 = straight out, 180 = straight up, negative = across
# the body; drawn as ONE smooth noodle (rounded elbow, no joint; rule 253) of the same thickness and mitten as the hanging arm.
POSES={
 'hang':(8,14),            # rest (our current arm)
 'akimbo':(42,-38),        # hand on hip, elbow out: Rick #03 f466-485 (elbow ~75), #04 f700, #22 f212-235
 'scratch':(122,198),      # hand to the back/side of the head: #03 f370-372 (elbow ~60)
  'chin':(-10,-160),        # hand to chin, thinking: #24 f1112-1116 (elbow ~50)
 'point_up':(168,174),     # straight arm up: #04 f343-344, #04 f405-425 (180)
 'point_out':(96,92),      # straight arm out to the side: #22 f1253-1256 (180), #14 f428-431 (~120)
 'raise':(100,172),        # forearm up beside the head, elbow ~90 ('here is the thing'): #04 f1352, #22 f1077-1084
 'up':(138,168),           # both arms flung up in a U (shock): #03 f1619-1621 (~130), #22 f779-795
 'shrug':(62,118),         # elbows bent down, hands out ('come at me' / shrug): #22 f1325-1331, #10 f397-403
 'belly':(16,-82),         # hand on the belly (laugh): #14 f184-186
 'palm':(24,78),           # forearm out, palm up (talking): #12 f488-498, #10 f600-603
 'windup':(140,218),       # arm cocked back over the shoulder (anticipation of a throw/strike): #03 f625-627, #04 f569-575
 'fling':(108,112),        # arm flung out wide, nearly straight (panic): #14 f141-144, #14 f1089-1100
 'lift':(20,152),          # hand raised to shoulder height in front (toast, sip, show a prop): #04 f702-711, #14 f790-796, #03 f834-838
 'dip':(4,-18),            # 2-frame anticipation dip before a point (#14 f117-119); also the 'pull in' breakdown
}
# ---- ROUND 6 (Nov 23 2026, coordinated motion): more Rick arm drawings, from 70 new strips (#05 #08 #13 #21 #23, two measurers).
# Additive: existing poses unchanged; cards are only made for characters with cast.json "poses". INFERRED = fewer than 2 Rick examples.
POSES.update({
 'reach':(74,84),          # arm out and forward to take something: #13 f722, #08 f983, #21 f1054-1061, #23 f506
 'swing':(34,30),          # arm swung down-forward after an overhead strike/stamp: #21 f359-373, #05 f28-31
 'throw':(86,64),          # follow-through after a fling/toss: #21 f437-443, #23 f1298
 'hands_head':(150,250),   # hand clamped on the head/neck (panic): #21 f1468, #22 f1325-1327 (old labels)
 'wave_a':(128,158),       # [INFERRED] wave, hand up beside the head: #05 f139, #05 f469 (one measurer each)
 'wave_b':(128,196),       # [INFERRED] wave, hand tipped over
 'clap_open':(18,-58),     # [INFERRED] forearms in front, apart: #08 f1116 (one measurer)
 'clap':(10,-96),          # [INFERRED] mittens together in front of the chest
 'cross':(-4,-104),        # [INFERRED] arms folded across the belly (owner list; no Rick example in the new strips)
})
# ROUND 6: Rick leans the TORSO while the legs stay planted (70 new strips: legs moved in 5 of 63, torso leans 10-30 deg, median ~12).
# For characters that use lib.combo() the body card is split in two cards cut from the SAME drawing: the garment (torso) and the legs.
HIP_ROW=520   # texture row (of 1100) of the lean pivot, inside the rounded hem (HEMY 545) so the turning torso always covers the leg tops
def split_body(name,stride=0):
    from PIL import ImageFilter as _F
    im=body(name,stride); kind=C[name].get('body','tall'); pts=_sil(kind)[0]
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).polygon(pts,fill=255); m=m.filter(_F.MaxFilter(2*BOUT+5))
    a=im.getchannel('A'); from PIL import ImageChops as _C
    top=im.copy(); top.putalpha(_C.multiply(a,m))
    legs=im.copy(); legs.putalpha(_C.multiply(a,_C.invert(m)))
    # leg tubes redrawn from higher up (same curve as body(), start 120 px above the hem) and laid BEHIND, so a leaning torso never
    # uncovers a cut leg top
    c=C[name]; legc=dk(tuple(c.get('legs',(40,36,40))),0.8); y1=_sil(kind)[4]; LW=34
    W,H=800*SS,1100*SS; ul=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ul); s_=lambda v:int(v*SS)
    for sx in(-1,1):
        x=400+sx*62; fx=x+sx*20+(sx*60 if stride else 0); lift=(70 if (stride==1 and sx<0) or (stride==2 and sx>0) else 0); fy=1056-lift
        y_0=y1-60; cx_=(x+fx)/2+sx*30; cy_=(y_0+fy)/2
        P=[((1-t)**2*x+2*(1-t)*t*cx_+t*t*fx,(1-t)**2*y_0+2*(1-t)*t*cy_+t*t*fy) for t in [i/24 for i in range(25)]]
        P=[(x+(P[1][0]-x)*-5*k/5,y_0-60*k/5) for k in range(5,0,-1)]+P   # extend the tube straight up 60 px
        d.line(_S(P),fill=K,width=s_(LW),joint='curve'); d.line(_S(P),fill=legc,width=s_(LW-16),joint='curve')
    ul=ul.resize((800,1100),Image.LANCZOS); ul.putalpha(_C.multiply(ul.getchannel('A'),m.point(lambda v:255 if v>0 else 0)))
    out=Image.new('RGBA',im.size,(0,0,0,0)); out.alpha_composite(ul); out.alpha_composite(legs)
    return top,out
POSE_W,POSE_H,POSE_MARGIN=1600,1800,20   # r5b (owner Nov 23 test clip: a shrugging hand was cut off by a straight 'wall graphic' edge): 14 of 45 pose drawings ran past the old 1200 px canvas; shoulder stays at the canvas centre
def pose_arm(name,pose,mix=1.0,over=0.0,frm='hang'):
    """POSE_W x POSE_H card, shoulder at the centre: the pose (or a mix toward it from `frm` for in-betweens, `over` degrees of overshoot)"""
    P0=tuple(POSES[frm])+(330,372)[len(POSES[frm])-2:]; P1=tuple(POSES[pose])+(330,372)[len(POSES[pose])-2:]   # r7: optional (a, cc, U, F) lengths
    a0,c0=P0[:2]; a1,c1=P1[:2]
    a=a0+(a1-a0)*mix+over*(1 if a1>=a0 else -1); cc=c0+(c1-c0)*mix+over*(1 if c1>=c0 else -1)
    U,F=P0[2]+(P1[2]-P0[2])*mix,P0[3]+(P1[3]-P0[3])*mix   # upper arm and forearm; default 330/372 = noodle() reach (712 px at y=40)
    sx0,sy0=POSE_W//2,POSE_H//2
    ex_=sx0+U*math.sin(math.radians(a)); ey_=sy0+U*math.cos(math.radians(a))
    hx=ex_+F*math.sin(math.radians(cc)); hy=ey_+F*math.cos(math.radians(cc))
    # rounded elbow: quadratic through points pulled 28 % in from the elbow on each segment, straight segments elsewhere
    def lerp(p,q,t): return (p[0]+(q[0]-p[0])*t,p[1]+(q[1]-p[1])*t)
    S,E,H=(sx0,sy0),(ex_,ey_),(hx,hy); P1=lerp(E,S,0.28); P2=lerp(E,H,0.28)
    pts=[lerp(S,P1,i/12) for i in range(13)]+[((1-t)**2*P1[0]+2*(1-t)*t*E[0]+t*t*P2[0],(1-t)**2*P1[1]+2*(1-t)*t*E[1]+t*t*P2[1]) for t in [i/16 for i in range(1,17)]]+[lerp(P2,H,i/12) for i in range(1,13)]
    W,Hh=POSE_W,POSE_H; big=Image.new('RGBA',(W*SS,Hh*SS),(0,0,0,0)); bd=ImageDraw.Draw(big)
    bd.line([(x*SS,y*SS) for x,y in pts],fill=K,width=AW*SS,joint='curve')
    for x,y in (pts[0],): bd.ellipse([(x-AW/2)*SS,(y-AW/2)*SS,(x+AW/2)*SS,(y+AW/2)*SS],fill=K)
    bd.ellipse([(hx-50)*SS,(hy-50)*SS,(hx+50)*SS,(hy+50)*SS],fill=K)   # mitten 100 px, as arm()
    im=big.resize((W,Hh),Image.LANCZOS)
    # rule 354b (a): the drawing (arm stroke + mitten) must stay POSE_MARGIN px inside the canvas, or the card edge slices it
    bb=im.getchannel('A').point(lambda v:255 if v>8 else 0).getbbox()
    if bb and (bb[0]<POSE_MARGIN or bb[1]<POSE_MARGIN or bb[2]>W-POSE_MARGIN or bb[3]>Hh-POSE_MARGIN):
        raise SystemExit(f'POSE_CLIP {name} {pose} mix={mix} over={over} bbox={bb} canvas={W}x{Hh}')
    return im
def pose_list(c):
    want=c.get('poses')
    if not want: return []
    return list(POSES) if want=='all' else [p for p in want if p in POSES]

# ---- ROUND 6: back-of-head face ('backview' token, expressions.py round 6). Wraps head() for that one token only.
_head_r5=head
def head(name,fk):
    c=C[name]; spec=c['faces'][fk]; ex=spec[3] if len(spec)>3 else ''
    if 'backview' not in ex: return _head_r5(name,fk)
    keep={k:c.get(k) for k in ('nose','fhair','mustache','stache_small','stubble','beard','glasses')}
    c['nose']=False
    for k in ('fhair','mustache','stache_small','stubble','beard','glasses'): c.pop(k,None)
    try: im=_head_r5(name,fk)
    finally:
        for k,v in keep.items():
            if v is None: c.pop(k,None)
            else: c[k]=v
    # Rick's back views (#04 f349-350 chef and captain, #05 f577 farmer) are the PLAIN head disc: no hair mass, no nape line; hats and the
    # hair that shows above the outline stay as drawn. (A first try painted a hair mass over the crown; the rule-330 sheet showed Rick does not.)
    return im
# ---- ROUND 7 (Nov 23 2026, owner review of the inferred moves): new arm drawings, run legs, 2D effect cards, 3/4 back head.
# Owner: clap with elbows out and hands meeting under the chin; chin taps; a jog and a sprint with all four limbs moving; small
# Rick-style effect drawings (his own: speed lines #14 f143-156, dust puffs under heels #12 f1071-1079, blow arcs #04 f1464-1497,
# impact ticks #14 f570-576, sweat drop #04 f394). All [INFERRED] until the owner approves them on the page.
POSES.update({
 'clap_hi_open':(40.4,-122.2,262,319),   # elbows out to the sides, hands apart just under the chin (owner Nov 23); arms sit behind the face disc, so the hands stay below it
 'clap_hi':(40.4,-112.0,262,426),        # mittens meet under the chin
 'chin_tap':(-10,-146),                  # hand 14 deg off the chin, between taps
 'pump_out_hi':(62,150),                 # run: arm forward and up on the outer side, elbow ~90 deg
 'pump_out_lo':(38,12),                  # run: arm swung back and low on the outer side
 'pump_in_hi':(-8,-132),                 # run: forearm swung up across the chest
 'pump_in_lo':(-14,-38),                 # run: hand low across the belly
})
def run_legs(name,phase,side=1):
    """legs card for a run cycle drawn like split_body()'s legs: phase 1 contact (near leg reaching forward, far leg back), 2 air
    (near knee up, far foot kicked back), 3 and 4 the same with the legs swapped. side +1 = running toward screen right."""
    from PIL import ImageFilter as _F, ImageChops as _C
    c=C[name]; kind=c.get('body','tall'); pts,y0,w0,w1,y1=_sil(kind)
    legc=dk(tuple(c.get('legs',(40,36,40))),0.8); LW=34; s_=lambda v:int(v*SS)
    W,H=800*SS,1100*SS; im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    fwd,bk=((1,-1) if phase in (1,2) else (-1,1))
    def leg(x,knee,foot,lift_toe,col=None):
        h0=(x,y1-120); cpt=(2*knee[0]-(h0[0]+foot[0])/2,2*knee[1]-(h0[1]+foot[1])/2)   # one noodle curve through the knee (Rick legs bend, no joint)
        P=[((1-t)**2*h0[0]+2*(1-t)*t*cpt[0]+t*t*foot[0],(1-t)**2*h0[1]+2*(1-t)*t*cpt[1]+t*t*foot[1]) for t in [i/28 for i in range(29)]]
        d.line(_S(P),fill=K,width=s_(LW),joint='curve'); d.line(_S(P),fill=col or legc,width=s_(LW-16),joint='curve')
        for p_ in (P[0],P[-1]): d.ellipse([s_(p_[0]-LW/2),s_(p_[1]-LW/2),s_(p_[0]+LW/2),s_(p_[1]+LW/2)],fill=K)
        fx,fy=foot; d.ellipse([s_(fx-30+side*16),s_(fy-14-lift_toe),s_(fx+34+side*16),s_(fy+18-lift_toe)],fill=K)
    # the leg on the far side of the body is drawn first and a shade darker, so phases 3/4 read as the other leg (front-on cards)
    farleg=('near' if phase in (3,4) else 'far')
    for who,sx in sorted((('near',side*fwd),('far',side*bk)),key=lambda w:w[0]!=farleg):
        x=400+sx*40; col=dk(legc,0.7) if who==farleg else None
        if phase in (1,3):   # contact: front leg reaches, back leg pushes off
            if who=='near': leg(x,(x+side*120,y1+170),(x+side*230,1056),0,col)   # contact foot on the same row as the standing feet
            else: leg(x,(x-side*70,y1+200),(x-side*190,1010),0,col)
        else:               # air: front knee lifted, back foot kicked up behind
            if who=='near': leg(x,(x+side*150,y1+120),(x+side*120,y1+330),0,col)
            else: leg(x,(x-side*60,y1+240),(x-side*220,y1+170),0,col)
    return im.resize((800,1100),Image.LANCZOS)   # sits 1.5 mm behind the torso card, which covers the hip ends
FX_SIZE=600
def fx(kind):
    """2D effect cards, 600x600, drawn in our ink colour. Anchor = card centre."""
    S2=FX_SIZE*SS; im=Image.new('RGBA',(S2,S2),(0,0,0,0)); d=ImageDraw.Draw(im); s_=lambda v:int(v*SS); cx=cy=300
    W_=(255,255,255,255)
    if kind=='clap':      # short dashed strokes bursting out of the clap, both sides
        for ang in (-150,-120,-90,-60,-30,30,150):
            r=math.radians(ang)
            for r0,r1 in ((90,140),(160,210)):
                p0=(cx+r0*math.cos(r),cy+r0*math.sin(r)); p1=(cx+r1*math.cos(r),cy+r1*math.sin(r))
                d.line([(p0[0]*SS,p0[1]*SS),(p1[0]*SS,p1[1]*SS)],fill=K,width=s_(20)); d.line([(p0[0]*SS,p0[1]*SS),(p1[0]*SS,p1[1]*SS)],fill=W_,width=s_(8))   # white core: reads on dark coats
    elif kind=='puff':    # huff: three blow arcs and a small cloud puff out of the nose (to the right; mirrored for left)
        for k,(r0,w) in enumerate(((60,14),(105,12),(150,10))):
            d.arc([s_(cx-r0),s_(cy-r0),s_(cx+r0),s_(cy+r0)],-35,35,fill=K,width=s_(w))
        for (px,py,r) in ((cx+200,cy-20,34),(cx+240,cy+18,28),(cx+186,cy+30,24)):
            d.ellipse([s_(px-r),s_(py-r),s_(px+r),s_(py+r)],fill=W_,outline=K,width=s_(9))
    elif kind=='startle': # jolt ticks all round the head (teardrop ticks like Rick's impact bursts)
        for ang in range(-170,10,20):
            r=math.radians(ang); r0,r1=215,280
            p0=(cx+r0*math.cos(r),cy+r0*math.sin(r)); p1=(cx+r1*math.cos(r),cy+r1*math.sin(r))
            d.line([(p0[0]*SS,p0[1]*SS),(p1[0]*SS,p1[1]*SS)],fill=K,width=s_(13))
        for ang in (-170,-10):
            r=math.radians(ang); p0=(cx+215*math.cos(r),cy+215*math.sin(r)); p1=(cx+290*math.cos(r),cy+290*math.sin(r))
            d.line([(p0[0]*SS,p0[1]*SS),(p1[0]*SS,p1[1]*SS)],fill=K,width=s_(13))
    elif kind=='sweat':   # one sweat drop
        P=[(cx,cy-70)]+[(cx+42*math.sin(t),cy+20-42*math.cos(t)) for t in [math.radians(a) for a in range(-120,121,10)]]
        d.polygon(_S(P),fill=(150,205,240,255),outline=K,width=s_(10)); d.ellipse([s_(cx-14),s_(cy-8),s_(cx-2),s_(cy+10)],fill=W_)
    elif kind=='speed':   # speed lines trailing behind a runner (runner faces right; mirrored for left)
        for y_,x0,x1 in ((-170,40,250),(-90,0,230),(-10,30,270),(70,10,220),(150,50,240)):
            d.line([(s_(x0)),s_(cy+y_),s_(x1),s_(cy+y_)],fill=K,width=s_(10))
    elif kind=='dust':    # dust puffs kicked up under the heels
        for (px,py,r) in ((cx-60,cy+40,52),(cx-130,cy+60,40),(cx+10,cy+70,36),(cx-190,cy+20,28)):
            d.ellipse([s_(px-r),s_(py-r),s_(px+r),s_(py+r)],fill=(236,228,214,255),outline=K,width=s_(9))
    elif kind=='think':   # three small bubbles rising beside the head
        for (px,py,r) in ((cx+40,cy+120,16),(cx+90,cy+60,24),(cx+150,cy-10,34)):
            d.ellipse([s_(px-r),s_(py-r),s_(px+r),s_(py+r)],fill=W_,outline=K,width=s_(8))
    return im.resize((FX_SIZE,FX_SIZE),Image.LANCZOS)
FX_KINDS=('clap','puff','startle','sweat','speed','dust','think')
_head_r6=head
def head(name,fk):
    """'back3qL' / 'back3qR' (token backview + ear side): the back view turned a little toward one side, so an ear and the edge of the
    cheek show at that side (Rick #22 f468-469, #03 f80: on the way round to the back the face slides off the disc)."""
    c=C[name]; spec=c['faces'][fk]; ex=spec[3] if len(spec)>3 else ''
    if 'back3q' not in ex: return _head_r6(name,fk)
    side=1 if 'back3qR' in ex else -1
    sp0=c['faces'][fk]; c['faces'][fk]=[sp0[0],sp0[1],sp0[2],'backview']
    try: im=_head_r6(name,fk)
    finally: c['faces'][fk]=sp0
    w,h=im.size; d=ImageDraw.Draw(im); pt,pb=X.pads(c)
    R=w*400/1024; cx=w/2+side*0; cy=pt+512   # disc centre in card px
    ex_=cx+side*R*0.93; ey=cy+R*0.12; er=R*0.15
    skin=im.getpixel((int(cx),int(cy+R*0.3)))[:3]+(255,)   # the disc's own (scene-tinted) skin
    d.ellipse([ex_-er,ey-er*1.3,ex_+er,ey+er*1.3],fill=skin,outline=K,width=int(OUT*w/1024*0.8))
    d.arc([cx-R*0.98,cy-R*0.98,cx+R*0.98,cy+R*0.98],(10 if side>0 else 150),(30 if side>0 else 170),fill=K,width=int(OUT*w/1024*0.5))
    return im
# ---- ROUND 8 (Nov 23 2026, owner review of round 7): the BODY turns with the head (look back, turn away).
# Rick swaps the whole figure, not just the head, when someone turns to the back: #04 f349-350 (captain: whole figure to a back view),
# #22 f469-470 (head + torso swap to the back drawing, one 3/4 in-between), #03 f80 (body to 3/4 back in 1 f). Our torso card is turned
# like a cylinder: the front details slide toward the turned side and wrap out of view, the revealed side is plain coat (the back), and
# the original outline is kept, so the silhouette and limb joins do not move. Feet turn with it. [INFERRED drawings]
def turn_top(name,theta):
    """torso card turned theta degrees (+ = toward screen right; 180 = back view)"""
    top=split_body(name,0)[0]; A=np.asarray(top).astype(np.float32); H,W=A.shape[:2]; a=A[...,3]
    from PIL import ImageFilter as _F
    m=Image.fromarray((a>8).astype(np.uint8)*255); er=np.asarray(m.filter(_F.MinFilter(2*int(BOUT*0.8)+1)))>0
    ring=(a>8)&~er
    c=C[name]; coat=np.array(list(c['coat'][:3])+[255],np.float32); shade=np.array(list(dk(tuple(c['coat'][:3]),0.74)),np.float32)
    out=A.copy(); th=math.radians(theta)
    for y in range(H):
        xs=np.nonzero(er[y])[0]
        if len(xs)<4: continue
        xl,xr=xs[0],xs[-1]; cx=(xl+xr)/2; R=max(1.0,(xr-xl)/2)
        for x in range(xl,xr+1):
            u=max(-1.0,min(1.0,(x-cx)/R)); phi=math.asin(u)-th
            if abs(phi)<=math.pi/2:
                sx_=int(round(cx+R*math.sin(phi)))
                if er[y,min(W-1,max(0,sx_))]: out[y,x]=A[y,sx_]; continue
            out[y,x]=shade if x<cx-0.33*R else coat   # the coat's back, with the same cel shadow side as the front
        if abs(theta)>=150:   # back view: a centre seam
            for x in range(int(cx)-3,int(cx)+4): out[y,x]=np.array(list(dk(tuple(c['coat'][:3]),0.55)),np.float32)
    out[ring]=A[ring]
    return Image.fromarray(out.clip(0,255).astype(np.uint8),'RGBA')
def turned_legs(name,kind,side=1):
    """legs card for a turned body: kind 'turn' (both feet point to `side`) or 'back' (feet seen from behind)"""
    c=C[name]; k_=c.get('body','tall'); pts,y0,w0,w1,y1=_sil(k_)
    legc=dk(tuple(c.get('legs',(40,36,40))),0.8); LW=34; s_=lambda v:int(v*SS)
    im=Image.new('RGBA',(800*SS,1100*SS),(0,0,0,0)); d=ImageDraw.Draw(im)
    for sx in (-1,1):
        x=400+sx*(44 if kind=='turn' else 56); fx=x+(side*14 if kind=='turn' else sx*8); fy=1056
        y_0=y1-120; cx_=(x+fx)/2+(side*18 if kind=='turn' else sx*14); cy_=(y_0+fy)/2
        P=[((1-t)**2*x+2*(1-t)*t*cx_+t*t*fx,(1-t)**2*y_0+2*(1-t)*t*cy_+t*t*fy) for t in [i/24 for i in range(25)]]
        col=dk(legc,0.7) if (kind=='turn' and sx==-side) else legc   # far leg a shade darker
        d.line(_S(P),fill=K,width=s_(LW),joint='curve'); d.line(_S(P),fill=col,width=s_(LW-16),joint='curve')
        for p_ in (P[0],P[-1]): d.ellipse([s_(p_[0]-LW/2),s_(p_[1]-LW/2),s_(p_[0]+LW/2),s_(p_[1]+LW/2)],fill=K)
        if kind=='turn': d.ellipse([s_(fx-24+side*30),s_(fy-14),s_(fx+40+side*30),s_(fy+18)],fill=K)   # foot pointing to the side
        else: d.ellipse([s_(fx-26),s_(fy-12),s_(fx+26),s_(fy+16)],fill=K)                             # heel seen from behind
    return im.resize((800,1100),Image.LANCZOS)
TOP_TURNS={'q':45,'qb':135,'back':180}
# ---- ROUND 8b (owner review 2, Nov 23 14:46Z): clap hands higher and touching; chin taps higher on the face; clap dashes start
# outside the body outline. These hands sit IN FRONT of the face (owner asked for it; exception to rule 268, see FRONT_POSES).
POSES.update({
 'clap_up_open':(40.4,-130.65,262,421.5),   # elbows out, hands apart over the chin line (hand centre -150,-75 px from the shoulder)
 'clap_up':(40.4,-123.2,262,501.6),        # mittens touch at the body centre, over the chin line (hand centre -250,-75)
 'chin_hi':(32.7,-149.67,166,474.7),        # hand on the chin and lower face, elbow tucked (Rick #24 f1112-1116 think pose, higher contact)
 'chin_hi_tap':(36.0,-145.78,166,422.4),    # hand drops off the face between taps
})
FRONT_POSES={'clap_up_open','clap_up','chin_hi','chin_hi_tap'}   # drawn between the face (-12 mm) and the head effects (-16 mm)
def _fx_clap2(d,cx,cy,s_,W_):
    """r8b clap dashes: two short strokes per ray, upward and outward only, starting OUTSIDE the body outline (radius 205-290 px of
    a 600 px card = 0.24-0.34 m at 0.7 m), so they read off to the side of the character but close to it (owner Nov 23 14:46Z)"""
    for ang in (-172,-155,-138,-42,-25,-8):
        r=math.radians(ang)
        for r0,r1 in ((218,250),(262,292)):
            p0=(cx+r0*math.cos(r),cy+r0*math.sin(r)); p1=(cx+r1*math.cos(r),cy+r1*math.sin(r))
            d.line([(p0[0]*SS,p0[1]*SS),(p1[0]*SS,p1[1]*SS)],fill=K,width=s_(20)); d.line([(p0[0]*SS,p0[1]*SS),(p1[0]*SS,p1[1]*SS)],fill=W_,width=s_(8))
_fx_r7=fx
def fx(kind):
    if kind!='clap2': return _fx_r7(kind)
    S2=FX_SIZE*SS; im=Image.new('RGBA',(S2,S2),(0,0,0,0)); d=ImageDraw.Draw(im); s_=lambda v:int(v*SS)
    _fx_clap2(d,300,300,s_,(255,255,255,255))
    return im.resize((FX_SIZE,FX_SIZE),Image.LANCZOS)
FX_KINDS=FX_KINDS+('clap2',)
# ---- ROUND 8c (owner Nov 23 15:02Z: "make a walking animation"): walk cycle legs + arm swing drawings. Rick #12 f145-205 walks with the
# legs redrawn on every drawing, one foot always on the ground, short strides, arms swinging opposite the legs. [INFERRED] timing.
POSES.update({
 'walk_out':(22,30),     # walk: arm swung forward/out, a soft elbow (opposite the forward leg)
 'walk_in':(-10,-4),     # walk: arm swung back/in, nearly straight
 'walk_mid':(4,6),       # walk passing drawing: arm by the side
})
def walk_legs(name,phase,side=1):
    """legs card for a walk cycle, same build as run_legs(): 1 contact (front heel down, back toe pushing off, both feet on the floor row),
    2 passing (support leg straight under the hip, swing foot lifted 60 px and passing), 3/4 the same with the legs swapped.
    side +1 = walking toward screen right. No airborne drawing: one foot is always on row 1056."""
    c=C[name]; kind=c.get('body','tall'); pts,y0,w0,w1,y1=_sil(kind)
    legc=dk(tuple(c.get('legs',(40,36,40))),0.8); LW=34; s_=lambda v:int(v*SS)
    W,H=800*SS,1100*SS; im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    def leg(x,knee,foot,lift_toe,col=None,heel=False):
        h0=(x,y1-120); cpt=(2*knee[0]-(h0[0]+foot[0])/2,2*knee[1]-(h0[1]+foot[1])/2)
        P=[((1-t)**2*h0[0]+2*(1-t)*t*cpt[0]+t*t*foot[0],(1-t)**2*h0[1]+2*(1-t)*t*cpt[1]+t*t*foot[1]) for t in [i/28 for i in range(29)]]
        d.line(_S(P),fill=K,width=s_(LW),joint='curve'); d.line(_S(P),fill=col or legc,width=s_(LW-16),joint='curve')
        for p_ in (P[0],P[-1]): d.ellipse([s_(p_[0]-LW/2),s_(p_[1]-LW/2),s_(p_[0]+LW/2),s_(p_[1]+LW/2)],fill=K)
        fx,fy=foot; d.ellipse([s_(fx-30+side*16),s_(fy-14-lift_toe),s_(fx+34+side*16),s_(fy+18-lift_toe)],fill=K)
    farleg=('near' if phase in (3,4) else 'far')
    fwd,bk=((1,-1) if phase in (1,2) else (-1,1))
    for who,sx in sorted((('near',side*fwd),('far',side*bk)),key=lambda w:w[0]!=farleg):
        x=400+(side if who=='near' else -side)*36; col=dk(legc,0.7) if who==farleg else None   # forward/support role on the walk side's hip: legs never cross
        if phase in (1,3):   # contact: front heel down ahead, back foot behind on its toe; both on the floor row
            if who=='near': leg(x,(x+side*70,y1+230),(x+side*130,1056),6,col)
            else: leg(x,(x-side*50,y1+240),(x-side*120,1050),0,col)
        else:               # passing: support leg under the hip, swing foot lifted beside it
            if who=='near': leg(x,(x+side*6,y1+250),(x+side*10,1056),0,col)
            else: leg(x,(x+side*40,y1+190),(x-side*10,996),0,col)
    return im.resize((800,1100),Image.LANCZOS)
# ---- ROUND 9 (owner Nov 23 10:49 AM CT: the round-8 walk "feels unnatural"; vary stride by situation, better arms and legs).
# Rick #12 f145-205: legs redrawn every 2 f, noodle legs that bend at the knee as the foot swings, a step every ~7.5 f (median of 23
# Rick walk cadences), no squash and stretch on walks, bodies slide while the legs cycle, arms hang and swing a little about the shoulder
# (guide: rotating the rest arm about the shoulder is kept for walking swing). Our walk v2 is a CONTINUOUS cycle (not 4 held drawings):
# each leg follows a stance (foot flat, sliding back) and a swing (foot lifts on a sine and comes forward with ease-in-out); the knee
# bends by keeping the leg length, so a lifted or reaching foot bends it the way Rick's do. [INFERRED: stride, lift, cadence]
WALK_STYLES={   # stride px (foot travel per step on an 800 px card), lift px, drawings per cycle (on 2s), hips apart px, toe lift px
 'st':dict(name='stroll',stride=96,lift=36,n=10,toe=6),    # 20 f cycle = 10 f a step: easy, unhurried
 'nm':dict(name='walk',  stride=140,lift=52,n=8, toe=8),   # 16 f cycle = 8 f a step (Rick median 7.5)
 'br':dict(name='brisk', stride=186,lift=70,n=6, toe=10),  # 12 f cycle = 6 f a step: in a hurry
}
def walk2_legs(name,style,i,view='R'):
    """walk v2 legs card: drawing i of WALK_STYLES[style]['n']; view 'R'/'L' = walking across toward screen right/left (3/4 body),
    'F' = walking toward the camera (front body; knees bend outward, feet lift; feet never below row 1056). Leg A (light) and leg B (a shade darker, drawn first)
    are half a cycle apart; one foot is always on row 1056 (each leg is in stance for half the cycle)."""
    W_=WALK_STYLES[style]; c=C[name]; kind=c.get('body','tall'); pts,y0,w0,w1,y1=_sil(kind)
    legc=dk(tuple(c.get('legs',(40,36,40))),0.8); LW=34; s_=lambda v:int(v*SS)
    im=Image.new('RGBA',(800*SS,1100*SS),(0,0,0,0)); d=ImageDraw.Draw(im)
    side=-1 if view=='L' else 1; hy=y1-120; L0=1056-hy; Lc=L0*1.01
    def foot_at(p):
        if p<0.5:   # stance: foot flat, slides from front to back; heel rises in the last fifth (toe-off)
            t=p/0.5; return W_['stride']/2-W_['stride']*t,0.0,(W_['toe']*max(0.0,(t-0.8)/0.2))
        t=(p-0.5)/0.5; e=(1-math.cos(math.pi*t))/2   # swing: ease-in-out forward, sine lift
        return -W_['stride']/2+W_['stride']*e,W_['lift']*math.sin(math.pi*t),0.0
    def draw(hx,p,col,sx):
        dx,lift,toe=foot_at(p)
        if view=='F':   # toward the camera: travel is depth, so the foot stays under the hip; the knee bows outward
            fx_=hx+sx*6; fy=1056-lift; dd=math.hypot(dx*0.35,fy-hy); kdir=sx   # feet stay on the floor row (rigcheck FOOT); depth shortens the leg only a little   # a foot further forward sits a touch lower
        else:
            fx_=hx+side*dx; fy=1056-lift; dd=math.hypot(fx_-hx,fy-hy); kdir=side
        # thigh + shin of equal length Lc/2 with a ROUNDED knee (like the arm elbow), knee pushed out perpendicular to the hip-foot line
        cx_,cy_=(hx+fx_)/2,(hy+fy)/2; ux,uy=(fx_-hx)/max(dd,1),(fy-hy)/max(dd,1); nx,ny=-uy,ux
        if nx*kdir<0: nx,ny=-nx,-ny
        if view=='F': nx,ny=kdir*0.8,0.0
        b=0.5*math.sqrt(max(0.0,Lc*Lc-dd*dd)); Kn=(cx_+nx*b,cy_+ny*b)
        def lerp(P_,Q_,t): return (P_[0]+(Q_[0]-P_[0])*t,P_[1]+(Q_[1]-P_[1])*t)
        S0,F0=(hx,hy),(fx_,fy); A_=lerp(Kn,S0,0.30); B_=lerp(Kn,F0,0.30)
        P=[lerp(S0,A_,k/12) for k in range(13)]+[((1-t)**2*A_[0]+2*(1-t)*t*Kn[0]+t*t*B_[0],(1-t)**2*A_[1]+2*(1-t)*t*Kn[1]+t*t*B_[1]) for t in [k/16 for k in range(1,17)]]+[lerp(B_,F0,k/12) for k in range(1,13)]
        d.line(_S(P),fill=K,width=s_(LW),joint='curve'); d.line(_S(P),fill=col,width=s_(LW-16),joint='curve')
        for p_ in (P[0],P[-1]): d.ellipse([s_(p_[0]-LW/2),s_(p_[1]-LW/2),s_(p_[0]+LW/2),s_(p_[1]+LW/2)],fill=K)
        if view=='F': d.ellipse([s_(fx_-28),s_(fy-14-toe),s_(fx_+28),s_(fy+16-toe)],fill=K)
        else: d.ellipse([s_(fx_-30+side*16),s_(fy-14-toe),s_(fx_+34+side*16),s_(fy+18-toe)],fill=K)
    p=i/W_['n']; hs=40 if view=='F' else 20   # hips: wide apart from the front, nearly one line from the side (legs overlap, never an X)
    draw(400+(-hs if view=='F' else -side*hs),(p+0.5)%1.0,dk(legc,0.7),-1)   # leg B, far / darker, first
    draw(400+(hs if view=='F' else side*hs),p,legc,1)                        # leg A
    return im.resize((800,1100),Image.LANCZOS)
# ---- ROUND 10 (owner Nov 23 2:31 PM CT: walk arms swung together and stayed bent inward; arms must swing opposite each other, changing
# with each step). Rick #24 f733-771 (pedestrian walking across, 3/4 body): the arm on the trailing side hangs in FRONT of the torso and
# swings forward (hand toward the walk direction, elbow softly bent, hand up to the belly) and back (nearly straight, hand behind the
# hip); the leading-side arm is mostly hidden BEHIND the torso and shows its hand ahead of or behind the body on the opposite beat.
# Rick #04 f941-952 / #12 f145-205 (toward camera): arms hang a little away from the body and swing gently. Drawings on 2s like the legs.
WALK_ARMS={   # (a, cc) back extreme -> forward extreme, per role; a = upper arm from straight down (+ outward), cc = forearm direction
 'st':{'n':((10,14),(-14,-38)),'f':((-6,-6),(16,34)),'t':((8,10),(3,-16))},
 'nm':{'n':((16,22),(-24,-62)),'f':((-8,-8),(22,50)),'t':((10,13),(2,-28))},
 'br':{'n':((22,30),(-32,-92)),'f':((-10,-10),(28,72)),'t':((12,16),(0,-44))},
}
def _walk_arm_poses():
    for st,R in WALK_ARMS.items():
        n=WALK_STYLES[st]['n']
        for role,(bk,fw) in R.items():
            for k in range(n):
                w=(1+math.cos(2*math.pi*k/n))/2   # k=0: forward extreme, k=n/2: back extreme
                POSES[f'wa{st}{role}{k}']=(round(bk[0]+(fw[0]-bk[0])*w,2),round(bk[1]+(fw[1]-bk[1])*w,2))
_walk_arm_poses()
BACK_POSE_ROLE='f'   # walk poses 'wa<st>f<k>' (leading-side arm) are drawn BEHIND the torso (lib BACK_Y)
if __name__=='__main__':
    out={}
    import os as _os; ONLY=[x for x in _os.environ.get('ONLY','').split(',') if x]
    for n,c in C.items():
        if ONLY and n not in ONLY: continue
        for fk in c['faces']:
            _fp=f'{T}{n}_h_{fk}.png'
            if _os.environ.get('SKIPEXIST') and _os.path.exists(_fp) and _os.path.getsize(_fp)>2000:
                try: Image.open(_fp).load(); continue
                except Exception: pass
            head(n,fk).save(_fp)
        body(n).save(f'{T}{n}_body.png'); body(n,1).save(f'{T}{n}_bodyw1.png'); body(n,2).save(f'{T}{n}_bodyw2.png')
        for p in c.get('props',[None]): arm(n,p).save(f'{T}{n}_arm{"_"+p if p else ""}.png')
        arm(n).save(f'{T}{n}_arm.png'); arm(n,straight=4).save(f'{T}{n}_armS.png')
        if c.get('combos') or c.get('combos_approved'):   # round 6 (opt-in): split torso/legs cards for lib.combo()
            _t,_l=split_body(n); _t.save(f'{T}{n}_btop.png'); _l.save(f'{T}{n}_blegs.png')
            for _s in (1,2): split_body(n,_s)[1].save(f'{T}{n}_blegsw{_s}.png')
            for _k,_t in TOP_TURNS.items():   # round 8: turned torso cards + turned feet
                if _k=='back': turn_top(n,180).save(f'{T}{n}_btopback.png')
                else: turn_top(n,_t).save(f'{T}{n}_btop{_k}R.png'); turn_top(n,-_t).save(f'{T}{n}_btop{_k}L.png')
            turned_legs(n,'turn',1).save(f'{T}{n}_blegsturnR.png'); turned_legs(n,'turn',-1).save(f'{T}{n}_blegsturnL.png'); turned_legs(n,'back').save(f'{T}{n}_blegsback.png')
            for _ph in (1,2,3,4):   # round 7: run cycle legs, both directions (no mirrored cards, rule 272)
                walk_legs(n,_ph,1).save(f'{T}{n}_blegswalkR{_ph}.png'); walk_legs(n,_ph,-1).save(f'{T}{n}_blegswalkL{_ph}.png')   # r8c walk
            for _st,_W in WALK_STYLES.items():   # r9 walk v2 (continuous cycle, three strides, across both ways + toward camera)
                for _i in range(_W['n']):
                    for _v in 'RLF': walk2_legs(n,_st,_i,_v).save(f'{T}{n}_blegswk{_v}{_st}{_i}.png')
            for _ph in (1,2,3,4):   # bcn fix: d5 had this line inside the walk-style loop, so only run phase 4 was ever written (jog/sprint need 1-4)
                run_legs(n,_ph,1).save(f'{T}{n}_blegsrunR{_ph}.png'); run_legs(n,_ph,-1).save(f'{T}{n}_blegsrunL{_ph}.png')
        for _p in pose_list(c):   # round 5 proposal (opt-in "poses"): pose card, 1-frame in-between from rest, overshoot for settles
            pose_arm(n,_p).save(f'{T}{n}_arm_pose_{_p}.png'); pose_arm(n,_p,mix=0.5).save(f'{T}{n}_arm_pose_{_p}_m.png'); pose_arm(n,_p,over=9).save(f'{T}{n}_arm_pose_{_p}_o.png')
        # r7 (rule 272): left arms get their own mirrored texture, never a negative object scale (the PC GPU drew a mirrored card as a black box)
        import glob as _g
        for fp in _g.glob(f'{T}{n}_arm*.png'):
            if fp.endswith('_L.png'): continue
            Image.open(fp).transpose(Image.FLIP_LEFT_RIGHT).save(fp[:-4]+'_L.png')
    if ONLY and '__fx__' not in ONLY: raise SystemExit('PART_OK')
    for _k in FX_KINDS:   # round 7: effect cards (shared by every character), both facings
        _im=fx(_k); _im.save(f'{T}fx_{_k}.png'); _im.transpose(Image.FLIP_LEFT_RIGHT).save(f'{T}fx_{_k}_L.png')
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
