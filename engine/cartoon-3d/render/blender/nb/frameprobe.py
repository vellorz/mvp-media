# framing probe: per shot, every character's head centre (x,y in frame 0-1) and head width as % of frame width at start/mid/end
import bpy, json
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view as w2c
sc=bpy.context.scene; SH=json.loads(sc['shots'])
roots=[o for o in bpy.data.objects if o.get('is_char')]
for n,(a,b) in SH.items():
    cam=bpy.data.objects['cam_'+n]; out=[]
    for f in (a+2,(a+b)//2,b-2):
        sc.frame_set(f); row=[]
        for r in roots:
            if r.get('shot')!=n: continue
            hp=bpy.data.objects[r.name+'_hp']; c=hp.matrix_world.translation+Vector((0,0,0.20))
            p=w2c(sc,cam,c); right=cam.matrix_world.to_3x3()@Vector((1,0,0)); p2=w2c(sc,cam,c+right*0.43)
            row.append(f"{r.name.split('_',1)[1]}({p.x:.2f},{p.y:.2f},{abs(p2.x-p.x)*100:.0f}%)")
        out.append(f'f{f}: '+' '.join(row))
    print('FP',n,' | '.join(out))
