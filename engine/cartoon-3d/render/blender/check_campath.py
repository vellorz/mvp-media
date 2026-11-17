# Rule 153 check: camera never passes through geometry. blender -b scene.blend --python check_campath.py  (reads sc["shots"]; NEAR lines = mesh within 0.25 m of the lens; hidden objects also report, so confirm in frames)
import bpy,json
from mathutils import Vector
sc=bpy.context.scene; S=json.loads(sc['shots'])
bad={}
for n,(a,b) in S.items():
    cam=bpy.data.objects['cam_'+n]
    for f in range(a,b+1,3):
        sc.frame_set(f); dg=bpy.context.evaluated_depsgraph_get(); o=cam.matrix_world.translation
        for dx in (-1,0,1):
          for dy in (-1,0,1):
            d=(cam.matrix_world.to_quaternion()@Vector((dx*0.35,dy*0.6,-1))).normalized()
            h=sc.ray_cast(dg,o,d)
            if h[0] and (h[1]-o).length<0.25: bad.setdefault((n,h[4].name),[]).append(f)
for k,v in bad.items(): print('NEAR',k,v[0],v[-1],len(v))
print('NEAR_DONE')
