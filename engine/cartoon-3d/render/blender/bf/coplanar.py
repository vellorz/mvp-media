# round 4: find overlapping coplanar faces (axis-aligned boxes whose top/bottom/side planes coincide and overlap):
# Cycles self-shadows these to black (BF sidewalk corners, rounds 1-3). Prints pairs; rule 163/228.
import bpy, itertools
from mathutils import Vector
B=[]
for o in bpy.data.objects:
    if o.type!='MESH' or o.name.endswith('_ink') or o.hide_render or o.get('chr'): continue
    if len(o.data.vertices)>64: continue
    bb=[o.matrix_world@Vector(c) for c in o.bound_box]
    lo=Vector((min(p.x for p in bb),min(p.y for p in bb),min(p.z for p in bb))); hi=Vector((max(p.x for p in bb),max(p.y for p in bb),max(p.z for p in bb)))
    B.append((o.name,lo,hi,o.users_collection[0].name))
bad=0
for a,b in itertools.combinations(B,2):
    if a[3]!=b[3] and a[3].startswith('CHR_') and b[3].startswith('CHR_'): continue
    for ax in range(3):
        o1,o2=[(i) for i in range(3) if i!=ax]
        ov=all(min(a[2][k],b[2][k])-max(a[1][k],b[1][k])>0.05 for k in (o1,o2))
        if not ov: continue
        if abs(a[2][ax]-b[2][ax])<0.002 or abs(a[1][ax]-b[1][ax])<0.002:
            # only flag when the shared plane is an outer face of the overlap region (both boxes' faces visible)
            bad+=1
            if bad<=60: print('COPLANAR',a[0],b[0],'axis','xyz'[ax])
            break
print('COPLANAR_COUNT',bad)
