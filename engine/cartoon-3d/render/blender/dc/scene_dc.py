# Washington DC Thanksgiving short (thu-washington-dc): Blender builder.   blender -b --python scene_dc.py   -> /root/dc/blend16/dc.blend
# Built on the Black Friday / Cape Cod pipeline (lib.py rig, ink hulls, cast cards, render setup); every set, prop and scene here is new for this video.
# Story: one magazine editor writes to five presidents for one shared Thanksgiving day; four say no, the fifth says yes (1863).
import sys, os, math, random, json
sys.path.insert(0,'/root/dc/src16')
import bpy, bmesh
from mathutils import Vector, Euler, Matrix
import lib as L
from lib import box,cyl,sph,plane,flat,surf,card_mat,lin,vis,kloc,krot,kscale,empty,cam,char,face,faces,arm,bob,walk,finish,lipsync
END=2086
sc=L.init(END); R=random.Random(11)
WORDS=json.load(open('/root/dc/vo/vo_trim.wav.words.json'))
# shot table: overlaps are dissolves (smoothstep in post), touching ranges are hard cuts (4: 411, 626, 1391, 1439). Long take (rule 312) = S11.
SH={'S01':(0,70),'S02':(64,162),'S03':(156,302),'S04':(296,410),'S05':(411,500),'S06':(494,625),'S07':(626,672),'S08':(666,808),
    'S09':(802,892),'S10':(886,978),'S11':(972,1240),'S12':(1234,1314),'S13':(1308,1390),'S14':(1391,1438),'S15':(1439,1490),
    'S16':(1484,1598),'S17':(1592,1644),'S18':(1638,1732),'S19':(1726,1892),'S20':(1886,1980),'S21':(1974,END)}
sc['shots']=json.dumps(SH); os.makedirs('/root/dc/bridge16',exist_ok=True); json.dump(SH,open('/root/dc/bridge16/shots.json','w'))
LENS={n:30 for n in SH}; LENS.update({'S07':34,'S14':38,'S15':36,'S17':36,'S16':28,'S19':28})
for n in SH: cam(n,LENS[n],11.0)   # sets stay sharp (BF r6 lesson)
def C(n): return L.chr_coll(n)
PATHS={}
TILT=json.load(open('/root/dc/bridge16/tilt.json')) if os.path.exists('/root/dc/bridge16/tilt.json') else {}   # dc14 rule 344: per-shot look-at drop (m) so faces in the caption column end above 0.665 H
def path(n,keys):
    t_=TILT.get(n,0.0); dz,upto=(t_ if isinstance(t_,list) else (t_,10**6)); keys=[(k[0],k[1],(k[2][0],k[2][1],k[2][2]+(dz if k[0]<=upto else 0.0)))+tuple(k[3:]) for k in keys]
    PATHS.setdefault(n,[]).extend(keys); L.path(n,keys)
ALL=[]
def shared(name,shots):
    """one collection of shot-only dressing linked under several shots' CHR_ collections"""
    c=bpy.data.collections.new(name)
    for s_ in shots: C(s_).children.link(c)
    return c
INK=flat('inkc',lin((50,28,42)),0.9)
def char_on(inst,kind,shot,loc,rng,face0=None,arms=('arm','arm'),walker=False,scale=1.0):
    ch=char(inst,kind,shot,loc,rng,face0,arms=arms,walker=walker,scale=scale); ALL.append(ch); return ch
def drift_faces(ch,f0,f1,pool,seed,step=(20,38)):
    rr=random.Random(seed); f=f0; seq=[]
    while f<f1: seq.append((f,rr.choice(pool))); f+=rr.randint(*step)
    faces(ch,seq)
# ---- dc14 rule 354 (interim, [INFERRED] catalogue pending Rick research + owner approval): named arm actions, logged so a probe can check
# that neighbours in a shot never share a move and no character repeats a move more than twice. Outward = negative angle on both sides.
import motion as MO
REST=-12; ACTLOG=[]
ACTS={'point':[(0,REST),(5,-95),(20,-90),(26,REST)],'reach':[(0,REST),(6,-120),(22,-115),(28,REST)],'reach_high':[(0,REST),(6,-140),(22,-136),(28,REST)],
      'wave':[(0,REST),(4,-150),(8,-122),(12,-150),(16,-122),(20,-150),(26,REST)],'throw':[(0,-25),(3,15),(7,-140),(11,-70),(17,REST)],
      'drop':[(0,-60),(4,-70),(8,-5),(14,REST)],'flick':[(0,-30),(4,25),(7,-110),(12,-40),(18,REST)],'present':[(0,REST),(6,-70),(22,-65),(28,REST)],
      'fist_pump':[(0,-30),(3,-160),(6,-120),(9,-160),(14,-40),(18,REST)],'head_grab':[(0,REST),(5,-150),(18,-145),(24,REST)],
      'stamp':[(0,-50),(6,-130),(9,-35),(14,-40),(20,REST)],'offer':[(0,-30),(6,-60),(20,-55),(26,-30)],'wag':[(0,-60),(5,-80),(10,-62),(15,-80),(20,-62),(25,-60)]}
BOTH={'shrug':[(0,REST),(4,-48),(14,-48),(19,REST)],'clutch':[(0,REST),(6,22),(24,22),(30,REST)]}
WORK={'write','press','carry','eat'}   # continuous work loops: not raises, exempt from the repeat count
# dc15 (owner approved the coordinated motion library Nov 23; rules 356-364): story beats play as Rick's MEASURED/APPROVED combos (lib.combo):
# head, torso lean and arm on one plan. Legacy keyframed moves stay only where a prop card is in the hand (346 contact), for lip-synced
# characters and for hand-placed contacts (S08 map reach).
CMAP={'point':'point_out_tilt','reach':'lean_reach','wave':'wave_hello','throw':'toss','flick':'toss','stamp':'swing_down','fist_pump':'victory_up',
      'head_grab':'panic_clutch','clutch':'panic_clutch','shrug':'look_back_shrug','shrugtalk':'dip_talk','think':'think_chin','doubletake':'double_take','clap':'clap','recoil':'startle_recoil','huff':'cross_arms_huff','present':'tilt_talk','offer':'tilt_talk','drop':'dip_talk','wag':'akimbo_scold'}
COMBOLOG=[]
def _active_face(ch,f):
    k=None
    for f_,k_ in sorted(ch['faces']):
        if f_<=f: k=k_
    k=k or (sorted(ch['faces'])[0][1] if ch['faces'] else 'neutral')
    return k.split('@')[0].replace('_ta','').replace('_tb','')
def _card_at(ch,sx,f):
    c='arm'
    for f_,k_ in sorted(ch['A'][sx].get('sched',[])):
        if f_<=f: c=k_
    return c
def act(ch,name,f,sx=1):
    cm=CMAP.get(name); ci=L.CI[ch['kind']]
    def _free(side):   # arms this combo moves must not hold a prop card (346 contact); a free arm may be on a plain or pose card
        used={a for st in MO.frames(cm,side,'neutral',0,None,pre=0,post=0) for a in (-1,1) if st['arms'][a]!='hang'}
        return all(_card_at(ch,a,f)=='arm' or _card_at(ch,a,f).startswith('arm_pose_') for a in used)
    side_=None
    PROPMOVES={'throw','flick','stamp','drop','offer'}   # the prop hand itself acts: keep the keyframed move with its prop card
    if cm and name in PROPMOVES and any(_card_at(ch,a,f) not in ('arm',) and not _card_at(ch,a,f).startswith('arm_pose_') for a in (-1,1)): cm=None
    if cm: side_=sx if _free(sx) else (-sx if _free(-sx) else None)
    if (cm and side_ and ci.get('combos') and not any(k.startswith('talk') for _,k in ch['faces']) and not ch.get('nocombo')
        and sum(1 for c in COMBOLOG if c['kind']==ch['kind'] and c['combo']==cm)<3):
        try:
            last=L.combo(ch,f,cm,side=side_,face=_active_face(ch,f))
            ch.setdefault('cwin',[]).append((f,last)); COMBOLOG.append(dict(shot=ch['shot'],inst=ch['inst'],kind=ch['kind'],combo=cm,f=f,last=last))
            ACTLOG.append(dict(shot=ch['shot'],inst=ch['inst'],kind=ch['kind'],act=cm,f=f)); return
        except KeyError as e:
            print('COMBO_SKIP',ch['inst'],cm,f,e)
    if cm: print('COMBO_NO',ch['inst'],name,f,'combos' if not ci.get('combos') else '', 'talk' if any(k.startswith('talk') for _,k in ch['faces']) else '', [_card_at(ch,s_,f) for s_ in (-1,1)], ch.get('nocombo'))
    name={'shrugtalk':'shrug','think':'shrug','doubletake':'head_grab','clap':'present','recoil':'clutch','huff':'head_grab'}.get(name,name)   # dc16: legacy arms when a new combo cannot run
    if name in BOTH:
        for side in (-1,1):
            for d,a_ in BOTH[name]: arm(ch,side,f+d,a_)
    elif name in ACTS:
        for d,a_ in ACTS[name]: arm(ch,sx,f+d,a_)
    ACTLOG.append(dict(shot=ch['shot'],inst=ch['inst'],kind=ch['kind'],act=name,f=f))
def work(ch,name,keys,sx=1):
    for f,a_ in keys: arm(ch,sx,f,a_)
    ACTLOG.append(dict(shot=ch['shot'],inst=ch['inst'],kind=ch['kind'],act=name,f=keys[0][0]))
# ---- dc14 rule 353 (interim): a character on screen over 2 s changes head angle at least once (twice over 4 s): side -> 2 f in-between
# (front, or the other side for front-facing characters) -> about 0.8 s on the other side -> 2 f in-between -> the shot's next face
TURNLOG=[]
def turnpass(ch):
    a,b=ch['rng']; n=b-a+1; V=L.CI[ch['kind']].get('turnbase',[])
    seq=sorted(ch['faces'])
    if n<60 or not V or any(k.startswith('talk') for _,k in seq): return
    def active(f,sq):
        k=sq[0][1]
        for f_,k_ in sq:
            if f_<=f: k=k_
        return k
    orig=seq[:]; done=[]
    nb=1 if n<=120 else 2
    for i in range(nb):
        t=a+n*(i+1)//(nb+1); cands=[f for f,k in orig if a+15<=f<=b-34 and all(abs(f-d)>40 for d in done) and all(not(c0-6<=f<=c1+30) for c0,c1 in ch.get('cwin',[]))]   # dc15: combos already turn the head
        fb=min(cands,key=lambda f:abs(f-t)) if cands else t
        K=active(fb,orig); base=K if K in V else V[0]
        hold=max(12,min(24,b-fb-8)); f_end=fb+2+hold; nxt=active(f_end,orig)
        ch['faces']=[(f,k) for f,k in ch['faces'] if not (fb<=f<=f_end)]
        ch['faces']+=[(fb,base+'_ta'),(fb+2,base+'_tb'),(f_end-2,base+'_ta'),(f_end,nxt)]
        done.append(fb); TURNLOG.append(dict(shot=ch['shot'],inst=ch['inst'],kind=ch['kind'],frames=[fb,fb+2,f_end-2,f_end],face=base))
