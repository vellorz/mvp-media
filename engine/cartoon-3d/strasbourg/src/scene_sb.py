# Strasbourg 1570 short (sun-strasbourg): Blender builder.   blender -b --python scene_sb.py   -> /root/sb/blend/sb.blend
# Built on the d5lr4u det pipeline (lib.py rig, combos, approved walks, ink hulls) + Cape Cod helpers (sky dome, fx, snap).
# Every set, prop and scene here is new for this video. Frames = VO take E (trimmed, +0.1 s mix offset) at 30 fps.
import sys, os, math, random, json
sys.path.insert(0,'/root/sb/src')
import bpy, bmesh
from mathutils import Vector, Matrix
import lib as L
from lib import combo,box,cyl,sph,plane,flat,surf,card_mat,lin,vis,kloc,krot,kscale,empty,cam,char,face,faces,arm,bob,walk,finish,lipsync
END=2040
sc=L.init(END); R=random.Random(1570)
WORDS=json.load(open('/root/sb/vo/vo_final.words.json'))
def WF(i): return int(round((WORDS[i][1]+0.1)*30))
# shot table: overlaps are dissolves (post), touching ranges are hard cuts (853 decree, 1444 turn, 1769 match cut to today)
SH={'S01':(0,130),'S02':(123,255),'S03':(248,355),'S04':(348,421),'S05':(414,514),'S06':(507,565),'S07':(558,710),'S08':(703,800),
    'S09':(793,852),'S10':(853,943),'S11':(936,1003),'S12':(996,1148),'S13':(1141,1259),'S14':(1252,1312),'S15':(1305,1405),
    'S16':(1398,1443),'S17':(1444,1531),'S18':(1524,1654),'S19':(1647,1768),'S20':(1769,1825),'S21':(1818,1927),'S22':(1920,END)}
sc['shots']=json.dumps(SH)
LENS={'S01':30,'S02':28,'S03':32,'S04':34,'S05':24,'S06':28,'S07':34,'S08':30,'S09':34,'S10':30,'S11':34,'S12':30,'S13':28,'S14':30,
      'S15':32,'S16':30,'S17':30,'S18':32,'S19':34,'S20':26,'S21':30,'S22':32}
for n in SH: cam(n,LENS[n],11.0)   # sets stay sharp (BF r6 lesson)
def C(n): return L.chr_coll(n)
PATHS={}
def path(n,keys):
    PATHS.setdefault(n,[]).extend(keys); L.path(n,keys)
ALL=[]; COMBOS=[]
INK=flat('inkc',lin((50,28,42)),0.9)
SHARED={}
def shared(name,shots):
    """v3: shot-only dressing for several shots lives in its own top-level collection; every object gets hide_render keys over those
    shots' frame ranges (nested collections under CHR_ came back excluded after a per-shot exclude/include, so the tree vanished)"""
    c=bpy.data.collections.new(name); sc.collection.children.link(c); SHARED[name]=(c,shots); return c
def char_on(inst,kind,shot,loc,rng,face0=None,arms=('arm','arm'),walker=False,scale=None):
    if scale is None: scale=0.8 if kind.startswith('kid') else 1.0
    ch=char(inst,kind,shot,loc,rng,face0,arms=arms,walker=walker,scale=scale); ALL.append(ch)
    if scale!=1.0: ch['root'].scale=(scale,1.0,scale)   # v5 (rigcheck COPLANAR_CARD on every kid): keep full card depth gaps (1.25 mm) on scaled children
    if scale!=1.0:
        o_=bpy.data.objects.get(inst+'_shadow')
        if o_: o_.location.z/=scale   # v5b: keep the blob's own height (rule 367 SHADOW_OVERLAP 0.02 mm in S10)
    return ch
def drift_faces(ch,f0,f1,pool,seed,step=(20,38)):
    rr=random.Random(seed); f=f0; seq=[]
    while f<f1: seq.append((f,rr.choice(pool))); f+=rr.randint(*step)
    faces(ch,seq)
def onone(o):
    if o.animation_data and o.animation_data.action:
        for fc in o.animation_data.action.fcurves:
            if fc.data_path!='hide_render':
                for kp in fc.keyframe_points: kp.interpolation='CONSTANT'
def fall(o,f0,dur,p0,p1,rot0=None,rot1=None):
    for k in range(dur+1):
        t=(k/dur)**2; o.location=tuple(p0[i]+(p1[i]-p0[i])*t for i in range(3)); o.keyframe_insert('location',frame=f0+k)
        if rot0: o.rotation_euler=tuple(rot0[i]+(rot1[i]-rot0[i])*t for i in range(3)); o.keyframe_insert('rotation_euler',frame=f0+k)
    onone(o)
def fx(n,img,loc,f0,dur,size,coll,face='-Y',grow=1.6,rise=0.0):
    o=plane(n,loc,size,size,card_mat(img,img,emit=0.6),coll=coll,face=face); o['noink']=1
    for k in range(0,dur+1,2):
        s_=1+(grow-1)*k/dur; o.scale=(s_,s_,s_); o.keyframe_insert('scale',frame=f0+k)
        o.location=(loc[0],loc[1],loc[2]+rise*k/dur); o.keyframe_insert('location',frame=f0+k)
    vis(o,[(f0,f0+dur)]); onone(o); return o
# approved walks (round 11): the combo walks in place, the root slides at stride speed so feet do not skate
SPEED={'st':0.096/10,'nm':0.140/8,'br':0.186/6}
def walk_move(ch,f,name,side,face_,axis='x',dirv=None,**k):
    end=combo(ch,f,name,side=side,face=face_,**k); st=L.MO.COMBOS[name]['walk_style']
    ev=[e for e in L.MO.COMBOS[name]['events'] if e['ch']=='legs']; a,b=f+ev[0]['at'],f+ev[-1]['at']
    r=ch['root']; p0=tuple(r.location); d=SPEED[st]*(b-a)*r.scale[0]
    if dirv: v=Vector(dirv).normalized(); p1=(p0[0]+v.x*d,p0[1]+v.y*d,p0[2])
    elif axis=='x': p1=(p0[0]+side*d,p0[1],p0[2])
    else: p1=(p0[0],p0[1]-d,p0[2])
    kloc(r,a,p0); kloc(r,b,p1)
    for fc in r.animation_data.action.fcurves:
        if fc.data_path=='location':
            for kp in fc.keyframe_points:
                if kp.co[0] in (a,b): kp.interpolation='LINEAR'
    r.location=p1; return end
def skydome(n,c,rad,h,img,z0=-20,rep=4):
    bm=bmesh.new(); seg=72; lo=[];hi=[]
    for i in range(seg+1):
        a=2*math.pi*i/seg; lo.append(bm.verts.new((c[0]+rad*math.cos(a),c[1]+rad*math.sin(a),z0))); hi.append(bm.verts.new((c[0]+rad*math.cos(a),c[1]+rad*math.sin(a),z0+h)))
    for i in range(seg): bm.faces.new((lo[i],hi[i],hi[i+1],lo[i+1]))
    me=bpy.data.meshes.new(n); bm.to_mesh(me); bm.free(); uv=me.uv_layers.new()
    for p in me.polygons:
        for li in p.loop_indices:
            v=me.vertices[me.loops[li].vertex_index].co; a=math.atan2(v.y-c[1],v.x-c[0])%(2*math.pi); uv.data[li].uv=(a/(2*math.pi)*rep,(v.z-z0)/h)
    for p in me.polygons:
        us=[uv.data[li].uv[0] for li in p.loop_indices]
        if max(us)-min(us)>rep/2:
            for li in p.loop_indices:
                if uv.data[li].uv[0]<rep/2: uv.data[li].uv=(uv.data[li].uv[0]+rep,uv.data[li].uv[1])
    o=bpy.data.objects.new(n,me); L.C_NOI.objects.link(o); m=card_mat(img,img,emit=1.0); me.materials.append(m); o['fly']=1; o['noink']=1
    o.visible_shadow=False   # v4: the dome wall stood between the low winter sun and the square, so every day face read grey (skin probe 131/255)
    m.node_tree.nodes['Image Texture'].extension='REPEAT'
    cb=bmesh.new(); cv=[cb.verts.new((c[0]+rad*math.cos(2*math.pi*i/seg),c[1]+rad*math.sin(2*math.pi*i/seg),z0+h-0.5)) for i in range(seg)]; cb.faces.new(cv)
    cm=bpy.data.meshes.new(n+'_cap'); cb.to_mesh(cm); cb.free(); cu=cm.uv_layers.new()
    for li in range(len(cu.data)): cu.data[li].uv=(0.5,0.985)
    co_=bpy.data.objects.new(n+'_cap',cm); L.C_NOI.objects.link(co_); cm.materials.append(m); co_['fly']=1; co_['noink']=1
    for a_ in ('visible_diffuse','visible_glossy','visible_transmission','visible_volume_scatter','visible_shadow'): setattr(co_,a_,False)
    return o
def mesh(n,verts,faces_,m,coll=None,loc=(0,0,0)):
    me=bpy.data.meshes.new(n); me.from_pydata(verts,[],faces_); me.update()
    o=bpy.data.objects.new(n,me); (coll or L.C_SET).objects.link(o); me.materials.append(m); o.location=loc; return o
def gable(n,c,w,d,h,m,axis='x',coll=None,over=0.35):
    """pitched roof: ridge along `axis`; w along the ridge, d across, h ridge height above the eaves"""
    W,D=w/2+over,d/2+over
    if axis=='x': V=[(-W,-D,0),(W,-D,0),(W,D,0),(-W,D,0),(-W,0,h),(W,0,h)]
    else: V=[(-D,-W,0),(-D,W,0),(D,W,0),(D,-W,0),(0,-W,h),(0,W,h)]
    F=[(0,1,5,4),(2,3,4,5),(0,4,3),(1,2,5)] if axis=='x' else [(0,1,5,4),(2,3,4,5),(0,4,3),(1,2,5)]
    return mesh(n,V,F,m,coll,c)
