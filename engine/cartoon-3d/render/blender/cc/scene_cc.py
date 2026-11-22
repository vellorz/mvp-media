# Cape Cod Pilgrims short (tue-cape-cod): Blender builder.   blender -b --python scene_cc.py   -> /root/cc/blend/cc.blend
# Built on the Black Friday pipeline (lib.py rig, ink hulls, cast cards, render setup); every set, prop and scene here is new for this video.
import sys, os, math, random, json
sys.path.insert(0,'/root/cc/src')
import bpy, bmesh
from mathutils import Vector, Euler, Matrix
import lib as L
from lib import box,cyl,sph,plane,flat,surf,card_mat,lin,vis,kloc,krot,kscale,empty,cam,char,face,faces,arm,bob,walk,finish,lipsync
END=1816
sc=L.init(END); R=random.Random(7)
WORDS=json.load(open('/root/cc/vo/vo_trim.wav.words.json'))
# shot table: overlaps are dissolves (smoothstep in post), touching ranges are hard cuts (4: 766, 1141, 1413, 1759)
SH={'S01':(0,123),'S02':(116,214),'S03':(207,278),'S04':(271,392),'S05':(385,510),'S06':(502,583),'S07':(576,662),'S08':(654,765),
    'S09':(766,1012),'S10':(1005,1140),'S11':(1141,1252),'S12':(1244,1330),'S13':(1322,1412),'S14':(1413,1443),'S15':(1436,1516),
    'S16':(1509,1574),'S17':(1567,1712),'S18':(1702,1758),'S19':(1759,END)}
sc['shots']=json.dumps(SH)
LENS={'S01':30,'S02':32,'S03':40,'S04':30,'S05':34,'S06':32,'S07':30,'S08':34,'S09':30,'S10':32,'S11':30,'S12':30,'S13':30,'S14':36,'S15':38,'S16':30,'S17':32,'S18':32,'S19':34}
for n in SH: cam(n,LENS[n],11.0)   # sets stay sharp like Rick's newest videos (BF r6 lesson: DOF blur, not missing paint, killed surface detail)
def C(n): return L.chr_coll(n)
PATHS={}
def path(n,keys):
    PATHS.setdefault(n,[]).extend(keys); L.path(n,keys)
def dolly(n,k,frames=None):
    """pull every camera key of shot n toward its own target by factor k (keeps angles and pitch; rule 309 head size)"""
    for key in PATHS[n]:
        f,l,t=key[:3]
        if frames and not(frames[0]<=f<=frames[1]): continue
        kloc(L.CAM[n],f,tuple(t[i]+(l[i]-t[i])*k for i in range(3)))
ALL=[]
def gwalk(ch,f0,f1,p0,p1,hf,step=4):
    """walk whose feet follow the terrain (check_scene r1: linear z between end heights sank feet into the dunes)"""
    walk(ch,f0,f1,p0,p1,step=step); r=ch['root']
    for f in range(f0,f1+1,2):
        t=(f-f0)/(f1-f0); x=p0[0]+(p1[0]-p0[0])*t; y=p0[1]+(p1[1]-p0[1])*t
        r.location=(x,y,hf(x,y)); r.keyframe_insert('location',frame=f)
    for fc in r.animation_data.action.fcurves:
        if fc.data_path=='location':
            for kp in fc.keyframe_points:
                if f0<=kp.co[0]<=f1: kp.interpolation='LINEAR'
def rb(x,y): return 0.25*noise2(x,y,1.0)-max(0,(y-6))*0.06
def shared(name,shots):
    """one collection of shot-only dressing linked under several shots' CHR_ collections"""
    c=bpy.data.collections.new(name)
    for s_ in shots: C(s_).children.link(c)
    return c
# ---------------- generic helpers ----------------
INK=flat('inkc',lin((50,28,42)),0.9)
def grid(n,cx,cy,w,d,res,hf,m,coll=None,z0=0.0):
    bm=bmesh.new(); nx,ny=res
    vs=[[bm.verts.new((cx-w/2+w*i/(nx-1),cy-d/2+d*j/(ny-1),z0+hf(cx-w/2+w*i/(nx-1),cy-d/2+d*j/(ny-1)))) for i in range(nx)] for j in range(ny)]
    for j in range(ny-1):
        for i in range(nx-1): bm.faces.new((vs[j][i],vs[j][i+1],vs[j+1][i+1],vs[j+1][i]))
    me=bpy.data.meshes.new(n); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth=True
    o=bpy.data.objects.new(n,me); (coll or L.C_SET).objects.link(o); me.materials.append(m); o['noink']=1; return o
def ocean(n,cx,cy,w,d,m,amp=0.18,coll=None,speed=0.25):
    o=grid(n,cx,cy,w,d,(90,90),lambda x,y:0.0,m,coll)
    for k,(h,wd,sp) in enumerate([(amp,9.0,speed),(amp*0.6,4.2,speed*1.3)]):
        md=o.modifiers.new(f'wave{k}','WAVE'); md.height=h; md.width=wd; md.speed=sp; md.narrowness=1.2; md.use_normal=False
        md.start_position_x=cx-60+k*90; md.start_position_y=cy-40-k*70; md.time_offset=-200; md.lifetime=0
    return o
def noise2(x,y,s):   # cheap smooth value noise for dunes
    return (math.sin(x*0.13*s+1.7)*math.cos(y*0.11*s+0.3)+0.6*math.sin(x*0.29*s+y*0.21*s+2.1)+0.3*math.cos(x*0.53*s-y*0.47*s))/1.9
def grass(n,c,s=1.0,seed=0,coll=None,col=None):
    m=card_mat('grass%d'%(seed%3),'grass%d'%(seed%3),emit=0.15)
    for k in range(2):
        g=plane(f'{n}_{k}',(c[0],c[1],c[2]+0.5*s),1.0*s,1.0*s,m,coll=coll); g.rotation_euler=(0,0,math.radians(seed*37%180+k*90)); g['noink']=1
def ship(n,loc,heading=0.0,coll=None,detail=True,sails=True,scale=1.0):
    """our own 17th-century merchant ship: lofted hull, raised castles, three masts with square sails, rigging lines"""
    e=empty(n,loc,coll=coll); e.rotation_euler=(0,0,math.radians(heading)); e.scale=(scale,)*3
    HULL=surf('hull','hull',(3,3)); DECK=surf('deckm','deck',(3,3)); SAIL=surf('sailm','sail',(6,6),gen=True)
    Lh,Wd,Dp=26.0,7.2,4.6
    bm=bmesh.new(); rings=[]; ns=22; nr=9
    for i in range(ns):
        t=i/(ns-1); y=-Lh/2+Lh*t
        bowk=max(0.0,(t-0.62)/0.38); hw=Wd/2*(1-bowk**1.8*0.92)*(0.92 if t<0.08 else 1.0)
        top=Dp*0.5+ (1.2*max(0,0.12-t)/0.12) + 0.9*bowk**2
        ring=[]
        for k in range(nr):
            a=math.pi*k/(nr-1); x=-hw*math.cos(a); zf=math.sin(a)
            z=top-(Dp*(1-bowk*0.35))*zf**0.75 if 0<k<nr-1 else top
            ring.append(bm.verts.new((x,y,z)))
        rings.append(ring)
    for i in range(ns-1):
        for k in range(nr-1): bm.faces.new((rings[i][k],rings[i][k+1],rings[i+1][k+1],rings[i+1][k]))
    bm.faces.new(list(reversed(rings[0]))); bm.faces.new(rings[-1])
    me=bpy.data.meshes.new(n+'_hull'); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth=True
    h=bpy.data.objects.new(n+'_hull',me); (coll or L.C_SET).objects.link(h); me.materials.append(HULL); h.parent=e
    parts=[]
    parts.append(box(n+'_deck',(0,0.4,Dp*0.5-0.05),(Wd*0.9,Lh*0.78,0.1),DECK,coll=coll,bv=0))
    parts.append(box(n+'_stern',(0,-Lh/2+3.0,Dp*0.5+1.1),(Wd*0.92,5.6,2.2),HULL,coll=coll))
    parts.append(box(n+'_sterntop',(0,-Lh/2+2.4,Dp*0.5+2.25),(Wd*0.94,4.6,0.12),DECK,coll=coll,bv=0))
    parts.append(box(n+'_fore',(0,Lh/2-4.0,Dp*0.5+0.75),(Wd*0.62,3.6,1.5),HULL,coll=coll))
    parts.append(box(n+'_wale',(0,-2.0,Dp*0.5-0.9),(Wd*1.0,Lh*0.45,0.2),flat('wale',lin((86,56,36)),0.6),coll=coll,bv=0.02))
    for sx in(-1,1):   # deck rails
        parts.append(box(f'{n}_rail{sx}',(sx*Wd*0.44,0.3,Dp*0.5+0.55),(0.12,Lh*0.6,0.12),HULL,coll=coll,bv=0))
        if detail:
            for j in range(9): parts.append(cyl(f'{n}_bal{sx}{j}',(sx*Wd*0.44,-7+j*1.9,Dp*0.5+0.27),0.05,0.55,HULL,v=6,coll=coll))
            for j in range(4): parts.append(box(f'{n}_port{sx}{j}',(sx*Wd*0.47,-6+j*3.4,Dp*0.5-1.6),(0.1,0.6,0.5),flat('portlid',lin((150,40,34)),0.6),coll=coll,bv=0.02))
    parts.append(cyl(n+'_bowsprit',(0,Lh/2+0.5,Dp*0.5+1.55),0.16,7.0,HULL,v=8,coll=coll,rot=(math.radians(-70),0,0)))
    MAST=flat('mast',lin((120,86,54)),0.7)
    for j,(y,hgt) in enumerate([(5.5,18.0),(-0.5,21.0),(-7.5,14.0)]):
        parts.append(cyl(f'{n}_mast{j}',(0,y,Dp*0.5+hgt/2),0.24,hgt,MAST,v=10,coll=coll))
        parts.append(cyl(f'{n}_top{j}',(0,y,Dp*0.5+hgt*0.62),0.9,0.25,MAST,v=12,coll=coll))
        if sails:
            for k,(zz,wsail,hs) in enumerate([(0.32,8.4 if j<2 else 5.0,5.0),(0.78,6.0 if j<2 else 3.6,3.6)]):
                z=Dp*0.5+hgt*zz; parts.append(cyl(f'{n}_yard{j}{k}',(0,y+0.25,z+hs/2+0.1),0.12,wsail+0.8,MAST,v=8,coll=coll,rot=(0,math.radians(90),0)))
                bm=bmesh.new(); vv=[]
                for a_ in range(7):
                    row=[]
                    for b_ in range(7):
                        u,v=a_/6,b_/6; row.append(bm.verts.new(((u-0.5)*wsail,0.9*math.sin(math.pi*u)*math.sin(math.pi*(0.15+0.85*v))+0.3,(v-0.5)*hs)))
                    vv.append(row)
                for a_ in range(6):
                    for b_ in range(6): bm.faces.new((vv[a_][b_],vv[a_+1][b_],vv[a_+1][b_+1],vv[a_][b_+1]))
                me=bpy.data.meshes.new(f'{n}_sail{j}{k}'); bm.to_mesh(me); bm.free(); uv=me.uv_layers.new()
                for p in me.polygons:
                    p.use_smooth=True
                    for li in p.loop_indices:
                        co=me.vertices[me.loops[li].vertex_index].co; uv.data[li].uv=(co.x/wsail+0.5,co.z/hs+0.5)
                so=bpy.data.objects.new(f'{n}_sail{j}{k}',me); (coll or L.C_SET).objects.link(so); me.materials.append(SAIL); so.location=(0,y-0.05,z); parts.append(so)
        if detail:   # shrouds: lines from the mast top to the rails
            for sx in(-1,1):
                for q in range(3):
                    a=Vector((sx*Wd*0.46,y-1.2+q*1.2,Dp*0.5+0.6)); b=Vector((0,y,Dp*0.5+hgt*0.62)); mid=(a+b)/2; dv=b-a
                    ln=cyl(f'{n}_shroud{j}{sx}{q}',tuple(mid),0.025,dv.length,INK,v=5,coll=coll); ln.rotation_mode='QUATERNION'; ln.rotation_quaternion=dv.to_track_quat('Z','Y'); ln['noink']=1; parts.append(ln)
    if detail:
        lan=sph(n+'_lantern',(0,-Lh/2+0.4,Dp*0.5+2.61),0.3,flat('lanternglow',lin((255,220,140)),0.4,emit=4.0),coll=coll); parts.append(lan)
    for p in parts: p.parent=e
    return e
