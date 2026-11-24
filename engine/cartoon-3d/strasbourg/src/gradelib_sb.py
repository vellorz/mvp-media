# Strasbourg grade library (from Cape Cod post_cc.py r6d: same apply/finish/floor/solve chain, SKMAX 1.0 and the warm-colour protect on every shot per rules 355/369).
# Imported by post_sb.py and gradeprobe_sb.py. Shot table = scene_sb.py SH.
import os, numpy as np, cv2
K=float(os.environ.get('GRADE_K','1.0'))
END=2040
SH={'S01':(0,130),'S02':(123,255),'S03':(248,355),'S04':(348,421),'S05':(414,514),'S06':(507,565),'S07':(558,710),'S08':(703,800),
    'S09':(793,852),'S10':(853,943),'S11':(936,1003),'S12':(996,1148),'S13':(1141,1259),'S14':(1252,1312),'S15':(1305,1405),
    'S16':(1398,1443),'S17':(1444,1531),'S18':(1524,1654),'S19':(1647,1768),'S20':(1769,1825),'S21':(1818,1927),'S22':(1920,END)}
# palette per era/mood (R,G,B multipliers); base values, then gradeprobe_sb.py trims R/B per shot so graded faces sit in rule 355's band
# 1570 day square: low winter sun, slightly warm; snow: cooler; nave/council/rooms: candle-warm; today's night market: bulb-warm, trimmed cooler for skin
TINT={'S01':(1.02,1.0,0.97),'S02':(1.02,1.0,0.97),'S03':(1.02,1.0,0.97),'S04':(1.02,1.0,0.97),'S05':(1.0,1.0,1.0),'S06':(1.02,1.0,0.98),'S07':(1.02,1.0,0.98),
      'S08':(1.02,1.0,0.98),'S09':(1.02,1.0,0.98),'S10':(1.02,1.0,0.97),'S11':(1.02,1.0,0.97),'S12':(1.02,1.0,0.97),'S13':(0.99,1.0,1.02),'S14':(1.0,1.0,1.0),
      'S15':(1.0,1.0,1.0),'S16':(0.99,1.0,1.02),'S17':(0.99,1.0,1.02),'S18':(1.0,1.0,1.0),'S19':(1.0,1.0,1.0),'S20':(0.98,1.0,1.03),'S21':(0.98,1.0,1.03),'S22':(1.0,1.0,1.0)}
LT={'S01':0.50,'S02':0.50,'S03':0.48,'S04':0.48,'S05':0.46,'S06':0.40,'S07':0.44,'S08':0.44,'S09':0.46,'S10':0.48,'S11':0.48,'S12':0.48,
    'S13':0.50,'S14':0.42,'S15':0.42,'S16':0.50,'S17':0.50,'S18':0.44,'S19':0.44,'S20':0.36,'S21':0.38,'S22':0.42}
