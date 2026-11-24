# dc16d (rules 374(b), 375; owner's-eye pass: the quill stood in the inkwell / floated with no hand in S01 S10 S13 S14):
# ONE reusable writing setup. A 3D quill (feather card with nib) whose TIP sits on the sheet (<= 2 mm) on every writing frame and runs along
# the lines; its shaft goes up through the writer's mitten (grip) and the feather faces the camera; ink words appear behind the tip.
# Built from real quill grip references [INFERRED, Rick has no quill close-up]: tip on the page, shaft leaning back over the hand ~45-60 deg.
import bpy, math
from mathutils import Vector, Matrix
def _mat(L):
    return L.card_mat('quill_feather','quill_feather',emit=0.6)
def make_quill(L,n,coll,length=0.22):
    q=L.empty(n,(0,0,0),coll=coll)
    w=length*256/1024
    f=L.plane(n+'_card',(0,0,0),w,length,_mat(L),coll=coll); f.parent=q; f.location=(-(133.6/256-0.5)*w,0,length/2); f['noink']=1
    f.visible_shadow=False
    return q
def mitten_world(o,bend):
    # handpos.py logic: mitten centre on the arm card texture (1200 x 900 canvas), then to world
    sx=1 if '_arm1_' in o.name else -1
    hx=600+(712-330)*math.sin(math.radians(bend)); hy=330+(712-330)*math.cos(math.radians(bend))
    if sx<0: hx=1200-hx
    bb=[Vector(v) for v in o.bound_box]; xs=[v.x for v in bb]; ys=[v.y for v in bb]; zs=[v.z for v in bb]
    loc=Vector((min(xs)+(max(xs)-min(xs))*hx/1200,(min(ys)+max(ys))/2,max(zs)-(max(zs)-min(zs))*hy/900))
    if max(ys)-min(ys)>max(zs)-min(zs): loc=Vector((min(xs)+(max(xs)-min(xs))*hx/1200,max(ys)-(max(ys)-min(ys))*hy/900,(min(zs)+max(zs))/2))
    return o.matrix_world@loc
def orient(q,tip,grip,cam,prev=None):
    z=(grip-tip).normalized(); v=(cam-tip).normalized()
    y=-(v-v.dot(z)*z).normalized(); x=y.cross(z).normalized()
    M=Matrix((x,y,z)).transposed()
    e=M.to_euler('XYZ',prev) if prev else M.to_euler('XYZ')
    q.location=tip; q.keyframe_insert('location'); q.rotation_euler=e; q.keyframe_insert('rotation_euler'); return e
def words(L,n,coll,pts,f_show,f_end,z):
    # ink word dashes laid on the sheet; each appears the frame the tip has passed it (rule 374(b): marks behind the tip)
    out=[]
    for k,(p,f) in enumerate(zip(pts,f_show)):
        o=L.plane(f'{n}_w{k}',(p.x,p.y,z),0.022,0.008,L.card_mat(f'ink_word{k%4}',f'ink_word{k%4}',emit=0.3),coll=coll,horiz=True); o['noink']=1; o.visible_shadow=False
        o.rotation_euler=(0,0,0); L.vis(o,[(f,f_end)]); out.append(o)
    return out
def write_desk(L,sc,ch,f0,f1,sheet,coll,arm_key='arm_quill',bend=30,lines_f=22,line_len=0.075,line_gap=0.02):
    """desk writer: tip on the sheet under her mitten, sweeping along a line, then back to the next line; arm keys sweep with it"""
    o=bpy.data.objects[f"{ch['inst']}_arm1_{arm_key}"]; cam=L.CAM[ch['shot']]
    q=make_quill(L,ch['inst']+'_quill',coll)
    # the arm sweeps 6 deg per line (outward = negative), quick return; tip leads the mitten along the line
    for f in range(f0,f1+1,lines_f):
        L.arm(ch,1,f,-27); L.arm(ch,1,min(f+lines_f-5,f1),-21)
    sheetz=sheet[2]+0.004; prev=None; marks=[]; fshow=[]
    base=None
    for f in range(f0,f1+1):
        sc.frame_set(f); g=mitten_world(o,bend); line=(f-f0)//lines_f; u=min(1.0,((f-f0)%lines_f)/(lines_f-5))
        if base is None: base=Vector((g.x-0.03,g.y-0.035,sheetz))
        tip=Vector((base.x+u*line_len, base.y-line*line_gap+0.0025*math.sin(f*1.6), sheetz))
        grip=Vector((g.x,g.y,max(g.z,sheetz+0.05)))
        prev=orient(q,tip,grip,cam.matrix_world.translation,prev)
        if u<1.0 and (f-f0)%lines_f%3==0 and (f-f0)%lines_f>0: marks.append(Vector((tip.x-0.012,tip.y,sheetz))); fshow.append(f)
    for fc in q.animation_data.action.fcurves:
        for kp in fc.keyframe_points: kp.interpolation='LINEAR'
    L.vis(q,[(f0,f1)]); [L.vis(c_,[(f0,f1)]) for c_ in q.children]
    words(L,ch['inst']+'_ink',coll,marks,fshow,f1,sheet[2]+0.0025)
    print('QUILL',ch['inst'],f0,f1,'marks',len(marks),'tip_z',round(sheetz,4))
    return q