def char_on(inst,kind,shot,loc,rng,face0=None,arms=('arm','arm'),walker=False,scale=1.0):
    ch=char(inst,kind,shot,loc,rng,face0,arms=arms,walker=walker,scale=scale); ALL.append(ch); return ch
def onship(ch,ship_=None):
    ship_=ship_ or MF; p=ch['root'].location.copy(); ch['root'].parent=ship_; ch['root'].location=(p.x-ship_.location.x,p.y-ship_.location.y,p.z-0.02); return ch
def drift_faces(ch,f0,f1,pool,seed,step=(20,38)):
    rr=random.Random(seed); f=f0; seq=[]
    while f<f1: seq.append((f,rr.choice(pool))); f+=rr.randint(*step)
    faces(ch,seq)
def fx(n,img,loc,f0,dur,size,coll,face='-Y',grow=1.6,rise=0.0):
    """flat FX card on ones: pops at f0, grows, fades by hiding (Rick flat FX 12-27 f)"""
    o=plane(n,loc,size,size,card_mat(img,img,emit=0.6),coll=coll,face=face); o['noink']=1
    for k in range(0,dur+1,2):
        s_=1+(grow-1)*k/dur; o.scale=(s_,s_,s_); o.keyframe_insert('scale',frame=f0+k)
        o.location=(loc[0],loc[1],loc[2]+rise*k/dur); o.keyframe_insert('location',frame=f0+k)
    vis(o,[(f0,f0+dur)])
    for fc in o.animation_data.action.fcurves:
        if fc.data_path in('scale','location'):
            for kp in fc.keyframe_points: kp.interpolation='CONSTANT'   # assets on ones [RULE]
    return o
def onone(o):
    if o.animation_data and o.animation_data.action:
        for fc in o.animation_data.action.fcurves:
            if fc.data_path!='hide_render':
                for kp in fc.keyframe_points: kp.interpolation='CONSTANT'
def fall(o,f0,dur,p0,p1,rot0=None,rot1=None):
    """ease-in fall on ones, no bounce (asset physics: fall 12.5 f ease-in)"""
    for k in range(dur+1):
        t=(k/dur)**2; o.location=tuple(p0[i]+(p1[i]-p0[i])*t for i in range(3)); o.keyframe_insert('location',frame=f0+k)
        if rot0: o.rotation_euler=tuple(rot0[i]+(rot1[i]-rot0[i])*t for i in range(3)); o.keyframe_insert('rotation_euler',frame=f0+k)
    onone(o)
def hardcut(shot,f):
    for o_ in (L.CAM[shot],L.TGT[shot]):
        for fc in o_.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                if int(round(kp.co[0]))==f-1: kp.interpolation='CONSTANT'
def skydome(n,c,rad,h,img,z0=-20,rep=5):
    bm=bmesh.new(); seg=72; lo=[];hi=[]
    for i in range(seg+1):
        a=2*math.pi*i/seg; lo.append(bm.verts.new((c[0]+rad*math.cos(a),c[1]+rad*math.sin(a),z0))); hi.append(bm.verts.new((c[0]+rad*math.cos(a),c[1]+rad*math.sin(a),z0+h)))
    fs=[bm.faces.new((lo[i],hi[i],hi[i+1],lo[i+1])) for i in range(seg)]
    me=bpy.data.meshes.new(n); bm.to_mesh(me); bm.free(); uv=me.uv_layers.new()
    for p in me.polygons:
        for li in p.loop_indices:
            v=me.vertices[me.loops[li].vertex_index].co; a=math.atan2(v.y-c[1],v.x-c[0])%(2*math.pi); uv.data[li].uv=(a/(2*math.pi)*rep,(v.z-z0)/h)
    # fix the seam column
    for p in me.polygons:
        us=[uv.data[li].uv[0] for li in p.loop_indices]
        if max(us)-min(us)>rep/2:
            for li in p.loop_indices:
                if uv.data[li].uv[0]<rep/2: uv.data[li].uv=(uv.data[li].uv[0]+rep,uv.data[li].uv[1])
    o=bpy.data.objects.new(n,me); L.C_NOI.objects.link(o); m=card_mat(img,img,emit=1.0); me.materials.append(m); o['fly']=1; o['noink']=1
    m.node_tree.nodes['Image Texture'].extension='REPEAT'
    return o
def skycard(n,loc,face_,w,h,img,coll=None):
    s_=plane(n,loc,w,h,card_mat(img,img,emit=1.0),coll=coll or L.C_NOI,face=face_); s_['fly']=1; s_['noink']=1; return s_
# ======================= SET R: Plymouth shore (x=0): the rock; dressed for today (S01, S14, S18) and for 1741 (S16, S17) =======================
SAND=surf('sand','sand',(4,4)); WET=surf('sandwet','sand_wet',(4,4)); WAT=surf('water','water',(8,8),rough=0.25)
grid('R_beach',0,-10,90,60,(60,40),lambda x,y:0.25*noise2(x,y,1.0)+0.02*(y+20)*0 - max(0,(y-6))*0.06,SAND)
grid('R_wet',0,14,90,12,(40,8),lambda x,y:-0.25-(y-8)*0.05,WET)
ocean('R_sea',0,60,160,90,WAT,amp=0.10)
skydome('R_sky',(0,0),240,170,'sky_cape')
sf=plane('R_shore',(0,118,3.5),300,70,card_mat('shore_far','shore_far',emit=0.5),coll=L.C_NOI,face='-Y'); sf['fly']=1
ROCK=surf('rockm','rock',(1.6,1.6))
rk=sph('rock',(0,4,0.15),1.0,ROCK,sc_=(1.7,1.15,0.75),seg=20)
for v in rk.data.vertices: v.co*= (1+0.08*math.sin(v.co.x*7+v.co.z*5)+0.05*math.cos(v.co.y*9))
plate=plane('rock_1620',(0,2.86,0.42),1.25,0.62,card_mat('rock1620','rock1620',emit=0.05),face='-Y'); plate.rotation_euler=(math.radians(-14),0,0); plate['noink']=1
for i,(x,y) in enumerate([(-4,-3),(5,-6),(-7,6),(8,3),(3,9)]): sph(f'R_stone{i}',(x,y,0.05),0.4+0.1*i,ROCK,sc_=(1.3,1.0,0.6),seg=10)
for i in range(18):
    a=R.uniform(0,2*math.pi); rr=R.uniform(7,16); grass(f'R_g{i}',(math.cos(a)*rr,-abs(math.sin(a))*rr-3,0.1),R.uniform(0.7,1.2),i)
