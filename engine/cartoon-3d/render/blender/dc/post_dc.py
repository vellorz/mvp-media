# Washington DC (thu-washington-dc) post, from the Cape Cod / BF post.py. Post: per-shot grade (rule 187 window) -> dissolves (smoothstep, varied lengths) -> captions on top (rule 186) -> encode with the mix.
# python3 post.py SRC OUT.mp4 [scale]     SRC holds <shot>_<first>_.mp4 clips (PC encode) or <shot>/f_####.png folders
import sys, os, glob, json, subprocess, numpy as np, re, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRC,OUT=sys.argv[1],sys.argv[2]; K=float(sys.argv[3]) if len(sys.argv)>3 else 1.0
W,H=int(1440*K),int(2560*K)
SH={k:tuple(v) for k,v in json.load(open('/root/dc/bridge/shots.json')).items()}; END=max(b for a,b in SH.values())
# palette per place/mood (multipliers R,G,B): flips across each place/time join (rule 187). Philadelphia office warm, Washington mail room cool, the President's office neutral-cool,
# print room warm-red, night shots blue-violet, autumn street amber, hall warm, today neutral-bright
TINT={'S01':(1.04,1.0,0.94),'S02':(0.98,1.0,1.03),'S03':(0.97,1.0,1.04),'S04':(0.97,1.0,1.04),'S05':(0.97,1.0,1.04),'S06':(1.06,0.99,0.92),
      'S07':(1.04,1.0,0.94),'S08':(1.04,1.0,0.94),'S09':(1.06,0.99,0.92),'S10':(1.04,1.0,0.94),'S11':(0.99,1.0,1.02),'S12':(0.93,0.96,1.08),
      'S13':(0.95,0.96,1.07),'S14':(1.02,0.98,0.98),'S15':(1.0,0.98,1.0),'S16':(1.07,1.0,0.88),'S17':(1.0,1.0,1.01),'S18':(1.0,1.0,1.01),
      'S19':(1.05,1.0,0.93),'S20':(1.01,1.0,0.99),'S21':(1.01,1.0,0.99)}
# per-shot brightness targets: day rooms bright, night shots darker (Rick's film swings 0.2-0.7 across scenes)
LT={'S01':0.50,'S02':0.50,'S03':0.50,'S04':0.50,'S05':0.48,'S06':0.46,'S07':0.52,'S08':0.50,'S09':0.46,'S10':0.48,'S11':0.48,'S12':0.36,
    'S13':0.38,'S14':0.42,'S15':0.42,'S16':0.50,'S17':0.50,'S18':0.50,'S19':0.50,'S20':0.54,'S21':0.54}
