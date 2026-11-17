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
LENS={'S01':30,'S02':28,'S03':32,'S04':30,'S05':26,'S06':32,'S07':28,'S08':24,'S09':26,'S10':40,'S11':24,'S12':30,'S13':38,'S14':34,'S15':34,'S16':30}
for n in SH: cam(n,LENS[n],5.6)
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
def lamppost(n,loc):
    cyl(n+'_base',(loc[0],loc[1],0.25),0.16,0.5,INK,v=12); cyl(n+'_pole',(loc[0],loc[1],2.4),0.07,4.0,INK,v=10)
    cyl(n+'_cap',(loc[0],loc[1],4.45),0.12,0.1,INK,v=12); sph(n+'_glob',(loc[0],loc[1],4.75),0.28,LAMPG,sc_=(1,1,1.15))
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
    box(n+'_cap',(cx+ax[0]*0.2,cy+ax[1]*0.2,h+0.25),(sx_+0.4+abs(ax[0])*0.4,sy_+0.4+abs(ax[1])*0.4,0.5),capm,bv=0.04)
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
    for seg,(x0,x1) in enumerate([(-90,-6),(6,90)]):
        box(f'walkx{sx}{seg}',((x0+x1)/2,sx*8,0.07),(x1-x0,4,0.14),WALK,bv=0.03)
    for sy in(-1,1): box(f'walkc{sx}{sy}',(sx*8,sy*8,0.07),(4,4,0.14),WALK,bv=0.03)
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
            x=side_*(14+i*8)
            building(f'bX{k}',(x,sy*10),face_,FAC[k%8],awn=AW[k%8]); k+=1
# far skyline with City Hall + sky cards at both street ends and both cross-street ends
for nme,loc,fc,w_ in [('N',(0,170,24),'-Y',260),('S',(0,-150,24),'+Y',260),('E',(150,0,24),'-X',260),('W',(-150,0,24),'+X',260)]:
    sk=plane('sky'+nme,(loc[0]*1.3,loc[1]*1.3,60),w_*1.6,200,card_mat('skyday','sky_day',emit=1.0),coll=L.C_NOI,face=fc); sk['fly']=1
    sl=plane('skyline'+nme,loc,w_,w_*1400/4096,card_mat('skyline50','skyline50',emit=0.55),coll=L.C_NOI,face=fc); sl['fly']=1
# street furniture
for sx in(-1,1):
    for y in range(-70,104,14):
        if abs(y)<9 or (sx<0 and 34<y+3<62): continue
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
for i,y in enumerate([-46,-22,22,70,86]):
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
def crowd(shot,rng,spots,kinds,seed,walkers=None,faces_pool=None,camname=None):
    """extras: spots=[(x,y,z)], walkers: list of (i, f0, f1, dx, dy)"""
    rr=random.Random(seed); out=[]
    for i,p in enumerate(spots):
        kd=kinds[i%len(kinds)]; wk=bool(walkers and any(w[0]==i for w in walkers))
        props=CI_PROPS.get(kd,[])
        arms_=('arm','arm_'+props[0]) if props and rr.random()<0.6 else ('arm','arm')
        ch=char(f'{shot}_x{i}_{kd}',kd,shot,p,rng,arms=arms_,walker=wk,camname=camname)
        fl=list(L.CI[kd]['faces']); fl=[f for f in fl if f!='blink']
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
s='S01'; r=SH[s]
cop=char('S01_cop','cop',s,(0,0,0.64),r,'whistle',arms=('arm','arm')); ALL.append(cop)
faces(cop,[(0,'whistle'),(28,'annoyed'),(60,'grit'),(88,'shout'),(106,'annoyed'),(128,'shock'),(140,'whistle')])
for f,a in [(0,-150),(14,-160),(24,-120),(46,-155),(70,-95),(90,-160),(118,-140),(136,-165)]: arm(cop,1,f,a)
for f,a in [(0,-60),(30,-90),(60,-40),(96,-95),(140,-70)]: arm(cop,-1,f,a)
bob(cop,[8,30,62,90,128])
ex=crowd(s,r,[(7.6,-8.2,0.14),(8.6,-7.4,0.14),(-7.8,-7.6,0.14),(-8.6,8.0,0.14),(7.7,8.3,0.14),(9.0,-9.0,0.14),(-9.2,-8.8,0.14)],
         ['shopper','fanblue','tourist','granny','fangold','kid','shopper'],5); ALL+=ex
path(s,[(0,(1.0,-2.05,0.95),(0,0.2,1.9)),(45,(0.45,-2.3,0.95),(0,0.2,1.92)),(100,(-0.5,-2.25,1.0),(0,0.2,1.92)),(126,(-0.75,-2.5,1.1),(0,0.3,1.9)),
        (136,(-2.5,-6.5,4.0),(0,1.0,1.4)),(152,(-6.0,-15.0,9.5),(0,2.0,0.8)),(170,(-6.8,-17.0,10.6),(0.2,2.4,0.8))])