# today's dressing (S01, S14, S18): route signpost, rope posts
TODAY=shared('R_today',['S01','S14','S18'])
cyl('R_post',(2.7,2.2,1.1),0.08,2.2,surf('wharfm','wharf',(1,1)),v=10,coll=TODAY)
sg=plane('R_sign',(2.7,2.12,1.75),1.3,0.65,card_mat('sign_route','sign_route',emit=0.12),coll=TODAY,face='-Y'); sg.rotation_euler=(math.radians(90),0,math.radians(-12))
for i in range(7):
    a=math.radians(200+i*20); cyl(f'R_rp{i}',(math.cos(a)*2.6,4+math.sin(a)*2.0,0.45),0.06,0.9,flat('ropepost',lin((176,150,110)),0.8),v=8,coll=TODAY)
# 1741 dressing (S16, S17): a wharf being built toward the rock
OLD=shared('R_1741',['S16','S17'])
WH=flat('pilewood',lin((156,116,78)),0.8,emit=0.3)   # r2: the painted wharf texture read near-black on piles in shadow
for i in range(7):
    for sx in(-1,1): cyl(f'R_pile{i}{sx}',(7.0+sx*1.35,3.0+i*2.0,0.35),0.15,1.4,WH,v=10,coll=OLD)
box('R_deckw',(7.0,9.5,0.78),(2.9,11.0,0.12),WH,coll=OLD,bv=0.02)
for i in range(5): box(f'R_plank{i}',(1.8+R.uniform(-0.3,0.3),-0.8+i*0.2,0.06+i*0.09),(2.6,0.32,0.08),WH,coll=OLD,bv=0.01).rotation_euler=(0,0,R.uniform(-0.2,0.2))
pass   # stills r3: the lone barrel read as a dark flat panel; removed
# ======================= SET S: the sea (x=300): Mayflower, sandbars, the Cape tip =======================
SX=700
WST=surf('waterstorm','water_storm',(8,8),rough=0.2)
ocean('S_sea',SX,0,420,420,surf('waterS','water',(8,8),rough=0.25),amp=0.35,speed=0.3)
skydome('S_sky',(SX,0),260,190,'sky_cape')
cape=plane('S_cape',(SX,200,6),420,92,card_mat('dunes_far','dunes_far',emit=0.5),coll=L.C_NOI,face='-Y'); cape['fly']=1
capeW=plane('S_capeW',(SX-200,40,6),300,66,card_mat('dunes_far','dunes_far',emit=0.5),coll=L.C_NOI,face='+X'); capeW['fly']=1
MF=ship('MF',(SX,0,-0.6),heading=0)
# sea motion: the ship rolls and pitches gently through every sea shot (assets on ones)
for f in range(0,END+1,2):
    MF.rotation_euler=(math.radians(1.6*math.sin(f/23)),math.radians(2.2*math.sin(f/31+1)),0); MF.keyframe_insert('rotation_euler',frame=f)
onone(MF)
# S04 sandbars: foam lines and breaking shoals ahead of the ship (shot only)
C4=C('S04')
for i in range(9):
    x=SX+R.uniform(-30,30); y=R.uniform(26,60)
    fm=plane(f'S4_foam{i}',(x,y,0.12),R.uniform(8,18),R.uniform(1.0,2.4),card_mat('fx_splash','fx_splash',emit=0.4),coll=C4,horiz=True); fm['noink']=1
    grid(f'S4_bar{i}',x,y+2,R.uniform(6,12),R.uniform(2,4),(6,4),lambda X,Y:0.05,WET,coll=C4,z0=-0.05)
st=ocean('S4_rough',SX,20,160,160,WST,amp=0.7,coll=C4,speed=0.45); st.location.z=0.05
# shallop for S13 (bay crossing) sits east in the same sea
SHAL=empty('shallop',(SX+70,40,0.0)); SHAL.rotation_euler=(0,0,math.radians(-90))
hb=bmesh.new(); bmesh.ops.create_cube(hb,size=1.0); bmesh.ops.scale(hb,vec=Vector((2.2,8.0,1.0)),verts=hb.verts)
for v in hb.verts:
    t=(v.co.y+4)/8; v.co.x*= (1-0.85*max(0,t-0.7)/0.3) ; v.co.z-=0.0
    if v.co.z<0: v.co.x*=0.55
me=bpy.data.meshes.new('shal_hull'); hb.to_mesh(me); hb.free(); sh_=bpy.data.objects.new('shal_hull',me); L.C_SET.objects.link(sh_); me.materials.append(surf('hull','hull',(3,3))); sh_.parent=SHAL; sh_.location=(0,0,0.3)
cyl('shal_mast',(0,1.2,3.2),0.1,5.6,flat('mast',lin((120,86,54))),v=8).parent=SHAL
ss=plane('shal_sail',(0,1.4,3.6),2.3,2.7,surf('sailm','sail',(6,6),gen=True)); ss.rotation_euler=(0,0,math.radians(90+8)); ss.parent=SHAL
for f in range(1322,1413,2):
    SHAL.location=(SX+70+(f-1322)*0.12,40,0.05*math.sin(f/9)); SHAL.keyframe_insert('location',frame=f)
    SHAL.rotation_euler=(math.radians(2*math.sin(f/11)),0,math.radians(-90)); SHAL.keyframe_insert('rotation_euler',frame=f)
onone(SHAL)
sf2=plane('S_plyshore',(SX+190,40,4),300,66,card_mat('shore_far','shore_far',emit=0.5),coll=L.C_NOI,face='-X'); sf2['fly']=1
# ======================= SET I: below deck (x=600): the signing (S06), the chart (S03), the journal (S15) =======================
IX=1300; CAB=surf('cabinw','cabin',(2.4,2.4)); CFL=surf('cabinf','cabin_floor',(2.4,2.4))
box('I_floor',(IX,0,-0.05),(10,8,0.1),CFL,bv=0); box('I_ceil',(IX,0,2.65),(10,8,0.1),CAB,bv=0)
for sx in(-1,1): box(f'I_wallx{sx}',(IX+sx*5,0,1.3),(0.1,8,2.7),CAB,bv=0)
for sy in(-1,1): box(f'I_wally{sy}',(IX,sy*4,1.3),(10,0.1,2.7),CAB,bv=0)
for i in range(6): box(f'I_beam{i}',(IX-4.2+i*1.7,0,2.5),(0.22,8,0.22),flat('beam',lin((90,60,40)),0.8),bv=0.02)
for i in range(3): box(f'I_knee{i}',(IX-4.85,-2.5+i*2.5,1.6),(0.2,0.2,1.8),flat('beam',lin((90,60,40))),bv=0.02)
def lantern(n,c,strength=60):
    cyl(n+'_cap',(c[0],c[1],c[2]+0.2),0.12,0.06,INK,v=10); g=cyl(n,c,0.11,0.3,flat('lanternglow',lin((255,220,140)),0.4,emit=4.0),v=12)
    bpy.ops.object.light_add(type='POINT',location=c); l=bpy.context.object; l.name=n+'_L'; l.data.energy=strength; l.data.color=(1.0,0.82,0.55); l.data.shadow_soft_size=0.3
for i,c in enumerate([(IX-1.0,0.6,2.1),(IX+2.0,-1.0,2.1),(IX-3.2,-2.2,2.1),(IX+3.6,2.4,2.1)]): lantern(f'I_lan{i}',c,90)
bpy.ops.object.light_add(type='AREA',location=(IX,0,2.45)); al=bpy.context.object; al.name='I_fill'; al.data.energy=320; al.data.size=6; al.data.color=(1.0,0.86,0.7)
BAR=surf('barrelm','barricade',(1,1))
cyl('I_barrel',(IX,0.6,0.42),0.42,0.84,BAR,v=20); cyl('I_hoop',(IX,0.6,0.7),0.44,0.06,INK,v=20)
CP=[plane(f'I_compact{k}',(IX,0.55,0.845),0.36,0.49,card_mat(f'compact{k}',f'compact{k}',emit=0.25),coll=C('S06'),horiz=True) for k in range(3)]
for o_ in CP: o_.rotation_euler=(0,0,math.radians(8)); o_['noink']=1
vis(CP[0],[(502,529)]); vis(CP[1],[(530,551)]); vis(CP[2],[(552,583)])
for k,(x,y) in enumerate([(IX-2.2,1.8),(IX+1.9,2.6),(IX-3.6,-0.4)]):
    cyl(f'I_crate{k}',(x,y,0.35),0.35,0.7,BAR,v=8) if k==2 else box(f'I_crate{k}',(x,y,0.4),(0.8,0.8,0.8),BAR,bv=0.04)
for k in range(5): cyl(f'I_rope{k}',(IX+3.8,-3.2+k*0.08,0.08+k*0.09),0.4-0.04*k,0.08,flat('rope',lin((190,160,110)),0.9),v=16)
# chart table (S03)
box('I_ctable',(IX+2.6,-2.2,0.74),(1.8,1.2,0.06),surf('deckm','deck',(3,3)),bv=0.02)
for sx in(-1,1):
    for sy in(-1,1): box(f'I_ctl{sx}{sy}',(IX+2.6+sx*0.8,-2.2+sy*0.5,0.36),(0.08,0.08,0.72),INK,bv=0)