ROOF=flat('roofm',lin((150,70,52)),0.85); ROOFS=flat('roofsnow',lin((240,242,248)),0.8)
BODYW=flat('housebody',lin((226,210,184)),0.9)
def house(n,c,face_,w,h,tex,roof,coll=None,dep=7.0):
    """half-timbered house: plain body, painted facade card, steep gable roof (Alsace)"""
    x,y=c[0],c[1]
    if face_ in('+X','-X'):
        sx=1 if face_=='+X' else -1
        box(n,(x-sx*dep/2,y,h/2),(dep,w,h),BODYW,coll=coll,bv=0.02)
        f=plane(n+'_f',(x+sx*0.015,y,h/2),w,h,card_mat(tex,tex,emit=0.12),coll=coll,face=face_); f['noink']=1
        gable(n+'_roof',(x-sx*dep/2,y,h),w,dep,w*0.75,roof,axis='y',coll=coll)
    else:
        sy=1 if face_=='+Y' else -1
        box(n,(x,y-sy*dep/2,h/2),(w,dep,h),BODYW,coll=coll,bv=0.02)
        f=plane(n+'_f',(x,y+sy*0.015,h/2),w,h,card_mat(tex,tex,emit=0.12),coll=coll,face=face_); f['noink']=1
        gable(n+'_roof',(x,y-sy*dep/2,h),w,dep,w*0.75,roof,axis='y' if False else 'x',coll=coll)
    return f
SAND_=surf('sandst','sandstone',(3,3)); SANDD=surf('sandstd','sandstone_dark',(3,3)); GREY=surf('greyst','greystone',(2,2))
WOOD=surf('stallw','stallwood',(1.2,1.2)); PANEL=surf('panelw','panel',(1.5,1.5)); FLOORW=surf('floorw','floorw',(1.6,1.6)); PEW=surf('peww','pew',(1,1))
def cathedral(n,c,tex,coll=None):
    """our own pink-sandstone Gothic west front: facade card on a stone block, ONE north spire (Strasbourg's single tower)"""
    x,y=c; W,H=30.0,45.0
    box(n+'_body',(x,y+20,H/2),(W,40,H),SAND_,coll=coll,bv=0.05)
    f=plane(n+'_front',(x,y-0.02,H/2),W,H,card_mat(tex,tex,emit=0.15),coll=coll); f['noink']=1
    box(n+'_tower',(x-8.0,y+5,H+8),(11,10,16),SAND_,coll=coll,bv=0.05)
    for i in range(3): box(f'{n}_twin{i}',(x-8.0-3.3+i*3.3,y-0.03,H+8),(1.3,0.1,9.0),flat('winblue',lin((60,80,150)),0.6,emit=0.2),coll=coll,bv=0)
    cyl(n+'_spire',(x-8.0,y+5,H+16+18),4.6,36,SAND_,v=8,r2=0.25,coll=coll)
    for k in range(4): cyl(f'{n}_pin{k}',(x-8.0+(-3.6 if k%2 else 3.6),y+5+(-3.6 if k<2 else 3.6),H+16+3.5),0.6,7,SAND_,v=6,r2=0.05,coll=coll)
    box(n+'_south',(x+8.0,y+5,H+2.0),(11,10,4),SAND_,coll=coll,bv=0.05)   # the south tower never got its spire
    return f
def stall(n,c,awn,goods,coll=None,rot=0.0,snow=False):
    """market stall: counter, four posts, striped awning, goods on the counter"""
    e=empty(n,c,coll=coll); e.rotation_euler=(0,0,rot); parts=[]
    parts.append(box(n+'_cnt',(0,0,0.5),(2.4,0.9,1.0),WOOD,coll=coll,bv=0.02))
    parts.append(box(n+'_top',(0,-0.02,1.02),(2.55,1.0,0.06),WOOD,coll=coll,bv=0.01))
    for sx in(-1,1):
        for sy in(-1,1): parts.append(cyl(f'{n}_p{sx}{sy}',(sx*1.18,sy*0.42,1.25),0.05,2.5,WOOD,v=8,coll=coll))
    aw=plane(n+'_awn',(0,-0.1,2.45),2.8,1.4,card_mat(awn,awn,emit=0.1),coll=coll,horiz=True); aw.rotation_euler=(math.radians(-18),0,0); aw['noink']=1; parts.append(aw)
    if snow:
        sn=box(n+'_snowcap',(0,0.0,2.62),(2.8,1.3,0.06),ROOFS,coll=coll,bv=0.02); sn.rotation_euler=(math.radians(-18),0,0); parts.append(sn)
        for k in range(7): parts.append(sph(f'{n}_garl{k}',(-1.2+k*0.4,-0.62,2.25-0.12*math.sin(math.pi*k/6)),0.09,flat('garl',lin((40,110,60)),0.8),coll=coll,seg=8))
    for i,g in enumerate(goods):
        gx=-0.95+i*(1.9/max(1,len(goods)-1))
        if g=='doll':
            parts.append(cyl(f'{n}_dollb{i}',(gx,-0.2,1.17),0.08,0.24,flat('dollred',lin((200,50,50)),0.7),v=10,coll=coll,r2=0.05))
            parts.append(sph(f'{n}_dollh{i}',(gx,-0.2,1.34),0.075,flat('dollface',lin((246,226,206)),0.7),coll=coll,seg=10))
        elif g=='ginger':
            gb=cyl(f'{n}_gb{i}',(gx,-0.25,1.2),0.12,0.03,flat('ginger',lin((170,100,50)),0.8),v=14,coll=coll,rot=(math.radians(75),0,0)); parts.append(gb)
            parts.append(cyl(f'{n}_gbi{i}',(gx,-0.27,1.2),0.085,0.031,flat('icing',lin((250,246,240)),0.6),v=14,coll=coll,rot=(math.radians(75),0,0)))
        elif g=='sweets':
            for k in range(3): parts.append(sph(f'{n}_sw{i}{k}',(gx-0.1+k*0.1,-0.25,1.1),0.05,flat('sweet%d'%k,lin([(230,80,90),(250,210,80),(120,190,240)][k]),0.5),coll=coll,seg=8))
        elif g=='candle':
            parts.append(cyl(f'{n}_cd{i}',(gx,-0.2,1.15),0.035,0.2,flat('wax',lin((240,230,200)),0.6),v=10,coll=coll))
            parts.append(sph(f'{n}_cf{i}',(gx,-0.2,1.28),0.025,flat('flame',lin((255,200,110)),0.3,emit=8.0),coll=coll,sc_=(1,1,1.8)))
        elif g=='mug':
            parts.append(cyl(f'{n}_mg{i}',(gx,-0.2,1.13),0.05,0.12,flat('mugred',lin((180,40,40)),0.6),v=12,coll=coll))
    for p in parts: p.parent=e
    return e
def fir_tree(n,c,h,coll=None,snow=False,decor=None):
    """fir: three stacked painted cones + trunk"""
    m=surf('firm'+('s' if snow else ''),'fir_snow' if snow else 'fir',(1,1))
    cyl(n+'_trunk',(c[0],c[1],c[2]+h*0.08),h*0.045,h*0.16,flat('bark',lin((100,66,40)),0.9),v=10,coll=coll)
    for k,(z,r_) in enumerate([(0.32,0.36),(0.56,0.28),(0.78,0.19)]):
        o_=cyl(f'{n}_c{k}',(c[0],c[1],c[2]+h*z),h*r_,h*0.34,m,v=14,r2=h*0.02,coll=coll); o_['noink']=1   # v2: the cone ink hull sat in the set collection and showed as a dark tree in S15
    return (c[0],c[1],c[2])
def snowfall(shot,center,rx,ry,zr,count,seed,f0,f1,size=0.06):
    """falling flakes on ones (assets on ones), drifting; per shot collection"""
    rr=random.Random(seed); co=C(shot); m=card_mat('snowflk','snow',emit=0.8)
    for i in range(count):
        x=center[0]+rr.uniform(-rx,rx); y=center[1]+rr.uniform(-ry,ry); z=rr.uniform(*zr); sp=rr.uniform(0.012,0.022); ph=rr.uniform(0,6.28)
        o=plane(f'{shot}_flk{i}',(x,y,z),size,size,m,coll=co); o['noink']=1; o.visible_shadow=False
        for f in range(f0,f1+1,2):
            zz=z-sp*(f-f0)
            while zz<0: zz+=zr[1]
            o.location=(x+0.08*math.sin(f/14+ph),y,zz); o.keyframe_insert('location',frame=f)
        onone(o)
# ======================= SET A: 1570 cathedral square (x=0 day; x=300 snow, Christmas fair) =======================
def square(X,snow):
    sfx='_snow' if snow else ''
    box(f'A{X}_ground',(X,0,-0.1),(80,90,0.2),surf('cob'+sfx,'cobble'+sfx,(2.2,2.2),emit=0.18),bv=0)
    skydome(f'A{X}_sky',(X,0),150,140,'sky_snow' if snow else 'sky_winter')
    cathedral(f'A{X}_cath',(X,30),'cathedral')
    for i in range(6):
        y=-24+i*8.2
        house(f'A{X}_hl{i}',(X-15,y),'+X',8.0,11.0+(i%3)*1.2,f'timber{i%4}{sfx}',ROOFS if snow else ROOF)
        house(f'A{X}_hr{i}',(X+15,y+3),'-X',8.0,11.5+((i+1)%3)*1.0,f'timber{(i+2)%4}{sfx}',ROOFS if snow else ROOF)
    for i in range(4): house(f'A{X}_hb{i}',(X-12+i*8,-30),'+Y',8.0,11.0+(i%2)*1.5,f'timber{(i+1)%4}{sfx}',ROOFS if snow else ROOF)
    S=[]
    for i,(x,y,aw,g) in enumerate([(-6.5,2,'awn_red',['doll','doll','ginger','doll']),(-6.5,7.5,'awn_green',['ginger','sweets','ginger']),
                                    (6.5,3,'awn_blue',['candle','doll','sweets','candle']),(6.5,8.5,'awn_red',['sweets','ginger','doll']),(-1.0,14,'awn_green',['doll','ginger','sweets','doll'])]):
        rot=math.radians(90 if x<0 else -90) if abs(x)>3 else 0.0
        S.append(stall(f'A{X}_st{i}',(X+x,y,0),aw,g,rot=rot,snow=snow))
    if snow:
        for i,(x,y,h) in enumerate([(-10,18,4.5),(10,18,4.0),(-10.5,-6,3.6),(11,-12,3.8)]): fir_tree(f'A{X}_fir{i}',(X+x,y,0),h,snow=True)
    return S
