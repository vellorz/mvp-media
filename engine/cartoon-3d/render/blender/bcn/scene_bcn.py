# Barcelona / FC Barcelona origin short (sat-barcelona): Blender builder.   blender -b --python scene_bcn.py   -> /root/cc/blend/bcn.blend
# Built on the Cape Cod pipeline (lib.py rig from the d5lr4u motion library: walks v3, combos, shadow blob heights; cast cards; ink; render setup).
# Every set here is new: night street + LOS DEPORTES building (R), newsroom (N), gym (G), Bonanova velodrome (V), big stadium bowl (B), day Rambla kiosk (K).
import sys, os, math, random, json
sys.path.insert(0,'/root/cc/src')
import bpy, bmesh
from mathutils import Vector, Euler, Matrix
import lib as L
from lib import combo,box,cyl,sph,plane,flat,surf,card_mat,lin,vis,kloc,krot,kscale,empty,cam,char,face,faces,arm,bob,finish,lipsync,turn,look
END=1767
sc=L.init(END); R=random.Random(11)
WORDS=json.load(open('/root/cc/vo/vo_trim.wav.words.json'))
WT=[(w['w'],w['s'],w['e']) for w in WORDS]
def wf(i): return int(round((WORDS[i]['s']+0.1)*30))
# shot table: overlaps are dissolves (smoothstep in post), touching ranges are hard cuts
SH={'S01':(0,94),'S02':(88,172),'S03':(172,300),'S04':(300,420),'S05':(420,482),'S06':(476,516),'S07':(512,540),
    'S08':(540,656),'S09':(656,815),'S10':(815,904),'S11':(898,950),'S12':(944,985),'S13':(985,1125),'S14':(1125,1192),
    'S15':(1186,1268),'S16':(1268,1330),'S17':(1330,1420),'S18':(1414,1500),'S19':(1500,1640),'S20':(1634,END)}
sc['shots']=json.dumps(SH)
LENS={'S01':30,'S02':34,'S03':30,'S04':30,'S05':32,'S06':36,'S07':32,'S08':30,'S09':28,'S10':28,'S11':26,'S12':30,'S13':24,'S14':32,
      'S15':30,'S16':32,'S17':28,'S18':22,'S19':30,'S20':32}
for n in SH: cam(n,LENS[n],11.0)
NIGHT=[(0,171),(540,984)]   # sun/world switch frames (hard cuts at 172 and 985 sit on every day/night change)
def C(n): return L.chr_coll(n)
PATHS={}
def path(n,keys):
    PATHS.setdefault(n,[]).extend(keys); L.path(n,keys)
def dolly(n,k,frames=None):
    for key in PATHS[n]:
        f,l,t=key[:3]
        if frames and not(frames[0]<=f<=frames[1]): continue
        kloc(L.CAM[n],f,tuple(t[i]+(l[i]-t[i])*k for i in range(3)))
ALL=[]
INK=flat('inkc',lin((50,28,42)),0.9)
def grid(n,cx,cy,w,d,res,hf,m,coll=None,z0=0.0):
    bm=bmesh.new(); nx,ny=res
    vs=[[bm.verts.new((cx-w/2+w*i/(nx-1),cy-d/2+d*j/(ny-1),z0+hf(cx-w/2+w*i/(nx-1),cy-d/2+d*j/(ny-1)))) for i in range(nx)] for j in range(ny)]
    for j in range(ny-1):
        for i in range(nx-1): bm.faces.new((vs[j][i],vs[j][i+1],vs[j+1][i+1],vs[j+1][i]))
    me=bpy.data.meshes.new(n); bm.to_mesh(me); bm.free()
    o=bpy.data.objects.new(n,me); (coll or L.C_SET).objects.link(o); me.materials.append(m); o['noink']=1; return o
def char_on(inst,kind,shot,loc,rng,face0=None,arms=('arm','arm'),walker=False,scale=1.0):
    ch=char(inst,kind,shot,loc,rng,face0,arms=arms,walker=walker,scale=scale); ALL.append(ch); return ch
def drift_faces(ch,f0,f1,pool,seed,step=(20,38)):
    rr=random.Random(seed); f=f0; seq=[]
    while f<f1: seq.append((f,rr.choice(pool))); f+=rr.randint(*step)
    faces(ch,seq)
def fx(n,img,loc,f0,dur,size,coll,face='-Y',grow=1.6,rise=0.0):
    o=plane(n,loc,size,size,card_mat(img,img,emit=0.6),coll=coll,face=face); o['noink']=1
    for k in range(0,dur+1,2):
        s_=1+(grow-1)*k/dur; o.scale=(s_,s_,s_); o.keyframe_insert('scale',frame=f0+k)
        o.location=(loc[0],loc[1],loc[2]+rise*k/dur); o.keyframe_insert('location',frame=f0+k)
    vis(o,[(f0,f0+dur)])
    for fc in o.animation_data.action.fcurves:
        if fc.data_path in('scale','location'):
            for kp in fc.keyframe_points: kp.interpolation='CONSTANT'
    return o
def onone(o):
    if o.animation_data and o.animation_data.action:
        for fc in o.animation_data.action.fcurves:
            if fc.data_path!='hide_render':
                for kp in fc.keyframe_points: kp.interpolation='CONSTANT'
def hardcut(shot,f):
    for o_ in (L.CAM[shot],L.TGT[shot]):
        for fc in o_.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                if int(round(kp.co[0]))==f-1: kp.interpolation='CONSTANT'
def skydome(n,c,rad,h,img,z0=-20,rep=5):
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
    m.node_tree.nodes['Image Texture'].extension='REPEAT'
    cb=bmesh.new(); cv=[cb.verts.new((c[0]+rad*math.cos(2*math.pi*i/seg),c[1]+rad*math.sin(2*math.pi*i/seg),z0+h-0.5)) for i in range(seg)]; cb.faces.new(cv)
    cm=bpy.data.meshes.new(n+'_cap'); cb.to_mesh(cm); cb.free(); cu=cm.uv_layers.new()
    for li in range(len(cu.data)): cu.data[li].uv=(0.5,0.985)
    co_=bpy.data.objects.new(n+'_cap',cm); L.C_NOI.objects.link(co_); cm.materials.append(m); co_['fly']=1; co_['noink']=1
    for o2 in (o,co_): o2.visible_diffuse=False; o2.visible_glossy=False; o2.visible_transmission=False; o2.visible_volume_scatter=False; o2.visible_shadow=False
    return o
def skycard(n,loc,face_,w,h,img,coll=None,emit=1.0):
    s_=plane(n,loc,w,h,card_mat(img,img,emit=emit),coll=coll or L.C_NOI,face=face_); s_['fly']=1; s_['noink']=1; s_.visible_shadow=False; return s_
def card(n,loc,w,h,img,rotz=0.0,emit=0.25,coll=None,ink=False):
    """painted picture card (facade, sign, poster-like dressing) facing -Y before rotz"""
    o=plane(n,loc,w,h,card_mat(img,img,emit=emit),coll=coll or L.C_NOI,face='-Y'); o.rotation_euler=(0,0,rotz)
    if not ink: o['noink']=1
    return o
def ring(n,cx,cy,a0,b0,a1,b1,z0,z1,m,seg=96,coll=None,ink=False):
    """elliptic band from the inner ellipse (a0,b0) at z0 to the outer (a1,b1) at z1 (banked track, stadium tiers)"""
    bm=bmesh.new(); inn=[];out=[]
    for i in range(seg):
        t=2*math.pi*i/seg; inn.append(bm.verts.new((cx+a0*math.cos(t),cy+b0*math.sin(t),z0))); out.append(bm.verts.new((cx+a1*math.cos(t),cy+b1*math.sin(t),z1)))
    for i in range(seg): j=(i+1)%seg; bm.faces.new((inn[i],inn[j],out[j],out[i]))
    me=bpy.data.meshes.new(n); bm.to_mesh(me); bm.free(); o=bpy.data.objects.new(n,me); (coll or L.C_SET).objects.link(o); me.materials.append(m)
    if not ink: o['noink']=1
    return o
def disc(n,cx,cy,a,b,z,m,seg=96,coll=None):
    bm=bmesh.new(); vs=[bm.verts.new((cx+a*math.cos(2*math.pi*i/seg),cy+b*math.sin(2*math.pi*i/seg),z)) for i in range(seg)]; bm.faces.new(vs)
    me=bpy.data.meshes.new(n); bm.to_mesh(me); bm.free(); o=bpy.data.objects.new(n,me); (coll or L.C_SET).objects.link(o); me.materials.append(m); o['noink']=1; return o
