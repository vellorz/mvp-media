# Detroit Thanksgiving short (mon-detroit): Blender builder.  blender -b --python scene_det.py   (writes /root/det/blend/det.blend)
# Built from the Black Friday pipeline (lib.py, cast.py, helpers copied from scene.py); every set, prop and scene here is new for this video.
import sys, os, math, random, json
sys.path.insert(0,'/root/det/src')
import bpy
from mathutils import Vector
import lib as L
from lib import box,cyl,sph,plane,flat,surf,card_mat,lin,vis,kloc,krot,kscale,empty,cam,path,char,face,faces,arm,bob,walk,finish,lipsync
END=1940
sc=L.init(END); R=random.Random(23)
WORDS=json.load(open('/root/det/audio/vo_trim.wav.words.json'))
def WF(i): return int(round((WORDS[i][1]+0.1)*30))
# shot table: overlapping ranges are declared dissolves (post.py), touching ranges are hard cuts (lessons-log N-001: no frame plays twice)
SH={'S01':(0,112),'S02':(113,196),'S03':(197,330),'S04':(331,414),'S05':(415,494),'S06':(495,547),'S07':(548,605),'S08':(598,716),
    'S09':(717,794),'S10':(795,931),'S11':(932,1180),'S12':(1171,1226),'S13':(1227,1276),'S14':(1277,1349),'S15':(1350,1409),'S16':(1402,1536),
    'S17':(1537,1558),'S18':(1559,1729),'S19':(1718,1795),'S20':(1784,1863),'S21':(1852,END)}
sc['shots']=json.dumps(SH)
LENS={'S01':30,'S02':34,'S03':32,'S04':28,'S05':26,'S06':40,'S07':26,'S08':26,'S09':36,'S10':32,'S11':28,'S12':34,'S13':34,'S14':24,'S15':30,'S16':30,'S17':40,'S18':32,'S19':28,'S20':30,'S21':34}
FSTOP={k:9.0 for k in SH}; FSTOP.update({'S06':7.0,'S17':7.0,'S18':8.0,'S21':8.0})   # sets stay sharp (BF r6 lesson: DOF blur, not missing paint, killed set detail)
for n in SH: cam(n,LENS[n],FSTOP[n])
CHRS=set(SH); ALL=[]
CI_PROPS={k:v.get('props',[]) for k,v in L.CI.items()}
INK=flat('inkc',lin((50,28,42)),0.9)
CHROME=flat('chrome',(0.75,0.75,0.78),0.25,metal=1.0)
TYRE=flat('tyre',lin((30,26,26)),0.8)
GLASS=flat('glass',lin((70,96,118)),0.15)
LAMPG=flat('lampglow',lin((255,226,150)),0.5,emit=3.0)
WOOD=surf('deskwood_p','wood',(0.5,0.5))
def hardcut(shot,f):
    for o_ in (L.CAM[shot],L.TGT[shot]):
        for fc in o_.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                if int(round(kp.co[0]))==f-1: kp.interpolation='CONSTANT'
def crowd(shot,rng,spots,kinds,seed,camname=None,base=0,faces_pool=None,props=0.6,walker=False):
    rr=random.Random(seed); out=[]
    for i,p in enumerate(spots):
        kd=kinds[i%len(kinds)]; pr=CI_PROPS.get(kd,[])
        arms_=('arm','arm_'+pr[0]) if pr and rr.random()<props else ('arm','arm')
        sc_=0.8 if kd in('kid34','kidM','newsboy') else 1.0
        ch=char(f'{shot}_x{i+base}_{kd}',kd,shot,p,rng,arms=arms_,camname=camname,scale=sc_,walker=walker)
        fl=[f for f in L.CI[kd]['faces'] if f!='blink' and not f.startswith('talk')]
        if faces_pool: fl=[f for f in fl if f in faces_pool] or fl
        f0=rng[0]; seq=[]
        while f0<rng[1]: seq.append((f0,rr.choice(fl))); f0+=rr.randint(22,40)
        faces(ch,seq); out.append(ch)
    return out
def cheer(ch,f0,f1,seed,up=(-150,-110),down=(-40,-20),side=None):
    """arms pump: hold, snap (RENDER_SPEC v1.5 A: react 5 f, holds ~26 f). side=-1/1 pumps only the outer arm (occprobe: no arm across a neighbour's face)"""
    rr=random.Random(seed); f=f0; sx=side or rr.choice((-1,1))
    while f<f1:
        arm(ch,sx,f,rr.uniform(*down)); arm(ch,sx,f+5,rr.uniform(*up)); f+=rr.randint(14,26); sx=sx if side else -sx
def glow(n,c,size,rgb,strength,face='-Y',coll=None,img='glow',on=None):
    key=f'glowm_{img}_{rgb}_{strength}'
    m=bpy.data.materials.get(key)
    if not m:
        m=bpy.data.materials.new(key); N,Lk=L.nodes(m)
        for x in list(N): N.remove(x)
        o=N.new('ShaderNodeOutputMaterial'); it=N.new('ShaderNodeTexImage'); it.image=bpy.data.images.load(L.TX+img+'.png',check_existing=True)
        em=N.new('ShaderNodeEmission'); em.inputs['Color'].default_value=(*lin(rgb),1); em.inputs['Strength'].default_value=strength
        tr=N.new('ShaderNodeBsdfTransparent'); ad=N.new('ShaderNodeAddShader'); mx=N.new('ShaderNodeMixShader')
        Lk.new(it.outputs['Alpha'],mx.inputs['Fac']); Lk.new(tr.outputs[0],mx.inputs[1]); Lk.new(em.outputs[0],ad.inputs[0]); Lk.new(tr.outputs[0],ad.inputs[1]); Lk.new(ad.outputs[0],mx.inputs[2]); Lk.new(mx.outputs[0],o.inputs['Surface'])
    g=plane(n,c,size,size,m,coll=coll,face=face); g['noink']=1; g['fly']=1; g.visible_shadow=False; g.visible_diffuse=False; g.visible_glossy=False
    if on is not None: L.vis(g,[on])
    return g
def room(n,cx,w,d,h,wall,floor,ftile=(2.5,2.5),wtile=(4,4),lights=True):
    box(n+'_floor',(cx,0,-0.1),(w+2,d+4,0.2),surf(n+'_fl',floor,ftile,rough=0.6),bv=0)
    box(n+'_back',(cx,d/2+0.15,h/2),(w+0.6,0.3,h),surf(n+'_wall',wall,wtile),bv=0.02)
    for sx in(-1,1): box(f'{n}_side{sx}',(cx+sx*(w/2+0.15),0.5,h/2),(0.3,d+1,h),surf(n+'_wall',wall,wtile),bv=0.02)
    box(n+'_base',(cx,d/2-0.02,0.08),(w,0.06,0.16),flat(n+'_skirt',lin((128,96,70)),0.6),bv=0.01)   # r2 rule 317
    box(n+'_crown',(cx,d/2-0.02,h-0.1),(w,0.1,0.18),flat(n+'_skirt',lin((70,48,34))),bv=0.01)
    box(n+'_ceil',(cx,0.5,h+0.1),(w+0.6,d+1,0.2),surf('ceiltile','ceiltile',(1.2,1.2)),bv=0)
def frame_pic(n,c,w,h,tex,col=(70,48,34),emit=0.2):
    box(n,(c[0],c[1]+0.02,c[2]),(w+0.08,0.04,h+0.08),flat('frame%d'%sum(col),lin(col),0.5),bv=0.01)
    return plane(n+'_pic',(c[0],c[1]-0.007,c[2]),w,h,card_mat(tex+'_pic',tex,emit=emit))
def lampT(n,c,shade=(200,150,90)):
    b=flat('brass',lin((180,140,60)),0.3,metal=0.8); cyl(n+'_b',(c[0],c[1],c[2]+0.02),0.09,0.04,b,v=14); cyl(n+'_s',(c[0],c[1],c[2]+0.2),0.014,0.36,b,v=8)
    cyl(n+'_shade',(c[0],c[1],c[2]+0.42),0.17,0.18,flat(n+'_shm',lin(shade),0.6),v=18,r2=0.09)
    glow(n+'_glow',(c[0],c[1]-0.18,c[2]+0.35),0.42,(255,214,140),2.5)
def chair(n,c,col=(110,70,44)):
    m=flat('chair%d'%sum(col),lin(col),0.6); box(n+'_seat',(c[0],c[1],0.46),(0.44,0.42,0.05),m,bv=0.01); box(n+'_back',(c[0],c[1]+0.2,0.78),(0.44,0.04,0.6),m,bv=0.01)
    for sx in(-1,1):
        for sy in(-1,1): box(f'{n}_l{sx}{sy}',(c[0]+sx*0.19,c[1]+sy*0.18,0.22),(0.04,0.04,0.44),m,bv=0)