SQ_DAY=square(0,False); SQ_SNOW=square(300,True); SX=300
# the painted Saint Nicholas sign on its stand (day square only)
NB_P=(1.6,5.0)
nbst=empty('nick_stand',(NB_P[0],NB_P[1],0))
for sx in(-1,1): cyl(f'nick_leg{sx}',(sx*0.55,0.08,0.95),0.05,1.9,WOOD,v=8).parent=nbst
NB=empty('nick_pivot',(NB_P[0],NB_P[1]+0.08,0.0))
nb=plane('nickboard',(0,-0.03,1.25),1.2,1.6,card_mat('nickboard','nickboard',emit=0.12)); nb.parent=NB; nb['noink']=1
box('nickback',(0,0.0,1.25),(1.24,0.04,1.64),WOOD,bv=0.005).parent=NB
# ======================= SET B: cathedral nave (x=600) =======================
BX=600
box('B_floor',(BX,0,-0.1),(24,40,0.2),GREY,bv=0)
for sx in(-1,1): box(f'B_wall{sx}',(BX+sx*12,0,9),(0.4,40,18),SANDD,bv=0)
box('B_back',(BX,20,9),(24,0.4,18),SANDD,bv=0); box('B_front',(BX,-20,9),(24,0.4,18),SANDD,bv=0); box('B_roof',(BX,0,18.2),(24,40,0.4),SANDD,bv=0)
for sx in(-1,1):
    for i in range(6): cyl(f'B_pil{sx}{i}',(BX+sx*5.5,-14+i*6,8),0.7,16,SAND_,v=16)
    for i in range(6): plane(f'B_win{sx}{i}',(BX+sx*11.78,-14+i*6,8),1.6,5.5,flat('stain%d'%(i%3),lin([(80,110,200),(200,70,60),(230,190,80)][i%3]),0.5,emit=1.6),face='-X' if sx>0 else '+X')['noink']=1
for r_ in range(7):
    for sx in(-1,1): box(f'B_pew{r_}{sx}',(BX+sx*2.6,-8+r_*1.5,0.45),(3.6,0.5,0.9),PEW,bv=0.02)
# pulpit on the left pillar, raised (Strasbourg's stone pulpit stands on the nave's north side)
PU=(BX-3.6,1.0)   # v2: between the pillars (was inside the pillar at y 4)
# v5f (run lead: S07 'pulpit reads as a pink drum or cake', rules 374/376): a goblet-shaped Gothic pulpit in dark oak:
# column, flared cup, eight arched panels with gilt posts and rail, a red cloth with a gold cross facing the camera, railed stair
GOLD=flat('gold',lin((222,180,80)),0.4); RED=flat('banred',lin((200,40,44)),0.7); WHT=flat('banwht',lin((244,238,226)),0.7)
OAK=flat('pulpoak',lin((92,56,32)),0.6); OAKL=flat('pulpoakl',lin((150,100,58)),0.55)
cyl('B_pulpitcol',(PU[0],PU[1],0.7),0.26,1.4,SAND_,v=12)
cyl('B_pulpitcup',(PU[0],PU[1],1.48),0.30,0.28,OAK,v=8,r2=0.84)
cyl('B_pulpitfloor',(PU[0],PU[1],1.64),0.86,0.06,OAK,v=8)
cyl('B_pulpit',(PU[0],PU[1],1.95),0.84,0.62,OAK,v=8)
cyl('B_pulpitrail',(PU[0],PU[1],2.29),0.90,0.07,GOLD,v=8)
cyl('B_pulpitbase',(PU[0],PU[1],1.67),0.89,0.06,GOLD,v=8)
for k in range(8):
    a=math.radians(22.5+45*k); ca,sa=math.cos(a),math.sin(a)
    po=box(f'B_pupost{k}',(PU[0]+ca*0.86,PU[1]+sa*0.86,1.95),(0.06,0.06,0.62),GOLD,bv=0.005)
    a2=math.radians(45*k); pn=box(f'B_pupanel{k}',(PU[0]+math.cos(a2)*0.80,PU[1]+math.sin(a2)*0.80,1.93),(0.05,0.42,0.40),OAKL,bv=0.01); pn.rotation_euler=(0,0,a2)
    ar=cyl(f'B_puarch{k}',(PU[0]+math.cos(a2)*0.83,PU[1]+math.sin(a2)*0.83,2.10),0.12,0.02,GOLD,v=12,rot=(math.radians(90),0,a2+math.radians(90)))
th=math.atan2(-3.0,2.2); pfx,pfy=math.cos(th),math.sin(th); rz=th+math.radians(90)
cl=plane('B_pucloth',(PU[0]+pfx*0.90,PU[1]+pfy*0.90,1.86),0.46,0.66,flat('pucloth',lin((170,28,36)),0.8),face='-Y'); cl.rotation_euler=(0,0,rz); cl['noink']=1
for (w_,h_,dz) in ((0.06,0.40,0.0),(0.26,0.06,0.07)):
    cr=plane(f'B_pucross{w_}',(PU[0]+pfx*0.905,PU[1]+pfy*0.905,1.88+dz),w_,h_,GOLD,face='-Y'); cr.rotation_euler=(0,0,rz); cr['noink']=1
st_=box('B_stair',(PU[0]+1.2,PU[1]+0.9,0.8),(0.7,1.8,1.6),OAK,bv=0.02); st_.rotation_euler=(0,0,math.radians(30))
for k in range(5):
    s_=box(f'B_step{k}',(0,-0.75+k*0.36,-0.8+0.32*(k+1)),(0.74,0.08,0.06),OAKL,bv=0.005); s_.parent=st_
for k in range(4):
    rp=cyl(f'B_srp{k}',(0.37,-0.8+k*0.5,0.0+0.28*k),0.025,0.9,GOLD,v=6); rp.parent=st_
for i,c in enumerate([(BX-3,-6,4.0),(BX+3,-6,4.0),(BX,4,4.5),(PU[0]+1.2,PU[1]-1.5,3.4)]):
    bpy.ops.object.light_add(type='POINT',location=c); l=bpy.context.object; l.name=f'B_L{i}'; l.data.energy=260; l.data.color=(1.0,0.82,0.6); l.data.shadow_soft_size=0.6
bpy.ops.object.light_add(type='AREA',location=(BX,0,16)); al=bpy.context.object; al.name='B_fill'; al.data.energy=1800; al.data.size=14; al.data.color=(1.0,0.84,0.66)   # v4 (rule 335 probe): candlelit nave, warm fill (was cool, faces 0.94/0.90)
# ======================= SET C: council chamber (x=800) =======================
CX=800; PLC=surf('plc','plaster_council',(2.5,2.5))
box('C_floor',(CX,0,-0.05),(10,8,0.1),FLOORW,bv=0); box('C_ceil',(CX,0,3.6),(10,8,0.1),PANEL,bv=0)
for sx in(-1,1): box(f'C_wallx{sx}',(CX+sx*5,0,1.8),(0.1,8,3.6),PLC,bv=0)
box('C_wallb',(CX,4,1.8),(10,0.1,3.6),PLC,bv=0)
for sx in(-1,1): box(f'C_wain{sx}',(CX+sx*4.92,0,0.6),(0.06,8,1.2),PANEL,bv=0.01)
box('C_wainb',(CX,3.92,0.6),(10,0.06,1.2),PANEL,bv=0.01)
for i in range(5): box(f'C_beam{i}',(CX-4+i*2,0,3.45),(0.25,8,0.25),flat('beam',lin((90,60,40)),0.8),bv=0.02)
for i in range(3): plane(f'C_win{i}',(CX-3+i*3,3.93,2.0),1.1,1.6,flat('cwin',lin((200,214,232)),0.4,emit=1.4),face='-Y')['noink']=1
box('C_table',(CX,1.4,0.62),(4.6,1.0,0.08),surf('cloth','fir',(0.6,0.6)) if False else flat('cloth',lin((40,90,60)),0.9),bv=0.02)
box('C_tablebody',(CX,1.4,0.31),(4.4,0.8,0.58),flat('cloth',lin((40,90,60)),0.9),bv=0.02)
for i in range(3): box(f'C_chair{i}',(CX-1.5+i*1.5,2.6,0.9),(0.7,0.12,1.8),PANEL,bv=0.02)
plane('C_crest',(CX,3.93,2.6),1.0,1.2,flat('crest',lin((200,40,40)),0.6),face='-Y')['noink']=1
box('C_crestbar',(CX,3.92,2.6),(0.22,0.02,1.0),flat('crestw',lin((246,240,230)),0.6),bv=0)
for i,c in enumerate([(CX-2,0,3.0),(CX+2,0,3.0)]):
    bpy.ops.object.light_add(type='POINT',location=c); l=bpy.context.object; l.name=f'C_L{i}'; l.data.energy=180; l.data.color=(1.0,0.86,0.66)
bpy.ops.object.light_add(type='AREA',location=(CX,-2,3.4)); al=bpy.context.object; al.name='C_fill'; al.data.energy=380; al.data.size=6; al.data.color=(1.0,0.82,0.62)   # v4 (rule 335 probe): fill was white, faces read 0.97/0.95
# ======================= SET D: a family room (x=1000): 1570 Christmas Eve (S14, S15), 1605 tree (S18), chronicle desk (S19) =======================
DX=1000; PLR=surf('plr','plaster_room',(2.0,2.0))
box('D_floor',(DX,0,-0.05),(8,7,0.1),FLOORW,bv=0); box('D_ceil',(DX,0,3.0),(8,7,0.1),PANEL,bv=0)
for sx in(-1,1): box(f'D_wallx{sx}',(DX+sx*4,0,1.5),(0.1,7,3.0),PLR,bv=0)
box('D_wallb',(DX,3.5,1.5),(8,0.1,3.0),PLR,bv=0)
for i in range(4): box(f'D_beam{i}',(DX-3+i*2,0,2.88),(0.22,7,0.22),flat('beam',lin((90,60,40)),0.8),bv=0.02)
WINN=plane('D_window',(DX+1.6,3.43,1.6),1.2,1.4,card_mat('dwin','sky_night',emit=1.2),face='-Y'); WINN['noink']=1
box('D_winframe',(DX+1.6,3.44,1.6),(1.36,0.04,1.56),flat('wframe',lin((90,60,40)),0.8),bv=0.01)
for k in range(2): box(f'D_wbar{k}',(DX+1.6,3.41,1.6),(0.05 if k==0 else 1.2,0.03,1.4 if k==0 else 0.05),flat('wframe',lin((90,60,40)),0.8),bv=0)
STAR=sph('D_star',(DX+1.9,3.3,2.05),0.05,flat('starglow',lin((255,240,180)),0.3,emit=12.0)); STAR['noink']=1
box('D_hearth',(DX-3.6,1.5,0.8),(0.7,1.8,1.6),GREY,bv=0.03); box('D_hearthin',(DX-3.25,1.5,0.5),(0.05,1.2,0.8),flat('ember',lin((255,140,60)),0.5,emit=3.0),bv=0)
box('D_table',(DX-0.6,1.6,0.74),(2.0,1.0,0.06),WOOD,bv=0.02)
for sx in(-1,1):
    for sy in(-1,1): box(f'D_tl{sx}{sy}',(DX-0.6+sx*0.9,1.6+sy*0.42,0.36),(0.08,0.08,0.72),WOOD,bv=0)