ch_=plane('I_chart',(IX+2.6,-2.2,0.775),1.5,1.0,card_mat('chart','chart',emit=0.2),horiz=True); ch_['noink']=1
cyl('I_divider',(IX+2.2,-2.0,0.79),0.012,0.5,flat('brass',lin((200,170,90)),0.3,metal=0.6),v=6,rot=(0,math.radians(80),0.4))
# journal desk (S15)
box('I_desk',(IX-3.4,2.6,0.74),(1.6,1.0,0.06),surf('deckm','deck',(3,3)),bv=0.02)
box('I_deskbody',(IX-3.4,2.85,0.37),(1.5,0.4,0.7),BAR,bv=0.02)
jr=plane('I_journal',(IX-3.4,2.55,0.775),0.9,0.6,card_mat('journal','journal',emit=0.22),horiz=True); jr['noink']=1
cyl('I_candle',(IX-2.85,2.8,0.86),0.035,0.2,flat('wax',lin((240,230,200)),0.6),v=10); sph('I_flame',(IX-2.85,2.8,0.99),0.03,flat('flame',lin((255,200,110)),0.3,emit=8.0),sc_=(1,1,1.8))
bpy.ops.object.light_add(type='POINT',location=(IX-2.85,2.8,1.05)); cl=bpy.context.object; cl.name='I_candleL'; cl.data.energy=25; cl.data.color=(1.0,0.75,0.45)
# ======================= SET D: Cape dunes and Corn Hill (x=900) =======================
DX=1900
def dune(x,y):
    h=1.2*noise2(x,y,0.8)+0.5*noise2(x+40,y-20,2.0)
    h+=3.0*math.exp(-((x-DX)**2+(y-12)**2)/60.0)   # Corn Hill
    return h-max(0,(y-38))*0.25
grid('D_dunes',DX,0,140,100,(90,70),dune,SAND)
ocean('D_bay',DX,95,240,90,surf('waterB','water_bay',(8,8),rough=0.25),amp=0.12)
skydome('D_sky',(DX,0),200,160,'sky_cape')
ship('MF2',(DX+18,112,-0.6),heading=70,detail=False)
for i in range(170):
    x=DX+R.uniform(-55,55); y=R.uniform(-40,36)
    if abs(x-DX)<2.4 and abs(y-12)<2.4: continue
    grass(f'D_g{i}',(x,y,dune(x,y)-0.05),R.uniform(0.7,1.5),i)
C9=C('S09')
pit=plane('D_pit',(DX,12,dune(DX,12)+0.03),1.4,1.4,flat('pit',lin((150,120,84)),0.9),coll=C9,horiz=True); pit['noink']=1
bsk=cyl('D_basket',(DX,12,dune(DX,12)-0.5),0.32,0.36,surf('basketm','basket',(0.5,0.5)),v=16,coll=C9)
crn=cyl('D_corn',(0,0,0.19),0.29,0.04,surf('cornm','corn',(0.3,0.3)),v=16,coll=C9); crn.parent=bsk; vis(crn,[(766,898)])   # check_scene r2: corn stayed visible after the basket left
bz=dune(DX,12)
for f,z in [(766,bz-0.5),(812,bz-0.5),(816,bz-0.05),(818,bz+0.1),(820,bz+0.05)]: kloc(bsk,f,(DX,12,z))
onone(bsk)
cyl('D_signpost',(DX+3.2,10.5,dune(DX+3.2,10.5)+0.8),0.07,1.7,surf('wharfm','wharf',(1,1)),v=8,coll=C9)
s9=plane('D_sign',(DX+3.2,10.4,dune(DX+3.2,10.5)+1.45),1.1,0.41,card_mat('sign_cornhill','sign_cornhill',emit=0.15),coll=C9,face='-Y'); s9.rotation_euler=(math.radians(90),0,math.radians(-20))
fx('D_spray1','fx_sand',(DX-0.3,11.5,bz+0.5),804,14,1.0,C9,grow=1.8,rise=0.4); fx('D_spray2','fx_sand',(DX+0.3,11.6,bz+0.5),811,12,0.8,C9,grow=1.7,rise=0.3)
fx('D_spark','fx_spark',(DX,11.4,bz+0.6),818,14,0.9,C9,grow=1.4)
# ======================= SET E: dawn beach, the First Encounter (x=1200) =======================
EX=2600; SD=surf('sanddawn','sand_dawn',(4,4))
def eb(x,y): return 0.25*noise2(x,y,1.3)-max(0,(y-8))*0.08+max(0,(-y-14))*0.12
grid('E_beach',EX,0,120,80,(70,50),eb,SD)
ocean('E_sea',EX,70,240,80,surf('waterD','water_dawn',(8,8),rough=0.25),amp=0.12)
skydome('E_sky',(EX,0),200,160,'sky_dawn')
tl=plane('E_trees',(EX,-32,3.6),150,11,card_mat('trees_dawn','trees_dawn',emit=0.35),coll=L.C_NOI,face='+Y'); tl['fly']=1
tl2=plane('E_trees2',(EX-6,-46,5.0),190,15,card_mat('trees','trees',emit=0.3),coll=L.C_NOI,face='+Y'); tl2['fly']=1
for i in range(60):
    x=EX+R.uniform(-50,50); y=R.uniform(-30,-6); grass(f'E_g{i}',(x,y,eb(x,y)-0.05),R.uniform(0.7,1.4),i+5)
BARR=surf('barrm','barricade',(1.5,1.5))
for i in range(9):   # log barricade in an arc
    a=math.radians(200+i*17); x=EX+math.cos(a)*5.5; y=1.5+math.sin(a)*4.0
    for k in range(3): o_=cyl(f'E_log{i}{k}',(x,y,0.25+k*0.42),0.22,2.4,BARR,v=10,rot=(0,math.radians(90),a+math.pi/2+R.uniform(-0.1,0.1)))
    cyl(f'E_stake{i}',(x,y-0.1,0.9),0.07,1.9,BARR,v=6)
for k in range(5): cyl(f'E_fire{k}',(EX+0.6,3.2,0.12),0.06,1.1,BARR,v=6,rot=(0,math.radians(90),k*0.63))
for k in range(3): o_=cyl(f'E_flame{k}',(EX+0.6+0.12*(k-1),3.2,0.42),0.16,0.6,flat('flame',lin((255,180,80)),0.3,emit=6.0),v=10,r2=0.01); o_['noink']=1
bpy.ops.object.light_add(type='POINT',location=(EX+0.6,3.2,0.9)); fl=bpy.context.object; fl.name='E_fireL'; fl.data.energy=400; fl.data.color=(1.0,0.62,0.3)
ship('MF3',(EX+90,120,-0.6),heading=95,detail=False)
C11=C('S11')
ARROW=flat('arrowshaft',lin((170,130,80)),0.7); FL=flat('fletch',lin((230,226,214)),0.8)
def arrow(n,p0,p1,f0,dur,coll):
    e=empty(n,p0,coll=coll); d_=Vector(p1)-Vector(p0)
    s_=cyl(n+'_s',(0,0,0),0.018,0.85,ARROW,v=6,coll=coll,rot=(0,math.radians(90),0)); s_.parent=e
    for k in range(2): f_=plane(f'{n}_f{k}',(-0.38,0,0),0.16,0.07,FL,coll=coll); f_.rotation_euler=(k*math.pi/2,0,0); f_.parent=e; f_['noink']=1
    yaw=math.atan2(d_.y,d_.x); pit_=math.atan2(-d_.z,math.hypot(d_.x,d_.y))
    for k in range(dur+1):
        t=k/dur; e.location=tuple(p0[i]+(p1[i]-p0[i])*t for i in range(2))+(p0[2]+(p1[2]-p0[2])*t+1.2*math.sin(math.pi*t),); e.keyframe_insert('location',frame=f0+k)
        ang=pit_-math.radians(26)*math.cos(math.pi*t); e.rotation_euler=(0,ang,yaw); e.keyframe_insert('rotation_euler',frame=f0+k)
    onone(e); return e
for i,(x,y) in enumerate([(-1.8,-0.9),(0.3,-1.6),(1.9,-1.0),(-0.6,-1.4),(1.0,-1.5)]):
    arrow(f'E_arrow{i}',(EX+x*3,-22,1.4),(EX+x,y+0.2,0.7+0.25*(i%2)),1157+i*3,12,C11)
