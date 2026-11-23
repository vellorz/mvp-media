# Shared Blender helpers for the Black Friday short (Rick method: painted 3D sets + flat 2D cut-out cast)
import bpy, bmesh, math, random, json, os
from mathutils import Vector
TX='/root/det/tex/'
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
TILT=json.load(open('/root/det/src/tilt.json')) if os.path.exists('/root/det/src/tilt.json') else {}
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
CI=XL.expand(json.load(open('/root/det/src/cast.json')))
# r7 (round-6 visual: round bodies torso 0.63, legs 0.88 head-heights; need 0.7-1.05 / 0.9-1.5): round body cards stretched 1.118x up from the feet
BSY={'tall':0.91,'short':0.91,'round':0.91}   # det r4: body cards z 0.91 about the feet (torso/legs were 1.10/1.36 head widths)
BSY0=1.0   # r8b: one Rick build for every kind (cast.py GB/HEMY), no stretch
# r8b (owner Nov 20: clone Rick's build; guide v1.3 x.3): head 0.43 m wide = H; torso 0.962->0.532 = 1.00 H; legs 0.532->-0.014 = 1.27 H;
# head disc centre 1.167 (top 1.382): total 3.25 H. Shoulder pivots 0.95, hand (HAND_Z 0.407) at the hem.
HS=0.43/0.586   # head card scale vs rounds 1-7 (disc 800/1024 of a 0.75 card)
GEO={'tall':(0.966,0.141,0.86),'short':(0.966,0.156,0.86),'round':(0.966,0.165,0.86)}   # r7b (owner Nov 22 sheet comment 'arm issue?': arm roots poked out above the rounded shoulders): shoulder pivot 0.92 -> 0.86 and x out to the outline (0.126/0.142/0.151 -> 0.141/0.156/0.165) so the arm stroke grows out of the side outline instead of a parallel line with a sliver.   # r7det (rule 329, Rick f606: head overlaps the capsule top ~0.3 H): head and shoulders 0.03 lower; was 0.996/0.95
#   # r9: shoulders follow the narrower torso (0.73-0.89 H)
ARM_W,ARM_H,ARM_OFF=0.744,0.558,0.242   # r6: arm canvas 1200 wide (bent forearm swings outward)
SHADOW=None
def chr_coll(shot):
    if shot not in CHRC: CHRC[shot]=col('CHR_'+shot)
    return CHRC[shot]