box('D_bench',(DX-0.6,0.8,0.42),(1.8,0.35,0.06),WOOD,bv=0.01)
cyl('D_candle',(DX-0.1,1.55,0.87),0.035,0.2,flat('wax',lin((240,230,200)),0.6),v=10); sph('D_flame',(DX-0.1,1.55,1.0),0.03,flat('flame',lin((255,200,110)),0.3,emit=8.0),sc_=(1,1,1.8))
bpy.ops.object.light_add(type='POINT',location=(DX-0.1,1.4,1.2)); l=bpy.context.object; l.name='D_candleL'; l.data.energy=40; l.data.color=(1.0,0.75,0.45)
bpy.ops.object.light_add(type='POINT',location=(DX-3.0,1.5,1.0)); l=bpy.context.object; l.name='D_fireL'; l.data.energy=160; l.data.color=(1.0,0.6,0.3)
bpy.ops.object.light_add(type='AREA',location=(DX,-1,2.85)); al=bpy.context.object; al.name='D_fill'; al.data.energy=260; al.data.size=5; al.data.color=(1.0,0.82,0.62)   # v4: warmer (kids 0.945/0.912)
# Christmas Eve gifts (S14, S15): wrapped boxes on the table, one per child
GIFTS=shared('D_gifts',['S14','S15'])
GC=[(200,50,50),(60,120,180),(60,140,80)]
GIFT=[]
for i,(x,y) in enumerate([(-1.2,1.55),(-0.65,1.7),(-0.1,1.45)]):
    g=box(f'D_gift{i}',(DX+x,y,0.89),(0.26,0.22,0.24),flat(f'giftc{i}',lin(GC[i]),0.6),coll=GIFTS,bv=0.01)
    box(f'D_ribbon{i}',(DX+x,y,0.89),(0.27,0.04,0.25),flat('ribbon',lin((250,220,110)),0.4),coll=GIFTS,bv=0).parent=None
    GIFT.append(g)
# 1605 tree (S18): fir in a tub by the window; decorations appear where a hand places them
TREEC=shared('D_tree',['S18'])
TP=(DX+1.2,2.2,0.0)
cyl('D_tub',(TP[0],TP[1],0.22),0.36,0.44,WOOD,v=16,coll=TREEC)
fir_tree('D_fir',(TP[0],TP[1],0.4),2.3,coll=TREEC)
# chronicle desk (S19): the open chronicle with the tree entry; quill rests in the pot (nobody writes)
CHRC=shared('D_chron',['S19'])
box('D_desk',(DX-2.6,-1.6,0.76),(1.4,0.9,0.06),WOOD,coll=CHRC,bv=0.02); box('D_deskbody',(DX-2.6,-1.35,0.38),(1.3,0.4,0.72),WOOD,coll=CHRC,bv=0.02)
cb_=plane('D_chronicle',(DX-2.6,-1.62,0.795),0.84,0.575,card_mat('chronicle','chronicle',emit=0.18),coll=CHRC,horiz=True); cb_['noink']=1
cyl('D_inkpot',(DX-2.05,-1.35,0.83),0.045,0.08,INK,v=12,coll=CHRC)
cyl('D_quill',(DX-2.0,-1.32,0.95),0.008,0.32,flat('quill',lin((246,244,236)),0.7),v=6,coll=CHRC,rot=(0,math.radians(-20),0))
cyl('D_candle2',(DX-3.15,-1.35,0.88),0.035,0.2,flat('wax',lin((240,230,200)),0.6),v=10,coll=CHRC); sph('D_flame2',(DX-3.15,-1.35,1.01),0.03,flat('flame',lin((255,200,110)),0.3,emit=8.0),coll=CHRC,sc_=(1,1,1.8))
# ======================= SET E: today's Christmas market at night (x=1300) =======================
EX=1300
box('E_ground',(EX,0,-0.1),(80,90,0.2),surf('cobsn','cobble_snow',(2.2,2.2)),bv=0)
skydome('E_sky',(EX,0),150,140,'sky_night')
cathedral('E_cath',(EX,34),'cathedral_night')
for i in range(6):
    y=-24+i*8.2
    house(f'E_hl{i}',(EX-15,y),'+X',8.0,11.0+(i%3)*1.2,f'timber{i%4}_night',ROOFS)
    house(f'E_hr{i}',(EX+15,y+3),'-X',8.0,11.5+((i+1)%3)*1.0,f'timber{(i+2)%4}_night',ROOFS)
for i in range(4): house(f'E_hb{i}',(EX-12+i*8,-30),'+Y',8.0,11.0+(i%2)*1.5,f'timber{(i+1)%4}_night',ROOFS)
CHAL=surf('chaletw','chalet',(1.2,1.2))
BULB=flat('bulbm',lin((255,214,130)),0.4,emit=6.0)
def chalet(n,c,rot=0.0,poster=False):
    e=empty(n,c); e.rotation_euler=(0,0,rot); parts=[]
    parts.append(box(n+'_back',(0,0.9,1.3),(3.0,0.12,2.6),CHAL,bv=0.02))
    for sx in(-1,1): parts.append(box(f'{n}_side{sx}',(sx*1.44,0.3,1.3),(0.12,1.3,2.6),CHAL,bv=0.02))
    parts.append(box(n+'_cnt',(0,-0.3,0.55),(2.8,0.5,1.1),CHAL,bv=0.02))
    parts.append(gable(n+'_roof',(0,0.3,2.6),3.0,1.5,0.9,ROOFS,axis='x'))
    parts.append(box(n+'_fascia',(0,-0.42,2.55),(3.2,0.06,0.24),flat('fascia',lin((150,40,40)),0.6),bv=0.01))
    for k in range(11): parts.append(sph(f'{n}_b{k}',(-1.5+k*0.3,-0.48,2.42-0.08*math.sin(math.pi*k/10)),0.03,BULB,seg=8))
    for k in range(5): parts.append(cyl(f'{n}_mug{k}',(-1.0+k*0.5,-0.32,1.17),0.05,0.12,flat('mugred',lin((180,40,40)),0.6),v=12))
    for p in parts: p.parent=e
    return e
for i,(x,y,r_) in enumerate([(-7,0,90),(-7,6,90),(-7,12,90),(7,-1,-90),(7,5,-90),(7,11,-90),(-3,-8,0),(3,-8,0)]):
    chalet(f'E_ch{i}',(EX+x,y,0),math.radians(r_))
for i in range(30):   # light strings across the square
    for k in range(14): sph(f'E_ls{i}_{k}',(EX-14+k*2.15,-20+i*1.5,6.2-0.6*math.sin(math.pi*k/13)),0.06,BULB,seg=6)['noink']=1
BT=(EX,18,0)   # the big tree in front of the cathedral
fir_tree('E_bigtree',BT,16,snow=True)
rr=random.Random(5)
for i in range(90):
    z=rr.uniform(2.0,14.5); rad=16*(0.40-0.30*(z-2)/12.5)*rr.uniform(0.85,1.0); a=rr.uniform(0,6.28)
    sph(f'E_tb{i}',(BT[0]+math.cos(a)*rad,BT[1]+math.sin(a)*rad-0.3,z),0.12,BULB,seg=6)['noink']=1
sph('E_treestar',(BT[0],BT[1],16.4),0.5,flat('starglow',lin((255,240,180)),0.3,emit=12.0))['noink']=1
for i,c in enumerate([(EX-6,0,5),(EX+6,6,5),(EX,-6,5),(EX,12,6)]):
    bpy.ops.object.light_add(type='POINT',location=c); l=bpy.context.object; l.name=f'E_L{i}'; l.data.energy=900; l.data.color=(1.0,0.87,0.72)   # v5h: graded S20 faces read B/R 0.80 even with the grade's B at 1.22 (rule 355); softer bulb-warm key; l.data.shadow_soft_size=1.0
# payoff chalet with the poster: framed, whole, lit (rule: poster ending sits inside the payoff scene)
PCH=(EX+0.2,-12.5,0)
chalet('E_pch',PCH,0.0)
PW,PH=0.80,1.20; PZ=1.70; PY=PCH[1]+0.82
box('poster_frame',(PCH[0],PY+0.03,PZ),(PW+0.12,0.04,PH+0.12),flat('pframe',lin((246,236,214)),0.35,emit=0.9),bv=0.01)
pmat=bpy.data.materials.new('poster'); N_,L_=L.nodes(pmat); pp_=N_['Principled BSDF']; it_=N_.new('ShaderNodeTexImage'); it_.image=bpy.data.images.load(L.TX+'poster.png'); it_.interpolation='Cubic'
L_.new(it_.outputs['Color'],pp_.inputs['Base Color']); L_.new(it_.outputs['Color'],pp_.inputs['Emission Color']); pp_.inputs['Emission Strength'].default_value=0.35; pp_.inputs['Roughness'].default_value=1.0; pp_.inputs['Specular IOR Level'].default_value=0.0
poster=plane('poster',(PCH[0],PY,PZ),PW,PH,pmat,coll=L.C_NOI); poster['noink']=1
bpy.ops.object.light_add(type='AREA',location=(PCH[0],PCH[1]-0.6,2.4)); gl=bpy.context.object; gl.name='E_posterL'; gl.data.energy=60; gl.data.size=1.2; gl.data.color=(1.0,0.9,0.75); gl.rotation_euler=(math.radians(35),0,0)

