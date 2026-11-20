import re
# Black Friday short: Blender builder.  blender -b --python scene.py      (writes /root/bf/blend/bf.blend)
import sys, os, math, random, json
sys.path.insert(0,'/root/bf/src')
import bpy
from mathutils import Vector
import lib as L
from lib import box,cyl,sph,plane,flat,surf,card_mat,lin,vis,kloc,krot,kscale,empty,cam,path,char,face,faces,arm,bob,walk,finish,lipsync
END=1752
sc=L.init(END); R=random.Random(11)
WORDS=json.load(open('/mnt/project-files/modern-vista-social/experiments/2026-11-18_rick-99-test/audio/vo_trim.wav.words.json'))
SH={'S01':(0,170),'S02':(163,297),'S03':(292,432),'S04':(426,528),'S05':(520,652),'S06':(643,781),'S07':(775,866),'S08':(867,938),
    'S09':(931,1013),'S10':(1008,1057),'S11':(1051,1125),'S12':(1114,1218),'S13':(1210,1359),'S14':(1352,1487),'S15':(1481,1565),'S16':(1556,END)}
sc['shots']=json.dumps(SH)
LENS={'S01':30,'S02':28,'S03':33.5,'S04':30,'S05':31.5,'S06':37,'S07':28,'S08':28,'S09':26,'S10':40,'S11':36,'S12':42,'S13':38,'S14':34,'S15':34,'S16':30}
FSTOP={k:max(9.0,v*6.0) for k,v in {'S01': 2.8, 'S02': 11.2, 'S03': 2.4, 'S04': 2.8, 'S05': 1.8, 'S06': 1.8, 'S07': 1.8, 'S08': 2.4, 'S09': 1.8, 'S10': 3.2, 'S11': 1.8, 'S12': 1.8, 'S13': 4.4, 'S14': 2.0, 'S15': 1.8, 'S16': 3.2}.items()}   # r6: round-5 measure showed DOF blur, not missing paint, kept set detail at 18 vs Rick 75+ (no-DOF test: 89). Sets stay sharp like Rick's newest videos
for n in SH: cam(n,LENS[n],FSTOP[n])
STAGE=os.environ.get('STAGE','all')
# ======================= shared props =======================
INK=flat('inkc',lin((30,24,22)),0.9)
CHROME=flat('chrome',(0.75,0.75,0.78),0.25,metal=1.0)
TYRE=flat('tyre',lin((26,24,24)),0.8)
GLASS=flat('glass',lin((70,96,118)),0.15)
LAMPG=flat('lampglow',lin((255,226,150)),0.5,emit=3.0)
def car(n,loc,heading,color,coll=None,taxi=False):
    """1950s sedan; heading in degrees (0 = nose to +Y)"""
    e=empty(n,loc); e.rotation_euler=(0,0,math.radians(heading))
    body=flat('car_'+n,lin(color),0.35)
    parts=[box(n+'_b',(0,0,0.62),(1.9,4.7,0.62),body,bv=0.22,seg=3),
           box(n+'_c',(0,-0.25,1.18),(1.66,2.3,0.6),GLASS,bv=0.18,seg=3),
           box(n+'_r',(0,-0.25,1.5),(1.6,2.0,0.08),body,bv=0.04),
           box(n+'_bf',(0,2.38,0.5),(1.95,0.14,0.2),CHROME,bv=0.05),box(n+'_bb',(0,-2.38,0.5),(1.95,0.14,0.2),CHROME,bv=0.05),
           box(n+'_grill',(0,2.36,0.74),(1.2,0.06,0.2),CHROME,bv=0.02)]
    for sx in(-1,1):
        parts.append(sph(f'{n}_hl{sx}',(sx*0.7,2.33,0.82),0.13,LAMPG,sc_=(1,0.5,1)))
        parts.append(box(f'{n}_tl{sx}',(sx*0.78,-2.35,0.8),(0.22,0.06,0.16),flat('taillight',lin((200,30,30)),0.4,emit=1.0),bv=0.02))
        for sy in(-1,1):
            parts.append(cyl(f'{n}_w{sx}{sy}',(sx*0.86,sy*1.5,0.36),0.36,0.3,TYRE,v=20,rot=(0,math.pi/2,0)))
            parts.append(cyl(f'{n}_hub{sx}{sy}',(sx*1.02,sy*1.5,0.36),0.2,0.04,flat('whitewall',lin((236,232,224)),0.6),v=20,rot=(0,math.pi/2,0)))
    if taxi: parts.append(box(n+'_taxi',(0,-0.2,1.66),(0.6,0.3,0.22),flat('taxisign',lin((250,240,200)),0.5,emit=0.6),bv=0.03))
    for p in parts:
        p.parent=e
        if coll: L.put(p,coll)
    return e
LPM=flat('lampmetal',lin((52,74,62)),0.45,metal=0.35)   # r5: painted dark-green iron, shaded (round-4: flat pure-black pole read as a void, S15 1488-1554)
def lamppost(n,loc):
    cyl(n+'_base',(loc[0],loc[1],0.25),0.16,0.5,LPM,v=12); cyl(n+'_pole',(loc[0],loc[1],2.4),0.07,4.0,LPM,v=10)
    cyl(n+'_cap',(loc[0],loc[1],4.45),0.12,0.1,LPM,v=12); sph(n+'_glob',(loc[0],loc[1],4.75),0.28,LAMPG,sc_=(1,1,1.15))
def hydrant(n,loc):
    red=flat('hydrant',lin((200,40,34)),0.4); cyl(n,(loc[0],loc[1],0.35),0.13,0.7,red,v=14); sph(n+'_t',(loc[0],loc[1],0.72),0.14,red)
    cyl(n+'_n',(loc[0],loc[1],0.45),0.06,0.4,red,v=10,rot=(0,math.pi/2,0))
def mailbox(n,loc):
    b=flat('mailbox',lin((40,70,140)),0.5); box(n,(loc[0],loc[1],0.69),(0.5,0.5,1.0),b,bv=0.12);
    for sx in(-1,1):
        for sy in(-1,1): box(f'{n}_leg{sx}{sy}',(loc[0]+sx*0.12,loc[1]+sy*0.12,0.15),(0.06,0.06,0.3),INK,bv=0)
def trashcan(n,loc): cyl(n,(loc[0],loc[1],0.45),0.28,0.9,flat('can',lin((90,100,96)),0.5,metal=0.3),v=18); cyl(n+'_lid',(loc[0],loc[1],0.93),0.31,0.06,flat('can',lin((90,100,96))),v=18)
def building(n,front,facing,tex,w=8.0,h=12.0,d=8.0,awn=None,side=None,cap=(64,52,48)):
    """painted facade card on a box: front=(x,y) centre of the front face at ground; facing in L.FACING"""
    fx,fy=front; ax={'+X':(1,0),'-X':(-1,0),'+Y':(0,1),'-Y':(0,-1)}[facing]
    cx,cy=fx-ax[0]*d/2,fy-ax[1]*d/2; sx_,sy_=(d,w) if ax[0] else (w,d)
    sm=surf('side_'+(side or tex),'side_'+(side or tex),(w,h),gen=True)
    box(n,(cx,cy,h/2-0.3),(sx_,sy_,h+0.6),sm,bv=0.02)
    plane(n+'_front',(fx+ax[0]*0.012,fy+ax[1]*0.012,h/2),w,h,card_mat('fac_'+tex,tex,emit=0.12),face=facing)
    capm=flat('cap%d'%sum(cap),lin(cap),0.7)
    k_=int(''.join(ch for ch in n if ch.isdigit()) or 0); j_=0.012*(k_%4)+(0.006 if n.startswith('bX') else 0.0)   # r4: jitter overlapping neighbour caps so their faces are never coplanar (rule 163/228)
    box(n+'_cap',(cx+ax[0]*0.2,cy+ax[1]*0.2,h+0.25),(sx_+0.4+abs(ax[0])*0.4+j_,sy_+0.4+abs(ax[1])*0.4+j_,0.5+j_),capm,bv=0.04)
    box(n+'_ledge',(fx+ax[0]*0.15,fy+ax[1]*0.15,4.05),(abs(ax[1])*w+0.3*abs(ax[0]) or 0.3,abs(ax[0])*w+0.3*abs(ax[1]) or 0.3,0.18),capm,bv=0.02)
    if awn:
        am=flat('awn%d'%sum(awn),lin(awn),0.6)
        for k in (-1,1):
            ox,oy=(ax[1]*k*w*0.27*-1 if ax[1] else 0),(ax[0]*k*w*0.27 if ax[0] else 0)
            a=box(f'{n}_awn{k}',(fx+ax[0]*0.45+ox,fy+ax[1]*0.45+oy,2.95),(abs(ax[1])*w*0.3 or 0.9,abs(ax[0])*w*0.3 or 0.9,0.08),am,bv=0.02)
            a.rotation_euler=(math.radians(-14)*ax[1],math.radians(14)*ax[0],0)
    # roof clutter: water tank or chimney (rests on the cap)
    if R.random()<0.5:
        tx,ty=cx+R.uniform(-1.5,1.5),cy+R.uniform(-1.5,1.5)
        for lx in(-0.5,0.5):
            for ly in(-0.5,0.5): box(f'{n}_tl{lx}{ly}',(tx+lx,ty+ly,h+1.0),(0.12,0.12,1.0),INK,bv=0)
        cyl(n+'_tank',(tx,ty,h+2.3),0.9,1.6,flat('tank',lin((120,86,60)),0.8),v=18); cyl(n+'_tankr',(tx,ty,h+3.3),0.95,0.4,flat('tankroof',lin((70,60,56)),0.7),v=18,r2=0.1)
    else:
        box(n+'_chim',(cx+R.uniform(-2,2),cy+R.uniform(-2,2),h+1.2),(0.7,0.7,1.6),flat('chim',lin((150,70,50)),0.8),bv=0.03)
# ======================= SET A: 1950s Philadelphia downtown (origin) =======================
ROAD=surf('road','asphalt',(12,24),rough=0.8)
ROADX=surf('roadx','asphalt',(12,24),rough=0.8,rot=math.pi/2)
WALK=surf('walk','sidewalk',(3,3),rough=0.9)
box('roadNS',(0,15,-0.1),(12,190,0.2),ROAD,bv=0)
box('roadEW',(0,0,-0.098),(190,12,0.2),ROADX,bv=0)
for sx in(-1,1):
    for seg,(y0,y1) in enumerate([(-80,-6),(6,110)]):
        box(f'walk{sx}{seg}',(sx*8,(y0+y1)/2,0.07),(4,y1-y0,0.14),WALK,bv=0.03)
        box(f'curb{sx}{seg}',(sx*6.05,(y0+y1)/2,0.075),(0.12,y1-y0,0.15),flat('curb',lin((170,166,156)),0.8),bv=0)
    for seg,(x0,x1) in enumerate([(-90,-10),(10,90)]):
        box(f'walkx{sx}{seg}',((x0+x1)/2,sx*8,0.07),(x1-x0,4,0.14),WALK,bv=0.03)
    pass  # r4: corner pieces removed (walk strips already cover the corners; the triple coplanar overlap self-shadowed to black, rule 163)
    # for sy in(-1,1): box(f'walkc{sx}{sy}',(sx*8,sy*8,0.07),(4,4,0.14),WALK,bv=0.03)
FAC=[f'fac{i}' for i in range(8)]; AW=[(170,40,40),(40,110,90),(200,150,40),(60,80,150),(150,60,110),(200,90,40),(40,90,60),(120,40,40)]
k=0
for sx,face_ in ((-1,'+X'),(1,'-X')):
    y=-74.0
    while y<104:
        if -10<y<10: y=10.0
        if sx<0 and 36<=y<=56:
            if y<44: y=44.0
            building('deptA',(-10,48),'+X','dept50',w=16,h=12,d=10,side='dept50'); y=56.0+4; continue
        hh=[12,12,12][k%3]
        building(f'bA{k}',(sx*10,y),face_,FAC[k%8],h=hh,awn=AW[k%8]); y+=8.0; k+=1
for sy,face_ in ((-1,'+Y'),(1,'-Y')):
    for side_ in (-1,1):
        for i in range(6):
            x=side_*(14.03+i*8)   # r4: 3 cm off the A-row facades (coplanar corner faces, rule 228)
            building(f'bX{k}',(x,sy*10),face_,FAC[k%8],awn=AW[k%8]); k+=1
# far skyline with City Hall + sky cards at both street ends and both cross-street ends
for nme,loc,fc,w_ in [('N',(0,170,24),'-Y',260),('S',(0,-150,24),'+Y',260),('E',(150,0,24),'-X',260),('W',(-150,0,24),'+X',260)]:
    sk=plane('sky'+nme,(loc[0]*1.3,loc[1]*1.3,60),w_*1.6,200,card_mat('skyday','sky_day',emit=1.0),coll=L.C_NOI,face=fc); sk['fly']=1
    sl=plane('skyline'+nme,loc,w_,w_*1400/4096,card_mat('skyline50','skyline50',emit=0.55),coll=L.C_NOI,face=fc); sl['fly']=1