def tree(n,loc,s=1.0,img='planetree'):
    """plane tree: ink-lined trunk + two crossed painted canopy cards"""
    cyl(n+'_trunk',(loc[0],loc[1],loc[2]+1.6*s),0.16*s,3.2*s,flat('bark',lin((128,112,90)),0.85),v=10)
    for k in range(2):
        g=plane(f'{n}_c{k}',(loc[0],loc[1],loc[2]+4.2*s),3.6*s,7.2*s*0.5,card_mat(img,img,emit=0.12),face='-Y'); g.rotation_euler=(0,0,math.radians(20+k*90)); g['noink']=1; g.scale=(1,1,1)
def lamp(n,loc,night=True,coll=None):
    """iron street lamp; the glass glows and (night) a warm point light sits in it"""
    iron=flat('iron',lin((52,62,58)),0.6)
    cyl(n+'_post',(loc[0],loc[1],loc[2]+1.6),0.06,3.2,iron,v=10,coll=coll); cyl(n+'_base',(loc[0],loc[1],loc[2]+0.2),0.14,0.4,iron,v=10,coll=coll)
    box(n+'_cage',(loc[0],loc[1],loc[2]+3.42),(0.34,0.34,0.44),flat('lampglass',lin((255,214,140)),0.3,emit=(6.0 if night else 0.6)),coll=coll,bv=0.02)
    cyl(n+'_cap',(loc[0],loc[1],loc[2]+3.72),0.24,0.12,iron,v=10,coll=coll,r2=0.04)
    if night:
        ld=bpy.data.lights.new(n+'_L','POINT'); ld.energy=160; ld.color=(1.0,0.78,0.5); ld.shadow_soft_size=0.3
        lo=bpy.data.objects.new(n+'_L',ld); (coll or L.C_SET).objects.link(lo); lo.location=(loc[0],loc[1]-0.25,loc[2]+3.3)
def plight(n,loc,energy,col=(1.0,0.8,0.55),size=0.3):
    ld=bpy.data.lights.new(n,'POINT'); ld.energy=energy; ld.color=col; ld.shadow_soft_size=size; lo=bpy.data.objects.new(n,ld); L.C_SET.objects.link(lo); lo.location=loc; return lo
def building(n,x,y,w,h,img,face_='-Y',depth=6.0,emit=0.22,roof=(150,90,70)):
    """3D block with the painted facade card on its street face; cornice and roof edge get ink"""
    sgn=1 if face_=='-Y' else -1; yb=y+sgn*depth/2
    box(n+'_blk',(x,yb,h/2),(w,depth,h),flat(n+'_wall',lin((200,170,140)),0.9),bv=0.02)
    o=card(n+'_fac',(x,y-sgn*0.012,h/2),w,h,img,rotz=(0 if face_=='-Y' else math.pi),emit=emit)
    box(n+'_corn',(x,y-sgn*0.12,h+0.12),(w+0.2,0.36,0.24),flat('cornice',lin((226,210,180)),0.8),bv=0.02)
    box(n+'_roof',(x,yb,h+0.32),(w,depth,0.2),flat('roof'+str(roof[0]),lin(roof),0.9),bv=0.02)
    return o
# ======================= world: per-frame day/night (hard cuts on every change) =======================
w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; BG=w.node_tree.nodes['Background']
bpy.ops.object.light_add(type='SUN',rotation=(math.radians(52),0,math.radians(40))); SUN=bpy.context.object; SUN.name='sun'; SUN.data.angle=math.radians(3)
def daynight():
    for f in range(0,END+1):
        night=any(a<=f<=b for a,b in NIGHT); prev=any(a<=f-1<=b for a,b in NIGHT)
        if f==0 or night!=prev:
            SUN.data.energy=0.55 if night else 4.6; SUN.data.color=(0.62,0.7,1.0) if night else (1.0,0.93,0.82)
            SUN.data.keyframe_insert('energy',frame=f); SUN.data.keyframe_insert('color',frame=f)
            BG.inputs['Color'].default_value=(*lin((44,52,92) if night else (160,196,226)),1); BG.inputs['Strength'].default_value=0.45 if night else 1.0
            BG.inputs['Color'].keyframe_insert('default_value',frame=f); BG.inputs['Strength'].keyframe_insert('default_value',frame=f)
    for ad in (SUN.data.animation_data,w.node_tree.animation_data):
        for fc in ad.action.fcurves:
            for kp in fc.keyframe_points: kp.interpolation='CONSTANT'
daynight()
# ======================= SET R: Barcelona street at night (x=0); the LOS DEPORTES building with the GIMNASIO in the same block =======================
RX=0
SETTSN=surf('settsN','settsN',(2,2)); PAVN=surf('pavingN','pavingN',(2.5,2.5))
box('R_road',(RX,-1,-0.05),(80,8,0.1),SETTSN,bv=0); box('R_walk',(RX,4.4,0.06),(80,3.6,0.12),PAVN,bv=0.01); box('R_walk2',(RX,-6.4,0.06),(80,3.6,0.12),PAVN,bv=0.01)
for n_ in ('R_road','R_walk','R_walk2'): bpy.data.objects[n_]['noink']=1
box('R_curb',(RX,2.58,0.07),(80,0.16,0.14),flat('curbN',lin((120,116,120)),0.8),bv=0.01)
# far side: building row; the newspaper building is the middle one (x -3..3)
for i,(x,img) in enumerate([(-15,'facN2'),(-9,'facN3'),(9,'facN4'),(15,'facN5'),(-21,'facN1'),(21,'facN0')]): building(f'R_b{i}',RX+x,6.2,6.0,9.0,img,emit=0.35)
DEP=building('R_dep',RX,6.2,6.0,9.0,'facN0',emit=0.35)
card('R_sign_dep',(RX-0.6,6.15,3.15),3.4,0.64,'sign_deportes',emit=0.7,ink=True)
card('R_sign_gym',(RX+1.7,6.15,4.75),2.6,0.49,'sign_gym',emit=0.7,ink=True)
card('R_sign_pr',(RX-1.9,6.15,2.42),1.6,0.30,'sign_prensa',emit=0.6)
box('R_door',(RX-0.6,6.25,1.15),(1.3,0.2,2.3),flat('doorglow',lin((255,200,120)),0.5,emit=0.9),bv=0.01); bpy.data.objects['R_door']['noink']=1
box('R_doorframe',(RX-0.6,6.12,2.34),(1.6,0.14,0.14),flat('doorwood',lin((90,60,40)),0.8),bv=0.01)
for sx in(-1,1): box(f'R_doorjamb{sx}',(RX-0.6+sx*0.72,6.12,1.15),(0.14,0.14,2.3),flat('doorwood',lin((90,60,40)),0.8),bv=0.01)
for i,x in enumerate([-12,-6,3.2,6,12,18,-18]): lamp(f'R_lamp{i}',(RX+x,3.0,0.12))
for i,x in enumerate([-9,-3,3,9,-15,15]): tree(f'R_tree{i}',(RX+x,-5.6,0.12),0.95,'planetreeN')
for i,(x,img) in enumerate([(-6,'facN1'),(0,'facN2'),(6,'facN3'),(-12,'facN4'),(12,'facN5')]): building(f'R_n{i}',RX+x,-8.4,6.0,9.0,img,face_='+Y',emit=0.3)
skydome('R_sky',(RX,0),120,90,'sky_night',z0=-10,rep=3)
plight('R_doorL',(RX-0.6,5.4,2.0),70,(1.0,0.75,0.45))
# ======================= SET N: newsroom of Los Deportes (x=300) =======================
NX=300; WN=surf('wallnews','wall_news',(3,3)); FN=surf('floornews','floor_news',(2,2)); WOOD=flat('wood',lin((150,104,66)),0.8); DWOOD=flat('dwood',lin((104,70,46)),0.8)
box('N_floor',(NX,0,-0.05),(12,10,0.1),FN,bv=0); bpy.data.objects['N_floor']['noink']=1
box('N_back',(NX,3.2,1.75),(12,0.2,3.5),WN,bv=0); box('N_left',(NX-5,0,1.75),(0.2,10,3.5),WN,bv=0); box('N_right',(NX+5,0,1.75),(0.2,10,3.5),WN,bv=0)
for nm_,cx_,w_,d_ in (('N_ceil',NX,12,10),('G_ceil',600,16,12)):
    c_=box(nm_,(cx_,0,(3.55 if nm_[0]=='N' else 4.05)),(w_,d_,0.1),flat('ceil',lin((214,200,178)),0.9),bv=0); c_.visible_shadow=False; c_['noink']=1   # camera sees a ceiling (no night sky over the walls); sun still lights the room