def turkey(n,c,coll=None,steam=None):
    plat=flat('platter',lin((240,236,226)),0.3); cyl(n+'_plat',(c[0],c[1],c[2]+0.012),0.34,0.025,plat,v=28,coll=coll)
    sk=flat('turkeyskin',lin((196,116,52)),0.45); sph(n+'_body',(c[0],c[1],c[2]+0.13),0.19,sk,sc_=(1.25,1.0,0.72),coll=coll)
    for sx in(-1,1):
        sph(f'{n}_leg{sx}',(c[0]+sx*0.17,c[1]-0.1,c[2]+0.15),0.075,sk,sc_=(1,1.5,1),coll=coll); cyl(f'{n}_bone{sx}',(c[0]+sx*0.2,c[1]-0.22,c[2]+0.17),0.016,0.09,flat('bone',lin((250,246,236)),0.4),v=8,rot=(math.radians(75),0,0),coll=coll)
    for k,(dx,col) in enumerate([(-0.26,(80,140,60)),(0.26,(200,60,40)),(0.0,(240,200,80))]): sph(f'{n}_garn{k}',(c[0]+dx,c[1]-0.2,c[2]+0.04),0.045,flat('garn%d'%k,lin(col),0.5),coll=coll)
    if steam:
        for k in range(3):
            g=glow(f'{n}_steam{k}',(c[0]+(k-1)*0.08,c[1]-0.05,c[2]+0.45),0.22,(255,255,255),0.6,coll=coll)
            vis(g,[(steam[0],steam[1])])
            for f in range(steam[0],steam[1],24): kloc(g,f,(c[0]+(k-1)*0.08,c[1]-0.05,c[2]+0.4)); kloc(g,f+23,(c[0]+(k-1)*0.08+0.03,c[1]-0.05,c[2]+0.62))
def table(n,c,w=1.9,d=0.95,h=0.78,cloth=(240,234,220)):
    box(n+'_top',(c[0],c[1],h-0.03),(w,d,0.06),WOOD,bv=0.015)
    box(n+'_cloth',(c[0],c[1],h+0.004),(w+0.06,d+0.06,0.012),flat('cloth%d'%sum(cloth),lin(cloth),0.8),bv=0)
    box(n+'_drape',(c[0],c[1]-d/2-0.03,h-0.14),(w+0.06,0.012,0.28),flat('cloth%d'%sum(cloth),lin(cloth),0.8),bv=0)
    for sx in(-1,1):
        for sy in(-1,1): box(f'{n}_l{sx}{sy}',(c[0]+sx*(w/2-0.08),c[1]+sy*(d/2-0.08),(h-0.06)/2),(0.07,0.07,h-0.06),WOOD,bv=0.01)
    return h
def plates(n,c,xs,h):
    p=flat('plate',lin((246,244,236)),0.3)
    for i,x in enumerate(xs):
        cyl(f'{n}_p{i}',(c[0]+x,c[1]-0.3,h+0.012),0.12,0.015,p,v=24); cyl(f'{n}_f{i}',(c[0]+x,c[1]-0.3,h+0.03),0.07,0.02,flat('food%d'%(i%3),lin([(200,150,80),(120,160,80),(230,210,170)][i%3]),0.6),v=16)
        cyl(f'{n}_g{i}',(c[0]+x+0.15,c[1]-0.22,h+0.07),0.035,0.13,flat('glassw',lin((200,220,230)),0.1),v=14)
def radio34(n,c):
    m=surf('radiowood','wood',(0.4,0.4)); box(n,(c[0],c[1],0.55),(0.62,0.4,1.1),m,bv=0.04)
    box(n+'_top',(c[0],c[1],1.13),(0.66,0.44,0.06),m,bv=0.02)
    p=plane(n+'_front',(c[0],c[1]-0.205,0.62),0.5,0.75,card_mat('radiofront','radiofront',emit=0.35)); return p
# ============== SET LIV: today's living room, Thanksgiving (X=0) ==============
LX=0.0
room('liv',LX,7.0,5.6,2.8,'livwall','dwood2',ftile=(2.0,2.0),wtile=(3.2,3.2))
box('liv_rug',(LX-1.0,0.6,0.004),(3.2,2.4,0.008),surf('rugM','rugM',(3.2,2.4),gen=True),bv=0)
couch=flat('couch',lin((150,120,90)),0.8)
box('couch_base',(LX-1.2,2.3,0.25),(2.4,0.9,0.5),couch,bv=0.08,seg=3); box('couch_back',(LX-1.2,2.7,0.62),(2.4,0.25,0.7),couch,bv=0.08,seg=3)
for sx in(-1,1): box(f'couch_arm{sx}',(LX-1.2+sx*1.15,2.3,0.52),(0.25,0.9,0.42),couch,bv=0.08,seg=3)
for k,col in enumerate([(200,90,70),(70,110,150),(230,200,90)]): box(f'pillow{k}',(LX-1.9+k*0.7,2.52,0.7),(0.42,0.14,0.36),flat('pil%d'%k,lin(col),0.8),bv=0.06,seg=3)
# TV on a low stand, seen from behind in S01 (foreground layer), its screen glow lights the family
box('tv_stand',(LX-3.2,-0.6,0.25),(1.6,0.45,0.5),WOOD,bv=0.02); box('tv_back',(LX-3.2,-0.62,0.95),(1.35,0.12,0.78),flat('tvback',lin((36,34,38)),0.5),bv=0.02)
tvs=plane('tv_screen',(LX-3.2,-0.565,0.95),1.25,0.7,card_mat('tvfield','tvfield',emit=1.2),face='+Y'); tvs['noink']=1
bpy.ops.object.light_add(type='AREA',location=(LX-2.5,-0.4,0.95),rotation=(math.radians(-90),0,0)); tl=bpy.context.object; tl.name='tv_light'; tl.data.energy=60; tl.data.size=1.2; tl.data.color=(0.8,1.0,0.85)
box('coffee',(LX-1.2,1.15,0.2),(1.2,0.6,0.06),WOOD,bv=0.01); box('coffee_leg',(LX-1.2,1.15,0.1),(1.0,0.4,0.18),flat('coffleg',lin((80,56,40)),0.6),bv=0.01)
for k,col in enumerate([(220,60,50),(240,200,70),(60,120,200)]): cyl(f'snack{k}',(LX-1.6+k*0.4,1.12,0.27),0.09,0.08,flat('bowl%d'%k,lin(col),0.5),v=16)
plant=flat('plant',lin((60,130,70)),0.7)
for k in range(5): sph(f'liv_plant{k}',(LX-3.0+0.12*math.cos(k),2.5+0.1*math.sin(k),0.9+k*0.12),0.22-0.02*k,plant)
cyl('liv_pot',(LX-3.0,2.5,0.3),0.2,0.6,flat('pot',lin((190,110,70)),0.6),v=18)
lampT('liv_lamp',(LX-2.6,2.4,0.0+1.0)); box('liv_side',(LX-2.6,2.4,0.5),(0.5,0.5,1.0),WOOD,bv=0.02)
frame_pic('liv_ph1',(LX-1.8,2.79,1.75),0.5,0.4,'dfac2'); frame_pic('liv_ph2',(LX-0.7,2.79,1.8),0.4,0.5,'dfac4')
# payoff wall: sideboard with the turkey, the Detroit poster framed above it (whole, gilt frame, lit)
PX=LX+1.85; PY=2.8
box('sideboard',(PX,PY-0.3,0.45),(2.0,0.5,0.9),WOOD,bv=0.02)
for k in range(3): box(f'sb_door{k}',(PX-0.62+k*0.62,PY-0.555,0.45),(0.56,0.02,0.7),flat('sbdoor',lin((130,86,56)),0.5),bv=0.01)
turkey('liv_turkey',(PX,PY-0.36,0.9))   # no steam: nothing may cross the poster
for k,x in enumerate((-0.75,0.75)):
    cyl(f'candle{k}',(PX+x,PY-0.3,1.05),0.03,0.3,flat('candle',lin((246,236,210)),0.5),v=12); glow(f'candleg{k}',(PX+x,PY-0.34,1.25),0.18,(255,200,120),5.0)