def onone(o):
    if o.animation_data and o.animation_data.action:
        for fc in o.animation_data.action.fcurves:
            if fc.data_path!='hide_render':
                for kp in fc.keyframe_points: kp.interpolation='CONSTANT'
def fx(n,img,loc,f0,dur,size,coll,face='-Y',grow=1.6,rise=0.0):
    """flat FX card on ones: pops at f0, grows, hides (Rick flat FX 12-27 f)"""
    o=plane(n,loc,size,size,card_mat(img,img,emit=0.6),coll=coll,face=face); o['noink']=1; o['fly']=1
    for k in range(0,dur+1,2):
        s_=1+(grow-1)*k/dur; o.scale=(s_,s_,s_); o.keyframe_insert('scale',frame=f0+k)
        o.location=(loc[0],loc[1],loc[2]+rise*k/dur); o.keyframe_insert('location',frame=f0+k)
    vis(o,[(f0,f0+dur)]); onone(o); return o
def fall(o,f0,dur,p0,p1,rot0=None,rot1=None):
    """ease-in fall on ones, no bounce (asset physics: fall 12.5 f ease-in)"""
    for k in range(dur+1):
        t=(k/dur)**2; o.location=tuple(p0[i]+(p1[i]-p0[i])*t for i in range(3)); o.keyframe_insert('location',frame=f0+k)
        if rot0: o.rotation_euler=tuple(rot0[i]+(rot1[i]-rot0[i])*t for i in range(3)); o.keyframe_insert('rotation_euler',frame=f0+k)
    onone(o)
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
    # Cape Cod F10: camera-only cap over the open top, invisible to light rays
    cb=bmesh.new(); cv=[cb.verts.new((c[0]+rad*math.cos(2*math.pi*i/seg),c[1]+rad*math.sin(2*math.pi*i/seg),z0+h-0.5)) for i in range(seg)]; cb.faces.new(cv)
    cm=bpy.data.meshes.new(n+'_cap'); cb.to_mesh(cm); cb.free(); cu=cm.uv_layers.new()
    for li in range(len(cu.data)): cu.data[li].uv=(0.5,0.985)
    co_=bpy.data.objects.new(n+'_cap',cm); L.C_NOI.objects.link(co_); cm.materials.append(m); co_['fly']=1; co_['noink']=1
    co_.visible_diffuse=False; co_.visible_glossy=False; co_.visible_transmission=False; co_.visible_volume_scatter=False; co_.visible_shadow=False
    return o
def light(n,kind,loc,energy,color=(1.0,0.9,0.78),size=1.0,rot=(0,0,0),coll=None):
    bpy.ops.object.light_add(type=kind,location=loc,rotation=rot); l=bpy.context.object; l.name=n; l.data.energy=energy; l.data.color=color
    if kind=='AREA': l.data.size=size
    else: l.data.shadow_soft_size=size
    if coll: L.put(l,coll)
    return l
# ---------------- set helpers (all new for this video) ----------------
WM={}
def wmat(img,emit=0.1):
    k=f'w_{img}_{emit}'
    if k in WM: return WM[k]
    m=card_mat(k,img,emit=emit); m.node_tree.nodes['Image Texture'].extension='REPEAT'; WM[k]=m; return m
def wallcard(n,c,w,h,img,face,tw,emit=0.1,coll=None):
    """wall plane whose painted texture repeats every tw metres across (wainscot stays at the floor)"""
    o=plane(n,c,w,h,wmat(img,emit),coll=coll,face=face); uv=o.data.uv_layers[0]
    for i,(u,v) in enumerate([(0,0),(1,0),(1,1),(0,1)]): uv.data[i].uv=(u*w/tw,v)
    o['noink']=1; return o
def room(p,cx,w,d,h,wall,floor,ftile=2.2,ceil=(232,220,196),side=None,emit=0.1):
    box(p+'_floor',(cx,0,-0.05),(w,d,0.1),surf(p+'fl',floor,(ftile,ftile)),bv=0)
    wallcard(p+'_wb',(cx,d/2,h/2),w,h,wall,'-Y',h,emit)
    wallcard(p+'_wl',(cx-w/2,0,h/2),d,h,side or wall,'+X',h,emit)
    wallcard(p+'_wr',(cx+w/2,0,h/2),d,h,side or wall,'-X',h,emit)
    c=plane(p+'_ceil',(cx,0,h),w,d,flat(p+'ceil',lin(ceil),0.9,emit=0.25),horiz=True); c.rotation_euler=(math.pi,0,0); c['noink']=1
    for sx in(-1,1): box(f'{p}_base{sx}',(cx+sx*(w/2-0.03),0,0.06),(0.06,d,0.12),flat('trim_'+p,lin((96,62,40)),0.7),bv=0.01)
    box(p+'_baseb',(cx,d/2-0.03,0.06),(w,0.06,0.12),flat('trim_'+p,lin((96,62,40)),0.7),bv=0.01)
    box(p+'_crown',(cx,d/2-0.04,h-0.06),(w,0.08,0.12),flat('crown_'+p,lin((236,226,206)),0.7),bv=0.01)
FRAME=flat('winframe',lin((240,232,214)),0.6)
def onwall(n,c,face):
    e=empty(n,c); e.rotation_euler=(0,0,L.FACING[face]); return e
def window(n,c,w,h,img,face='-Y',coll=None,img2=None,swap=None):
    """painted view card (emissive) + frame, mullions and sill, all just in front of the wall"""
    e=onwall(n,c,face)
    v=plane(n+'_view',(0,-0.01,0),w,h,card_mat('v_'+img,img,emit=1.1),coll=coll); v.parent=e; v['noink']=1
    if img2:
        v2=plane(n+'_view2',(0,-0.012,0),w,h,card_mat('v_'+img2,img2,emit=1.1),coll=coll); v2.parent=e; v2['noink']=1
        vis(v,[(0,swap-1)]); vis(v2,[(swap,END)])
    for nm,lc,sz in [('t',(0,-0.04,h/2+0.05),(w+0.24,0.08,0.1)),('b',(0,-0.04,-h/2-0.05),(w+0.24,0.08,0.1)),('l',(-w/2-0.06,-0.04,0),(0.1,0.08,h+0.2)),('r',(w/2+0.06,-0.04,0),(0.1,0.08,h+0.2)),
                     ('mv',(0,-0.03,0),(0.05,0.05,h)),('mh',(0,-0.03,h*0.08),(w,0.05,0.05)),('sill',(0,-0.11,-h/2-0.12),(w+0.36,0.22,0.06))]:
        b=box(f'{n}_{nm}',lc,sz,FRAME,coll=coll,bv=0.008); b.parent=e
    return e
def wallprop(n,c,w,h,img,face='-Y',emit=0.15,coll=None,frame=None,depth=0.04):
    """picture, map or board hung on a wall: card plus an optional wooden frame"""
    e=onwall(n,c,face)
    p=plane(n,(0,(-depth-0.006) if frame else -0.006,0),w,h,card_mat('p_'+img,img,emit=emit),coll=coll); p.parent=e; p['noink']=1
    if frame:
        fm=flat('fr_%d_%d_%d'%frame,lin(frame),0.5)
        for nm,lc,sz in [('t',(0,-depth/2,h/2+0.03),(w+0.1,depth,0.06)),('b',(0,-depth/2,-h/2-0.03),(w+0.1,depth,0.06)),('l',(-w/2-0.03,-depth/2,0),(0.06,depth,h)),('r',(w/2+0.03,-depth/2,0),(0.06,depth,h))]:
            b=box(f'{n}_f{nm}',lc,sz,fm,coll=coll,bv=0.005); b.parent=e
    return p
def desk(n,c,w,d,h,m,coll=None):
    box(n+'_top',(c[0],c[1],h-0.03),(w+0.08,d+0.06,0.06),m,coll=coll,bv=0.01)
    box(n+'_body',(c[0],c[1]+0.03,(h-0.06)/2),(w,d-0.06,h-0.06),m,coll=coll,bv=0.02)
    for k in range(2): box(f'{n}_drw{k}',(c[0]+(k-0.5)*w*0.5,c[1]-d/2+0.01,h*0.62),(w*0.4,0.03,h*0.22),m,coll=coll,bv=0.01)
    for k in range(2): sph(f'{n}_knob{k}',(c[0]+(k-0.5)*w*0.5,c[1]-d/2-0.02,h*0.62),0.025,flat('brass',lin((206,170,90)),0.35,metal=0.6),coll=coll)
def paper(n,c,w,h,img,rotz=0.0,coll=None,emit=0.2,tilt=0.0):
    o=plane(n,c,w,h,card_mat(img,img,emit=emit),coll=coll,horiz=True); o.rotation_euler=(tilt,0,rotz); o['noink']=1; return o
def oillamp(n,c,coll=None,energy=40):
    cyl(n+'_base',(c[0],c[1],c[2]+0.04),0.07,0.08,flat('brass',lin((206,170,90)),0.35,metal=0.6),v=14,coll=coll)
    cyl(n+'_stem',(c[0],c[1],c[2]+0.13),0.02,0.12,flat('brass',lin((206,170,90)),0.35,metal=0.6),v=8,coll=coll)
    g=sph(n+'_glass',(c[0],c[1],c[2]+0.26),0.075,flat('lampglow',lin((255,214,140)),0.3,emit=5.0),sc_=(1,1,1.3),coll=coll); g['noink']=1
    cyl(n+'_chim',(c[0],c[1],c[2]+0.38),0.03,0.12,flat('chimglass',lin((236,226,206)),0.3,emit=1.0),v=10,coll=coll)
    return light(n+'_L','POINT',(c[0],c[1],c[2]+0.3),energy,(1.0,0.78,0.5),0.08,coll=coll)