# ======================= v5 SET DRESSING (set sheet vs Rick 10#0406/10#0757/14#0695: our sets read bare) =======================
RED=flat('banred',lin((200,40,44)),0.7); WHT=flat('banwht',lin((244,238,226)),0.7); GOLD=flat('gold',lin((222,180,80)),0.4)
BARREL=flat('barrelw',lin((140,92,56)),0.8); HOOP=flat('hoop',lin((70,60,60)),0.6,metal=0.3)
LAMPG=flat('lampglow',lin((255,214,130)),0.4,emit=5.0)
def banner(n,c,face_,w=0.9,h=2.4,col=None,coll=None):
    """Strasbourg red-and-white banner on a pole bracket (city colours)"""
    b=plane(n,c,w,h,col or RED,coll=coll,face=face_); b['noink']=1
    st=plane(n+'_s',(c[0],c[1],c[2]),w*0.34,h,WHT,coll=coll,face=face_); st['noink']=1
    off={'-Y':(0,-0.006,0),'+Y':(0,0.006,0),'+X':(0.006,0,0),'-X':(-0.006,0,0)}[face_]; st.location=(c[0]+off[0],c[1]+off[1],c[2])
    ax=(1,0,0) if face_ in('-Y','+Y') else (0,1,0)
    cyl(n+'_pole',(c[0]+off[0]*2,c[1]+off[1]*2,c[2]+h/2+0.04),0.03,w+0.3,GOLD,v=8,coll=coll,rot=(0,math.radians(90),0) if ax==(1,0,0) else (math.radians(90),0,0))
def barrel(n,c,coll=None,r=0.32,h=0.8):
    cyl(n,(c[0],c[1],c[2]+h/2),r,h,BARREL,v=16,coll=coll); cyl(n+'_h1',(c[0],c[1],c[2]+h*0.2),r+0.01,0.05,HOOP,v=16,coll=coll); cyl(n+'_h2',(c[0],c[1],c[2]+h*0.8),r+0.01,0.05,HOOP,v=16,coll=coll)
def crate(n,c,coll=None,s_=0.55):
    box(n,(c[0],c[1],c[2]+s_/2),(s_,s_,s_),WOOD,coll=coll,bv=0.02)
def lantern_post(n,c,coll=None,h=2.6,lit=True):
    cyl(n+'_post',(c[0],c[1],h/2),0.06,h,flat('iron',lin((50,44,48)),0.6),v=8,coll=coll)
    box(n+'_box',(c[0],c[1],h+0.18),(0.26,0.26,0.36),LAMPG if lit else flat('lampoff',lin((200,180,120)),0.6),coll=coll,bv=0.02)
    cyl(n+'_cap',(c[0],c[1],h+0.42),0.2,0.14,flat('iron',lin((50,44,48)),0.6),v=8,coll=coll,r2=0.03)
for X,snow in ((0,False),(300,True)):
    for i in range(6):
        y=-24+i*8.2
        banner(f'A{X}_banL{i}',(X-14.95,y+2.0,7.2),'+X'); banner(f'A{X}_banR{i}',(X+14.95,y+1.0,7.4),'-X')
    for i,(x,y) in enumerate([(-8.6,0.5),(-8.4,5.2),(8.6,1.2),(8.5,6.8),(-3.0,15.6),(1.8,15.8),(-9.0,10.5),(9.2,11.0)]):
        barrel(f'A{X}_bar{i}',(X+x,y,0)); crate(f'A{X}_cr{i}',(X+x+0.5,y+0.6,0)); crate(f'A{X}_crt{i}',(X+x+0.5,y+0.6,0.55),s_=0.45)
    for i,(x,y) in enumerate([(-4.0,-3.0),(4.0,-2.5),(-4.2,11.0),(4.4,11.5)]): lantern_post(f'A{X}_lp{i}',(X+x,y,0),lit=snow)
    for k in range(18):   # pennant line across the square
        for j,(y0,z0) in enumerate([(-1.0,5.2),(9.5,5.6)]):
            x=X-13.5+k*1.6; z=z0-0.7*math.sin(math.pi*k/17)
            pn=mesh(f'A{X}_pen{j}_{k}',[(-0.22,0,0),(0.22,0,0),(0,0,-0.5)],[(0,1,2)],[RED,WHT,flat('penyel',lin((240,200,70)),0.6),flat('pengrn',lin((60,140,80)),0.6)][k%4],loc=(x,y0,z)); pn['noink']=1
# nave: aisle carpet, candle stands, hanging banners, stained glass brighter
plane('B_carpet',(BX,-4,0.005),2.2,30,flat('carpet',lin((150,30,40)),0.9),horiz=True)['noink']=1
for i,y in enumerate([-12,-6,0,6,12]):
    for sx in(-1,1):
        cyl(f'B_cs{i}{sx}',(BX+sx*4.2,y,0.7),0.05,1.4,GOLD,v=8); cyl(f'B_cand{i}{sx}',(BX+sx*4.2,y,1.5),0.04,0.2,flat('wax',lin((240,230,200)),0.6),v=8)
        sph(f'B_fl{i}{sx}',(BX+sx*4.2,y,1.64),0.035,flat('flame',lin((255,200,110)),0.3,emit=8.0),sc_=(1,1,1.8))
for i in range(4): banner(f'B_ban{i}',(BX-11.75 if i%2 else BX+11.75,-9+i*6,11.0),'+X' if i%2 else '-X',w=1.4,h=4.0)
# council: book shelf, candlestick and papers on the table, city banner pair
box('C_shelf',(CX+4.6,0.5,1.2),(0.4,2.4,2.4),PANEL,bv=0.02)
for r_ in range(4):
    for k in range(9): box(f'C_bk{r_}{k}',(CX+4.42,-0.5+k*0.22,0.3+r_*0.55+0.18),(0.06,0.18,0.36),flat(f'bk{(r_+k)%4}',lin([(140,40,40),(40,80,130),(60,110,60),(160,120,50)][(r_+k)%4]),0.7),bv=0.005)
cyl('C_csk',(CX+1.4,1.25,0.82),0.05,0.32,GOLD,v=8); sph('C_cfl',(CX+1.4,1.25,1.02),0.035,flat('flame',lin((255,200,110)),0.3,emit=8.0),sc_=(1,1,1.8))
for k in range(3): plane(f'C_paper{k}',(CX-1.0+k*0.6,1.3,0.665),0.3,0.4,flat('paper',lin((240,232,206)),0.8),horiz=True)['noink']=1
for sx in(-1,1): banner(f'C_ban{sx}',(CX+sx*2.0,3.93,2.0),'-Y',w=0.7,h=1.8)
# family room: striped rug (Rick 10#0406), plate shelf, hanging pots, picture
plane('D_rug',(DX,0.6,0.004),2.6,1.8,card_mat('awn_red','awn_red',emit=0.05),horiz=True)['noink']=1
box('D_pshelf',(DX-1.6,3.38,2.0),(1.6,0.2,0.05),WOOD,bv=0.01)
for k in range(5): cyl(f'D_plate{k}',(DX-2.25+k*0.32,3.36,2.17),0.12,0.02,flat('plate',lin((230,226,214)),0.4),v=16,rot=(math.radians(80),0,0))
for k in range(3): cyl(f'D_pot{k}',(DX-3.2+k*0.35,1.0,2.55),0.1,0.14,flat('copper',lin((190,110,60)),0.4,metal=0.4),v=12)
box('D_pic',(DX-0.6,3.43,1.9),(0.6,0.03,0.45),flat('picframe',lin((120,80,40)),0.6),bv=0.005); plane('D_picin',(DX-0.6,3.41,1.9),0.5,0.36,card_mat('dpic','sky_winter',emit=0.2),face='-Y')['noink']=1
# today's market: more visitors in the background (Rick crowds), chalet garlands
# v5f (run lead: sets plainer than Rick's): nave chandeliers, council arms + fringe + inkwell, snow-square well + sledge, lit underside on the market tree
for i,(x,y,z) in enumerate([(BX+0.8,-3.5,4.4),(BX-0.6,2.8,4.9)]):
    cyl(f'B_chring{i}',(x,y,z),0.55,0.05,flat('iron',lin((40,36,34)),0.5,metal=0.5),v=16)
    cyl(f'B_chrod{i}',(x,y,z+1.6),0.015,3.2,flat('iron',lin((40,36,34)),0.5,metal=0.5),v=6)
    for k in range(8):
        a=k*math.pi/4; cyl(f'B_chc{i}{k}',(x+math.cos(a)*0.55,y+math.sin(a)*0.55,z+0.12),0.03,0.18,flat('wax',lin((240,230,200)),0.6),v=6)
        sph(f'B_chf{i}{k}',(x+math.cos(a)*0.55,y+math.sin(a)*0.55,z+0.25),0.03,flat('flame',lin((255,200,110)),0.3,emit=8.0),sc_=(1,1,1.8))
sh_=box('C_arms',(CX,3.90,2.45),(0.9,0.05,1.1),WHT,bv=0.02)
rb=box('C_armsbend',(CX,3.86,2.45),(0.22,0.03,1.3),RED,bv=0.0); rb.rotation_euler=(0,math.radians(-38),0)
box('C_armsframe',(CX,3.93,2.45),(1.0,0.04,1.2),GOLD,bv=0.02)
box('C_fringe',(CX,0.89,0.55),(4.62,0.03,0.07),GOLD,bv=0.005)
cyl('C_ink',(CX-1.6,1.2,0.69),0.05,0.09,flat('inkpot',lin((30,30,40)),0.4),v=12); cyl('C_quill',(CX-1.58,1.2,0.82),0.008,0.3,WHT,v=6,rot=(0,math.radians(15),0))
box('C_seal',(CX+0.4,1.15,0.68),(0.12,0.12,0.06),RED,bv=0.01)
WX,WY=SX+2.2,7.2
cyl('A_well',(WX,WY,0.45),0.7,0.9,GREY,v=16); cyl('A_wellrim',(WX,WY,0.92),0.74,0.08,SAND_,v=16); cyl('A_wellsnow',(WX,WY,0.98),0.72,0.05,flat('snowcap',lin((240,244,250)),0.8),v=16)
for sx in(-1,1): box(f'A_wellpost{sx}',(WX+sx*0.62,WY,1.5),(0.1,0.1,1.2),WOOD,bv=0.01)
box('A_wellroof',(WX,WY,2.18),(1.6,1.0,0.12),WOOD,bv=0.01); box('A_wellroofsnow',(WX,WY,2.27),(1.6,1.0,0.08),flat('snowcap',lin((240,244,250)),0.8),bv=0.02)
cyl('A_wellbeam',(WX,WY,1.85),0.05,1.3,WOOD,v=8,rot=(0,math.radians(90),0)); cyl('A_wellbucket',(WX+0.1,WY,1.35),0.12,0.2,BARREL,v=10)
SLX,SLY=SX-2.4,6.4
for sx in(-1,1): box(f'A_sledrun{sx}',(SLX,SLY+sx*0.3,0.05),(1.4,0.05,0.08),flat('sledred',lin((170,40,40)),0.6),bv=0.01)
box('A_sledbed',(SLX,SLY,0.22),(1.2,0.66,0.1),WOOD,bv=0.01)
for k,(dx,col) in enumerate([(-0.35,(150,40,40)),(0.05,(40,110,70)),(0.4,(200,160,60))]): box(f'A_sledgift{k}',(SLX+dx,SLY,0.42),(0.32,0.4,0.3),flat(f'sgift{k}',lin(col),0.6),bv=0.01)
for k,(zb,rad) in enumerate([(2.4,5.76),(6.24,4.48),(9.76,3.04)]):
    bpy.ops.object.light_add(type='POINT',location=(BT[0],BT[1]-rad*0.75,zb-0.6)); l=bpy.context.object; l.name=f'E_treefill{k}'; l.data.energy=[1600,1100,700][k]; l.data.color=(1.0,0.82,0.58); l.data.shadow_soft_size=1.5
    for m_ in range(28):
        a=math.pi*(1.05+0.9*m_/27); sph(f'E_rim{k}_{m_}',(BT[0]+math.cos(a)*rad*0.97,BT[1]+math.sin(a)*rad*0.97,zb+0.05),0.09,BULB,seg=6)['noink']=1
