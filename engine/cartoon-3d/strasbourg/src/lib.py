# Shared Blender helpers for the Black Friday short (Rick method: painted 3D sets + flat 2D cut-out cast)
import bpy, bmesh, math, random, json, os
from mathutils import Vector
TX='/root/sb/tex/'
sc=None; C_SET=None; C_NOI=None; MC={}; CHRC={}; CAM={}; TGT={}
def init(end):
    global sc,C_SET,C_NOI
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc=bpy.context.scene; sc.render.fps=30; sc.frame_start=0; sc.frame_end=end
    C_SET=col('SET'); C_NOI=col('NOINK'); return sc
def col(n,parent=None):
    c=bpy.data.collections.new(n); (parent or bpy.context.scene.collection).children.link(c); return c
def put(o,c):
    if c in o.users_collection and len(o.users_collection)==1: return o
    for cc in list(o.users_collection): cc.objects.unlink(o)
    c.objects.link(o); return o
def apply(o):
    bpy.ops.object.select_all(action='DESELECT'); bpy.context.view_layer.objects.active=o; o.select_set(True)
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True); o.select_set(False)
def lin(c): return tuple((v/255)**2.2 for v in c)
def nodes(m): m.use_nodes=True; return m.node_tree.nodes,m.node_tree.links
# ---------------- materials ----------------
def _paint(m,grain=0.10,ao=0.30):
    """round 4: painted look for set materials: low-freq brush grain (object space) + AO crease darkening (Rick's painted sets, not clean CG)."""
    N,L=m.node_tree.nodes,m.node_tree.links; p=N['Principled BSDF']; bc=p.inputs['Base Color']
    if bc.links: src=bc.links[0].from_socket
    else:
        rg=N.new('ShaderNodeRGB'); rg.outputs[0].default_value=tuple(bc.default_value); src=rg.outputs[0]
    tc=N.new('ShaderNodeTexCoord'); nz=N.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value=3.2; nz.inputs['Detail'].default_value=6.0; nz.inputs['Roughness'].default_value=0.62
    L.new(tc.outputs['Object'],nz.inputs['Vector'])
    mr=N.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value=0.3; mr.inputs['From Max'].default_value=0.7; mr.inputs['To Min'].default_value=1-grain; mr.inputs['To Max'].default_value=1+grain*0.6
    L.new(nz.outputs['Fac'],mr.inputs['Value'])
    # round 5 (A2/A4): fine grit in object space (~1-3 cm features) so near surfaces carry painted detail, not flat CG colour
    nf=N.new('ShaderNodeTexNoise'); nf.inputs['Scale'].default_value=55.0; nf.inputs['Detail'].default_value=8.0; nf.inputs['Roughness'].default_value=0.75
    L.new(tc.outputs['Object'],nf.inputs['Vector'])
    mf=N.new('ShaderNodeMapRange'); mf.inputs['From Min'].default_value=0.35; mf.inputs['From Max'].default_value=0.65; mf.inputs['To Min'].default_value=0.76; mf.inputs['To Max'].default_value=1.10   # r6: stronger grit (round-5 surface detail 17.9 vs Rick 75+)
    L.new(nf.outputs['Fac'],mf.inputs['Value'])
    vo=N.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value=140.0; L.new(tc.outputs['Object'],vo.inputs['Vector'])
    vr=N.new('ShaderNodeMapRange'); vr.inputs['From Min'].default_value=0.0; vr.inputs['From Max'].default_value=0.12; vr.inputs['To Min'].default_value=0.58; vr.inputs['To Max'].default_value=1.0
    L.new(vo.outputs['Distance'],vr.inputs['Value'])
    mg=N.new('ShaderNodeMath'); mg.operation='MULTIPLY'; L.new(mf.outputs['Result'],mg.inputs[0]); L.new(vr.outputs['Result'],mg.inputs[1])
    # r6: vertical brush streaks (stretched noise) + fine speckle, the painted surface marks Rick's sets carry
    ms=N.new('ShaderNodeMapping'); ms.inputs['Scale'].default_value=(34.0,34.0,3.0); L.new(tc.outputs['Object'],ms.inputs['Vector'])
    ns=N.new('ShaderNodeTexNoise'); ns.inputs['Scale'].default_value=1.0; ns.inputs['Detail'].default_value=10.0; ns.inputs['Roughness'].default_value=0.7; L.new(ms.outputs['Vector'],ns.inputs['Vector'])
    rs=N.new('ShaderNodeMapRange'); rs.inputs['From Min'].default_value=0.3; rs.inputs['From Max'].default_value=0.7; rs.inputs['To Min'].default_value=0.84; rs.inputs['To Max'].default_value=1.10; L.new(ns.outputs['Fac'],rs.inputs['Value'])
    nk=N.new('ShaderNodeTexNoise'); nk.inputs['Scale'].default_value=260.0; nk.inputs['Detail'].default_value=2.0; L.new(tc.outputs['Object'],nk.inputs['Vector'])
    rk=N.new('ShaderNodeMapRange'); rk.inputs['From Min'].default_value=0.35; rk.inputs['From Max'].default_value=0.65; rk.inputs['To Min'].default_value=0.88; rk.inputs['To Max'].default_value=1.06; L.new(nk.outputs['Fac'],rk.inputs['Value'])
    mg3=N.new('ShaderNodeMath'); mg3.operation='MULTIPLY'; L.new(mg.outputs[0],mg3.inputs[0]); L.new(rs.outputs['Result'],mg3.inputs[1])
    mg4=N.new('ShaderNodeMath'); mg4.operation='MULTIPLY'; L.new(mg3.outputs[0],mg4.inputs[0]); L.new(rk.outputs['Result'],mg4.inputs[1])
    mg2=N.new('ShaderNodeMath'); mg2.operation='MULTIPLY'; L.new(mg4.outputs[0],mg2.inputs[0]); L.new(mr.outputs['Result'],mg2.inputs[1])
    a=N.new('ShaderNodeAmbientOcclusion'); a.samples=6; a.inputs['Distance'].default_value=0.35
    ar=N.new('ShaderNodeMapRange'); ar.inputs['To Min'].default_value=1-ao; ar.inputs['To Max'].default_value=1.0
    L.new(a.outputs['AO'],ar.inputs['Value'])
    m1=N.new('ShaderNodeMix'); m1.data_type='RGBA'; m1.blend_type='MULTIPLY'; m1.inputs['Factor'].default_value=1.0
    L.new(src,m1.inputs[6]); L.new(mg2.outputs[0],m1.inputs[7])
    m2=N.new('ShaderNodeMix'); m2.data_type='RGBA'; m2.blend_type='MULTIPLY'; m2.inputs['Factor'].default_value=1.0
    L.new(m1.outputs[2],m2.inputs[6]); L.new(ar.outputs['Result'],m2.inputs[7])
    L.new(m2.outputs[2],bc)
    return m
PAINT=True
def surf(name,img,tile,rough=0.85,rot=0.0,gen=False,emit=0.0):
    """tiled painted texture, box projected. gen=True fits the image once over the object's bounding box."""
    key=name
    if key in MC: return MC[key]
    m=bpy.data.materials.new(name); N,L=nodes(m); p=N['Principled BSDF']; p.inputs['Roughness'].default_value=rough
    p.inputs['Specular IOR Level'].default_value=0.2
    tc=N.new('ShaderNodeTexCoord'); mp=N.new('ShaderNodeMapping')
    if gen: L.new(tc.outputs['Generated'],mp.inputs['Vector'])
    else:
        L.new(tc.outputs['Object'],mp.inputs['Vector']); mp.inputs['Scale'].default_value=(1/tile[0],1/tile[1],1/tile[1]); mp.inputs['Rotation'].default_value=(0,0,rot)
    it=N.new('ShaderNodeTexImage'); it.image=bpy.data.images.load(TX+img+'.png',check_existing=True); it.projection='BOX'; it.projection_blend=0.1
    L.new(mp.outputs['Vector'],it.inputs['Vector']); L.new(it.outputs['Color'],p.inputs['Base Color'])
    if emit: L.new(it.outputs['Color'],p.inputs['Emission Color']); p.inputs['Emission Strength'].default_value=emit
    if PAINT and not emit: _paint(m)
    MC[key]=m; return m