def inkwell(n,c,coll=None):
    cyl(n,(c[0],c[1],c[2]+0.03),0.035,0.06,flat('inkglass',lin((40,40,60)),0.3),v=12,coll=coll)
    q=cyl(n+'_quill',(c[0]+0.03,c[1],c[2]+0.16),0.006,0.26,flat('quillshaft',lin((236,230,214)),0.6),v=6,coll=coll,rot=(0,math.radians(20),0))
    f=plane(n+'_feather',(c[0]+0.07,c[1],c[2]+0.22),0.05,0.18,flat('feather',lin((246,240,228)),0.8),coll=coll); f.rotation_euler=(math.radians(90),math.radians(20),0); f['noink']=1
def stack(n,c,k,img,coll=None,step=0.012,seed=0,size=(0.24,0.32),frames=None):
    """paper pile, one sheet card per layer; frames (list) makes it grow on ones"""
    rr=random.Random(seed); out=[]
    for i in range(k):
        o=paper(f'{n}{i}',(c[0]+rr.uniform(-0.02,0.02),c[1]+rr.uniform(-0.02,0.02),c[2]+0.012+i*step),size[0],size[1],img,rr.uniform(-0.25,0.25),coll=coll)
        if frames: vis(o,[(frames[i],END)])
        out.append(o)
    b=box(n+'_block',(c[0],c[1],c[2]+k*step/2),(size[0]*0.92,size[1]*0.92,max(0.004,k*step-0.004)),flat('paperblock',lin((236,228,206)),0.8),coll=coll,bv=0.002)
    if frames: vis(b,[(frames[0],END)])
    return out
def basket(n,c,coll=None):
    cyl(n,(c[0],c[1],c[2]+0.19),0.17,0.38,surf('wicker','crate',(0.3,0.3)),v=16,coll=coll,r2=0.21)
    o=cyl(n+'_in',(c[0],c[1],c[2]+0.37),0.19,0.02,flat('basketin',lin((60,40,30)),0.9),v=16,coll=coll); o['noink']=1
def shelfunit(n,c,w,h,face='-Y',coll=None):
    e=onwall(n,c,face)
    b=box(n+'_case',(0,-0.18,0),(w,0.36,h),surf('deskdarkm','deskdark',(1.2,1.2)),coll=coll,bv=0.02); b.parent=e
    p=plane(n+'_books',(0,-0.365,0),w*0.92,h*0.94,card_mat('shelf','shelf',emit=0.18),coll=coll); p.parent=e; p['noink']=1
    return e
def chair(n,c,rotz=0.0,coll=None,m=None):
    m=m or surf('deskdarkm','deskdark',(1.2,1.2)); e=empty(n,c,coll=coll); e.rotation_euler=(0,0,rotz)
    for nm,lc,sz in [('seat',(0,0,0.42),(0.44,0.42,0.05)),('back',(0,0.19,0.78),(0.44,0.04,0.66))]+[(f'leg{i}',(sx*0.19,sy*0.18,0.2),(0.04,0.04,0.4)) for i,(sx,sy) in enumerate([(-1,-1),(1,-1),(-1,1),(1,1)])]:
        b=box(f'{n}_{nm}',lc,sz,m,coll=coll,bv=0.008); b.parent=e
    return e
def pie(n,c,coll=None):
    cyl(n+'_tin',(c[0],c[1],c[2]+0.02),0.15,0.04,flat('pietin',lin((150,150,156)),0.4,metal=0.5),v=20,coll=coll)
    cyl(n,(c[0],c[1],c[2]+0.05),0.135,0.04,flat('piecrust',lin((214,150,80)),0.8),v=20,coll=coll)
def plate(n,c,coll=None):
    cyl(n,(c[0],c[1],c[2]+0.01),0.13,0.02,flat('plate',lin((246,242,232)),0.4),v=20,coll=coll)
def crate(n,c,s=0.5,coll=None):
    return box(n,(c[0],c[1],c[2]+s/2),(s,s,s),surf('cratem','crate',(0.6,0.6)),coll=coll,bv=0.02)
def sack(n,c,coll=None,s=1.0):
    return sph(n,(c[0],c[1],c[2]+0.22*s),0.26*s,surf('sackm','sackcloth',(0.6,0.6)),sc_=(1.0,0.8,0.9),coll=coll,seg=14)
DESKM=surf('deskm','desk',(1.2,1.2)); DARK=surf('deskdarkm','deskdark',(1.2,1.2))
# ======================= SET P: the editor's office, Philadelphia (x=0). S01 S07 S08 S10 (day), S13 S14 S15 (night) =======================
PX=0
room('P',PX,7,6,3.4,'wp_office','floor_office')
P_DAY=shared('P_day',['S01','S07','S08','S10']); P_NIGHT=shared('P_night',['S13','S14','S15'])
window('P_win',(PX+1.9,2.98,1.85),1.3,1.5,'win_phil',coll=P_DAY); window('P_winN',(PX+1.9,2.98,1.85),1.3,1.5,'win_phil_night',coll=P_NIGHT)
shelfunit('P_shelf',(PX-2.4,3.0,1.3),1.6,2.6)
PG_AT=json.load(open('/root/dc/bridge16/pg_at.json')) if os.path.exists('/root/dc/bridge16/pg_at.json') else (PX-0.25,1.55)
PMAP=wallprop('P_map',(PX-0.35,3.0,1.62),1.6,1.0,'map_land',frame=(120,80,50))   # dc14 (346): hung 0.3 m lower so the editor can reach it in S08
desk('P_desk',(PX,0.9),1.5,0.7,0.62,DESKM)
inkwell('P_ink',(PX+0.32,0.78,0.62)); oillamp('P_lamp',(PX+0.58,1.05,0.62),energy=30)
PILE=stack('P_pile',(PX-0.5,0.9,0.62),4,'letter1',seed=3)
GROW=stack('P_grow',(PX-0.5,0.9,0.62+4*0.012+0.012),5,'letter2',seed=4,frames=[0,905,928,951,964])   # S10: one more letter on each "wrote"
paper('P_sheet',(PX+0.05,0.78,0.635),0.26,0.34,'letter_hero',0.08)
chair('P_chair',(PX-1.6,0.4,0),0.5); box('P_rug',(PX,0.4,0.004),(3.0,2.0,0.008),flat('rugP',lin((128,50,46)),0.9),bv=0)
light('P_fill','AREA',(PX,0.2,3.25),520,(1.0,0.9,0.78),5.0,coll=P_DAY)
light('P_fillN','AREA',(PX,0.2,3.25),120,(1.0,0.78,0.55),5.0,coll=P_NIGHT)   # rule 317: the night room keeps a lit ceiling and walls, no black band
light('P_moon','AREA',(PX+1.9,2.6,1.9),60,(0.55,0.62,1.0),1.2,rot=(math.radians(-90),0,0),coll=P_NIGHT)
# S08: the "ONE DAY OF THANKS" page pinned on the map on "thing"
PGX,PGZ=PG_AT   # dc14 (346): the page appears where the editor's mitten presses it (handpos.py at the reach peak)
c8=C('S08'); pg=wallprop('S08_page',(PGX,2.96,PGZ),0.36,0.48,'page_print',coll=c8,depth=0.02); vis(pg,[(719,END)])
# S15: wall year calendar beside the window, flips on ones (For 17 years)
YC=[wallprop(f'S15_y{y}',(PX+0.85,2.995,1.6),0.4,0.5,f'ycal{y}',coll=C('S15'),depth=0.015,emit=0.25) for y in (1846,1850,1854,1858,1861,1863)]
for o_,(a,b) in zip(YC,[(1439,1445),(1446,1451),(1452,1457),(1458,1462),(1463,1468),(1469,END)]): vis(o_,[(a,b)])
box('S15_nail',(PX+0.85,2.97,1.88),(0.02,0.03,0.02),INK,coll=C('S15'),bv=0)
# S07: the little lamb trots across the desk
c7=C('S07'); lamb=plane('S07_lamb',(PX-0.6,0.8,0.80),0.34,0.34,card_mat('lamb','lamb',emit=0.25),coll=c7); lamb['noink']=1
for f in range(626,673,2):
    t=(f-626)/46; kloc(lamb,f,(PX-0.62+1.0*t,0.78,0.80+0.04*abs(math.sin(t*math.pi*5))))
