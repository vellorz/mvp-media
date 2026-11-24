# Nuremberg Christkindlesmarkt short (fri-nuremberg): Blender builder.   blender -b --python scene_nb.py   -> /root/nb/blend/cc.blend
# Built on the Cape Cod cc pipeline (lib.py rig, ink hulls, cast cards, render setup, owner-approved r6d); every set, prop and shot here is new.
# Story: the bentwood box (Spanschachtel) "zum Kindles marck ... 16?8"; the city archive's cemetery records date it 1678, not 1628.
import sys, os, math, random, json
sys.path.insert(0,'/root/nb/src')
import bpy, bmesh
from mathutils import Vector, Euler, Matrix
import lib as L
from lib import combo,box,cyl,sph,plane,flat,surf,card_mat,lin,vis,kloc,krot,kscale,empty,cam,char,face,faces,arm,bob,walk,finish,lipsync,turn,look
END=1905
sc=L.init(END); R=random.Random(11)
_W=json.load(open('/root/nb/vo/vo_trim.wav.words.json'))
WORDS=[(w['w'],w['s'],w['e']) for w in _W]   # lipsync takes (word, start, end); +0.1 s VO delay is added inside lipsync (mix adelay=100)
def WF(i): return int(round((_W[i]['s']+0.1)*30))   # frame a word starts on screen
# shot table: touching ranges are hard cuts; overlaps are dissolves (none: Rick cuts)
SH={'S01':(0,130),'S02':(130,193),'S03':(193,332),'S04':(332,505),'S05':(505,668),'S06':(668,725),'S07':(725,815),'S08':(815,935),
    'S09':(935,1062),'S10':(1062,1158),'S11':(1158,1246),'S12':(1246,1334),'S13':(1334,1404),'S14':(1404,1520),'S15':(1520,1588),
    'S16':(1588,1676),'S17':(1676,1800),'S18':(1800,END)}
sc['shots']=json.dumps(SH)
LENS={'S01':30,'S02':40,'S03':34,'S04':30,'S05':40,'S06':40,'S07':32,'S08':28,'S09':32,'S10':30,'S11':40,'S12':32,'S13':32,'S14':32,'S15':40,'S16':30,'S17':30,'S18':34}
for n in SH: cam(n,LENS[n],11.0)
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
    HULL=surf('hull','hull',(3,3),emit=0.35); DECK=surf('deckm','deck',(3,3)); SAIL=surf('sailm','sail',(6,6),gen=True)   # r3 (visual verifier: hull a near-black mass, 5.3 % of the frame at f324)
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
    # r2: camera-only cap over the open top (the world colour showed as a grey band at the top of S01/S02/S04); invisible to light rays so the world still lights the set
    cb=bmesh.new(); cv=[cb.verts.new((c[0]+rad*math.cos(2*math.pi*i/seg),c[1]+rad*math.sin(2*math.pi*i/seg),z0+h-0.5)) for i in range(seg)]; cb.faces.new(cv)
    cm=bpy.data.meshes.new(n+'_cap'); cb.to_mesh(cm); cb.free(); cu=cm.uv_layers.new()
    for li in range(len(cu.data)): cu.data[li].uv=(0.5,0.985)
    co_=bpy.data.objects.new(n+'_cap',cm); L.C_NOI.objects.link(co_); cm.materials.append(m); co_['fly']=1; co_['noink']=1
    co_.visible_diffuse=False; co_.visible_glossy=False; co_.visible_transmission=False; co_.visible_volume_scatter=False; co_.visible_shadow=False
    return o
def skycard(n,loc,face_,w,h,img,coll=None):
    s_=plane(n,loc,w,h,card_mat(img,img,emit=1.0),coll=coll or L.C_NOI,face=face_); s_['fly']=1; s_['noink']=1; return s_
# ======================= shared nb helpers =======================
WOOD=surf('woodm','wood',(1.5,1.5)); TABLE=surf('tablem','table',(1.5,1.5)); DARK=flat('darkwood',lin((84,56,40)),0.8)
GOLD=flat('gold',lin((226,180,70)),0.35,metal=0.4); WHITE=flat('whitepaint',lin((240,236,228)),0.8)
def floor(n,cx,cy,w,d,img,tile,coll=None):
    o=box(n,(cx,cy,-0.05),(w,d,0.1),surf(n+'m',img,tile),coll=coll,bv=0); o['ground']=1; return o
def wall(n,c,s,img,tile,coll=None): return box(n,c,s,surf(n+'m',img,tile),coll=coll,bv=0)
def card(n,c,w,h,img,face_='-Y',emit=0.15,coll=None,noink=True,rot=None):
    o=plane(n,c,w,h,card_mat(img,img,emit=emit),coll=coll,face=face_)
    if noink: o['noink']=1
    if rot: o.rotation_euler=rot
    return o
def snowfall(n,cx,cy,w,d,h,count,seed,z0=0.0,speed=0.55,avoid=()):
    """falling snow on ones: small white spheres fall at ~0.55 m/s and wrap to the top (rule 379 environment detail; Rick weather FX)"""
    rr=random.Random(seed); m=flat('snowflake',lin((250,250,255)),0.6,emit=1.2); P=int(h/speed*30)
    for i in range(count):
        x=cx+rr.uniform(-w/2,w/2); y=cy+rr.uniform(-d/2,d/2); ph=rr.randint(0,P); r_=rr.uniform(0.012,0.024)
        if any(abs(x-ax)<aw and abs(y-ay)<ad for ax,ay,aw,ad in avoid): continue   # rule 372: no flake falls through a roof or a building
        o=sph(f'{n}{i}',(x,y,z0+h),r_,m,seg=6); o['noink']=1; o.visible_shadow=False
        f=-ph
        while f<END+P:
            a=max(f,0); b=min(f+P-1,END)
            if a<=b:
                za=z0+h-(a-f)/P*h; zb=z0+h-(b-f)/P*h; dx=0.15*math.sin(i)
                kloc(o,a,(x,y,za)); kloc(o,b,(x+dx,y,zb))
            f+=P
        for fc in o.animation_data.action.fcurves:
            for k_ in fc.keyframe_points: k_.interpolation='LINEAR'
def steam(n,loc,f0,f1,coll):
    for k,f in enumerate(range(f0,f1,16)): fx(f'{n}{k}','fx_steam',(loc[0]+0.04*(k%2),loc[1],loc[2]),f,22,0.35,coll,grow=1.5,rise=0.35)
def stall(n,c,yaw,front,roof='stall_roof',w=2.6,d=1.3,coll=None,lit=True):
    """market stall: counter, four posts, red/white pitched roof, painted name board; planted on the cobbles (rule 376)"""
    e=empty(n,c,coll=coll); e.rotation_euler=(0,0,yaw); parts=[]
    parts.append(box(n+'_ctr',(0,0,0.5),(w,d*0.55,1.0),WOOD,coll=coll,bv=0.02))
    parts.append(box(n+'_top',(0,-0.02,1.03),(w+0.1,d*0.6,0.06),DARK,coll=coll,bv=0.01))
    for sx in(-1,1):
        for sy in(-1,1): parts.append(cyl(f'{n}_p{sx}{sy}',(sx*(w/2-0.06),sy*(d/2-0.06),1.3),0.05,2.6,DARK,v=8,coll=coll))
    RM=surf(roof+'m',roof,(1,1))
    for sy in(-1,1):
        o=plane(f'{n}_roof{sy}',(0,sy*d*0.27,2.72),w+0.4,d*0.62,RM,coll=coll,horiz=True); o.rotation_euler=(sy*math.radians(-24),0,0); parts.append(o)
    parts.append(card(f'{n}_sign',(0,-d/2-0.02,2.27),w-0.04,w*0.25,front,coll=coll,emit=0.25))
    parts.append(box(n+'_back',(0,d/2-0.05,1.6),(w,0.06,1.2),WOOD,coll=coll,bv=0))
    if lit:
        for i in range(6): parts.append(sph(f'{n}_bulb{i}',(-w/2+0.15+i*(w-0.3)/5,-d/2-0.05,2.45),0.035,BULB,coll=coll))
    for p in parts: p.parent=e
    return e
BULB=flat('bulb',lin((255,226,150)),0.4,emit=5.0)
def house(n,c,face_,img,w=7.0):
    """half-timbered gable house card, bottom on the ground (texture 1024x1536, alpha gable)"""
    h=w*1.5; o=card(n,(c[0],c[1],h/2-0.02),w,h,img,face_=face_,emit=0.35,coll=L.C_NOI); o['fly']=1; return o