for k,x in enumerate((-0.45,0.45)): sph(f'pumpkin{k}',(PX+x,PY-0.25,0.98),0.09,flat('pumpkin',lin((230,130,40)),0.6),sc_=(1.2,1.2,0.85))
PW,PH=0.9,1.35; PZ=0.95+0.12+PH/2+0.12
box('poster_frame',(PX,PY-0.04,PZ),(PW+0.12,0.05,PH+0.12),flat('pframe_gilt',lin((240,214,140)),0.35,emit=0.3),bv=0.012)
pmat=bpy.data.materials.new('poster'); N_,L_=L.nodes(pmat); pp_=N_['Principled BSDF']; it_=N_.new('ShaderNodeTexImage'); it_.image=bpy.data.images.load('/root/det/poster_2k.png'); it_.interpolation='Cubic'
L_.new(it_.outputs['Color'],pp_.inputs['Base Color']); L_.new(it_.outputs['Color'],pp_.inputs['Emission Color']); pp_.inputs['Emission Strength'].default_value=0.25
poster=plane('poster',(PX,PY-0.068,PZ),PW,PH,pmat,coll=L.C_NOI); poster['noink']=1
_bulb=flat('stringbulb',lin((255,226,150)),0.3,emit=6.0)
for i_ in range(13): cyl(f'liv_string{i_}',(PX-1.2+0.2*i_,PY-0.03,2.72-0.05*math.sin(i_/12*math.pi)),0.03,0.05,_bulb,v=10,rot=(math.radians(90),0,0))
bpy.ops.object.light_add(type='AREA',location=(PX,PY-1.4,2.5),rotation=(math.radians(40),0,0)); pl=bpy.context.object; pl.name='poster_light'; pl.data.energy=220; pl.data.size=1.4; pl.data.color=(1,0.93,0.8)
bpy.ops.object.light_add(type='AREA',location=(LX-1,-2.5,2.4),rotation=(math.radians(70),0,0)); a_=bpy.context.object; a_.data.energy=900; a_.data.size=5; a_.data.color=(1.0,0.93,0.84)
# ---------- S01 (0-112): hook. Family yelling at the game from the couch; the TV back in the foreground; on 'lost' they all go deadpan ----------
s='S01'; r=SH[s]
dad=char('S01_dad','dadM',s,(LX-1.6,1.45,0),r,'cheer',arms=('arm','arm_remote')); mom=char('S01_mom','momM',s,(LX-0.75,1.78,0),r,'happy',arms=('arm','arm'))
kid=char('S01_kid','kidM',s,(LX-2.45,0.95,0),r,'cheer',arms=('arm_ball','arm'),scale=0.8); gm=char('S01_gma','grandmaM',s,(LX+0.25,1.2,0),r,'happy',arms=('arm','arm'))
ALL+=[dad,mom,kid,gm]
faces(dad,[(0,'cheer'),(20,'shout'),(44,'cheer'),(70,'shout'),(98,'shock'),(104,'deadpan')]); faces(mom,[(0,'happy'),(24,'cheer'),(60,'wow'),(99,'deadpan')])
faces(kid,[(0,'cheer'),(30,'wow'),(56,'cheer'),(100,'wow')]); faces(gm,[(0,'happy'),(36,'cheer'),(101,'deadpan')])
cheer(dad,4,90,1,up=(-140,-120),side=-1); cheer(kid,10,92,2,up=(-140,-120),side=-1); cheer(mom,24,88,3,up=(-138,-120),side=1); cheer(gm,40,90,4,up=(-135,-118),side=1)
for c_,f_ in ((dad,98),(mom,99),(kid,100),(gm,101)):
    for sx in(-1,1): arm(c_,sx,f_,-12)
bob(dad,[20,44,70]); bob(kid,[30,56]); bob(mom,[60]); bob(gm,[36])
path(s,[(0,(LX-1.55,-2.4,1.15),(LX-1.25,2.0,1.05)),(53,(LX-1.4,-1.95,1.12),(LX-1.25,2.0,1.08)),(93,(LX-1.3,-1.55,1.1),(LX-1.2,2.0,1.1)),(112,(LX-1.42,-1.6,1.1),(LX-1.25,2.0,1.1))])   # ends on a sideways drift (rule 306: S02 opens on a push)
# ============== SET STU: radio studio 1934 (X=300) ==============
UX=300.0
room('stu',UX,6.0,5.0,2.9,'studiowall','dwood',ftile=(2.0,2.0))
ona=[plane(f'onair{i}',(UX+0.9,2.47,2.3),0.72,0.24,card_mat(f'onair{i}',f'onair{i}',emit=(0.3 if i==0 else 2.0))) for i in range(2)]
vis(ona[0],[(0,136)]); vis(ona[1],[(137,END)])
g_on=glow('onair_glow',(UX+0.9,2.4,2.3),1.1,(255,80,60),2.0,on=(137,END))
box('stu_win',(UX-1.3,2.47,1.6),(1.6,0.06,1.0),flat('winframe2',lin((90,60,40)),0.5),bv=0.02); plane('stu_glass',(UX-1.3,2.43,1.6),1.45,0.85,flat('ctrlglass',lin((60,80,90)),0.1))
for k in range(3): box(f'stu_dial{k}',(UX-1.75+k*0.45,2.44,1.35),(0.3,0.04,0.2),flat('dialpanel',lin((50,52,56)),0.4),bv=0.01); glow(f'stu_dg{k}',(UX-1.75+k*0.45,2.40,1.38),0.2,(255,210,120),3.0)
mic=flat('micchrome',(0.7,0.7,0.72),0.25,metal=0.9)
MX_=UX+0.42
cyl('mic_base',(MX_,0.95,0.03),0.22,0.06,mic,v=20); cyl('mic_pole',(MX_,0.95,0.62),0.02,1.2,mic,v=10)
box('mic_head',(MX_,0.9,1.3),(0.14,0.06,0.2),mic,bv=0.05,seg=3); box('mic_ring',(MX_,0.9,1.3),(0.2,0.03,0.28),flat('micring',lin((40,40,44)),0.4),bv=0.02)
box('stu_piano',(UX+2.2,1.9,0.6),(1.4,0.6,1.2),flat('piano',lin((40,28,24)),0.3),bv=0.03); box('stu_keys',(UX+2.2,1.55,0.78),(1.3,0.18,0.05),flat('keys',lin((246,244,236)),0.4),bv=0.005)
for k in range(2): cyl(f'stu_score{k}',(UX+1.9+k*0.5,1.65,1.25),0.12,0.02,flat('sheet',lin((246,240,220)),0.6),v=4,rot=(math.radians(80),0,0))
wclk=cyl('stu_clock',(UX-0.1,2.46,2.35),0.25,0.05,flat('clockrim',lin((70,48,34)),0.5),v=24,rot=(math.pi/2,0,0)); cyl('stu_clockf',(UX-0.1,2.43,2.35),0.22,0.01,flat('clockface',lin((246,240,226)),0.6),v=24,rot=(math.pi/2,0,0))
chair('stu_chair',(UX-2.2,1.6)); box('stu_stand',(UX+1.2,1.3,0.55),(0.08,0.08,1.1),INK,bv=0); box('stu_standtop',(UX+1.2,1.27,1.12),(0.4,0.04,0.3),flat('standwood',lin((110,74,48)),0.5),bv=0.01)
bpy.ops.object.light_add(type='AREA',location=(UX,-2.0,2.5),rotation=(math.radians(65),0,0)); a_=bpy.context.object; a_.data.energy=800; a_.data.size=4; a_.data.color=(1.0,0.92,0.82)
# ---------- S02 (113-196): "In 1934, a radio man named George Richards" - the ON AIR sign lights on 'In', he leans into the mic ----------
s='S02'; r=SH[s]
rm2=char('S02_rich','radioman',s,(UX+0.0,1.25,0),r,'talkD',arms=('arm','arm')); ALL.append(rm2)
faces(rm2,[(113,'deadpan'),(137,'talkA')]); lipsync(rm2,[w for w in WORDS if 4.4<=w[1]<=7.3],137,196); faces(rm2,[(176,'grin')])
arm(rm2,1,113,-15); arm(rm2,1,137,-60); arm(rm2,1,142,-55); arm(rm2,1,174,-120); arm(rm2,1,180,-110); arm(rm2,-1,150,-30); arm(rm2,-1,156,-45)
bob(rm2,[137,174,190])
fg2=box('S02_fgmic',(UX+0.62,-0.2,1.0),(0.12,0.12,2.0),flat('boom',lin((60,60,66)),0.4),bv=0.03,coll=L.chr_coll(s))   # FG boom pole (rule 311)
path(s,[(113,(UX+0.7,-1.4,1.3),(UX+0.0,1.2,1.2)),(150,(UX+0.45,-0.95,1.28),(UX+0.0,1.2,1.22)),(176,(UX+0.3,-0.7,1.27),(UX+0.0,1.2,1.25)),(196,(UX+0.25,-0.62,1.27),(UX+0.0,1.2,1.25))])
# ============== SET OFF: Richards' office 1934 (X=340) ==============
OX=340.0
room('off',OX,7.0,6.0,3.0,'office34','dwood',ftile=(2.0,2.0))
box('rug_off',(OX,0.6,0.004),(3.4,2.4,0.008),surf('rug34','rug34',(3.4,2.4),gen=True),bv=0)
DX,DY=OX-0.4,0.85
desk_h=0.78
box('odesk_top',(DX,DY,desk_h-0.03),(1.9,0.85,0.06),WOOD,bv=0.015)
for sx in(-1,1): box(f'odesk_ped{sx}',(DX+sx*0.7,DY,(desk_h-0.06)/2),(0.46,0.8,desk_h-0.06),WOOD,bv=0.015)
box('odesk_front',(DX,DY-0.38,desk_h/2),(0.96,0.04,desk_h-0.2),WOOD,bv=0.01)
for sx in(-1,1):
    for j in range(3): box(f'odesk_dr{sx}{j}',(DX+sx*0.7,DY-0.41,0.15+j*0.2),(0.38,0.03,0.16),flat('drawer',lin((130,86,56)),0.5),bv=0.01)
k_=flat('bakelite',lin((30,26,26)),0.3)
def phoneD(n,c,coll=None):
    cyl(n+'_b',(c[0],c[1],c[2]+0.04),0.08,0.08,k_,v=16,coll=coll); cyl(n+'_st',(c[0],c[1],c[2]+0.2),0.025,0.25,k_,v=10,coll=coll); cyl(n+'_mo',(c[0],c[1]-0.04,c[2]+0.34),0.05,0.06,k_,v=14,rot=(math.radians(70),0,0),coll=coll)