PAY0,PAY1=2030,2054; PAYP=(0.0,1.0,1.0,1.0,(1.03,0.99,1.0))   # S21 payoff grade, eased in while the camera lands on the poster
INTR=('S06','S09','S12','S13','S14','S19')
# vignette strength (corner multiplier = 1-k): interiors get Rick's lantern falloff, exteriors a light one
PAY0,PAY1=1778,1793; PAYP=(0.0,1.0,1.0,1.0,(1.03,0.99,1.0))   # S19 payoff grade (poster <1% clipped, luma ~143 vs file 117)
VIG={n:(0.70 if n in INTR else 0.10) for n in SH}   # start values; interiors are calibrated per shot below to corner/centre 0.38 (guide 0.33-0.42); day exteriors light only
BLOOM=0.0   # light glow on emitters (lamps, screens, lit windows): guide L8
def bloom(x,amt=BLOOM):
    h,w=x.shape[:2]; sm=cv2.resize(x,(w//4,h//4),interpolation=cv2.INTER_AREA); Y=gray(sm)
    m=np.clip((Y-0.80)/0.2,0,1)[...,None]*sm
    g=cv2.GaussianBlur(m,(0,0),10*K)+cv2.GaussianBlur(m,(0,0),28*K)
    g=cv2.resize(g,(w,h),interpolation=cv2.INTER_LINEAR); return np.clip(x+amt*g*(1-x),0,1)
HIFLOOR=('S21',)
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
class Reader:
    def __init__(s,shot):
        a,b=SH[shot]; s.a=a; s.n=b-a+1; s.i=0
        mp=sorted(glob.glob(f'{SRC}/{shot}_*.mp4')); s.png=None
        if mp:
            lst=f'/tmp/{shot}_list.txt'; open(lst,'w').write(''.join(f"file '{os.path.abspath(m)}'\n" for m in mp))
            s.p=subprocess.Popen(['ffmpeg','-v','error','-f','concat','-safe','0','-i',lst,'-vf',f'scale={W}:{H}:flags=lanczos','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
        else: s.png=sorted(glob.glob(f'{SRC}/{shot}/f_*.png'))
    def next(s):
        s.i+=1
        if s.png is not None:
            im=Image.open(s.png[s.i-1]).convert('RGB')
            if im.size!=(W,H): im=im.resize((W,H),Image.LANCZOS)
            return np.asarray(im,np.float32)/255
        b=s.p.stdout.read(W*H*3); return np.frombuffer(b,np.uint8).reshape(H,W,3).astype(np.float32)/255
def gray(x): return x[...,0]*0.299+x[...,1]*0.587+x[...,2]*0.114
def hsv_s(x):
    mx=x.max(-1); mn=x.min(-1); return np.where(mx>1e-4,(mx-mn)/np.maximum(mx,1e-4),0)
def apply(x,p):
    lo,hi,g,sat,tint=p
    y=gray(x); yn=np.clip((y-lo)/(hi-lo),0,1); y2=0.055+0.925*yn**g
    r=(y2/np.maximum(y,1e-4))[...,None]; z=np.clip(x*r,0,1)
    y3=gray(z)[...,None]; z=np.clip(y3+sat*(z-y3),0,1); z=np.clip(z*np.array(tint,np.float32),0,1); return z
CLAR=0.8; CLS=24.0; PLUM=np.array([46,28,54],np.float32)/255   # r2 (visual verifier L5/R20: edge density 22.9 % vs >= 28 %): painted-surface local contrast, sigma 24 px at 2K
def finish(o):
    y=gray(o)[...,None]; mid=np.clip(4*y*(1-y),0,1)   # r3: local contrast on midtones only (r2 crushed ink and coats to RGB 0)
    o=np.clip(o+CLAR*mid*(o-cv2.GaussianBlur(o,(0,0),CLS*K)),0,1)
    y=gray(o)[...,None]; w=np.clip((0.22-y)/0.14,0,1)*0.75   # r3 (rule 308 / R19): darks go to Rick's dull plum ink (46,28,54), floor about luma 0.12, never black
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
def font(px):
    f=ImageFont.truetype(FONT,px); f.set_variation_by_name('Black'); return f
CAP=72*K; fs=int(100*K)
for _ in range(30):
    f=font(fs); bb=f.getbbox('H'); ch=bb[3]-bb[1]
    if abs(ch-CAP)<1: break
    fs=int(round(fs*CAP/ch))
FNT=font(fs); BASE=int(0.717*H); STROKE=max(1,int(round(7*K))); SHX,SHY=int(round(4*K)),int(round(5*K))
WORDS=json.load(open('/root/dc/vo/vo_trim.wav.words.json'))
def fixwords(W_):
    """caption text follows script.md, not ASR spelling: quote marks on the clerk's line"""
    MERGE=[]
    SUB={'Oh':'\u201cOh'}
    o=[]; i=0
    while i<len(W_):
        hit=False
        for src,dst in MERGE:
            if [w[0].strip() for w in W_[i:i+len(src)]]==src:
                s0,e0=W_[i][1],W_[i+len(src)-1][2]
                if len(dst)==1: o.append([dst[0],s0,e0])
                else: o.append([dst[0],W_[i][1],W_[i][2]]); o.append([dst[1],W_[i+1][1],W_[i+len(src)-1][2]])
                i+=len(src); hit=True; break
        if hit: continue
        w,s_,e=W_[i]; t=w.strip(); t=SUB.get(t,t)
        if t=='again.' and o and o[-1][0]=='lady': t='again.\u201d'
        o.append([t,s_,e]); i+=1
    return o
WORDS=fixwords(WORDS)
def chunks():
    out=[]; cur=[]
    for i,(w,s,e) in enumerate(WORDS):
        cur.append((w,s,e)); punct=w.strip()[-1] in ',.?!'
        nxt=WORDS[i+1][1] if i+1<len(WORDS) else e+0.4
        dur=(nxt-cur[0][1])*30
        if punct or len(cur)==2 or dur>=5 or (len(cur)==2 and len(''.join(x[0] for x in cur))>6):   # round 5 (T1-T3): 1-2 words per card, 162 cards, mean 0.36 s, P90 0.54 s
            out.append(cur); cur=[]
    if cur: out.append(cur)
    C=[]
    for c in out:
        txt=' '.join(x[0].strip() for x in c).replace('Army Navy','Army-Navy').replace('  ',' ')
        C.append([int((c[0][1]+0.1)*30),txt])   # r9 (rule 9/186 revised: on the word or 0-1 f before, never later than +2): floor of the audible onset frame (round 7 ran 1.7-3.1 f early)
    C[0][0]=0   # the hook frame carries its caption from f0
    for i in range(len(C)): C[i].append(C[i+1][0] if i+1<len(C) else END+1)
    return C
CAPS=chunks()
DWMAX=17   # r2 (text verifier: dwell mean 0.374 s / P90 0.663 s vs Rick 0.32-0.35 / 0.53-0.57): a card leaves after at most 17 f (0.57 s); a gap shows no caption until the next word
CAPS=[[a,t,min(b,a+DWMAX)] for a,t,b in CAPS]
def cap_layer(txt):
    l,t,r,b=FNT.getbbox(txt,anchor='ls',stroke_width=STROKE); w=r-l
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); sh=Image.new('RGBA',(W,H),(0,0,0,0))
    x=(W-w)//2-l; ImageDraw.Draw(sh).text((x+SHX,BASE+SHY),txt,font=FNT,fill=(0,0,0,150),anchor='ls',stroke_width=STROKE,stroke_fill=(0,0,0,150))
    sh=sh.filter(ImageFilter.GaussianBlur(2*K)); lay.alpha_composite(sh)
    ImageDraw.Draw(lay).text((x,BASE),txt,font=FNT,fill=(255,255,255,255),anchor='ls',stroke_width=STROKE,stroke_fill=(0,0,0,255))
    return lay,w/W
PQ=json.load(open('/root/dc/bridge/posterquad.json'))
_PF=np.asarray(Image.open('/root/dc/poster_2k.png').convert('RGB')).astype(np.float32)/255.0
def truepost(o,q,k=0.96):
    h,w=o.shape[:2]; ph,pw=_PF.shape[:2]
    src=np.float32([[0,ph],[pw,ph],[pw,0],[0,0]]); dst=np.float32([[x*w,(1-y)*h] for x,y in q])
    Mx=cv2.getPerspectiveTransform(src,dst)
    wf=cv2.warpPerspective(_PF,Mx,(w,h),flags=cv2.INTER_AREA if (dst[1][0]-dst[0][0])<pw else cv2.INTER_LINEAR)
    m=cv2.warpPerspective(np.ones((ph,pw),np.float32),Mx,(w,h)); m=cv2.GaussianBlur(m,(0,0),0.8*K)[...,None]
    return o*(1-m)+np.clip(wf*k,0,1)*m
if __name__=='__main__':
    # grade params per shot from 5 sampled frames
    P={}; rep={}
    for n in SH:
        rd=Reader(n); idx=set(np.linspace(0,rd.n-1,5).astype(int)); smp=[]
        for i in range(rd.n):
            fr=rd.next()
            if i in idx: smp.append(fr[::8,::8])
        b=solve(smp,TINT[n],LT[n],VIG[n])
        if n in INTR:
            lo_,hi_=0.0,0.9
            for _ in range(14):
                k=(lo_+hi_)/2; r=np.mean([vratio(vig(apply(q,b[1]),k)) for q in smp])
                if r>0.38: lo_=k
                else: hi_=k
            VIG[n]=round((lo_+hi_)/2,3); b=solve(smp,TINT[n],LT[n],VIG[n])
        P[n]=b[1]; rep[n]=dict(mean=b[2],sat=b[3],p2=b[4],p98=b[5],gamma=round(float(b[1][2]),2),satk=round(float(b[1][3]),2),vig=VIG[n],vratio=round(float(np.mean([vratio(vig(apply(q,b[1]),VIG[n])) for q in smp])),3)); print('GRADE',n,rep[n],flush=True)
    json.dump({'grade':rep,'payoff_grade':dict(from_frame=PAY0,full_at=PAY1,params=PAYP[:4]),'captions':CAPS,'font_px':fs},open(OUT+'.post.json','w'),indent=1,default=str)
    widths=[]
    R={n:Reader(n) for n in SH}; cache={}
    enc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-','-i','/root/dc/audio/mix.wav',
        '-c:v','libx264','-preset','slow','-crf','14' if K==1 else '20','-pix_fmt','yuv420p','-c:a','aac','-b:a','320k','-shortest','-movflags','+faststart',OUT],stdin=subprocess.PIPE)
    ci=0; capimg=None; capkey=None
    for f in range(END+1):
        act=[n for n,(a,b) in SH.items() if a<=f<=b]
        frames={}
        for n in act:
            raw=R[n].next(); o=finish(apply(raw,P[n]))
            if n=='S21' and f>=PAY0:   # payoff close-up: protect the poster's real colours (no highlight stretch, gentle gamma)
                q=apply(raw,PAYP); q=np.clip(q+0.7*(q-cv2.GaussianBlur(q,(0,0),1.4*K)),0,1);   # round 4: poster read soft (38 % of file sharpness): gentle unsharp on the payoff
                t=min(1.0,(f-PAY0+1)/(PAY1-PAY0+1)); t=t*t*(3-2*t); o=o*(1-t)+q*t
            if n in HIFLOOR: o=hifloor(o)   # r7 (rule 274): bright ending and S11 highlights (p98 >= 0.86 before the poster's true colours go on)
            if n=='S21' and str(f) in PQ: o=truepost(o,PQ[str(f)])   # r5 (rule 196, round-4 E5 note): the shop file's true colours on the projected poster quad
            frames[n]=vig(bloom(o,BLOOM),VIG[n])
        if len(act)==1: img=frames[act[0]]
        else:
            A,B=act[0],act[1]; s0,e0=SH[B][0],SH[A][1]; t=(f-s0+1)/(e0-s0+2); w_=t*t*(3-2*t); img=frames[A]*(1-w_)+frames[B]*w_
        im=Image.fromarray((img*255+0.5).astype(np.uint8)).convert('RGBA')
        cur=[c for c in CAPS if c[0]<=f<c[2]]
        if cur:
            if capkey!=cur[0][1]: capimg,wd=cap_layer(cur[0][1]); capkey=cur[0][1]; widths.append(wd)
            im.alpha_composite(capimg)
        enc.stdin.write(np.asarray(im.convert('RGB')).tobytes())
        if f%100==0: print('POST',f,flush=True)
    enc.stdin.close(); enc.wait()
    print('CAPTION_WIDTH_MED',round(float(np.median(widths))*100,1),'MAX',round(float(max(widths))*100,1),'N',len(CAPS))
    print('POST_DONE',OUT)
