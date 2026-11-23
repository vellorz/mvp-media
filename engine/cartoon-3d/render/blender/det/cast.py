# Flat 2D cut-out cast, Rick construction: round cream head, monoline dark outline (~2.3 % of head width), drawn face,
# bean/stick body with one costume cue, flat colour blocks + soft gradient + fabric lines. Our own designs.
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import json, math
import expressions as X   # Rick-style expression library (opt-in per character via cast.json "library")
T='/root/det/tex/'; K=(50,28,42,255); SK=(251,244,241,255); OUT=27   # r8 (owner Nov 20: clone Rick's characters): pure white heads like Rick's. r8b (guide v1.3 x.3): dark plum ink, never pure black; 27 px on an 800 px disc = 3.4 % lit side
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
C=X.expand(json.load(open('/root/det/src/cast.json')))
def head(name,fk):
    c=C[name]; e,b,m=c['faces'][fk][:3]; ex=c['faces'][fk][3] if len(c['faces'][fk])>3 else ''
    im,d=new(1024,1024); hair=tuple(c.get('hair',(60,40,30)))+(255,)
    hs=c.get('hairstyle','short')
    HD=c.get('hairdo'); TD=X.turn_dx(c,ex); PT,PB=X.pads(c)   # round 3: PT/PB = extra texture rows above/below for tall hats, hair and beards   # round 2: Rick hairstyles replace the old ones; TD = face slide toward the turned side
    if HD: hs='_hairdo'; X.hairdo_back(d,HD,hair,K)
    if hs=='bun': d.ellipse([382,40,642,280],fill=hair,outline=K,width=OUT)
    if hs=='long': d.rounded_rectangle([100,260,924,980],200,fill=hair,outline=K,width=OUT)
    if hs=='mullet': d.rounded_rectangle([170,320,854,1010],140,fill=hair,outline=K,width=OUT)   # back hair, crown to shoulders
    # r5 (owner Nov 22: the M family's slab of 'long' hair read as weird): new women's styles that frame the head, never a slab behind it
    if hs=='bob': d.rounded_rectangle([96,190,928,760],250,fill=hair,outline=K,width=OUT)   # chin-length bob, sides show down to the jaw
    if hs=='ponytail': d.ellipse([800,330,1000,640],fill=hair,outline=K,width=OUT); d.ellipse([850,300,930,380],fill=dk(hair,0.7),outline=K,width=10)   # tail out to the side
    if hs=='perm':
        for a in range(0,360,30): x=CX+380*math.cos(math.radians(a)); y=500+360*math.sin(math.radians(a))*0.95; d.ellipse([x-120,y-120,x+120,y+120],fill=hair,outline=K,width=OUT)
    skin=tuple(X.skin_rgb(c.get('skin'),SK[:3]))+(255,)   # round 4 proposal: 'skin' may name a Rick skin preset (X.SKIN)
    # r8b (guide v1.3 x.3): ink 3.4 % of head width toward the light (upper right), 6 % away from it and under the chin
    d.ellipse([112,140,912,940],fill=K); d.ellipse([112+48,140+27,912-27,940-48],fill=skin)
    head_shade(im,skin); d=ImageDraw.Draw(im)
    # r9 (RENDER_SPEC_v1.4 A: eyes centred ~69 % up the head): hair and hats are drawn on their own layer and squashed to the top 40 % of the
    # head (x0.6 from the top), the face features on a layer moved up 105 px (eyes at 65.6 % up)
    if 'angryfill' in ex: 
        ov=Image.new('RGBA',(1024,1024),(0,0,0,0)); od=ImageDraw.Draw(ov); od.ellipse([130,158,894,922],fill=(170,60,170,120)); im.alpha_composite(ov); d=ImageDraw.Draw(im)
    if 'gloom' in ex or 'redglow' in ex: X.pre(im,ex); d=ImageDraw.Draw(im)   # library: rage gloom on the head top
    PRE=im.copy() if c.get('hat3d') else None   # round 3: head before any front hair, to undo hair under a hat
    if hs in('short','bald','bun','mullet'):   # r9: hairlines raised with the features (hair ends ~285, brows at 300)
        if hs=='short': d.chord([150,150,874,420],180,360,fill=hair,outline=K,width=OUT)
        if hs=='bun': d.chord([150,150,874,410],180,360,fill=hair,outline=K,width=OUT)
        if hs=='bald':
            for sx in(-1,1): d.chord([CX+sx*390-100,300,CX+sx*390+100,580],90 if sx>0 else 270,270 if sx>0 else 450,fill=hair)
        if hs=='mullet': d.chord([150,150,874,420],180,360,fill=hair,outline=K,width=OUT)
        pass
    if hs in('bob','ponytail','topbun'):
        if hs=='topbun': d.ellipse([392,30,632,250],fill=hair,outline=K,width=OUT)
        d.chord([150,150,874,440],180,360,fill=hair,outline=K,width=OUT)
        if hs=='bob': d.chord([150,150,640,520],180,330,fill=hair,outline=K,width=OUT-8)   # side-swept fringe, part on the right
    if HD: X.hairdo(d,HD,hair,K,dx=TD//3)
    if c.get('hat')=='leather':
        HC=tuple(c.get('hatcol',(80,60,44)))+(255,)
        for sx in(-1,1): d.rounded_rectangle([CX+sx*400-70,330,CX+sx*400+70,660],50,fill=HC,outline=K,width=OUT-6)
        d.arc([CX-360,420,CX+360,900],20,160,fill=dk(HC,0.6),width=12)   # chin strap
        d.chord([100,20,924,470],180,360,fill=HC,outline=K,width=OUT); d.rectangle([112,222,912,256],fill=dk(HC,0.8),outline=K,width=10)
        for x in (CX-170,CX,CX+170): d.line([x,40,x,222],fill=dk(HC,0.6),width=12)
    if c.get('headset'):
        d.arc([140,110,884,700],200,340,fill=(50,50,56,255),width=30)
        for sx in(-1,1): d.ellipse([CX+sx*385-60,420,CX+sx*385+60,560],fill=(50,50,56,255),outline=K,width=12)
        d.line([CX+385,540,CX+180,730],fill=(50,50,56,255),width=14); d.ellipse([CX+150,700,CX+210,760],fill=(30,30,34,255))
    base=im; im,d=new(1024,1024)   # hats on their own layer, squashed x0.6 from the top (peaks end <= 245)
    hat=c.get('hat')
    if hat=='cop':
        d.chord([140,60,884,400],180,360,fill=(28,36,70,255),outline=K,width=OUT); d.rectangle([150,230,874,300],fill=(28,36,70,255),outline=K,width=OUT)
        d.chord([180,270,844,400],0,180,fill=(20,20,26,255),outline=K,width=OUT)   # peak; r8b (round-7 C4: brows were drawn on the dark peak): peak ends at y 400, brows sit below it
        d.polygon([(CX,130),(CX+44,175),(CX+30,225),(CX-30,225),(CX-44,175)],fill=(214,180,80,255),outline=K)  # plain shield, no text
    if hat=='flatcap': d.chord([150,140,874,480],180,360,fill=(90,90,96,255),outline=K,width=OUT); d.chord([200,300,760,400],0,180,fill=(70,70,76,255),outline=K,width=OUT)
    if hat=='ladyhat': d.ellipse([60,250,964,380],fill=(150,40,60,255),outline=K,width=OUT); d.chord([230,90,794,420],180,360,fill=(150,40,60,255),outline=K,width=OUT); d.ellipse([680,150,780,250],fill=(240,200,80,255),outline=K,width=10)
    if hat=='beanie': d.chord([140,110,884,460],180,360,fill=tuple(c['scarf'])+(255,),outline=K,width=OUT); d.ellipse([462,60,562,160],fill=(250,250,250,255),outline=K,width=12)
    HC=tuple(c.get('hatcol',(80,60,44)))+(255,)
    if hat=='fedora': d.ellipse([90,300,934,400],fill=HC,outline=K,width=OUT); d.rounded_rectangle([250,90,774,350],60,fill=HC,outline=K,width=OUT); d.rectangle([250,280,774,330],fill=dk(HC,0.5)); d.line([400,110,512,150,624,110],fill=dk(HC,0.7),width=12)
    if hat=='cloche': d.chord([150,70,874,470],180,360,fill=HC,outline=K,width=OUT); d.ellipse([150,240,874,330],fill=HC,outline=K,width=OUT-6); d.rectangle([160,250,864,290],fill=dk(HC,0.6)); d.ellipse([690,200,770,280],fill=(240,220,170,255),outline=K,width=9)
    if hat=='visor': d.chord([170,270,854,420],180,360,fill=(60,140,90,200),outline=K,width=OUT); d.rectangle([170,330,854,350],fill=K)
    top=im.resize((1024,int(1024*0.6)),Image.LANCZOS); im=base
    if c.get('hat_tilt') or TD:   # round 2: hats sit tilted and slide a little with the turn (Rick #24 trucker, #03 bowler)
        tl=Image.new('RGBA',(1024,1024),(0,0,0,0)); tl.alpha_composite(top,(0,0)); top=tl.rotate(-c.get('hat_tilt',0),resample=Image.BICUBIC,center=(CX,180),translate=(TD//2,0))
    im.alpha_composite(top,(0,0)); top=None
    HAT=None
    if c.get('hat3d'):   # round 3: Rick-proportioned hat on a padded layer, composited last; every bit of hair above its brim is removed
        HAT,_by=X.hat3d_layer(c['hat3d'],c.get('hatcol',(80,60,44)),K,tilt=c.get('hat_tilt',0),dx=TD//2,col2=c.get('hatcol2'),top=PT,bottom=PB)
        HREG=X.hat_region(HAT); X.restore_under_hat(im,PRE,HREG.crop((0,PT,1024,PT+1024)))
    if c.get('fhair'): X.fhair(im,c['fhair'],c.get('fhaircol',c.get('hair',(60,40,30))),K,dx=TD)   # round 2: Rick facial hair (rule 326a revision pending owner pick)
    feat,d=new(1024,1024)
    FS=X.feat_scale(c)   # round 4 proposal: Rick-sized eyes / brows / mouth, opt-in per character ("feat_scale": "rick" or [eyes, brows, mouth])
    _gl=(tuple(c['glasses'])+(255,)) if c.get('glasses') else None; _bk=b if hat not in('cop','flatcap','fedora','beanie','ladyhat','leather','cloche','visor') or b!='up' else 'flat'
    if FS:
        X.scaled(feat,lambda dd: eyes(dd,e,glasses=_gl),X.EYE_BOXES,FS[0]); X.scaled(feat,lambda dd: brows(dd,_bk),X.BROW_BOXES,FS[1]); d=ImageDraw.Draw(feat)
    else:
        eyes(d,e,glasses=_gl); brows(d,_bk)
    MSIDE=X.mouth_side(c,ex)   # round 3: per-face mouthL/mouthR/lookL/lookR tokens override the character's mouth_side
    if FS:
        _ml,_md=new(1024,1024); X.scaled(_ml,lambda dd: mouth(dd,m),X.MOUTH_BOXES,FS[2]); feat.alpha_composite(X.mouth_set(_ml,m,MSIDE)); d=ImageDraw.Draw(feat)
    elif MSIDE: feat.alpha_composite(X.mouth_layer(mouth,m,MSIDE)); d=ImageDraw.Draw(feat)   # round 2: Rick's off-centre, lopsided mouths
    else: mouth(d,m)
    if c.get('mustache'):   # r8: Rick's bushy two-lobe mustache
        mc=tuple(c['mustache'])+(255,)
        for sx in(-1,1): d.ellipse([CX+sx*80-95,605,CX+sx*80+95,705],fill=mc,outline=K,width=12)
        d.ellipse([CX-70,610,CX+70,690],fill=mc)
    if c.get('stache_small'):   # r5 (owner Nov 22: the big beard read as weird): one slim rounded mustache, narrower than the mouth
        mc=tuple(c['stache_small'])+(255,); d.rounded_rectangle([CX-105,628,CX+105,672],22,fill=mc,outline=K,width=10)
    if c.get('stubble'):   # r5: light jaw shadow, no outline
        ov=Image.new('RGBA',(1024,1024),(0,0,0,0)); od=ImageDraw.Draw(ov); od.chord([CX-330,520,CX+330,860],0,180,fill=tuple(c['stubble'])+(42,)); feat.alpha_composite(ov); d=ImageDraw.Draw(feat)
    if c.get('beard'):
        bc=tuple(c['beard'])+(255,); d.chord([CX-300,560,CX+300,900],0,180,fill=bc,outline=K,width=12); d.chord([CX-90,640,CX+90,760],0,180,fill=(251,244,241,255))
    if c.get('nose',True): d.arc([CX-30,560,CX+30,640],-30,200,fill=K,width=10)
    extras(d,ex)
    im.alpha_composite(feat.crop((0,105,1024,1024)),(TD,0))
    HL=X.hair_layer(HD,hair,K,dx=TD//2,top=PT) if HD else None
    FL=X.fhair_layer(c['fhair'],c.get('fhaircol',c.get('hair',(60,40,30))),K,dx=TD,top=PT,bottom=PB) if c.get('fhair') else None
    TILT=X.head_tilt(c,ex)
    if not (PT or PB or HL or HAT or TILT): return im
    # round 3: final texture is 1024 x (PT+1024+PB); lib.char() sizes the face card to match (head stays in place)
    out=Image.new('RGBA',(1024,PT+1024+PB),(0,0,0,0)); out.alpha_composite(im,(0,PT))
    if FL is not None and PB: out.alpha_composite(FL.crop((0,PT+1024,1024,PT+1024+PB)),(0,PT+1024))
    if HL is not None:
        if HAT is not None: HL=X.erase_under_hat(HL,HREG,PT)
        out.alpha_composite(HL,(0,0))
    if HAT is not None: out.alpha_composite(HAT,(0,0))
    if TILT: out=out.rotate(TILT,resample=Image.BICUBIC,center=(512,PT+540))   # round 3: tiltL/tiltR tokens tip the whole head about its centre
    return out
# ---- round 3 (rule 193): Rick-style construction ----
# slim column garment (narrower than the head), long coat/robe to the shins, hard cel shadow on the left third,
# light rim on the right, ink detail (collar, placket, buttons, belt + buckle, hem band, fold lines),
# stick legs with small shoes; thin sleeves with a cuff and a small hand. Drawn at 2x and downsampled (clean edges).
SS=2; BOUT=20   # round 4: body outline as heavy as the head's (verifier: thin body outlines vs heads)
def lt(c,f=1.12): return tuple(min(255,int(v*f)) for v in c[:3])+(255,)
GB={'tall':(98,175,215),'short':(98,180,222),'round':(98,200,238)}   # r8b: one build for all (guide v1.3 x.3: torso 1.00 H, legs 1.25-1.3 H, total 3.2-3.35 H); kinds differ in width only   # top px, shoulder half-width, hem half-width
HEMY={'tall':545,'short':545,'round':545}   # r6det (rule 329, Rick f606/f771: torso ~1.05 H capsule): hem lower   # r8b: torso 430 px = 1.00 H (head 0.43 m), legs 528->1074 = 1.27 H   # r6 (round-5: legs 0.64-0.90 H, Rick 0.93-1.31): shorter torso, longer legs   # round 5 (B1/B2): torso ~0.86 H tall (H = head disc ~560 px), legs ~0.85 H visible
WK={'tall':0.86,'short':0.87,'round':0.84}   # r6det (rule 329, Rick f606: torso ~0.85-0.9 H wide): was 0.72-0.745
def _sil(kind):
    y0,w0,w1=GB[kind]; y1=HEMY[kind]; pts=[]
    k_=WK[kind]; w0=int(w0*k_); w1=int(w1*k_)   # r9 (RENDER_SPEC_v1.4 A: torso width 0.73-0.89 H): widths x0.72-0.745
    w1=int(w0*1.10); rr=int(0.36*2*w1)   # r6det (rule 329): Rick's bean is widest near the hem (pear), sides near-straight   # r6det (rule 329): near-straight sides like Rick's capsule torso (was hem x0.74 = egg)   # r6: hem narrower than the middle (Rick: widest at mid-torso)   # rounded bottom: corner radius >= 0.35 of the torso width (Rick bean)
    BG_=int(18*k_)   # r6det: small side bulge (was 62)
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
    LW=34   # r6det (rule 329, Rick legs 6-7.5 % H filled tubes): ink tube 34 px with a trouser fill inside
    for sx in(-1,1):
        x=400+sx*62; fx=x+sx*20+(sx*60 if stride else 0); lift=(70 if (stride==1 and sx<0) or (stride==2 and sx>0) else 0); fy=1056-lift
        y_0=y1-60; cx_=(x+fx)/2+sx*30; cy_=(y_0+fy)/2
        P=[((1-t)**2*x+2*(1-t)*t*cx_+t*t*fx,(1-t)**2*y_0+2*(1-t)*t*cy_+t*t*fy) for t in [i/24 for i in range(25)]]
        d.line(_S(P),fill=K,width=s(LW),joint='curve')
        d.line(_S(P),fill=legc,width=s(LW-16),joint='curve')   # r6det: filled tube (trouser colour) inside the ink
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
    elif cue=='jersey':   # det: plain 1930s wool jersey, number front, sleeve stripes; no logo
        st=tuple(c.get('stripe',(236,232,220)))+(255,)
        collar(dk(R,0.7),40); 
        for yy in (y0+70,y0+100): dd.line([0,s(yy),W,s(yy)],fill=st,width=s(14))
        from PIL import ImageFont as _IF
        f_=_IF.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',s(150)); dd.text((s(400),s(y0+250)),c.get('num','1'),font=f_,fill=(240,236,226,255),anchor='mm',stroke_width=s(6),stroke_fill=K)
        dd.rectangle([0,s(y1-110),W,s(y1-40)],fill=dk(tuple(c.get('legs'))+(255,),0.95)); dd.line([0,s(y1-110),W,s(y1-110)],fill=K,width=s(6))
        folds(2)
    elif cue=='hoodie':
        dd.polygon(_S([(400-150,y0-20),(400,y0+120),(400+150,y0-20)]),fill=dk(R,0.8)); dd.line(_S([(400-150,y0-20),(400,y0+120),(400+150,y0-20)]),fill=K,width=s(7))
        for sx in(-1,1): dd.line(_S([(400+sx*30,y0+110),(400+sx*36,y0+230)]),fill=(240,240,240,255),width=s(8))
        dd.rounded_rectangle([s(290),s(beltY+20),s(510),s(beltY+140)],s(20),fill=dk(R,0.86),outline=K,width=s(6))
        dd.rectangle([0,s(y1-60),W,s(y1+60)],fill=dk(R,0.7)); folds(2)
    elif cue=='sweater':
        collar(lt(R,1.1),40)
        for y in range(y0+90,y1-40,60):
            for x in range(240,580,60): dd.polygon(_S([(x,y),(x+22,y+22),(x,y+44),(x-22,y+22)]),fill=lt(R,1.18))
        dd.rectangle([0,s(y1-60),W,s(y1+60)],fill=dk(R,0.72)); folds(2)
    elif cue=='vest':
        dd.polygon(_S([(400-100,y0),(400+100,y0),(400+80,y1),(400-80,y1)]),fill=(240,238,232,255))
        for sx in(-1,1): dd.polygon(_S([(400+sx*100,y0-10),(400+sx*20,y0+260),(400+sx*20,y1),(400+sx*260,y1),(400+sx*260,y0-10)]),fill=dk(R,0.8),outline=K,width=s(7))
        for y in range(y0+80,y1,70): dd.line([0,s(y),s(380),s(y)],fill=K,width=s(4)); dd.line([s(420),s(y),W,s(y)],fill=K,width=s(4))
        folds(3)
    # clip detail to the garment, paste
    clip=Image.new('RGBA',(W,H),(0,0,0,0)); clip.paste(det,(0,0),Image.composite(det.split()[3],Image.new('L',(W,H),0),gm))
    im.alpha_composite(clip); d=ImageDraw.Draw(im)
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
    if prop=='paper': d.rectangle([60,640,340,860],fill=(238,232,214,255),outline=K,width=10); d.text((80,660),'BLACK\nFRIDAY',fill=K)
    if prop=='phone': d.rounded_rectangle([120,700,280,760],24,fill=(30,28,30,255),outline=K,width=8); d.ellipse([90,680,170,780],fill=(30,28,30,255),outline=K,width=8); d.ellipse([230,680,310,780],fill=(30,28,30,255),outline=K,width=8)
    if prop=='money': d.rectangle([110,720,300,820],fill=(140,180,120,255),outline=K,width=9); d.rectangle([120,740,290,800],outline=(80,120,70,255),width=6); d.ellipse([175,745,235,795],outline=(80,120,70,255),width=6); d.rectangle([180,720,220,820],fill=(240,236,220,255),outline=K,width=5)
    if prop=='marker': d.line([200,700,200,880],fill=(196,30,30,255),width=22); d.polygon([(190,880),(210,880),(200,900)],fill=K)
    if prop=='mic': d.line([200,720,200,880],fill=(60,60,66,255),width=14); d.rounded_rectangle([150,820,250,900],30,fill=(190,190,196,255),outline=K,width=8)
    if prop=='ball': d.ellipse([110,700,290,800],fill=(130,70,40,255),outline=K,width=10); d.line([150,750,250,750],fill=(240,236,226,255),width=8); [d.line([x,738,x,762],fill=(240,236,226,255),width=6) for x in (170,190,210,230)]
    if prop=='hotdog': d.rounded_rectangle([100,720,300,780],30,fill=(220,170,100,255),outline=K,width=9); d.rounded_rectangle([90,735,310,765],15,fill=(170,70,50,255),outline=K,width=6); d.line([110,750,290,750],fill=(240,200,40,255),width=6)
    if prop=='fork': d.line([200,700,200,860],fill=(190,190,196,255),width=12); [d.line([x,860,x,900],fill=(190,190,196,255),width=7) for x in (186,200,214)]
    if prop=='plate': d.ellipse([60,730,340,810],fill=(246,244,236,255),outline=K,width=9); d.ellipse([130,735,270,785],fill=(200,140,70,255),outline=K,width=6)
    if prop=='plug': d.line([200,720,200,860],fill=(30,30,30,255),width=12); d.rectangle([186,820,214,890],fill=(200,170,80,255),outline=K,width=6)
    if prop=='sign': d.rectangle([40,620,360,860],fill=(250,240,200,255),outline=K,width=12); d.text((200,740),'SOLD OUT',fill=(190,30,30,255),anchor='mm')
    if prop=='remote': d.rounded_rectangle([170,690,230,880],18,fill=(40,40,44,255),outline=K,width=8); [d.ellipse([190,y,210,y+20],fill=(200,60,60,255)) for y in (720,760,800)]
    if prop=='drumstick': d.ellipse([110,720,260,840],fill=(190,110,50,255),outline=K,width=9); d.line([240,820,300,880],fill=(246,240,226,255),width=22); d.ellipse([285,862,320,897],fill=(246,240,226,255),outline=K,width=5)
    if prop in ('box','bag','paper','megaphone','camera','phone','money','ball','hotdog','plate','sign','remote','drumstick'): mitt()   # the mitten sits over the prop so it is held, not floating
    return noodle(im,BEND.get(prop,18) if straight is None else straight)
# r7 (owner Nov 19: forearms stuck out sideways and swung across faces): natural hang 18 deg; 'armS' = straight card for raised and gripping arms
BEND={'phone':30,'money':20,'marker':25,'mic':25,'ball':25,'hotdog':20,'fork':25,'plate':25,'plug':25,'sign':0,'remote':25,'drumstick':25,'pennant':0,'megaphone':15,'paper':20,'bag':20,'box':25,'camera':25,'chalk':30,'pen':30,'redpen':30}
AW=52   # r6det (rule 329, Rick arms 5.5-6 % H): was 38
def noodle(hand,deg,ey=330):
    # the hand (with its prop) swings outward by deg about a point 330 px down; the arm is one quadratic curve from the shoulder to the hand
    W,H=hand.size; out=Image.new('RGBA',(W*3,H),(0,0,0,0)); X=W*3//2
    lay=Image.new('RGBA',(W*3,H),(0,0,0,0)); lay.paste(hand,(W,0),hand)
    if deg: lay=lay.rotate(deg,resample=Image.BICUBIC,center=(X,ey))   # PIL rotates counter-clockwise: the hand swings to +x (outward)
    a=math.radians(deg); hx=X+(712-ey)*math.sin(a); hy=ey+(712-ey)*math.cos(a)
    sx0,sy0=X,40; cxp,cyp=X,(sy0+hy)/2+40   # control point straight below the shoulder: leaves the shoulder down, bends smoothly into the hand
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
def pose_arm(name,pose,mix=1.0,over=0.0,frm='hang'):
    """1200 x 1800 card, shoulder at (600,900): the pose (or a mix toward it from `frm` for in-betweens, `over` degrees of overshoot)"""
    a0,c0=POSES[frm]; a1,c1=POSES[pose]
    a=a0+(a1-a0)*mix+over*(1 if a1>=a0 else -1); cc=c0+(c1-c0)*mix+over*(1 if c1>=c0 else -1)
    U,F=330,372   # upper arm and forearm (same total reach as noodle(): hand centre 712 px from the shoulder at y=40)
    sx0,sy0=600,900
    ex_=sx0+U*math.sin(math.radians(a)); ey_=sy0+U*math.cos(math.radians(a))
    hx=ex_+F*math.sin(math.radians(cc)); hy=ey_+F*math.cos(math.radians(cc))
    # rounded elbow: quadratic through points pulled 28 % in from the elbow on each segment, straight segments elsewhere
    def lerp(p,q,t): return (p[0]+(q[0]-p[0])*t,p[1]+(q[1]-p[1])*t)
    S,E,H=(sx0,sy0),(ex_,ey_),(hx,hy); P1=lerp(E,S,0.28); P2=lerp(E,H,0.28)
    pts=[lerp(S,P1,i/12) for i in range(13)]+[((1-t)**2*P1[0]+2*(1-t)*t*E[0]+t*t*P2[0],(1-t)**2*P1[1]+2*(1-t)*t*E[1]+t*t*P2[1]) for t in [i/16 for i in range(1,17)]]+[lerp(P2,H,i/12) for i in range(1,13)]
    W,Hh=1200,1800; big=Image.new('RGBA',(W*SS,Hh*SS),(0,0,0,0)); bd=ImageDraw.Draw(big)
    bd.line([(x*SS,y*SS) for x,y in pts],fill=K,width=AW*SS,joint='curve')
    for x,y in (pts[0],): bd.ellipse([(x-AW/2)*SS,(y-AW/2)*SS,(x+AW/2)*SS,(y+AW/2)*SS],fill=K)
    bd.ellipse([(hx-50)*SS,(hy-50)*SS,(hx+50)*SS,(hy+50)*SS],fill=K)   # mitten 100 px, as arm()
    return big.resize((W,Hh),Image.LANCZOS)
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
if __name__=='__main__':
    out={}
    for n,c in C.items():
        for fk in c['faces']: head(n,fk).save(f'{T}{n}_h_{fk}.png')
        body(n).save(f'{T}{n}_body.png'); body(n,1).save(f'{T}{n}_bodyw1.png'); body(n,2).save(f'{T}{n}_bodyw2.png')
        for p in c.get('props',[None]): arm(n,p).save(f'{T}{n}_arm{"_"+p if p else ""}.png')
        arm(n).save(f'{T}{n}_arm.png'); arm(n,straight=4).save(f'{T}{n}_armS.png')
        if c.get('combos') or c.get('combos_approved'):   # round 6 (opt-in): split torso/legs cards for lib.combo()
            _t,_l=split_body(n); _t.save(f'{T}{n}_btop.png'); _l.save(f'{T}{n}_blegs.png')
            for _s in (1,2): split_body(n,_s)[1].save(f'{T}{n}_blegsw{_s}.png')
        for _p in pose_list(c):   # round 5 proposal (opt-in "poses"): pose card, 1-frame in-between from rest, overshoot for settles
            pose_arm(n,_p).save(f'{T}{n}_arm_pose_{_p}.png'); pose_arm(n,_p,mix=0.5).save(f'{T}{n}_arm_pose_{_p}_m.png'); pose_arm(n,_p,over=9).save(f'{T}{n}_arm_pose_{_p}_o.png')
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
    pv.convert('RGB').save('/root/det/cast_preview.jpg')
    faces=[]
    for n,c in C.items():
        for fk in c['faces']: faces.append(Image.open(f'{T}{n}_h_{fk}.png').resize((128,128)))
    sh=Image.new('RGBA',(128*16,128*((len(faces)+15)//16)),(236,230,218,255))
    for i,f in enumerate(faces): sh.alpha_composite(f,((i%16)*128,(i//16)*128))
    sh.convert('RGB').save('/root/det/faces_sheet.jpg'); print('CAST_OK',len(faces),'faces')