onone(lamb)
# S14: quill close-up, the line of writing grows (letter cards swap on ones)
c14=C('S14'); LT=[paper(f'S14_l{k}',(PX+0.05,0.78,0.637+0.002*k),0.26,0.34,f'letter{k}',0.08,coll=c14) for k in range(6)]
for k,o_ in enumerate(LT): vis(o_,[(1391+k*8,1391+k*8+7 if k<5 else END)])
qq=empty('S14_quill',(PX,0.75,0.70),coll=c14)
s_=cyl('S14_qs',(0,0,0.0),0.006,0.30,flat('quillshaft',lin((236,230,214)),0.6),v=6,coll=c14,rot=(0,math.radians(28),0)); s_.parent=qq
fq=plane('S14_qf',(0.05,0,0.07),0.06,0.22,flat('feather',lin((246,240,228)),0.8),coll=c14); fq.rotation_euler=(math.radians(90),math.radians(28),0); fq.parent=qq; fq['noink']=1
for f in range(1391,1439,2):
    t=(f-1391)/47; kloc(qq,f,(PX-0.05+0.16*((f//2)%6)/5,0.70+0.12*t,0.70+0.02*((f//2)%2)))
onone(qq)
# ======================= SET W: the Washington mail room (x=600). S03 S04 S05 (day), S12 (night) =======================
WX=600
room('W',WX,8,6,3.4,'plaster_clerk','floor_clerk',emit=0.12)
W_DAY=shared('W_day',['S03','S04','S05'])
window('W_win',(WX-3.98,0.2,1.8),1.3,1.5,'win_wash',face='+X',coll=W_DAY); window('W_winN',(WX-3.98,0.2,1.8),1.3,1.5,'win_war',face='+X',coll=C('S12'))
pg_=onwall('W_pigeon',(WX+1.6,3.0,1.65),'-Y'); b=box('W_pigeonbox',(0,-0.12,0),(2.7,0.24,1.8),DARK,bv=0.02); b.parent=pg_
pp=plane('W_pigeonface',(0,-0.245,0),2.6,1.72,card_mat('pigeon','pigeon',emit=0.18)); pp.parent=pg_; pp['noink']=1
wallprop('W_states',(WX-1.9,3.0,2.05),2.4,1.2,'states_board',frame=(96,62,40),emit=0.2)
wallprop('W_sign',(WX+1.6,3.0,2.85),1.6,0.4,'sign_mail',depth=0.03,emit=0.2)
desk('W_counter',(WX+0.4,1.0),2.2,0.7,0.62,DARK)
stack('W_cpile',(WX+1.1,0.95,0.62),6,'env',seed=7,size=(0.3,0.2))
for i,(x,y) in enumerate([(-2.8,2.2),(-3.2,1.2),(2.9,2.2)]): sack(f'W_sack{i}',(WX+x,y,0))
for i,(x,y) in enumerate([(3.2,1.0),(3.0,0.2)]): crate(f'W_crate{i}',(WX+x,y,0),0.55)
chair('W_chair',(WX-2.4,-0.8,0),0.6,m=DARK)
light('W_fill','AREA',(WX,0.2,3.25),560,(1.0,0.92,0.8),5.0,coll=W_DAY)
light('W_fillN','AREA',(WX,0.2,3.25),110,(1.0,0.75,0.5),5.0,coll=C('S12')); light('W_glowN','AREA',(WX-3.7,0.2,1.8),90,(1.0,0.45,0.3),1.4,rot=(0,math.radians(90),0),coll=C('S12'))
oillamp('W_lampN',(WX-0.3,0.85,0.62),coll=C('S12'),energy=35)
# S03: red crosses pop on the states board on "some just had none"
c3=C('S03'); RED=flat('redx',lin((190,40,40)),0.6,emit=0.3)
for i,(x,z,f) in enumerate([(-2.6,2.35,264),(-1.9,1.9,270),(-1.2,2.4,277),(-2.3,1.75,285),(-1.5,1.75,293)]):
    for k in(-1,1):
        o_=box(f'S03_x{i}{k}',(WX+x,2.955,z),(0.2,0.01,0.035),RED,coll=c3,bv=0); o_.rotation_euler=(0,math.radians(45*k),0); vis(o_,[(f,END)])
# S04: mail piles up on the floor (grows on ones) while the mailman empties his sack
c4=C('S04'); MP=[]
rr=random.Random(5)
for i in range(16):
    f=318+i*5; o_=paper(f'S04_m{i}',(WX-1.3+rr.uniform(-0.35,0.35),1.6+rr.uniform(-0.3,0.3),0.01+0.03*(i//4)),0.3,0.2,'env',rr.uniform(-1,1),coll=c4); o_.rotation_euler=(rr.uniform(-0.3,0.3),rr.uniform(-0.3,0.3),rr.uniform(-1,1)); vis(o_,[(f,END)])
for i in range(4):
    sp=sph(f'S04_mound{i}',(WX-1.3,1.6,0.0),0.45+0.08*i,flat('paperblock',lin((236,228,206)),0.8),sc_=(1.0,0.8,0.25),coll=c4,seg=12); vis(sp,[(330+i*18,END)])
for k,f in enumerate((317,331,346,359)): fx(f'S04_puff{k}','fx_paper',(WX-1.3,1.5,0.5),f,14,0.7,c4,grow=1.8,rise=0.3)
# S05: letters keep dropping behind the clerk
c5=C('S05')
for k,f in enumerate((430,452,474)):
    o_=paper(f'S05_drop{k}',(WX+1.1,1.9,1.6),0.3,0.2,'env',0.2*k,coll=c5); fall(o_,f,10,(WX+1.1-0.25*k,1.95,1.7),(WX+1.1-0.25*k,1.95,0.66),(0.6,0,0),(0.0,0.3,0.8)); vis(o_,[(f,f+16)])
# S12: the untouched pie on the counter (night)
c12=C('S12'); pie('S12_pie',(WX+0.0,0.85,0.62),coll=c12); stack('S12_pile',(WX+0.9,0.95,0.62),9,'env',coll=c12,seed=9,size=(0.3,0.2))
fx('S12_steam','fx_smoke',(WX+0.0,0.85,0.85),1290,24,0.25,c12,grow=1.8,rise=0.15)
# ======================= SET O: the President's office, Washington (x=1200). S02 S11 S17 S18 =======================
OX=1200
room('O',OX,8,6,3.6,'wp_pres','carpet_pres',ftile=1.6)
window('O_win',(OX+2.2,2.98,1.95),1.4,1.8,'win_wash',img2='win_war',swap=1230)
OMAP=wallprop('O_map',(OX-1.55,3.0,2.1),1.9,1.19,'map_land',frame=(120,80,50))
ML=wallprop('O_mapL',(OX-1.55,2.995,2.1),1.9,1.19,'map_L',depth=0.045); MR=wallprop('O_mapR',(OX-1.55,2.993,2.1),1.9,1.19,'map_R',depth=0.047)
vis(OMAP,[(0,1193)]); vis(ML,[(1194,END)]); vis(MR,[(1194,END)])
for o_,sx in((ML,-1),(MR,1)):
    e_=o_.parent
    for f in range(1194,1213,2): t=min(1,(f-1194)/16); kloc(e_,f,(OX-1.55+sx*0.22*t,3.0,2.1-0.06*t)); krot(e_,f,(0,sx*math.radians(5)*t,0))
    onone(e_)
fx('O_tear','fx_dust',(OX-1.55,2.9,2.1),1194,16,0.6,C('S11'),grow=2.0)
shelfunit('O_shelf',(OX-3.6,1.4,1.3),1.6,2.6,face='+X')
desk('O_desk',(OX,1.0),1.8,0.8,0.64,DESKM)
oillamp('O_lamp',(OX-0.7,1.15,0.64),energy=30); inkwell('O_ink',(OX+0.45,0.85,0.64))
stack('O_pile',(OX+0.6,1.1,0.64),5,'letter3',seed=12)
basket('O_bin',(OX+1.25,0.55,0))
chair('O_chair',(OX+2.9,1.4,0),math.pi*0.8,m=DARK)
box('O_rug',(OX,0.6,0.004),(3.4,2.2,0.008),flat('rugO',lin((40,60,110)),0.9),bv=0)
light('O_fill','AREA',(OX,0.2,3.45),600,(1.0,0.92,0.82),5.5)
# the war glow through the window (S11, from "war")
wl=light('O_war','AREA',(OX+2.2,2.6,1.9),0,(1.0,0.4,0.25),1.4,rot=(math.radians(-90),0,0),coll=C('S11'))
for f,e_ in[(1229,0),(1231,140),(1235,90),(1238,160)]: wl.data.energy=e_; wl.data.keyframe_insert('energy',frame=f)
for k,(x,f) in enumerate([(-0.3,1232),(0.25,1235)]): fx(f'O_smoke{k}','fx_smoke',(OX+2.2+x,2.93,1.7),f,8,0.5,C('S11'),grow=1.5,rise=0.2)
# letters tossed into the bin: S02 (four, on "four of them did not do a thing") and S11 (one per president)
def toss(n,f,coll,src=(OX+0.55,0.9,0.95)):
    o_=paper(n,src,0.3,0.2,'env',0.4,coll=coll); fall(o_,f,10,src,(OX+1.25,0.55,0.36),(0.3,0,0.4),(1.2,0.4,2.0)); vis(o_,[(f,f+12)])
    fx(n+'_puff','fx_paper',(OX+1.25,0.5,0.45),f+10,12,0.35,coll,grow=1.7,rise=0.15)
for k,f in enumerate((101,110,120,134)): toss(f'S02_t{k}',f,C('S02'),(OX+0.5+0.05*k,0.9,0.95))
for k,f in enumerate((1040,1068,1104,1140)): toss(f'S11_t{k}',f,C('S11'))
# S17: the envelope arrives on the desk;   S18: proclamation stamped YES, desk calendar flips
c17=C('S17'); envl=paper('S17_env',(OX-0.05,0.8,0.645),0.36,0.24,'env',0.0,coll=c17); envl['fly']=1
for f in range(1592,1611,2): t=min(1,(f-1598)/10) if f>=1598 else 0; kloc(envl,f,(OX-0.05,0.2+0.6*t,0.645+0.15*(1-t)))
onone(envl); fx('S17_spark','fx_spark',(OX-0.05,0.75,0.8),1626,14,0.35,c17,grow=1.4)
c18=C('S18')
pr0=paper('S18_procl',(OX-0.1,0.78,0.70),0.34,0.46,'procl',0.0,coll=c18,tilt=math.radians(-55)); pr1=paper('S18_proclY',(OX-0.1,0.779,0.701),0.34,0.46,'procl_yes',0.0,coll=c18,tilt=math.radians(-55))
for o_ in (pr0,pr1): o_.rotation_euler=(math.radians(55),0,0)
vis(pr0,[(1638,1681)]); vis(pr1,[(1682,END)]); fx('S18_spark','fx_spark',(OX-0.1,0.7,0.95),1682,16,0.5,c18,grow=1.5)
DC=[]
for i,f in enumerate((1638,1693,1700,1706,1711,1715)):
    o_=plane(f'S18_cal{i}',(OX+0.55,0.86,0.80),0.18,0.225,card_mat(f'dcal{i}',f'dcal{i}',emit=0.25),coll=c18); o_['noink']=1; DC.append(o_)
for i,o_ in enumerate(DC): vis(o_,[((1638,1693,1700,1706,1711,1715)[i],(1692,1699,1705,1710,1714,END)[i])])
box('S18_calstand',(OX+0.55,0.88,0.68),(0.2,0.06,0.08),DARK,coll=c18,bv=0.01)
# ======================= SET R: the magazine's print room, Philadelphia (x=1800). S06 S09 =======================
RX=1800
room('R',RX,9,6,3.8,'brick_print','floor_clerk',side='plaster_print',emit=0.12)
window('R_win',(RX-3.0,2.98,2.0),1.2,1.6,'win_phil')
wallprop('R_sign',(RX+0.6,3.0,3.2),2.4,0.6,'sign_print',depth=0.03,emit=0.2)
wallprop('R_cover',(RX-1.1,3.0,2.0),0.9,1.2,'magazine',frame=(120,80,50),emit=0.2)
# hand press: two uprights, head, platen, bed, lever and wheel (our own design)
IRON=flat('iron',lin((58,58,66)),0.45,metal=0.4)
PRX,PRY=RX+1.3,1.6
for sx in(-1,1): box(f'R_up{sx}',(PRX+sx*0.45,PRY,0.95),(0.14,0.3,1.9),IRON,bv=0.02)
box('R_head',(PRX,PRY,1.82),(1.1,0.34,0.22),IRON,bv=0.03); box('R_bed',(PRX,PRY-0.15,0.78),(1.0,1.2,0.12),IRON,bv=0.02)
box('R_bedtop',(PRX,PRY-0.15,0.85),(0.8,0.9,0.02),flat('typebed',lin((90,90,100)),0.5),bv=0)
PLATEN=box('R_platen',(PRX,PRY,1.2),(0.7,0.5,0.08),IRON,bv=0.02); cyl('R_screw',(PRX,PRY,1.36),0.05,0.88,IRON,v=10)
LEVER=empty('R_leverpiv',(PRX+0.3,PRY,1.5)); lv=cyl('R_lever',(0.35,0,0),0.03,0.7,IRON,v=8,rot=(0,math.radians(90),0)); lv.parent=LEVER
for i,(x,f) in enumerate([(0,0)]): pass
cyl('R_wheel',(PRX-0.545,PRY,0.95),0.32,0.05,IRON,v=20,rot=(0,math.radians(90),0))
for f,a in[(802,0),(833,-35),(840,0),(853,-35),(860,0),(872,-35),(879,0),(887,-35),(892,-20)]: krot(LEVER,f,(0,0,math.radians(a)))
for f,z in[(802,1.2),(833,0.92),(840,1.2),(853,0.92),(860,1.2),(872,0.92),(879,1.2),(887,0.92),(892,1.0)]: kloc(PLATEN,f,(PRX,PRY,z))
onone(LEVER); onone(PLATEN)
c9=C('S09'); stack('S09_out',(PRX+0.9,PRY-0.4,0.66),6,'page_print',coll=c9,seed=21,size=(0.3,0.4),frames=[802,836,856,875,890,892])
box('S09_table',(PRX+0.9,PRY-0.4,0.33),(0.6,0.6,0.66),DARK,coll=c9,bv=0.02)
for k,f in enumerate((834,854,873)): fx(f'S09_puff{k}','fx_paper',(PRX+0.9,PRY-0.5,0.85),f,14,0.4,c9,grow=1.6,rise=0.2)
for i,(x,y,h) in enumerate([(-2.0,1.8,0.9),(-1.5,2.1,1.1),(-2.4,1.2,0.7),(-0.6,1.95,0.8),(2.8,1.0,0.9),(3.2,2.0,1.1)]):
    box(f'R_stack{i}',(RX+x,y,h/2),(0.5,0.62,h),flat('magpaper',lin((238,230,212)),0.8),bv=0.01)
    paper(f'R_stacktop{i}',(RX+x,y,h+0.012),0.46,0.6,'magazine',R.uniform(-0.2,0.2))
    for k in range(int(h/0.12)): box(f'R_band{i}{k}',(RX+x,y-0.311,0.08+k*0.12),(0.5,0.005,0.012),flat('magband',lin((150,60,90)),0.8),bv=0)
c6=C('S06'); mg=wallprop('S06_mag',(RX-0.7,1.495,0.95),0.36,0.48,'magazine',coll=c6,depth=0.01,emit=0.25); vis(mg,[(580,END)])
box('S06_stand',(RX-0.7,1.6,0.47),(0.5,0.25,0.94),flat('magpaper',lin((238,230,212)),0.8),coll=c6,bv=0.01)
fx('S06_spark','fx_spark',(RX-0.7,1.45,1.25),580,14,0.35,c6,grow=1.4)
light('R_fill','AREA',(RX,0.2,3.65),700,(1.0,0.92,0.8),6.0)
# ======================= SET S: a Washington street in autumn 1863 (x=2400). S16 =======================
SX=2400
box('S_street',(SX,10,-0.06),(10,70,0.12),surf('cobblem','cobble',(1.2,1.2)),bv=0)
for sx in(-1,1): box(f'S_walk{sx}',(SX+sx*4.0,10,0.06),(2.0,70,0.12),flat('walkstone',lin((176,166,150)),0.85),bv=0.01)
for sx,face_ in((-1,'+X'),(1,'-X')):
    wallcard(f'S_rows{sx}',(SX+sx*5.0,10,4.5),70,9.0,'rows',face_,12.0,emit=0.25)
    for k in range(8): box(f'S_stoop{sx}{k}',(SX+sx*4.75,-14+k*6,0.2),(0.5,1.2,0.4),flat('stoop',lin((170,150,130)),0.8),bv=0.02)
skydome('S_sky',(SX,10),120,90,'sky_fall')
far=plane('S_far',(SX,44,6),14,14,card_mat('street_far','street_far',emit=0.6),coll=L.C_NOI,face='-Y'); far['fly']=1
for i,(x,y) in enumerate([(-3.4,-2),(3.4,4),(-3.4,10),(3.4,16),(-3.4,22)]):
    for k in range(2):
        t_=plane(f'S_tree{i}{k}',(SX+x,y,2.0),3.0,4.0,card_mat(f'tree{i%2}',f'tree{i%2}',emit=0.25),face='-Y'); t_.rotation_euler=(0,0,math.radians(k*90+20)); t_['noink']=1
    cyl(f'S_trunk{i}',(SX+x,y,0.6),0.09,1.2,flat('trunk',lin((90,60,40)),0.8),v=8)
for i,y in enumerate([-6,6,18]):
    for sx in(-1,1):
        cyl(f'S_lp{i}{sx}',(SX+sx*3.2,y,1.4),0.05,2.8,IRON,v=8); g=sph(f'S_lpg{i}{sx}',(SX+sx*3.2,y,2.9),0.14,flat('lampglow',lin((255,214,140)),0.3,emit=5.0),sc_=(1,1,1.3)); g['noink']=1
c16=C('S16')
for k in range(14):
    f0=1484+k*8; x=SX+R.uniform(-2.5,2.5); y=R.uniform(-1,6)
    lf=plane(f'S16_leaf{k}',(x,y,3.2),0.5,0.5,card_mat('fx_leaves','fx_leaves',emit=0.4),coll=c16,face='-Y'); lf['noink']=1; lf['fly']=1
    for f in range(f0,f0+41,2):
        t=(f-f0)/40; kloc(lf,f,(x+0.4*math.sin(t*6),y,3.2-3.1*t)); krot(lf,f,(0,0,math.radians(40*math.sin(t*8))))
    onone(lf); vis(lf,[(f0,f0+40)])
for k,f in enumerate((1584,1590)): fx(f'S16_gust{k}','fx_leaves',(SX-0.5+k,1.0,1.2),f,14,1.0,c16,grow=1.8,rise=0.3)
light('S_sunfill','SUN',(SX,0,10),1.2,(1.0,0.75,0.55),2.0,rot=(math.radians(60),0,math.radians(-30)),coll=c16)
# ======================= SET H: the long table, a hall (x=3000). S19 =======================
HX=3000
room('H',HX,10,6,4.0,'wp_hall','floor_office')
for k,x in enumerate((-3.0,3.0)): window(f'H_win{k}',(HX+x,2.98,2.1),1.3,1.8,'win_phil')
wallprop('H_banner',(HX,3.0,3.2),4.0,0.75,'banner_thanks',depth=0.02,emit=0.25)
TBL=(HX,0.9)
box('H_table',(HX,0.9,0.31),(5.6,1.0,0.62),DARK,bv=0.02)
paper('H_cloth',(HX,0.9,0.632),5.8,1.15,'cloth_hall',0.0,emit=0.12)
sk=plane('H_skirt',(HX,0.32,0.45),5.8,0.34,card_mat('cloth_hall','cloth_hall',emit=0.12),face='-Y'); sk['noink']=1
for i in range(9): plate(f'H_plate{i}',(HX-2.4+i*0.6,0.7,0.63))
plate('H_platter',(HX-0.2,1.0,0.63)); tk=plane('H_turkey',(HX-0.2,1.0,0.85),0.62,0.41,card_mat('turkey','turkey',emit=0.25),face='-Y'); tk['noink']=1
pie('H_pie1',(HX+1.0,1.0,0.63)); pie('H_pie2',(HX-1.6,1.05,0.63))
for i,x in enumerate((-2.1,1.8)):
    cyl(f'H_candle{i}',(HX+x,1.0,0.75),0.025,0.24,flat('wax',lin((240,230,200)),0.6),v=10); g=sph(f'H_flame{i}',(HX+x,1.0,0.9),0.025,flat('flame',lin((255,200,110)),0.3,emit=8.0),sc_=(1,1,1.8)); g['noink']=1
light('H_fill','AREA',(HX,0.2,3.85),760,(1.0,0.9,0.76),7.0)
c19=C('S19'); pie('S19_pie',(HX+2.2,1.0,0.63),coll=c19)   # brought in on "one big table"
vis(bpy.data.objects['S19_pie'],[(1866,END)]); vis(bpy.data.objects['S19_pie_tin'],[(1866,END)])
fx('S19_spark','fx_spark',(HX+2.2,0.95,0.9),1866,14,0.4,c19,grow=1.4)
# ======================= SET T: a dining room in Washington today (x=3600). S20 S21 (payoff) =======================
TX=3600
room('T',TX,8,6,3.2,'wp_today','floor_today')
window('T_win',(TX-1.7,2.98,1.75),1.3,1.5,'win_today')
box('T_rug',(TX,0.5,0.004),(3.6,2.6,0.008),surf('carpetT','carpet_today',(1.2,1.2)),bv=0)
box('T_table',(TX-0.4,0.8,0.31),(2.4,1.0,0.62),DARK,bv=0.02)
paper('T_cloth',(TX-0.4,0.8,0.632),2.6,1.15,'cloth_today',0.0,emit=0.12)
sk=plane('T_skirt',(TX-0.4,0.22,0.45),2.6,0.34,card_mat('cloth_today','cloth_today',emit=0.12),face='-Y'); sk['noink']=1
for i in range(4): plate(f'T_plate{i}',(TX-1.3+i*0.6,0.62,0.63))
plate('T_platter',(TX-0.4,0.95,0.63)); tk=plane('T_turkey',(TX-0.4,0.95,0.85),0.62,0.41,card_mat('turkey','turkey',emit=0.25),face='-Y'); tk['noink']=1
pie('T_pie',(TX+0.45,0.95,0.63))
FL=wallprop('T_letter',(TX+0.75,3.0,1.85),0.42,0.56,'framed_letter',frame=(150,110,60),emit=0.2)
# the poster: gilt frame on the dining room wall, pasted at true colour in post (posterquad)
PW,PH=0.80,1.20; PZ=1.72; PXP=TX+2.0; PY=2.94
box('poster_frame',(PXP,PY+0.03,PZ),(PW+0.12,0.04,PH+0.12),flat('pframe',lin((214,180,110)),0.35,emit=0.4),bv=0.01)
pmat=bpy.data.materials.new('poster'); N_,L_=L.nodes(pmat); pp_=N_['Principled BSDF']; it_=N_.new('ShaderNodeTexImage'); it_.image=bpy.data.images.load('/root/dc/poster_2k.png'); it_.interpolation='Cubic'
L_.new(it_.outputs['Color'],pp_.inputs['Base Color']); L_.new(it_.outputs['Color'],pp_.inputs['Emission Color']); pp_.inputs['Emission Strength'].default_value=0.15; pp_.inputs['Roughness'].default_value=1.0; pp_.inputs['Specular IOR Level'].default_value=0.0
poster=plane('poster',(PXP,PY,PZ),PW,PH,pmat,coll=L.C_NOI); poster['noink']=1
box('T_side',(TX+2.0,2.6,0.4),(1.2,0.45,0.8),DARK,bv=0.02); oillamp('T_lamp',(TX+1.6,2.6,0.8),energy=20)
chair('T_chair0',(TX-2.0,0.4,0),0.4)
light('T_fill','AREA',(TX,0.2,3.05),520,(1.0,0.93,0.84),5.0)
light('T_pl','AREA',(PXP,1.9,2.9),60,(1.0,0.95,0.88),1.2,rot=(math.radians(35),0,0))
# ======================= CAST + CAMERAS =======================
def S(n): return SH[n]
# ---- S01 (0-70): hook. The editor writes; the camera eases in to her (push) ----
s='S01'; r=S(s)
ed=char_on('S01_ed','editor',s,(PX,1.12,-L.FOOT_LIFT),r,'determined',arms=('arm',[(0,'arm_quill')]))   # dc15 (346): desk writers keep their rule-346 hand contact; feet hidden by the desk
faces(ed,[(0,'determined'),(22,'squint'),(40,'determined'),(58,'smug')])
work(ed,'write',[(f,-22 if (f//6)%2 else -28) for f in range(0,71,6)])   # dc14 (346): the quill mitten rests on her sheet (desk top 0.62 m)
bob(ed,[34,62])
path(s,[(0,(PX+0.95,-1.3,1.5),(PX,1.5,1.0)),(70,(PX+0.55,-0.55,1.42),(PX,1.5,1.02))])
# ---- S02 (64-162): four letters land in the President's bin (truck) ----
s='S02'; r=S(s)
pA=char_on('S02_pres','presA',s,(OX+0.35,1.6,0),r,'meh',arms=('arm',[(64,'arm_letter'),(136,'arm')]))
faces(pA,[(64,'skeptical'),(96,'side_eye'),(118,'smug'),(140,'blink'),(150,'deadpan')])
arm(pA,1,64,-30); act(pA,'throw',96); act(pA,'shrugtalk',122)
bob(pA,[100,119,140])
path(s,[(64,(OX+0.2,-1.1,1.25),(OX+0.75,1.0,0.75)),(162,(OX+1.35,-1.0,1.3),(OX+0.8,1.0,0.8))])
# ---- S03 (156-302): the states board; every state its own day (truck along the board) ----
s='S03'; r=S(s)
cl3=char_on('S03_clerk','clerk',s,(WX-1.45,1.95,0),r,'neutral',arms=('arm','arm'))
faces(cl3,[(156,'neutral'),(190,'skeptical'),(230,'grin'),(262,'shock'),(286,'annoyed')])
act(cl3,'reach',190,-1); act(cl3,'present',236,-1); act(cl3,'think',280)   # dc14 (354): named actions; outward = negative on both sides   # dc16b: reach (lean_reach), the point_out pose card is nearly straight (visual verifier f198, rule 350)
bob(cl3,[214,264,293])
path(s,[(156,(WX-0.7,-0.6,1.75),(WX-1.2,3.0,1.75)),(230,(WX-1.3,-0.5,1.75),(WX-1.6,3.0,1.75)),(302,(WX-1.9,-0.45,1.7),(WX-1.9,3.0,1.72))])
# ---- S04 (296-410): mail piles up; the mailman dumps a sack; the clerk groans (crane up / pull out) ----
s='S04'; r=S(s)
mm=char_on('S04_mail','mailman',s,(WX-2.4,1.0,0),r,'happy',arms=('arm',[(296,'arm_sack'),(330,'arm')]),walker=True)
walk(mm,296,318,(WX-3.0,0.5,0),(WX-1.5,1.0,0),step=4)   # dc15 (345): the mailman ends 0.8 m nearer than the clerk
act(mm,'throw',316)
faces(mm,[(296,'happy'),(326,'open_smile'),(356,'proud'),(380,'whistle')])
sk4=sack('S04_sack',(0,0,0),coll=C(s),s=0.8); kloc(sk4,296,(WX-3.0,0.45,0.55)); kloc(sk4,318,(WX-1.8,1.3,0.55)); fall(sk4,322,8,(WX-1.7,1.35,0.6),(WX-1.6,1.4,0.0)); onone(sk4)
fx('S04_dust','fx_dust',(WX-1.6,1.3,0.25),330,14,0.8,C(s),grow=1.8,rise=0.2)
cl4=char_on('S04_clerk','clerk',s,(WX-0.5,1.65,0),r,'neutral',arms=('arm','arm'))
faces(cl4,[(296,'neutral'),(330,'nervous'),(360,'panic'),(380,'annoyed'),(400,'groan')]); bob(cl4,[362,402]); act(cl4,'doubletake',370)   # dc16b: the snap lands at ~400, before the cut at 411
path(s,[(296,(WX-1.7,-1.5,1.45),(WX-1.35,1.4,0.85)),(350,(WX-1.3,-1.9,1.7),(WX-1.05,1.5,0.95)),(410,(WX-0.15,-1.75,1.85),(WX+0.05,1.6,1.0))])   # dc15 (shots verifier: clerk cut at the edge 315-340): framed between the two
# ---- S05 (411-500): the clerk, close: "Oh no, it's the turkey lady again." (slow push; lips on the quoted line only) ----
s='S05'; r=S(s)
cl5=char_on('S05_clerk','clerk',s,(WX+0.4,1.65,0),r,'groan',arms=('arm',[(411,'arm_letter')]))
faces(cl5,[(411,'groan'),(450,'sigh'),(490,'annoyed')]); lipsync(cl5,WORDS[48:55],415,492)
act(cl5,'wag',430); act(cl5,'wag',466)
bob(cl5,[422,461,482])
path(s,[(411,(WX+0.75,-0.75,1.5),(WX+0.4,1.65,1.12)),(500,(WX+0.62,-0.45,1.48),(WX+0.4,1.65,1.12))])
# ---- S06 (494-625): she was no nobody: the editor among her magazine stacks; a printer carries a bundle by (truck) ----
s='S06'; r=S(s)
ed6=char_on('S06_ed','editor',s,(RX-1.15,1.25,0),r,'proud',arms=('arm','arm'))
faces(ed6,[(494,'proud'),(523,'side_eye'),(546,'smug'),(580,'grin'),(605,'proud')])
arm(ed6,1,494,REST); act(ed6,'clap',536); act(ed6,'fist_pump',584)
bob(ed6,[523,560,601])
pr6=char_on('S06_printer','printer',s,(RX+2.2,2.6,0),r,'happy',walker=True)
walk(pr6,494,600,(RX+2.2,2.6,0),(RX-1.4,2.6,0),step=5); work(pr6,'carry',[(494,-35)]); drift_faces(pr6,494,625,['happy','proud','grin','whistle'],61)
path(s,[(494,(RX-0.2,-0.85,1.45),(RX-0.9,1.3,1.05)),(625,(RX-1.5,-0.8,1.45),(RX-1.0,1.3,1.05))])
# ---- S07 (626-672): Mary Had a Little Lamb: the lamb trots over her desk (insert, push) ----
s='S07'; r=S(s)
ed7=char_on('S07_ed','editor',s,(PX,1.5,0),r,'happy'); faces(ed7,[(626,'happy'),(648,'wink_grin')]); bob(ed7,[650])
path(s,[(626,(PX+0.2,-0.6,1.05),(PX,0.9,0.9)),(672,(PX+0.15,-0.35,1.02),(PX+0.05,0.9,0.9))])
# ---- S08 (666-808): one day for the whole land: she pins her page on the map (pull out on "whole land") ----
s='S08'; r=S(s)
ed8=char_on('S08_ed','editor',s,(PX+0.3,2.78,0),r,'determined',arms=([(666,'arm_page'),(721,'arm')],'arm'))   # dc14 (346): stands at the map, page in hand until she presses it on
faces(ed8,[(666,'determined'),(700,'happy'),(719,'proud'),(746,'open_smile'),(782,'happy'),(800,'proud')])
arm(ed8,-1,666,REST); act(ed8,'reach_high',713,-1); act(ed8,'point',770,-1)   # dc14 (354, 346): reach peaks at 719 when the page goes up
bob(ed8,[719,782])
fx('S08_spark','fx_spark',(PX-0.35,2.9,2.0),797,14,0.6,C(s),grow=1.5)
path(s,[(666,(PX+0.35,0.3,1.6),(PX+0.15,3.0,1.6)),(720,(PX+0.25,0.1,1.62),(PX+0.05,3.0,1.62)),(782,(PX-0.1,-1.0,1.6),(PX-0.05,3.0,1.6)),(808,(PX-0.2,-1.15,1.6),(PX-0.1,3.0,1.6))])
# ---- S09 (802-892): year after year, in print: the hand press (truck / arc) ----
s='S09'; r=S(s)
pr9=char_on('S09_printer','printer',s,(PRX+0.55,PRY-0.55,0),r,'grit',arms=('arm','arm'))
faces(pr9,[(802,'grit'),(833,'manic_grin'),(853,'squint'),(872,'grin'),(887,'proud')])
work(pr9,'press',[(802,-40),(833,-110),(840,-40),(853,-110),(860,-40),(872,-110),(879,-40),(887,-110)])
ed9=char_on('S09_ed','editor',s,(PRX+1.3,PRY-0.1,0),r,'proud'); drift_faces(ed9,802,892,['proud','happy','grin','content'],91,(16,26)); bob(ed9,[836,875]); act(ed9,'present',846,-1)
path(s,[(802,(PRX-0.6,-1.2,1.5),(PRX+0.5,PRY-0.2,1.05)),(892,(PRX+0.3,-1.45,1.5),(PRX+0.9,PRY-0.2,1.05))])
# ---- S10 (886-978): she wrote it, and wrote it, and wrote it again (push) ----
s='S10'; r=S(s)
ed10=char_on('S10_ed','editor',s,(PX,1.12,-L.FOOT_LIFT),r,'determined',arms=('arm',[(886,'arm_quill')]))
faces(ed10,[(886,'determined'),(905,'squint'),(928,'determined'),(951,'grit'),(966,'stern')])
work(ed10,'write',[(f,-22 if (f//6)%2 else -28) for f in range(886,978,6)])
bob(ed10,[905,928,951])
for k,f in enumerate((905,928,951)): fx(f'S10_puff{k}','fx_paper',(PX-0.5,0.9,0.75),f,12,0.3,C(s),grow=1.6,rise=0.1)
path(s,[(886,(PX-0.4,-1.2,1.55),(PX-0.2,1.3,0.95)),(978,(PX-0.3,-0.6,1.48),(PX-0.15,1.3,0.98))])
# ---- S11 (972-1240): THE LONG TAKE (rule 312). Four presidents in turn: nope, nope, nope, still nope; the map tears; war glow in the window ----
s='S11'; r=S(s)
def pres(kind,i,a,b,fin,fout,ftoss,stay=False,move='throw'):
    rng=(a,b)
    p=char_on(f'S11_{kind}',kind,s,(OX+1.7,1.75,0),rng,'neutral',arms=('arm',[(a,'arm_letter'),(ftoss+2,'arm')]),walker=True)
    walk(p,fin,fin+14,(OX+1.7,1.75,0),(OX,1.68,0),step=3)
    if not stay: walk(p,fout,fout+14,(OX,1.68,0),(OX-1.9,1.9,0),step=3)
    faces(p,[(a,'neutral'),(fin+16,'skeptical'),(ftoss-10,'side_eye'),(ftoss+4,'deadpan'),(ftoss+14,'smug')])
    arm(p,1,a,-30); act(p,move,ftoss-6)
    bob(p,[ftoss-2,ftoss+10]); return p
P1=pres('presA',0,972,1062,972,1046,1040)
P2=pres('presB',1,1044,1094,1044,1080,1068,move='drop')
P3=pres('presC',2,1078,1128,1078,1114,1104,move='flick')
P4=pres('presD',3,1112,1240,1112,0,1140,stay=True,move='wave'); act(P4,'huff',1154); walk(P4,1190,1200,(OX,1.68,0),(OX+0.45,1.7,0),step=3);   # dc16: huff on camera right after the toss (at 1198 the camera was on the map) faces(P4,[(1150,'meh'),(1170,'worried'),(1196,'shock'),(1232,'stunned')])
path(s,[(972,(OX+0.35,-1.0,1.48),(OX+0.15,1.6,1.05)),(1040,(OX+0.6,-1.05,1.45),(OX+0.35,1.4,0.95)),(1070,(OX+0.2,-1.1,1.5),(OX+0.1,1.6,1.05)),
        (1104,(OX+0.55,-1.0,1.45),(OX+0.35,1.4,0.95)),(1140,(OX+0.25,-1.0,1.48),(OX+0.3,1.4,1.0)),(1160,(OX-0.1,-0.9,1.6),(OX-0.4,2.5,1.55)),
        (1190,(OX-0.75,-0.55,1.75),(OX-1.5,3.0,2.0)),(1208,(OX-0.75,-0.6,1.75),(OX-1.45,3.0,2.0)),(1236,(OX+0.9,-0.3,1.75),(OX+2.2,3.0,1.95)),(1240,(OX+0.95,-0.25,1.75),(OX+2.22,3.0,1.95))])
# ---- S12 (1234-1314): no one had time for pie: the clerk rushes by at night; the pie sits (truck, settles on "pie") ----
s='S12'; r=S(s)
cl12=char_on('S12_clerk','clerk',s,(WX-1.6,1.5,0),r,'worry',arms=('arm','arm_letter'),walker=True)
walk(cl12,1238,1290,(WX-1.8,1.55,0),(WX+1.8,1.65,0),step=3); work(cl12,'carry',[(1234,-30)])
faces(cl12,[(1234,'worry'),(1262,'panic'),(1285,'dazed')])
path(s,[(1234,(WX-1.0,-0.9,1.5),(WX-0.8,1.4,1.0)),(1305,(WX+0.25,-0.75,1.25),(WX+0.0,0.85,0.75)),(1314,(WX+0.27,-0.72,1.24),(WX+0.0,0.85,0.74))])
# ---- S13 (1308-1390): most folks would have quit. Not her. (night, push) ----
s='S13'; r=S(s)
ed13=char_on('S13_ed','editor',s,(PX,1.12,-L.FOOT_LIFT),r,'worry',arms=('arm',[(1308,'arm_quill')]))
faces(ed13,[(1308,'worried'),(1340,'sigh'),(1357,'blink'),(1362,'sad'),(1372,'determined')])
work(ed13,'write',[(1308,-24),(1314,-28),(1320,-22),(1326,-26)]); act(ed13,'clutch',1334); act(ed13,'point',1368)
bob(ed13,[1372])
path(s,[(1308,(PX+0.8,-1.2,1.5),(PX,1.5,1.0)),(1390,(PX+0.5,-0.6,1.43),(PX,1.5,1.03))])
# ---- S14 (1391-1438): quill close-up (truck) ----
s='S14'; r=S(s)
path(s,[(1391,(PX-0.35,0.25,1.05),(PX+0.0,0.8,0.63)),(1438,(PX+0.3,0.25,1.05),(PX+0.1,0.82,0.63))])
# ---- S15 (1439-1490): seventeen years on the wall calendar (slow push) ----
s='S15'; r=S(s)
path(s,[(1439,(PX+0.85,1.6,1.62),(PX+0.85,3.0,1.6)),(1490,(PX+0.82,1.85,1.61),(PX+0.85,3.0,1.6))])
# ---- S16 (1484-1598): autumn 1863, Washington: leaves fall, the mail goes out (crane down, the camera backs off as he walks in) ----
s='S16'; r=S(s)
mm16=char_on('S16_mail','mailman',s,(SX+0.6,8.0,0),r,'neutral',arms=('arm','arm_sack'),walker=True)
walk(mm16,1484,1598,(SX+0.6,9.0,0),(SX+0.4,1.6,0),step=4); work(mm16,'carry',[(1484,-30)],-1); drift_faces(mm16,1484,1598,['neutral','worried','look_up'],160,(18,30)); faces(mm16,[(1552,'nervous'),(1584,'grit')])
tw=char_on('S16_town','townW',s,(SX-0.55,4.6,0.0),r,'worry'); drift_faces(tw,1484,1598,['worried','look_up','neutral','smile'],161); bob(tw,[1530,1570]); act(tw,'recoil',1526)   # dc16b (shots verifier: she stood off camera, so her startle_recoil never showed)
# dc16b (visual verifier: flat plum band under the S16 walker): the blob's dark plum turned into unlit ink on the cobbles; S16 blobs use a lighter, lit shadow texture
for _o in [o for o in bpy.data.objects if o.name.startswith('S16_') and o.name.endswith('_shadow')]: _o.data.materials[0]=L.card_mat('shadow_soft','shadow_soft',emit=0.0)
path(s,[(1484,(SX+0.3,-2.6,3.4),(SX+0.2,10,2.0)),(1540,(SX+0.4,-2.9,2.3),(SX+0.4,8,1.4)),(1598,(SX+0.5,-3.4,1.5),(SX+0.4,5,1.2))])
# ---- S17 (1592-1644): the letter to the fifth president (insert, push) ----
s='S17'; r=S(s)
path(s,[(1592,(OX-0.05,-0.1,1.35),(OX-0.05,0.8,0.64)),(1644,(OX-0.05,0.15,1.22),(OX-0.05,0.82,0.64))])
# ---- S18 (1638-1732): this time, yes: he stamps it; the desk calendar runs out in a week (truck) ----
s='S18'; r=S(s)
p5=char_on('S18_pres','presE',s,(OX,1.25,-L.FOOT_LIFT),r,'neutral',arms=('arm',[(1638,'arm_letter'),(1664,'arm_stamp')]))
faces(p5,[(1638,'neutral'),(1654,'look_down'),(1670,'proud'),(1682,'open_smile'),(1700,'grin'),(1718,'proud')])
arm(p5,1,1638,-50); arm(p5,1,1664,-50); act(p5,'stamp',1670); act(p5,'present',1698)
bob(p5,[1682,1718])
SHX_=json.load(open('/root/dc/bridge16/hand_at.json')) if os.path.exists('/root/dc/bridge16/hand_at.json') else {}
for nm_,key_,c_ in (('S01','write',C('S01')),('S10','write',C('S10')),('S13','write',C('S13')),('S18','stamp',C('S18'))):   # dc14 (346): the sheet sits under the mitten
    if nm_ in SHX_: x_,y_=SHX_[nm_]; paper(f'{nm_}_wsheet',(x_,y_,0.645 if nm_=='S18' else 0.625),0.24,0.32,'letter_hero',0.15,coll=c_)
path(s,[(1638,(OX-0.7,-1.0,1.42),(OX-0.1,1.3,0.95)),(1732,(OX+0.35,-1.05,1.42),(OX+0.15,1.3,0.95))])
# ---- S19 (1726-1892): one big table: blue and grey sit down together (pull out and rise; lands wide on "table") ----
s='S19'; r=S(s)
G=[]
# dc14 rule 345: real depth. blueA stands at the near end of the table (about 2 m from the landing camera), the rest 1.6 m further back;
# the frontal row becomes a high three-quarter view (camera 2.5 m up, about 36 deg off axis). Each soldier a different arm move (354).
for i,(x,y,k) in enumerate([(-1.6,0.2,'blueA'),(-0.35,1.6,'greyA'),(0.4,1.6,'blueB'),(1.05,1.6,'greyB')]):   # dc15 (visual verifier 345: greyA sat on blueA's line of sight, a stacked totem 1776-1884): back row spread right of the front head
    c_=char_on(f'S19_{k}',k,s,(HX+x,y,0),r,'happy',arms=('arm',[(1726,'arm_plate')] if i%2==0 else 'arm')); G.append(c_)
    drift_faces(c_,1726,1892,['happy','grin','proud','laugh','content'],190+i,(16,28)); bob(c_,[1760+i*9,1820+i*7,1873])
    arm(c_,1,1726,-40); act(c_,['offer','shrug','clutch','wave'][i],1790+i*6)
tw19=char_on('S19_town','townW',s,(HX+2.2,1.95,0),r,'happy',arms=('arm',[(1726,'arm_pie'),(1866,'arm')]),walker=True)
walk(tw19,1830,1862,(HX+3.6,1.95,0),(HX+2.2,1.95,0),step=4); faces(tw19,[(1726,'happy'),(1862,'laugh'),(1878,'proud')]); work(tw19,'carry',[(1726,-35)]); act(tw19,'present',1864)
path(s,[(1726,(HX-2.2,-1.7,1.45),(HX-0.55,1.4,1.0)),(1800,(HX-2.35,-1.7,1.65),(HX-0.5,1.35,0.88)),(1873,(HX-2.5,-1.7,1.88),(HX-0.3,1.3,0.76)),(1892,(HX-2.52,-1.74,1.9),(HX-0.3,1.3,0.76))])   # dc16b (rule 336 medians vs 345, coordinator ruling (b)): milder high three-quarter, end pitch ~17 deg (was ~27)   # dc14 (345): high three-quarter landing
# ---- S20 (1886-1980): today, the whole country eats on the same Thursday (truck) ----
s='S20'; r=S(s)
F=[]
# dc14 rule 345: dad stands at the near right corner (about 1.8 m from camera), the family 1.5 m behind; high three-quarter from the right,
# 2.1 m up (S19 was 2.5 m: consecutive group shots change height)
for i,(x,y,k) in enumerate([(-1.65,1.5,'grandT'),(-1.05,1.5,'momT'),   # dc16b: grandma and mom 0.35 m left so dad's head clears mom's at f1960
                             (0.8,0.15,'dadT'),(0.55,1.5,'kidT')]):
    c_=char_on(f'S20_{k}',k,s,(TX+x,y,0),r,'happy',arms=('arm',{'grandT':'arm','momT':'arm_plate','dadT':'arm_fork','kidT':'arm_fork'}[k]),scale=(0.8 if k=='kidT' else 1.0)); F.append(c_)   # CAST GATE: the child stands 0.8 of an adult [INFERRED]
    drift_faces(c_,1886,1980,['happy','grin','laugh','cry_laugh','open_smile'],200+i,(14,26)); bob(c_,[1910+i*8,1950+i*5])
work(F[2],'eat',[(f+d,a_) for f in range(1890,1980,10) for d,a_ in ((0,-50),(5,-30))])
act(F[3],'fist_pump',1930); act(F[1],'offer',1912); act(F[0],'wave',1948)   # dc14 (354): four different moves
faces(F[1],[(1944,'open_smile'),(1962,'proud')]); faces(F[2],[(1920,'laugh'),(1958,'content')])   # exprlib: >=4 faces per featured character
path(s,[(1886,(TX+1.5,-1.65,1.7),(TX-0.2,1.3,0.92)),(1980,(TX+2.0,-1.25,1.65),(TX-0.2,1.3,0.92))])   # dc16b: milder high angle, pitch ~16 deg (was ~26)   # dc14 (345)
# ---- S21 (1974-2086): all because one woman would not stop writing: past her framed letter, the camera lands on the poster on "writing" ----
s='S21'; r=S(s)
k21=char_on('S21_kid','kidT',s,(TX-0.12,1.5,0),r,'happy',arms=('arm','arm_fork'),scale=0.8); faces(k21,[(1974,'happy'),(1999,'wink_grin')]); act(k21,'wave',1996,-1)
path(s,[(1974,(TX+0.0,-1.2,1.5),(TX+0.2,1.6,1.15)),(2012,(TX+0.75,-0.5,1.65),(TX+0.75,3.0,1.8)),(2054,(PXP+0.05,PY-2.25,1.53),(PXP,PY,PZ-0.21)),(END,(PXP+0.03,PY-2.05,1.52),(PXP,PY,PZ-0.21))])
# ======================= foreground layers (rule 311): one near object per shot over 60 f, low in a corner, never over a face or the poster =======================
def campos(n,f):
    def ev(o):
        return Vector([next(fc for fc in o.animation_data.action.fcurves if fc.data_path=='location' and fc.array_index==i).evaluate(f) for i in range(3)])
    return ev(L.CAM[n]),ev(L.TGT[n])
def fgobj(n,kind,side=1,dist=1.3,drop=0.75,f=None,lat=0.5,z0=0.0):
    f0=SH[n][0] if f is None else f; c_,t_=campos(n,f0); d_=(t_-c_); d_.z=0; d_.normalize(); rt=Vector((d_.y,-d_.x,0)).normalized()
    p=c_+d_*dist+rt*lat*side*dist; p.z=z0; co=C(n); yaw=math.atan2(d_.y,d_.x)
    if kind=='books':
        for k in range(4): box(f'{n}_fgb{k}',(p.x+0.02*k,p.y,0.06+k*0.1+0.62*0),(0.4-0.04*k,0.3,0.1),flat(f'book{k%3}',lin([(140,50,50),(50,80,120),(70,110,70)][k%3]),0.8),coll=co,bv=0.01).rotation_euler=(0,0,yaw+0.2*k)
        box(f'{n}_fgstool',(p.x,p.y,0.0),(0.01,0.01,0.01),INK,coll=co,bv=0)
    elif kind=='stool':
        cyl(f'{n}_fgst',(p.x,p.y,0.32),0.2,0.06,DARK,v=16,coll=co)
        for k in range(3): cyl(f'{n}_fgsl{k}',(p.x+0.13*math.cos(k*2.1),p.y+0.13*math.sin(k*2.1),0.15),0.025,0.3,DARK,v=6,coll=co)
        for k in range(3): box(f'{n}_fgbk{k}',(p.x,p.y,0.39+k*0.08),(0.32-0.04*k,0.24,0.08),flat(f'book{k%3}',lin([(140,50,50),(50,80,120),(70,110,70)][k%3]),0.8),coll=co,bv=0.01).rotation_euler=(0,0,yaw+0.25*k)
    elif kind=='crate': crate(f'{n}_fgcrate',(p.x,p.y,z0),0.5,coll=co).rotation_euler=(0,0,yaw+0.3)
    elif kind=='sack': sack(f'{n}_fgsack',(p.x,p.y,z0),coll=co)
    elif kind=='chair': chair(f'{n}_fgchair',(p.x,p.y,z0),yaw+math.pi/2+0.4,coll=co)
    elif kind=='post':
        cyl(f'{n}_fgpost',(p.x,p.y,1.0),0.06,2.0,IRON,v=10,coll=co)
    elif kind=='plant':
        cyl(f'{n}_fgpot',(p.x,p.y,0.2),0.18,0.4,flat('pot',lin((170,90,60)),0.8),v=14,coll=co,r2=0.22)
        for k in range(3):
            g=plane(f'{n}_fgleaf{k}',(p.x,p.y,0.75),0.7,0.7,card_mat('tree1','tree1',emit=0.25),coll=co); g.rotation_euler=(0,0,yaw+math.radians(60*k)); g['noink']=1
for n,k,sd,dr in [('S01','stool',-1,0.75),('S02','chair',-1,0.7),('S03','sack',1,0.7),('S04','crate',1,0.7),('S05','sack',-1,0.7),('S06','crate',1,0.7),('S08','stool',1,0.7),
                  ('S09','crate',-1,0.7),('S10','stool',1,0.7),('S11','chair',-1,0.7),('S12','sack',-1,0.7),('S13','stool',1,0.7),('S16','post',-1,0.7),('S18','plant',-1,0.7),
                  ('S19','plant',-1,0.7),('S20','plant',-1,0.7),('S21','plant',-1,0.7)]:
    fgobj(n,k,sd,1.3)
# ======================= world, finish, ink, render settings =======================
def world_and_sun():
    w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; bg=w.node_tree.nodes['Background']; bg.inputs['Color'].default_value=(*lin((200,196,186)),1); bg.inputs['Strength'].default_value=0.8
    bpy.ops.object.light_add(type='SUN',rotation=(math.radians(52),0,math.radians(40))); sun=bpy.context.object; sun.name='sun'; sun.data.energy=3.6; sun.data.color=(1.0,0.93,0.82); sun.data.angle=math.radians(3)
world_and_sun()
for a in ALL: turnpass(a)
for a in ALL: finish(a)
if os.environ.get('RIGCHECK','1')=='1':
    _rc=L.rigcheck(range(0,END+1,2)); print('RIGCHECK_FAULTS',_rc,flush=True)   # dc15 rule 354b: blocking before any render
json.dump(dict(acts=ACTLOG,turns=TURNLOG,combos=COMBOLOG),open('/root/dc/bridge16/motion.json','w'),indent=0)   # dc14: armvariety.py / turn check input
json.dump([dict(inst=a['inst'],kind=a['kind'],shot=a['shot'],rng=list(a['rng']),faces=sorted([(int(f),k) for f,k in a['faces']]),avail=sorted(a['F'])) for a in ALL],open('/root/dc/bridge16/faces.json','w'))   # facecheck.py input
print('hulls',L.ink())
for o_ in bpy.data.objects:
    if o_.type=='LIGHT' and o_.data.type!='SUN': o_.visible_camera=False
L.render_setup(100,8)
sc.cycles.samples=4; sc.cycles.transparent_max_bounces=8; sc.cycles.diffuse_bounces=1; sc.cycles.max_bounces=3
os.makedirs('/root/dc/blend16',exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath='/root/dc/blend16/dc.blend'); print('SCENE_OK all')