def lights(n,p0,p1,count,sag=0.35,coll=None):
    for i in range(count):
        t=i/(count-1); x=p0[0]+(p1[0]-p0[0])*t; y=p0[1]+(p1[1]-p0[1])*t; z=p0[2]+(p1[2]-p0[2])*t-sag*4*t*(1-t)
        sph(f'{n}{i}',(x,y,z),0.05,BULB,coll=coll)
    for i in range(count-1):   # the wire the bulbs hang on (contactcheck r1: bulbs floated with no cable)
        a=[p0[k]+(p1[k]-p0[k])*i/(count-1) for k in range(3)]; b=[p0[k]+(p1[k]-p0[k])*(i+1)/(count-1) for k in range(3)]
        ta,tb=i/(count-1),(i+1)/(count-1); a[2]+=0.05-sag*4*ta*(1-ta); b[2]+=0.05-sag*4*tb*(1-tb)
        d_=Vector(b)-Vector(a); o=cyl(f'{n}w{i}',tuple((Vector(a)+Vector(b))/2),0.008,d_.length+0.01,INK,v=6,coll=coll); o.rotation_euler=d_.to_track_quat('Z','Y').to_euler()
def strand(n,p0,p1,count,sag,coll=None,mat=None,r=0.012):
    """a sagging string drawn as short cylinders (the banner's 'one wiggly line')"""
    pts=[]
    for i in range(count+1):
        t=i/count; pts.append(Vector((p0[0]+(p1[0]-p0[0])*t,p0[1]+(p1[1]-p0[1])*t,p0[2]+(p1[2]-p0[2])*t-sag*4*t*(1-t)+0.03*math.sin(t*19))))
    out=[]
    for i,(a,b) in enumerate(zip(pts,pts[1:])):
        d_=b-a; mid=(a+b)/2; o=cyl(f'{n}{i}',tuple(mid),r,d_.length,mat or INK,v=6,coll=coll)
        o.rotation_euler=d_.to_track_quat('Z','Y').to_euler(); out.append(o)
    return out,pts
# ======================= SET M: the Hauptmarkt at dusk, snow (x=0): S01, S17, S18 =======================
floor('M_cobble',0,4,70,60,'cobble',(10,10))
skydome('M_sky',(0,4),170,130,'sky_dusk')
CH=surf('churchm','church',(2.5,2.5)); SST=surf('sandstm','sandstone',(2,2))
CY=20.0   # church front face
CH=surf('churchfacm','sandstone',(0.9,0.9))   # eyepass r1: finer stone grain up close. run lead r1 (S17): the church_stone strokes read as scratches up close; the facade uses the sandstone paint
box('M_church',(0,CY+4,8),(13,8,16),CH,bv=0.04)
gb=bmesh.new(); gv=[gb.verts.new(p) for p in [(-6.5,0,0),(6.5,0,0),(0,0,7.5),(-6.5,8,0),(6.5,8,0),(0,8,7.5)]]
for f_ in [(0,1,2),(3,5,4),(0,3,4,1)[::-1],(0,2,5,3),(1,4,5,2)]: gb.faces.new([gv[i] for i in f_])
me=bpy.data.meshes.new('M_gable'); gb.to_mesh(me); gb.free(); go=bpy.data.objects.new('M_gable',me); L.C_SET.objects.link(go); me.materials.append(CH); go.location=(0,CY,16)
for i in range(7): box(f'M_pin{i}',(-5.4+i*1.8,CY-0.15,16.2+3.4*(1-abs(i-3)/3.5)),(0.3,0.3,1.4),SST,bv=0.03)   # little gothic pinnacles along the gable (our own design)
for k,(x,z,w_,h_) in enumerate([(-4.2,9.5,1.4,4.0),(4.2,9.5,1.4,4.0),(0,11.6,2.0,3.2),(-4.2,2.4,1.4,3.0),(4.2,2.4,1.4,3.0)]):
    box(f'M_win{k}',(x,CY-0.02,z),(w_,0.1,h_),flat('winglass',lin((70,64,96)),0.4,emit=0.6),bv=0.02)
    pb=bmesh.new(); pv=[pb.verts.new(p) for p in [(-w_/2,0,0),(w_/2,0,0),(0,0,w_*0.7)]]; pb.faces.new(pv); pm=bpy.data.meshes.new(f'M_arch{k}'); pb.to_mesh(pm); pb.free()
    po=bpy.data.objects.new(f'M_arch{k}',pm); L.C_SET.objects.link(po); pm.materials.append(bpy.data.materials['winglass']); po.location=(x,CY-0.03,z+h_/2)
box('M_door',(0,CY-0.02,1.6),(2.2,0.12,3.2),DARK,bv=0.02)
BZ=4.6   # balcony floor (the Christkind's gallery above the doors)
box('M_balc',(0,CY-0.75,BZ-0.1),(4.2,1.5,0.2),SST,bv=0.03)
box('M_balcdoorf',(0,CY-0.01,BZ+1.15),(1.6,0.08,2.4),DARK,bv=0.02)
card('M_balcdoor',(0,CY-0.06,BZ+1.1),1.4,2.2,'balcdoor',emit=0.8)   # run lead r1: painted open doorway (was a plain cream panel)
for i in range(11): cyl(f'M_bal{i}',(-2.0+i*0.4,CY-1.45,BZ+0.35),0.04,0.7,SST,v=8)
box('M_rail',(0,CY-1.45,BZ+0.72),(4.2,0.12,0.08),SST,bv=0.02)
for sx in(-1,1): box(f'M_corb{sx}',(sx*1.8,CY-0.8,BZ-0.55),(0.3,1.2,0.7),SST,bv=0.03)
banner350_hang=card('M_banner350',(0,CY-1.505,BZ-0.42),2.6,0.53,'banner350',emit=0.35,coll=None)
vis(banner350_hang,[(1588,END)])
for i,(x,y,img) in enumerate([(-13,14,'house0'),(-13,6,'house1'),(-13,-2,'house2'),(13,15,'house3'),(13,7,'house4'),(13,-1,'house1'),(-9,24,'house2'),(9,24,'house0')]):
    house(f'M_house{i}',(x,y),'+X' if x<0 else '-X',img) if abs(x)>10 else house(f'M_house{i}',(x,y),'-Y',img,w=6.0)
for i,(x,y) in enumerate([(-13,-10),(13,-9),(-6,-14),(6,-14)]): house(f'M_houseB{i}',(x,y),'+Y' if abs(x)<10 else ('+X' if x<0 else '-X'),f'house{i}')
STALLS=[('lebk',(-5.5,9.0),0.0),('glueh',(5.5,9.0),0.0),('stars',(-6.8,3.0),math.radians(80)),('prints',(4.8,1.0),0.0)]
for nm,(x,y),yaw in STALLS: stall(f'M_st_{nm}',(x,y,0),yaw,f'stall_{nm}',roof=('stall_roof_g' if nm in('stars',) else 'stall_roof'))
lights('M_lt0',(-9,12,4.2),(9,12,4.2),24,0.6); lights('M_lt1',(-9,4,4.0),(9,4,4.0),24,0.6)
for sx in(-1,1):
    for y in(4,12): cyl(f'M_ltpost{sx}{y}',(sx*9,y,2.1),0.08,4.2,DARK,v=8)