phoneD('ophone1',(DX+0.7,DY-0.1,desk_h)); phoneD('ophone2',(DX-0.8,DY-0.05,desk_h))
lampT('olamp',(DX-0.95,DY+0.2,desk_h),shade=(60,120,80))
for k in range(4): box(f'opaper{k}',(DX+0.1+0.05*k,DY-0.05,desk_h+0.005+0.004*k),(0.3,0.22,0.004),flat('paperw',lin((244,238,222)),0.8),bv=0)
money=[box(f'omoney{k}',(DX-0.05,DY-0.2,desk_h+0.02+0.03*k),(0.28,0.14,0.03),flat('cash',lin((140,180,120)),0.7),bv=0.005) for k in range(6)]
for k,m_ in enumerate(money): vis(m_,[(-9,-8)])   # r2: the cash travels in the hands (arm_money), not as a stack sliding by itself
# back wall: calendar (left), door (far left), map (right), switchboard under the map
CALX,CALZ=OX-1.25,1.55
cal_names=['cal1934a','cal1934']+[f'cal{y}' for y in range(1935,1946)]+['cal2026']
cals=[plane(f'cal_{n}',(CALX,2.97,CALZ),0.48,0.64,card_mat(n,n,emit=0.25)) for n in cal_names]
door=box('odoor',(OX-2.65,2.6,1.1),(0.95,0.06,2.2),flat('doorwood',lin((110,74,48)),0.5),bv=0.02); box('odoor_fr',(OX-2.65,2.99,1.15),(1.1,0.04,2.32),flat('doorfr',lin((70,48,34)),0.5),bv=0.01)
plane('odoor_dark',(OX-2.65,2.965,1.1),0.92,2.18,flat('hallway',lin((60,50,44)),0.9))
kloc(door,844,(OX-2.65,2.6,1.1)); kloc(door,858,(OX-3.55,2.6,1.1))   # r2: 14 f slide (was 6)
MAPX,MAPZ=OX+1.6,1.75
maps=[plane(f'map_{n}',(MAPX,2.962,MAPZ),2.3,1.44,card_mat(f'map{n}',f'map{n}',emit=0.35)) for n in (0,10,30,60,94)]
box('map_fr',(MAPX,2.99,MAPZ),(2.42,0.04,1.56),flat('mapfr',lin((80,54,36)),0.5),bv=0.01)
sw=box('switchboard',(MAPX+0.2,2.5,0.62),(1.5,0.5,1.24),WOOD,bv=0.02)
plane('sw_panel',(MAPX+0.2,2.24,0.95),1.3,0.5,flat('swpanel',lin((40,36,32)),0.5))
jacks=[]
for i in range(8):
    for j in range(3): cyl(f'sw_j{i}{j}',(MAPX-0.35+i*0.155,2.23,0.8+j*0.14),0.022,0.01,flat('jack',lin((200,170,80)),0.3,metal=0.6),v=10,rot=(math.pi/2,0,0))
lamps_sw=[glow(f'sw_l{i}',(MAPX-0.35+i*0.155,2.21,1.15),0.07,(255,200,90),4.0) for i in range(8)]
cords=[]
for i in range(6):
    c_=cyl(f'sw_cord{i}',(MAPX-0.3+i*0.18,2.2,0.72),0.012,0.3,flat('cord',lin((30,30,30)),0.6),v=6,rot=(math.radians(20),0,0)); cords.append(c_)
cabinetM=flat('cabinet',lin((110,120,110)),0.4,metal=0.3)
box('ocab',(OX+3.1,2.6,0.65),(0.5,0.6,1.3),cabinetM,bv=0.02)
frame_pic('oph1',(OX-0.4,2.97,2.35),0.55,0.42,'dfac0'); frame_pic('oph2',(OX+0.25,2.97,2.3),0.32,0.42,'paperTigers')
cyl('ofan',(OX+2.9,2.4,1.45),0.18,0.06,flat('fanm',lin((60,70,64)),0.4,metal=0.5),v=20,rot=(math.pi/2,0,0))
bpy.ops.object.light_add(type='AREA',location=(OX,-2.6,2.7),rotation=(math.radians(62),0,0)); a_=bpy.context.object; a_.data.energy=1000; a_.data.size=6; a_.data.color=(1.0,0.93,0.84)
# ---------- S03 (197-330): he buys a small-town team from Ohio: cash across the desk to the seller ----------
s='S03'; r=SH[s]
rm3=char('S03_rich','radioman',s,(DX+0.35,DY+0.75,0),r,'grin',arms=('arm',[(197,'arm'),(250,'arm_money'),(300,'arm')]))
sel=char('S03_seller','seller',s,(DX-0.9,DY-0.75,0),r,'deadpan',arms=('arm',[(197,'arm'),(300,'arm_money')]))
ALL+=[rm3,sel]
faces(rm3,[(197,'grin'),(224,'talkA'),(232,'talkB'),(240,'talkC'),(250,'smug'),(294,'wink'),(316,'grin')]); faces(sel,[(197,'deadpan'),(236,'happy'),(294,'wow'),(306,'happy')])
for f,a in [(197,-15),(250,-20),(256,-75),(294,-80),(300,-20)]: arm(rm3,-1,f,a)
for f,a in [(197,-12),(296,-70),(302,-25)]: arm(sel,1,f,a)
bob(sel,[236,294]); bob(rm3,[250,294])

fg3=box('S03_fgbooks',(DX+1.05,DY-1.05,(desk_h+0.3)/2),(0.34,0.3,desk_h+0.3),flat('booksfg',lin((96,62,40)),0.6),bv=0.01,coll=L.chr_coll(s))
path(s,[(197,(DX+0.4,DY-3.4,1.5),(DX-0.25,DY+0.3,1.1)),(251,(DX+0.1,DY-3.2,1.5),(DX-0.3,DY+0.25,1.08)),(294,(DX-0.3,DY-2.9,1.45),(DX-0.35,DY+0.1,1.02)),(330,(DX-0.45,DY-2.8,1.44),(DX-0.4,DY+0.1,1.02))])
# ============== SET STR: Detroit street 1934, ballpark gate, newsstand (X=600) ==============
SX=600.0
ROAD=surf('droad','dasphalt',(12,12)); WALK=surf('dwalk','dsidewalk',(2.6,2.6))
box('str_road',(SX,-7,-0.1),(120,10,0.2),ROAD,bv=0); box('str_walk',(SX,0,0.07),(120,5,0.14),WALK,bv=0.03); box('str_walk2',(SX,-14,0.07),(120,5,0.14),WALK,bv=0.03)
def building(n,front,tex,w=8.0,h=12.0,d=8.0,facing='-Y',side=None,cap=(64,52,48)):
    fx,fy=front; ay=-1 if facing=='-Y' else 1
    box(n,(fx,fy-ay*d/2,h/2-0.3),(w,d,h+0.6),surf('side_'+(side or tex),'side_'+(side or tex),(w,h),gen=True),bv=0.02)
    plane(n+'_front',(fx,fy+ay*0.012,h/2),w,h,card_mat('fac_'+tex,tex,emit=0.12),face=facing)
    k_=int(''.join(ch for ch in n if ch.isdigit()) or 0); j_=0.012*(k_%4)
    box(n+'_cap',(fx,fy-ay*d/2+ay*0.2,h+0.25),(w+0.4+j_,d+0.4+j_,0.5+j_),flat('cap%d'%sum(cap),lin(cap),0.7),bv=0.04)
for j in range(10):
    x=SX-36+j*8; building(f'bS{j}',(x,2.5),f'dfac{j%6}')
    if j%3==1: building(f'bN{j}',(x+3,-16.5),f'dfac{(j+2)%6}',facing='+Y')
sk=plane('S_sky',(SX,140,40),340,190,card_mat('dsky','dsky',emit=1.0),coll=L.C_NOI); sk['fly']=1
sl=plane('S_skyline',(SX,110,14),260,260*1500/4096,card_mat('dskyline','dskyline',emit=0.6),coll=L.C_NOI); sl['fly']=1
LPM=flat('lampmetal',lin((52,74,62)),0.45,metal=0.35)
def lamppost(n,loc):
    cyl(n+'_base',(loc[0],loc[1],0.25),0.16,0.5,LPM,v=12); cyl(n+'_pole',(loc[0],loc[1],2.4),0.07,4.0,LPM,v=10)
    cyl(n+'_cap',(loc[0],loc[1],4.45),0.12,0.1,LPM,v=12); sph(n+'_glob',(loc[0],loc[1],4.75),0.28,LAMPG,sc_=(1,1,1.15))
for j,x in enumerate([SX-26,SX-12,SX+10,SX+18]): lamppost(f'Slp{j}',(x,-2.1))   # r2 G6: SX+4 cut the S of LIONS
def truck(n,loc,heading,col=(90,40,36)):
    e=empty(n,loc); e.rotation_euler=(0,0,math.radians(heading)); bd=flat('truck_'+n,lin(col),0.4)
    P=[box(n+'_cab',(0,1.6,1.25),(1.9,1.4,1.4),bd,bv=0.15,seg=3),box(n+'_hood',(0,2.8,0.95),(1.4,1.2,0.8),bd,bv=0.18,seg=3),
       box(n+'_win',(0,2.2,1.5),(1.6,0.06,0.6),GLASS,bv=0.02),box(n+'_bed',(0,-0.9,0.8),(2.1,3.6,0.18),surf('truckbed','wood',(0.6,0.6)),bv=0.02),
       box(n+'_grill',(0,3.42,0.95),(1.0,0.06,0.7),CHROME,bv=0.03)]
    for sx in(-1,1):
        P.append(box(f'{n}_rail{sx}',(sx*1.03,-0.9,1.1),(0.06,3.6,0.45),surf('truckbed','wood',(0.6,0.6)),bv=0.01))
        P.append(sph(f'{n}_hl{sx}',(sx*0.55,3.45,1.25),0.14,LAMPG,sc_=(1,0.6,1)))
        P.append(box(f'{n}_fend{sx}',(sx*0.95,2.6,0.6),(0.4,1.2,0.3),flat('fender',lin((30,28,30)),0.4),bv=0.12,seg=3))
        for sy in(-1.8,2.6): P.append(cyl(f'{n}_w{sx}{sy}',(sx*0.95,sy,0.42),0.42,0.3,TYRE,v=20,rot=(0,math.pi/2,0)))
    for p in P: p.parent=e
    return e