# ---------- S02 (163-297): high crane over the day-after-Thanksgiving street, the town rushes downtown ----------
s='S02'; r=SH[s]
sp=[];W=[]
for i in range(26):
    sx=-1 if i%2 else 1; y=16+2.3*(i//2); x=sx*(7.6+0.5*((i//2)%4)); sp.append((x,y,0.14))
    if i%3!=2: W.append((i,163,297,0,-4.5))
ex=crowd(s,r,sp,['shopper','tourist','fanblue','fangold','granny','kid','shopper','fanblue'],9,walkers=W); ALL+=ex
path(s,[(163,(1.0,-14,26),(0,26,0)),(205,(1.6,-10,15),(0,24,1.0)),(251,(2.4,-4.5,5.2),(0,22,1.8)),(297,(2.6,-2.6,3.6),(0,20,2.0))])
# ---------- S03 (292-432): sidewalk truck past shoppers, the tourist and the football fans ----------
s='S03'; r=SH[s]
sho=char('S03_shopper','shopper',s,(8.2,-29.0,0.14),r,'happy',arms=('arm_bag','arm_box'))
tou=char('S03_tourist','tourist',s,(8.3,-26.2,0.14),r,'lost',arms=('arm','arm_camera'))
fb=char('S03_fanblue','fanblue',s,(8.0,-21.6,0.14),r,'cheer',arms=('arm','arm_pennant'))
fg=char('S03_fangold','fangold',s,(8.4,-20.4,0.14),r,'shout',arms=('arm_pennant','arm'))
ALL+=[sho,tou,fb,fg]
faces(sho,[(292,'happy'),(304,'shock'),(318,'happy'),(352,'angry'),(372,'happy')]); bob(sho,[296,318])
faces(tou,[(292,'lost'),(312,'happy'),(334,'lost'),(346,'happy'),(380,'lost')]); arm(tou,1,292,-20); arm(tou,1,308,-115); arm(tou,1,330,-120); arm(tou,1,342,-30); bob(tou,[312])
faces(fb,[(292,'cheer'),(352,'shout'),(366,'cheer'),(392,'shout'),(408,'cheer')]); faces(fg,[(292,'shout'),(352,'cheer'),(366,'shout'),(392,'cheer'),(410,'shout')])
for f in range(352,432,8): arm(fb,1,f,-150 if (f//8)%2 else -120); arm(fg,-1,f+3,-150 if (f//8)%2 else -120)
bob(fb,[358,392]); bob(fg,[361,396])
ex=crowd(s,r,[(9.2,-31.5,0.14),(9.3,-24.0,0.14),(9.2,-18.2,0.14),(7.2,-34,0.14)],['granny','kid','shopper','tourist'],13,walkers=[(3,292,432,0,9.0)]); ALL+=ex
path(s,[(292,(5.6,-30.0,1.3),(8.3,-28.4,1.45)),(330,(5.65,-27.2,1.3),(8.4,-25.8,1.45)),(366,(5.6,-23.4,1.3),(8.2,-21.6,1.5)),(400,(5.65,-21.6,1.3),(8.2,-20.6,1.55)),(432,(5.7,-20.6,1.35),(8.2,-19.9,1.5))])
# ---------- S04 (426-528): high over the jam, dive to the thief swiping a gift box on "thieves" (f487) ----------
s='S04'; r=SH[s]
sh4=char('S04_shopper','shopper',s,(8.3,-12.4,0.14),r,'happy',arms=([(426,'arm_bag'),(489,'arm')],[(426,'arm_box'),(489,'arm')]))
th=char('S04_thief','thief',s,(8.4,-17.0,0.14),r,'sneaky',arms=('arm',[(426,'arm'),(489,'arm_box')]),walker=True)
ALL+=[sh4,th]
walk(th,446,486,(8.4,-17.0,0.14),(8.4,-13.15,0.14),step=3); walk(th,493,528,(8.4,-13.15,0.14),(8.6,-5.0,0.14),step=2)
faces(th,[(426,'sneaky'),(470,'grin'),(486,'sneaky'),(492,'grin'),(512,'shock')]); arm(th,1,478,-20); arm(th,1,486,-70); arm(th,1,491,-15)
faces(sh4,[(426,'happy'),(492,'shock'),(503,'angry'),(518,'shock')]); arm(sh4,-1,492,-150); arm(sh4,1,494,-140); bob(sh4,[492,503])
ex=crowd(s,r,[(9.4,-15.4,0.14),(9.4,-9.6,0.14),(9.3,-7.6,0.14),(9.2,-19.5,0.14),(-7.6,-12,0.14),(-8.4,-9,0.14)],['granny','tourist','kid','fanblue','shopper','fangold'],17); ALL+=ex
path(s,[(426,(2.6,-9.0,30.0),(1.0,-4.0,0.0)),(452,(3.0,-10.0,24.0),(2.0,-6.0,0.0)),(487,(6.0,-15.8,1.6),(8.4,-12.8,1.4)),(510,(6.1,-14.6,1.55),(8.5,-10.6,1.4)),(528,(6.2,-13.4,1.55),(8.5,-8.0,1.35))])
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
def lamp(n,c,on=None,col=(255,220,150)):
    b=flat('brass',lin((180,140,60)),0.3,metal=0.8); cyl(n+'_b',(c[0],c[1],c[2]+0.02),0.1,0.04,b,v=14); cyl(n+'_s',(c[0],c[1],c[2]+0.22),0.015,0.4,b,v=8)
    sh=cyl(n+'_shade',(c[0],c[1]-0.04,c[2]+0.45),0.16,0.14,flat(n+'_shm',lin((40,110,70)),0.5),v=16,r2=0.06)
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
    plane(n+'_pic',(c[0]+ax[0]*0.006,c[1]+ax[1]*0.006,c[2]),w,h,card_mat(tex+'_pic',tex,emit=0.2),face=face)
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
BOARD_Z=1.6
box('board_frame',(BX,3.47,BOARD_Z),(2.5,0.08,1.7),flat('boardwood',lin((110,76,44)),0.6),bv=0.02)
boards=[plane(f'board{i}',(BX,3.42,BOARD_Z),2.4,1.6,card_mat(f'board{i}',f'board{i}',emit=0.35)) for i in range(6)]
box('chalktray',(BX,3.36,BOARD_Z-0.84),(2.4,0.14,0.05),flat('boardwood',lin((110,76,44))),bv=0.01)
desk('pdesk',(BX-3.0,1.6)); phone('pphone',(BX-3.3,1.6,0.78)); L_=lamp('plamp',(BX-2.5,1.8,0.78))
box('typew',(BX-2.9,1.45,0.86),(0.4,0.3,0.16),flat('typew',lin((50,56,52)),0.4),bv=0.03)
for j in range(3): cyl(f'mug{j}',(BX-3.6+j*0.1,1.4,0.84),0.04,0.11,flat('mug',lin((230,226,214)),0.4),v=12)
cabinet('pcab1',(BX+3.9,2.9)); cabinet('pcab2',(BX+3.3,2.9)); coatrack('prack',(BX-4.0,2.8))
wallclock('pclock',(BX+2.3,3.28,2.75)); cyl('cooler',(BX+2.6,2.9,0.5),0.18,1.0,flat('cooler',lin((200,200,190)),0.4),v=16); sph('coolerjug',(BX+2.6,2.9,1.22),0.2,flat('jug',lin((150,200,230)),0.1))
box('pbench',(BX-1.2,-1.6,0.24),(1.6,0.4,0.05),flat('deskwood',lin((110,70,44))),bv=0.01)
for sx in(-1,1): box(f'pbenchl{sx}',(BX-1.2+sx*0.7,-1.6,0.11),(0.06,0.36,0.22),INK,bv=0)
plane('pwanted',(BX-2.4,3.49,2.0),0.5,0.65,card_mat('paper62s','paper62',emit=0.15))
plane('pmap',(BX+3.2,3.49,2.1),1.1,0.75,card_mat('skyline50s','skyline50',emit=0.2))
wallframe('pph1',(BX-3.6,3.48,2.35),0.5,0.4,'fac3'); wallframe('pph2',(BX-1.75,3.48,2.6),0.35,0.45,'paper66'); wallframe('pph3',(BX+1.75,3.48,2.65),0.4,0.3,'fac5')
box('pcork',(BX+3.2,3.47,1.25),(1.0,0.04,0.6),flat('cork',lin((176,130,84)),0.8),bv=0.01)
for j in range(5): plane(f'pnote{j}',(BX+2.82+j*0.19,3.445,1.25+0.12*((j%2)*2-1)),0.16,0.22,card_mat('town%d_n'%(j%4),'town%d'%(j%4),emit=0.15))
shelf_items('pshelf',(BX-3.0,3.36,1.55),1.6,5)
# board swaps: roster -> stamped (on "off" f574) -> chalk BLACK FRIDAY letter by letter (f606-628)
BT=[(0,573),(574,605),(606,615),(616,621),(622,627),(628,END)]
for b_,(a_,z_) in zip(boards,BT): vis(b_,[(a_,z_)])
s='S05'; r=SH[s]
cp=char('S05_cop','cop',s,(BX-1.5,2.3,0),r,'neutral',arms=('arm',[(520,'arm'),(588,'arm_chalk')]),walker=True)
oc=char('S05_sarge','oldcop',s,(BX+1.5,2.4,0),r,'deadpan',arms=('arm','arm'))
c2=char('S05_cop2','cop',s,(BX+2.15,1.7,0),r,'neutral'); c3=char('S05_cop3','cop',s,(BX-2.2,1.65,0),r,'neutral')
ALL+=[cp,oc,c2,c3]
faces(cp,[(520,'neutral'),(548,'shock'),(568,'sad'),(586,'annoyed'),(600,'grit'),(618,'smug'),(636,'laugh')])
faces(oc,[(520,'deadpan'),(556,'raise'),(574,'smug'),(600,'deadpan'),(626,'raise')])
faces(c2,[(520,'neutral'),(556,'shock'),(574,'sad'),(612,'shock'),(630,'laugh')]); faces(c3,[(520,'blink'),(523,'neutral'),(559,'shock'),(577,'sad'),(615,'shock'),(633,'laugh')])
bob(cp,[548,568,618]); bob(c2,[556,574]); bob(c3,[559,577]); bob(oc,[574])
arm(oc,-1,560,-20); arm(oc,-1,570,-95); arm(oc,-1,574,-80); arm(oc,-1,590,-15)   # sergeant taps the board
# the cop steps to the board, then sidesteps right while the chalk writes left to right (hand on the letters, rule 166)
CH_L,CH_R,CH_Z=BX-0.84,BX+0.84,BOARD_Z+0.8-0.859*1.6
walk(cp,586,600,(BX-1.5,2.3,0),(CH_L+0.58,3.12,0),step=3)
walk(cp,606,628,(CH_L+0.58,3.12,0),(CH_R+0.58,3.12,0),step=3)
walk(cp,636,652,(CH_R+0.58,3.12,0),(CH_R+1.3,2.6,0),step=3)
for f,a_ in [(586,-10),(600,-82),(606,-84),(610,-80),(614,-85),(618,-80),(622,-84),(628,-82),(636,-20)]: arm(cp,-1,f,a_)
path(s,[(520,(BX+0.15,-1.9,1.4),(BX,2.6,1.5)),(574,(BX+0.6,-2.0,1.4),(BX+0.1,2.8,1.45)),(600,(BX+1.2,-0.9,1.3),(BX-0.2,3.1,1.25)),(628,(BX+1.9,-0.4,1.25),(BX+0.4,3.2,1.2)),(652,(BX+1.6,0.6,1.3),(BX+0.1,3.4,1.15))])
# ======================= SET C: store owners' office, 1961 (X=600) =======================
CX=600
room('off61',CX,7,6,3.2,'office','wood')
box('off61_win',(CX+1.8,2.96,1.9),(1.7,0.08,1.3),flat('winframe',lin((240,236,220)),0.5),bv=0.02)
plane('off61_view',(CX+1.8,2.9,1.9),1.5,1.1,card_mat('fac2v','fac2',emit=0.6))
for j in range(2): box(f'off61_mull{j}',(CX+1.8,2.86,1.9),(0.04 if j==0 else 1.5,0.03,1.1 if j==0 else 0.04),flat('winframe',lin((240,236,220))),bv=0)
desk('odesk',(CX,0.9,0),w=2.0)
reg=flat('register',lin((150,120,70)),0.3,metal=0.6)
box('register',(CX+0.6,0.9,0.95),(0.45,0.4,0.3),reg,bv=0.03); box('register_top',(CX+0.6,1.0,1.17),(0.4,0.2,0.16),reg,bv=0.02)
plane('regtag',(CX+0.6,0.89,1.2),0.3,0.1,card_mat('banner_s','banner',emit=0.3))
phone('ophone',(CX-0.6,0.8,0.78)); gifts('ogifts',(CX-2.4,1.8,0),k=5,seed=4); gifts('ogifts2',(CX+2.6,1.6,0),k=4,seed=8)
plane('cal61',(CX-1.6,2.98,2.0),0.45,0.56,card_mat('cal61','cal61',emit=0.2))
box('oshelf',(CX-1.6,2.8,1.25),(1.2,0.3,0.04),flat('deskwood',lin((110,70,44))),bv=0.01)
wallframe('oph1',(CX-0.2,2.98,2.25),0.7,0.5,'fac6'); wallframe('oph2',(CX+0.75,2.98,2.3),0.35,0.45,'fac1'); wallframe('oph3',(CX-2.7,2.98,2.2),0.45,0.6,'dept50')
shelf_items('oshelf2',(CX+2.7,2.855,1.4),1.0,9); coatrack('orack',(CX+3.0,2.5),hats=1)
for j in range(5): box(f'obook{j}',(CX-2.05+j*0.2,2.8,1.4),(0.12,0.24,0.26+0.03*(j%2)),flat('book%d'%(j%3),lin([(150,40,40),(40,70,120),(60,110,60)][j%3]),0.6),bv=0.01)
s='S06'; r=SH[s]
ow=char('S06_owner','owner',s,(CX-0.15,1.5,0),r,'neutral',arms=('arm','arm'))
gr=char('S06_partner','granny',s,(CX+1.35,1.95,0),r,'stern',arms=('arm','arm'))
ALL+=[ow,gr]
faces(ow,[(643,'neutral'),(664,'horror'),(673,'angry'),(690,'swirl'),(700,'talkD')])
lipsync(ow,[w for w in WORDS if 23.0<=w[1]<=25.6],700,770)
faces(ow,[(771,'sad')])
faces(gr,[(643,'stern'),(666,'shock'),(680,'stern'),(712,'shock'),(740,'stern'),(756,'shock')]); bob(gr,[666,712,756])
for f,a_ in [(700,-30),(706,-125),(720,-110),(730,-140),(745,-120),(754,-150),(770,-20)]: arm(ow,1,f,a_)
for f,a_ in [(700,-20),(712,-110),(726,-95),(742,-125),(758,-100),(772,-15)]: arm(ow,-1,f,a_)
bob(ow,[664,673,701,710,730,754],amt=9)
path(s,[(643,(CX+1.6,-3.4,1.5),(CX+0.2,1.5,1.4)),(690,(CX+0.9,-2.6,1.45),(CX,1.5,1.5)),(740,(CX+0.25,-1.75,1.5),(CX-0.15,1.5,1.55)),(781,(CX-0.25,-1.5,1.55),(CX-0.15,1.5,1.6))])
# ======================= S07 / S08 / S09: back in the street (set A) =======================
ban=empty('banner_pivot',(-9.75,47.9,10.6)); ban.rotation_euler=(0,0,math.pi/2)
bp=plane('banner',(0,0,0),8.0,2.0,card_mat('banner','banner',emit=0.25)); bp.parent=ban; bp.location=(0,-0.02,-1.0)
roll=cyl('banner_roll',(-9.72,47.9,10.6),0.14,8.2,flat('roll',lin((250,236,90)),0.6),v=16,rot=(math.pi/2,0,0))
for sy in(-1,1): cyl(f'banner_rope{sy}',(-9.85,47.9+sy*4.05,10.85),0.03,0.6,INK,v=6)
# unfurl on "Big Friday" (f845-851): banner hangs from its top edge; one rope gives on "not once" (f904-912): the banner swings and sags
bp.scale=(1,0.06,1); bp.keyframe_insert('scale',frame=842); bp.scale=(1,1,1); bp.keyframe_insert('scale',frame=851)
bp.location=(0,-0.02,-0.06); bp.keyframe_insert('location',frame=842); bp.location=(0,-0.02,-1.0); bp.keyframe_insert('location',frame=851)
ban.keyframe_insert('rotation_euler',frame=903); ban.rotation_euler=(math.radians(-24),0,math.pi/2); ban.keyframe_insert('rotation_euler',frame=912)
ban.rotation_euler=(math.radians(-19),0,math.pi/2); ban.keyframe_insert('rotation_euler',frame=918); ban.rotation_euler=(math.radians(-21),0,math.pi/2); ban.keyframe_insert('rotation_euler',frame=924)
vis(bp,[(775,938)]); vis(roll,[(775,850)])
s='S07'; r=SH[s]
o7=char('S07_owner','owner',s,(-8.4,45.6,0.14),r,'hope',arms=('arm','arm'))
ALL.append(o7); faces(o7,[(775,'hope'),(800,'neutral'),(820,'hope'),(851,'hope')]); bob(o7,[790,851])
for f,a_ in [(775,-150),(842,-150),(848,-60),(856,-140)]: arm(o7,1,f,a_)
ex=crowd(s,r,[(-7.6,42.6,0.14),(-8.9,50.4,0.14)],['shopper','granny'],21); ALL+=ex
path(s,[(775,(-5.6,44.0,1.35),(-8.4,45.6,1.5)),(812,(-4.8,43.6,1.2),(-8.6,46.2,2.4)),(851,(-2.6,42.8,0.9),(-9.6,47.9,9.4)),(866,(-2.4,42.7,0.85),(-9.6,47.9,9.6))])
s='S08'; r=SH[s]
o8=char('S08_owner','owner',s,(-8.5,47.4,0.14),r,'hope',arms=('arm','arm'))
c8=char('S08_cop','cop',s,(-9.35,52.6,0.14),r,'deadpan',arms=('arm','arm'))
ALL+=[o8,c8]
faces(o8,[(867,'hope'),(884,'neutral'),(897,'sad'),(912,'horror'),(925,'sad')]); bob(o8,[884,912])
faces(c8,[(867,'deadpan'),(895,'smug'),(912,'deadpan')]); arm(o8,1,867,-140); arm(o8,1,884,-20)
W8=[];sp8=[]
for i in range(8):
    y0=(36.0 if i%2 else 51.0)+1.6*i; sp8.append((-6.9 if i%2 else -8.3,y0,0.14)); W8.append((i,867,938,0,(9 if i%2 else -9)))
ex=crowd(s,r,sp8,['shopper','tourist','kid','granny','fanblue','fangold'],23,walkers=W8); ALL+=ex
path(s,[(867,(-1.4,46.4,0.7),(-8.6,48.0,4.2)),(904,(-1.6,47.0,0.75),(-8.8,48.0,4.4)),(938,(-1.9,47.6,0.8),(-8.8,48.2,4.3))])
s='S09'; r=SH[s]
c9=char('S09_cop','cop',s,(0,0,0.64),r,'neutral',arms=('arm','arm_megaphone'))
ALL.append(c9); faces(c9,[(931,'neutral'),(950,'shout'),(966,'grit'),(976,'shout'),(990,'laugh'),(1002,'shout')])
for f,a_ in [(931,-20),(948,-128),(1000,-128)]: arm(c9,1,f,a_)
for f,a_ in [(931,-15),(958,-90),(976,-110),(990,-30)]: arm(c9,-1,f,a_)
bob(c9,[950,968,977,1002],amt=10)
ex=crowd(s,r,[(-7.6,7.6,0.14),(-8.6,8.6,0.14),(7.4,7.8,0.14),(-7.4,-7.6,0.14),(8.2,8.9,0.14)],['granny','shopper','tourist','kid','fangold'],27); ALL+=ex
for i,e in enumerate(ex): faces(e,[(931,'blink'),(934,list(e['F'])[0]),(958+3*i,'shock'),(978+4*i,list(e['F'])[0])])
path(s,[(931,(-3.0,3.4,0.5),(0,0,1.8)),(970,(-2.3,2.6,0.55),(0,0,1.85)),(1013,(-1.85,2.1,0.6),(-0.1,-0.1,1.86))])
# ======================= SET D: the press room (X=900) =======================
DX=900
room('press',DX,10,8,4.5,'precinct','lino')
pm=flat('pressgrey',lin((70,80,86)),0.4,metal=0.5); pk=flat('pressblack',lin((30,30,34)),0.4,metal=0.4)
for sx in(-1,1): box(f'press_side{sx}',(DX+sx*1.6,1.0,1.4),(0.3,2.0,2.8),pm,bv=0.05)
rollers=[]
for j,(y,z,r_) in enumerate([(0.3,0.95,0.32),(1.0,1.55,0.42),(1.7,2.2,0.32),(0.6,2.35,0.22)]):
    rl=cyl(f'roller{j}',(DX,y,z),r_,3.0,pk if j%2 else pm,v=32,rot=(0,math.pi/2,0)); rollers.append(rl)
    for f in range(1008,1060,6): rl.rotation_euler=(math.radians((f-1008)*(-24 if j%2 else 24)),math.pi/2,0); rl.keyframe_insert('rotation_euler',frame=f)
    L.linear(rl)
web=plane('press_web',(DX,-0.6,0.612),2.6,1.8,flat('newsprint',lin((236,230,214)),0.9),horiz=True)
belt=box('press_belt',(DX,-1.8,0.55),(2.0,3.0,0.12),flat('belt',lin((44,40,38)),0.8),bv=0.02)
for sx in(-1,1): box(f'press_beltleg{sx}',(DX+sx*0.9,-1.8,0.25),(0.1,2.6,0.5),pm,bv=0.01)
stack=box('press_stack',(DX,-3.6,0.35),(0.9,1.2,0.7),flat('newsprint',lin((236,230,214))),bv=0.01)
for sx in(-1,1): box(f'press_ink{sx}',(DX+sx*1.6,0.6,3.05),(0.4,0.4,0.5),flat('inkwell',lin((180,40,40)),0.5),bv=0.03)
# sheets ride the belt toward the camera, headlines growing (paper62 -> 66 -> 70)
for j in range(8):
    tex_=['paper62','paper66','paper70'][min(2,j//3)]; f0=1004+j*7
    sh_=plane(f'sheet{j}',(DX,-0.4,0.62),0.8,1.1,card_mat(tex_+'_s',tex_,emit=0.2),horiz=True)
    kloc(sh_,f0,(DX,-0.6,0.616)); kloc(sh_,f0+24,(DX,-3.1,0.616)); L.linear(sh_); vis(sh_,[(max(1008,f0),min(1057,f0+24))])
s='S10'
path(s,[(1008,(DX+0.25,-2.9,1.25),(DX,-0.2,0.95)),(1030,(DX+0.2,-2.6,1.2),(DX,-1.2,0.62)),(1057,(DX-0.1,-2.9,1.55),(DX,-2.2,0.6))])
# ======================= SET E: newsstands, town to town (X=1200) =======================
EX=1200
box('E_road',(EX,-6,-0.1),(80,10,0.2),ROADX,bv=0); box('E_walk',(EX,1.5,0.07),(80,5,0.14),WALK,bv=0.03)
for j in range(9): building(f'bE{j}',(EX-32+j*8,4),'-Y',FAC[(j+3)%8],awn=AW[(j+3)%8])
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
pb=char('S11_paperboy','paperboy',s,(EX-6.9,0.9,0.14),r,'shout',arms=('arm','arm_paper'))
ALL.append(pb); faces(pb,[(1051,'shout'),(1068,'happy'),(1072,'shout'),(1092,'happy'),(1100,'shout')]); arm(pb,1,1051,-140); arm(pb,1,1066,-160); arm(pb,1,1080,-130); bob(pb,[1072,1100])
ex=crowd(s,r,[(STANDS[0]+1.4,0.6,0.14),(STANDS[1]+1.4,0.7,0.14),(STANDS[2]+1.5,0.6,0.14),(STANDS[3]+1.4,0.7,0.14),(STANDS[3]+2.4,0.2,0.14)],['granny','tourist','shopper','fanblue','kid'],31,walkers=[(4,1051,1125,-2.0,0)]); ALL+=ex
path(s,[(1051,(EX-8.2,-4.6,1.5),(EX-5.6,1.4,2.0)),(1082,(EX-4.4,-5.0,1.55),(EX-1.9,1.4,2.1)),(1099,(EX-0.8,-5.2,1.6),(EX+1.7,1.4,2.15)),(1125,(EX+2.8,-5.4,1.65),(EX+5.2,1.4,2.2))])
# ======================= SET F: 1981 office + the ledger (X=1500) =======================
FX=1500
room('off81',FX,7,6,3.0,'office81','lino')
box('off81_win',(FX-1.8,2.96,1.8),(1.9,0.08,1.4),flat('winframe81',lin((210,206,196)),0.5),bv=0.02)
plane('off81_view',(FX-1.8,2.9,1.8),1.7,1.2,card_mat('skyline_dawn_v','skyline_dawn',emit=0.7))
for j in range(6): box(f'blind{j}',(FX-1.8,2.905,1.3+j*0.2),(1.7,0.02,0.03),flat('blind',lin((230,226,214)),0.5),bv=0)
desk('fdesk',(FX,0.9,0),w=2.0,m=flat('desk81',lin((90,64,44)),0.4))
beige=flat('beige',lin((214,204,180)),0.5)
box('pc_base',(FX+0.55,1.05,0.86),(0.6,0.5,0.14),beige,bv=0.02); box('pc_mon',(FX+0.55,1.1,1.16),(0.5,0.42,0.42),beige,bv=0.04)
plane('pc_screen',(FX+0.55,0.885,1.18),0.38,0.29,card_mat('screen81','screen81',emit=1.2))
box('pc_kb',(FX+0.5,0.7,0.8),(0.5,0.18,0.04),beige,bv=0.01)
plane('cal81',(FX+1.7,2.98,1.9),0.45,0.56,card_mat('cal81','cal81',emit=0.2))
wallframe('fph1',(FX+0.4,2.98,2.15),0.8,0.55,'fac81_2'); wallframe('fph2',(FX-0.55,2.98,2.25),0.36,0.48,'paper70'); shelf_items('fshelf',(FX+2.6,2.855,1.6),1.1,21)
cabinet('fcab',(FX+2.8,2.6),h=1.0); sph('plant',(FX-2.8,2.4,1.25),0.45,flat('leafy',lin((60,120,60)),0.7),sc_=(1,1,1.2)); cyl('plantpot',(FX-2.8,2.4,0.4),0.3,0.8,flat('pot81',lin((190,90,60)),0.6),v=18,r2=0.24)
shade=lamp('flamp',(FX-0.75,1.05,0.78))
lm=flat('lampbulb81',lin((255,226,150)),0.4,emit=0.0); bulb=sph('flamp_bulb',(FX-0.75,1.01,1.17),0.05,lm)
# the lamp clicks on with "story" (f1184): bulb + warm point light keyed
p_=bulb.active_material.node_tree.nodes['Principled BSDF']; p_.inputs['Emission Strength'].default_value=0.0; p_.inputs['Emission Strength'].keyframe_insert('default_value',frame=1183)
p_.inputs['Emission Strength'].default_value=12.0; p_.inputs['Emission Strength'].keyframe_insert('default_value',frame=1184)
bpy.ops.object.light_add(type='POINT',location=(FX-0.75,0.85,1.15)); lp=bpy.context.object; lp.name='flamp_light'; lp.data.color=(1,0.8,0.5); lp.data.shadow_soft_size=0.1
lp.data.energy=0; lp.data.keyframe_insert('energy',frame=1183); lp.data.energy=60; lp.data.keyframe_insert('energy',frame=1184)
for fc in lp.data.animation_data.action.fcurves:
    for kp in fc.keyframe_points: kp.interpolation='CONSTANT'
# the ledger (open book on the desk): page swaps red entries -> black entries -> black total
LED_Z=0.786
box('ledger_cover',(FX-0.05,0.85,0.775),(0.66,0.46,0.02),flat('ledgercover',lin((40,60,40)),0.6),bv=0.004)
cyl('pencup',(FX-0.6,0.75,0.86),0.06,0.16,flat('pencup',lin((40,70,120)),0.5),v=16)
for j in range(4): cyl(f'pencil{j}',(FX-0.6+0.015*(j-1.5),0.75,0.98),0.008,0.2,flat('pencil%d'%j,lin([(240,200,60),(196,30,30),(20,20,26),(40,110,60)][j]),0.5),v=8)
cyl('mug81',(FX+0.15,0.55,0.83),0.05,0.1,flat('mug81',lin((200,60,50)),0.4),v=16)
for j in range(4): box(f'paperstack{j}',(FX-0.55,1.0,0.785+0.006*j),(0.3,0.4,0.005),flat('newsprint',lin((236,230,214))),bv=0)
box('stapler',(FX-0.25,1.16,0.81),(0.06,0.18,0.05),flat('stapler',lin((40,40,44)),0.4),bv=0.01)
box('calc81',(FX+0.85,0.68,0.795),(0.16,0.2,0.03),beige,bv=0.005)
for j in range(12): box(f'calckey{j}',(FX+0.8+0.035*(j%4),0.62+0.035*(j//4),0.812),(0.026,0.026,0.008),flat('key81',lin((60,60,64)),0.5),bv=0.002)
ledgers=[plane(f'ledger{i}',(FX-0.05,0.85,LED_Z),0.62,0.413,card_mat(f'ledger{i}',f'ledger{i}',emit=0.3),horiz=True) for i in range(5)]
LT=[(0,1300),(1301,1318),(1319,1334),(1335,1376),(1377,END)]
for l_,(a_,z_) in zip(ledgers,LT): vis(l_,[(a_,z_)])
s='S12'; r=SH[s]
x8=char('S12_exec','exec81',s,(FX-0.1,1.5,0),r,'smug',arms=('arm','arm_pen'))
ALL.append(x8); faces(x8,[(1114,'smug'),(1150,'talk'),(1166,'smug'),(1184,'idea'),(1200,'laugh')]); bob(x8,[1184,1200]); arm(x8,1,1170,-30); arm(x8,1,1184,-150); arm(x8,1,1200,-40)
import math as _m
orb=[]
for i,f in enumerate(range(1114,1219,13)):
    a_=_m.radians(-38+i*9); orb.append((f,(FX+3.2*_m.sin(a_),1.5-3.2*_m.cos(a_),1.55+0.05*i),(FX-0.1,1.3,1.45)))
path(s,orb)
# S13 top-down ledger: a flat drawn hand + pen lies on the page, tip on the paper, small strokes (rule 166)
s='S13'; r=SH[s]
C13=L.chr_coll(s)
hand_r=plane('S13_hand_red',(0,0,0),0.12,0.27,card_mat('exec81_arm_redpen','exec81_arm_redpen'),coll=C13,horiz=True)
hand_b=plane('S13_hand_black',(0,0,0),0.12,0.27,card_mat('exec81_arm_pen','exec81_arm_pen'),coll=C13,horiz=True)
for h_ in (hand_r,hand_b): h_.rotation_euler=(0,0,math.pi); h_['noink']=1
# red-pen hand writes the red column (f1270-1300), black-pen hand the black column (f1306-1345); tips touch the page (z = page + 1 mm)
def strokes(o,f0,f1,x0,y0,x1,y1):
    n=(f1-f0)//3
    for i in range(n+1):
        t=i/max(1,n); f=f0+i*3; kloc(o,f,(x0+(x1-x0)*t+(0.006 if i%2 else -0.006),y0+(y1-y0)*t+0.12,LED_Z+0.002))
TIPX_R,TIPX_B=FX-0.05-0.31+0.62*0.1,FX-0.05-0.31+0.62*0.9
strokes(hand_r,1262,1300,TIPX_R,0.85+0.12,TIPX_R+0.02,0.85-0.15); strokes(hand_b,1306,1346,TIPX_B,0.85+0.15,TIPX_B,0.85-0.15)
vis(hand_r,[(1262,1302)]); vis(hand_b,[(1306,1348)])
kloc(hand_r,1240,(TIPX_R+0.25,0.85-0.35,LED_Z+0.002)); kloc(hand_b,1350,(TIPX_B+0.25,0.85-0.4,LED_Z+0.002))
path(s,[(1210,(FX-0.05,0.85,2.25),(FX-0.05,0.859,LED_Z)),(1282,(FX-0.12,0.85,1.75),(FX-0.12,0.861,LED_Z)),(1319,(FX+0.06,0.85,1.8),(FX+0.06,0.861,LED_Z)),(1359,(FX+0.02,0.85,1.45),(FX+0.02,0.862,LED_Z))])
# S14: ledger total turns the books from red to black, pull back and up to the exec's wink
s='S14'; r=SH[s]
x14=char('S14_exec','exec81',s,(FX-0.1,1.5,0),r,'smug',arms=('arm','arm_redpen'))
ALL.append(x14); faces(x14,[(1352,'smug'),(1400,'talk'),(1420,'smug'),(1454,'idea'),(1468,'wink'),(1480,'laugh')]); bob(x14,[1468])
path(s,[(1352,(FX+0.02,0.85,1.45),(FX+0.02,0.862,LED_Z)),(1400,(FX+0.1,0.72,1.5),(FX+0.08,0.88,LED_Z+0.02)),(1440,(FX+0.4,-0.9,1.6),(FX,1.0,1.0)),(1467,(FX+0.3,-1.9,1.6),(FX-0.1,1.5,1.45)),(1487,(FX+0.2,-2.1,1.62),(FX-0.1,1.5,1.5))])
# ======================= SET H: 1981 downtown at dawn, Hartwell's (X=1800) =======================
HX=1800
box('H_road',(HX,-7,-0.1),(90,10,0.2),ROADX,bv=0); box('H_walk',(HX,0,0.07),(90,5,0.14),WALK,bv=0.03)
building('deptH',(HX,2.5),'-Y','dept81',w=16,h=12,d=10,side='dept81',cap=(90,80,70))
for j,x in enumerate([HX-16,HX-24,HX+16,HX+24,HX-32,HX+32]): building(f'bH{j}',(x+(4 if x>HX else -4),2.5),'-Y',f'fac81_{j%4}',awn=AW[j],side=f'fac81_{j%4}')
skH=plane('H_sky',(HX,120,50),300,170,card_mat('skydawn','sky_dawn',emit=1.0),coll=L.C_NOI); skH['fly']=1
slH=plane('H_skyline',(HX,100,18),240,240*1400/4096,card_mat('skyline_dawn','skyline_dawn',emit=0.6),coll=L.C_NOI); slH['fly']=1
for j,x in enumerate([HX-12,HX+4.5,HX+12]): lamppost(f'Hlp{j}',(x,-2.0))
# the payoff window display: a lit 3D bay in front of the left window bay, poster framed on an easel
WX=HX-5.6; WY=1.6
win=flat('bayframe',lin((40,60,46)),0.5)
box('bay_floor',(WX,WY,0.45),(3.0,1.6,0.9),win,bv=0.03); box('bay_top',(WX,WY,3.65),(3.2,1.7,0.3),win,bv=0.03)
for sx in(-1,1): box(f'bay_post{sx}',(WX+sx*1.5,WY-0.75,2.27),(0.14,0.14,2.46),win,bv=0.02)
box('bay_back',(WX,WY+0.78,2.27),(2.9,0.08,2.46),surf('baywall','window81',(1.5,1.5)),bv=0)
plane('bay_sign',(WX,WY-0.86,3.65),2.6,0.24,card_mat('banner81','banner',emit=0.3))
PW,PH=1.0,1.5; PZ=0.9+0.12+PH/2+0.14
easel=flat('easel',lin((120,80,50)),0.6)
for sx in(-1,1): box(f'easel_leg{sx}',(WX+sx*0.42,WY+0.25,0.9+1.05),(0.06,0.06,2.1),easel,bv=0)
box('easel_shelf',(WX,WY+0.16,1.06),(1.2,0.2,0.06),easel,bv=0.01)
box('poster_frame',(WX,WY+0.2,PZ),(PW+0.14,0.05,PH+0.14),flat('pframe',lin((30,24,20)),0.4),bv=0.012)
pmat=bpy.data.materials.new('poster'); N_,L_=L.nodes(pmat); pp_=N_['Principled BSDF']; it_=N_.new('ShaderNodeTexImage'); it_.image=bpy.data.images.load('/root/bf/poster_2k.png'); it_.interpolation='Cubic'
L_.new(it_.outputs['Color'],pp_.inputs['Base Color']); L_.new(it_.outputs['Color'],pp_.inputs['Emission Color']); pp_.inputs['Emission Strength'].default_value=0.6; pp_.inputs['Roughness'].default_value=0.7; pp_.inputs['Specular IOR Level'].default_value=0.05
poster=plane('poster',(WX,WY+0.17,PZ),PW,PH,pmat,coll=L.C_NOI); poster['noink']=1
gifts('bay_gifts',(WX-1.0,WY+0.1,0.9),k=3,seed=12); gifts('bay_gifts2',(WX+1.0,WY,0.9),k=4,seed=13)
bpy.ops.object.light_add(type='AREA',location=(WX,WY-0.6,3.3),rotation=(math.radians(35),0,0)); bl=bpy.context.object; bl.name='bay_light'; bl.data.energy=140; bl.data.size=1.6; bl.data.color=(1,0.9,0.75)
# doors of the store slide open on "became" (f1646)
dm=flat('doors81',lin((60,70,80)),0.2,metal=0.4)
for sx in(-1,1):
    d_=box(f'doorH{sx}',(HX+0.0+sx*0.95,2.42,1.4),(1.8,0.08,2.8),dm,bv=0.02)
    kloc(d_,1640,(HX+sx*0.95,2.42,1.4)); kloc(d_,1660,(HX+sx*2.6,2.42,1.4))
box('doorH_light',(HX,2.47,1.4),(3.6,0.04,2.8),flat('storeglow',lin((255,230,170)),0.5,emit=2.5),bv=0)
s='S15'; r=SH[s]
o15=char('S15_oldcop','oldcop',s,(HX+9.0,-0.9,0.14),r,'deadpan',arms=('arm','arm'))
ALL.append(o15)
pap=plane('S15_paper',(0,0,0),0.62,0.85,card_mat('paper81','paper81',emit=0.3),coll=L.chr_coll(s)); pap.parent=o15['root']; pap.location=(0,-0.03,0.52)
vis(pap,[r]); pap['chr']='S15_oldcop'
faces(o15,[(1481,'deadpan'),(1489,'raise'),(1505,'deadpan'),(1519,'eyeroll'),(1540,'smug'),(1552,'deadpan')]); bob(o15,[1489,1519])
arm(o15,-1,1481,30); arm(o15,1,1481,30); arm(o15,1,1519,22); arm(o15,1,1540,30)
path(s,[(1481,(HX+8.0,-3.6,1.45),(HX+9.0,-0.9,1.25)),(1520,(HX+8.4,-3.25,1.5),(HX+9.0,-0.9,1.35)),(1565,(HX+8.9,-3.0,1.55),(HX+9.0,-0.9,1.45))])
s='S16'; r=SH[s]
sp=[(HX-3.0,-0.5,0.14),(HX-1.9,-1.1,0.14),(HX-0.8,-0.6,0.14),(HX+0.6,-1.0,0.14),(HX+1.8,-0.5,0.14),(HX+3.0,-1.2,0.14),(HX-2.4,-2.0,0.14),(HX+2.4,-2.1,0.14),(HX-0.2,-2.2,0.14),(HX+4.0,-0.4,0.14)]
W16=[(i,1648,1700,(-1 if p[0]>HX else 1)*R.uniform(0.6,1.4),0.35) for i,p in enumerate(sp)]
ex=crowd(s,r,sp,['mullet','perm','kid','granny','shopper','tourist','mullet','perm','fanblue','kid'],41,walkers=W16); ALL+=ex
for i,e in enumerate(ex): faces(e,[(1640+3*i,'shock'),(1652+2*i,list(e['F'])[0]),(1690+2*i,'happy')])
path(s,[(1556,(HX+1.2,-9.5,1.9),(HX,1.0,2.4)),(1620,(HX+0.4,-8.2,1.7),(HX-0.5,1.0,2.0)),(1646,(HX-0.4,-7.4,1.6),(HX-1.6,1.0,1.9)),(1700,(HX-2.4,-6.0,1.55),(WX,WY,1.8)),
        (1709,(WX+0.35,-2.3,PZ+0.1),(WX,WY+0.17,PZ-0.05)),(1727,(WX+0.15,-1.85,PZ+0.05),(WX,WY+0.17,PZ-0.05)),(END,(WX+0.05,-1.72,PZ+0.04),(WX,WY+0.17,PZ-0.05))])
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
