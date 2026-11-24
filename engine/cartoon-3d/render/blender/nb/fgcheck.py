# round 4: where would a foreground box sit on screen over a whole shot?  env SHOT, BOX="x,y,z,sx,sy,sz" (centre + half sizes, world); prints screen x/y range per 10 frames
import bpy, json, os, itertools
from bpy_extras.object_utils import world_to_camera_view as w2c
from mathutils import Vector
sc=bpy.context.scene; SH=json.loads(sc['shots']); s=os.environ['SHOT']; a,b=SH[s]; cam=bpy.data.objects['cam_'+s]
for bx in os.environ['BOX'].split(';'):
    x,y,z,hx,hy,hz=[float(v) for v in bx.split(',')]
    pts=[Vector((x+i*hx,y+j*hy,z+k*hz)) for i,j,k in itertools.product((-1,1),repeat=3)]
    rows=[]
    for f in range(a,b+1,6):
        sc.frame_set(f); P=[w2c(sc,cam,p) for p in pts]
        rows.append((f,round(min(p.x for p in P),2),round(max(p.x for p in P),2),round(min(p.y for p in P),2),round(max(p.y for p in P),2),round(min(p.z for p in P),2)))
    print('FG',s,bx); [print('  ',r) for r in rows[::2]]