# the 400th banner over the market (S01 only; the 350th hangs on the balcony from S16 on)
b400=card('M_banner400',(0,12.0,2.9),5.4,1.1,'banner400',emit=0.35,coll=C('S01'))
for sx in(-1,1): cyl(f'M_b400c{sx}',(sx*2.6,12.0,3.555),0.012,0.21,INK,v=6,coll=C('S01'))   # tied up to the light string
snowfall('M_snow',0,6,20,22,7,360,3,avoid=[(x,y,1.9,1.9) for _,(x,y),_ in STALLS]+[(0,24,7,4.5)])
# payoff: the prints stall front, easel with the Nuremberg poster (pasted at true colour in post)
PX,PY0=4.8,1.0
PW,PH=0.80,1.20; PZ=1.75; PY=0.2
box('poster_frame',(PX-0.9,PY+0.03,PZ),(PW+0.12,0.04,PH+0.12),flat('pframe',lin((246,236,214)),0.35,emit=0.9),bv=0.01)
pmat=bpy.data.materials.new('poster'); N_,L_=L.nodes(pmat); pp_=N_['Principled BSDF']; it_=N_.new('ShaderNodeTexImage'); it_.image=bpy.data.images.load('/root/nb/poster_2k.png'); it_.interpolation='Cubic'
L_.new(it_.outputs['Color'],pp_.inputs['Base Color']); L_.new(it_.outputs['Color'],pp_.inputs['Emission Color']); pp_.inputs['Emission Strength'].default_value=0.15; pp_.inputs['Roughness'].default_value=1.0; pp_.inputs['Specular IOR Level'].default_value=0.0
poster=plane('poster',(PX-0.9,PY,PZ),PW,PH,pmat,coll=L.C_NOI); poster['noink']=1
for sx in(-1,1): cyl(f'M_easel{sx}',(PX-0.9+sx*0.36,PY+0.12,0.62),0.025,1.26,flat('easel',lin((120,86,54))),v=6,rot=(math.radians(-8),math.radians(sx*-10),0))
cyl('M_easelb',(PX-0.9,PY+0.3,0.62),0.025,1.26,flat('easel',lin((120,86,54))),v=6,rot=(math.radians(14),0,0))
box('M_easeltray',(PX-0.9,PY-0.02,PZ-PH/2-0.08),(PW+0.2,0.1,0.04),flat('easel',lin((120,86,54))),bv=0.005)
# ======================= SET A: museum workroom (x=300): the box, the inscription, the photo tests =======================
AX=300.0
floor('A_floor',AX,0,14,10,'parquet',(3,3)); wall('A_back',(AX,4,2.0),(14,0.2,4.0),'museum_wall',(2,2)); wall('A_side',(AX-6,0,2.0),(0.2,10,4.0),'museum_wall',(2,2))
box('A_ceiling',(AX,0,4.05),(14,10,0.1),WHITE,bv=0)
card('A_sign',(AX+2.6,3.88,3.2),2.2,0.55,'sign_museum',emit=0.3)
# the vitrine: plinth, glass edges (no glass sheet), the box and its label; a pencil case beside it for scale
box('A_plinth',(AX,1.2,0.5),(0.9,0.7,1.0),WHITE,bv=0.02)
for sx in(-1,1):
    for sy in(-1,1): box(f'A_vedge{sx}{sy}',(AX+sx*0.44,1.2+sy*0.34,1.3),(0.02,0.02,0.6),GOLD,bv=0)
for sy in(-1,1): box(f'A_vtop{sy}',(AX,1.2+sy*0.34,1.6),(0.9,0.02,0.02),GOLD,bv=0)
for sx in(-1,1): box(f'A_vtopx{sx}',(AX+sx*0.44,1.2,1.6),(0.02,0.7,0.02),GOLD,bv=0)
BOXM=flat('bentwood',lin((214,170,110)),0.7)
bx=cyl('A_box',(AX-0.05,1.2,1.035),0.1,0.07,BOXM,v=32); bx.scale=(1.0,0.62,1.0)
bl=plane('A_boxlid',(AX-0.05,1.2,1.0705),0.2,0.124,card_mat('boxlid','boxlid',emit=0.2),horiz=True); bl['noink']=1
box('A_pencil',(AX+0.17,1.15,1.02),(0.2,0.06,0.04),flat('pencilcase',lin((60,96,150)),0.6),bv=0.01)
card('A_label',(AX,0.95,1.033),0.36,0.18,'label_box',emit=0.2,rot=(math.radians(-70),0,0))   # tilted reading label lying on the plinth top
# work table with the box flipped over (the inscription on the bottom faces up) for the macro shots S02, S05, S06, S15
box('A_table',(AX+3.2,-0.6,0.74),(1.6,1.0,0.06),TABLE,bv=0.02)
for sx in(-1,1):
    for sy in(-1,1): box(f'A_tl{sx}{sy}',(AX+3.2+sx*0.72,-0.6+sy*0.42,0.36),(0.06,0.06,0.72),DARK,bv=0)
box('A_cloth',(AX+3.2,-0.6,0.775),(0.7,0.5,0.01),flat('cloth',lin((236,232,222)),0.9),bv=0)
fb=cyl('A_boxflip',(AX+3.2,-0.6,0.815),0.1,0.07,BOXM,v=32); fb.scale=(1.0,0.62,1.0)
NOTES=[plane(f'A_note_{k}',(AX+3.2,-0.6,0.8505+0.0004*i),0.19,0.118,card_mat('boxnote_'+k,'boxnote_'+k,emit=0.25),horiz=True) for i,k in enumerate(['blob','two','seven','reveal'])]
for o_ in NOTES: o_['noink']=1
vis(NOTES[0],[(130,193),(505,684),(1520,1564)]); vis(NOTES[1],[(684,712)]); vis(NOTES[2],[(712,725)]); vis(NOTES[3],[(1564,1588)])
box('A_lamp_b',(AX+3.85,-0.25,0.79),(0.18,0.18,0.04),DARK,bv=0.01); cyl('A_lamp_s',(AX+3.85,-0.25,1.05),0.012,0.5,DARK,v=6)
sph('A_lamp_h',(AX+3.75,-0.3,1.3),0.08,flat('lampshade',lin((60,110,80)),0.5),sc_=(1,1,0.6))
bpy.ops.object.light_add(type='POINT',location=(AX+3.6,-0.45,1.2)); _l=bpy.context.object; _l.name='A_lampL'; _l.data.energy=12; _l.data.color=(1,0.85,0.6); _l.data.shadow_soft_size=0.2
# photo corner (S08): tripod camera, a softbox, the test print pinned on the wall
for k in range(3):
    a=k*2*math.pi/3; cyl(f'A_tri{k}',(AX-3.6+0.22*math.cos(a),-0.2+0.22*math.sin(a),0.6),0.015,1.25,DARK,v=6,rot=(0.18*math.sin(a),-0.18*math.cos(a),0))
box('A_tricam',(AX-3.6,-0.2,1.28),(0.22,0.16,0.16),flat('camblack',lin((40,40,44)),0.5),bv=0.02); cyl('A_trilens',(AX-3.45,-0.15,1.27),0.05,0.08,flat('lensm',lin((90,110,140)),0.3),v=12,rot=(0,math.radians(90),0.45))   # aimed at the box on the photo table
box('A_soft',(AX-4.6,0.6,1.7),(0.7,0.08,0.7),flat('softbox',lin((250,250,250)),0.6,emit=1.6),bv=0.01); bpy.data.objects['A_soft'].rotation_euler=(0,0,math.radians(30))
cyl('A_softst',(AX-4.6,0.66,0.7),0.015,1.4,DARK,v=6)
pr=card('A_print',(AX-3.0,3.88,1.7),0.6,0.8,'photo_blob',emit=0.3); vis(pr,[(900,935)])
for i in range(3): card(f'A_print_old{i}',(AX-4.6+i*0.7,3.88,1.8),0.45,0.6,'photo_blob',emit=0.25)
box('A_ptable',(AX-2.6,0.3,0.74),(1.0,0.6,0.06),TABLE,bv=0.02)
for sx in(-1,1):
    for sy in(-1,1): box(f'A_ptl{sx}{sy}',(AX-2.6+sx*0.44,0.3+sy*0.25,0.36),(0.05,0.05,0.72),DARK,bv=0)
fb2=cyl('A_boxphoto',(AX-2.6,0.3,0.805),0.1,0.07,BOXM,v=32); fb2.scale=(1.0,0.62,1.0)
bpy.ops.object.light_add(type='AREA',location=(AX,0,3.9)); _l=bpy.context.object; _l.name='A_fill'; _l.data.energy=380; _l.data.size=6; _l.data.color=(1.0,0.92,0.82)
# ======================= SET P: the jubilee party office (x=600) =======================
PX0=600.0
floor('P_floor',PX0,0,12,9,'wood',(3,3)); wall('P_back',(PX0,3.5,1.9),(12,0.2,3.8),'office_wall',(2,2)); wall('P_side',(PX0+5.5,0,1.9),(0.2,9,3.8),'office_wall',(2,2))
box('P_ceiling',(PX0,0,3.85),(12,9,0.1),WHITE,bv=0)
box('P_desk',(PX0,1.2,0.74),(2.2,1.0,0.06),TABLE,bv=0.02)
for sx in(-1,1):
    for sy in(-1,1): box(f'P_dl{sx}{sy}',(PX0+sx*1.02,1.2+sy*0.42,0.36),(0.06,0.06,0.72),DARK,bv=0)