# street furniture
for sx in(-1,1):
    for y in range(-70,104,14):
        if abs(y)<9 or (sx<0 and 34<y+3<62) or (sx,y) in ((1,-28),(1,-14),(1,14)): continue   # r7: (1,14) stood between the S02 sidewalk lens and the walkers' faces   # no lamppost sweeping across the S03/S04 lens
        lamppost(f'lp{sx}_{y}',(sx*6.6,y+3))
for i,(x,y) in enumerate([(6.7,-8.2),(-6.8,9.0),(6.8,24),(-6.8,-30)]): hydrant(f'hyd{i}',(x,y))
for i,(x,y) in enumerate([(-7.0,-8.6),(7.0,52)]): mailbox(f'mb{i}',(x,y))
for i,(x,y) in enumerate([(6.8,-18.5),(-6.8,18),(6.8,31),(-6.8,-19)]): trashcan(f'tc{i}',(x,y))
# traffic signals on the four corners
for i,(x,y) in enumerate([(6.6,6.6),(-6.6,6.6),(6.6,-6.6),(-6.6,-6.6)]):
    cyl(f'sig{i}_pole',(x,y,1.9),0.08,3.8,INK,v=10); box(f'sig{i}_box',(x,y,4.15),(0.36,0.36,0.9),flat('sigbox',lin((40,70,50)),0.6),bv=0.04)
    for j,c in enumerate([(220,40,40),(240,200,60),(60,200,90)]):
        sph(f'sig{i}_l{j}',(x-0.19*(1 if x>0 else -1),y,4.45-j*0.28),0.08,flat(f'sigl{j}',lin(c),0.4,emit=2.0 if j==0 else 0.3))
# holiday garlands strung across the street between facing buildings (attached at both ends)
GAR=flat('garland',lin((40,110,60)),0.8)
for i,y in enumerate([-46,-22,3.6,6.4,22,70,86]):
    g=cyl(f'gar{i}',(0,y,7.6),0.09,20.0,GAR,v=8,rot=(0,math.pi/2,0)); g['inkmul']=0.5
    for j in range(5): sph(f'gar{i}_b{j}',(-8+j*4,y,7.45),0.22,flat('bauble%d'%(j%3),lin([(220,40,40),(250,200,60),(60,120,220)][j%3]),0.3,emit=0.6))
# traffic podium in the middle of the intersection
pod=flat('podium',lin((236,232,220)),0.6)
cyl('podium',(0,0,0.32),0.62,0.64,pod,v=24); cyl('podium_band',(0,0,0.46),0.64,0.14,flat('podband',lin((200,40,40)),0.5),v=24)
# ---- the jam: 1950s cars every which way ----
COLS=[(120,200,190),(240,226,190),(200,60,50),(70,130,190),(250,200,60),(150,200,120),(230,140,160),(90,90,120),(240,240,230)]
cars=[]; ci=0
for lane in (-4.5,-1.5,1.5):
    for y in (-58,-50,-42,-34,-26,-18,-11,13,20,27,34,41,48,56,63,70):
        if lane==1.5 and -30<y<-6: continue
        if lane<0 and 30<y<64: continue
        if R.random()<0.12: continue
        cars.append(car(f'car{ci}',(lane+R.uniform(-0.2,0.2),y+R.uniform(-0.8,0.8),0),(0 if lane>0 else 180)+R.uniform(-4,4),COLS[ci%9],taxi=(ci%5==2))); ci+=1
for lane in (-4.5,-1.5,1.5,4.5):
    for x in (-50,-42,-34,-26,-18,-11,11,18,26,34,42,50):
        if R.random()<0.15: continue
        cars.append(car(f'car{ci}',(x+R.uniform(-0.8,0.8),lane+R.uniform(-0.2,0.2),0),(90 if lane>0 else 270)+R.uniform(-4,4),COLS[ci%9],taxi=(ci%5==2))); ci+=1
# two cars nosed into the box, blocking (the jam)
cars.append(car('carX2',(3.4,-3.3,0),300,COLS[6],taxi=True))
cars.append(car('carX3',(-3.4,-3.8,0),40,COLS[1]))
print('SET A ok, cars',len(cars))
# ======================= CAST + CAMERAS, set A shots =======================
def crowd(shot,rng,spots,kinds,seed,walkers=None,faces_pool=None,camname=None,base=0):
    """extras: spots=[(x,y,z)], walkers: list of (i, f0, f1, dx, dy)"""
    rr=random.Random(seed); out=[]
    for i,p in enumerate(spots):
        kd=kinds[i%len(kinds)]; wk=bool(walkers and any(w[0]==i for w in walkers))
        props=CI_PROPS.get(kd,[])
        arms_=('arm','arm_'+props[0]) if props and rr.random()<0.6 else ('arm','arm')
        ch=char(f'{shot}_x{i+base}_{kd}',kd,shot,p,rng,arms=arms_,walker=wk,camname=camname)   # r7: base keeps a second crowd's names unique (no .001 duplicates)
        fl=list(L.CI[kd]['faces']); fl=[f for f in fl if f!='blink']
        if faces_pool=='glad': fl=[f for f in fl if f not in ('angry','stern','frown','push','lost')] or fl   # r5: a delighted crowd never shows a stern/angry card
        f0=rng[0]; seq=[]
        while f0<rng[1]: seq.append((f0,rr.choice(fl))); f0+=rr.randint(22,40)
        faces(ch,seq)
        if wk:
            for w in walkers:
                if w[0]==i: walk(ch,w[1],w[2],p,(p[0]+w[3],p[1]+w[4],p[2]))
        out.append(ch)
    return out
CHRS=set()
CI_PROPS={k:v.get('props',[]) for k,v in L.CI.items()}
ALL=[]
# ---------- S01 (0-170): low angle on the traffic cop blowing his whistle; crane up on "disaster" (f136) ----------
def hardcut(shot,f):
    """round 5 (retime): a hard cut inside a shot = CONSTANT key at f-1, new framing keyed at f"""
    for o_ in (L.CAM[shot],L.TGT[shot]):
        for fc in o_.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                if int(round(kp.co[0]))==f-1: kp.interpolation='CONSTANT'
s='S01'; r=SH[s]
cop=char('S01_cop','cop',s,(0,0,0.64),r,'whistle',arms=('arm','arm')); ALL.append(cop)
faces(cop,[(0,'whistle'),(28,'annoyed'),(60,'grit'),(88,'shout'),(106,'annoyed'),(128,'shock'),(140,'whistle')])
for f,a in [(0,-140),(14,-146),(24,-120),(46,-142),(70,-95),(90,-146),(118,-132),(136,-146)]: arm(cop,1,f,a)   # r7 (rule 268): raised whistle-hand stays out beside the head (armprobe), was -165 over the face
for f,a in [(0,-60),(30,-90),(60,-40),(96,-95),(140,-70)]: arm(cop,-1,f,a)
bob(cop,[8,30,62,90,128])
ex=crowd(s,r,[(7.60,-8.20,0.14),(8.60,-7.40,0.14),(-8.30,-7.43,0.14),(-8.60,8.00,0.14),(8.60,8.10,0.14),(9.00,-9.00,0.14),(-9.20,-8.80,0.14)],   # r4 pass3: prop-aware crowdopt
         ['shopper','fanblue','tourist','granny','fangold','kid','shopper'],5); ALL+=ex
path(s,[(0,(1.0,-2.05,0.95),(0,0.2,1.9)),(45,(0.45,-2.3,0.95),(0,0.2,1.92)),(87,(-0.27,-2.26,0.99),(0,0.2,1.92)),(88,(0.75,-1.5,1.22),(0,0.2,1.95)),(126,(0.55,-1.62,1.26),(0,0.25,1.93)),   # r5: hard cut on 'much,' (f88) to a 3/4 punch-in
        (136,(-2.5,-6.5,4.0),(0,1.0,1.4)),(152,(-6.0,-15.0,9.5),(0,2.0,0.8)),(170,(-6.8,-17.0,10.6),(0.2,2.4,0.8))])