def char(inst,kind,shot,loc,rng,face0=None,arms=('arm','arm'),scale=1.0,walker=False,camname=None):
    c=CI[kind]; top,shx,shz=GEO[c['body']]; _q=BSY[c['body']]; top=-0.04+(top+0.04)*_q; shz=-0.04+(shz+0.04)*_q; C=chr_coll(shot)
    root=empty(inst,loc,coll=C); root.scale=(scale,)*3
    bb=root.constraints.new('LOCKED_TRACK'); bb.target=CAM[camname or shot]; bb.track_axis='TRACK_NEGATIVE_Y'; bb.lock_axis='LOCK_Z'
    bodies={}
    for key in (['body','bodyw1','bodyw2'] if walker else ['body']):
        sy=BSY[c['body']]; b=plane(f'{inst}_{key}',(0,0,0),0.8,1.1*sy,card_mat(f'{kind}_{key}',f'{kind}_{key}'),coll=C); b.parent=root; b.location=(0,0,-0.04+0.55*sy); bodies[key]=b
    hp=empty(inst+'_hp',(0,0,top),root,coll=C)
    _sk=XL.SKIN.get(c.get('skin'),(252,246,236)) if isinstance(c.get('skin'),str) else tuple(c.get('skin',(252,246,236)))[:3]; neck=plane(inst+'_head',(0,0,0),0.16*HS,0.16*HS,flat('skin_'+str(_sk[0])+'_'+str(_sk[1]),lin(_sk),0.9),coll=C)   # det r10: neck matches the Rick skin preset; neck.parent=hp; neck.location=(0,0.004,0.04)
    F={}
    for fk in c['faces']:
        _pt,_pb=XL.pads(c)   # round 3: tall hats/hair/beards use a taller head texture; card grows by the same ratio, head disc stays put
        f=plane(f'{inst}_d_{fk}',(0,0,0),0.75*HS,0.75*HS*(1024+_pt+_pb)/1024,card_mat(f'{kind}_h_{fk}',f'{kind}_h_{fk}',emit=0.25),coll=C); f.parent=hp; f.location=(0,-0.012,0.2535*HS+0.75*HS*(_pt-_pb)/2048); F[fk]=f
    A={}
    for sx,ak in zip((-1,1),arms):
        # r7 (rule 268): arms sit BEHIND the face disc (face -0.012) and in front of the body (0): a raised hand can never paint over its own face
        ap=empty(f'{inst}_ap{sx}',(sx*shx,-0.006,shz),root,coll=C); A[sx]={'piv':ap,'cards':{}}
        keys=[ak] if isinstance(ak,str) else sorted(set(k for _,k in ak))
        if 'armS' not in keys: keys=keys+['armS']   # r7: straight card swapped in automatically while the arm is raised past 70 deg
        for k in keys:
            tk=f'{kind}_{k}'+('_L' if sx<0 else '')   # r7 (rule 272): mirrored texture, never a negative scale
            a=plane(f'{inst}_arm{sx}_{k}',(0,0,0),ARM_W*_q,ARM_H*_q,card_mat(tk,tk),coll=C); a.parent=ap; a.location=(0,0,-ARM_OFF*_q)
            a.visible_shadow=False   # r7b (owner Nov 22 'arm issue?'): the sun cast the arm card's shadow onto the torso as a dark notch on the lit side; Rick's arms cast none
            A[sx]['cards'][k]=a
        A[sx]['sched']=[(rng[0],ak)] if isinstance(ak,str) else ak
    sh=plane(inst+'_shadow',(0,0,0),1.0,0.45,card_mat('shadowblob','shadow',emit=0.0),coll=C,horiz=True); sh.parent=root; sh.location=(0,0,0.004)
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
    # det r9 (rule 332 b/c, Nov 22): a featured face never holds a long beat; long non-talk holds cycle through same-family library faces
    # (each piece 0.9-1.5 s) so no face but blink/deadpan passes ~25 % of a character's screen time and faces change every 0.3-2 s
    SAFE={'laugh':['happy','grin','open_smile'],'cheer':['laugh','happy','grin'],'happy':['smile','grin','laugh'],'grin':['smug_grin','happy','smile'],
          'smug':['side_eye','skeptical','smug_grin'],'wink':['smug','grin'],'shock':['surprise','panic','startle'],'wow':['surprise','shock','open_smile'],
          'surprise':['shock','startle','look_up'],'shout':['angry','angry_squint','annoyed'],'grit':['angry','annoyed','stern'],'angry_squint':['angry','stern','annoyed'],
          'sad':['sigh','frown','worried'],'worried':['nervous','wince','sad'],'idea':['open_smile','grin','surprise'],'manic_grin':['grin','open_smile'],
          'shrug':['skeptical','side_eye'],'stunned':['startle','surprise'],'deadpan':['skeptical','neutral','side_eye']}
    if not ch.get('novary'):
        hh=sum(map(ord,ch['inst'])); v=[]
        seq=[p for i,p in enumerate(seq) if i==0 or p[1]!=seq[i-1][1]]   # merge repeats of the same face into one hold
        for i,(f,k) in enumerate(seq):
            nx=seq[i+1][0] if i+1<len(seq) else b+1
            pool=[k]+[x for x in SAFE.get(k,[]) if x in ch['F']]
            if k.startswith('talk') or k=='blink' or len(pool)<2 or nx-f<40: v.append((f,k)); continue
            t=f; j=0
            while t<nx:
                v.append((t,pool[1+((j//2+hh)%(len(pool)-1))] if j%2 else k)); j+=1; t+=22+((hh+j*7)%15)
                if nx-t<18: break
        seq=v
        # a face that comes back later in the shot returns as its next family alternate (cheer, wow, cheer -> cheer, wow, laugh)
        cnt={}; w=[]
        for f,k in seq:
            pool=[k]+[x for x in SAFE.get(k,[]) if x in ch['F']]
            if k.startswith('talk') or k=='blink' or len(pool)<2: w.append((f,k)); continue
            n=cnt.get(k,0); cnt[k]=n+1; w.append((f,pool[n%len(pool)]))
        seq=w
    out=[]
    for i,(f,k) in enumerate(seq):
        nx=seq[i+1][0] if i+1<len(seq) else b+1
        out.append((f,k)); t=f+blink_every
        if 'blink' in ch['F'] and k!='blink':
            while t+2<nx-6: out.append((t,'blink')); out.append((t+2,k)); t+=blink_every+((t//7)%9)
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
        h=o.copy(); h.name=o.name+'_ink'; cc_=[c for c in o.users_collection if c.name.startswith('CHR_')]; (cc_[0] if cc_ else C_H).objects.link(h);  # round 4: a shot-only prop's ink hull stays in that shot's CHR_ collection (S07 mailbox hull showed as a black blob in S08)
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