for i,(x,f0) in enumerate([(-1.2,1197),(0.4,1200),(1.6,1204)]): fx(f'E_smoke{i}','fx_smoke',(EX+x,-0.6,1.35),f0,24,0.9,C11,face='-Y',grow=2.2,rise=0.6)
C12=C('S12')
for sx in(-1,1): cyl(f'E_spost{sx}',(EX+14+sx*0.9,-12,0.9),0.08,1.8,surf('wharfm','wharf',(1,1)),v=8,coll=C12)
se=plane('E_sign',(EX+14,-12.08,1.6),2.0,1.0,card_mat('sign_encounter','sign_encounter',emit=0.15),coll=C12,face='+Y')
# ======================= SET G: the payoff, a dune-top print shop (x=1800) =======================
GX=3300
def gd(x,y): return 0.6*noise2(x,y,1.0)-max(0,(y-14))*0.15
grid('G_dunes',GX,0,90,70,(60,50),gd,SAND)
ocean('G_sea',GX,70,200,80,surf('waterB','water_bay',(8,8),rough=0.25),amp=0.1)
skydome('G_sky',(GX,0),180,150,'sky_cape')
SHG=surf('shinglem','shingle',(2,2)); TRIM=surf('trimm','shingle_trim',(1.5,1.5))
HX,HY=GX,4.0
box('G_back',(HX,HY+3.0,1.6),(6.4,0.3,3.2),SHG,bv=0.02)
for sx in(-1,1): box(f'G_side{sx}',(HX+sx*3.05,HY+1.5,1.6),(0.3,3.0,3.2),SHG,bv=0.02)
box('G_frontL',(HX-2.15,HY,1.6),(2.1,0.3,3.2),SHG,bv=0.02); box('G_frontR',(HX+2.15,HY,1.6),(2.1,0.3,3.2),SHG,bv=0.02)
box('G_frontB',(HX,HY,0.4),(2.2,0.3,0.8),SHG,bv=0.02); box('G_frontT',(HX,HY,2.85),(2.2,0.3,0.7),SHG,bv=0.02)
for nm,c_,s_ in [('G_trimL',(HX-1.12,HY-0.18,1.6),(0.14,0.1,1.8)),('G_trimR',(HX+1.12,HY-0.18,1.6),(0.14,0.1,1.8)),('G_trimT',(HX,HY-0.18,2.52),(2.38,0.1,0.14)),('G_sill',(HX,HY-0.25,0.78),(2.5,0.3,0.1))]: box(nm,c_,s_,TRIM,bv=0.02)
rm=bmesh.new(); vv=[rm.verts.new(p) for p in [(-3.4,-0.4,3.2),(3.4,-0.4,3.2),(3.4,3.4,3.2),(-3.4,3.4,3.2),(-3.4,1.5,4.9),(3.4,1.5,4.9)]]
for f_ in [(0,1,5,4),(3,2,5,4)[::-1],(0,4,3),(1,2,5)]: rm.faces.new([vv[i] for i in f_])
me=bpy.data.meshes.new('G_roof'); rm.to_mesh(me); rm.free(); ro=bpy.data.objects.new('G_roof',me); L.C_SET.objects.link(ro); me.materials.append(surf('roofm','shingle',(1.5,1.5))); ro.location=(HX,HY,0)
box('G_chim',(HX+1.8,HY+2.0,4.6),(0.6,0.6,1.4),flat('brick',lin((150,70,50)),0.8),bv=0.03)
gs=plane('G_sign',(HX,HY-0.16,3.0),2.6,0.32,card_mat('sign_gallery','sign_gallery',emit=0.25),face='-Y'); gs['noink']=1
# display bay inside the window: warm back wall, easel, the poster (pasted at true colour in post)
box('G_bayback',(HX,HY+1.0,1.6),(2.2,0.08,2.0),flat('baywall',lin((236,222,196)),0.8),bv=0)
box('G_bayfloor',(HX,HY+0.5,0.82),(2.2,1.0,0.06),surf('deckm','deck',(3,3)),bv=0)
PW,PH=0.80,1.20; PZ=1.72; PY=HY+0.55
box('poster_frame',(HX,PY+0.03,PZ),(PW+0.12,0.04,PH+0.12),flat('pframe',lin((246,236,214)),0.35,emit=0.9),bv=0.01)   # r3: the facade's sun shadow drew a band across the frame
pmat=bpy.data.materials.new('poster'); N_,L_=L.nodes(pmat); pp_=N_['Principled BSDF']; it_=N_.new('ShaderNodeTexImage'); it_.image=bpy.data.images.load('/root/cc/poster_2k.png'); it_.interpolation='Cubic'
L_.new(it_.outputs['Color'],pp_.inputs['Base Color']); L_.new(it_.outputs['Color'],pp_.inputs['Emission Color']); pp_.inputs['Emission Strength'].default_value=0.15; pp_.inputs['Roughness'].default_value=1.0; pp_.inputs['Specular IOR Level'].default_value=0.0   # r2: no light-band reflection on the poster
poster=plane('poster',(HX,PY,PZ),PW,PH,pmat,coll=L.C_NOI); poster['noink']=1
for sx in(-1,1): cyl(f'G_easel{sx}',(HX+sx*0.36,PY+0.12,1.25),0.025,1.0,flat('easel',lin((120,86,54))),v=6,rot=(math.radians(-8),math.radians(sx*-10),0))
BULB=flat('bulb',lin((255,226,150)),0.4,emit=5.0)
for i in range(13): sph(f'G_bulb{i}',(HX-1.0+i*(2.0/12),HY-0.255,2.43),0.035,BULB)
bpy.ops.object.light_add(type='AREA',location=(HX,HY-0.7,2.45)); gl=bpy.context.object; gl.name='G_bayL'; gl.data.energy=140; gl.data.size=1.6; gl.data.color=(1.0,0.9,0.75); gl.rotation_euler=(math.radians(35),0,0)   # r3: was aimed away from the poster; its plane cut a lit band across the lower half
for i in range(70):
    x=GX+R.uniform(-30,30); y=R.uniform(-25,22)
    if abs(x-HX)<4.5 and -4<y<8: continue
    grass(f'G_g{i}',(x,y,gd(x,y)-0.05),R.uniform(0.7,1.4),i+11)
for i,(x,y) in enumerate([(-2.6,-0.9),(2.7,-1.0),(-1.6,-1.6)]): grass(f'G_gn{i}',(HX+x,HY+y,gd(HX+x,HY+y)),0.8,i+3)
cyl('G_fencepost0',(HX-4.5,HY-2.5,0.5),0.06,1.0,surf('wharfm','wharf',(1,1)),v=6)
# ======================= CAST + CAMERAS =======================
def S(n): return SH[n]
# ---- S01 (0-123): hook. Low angle on a Pilgrim posing on the famous rock, tourists snap photos; on "second stop" the camera swings to the route sign ----
s='S01'; r=S(s)
pa=char_on('S01_pil','pilgrimA',s,(-0.2,4.1,0.88),r,'proud',arms=('arm','arm'))
faces(pa,[(0,'proud'),(26,'grin'),(52,'proud'),(78,'happy'),(98,'shock'),(110,'worry')])
for f,a in [(0,-150),(10,-158),(30,-140),(60,-155),(96,-150),(102,-40)]: arm(pa,1,f,a)
for f,a in [(0,-20),(40,-30),(100,-60)]: arm(pa,-1,f,a)
bob(pa,[14,48,80])
t1=char_on('S01_tourA','tourA',s,(-1.6,1.5,0.08),r,'happy',arms=('arm',[(0,'arm_phone'),(90,'arm')]))
t2=char_on('S01_tourB','tourB',s,(1.5,1.2,0.06),r,'excited',arms=('arm_phone','arm'))
drift_faces(t1,0,123,['happy','excited','grin'],3); drift_faces(t2,0,123,['excited','happy','grin','shock'],4)
for f,a in [(0,-120),(30,-128),(60,-118),(90,-20)]: arm(t1,1,f,a)
for f,a in [(0,120),(40,128),(80,116),(98,80)]: arm(t2,-1,f,a)
path(s,[(0,(-0.6,-2.0,1.5),(-0.2,4.1,1.6)),(60,(-0.4,1.2,1.75),(-0.2,4.1,1.95)),(92,(0.1,1.6,1.8),(0.2,4.0,1.95)),(112,(1.4,0.2,1.7),(2.7,2.2,1.72)),(123,(1.25,0.0,1.74),(2.72,2.2,1.74))])
# ---- S02 (116-214): the Mayflower at sea, a wide truck and climb along her side ----
s='S02'; r=S(s)
path(s,[(116,(SX+28,-30,3.0),(SX,2,9)),(170,(SX+34,-12,5.0),(SX,4,9)),(214,(SX+36,6,7.0),(SX,8,9.5))])
mA=onship(char_on('S02_master','master',s,(SX+0.8,-8.0,4.62),r,'proud',arms=('arm_spyglass','arm')))
for f,a in [(116,-100),(150,-118),(190,-95)]: arm(mA,1,f,a)
drift_faces(mA,116,214,['proud','neutral','deadpan'],5)
for i,(x,y,k) in enumerate([(-1.6,2,'sailorA'),(1.5,6,'sailorB'),(-0.8,-3,'pilgrimC'),(1.2,-1.5,'pilgrimB')]):
    c_=onship(char_on(f'S02_x{i}',k,s,(SX+x,y,2.32),r,'neutral')); drift_faces(c_,116,214,['neutral','happy','deadpan'],10+i); bob(c_,[130+i*9,175+i*7])