# LIONS banner painted letter by letter on the facade above the shop (on 'called it the Lions')
BANX,BANZ=SX+4,5.2
ban=[plane(f'lionsban{n}',(BANX,2.47,BANZ),5.0,1.25,card_mat(f'lions{n}',f'lions{n}',emit=0.3)) for n in range(6)]
LT_=[366,371,376,381,386,390]
for n,b_ in enumerate(ban): vis(b_,[((331 if n==0 else LT_[n-1]),(LT_[n]-1 if n<5 else END))])
lad=flat('ladder',lin((150,110,70)),0.6)
for sx in(-1,1): box(f'ladder{sx}',(BANX+1.6+sx*0.25,2.3,1.75),(0.07,0.07,3.5),lad,bv=0)
for k in range(8): box(f'ladrung{k}',(BANX+1.6,2.3,0.4+k*0.42),(0.5,0.05,0.04),lad,bv=0)
bpy.ops.object.light_add(type='AREA',location=(SX,-18,9),rotation=(math.radians(62),0,0)); a_=bpy.context.object; a_.name='str_fill'; a_.data.energy=9000; a_.data.size=40; a_.data.color=(1.0,0.93,0.82)
# ---------- S04 (331-414): the team arrives by truck; the painter letters LIONS on the banner ----------
s='S04'; r=SH[s]
tk=truck('truck',(SX-14,-5.0,0.0),-90)
kloc(tk,331,(SX-14,-5.0,0.0)); kloc(tk,392,(SX+1.5,-5.0,0.0)); kloc(tk,414,(SX+3.0,-5.0,0.0))
pl=[]
for i,(dx,kd) in enumerate([(-0.9,'lion'),(0.0,'lion2'),(0.9,'lion')]):
    ch=char(f'S04_pl{i}',kd,s,(0,0,0),r,'grit',arms=('arm','arm_ball' if i==1 else 'arm'))
    ch['root'].parent=tk; ch['root'].location=(dx*1.0, -0.9+dx*1.3, 0.9+(0.3 if i==1 else 0.0))   # r2 P3: no row facing camera   # riding on the bed (truck local frame)
    pl.append(ch)
ALL+=pl
for i,ch in enumerate(pl): faces(ch,[(331,'grit'),(360+i*4,'cheer'),(390+i*2,'shock')]); cheer(ch,340+i*5,388,10+i,up=(-140,-120),side=(-1,1,1)[i])
pnt=char('S04_painter','fanold',s,(BANX+1.6,2.25,3.4),r,'deadpan',arms=('arm',[(331,'arm')])); ALL.append(pnt)   # r2: brush reaches the banner
faces(pnt,[(331,'deadpan'),(366,'shout'),(392,'cheer')])
for k,f in enumerate(range(362,392,5)): arm(pnt,-1,f,-158-10*(k%2))
ex4=crowd(s,r,[(SX+11.5,1.2,0.14),(SX+13.5,0.8,0.14),(SX+7,1.4,0.14),(SX+9.5,0.9,0.14)],['fanman','fanlady','newsboy','fanold'],44); ALL+=ex4
for e in ex4: faces(e,[(392,'cheer')]); cheer(e,394,414,hash(e['inst'])%97)
path(s,[(331,(SX-15.5,-11.6,2.0),(SX-15.0,-5,1.45)),(345,(SX-11.5,-11.8,2.0),(SX-11.6,-5,1.5)),(360,(SX-7.5,-11.6,2.0),(SX-7.2,-5,1.5)),(390,(SX+1,-12.4,2.4),(SX+2.8,0,3.3)),(414,(SX+1.5,-12.6,2.55),(SX+3.1,0,3.5))])
# ---------- S05 (415-494): "Detroit was a baseball town" - the crowd pours into the ballpark gate ----------
GX=SX+30
gate=flat('gatebrick',lin((150,80,60)),0.7)
for sx in(-1,1): box(f'gate_pier{sx}',(GX+sx*3.2,3.0,3.0),(1.4,1.4,6.0),surf('gbrick','stadwall',(2,2)),bv=0.03)
box('gate_arch',(GX,3.0,6.4),(8.0,1.5,1.2),surf('gbrick','stadwall',(2,2)),bv=0.03)
plane('gate_sign',(GX,2.245,6.4),5.6,1.4,card_mat('ballsign','ballsign',emit=0.25))
for k in range(5):
    pn=plane(f'pennant{k}',(GX-4+k*2,2.2,7.6),0.9,0.5,flat('pen%d'%k,lin([(200,60,40),(240,200,60),(60,90,160)][k%3]),0.6)); pn.rotation_euler[1]=math.radians(15*((k%2)*2-1)); pn['fly']=1
s='S05'; r=SH[s]
sp=[(GX-2.8,0.3,0.14),(GX-1.6,-0.8,0.14),(GX-0.4,0.6,0.14),(GX+0.9,-0.5,0.14),(GX+2.9,0.4,0.14),(GX-1.0,-2.0,0.14),(GX+1.6,-1.9,0.14),(GX-3.3,-1.5,0.14),(GX+3.1,-1.2,0.14)]
ex5=crowd(s,r,sp,['fanman','fanlady','kid34','fanold','fanman','newsboy','fanlady','fanold','fanman'],55,faces_pool=('cheer','happy','shout'),walker=True); ALL+=ex5
for i,e in enumerate(ex5): cheer(e,415+i*4,494,60+i,up=(-160,-120)); walk(e,415,494,sp[i],(sp[i][0]+random.Random(i).uniform(-0.4,0.4),min(sp[i][1]+1.6,1.6),0.14),step=4)
path(s,[(415,(GX+0.8,-6.5,1.5),(GX,1.0,1.8)),(452,(GX+0.4,-8.2,3.2),(GX,2.0,3.2)),(475,(GX,-7.8,4.4),(GX,2.5,4.4)),(494,(GX-0.2,-7.6,4.8),(GX,2.5,4.8))])
# ---------- S06 (495-547): newsstand: TIGERS WIN PENNANT, push-in on the paper ----------
NX=SX-20
box('kiosk',(NX,1.2,1.1),(2.2,1.0,2.2),flat('kiosk',lin((60,90,70)),0.6),bv=0.04); box('kiosk_roof',(NX,1.0,2.27),(2.6,1.5,0.15),flat('kroof',lin((140,50,40)),0.6),bv=0.04)
for k in range(4): plane(f'kpaper{k}',(NX-0.9+k*0.6,0.697,0.95),0.4,0.55,card_mat('paperTigers_k','paperTigers',emit=0.2))
s='S06'; r=SH[s]
nb=char('S06_newsboy','newsboy',s,(NX+0.2,0.0,0.14),r,'shout',arms=('arm','armS'),scale=0.8); ALL.append(nb)
faces(nb,[(495,'shout'),(518,'happy'),(530,'shout')]); arm(nb,1,495,-150); arm(nb,1,520,-160); arm(nb,-1,500,-40); arm(nb,-1,525,-70)
pap=plane('S06_paper',(0,0,0),0.5,0.68,card_mat('paperTigers','paperTigers',emit=0.35),coll=L.chr_coll(s)); pap.parent=nb['root']; pap.location=(0.38,-0.06,1.5); vis(pap,[r]); pap['chr']='S06_newsboy'; pap['fly']=1
path(s,[(495,(NX+0.6,-2.4,1.5),(NX+0.45,0.0,1.25)),(520,(NX+0.55,-1.9,1.6),(NX+0.45,0.0,1.35)),(547,(NX+0.52,-1.65,1.62),(NX+0.45,0.0,1.4))])
# ============== SET STA: University-of-Detroit-style 1934 stadium, wooden bleachers (X=900) ==============
TX=900.0
box('sta_field',(TX,0,-0.1),(70,46,0.2),surf('field','field',(16,16)),bv=0)
BLE=surf('bleacher','bleacher',(3,3))
for k in range(12): box(f'bleach{k}',(TX,14+k*0.9,0.25+k*0.45),(60,0.9,0.5+k*0.9),BLE,bv=0.02)   # stepped stands behind the field
box('sta_wall',(TX,13.3,0.6),(60,0.4,1.2),surf('stadwall','stadwall',(3,3)),bv=0.02)
box('sta_back',(TX,25.0,4.5),(62,0.6,9.0),surf('stadwall','stadwall',(3,3)),bv=0.02)
for j in range(7): cyl(f'sta_post{j}',(TX-27+j*9,24.3,6.5),0.15,7,flat('post',lin((60,74,64)),0.5),v=10)
sky2=plane('T_sky',(TX,150,30),360,200,card_mat('dsky_grey','dsky_grey',emit=1.0),coll=L.C_NOI); sky2['fly']=1
crowdcards=[plane(f'crowdcard{k}',(TX-22+k*14.7,21.2,8.3),14.6,7.3,card_mat('crowdcard','crowdcard',emit=0.25)) for k in range(4)]
for c_ in crowdcards: c_['fly']=1; c_.rotation_euler[0]=math.radians(-45); vis(c_,[(1277,1349),(1402,1536),(1718,1795)])   # painted far rows lie on the 45-degree stands; empty stands in S07
SBX,SBY=TX-14,10.0
bpy.ops.object.light_add(type='AREA',location=(TX-10,-2,11),rotation=(math.radians(58),0,0)); a_=bpy.context.object; a_.name='sta_fill'; a_.data.energy=14000; a_.data.size=50; a_.data.color=(1.0,0.9,0.78)
for sx in(-1,1): cyl(f'sb_pole{sx}',(SBX+sx*1.6,SBY,3.0),0.12,6.0,flat('sbpole',lin((60,74,64)),0.5),v=10)
box('sb_box',(SBX,SBY+0.1,6.6),(4.4,0.3,2.3),flat('sbbox',lin((40,50,44)),0.5),bv=0.03)
sbs=[plane(f'score{i}',(SBX,SBY-0.06,6.6),4.0,2.0,card_mat(f'score{i}',f'score{i}',emit=0.6)) for i in range(2)]
vis(sbs[0],[(0,1452)]); vis(sbs[1],[(1453,END)])
for j,(x,y) in enumerate([(TX-6,8),(TX+6,8)]):   # goalposts (H shape)
    cyl(f'gp{j}_a',(x-1.4,y,2.0),0.06,4.0,flat('gp',lin((236,232,220)),0.5),v=8); cyl(f'gp{j}_b',(x+1.4,y,2.0),0.06,4.0,flat('gp',lin((236,232,220)),0.5),v=8)
    cyl(f'gp{j}_c',(x,y,1.2),0.06,2.8,flat('gp',lin((236,232,220)),0.5),v=8,rot=(0,math.pi/2,0))