ck=cyl('P_cake',(PX0+0.5,1.2,0.92),0.26,0.3,card_mat('cake_side','cake_side',emit=0.2),v=32)
ckt=plane('P_caketop',(PX0+0.5,1.2,1.071),0.5,0.5,card_mat('cake_top','cake_top',emit=0.2),horiz=True); ckt['noink']=1
for k in range(4): cyl(f'P_candle{k}',(PX0+0.42+0.06*k,1.2+0.05*((k%2)*2-1),1.13),0.012,0.11,flat('candlew',lin([(230,70,80),(250,210,80),(90,160,220),(240,240,240)][k])),v=8)
for k in range(5): box(f'P_paper{k}',(PX0-0.6+0.1*k,1.1+0.05*k,0.775+0.004*k),(0.3,0.42,0.004),WHITE,bv=0).rotation_euler=(0,0,0.2*k-0.4)
box('P_shelf',(PX0-4.6,3.2,1.0),(1.6,0.4,2.0),WOOD,bv=0.02); card('P_shelfbooks',(PX0-4.6,2.99,1.2),1.5,1.5,'shelf_books',emit=0.2)
card('P_win',(PX0+5.39,0.8,2.0),1.6,1.6,'sky_winter',face_='-X',emit=0.8)
# the banner on one wiggly string across the back wall; it snaps at "fell" (S13)
HOOK_L=(PX0-2.6,3.34,2.9); HOOK_R=(PX0+2.6,3.34,2.9)
for i,h in enumerate((HOOK_L,HOOK_R)): sph(f'P_hook{i}',h,0.04,GOLD)
STR,STRP=strand('P_str',HOOK_L,HOOK_R,26,0.35,mat=flat('rope',lin((196,160,110)),0.9),r=0.016)   # a tan party cord (run lead r1: black lines read as scribbles)
BAN=empty('P_banpiv',HOOK_L)
ban=card('P_banner',(2.6,-0.02,-0.65),4.4,0.9,'banner400',emit=0.35); ban.parent=BAN; ban['noink']=0
# the snap: the right half of the string disappears at 1376 ("fell"), the banner swings down on the left hook and drops
SNAP=WF(158)
for o_ in STR: vis(o_,[(0,SNAP-1)])   # run lead r1: after the snap the cord is gone (the loose black lines read as scribbles); the banner hangs from the left hook by its corner
krot(BAN,SNAP-1,(0,0,0)); krot(BAN,SNAP+3,(0,math.radians(12),0)); krot(BAN,SNAP+7,(0,math.radians(26),0)); krot(BAN,SNAP+11,(0,math.radians(22),0)); krot(BAN,SNAP+14,(0,math.radians(25),0))   # r1: 60 deg put the free end through the floor; hangs at 25 deg, low corner 0.2 m above the floor
onone(BAN)
bpy.ops.object.light_add(type='AREA',location=(PX0,0,3.7)); _l=bpy.context.object; _l.name='P_fill'; _l.data.energy=360; _l.data.size=6; _l.data.color=(1.0,0.94,0.86)
# ---- set dressing (run lead r1: interiors were bare grey walls; Rick's backdrops are richly painted, core finding 3) ----
def window(n,c,w,h,face_='-Y',coll=None):
    card(n,c,w,h,'window_winter',face_=face_,emit=0.6,coll=coll)
def frame_pic(n,c,w,h,img,face_='-Y'):
    off=Vector((0,0.012,0)) if face_=='-Y' else Vector((0.012,0,0))
    box(n+'_fr',tuple(Vector(c)+off),(w+0.08,0.03,h+0.08) if face_=='-Y' else (0.03,w+0.08,h+0.08),flat('picframe',lin((120,82,50)),0.6),bv=0.005)
    card(n,c,w,h,img,face_=face_,emit=0.3)
def plant(n,c):
    cyl(n+'_pot',(c[0],c[1],0.22),0.2,0.44,flat('pot',lin((176,96,64)),0.8),v=16,r2=0.15)
    for k in range(6):
        a=k*1.05; sph(f'{n}_lf{k}',(c[0]+0.16*math.cos(a),c[1]+0.16*math.sin(a),0.62+0.1*(k%3)),0.2,flat('leaf',lin((70,130,70)),0.7),sc_=(1,1,0.8))
def wainscot(n,x0,x1,y,face_='-Y'):
    box(n,((x0+x1)/2,y,0.45),(x1-x0,0.05,0.9),flat('wains',lin((140,98,64)),0.7),bv=0.01)
    box(n+'_rail',((x0+x1)/2,y-0.03,0.92),(x1-x0,0.06,0.05),flat('wainsr',lin((110,74,48)),0.6),bv=0.005)
def pendant(n,c,top):
    cyl(n+'_c',(c[0],c[1],(c[2]+top)/2),0.008,top-c[2],INK,v=6); cyl(n,(c[0],c[1],c[2]-0.08),0.22,0.16,flat('shade',lin((60,110,80)),0.5),v=20,r2=0.06)
    sph(n+'_b',(c[0],c[1],c[2]-0.17),0.05,BULB)
# museum workroom
wainscot('A_wains',AX-6.9,AX+6.9,3.875)
window('A_win1',(AX-1.5,3.87,2.05),1.1,1.5); box('A_win1_sill',(AX-1.5,3.82,1.27),(1.3,0.14,0.06),WHITE,bv=0.01)
for k,(x,img) in enumerate([(AX+0.9,'house_old1'),(AX+1.6,'house_old3'),(AX-2.6,'house_old0')]): frame_pic(f'A_pic{k}',(x,3.86,2.0),0.5,0.75,img)
box('A_cab',(AX+0.7,3.55,1.05),(1.0,0.6,2.1),DARK,bv=0.02)
for k in range(3):
    box(f'A_cabsh{k}',(AX+0.7,3.3,0.45+k*0.6),(0.9,0.05,0.03),GOLD,bv=0)
    for j in range(3):
        vm=flat('vase'+str(j),lin([(60,110,170),(190,90,60),(220,190,90)][j]),0.4); x=AX+0.42+j*0.28; z=0.465+k*0.6
        if j%2: cyl(f'A_vase{k}{j}',(x,3.42,z+0.1),0.06,0.2,vm,v=14)
        else: sph(f'A_vase{k}{j}',(x,3.42,z+0.07),0.07,vm)
plant('A_plant',(AX-5.3,3.3)); plant('A_plant2',(AX+5.2,3.3))
box('A_backdrop',(AX-2.6,1.15,1.15),(1.6,0.02,2.3),flat('backdrop',lin((120,150,170)),0.9),bv=0)
for sx in(-1,1): cyl(f'A_bdst{sx}',(AX-2.6+sx*0.85,1.18,1.2),0.02,2.4,DARK,v=6)
cyl('A_bdroll',(AX-2.6,1.15,2.33),0.07,1.8,flat('backdropr',lin((100,130,150)),0.9),v=12,rot=(0,math.radians(90),0))
pendant('A_pend0',(AX-0.3,0.8,3.1),4.0); pendant('A_pend1',(AX+3.2,-0.6,3.0),4.0); pendant('A_pend2',(AX-2.8,0.2,3.0),4.0)
plane('A_rug',(AX-0.4,0.6,0.003),3.0,2.0,flat('rug',lin((150,50,50)),0.9),horiz=True)['noink']=1
# party office
wainscot('P_wains',PX0-5.9,PX0+5.4,3.375)
window('P_win1',(PX0+2.3,3.37,1.5),0.9,1.2); box('P_win1_sill',(PX0+2.3,3.32,0.87),(1.1,0.14,0.06),WHITE,bv=0.01)
box('P_board',(PX0-1.1,3.38,1.3),(1.0,0.04,0.65),flat('cork',lin((190,146,96)),0.9),bv=0.01)
for k,(x,z) in enumerate([(-1.45,1.42),(-1.15,1.2),(-0.85,1.4),(-1.3,1.12)]): plane(f'P_note{k}',(PX0+x,3.355,z),0.22,0.28,flat('note'+str(k%2),lin([(250,248,236),(250,230,120)][k%2]),0.8))['noink']=1
box('P_file',(PX0+1.6,3.1,0.6),(0.55,0.6,1.2),flat('filecab',lin((90,110,130)),0.5),bv=0.02)
for k in range(3): box(f'P_drawer{k}',(PX0+1.6,2.79,0.25+k*0.38),(0.3,0.02,0.05),GOLD,bv=0)
cyl('P_clock',(PX0+0.0,3.37,3.4),0.2,0.05,WHITE,v=24,rot=(math.radians(90),0,0)); cyl('P_clockr',(PX0,3.38,3.4),0.215,0.04,INK,v=24,rot=(math.radians(90),0,0))
box('P_hand1',(PX0,3.34,3.46),(0.02,0.01,0.13),INK,bv=0); box('P_hand2',(PX0+0.05,3.34,3.4),(0.1,0.01,0.02),INK,bv=0)
plant('P_plant',(PX0-2.3,3.0))
for k,(dx,col_) in enumerate([(-0.95,(230,70,80)),(-0.75,(90,160,220)),(-0.55,(250,210,80))]):
    sph(f'P_balloon{k}',(PX0+dx+3.1,3.0,1.55+0.12*k),0.14,flat('balloon'+str(k),lin(col_),0.3),sc_=(1,1,1.2))
    cyl(f'P_bstr{k}',(PX0+dx+3.1,3.0,(1.2+1.55+0.12*k-0.17)/2),0.004,1.55+0.12*k-0.17-1.2,flat('bstring',lin((240,240,240)),0.8),v=4)
