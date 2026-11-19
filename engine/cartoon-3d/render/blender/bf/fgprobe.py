# find set objects that pass within 1.2 m of a shot camera (foreground sweeps) and big red mug in S13/S14
import bpy
from mathutils import Vector
sc=bpy.context.scene
SH={'S03':(292,432),'S04':(426,528),'S13':(1210,1359),'S14':(1352,1487)}
for s,(a,b) in SH.items():
    cam=bpy.data.objects['cam_'+s]; near={}
    for f in range(a,b+1,2):
        sc.frame_set(f); c=cam.matrix_world.translation
        for o in sc.objects:
            if o.type!='MESH' or o.name.endswith('_ink'): continue
            if any(x.name.startswith('CHR_') for x in o.users_collection): continue
            p=o.matrix_world.translation
            if abs(p.x-c.x)>3 or abs(p.y-c.y)>3: continue
            bb=[o.matrix_world@Vector(k) for k in o.bound_box]
            lo=Vector([min(v[i] for v in bb) for i in range(3)]); hi=Vector([max(v[i] for v in bb) for i in range(3)])
            d=Vector([max(lo[i]-c[i],0,c[i]-hi[i]) for i in range(3)]).length
            lim=1.0 if s in('S03','S04') else 0.45
            if d<lim: near[o.name]=min(near.get(o.name,9),round(d,2))
    print('FG',s,sorted(near.items(),key=lambda x:x[1])[:15])