# ---- S03 (207-278): the chart; the master's mitten runs the course to the Hudson; push-in ----
s='S03'; r=S(s)
mB=char_on('S03_master','master',s,(IX+2.6,-3.15,0.0),r,'proud',arms=('arm','arm'))
for f,a in [(207,-30),(222,-62),(238,-70),(256,-58),(270,-66)]: arm(mB,1,f,a)
faces(mB,[(207,'proud'),(230,'grin'),(252,'proud'),(266,'happy')])
pg2=char_on('S03_pil','pilgrimD',s,(IX+3.7,-2.5,0.0),r,'neutral'); drift_faces(pg2,207,278,['neutral','happy','proud'],12); bob(pg2,[236])
path(s,[(207,(IX+1.3,-0.7,1.9),(IX+2.6,-2.2,0.8)),(278,(IX+1.8,-1.25,1.55),(IX+2.45,-2.15,0.78))])
# ---- S04 (271-392): sandbars and bad winds; the ship heels through the breakers, then the camera rises and turns to the Cape tip ----
s='S04'; r=S(s)
sA=onship(char_on('S04_sailA','sailorA',s,(SX-1.5,9.5,2.32),r,'shock')); sB=onship(char_on('S04_sailB','sailorB',s,(SX+1.6,8.0,2.32),r,'grit'))
faces(sA,[(271,'shock'),(300,'grit'),(330,'shock'),(356,'worry'),(380,'happy')]); faces(sB,[(271,'grit'),(296,'shock'),(322,'grit'),(350,'shock'),(378,'worry')])
for f,a in [(271,-150),(290,-120),(310,-160),(332,-100)]: arm(sA,1,f,a)
for f,a in [(275,95),(294,80),(314,100),(336,70)]: arm(sB,-1,f,a)   # armprobe r1: sailB forearm crossed his face at 150-160 deg
bob(sA,[284,318,344]); bob(sB,[290,326])
path(s,[(271,(SX-9,34,2.0),(SX,6,5.5)),(320,(SX-12,30,3.0),(SX,4,6.0)),(352,(SX-14,24,9.0),(SX-2,40,6.0)),(392,(SX-12,18,12.0),(SX-4,90,5.0))])
# ---- S05 (385-510): bow close: the anchor drops on "anchor"; a Pilgrim's foot dangles toward the sand and is pulled back on "sand" ----
s='S05'; r=S(s)
anc=empty('S05_anchor',(SX+1.6,14.8,3.4),coll=C(s))
cyl('S05_ashank',(0,0,0),0.06,1.4,INK,v=8,coll=C(s)).parent=anc
for sx in(-1,1): a_=cyl(f'S05_aarm{sx}',(sx*0.32,0,-0.62),0.05,0.75,INK,v=8,coll=C(s),rot=(0,math.radians(sx*55),0)); a_.parent=anc
cyl('S05_astock',(0,0,0.62),0.04,0.8,INK,v=6,coll=C(s),rot=(math.radians(90),0,0)).parent=anc
kloc(anc,385,(SX+1.6,14.8,3.4)); kloc(anc,419,(SX+1.6,14.8,3.4)); fall(anc,420,12,(SX+1.6,14.8,3.4),(SX+1.6,15.0,-1.2)); kloc(anc,433,(SX+1.6,15.0,-1.2)); onone(anc)
fx('S05_splash','fx_splash',(SX+1.6,15.1,0.4),432,18,1.4,C(s),face='+X',grow=1.6,rise=0.3)
pf=onship(char_on('S05_pil','pilgrimC',s,(SX+1.2,9.8,3.82),r,'happy')); pB=onship(char_on('S05_pilB','pilgrimB',s,(SX-1.5,8.4,3.82),r,'deadpan'))   # footprobe r1: were past the deck end at y 11.5
faces(pf,[(385,'happy'),(420,'excited'),(452,'happy'),(470,'grin'),(488,'shock'),(500,'worry')]); faces(pB,[(385,'deadpan'),(440,'neutral'),(486,'grit'),(498,'deadpan')])
for f,a in [(385,-20),(430,-55),(470,-65),(486,-35)]: arm(pf,1,f,a)   # armprobe r3: a raised forearm crossed the other Pilgrim's face
for f,a in [(470,-10),(484,-60),(492,-55)]: arm(pB,1,f,a)
kloc(pf['root'],458,(1.2,9.8,3.8)); kloc(pf['root'],470,(1.0,10.62,3.8)); kloc(pf['root'],488,(1.0,10.62,3.8)); kloc(pf['root'],492,(1.2,9.8,3.8))
path(s,[(385,(SX+5.0,18.6,2.7),(SX+1.6,14.9,3.0)),(419,(SX+4.7,18.2,2.5),(SX+1.6,14.9,2.7)),(432,(SX+4.5,17.9,1.7),(SX+1.6,15.0,0.5)),(446,(SX+3.2,12.6,4.5),(SX+1.1,9.9,4.0)),(510,(SX+2.9,12.2,4.55),(SX+1.0,9.7,4.1))])   # stills r3: the Pilgrim sat at the frame edge
# ---- S06 (502-583): below deck, the men sign the deal to rule themselves ----
s='S06'; r=S(s)
sg1=char_on('S06_sign','pilgrimD',s,(IX-0.1,1.35,0.0),r,'proud',arms=('arm',[(502,'arm'),(512,'arm_quill')]))
for f,a in [(502,-20),(512,-55),(520,-62),(528,-50),(536,-60),(546,-48)]: arm(sg1,1,f,a)
faces(sg1,[(502,'proud'),(518,'deadpan'),(534,'proud'),(552,'happy'),(570,'grin')])
SG=[]
for i,(x,y,k) in enumerate([(-1.0,1.6,'pilgrimA'),(1.0,1.7,'pilgrimB'),(-1.6,0.4,'pilgrimC'),(1.5,0.5,'master')]):
    c_=char_on(f'S06_x{i}',k,s,(IX+x,y,0.0),r,'neutral'); drift_faces(c_,502,583,['happy','proud','neutral','grin'],20+i,(14,28)); bob(c_,[515+i*11,548+i*7]); SG.append(c_)
for f,a in [(552,-150),(566,-140)]: arm(SG[1],1,f,a)
path(s,[(502,(IX+0.5,-1.2,1.6),(IX,1.2,1.15)),(546,(IX+0.2,-0.8,1.55),(IX,1.2,1.1)),(583,(IX-0.4,-0.6,1.6),(IX-0.1,1.3,1.15))])
# ---- S07 (576-662): five weeks poking around the Cape: a line of Pilgrims over the dunes, one with a spyglass ----
s='S07'; r=S(s)
for i,k in enumerate(['pilgrimA','pilgrimB','pilgrimC','pilgrimD']):
    p0=(DX-14+i*2.2,-6-i*0.7,0); p1=(DX-6+i*2.2,-2-i*0.7,0)
    z0=dune(p0[0],p0[1]); z1=dune(p1[0],p1[1])
    c_=char_on(f'S07_p{i}',k,s,(p0[0],p0[1],z0),r,'neutral',arms=('arm',('arm_spyglass' if i==0 else 'arm_musket')),walker=True)
    gwalk(c_,576,662,(p0[0],p0[1],z0),(p1[0],p1[1],z1),dune,step=4)
    drift_faces(c_,576,662,['neutral','deadpan','worry','proud'],30+i,(16,30))
    if i==0:
        for f,a in [(600,-95),(612,-110),(640,-100)]: arm(c_,1,f,a)
path(s,[(576,(DX-11.2,-9.6,dune(DX-11.2,-9.6)+1.6),(DX-11.8,-5.8,dune(DX-11.8,-5.8)+1.2)),(662,(DX-3.4,-5.8,dune(DX-3.4,-5.8)+1.6),(DX-4.0,-2.2,dune(DX-4.0,-2.2)+1.2))])   # tracks beside the line, lead walker framed (head probe r2)
# ---- S08 (654-765): on deck, the sailors gripe; lips move on the quoted line ----
s='S08'; r=S(s)
s8a=onship(char_on('S08_sailA','sailorA',s,(SX-1.2,2.0,2.32),r,'deadpan')); s8b=onship(char_on('S08_sailB','sailorB',s,(SX+0.9,2.6,2.32),r,'grit'))
faces(s8a,[(654,'deadpan'),(676,'grit'),(694,'deadpan')]); lipsync(s8a,WORDS[75:85],700,766)
faces(s8b,[(654,'grit'),(700,'sneaky'),(730,'grin'),(752,'deadpan')])
for f,a in [(654,-20),(700,-140),(712,-110),(730,-150),(750,-60)]: arm(s8a,1,f,a)
for f,a in [(654,-30),(705,-60),(740,-100)]: arm(s8b,-1,f,a)
bob(s8a,[703,732,756]); bob(s8b,[716,744])
p8=onship(char_on('S08_pil','pilgrimB',s,(SX+0.3,0.6,2.32),r,'worry')); faces(p8,[(654,'worry'),(712,'shock'),(740,'worry')])
path(s,[(654,(SX-1.8,4.7,3.0),(SX-0.2,2.0,2.75)),(700,(SX-1.6,4.4,2.95),(SX-0.4,2.0,2.8)),(765,(SX-1.3,4.0,2.9),(SX-0.5,2.0,2.8))])
# ---- S09 (766-1012): the packed long take on Corn Hill: climb, dig, the corn basket, take it, give it back, the name ----
s='S09'; r=S(s); hz=lambda x,y:dune(x,y)
cA=char_on('S09_dig','pilgrimC',s,(DX-0.9,11.0,hz(DX-0.9,11.0)),r,'neutral',arms=('arm',[(766,'arm_shovel'),(822,'arm')]),walker=True)
gwalk(cA,766,796,(DX-4.5,8.0,hz(DX-4.5,8.0)),(DX-0.9,11.0,hz(DX-0.9,11.0)),hz,step=4)
for f,a in [(800,-60),(804,-20),(808,-60),(812,-20),(822,-150),(832,-140),(846,-155)]: arm(cA,1,f,a)
faces(cA,[(766,'neutral'),(800,'grit'),(816,'shock'),(824,'excited'),(850,'grin'),(880,'sneaky'),(900,'happy'),(930,'worry'),(960,'happy'),(990,'proud')])
cB=char_on('S09_carry','pilgrimA',s,(DX+0.6,10.7,hz(DX+0.6,10.7)),r,'neutral',arms=('arm',[(766,'arm_musket'),(899,'arm_basket'),(936,'arm')]),walker=True)
gwalk(cB,766,800,(DX-3.0,7.0,hz(DX-3.0,7.0)),(DX+0.6,10.7,hz(DX+0.6,10.7)),hz,step=4)
faces(cB,[(766,'neutral'),(816,'excited'),(836,'grin'),(870,'proud'),(899,'sneaky'),(918,'worry'),(940,'happy'),(970,'grin')])
for f,a in [(899,-20),(905,-25)]: arm(cB,1,f,a)
gwalk(cB,903,918,(DX+0.6,10.7,hz(DX+0.6,10.7)),(DX+2.3,10.0,hz(DX+2.3,10.0)),hz,step=3)
cC=char_on('S09_look','pilgrimB',s,(DX-2.6,8.0,hz(DX-2.6,8.0)),r,'worry')
faces(cC,[(766,'worry'),(830,'shock'),(846,'worry'),(870,'deadpan'),(900,'shock'),(930,'neutral'),(980,'proud')])
bob(cC,[830,900,980])
# basket follows the carrier's hand from the lift (899) until the hand-back (936), then sits in the Wampanoag man's arms
for f,z in [(898,bz+0.05),(899,bz+0.15)]: kloc(bsk,f,(DX,12,z))
vis(bsk,[(766,898)])
wp=char_on('S09_wamp','nausetC',s,(DX+3.6,9.4,hz(DX+3.6,9.4)),(918,1012),'neutral',arms=('arm',[(918,'arm'),(936,'arm_basket')]),walker=True)
gwalk(wp,918,932,(DX+6.0,8.6,hz(DX+6.0,8.6)),(DX+3.6,9.4,hz(DX+3.6,9.4)),hz,step=3)
faces(wp,[(918,'neutral'),(936,'happy'),(950,'proud'),(975,'grin')])
for f,a in [(936,-25),(950,-20)]: arm(wp,-1,f,a)
bob(wp,[938,966])
B=bz; path(s,[(766,(DX-6.5,3.0,B+0.4),(DX-3.0,9.0,B+0.2)),(800,(DX-3.6,7.0,B+1.6),(DX-0.6,11.2,B+1.0)),(822,(DX-2.4,8.6,B+1.5),(DX-0.2,11.6,B+0.7)),(862,(DX-1.6,8.4,B+1.6),(DX+0.3,11.2,B+0.9)),(899,(DX-0.6,8.0,B+1.6),(DX+1.0,10.8,B+1.0)),(936,(DX+0.8,7.0,B+1.4),(DX+2.6,9.8,B+0.9)),(972,(DX+1.6,7.2,B+1.4),(DX+3.0,10.0,B+1.1)),(1012,(DX+1.2,6.9,B+1.75),(DX+3.2,10.5,B+1.5))])
# ---- S10 (1005-1140): dawn camp behind the barricade, Nauset men at the tree line; push to one of them watching an English ship on the horizon ----
s='S10'; r=S(s)
for i,(x,y,k) in enumerate([(-1.4,2.4,'pilgrimA'),(1.3,2.0,'pilgrimB'),(2.2,2.6,'pilgrimC'),(-0.2,3.8,'pilgrimD')]):
    c_=char_on(f'S10_p{i}',k,s,(EX+x,y,eb(EX+x,y)),r,'blink' if i<2 else 'neutral'); faces(c_,[(1005,'blink'),(1030+i*8,'neutral'),(1080+i*5,'worry')]); bob(c_,[1040+i*9])