pendant('P_pend0',(PX0,1.2,2.9),3.8)
# ======================= SET G: archive stacks (x=900) =======================
GX0=900.0
floor('G_floor',GX0,0,12,10,'parquet',(3,3)); wall('G_back',(GX0,4.2,2.2),(12,0.2,4.4),'office_wall',(2,2)); box('G_ceiling',(GX0,0,4.45),(12,10,0.1),WHITE,bv=0)
card('G_sign',(GX0-3.2,4.08,3.6),2.4,0.6,'sign_archive',emit=0.3)
for i,x in enumerate([-4.0,-1.6,1.6,4.0]):
    box(f'G_shelf{i}',(GX0+x,2.8,1.6),(1.9,0.6,3.2),WOOD,bv=0.02)
    for k in range(2): card(f'G_books{i}{k}',(GX0+x,2.49,0.85+k*1.5),1.8,1.4,'shelf_books',emit=0.2)
box('G_table',(GX0,-0.2,0.74),(1.6,0.9,0.06),TABLE,bv=0.02)
for sx in(-1,1):
    for sy in(-1,1): box(f'G_tl{sx}{sy}',(GX0+sx*0.72,-0.2+sy*0.38,0.36),(0.06,0.06,0.72),DARK,bv=0)
for k in range(3): box(f'G_tome{k}',(GX0-0.55,-0.25,0.8+0.07*k),(0.34,0.46,0.06),flat('tome',lin([(110,40,36),(60,80,110),(90,70,40)][k])),bv=0.01)
box('G_lamp_b',(GX0+0.6,0.05,0.79),(0.16,0.16,0.04),DARK,bv=0.01); cyl('G_lamp_s',(GX0+0.6,0.05,1.0),0.012,0.42,DARK,v=6); sph('G_lamp_h',(GX0+0.52,0.0,1.2),0.08,flat('lampshade',lin((60,110,80)),0.5),sc_=(1,1,0.6))
bpy.ops.object.light_add(type='POINT',location=(GX0+0.4,-0.1,1.1)); _l=bpy.context.object; _l.name='G_lampL'; _l.data.energy=14; _l.data.color=(1,0.85,0.6)
# the open church book on the table (close-up S11): page with the three names, grave No. 54 and "getraut 1651"
LB=box('G_ledger',(GX0+0.05,-0.25,0.79),(0.62,0.42,0.04),flat('ledgerc',lin((110,40,36)),0.7),bv=0.01)
lp=plane('G_ledgerpage',(GX0+0.05,-0.25,0.8105),0.58,0.39,card_mat('ledger_page','ledger_page',emit=0.25),horiz=True); lp['noink']=1
bpy.ops.object.light_add(type='AREA',location=(GX0,0,4.3)); _l=bpy.context.object; _l.name='G_fill'; _l.data.energy=300; _l.data.size=6; _l.data.color=(1.0,0.92,0.84)
# ======================= SET C: St. Johannis cemetery in snow (x=1100) =======================
CX0=1100.0
floor('C_snow',CX0,0,60,50,'snow',(8,8)); skydome('C_sky',(CX0,0),150,110,'sky_winter')
box('C_wall',(CX0,14,1.3),(40,0.8,2.6),SST,bv=0.04); box('C_church',(CX0+6,22,5),(10,8,10),CH,bv=0.04)
for i,(x,y,img,rot) in enumerate([(0,2.0,'grave54',0.0),(-2.2,1.4,'grave_a',0.08),(2.3,1.6,'grave_b',-0.06),(-1.2,5.0,'grave_a',0.1),(1.4,5.4,'grave_b',0.0),(-3.6,4.0,'grave_b',0.05),(3.8,4.2,'grave_a',-0.1)]):
    sl=box(f'C_slab{i}',(CX0+x,y,0.12),(1.5,0.95,0.24),SST,bv=0.03); sl.rotation_euler=(0,0,rot)
    pl=plane(f'C_plate{i}',(CX0+x,y,0.2425),1.0,0.62,card_mat(img,img,emit=0.2),horiz=True); pl.rotation_euler=(0,0,rot); pl['noink']=1
    sn=plane(f'C_snowcap{i}',(CX0+x+0.45,y+0.25,0.2435),0.4,0.3,flat('snowcap',lin((246,248,252)),0.8),horiz=True); sn['noink']=1
for i,(x,y) in enumerate([(-0.55,2.62),(0.6,2.62),(0.0,1.35)]):
    cyl(f'C_lan{i}',(CX0+x,y,0.12),0.07,0.24,flat('lanternglow',lin((255,210,130)),0.4,emit=4.0),v=10); cyl(f'C_lancap{i}',(CX0+x,y,0.26),0.08,0.04,INK,v=10)
    bpy.ops.object.light_add(type='POINT',location=(CX0+x,y,0.2)); _l=bpy.context.object; _l.name=f'C_lanL{i}'; _l.data.energy=6; _l.data.color=(1,0.75,0.45)
for i,(x,y,h) in enumerate([(-9,16,4.5),(-5.5,17,5.5),(-1.5,16.5,4.2),(3.5,17.5,5.0),(9,16.2,4.6),(12.5,17,5.2)]):   # eyepass r1: bare backdrop; snowy firs behind the wall
    cyl(f'C_firt{i}',(CX0+x,y,0.4),0.15,0.8,DARK,v=8)
    for k in range(3): cyl(f'C_fir{i}{k}',(CX0+x,y,0.8+k*h*0.24+h*0.12),h*0.22*(1-0.25*k),h*0.3,flat('fir',lin((46,96,70)),0.8),v=14,r2=0.02); cyl(f'C_firsn{i}{k}',(CX0+x,y,0.8+k*h*0.24+h*0.12+h*0.1),h*0.12*(1-0.25*k),h*0.1,flat('snowcap',lin((246,248,252)),0.8),v=14,r2=0.01)
snowfall('C_snowf',CX0,3,14,14,6,200,5)
# ======================= SET H: the 1678 market (x=1400): S12 (imagined 1628), S16 (1678) =======================
HX0=1400.0
floor('H_cobble',HX0,4,50,40,'cobble_old',(8,8)); skydome('H_sky',(HX0,4),150,110,'sky_winter')
for i,(x,y) in enumerate([(-9,10),(-9,2),(9,10),(9,2),(-4,16),(4,16)]):
    house(f'H_house{i}',(HX0+x,y),('+X' if x<-5 else ('-X' if x>5 else '-Y')),f'house_old{i%5}',w=6.0)
stall('H_st1',(HX0-3.2,6.5,0),0.0,'stall_old1',lit=False); stall('H_st2',(HX0+3.4,7.0,0),0.0,'stall_old2',roof='stall_roof_g',lit=False)
for sx in(-1,1):
    cyl(f'H_lanp{sx}',(HX0+sx*1.9,4.2,1.1),0.05,2.2,DARK,v=8); cyl(f'H_lan{sx}',(HX0+sx*1.9,4.2,2.3),0.09,0.24,flat('lanternglow',lin((255,210,130)),0.4,emit=4.0),v=10)