hardcut('S01',88)
# ---------- S02 (163-297): high crane over the day-after-Thanksgiving street, the town rushes downtown ----------
s='S02'; r=SH[s]
sp=[];W=[]
for i in range(26):
    sx=-1 if i%2 else 1; y=16+2.3*(i//2)+[0,0.9,-0.6,0.4,-0.9,0.7][i%6]; x=sx*(7.2+[0.0,1.3,0.5,1.8,0.9,0.2,1.5][(i*3)%7]); sp.append((x,y,0.14))
    if i%3!=2: W.append((i,163,297,0,-4.5))
for i_,x_ in ((4,7.9),(10,8.2)): sp[i_]=(x_,sp[i_][1],sp[i_][2])   # r7 (occprobe): granny out from behind the tourist, fan off the lamppost
ex=crowd(s,r,sp,['shopper','tourist','fanblue','fangold','granny','kid','shopper','fanblue'],9,walkers=W); ALL+=ex
cop2=char('S02_cop','cop',s,(0,0,0.64),r,'whistle',arms=('arm','arm')); ALL.append(cop2)
faces(cop2,[(163,'whistle'),(200,'annoyed'),(236,'shout'),(270,'whistle')])
for f,a in [(163,-150),(180,-120),(198,-160),(220,-110),(244,-155),(270,-120)]: arm(cop2,1,f,a)
for f,a in [(163,-70),(190,-100),(230,-50),(262,-95)]: arm(cop2,-1,f,a)
# r6 (owner Nov 19: the crane down onto the traffic repeated S01's background): high hold over the town pouring in, hard cut on 'whole' (f220) to a low sidewalk view of the crowd rushing at the lens (no traffic in frame)
sp2=[];W2=[]
for i in range(10):   # r6: the town pours down the right sidewalk at the lens (denser rush, walkers toward camera only); wide lateral stagger so no face hides another
    sp2.append((7.55+[0.0,1.2,0.6,1.45,0.3,0.9,1.35][i%7], 19.0+2.1*i+[0,0.6,-0.4][i%3], 0.14)); W2.append((i,163,297,0,-4.5))
sp2[4]=(9.15,sp2[4][1],sp2[4][2])   # r7 (occprobe): granny out from behind the fan
ex2=crowd(s,r,sp2,['tourist','shopper','fangold','kid','granny','fanblue'],29,walkers=W2,base=20); ALL+=ex2
path(s,[(163,(1.0,-14,26),(0,26,0)),(200,(5.0,4.0,15.0),(8.4,24,0.4)),(219,(5.8,7.5,13.0),(8.4,25,0.4)),(220,(5.3,12.5,0.95),(9.2,25,1.5)),(297,(5.5,9.8,1.0),(9.2,23,1.5))])
hardcut('S02',220)
# r7 (rule 204 / occprobe): in the low sidewalk view (220-297) extras whose faces sit fully behind nearer walkers leave the shot at the hard cut (they read as headless bodies)
S02_HIDE=['S02_x4_granny','S02_x12_granny','S02_x21_shopper','S02_x22_fangold','S02_x23_kid','S02_x25_fanblue','S02_x26_tourist','S02_x6_shopper','S02_x8_shopper','S02_x2_fanblue']
for n_ in S02_HIDE:
    _r=bpy.data.objects[n_]
    for f_,v_ in ((219,1.0),(220,0.0001)): _r.scale=(v_,)*3; _r.keyframe_insert('scale',frame=f_)
    for fc_ in _r.animation_data.action.fcurves:
        if fc_.data_path=='scale':
            for k_ in fc_.keyframe_points: k_.interpolation='CONSTANT'
# ---------- S03 (292-432): sidewalk truck past shoppers, the tourist and the football fans ----------
s='S03'; r=SH[s]
sho=char('S03_shopper','shopper',s,(8.2,-29.0,0.14),r,'happy',arms=('arm_bag','arm_box'))
tou=char('S03_tourist','tourist',s,(8.3,-26.2,0.14),r,'lost',arms=('arm','arm_camera'))
fb=char('S03_fanblue','fanblue',s,(8.0,-22.1,0.14),r,'cheer',arms=('arm','arm_pennant'))
fg=char('S03_fangold','fangold',s,(8.4,-19.7,0.14),r,'shout',arms=('arm_pennant','arm'))
ALL+=[sho,tou,fb,fg]
faces(sho,[(292,'happy'),(304,'shock'),(318,'happy'),(352,'angry'),(372,'happy')]); bob(sho,[296,318])
faces(tou,[(292,'lost'),(312,'happy'),(334,'lost'),(346,'happy'),(380,'lost')]); arm(tou,1,292,-20); arm(tou,1,308,-115); arm(tou,1,330,-120); arm(tou,1,342,-30); bob(tou,[312])
faces(fb,[(292,'cheer'),(352,'shout'),(366,'cheer'),(392,'shout'),(408,'cheer')]); faces(fg,[(292,'shout'),(352,'cheer'),(366,'shout'),(392,'cheer'),(410,'shout')])
for f in range(352,432,8): arm(fb,1,f,-150 if (f//8)%2 else -120); arm(fg,-1,f+3,-150 if (f//8)%2 else -120)
bob(fb,[358,392]); bob(fg,[361,396])
ex=crowd(s,r,[(9.2,-31.5,0.14),(9.3,-24.0,0.14),(9.5,-16.3,0.14),(7.2,-34,0.14)],['granny','kid','shopper','tourist'],13,walkers=[(3,292,432,0,9.0)]); ALL+=ex
path(s,[(292,(5.85,-30.0,1.3),(8.3,-28.4,1.45)),(344,(5.9,-27.2,1.3),(8.4,-25.8,1.45)),(366,(5.85,-23.6,1.3),(8.2,-22.1,1.5)),(400,(5.9,-21.4,1.3),(8.2,-20.4,1.55)),(432,(5.95,-20.4,1.35),(8.3,-19.6,1.5))])
# round 4 (L9): we ride the truck: its side mirror frames the lower left of S03 (parented to the camera, so no sweep; deep DOF blur)
_c3=L.chr_coll('S03'); _cam3=L.CAM['S03']
# r6 (owner Nov 19): the camera-parented truck mirror read as a glitch blob in the lower left; removed
# ---------- S04 (426-528): high over the jam, dive to the thief swiping a gift box on "thieves" (f487) ----------
s='S04'; r=SH[s]
sh4=char('S04_shopper','shopper',s,(8.3,-12.4,0.14),r,'happy',arms=([(426,'arm_bag'),(489,'arm')],[(426,'arm_box'),(489,'arm')]))
th=char('S04_thief','thief',s,(8.4,-17.0,0.14),r,'sneaky',arms=('arm',[(426,'arm'),(489,'arm_box')]),walker=True)
ALL+=[sh4,th]
walk(th,446,486,(8.4,-17.0,0.14),(8.8,-13.1,0.14),step=3); walk(th,493,528,(8.8,-13.1,0.14),(8.9,-17.8,0.14),step=2)
faces(th,[(426,'sneaky'),(470,'grin'),(486,'sneaky'),(492,'grin'),(512,'shock')]); arm(th,1,478,-20); arm(th,1,486,-70); arm(th,1,491,-15)
faces(sh4,[(426,'happy'),(492,'shock'),(503,'angry'),(518,'shock')]); arm(sh4,-1,492,-150); arm(sh4,1,494,-140); bob(sh4,[492,503])
ex=crowd(s,r,[(7.31,-10.75,0.14),(8.90,-9.33,0.14),(9.20,-19.50,0.14),(-7.60,-12.00,0.14),(-8.40,-15.00,0.14)],['granny','tourist','fanblue','shopper','fangold'],17); ALL+=ex   # x1 tourist is the S04>S05 bridge head   # round 4: occprobe moves (awning, car, shopper no longer cover faces) | r4: ALL+=ex was inside the comment; tourist x 9.4->10.1 (shopper covered it 483-504)   # r4 pass3: prop-aware crowdopt
path(s,[(426,(2.6,-9.0,30.0),(3.6,-9.5,0.0)),(452,(3.0,-10.0,24.0),(4.6,-11.5,0.0)),(487,(6.0,-15.8,1.6),(8.4,-12.8,1.4)),(505,(6.1,-14.6,1.55),(8.5,-10.6,1.4)),(528,(6.2,-13.4,1.55),(8.5,-8.0,1.35))])
def world_and_sun():
    w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; bg=w.node_tree.nodes['Background']; bg.inputs['Color'].default_value=(*lin((150,190,225)),1); bg.inputs['Strength'].default_value=1.1
    bpy.ops.object.light_add(type='SUN',rotation=(math.radians(50),0,math.radians(-140))); sun=bpy.context.object; sun.name='sun'; sun.data.energy=5.2; sun.data.color=(1.0,0.92,0.8); sun.data.angle=math.radians(3)
def shot_list(): return [n for n in SH if n in CHRS]
if STAGE=='A':
    for a in ALL: finish(a)
    world_and_sun(); print('hulls',L.ink()); L.render_setup(25,8)
    bpy.ops.wm.save_as_mainfile(filepath='/root/bf/blend/bfA.blend'); print('SCENE_OK A'); raise SystemExit
# ======================= interior helper =======================
def room(n,cx,w,d,h,wall,floor,ftile=(2.5,2.5),wtile=(4,4)):
    """three-wall diorama room; back wall at y=+d/2 facing -Y; floor centred at (cx,0)"""
    box(n+'_floor',(cx,0,-0.1),(w+2,d+4,0.2),surf(n+'_fl',floor,ftile,rough=0.6),bv=0)
    box(n+'_back',(cx,d/2+0.15,h/2),(w+0.6,0.3,h),surf(n+'_wall',wall,wtile),bv=0.02)
    for sx in(-1,1): box(f'{n}_side{sx}',(cx+sx*(w/2+0.15),0.5,h/2),(0.3,d+1,h),surf(n+'_wall',wall,wtile),bv=0.02)
    box(n+'_base',(cx,d/2-0.02,0.08),(w,0.06,0.16),flat(n+'_skirt',lin((60,44,34)),0.6),bv=0.01)
    box(n+'_crown',(cx,d/2-0.02,h-0.1),(w,0.1,0.18),flat(n+'_skirt',lin((60,44,34))),bv=0.01)
    box(n+'_ceil',(cx,0.5,h+0.1),(w+0.6,d+1,0.2),flat(n+'_ceilm',lin((226,220,204)),0.9),bv=0)
    for j in range(2): cyl(f'{n}_light{j}',(cx+(j-0.5)*w*0.4,0.4,h-0.06),0.28,0.12,flat('ceillamp',lin((255,240,210)),0.5,emit=4.0),v=20)
    for j in range(2): glow(f'{n}_lglow{j}',(cx+(j-0.5)*w*0.4,0.1,h-0.2),1.3,(255,232,190),1.4)
def desk(n,c,w=1.8,d=0.8,h=0.78,m=None):
    m=m or flat('deskwood',lin((110,70,44)),0.5)
    box(n+'_top',(c[0],c[1],h-0.03),(w,d,0.06),m,bv=0.015)
    box(n+'_pedL',(c[0]-w/2+0.25,c[1],(h-0.06)/2),(0.46,d-0.06,h-0.06),m,bv=0.015)
    box(n+'_pedR',(c[0]+w/2-0.25,c[1],(h-0.06)/2),(0.46,d-0.06,h-0.06),m,bv=0.015)
    box(n+'_front',(c[0],c[1]-d/2+0.04,h/2),(w-0.96,0.04,h-0.2),m,bv=0.01)
    for sx in(-1,1):
        for j in range(3): box(f'{n}_dr{sx}{j}',(c[0]+sx*(w/2-0.25),c[1]-d/2+0.01,0.15+j*0.2),(0.38,0.03,0.16),flat('drawer',lin((130,86,56)),0.5),bv=0.01)
    return h
def phone(n,c):
    k=flat('bakelite',lin((24,22,22)),0.3); box(n,(c[0],c[1],c[2]+0.05),(0.22,0.24,0.1),k,bv=0.03); box(n+'_h',(c[0],c[1],c[2]+0.13),(0.26,0.07,0.06),k,bv=0.025)
    cyl(n+'_dial',(c[0],c[1]-0.05,c[2]+0.105),0.06,0.012,flat('dial',lin((230,226,214)),0.4),v=16,rot=(math.radians(20),0,0))
def glow(n,c,size,rgb,strength,face='-Y',coll=None,img='glow',on=None):
    """in-world bloom: camera-side additive glow card (rule L8: emitters get a glow + light pool), never post bloom over faces"""
    key=f'glowm_{img}_{rgb}_{strength}'
    m=bpy.data.materials.get(key)
    if not m:
        m=bpy.data.materials.new(key); N,Lk=L.nodes(m)
        for x in list(N): N.remove(x)
        o=N.new('ShaderNodeOutputMaterial'); it=N.new('ShaderNodeTexImage'); it.image=bpy.data.images.load(L.TX+img+'.png',check_existing=True)
        em=N.new('ShaderNodeEmission'); em.inputs['Color'].default_value=(*lin(rgb),1); em.inputs['Strength'].default_value=strength
        tr=N.new('ShaderNodeBsdfTransparent'); ad=N.new('ShaderNodeAddShader'); mx=N.new('ShaderNodeMixShader')
        Lk.new(it.outputs['Alpha'],mx.inputs['Fac']); Lk.new(tr.outputs[0],mx.inputs[1]); Lk.new(em.outputs[0],ad.inputs[0]); Lk.new(tr.outputs[0],ad.inputs[1]); Lk.new(ad.outputs[0],mx.inputs[2]); Lk.new(mx.outputs[0],o.inputs['Surface'])
    g=plane(n,c,size,size if img=='glow' else size*2.2,m,coll=coll,face=face); g['noink']=1; g.visible_shadow=False; g.visible_diffuse=False; g.visible_glossy=False
    if on is not None: L.vis(g,[on])
    return g
def pool(n,c,w,h,coll=None,on=None):
    m=bpy.data.materials.get('poolm')
    if not m:
        m=bpy.data.materials.new('poolm'); N,Lk=L.nodes(m); p=N['Principled BSDF']; it=N.new('ShaderNodeTexImage'); it.image=bpy.data.images.load(L.TX+'pool.png',check_existing=True)
        Lk.new(it.outputs['Color'],p.inputs['Emission Color']); Lk.new(it.outputs['Alpha'],p.inputs['Alpha']); p.inputs['Base Color'].default_value=(0,0,0,1); p.inputs['Emission Strength'].default_value=2.4; p.inputs['Specular IOR Level'].default_value=0
    o=plane(n,c,w,h,m,coll=coll,horiz=True); o['noink']=1; o.visible_shadow=False
    if on is not None: L.vis(o,[on])
    return o
def lamp(n,c,on=None,col=(255,220,150)):
    b=flat('brass',lin((180,140,60)),0.3,metal=0.8); cyl(n+'_b',(c[0],c[1],c[2]+0.02),0.1,0.04,b,v=14); cyl(n+'_s',(c[0],c[1],c[2]+0.22),0.015,0.4,b,v=8)
    sh=cyl(n+'_shade',(c[0],c[1]-0.04,c[2]+0.45),0.16,0.14,flat(n+'_shm',lin((40,110,70)),0.5),v=16,r2=0.06)
    rng=on if on is not None else (0,99999)
    glow(n+'_glow',(c[0],c[1]-0.2,c[2]+0.36),0.85,(255,214,140),6.0,on=rng)          # bulb glow under the shade
    pool(n+'_pool',(c[0]+0.05,c[1]-0.15,c[2]+0.003),0.9,0.65,on=rng)                  # warm light pool on the desk top
    return sh
def cabinet(n,c,h=1.3):
    m=flat('cabinet',lin((110,120,110)),0.4,metal=0.3); box(n,(c[0],c[1],h/2),(0.5,0.6,h),m,bv=0.02)
    for j in range(int(h/0.33)): box(f'{n}_d{j}',(c[0],c[1]-0.3,0.2+j*0.33),(0.42,0.03,0.26),m,bv=0.01); box(f'{n}_hd{j}',(c[0],c[1]-0.32,0.26+j*0.33),(0.12,0.03,0.03),CHROME,bv=0)
def coatrack(n,c,hats=2):
    cyl(n,(c[0],c[1],0.9),0.03,1.8,INK,v=8); cyl(n+'_ft',(c[0],c[1],0.03),0.25,0.06,INK,v=12)
    for j in range(hats): cyl(f'{n}_hat{j}',(c[0]+(j-0.5)*0.16,c[1],1.78+j*0.002),0.13,0.1,flat('copcap',lin((28,36,70)),0.6),v=16)
def wallclock(n,c):
    cyl(n,c,0.3,0.06,flat('clockrim',lin((60,44,34)),0.5),v=24,rot=(math.pi/2,0,0)); cyl(n+'_f',(c[0],c[1]-0.035,c[2]),0.26,0.01,flat('clockface',lin((246,240,226)),0.6),v=24,rot=(math.pi/2,0,0))
    for j,(l,a) in enumerate([(0.16,30),(0.22,-80)]):
        h=box(f'{n}_hand{j}',(c[0],c[1]-0.045,c[2]),(0.02,0.01,l),INK,bv=0); h.location=(c[0]+math.sin(math.radians(a))*l/2,c[1]-0.045,c[2]+math.cos(math.radians(a))*l/2); h.rotation_euler=(0,math.radians(a),0)
def gifts(n,c,k=4,seed=1):
    rr=random.Random(seed); z=c[2]
    for j in range(k):
        s_=rr.uniform(0.18,0.32); col_=rr.choice([(200,40,40),(40,110,180),(40,140,80),(230,190,60),(150,60,150)])
        b=box(f'{n}_{j}',(c[0]+rr.uniform(-0.05,0.05),c[1]+rr.uniform(-0.05,0.05),z+s_*0.4),(s_,s_*0.9,s_*0.8),flat('gift%d'%sum(col_),lin(col_),0.5),bv=0.01)
        box(f'{n}_{j}r',(b.location.x,b.location.y,b.location.z),(s_*1.01,0.04,s_*0.81),flat('ribbon',lin((250,230,120)),0.4),bv=0)
        z+=s_*0.8
def wallframe(n,c,w,h,tex,face='-Y',col=(60,44,34)):
    ax={'-Y':(0,-1),'+X':(1,0),'-X':(-1,0)}[face]
    box(n,(c[0]-ax[0]*0.02,c[1]-ax[1]*0.02,c[2]),((0.05 if ax[0] else w+0.08),(0.05 if ax[1] else w+0.08),h+0.08),flat('frame%d'%sum(col),lin(col),0.5),bv=0.01)
    plane(n+'_pic',(c[0]+ax[0]*0.009,c[1]+ax[1]*0.009,c[2]),w,h,card_mat(tex+'_pic',tex,emit=0.2),face=face)
def shelf_items(n,c,w,seed):
    rr=random.Random(seed); x=c[0]-w/2+0.08
    box(n,(c[0],c[1],c[2]),(w,0.28,0.04),flat('shelfwood',lin((100,66,42)),0.6),bv=0.01)
    while x<c[0]+w/2-0.08:
        k=rr.random(); hh=rr.uniform(0.18,0.3); ww=rr.uniform(0.05,0.1)
        col_=rr.choice([(150,40,40),(40,70,120),(60,110,60),(200,170,90),(90,60,110),(220,210,190)])
        if k<0.75: box(f'{n}_b{x:.2f}',(x+ww/2,c[1],c[2]+0.02+hh/2),(ww,0.22,hh),flat('bk%d'%sum(col_),lin(col_),0.6),bv=0.006)
        else: cyl(f'{n}_j{x:.2f}',(x+0.06,c[1],c[2]+0.02+0.08),0.05,0.16,flat('jar%d'%sum(col_),lin(col_),0.4),v=14); ww=0.1
        x+=ww+0.012
# ======================= SET B: precinct (X=300) =======================
BX=300
room('prec',BX,9,7,3.6,'precinct','lino')
BOARD_Z=1.58
box('board_frame',(BX,3.47,BOARD_Z),(1.68,0.08,1.58),flat('boardwood',lin((110,76,44)),0.6),bv=0.02)
boards=[plane(f'board{i}',(BX,3.42,BOARD_Z),1.6,1.5,card_mat(f'board{i}',f'board{i}',emit=0.35)) for i in range(2)]+[plane(f'boardw{n:02d}',(BX,3.42,BOARD_Z),1.6,1.5,card_mat(f'boardw{n:02d}',f'boardw{n:02d}',emit=0.35)) for n in range(1,13)]
box('chalktray',(BX,3.36,BOARD_Z-0.77),(1.6,0.14,0.05),flat('boardwood',lin((110,76,44))),bv=0.01)
desk('pdesk',(BX-3.0,1.6)); phone('pphone',(BX-3.3,1.6,0.78)); L_=lamp('plamp',(BX-2.5,1.8,0.78))
box('typew',(BX-2.9,1.45,0.86),(0.4,0.3,0.16),flat('typew',lin((50,56,52)),0.4),bv=0.03)
for j in range(3): cyl(f'mug{j}',(BX-3.6+j*0.1,1.4,0.84),0.04,0.11,flat('mug',lin((230,226,214)),0.4),v=12)
cabinet('pcab1',(BX+3.9,2.9)); cabinet('pcab2',(BX+3.3,2.9)); coatrack('prack',(BX-4.0,2.8))
# round 3 (L9 density, >=20 props in frame): cork notice board with pinned sheets, wall clock, framed photo, shelf, radiator, wanted sheets
cork=flat('cork',lin((176,130,84)),0.9)
box('pnb',(BX+1.42,3.46,1.62),(0.95,0.04,1.05),cork,bv=0.01); box('pnb_fr',(BX+1.42,3.475,1.62),(1.03,0.03,1.13),flat('boardwood',lin((110,76,44))),bv=0.01)
for j,(dx,dz,t,w_,h_,rz) in enumerate([(-0.24,0.24,'memo0',0.3,0.4,4),(0.18,0.28,'memo1',0.32,0.42,-5),(-0.22,-0.24,'memo2',0.3,0.4,-3),(0.2,-0.2,'memo0',0.3,0.36,3)]):
    pp=plane(f'pnb_p{j}',(BX+1.42+dx,3.43,1.62+dz),w_,h_,card_mat(t+'_pin',t,emit=0.15)); pp.rotation_euler[1]=math.radians(rz)
    sph(f'pnb_pin{j}',(BX+1.42+dx,3.42,1.62+dz+h_/2-0.04),0.018,flat('pinred',lin((200,40,40)),0.4))
wallclock('pclock',(BX-1.25,3.46,2.78))
wallframe('pph1',(BX-1.35,3.48,1.85),0.6,0.45,'fac0'); wallframe('pph2',(BX-1.35,3.48,1.25),0.36,0.48,'paper66')
shelf_items('pshelf',(BX+1.4,3.36,2.5),1.1,33)
rad=flat('radiator',lin((190,186,170)),0.5,metal=0.3)
for j in range(9): box(f'prad{j}',(BX+1.05+j*0.09,3.38,0.42),(0.06,0.14,0.6),rad,bv=0.02)
box('pradtop',(BX+1.41,3.38,0.73),(0.86,0.16,0.03),rad,bv=0.01)
cyl('ppipe',(BX+0.95,3.42,1.9),0.03,3.6,rad,v=10)

wallclock('pclock',(BX+2.3,3.28,2.75)); cyl('cooler',(BX+2.6,2.9,0.5),0.18,1.0,flat('cooler',lin((200,200,190)),0.4),v=16); sph('coolerjug',(BX+2.6,2.9,1.22),0.2,flat('jug',lin((150,200,230)),0.1))
box('pbench',(BX-1.2,-1.6,0.24),(1.6,0.4,0.05),flat('deskwood',lin((110,70,44))),bv=0.01)
for sx in(-1,1): box(f'pbenchl{sx}',(BX-1.2+sx*0.7,-1.6,0.11),(0.06,0.36,0.22),INK,bv=0)
plane('pwanted',(BX-2.4,3.49,2.0),0.5,0.65,card_mat('paper62s','paper62',emit=0.15))
plane('pmap',(BX+3.2,3.49,2.1),1.1,0.75,card_mat('skyline50s','skyline50',emit=0.2))
wallframe('pph1',(BX-3.6,3.48,2.35),0.5,0.4,'fac3'); wallframe('pph2',(BX-1.75,3.48,2.6),0.35,0.45,'fac1'); wallframe('pph3',(BX+1.75,3.48,2.65),0.4,0.3,'fac5')
box('pcork',(BX+3.2,3.47,1.25),(1.0,0.04,0.6),flat('cork',lin((176,130,84)),0.8),bv=0.01)
for j in range(5): plane(f'pnote{j}',(BX+2.82+j*0.19,3.445,1.25+0.12*((j%2)*2-1)),0.16,0.22,card_mat('town%d_n'%(j%4),'town%d'%(j%4),emit=0.15))
shelf_items('pshelf',(BX-3.0,3.36,1.55),1.6,5)
# board swaps: roster -> stamped (on "off" f574) -> chalk BLACK FRIDAY letter by letter (f606-628)
WT=[606+round(n*22/12) for n in range(1,13)]   # one letter at a time, under the chalk as the cop sidesteps (606-628)
BT=[(0,573),(574,WT[0]-1)]+[(WT[i],(WT[i+1]-1 if i<11 else END)) for i in range(12)]
for b_,(a_,z_) in zip(boards,BT): vis(b_,[(a_,z_)])
s='S05'; r=SH[s]
cp=char('S05_cop','cop',s,(BX+0.0,1.95,0),r,'neutral',arms=('arm',[(520,'arm'),(588,'arm_chalk')]),walker=True)
oc=char('S05_sarge','oldcop',s,(BX+1.3,2.55,0),r,'deadpan',arms=('arm','arm'),walker=True)
walk(oc,592,606,(BX+1.3,2.55,0),(BX+2.3,1.85,0),step=3)
c2=char('S05_cop2','cop',s,(BX+2.3,0.7,0),r,'neutral'); c3=char('S05_cop3','cop',s,(BX-2.2,1.65,0),r,'neutral')
ALL+=[cp,oc,c2,c3]
faces(cp,[(520,'neutral'),(548,'shock'),(568,'sad'),(586,'annoyed'),(600,'grit'),(618,'smug'),(636,'laugh')])
faces(oc,[(520,'deadpan'),(556,'raise'),(574,'smug'),(600,'deadpan'),(626,'raise')])
faces(c2,[(520,'neutral'),(556,'shock'),(574,'sad'),(612,'shock'),(630,'laugh')]); faces(c3,[(520,'blink'),(523,'neutral'),(559,'shock'),(577,'sad'),(615,'shock'),(633,'laugh')])
bob(cp,[548,568,618]); bob(c2,[556,574]); bob(c3,[559,577]); bob(oc,[574])
arm(oc,-1,560,-20); arm(oc,-1,570,-95); arm(oc,-1,574,-80); arm(oc,-1,590,-15)   # sergeant taps the board
# the cop steps to the board, then sidesteps right while the chalk writes left to right (hand on the letters, rule 166)
CH_L,CH_R,CH_Z=BX-0.62,BX+0.62,BOARD_Z+0.75-1.3
walk(cp,586,600,(BX+0.0,1.95,0),(CH_L+0.58,3.12,0),step=3)
walk(cp,606,628,(CH_L+0.58,3.12,0),(CH_R+0.58,3.12,0),step=3,swing=(1,))   # round 4: the stride swing overrode the chalk arm (letters appeared with the arm down)
walk(cp,632,652,(CH_R+0.58,3.12,0),(BX+0.98,2.62,0),step=3)
for f,a_ in [(586,-10),(600,-92),(606,-95),(610,-91),(614,-96),(618,-91),(622,-95),(628,-93),(636,-20)]: arm(cp,-1,f,a_)
path(s,[(520,(BX-0.85,-0.15,1.95),(BX+0.38,2.3,1.3)),(574,(BX-0.8,-0.15,1.9),(BX+0.02,2.35,1.12)),   # r5 (round-4 P3): camera ~25 deg off-axis so the cop and sergeant stand on a diagonal, not a frontal two-shot
        (600,(BX-0.6,0.25,1.75),(BX+0.05,3.2,1.1)),(619,(BX-0.05,0.25,1.7),(BX+0.2,3.2,1.22)),(625,(BX+0.1,0.0,1.68),(BX+0.3,3.2,1.22)),(631,(BX+0.26,0.0,1.66),(BX+0.39,3.15,1.22)),(640,(BX+0.36,-0.05,1.65),(BX+0.4,3.1,1.22)),(652,(BX+0.36,-0.1,1.65),(BX+0.4,3.1,1.22))])
# round 4 (L9): FG water cooler at the right edge of S05 (fgcheck.py: in at x 0.77-1.1 except a smooth exit/return 592-616)
_c5=L.chr_coll('S05'); box('coolS05',(BX+1.08,1.6,0.55),(0.32,0.32,1.1),flat('cooler',lin((220,214,200)),0.5),coll=_c5,bv=0.03); cyl('coolS05_btl',(BX+1.08,1.6,1.28),0.13,0.32,flat('coolbtl',lin((120,170,220)),0.15),v=20,coll=_c5)
# ======================= SET C: store owners' office, 1961 (X=600) =======================
CX=600
room('off61',CX,7,6,3.2,'office','wood')
box('off61_win',(CX+1.8,2.96,1.9),(1.7,0.08,1.3),flat('winframe',lin((240,236,220)),0.5),bv=0.02)
plane('off61_view',(CX+1.8,2.9,1.9),1.5,1.1,card_mat('fac2v','fac2',emit=0.6))
for j in range(2): box(f'off61_mull{j}',(CX+1.8,2.86,1.9),(0.04 if j==0 else 1.5,0.03,1.1 if j==0 else 0.04),flat('winframe',lin((240,236,220))),bv=0)
desk('odesk',(CX,0.9,0),w=2.0)
reg=flat('register',lin((150,120,70)),0.3,metal=0.6)
box('register',(CX-0.3,0.85,0.95),(0.45,0.4,0.3),reg,bv=0.03); box('register_top',(CX-0.3,0.95,1.17),(0.4,0.2,0.16),reg,bv=0.02)
phone('ophone',(CX+0.8,0.8,0.78)); gifts('ogifts',(CX-2.4,1.8,0),k=5,seed=4); gifts('ogifts2',(CX+2.6,1.6,0),k=4,seed=8)
plane('cal61',(CX+0.65,2.98,2.05),0.45,0.56,card_mat('cal61','cal61',emit=0.2))
box('oshelf',(CX-1.6,2.8,1.25),(1.2,0.3,0.04),flat('deskwood',lin((110,70,44))),bv=0.01)
wallframe('oph1',(CX-0.2,2.98,2.25),0.7,0.5,'fac6'); wallframe('oph2',(CX-1.0,2.98,2.3),0.35,0.45,'fac1'); wallframe('oph3',(CX-2.7,2.98,2.2),0.45,0.6,'dept50')
shelf_items('oshelf2',(CX+2.7,2.855,1.4),1.0,9); coatrack('orack',(CX+3.0,2.5),hats=1)
for j in range(5): box(f'obook{j}',(CX-2.05+j*0.2,2.8,1.4),(0.12,0.24,0.26+0.03*(j%2)),flat('book%d'%(j%3),lin([(150,40,40),(40,70,120),(60,110,60)][j%3]),0.6),bv=0.01)
s='S06'; r=SH[s]
ow=char('S06_owner','owner',s,(CX-0.5,1.51,0),r,'neutral',arms=('arm','arm'))
gr=char('S06_partner','granny',s,(CX+0.75,1.45,0),r,'stern',arms=('arm','arm'))
ALL+=[ow,gr]
faces(ow,[(643,'neutral'),(664,'horror'),(673,'angry'),(690,'swirl'),(700,'talkD')])
lipsync(ow,[w for w in WORDS if 23.0<=w[1]<=25.6],700,770)
faces(ow,[(771,'sad')])
faces(gr,[(643,'stern'),(666,'shock'),(680,'stern'),(712,'shock'),(740,'stern'),(756,'shock')]); bob(gr,[666,712,756])
for f,a_ in [(700,-30),(706,-125),(720,-110),(730,-140),(745,-120),(754,-150),(770,-20)]: arm(ow,1,f,a_)
for f,a_ in [(700,-20),(712,-110),(726,-95),(742,-125),(758,-100),(772,-15)]: arm(ow,-1,f,a_)
bob(ow,[664,673,701,710,730,754],amt=9)
path(s,[(643,(CX-2.72,-1.91,2.6),(CX-0.12,1.46,1.15)),(690,(CX-1.95,-0.99,1.95),(CX-0.12,1.46,1.3)),(754,(CX-1.89,-0.91,1.92),(CX-0.12,1.46,1.33)),(781,(CX-1.85,-0.87,1.9),(CX-0.12,1.46,1.35))])
# ======================= S07 / S08 / S09: back in the street (set A) =======================
# ---- S07/S08: the owner thrusts up a hand-held BIG FRIDAY! placard in front of his store (1961); nobody looks; it droops on "not once"
def placard(ch,sx,f_up,f_open,droop=None,held=-25):
    """r7 (owner Nov 19: 'limbs detached, not holding the sign'; rules 270-271): the grip sits exactly on the straight arm card's hand
    (0.407 below the shoulder pivot), the fist card covers the hand + stick, and the stick is counter-rotated every frame so it
    tilts outward (board clear of the face) while carried low and stands upright above the head once raised"""
    piv=ch['A'][sx]['piv']; C=L.chr_coll(ch['shot'])
    hold=empty(ch['inst']+'_hold',(0,0,0),coll=C); hold.parent=piv; hold.location=(0,-0.03,-HAND_Z)
    stick=cyl(ch['inst']+'_stick',(0,0,0),0.022,1.0,flat('stick',lin((150,105,60)),0.7),v=8,coll=C); stick.parent=hold; stick.location=(0,0.0,0.36)
    bp=empty(ch['inst']+'_bpiv',(0,0,0),coll=C); bp.parent=hold; bp.location=(0,0,0.86)
    card=plane(ch['inst']+'_placard',(0,0,0),1.0,0.5,card_mat('placard','placard',emit=0.25),coll=C); card.parent=bp; card.location=(0,-0.032,0)
    back=plane(ch['inst']+'_placardb',(0,0,0),1.0,0.5,card_mat('placard_back','placard_back',emit=0.2),coll=C,face='+Y'); back.parent=bp; back.location=(0,0.032,0)
    fist=plane(ch['inst']+'_fist',(0,0,0),0.15,0.15,card_mat('fist','fist',emit=0.25),coll=C); fist.parent=hold; fist.location=(0,-0.03,0.0)
    for o in (stick,card,back,fist): o['chr']=ch['inst']
    krot(bp,f_open-4,(0,0,math.pi)); krot(bp,f_open+2,(0,0,0))
    arm(ch,sx,f_up,held); arm(ch,sx,f_open,-150)
    if droop: arm(ch,sx,droop[0],-150); arm(ch,sx,droop[1],-130)
    tilt=[(ch['rng'][0],35),(f_up,35),(f_up+4,0)]+([(droop[0],0),(droop[1],14)] if droop else [])
    COUNTER.append((hold,piv,sx,ch['rng'],tilt))
    return hold
COUNTER=[]
HAND_Z=0.407   # straight arm card: hand centre 0.407 below the shoulder pivot (cast.arm hand at canvas y 716 of 900, card 0.558 tall, offset 0.242)
SX=-8.6; SY=47.6   # the owner's spot on the sidewalk in front of Hartwell & Sons
s='S07'; r=SH[s]
o7=char('S07_owner','owner',s,(SX,SY,0.14),r,'hope',arms=('arm','armS'))
ALL.append(o7); faces(o7,[(775,'hope'),(800,'neutral'),(820,'hope'),(846,'hope'),(856,'hope')]); bob(o7,[790,846,856])
arm(o7,-1,775,-15); arm(o7,-1,846,-40); arm(o7,-1,858,-20)
arm(o7,1,775,-30); arm(o7,1,812,-35); placard(o7,1,836,846,held=-140)   # r5 (rule 219): raised on 'name' (836) so the blank back shows <= 8 f before the spin; round 4: board carried low, raised on 'tried', spun to the slogan on 'Big' (was a blank back up for 2 s)
ex=crowd(s,r,[(SX+1.1,SY+3.6,0.14),(SX-0.4,SY+5.2,0.14)],['shopper','granny'],21); ALL+=ex
path(s,[(775,(SX+2.05,SY-1.3,1.75),(SX+0.3,SY+0.2,1.5)),(790,(SX+2.0,SY-1.2,1.75),(SX+0.3,SY+0.25,1.48)),(846,(SX+2.05,SY-1.2,1.8),(SX+0.3,SY+0.3,1.52)),(854,(SX+2.4,SY-1.45,1.82),(SX+0.3,SY+0.3,1.56)),(866,(SX+2.6,SY-1.62,1.86),(SX+0.3,SY+0.3,1.58))])
# round 3: blurred FG mailbox at the lower right of S07 (projection-checked: x 0.6-0.75, stays in frame, no sweep; FG depth layer)
_c7=L.chr_coll('S07'); _mx,_my=SX+1.2,SY-0.3
box('mbS07',(_mx,_my+0.25,0.69),(0.5,0.5,1.0),flat('mailbox',lin((40,70,140)),0.5),coll=_c7,bv=0.12); box('mbS07_slot',(_mx,_my-0.005,0.95),(0.3,0.02,0.05),INK,coll=_c7,bv=0)
for sx_ in(-1,1):
    for sy_ in(-1,1): box(f'mbS07_leg{sx_}{sy_}',(_mx+sx_*0.12,_my+0.25+sy_*0.12,0.15),(0.06,0.06,0.3),INK,coll=_c7,bv=0)
s='S08'; r=SH[s]
o8=char('S08_owner','owner',s,(SX,SY,0.14),r,'hope',arms=('arm','armS'))
c8=char('S08_cop','cop',s,(-7.0,54.0,0.14),r,'deadpan',arms=('arm','arm'),walker=True)
ALL+=[o8,c8]
faces(o8,[(867,'hope'),(884,'neutral'),(897,'sad'),(910,'horror'),(925,'sad')]); bob(o8,[884,910])
faces(c8,[(867,'deadpan'),(895,'smug'),(912,'deadpan')])
placard(o8,1,860,861,droop=(903,912)); arm(o8,1,867,-150); arm(o8,1,912,-130)   # r4: smaller droop (the -112 droop swung the board over the crowd's faces 911-937); arm(o8,-1,867,-15); arm(o8,-1,910,-35)
walk(c8,867,938,(-7.0,54.0,0.14),(-6.85,48.6,0.14),step=3)   # r4: cop lane moved right, clear of the board
# passers-by in depth along the sidewalk: a near lane by the curb (camera right) and a far lane beyond the owner; nobody looks up
# rule 194: every walker comes TOWARD camera (round 3: a walker going away read as a headless brown body 867-930)
sp8=[(-5.14,50.43,0.14),(-7.91,56.08,0.14),(-5.64,56.46,0.14),(-6.55,59.3,0.14),(-9.25,57.92,0.14),(-7.48,60.87,0.14)]   # r4 crowdopt S08 pass 2 BEST 14.93 (placard droop reduced, cop lane right)   # r4 pass3: prop-aware crowdopt
W8=[(0,867,938,0,-2.4),(1,867,938,0,-2.6),(2,867,938,0,-2.4),(3,867,938,0,-2.4),(4,867,938,0,-2.8),(5,867,938,0,-2.6)]
ex=crowd(s,r,sp8,['shopper','tourist','granny','fanblue','kid','fangold'],23,walkers=W8); ALL+=ex
b_=flat('mailbox',lin((40,70,140)),0.5); box('mbS08',(-7.6,43.75,0.69),(0.5,0.5,1.0),b_,coll=L.chr_coll('S08'),bv=0.12)
plane('mbS08_front',(-7.6,43.495,0.72),0.46,0.64,card_mat('mailbox_front','mailbox_front',emit=0.15),coll=L.chr_coll('S08'))
for sx_ in(-1,1):
    for sy_ in(-1,1): box(f'mbS08_leg{sx_}{sy_}',(-7.6+sx_*0.12,43.75+sy_*0.12,0.15),(0.06,0.06,0.3),INK,coll=L.chr_coll('S08'),bv=0)
path(s,[(867,(-7.0,42.4,1.5),(-7.95,47.7,1.6)),(904,(-6.95,42.7,1.5),(-7.95,47.9,1.6)),(938,(-6.9,43.0,1.5),(-7.95,48.1,1.6))])
s='S09'; r=SH[s]
c9=char('S09_cop','cop',s,(0,0,0.64),r,'neutral',arms=('arm','arm_megaphone'))
ALL.append(c9); faces(c9,[(931,'neutral'),(950,'shout'),(966,'grit'),(976,'shout'),(990,'laugh'),(1002,'shout')])
for f,a_ in [(931,-20),(948,-128),(1000,-128)]: arm(c9,1,f,a_)
for f,a_ in [(931,-15),(958,-90),(976,-110),(990,-30)]: arm(c9,-1,f,a_)
bob(c9,[950,968,977,1002],amt=10)
ex=crowd(s,r,[(-7.6,7.6,0.14),(-8.6,8.6,0.14),(7.4,7.8,0.14),(-7.4,-7.6,0.14),(8.2,8.9,0.14)],['granny','shopper','tourist','kid','fangold'],27); ALL+=ex
for i,e in enumerate(ex): faces(e,[(931,'blink'),(934,list(e['F'])[0]),(958+3*i,'shock'),(978+4*i,list(e['F'])[0])])
path(s,[(931,(-2.2,2.4,1.35),(0,0,1.8)),(955,(-1.55,1.75,1.15),(0,0,1.86)),(977,(-1.35,1.5,1.1),(0,0,1.86)),(1013,(-1.32,1.48,1.12),(-0.05,-0.05,1.86))])
# ======================= SET D: the press room (X=900) =======================
DX=900
room('press',DX,10,8,4.5,'precinct','lino')
pm=flat('pressgrey',lin((40,112,112)),0.4,metal=0.5); pk=flat('pressblack',lin((30,30,34)),0.4,metal=0.4)
for sx in(-1,1): box(f'press_side{sx}',(DX+sx*1.6,1.0,1.4),(0.3,2.0,2.8),pm,bv=0.05)
rollers=[]
for j,(y,z,r_) in enumerate([(0.3,0.95,0.32),(1.0,1.55,0.42),(1.7,2.2,0.32),(0.6,2.35,0.22)]):
    rl=cyl(f'roller{j}',(DX,y,z),r_,3.0,pk if j%2 else pm,v=32,rot=(0,math.pi/2,0)); rollers.append(rl)
    for f in range(1008,1060,6): rl.rotation_euler=(math.radians((f-1008)*(-24 if j%2 else 24)),0,0); rl.keyframe_insert('rotation_euler',frame=f)
    L.linear(rl)
web=plane('press_web',(DX,-0.6,0.612),2.6,1.8,flat('newsprint_web',lin((214,206,186)),0.9),horiz=True)
belt=box('press_belt',(DX,-1.8,0.55),(2.0,3.0,0.12),flat('belt',lin((150,44,36)),0.8),bv=0.02)
for sx in(-1,1): box(f'press_beltleg{sx}',(DX+sx*0.9,-1.8,0.25),(0.1,2.6,0.5),pm,bv=0.01)
stack=box('press_stack',(DX,-3.6,0.35),(0.9,1.2,0.7),flat('newsprint',lin((236,230,214))),bv=0.01)
for sx in(-1,1): box(f'press_ink{sx}',(DX+sx*1.6,0.6,3.05),(0.4,0.4,0.5),flat('inkwell',lin((180,40,40)),0.5),bv=0.03)
# sheets ride the belt toward the camera, headlines growing (paper62 -> 66 -> 70)
for j in range(8):
    tex_=['paper62','paper66','paper70'][min(2,j//3)]; f0=1004+j*7
    sh_=plane(f'sheet{j}',(DX,-0.4,0.62),0.8,1.1,card_mat(tex_+'run_s',tex_+'run',emit=0.06),horiz=True)   # round 4: running sheets carry no legible lettering (they always cross the frame edge); only the hero sheet reads
    kloc(sh_,f0,(DX,-0.6,0.616)); kloc(sh_,f0+24,(DX,-3.1,0.616)); L.linear(sh_); vis(sh_,[(max(1008,f0),min(1057,f0+24))])
# hero sheet: the biggest headline slides off the belt and stops whole in frame for the last beat
shH=plane('sheetH',(DX,-0.6,0.63),0.8,1.1,card_mat('paper70_s','paper70',emit=0.06),horiz=True)
kloc(shH,1030,(DX,-1.05,0.63)); kloc(shH,1044,(DX,-2.1,0.63)); vis(shH,[(1030,1057)])
s='S10'
path(s,[(1008,(DX+1.35,-3.5,2.35),(DX,0.7,1.25)),(1024,(DX+0.8,-3.3,2.05),(DX,-0.7,0.85)),(1044,(DX-0.05,-3.0,1.85),(DX,-1.95,0.6)),(1057,(DX-0.05,-3.05,1.9),(DX,-1.95,0.6))])   # r7 (round-6 visual: S10 washed out, all white paper): opens wide on the red belt, rollers and press frame, then settles on the hero sheet
# ======================= SET E: newsstands, town to town (X=1200) =======================
EX=1200
box('E_road',(EX,-6,-0.1),(80,10,0.2),ROADX,bv=0); box('E_walk',(EX,1.5,0.07),(80,5,0.14),WALK,bv=0.03)
for j in range(9): building(f'bE{j}',(EX-32+j*8,4),'-Y',FAC[(j+3)%8],awn=AW[(j+3)%8])
# round 3: the far side of the street (S11 looks along the sidewalk; no void beyond the road), curb lampposts and parked cars
box('E_walk2',(EX,-12.5,0.07),(80,3,0.14),WALK,bv=0.03)
for j in range(9): building(f'bEo{j}',(EX-36+j*8,-14),'+Y',FAC[(j+6)%8],awn=AW[(j+5)%8])
for j,x in enumerate([EX-9.0,EX-17.0,EX-25.0]): lamppost(f'Elp{j}',(x,-0.9))
for j,y in enumerate([-10.0,-2.0,6.0]): building(f'bEend{j}',(EX-42,y),'+X',FAC[(j+1)%8],awn=AW[(j+2)%8])   # closes the street vista (no void at the frame edge)
for j,x in enumerate([EX-12.0,EX-20.5]): car(f'Ecar{j}',(x,-2.7,0.0),90.0,[(60,120,90),(200,170,80)][j])
skE=plane('E_sky',(EX,90,40),260,140,card_mat('skygrey','sky_grey',emit=1.0),coll=L.C_NOI); skE['fly']=1
STANDS=[]
for j in range(4):
    x=EX-5.4+j*3.6; sm=flat('stand%d'%j,lin([(40,70,120),(120,40,40),(40,100,70),(90,60,110)][j]),0.6)
    box(f'stand{j}_body',(x,1.6,0.6),(2.2,1.0,1.2),sm,bv=0.03); box(f'stand{j}_roof',(x,1.45,2.55),(2.6,1.4,0.12),sm,bv=0.03)
    for sx in(-1,1): box(f'stand{j}_post{sx}',(x+sx*1.05,1.9,1.62),(0.08,0.08,1.75),INK,bv=0)
    plane(f'stand{j}_sign',(x,0.738,2.82),2.2,0.55,card_mat(f'standsign{j}',f'stand{j}',emit=0.35))
    box(f'stand{j}_signb',(x,0.78,2.82),(2.3,0.06,0.62),sm,bv=0.01)
    box(f'stand{j}_rack',(x,2.0,1.65),(2.0,0.08,1.0),flat('rack',lin((70,56,44)),0.6),bv=0.01)
    for q in range(3): plane(f'stand{j}_p{q}',(x-0.62+q*0.62,1.94,1.65),0.5,0.68,card_mat(f'town{j}',f'town{j}',emit=0.2))
    for q in range(4): box(f'stand{j}_pile{q}',(x-0.75+q*0.5,1.35,1.24),(0.42,0.56,0.08),flat('newsprint',lin((236,230,214))),bv=0.005)
    STANDS.append(x)
s='S11'; r=SH[s]
pb=char('S11_paperboy','paperboy',s,(EX-6.2,0.05,0.14),r,'shout',arms=('arm','arm_paper'),walker=True)
walk(pb,1051,1125,(EX-6.2,0.05,0.14),(EX-0.3,0.05,0.14),step=2)
ALL.append(pb); faces(pb,[(1051,'shout'),(1068,'happy'),(1072,'shout'),(1092,'happy'),(1100,'shout')]); arm(pb,1,1051,-140); arm(pb,1,1066,-160); arm(pb,1,1080,-130); bob(pb,[1072,1100])
ex=crowd(s,r,[(STANDS[1]+1.45,1.6,0.14),(STANDS[2]+1.5,1.5,0.14),(STANDS[3]+1.45,1.6,0.14),(STANDS[3]+2.6,1.7,0.14)],['tourist','shopper','fanblue','kid'],31); ALL+=ex
path(s,[(1051,(EX+2.85,-0.95,1.72),(EX-3.0,0.56,1.15)),(1125,(EX+2.95,-0.95,1.74),(EX-2.9,0.56,1.17))])   # round 3: near-static camera, the boy walks up to it; stands stay put on screen (signs fully in or out)
for o_ in (L.CAM['S11'],L.TGT['S11']):
    for fc in o_.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            if 1051<=kp.co[0]<=1125: kp.interpolation='LINEAR'
# ======================= SET F: 1981 office + the ledger (X=1500) =======================
FX=1500
room('off81',FX,7,6,3.0,'office81','lino')
box('off81_win',(FX-1.8,2.96,1.8),(1.9,0.08,1.4),flat('winframe81',lin((210,206,196)),0.5),bv=0.02)
plane('off81_view',(FX-1.8,2.9,1.8),1.7,1.2,card_mat('skyline_dawn_v','skyline_dawn',emit=0.7))
for j in range(6): box(f'blind{j}',(FX-1.8,2.905,1.3+j*0.2),(1.7,0.02,0.03),flat('blind',lin((230,226,214)),0.5),bv=0)
desk('fdesk',(FX,0.9,0),w=2.0,m=flat('desk81',lin((90,64,44)),0.4))
beige=flat('beige',lin((214,204,180)),0.5)
box('pc_base',(FX+0.78,1.05,0.86),(0.6,0.5,0.14),beige,bv=0.02); box('pc_mon',(FX+0.78,1.1,1.16),(0.5,0.42,0.42),beige,bv=0.04)
plane('pc_screen',(FX+0.78,0.885,1.18),0.38,0.29,card_mat('screen81','screen81',emit=1.2))
glow('pc_glow',(FX+0.78,0.86,1.18),0.95,(150,255,190),1.6)
box('pc_kb',(FX+0.5,0.7,0.8),(0.5,0.18,0.04),beige,bv=0.01)
plane('cal81',(FX+1.7,2.98,1.9),0.45,0.56,card_mat('calx','calx',emit=0.2))   # round 3: no lettering (the S12 orbit sweeps it across the frame edge); the 1981 date is on the paper
wallframe('fph1',(FX+0.4,2.98,2.15),0.8,0.55,'fac81_2'); wallframe('fph2',(FX-0.55,2.98,2.25),0.36,0.48,'fac81_1'); shelf_items('fshelf',(FX+2.6,2.855,1.6),1.1,21)
cabinet('fcab',(FX+2.8,2.6),h=1.0); sph('plant',(FX-2.8,2.4,1.25),0.45,flat('leafy',lin((60,120,60)),0.7),sc_=(1,1,1.2)); cyl('plantpot',(FX-2.8,2.4,0.4),0.3,0.8,flat('pot81',lin((190,90,60)),0.6),v=18,r2=0.24)
shade=lamp('flamp',(FX-1.0,1.2,0.78),on=(1184,99999))
lm=flat('lampbulb81',lin((255,226,150)),0.4,emit=0.0); bulb=sph('flamp_bulb',(FX-1.0,1.16,1.17),0.05,lm)
# the lamp clicks on with "story" (f1184): bulb + warm point light keyed
p_=bulb.active_material.node_tree.nodes['Principled BSDF']; p_.inputs['Emission Strength'].default_value=0.0; p_.inputs['Emission Strength'].keyframe_insert('default_value',frame=1183)
p_.inputs['Emission Strength'].default_value=12.0; p_.inputs['Emission Strength'].keyframe_insert('default_value',frame=1184)
bpy.ops.object.light_add(type='POINT',location=(FX-1.0,1.0,1.15)); lp=bpy.context.object; lp.name='flamp_light'; lp.data.color=(1,0.8,0.5); lp.data.shadow_soft_size=0.1
lp.data.energy=0; lp.data.keyframe_insert('energy',frame=1183); lp.data.energy=60; lp.data.keyframe_insert('energy',frame=1184)
for fc in lp.data.animation_data.action.fcurves:
    for kp in fc.keyframe_points: kp.interpolation='CONSTANT'
# the ledger (open book on the desk): page swaps red entries -> black entries -> black total
LED_Z=0.786
box('ledger_cover',(FX-0.05,0.85,0.775),(0.66,0.46,0.02),flat('ledgercover',lin((40,60,40)),0.6),bv=0.004)
cyl('pencup',(FX-0.6,0.75,0.86),0.06,0.16,flat('pencup',lin((40,70,120)),0.5),v=16)
for j in range(4): cyl(f'pencil{j}',(FX-0.6+0.015*(j-1.5),0.75,0.98),0.008,0.2,flat('pencil%d'%j,lin([(240,200,60),(196,30,30),(20,20,26),(40,110,60)][j]),0.5),v=8)
cyl('mug81',(FX+0.9,1.15,0.83),0.05,0.1,flat('mug81',lin((200,60,50)),0.4),v=16)
for j in range(4): box(f'paperstack{j}',(FX-0.55,1.0,0.785+0.006*j),(0.3,0.4,0.005),flat('newsprint',lin((236,230,214))),bv=0)
box('stapler',(FX-0.25,1.16,0.81),(0.06,0.18,0.05),flat('stapler',lin((40,40,44)),0.4),bv=0.01)
box('calc81',(FX+0.85,0.68,0.795),(0.16,0.2,0.03),beige,bv=0.005)
for j in range(12): box(f'calckey{j}',(FX+0.8+0.035*(j%4),0.62+0.035*(j//4),0.812),(0.026,0.026,0.008),flat('key81',lin((60,60,64)),0.5),bv=0.002)
ledgers=[plane(f'ledger{i}',(FX-0.05,0.85,LED_Z),0.62,0.413,card_mat(f'ledger{i}',f'ledger{i}',emit=0.3),horiz=True) for i in (0,4)]
vis(ledgers[0],[(0,1300)]); vis(ledgers[1],[(1301,END)])
# ink appears only under the pen (rules 155/166): a blank-page cover sits over the column from the pen tip down to the page foot.
# The cover samples the blank page through the page's own object coordinates, so the paper and ruling match exactly while it shrinks.
PG_X0,PG_Y1=FX-0.05-0.31,0.85+0.2065
def pgx(px): return PG_X0+px*0.62/1536
def pgy(py): return PG_Y1-py*0.413/1024
def ledger_cover(n,px0,px1,page):
    me=bpy.data.meshes.new(n); x0,x1=pgx(px0)-(FX-0.05),pgx(px1)-(FX-0.05)
    me.from_pydata([(x0,0,0),(x1,0,0),(x1,1,0),(x0,1,0)],[],[(0,1,2,3)]); o=bpy.data.objects.new(n,me); L.C_SET.objects.link(o)
    m=bpy.data.materials.new(n+'_m'); N_,L_=L.nodes(m); p_=N_['Principled BSDF']; p_.inputs['Roughness'].default_value=1.0; p_.inputs['Specular IOR Level'].default_value=0.0
    tc=N_.new('ShaderNodeTexCoord'); tc.object=page; mp=N_.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value=(1/0.62,1/0.413,1); mp.inputs['Location'].default_value=(0.5,0.5,0)
    it=N_.new('ShaderNodeTexImage'); it.image=bpy.data.images.load('/root/bf/tex/ledgerN.png',check_existing=True); it.interpolation='Cubic'
    L_.new(tc.outputs['Object'],mp.inputs['Vector']); L_.new(mp.outputs['Vector'],it.inputs['Vector']); L_.new(it.outputs['Color'],p_.inputs['Base Color'])
    L_.new(it.outputs['Color'],p_.inputs['Emission Color']); p_.inputs['Emission Strength'].default_value=0.3
    me.materials.append(m); o.location=(FX-0.05,pgy(1024),LED_Z+0.0006); o['noink']=1; return o
cov_r=ledger_cover('ledger_cover_red',420,775,ledgers[0]); cov_b=ledger_cover('ledger_cover_black',1180,1505,ledgers[1])   # r5: labels pre-printed; the cover hides only the figure column
vis(cov_r,[(0,1300)]); vis(cov_b,[(1301,1347)])
s='S12'; r=SH[s]
x8=char('S12_exec','exec81',s,(FX-0.1,1.5,0),r,'smug',arms=('arm','arm_pen'))
ALL.append(x8); faces(x8,[(1114,'smug'),(1150,'talk'),(1166,'smug'),(1184,'idea'),(1200,'laugh')]); bob(x8,[1184,1200]); arm(x8,1,1170,-30); arm(x8,1,1184,-135); arm(x8,1,1200,-40)   # r7: pen hand beside the head, not over it
import math as _m
orb=[]
# round 4: orbit step 9 -> 4.5 deg (its last 12 f put the monitor over her face)
for i,f in enumerate(range(1114,1219,13)):
    a_=_m.radians(-38+i*4.5); orb.append((f,(FX+3.2*_m.sin(a_),1.5-3.2*_m.cos(a_),1.55+0.05*i),(FX-0.1,1.3,1.45)))
path(s,orb)
# S13 top-down ledger: a flat drawn hand + pen lies on the page, tip on the paper, small strokes (rule 166)
s='S13'; r=SH[s]
C13=L.chr_coll(s)
HL=0.75
card_r=plane('S13_hand_red',(0,0,0),0.12,HL,card_mat('exec81_writehand_red','exec81_writehand_red'),coll=C13,horiz=True)
card_b=plane('S13_hand_black',(0,0,0),0.12,HL,card_mat('exec81_writehand_black','exec81_writehand_black'),coll=C13,horiz=True)
hand_r=empty('S13_hand_red_piv',(0,0,0),coll=C13); hand_b=empty('S13_hand_black_piv',(0,0,0),coll=C13)
for c_,h_ in ((card_r,hand_r),(card_b,hand_b)):
    c_.parent=h_; c_.location=(0,HL/2,0); c_.rotation_euler=(0,0,0); c_['noink']=1
    h_.rotation_euler=(math.radians(24),0,math.radians(18 if h_ is hand_b else -6))   # nib on the page, forearm rises toward the writer, black-pen arm angled clear of the PC
# red-pen hand writes the red column (f1270-1300), black-pen hand the black column (f1306-1345); tips touch the page (z = page + 1 mm)
def strokes(o,cov,f0,f1,x0,y0,y1):
    n=(f1-f0)//3
    for i in range(n+1):
        t=i/max(1,n); f=f0+i*3; y=y0+(y1-y0)*t; kloc(o,f,(x0+(0.006 if i%2 else -0.006),y,LED_Z+0.003))
        cov.scale=(1,max(0.001,y-pgy(1024)),1); cov.keyframe_insert('scale',frame=f)
    cov.scale=(1,pgy(84)-pgy(1024),1); cov.keyframe_insert('scale',frame=f0-1)
    for fc in cov.animation_data.action.fcurves:
        for kp in fc.keyframe_points: kp.interpolation='LINEAR'
TIPX_R,TIPX_B=pgx(630),pgx(1350)
# each hand slides in from beyond the top of the frame (the writer's side), writes its column top to bottom incl. the total, then slides out
kloc(hand_r,1249,(TIPX_R,1.66,LED_Z+0.003)); strokes(hand_r,cov_r,1262,1300,TIPX_R,pgy(112),pgy(992)); kloc(hand_r,1302,(TIPX_R,pgy(992),LED_Z+0.003)); kloc(hand_r,1308,(TIPX_R,1.7,LED_Z+0.003))   # r5: the pen rests on the total 4 f before it leaves
kloc(hand_b,1299,(TIPX_B,1.66,LED_Z+0.003)); strokes(hand_b,cov_b,1306,1345,TIPX_B,pgy(112),pgy(992)); kloc(hand_b,1349,(TIPX_B,pgy(992),LED_Z+0.003)); kloc(hand_b,1354,(TIPX_B,1.7,LED_Z+0.003))
vis(card_r,[(1249,1308)]); vis(card_b,[(1299,1354)])
# r7 (round-6 L9: no foreground in the S13 ledger insert): desk objects near the lens, one per camera set-up, each fixed in its corner for its whole set-up (corners.py)
DZ=0.7815   # r7: 1.5 mm above the desk top (no coplanar contact, rule 228)
def pencup(n,x,y,col):
    cyl(n,(x,y,DZ+0.06),0.042,0.12,flat(n+'_m',lin(col),0.45),v=20,coll=C13); cyl(n+'_rim',(x,y,DZ+0.121),0.044,0.008,INK,v=20,coll=C13)
    for j,(dx,dy,c_) in enumerate([(-0.014,0.008,(240,200,60)),(0.012,-0.01,(196,30,30)),(0.0,0.016,(40,110,60)),(0.016,0.012,(20,20,26))]):
        pc=cyl(f'{n}_p{j}',(x+dx,y+dy,DZ+0.16+0.012*j),0.006,0.2,flat(f'{n}_pc{j}',lin(c_),0.5),v=8,coll=C13); pc.rotation_euler=(math.radians(8*(j-1.5)),math.radians(6*(1.5-j)),0)
cyl('S13_cup',(FX-0.30,1.24,DZ+0.05),0.05,0.1,flat('cup13',lin((236,232,220)),0.35),v=24,coll=C13); cyl('S13_coffee',(FX-0.30,1.24,DZ+0.098),0.043,0.006,flat('coffee',lin((70,40,24)),0.2),v=24,coll=C13)
cyl('S13_saucer',(FX-0.30,1.24,DZ+0.004),0.085,0.008,flat('cup13',lin((236,232,220)),0.35),v=24,coll=C13)
pencup('S13_pencupL',FX-0.23,0.56,(60,90,140)); pencup('S13_pencupR',FX+0.27,0.55,(150,60,50))
path(s,[(1210,(FX-0.05,0.85,2.25),(FX-0.05,0.859,LED_Z)),(1281,(FX-0.11,0.79,1.78),(FX-0.11,0.80,LED_Z)),(1282,(FX-0.13,0.60,1.42),(FX-0.13,0.70,LED_Z)),(1318,(FX-0.13,0.61,1.40),(FX-0.13,0.70,LED_Z)),(1319,(FX+0.15,0.785,1.51),(FX+0.15,0.796,LED_Z)),(1344,(FX+0.11,0.79,1.45),(FX+0.11,0.802,LED_Z)),(1359,(FX+0.11,0.79,1.45),(FX+0.11,0.802,LED_Z))])   # round 4: totals whole in frame or fully out (rule 206)
# S14: ledger total turns the books from red to black, pull back and up to the exec's wink
s='S14'; r=SH[s]
x14=char('S14_exec','exec81',s,(FX-0.1,1.5,0),r,'smug',arms=('arm','arm_redpen'))
ALL.append(x14); faces(x14,[(1352,'smug'),(1400,'talk'),(1420,'smug'),(1454,'idea'),(1468,'wink'),(1480,'laugh')]); bob(x14,[1468])
path(s,[(1352,(FX+0.11,0.79,1.45),(FX+0.11,0.802,LED_Z)),(1400,(FX+0.13,0.72,1.5),(FX+0.12,0.88,LED_Z+0.02)),(1403,(FX+0.13,0.70,1.5),(FX+0.12,0.885,LED_Z+0.02)),(1404,(FX+0.30,-0.62,1.6),(FX-0.04,1.44,1.3)),(1416,(FX+0.32,-0.9,1.6),(FX-0.05,1.45,1.3)),(1440,(FX+0.35,-1.2,1.6),(FX-0.08,1.5,1.38)),(1467,(FX+0.3,-1.9,1.6),(FX-0.1,1.5,1.25)),(1487,(FX+0.2,-2.1,1.62),(FX-0.1,1.5,1.22))])
hardcut('S13',1282); hardcut('S13',1319)   # r5: hard cuts on 'red' (1282) and 'and' (1319): red-column close-up, then black column
# round 4: the ledger->bookkeeper crane cut her head for 8 frames (C4); now a hard cut at 1403/1404 (CONSTANT key)
for o_ in (L.CAM[s],L.TGT[s]):
    for fc in o_.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            if int(round(kp.co[0]))==1403: kp.interpolation='CONSTANT'
# r5 (round-4 text/shots): the ledger TOTAL sat in the caption band / bottom UI zone (71-81 % H) and the left page's lettering was cut by the frame edge.
# Nudge the S13 black-column and S14 opening keys so the total sits near 64 % H and the gutter just outside the left edge (ledproj check).
def nudge(shot,frames,dx,dy):
    for o_ in (L.CAM[shot],L.TGT[shot]):
        for fc in o_.animation_data.action.fcurves:
            if fc.array_index>1: continue
            for kp in fc.keyframe_points:
                if int(round(kp.co[0])) in frames:
                    d_=dx if fc.array_index==0 else dy; kp.co[1]+=d_; kp.handle_left[1]+=d_; kp.handle_right[1]+=d_
            fc.update()
NUDGE={('S13',1282):(0.016,0.0),('S13',1318):(0.016,0.0),('S13',1319):(0.0,-0.043),('S13',1344):(0.026,-0.0625),('S13',1359):(0.035,-0.055),('S14',1352):(0.051,-0.055),('S14',1400):(0.086,-0.118),('S14',1403):(0.086,-0.118)}
for (sh_,f_),(dx_,dy_) in NUDGE.items(): nudge(sh_,[f_],dx_,dy_)
# ======================= SET H: 1981 downtown at dawn, Hartwell's (X=1800) =======================
HX=1800
box('H_road',(HX,-7,-0.1),(90,10,0.2),ROADX,bv=0); box('H_walk',(HX,0,0.07),(90,5,0.14),WALK,bv=0.03)
building('deptH',(HX,2.5),'-Y','dept81',w=16,h=12,d=10,side='dept81',cap=(90,80,70))
for j,x in enumerate([HX-16,HX-24,HX+16,HX+24,HX-32,HX+32]): building(f'bH{j}',(x+(4 if x>HX else -4),2.5),'-Y',f'fac81_{j%4}',awn=AW[j],side=f'fac81_{j%4}')
skH=plane('H_sky',(HX,120,50),300,170,card_mat('skydawn','sky_dawn',emit=1.0),coll=L.C_NOI); skH['fly']=1
slH=plane('H_skyline',(HX,100,18),240,240*1400/4096,card_mat('skyline_dawn','skyline_dawn',emit=0.6),coll=L.C_NOI); slH['fly']=1
for j,x in enumerate([HX-12,HX+5.3,HX+12]): lamppost(f'Hlp{j}',(x,-2.0))   # r7: pole moved off the payoff crowd's faces (occprobe)
# the payoff window display: a lit 3D bay in front of the left window bay, poster framed on an easel
WX=HX-5.6; WY=1.6
win=flat('bayframe',lin((40,60,46)),0.5)
box('bay_floor',(WX,WY,0.45),(3.0,1.6,0.9),win,bv=0.03); box('bay_top',(WX,WY,3.65),(3.2,1.7,0.3),win,bv=0.03)
for sx in(-1,1): box(f'bay_post{sx}',(WX+sx*1.5,WY-0.75,2.27),(0.14,0.14,2.46),win,bv=0.02)
box('bay_back',(WX,WY+0.78,2.27),(2.9,0.08,2.46),surf('baywall','window81',(1.5,1.5)),bv=0)
plane('bay_sign',(WX,WY-0.86,4.12),2.6,0.65,card_mat('banner81x','banner81x',emit=0.3))   # round 3: textless festive sign (the payoff push always cropped its lettering)
PW,PH=1.0,1.5; PZ=0.9+0.12+PH/2+0.14
easel=flat('easel',lin((120,80,50)),0.6)
for sx in(-1,1): box(f'easel_leg{sx}',(WX+sx*0.42,WY+0.25,0.9+1.05),(0.06,0.06,2.1),easel,bv=0)
box('easel_shelf',(WX,WY+0.16,1.06),(1.2,0.2,0.06),easel,bv=0.01)
box('poster_frame',(WX,WY+0.2,PZ),(PW+0.14,0.05,PH+0.14),flat('pframe',lin((30,24,20)),0.4),bv=0.012)
pmat=bpy.data.materials.new('poster'); N_,L_=L.nodes(pmat); pp_=N_['Principled BSDF']; it_=N_.new('ShaderNodeTexImage'); it_.image=bpy.data.images.load('/root/bf/poster_2k.png'); it_.interpolation='Cubic'
L_.new(it_.outputs['Color'],pp_.inputs['Base Color']); L_.new(it_.outputs['Color'],pp_.inputs['Emission Color']); pp_.inputs['Emission Strength'].default_value=0.12   # r5: round-4 grey 137 vs file 117 (washed);   # round 4: 0.6 washed the poster out (grey 142 vs file 117); pp_.inputs['Roughness'].default_value=0.7; pp_.inputs['Specular IOR Level'].default_value=0.05
poster=plane('poster',(WX,WY+0.17,PZ),PW,PH,pmat,coll=L.C_NOI); poster['noink']=1
# r5 (round-4 E2): before the payoff the display is wrapped in kraft paper, so the poster is never seen small, cut by the frame edge or behind a post (1593-1679); unwrapped on the hard cut at 1688
pcov=box('poster_cover',(WX,WY+0.155,PZ),(PW+0.16,0.012,PH+0.16),flat('kraft',lin((176,138,96)),0.85),bv=0.006)
for f_,h_ in ((1556,False),(1687,False),(1688,True)):
    pcov.hide_render=h_; pcov.keyframe_insert('hide_render',frame=f_); pcov.hide_viewport=h_; pcov.keyframe_insert('hide_viewport',frame=f_)
for fc_ in pcov.animation_data.action.fcurves:
    for k_ in fc_.keyframe_points: k_.interpolation='CONSTANT'
gifts('bay_gifts',(WX-1.0,WY+0.1,0.9),k=3,seed=12); gifts('bay_gifts2',(WX+1.0,WY,0.9),k=4,seed=13)
bpy.ops.object.light_add(type='AREA',location=(WX,WY-0.6,3.3),rotation=(math.radians(35),0,0)); bl=bpy.context.object; bl.name='bay_light'; bl.data.energy=700; bl.data.size=1.6; bl.data.color=(1,0.9,0.75)
# r6 (round-5 R19): bright payoff - front fill on the bay so highlights reach p98 >= .84
bpy.ops.object.light_add(type='AREA',location=(WX,WY-2.6,1.9),rotation=(math.radians(80),0,0)); fl_=bpy.context.object; fl_.name='bay_fill'; fl_.data.energy=350; fl_.data.size=2.4; fl_.data.color=(1,0.93,0.82)
# doors of the store slide open on "became" (f1646)
dm=flat('doors81',lin((60,70,80)),0.2,metal=0.4)
for sx in(-1,1):
    d_=box(f'doorH{sx}',(HX+0.0+sx*0.95,2.42,1.4),(1.8,0.08,2.8),dm,bv=0.02)
    kloc(d_,1640,(HX+sx*0.95,2.42,1.4)); kloc(d_,1660,(HX+sx*2.6,2.42,1.4))
    dp_=plane(f'doorH{sx}_face',(0,0,0),1.7,2.66,card_mat('door81','door81',emit=0.25)); dp_.parent=d_; dp_.location=(0,-0.045,0)
plane('doorH_int',(HX,2.47,1.4),3.6,2.8,card_mat('storeint','storeint',emit=0.9))
# round 3: depth layer beside the S15 cop (lamppost stays in frame left through the drift; no FG sweep)
lamppost('Hlp_S15',(HX+8.28,0.04))
s='S15'; r=SH[s]
o15=char('S15_oldcop','oldcop',s,(HX+9.0,-0.9,0.14),r,'deadpan',arms=('armS','armS'))   # r7 (rule 271): straight arms whose hands end under the grip cards
ALL.append(o15)
pap=plane('S15_paper',(0,0,0),0.62,0.85,card_mat('paper81','paper81',emit=0.3),coll=L.chr_coll(s)); pap.parent=o15['root']; pap.location=(0,-0.03,0.60)   # r7: round bodies are 1.118x taller
vis(pap,[r]); pap['chr']='S15_oldcop'
for sx_,tx_ in ((-1,'grip_L'),(1,'grip_R')):
    g_=plane(f'S15_grip{sx_}',(0,0,0),0.17,0.223,card_mat(tx_,tx_,emit=0.25),coll=L.chr_coll(s)); g_.parent=o15['root']; g_.location=(sx_*0.355,-0.045,0.565); g_['chr']='S15_oldcop'; vis(g_,[r])
faces(o15,[(1481,'deadpan'),(1489,'raise'),(1505,'deadpan'),(1519,'eyeroll'),(1540,'smug'),(1552,'deadpan')]); bob(o15,[1489,1519])
arm(o15,-1,1481,-21.4); arm(o15,1,1481,-21.4); arm(o15,1,1519,-20); arm(o15,1,1540,-21.4)   # r7: hand centre lands on the grip at (0.355,0.565) (shoulder 0.21,0.944)
path(s,[(1481,(HX+8.0,-3.6,1.3),(HX+9.0,-0.9,1.0)),(1537,(HX+8.4,-3.25,1.35),(HX+9.0,-0.9,1.08)),(1565,(HX+8.9,-3.0,1.4),(HX+9.0,-0.9,1.16))])
# round 4 (L9): blurred FG litter bin at the lower right of S15 (fgcheck.py: x 0.67-1.27, y <= 0.37 for the whole shot, no sweep)
_c15=L.chr_coll('S15'); cyl('binS15',(HX+9.35,-1.6,0.42),0.24,0.84,flat('bin',lin((50,84,60)),0.6),v=20,coll=_c15); cyl('binS15_rim',(HX+9.35,-1.6,0.86),0.26,0.05,flat('binrim',lin((36,60,44)),0.5),v=20,coll=_c15)
s='S16'; r=SH[s]
sp=[(HX+0.01,0.13,0.14),(HX-2.10,-3.30,0.14),(HX+6.80,-5.60,0.14),(HX-2.69,0.79,0.14),(HX+3.75,-1.41,0.14),(HX+4.29,0.65,0.14),(HX+5.83,-2.20,0.14),(HX+1.34,3.44,0.14),(HX+4.03,-0.19,0.14)]   # r7: crowdopt 1576-1686 on the taller round bodies (74.7 -> 49.1); x2 kid moved out of the shot (its near head covered three faces in every candidate spot)   # r6: crowdopt on the new cameras (238.8 -> 66.1)   # r5: crowdopt 1556-1700 (wide + crowd-surge insert), 20.3 -> 11.9
ordr=sorted(range(len(sp)),key=lambda i:sp[i][0]); SLOT=[(HX-2.2,1.0),(HX-1.6,1.9),(HX-1.0,0.9),(HX-0.4,1.85),(HX+0.2,0.95),(HX+0.8,1.9),(HX+1.4,0.9),(HX+2.0,1.85),(HX+2.6,1.0),(HX+3.2,1.9)]
ex=crowd(s,r,sp,['mullet','perm','kid','granny','shopper','tourist','perm','fanblue','kid'],41,faces_pool='glad'); ALL+=ex
# r5 (round-4 P3/R21): no identical line-up gesture. Each extra gets its own action, offsets and timing (pointing, waving, hugging a bag, cheering, shrugging)
GEST=[[(1,1640,-20),(1,1652,-150),(1,1678,-115)],          # x0 cheer, fist up
      [(-1,1644,-70),(-1,1672,-35)],                         # x1 points across at the window
      [(1,1648,-45),(-1,1648,-45)],                          # x2 kid hugs the bag up
      [(1,1642,-95),(-1,1650,-95),(1,1680,-40)],             # x3 granny both hands up, then one down
      [(-1,1654,-25),(1,1666,-60)],                          # x4 shopper shifts the bag, small wave
      [(1,1646,-130),(1,1658,-100),(1,1670,-130)],           # x5 tourist waves
      [],                                                    # x6 just watches
      [(-1,1650,-160),(-1,1676,-140)],                       # x7 fan pennant up high
      [(1,1660,-55)]]                                        # x8 kid tugs
for i,e in enumerate(ex):
    bob(e,[1647+(5*i)%13,1667+(7*i)%17],amt=6+(i%3)*4)
    for sx_,f_,d_ in GEST[i%len(GEST)]: arm(e,sx_,f_,d_)
# r5 (L9): FG stack of tied shopping boxes at the lower-left corner (fgfine: rises in from the bottom edge 1595-1604, held in the corner to 1687, never crosses a face)
def boxstack(n,x,y):
    cols=[(176,46,40),(46,84,140),(220,190,120)]; rib=flat('ribbon',lin((236,214,90)),0.5)
    zs=0.0
    for k,(w_,d_,h_) in enumerate([(0.52,0.42,0.36),(0.42,0.36,0.30),(0.32,0.30,0.22)]):
        c_=(x+0.03*k,y-0.02*k,zs+h_/2); box(f'{n}_b{k}',c_,(w_,d_,h_),flat(f'giftbox{k}',lin(cols[k]),0.6),bv=0.015)
        box(f'{n}_r{k}a',c_,(w_+0.008,0.05,h_+0.008),rib,bv=0.0); box(f'{n}_r{k}b',c_,(0.05,d_+0.016,h_+0.016),rib,bv=0.0)   # bigger than ribbon a: no coplanar overlap (rule 228)
        zs+=h_+0.011   # rests 3 mm above the ribbon top (rule 228), no visible gap
boxstack('S16_fgbox',HX+2.2,-4.5)
def _glad(e,alt=False):   # r5: S16 crowd reacts with delight, never a stern/angry card (round-4: purple 'stern' granny)
    pref=(['wow','shock','cheer','excited','happy'] if alt else ['happy','excited','cheer','wow','shock'])
    return next(f for f in pref if f in e['F'])
for i,e in enumerate(ex): faces(e,[(1640+3*i,_glad(e,True)),(1652+2*i+(i%3)*3,_glad(e)),(1690+2*i,_glad(e,i%2==1))])
path(s,[(1556,(HX+1.2,-9.5,1.9),(HX,1.0,2.4)),(1590,(HX+4.6,-4.9,2.0),(HX-0.6,0.2,1.55)),(1616,(HX+6.3,-4.0,2.1),(HX-1.0,0.4,1.5)),(1645,(HX+6.2,-3.5,1.95),(HX-0.8,0.4,1.5)),(1646,(HX-5.2,-4.4,1.15),(HX+2.0,0.6,1.42)),(1687,(HX-4.9,-4.1,1.2),(HX+2.0,0.6,1.46)),(1688,(WX+2.4,-4.9,1.7),(WX,WY+0.02,1.76)),
        (1718,(WX+1.5,-4.3,1.66),(WX,WY+0.06,1.7)),   # r5: hard cuts on 'became' (1646, low crowd-surge insert) and 'we' (1688, poster bay), crash push 1718-1727 on 'purpose'   # r4 K8: slow drift through 'show', crash push 1718-1727 lands on 'purpose'
       (1727,(WX+0.15,-1.85,PZ+0.05),(WX,WY+0.17,PZ-0.05)),(END,(WX+0.05,-1.72,PZ+0.04),(WX,WY+0.17,PZ-0.05))])
hardcut('S16',1646); hardcut('S16',1688)
# r6: the near perm shopper steps out of the 1646-1687 insert (her card covered the faces behind her): root scaled to ~0 for the insert only
for _i in (1,7):   # r7: x7 fanblue also steps out of the insert (only its body showed beside the door; face fully behind the door)
    _r=bpy.data.objects[ex[_i]['inst']]
    for f_,v_ in ((1645,1.0),(1646,0.0001),(1687,0.0001),(1688,1.0)): _r.scale=(v_,)*3; _r.keyframe_insert('scale',frame=f_)
    for fc_ in _r.animation_data.action.fcurves:
        if fc_.data_path=='scale':
            for k_ in fc_.keyframe_points: k_.interpolation='CONSTANT'
# r6 (round-5 payoff note): shoppers crowd the window bay on "we all show up" (never in front of the poster; out of the final close-up)
exw=crowd(s,r,[(WX-1.31,WY-1.0,0.14),(WX+1.29,WY-1.18,0.14),(WX-1.92,WY-1.74,0.14)],['shopper','kid','perm'],77,faces_pool='glad',base=20); ALL+=exw
for i,e in enumerate(exw): faces(e,[(1688,_glad(e,i%2==0)),(1712+3*i,_glad(e,i%2==1))]); bob(e,[1700+4*i,1722],amt=6)
# r7: arm snaps first, then finish() (it reads the final arm angles to pick straight cards)
# round 5 (P3): arms hold poses and snap (hold, then a 2-frame change) instead of easing continuously; work arms in S05/S13 keep their strokes
for o_ in bpy.data.objects:
    if not re.search(r'_ap-?1$',o_.name) or o_.name.startswith(('S05_','S13_')) or not o_.animation_data or not o_.animation_data.action: continue
    for fc_ in o_.animation_data.action.fcurves:
        if fc_.data_path!='rotation_euler': continue
        ks_=sorted((k.co[0],k.co[1]) for k in fc_.keyframe_points)
        for (f0_,v0_),(f1_,v1_) in zip(ks_,ks_[1:]):
            if f1_-f0_>4 and abs(v1_-v0_)>0.05: fc_.keyframe_points.insert(f1_-2,v0_,options={'FAST'})
        for k in fc_.keyframe_points: k.interpolation='LINEAR'
        fc_.update()
        _P3N=globals().get('_P3N',0)+1; globals()['_P3N']=_P3N
print('P3 curves',globals().get('_P3N',0))
# r7: placard sticks counter-rotated per frame against the final (snapped) arm angle
for hold_,piv_,sx_,rng_,tilt_ in COUNTER:
    fc_=next(c for c in piv_.animation_data.action.fcurves if c.data_path=='rotation_euler' and c.array_index==1)
    for g in range(rng_[0],rng_[1]+1):
        w_=tilt_[0][1]
        for (fa,wa),(fb,wb) in zip(tilt_,tilt_[1:]):
            if fa<=g<=fb: w_=wa+(wb-wa)*((g-fa)/max(1,fb-fa)); break
            if g>fb: w_=wb
        krot(hold_,g,(0,math.radians(w_)*sx_-fc_.evaluate(g),0))
# ======================= finish =======================
for a in ALL: finish(a)
world_and_sun()
# indoor fill lights (sets are far apart; area lights only reach their own set)
for x,e_ in [(BX,1100),(CX,900),(DX,1000),(FX,850)]:
    bpy.ops.object.light_add(type='AREA',location=(x,-3.0,3.6),rotation=(math.radians(58),0,0)); a_=bpy.context.object; a_.data.energy=e_; a_.data.size=6; a_.data.color=(1.0,0.94,0.86)
print('hulls',L.ink())
L.render_setup(100,8)
for m in bpy.data.materials: m.use_fake_user=True
bpy.ops.wm.save_as_mainfile(filepath='/root/bf/blend/bf.blend'); print('SCENE_OK all')