# ======================= CAST + CAMERAS =======================
def S(n): return SH[n]
A0=0.0   # day square x
# ---- S01 (0-130): hook. The preacher glares at the saint's painted sign at the 1570 fair, points, scolds ----
s='S01'; r=S(s)
pr=char_on('S01_pre','preacher',s,(NB_P[0]-0.85,NB_P[1]-1.9,0),r,'angry',arms=('arm','arm_book'))
faces(pr,[(0,'angry'),(40,'angry_squint'),(96,'rage')])
COMBOS+=[(pr,30,'point_out_tilt',1,'angry'),(pr,92,'akimbo_scold',1,'rage')]
k1=char_on('S01_kidC','kidC',s,(NB_P[0]+0.8,NB_P[1]-1.5,0),r,'happy',arms=('arm','arm_apple')); drift_faces(k1,0,130,['happy','smile','content'],1)
COMBOS.append((k1,60,'startle_recoil',-1,'shock'))
path(s,[(0,(NB_P[0]-0.1,NB_P[1]-6.4,1.35),(NB_P[0]-0.1,NB_P[1]-1.0,1.25)),(130,(NB_P[0]-0.4,NB_P[1]-5.4,1.3),(NB_P[0]-0.3,NB_P[1]-1.0,1.25))])   # v5b: st9 had both characters out of frame
# ---- S02 (123-255): the 1570 St Nicholas fair: kids with toys, a seller hands over a doll ----
s='S02'; r=S(s)
sA=char_on('S02_sell','sellerA',s,(-5.4,2.0,0),r,'happy',arms=('arm','arm_doll')); drift_faces(sA,123,255,['happy','grin','open_smile'],2)
COMBOS.append((sA,170,'lean_reach',1,'grin'))
kA=char_on('S02_kidA','kidA',s,(-4.2,0.6,0),r,'excited',arms=('arm','arm_gift')); faces(kA,[(123,'excited'),(190,'happy'),(230,'grin')])
COMBOS.append((kA,200,'victory_up',-1,'happy'))
kB=char_on('S02_kidB','kidB',s,(-2.0,-1.2,0),r,'happy',arms=('arm','arm_gingerbread')); drift_faces(kB,123,255,['happy','smile','grin'],3)
walk_move(kB,128,'walk_stroll',-1,'happy')
for i,(x,y,k) in enumerate([(1.5,6.0,'father'),(3.6,4.0,'mother'),(-1.0,9.5,'sellerB'),(4.8,9.0,'kidC')]):
    c_=char_on(f'S02_x{i}',k,s,(x,y,0),r,'neutral'); drift_faces(c_,123,255,['happy','content','smile','neutral'],10+i)
path(s,[(123,(-2.0,-4.6,1.8),(-3.6,2.0,1.2)),(255,(-2.9,-3.8,1.55),(-4.2,1.6,1.05))])
# ---- S03 (248-355): the preacher tells the kids the saint has to go ----
s='S03'; r=S(s)
p3=char_on('S03_pre','preacher',s,(-1.2,3.2,0),r,'stern',arms=('arm','arm_book')); faces(p3,[(248,'stern'),(300,'determined')])
COMBOS+=[(p3,262,'dip_talk',1,'stern'),(p3,312,'akimbo_scold',1,'determined')]
k3=[char_on('S03_kA','kidA',s,(0.6,2.2,0),r,'happy',arms=('arm','arm_doll')),char_on('S03_kB','kidB',s,(1.5,3.0,0),r,'happy',arms=('arm','arm_gift'))]
faces(k3[0],[(248,'happy'),(300,'surprise'),(330,'stunned')]); faces(k3[1],[(248,'smile'),(304,'shock'),(334,'stunned')])
path(s,[(248,(1.6,-1.6,1.25),(-0.4,3.0,1.15)),(355,(1.1,-0.9,1.2),(-0.2,3.0,1.1))])
# ---- S04 (348-421): the doubter: kidA's quoted line, lips move; double take on "You?" ----
s='S04'; r=S(s)
k4=char_on('S04_kA','kidA',s,(0.6,2.2,0),r,'stunned',arms=('arm','arm_doll'))
lipsync(k4,[w for w in WORDS if 11.6<=w[1]<=13.8],355,421)
COMBOS.append((k4,396,'point_out_tilt',-1,'skeptical'))
k4b=char_on('S04_kB','kidB',s,(1.5,3.0,0),r,'stunned',arms=('arm','arm_gift')); faces(k4b,[(348,'stunned'),(380,'skeptical')])
p4=char_on('S04_pre','preacher',s,(-1.2,3.2,0),r,'stern',arms=('arm','arm_book')); COMBOS.append((p4,404,'double_take',1,'shock'))
path(s,[(348,(1.9,-0.4,1.05),(0.9,2.6,1.0)),(421,(1.6,-0.2,1.05),(0.6,2.6,1.0))])
# ---- S05 (414-514): "no small voice": the great church; people stream in; camera rises up the front ----
s='S05'; r=S(s)
for i,(x,k,st) in enumerate([(-3.0,'father','walk'),(-1.4,'mother','walk_stroll'),(1.0,'sellerB','walk'),(2.6,'councilC','walk_brisk'),(-0.2,'kidC','walk')]):
    c_=char_on(f'S05_w{i}',k,s,(x,22.0-i*0.9,0),r,'neutral'); drift_faces(c_,414,514,['neutral','content','happy'],20+i)
    walk_move(c_,418+i*6,st,1 if i%2 else -1,'neutral',axis='y',dirv=(0.05*(1 if i%2 else -1),1,0))