SIGN_Q=card('H_sign1628q',(HX0,8.5,3.0),1.6,0.6,'sign_1628q',emit=0.3); vis(SIGN_Q,[(1246,1334)])
SIGN_Y=card('H_sign1678',(HX0,8.5,3.0),1.6,0.6,'sign_1678',emit=0.3); vis(SIGN_Y,[(1588,1676)])
for sx in(-1,1): cyl(f'H_signc{sx}',(HX0+sx*0.7,8.5,3.6),0.022,0.6,INK,v=6)   # eyepass r1: hangers too thin to read
cyl('H_signbar',(HX0,8.5,3.9),0.03,2.4,DARK,v=6,rot=(0,math.radians(90),0))
for sx in(-1,1): cyl(f'H_signpost{sx}',(HX0+sx*1.2,8.5,1.95),0.06,3.9,DARK,v=8)
GHOST=card('H_ghost',(HX0+0.75,3.6,0.7),0.8,1.4,'ghost_outline',emit=0.4); vis(GHOST,[(WF(149),1334)])
snowfall('H_snowf',HX0,4,14,14,6,160,9,avoid=[(HX0-3.2,6.5,1.9,1.9),(HX0+3.4,7.0,1.9,1.9)])
# ======================= CAST + CAMERAS =======================
def S(n): return SH[n]
COMBOS=[]
def at(ch,seq): faces(ch,seq)
NX,NY=AX+3.2,-0.6            # flipped box note centre (macro shots); blob at (NX, NY-0.022), text starts at (NX-0.084, NY+0.035)
NZ=0.851
LX,LY=GX0+0.05,-0.25         # ledger page centre; "getraut 1651" at (LX-0.145, LY-0.07), "Grab No. 54" at (LX-0.145, LY+0.125)
# ---- S01 (0-130): hook. The market at dusk under the 400 JAHRE banner; the party man cheers on "birthday party" ----
s='S01'; r=S(s)
pa=char_on('S01_partyA','partyA',s,(0.5,8.3,0.0),r,'open_smile',arms=('arm','arm'))
look(pa,0,'open_smile',-1); turn(pa,40,'open_smile',-1,1); COMBOS.append((pa,WF(10)-4,'victory_up',1,'laugh'))
tA=char_on('S01_townA','townA',s,(-0.55,9.6,0.0),r,'happy',arms=('arm','arm_mug')); arm(tA,1,0,-35)
at(tA,[(0,'happy@R1'),(34,'smile@R2'),(70,'grin@R1'),(104,'laugh@F')])
tB=char_on('S01_townB','townB',s,(1.0,10.0,0.0),r,'smile',arms=('arm_mug','arm')); arm(tB,-1,0,-35)
at(tB,[(0,'smile@L1'),(46,'happy@L2'),(88,'open_smile@L1'),(112,'laugh@F')])
   # eyepass r1: the stacked-disc steam read as an odd floating shape; removed
