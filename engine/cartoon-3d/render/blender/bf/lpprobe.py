import bpy
from bpy_extras.object_utils import world_to_camera_view as w2c
from mathutils import Vector
sc=bpy.context.scene
for s,fr in (('S03',range(292,433,4)),('S04',range(426,529,2)),('S02',range(163,298,4))):
    cam=bpy.data.objects['cam_'+s]; big={}
    for f in fr:
        sc.frame_set(f)
        for o in sc.objects:
            if not (o.name.startswith('lp') and o.name.endswith('_pole')): continue
            P=[w2c(sc,cam,o.matrix_world@Vector(k)) for k in o.bound_box]
            if min(p.z for p in P)<0.05: continue
            xs=[p.x for p in P]; w=max(xs)-min(xs)
            if max(xs)>0 and min(xs)<1 and w>0.04: big[o.name]=max(big.get(o.name,0),round(w,3))
    print('LP',s,big)