box('N_counter',(NX-0.6,0.9,0.52),(4.2,0.7,1.04),WOOD,bv=0.02); box('N_countertop',(NX-0.6,0.9,1.06),(4.4,0.86,0.06),DWOOD,bv=0.01)
for i in range(3): box(f'N_tcase{i}',(NX-3.4+i*1.05,2.85,1.0),(1.0,0.5,2.0),DWOOD,bv=0.02); card(f'N_tcasef{i}',(NX-3.4+i*1.05,2.59,1.0),0.96,0.72,'typecase',emit=0.15)
# hand press: iron frame, platen, big wheel
IRON=flat('pressiron',lin((44,46,52)),0.5,metal=0.3)
box('N_pressbase',(NX+3.1,2.1,0.45),(1.4,0.9,0.9),IRON,bv=0.03); box('N_pressbed',(NX+3.1,2.1,0.98),(1.6,1.0,0.12),flat('pressbed',lin((90,86,84)),0.6),bv=0.01)
for sx in(-1,1): box(f'N_presspost{sx}',(NX+3.1+sx*0.6,2.1,1.6),(0.14,0.3,1.3),IRON,bv=0.02)
box('N_presshead',(NX+3.1,2.1,2.28),(1.5,0.4,0.22),IRON,bv=0.02); cyl('N_presswheel',(NX+3.95,1.7,1.4),0.55,0.08,IRON,v=24,rot=(0,math.radians(90),0))
box('N_paperstack',(NX+1.9,1.6,0.3),(0.6,0.45,0.6),flat('newsprint',lin((236,230,212)),0.9),bv=0.01)
card('N_clock',(NX+0.6,3.08,2.65),0.7,0.7,'clock9',emit=0.4,ink=True)
WIN_D=card('N_winD',(NX+1.9,3.085,2.0),1.1,1.5,'sky_bcn',emit=0.9); WIN_N=card('N_winN',(NX+1.9,3.08,2.0),1.1,1.5,'sky_night',emit=0.7)
box('N_winframe',(NX+1.9,3.095,2.0),(1.24,0.01,1.64),DWOOD,bv=0.0)   # r3: frame BEHIND the window cards (it hid them)
vis(WIN_D,[(172,539),(985,END)]); vis(WIN_N,[(0,171),(540,984)])
# reading desk by the window (the paper inserts S02/S06)
box('N_desk',(NX+3.0,-1.6,0.74),(1.5,0.9,0.06),DWOOD,bv=0.01)
for sx,sy in((-1,-1),(1,-1),(-1,1),(1,1)): box(f'N_deskleg{sx}{sy}',(NX+3.0+sx*0.68,-1.6+sy*0.38,0.36),(0.06,0.06,0.72),DWOOD,bv=0.005)
PAP=plane('N_paper',(NX+3.0,-1.6,0.775),0.42,0.574,card_mat('paper_ad','paper_ad',emit=0.35),horiz=True); PAP['noink']=1; PAP.rotation_euler=(0,0,math.radians(6))
PAPH=plane('N_paperhl',(NX+3.0,-1.6,0.776),0.42,0.574,card_mat('paper_ad_hl','paper_ad_hl',emit=0.35),horiz=True); PAPH['noink']=1; PAPH.rotation_euler=(0,0,math.radians(6))
vis(PAP,[(0,300)]); vis(PAPH,[(301,END)])
cyl('N_deskcandle',(NX+3.55,-1.35,0.86),0.035,0.18,flat('wax',lin((240,232,210)),0.7),v=10); sph('N_flame',(NX+3.55,-1.35,0.98),0.03,flat('flame',lin((255,190,90)),0.3,emit=8.0))
for i,(x,y) in enumerate([(-2.2,0.0),(1.0,-0.4),(3.0,-0.2)]):
    sph(f'N_pend{i}',(NX+x,y,3.0),0.14,flat('pendglow',lin((255,214,150)),0.3,emit=5.0)); cyl(f'N_pendc{i}',(NX+x,y,3.3),0.01,0.6,IRON,v=6)
    plight(f'N_pendL{i}',(NX+x,y,2.8),110)
plight('N_candleL',(NX+3.5,-1.4,1.2),25,(1.0,0.7,0.4),0.1)
# ======================= SET G: the Gimnasio Solé (x=600) =======================
GX=600; WG=surf('wallgym','wall_gym',(3,3)); FG=surf('floorgym','floor_gym',(2,2))
box('G_floor',(GX,0,-0.05),(16,12,0.1),FG,bv=0); bpy.data.objects['G_floor']['noink']=1
box('G_back',(GX,4.2,2.0),(16,0.2,4.0),WG,bv=0); box('G_left',(GX-7,0,2.0),(0.2,12,4.0),WG,bv=0); box('G_right',(GX+7,0,2.0),(0.2,12,4.0),WG,bv=0)
box('G_beam',(GX,1.2,3.7),(14,0.24,0.24),DWOOD,bv=0.02)
for sx in(-1,1):   # rings on ropes
    cyl(f'G_rope{sx}',(GX-3.2+sx*0.3,1.2,2.9),0.015,1.6,flat('rope',lin((190,160,110)),0.9),v=6)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.13,minor_radius=0.022,location=(GX-3.2+sx*0.3,1.2,2.0),rotation=(math.radians(90),0,0)); t_=bpy.context.object; t_.name=f'G_ring{sx}'; t_.data.materials.append(DWOOD)
    for c_ in list(t_.users_collection): c_.objects.unlink(t_)
    L.C_SET.objects.link(t_)
for sy in(-1,1):   # parallel bars
    cyl(f'G_bar{sy}',(GX+3.4,2.6+sy*0.25,1.4),0.035,2.6,WOOD,v=10,rot=(0,math.radians(90),0))
    for sx in(-1,1): cyl(f'G_barpost{sy}{sx}',(GX+3.4+sx*1.0,2.6+sy*0.25,0.7),0.04,1.4,DWOOD,v=8)
box('G_rack',(GX+5.6,3.6,0.5),(1.6,0.4,0.08),DWOOD,bv=0.01)
for k in range(4):
    for sx in(-1,1): sph(f'G_db{k}{sx}',(GX+5.0+k*0.4+sx*0.12,3.6,0.62),0.07,flat('dbiron',lin((36,34,38)),0.5))
box('G_mat',(GX-3.2,1.2,0.04),(2.0,1.2,0.08),flat('mat',lin((150,60,50)),0.9),bv=0.02)
# founding table: long table + benches, lamps above (night)
box('G_table',(GX,0.6,0.76),(3.6,1.0,0.06),WOOD,bv=0.01)
for sx in(-1,1):
    for sy in(-1,1): box(f'G_tleg{sx}{sy}',(GX+sx*1.65,0.6+sy*0.4,0.37),(0.07,0.07,0.74),DWOOD,bv=0.005)
box('G_bench',(GX,1.55,0.24),(3.6,0.3,0.06),DWOOD,bv=0.01)
for sx in(-1,1): box(f'G_benchleg{sx}',(GX+sx*1.6,1.55,0.12),(0.06,0.26,0.24),DWOOD,bv=0.005)
box('G_ledger',(GX-0.2,0.5,0.8),(0.5,0.36,0.03),flat('ledger',lin((120,40,36)),0.8),bv=0.005); plane('G_ledgerpg',(GX-0.2,0.5,0.818),0.44,0.3,flat('pg',lin((240,232,212)),0.9),horiz=True)['noink']=1
GW_D=card('G_winD',(GX+1.5,4.085,2.4),1.4,1.8,'sky_bcn',emit=0.9); GW_N=card('G_winN',(GX+1.5,4.08,2.4),1.4,1.8,'sky_night',emit=0.7)
box('G_winframe',(GX+1.5,4.095,2.4),(1.54,0.01,1.94),DWOOD,bv=0.0); vis(GW_D,[(172,539),(985,END)]); vis(GW_N,[(0,171),(540,984)])
card('G_signin',(GX-1.75,4.08,3.2),2.6,0.49,'sign_gym',emit=0.4,ink=True)
for i,x in enumerate([0.25,2.5]):   # r3b: pendants and sign moved apart; the left bulb sat over the G of GIMNASIO in S10
    sph(f'G_pend{i}',(GX+x,0.6,2.6),0.14,flat('pendglow',lin((255,214,150)),0.3,emit=5.0)); cyl(f'G_pendc{i}',(GX+x,0.6,3.15),0.01,1.0,IRON,v=6)
    plight(f'G_pendL{i}',(GX+x,0.4,2.45),120)