N=[]
for i,(x,y,k) in enumerate([(-3.0,-18,'nausetA'),(0.5,-19.5,'nausetB'),(3.9,-18.6,'nausetC')]):
    c_=char_on(f'S10_n{i}',k,s,(EX+x,y,eb(EX+x,y)),r,'neutral',arms=('arm','arm_bow')); N.append(c_)
    faces(c_,[(1005,'neutral'),(1060+i*6,'deadpan'),(1100+i*4,'worry')]); bob(c_,[1050+i*12])
for f,a in [(1066,-30),(1100,-20)]: arm(N[1],1,f,a)
path(s,[(1005,(EX+0.5,-4.0,1.9),(EX+0.4,-18,1.35)),(1050,(EX+0.5,-11.0,1.8),(EX+0.4,-19,1.5)),   # stills r3: the push now starts on the beach, not over the empty camp
       (1100,(EX+1.2,-15.2,1.55),(EX+0.5,-19.5,1.65))])
# rotate the last framing to show the Nauset man in profile looking to sea, with the English ship on the horizon
path(s,[(1110,(EX-1.2,-21.6,1.7),(EX+0.5,-19.5,1.7)),(1140,(EX-1.5,-22.2,1.75),(EX+0.6,-19.4,1.75))])
# ---- S11 (1141-1252): arrows thud into the barricade; the Pilgrims fire back (smoke); no one is hurt ----
s='S11'; r=S(s)
P11=[]
for i,(x,y,k) in enumerate([(-1.6,1.6,'pilgrimA'),(0.2,1.2,'pilgrimB'),(1.8,1.6,'pilgrimC')]):
    c_=char_on(f'S11_p{i}',k,s,(EX+x,y,eb(EX+x,y)),r,'neutral',arms=('arm','arm_musket')); P11.append(c_)
    faces(c_,[(1141,'worry'),(1158+i*2,'shock'),(1176,'grit'),(1198+i*3,'grit'),(1222,'worry'),(1236+i*2,'happy'),(1246,'grin')])
    for f,a in [(1141,-20),(1186,-70),(1194,-85),(1226,-20)]: arm(c_,1,f+i*2,a)
    bob(c_,[1160+i*2,1230+i*3])
path(s,[(1141,(EX+0.4,4.6,1.75),(EX,0.8,1.15)),(1180,(EX+0.2,4.2,1.7),(EX,0.8,1.2)),(1252,(EX-0.4,3.9,1.65),(EX,1.0,1.2))])
# ---- S12 (1244-1330): today's sign, First Encounter Beach; pull-out reveal over the dune grass ----
s='S12'; r=S(s)
path(s,[(1244,(EX+14.2,-9.6,1.65),(EX+14,-12,1.6)),(1330,(EX+15.8,-5.0,2.6),(EX+14,-12,1.4))])
# ---- S13 (1322-1412): the shallop crosses the bay to Plymouth ----
s='S13'; r=S(s)
for i,(y,k) in enumerate([(-2.0,'pilgrimA'),(0.0,'pilgrimB'),(-1.0,'sailorA')]):
    c_=char_on(f'S13_r{i}',k,s,(SX+70,40+y,0.5),r,'neutral',arms=('arm_oar','arm')); drift_faces(c_,1322,1412,['neutral','grit','happy','proud'],40+i,(14,26))
    c_['root'].parent=SHAL; c_['root'].location=(0.0,y,0.6)   # seated in the shallop, hull hides the legs
    for f in range(1322,1412,14): arm(c_,1,f,-40); arm(c_,1,f+7,-75)
path(s,[(1322,(SX+66,33.5,2.2),(SX+70,40,1.2)),(1412,(SX+74,27.0,2.3),(SX+81,40,1.3))])
# ---- S14 (1413-1443): "And the famous rock?" crash push on today's rock ----
s='S14'; r=S(s)
path(s,[(1413,(0.0,-4.5,1.4),(0,3.8,0.5)),(1424,(0.0,-1.6,1.1),(0,3.6,0.45)),(1443,(0.05,-1.3,1.05),(0,3.6,0.45))])
L.CAM[s].data.lens=36
# ---- S15 (1436-1516): the journal by candle; the camera runs across the pages: corn, arrows, Plymouth, no rock ----
s='S15'; r=S(s)
wr=char_on('S15_writer','pilgrimD',s,(IX-3.4,3.35,0.0),r,'neutral',arms=('arm',[(1436,'arm_quill')]))
for f,a in [(1436,-50),(1450,-58),(1466,-46),(1480,-56),(1496,-44)]: arm(wr,1,f,a)
faces(wr,[(1436,'neutral'),(1460,'deadpan'),(1486,'proud'),(1504,'deadpan')])
path(s,[(1436,(IX-4.1,1.6,1.45),(IX-3.6,2.55,0.8)),(1480,(IX-3.4,1.65,1.35),(IX-3.2,2.55,0.79)),(1516,(IX-2.9,1.8,1.4),(IX-3.0,2.6,0.85))])
# ---- S16 (1509-1574): 1741, a wharf going up beside the rock; hammers ----
s='S16'; r=S(s)
for i,(x,y,k) in enumerate([(3.8,2.6,'townA'),(6.0,2.4,'townB'),(-2.4,0.4,'townA')]):
    c_=char_on(f'S16_w{i}',k,s,(x,y,0.15),r,'grit',arms=('arm','arm_shovel'))
    for f in range(1509,1574,10): arm(c_,1,f+i*3,-120); arm(c_,1,f+i*3+5,-40)
    drift_faces(c_,1509,1574,['grit','neutral','happy'],50+i,(14,24)); bob(c_,[1520+i*6,1550])
path(s,[(1509,(4.2,-3.0,1.9),(4.6,2.6,1.2)),(1574,(3.2,-2.0,1.8),(4.0,2.6,1.2))])
# ---- S17 (1567-1712): the 94-year-old elder arrives, points at the gray stone; the town gasps; "That's the one." ----
s='S17'; r=S(s)
el=char_on('S17_elder','elder',s,(-1.8,0.6,0.1),r,'deadpan',arms=('arm_cane','arm'),walker=True)
gwalk(el,1567,1612,(-4.6,-0.6,rb(-4.6,-0.6)),(-1.8,0.6,rb(-1.8,0.6)),rb,step=5)
for f,a in [(1612,-30),(1624,-95),(1640,-100),(1700,-90)]: arm(el,-1,f,a)
faces(el,[(1567,'deadpan'),(1600,'proud'),(1624,'excited'),(1660,'proud')]); lipsync(el,WORDS[194:197],1686,1712)
T17=[]
for i,(x,y,k) in enumerate([(2.6,1.0,'townA'),(3.4,-0.4,'townB'),(1.2,-1.4,'townA')]):
    c_=char_on(f'S17_t{i}',k,s,(x,y,0.12),r,'neutral'); T17.append(c_)
    faces(c_,[(1567,'neutral'),(1600,'deadpan'),(1626+i*2,'shock'),(1640,'excited'),(1676,'worry'),(1700+i,'shock')])
    bob(c_,[1628+i*2,1700]); arm(c_,1,1628,-150-10*i); arm(c_,1,1650,-30)