def flat(name,rgb,rough=0.7,emit=0.0,metal=0.0):
    if name in MC: return MC[name]
    m=bpy.data.materials.new(name); N,L=nodes(m); p=N['Principled BSDF']
    p.inputs['Base Color'].default_value=(*rgb,1); p.inputs['Roughness'].default_value=rough; p.inputs['Metallic'].default_value=metal
    p.inputs['Specular IOR Level'].default_value=0.3
    if emit: p.inputs['Emission Color'].default_value=(*rgb,1); p.inputs['Emission Strength'].default_value=emit
    if PAINT and not emit and not metal: _paint(m)
    MC[name]=m; return m
def card_mat(name,img,emit=0.3,rough=1.0):
    if name in MC: return MC[name]
    m=bpy.data.materials.new(name); N,L=nodes(m); p=N['Principled BSDF']; p.inputs['Roughness'].default_value=rough
    p.inputs['Specular IOR Level'].default_value=0.0
    it=N.new('ShaderNodeTexImage'); it.image=bpy.data.images.load(img if img.startswith('/') else TX+img+'.png',check_existing=True); it.interpolation='Cubic'
    L.new(it.outputs['Color'],p.inputs['Base Color']); L.new(it.outputs['Alpha'],p.inputs['Alpha'])
    if emit: L.new(it.outputs['Color'],p.inputs['Emission Color']); p.inputs['Emission Strength'].default_value=emit
    MC[name]=m; return m
# ---------------- geometry (bmesh, no operators: fast with thousands of objects) ----------------
from mathutils import Matrix, Euler
def _obj(n,bm,m,coll,smooth=False):
    me=bpy.data.meshes.new(n); bm.to_mesh(me); bm.free()
    if smooth:
        for f in me.polygons: f.use_smooth=True
    o=bpy.data.objects.new(n,me); (coll or C_SET).objects.link(o); me.materials.append(m); return o
def box(n,c,s,m,coll=None,bv=0.03,seg=2):
    bm=bmesh.new(); bmesh.ops.create_cube(bm,size=1.0); bmesh.ops.scale(bm,vec=Vector(s),verts=bm.verts)
    o=_obj(n,bm,m,coll); o.location=c
    if bv: b=o.modifiers.new('bv','BEVEL'); b.width=bv; b.segments=seg; b.limit_method='ANGLE'
    return o
def cyl(n,c,r,d,m,v=24,coll=None,r2=None,rot=(0,0,0)):
    bm=bmesh.new(); bmesh.ops.create_cone(bm,cap_ends=True,cap_tris=False,segments=v,radius1=r,radius2=(r if r2 is None else r2),depth=d)
    bmesh.ops.rotate(bm,cent=(0,0,0),matrix=Euler(rot).to_matrix(),verts=bm.verts)
    o=_obj(n,bm,m,coll,smooth=v>12); o.location=c
    if v>12:
        try: o.data.set_sharp_from_angle(angle=math.radians(40))
        except Exception: pass
    return o