plight('G_fill',(GX-3,-2,2.6),90,(1.0,0.86,0.7),1.0)
# ======================= SET V: the old Bonanova bike track (x=1000): banked oval, turf infield, goals, fence, small stand =======================
VX=1000; TRK=surf('trackm','track',(3,3)); TURF=surf('turfm','turf',(4,4))
grid('V_ground',VX,0,160,120,(20,16),lambda x,y:-0.02,surf('grassfar','grass2',(6,6)))
disc('V_turf',VX,0,24,10.5,0.0,TURF)
ring('V_track',VX,0,24,10.5,31,17,0.0,1.5,TRK,ink=False)
ring('V_trackrim',VX,0,31,17,31.2,17.2,1.5,1.5,flat('rimwhite',lin((236,232,220)),0.8))
FENCE=card_mat('fence','fence',emit=0.15)
for i in range(64):
    t=2*math.pi*(i+0.5)/64; x=VX+32.2*math.cos(t); y=17.9*math.sin(t)
    o=plane(f'V_fence{i}',(x,y,0.7),3.4,1.4,FENCE,face='-Y'); o.rotation_euler=(0,0,t-math.pi/2+math.pi)
for sx in(-1,1):   # goals: two white posts and a bar (no nets: 1899 match photos), on the long axis
    for sy in(-1,1): cyl(f'V_gpost{sx}{sy}',(VX+sx*20,sy*3.66,1.22),0.06,2.44,flat('gwhite',lin((246,244,236)),0.6),v=10)
    cyl(f'V_gbar{sx}',(VX+sx*20,0,2.44),0.06,7.44,flat('gwhite',lin((246,244,236)),0.6),v=10,rot=(math.radians(90),0,0))
for i in range(5):   # chalk lines on the turf
    pass
box('V_halfline',(VX,0,0.006),(0.1,20,0.01),flat('chalk',lin((240,240,232)),0.9),bv=0); bpy.data.objects['V_halfline']['noink']=1
# small wooden stand on the far straight, crowd card in it
box('V_stand',(VX+2,22.5,1.3),(16,3.6,2.6),flat('standwood',lin((150,112,76)),0.85),bv=0.03)
box('V_standroof',(VX+2,22.8,4.4),(17,4.4,0.16),flat('standroof',lin((120,60,50)),0.85),bv=0.02)
for k in range(5): cyl(f'V_standpost{k}',(VX-6+k*4,21.0,3.4),0.07,2.0,DWOOD,v=8)
card('V_crowd',(VX+2,21.0,3.1),15.0,2.4,'crowd_small',emit=0.35)
skycard('V_hills',(VX,70,7),'-Y',200,40,'hills_far',emit=0.7); skycard('V_hillsB',(VX,-70,7),'+Y',200,40,'hills_far',emit=0.7)
skydome('V_sky',(VX,0),130,200,'sky_bcn',z0=-10,rep=3)
SCORE=card('V_score',(VX-12,9.6,1.7),2.2,1.38,'score01',emit=0.4,ink=True)
for sx in(-1,1): vis(cyl(f'V_scorepost{sx}',(VX-12+sx*1.0,9.75,0.9),0.05,1.8,DWOOD,v=8),[(1220,END)])
vis(SCORE,[(1220,END)])   # the 0-1 board only exists after the goal (continuity)
# ======================= SET B: the big stadium bowl (x=1500) =======================
BX=1500; SEAT=surf('seatm','seats',(3,3))
disc('B_pitch',BX,0,40,28,0.0,TURF)
for k,(a0,b0,z0,a1,b1,z1) in enumerate([(41,29,0.0,52,40,8.0),(52,40,8.0,53,41,8.4),(53,41,8.4,66,54,20.0)]):
    ring(f'B_tier{k}',BX,0,a0,b0,a1,b1,z0,z1,SEAT if k!=1 else flat('tierlip',lin((220,214,204)),0.8),seg=120)
CRB=card_mat('crowd_xl','crowd_xl',emit=0.6)   # r3: big-figure crowd (F8)
ROWS=[(42.6,30.6,1.25,2.3),(45.4,33.4,3.15,2.3),(48.2,36.2,5.05,2.3),(51.0,39.0,6.95,2.3),(55.2,43.2,11.0,3.0),(58.6,46.6,14.0,3.0),(62.0,50.0,17.0,3.0)]   # bcn r2: upright crowd cards stepped up the tiers (tilted cards read as grey at grazing angles)
for row,(ra,rb,zc,hh) in enumerate(ROWS):
    for i in range(44):
        t=2*math.pi*(i+0.5+0.5*(row%2))/44; x=BX+ra*math.cos(t); y=rb*math.sin(t)
        o=plane(f'B_crowd{row}_{i}',(x,y,zc),2*math.pi*ra/44*1.08,hh,CRB,face='-Y'); o.rotation_euler=(0,0,t-math.pi/2+math.pi); o['noink']=1; o.visible_shadow=False
box('B_line',(BX,0,0.006),(0.12,40,0.01),flat('chalk',lin((240,240,232)),0.9),bv=0); bpy.data.objects['B_line']['noink']=1
for sx in(-1,1):
    for sy in(-1,1): cyl(f'B_gpost{sx}{sy}',(BX+sx*34,sy*3.66,1.22),0.06,2.44,flat('gwhite',lin((246,244,236)),0.6),v=10)
    cyl(f'B_gbar{sx}',(BX+sx*34,0,2.44),0.06,7.44,flat('gwhite',lin((246,244,236)),0.6),v=10,rot=(math.radians(90),0,0))
skydome('B_sky',(BX,0),160,230,'sky_pm',z0=-10,rep=3)
# ======================= SET K: the Rambla by day (x=2000): promenade, plane trees, newspaper kiosk with the poster =======================
KX=2000; PAV=surf('paving','paving',(2.5,2.5)); SETTS=surf('setts','setts',(2,2))
box('K_prom',(KX,0,0.04),(120,7,0.08),PAV,bv=0); box('K_roadL',(KX,-6,-0.05),(120,5,0.1),SETTS,bv=0); box('K_roadR',(KX,6,-0.05),(120,5,0.1),SETTS,bv=0)
box('K_walkL',(KX,-10,0.06),(120,3,0.12),PAV,bv=0); box('K_walkR',(KX,10,0.06),(120,3,0.12),PAV,bv=0)
for n_ in ('K_prom','K_roadL','K_roadR','K_walkL','K_walkR'): bpy.data.objects[n_]['noink']=1
for i in range(14):
    x=-39+i*6
    for sy in(-1,1): tree(f'K_tree{i}{sy}',(KX+x,sy*3.0,0.08),1.0)
for i in range(12):
    x=-33+i*6
    building(f'K_bR{i}',KX+x,11.6,6.0,9.0,'fac%d'%(i%6),emit=0.18)
    building(f'K_bL{i}',KX+x,-11.6,6.0,9.0,'fac%d'%((i+3)%6),face_='+Y',emit=0.18)
