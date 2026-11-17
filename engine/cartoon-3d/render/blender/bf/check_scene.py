# Scene checks for multi-set blends (rules 142, 158): blender -b bf.blend --python check_scene.py -- [shot ...]
# FLOAT: every visible mesh near the shot touches another mesh or the ground (fly=1 exempt); static meshes once, animated ones on first/mid/last frame.
# WALK_CLIP: every walking character's body card keeps clear of set meshes and of other characters' bodies, every 2nd frame.
# Only the shot's own CHR_<shot> collection counts (other shots' cast is excluded at render time).
import bpy, sys, json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
TOL=0.02
sc=bpy.context.scene; SH=json.loads(sc['shots'])
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
shots=argv or list(SH)
def fly(o):
    while o:
        if o.get('fly'): return True
        o=o.parent
    return False
def animated(o):
    while o:
        if o.animation_data and o.animation_data.action and any(fc.data_path!='hide_render' for fc in o.animation_data.action.fcurves): return True
        if o.constraints: return True
        o=o.parent
    return False
def chrcoll(o):
    for c in o.users_collection:
        if c.name.startswith('CHR_'): return c.name[4:]
        if c.name=='HULL': return 'HULL'
    return None
def md(o,dg):
    oe=o.evaluated_get(dg); m=oe.to_mesh()
    vs=[oe.matrix_world@v.co for v in m.vertices]; ps=[p.vertices[:] for p in m.polygons]; ctr=[oe.matrix_world@p.center for p in m.polygons]; oe.to_mesh_clear()
    if not vs: return None
    lo=Vector((min(v.x for v in vs),min(v.y for v in vs),min(v.z for v in vs))); hi=Vector((max(v.x for v in vs),max(v.y for v in vs),max(v.z for v in vs)))
    return BVHTree.FromPolygons(vs,ps),vs+ctr,lo,hi
def near(a,b,t=TOL): return all(a[2][i]-t<=b[3][i] and b[2][i]-t<=a[3][i] for i in range(3))
def touching(d,d2):
    if d[0].overlap(d2[0]): return True
    return any(d2[0].find_nearest(v,TOL)[0] is not None for v in d[1][::max(1,len(d[1])//300)])
sc.frame_set(0); dg=bpy.context.evaluated_depsgraph_get()
MESH=[o for o in sc.objects if o.type=='MESH' and not o.name.endswith('_ink')]
STAT={}; DYN=[]
for o in MESH:
    if chrcoll(o): DYN.append(o); continue
    if animated(o): DYN.append(o); continue
    d=md(o,dg)
    if d: STAT[o.name]=d
print('static',len(STAT),'dynamic',len(DYN),flush=True)
# static float test once (static objects only touch static objects or the ground)
fl=0
for n,d in STAT.items():
    if fly(bpy.data.objects[n]) or d[2].z<=TOL: continue
    if not any(n2!=n and near(d,d2) and touching(d,d2) for n2,d2 in STAT.items()): fl+=1; print('FLOATING static',n)
clip=0
for shot in shots:
    a,b=SH[shot]
    dyn=[o for o in DYN if chrcoll(o) in (None,shot)]
    for f in sorted({a,(a+b)//2,b}):
        sc.frame_set(f); dg=bpy.context.evaluated_depsgraph_get()
        D={o.name:md(o,dg) for o in dyn if not o.hide_render}; D={k:v for k,v in D.items() if v}
        for n,d in D.items():
            if fly(bpy.data.objects[n]) or d[2].z<=TOL: continue
            ok=any(n2!=n and near(d,d2) and touching(d,d2) for n2,d2 in D.items()) or any(near(d,d2) and touching(d,d2) for d2 in STAT.values())
            if not ok: fl+=1; print('FLOATING',shot,f,n)
    C=bpy.data.collections.get('CHR_'+shot)
    if not C: continue
    roots=sorted({o.parent.name for o in C.all_objects if o.name.endswith('_bodyw1')})
    bodies=[o for o in C.all_objects if o.name.endswith(('_body','_bodyw1','_bodyw2'))]
    SKIP=('walk','road','curb','_floor','podium','H_walk','E_walk')
    for f in range(a,b+1,2):
        if not roots: break
        sc.frame_set(f); dg=bpy.context.evaluated_depsgraph_get()
        BD={o.name:md(o,dg) for o in bodies if not o.hide_render}
        for rn in roots:
            mine=[k for k in BD if k.startswith(rn+'_body')]
            if not mine: continue
            d=BD[mine[0]]
            for n2,d2 in list(STAT.items())+[(k,v) for k,v in BD.items() if not k.startswith(rn+'_')]:
                if any(s in n2 for s in SKIP): continue
                if near(d,d2,0.0) and d[0].overlap(d2[0]): clip+=1; print('WALK_CLIP',shot,f,rn,n2)
print('CHECK_FLOAT','FAIL' if fl else 'PASS',fl); print('CHECK_WALKCLIP','FAIL' if clip else 'PASS',clip)
