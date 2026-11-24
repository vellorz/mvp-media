import bpy,json
from bpy_extras.object_utils import world_to_camera_view as w2c
from mathutils import Vector
sc=bpy.context.scene; SH=json.loads(sc['shots']); o=bpy.data.objects['M_banner350']; cam=bpy.data.objects['cam_S17']; out={}
for f in range(SH['S17'][0],SH['S17'][1]+1):
    sc.frame_set(f); ps=[w2c(sc,cam,o.matrix_world@Vector(c)) for c in o.bound_box]; ys=[1-p.y for p in ps]; out[f]=[round(min(ys),4),round(max(ys),4)]
json.dump(out,open('/root/nb/bridge/banner17.json','w')); print('B17',len(out))