BENX=TX+8
box('bench',(BENX,4.0,0.42),(3.0,0.4,0.06),WOOD,bv=0.01);
for sx in(-1,1): box(f'bench_l{sx}',(BENX+sx*1.3,4.0,0.2),(0.08,0.36,0.4),INK,bv=0)
for k in range(3): cyl(f'bucket{k}',(BENX-2.0+k*0.35,3.7,0.18),0.14,0.36,flat('bucket',lin((150,150,156)),0.4,metal=0.5),v=14)
cyl('waterjug',(BENX+1.9,3.8,0.3),0.2,0.6,flat('jug2',lin((200,60,40)),0.5),v=16)
# ticket booth outside the wall (X=TX+60)
BX_=TX+60
box('booth',(BX_,2.0,1.3),(2.4,1.6,2.6),flat('boothbody',lin((180,60,50)),0.6),bv=0.04); box('booth_roof',(BX_,1.9,2.7),(2.8,2.0,0.2),flat('broof',lin((60,60,70)),0.6),bv=0.04)
bth=[plane(f'booth{i}',(BX_,1.18,1.35),2.3,2.3,card_mat(f'booth{i}',f'booth{i}',emit=0.25)) for i in range(2)]
vis(bth[0],[(0,1244)]); vis(bth[1],[(1245,END)])
box('booth_ground',(BX_,0,-0.1),(50,30,0.2),surf('dwalk','dsidewalk',(2.6,2.6)),bv=0)
box('booth_wall',(BX_,6,2.5),(40,0.5,5.0),surf('stadwall','stadwall',(3,3)),bv=0.02)
for k in range(6): pn=plane(f'bpen{k}',(BX_-5+k*2,5.747,4.6),0.8,0.45,flat('pen%d'%(k%3),lin([(200,60,40),(240,200,60),(60,90,160)][k%3]),0.6))
# ---------- S07 (548-605): empty seats: one fan alone, a player looks up at the stands ----------
s='S07'; r=SH[s]
lone=char('S07_lone','fanold',s,(TX+1.0,14.9,1.4),r,'deadpan',arms=('arm','arm_hotdog')); ply=char('S07_player','lion',s,(TX-1.2,9.5,0.0),r,'sad',arms=('arm','arm_ball'))
ALL+=[lone,ply]
faces(lone,[(548,'deadpan'),(572,'sad'),(590,'deadpan')]); faces(ply,[(548,'shock'),(570,'sad')]); arm(lone,1,560,-60); arm(lone,1,566,-20); arm(lone,1,584,-62); bob(ply,[570])
path(s,[(548,(TX-0.8,5.2,1.3),(TX,13,2.4)),(580,(TX-1.3,3.6,1.6),(TX,14,2.8)),(605,(TX-1.6,2.6,1.9),(TX,15,3.2))])
# ---------- S14 (1277-1349): 26,000 people on a holiday: crane up over packed stands ----------
s='S14'; r=SH[s]
sp=[]
for k in range(4):
    for j in range(7): sp.append((TX-6+j*2.0+(k%2)*0.9,14.0+k*1.8,0.5+k*1.8))
ex14=crowd(s,r,sp,['fanman','fanlady','fanold','kid34','fanman','fanlady','newsboy'],71,faces_pool=('cheer','happy','shout')); ALL+=ex14
for i,e in enumerate(ex14): cheer(e,1277+(i*3)%20,1349,80+i,up=(-160,-115))
path(s,[(1277,(TX,4.0,1.2),(TX,16,2.6)),(1314,(TX+0.5,5.0,3.0),(TX,17,3.4)),(1349,(TX+1.0,5.6,5.0),(TX,18,4.0))])
# ---------- S16 (1402-1536): the Lions lost 19-16: scoreboard flips; the camera drops to the bench ----------
s='S16'; r=SH[s]
b1=char('S16_bear','bear',s,(SBX+2.2,7.2,0),r,'smug',arms=('arm','arm_ball')); b2=char('S16_bear2','bear',s,(SBX+3.6,6.4,0),r,'cheer',arms=('arm','arm'))
l1=char('S16_lion','lion',s,(BENX+0.0,4.2,0.0),r,'deadpan',arms=('arm','arm')); l2=char('S16_lion2','lion2',s,(BENX-1.15,3.55,0.0),r,'sad',arms=('arm','arm'))
ALL+=[b1,b2,l1,l2]
faces(b1,[(1402,'smug'),(1453,'cheer'),(1480,'smug')]); faces(b2,[(1402,'grit'),(1453,'cheer')]); cheer(b2,1455,1500,91); cheer(b1,1458,1490,92)
faces(l1,[(1402,'grit'),(1453,'shock'),(1462,'sad'),(1508,'deadpan'),(1520,'sad')]); faces(l2,[(1402,'grit'),(1455,'shock'),(1465,'sad')])
for c_ in (l1,l2):
    for sx in(-1,1): arm(c_,sx,1453,-25); arm(c_,sx,1460,-8)
bob(l1,[1453,1508]); bob(l2,[1455])
path(s,[(1402,(SBX+1.0,1.0,1.6),(SBX,SBY,5.8)),(1440,(SBX+1.4,1.6,1.8),(SBX,SBY,6.4)),(1453,(SBX+1.5,1.8,1.85),(SBX,SBY,6.5)),(1480,(SBX+4.0,0.6,1.5),(SBX+3,6,1.6)),
        (1508,(BENX-0.5,0.8,1.25),(BENX-0.5,4.2,0.95)),(1536,(BENX-0.45,1.15,1.22),(BENX-0.5,4.2,0.95))])