INTR=('S06','S07','S08','S09','S14','S15','S18','S19')
VIG={n:(0.70 if n in INTR else 0.10) for n in SH}
TINT.update({k:tuple(v) for k,v in {"S01": [1.02, 1.0, 1.0408], "S02": [1.02, 1.0, 1.0486], "S03": [1.02, 1.0, 1.0778], "S04": [1.02, 1.0, 1.075], "S05": [1.0, 0.9369, 1.0], "S06": [1.02, 1.0, 1.0322], "S07": [1.02, 0.9514, 0.98], "S08": [1.02, 0.9664, 0.98], "S09": [1.02, 1.0, 0.98], "S10": [1.02, 0.9489, 0.97], "S11": [1.02, 0.9524, 0.97], "S12": [1.02, 1.0557, 1.1243], "S13": [0.99, 1.0, 1.02], "S14": [1.0, 1.0, 1.0], "S15": [1.0, 0.9654, 1.0], "S16": [0.99, 1.0, 1.02], "S17": [0.99, 1.0, 1.02], "S18": [1.0, 1.0, 1.0], "S19": [1.0, 1.0, 1.0], "S20": [0.98, 1.0, 1.22], "S21": [0.98, 1.0, 1.099], "S22": [1.0, 0.9634, 1.0]}.items()})   # gradeprobe_sb v5g3 (S01-S19) + v5h (S20-S22): every shot's graded faces in rule 355's band
BLOOM=0.0
_VM={}
def bloom(x,amt=BLOOM):
    h,w=x.shape[:2]; sm=cv2.resize(x,(w//4,h//4),interpolation=cv2.INTER_AREA); Y=gray(sm)
    m=np.clip((Y-0.80)/0.2,0,1)[...,None]*sm
    g=cv2.GaussianBlur(m,(0,0),10*K)+cv2.GaussianBlur(m,(0,0),28*K)
    g=cv2.resize(g,(w,h),interpolation=cv2.INTER_LINEAR); return np.clip(x+amt*g*(1-x),0,1)
HIFLOOR=('S19',)
def hifloor(x,target=0.88,gmax=1.28):
    """r7: per-frame highlight floor. Round 6 measured p98 0.73-0.80 over 1548-1751 (R19 needs >= 0.84): lift by gain to p98 target, soft knee above 0.9"""
    Y=gray(x[::6,::6]); p=float(np.percentile(Y,98))
    if p>=target: return x
    g=min(gmax,target/max(p,1e-3)); z=x*g; k=0.9
    return np.where(z>k,k+(z-k)/(1+(z-k)/0.1),z).astype(np.float32)
def vratio(x):  # verifier metric: 4 corner patches (15%W x 10%H) / centre patch (40%W x 30%H)
    h,w=x.shape[:2]; Y=gray(x); cw,ch=int(w*0.15),int(h*0.10)
    c=np.mean([Y[:ch,:cw].mean(),Y[:ch,-cw:].mean(),Y[-ch:,:cw].mean(),Y[-ch:,-cw:].mean()])
    m=Y[int(h*0.35):int(h*0.65),int(w*0.3):int(w*0.7)].mean(); return c/max(m,1e-4)
_VM={}
def vig(x,k):
    h,w=x.shape[:2]; key=(h,w,k)
    if key not in _VM:
        yy,xx=np.mgrid[0:h,0:w].astype(np.float32); r=np.sqrt(((xx-(w-1)/2)/(w/2))**2+((yy-(h-1)/2)/(h/2))**2)/np.sqrt(2)
        t=np.clip((r-0.25)/0.75,0,1); _VM[key]=(1-k*t*t*(3-2*t))[...,None].astype(np.float32)
    return x*_VM[key]
def gray(x): return x[...,0]*0.299+x[...,1]*0.587+x[...,2]*0.114
def hsv_s(x):
    mx=x.max(-1); mn=x.min(-1); return np.where(mx>1e-4,(mx-mn)/np.maximum(mx,1e-4),0)
def apply(x,p):
    lo,hi,g,sat,tint=p
    y=gray(x); yn=np.clip((y-lo)/(hi-lo),0,1); y2=0.055+0.925*yn**g
    r=(y2/np.maximum(y,1e-4))[...,None]; z=np.clip(x*r,0,1)
    y3=gray(z)[...,None]
    # r4b (visual r4 critical: S10 Nauset and S01 Pilgrim skin went orange under satk 2.4): skin-hued pixels (R>G>B, warm hue, mid saturation, lit) keep at most SKMAX saturation gain
    mx=x.max(-1); mn=x.min(-1); hs=(mx-mn)/np.maximum(mx,1e-4); hue=(x[...,1]-x[...,2])/np.maximum(mx-mn,1e-4)
    skin=((x[...,0]>=x[...,1])&(x[...,1]>=x[...,2]-0.02)&(hs>0.14)&(hs<0.55)&(hue>0.22)&(hue<0.58)&(y>0.22)).astype(np.float32)
    skin=cv2.GaussianBlur(skin,(0,0),2.0)[...,None]; sk=np.minimum(sat,SKMAX)*skin+sat*(1-skin)
    if PROT[0] and sat>1:   # r6b (visual r6 critical: S10 Nauset deerskin mantles 163,103,62 went traffic-cone orange 222,88,0 and the face rim speckled once the narrowed skin mask left them out): warm pixels that are already saturated get little of the gain, low-sat sand still gets all of it
        warm=np.clip((hue[...,None]+0.1)/0.2,0,1)*np.clip((0.75-hue[...,None])/0.15,0,1)*(x[...,:1]>=x[...,2:3])
        keep=np.clip((0.62-hs[...,None])/0.32,0,1); sk=sk*(1-warm)+(1+(sk-1)*keep)*warm
    z=np.clip(y3+sk*(z-y3),0,1); z=np.clip(z*np.array(tint,np.float32),0,1); return z
SKMAX=1.0
SATPROT=set(os.environ.get('SATPROT','S10').split(','))   # r6b: shots graded with the saturated-warm protect (only S10 re-posted in round 6b; apply to every shot from the next video on)
PROT=[False]
CLAR=0.55; CLS=14.0; PLUM=np.array([46,28,54],np.float32)/255   # r4 (visual L6 0.361 > 0.35 and halos at f60/f1720): weaker, tighter local contrast (r3 was 0.8 / 24 px)
def finish(o):
    y=gray(o)[...,None]; mid=np.clip(4*y*(1-y),0,1)   # r3: local contrast on midtones only (r2 crushed ink and coats to RGB 0)
    return np.clip(o+CLAR*mid*(o-cv2.GaussianBlur(o,(0,0),CLS*K)),0,1)
def floor_(o):
    y=gray(o)[...,None]
    # rule 308: dark saturated crimson ink (S03/S06/S11/S15 at ~(100,24,44)) pulled to Rick's dull plum
    mx=o.max(-1,keepdims=True); mn=o.min(-1,keepdims=True); sat=(mx-mn)/np.maximum(mx,1e-4)
    line=np.clip((0.75*cv2.GaussianBlur(y[...,0],(0,0),5*K)[...,None]-y)/0.05,0,1)   # thin ink lines only (darker than their surroundings), not smooth wood shadow
    red=np.clip((o[...,:1]-np.maximum(o[...,1:2],o[...,2:3]))/0.12,0,1)*np.clip((sat-0.45)/0.2,0,1)*np.clip((0.40-y)/0.12,0,1)*np.maximum(line,np.clip((sat-0.6)/0.1,0,1)*np.clip((0.22-y)/0.08,0,1))   # r6: deep crimson fills (S03/S11 at sat 0.67-0.73, verifier r5) count even when not thin lines. r4b: rule 308 still crimson in S03/S06/S11/S15 (sat 0.61-0.74): reach brighter line pixels
    o=o*(1-0.85*red)+(PLUM*1.15)*0.85*red
    y=gray(o)[...,None]; w=np.clip((0.24-y)/0.14,0,1)*0.85   # darks go to Rick's plum (46,28,54); floor about luma 0.12, never black
    return np.clip(o*(1-w)+PLUM*w,0,1)
def solve(samples,tint,lt=0.45,vk=0.0):
    allY=np.concatenate([gray(s).ravel() for s in samples]); lo,hi=np.percentile(allY,0.8),np.percentile(allY,99.6)
    best=None
    for g in np.linspace(0.55,1.6,22):
        for sat in np.linspace(0.8,2.4,17):
            p=(lo,hi,g,sat,tint); o=[vig(apply(s,p),vk) for s in samples]; Y=np.concatenate([gray(q).ravel() for q in o])
            m=Y.mean(); S_=np.mean([hsv_s(q).mean() for q in o]); p2,p98=np.percentile(Y,2),np.percentile(Y,98)
            cost=abs(m-lt)+abs(S_-0.52)+max(0,0.07-p2)*4+max(0,0.86-p98)*4
            if best is None or cost<best[0]: best=(cost,p,round(float(m),3),round(float(S_),3),round(float(p2),3),round(float(p98),3))
    return best
# ---- captions ----
FONT='/home/user/mvp-media/engine/cartoon-3d/project/public/havasu/fonts/Montserrat.ttf'
PROT[0]=True   # rule 369: warm saturated colour protect on every shot from the next video on
