import bpy,sys,json
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view as w2c
a=sys.argv[sys.argv.index('--')+1:]; cam=bpy.data.objects['cam_'+a[0]]; frames=[int(x) for x in a[1].split(',')]; pts=json.loads(a[2])
sc=bpy.context.scene
for f in frames:
    sc.frame_set(f)
    print('F',f,[tuple(round(v,2) for v in w2c(sc,cam,Vector(p))) for p in pts])