# ---------- S19 (1718-1795): 'a stunt that lost its very first game': 1934 field at dusk, the radio man grins in the stands under the final score ----------
s='S19'; r=SH[s]
rm19=char('S19_rich','radioman',s,(SBX+1.0,14.9,1.4),r,'grin',arms=('arm','arm_mic')); ALL.append(rm19)
faces(rm19,[(1718,'deadpan'),(1746,'wink'),(1760,'grin'),(1772,'idea')]); arm(rm19,1,1750,-120); arm(rm19,1,1770,-140); bob(rm19,[1746,1772])
ex19=crowd(s,r,[(SBX-1.5,14.9,1.4),(SBX+3.2,15.8,2.3),(SBX-0.2,16.7,3.2),(SBX+2.4,14.9,1.4)],['fanman','fanlady','fanold','kid34'],93); ALL+=ex19
path(s,[(1718,(SBX+0.5,11.0,2.85),(SBX+0.9,14.9,2.55)),(1760,(SBX+0.85,12.3,2.75),(SBX+1.0,14.9,2.55)),(1795,(SBX+0.95,12.8,2.72),(SBX+1.0,14.9,2.55))])
# ---------- S13 (1227-1276): ticket booth: the clerk slaps up SOLD OUT on 'sold' ----------
s='S13'; r=SH[s]
clk=char('S13_clerk','clerk',s,(BX_+0.72,-0.25,0.0),r,'happy',arms=('arm','arm')); ALL.append(clk)
faces(clk,[(1227,'happy'),(1245,'wow'),(1258,'happy')]); arm(clk,1,1238,-40); arm(clk,1,1243,-150); arm(clk,1,1250,-30); bob(clk,[1245])
ex13=crowd(s,r,[(BX_-0.75,-1.2,0),(BX_-2.6,-1.3,0),(BX_+1.8,-1.0,0),(BX_-3.6,-0.6,0)],['fanman','fanlady','fanold','kid34'],97,faces_pool=('shock','sad','shout','wow')); ALL+=ex13
for e in ex13: faces(e,[(1248,'shock')])
path(s,[(1227,(BX_+0.15,-3.15,1.45),(BX_+0.35,1.2,1.5)),(1245,(BX_-0.05,-3.45,1.42),(BX_+0.25,1.2,1.5)),(1276,(BX_-0.3,-3.8,1.4),(BX_+0.1,1.2,1.45))])   # pull-back reveal (rule 306: S12 ends on a push)
# ============== SET DIN: dining room 1934 (X=1200) ==============
NX2=1200.0
room('din',NX2,6.0,5.0,2.8,'dining','dwood',ftile=(2.0,2.0))
box('din_rug',(NX2,0.9,0.004),(3.6,2.6,0.008),surf('rug34','rug34',(3.6,2.6),gen=True),bv=0)
TH=table('dtable',(NX2,0.6))
turkey('din_turkey',(NX2,0.6,TH),steam=(1350,1409)); plates('dplates',(NX2,0.6+0.25),(-0.7,-0.25,0.25,0.7),TH)
for k,x in enumerate((-0.85,0.85)): cyl(f'dcandle{k}',(NX2+x,0.6,TH+0.15),0.025,0.3,flat('candle',lin((246,236,210)),0.5),v=12); glow(f'dcg{k}',(NX2+x,0.55,TH+0.36),0.16,(255,200,120),5.0)
for k,x in enumerate((-0.6,0.0,0.6)): chair(f'dchair{k}',(NX2+x,1.45))
rad=radio34('dradio',(NX2+2.2,1.6))
glow('dradio_glow',(NX2+2.2,1.37,0.47),0.25,(255,210,120),3.0)
box('dbuffet',(NX2-2.1,2.15,0.5),(1.4,0.5,1.0),WOOD,bv=0.02)
for k in range(4): cyl(f'dpie{k}',(NX2-2.6+k*0.33,2.1,1.04),0.12,0.06,flat('pie%d'%(k%2),lin([(200,140,60),(170,90,50)][k%2]),0.6),v=18)
box('din_win',(NX2+0.6,2.47,1.7),(1.4,0.06,1.2),flat('winframe3',lin((240,236,220)),0.5),bv=0.02); plane('din_view',(NX2+0.6,2.43,1.7),1.25,1.05,card_mat('dsky_v','dsky_grey',emit=0.7))
for sx in(-1,1): box(f'din_curt{sx}',(NX2+0.6+sx*0.72,2.4,1.7),(0.3,0.04,1.4),flat('curtain',lin((190,70,60)),0.8),bv=0.02)
frame_pic('dph1',(NX2-1.0,2.47,1.85),0.45,0.35,'dfac3'); frame_pic('dph2',(NX2-1.7,2.47,1.7),0.3,0.4,'dfac5')
lampT('din_lamp',(NX2-2.6,2.1,1.0),shade=(220,180,120))
bpy.ops.object.light_add(type='AREA',location=(NX2,-2.2,2.5),rotation=(math.radians(60),0,0)); a_=bpy.context.object; a_.data.energy=850; a_.data.size=5; a_.data.color=(1.0,0.92,0.8)
bpy.ops.object.light_add(type='POINT',location=(NX2,0.6,1.9)); a_=bpy.context.object; a_.data.energy=60; a_.data.color=(1.0,0.85,0.6)
# ---------- S08 (598-716): "Football on a holiday? Everybody figured folks would stay home and eat." ----------
s='S08'; r=SH[s]
d8=char('S08_dad','dad34',s,(NX2-1.3,0.55,0),r,'deadpan',arms=('arm','arm_fork')); m8=char('S08_mom','mom34',s,(NX2+0.4,1.2,0),r,'happy',arms=('arm_plate','arm'))
g8=char('S08_gramps','gramps',s,(NX2+1.5,1.55,0),r,'deadpan',arms=('arm','arm_fork')); k8=char('S08_kid','kid34',s,(NX2-1.55,0.35,0),r,'wow',arms=('arm_ball','arm'),scale=0.8)
ALL+=[d8,m8,g8,k8]
faces(d8,[(598,'deadpan'),(626,'shrug'),(650,'deadpan'),(684,'happy'),(700,'cheer')]); faces(m8,[(598,'happy'),(626,'deadpan'),(660,'happy'),(692,'wow')])
faces(g8,[(598,'deadpan'),(626,'eyeroll'),(660,'deadpan'),(700,'cheer')]); faces(k8,[(598,'wow'),(626,'happy'),(690,'wow')])
for c_,sx in ((d8,1),(g8,1)):
    for f in range(684,716,10): arm(c_,sx,f,-60); arm(c_,sx,f+5,-85)
arm(d8,-1,626,-110); arm(d8,-1,634,-100); arm(d8,-1,650,-15); arm(g8,-1,626,-160); arm(g8,-1,640,-20); arm(k8,-1,612,-140); arm(k8,-1,640,-60)
bob(d8,[626,700]); bob(g8,[626]); bob(m8,[692]); bob(k8,[612])
lipsync(g8,[w for w in WORDS if 20.4<=w[1]<=23.9],600,716)   # r2 C6: the doubter's line is spoken by gramps
path(s,[(598,(NX2+0.9,-3.4,2.0),(NX2,1.0,1.15)),(626,(NX2+0.6,-3.2,1.95),(NX2,1.0,1.17)),(684,(NX2+0.1,-2.9,1.9),(NX2,1.0,1.18)),(716,(NX2-0.15,-2.8,1.88),(NX2,1.0,1.18))])
# ---------- S12 (1171-1226): 'the whole country could hear': a family leans in to the radio ----------
s='S12'; r=SH[s]
d12=char('S12_dad','dad34',s,(NX2+1.35,1.4,0),r,'wow',arms=('arm','arm')); k12=char('S12_kid','kid34',s,(NX2+1.95,1.0,0),r,'wow',arms=('arm','arm'),scale=0.8); g12=char('S12_gramps','gramps',s,(NX2+2.55,1.2,0),r,'shock',arms=('arm','arm'))
ALL+=[d12,k12,g12]
faces(d12,[(1171,'wow'),(1192,'cheer')]); faces(k12,[(1171,'wow'),(1200,'cheer')]); faces(g12,[(1171,'shock'),(1205,'cheer')]); arm(k12,1,1196,-150); arm(g12,-1,1200,-60); bob(d12,[1192]); bob(k12,[1200])
path(s,[(1171,(NX2+2.6,-1.4,1.3),(NX2+2.2,1.4,1.0)),(1226,(NX2+2.4,-0.85,1.22),(NX2+2.2,1.4,1.0))])
# ---------- S15 (1350-1409): empty chairs, the turkey waiting at home ----------
s='S15'; r=SH[s]
fg15=box('S15_fgchair',(NX2+0.95,-0.5,0.55),(0.12,0.12,1.1),flat('chair%d'%sum((110,70,44)),lin((110,70,44)),0.6),bv=0.01,coll=L.chr_coll(s))
path(s,[(1350,(NX2-0.5,-1.6,1.45),(NX2,0.6,0.95)),(1409,(NX2-0.2,-1.0,1.3),(NX2,0.6,0.95))])
# ---------- S09 (717-794): "the most radio-guy thing ever": idea face, crash push ----------
s='S09'; r=SH[s]
rm9=char('S09_rich','radioman',s,(DX+0.35,DY+0.75,0),r,'deadpan',arms=('arm','arm')); ALL.append(rm9)
faces(rm9,[(717,'deadpan'),(732,'idea'),(749,'grin'),(765,'wink'),(781,'grin')]); arm(rm9,1,732,-140); arm(rm9,1,748,-120); arm(rm9,-1,749,-60); arm(rm9,-1,765,-20); bob(rm9,[732,749,765],amt=9)
path(s,[(717,(DX+0.5,DY-1.9,1.45),(DX+0.35,DY+0.75,1.2)),(745,(DX+0.45,DY-1.6,1.44),(DX+0.35,DY+0.75,1.22)),(765,(DX+0.4,DY-0.85,1.4),(DX+0.35,DY+0.75,1.25)),(794,(DX+0.38,DY-0.75,1.4),(DX+0.35,DY+0.75,1.25))])
# ---------- S10 (795-931): he books the champs on the phone; a Bears player fills the doorway; he circles Thanksgiving on the calendar ----------
s='S10'; r=SH[s]
rm10=char('S10_rich','radioman',s,(DX-0.3,DY+0.8,0),r,'talkD',arms=([(795,'arm_phone')],[(795,'arm'),(880,'arm_marker')]),)
br10=char('S10_bear','bear',s,(OX-2.65,2.75,0),r,'smug',arms=('arm','arm')); ALL+=[rm10,br10]
lipsync(rm10,[w for w in WORDS if 26.3<=w[1]<=30.5],795,915); faces(rm10,[(843,'grin'),(856,'talkA')])
arm(rm10,-1,795,-150); arm(rm10,1,880,-25); arm(rm10,1,890,-100); arm(rm10,1,898,-112); arm(rm10,1,906,-100); arm(rm10,1,914,-112)
kloc(br10['root'],795,(OX-2.65,2.75,0))   # r2: always there, hidden behind the closed door until it slides open   # r2: stands behind the closed door, revealed as it slides
for fc in br10['root'].animation_data.action.fcurves:
    for kp in fc.keyframe_points: kp.interpolation='CONSTANT'