path(s,[(1567,(-5.0,-4.4,1.6),(-3.6,0.0,1.4)),(1612,(-3.4,-3.2,1.6),(-1.6,0.8,1.35)),(1640,(-1.6,-3.2,1.6),(-0.4,1.8,1.2)),(1686,(-1.0,-1.8,1.5),(-1.7,0.7,1.4)),(1712,(-1.1,-1.5,1.48),(-1.75,0.7,1.42))])
# ---- S18 (1702-1758): today: the rock with 1620 carved, tourists, the posing Pilgrim again; slow pull-out ----
s='S18'; r=S(s)
p18=char_on('S18_pil','pilgrimA',s,(-0.2,4.1,0.88),r,'proud'); faces(p18,[(1702,'proud'),(1726,'grin'),(1746,'proud')])
for f,a in [(1702,-150),(1730,-158)]: arm(p18,1,f,a)
q1=char_on('S18_tourA','tourA',s,(-2.4,0.4,0.08),r,'happy',arms=('arm','arm_phone')); q2=char_on('S18_tourB','tourB',s,(2.1,0.0,0.06),r,'excited',arms=('arm_phone','arm'))
arm(q1,1,1702,-122); arm(q2,-1,1702,122); drift_faces(q1,1702,1758,['happy','grin'],60); drift_faces(q2,1702,1758,['excited','happy'],61)
path(s,[(1702,(0.1,1.3,1.75),(-0.2,4.1,1.9)),(1758,(0.0,-1.0,1.6),(-0.1,4.0,1.5))])
# ---- S19 (1759-1816): payoff, the dune-top print shop; push lands on the poster on "first" (1793) ----
s='S19'; r=S(s)
g1=char_on('S19_a','tourA',s,(HX-2.0,HY-1.6,gd(HX-2.0,HY-1.6)),r,'happy'); g2=char_on('S19_b','tourB',s,(HX+2.0,HY-1.7,gd(HX+2.0,HY-1.7)),r,'excited')
faces(g1,[(1759,'happy'),(1780,'excited'),(1798,'grin')]); faces(g2,[(1759,'excited'),(1784,'happy'),(1800,'grin')])
arm(g1,1,1782,-120); arm(g2,-1,1786,110)
path(s,[(1759,(HX+0.4,HY-7.5,1.75),(HX,PY,1.45)),(1793,(HX+0.05,HY-2.25,1.575),(HX,PY,PZ-0.165)),(1816,(HX+0.03,HY-2.05,1.565),(HX,PY,PZ-0.165))])   # r2 (rule T7): poster sits above the caption band (bottom >= 34 % H from the frame bottom)
# ---- ground snap (footprobe r1: tourists sank 0.11 m into the beach mesh; analytic dune heights differ from the grid by up to 0.06 m) ----
CHRN=set()
TERRAIN=('R_beach','R_wet','D_dunes','E_beach','E_sand','G_dunes','I_floor')
def _ground(x,y,f,z0,terrain=False):
    sc.frame_set(f); dg=bpy.context.evaluated_depsgraph_get(); o_=Vector((x,y,z0+1.2))   # from just above the root: a ray from the sky hit the cabin ceiling (r2)
    for k in range(40):
        ok,loc,nrm,i,ob,m=sc.ray_cast(dg,o_,Vector((0,0,-1)))
        if not ok: return None
        o_=loc+Vector((0,0,-0.001))
        if terrain and not ob.name.startswith(TERRAIN): continue
        if ob.name in CHRN or ob.name.endswith('_ink') or ob.get('fly') or ob.hide_render or (ob.get('noink') and len(ob.data.vertices)<=4): continue
        return loc.z
    return None
def snap_all():
    global CHRN
    CHRN=set(o.name for c in bpy.data.collections if c.name.startswith('CHR_') for o in c.all_objects)
    n=0
    for ch in ALL:
        r=ch['root']
        if r.parent: continue
        fcz=None
        if r.animation_data and r.animation_data.action:
            fcz=next((fc for fc in r.animation_data.action.fcurves if fc.data_path=='location' and fc.array_index==2),None)
        if fcz is None:
            g=_ground(r.location.x,r.location.y,ch['rng'][0],r.location.z)
            if g is not None: r.location.z=g; n+=1
            continue
        fx=[fc for fc in r.animation_data.action.fcurves if fc.data_path=='location' and fc.array_index in (0,1)]
        for kp in fcz.keyframe_points:
            f=kp.co[0]; x=fx[0].evaluate(f); y=fx[1].evaluate(f); g=_ground(x,y,int(f),kp.co[1])
            if g is not None: kp.co[1]=g; kp.handle_left[1]=g; kp.handle_right[1]=g; n+=1
    print('SNAPPED',n)
snap_all()
# ---- rule 309 pass (head probe r1: S05 14%, S07 18%, S16 12%, S18 18% of W): dolly cameras in toward their targets ----
for n,k,fr in [('S01',0.7,(0,92)),('S09',0.75,None),('S11',0.75,None),
               ('S13',0.9,None),('S16',0.45,None),('S17',0.65,(1567,1640)),('S18',0.6,None)]: dolly(n,k,fr)
# ======================= foreground layers (rule 311): one near object per shot over 60 f, low in a corner, never over a face or the poster =======================
def campos(n,f):
    def ev(o):
        return Vector([next(fc for fc in o.animation_data.action.fcurves if fc.data_path=='location' and fc.array_index==i).evaluate(f) for i in range(3)])
    return ev(L.CAM[n]),ev(L.TGT[n])
def fgobj(n,kind,side=1,dist=1.5,drop=0.75,f=None,lat=0.55):
    f0=SH[n][0] if f is None else f; c_,t_=campos(n,f0); d_=(t_-c_).normalized(); rt=Vector((d_.y,-d_.x,0)).normalized()
    p=c_+d_*dist+rt*lat*side*dist; p.z=c_.z-drop*dist
    global CHRN
    g=_ground(p.x,p.y,f0,c_.z-1.0,terrain=True) if kind!='rail' else None
    if g is not None: p.z=g+{'grass':0.02,'post':0.2,'barrel':0.2,'log':-0.06}[kind]   # check_scene r2: FG props floated
    co=C(n)
    if kind=='grass':
        for k in range(2): g=plane(f'{n}_fg{k}',(p.x,p.y,p.z+0.45),0.95,0.95,card_mat('grass1','grass1',emit=0.15),coll=co); g.rotation_euler=(0,0,math.radians(30+k*90)); g['noink']=1
    elif kind=='post': cyl(f'{n}_fgpost',(p.x,p.y,p.z+0.6),0.07,1.6,surf('wharfm','wharf',(1,1)),v=10,coll=co)
    elif kind=='rail':
        box(f'{n}_fgrail',(p.x,p.y,p.z+0.35),(0.14,1.6,0.14),surf('hull','hull',(3,3)),coll=co,bv=0.01).rotation_euler=(0,0,math.atan2(d_.y,d_.x))
        cyl(f'{n}_fgbal',(p.x,p.y,p.z),0.05,0.7,surf('hull','hull',(3,3)),v=6,coll=co)
    elif kind=='barrel': cyl(f'{n}_fgbarrel',(p.x,p.y,p.z+0.2),0.36,0.8,surf('barrelm','barricade',(1,1)),v=16,coll=co)
    elif kind=='log': cyl(f'{n}_fglog',(p.x,p.y,p.z+0.2),0.18,2.0,surf('barrm','barricade',(1.5,1.5)),v=10,coll=co,rot=(0,math.radians(90),math.atan2(d_.y,d_.x)+0.6))
for n,k,sd,dr in [('S01','grass',-1,0.62),('S05','rail',1,0.7),('S06','barrel',-1,0.62),('S07','grass',-1,0.75),('S08','rail',-1,0.55),('S09','grass',-1,0.55),
                  ('S10','log',-1,0.6),('S11','log',1,0.62),('S12','grass',-1,0.55),('S15','barrel',1,0.6),('S16','post',1,0.5),('S18','grass',1,0.55),('S19','grass',-1,0.55),('S03','barrel',-1,0.6)]:
    fgobj(n,k,sd,1.5,dr)
fgobj('S17','grass',1,1.4,0.7,f=1686,lat=0.8)   # r2: placed from the end framing (camera travels far in S17)
# ======================= world, finish, ink, render settings =======================
def world_and_sun():
    w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; bg=w.node_tree.nodes['Background']; bg.inputs['Color'].default_value=(*lin((160,196,226)),1); bg.inputs['Strength'].default_value=1.0
    bpy.ops.object.light_add(type='SUN',rotation=(math.radians(52),0,math.radians(40)))   # preview r1: sun moved from behind the subjects (3D props read near-black) to camera-right; sun=bpy.context.object; sun.name='sun'; sun.data.energy=4.6; sun.data.color=(1.0,0.93,0.82); sun.data.angle=math.radians(3)
world_and_sun()
for a in ALL: finish(a)
print('hulls',L.ink())
for o_ in bpy.data.objects:
    if o_.type=='LIGHT' and o_.data.type!='SUN': o_.visible_camera=False   # r2: S19 area light read as a white band across the poster
L.render_setup(100,8)
sc.cycles.samples=4; sc.cycles.transparent_max_bounces=8; sc.cycles.diffuse_bounces=1; sc.cycles.max_bounces=3   # r1 speed test: 89 s -> 53 s per 2K frame, mean abs diff 1.4/255
os.makedirs('/root/cc/blend',exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath='/root/cc/blend/cc.blend'); print('SCENE_OK all')