path(s,[(414,(2.6,8.0,1.6),(1.0,22,3.5)),(470,(2.4,10.5,3.5),(0.6,26,14.0)),(514,(2.2,11.5,6.0),(-3,28,30.0))])   # v5f: run lead, stall awning + pole crossed the bottom; camera rises right of the stall row
# ---- S06 (507-565): inside, the packed nave from behind; the preacher in the pulpit ----
s='S06'; r=S(s)
p6=char_on('S06_pre','preacher',s,(PU[0],PU[1],1.65),r,'determined',arms=('arm','arm_book')); COMBOS.append((p6,520,'tilt_talk',1,'determined'))
for i in range(10):
    x=BX+(-1)**i*(1.6+0.8*(i%3)); y=-4.6+(i//2)*0.9
    c_=char_on(f'S06_c{i}',['father','mother','sellerA','sellerB','councilC','kidC'][i%6],s,(x,y,0),r,'back',scale=None); faces(c_,[(507,'back')])
path(s,[(507,(BX+0.6,-7.6,2.2),(PU[0]+0.6,PU[1],2.4)),(565,(BX+0.1,-6.6,2.4),(PU[0]+0.3,PU[1],2.5))])
# ---- S07 (558-710): pulpit close: "gifts come from the Christ Child, not a saint" ----
s='S07'; r=S(s)
p7=char_on('S07_pre','preacher',s,(PU[0],PU[1],1.65),r,'determined',arms=('arm','arm_book'))
faces(p7,[(558,'determined'),(600,'shout'),(640,'proud'),(690,'smug')])
COMBOS+=[(p7,566,'eureka_point_up',-1,'determined'),(p7,618,'point_out_tilt',1,'shout'),(p7,668,'tilt_talk',-1,'proud')]
path(s,[(558,(PU[0]+2.2,PU[1]-3.0,3.05),(PU[0],PU[1],2.55)),(710,(PU[0]+1.7,PU[1]-2.4,2.95),(PU[0],PU[1],2.55))])
# ---- S08 (703-800): the council hears him and does not laugh ----
s='S08'; r=S(s)
cA=char_on('S08_cA','councilA',s,(CX-1.5,2.25,0),r,'stern',arms=('arm','arm_scroll')); cB=char_on('S08_cB','councilB',s,(CX,2.3,0),r,'skeptical',arms=('arm','arm_scroll')); cC=char_on('S08_cC','councilC',s,(CX+1.5,2.25,0),r,'stern',arms=('arm','arm_scroll'))
faces(cA,[(703,'stern'),(760,'frown')]); faces(cB,[(703,'skeptical'),(770,'stern')]); faces(cC,[(703,'stern'),(750,'deadpan')])
COMBOS+=[(cB,716,'cross_arms_huff',-1,'stern'),(cC,744,'think_chin',1,'skeptical'),(cA,770,'glance_shift',1,'stern')]
path(s,[(703,(CX+0.4,-2.4,1.75),(CX,2.1,1.25)),(800,(CX+0.1,-1.9,1.7),(CX,2.1,1.25))])
# ---- S09 (793-852): "fine, the saint is out": councilA raises the decree ----
s='S09'; r=S(s)
c9=char_on('S09_cA','councilA',s,(CX-1.5,2.25,0),r,'stern',arms=('arm','arm_scroll')); faces(c9,[(793,'stern'),(830,'smug')])
COMBOS.append((c9,808,'victory_up',1,'determined'))
lipsync(c9,[w for w in WORDS if 25.0<=w[1]<=27.4],810,852)
o9=char_on('S09_cB','councilB',s,(CX,2.3,0),r,'stern',arms=('arm','arm_scroll')); faces(o9,[(793,'stern'),(830,'content')])
path(s,[(793,(CX-0.6,-1.4,1.35),(CX-1.2,2.2,1.4)),(852,(CX-0.8,-1.1,1.4),(CX-1.3,2.2,1.45))])
# ---- S10 (853-943): two days before the feast: the clerk tips the saint's sign off its stand; sellers and kids watch ----
s='S10'; r=S(s)
cl=char_on('S10_clerk','councilC',s,(NB_P[0]-0.9,NB_P[1]-0.25,0),r,'stern'); faces(cl,[(853,'stern'),(900,'deadpan')])
COMBOS.append((cl,868,'lean_reach',1,'stern'))   # mitten meets the sign's edge at the reach peak (~880), then the sign tips back
krot(NB,853,(0,0,0)); krot(NB,884,(0,0,0)); fall(NB,885,13,(NB_P[0],NB_P[1]+0.08,0.0),(NB_P[0],NB_P[1]+0.08,0.0),(0,0,0),(math.radians(-86),0,0))
fx('S10_dust','fx_dust' if os.path.exists(L.TX+'fx_dust.png') else 'fx_smoke',(NB_P[0],NB_P[1]+1.0,0.3),897,16,1.2,C(s),grow=1.8,rise=0.3)
w1=char_on('S10_sell','sellerA',s,(NB_P[0]+1.6,NB_P[1]-1.4,0),r,'neutral',arms=('arm','arm_doll')); faces(w1,[(853,'neutral'),(898,'shock'),(920,'sad')])
w2=char_on('S10_kid','kidB',s,(NB_P[0]+2.6,NB_P[1]-0.9,0),r,'neutral',arms=('arm','arm_gingerbread')); faces(w2,[(853,'neutral'),(899,'shock')])
COMBOS.append((w2,898,'startle_recoil',-1,'shock'))
path(s,[(853,(NB_P[0]+0.4,NB_P[1]-6.4,1.4),(NB_P[0]+0.4,NB_P[1],1.2)),(943,(NB_P[0]+0.2,NB_P[1]-5.6,1.35),(NB_P[0]+0.3,NB_P[1],1.15))])
# ---- S11 (936-1003): "No saint. No saint's day. Done.": kids crushed, the preacher smug ----
s='S11'; r=S(s)
k11=char_on('S11_kA','kidA',s,(-0.4,2.0,0),r,'sad',arms=('arm','arm_doll')); faces(k11,[(936,'sad'),(970,'sad_tears')])
COMBOS.append((k11,944,'panic_clutch',1,'shock'))
k11b=char_on('S11_kC','kidC',s,(0.6,2.4,0),r,'shock'); faces(k11b,[(936,'shock'),(965,'sad')])
p11=char_on('S11_pre','preacher',s,(-1.8,3.0,0),r,'smug',arms=('arm','arm_book')); faces(p11,[(936,'smug'),(975,'smug_grin')])
COMBOS.append((p11,970,'cross_arms_huff',1,'smug'))
path(s,[(936,(-0.4,-2.4,1.2),(-0.6,2.5,1.0)),(1003,(-0.5,-2.0,1.2),(-0.6,2.5,1.0))])
# ---- S12 (996-1148): the sellers still had dolls and sweets; kids still wanted toys ----
s='S12'; r=S(s)
s12=char_on('S12_sell','sellerB',s,(5.4,8.5,0),r,'sigh',arms=('arm','arm_candle')); faces(s12,[(996,'sigh'),(1040,'worried'),(1090,'hopeful' if False else 'smile')])
s12b=char_on('S12_sellA','sellerA',s,(5.4,3.0,0),r,'worried',arms=('arm','arm_doll')); COMBOS.append((s12b,1020,'tilt_talk',-1,'worried'))
k12=char_on('S12_kA','kidA',s,(4.1,5.4,0),r,'happy'); faces(k12,[(996,'happy'),(1080,'open_smile')]); COMBOS.append((k12,1074,'lean_reach',1,'happy'))
k12b=char_on('S12_kB','kidB',s,(3.4,6.6,0),r,'content'); COMBOS.append((k12b,1100,'clap',1,'happy'))
path(s,[(996,(2.2,2.4,1.4),(4.8,5.7,1.15)),(1148,(2.6,3.0,1.35),(4.8,5.5,1.1))])
# ---- S13 (1141-1259): the fair moves to just before Christmas: snow, firs, families walking ----
s='S13'; r=S(s)
for i,(x,y,k,st,sd) in enumerate([(SX-2.2,0.4,'father','walk',1),(SX-2.8,1.3,'mother','walk_stroll',1),(SX+2.0,1.8,'kidA','walk',-1),(SX+2.6,2.6,'kidB','walk_stroll',-1),(SX-1.4,4.4,'sellerA','walk_brisk',1)]):
    c_=char_on(f'S13_w{i}',k,s,(x,y,0),r,'happy'); drift_faces(c_,1141,1259,['happy','smile','content','excited'],30+i)
    walk_move(c_,1146+i*7,st,sd,'happy')
snowfall(s,(SX,0.0),5.0,3.0,(0.2,4.5),160,13,1141,1259)
path(s,[(1141,(SX,-5.4,2.0),(SX,3.0,1.4)),(1259,(SX+0.4,-4.6,1.8),(SX,3.0,1.2))])
# ---- S14 (1252-1312): Christmas Eve: the mother sets the gifts down ----
s='S14'; r=S(s)
m14=char_on('S14_mom','mother',s,(DX-0.9,2.35,0),r,'happy',arms=('arm','arm_gift')); faces(m14,[(1252,'happy'),(1290,'smile')])
COMBOS.append((m14,1262,'lean_reach',1,'happy'))
path(s,[(1252,(DX-0.2,-1.4,1.55),(DX-0.7,1.8,1.1)),(1312,(DX-0.4,-1.0,1.45),(DX-0.7,1.8,1.05))])
# ---- S15 (1305-1405): the gifts come from the Christ Child now: kids and their gifts by the starlit window ----
s='S15'; r=S(s)
for i,(x,y,k,fc_) in enumerate([(DX-1.4,0.9,'kidA','excited'),(DX-0.4,0.8,'kidB','happy'),(DX+0.5,1.0,'kidC','excited')]):
    c_=char_on(f'S15_k{i}',k,s,(x,y,0),r,fc_,arms=('arm','arm_gift')); drift_faces(c_,1305,1405,['excited','happy','grin','open_smile'],40+i)
    COMBOS.append((c_,1320+i*14,['victory_up','clap','laugh_bob'][i],1 if i%2 else -1,'excited'))
f15=char_on('S15_dad','father',s,(DX+1.8,2.2,0),r,'content'); faces(f15,[(1305,'content'),(1360,'smile')])
path(s,[(1305,(DX-0.3,-3.0,1.4),(DX-0.1,1.6,1.15)),(1405,(DX+0.3,-2.5,1.4),(DX+0.6,2.2,1.4))])
# ---- S16 (1398-1443): "The preacher had won." victory in the snowy square ----
s='S16'; r=S(s)
p16=char_on('S16_pre','preacher',s,(SX+0.2,4.0,0),r,'smug_grin',arms=('arm','arm_book')); faces(p16,[(1398,'smug_grin'),(1425,'cool_shades')])
COMBOS.append((p16,1404,'victory_up',1,'smug_grin'))
snowfall(s,(SX,1.0),3.0,2.0,(0.2,3.5),90,16,1398,1443)
path(s,[(1398,(SX+0.6,0.6,1.1),(SX+0.2,4.0,1.35)),(1443,(SX+0.5,1.0,1.05),(SX+0.2,4.0,1.4))])
# ---- S17 (1444-1531): the turn: a father carries a fir into his house; a neighbour does a double take ----
s='S17'; r=S(s)
fa=char_on('S17_dad','father',s,(SX-4.6,-2.0,0),r,'proud',arms=('arm','arm')); faces(fa,[(1444,'proud'),(1490,'grin')])
walk_move(fa,1450,'walk',1,'proud')
tree17=empty('S17_tree',(0.0,-0.02,0.0),parent=fa['root'],coll=C(s)); tree17.rotation_euler=(0,math.radians(48),0); tree17.location=(0.24,0.03,0.62)   # v3: behind the body card, top out past his right shoulder (v2 crossed his face)
for k,(z,r_) in enumerate([(0.15,0.30),(0.40,0.24),(0.62,0.16)]):
    o_=cyl(f'S17_fir{k}',(0,0,z),r_,0.5,surf('firms','fir_snow',(1,1)),v=12,r2=0.02,coll=C(s)); o_.parent=tree17
o_=cyl('S17_firtrunk',(0,0,-0.15),0.035,0.4,flat('bark',lin((100,66,40)),0.9),v=8,coll=C(s)); o_.parent=tree17
arm(fa,1,1444,-62); arm(fa,-1,1444,-30)   # right mitten under the trunk, left steadies the boughs
nb17=char_on('S17_nb','sellerB',s,(SX-1.9,0.4,0),r,'content'); faces(nb17,[(1444,'content'),(1480,'stunned')])
COMBOS.append((nb17,1470,'double_take',-1,'surprise'))
snowfall(s,(SX-1.5,-1.0),4.5,2.5,(0.2,3.8),120,17,1444,1531)
path(s,[(1444,(SX-4.2,-6.0,1.45),(SX-4.3,-1.6,1.2)),(1531,(SX-2.6,-5.6,1.4),(SX-2.6,-1.2,1.2))])
# ---- S18 (1524-1654): 1605: the fir indoors; paper roses, apples, sugar placed by hand on "roses", "apples", "sugar" ----
s='S18'; r=S(s)
mo=char_on('S18_mom','mother',s,(TP[0]-0.75,TP[1]-0.45,0),r,'happy',arms=('arm','arm_rose')); faces(mo,[(1524,'happy'),(1620,'content')])
COMBOS.append((mo,1590,'lean_reach',1,'happy'))
kc=char_on('S18_kC','kidC',s,(TP[0]+0.75,TP[1]-0.5,0),r,'excited',arms=('arm_apple','arm')); drift_faces(kc,1524,1654,['excited','happy','grin'],50)
COMBOS.append((kc,1612,'lean_reach',-1,'excited'))
kb=char_on('S18_kB','kidB',s,(TP[0]+0.2,TP[1]-0.95,0),r,'happy',arms=('arm','arm_gingerbread')); drift_faces(kb,1524,1654,['happy','smile','open_smile'],51)
COMBOS.append((kb,1632,'lean_reach',1,'happy'))
DEC=C(s)
def ornament(n,kind,p,f0):
    if kind=='rose': o=sph(n,p,0.055,flat('paperrose',lin((236,120,150)),0.8),coll=DEC,seg=10)
    elif kind=='apple': o=sph(n,p,0.06,flat('applered',lin((200,40,40)),0.5),coll=DEC,seg=12)
    else: o=box(n,p,(0.07,0.03,0.09),flat('sugarw',lin((250,248,240)),0.4),coll=DEC,bv=0.01)
    vis(o,[(f0,END)]); return o
TIERS=[(0.4+2.3*z-2.3*0.17,0.4+2.3*z+2.3*0.17,2.3*r_) for z,r_ in [(0.32,0.36),(0.56,0.28),(0.78,0.19)]]
def cone_R(z): return max([R0*(1-(z-a)/(b-a))+0.046*(z-a)/(b-a) for a,b,R0 in TIERS if a<=z<=b] or [0.05])
for i,(kind,dx,z,f0) in enumerate([('rose',-0.35,1.05,1605),('rose',-0.2,1.65,1525),('apple',0.40,0.95,1627),('apple',0.2,1.95,1525),('sugar',0.05,0.9,1645),('sugar',-0.1,2.2,1525)]):
    Rz=cone_R(z); dy=math.sqrt(max(0.0,Rz*Rz-dx*dx))
    ornament(f'S18_orn{i}',kind,(TP[0]+dx,TP[1]-dy-0.03,z),f0)   # v2: on the cone surface facing the camera (v1 floated off the boughs)
path(s,[(1524,(TP[0]-0.2,TP[1]-4.4,1.45),(TP[0],TP[1],1.3)),(1654,(TP[0]-0.4,TP[1]-3.4,1.4),(TP[0],TP[1],1.25))])
# ---- S19 (1647-1768): one of the first written records: the chronicle, pushed in until the tree sketch fills the frame ----
s='S19'; r=S(s)
rd=char_on('S19_cC','councilC',s,(DX-2.6,-0.6,0),r,'look_down'); faces(rd,[(1647,'look_down'),(1700,'impressed' if False else 'surprise'),(1730,'proud')])
COMBOS.append((rd,1688,'think_chin',-1,'look_down'))
path(s,[(1647,(DX-2.5,-3.9,1.75),(DX-2.6,-0.6,1.2)),(1700,(DX-2.55,-3.3,1.75),(DX-2.6,-1.0,1.05)),(1768,(DX-2.45,-2.25,1.45),(DX-2.42,-1.62,0.80))])   # v5b: st8/st9 cut the reader's head at 1700
# ---- S20 (1769-1825): match cut to today: the same square at night, the market still here ----
s='S20'; r=S(s)
for i,(x,y,k,st,sd) in enumerate([(EX-3.0,-2.0,'tourA','walk_stroll',1),(EX+2.6,0.0,'tourB','walk',-1),(EX-1.0,4.0,'kidM','walk',1),(EX+1.5,6.0,'mother','walk_stroll',-1)]):
    c_=char_on(f'S20_w{i}',k,s,(x,y,0),r,'happy',arms=('arm','arm_mug') if k.startswith('tour') else ('arm','arm')); drift_faces(c_,1769,1825,['happy','smile','excited'],60+i)
    walk_move(c_,1772+i*5,st,sd,'happy')
snowfall(s,(EX,0.0),5.0,4.0,(0.2,5.0),140,20,1769,1825)
path(s,[(1769,(EX,-9.5,2.4),(EX,8.0,3.0)),(1825,(EX+0.6,-8.0,2.0),(EX,8.0,3.6))])
# ---- S21 (1818-1927): France's oldest Christmas market: mugs, phones, the big tree ----
s='S21'; r=S(s)
tA=char_on('S21_tA','tourA',s,(EX-0.9,8.0,0),r,'happy',arms=('arm_mug','arm_smartphone')); tB=char_on('S21_tB','tourB',s,(EX+0.8,8.3,0),r,'excited',arms=('arm_mug','arm'))
drift_faces(tA,1818,1927,['happy','grin','laugh'],70); drift_faces(tB,1818,1927,['excited','happy','open_smile'],71)
COMBOS+=[(tB,1840,'wave_hello',1,'excited'),(tA,1880,'laugh_bob',-1,'laugh')]
kM=char_on('S21_kid','kidM',s,(EX+0.1,7.2,0),r,'excited',arms=('arm','arm_gift')); COMBOS.append((kM,1862,'clap',1,'excited'))
snowfall(s,(EX,6.0),3.5,3.0,(0.2,4.5),110,21,1818,1927)
path(s,[(1818,(EX+0.2,4.4,1.3),(EX,9.0,1.25)),(1872,(EX+0.1,4.2,1.3),(EX,9.5,1.6)),(1927,(EX-0.2,3.6,1.3),(EX,12.0,4.2))])   # v5b: people first, tilt up to the tree on 'the big tree'
# ---- S22 (1920-2040): payoff at the market chalet: the poster, whole, lands on "Nicholas" ----
s='S22'; r=S(s)
ve=char_on('S22_vend','chalet',s,(PCH[0]+0.95,PCH[1]+0.25,0),r,'happy',arms=('arm','arm_mug')); faces(ve,[(1920,'happy'),(1960,'grin')])
COMBOS.append((ve,1932,'tilt_talk',-1,'happy'))
vi=char_on('S22_tA','tourA',s,(PCH[0]-1.2,PCH[1]-1.3,0),r,'happy',arms=('arm','arm_smartphone')); COMBOS.append((vi,1946,'point_out_tilt',1,'excited'))
snowfall(s,(PCH[0],PCH[1]-2.0),2.5,1.5,(0.2,3.2),70,22,1920,END)
path(s,[(1920,(PCH[0]+0.3,PCH[1]-6.0,1.75),(PCH[0],PY,1.55)),(1990,(PCH[0]+0.04,PCH[1]-2.35,1.7),(PCH[0],PY,PZ-0.16)),(END,(PCH[0]+0.03,PCH[1]-2.2,1.7),(PCH[0],PY,PZ-0.16))])
# v5: dolly cameras toward their targets (set sheet: heads ~10 % of frame width vs Rick's 25-35 %)
def dolly(n,k,frames=None):
    for key in PATHS[n]:
        f,l,t=key[:3]
        if frames and not(frames[0]<=f<=frames[1]): continue
        kloc(L.CAM[n],f,tuple(t[i]+(l[i]-t[i])*k for i in range(3)))
for n,k in [('S02',0.62),('S03',0.7),('S08',0.75),('S10',0.7),('S11',0.75),('S13',0.62),('S15',0.75),('S16',0.85),('S17',0.7),('S18',0.8)]: dolly(n,k)
# background crowd in the wide shots (Rick fills the square)
def crowd(shot,spots,kinds,seed,pool=('happy','content','smile','neutral','excited')):
    rr=random.Random(seed)
    for i,(x,y) in enumerate(spots):
        k=kinds[i%len(kinds)]; c_=char_on(f'{shot}_bg{i}',k,shot,(x,y,0),SH[shot],rr.choice(pool)); drift_faces(c_,SH[shot][0],SH[shot][1],list(pool),seed*10+i)
crowd('S02',[(-6.8,6.0),(-3.4,8.4),(0.4,7.6),(2.6,10.4),(-8.0,9.6)],['councilC','sellerB','father','mother','kidC'],2)
crowd('S13',[(SX-3.4,7.0),(SX+3.0,8.5),(SX-0.4,10.0),(SX+1.6,6.4)],['councilB','sellerB','father','kidC'],13)
crowd('S20',[(EX-3.0,6.0),(EX+3.4,7.0),(EX-1.2,9.4),(EX+1.0,10.6),(EX+4.2,3.2)],['tourB','tourA','kidM','mother','father'],20)
crowd('S21',[(EX-2.6,11.0),(EX+2.4,11.6),(EX-1.4,13.2),(EX+3.0,9.6)],['father','mother','tourB','kidM'],21)
# ======================= world, finish, ink, render settings =======================
def world_and_sun():
    w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; bg=w.node_tree.nodes['Background']; bg.inputs['Color'].default_value=(*lin((170,190,220)),1); bg.inputs['Strength'].default_value=0.9
    bpy.ops.object.light_add(type='SUN',rotation=(math.radians(55),0,math.radians(35))); sun=bpy.context.object; sun.name='sun'; sun.data.energy=3.6; sun.data.color=(1.0,0.94,0.86); sun.data.angle=math.radians(3)
for _n,(_c,_shots) in SHARED.items():
    for _o in list(_c.all_objects):
        if not (_o.animation_data and _o.animation_data.action and any(fc.data_path=='hide_render' for fc in _o.animation_data.action.fcurves)): vis(_o,[SH[x] for x in _shots])
world_and_sun()
# light plan: clear winter day (1570 day square), overcast snow (S13, S16, S17), night (today, S20-S22); interiors are closed boxes
SUN=bpy.data.objects['sun']; WBG=sc.world.node_tree.nodes['Background']
for f,e,ws in [(0,5.0,1.3),(1140,5.0,1.3),(1141,3.4,1.1),(1531,3.4,1.1),(1532,5.0,1.3),(1768,5.0,1.3),(1769,0.12,0.18)]:
    SUN.data.energy=e; SUN.data.keyframe_insert('energy',frame=f); WBG.inputs['Strength'].default_value=ws; WBG.inputs['Strength'].keyframe_insert('default_value',frame=f)
for ad in (SUN.data.animation_data,sc.world.node_tree.animation_data):
    for fc in ad.action.fcurves:
        for kp in fc.keyframe_points: kp.interpolation='CONSTANT'
for c_,f_,k_,sd_,fc_ in COMBOS: combo(c_,f_,k_,side=sd_,face=fc_)
print('COMBOS',len(COMBOS),len(set(k for _,_,k,_,_ in COMBOS)))
sc['air']=json.dumps(sorted(L.AIR))
for a in ALL: finish(a)
print('hulls',L.ink())
for o_ in bpy.data.objects:
    if o_.type=='LIGHT' and o_.data.type!='SUN': o_.visible_camera=False
L.render_setup(100,8)
sc.cycles.samples=4; sc.cycles.transparent_max_bounces=8; sc.cycles.diffuse_bounces=1; sc.cycles.max_bounces=3
os.makedirs('/root/sb/blend',exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath='/root/sb/blend/sb.blend'); print('SCENE_OK all')