path(s,[(0,(0.4,3.4,1.35),(0.4,9.5,1.9)),(70,(0.45,4.5,1.42),(0.45,9.5,2.05)),(130,(0.5,5.3,1.5),(0.5,9.5,2.2))])   # r1 framing probe: heads 10-16 % W, townA/B at the frame edges
# ---- S02 (130-193): "all because of one ink blot": macro push down onto the smudged digit ----
s='S02'; r=S(s)
path(s,[(130,(NX-0.04,NY-0.36,NZ+0.30),(NX-0.02,NY-0.005,NZ)),(193,(NX,NY-0.17,NZ+0.13),(NX,NY-0.022,NZ))])
# ---- S03 (193-332): the oldest proof: the box in its case, label and a pencil case for size; the archivist leans in with a magnifier ----
s='S03'; r=S(s)
ar=char_on('S03_arch','archivist',s,(AX-0.62,0.95,0.0),r,'smile',arms=('arm',[(193,'arm'),(240,'arm_magnifier')]))
for f,a in [(193,-15),(236,-30),(244,-92),(270,-98),(300,-94)]: arm(ar,1,f,a)
at(ar,[(193,'smile@R1')]); turn(ar,232,'surprise',1,2); at(ar,[(262,'open_smile@R2'),(290,'look_down@R2')]); turn(ar,312,'smile',2,0)
path(s,[(193,(AX-0.75,-1.55,1.36),(AX-0.5,1.08,1.08)),(332,(AX-0.1,-1.6,1.36),(AX-0.25,1.08,1.08))])   # run lead r1 (archivist huge against a bare table mid-move): lateral truck at one distance, no push after S02's push (rule 306)
# ---- S04 (332-505): the archivist shows the box; the party team laughs; "It says 1628! Print the banners!" ----
s='S04'; r=S(s)
a4=char_on('S04_arch','archivist',s,(PX0-0.55,-0.5,0.0),r,'neutral',arms=('arm','arm_woodbox')); arm(a4,1,332,-48)
at(a4,[(332,'neutral@R1'),(380,'smile@R1'),(410,'skeptical@R2'),(452,'side_eye@R1'),(486,'deadpan@R2')])
p4=char_on('S04_partyA','partyA',s,(PX0+0.3,0.0,0.0),r,'open_smile')
at(p4,[(332,'open_smile@L1'),(372,'grin@L2')]); COMBOS.append((p4,WF(48)-2,'point_out_tilt',1,'laugh'))
lipsync(p4,WORDS[49:55],WF(49)-1,WF(54)+12)
b4=char_on('S04_partyB','partyB',s,(PX0+0.75,0.4,0.0),r,'happy'); at(b4,[(332,'happy@L1'),(366,'smile@L2')]); COMBOS.append((b4,WF(48)-6,'laugh_lean_back',-1,'laugh'))
at(b4,[(440,'open_smile@L1'),(476,'laugh@L2')])
c4=char_on('S04_partyC','partyC',s,(PX0-0.2,0.45,0.0),r,'smile',arms=('arm','arm_brush')); arm(c4,1,332,-40)
at(c4,[(332,'smile@R1'),(360,'happy@L1')]); COMBOS.append((c4,WF(48)+2,'laugh_bob',1,'laugh')); at(c4,[(450,'grin@R1'),(480,'open_smile@F')])
path(s,[(332,(PX0-0.05,-3.45,1.45),(PX0+0.05,0.4,1.12)),(420,(PX0+0.08,-3.35,1.45),(PX0+0.1,0.4,1.13)),(505,(PX0+0.2,-3.25,1.44),(PX0+0.15,0.4,1.14))])   # r1 framing: 4 people staggered in depth inside the 9:16 frame
# ---- S05 (505-668): the bottom of the box: the note, read along the lines, ends on the smear ----
s='S05'; r=S(s)
path(s,[(505,(NX-0.07,NY-0.10,NZ+0.17),(NX-0.06,NY+0.035,NZ)),(580,(NX+0.02,NY-0.11,NZ+0.17),(NX+0.03,NY+0.02,NZ)),(668,(NX+0.0,NY-0.12,NZ+0.13),(NX,NY-0.022,NZ))])
# ---- S06 (668-725): "Was it a two? Or a seven?": the smudge, the 2 and the 7 tried on in turn ----
s='S06'; r=S(s)
path(s,[(668,(NX,NY-0.11,NZ+0.12),(NX,NY-0.022,NZ)),(725,(NX,NY-0.095,NZ+0.105),(NX,NY-0.022,NZ))])
# ---- S07 (725-815): "A big party hung on one wiggly line": low angle up to the banner on its sagging string ----
s='S07'; r=S(s)
b7=char_on('S07_partyB','partyB',s,(PX0+0.42,-0.2,0.0),r,'worried')
at(b7,[(725,'worried@L1'),(745,'nervous@L2')]); COMBOS.append((b7,WF(86),'glance_shift',-1,'nervous')); at(b7,[(790,'wince@L1')])
c7=char_on('S07_partyC','partyC',s,(PX0-0.42,-0.1,0.0),r,'worried',arms=('arm','arm_brush')); arm(c7,1,725,-30)
at(c7,[(725,'worried@R1'),(760,'look_up@R1'),(784,'nervous@R2'),(804,'wince@R1')])
path(s,[(725,(PX0-0.08,-2.75,0.95),(PX0,3.0,1.95)),(815,(PX0+0.08,-2.6,0.97),(PX0+0.03,3.0,2.15))])   # r1: low angle from in front of the pair (the cake hid partyB when they stood at the back wall)
# ---- S08 (815-935): the photo tests: two flashes, the print on the wall, still a blob ----
s='S08'; r=S(s)
ph=char_on('S08_photog','photog',s,(AX-3.75,-0.75,0.0),r,'determined',arms=('arm','arm'))
for f,a in [(815,-20),(855,-62),(862,-70),(866,-62),(871,-70),(876,-25)]: arm(ph,1,f,a)
at(ph,[(815,'determined@R1'),(850,'squint@R1'),(884,'neutral@R2')]); COMBOS.append((ph,WF(103)-6,'tilt_talk',1,'deadpan'))
a8=char_on('S08_arch','archivist',s,(AX-2.3,-0.45,0.0),r,'hope' if False else 'smile')
at(a8,[(815,'smile@L1'),(846,'open_smile@L2'),(880,'worried@R1')]); COMBOS.append((a8,WF(100),'dip_talk',-1,'sigh'))
for f_ in (WF(96)-2,WF(97)): fx(f'S08_flash{f_}','fx_spark',(AX-3.25,-0.12,1.27),f_,8,0.35,C(s),grow=1.4)   # eyepass r1: smaller, clear of the photographer's face
path(s,[(815,(AX-3.05,-3.6,1.45),(AX-3.05,0.0,1.15)),(880,(AX-3.0,-3.4,1.5),(AX-3.0,1.0,1.3)),(935,(AX-3.15,-2.4,1.62),(AX-3.0,3.6,1.65))])   # eyepass r1: the archivist was cut by the right edge; the pan now leaves her out
# ---- S09 (935-1062): "Then she went where no one looks for a Christmas gift. The old graveyard books." ----
s='S09'; r=S(s)
a9=char_on('S09_arch','archivist',s,(GX0-1.3,-0.45,0.0),r,'determined',arms=([(935,'arm'),(WF(117),'arm_ledger')],'arm'))
arm(a9,-1,WF(117),-42); arm(a9,-1,WF(117)+20,-40)
at(a9,[(935,'determined@R1')]); COMBOS.append((a9,965,'turn_and_point',1,'determined')); at(a9,[(1010,'smile@L1'),(1036,'proud@F'),(1050,'smug@R1')])
path(s,[(935,(GX0+0.3,-4.3,1.6),(GX0-0.9,1.4,1.45)),(1000,(GX0+0.2,-3.6,1.5),(GX0-0.9,0.5,1.25)),(1062,(GX0-0.1,-3.2,1.45),(GX0-1.0,0.0,1.2))])
# ---- S10 (1062-1158): St. Johannis, grave No. 54: three lanterns for the girl and her parents ----
s='S10'; r=S(s)
a10=char_on('S10_arch','archivist',s,(CX0-0.6,1.0,0.0),r,'sad',arms=('arm_ledger','arm')); arm(a10,-1,1062,-40)
at(a10,[(1062,'sad@R1'),(1090,'look_down@R2'),(1122,'content@R1'),(1146,'smile@R2')])
path(s,[(1062,(CX0+0.1,-3.0,1.65),(CX0-0.2,1.7,0.65)),(1158,(CX0-0.2,-1.3,1.3),(CX0-0.25,2.0,0.45))])
# ---- S11 (1158-1246): the church book: "getraut 1651", long before 1628? no: long AFTER 1628 ----
s='S11'; r=S(s)
path(s,[(1158,(LX-0.12,LY+0.0,0.811+0.28),(LX-0.14,LY+0.125,0.811)),(1200,(LX-0.13,LY-0.15,0.811+0.24),(LX-0.14,LY-0.02,0.811)),(1246,(LX-0.14,LY-0.18,0.811+0.18),(LX-0.145,LY-0.07,0.811))])
# ---- S12 (1246-1334): 1628, imagined: the girl holds the box out; the one who should take it is not there yet ----
s='S12'; r=S(s)
g12=char_on('S12_giver','giver1678',s,(HX0-0.45,3.6,0.0),r,'smile',arms=('arm','arm_woodbox'))
for f,a in [(1246,-40),(WF(146),-74),(1300,-74)]: arm(g12,1,f,a)
at(g12,[(1246,'smile@R1'),(1268,'open_smile@R2'),(1288,'happy@R1')]); COMBOS.append((g12,WF(150)+2,'startle_recoil',-1,'shock')); at(g12,[(1324,'stunned@R1')])
pass   # eyepass r1: the background man lined up with the held-out box (read as a hand-over to him); removed
path(s,[(1246,(HX0-0.2,-0.4,1.45),(HX0-0.1,3.6,1.4)),(1334,(HX0+0.1,0.6,1.45),(HX0+0.25,3.6,1.45))])
# ---- S13 (1334-1404): "That's when the big birthday fell apart": the string snaps, the banner drops ----
s='S13'; r=S(s)
p13=char_on('S13_partyA','partyA',s,(PX0-0.35,0.2,0.0),r,'proud'); at(p13,[(1334,'proud@R1'),(1352,'smile@R2')]); COMBOS.append((p13,SNAP+2,'startle_recoil',1,'shock')); at(p13,[(1396,'stunned@F')])
b13=char_on('S13_partyB','partyB',s,(PX0+0.65,0.4,0.0),r,'smile'); at(b13,[(1334,'smile@L1'),(1356,'happy@L2')]); COMBOS.append((b13,SNAP+4,'panic_clutch',-1,'panic'))
path(s,[(1334,(PX0+0.15,-2.6,1.5),(PX0+0.15,1.6,1.7)),(1404,(PX0+0.15,-2.85,1.55),(PX0+0.15,1.6,1.8))])
# ---- S14 (1404-1520): "no one gets a gift before she's born, so that blob had to be a seven" ----
s='S14'; r=S(s)
a14=char_on('S14_arch','archivist',s,(AX-0.8,0.95,0.0),r,'determined')
at(a14,[(1404,'determined@R1'),(1430,'squint@R2'),(1460,'skeptical@R1')]); COMBOS.append((a14,WF(172)-2,'eureka_point_up',1,'open_smile')); at(a14,[(1512,'proud@F')])
path(s,[(1404,(AX-0.1,-1.9,1.4),(AX-0.45,1.1,1.12)),(1520,(AX-0.3,-1.35,1.38),(AX-0.5,1.1,1.15))])
# ---- S15 (1520-1588): the seven shows through the smudge: 1678 ----
s='S15'; r=S(s)
path(s,[(1520,(NX,NY-0.15,NZ+0.15),(NX,NY-0.022,NZ)),(1564,(NX,NY-0.12,NZ+0.12),(NX,NY-0.022,NZ)),(1588,(NX,NY-0.115,NZ+0.115),(NX,NY-0.022,NZ))])
# ---- S16 (1588-1676): 1678: the market is real; Susanna hands the box to little Regina ----
s='S16'; r=S(s)
HAND=1618
g16=char_on('S16_giver','giver1678',s,(HX0-0.55,3.6,0.0),r,'happy',arms=('arm',[(1588,'arm_woodbox'),(HAND,'arm')]))
for f,a in [(1588,-42),(1604,-72),(HAND+6,-60),(HAND+16,-15)]: arm(g16,1,f,a)
at(g16,[(1588,'happy@R1'),(1606,'open_smile@R2'),(1636,'smile@R1'),(1660,'content@F')])
q16=char_on('S16_recip','recip1678',s,(HX0+0.6,3.5,0.0),r,'surprise',arms=([(1588,'arm'),(HAND,'arm_woodbox')],'arm'))
for f,a in [(1588,-12),(1604,-70),(HAND+12,-56),(HAND+26,-40)]: arm(q16,-1,f,a)
at(q16,[(1588,'surprise@L1'),(1612,'open_smile@L2'),(1640,'laugh@L1'),(1662,'happy@F')])
pass   # eyepass r1: the hand-over met on the background man's body; removed
path(s,[(1588,(HX0,0.2,1.35),(HX0,3.6,1.3)),(1640,(HX0+0.05,0.3,1.42),(HX0+0.05,3.6,1.55)),(1676,(HX0+0.05,0.1,1.55),(HX0,4.0,2.0))])
# ---- S17 (1676-1800): "So this week, Nuremberg's Christkind opens it again from the church balcony" ----
s='S17'; r=S(s)
ck=char_on('S17_christkind','christkind',s,(0.0,CY-0.6,BZ),r,'smile'); at(ck,[(1676,'smile@L1'),(1710,'open_smile@F')]); COMBOS.append((ck,WF(196)-2,'wave_hello',1,'happy')); at(ck,[(1790,'laugh@R1')])
CR=[]
for i,(x,y,k,arms_) in enumerate([(-1.1,13.8,'townA',('arm','arm_mug')),(0.15,14.6,'townC',('arm','arm')),(1.15,13.9,'townB',('arm_mug','arm')),(-0.8,12.6,'partyB',('arm','arm')),(1.0,12.4,'vendor',('arm','arm'))]):
    c_=char_on(f'S17_crowd{i}',k,s,(x,y,0.0),r,'happy',arms=arms_); CR.append(c_)
    at(c_,[(1676,['happy@R1','smile@F','open_smile@L1','happy@L1','grin@R1'][i]),(1712+i*6,['look_up@R1','look_up@F','look_up@L1','look_up@L1','look_up@R1'][i]),(1760+i*4,['open_smile@R1','laugh@F','happy@L2','open_smile@L1','grin@R2'][i])])