def write_close(L,sc,n,f0,f1,coll,shot,x0,y0,z,line_len=0.16,lines_f=12,line_gap=0.03,armfrom=(0.55,-0.25,0.55)):
    """close-up: a mitten (plum ink disc, rule 329 mitt) on a short noodle arm from the frame edge holds the quill; tip on the sheet"""
    cam=L.CAM[shot]; q=make_quill(L,n+'_quill',coll,length=0.24)
    ink=bpy.data.materials.get('S14_inkmat') or L.flat('S14_inkmat',L.lin(L.INK_RGB),0.9,emit=1.0)
    mit=bpy.data.objects.new(n+'_mitt',None); mit.empty_display_size=0.03; coll.objects.link(mit)
    import bmesh
    me=bpy.data.meshes.new(n+'_mittm'); bm=bmesh.new(); bmesh.ops.create_uvsphere(bm,u_segments=16,v_segments=10,radius=0.034); bm.to_mesh(me); bm.free()
    mo=bpy.data.objects.new(n+'_mittmesh',me); me.materials.append(ink); coll.objects.link(mo); mo.parent=mit; mo['noink']=1; mo.scale=(1,0.8,0.9); mo.visible_shadow=False
    cu=bpy.data.curves.new(n+'_armc','CURVE'); cu.dimensions='3D'; cu.bevel_depth=0.0125; cu.bevel_resolution=4
    sp=cu.splines.new('BEZIER'); sp.bezier_points.add(1)
    ao=bpy.data.objects.new(n+'_arm',cu); ao.data.materials.append(ink); coll.objects.link(ao); ao['noink']=1; ao.visible_shadow=False
    prev=None; marks=[]; fshow=[]
    for f in range(f0,f1+1):
        line=(f-f0)//lines_f; u=min(1.0,((f-f0)%lines_f)/(lines_f-3))
        tip=Vector((x0+u*line_len,y0-line*line_gap+0.003*math.sin(f*1.7),z+0.004))
        grip=tip+Vector((0.05,-0.035,0.075))
        sc.frame_set(f); prev=orient(q,tip,grip+ (grip-tip)*0.0,cam.matrix_world.translation,prev)
        mit.location=grip; mit.keyframe_insert('location')
        A=grip+Vector(armfrom); P=sp.bezier_points
        P[0].co=A; P[0].handle_left=A+Vector((0.05,0,0.05)); P[0].handle_right=A+Vector((-0.08,0.02,-0.02))
        P[1].co=grip; P[1].handle_left=grip+Vector((0.12,-0.02,0.10)); P[1].handle_right=grip
        for i_,p_ in enumerate(P):
            p_.keyframe_insert('co',frame=f); p_.keyframe_insert('handle_left',frame=f); p_.keyframe_insert('handle_right',frame=f)
        if u<1.0 and (f-f0)%lines_f%2==0 and (f-f0)%lines_f>0: marks.append(Vector((tip.x-0.014,tip.y,z))); fshow.append(f)
    for ob in (q,mit):
        for fc in ob.animation_data.action.fcurves:
            for kp in fc.keyframe_points: kp.interpolation='LINEAR'
    for ob in (q,mo,ao)+tuple(q.children): L.vis(ob,[(f0,f1)])
    words(L,n+'_ink',coll,marks,fshow,f1,z+0.0025)
    print('QUILL_CLOSE',n,f0,f1,'marks',len(marks))