faces(br10,[(856,'smug'),(870,'grit'),(884,'smug')]); arm(br10,1,858,-80); arm(br10,-1,858,-80); bob(br10,[870])
path(s,[(795,(DX-0.3,DY-1.5,1.38),(DX-0.3,DY+0.8,1.2)),(843,(DX-0.8,DY-1.95,1.42),(DX-0.9,DY+1.2,1.25)),(866,(DX-1.3,DY-1.6,1.45),(OX-2.0,2.5,1.3)),
        (884,(CALX+0.15,1.0,1.55),(CALX,2.97,CALZ)),(898,(CALX+0.05,1.55,1.55),(CALX,2.97,CALZ)),(931,(CALX,1.7,1.55),(CALX,2.97,CALZ))])
# ---------- S11 (932-1180): ONE PACKED LONG TAKE: favors on two phones, the operator plugs in, the map lights up coast to coast ----------
s='S11'; r=SH[s]
rm11=char('S11_rich','radioman',s,(DX+0.2,DY+0.8,0),r,'talkD',arms=([(932,'arm_phone')],[(932,'arm'),(992,'arm_phone')]))
op=char('S11_op','operator',s,(MAPX+0.2,2.1,0),r,'happy',arms=('arm_plug','arm_plug')); ALL+=[rm11,op]
lipsync(rm11,[w for w in WORDS if 30.9<=w[1]<=33.7],932,1020)
faces(rm11,[(1020,'grin'),(1054,'idea'),(1084,'wink'),(1109,'grin'),(1150,'smug')])
for f,a in [(932,-150),(968,-140),(1000,-150)]: arm(rm11,-1,f,a)
for f,a in [(932,-20),(984,-60),(992,-150),(1040,-140)]: arm(rm11,1,f,a)
faces(op,[(932,'happy'),(990,'talkA'),(996,'talkB'),(1002,'talkA'),(1013,'wow'),(1054,'happy'),(1084,'wow'),(1109,'happy')])
for k,f in enumerate(range(1000,1150,12)): arm(op,(-1 if k%2 else 1),f,-138+6*(k%3)); arm(op,(-1 if k%2 else 1),f+6,-122)   # r2: plugs land on the panel above his shoulders
for i,l_ in enumerate(lamps_sw): vis(l_,[(1000+i*12,1180)])
MAPT=[(0,1012),(1013,1053),(1054,1083),(1084,1108),(1109,END)]
for m_,rg in zip(maps,MAPT): vis(m_,[rg])
path(s,[(932,(DX+0.3,DY-1.9,1.45),(DX+0.2,DY+0.8,1.2)),(990,(DX+0.9,DY-1.7,1.5),(DX+0.8,DY+0.9,1.25)),(1013,(MAPX-0.3,-0.4,1.6),(MAPX,2.6,1.45)),
        (1054,(MAPX+0.2,-0.6,1.7),(MAPX,2.97,1.6)),(1084,(MAPX+0.3,-1.2,1.8),(MAPX,2.97,1.7)),(1109,(MAPX+0.2,-2.0,1.75),(MAPX,2.97,1.7)),(1152,(MAPX-0.6,-2.6,1.7),(MAPX-0.5,2.6,1.5)),(1180,(MAPX-0.8,-2.7,1.65),(MAPX-0.6,2.6,1.45))])
# ---------- S17 (1537-1558): "Didn't matter." shrug and grin ----------
s='S17'; r=SH[s]
rm17=char('S17_rich','radioman',s,(DX+0.35,DY+0.75,0),r,'deadpan',arms=('arm','arm')); ALL.append(rm17)
faces(rm17,[(1537,'deadpan'),(1542,'grin')]); arm(rm17,1,1537,-15); arm(rm17,1,1542,-70); arm(rm17,-1,1537,-15); arm(rm17,-1,1542,-70); bob(rm17,[1542])
path(s,[(1537,(DX+0.25,DY-0.82,1.4),(DX+0.35,DY+0.75,1.26)),(1558,(DX+0.5,DY-0.9,1.41),(DX+0.35,DY+0.75,1.27))])   # sideways drift, no push (rule 306: S16 ends on a drop)
# ---------- S18 (1559-1729): calendar years flip: 1935, 1936 ... grey war years ... on to 2026 ----------
s='S18'; r=SH[s]
hand=char('S18_rich','radioman',s,(CALX+0.75,2.3,0),r,'grin',arms=('arm','arm')); ALL.append(hand)
faces(hand,[(1559,'grin'),(1639,'deadpan'),(1681,'grin'),(1702,'wink')])
FL=[1589,1600,1612,1621,1639,1645,1651,1657,1663,1670,1681,1702]   # 1935..1938, 1939-1944 grey (no game), 1945, then 2026 on 'stopped'
CR=[(0,897),(898,FL[0]-1)]+[(FL[i],(FL[i+1]-1 if i+1<len(FL) else END)) for i in range(len(FL))]
for c_,rg in zip(cals,CR): vis(c_,[rg])
for k,f in enumerate(FL): arm(hand,-1,f-4,-100); arm(hand,-1,f,-130); arm(hand,-1,f+3,-60)
path(s,[(1559,(CALX+0.55,0.3,1.45),(CALX+0.35,2.8,1.4)),(1621,(CALX+0.45,0.5,1.45),(CALX+0.3,2.8,1.42)),(1670,(CALX+0.35,0.7,1.45),(CALX+0.25,2.8,1.45)),(1702,(CALX+0.25,0.95,1.47),(CALX+0.2,2.8,1.47)),(1729,(CALX+0.22,1.0,1.47),(CALX+0.2,2.8,1.47))])
# ---------- S20 (1784-1863): today: 'became the one game' - the family jumps for the TV ----------
s='S20'; r=SH[s]
d20=char('S20_dad','dadM',s,(LX-1.6,1.45,0),r,'cheer',arms=('arm_drumstick','arm_remote')); m20=char('S20_mom','momM',s,(LX-0.55,1.78,0),r,'cheer',arms=('arm','arm'))
k20=char('S20_kid','kidM',s,(LX-2.45,0.95,0),r,'cheer',arms=('arm_ball','arm'),scale=0.8); g20=char('S20_gma','grandmaM',s,(LX+0.25,1.2,0),r,'cheer',arms=('arm','arm_plate'))
ALL+=[d20,m20,k20,g20]
for i,c_ in enumerate((d20,m20,k20,g20)): cheer(c_,1784+i*3,1863,120+i,up=((-152,-138) if i==0 else (-140,-120)),side=(1,-1,-1,1)[i]); bob(c_,[1793+i*4,1819+i*3,1844])
faces(d20,[(1784,'cheer'),(1810,'shout'),(1834,'cheer')]); faces(m20,[(1784,'cheer'),(1820,'wow'),(1844,'cheer')]); faces(k20,[(1784,'cheer'),(1815,'wow')]); faces(g20,[(1784,'happy'),(1810,'cheer')])
path(s,[(1784,(LX-1.0,-1.7,1.05),(LX-1.2,2.0,1.1)),(1819,(LX-1.4,-1.9,1.1),(LX-1.25,2.0,1.12)),(1863,(LX-1.75,-2.2,1.14),(LX-1.3,2.0,1.14))])
# ---------- S21 (1852-1920): payoff: push past the turkey onto the Detroit poster ('turkey' 1876); ending hold ----------
s='S21'; r=SH[s]
m21=char('S21_mom','momM',s,(PX-0.95,PY-0.75,0),r,'happy',arms=('arm_plate','arm')); k21=char('S21_kid','kidM',s,(PX+0.95,PY-0.7,0),r,'wow',arms=('arm','arm'),scale=0.8)
ALL+=[m21,k21]
faces(m21,[(1852,'happy'),(1876,'cheer')]); faces(k21,[(1852,'wow'),(1876,'cheer')]); arm(k21,1,1874,-140); arm(m21,-1,1870,-90); bob(k21,[1876]); bob(m21,[1878])
path(s,[(1852,(PX-0.3,-1.6,1.45),(PX,PY,1.4)),(1876,(PX-0.05,0.05,1.68),(PX,PY,PZ)),(1900,(PX-0.02,0.35,1.72),(PX,PY,PZ)),(END,(PX-0.01,0.42,1.73),(PX,PY,PZ))])
# ======================= finish =======================
for a in ALL: finish(a)
def world_and_sun():
    w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; bg=w.node_tree.nodes['Background']; bg.inputs['Color'].default_value=(*lin((170,190,215)),1); bg.inputs['Strength'].default_value=1.0
    bpy.ops.object.light_add(type='SUN',rotation=(math.radians(50),0,math.radians(35))); sun=bpy.context.object; sun.name='sun'; sun.data.energy=4.2; sun.data.color=(1.0,0.9,0.78); sun.data.angle=math.radians(3)
world_and_sun()
print('hulls',L.ink())
L.render_setup(100,8)
if os.environ.get('DET_WARP','1')=='1':   # retime to the take-3 VO (pace 3.42 w/s): every key through the word map
    import warp_det; warp_det.run(SH)
for m in bpy.data.materials: m.use_fake_user=True
bpy.ops.wm.save_as_mainfile(filepath='/root/det/blend/det.blend'); print('SCENE_OK all')