COMBOS.append((CR[3],1765,'victory_up',-1,'laugh'))
path(s,[(1676,(0.6,9.0,1.5),(0.2,14.0,1.6)),(1720,(0.5,10.5,2.2),(0.0,16.0,3.2)),(1760,(0.35,14.8,4.7),(0.0,CY-0.6,BZ+1.0)),(1800,(0.3,16.2,5.4),(0.0,CY-0.6,BZ+0.95))])   # r1: crane up over the crowd to the Christkind (head was 6-7 % W)
# ---- S18 (1800-1905): payoff. The party's still on, just fifty candles short: the prints stall, the poster lands on "short" ----
s='S18'; r=S(s)
p18=char_on('S18_partyA','partyA',s,(3.05,-1.0,0.0),r,'happy',arms=('arm','arm_candles')); arm(p18,1,1800,-55); arm(p18,1,WF(208)-4,-55); arm(p18,1,WF(208)+2,-6)   # eyepass r1 (critical): the raised candles floated into the landing frame without her; arm drops after 'candles'
at(p18,[(1800,'happy@R1'),(1830,'open_smile@R2'),(WF(210),'grin@F'),(1890,'smile@R1')])
LAND=WF(211)
path(s,[(1800,(3.4,-4.6,1.7),(3.7,0.2,1.55)),(1850,(3.7,-4.2,1.66),(3.8,0.2,1.57)),(LAND,(3.95,-2.35,1.62),(3.9,0.2,1.58)),(END,(3.95,-2.3,1.62),(3.9,0.2,1.58))])
# ======================= foreground layers (rule 311): one near object per shot over 60 f, low in a corner, never over a face or the poster =======================
CHRN=set()
TERRAIN=('M_cobble','A_floor','P_floor','G_floor','C_snow','H_cobble','A_cloth','G_table','A_table')
def _ground(x,y,f,z0,terrain=False):
    sc.frame_set(f); dg=bpy.context.evaluated_depsgraph_get(); o_=Vector((x,y,z0+1.2))
    for k in range(40):
        ok,loc,nrm,i,ob,m=sc.ray_cast(dg,o_,Vector((0,0,-1)))
        if not ok: return None
        o_=loc+Vector((0,0,-0.001))
        if terrain and not ob.name.startswith(TERRAIN): continue
        if ob.name in CHRN or ob.get('fly') or ob.hide_render: continue
        return loc.z
    return None
def campos(n,f):
    def ev(o):
        return Vector([next(fc for fc in o.animation_data.action.fcurves if fc.data_path=='location' and fc.array_index==i).evaluate(f) for i in range(3)])
    return ev(L.CAM[n]),ev(L.TGT[n])
def fgobj(n,kind,side=1,dist=1.5,drop=0.75,f=None,lat=0.55):
    f0=SH[n][0] if f is None else f; c_,t_=campos(n,f0); d_=(t_-c_); d_.z=0; d_=d_.normalized(); rt=Vector((d_.y,-d_.x,0)).normalized()
    p=c_+d_*dist+rt*lat*side*dist
    g=_ground(p.x,p.y,f0,c_.z,terrain=True); p.z=g if g is not None else 0.0   # planted on the floor/table it stands on (rule 376)
    co=C(n)
    if kind=='post': cyl(f'{n}_fgpost',(p.x,p.y,p.z+0.6),0.07,1.2,DARK,v=10,coll=co)
    elif kind=='crate': box(f'{n}_fgcrate',(p.x,p.y,p.z+0.25),(0.5,0.5,0.5),WOOD,coll=co,bv=0.02).rotation_euler=(0,0,0.4)
    elif kind=='snowbank': o=sph(f'{n}_fgsnow',(p.x,p.y,p.z),0.45,flat('snowbank',lin((240,244,250)),0.8),sc_=(1.4,1.0,0.5),coll=co)
    elif kind=='books':
        for k in range(3): box(f'{n}_fgbook{k}',(p.x,p.y,p.z+0.04+0.08*k),(0.36-0.03*k,0.26,0.08),flat('tome',lin([(110,40,36),(60,80,110),(90,70,40)][k])),coll=co,bv=0.01).rotation_euler=(0,0,0.15*k)
    elif kind=='pencil': cyl(f'{n}_fgpencil',(p.x,p.y,p.z+0.005),0.005,0.17,flat('pencil',lin((230,190,60)),0.6),v=6,coll=co,rot=(0,math.radians(90),0.5))
    elif kind=='stool':
        cyl(f'{n}_fgstool',(p.x,p.y,p.z+0.45),0.2,0.05,WOOD,v=16,coll=co)
        for k in range(3): a=k*2.09; cyl(f'{n}_fgsl{k}',(p.x+0.13*math.cos(a),p.y+0.13*math.sin(a),p.z+0.21),0.02,0.42,DARK,v=6,coll=co)
for n,k,sd,ds,lt in [('S01','crate',-1,1.6,0.6),('S02','pencil',1,0.12,0.9),('S03','stool',-1,1.0,0.55),('S04','crate',1,1.4,0.6),('S05','pencil',-1,0.1,0.9),
                  ('S07','books',1,0.9,0.7),('S08','stool',1,1.3,0.6),('S09','books',-1,1.2,0.6),('S10','snowbank',1,1.5,0.6),('S11','pencil',1,0.12,0.8),
                  ('S12','crate',1,1.4,0.6),('S13','books',-1,1.3,0.6),('S14','stool',1,1.0,0.6),('S15','pencil',1,0.1,0.9),('S16','crate',-1,1.5,0.6),
                  ('S17','crate',1,1.6,0.6),('S18','crate',-1,1.4,0.7)]:
    fgobj(n,k,sd,ds,0.0,lat=lt)
# ======================= world, finish, ink, render settings =======================
def world_and_sun():
    w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; bg=w.node_tree.nodes['Background']; bg.inputs['Color'].default_value=(*lin((150,160,200)),1); bg.inputs['Strength'].default_value=0.9
    bpy.ops.object.light_add(type='SUN',rotation=(math.radians(58),0,math.radians(35))); sun=bpy.context.object; sun.name='sun'; sun.data.energy=3.2; sun.data.color=(1.0,0.86,0.74); sun.data.angle=math.radians(3)   # low warm dusk sun
world_and_sun()
for c_,f_,k_,sd_,fc_ in COMBOS: combo(c_,f_,k_,side=sd_,face=fc_)
print('COMBOS',len(COMBOS),len(set(k for _,_,k,_,_ in COMBOS)))
sc['air']=json.dumps(sorted(L.AIR))
for a in ALL: finish(a)
for c_ in bpy.data.collections:   # rule 367c (rigcheck r1 CARD_SHADOW x30): combo split cards (btop/blegs/pose) made after char() also cast no lamp shadow; the blob is the only shadow
    if c_.name.startswith('CHR_'):
        for o_ in c_.all_objects:
            if o_.type=='MESH' and not o_.name.endswith('_shadow'): o_.visible_shadow=False
print('hulls',L.ink())
for o_ in bpy.data.objects:
    if o_.type=='LIGHT' and o_.data.type!='SUN': o_.visible_camera=False
L.render_setup(100,8)
sc.cycles.samples=4; sc.cycles.transparent_max_bounces=8; sc.cycles.diffuse_bounces=1; sc.cycles.max_bounces=3
os.makedirs('/root/nb/blend',exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath='/root/nb/blend/cc.blend'); print('SCENE_OK all')