for i,x in enumerate([-30,-18,-6,6,18,30]): lamp(f'K_lamp{i}',(KX+x,-3.3,0.08),night=False)
# kiosk (x=KX+0): green iron box, panel textures, awning, paper racks, the Barcelona poster in a frame on its street-facing side
KG=flat('kioskgreen',lin((52,104,76)),0.6)
box('K_kiosk',(KX,0.6,1.2),(2.4,1.6,2.4),KG,bv=0.03)
for i,(x,y,r_) in enumerate([(KX-0.6,-0.21,0),(KX+0.6,-0.21,0)]): card(f'K_kpanel{i}',(x,y,0.6),1.1,1.1,'kioskpanel',rotz=r_,emit=0.2)
box('K_awning',(KX,0.2,2.55),(2.9,2.4,0.14),flat('awning',lin((180,60,50)),0.8),bv=0.03)
cyl('K_dome',(KX,0.6,2.85),1.2,0.5,KG,v=24,r2=0.18)
box('K_counter',(KX,-0.32,1.0),(2.2,0.36,0.06),DWOOD,bv=0.01)
for k in range(5): box(f'K_rack{k}',(KX-0.9+k*0.45,-0.32,1.08),(0.36,0.26,0.06),flat('newsprint',lin((236,230,212)),0.9),bv=0.005)
PW,PH=0.80,1.20; PZ=1.72; PXc=KX+1.4; PYc=0.6
box('poster_frame',(PXc+0.025,PYc,PZ),(0.04,PW+0.12,PH+0.12),flat('pframe',lin((246,236,214)),0.35,emit=0.9),bv=0.01)
pmat=bpy.data.materials.new('poster'); N_,L_=L.nodes(pmat); pp_=N_['Principled BSDF']; it_=N_.new('ShaderNodeTexImage'); it_.image=bpy.data.images.load('/root/cc/poster_2k.png'); it_.interpolation='Cubic'
L_.new(it_.outputs['Color'],pp_.inputs['Base Color']); L_.new(it_.outputs['Color'],pp_.inputs['Emission Color']); pp_.inputs['Emission Strength'].default_value=0.15; pp_.inputs['Roughness'].default_value=1.0; pp_.inputs['Specular IOR Level'].default_value=0.0
poster=plane('poster',(PXc+0.05,PYc,PZ),PW,PH,pmat,coll=L.C_NOI,face='-Y'); poster.rotation_euler=(0,0,math.radians(90)); poster['noink']=1   # faces +X (toward the S20 camera)
skydome('K_sky',(KX,0),160,230,'sky_bcn',z0=-10,rep=3)
# falling plane-tree leaves (rule 379 environment life): small leaf cards drifting down in K and R
LEAF=flat('leaf',lin((196,150,60)),0.8,emit=0.2)
def leaves(prefix,cx,cy,n,f0,f1,seed,coll=None):
    rr=random.Random(seed)
    for i in range(n):
        x=cx+rr.uniform(-4,4); y=cy+rr.uniform(-2,2); z0=rr.uniform(3.2,4.6); o=plane(f'{prefix}{i}',(x,y,z0),0.09,0.06,LEAF,coll=coll); o['noink']=1; o.visible_shadow=False
        st=f0+rr.randint(0,max(1,(f1-f0)//2)); du=rr.randint(70,120)
        for k in range(0,du+1,3):
            t=k/du; kloc(o,st+k,(x+0.6*math.sin(t*7+i),y+0.3*math.cos(t*5+i),z0-(z0-0.1)*t)); krot(o,st+k,(t*9+i,t*5,t*3))
        vis(o,[(st,st+du)])
if os.environ.get('SETS_ONLY'): bpy.ops.wm.save_as_mainfile(filepath='/root/cc/blend/bcn_sets.blend'); print('SETS_OK'); raise SystemExit(0)
# ======================= CAST + CAMERAS =======================
def S(n): return SH[n]
COMBOS=[]
SPEED={'st':0.096/10,'nm':0.140/8,'br':0.186/6}
WALKS=[]
def walk_move(ch,f,name,side,face_,axis='x',dirv=None):
    """approved walk v3 combo; the root slides at the stride speed so the feet do not skate (Detroit m11test)"""
    WALKS.append((ch,f,name,side,face_,axis,dirv)); combo(ch,f,name,side=side,face=face_)
    st=L.MO.COMBOS[name]['walk_style']; ev=[e for e in L.MO.COMBOS[name]['events'] if e['ch']=='legs']; a,b=f+ev[0]['at'],f+ev[-1]['at']
    r=ch['root']; p0=tuple(r.location); d=SPEED[st]*(b-a)
    if dirv: p1=(p0[0]+dirv[0]*d,p0[1]+dirv[1]*d,p0[2])
    elif axis=='x': p1=(p0[0]+side*d,p0[1],p0[2])
    else: p1=(p0[0],p0[1]-d,p0[2])
    kloc(r,a,p0); kloc(r,b,p1)
    for fc in r.animation_data.action.fcurves:
        if fc.data_path=='location':
            for kp in fc.keyframe_points:
                if kp.co[0] in (a,b): kp.interpolation='LINEAR'
    r.location=p1; return f+max(e['at'] for e in L.MO.COMBOS[name]['events'])
def walk_far(ch,f0,f1,name,side,face_,axis='x',dirv=None):
    f=f0
    while f+60<=f1: f=walk_move(ch,f,name,side,face_,axis,dirv)+1
    return f
# ---- S01 (0-94): hook. Night street, the young Swiss guy alone under a lamp with his football; nobody to play with ----
s='S01'; r=S(s)
h1=char_on('S01_hero','hero',s,(RX+0.2,3.7,0.12),r,'happy',arms=('arm','arm_ball'))
faces(h1,[(0,'determined'),(30,'happy'),(56,'worried')])
look(h1,0,'determined',0); turn(h1,18,'determined',0,-2); turn(h1,40,'happy',-2,1); turn(h1,62,'worried',1,0)
arm(h1,1,0,-30); arm(h1,-1,0,-8); arm(h1,-1,64,-14)
COMBOS.append((h1,70,'glance_shift',1,'worried'))
path(s,[(0,(RX-1.2,0.3,1.05),(RX+0.2,3.7,1.2)),(60,(RX-0.6,1.5,1.12),(RX+0.2,3.7,1.25)),(94,(RX-0.45,1.85,1.15),(RX+0.2,3.7,1.25))])
leaves('S01_leaf',RX,4.2,6,0,94,1,coll=C(s))
# ---- S02 (88-172): insert. His ad in the paper on the newsroom desk at night; push in; "asking strangers to play" ----
s='S02'; r=S(s)
path(s,[(88,(NX+3.0,-2.55,1.55),(NX+3.0,-1.62,0.78)),(172,(NX+3.0,-2.15,1.32),(NX+3.0,-1.6,0.78))])
# ---- S03 (172-300): he'd just moved to Barcelona: the Rambla by day, suitcase down beside him, locals stroll past in pairs ----
s='S03'; r=S(s); X3=KX-24
h3=char_on('S03_hero','heroH',s,(X3,0.4,0.08),r,'happy',arms=('arm_suitcase','arm'))
faces(h3,[(172,'happy'),(215,'open_smile'),(236,'neutral'),(258,'worried'),(284,'sad')])
turn(h3,236,'neutral',0,2); turn(h3,262,'worried',2,-2); turn(h3,284,'sad',-2,0)
arm(h3,-1,172,-4); arm(h3,1,172,-8); arm(h3,1,228,-60); arm(h3,1,246,-8)
COMBOS.append((h3,276,'glance_shift',1,'sad'))
pa=char_on('S03_locA','locA',s,(X3-1.6,1.5,0.08),r,'happy'); pb=char_on('S03_locB','locB',s,(X3-2.2,2.0,0.08),r,'laugh')
walk_far(pa,176,300,'walk_stroll',1,'happy'); walk_far(pb,176,300,'walk_stroll',1,'laugh')
pc=char_on('S03_locC','locC',s,(X3+2.6,1.1,0.08),r,'smile'); walk_far(pc,196,300,'walk',-1,'smile')
path(s,[(172,(X3+0.5,-3.4,1.4),(X3,0.6,1.25)),(240,(X3+0.3,-2.5,1.35),(X3,0.5,1.25)),(300,(X3+0.2,-2.1,1.3),(X3,0.4,1.25))])
leaves('S03_leaf',X3,1.0,8,172,300,3,coll=C(s))
# ---- S04 (300-420): the guys at the gym laugh; one says the quote (lipsync only on the quoted words, rule 185) ----
s='S04'; r=S(s)
gA=char_on('S04_gymA','gymA',s,(GX+2.6,1.8,0),r,'laugh',arms=('arm','arm_dumbbell')); gB=char_on('S04_gymB','gymB',s,(GX+3.9,2.5,0),r,'laugh',arms=('arm_dumbbell','arm'))
h4=char_on('S04_hero','heroH',s,(GX+1.45,-0.2,0),r,'happy',arms=('arm_paper','arm'))
faces(h4,[(300,'happy'),(338,'worried'),(362,'nervous'),(404,'sad')]); turn(h4,300,'happy',0,2); turn(h4,370,'nervous',2,1)
COMBOS+=[(gB,330,'laugh_lean_back',-1,'laugh'),(gA,410,'laugh_bob',-1,'laugh')]
faces(gA,[(300,'smug'),(337,'laugh'),(356,'smug_grin')]); faces(gB,[(300,'grin'),(356,'laugh')])
lipsync(gA,WT,358,412,shapes=('talkA','talkB','talkC','talkD'))
look(gA,300,'smug',-2); look(gB,300,'grin',-2)
path(s,[(300,(GX+1.0,-3.0,1.35),(GX+1.7,1.6,1.2)),(360,(GX+1.9,-2.6,1.3),(GX+2.4,1.8,1.25)),(420,(GX+2.0,-2.4,1.3),(GX+2.4,1.8,1.25))])   # r3b: the push ended 0.6 m from the hero and passed his head (giant cut face at f400); push now stops 1.4 m back
# ---- S05 (420-482): in the newsroom by day he reads the paper: his name is spelled wrong ----
s='S05'; r=S(s)
h5=char_on('S05_hero','heroH',s,(NX+2.6,-0.9,0),r,'happy',arms=('arm','arm'))   # reads the paper lying on the desk (both arms free for the double take)
faces(h5,[(420,'happy'),(444,'squint'),(462,'shock')]); look(h5,420,'happy',1)
COMBOS.append((h5,456,'double_take',1,'shock'))
path(s,[(420,(NX+1.7,-3.0,1.3),(NX+2.6,-0.9,1.2)),(482,(NX+2.0,-2.6,1.28),(NX+2.6,-0.9,1.22))])
# ---- S06 (476-516): insert, the misprint circled: "Kans Kamper" ----
s='S06'; r=S(s)
path(s,[(476,(NX+3.02,-2.15,1.32),(NX+3.0,-1.55,0.78)),(516,(NX+3.0,-1.95,1.12),(NX+2.97,-1.5,0.78))])
# ---- S07 (512-540): "Close enough." shrug ----
s='S07'; r=S(s)
h7=char_on('S07_hero','heroH',s,(NX+2.6,-0.9,0),r,'deadpan',arms=('arm','arm'))
faces(h7,[(512,'deadpan'),(521,'smile')]); COMBOS.append((h7,516,'look_back_shrug',1,'deadpan'))
path(s,[(512,(NX+2.0,-2.5,1.3),(NX+2.6,-0.9,1.22)),(540,(NX+2.1,-2.3,1.28),(NX+2.6,-0.9,1.22))])
# ---- S08 (540-656): the office late at night: clock at nine, clerk behind the counter, he waits for anyone who loves the game ----
s='S08'; r=S(s)
ck=char_on('S08_clerk','clerk',s,(NX-1.2,1.45,0),r,'sleepy',arms=('arm','arm_paper')); h8=char_on('S08_hero','hero',s,(NX-0.12,0.1,0),r,'happy',arms=('arm','arm_ball'))
faces(ck,[(540,'sleepy'),(590,'asleep'),(612,'blink'),(620,'sleepy'),(646,'asleep')]); faces(h8,[(540,'happy'),(574,'determined'),(600,'happy'),(632,'worried')])
turn(h8,560,'determined',0,-2); turn(h8,600,'happy',-2,1); turn(h8,630,'worried',1,-1); bob(ck,[596,640],5)
COMBOS.append((h8,578,'tilt_talk',-1,'determined'))
path(s,[(540,(NX-0.6,-3.0,1.5),(NX-0.55,1.0,1.45)),(600,(NX-0.6,-2.4,1.45),(NX-0.55,0.9,1.4)),(656,(NX-0.6,-2.1,1.42),(NX-0.55,0.9,1.4))])
# ---- S09 (656-815): "And they came." outside the building at night: the Swiss pal, two English brothers, a German, a pack of locals walk up ----
s='S09'; r=S(s)
h9=char_on('S09_hero','hero',s,(RX-0.4,4.9,0.12),r,'happy',arms=('arm','arm_ball'))
faces(h9,[(656,'happy'),(666,'surprise'),(690,'happy'),(730,'grin'),(780,'laugh')]); COMBOS.append((h9,668,'wave_hello',-1,'happy'))
# (kind, walk start frame, style, start x, y): each walks in from off frame and stops in the group by the door (one cycle each)
ARR=[('pal',674,'walk_brisk',-3.3,4.2),('engA',704,'walk',-3.3,4.6),('engB',708,'walk',-4.0,3.9),('german',736,'walk',1.7,4.3),
     ('locA',758,'walk_brisk',3.2,3.8),('locB',762,'walk_brisk',3.9,4.6),('locC',766,'walk_brisk',-5.5,3.7),('locD',770,'walk_brisk',4.6,3.9)]
for i,(k,f0,wk,x,y) in enumerate(ARR):
    fc=['happy','smile','grin','proud','happy','laugh','grin','open_smile'][i]
    a_=char_on(f'S09_{k}',k,s,(RX+x,y,0.12),r,fc); sd=1 if x<0 else -1
    look(a_,656,fc,2*sd); walk_move(a_,f0,wk,sd,fc); faces(a_,[(f0+70,fc),(f0+96,'laugh')])
path(s,[(656,(RX-0.3,0.6,1.35),(RX-0.4,4.9,1.3)),(700,(RX-1.2,-0.4,1.6),(RX-2.4,4.5,1.25)),(760,(RX+0.4,-1.6,1.8),(RX+0.6,4.4,1.25)),(815,(RX,-2.4,1.9),(RX,4.6,1.3))])
leaves('S09_leaf',RX,4.0,5,656,815,9,coll=C(s))
# ---- S10 (815-904): "one night that fall, twelve of them met in a gym": the founding table, wide, slow push ----
s='S10'; r=S(s)
TWELVE=['hero','pal','engA','engB','german','locA','locB','locC','locD','swiss2','locE','locF']
SEATS=[(-1.6,1.55),(-1.05,1.6),(-0.5,1.55),(0.05,1.6),(0.6,1.55),(1.15,1.6),(1.7,1.55),(-2.3,0.9),(2.35,0.9),(-1.9,2.2),(0.0,2.3),(1.9,2.2)]
T10=[];T12=[]
for i,(k,(x,y)) in enumerate(zip(TWELVE,SEATS)):
    a_=char_on(f'S10_{k}',k,s,(GX+x,y,0),r,'happy'); drift_faces(a_,815,904,['happy','smile','grin','proud','content','open_smile'],100+i); T10.append(a_)
    if i%3==0: turn(a_,840+i*3,'happy',0,(-1 if x>0 else 1))
COMBOS+=[(T10[0],878,'tilt_talk',1,'determined'),(T10[4],884,'dip_talk',-1,'proud'),(T10[9],870,'glance_shift',1,'smile')]
path(s,[(815,(GX+0.3,-4.6,2.3),(GX,1.4,1.1)),(904,(GX+0.2,-3.4,2.0),(GX,1.4,1.15))])
# ---- S11 (898-950): "in the same building as the paper": exterior, both signs on one building, lit windows, pull back ----
s='S11'; r=S(s)
path(s,[(898,(RX-1.6,2.2,2.4),(RX+0.4,6.1,3.9)),(950,(RX-2.0,-0.8,2.1),(RX+0.5,6.1,4.0))])
leaves('S11_leaf',RX,4.4,4,898,950,11,coll=C(s))
# ---- S12 (944-985): "and made a club": all twelve cheer (approved victory_up), the ledger signed ----
s='S12'; r=S(s)
for i,(k,(x,y)) in enumerate(zip(TWELVE,SEATS)):
    a_=char_on(f'S12_{k}',k,s,(GX+x,y,0),r,'happy'); faces(a_,[(944,'happy'),(964,'laugh')]); T12.append(a_)
    COMBOS.append((a_,962+(i%4),'victory_up',(1 if i%2 else -1),'laugh'))
path(s,[(944,(GX+0.2,-3.0,1.7),(GX,1.4,1.3)),(985,(GX+0.25,-2.8,1.65),(GX,1.4,1.32))])
# ---- S13 (985-1125): no field, so nine days later: the old bike track by day; the team in plain white shirts walks onto the turf ----
s='S13'; r=S(s)
T13=[]
for i,(k,(x,y)) in enumerate(zip(['heroK','palK','keeper','heroK','palK'],[(-14,-4.6),(-15.2,-5.2),(-16.4,-4.4),(-17.6,-5.0),(-18.6,-4.5)])):
    a_=char_on(f'S13_t{i}',k,s,(VX+x,y,0),r,'happy'); T13.append(a_); walk_far(a_,1035+i*4,1125,'walk',1,'happy')
    drift_faces(a_,985,1125,['happy','proud','determined','grin'],130+i)
path(s,[(985,(VX-2,-15.0,9.5),(VX,0,0.5)),(1050,(VX-11,-12.5,3.6),(VX-14,-3,1.0)),(1125,(VX-13.6,-8.6,1.6),(VX-14.6,-4.7,1.2))])
# ---- S14 (1125-1192): against a team of Englishmen who lived in town: green shirts, arms crossed, smug ----
s='S14'; r=S(s)
E14=[]
for i,(k,(x,y)) in enumerate(zip(['engT1','engT2','engT1'],[(-0.6,0.4),(0.7,0.9),(1.8,1.6)])):
    a_=char_on(f'S14_e{i}',k,s,(VX+4+x,y,0),r,'smug'); E14.append(a_); faces(a_,[(1125,'smug'),(1160,'smug_grin')])
COMBOS+=[(E14[0],1140,'cross_arms_huff',1,'smug'),(E14[1],1150,'akimbo_scold',-1,'smug_grin'),(E14[2],1146,'tilt_talk',-1,'smug')]
path(s,[(1125,(VX+3.9,-3.2,1.3),(VX+4.4,0.8,1.2)),(1192,(VX+4.0,-2.6,1.28),(VX+4.4,0.8,1.22))])
# ---- S15 (1186-1268): "and they lost, one to nothing": the ball flies past our keeper between the posts; chalk score insert at the end ----
s='S15'; r=S(s)
kp=char_on('S15_keeper','keeper',s,(VX-20+0.8,-0.6,0),r,'determined')
faces(kp,[(1186,'determined'),(1199,'shock'),(1218,'sad'),(1240,'wince')]); COMBOS.append((kp,1197,'startle_recoil',1,'shock'))
BALL=sph('S15_ball',(VX-12,1.5,0.4),0.11,flat('leather',lin((150,96,52)),0.7),coll=C(s))
for f,(x,y,z) in [(1186,(VX-12,1.5,0.4)),(1192,(VX-14.5,1.2,1.0)),(1198,(VX-17,0.9,1.5)),(1203,(VX-19.6,0.6,1.6)),(1207,(VX-20.6,0.5,0.6)),(1212,(VX-21.2,0.4,0.12)),(1268,(VX-21.2,0.4,0.12))]: kloc(BALL,f,(x,y,z))
onone(BALL)
path(s,[(1186,(VX-15.5,-5.5,1.5),(VX-19.4,0.2,1.2)),(1220,(VX-16.2,-4.6,1.45),(VX-19.6,0.0,1.2)),(1226,(VX-12.15,5.4,1.7),(VX-12,9.6,1.7)),(1268,(VX-12.1,5.8,1.7),(VX-12,9.6,1.7))])
hardcut(s,1226)   # cut to the chalk 0-1 board on "one to nothing"
# ---- S16 (1268-1330): the turn: "Most folks would have quit right there." The team sits on the turf, glum ----
s='S16'; r=S(s)
D16=[]
for i,(k,(x,y)) in enumerate(zip(['heroK','palK','keeper'],[(-0.8,0.6),(0.4,0.2),(1.4,0.9)])):
    a_=char_on(f'S16_t{i}',k,s,(VX-8+x,y,0),r,'sad'); D16.append(a_); faces(a_,[(1268,'sad'),(1298,'sigh'),(1316,'sad')])
COMBOS+=[(D16[0],1290,'dip_talk',1,'sad'),(D16[2],1300,'glance_shift',-1,'sigh')]
look(D16[1],1268,'sad',-1); turn(D16[1],1306,'sad',-1,1)
path(s,[(1268,(VX-7.6,-3.6,1.6),(VX-7.6,0.5,1.0)),(1330,(VX-7.65,-2.6,1.45),(VX-7.6,0.5,1.05))])
# ---- S17 (1330-1420): "Not them." He jumps up pointing (eureka); they kept on playing week after week: the team jogs past ----
s='S17'; r=S(s)
h17=char_on('S17_hero','heroK',s,(VX-8,0.4,0),r,'determined',arms=('arm','arm'))
faces(h17,[(1330,'determined'),(1340,'grin')]); COMBOS.append((h17,1333,'eureka_point_up',1,'determined'))
J17=[]
for i,(k,(x,y)) in enumerate(zip(['palK','keeper','heroK','palK'],[(-13,1.6),(-14.2,2.2),(-15.6,1.9),(-16.8,2.6)])):
    a_=char_on(f'S17_j{i}',k,s,(VX+x,y,0),r,'happy'); J17.append(a_)
    f=1356+i*3
    while f+36<=1420: COMBOS.append((a_,f,'jog',1,'happy')); kloc(a_['root'],f,(VX+x+(f-1356-i*3)*0.06,y,0)); f+=36
    kloc(a_['root'],1420,(VX+x+(1420-1356-i*3)*0.06,y,0))
    for fc in a_['root'].animation_data.action.fcurves:
        for kp in fc.keyframe_points: kp.interpolation='LINEAR'
path(s,[(1330,(VX-8.4,-3.4,1.25),(VX-8,0.4,1.3)),(1352,(VX-9.6,-4.6,1.45),(VX-10,1.4,1.1)),(1420,(VX-8.2,-4.2,1.45),(VX-9.0,1.8,1.1))])
# ---- S18 (1414-1500): "Then the crowds came, so they built bigger stadiums": the big bowl, crane up and back over the pitch ----
s='S18'; r=S(s)
B18=[]
for i,(k,(x,y)) in enumerate(zip(['heroK','palK','keeper'],[(-1.0,0.4),(0.2,0.0),(1.3,0.6)])):
    a_=char_on(f'S18_t{i}',k,s,(BX+x,y,0),r,'happy'); B18.append(a_); faces(a_,[(1414,'happy'),(1440,'laugh')])
COMBOS+=[(B18[0],1440,'wave_hello',1,'happy'),(B18[1],1444,'victory_up',1,'laugh'),(B18[2],1452,'clap',-1,'laugh')]
path(s,[(1414,(BX+0.2,-3.0,1.4),(BX,0.4,1.3)),(1446,(BX+0.4,-5.0,2.0),(BX,2,2.2)),(1500,(BX+0.6,-8.5,3.4),(BX,6,4.2))])
# ---- S19 (1500-1640): the reveal at the Rambla kiosk today: the vendor shows two visitors the old ad; "that little club ... is FC Barcelona" ----
s='S19'; r=S(s)
vd=char_on('S19_vendor','vendor',s,(KX+0.2,-0.85,0.08),r,'smug',arms=('arm_paper','arm')); tw=char_on('S19_tourW','tourW',s,(KX+1.5,-1.75,0.08),r,'happy'); tm=char_on('S19_tourM','tourM',s,(KX+2.4,-1.45,0.08),r,'skeptical')
faces(vd,[(1500,'smug'),(1530,'grin'),(1592,'smug_grin'),(1614,'wink_grin'),(1626,'smug')]); look(vd,1500,'smug',1)
faces(tw,[(1500,'happy'),(1540,'surprise'),(1586,'shock'),(1614,'stunned'),(1630,'laugh')]); faces(tm,[(1500,'skeptical'),(1550,'neutral'),(1586,'shock'),(1616,'stunned'),(1632,'cry_laugh')])
look(tw,1500,'happy',-1); look(tm,1500,'skeptical',-2)
COMBOS+=[(tw,1584,'startle_recoil',1,'shock'),(tm,1587,'double_take',-1,'shock'),(vd,1612,'tilt_talk',1,'wink_grin')]
path(s,[(1500,(KX+1.1,-5.4,1.45),(KX+1.1,-1.2,1.3)),(1586,(KX+1.2,-4.6,1.42),(KX+1.2,-1.3,1.3)),(1640,(KX+1.25,-4.3,1.4),(KX+1.2,-1.3,1.3))])
leaves('S19_leaf',KX+1,-1.5,6,1500,1640,19,coll=C(s))
# ---- S20 (1634-1767): payoff: "it all kicked off with one lonely guy's ad in the paper": push to the poster on the kiosk; lands on "paper" ----
s='S20'; r=S(s)
t20=char_on('S20_tourW','tourW',s,(PXc+1.3,PYc-1.7,0.08),r,'happy'); m20=char_on('S20_tourM','tourM',s,(PXc+1.9,PYc+1.6,0.08),r,'grin')
faces(t20,[(1634,'happy'),(1690,'grin')]); faces(m20,[(1634,'grin'),(1700,'happy')]); look(t20,1634,'happy',-2); look(m20,1634,'grin',-2)
COMBOS+=[(t20,1660,'point_out_tilt',-1,'excited')]
path(s,[(1634,(PXc+5.2,PYc-0.9,1.6),(PXc,PYc,1.55)),(1736,(PXc+2.15,PYc-0.05,1.6),(PXc,PYc,PZ-0.18)),(END,(PXc+2.05,PYc-0.04,1.6),(PXc,PYc,PZ-0.18))])
leaves('S20_leaf',PXc+1.5,PYc,5,1634,END,20,coll=C(s))
# ======================= ground snap (characters stand on the floor/sidewalk they are over) =======================
CHRN=set()
def _ground(x,y,f,z0):
    sc.frame_set(f); dg=bpy.context.evaluated_depsgraph_get(); o_=Vector((x,y,z0+1.2))
    for k in range(40):
        ok,loc,nrm,i,ob,m=sc.ray_cast(dg,o_,Vector((0,0,-1)))
        if not ok: return None
        o_=loc+Vector((0,0,-0.001))
        if ob.name in CHRN or ob.name.endswith('_ink') or ob.get('fly') or ob.hide_render or ob.type!='MESH': continue
        if ob.get('noink') and len(ob.data.vertices)<=4 and not ob.name.startswith(('R_','K_','N_','G_','V_','B_')): continue
        if ob.name.startswith(('S','N_paper','N_flame','G_ledger')) and len(ob.data.vertices)<=4: continue
        if 'leaf' in ob.name or ob.name.startswith(('G_table','G_bench','N_counter','N_desk','K_counter','K_rack','K_awning')): continue
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
        fx_=[fc for fc in r.animation_data.action.fcurves if fc.data_path=='location' and fc.array_index in (0,1)]
        for kp in fcz.keyframe_points:
            f=kp.co[0]; x=fx_[0].evaluate(f); y=fx_[1].evaluate(f); g=_ground(x,y,int(f),kp.co[1])
            if g is not None: kp.co[1]=g; kp.handle_left[1]=g; kp.handle_right[1]=g; n+=1
    print('SNAPPED',n)
snap_all()
# ======================= finish, ink, render settings =======================
for c_,f_,k_,sd_,fc_ in COMBOS: combo(c_,f_,k_,side=sd_,face=fc_)
print('COMBOS',len(COMBOS)+len(WALKS),len(set([k for _,_,k,_,_ in COMBOS]+[w_[2] for w_ in WALKS])))
sc['air']=json.dumps(sorted(L.AIR))
for a in ALL: finish(a)
print('hulls',L.ink())
for o_ in bpy.data.objects:
    if o_.type=='LIGHT' and o_.data.type!='SUN': o_.visible_camera=False
L.render_setup(100,8)
sc.cycles.samples=4; sc.cycles.transparent_max_bounces=8; sc.cycles.diffuse_bounces=1; sc.cycles.max_bounces=3
# r3 (C4 probe, headedge 324 frames): heads cut by the frame edge while the body is on screen; headnudge_cc.py shifts x1.15 (Cape Cod r5 method)
SKB_DEFAULT={"S01": [0.775, 1.031, 1.352], "S02": [0.849, 1.016, 1.287], "S03": [0.884, 1.005, 1.294], "S04": [0.844, 1.017, 1.289], "S05": [0.849, 1.016, 1.287], "S06": [0.849, 1.016, 1.287], "S07": [0.845, 1.018, 1.278], "S08": [0.725, 1.032, 1.495], "S09": [0.744, 1.042, 1.335], "S10": [0.747, 1.023, 1.521], "S11": [0.744, 1.042, 1.335], "S12": [0.752, 1.022, 1.509], "S13": [1.003, 0.984, 1.153], "S14": [0.976, 0.984, 1.228], "S15": [1.007, 0.983, 1.146], "S16": [0.986, 0.985, 1.193], "S17": [0.986, 0.984, 1.196], "S18": [0.962, 0.989, 1.217], "S19": [0.895, 1.005, 1.261], "S20": [0.895, 1.005, 1.261]}   # r3 pass 2 (+ S01 interpolated between pass 2 (0.964/0.91) and pass 3 (0.87/0.80))
NUDGE={"S03_locA": [0.069, 0.006], "S03_locB": [0.324, 0.026], "S04_gymB": [-0.319, 0.071], "S04_hero": [0.22, -0.049], "S09_engA": [0.349, -0.0], "S09_engB": [0.322, -0.0], "S09_german": [-0.162, 0.0], "S09_hero": [-0.34, 0.0], "S09_locA": [-0.301, 0.0], "S09_locB": [-0.292, 0.0], "S09_pal": [0.276, -0.0], "S10_hero": [0.076, 0.003], "S10_locB": [-0.234, -0.01], "S10_locF": [-0.246, -0.01], "S10_swiss2": [0.127, 0.005], "S13_t0": [0.398, 0.102], "S13_t1": [0.463, 0.119], "S13_t2": [0.258, 0.066], "S13_t3": [0.465, 0.119], "S14_e0": [0.302, -0.036], "S14_e2": [-0.207, 0.024], "S16_t0": [0.247, -0.004], "S16_t2": [-0.159, 0.003], "S17_hero": [-0.3, -0.04], "S17_j0": [0.231, 0.031], "S17_j1": [0.317, 0.042], "S19_tourM": [-0.295, -0.005], "S19_vendor": [0.106, 0.002]}
# r3b second headnudge pass, static characters only (walk-ins that start off frame are entrances, not C4 cuts)
for _n,(_dx,_dy) in {"S03_locB":[0.054,0.004],"S04_hero":[0.121,-0.027],"S16_t0":[0.182,-0.003],"S19_tourM":[-0.238,-0.004],"S09_hero":[-0.157,0.0],"S17_hero":[-0.136,-0.018]}.items():
    NUDGE[_n]=[NUDGE.get(_n,[0,0])[0]+_dx,NUDGE.get(_n,[0,0])[1]+_dy]
for _n,(_dx,_dy) in NUDGE.items():
    _o=bpy.data.objects.get(_n)
    if not _o: continue
    _o.location.x+=_dx*1.15; _o.location.y+=_dy*1.15
    _ad=_o.animation_data
    if _ad and _ad.action:
        for _fc in _ad.action.fcurves:
            if _fc.data_path=='location' and _fc.array_index in (0,1):
                for _k in _fc.keyframe_points:
                    _d=(_dx if _fc.array_index==0 else _dy)*1.15; _k.co[1]+=_d; _k.handle_left[1]+=_d; _k.handle_right[1]+=_d
# bcn r3 (rules 335a/355 probe Nov 24): rendered skin was too warm for Rick's on-screen ratios (raw G/R 0.80-0.88, B/R 0.65-0.78 vs 0.92/0.86).
# Per-shot skin balance: head textures are multiplied by the object's own "skb" colour (Attribute node, Object type), set per shot below,
# so one character's material serves every set and each shot's light is balanced on its own (dissolve overlaps render per shot, so frame keys could not do it).
SKB=json.loads(os.environ.get('SKB','{}')) or SKB_DEFAULT
HM=set()
for m_ in bpy.data.materials:
    if not m_.use_nodes: continue
    N_=m_.node_tree.nodes; it_=next((n for n in N_ if n.type=='TEX_IMAGE' and n.image and '_h_' in os.path.basename(n.image.filepath)),None)
    if not it_ or 'skb_mul' in N_: continue
    p_=N_.get('Principled BSDF'); at=N_.new('ShaderNodeAttribute'); at.attribute_type='OBJECT'; at.attribute_name='skb'
    mu=N_.new('ShaderNodeMix'); mu.name='skb_mul'; mu.data_type='RGBA'; mu.blend_type='MULTIPLY'; mu.inputs['Factor'].default_value=1.0
    Lk=m_.node_tree.links; Lk.new(it_.outputs['Color'],mu.inputs[6]); Lk.new(at.outputs['Color'],mu.inputs[7])
    for sock in ('Base Color','Emission Color'):
        for l_ in list(p_.inputs[sock].links): Lk.remove(l_)
        Lk.new(mu.outputs[2],p_.inputs[sock])
    HM.add(m_.name)
nskb=0
for o_ in bpy.data.objects:
    if o_.type=='MESH' and o_.active_material and o_.active_material.name in HM:
        sh_=o_.users_collection[0].name.replace('CHR_',''); o_['skb']=list(SKB.get(sh_,(1.0,1.0,1.0))); nskb+=1
print('SKB objects',nskb,'materials',len(HM))
bpy.ops.wm.save_as_mainfile(filepath='/root/cc/blend/bcn.blend'); print('SCENE_OK all')