def sph(n,c,r,m,sc_=(1,1,1),coll=None,seg=16):
    bm=bmesh.new(); bmesh.ops.create_uvsphere(bm,u_segments=seg,v_segments=max(6,seg//2),radius=r)
    bmesh.ops.scale(bm,vec=Vector(sc_),verts=bm.verts); o=_obj(n,bm,m,coll,smooth=True); o.location=c; return o
FACING={'-Y':0.0,'+X':math.pi/2,'+Y':math.pi,'-X':-math.pi/2}
def plane(n,c,w,h,m,coll=None,face='-Y',horiz=False):
    """card whose front (readable side, UV upright) faces the given axis; horiz=True lies flat, image up = +Y"""
    me=bpy.data.meshes.new(n); vs=[(-w/2,-h/2,0),(w/2,-h/2,0),(w/2,h/2,0),(-w/2,h/2,0)]
    me.from_pydata(vs,[],[(0,1,2,3)]); uv=me.uv_layers.new(name='UVMap')
    for i,co in enumerate([(0,0),(1,0),(1,1),(0,1)]): uv.data[i].uv=co
    if not horiz: me.transform(Matrix.Rotation(FACING[face],4,'Z')@Matrix.Rotation(math.pi/2,4,'X'))
    o=bpy.data.objects.new(n,me); (coll or C_SET).objects.link(o); me.materials.append(m); o.location=c; return o
def vis(o,ranges):
    """hide_render keyed so the object shows only inside the given frame ranges (merged, sorted)"""
    rs=sorted([list(r) for r in ranges if r[1]>=r[0]]); M=[]
    for a,b in rs:
        if M and a<=M[-1][1]+1: M[-1][1]=max(M[-1][1],b)
        else: M.append([a,b])
    o.hide_render=True; o.keyframe_insert('hide_render',frame=-1)
    for a,b in M:
        o.hide_render=False; o.keyframe_insert('hide_render',frame=a)
        o.hide_render=True; o.keyframe_insert('hide_render',frame=b+1)
    for fc in o.animation_data.action.fcurves:
        if fc.data_path=='hide_render':
            for kp in fc.keyframe_points: kp.interpolation='CONSTANT'
    o['vis']=json.dumps(M)
def kloc(o,f,loc,interp=None):
    o.location=loc; o.keyframe_insert('location',frame=f)
def krot(o,f,rot): o.rotation_euler=rot; o.keyframe_insert('rotation_euler',frame=f)
def kscale(o,f,s): o.scale=s; o.keyframe_insert('scale',frame=f)
def linear(o):
    if o.animation_data and o.animation_data.action:
        for fc in o.animation_data.action.fcurves:
            if fc.data_path!='hide_render':
                for kp in fc.keyframe_points: kp.interpolation='LINEAR'
def empty(n,loc=(0,0,0),parent=None,coll=None):
    e=bpy.data.objects.new(n,None); (coll or C_SET).objects.link(e); e.location=loc
    if parent: e.parent=parent
    return e
# ---------------- cameras ----------------
def cam(n,lens,fs=5.6):
    cd=bpy.data.cameras.new('cam_'+n); cd.lens=lens; cd.dof.use_dof=True; cd.dof.aperture_fstop=fs; cd.clip_start=0.05; cd.clip_end=800
    co=bpy.data.objects.new('cam_'+n,cd); sc.collection.objects.link(co); tg=bpy.data.objects.new('tgt_'+n,None); sc.collection.objects.link(tg)
    c=co.constraints.new('TRACK_TO'); c.target=tg; c.track_axis='TRACK_NEGATIVE_Z'; c.up_axis='UP_Y'; cd.dof.focus_object=tg
    CAM[n]=co; TGT[n]=tg; return co,tg
TILT=json.load(open('/root/sb/src/tilt.json')) if os.path.exists('/root/sb/src/tilt.json') else {}
def path(n,keys):
    """keys: (frame, cam_loc, target_loc[, lens])"""
    co,tg=CAM[n],TGT[n]
    for k in keys:
        f,l,t=k[:3]
        dv=TILT.get(n,0)   # det r4 (text T1): tilt down so faces clear the 71.7 % caption band (tiltcalc.py writes tilt.json)
        if dv:
            ln=k[3] if len(k)>3 else co.data.lens; dist=math.dist(l,t); t=(t[0],t[1],t[2]-dv*36.0/ln*dist)
        kloc(co,f,l); kloc(tg,f,t)
        if len(k)>3: co.data.lens=k[3]; co.data.keyframe_insert('lens',frame=f)
# ---------------- 2D cut-out cast ----------------
import expressions as XL   # Rick-style expression library: adds LIBRARY faces to characters with "library" in cast.json
CI=XL.expand(json.load(open('/root/sb/src/cast.json')))
# r7 (round-6 visual: round bodies torso 0.63, legs 0.88 head-heights; need 0.7-1.05 / 0.9-1.5): round body cards stretched 1.118x up from the feet
BSY={'tall':1.045,'short':1.045,'round':1.045}   # sb: rule 336/350 merge of DC 09eca41 (torso ~1.0 H, legs ~1.25 H, total ~3.25 H); was 0.91
ARM_Q=0.91   # arm and pose cards keep their rule-329 size (limb width)   # det r4: body cards z 0.91 about the feet (torso/legs were 1.10/1.36 head widths)
BSY0=1.0   # r8b: one Rick build for every kind (cast.py GB/HEMY), no stretch
# r8b (owner Nov 20: clone Rick's build; guide v1.3 x.3): head 0.43 m wide = H; torso 0.962->0.532 = 1.00 H; legs 0.532->-0.014 = 1.27 H;
# head disc centre 1.167 (top 1.382): total 3.25 H. Shoulder pivots 0.95, hand (HAND_Z 0.407) at the hem.
HS=0.43/0.586   # head card scale vs rounds 1-7 (disc 800/1024 of a 0.75 card)
GEO={'tall':(0.966,0.150,0.868),'short':(0.966,0.156,0.868),'round':(0.966,0.154,0.868)}   # sb: DC 09eca41 pivots for the rule-336 torso   # r7b (owner Nov 22 sheet comment 'arm issue?': arm roots poked out above the rounded shoulders): shoulder pivot 0.92 -> 0.86 and x out to the outline (0.126/0.142/0.151 -> 0.141/0.156/0.165) so the arm stroke grows out of the side outline instead of a parallel line with a sliver.   # r7det (rule 329, Rick f606: head overlaps the capsule top ~0.3 H): head and shoulders 0.03 lower; was 0.996/0.95
#   # r9: shoulders follow the narrower torso (0.73-0.89 H)
# r5b (owner Nov 23 test clip, rule 354b): both arm pivots sat at y -0.006, so the two arm cards were COPLANAR; where one arm's
# transparent canvas overlapped the other arm's ink, Cycles skipped the ink on some samples (grey, see-through arm, hand 'behind' the body).
# Every card of one character now has its own depth: body 0 > left arm -0.004 > right arm -0.006 > pose cards 3.5 mm nearer still > face -0.012.
ARM_Y={-1:-0.004,1:-0.006}; POSE_DY=-0.0035
# r8b (owner review 2, Nov 23 14:46Z: clap hands higher and touching, chin taps higher on the face): these four pose drawings sit IN
# FRONT of the face disc (-12 mm) and behind the head effects (-16 mm): left -13.25, right -14.75 mm (rule 354b gaps >= 1.25 mm).
# Exception to rule 268 for these poses only (= cast.FRONT_POSES).
FRONT_POSES={'clap_up_open','clap_up','chin_hi','chin_hi_tap'}; FRONT_Y={-1:-0.01325,1:-0.01475}
BACK_Y=0.00275   # r10 walk: leading-side arm card 2.75 mm behind the body card (1.25 mm from the legs card and the 'behind' fx layer)   # depths -4, -6, -7.5, -9.5 mm: every pair >= 1.5 mm apart, all behind the face (-12)
FOOT_LIFT=0.0173   # r5b (owner Nov 23: 'feet clipping through the floor'): drawn foot bottom sat at z -0.016 (over half the 2.9 cm foot under the floor); now +0.001
ARM_W,ARM_H,ARM_OFF=0.744,0.558,0.242   # r6: arm canvas 1200 wide (bent forearm swings outward)
SHADOW=None
def chr_coll(shot):
    if shot not in CHRC: CHRC[shot]=col('CHR_'+shot)
    return CHRC[shot]
# r11 (owner Nov 23 3:40 PM CT: "when the people walk really closely together ... their overlapping shadows cause the shadow to kind of
# disappear or glitch out"): every ground blob sat at z 0.004, so two overlapping blobs were coplanar transparent cards and Cycles
# flickered between them. Each character now gets its own blob height, 1.3 mm apart (2.5-6.4 mm above the floor, under every card),
# and rigcheck SHADOW_OVERLAP fails any two overlapping blobs closer than 1 mm in height.
_SHN=[0]
def _shadow_z():
    z=0.0025+0.0013*(_SHN[0]%4); _SHN[0]+=1; return z

def char(inst,kind,shot,loc,rng,face0=None,arms=('arm','arm'),scale=1.0,walker=False,camname=None):
    c=CI[kind]; top,shx,shz=GEO[c['body']]; _q=BSY[c['body']]; top=-0.04+(top+0.04)*_q+FOOT_LIFT; shz=-0.04+(shz+0.04)*_q+FOOT_LIFT; C=chr_coll(shot)
    root=empty(inst,loc,coll=C); root.scale=(scale,)*3
    bb=root.constraints.new('LOCKED_TRACK'); bb.target=CAM[camname or shot]; bb.track_axis='TRACK_NEGATIVE_Y'; bb.lock_axis='LOCK_Z'
    bodies={}
    for key in (['body','bodyw1','bodyw2'] if walker else ['body']):
        sy=BSY[c['body']]; b=plane(f'{inst}_{key}',(0,0,0),0.8,1.1*sy,card_mat(f'{kind}_{key}',f'{kind}_{key}'),coll=C); b.parent=root; b.location=(0,0,-0.04+0.55*sy+FOOT_LIFT); bodies[key]=b
    hp=empty(inst+'_hp',(0,0,top),root,coll=C)
    neck=plane(inst+'_head',(0,0,0),0.16*HS,0.16*HS,flat('skin',lin((252,246,236)),0.9),coll=C); neck.parent=hp; neck.location=(0,0.004,0.04)
    F={}
    for fk in c['faces']:
        _pt,_pb=XL.pads(c)   # round 3: tall hats/hair/beards use a taller head texture; card grows by the same ratio, head disc stays put
        f=plane(f'{inst}_d_{fk}',(0,0,0),0.75*HS,0.75*HS*(1024+_pt+_pb)/1024,card_mat(f'{kind}_h_{fk}',f'{kind}_h_{fk}',emit=0.25),coll=C); f.parent=hp; f.location=(0,-0.012,0.2535*HS+0.75*HS*(_pt-_pb)/2048); F[fk]=f
    A={}
    for sx,ak in zip((-1,1),arms):
        # r7 (rule 268): arms sit BEHIND the face disc (face -0.012) and in front of the body (0): a raised hand can never paint over its own face
        ap=empty(f'{inst}_ap{sx}',(sx*shx,ARM_Y[sx],shz),root,coll=C); A[sx]={'piv':ap,'cards':{}}
        keys=[ak] if isinstance(ak,str) else sorted(set(k for _,k in ak))
        if 'armS' not in keys: keys=keys+['armS']   # r7: straight card swapped in automatically while the arm is raised past 70 deg
        for k in keys:
            tk=f'{kind}_{k}'+('_L' if sx<0 else '')   # r7 (rule 272): mirrored texture, never a negative scale
            a=plane(f'{inst}_arm{sx}_{k}',(0,0,0),ARM_W*ARM_Q,ARM_H*ARM_Q,card_mat(tk,tk),coll=C); a.parent=ap; a.location=(0,0,-ARM_OFF*ARM_Q)
            a.visible_shadow=False   # r7b (owner Nov 22 'arm issue?'): the sun cast the arm card's shadow onto the torso as a dark notch on the lit side; Rick's arms cast none
            A[sx]['cards'][k]=a
        A[sx]['sched']=[(rng[0],ak)] if isinstance(ak,str) else ak
    sh=plane(inst+'_shadow',(0,0,0),1.0,0.45,card_mat('shadowblob','shadow',emit=0.0),coll=C,horiz=True); sh.parent=root; sh.location=(0,0,_shadow_z())   # r11: each character's blob on its own height, so two blobs never share a plane
    sh.visible_shadow=False   # r5b (owner Nov 23 'box-like shadow on the ground'): the flat blob card blocked the sun over its whole rectangle, so a dark box sat under every character
    ch=dict(inst=inst,kind=kind,root=root,hp=hp,F=F,A=A,bodies=bodies,rng=rng,faces=[],walk=[],neck=neck,shadow=sh,top=top,shot=shot)
    if face0: ch['faces'].append((rng[0],face0))
    for sx in (-1,1): krot(A[sx]['piv'],rng[0],(0,math.radians(-8)*sx,0))
    return ch
def face(ch,f,k):
    if k not in ch['F']:
        alt={'shock':['horror','wow','raise'],'happy':['hope','cheer','excited','grin'],'cheer':['happy','excited'],'laugh':['happy','cheer'],'sad':['deadpan','worry'],'smug':['grin','happy']}.get(k,[])
        alt=alt+XL.alternates(k)   # library: same-family fallback before the first face
        k=next((a for a in alt if a in ch['F']),list(ch['F'])[0])
    ch['faces'].append((f,k))
def faces(ch,seq):
    for f,k in seq: face(ch,f,k)
def arm(ch,sx,f,deg): krot(ch['A'][sx]['piv'],f,(0,math.radians(deg)*sx,0))
def bob(ch,frames,amt=7):
    hp=ch['hp']
    for f in frames:
        krot(hp,f,(0,0,0)); krot(hp,f+3,(math.radians(-amt),0,math.radians(amt*0.4))); krot(hp,f+6,(math.radians(amt*0.4),0,math.radians(-amt*0.15))); krot(hp,f+9,(0,0,0))
def walk(ch,f0,f1,p0,p1,step=4,swing=(-1,1)):
    """root moves p0->p1 linearly; body card cycles stride poses so the feet step (rule 162)"""
    r=ch['root']; kloc(r,f0,p0); kloc(r,f1,p1)
    for fc in r.animation_data.action.fcurves:
        if fc.data_path=='location':
            for kp in fc.keyframe_points:
                if kp.co[0] in (f0,f1): kp.interpolation='LINEAR'
    ch['walk'].append((f0,f1,step))
    for i,f in enumerate(range(f0,f1,step*2)):
        for sx in swing: krot(ch['A'][sx]['piv'],f,(0,math.radians(-(16 if (i%2)==(sx>0) else 2))*sx,0))   # round 4: a working arm (chalk) is left out of the stride swing
def finish(ch,blink_every=34):
    a,b=ch['rng']
    # faces: sorted, inside range, auto blinks so no face holds longer than ~1.3 s (rule 185), exactly one per frame (rule 168)
    seq=sorted(ch['faces'],key=lambda x:x[0]); seq=[(max(a,f),k) for f,k in seq if f<=b]
    if not seq: seq=[(a,list(ch['F'])[0])]
    seq[0]=(a,seq[0][1]); ded={}
    for f,k in seq: ded[f]=k
    seq=sorted(ded.items())
    out=[]
    for i,(f,k) in enumerate(seq):
        nx=seq[i+1][0] if i+1<len(seq) else b+1
        out.append((f,k)); t=f+blink_every
        bk='blink'+(k[k.index('@'):] if '@' in k else '')   # round 5 proposal: a turned face blinks at its own angle (keys with '@' exist only with cast.json "turns")
        if bk not in ch['F']: bk='blink'
        if 'blink' in ch['F'] and not k.startswith('blink'):
            while t+2<nx-6: out.append((t,bk)); out.append((t+2,k)); t+=blink_every+((t//7)%9)
    R={}
    for i,(f,k) in enumerate(out):
        nx=out[i+1][0] if i+1<len(out) else b+1
        R.setdefault(k,[]).append((f,nx-1))
    for k,o in ch['F'].items(): vis(o,R.get(k,[]))
    ch['face_seq']=out
    # bodies (stride poses while walking)
    st={}
    for f in range(a,b+1): st[f]='body'
    for f0,f1,step in ch['walk']:
        for f in range(f0,min(f1,b+1)):
            ph=((f-f0)//step)%4; st[f]=['bodyw1','body','bodyw2','body'][ph]
    BR={}
    cur=None
    for f in range(a,b+1):
        if st[f]!=cur: BR.setdefault(st[f],[]).append([f,f]); cur=st[f]
        else: BR[cur][-1][1]=f
    for k,o in ch['bodies'].items(): vis(o,BR.get(k,[]))
    vis(ch['neck'],[(a,b)]); vis(ch['shadow'],[(a,b)])
    for sx in (-1,1):
        s=sorted(ch['A'][sx]['sched'])
        cur={}
        for i,(f,k) in enumerate(s):
            nx=s[i+1][0] if i+1<len(s) else b+1
            for g in range(max(a,f),min(nx,b+1)): cur[g]=k
        # r7 (rule 269): a raised arm (|angle| > 70 deg) shows the straight card so the bent forearm never folds over the head
        piv=ch['A'][sx]['piv']; fc=None
        if piv.animation_data and piv.animation_data.action:
            fc=next((c for c in piv.animation_data.action.fcurves if c.data_path=='rotation_euler' and c.array_index==1),None)
        if fc and not ch.get('keep_arm_cards'):
            for g in range(a,b+1):
                if cur.get(g)=='arm' and abs(fc.evaluate(g))>math.radians(70): cur[g]='armS'
        AR={}; prev=None
        for g in range(a,b+1):
            k=cur.get(g,prev)
            if k!=prev or not AR.get(k) or AR[k][-1][1]!=g-1: AR.setdefault(k,[]).append([g,g])
            else: AR[k][-1][1]=g
            prev=k
        for k,o in ch['A'][sx]['cards'].items(): vis(o,[tuple(r) for r in AR.get(k,[])])
    for o in [ch['root']]+list(ch['root'].children_recursive):
        o['chr']=ch['inst']
    return ch
# ==== ROUND 5 PROPOSAL (Nov 23 2026; awaits owner approval; opt-in: nothing below runs unless a scene calls it) ====
# (1) Face turns in steps, Rick's way (research/rick-style-spec/face-turns-arms/ in project files):
#     - one level apart, or front <-> back view: a 1-frame snap (Rick #03 f1014-1015, #04 f349-350)
#     - left <-> right: pass through FRONT for 1-2 frames (#14 f1254-1258, #12 f1455-1462, #03 f1422 back-of-head in-between)
#     - two or more levels on the same side (e.g. strong 3/4 -> front): every level in between, 1 frame each, the last step held 2 frames
#       (#22 f379-385: 6 frames, 4 drawings; #10 f257-265; #24 f413-417; #22 f1458-1464)
#     Variants come from cast.json "turns" (expressions.turn_name: smug@L3 .. smug@F .. smug@R3); missing variants fall back to the base.
def turn_plan(frm,to,holds=None):
    """[(frame offset, level)] for a turn from level frm to level to (-3 left .. 0 front .. 3 right)"""
    if frm==to: return []
    if abs(to-frm)==1: return [(0,to)]
    if frm*to<0: return [(0,0),(2 if abs(frm)+abs(to)>=4 else 1,to)]
    step=1 if to>frm else -1; lv=list(range(frm+step,to+step,step)); out=[]; o=0
    for i,l in enumerate(lv):
        out.append((o,l)); o+=(holds[i] if holds and i<len(holds) else (2 if i==len(lv)-2 else 1))
    return out
def turn(ch,f,face_base,frm,to,holds=None,tilt=0):
    """schedule a stepped head turn starting at frame f; returns the frame the last level lands on. tilt: optional head lean in degrees
    during the turn (Rick #22 f379-385 leans ~6 deg into the turn and comes back)"""
    plan=turn_plan(frm,to,holds); last=f
    for o,l in plan:
        k=XL.turn_name(face_base,l)
        face(ch,f+o,k if k in ch['F'] else face_base); last=f+o
    if tilt and plan:
        hp=ch['hp']; krot(hp,f-1,(0,0,0)); krot(hp,f+max(1,(last-f)//2),(0,math.radians(tilt),0)); krot(hp,last+2,(0,0,0))
    return last
def look(ch,f,face_base,lv):
    """put the face straight at a level (no steps), e.g. the start of a shot"""
    k=XL.turn_name(face_base,lv); face(ch,f,k if k in ch['F'] else face_base)
# (2) Arm gestures: whole-arm POSE cards (cast.POSES, generated when cast.json has "poses"), swapped like Rick's drawings:
#     snap 1-2 f (59 of 144 labelled Rick arm actions, median 2 f), optional 1-frame in-between (_m), optional 1-2 frame settle on an
#     overshoot drawing (_o; 21 of 144), optional 2-frame anticipation dip (12 of 144: throws, strikes, points). One arm gestures, the
#     other usually stays put. Return to rest with gesture(ch,sx,f,'hang') or back to the old card with gesture(ch,sx,f,None).
ARM_PX=0.744/1200   # metres per arm-texture pixel (ARM_W covers 1200 px)
POSE_W,POSE_H=1600,1800   # = cast.POSE_W/POSE_H (r5b: wider canvas so no pose drawing is sliced by the card edge)
def _pose_card(ch,sx,key):
    A=ch['A'][sx]
    if key in A['cards']: return A['cards'][key]
    c=CI[ch['kind']]; _q=ARM_Q; tk=f"{ch['kind']}_{key}"+('_L' if sx<0 else '')
    a=plane(f"{ch['inst']}_arm{sx}_{key}",(0,0,0),POSE_W*ARM_PX*_q,POSE_H*ARM_PX*_q,card_mat(tk,tk),coll=chr_coll(ch['shot'])); a.parent=A['piv']
    a.location=(0,POSE_DY,(ARM_H/2-ARM_OFF-40*ARM_PX)*_q)   # drawn shoulder sits where the hanging card's shoulder sits
    _b=key.replace('arm_pose_','',1); _b=_b[:-2] if _b.endswith(('_m','_o')) else _b
    if _b.startswith('wa') and len(_b)>4 and _b[4]=='f':   # r10: leading-side walk arm sits BEHIND the torso (body 0, legs +1.5 mm, behind fx +4 mm)
        a.location.y=BACK_Y-ARM_Y[sx]
    if _b in FRONT_POSES:   # r8b: hand in front of the face (owner Nov 23)
        a.location.y=FRONT_Y[sx]-ARM_Y[sx]
    a.visible_shadow=False; A['cards'][key]=a; vis(a,[]); return a
def _piv_hold(ch,sx,f,deg):
    piv=ch['A'][sx]['piv']; fc=None
    if piv.animation_data and piv.animation_data.action:
        fc=next((c for c in piv.animation_data.action.fcurves if c.data_path=='rotation_euler' and c.array_index==1),None)
    if fc: krot(piv,f-1,(0,fc.evaluate(f-1),0))
    krot(piv,f,(0,math.radians(deg)*sx,0))
    for c in piv.animation_data.action.fcurves:
        for kp in c.keyframe_points:
            if kp.co[0] in (f-1,f): kp.interpolation='CONSTANT'
def gesture(ch,sx,f,pose,inb=True,settle=0,anticip=0):
    """swap arm sx (-1 left, 1 right) to a pose at frame f. inb: 1-frame in-between first; settle: frames on the overshoot drawing after
    landing (0-2); anticip: frames on the 'dip' drawing before it (0 or 2). pose 'hang' or None = back to the character's normal arm card."""
    A=ch['A'][sx]; seq=[]
    if pose in (None,'hang'):
        if inb and A.get('pose'): seq.append((f,f"arm_pose_{A['pose']}_m"))
        seq.append((f+(1 if inb and A.get('pose') else 0),'arm')); A['pose']=None
    else:
        g=f
        if anticip: seq.append((g,'arm_pose_dip')); g+=anticip
        if inb: seq.append((g,f'arm_pose_{pose}_m')); g+=1
        if settle: seq.append((g,f'arm_pose_{pose}_o')); g+=settle
        seq.append((g,f'arm_pose_{pose}')); A['pose']=pose
    for g,k in seq:
        if k!='arm': _pose_card(ch,sx,k)
        A['sched']=[s_ for s_ in A['sched'] if s_[0]!=g]+[(g,k)]
        _piv_hold(ch,sx,g,-8 if k=='arm' else 0)   # pose drawings carry their own angle; the rest card keeps its -8 deg hang
    return seq[-1][0]
# ==== ROUND 6 (Nov 23 2026): COORDINATED MOTION (owner: "face turns, arm gestures, leg motion and body posture are ONE movement") ====
# Opt-in and additive: nothing below runs unless a scene calls combo(). Combos live in motion_combos.json (catalogue + Rick evidence +
# agreement rates; research/rick-style-spec/motion-library/ in project files). motion.frames() is the single plan for both this
# function and the 2D preview sheet (m6sheet.py). Rules 356+ (RULES_CONSOLIDATED.md).
import motion as MO
HIP_ROW=520   # = cast.HIP_ROW: lean pivot row in the 1100-row body texture
def _lean_rig(ch):
    """Round 6 hierarchy, made on first combo() only: root -> whole (feet: squash, hop) -> [legs card, lean (hip: torso lean) ->
    [torso card, head pivot, arm pivots]]. The torso and legs cards are cut from the same body drawing (cast.split_body), so at
    lean 0 the character looks exactly as before; the original body card is hidden for this character (finish())."""
    if 'split' in ch: return ch['lean']   # r6b: 'in', not truthiness (a bpy object tested falsy here and the rig was rebuilt on every combo call)
    c=CI[ch['kind']]; sy=BSY[c['body']]; C_=chr_coll(ch['shot'])
    zc=-0.04+0.55*sy+FOOT_LIFT; zh=-0.04+1.1*sy*(1-HIP_ROW/1100)+FOOT_LIFT   # r5b FOOT_LIFT (rule 354b): same lift as char()
    wh=empty(ch['inst']+'_whole',(0,0,0),ch['root'],coll=C_)
    ln=empty(ch['inst']+'_lean',(0,0,zh),wh,coll=C_)
    tp=plane(f"{ch['inst']}_btop",(0,0,0),0.8,1.1*sy,card_mat(f"{ch['kind']}_btop",f"{ch['kind']}_btop"),coll=C_); tp.parent=ln; tp.location=(0,0,zc-zh)
    for o in [ch['hp']]+[ch['A'][sx]['piv'] for sx in (-1,1)]:
        x,y,z=o.location; o.parent=ln; o.location=(x,y,z-zh)
    ch['top']=ch['top']-zh   # head pivot z is now measured from the hip
    ch['split']=dict(whole=wh,top=tp,legs={},zc=zc); ch['lean']=ln; return ln
def _const(o):
    if o.animation_data and o.animation_data.action:
        for fc in o.animation_data.action.fcurves:
            if fc.data_path!='hide_render':
                for kp in fc.keyframe_points: kp.interpolation='CONSTANT'
LEGTEX={'body':'blegs','bodyw1':'blegsw1','bodyw2':'blegsw2'}
LEGTEX.update({f'run{d}{p}':f'blegsrun{d}{p}' for d in 'RL' for p in (1,2,3,4)})   # r7: run cycle legs (cast.run_legs)
LEGTEX.update({f'walk{d}{p}':f'blegswalk{d}{p}' for d in 'RL' for p in (1,2,3,4)})
WALK_N={'st':10,'nm':8,'br':6}   # = cast.WALK_STYLES n
LEGTEX.update({f'wk{v}{st}{i}':f'blegswk{v}{st}{i}' for v in 'RLF' for st,n in WALK_N.items() for i in range(n)})   # r9 walk v2   # r8c: walk cycle legs (cast.walk_legs), never airborne
LEGTEX.update({'turnR':'blegsturnR','turnL':'blegsturnL','back':'blegsback'})   # r8: turned feet (cast.turned_legs)
TOPTEX={'qR':'btopqR','qL':'btopqL','qbR':'btopqbR','qbL':'btopqbL','back':'btopback'}   # r8: turned torso cards (cast.turn_top)
def _body_card(ch,key):
    """legs card for 'body' (standing) or a stride drawing used as a step / weight shift / run (made on first use)"""
    L=ch['split']['legs']
    if key in L: return L[key]
    c=CI[ch['kind']]; sy=BSY[c['body']]; t=f"{ch['kind']}_{LEGTEX[key]}"
    b=plane(f"{ch['inst']}_body_{LEGTEX[key]}",(0,0,0),0.8,1.1*sy,card_mat(t,t),coll=chr_coll(ch['shot']))   # '_body' in the name: rigcheck FOOT tests it
    b.parent=ch['split']['whole']; b.location=(0,0.0015,ch['split']['zc']); L[key]=b; return b   # 1.5 mm behind the torso card (rule 354b: no coplanar cards)
_setface=face
def combo(ch,f,name,side=1,face=None,frm=0,face2=None):
    """Rick combined move `name` (motion_combos.json) starting at frame f, toward screen side `side` (+1 right, -1 left).
    face: base face (default: the character's current face); frm: head level at the start (-3..3).
    Bakes every channel on the same plan: face/turn (353a grammar), arm pose cards (354a), body lean/squash/hop on the lean pivot,
    head drop/tilt on the head pivot, stride cards for steps. Returns the last frame the combo changes anything."""
    st_=MO.COMBOS[name].get('status')
    if st_ not in ('MEASURED','APPROVED') and name not in (CI[ch['kind']].get('combos_approved') or []):   # r7: APPROVED = owner OK'd (Nov 23)
        raise ValueError(f"combo {name} is {st_}: owner approval needed (cast.json 'combos_approved')")   # inferred moves stay OFF (rule 360)
    base=face or (sorted(ch['faces'])[-1][1].split('@')[0] if ch['faces'] else list(ch['F'])[0].split('@')[0])
    seq=MO.frames(name,side,base,frm,face2,pre=0,post=0)
    ln=_lean_rig(ch); wh=ch['split']['whole']; hp=ch['hp']; top=ch['top']; prev=None; last=f
    _body_card(ch,'body')
    for s in seq:
        g=f+s['f']
        if prev is None or s['lv']!=prev['lv'] or s['face']!=prev['face']:
            k=XL.turn_name(s['face'],s['lv']) if s['lv'] is not None else s['face']
            _setface(ch,g,k if k in ch['F'] else s['face']); last=g
        for sx in (-1,1):
            a=s['arms'][sx]; pa=prev['arms'][sx] if prev else 'hang'
            if a!=pa:
                if a=='hang': ch['A'][sx]['sched']=[x for x in ch['A'][sx]['sched'] if x[0]!=g]+[(g,'arm')]; _piv_hold(ch,sx,g,-8); ch['A'][sx]['pose']=None
                else:
                    _pose_card(ch,sx,'arm_pose_'+a); ch['A'][sx]['sched']=[x for x in ch['A'][sx]['sched'] if x[0]!=g]+[(g,'arm_pose_'+a)]; _piv_hold(ch,sx,g,0)
                    ch['A'][sx]['pose']=a.split('_m')[0].split('_o')[0]
                last=g
        sw,psw=s.get('swing',0.0),(prev.get('swing',0.0) if prev else 0.0)   # r9 walk arm swing: rest arm rotates about the shoulder (one out, one in)
        if sw!=psw:
            for sx in (-1,1):
                if s['arms'][sx]=='hang': _piv_hold(ch,sx,g,-8+sw)   # same delta in each arm's own frame = opposite screen directions: one arm forward, one back
            last=g
        if prev is None or (s['lean'],s['squash'],s['hop'])!=(prev['lean'],prev['squash'],prev['hop']):
            if prev is None: krot(ln,g-1,(0,0,0)); kscale(wh,g-1,(1,1,1)); kloc(wh,g-1,(0,0,0))
            krot(ln,g,(0,math.radians(s['lean']),0)); kscale(wh,g,(1+s['squash']*0.6,1,1-s['squash'])); kloc(wh,g,(0,0,s['hop'])); last=g
        if prev is None or (s['hdy'],s['htilt'])!=(prev['hdy'],prev['htilt']):
            if prev is None: kloc(hp,g-1,(0,0,top)); krot(hp,g-1,(0,0,0))
            kloc(hp,g,(0,0,top-s['hdy'])); krot(hp,g,(0,math.radians(s['htilt']),0)); last=g
        if s['hop']>0.001 or (s['legs'].startswith('run') and s['legs'][-1] in '24'): AIR.add((ch['root'].name,g))   # r7: planned airborne frame
        if prev is None or s.get('top','front')!=prev.get('top','front'):   # r8: turned torso card
            if s.get('top','front')!='front': _top_card(ch,s['top'])
            ch.setdefault('topsched',[]).append((g,s.get('top','front'))); last=g
        for e in s.get('fx',[]):   # r7: effect cards, shown on the frames the plan lists them
            ch.setdefault('fxf',{}).setdefault(_fx_card(ch,*e),[]).append(g)
        if prev is None or s['legs']!=prev['legs']:
            if s['legs']!='body': _body_card(ch,s['legs'])
            ch.setdefault('legsched',[]).append((g,s['legs'])); last=g
        prev=s
    _const(ln); _const(wh); _const(hp)
    return last
def _top_card(ch,key):
    """r8: a turned torso card (3/4, 3/4 back, back), same size and place as the split torso card"""
    T_=ch['split'].setdefault('tops',{})
    if key in T_: return T_[key]
    c=CI[ch['kind']]; sy=BSY[c['body']]; t=f"{ch['kind']}_{TOPTEX[key]}"
    o=plane(f"{ch['inst']}_btop_{key}",(0,0,0),0.8,1.1*sy,card_mat(t,t),coll=chr_coll(ch['shot'])); o.parent=ch['lean']
    o.location=ch['split']['top'].location.copy(); vis(o,[]); T_[key]=o; return o
FX_Y={'head':-0.016,'torso':-0.0108,'feet':-0.002,'behind':0.004}   # r7 depths (rule 354b: >= 1 mm from every other card layer)
def _fx_card(ch,kind,anchor,dx,dz,size,side):
    """effect card (cast.fx textures) on the head pivot, the hip/lean pivot or the feet ('whole'); one card per kind/anchor/facing"""
    key=(kind,anchor,round(dx,3),round(dz,3),round(size,3),side); C_=ch.setdefault('fxc',{})
    if key in C_: return C_[key]
    t='fx_'+kind+('_L' if side<0 else '')
    o=plane(f"{ch['inst']}_fx_{kind}_{len(C_)}",(0,0,0),size,size,card_mat(t,t,emit=0.6),coll=chr_coll(ch['shot']))
    par={'head':ch['hp'],'torso':ch['lean'],'behind':ch['lean'],'feet':ch['split']['whole']}[anchor]
    o.parent=par; o.location=(dx,FX_Y[anchor],dz); o.visible_shadow=False; vis(o,[]); C_[key]=o; return o
def _revis(o,ranges):
    if o.animation_data and o.animation_data.action:
        for fc in list(o.animation_data.action.fcurves):
            if fc.data_path=='hide_render': o.animation_data.action.fcurves.remove(fc)
    vis(o,ranges)
_finish_r5=finish
def finish(ch,blink_every=34):
    """round 6: as before; a character that used combo() shows the split torso card for its whole range, its original body cards
    never, and the legs card that matches each frame (standing, or the stride drawings for walks and combo steps)"""
    ch=_finish_r5(ch,blink_every)
    if not ch.get('split'): return ch
    a,b=ch['rng']; st={}
    for fr in range(a,b+1): st[fr]='body'
    ls=sorted(ch.get('legsched',[]))
    for i,(g,k) in enumerate(ls):
        nx=ls[i+1][0] if i+1<len(ls) else b+1
        for fr in range(max(a,g),min(nx,b+1)): st[fr]=k
    for f0,f1,step in ch['walk']:
        for fr in range(f0,min(f1,b+1)):
            ph=((fr-f0)//step)%4; st[fr]=['bodyw1','body','bodyw2','body'][ph]
    for k in set(st.values()): _body_card(ch,k)
    BR={}; cur=None
    for fr in range(a,b+1):
        if st[fr]!=cur: BR.setdefault(st[fr],[]).append([fr,fr]); cur=st[fr]
        else: BR[cur][-1][1]=fr
    for o in ch['bodies'].values(): _revis(o,[])
    for k,o in ch['split']['legs'].items(): vis(o,BR.get(k,[]))
    vis(ch['split']['top'],[(a,b)])
    for o in [ch['split']['whole'],ch['lean']]+list(ch['split']['legs'].values())+[ch['split']['top']]: o['chr']=ch['inst']
    return ch
_finish_r6=finish
def finish(ch,blink_every=34):
    """round 7: as before, plus effect cards shown on their planned frames"""
    ch=_finish_r6(ch,blink_every)
    if ch.get('topsched'):   # r8: torso card per frame (front split card, or a turned one)
        a_,b_=ch['rng']; st={fr:'front' for fr in range(a_,b_+1)}; ts=sorted(ch['topsched'])
        for i,(g,k) in enumerate(ts):
            nx=ts[i+1][0] if i+1<len(ts) else b_+1
            for fr in range(max(a_,g),min(nx,b_+1)): st[fr]=k
        R={}; cur=None
        for fr in range(a_,b_+1):
            if st[fr]!=cur: R.setdefault(st[fr],[]).append([fr,fr]); cur=st[fr]
            else: R[cur][-1][1]=fr
        _revis(ch['split']['top'],[tuple(r) for r in R.get('front',[])])
        for k,o in ch['split'].get('tops',{}).items(): vis(o,[tuple(r) for r in R.get(k,[])]); o['chr']=ch['inst']
    for o,frs in (ch.get('fxf') or {}).items():
        frs=sorted(set(frs)); R=[]
        for f in frs:
            if R and f==R[-1][1]+1: R[-1][1]=f
            else: R.append([f,f])
        vis(o,[tuple(r) for r in R]); o['chr']=ch['inst']
    return ch
def lipsync(ch,words,f0,f1,shapes=('talkA','talkB','talkC','talkD'),rest='talkD'):
    """mouth shapes on the quoted words only (rule 185: lips move only on quoted lines)"""
    seq=[]
    for w,s,e in words:
        fs,fe=int(round((s+0.1)*30)),int(round((e+0.1)*30))
        if fs<f0 or fs>f1: continue
        k=0
        for f in range(fs,max(fs+3,fe),3): seq.append((f,shapes[k%3])); k+=1
        seq.append((max(fs+3,fe),rest))
    for f,k in seq: face(ch,f,k)
# ---------------- ink: camera-only inverted hulls ----------------
def ink(skip_prefix=()):
    hm=bpy.data.materials.new('hull'); N,L=nodes(hm)
    for n in list(N): N.remove(n)
    geo=N.new('ShaderNodeNewGeometry'); tr=N.new('ShaderNodeBsdfTransparent'); em=N.new('ShaderNodeEmission'); em.inputs['Color'].default_value=(0.02,0.016,0.014,1)
    oi=N.new('ShaderNodeObjectInfo'); L.new(oi.outputs['Color'],em.inputs['Color'])   # round 5 (A1): line in the surface's own dark colour, not black
    mx=N.new('ShaderNodeMixShader'); out=N.new('ShaderNodeOutputMaterial')
    L.new(geo.outputs['Backfacing'],mx.inputs['Fac']); L.new(em.outputs[0],mx.inputs[1]); L.new(tr.outputs[0],mx.inputs[2]); L.new(mx.outputs[0],out.inputs['Surface'])
    ng=bpy.data.node_groups.new('hullGN','GeometryNodeTree')
    ng.interface.new_socket('Geometry',in_out='INPUT',socket_type='NodeSocketGeometry'); ng.interface.new_socket('T',in_out='INPUT',socket_type='NodeSocketFloat')
    ng.interface.new_socket('Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
    gi=ng.nodes.new('NodeGroupInput'); go=ng.nodes.new('NodeGroupOutput'); nrm=ng.nodes.new('GeometryNodeInputNormal')
    sca=ng.nodes.new('ShaderNodeVectorMath'); sca.operation='SCALE'; sp=ng.nodes.new('GeometryNodeSetPosition'); ff=ng.nodes.new('GeometryNodeFlipFaces')
    sm=ng.nodes.new('GeometryNodeSetMaterial'); sm.inputs['Material'].default_value=hm
    ng.links.new(nrm.outputs['Normal'],sca.inputs[0]); ng.links.new(gi.outputs['T'],sca.inputs['Scale'])
    ng.links.new(gi.outputs['Geometry'],sp.inputs['Geometry']); ng.links.new(sca.outputs['Vector'],sp.inputs['Offset'])
    ng.links.new(sp.outputs['Geometry'],ff.inputs['Mesh']); ng.links.new(ff.outputs['Mesh'],sm.inputs['Geometry']); ng.links.new(sm.outputs['Geometry'],go.inputs['Geometry'])
    C_H=col('HULL'); nh=0
    for o in list(bpy.data.objects):
        if o.type!='MESH' or C_NOI in o.users_collection or o.get('chr') or o.get('noink') or len(o.data.vertices)<=4 or o.name.startswith(skip_prefix): continue
        if max(o.dimensions)>25 or o.name.startswith(('road','walk','car','curb','sky')): continue   # round 5 (A1): no lines on large clean surfaces
        t_=0.5*min(0.05,0.009+0.0062*math.sqrt(max(o.dimensions)))*o.get('inkmul',1.0)   # round 5: about half as thick (Rick 2-3 px vs our 4-8 px)
        h=o.copy(); h.name=o.name+'_ink'; cc_=[c for c in o.users_collection if c.name.startswith('CHR_') or (c is not C_SET and any(c.name in p_.children for p_ in bpy.data.collections if p_.name.startswith('CHR_')))]; (cc_[0] if cc_ else C_H).objects.link(h);   # sb: shared shot-only collections (linked under several CHR_) keep their hulls too (S19 desk hull drew as a solid block)  # round 4: a shot-only prop's ink hull stays in that shot's CHR_ collection (S07 mailbox hull showed as a black blob in S08)
        bc_=(0.30,0.22,0.18)
        m_=o.active_material
        if m_ and m_.use_nodes and 'Principled BSDF' in m_.node_tree.nodes:
            pb_=m_.node_tree.nodes['Principled BSDF'].inputs['Base Color']
            rgb_=[n_ for n_ in m_.node_tree.nodes if n_.type=='RGB']
            if not pb_.is_linked: bc_=tuple(pb_.default_value)[:3]
            elif rgb_: bc_=tuple(rgb_[0].outputs[0].default_value)[:3]
        h.color=(bc_[0]*0.22+0.004,bc_[1]*0.22+0.004,bc_[2]*0.22+0.004,1)
        h.parent=o; h.matrix_parent_inverse.identity(); h.location=(0,0,0); h.rotation_euler=(0,0,0); h.scale=(1,1,1)
        if h.animation_data: h.animation_data_clear()
        if o.animation_data and o.animation_data.action and any(fc.data_path=='hide_render' for fc in o.animation_data.action.fcurves):
            for fc in [fc for fc in o.animation_data.action.fcurves if fc.data_path=='hide_render']:
                for kp in fc.keyframe_points: h.hide_render=bool(kp.co[1]); h.keyframe_insert('hide_render',frame=int(kp.co[0]))
            for fc in h.animation_data.action.fcurves:
                for kp in fc.keyframe_points: kp.interpolation='CONSTANT'
        else: h.hide_render=False
        gm_=h.modifiers.new('hull','NODES'); gm_.node_group=ng; gm_[ng.interface.items_tree['T'].identifier]=t_/(max(o.matrix_world.to_scale()) or 1)
        h.visible_shadow=False; h.visible_diffuse=False; h.visible_glossy=False; h.visible_transmission=False; h.visible_volume_scatter=False
        if o.get('fly'): h['fly']=1
        nh+=1
    return nh
def render_setup(pct=100,samples=8):
    r=sc.render; r.engine='CYCLES'; r.resolution_x=1440; r.resolution_y=2560; r.resolution_percentage=pct
    cy=sc.cycles; cy.device='CPU'; cy.samples=samples; cy.use_adaptive_sampling=True; cy.adaptive_threshold=0.03; cy.use_denoising=True; cy.denoiser='OPENIMAGEDENOISE'
    cy.max_bounces=4; cy.diffuse_bounces=2; cy.glossy_bounces=1; cy.transmission_bounces=1; cy.transparent_max_bounces=16; cy.caustics_reflective=False; cy.caustics_refractive=False
    r.use_persistent_data=True; sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Punchy'
    sc.use_nodes=True; nt=sc.node_tree; N=nt.nodes; L=nt.links
    for n in list(N): N.remove(n)
    rl=N.new('CompositorNodeRLayers'); comp=N.new('CompositorNodeComposite'); gl=N.new('CompositorNodeGlare'); gl.glare_type='FOG_GLOW'; gl.threshold=0.9; gl.size=8; gl.mix=-0.75; gl.quality='LOW'
    # aerial haze (rule L8): mist pass mixes far geometry toward a warm-blue haze; starts at 14 m so interiors (rooms <= 9 m) are untouched
    vl=sc.view_layers[0]; vl.use_pass_mist=True
    if sc.world: sc.world.mist_settings.start=14; sc.world.mist_settings.depth=110; sc.world.mist_settings.falloff='LINEAR'
    mx=N.new('CompositorNodeMixRGB'); mx.blend_type='MIX'; mx.inputs[2].default_value=(0.62,0.68,0.78,1)
    mm=N.new('CompositorNodeMath'); mm.operation='MULTIPLY'; mm.inputs[1].default_value=0.42
    L.new(rl.outputs['Mist'],mm.inputs[0]); L.new(mm.outputs[0],mx.inputs[0]); L.new(rl.outputs['Image'],mx.inputs[1])
    L.new(mx.outputs['Image'],gl.inputs['Image']); L.new(gl.outputs['Image'],comp.inputs['Image'])
    r.image_settings.file_format='PNG'; r.image_settings.compression=30
# ---------------- rig check (rule 354b, owner Nov 23 test clip) ----------------
def _root(o):
    while o.parent: o=o.parent
    return o
_LOWROW={}
def _low_row(img):
    """lowest texture row (from the bottom, 0..1) holding opaque ink"""
    if img.name in _LOWROW: return _LOWROW[img.name]
    import numpy as np
    w,h=img.size; a=np.array(img.pixels[:]).reshape(h,w,4)[...,3]   # Blender rows start at the bottom
    rows=np.where(a.max(1)>0.5)[0]; v=(rows.min()/h) if len(rows) else 0.0
    _LOWROW[img.name]=v; return v
def _set_blocks(p):
    """r11c (DC thread feedback, dc16: 100 false FAILs on blobs hidden behind tables / crates): True when a set mesh (anything that is
    not a character card, ink hull or ground blob) sits between the camera and floor point p. Character hits are stepped through, so
    only furniture / walls count; the character cards themselves are dealt with by shadow_only_pass()."""
    dg=bpy.context.evaluated_depsgraph_get(); o=sc.camera.matrix_world.translation.copy(); d=(p-o); L_=d.length; d.normalize(); t=0.0
    for _ in range(40):
        hit,loc,_n,_i,ob,_m=sc.ray_cast(dg,o+d*t,d,distance=L_-t-0.02)
        if not hit: return False
        if ob.name.endswith('_shadow') or any(c.name.startswith('CHR_') for c in ob.users_collection): t=(loc-o).length+1e-4; continue
        return True
    return False
def shadow_pairs(frames,out_json,head_w=0.40):
    """r11 / rule 367 probe, part 1 (in Blender). r11b: only pairs whose ground blobs really overlap on the floor (the first version
    also took pairs up to 0.9 m apart, whose midpoint is plain floor). For each overlap it writes the screen pixels of
    M = centre of the overlap rectangle, A = M mirrored through blob A's centre (same distance from A's centre, outside B, so it shows
    A's darkness alone at that falloff), B likewise for blob B. shadowcheck.py then requires the overlap to be at least as dark as
    the darker single blob there (minus limit). Returns the number of overlapping pairs."""
    import json, itertools
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    R=sc.render; W=int(R.resolution_x*R.resolution_percentage/100); H=int(R.resolution_y*R.resolution_percentage/100); out=[]
    for f in frames:
        sc.frame_set(f)
        shs=[]
        for o in bpy.data.objects:
            if o.type=='MESH' and o.name.endswith('_shadow') and not o.hide_render:
                vs=[o.matrix_world@v.co for v in o.data.vertices]
                shs.append((o,min(v.x for v in vs),max(v.x for v in vs),min(v.y for v in vs),max(v.y for v in vs),sum(v.z for v in vs)/len(vs),o.matrix_world.translation.copy()))
        for (a,ax0,ax1,ay0,ay1,az,ca),(b,bx0,bx1,by0,by1,bz,cb) in itertools.combinations(shs,2):
            ox0,ox1,oy0,oy1=max(ax0,bx0),min(ax1,bx1),max(ay0,by0),min(ay1,by1)
            if ox1<=ox0 or oy1<=oy0: continue
            z=max(az,bz); M=Vector(((ox0+ox1)/2,(oy0+oy1)/2,z))
            pts=[]; hid=[]
            for p in (Vector((2*ca.x-M.x,2*ca.y-M.y,z)),M,Vector((2*cb.x-M.x,2*cb.y-M.y,z))):
                v=world_to_camera_view(sc,sc.camera,p); pts.append((round(v.x*W,1),round((1-v.y)*H,1)))
                # r11c: a mirror reference that falls inside a third character's blob reads two blobs, not one: drop it like a hidden one
                crowd=p is not M and any(s_[0] not in (a,b) and s_[1]<p.x<s_[2] and s_[3]<p.y<s_[4] for s_ in shs)
                hid.append(crowd or _set_blocks(p))
            out.append(dict(f=f,a=a.name,b=b.name,dist=round((ca-cb).length,3),overlap_m=(round(ox1-ox0,3),round(oy1-oy0,3)),A=pts[0],M=pts[1],B=pts[2],hidden=hid))
    json.dump(out,open(out_json,'w'),indent=0); print('SHADOW_PAIRS',len(out)); return len(out)
def shadow_only_pass():
    """r11b / rule 367 probe: hide every character card and ink hull from the camera and from the sun (ray visibility, so the card
    swaps keep working) and leave only the ground blobs on the floor. Rendered for the close-pair frames, this lets shadowcheck.py
    read the blobs without legs or ink crossing its sample windows. Probe renders only, never a delivery render."""
    n=0
    for o in bpy.data.objects:
        if o.type=='MESH' and not o.name.endswith('_shadow') and any(c.name.startswith('CHR_') for c in o.users_collection):
            o.visible_camera=False; o.visible_shadow=False; n+=1
    print('SHADOW_ONLY_PASS hidden',n); return n
AIR=set()   # r7: (character root name, frame) where combo() plans the feet off the ground (jumps, run air drawings); FOOT skips them
def rigcheck(frames,floor_z=None):
    """Prints RIGCHECK lines and returns the number of faults:
    COPLANAR_CARD  two visible cards of one character in the same plane (< 1 mm apart) that overlap on screen -> see-through ink
    FOOT           drawn foot bottom below the floor (clipping) or more than 6 mm above it (floating)
    SHADOW_CARD    a character's flat ground-blob card casts a sun shadow (dark box on the floor)
    SHADOW_OVERLAP two characters' ground blobs overlap on the floor at the same height (< 1 mm): the shadows flicker or vanish (r11)"""
    import itertools
    bad=0
    for o in bpy.data.objects:
        if o.name.endswith('_shadow') and o.type=='MESH' and o.visible_shadow:
            print('RIGCHECK SHADOW_CARD',o.name); bad+=1
    seen=set()
    for f in frames:
        sc.frame_set(f)
        shs=[]   # r11: SHADOW_OVERLAP
        for o in bpy.data.objects:
            if o.type=='MESH' and o.name.endswith('_shadow') and not o.hide_render:
                vs=[o.matrix_world@v.co for v in o.data.vertices]; shs.append((o,min(v.x for v in vs),max(v.x for v in vs),min(v.y for v in vs),max(v.y for v in vs),sum(v.z for v in vs)/len(vs)))
        for (a,ax0,ax1,ay0,ay1,az),(b,bx0,bx1,by0,by1,bz) in itertools.combinations(shs,2):
            if abs(az-bz)<0.001 and min(ax1,bx1)>max(ax0,bx0) and min(ay1,by1)>max(ay0,by0):
                k=('SHOV',a.name,b.name)
                if k not in seen: seen.add(k); print('RIGCHECK SHADOW_OVERLAP',f,a.name,b.name,f'{abs(az-bz)*1000:.2f}mm'); bad+=1
        by={}
        for o in bpy.data.objects:
            if o.type!='MESH' or o.hide_render or not any(c.name.startswith('CHR_') for c in o.users_collection): continue
            if o.name.endswith('_shadow'): continue
            by.setdefault(_root(o).name,[]).append(o)
        for r,obs in by.items():
            P=[]
            for o in obs:
                vs=[o.matrix_world@v.co for v in o.data.vertices]
                if len(vs)!=4: continue
                n=(vs[1]-vs[0]).cross(vs[3]-vs[0]).normalized(); P.append((o,vs,n))
            for (a,va,na),(b,vb,nb) in itertools.combinations(P,2):
                if abs(na.dot(nb))<0.999: continue
                d=abs((vb[0]-va[0]).dot(na))
                if d>=0.001: continue
                u=(va[1]-va[0]).normalized(); w=na.cross(u)
                ra=[((p-va[0]).dot(u),(p-va[0]).dot(w)) for p in va]; rb=[((p-va[0]).dot(u),(p-va[0]).dot(w)) for p in vb]
                ov=all(min(max(x[k] for x in ra),max(x[k] for x in rb))>max(min(x[k] for x in ra),min(x[k] for x in rb)) for k in (0,1))
                key=(a.name,b.name)
                if ov and key not in seen: seen.add(key); print('RIGCHECK COPLANAR_CARD',f,a.name,b.name,f'{d*1000:.2f}mm'); bad+=1
            for o,vs,n in P:
                if '_body' not in o.name or not o.active_material: continue
                im=next((nd.image for nd in o.active_material.node_tree.nodes if nd.type=='TEX_IMAGE' and nd.image),None)
                if not im: continue
                zb=min(v.z for v in vs); zt=max(v.z for v in vs); fz=zb+_low_row(im)*(zt-zb)-(_root(o).matrix_world.translation.z if floor_z is None else floor_z)   # floor = the character's root (feet planted on its own ground)
                if (_root(o).name,f) in AIR: continue   # r7: a planned jump or run air drawing, not a floating foot
                k=('FOOT',o.name)
                if (fz<0 or fz>0.006) and k not in seen: seen.add(k); print('RIGCHECK FOOT',f,o.name,f'{fz*1000:+.1f}mm'); bad+=1
    print('RIGCHECK_FAULTS',bad); return bad
