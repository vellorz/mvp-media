# For each character whose head is cut by the frame edge while its body is on screen: the sideways shift (m, along the camera's
# horizontal axis) that brings the whole head disc inside with a margin, plus a TOP flag. Prints a NUDGE dict for scene_cc.py.
import bpy, json, mathutils
from bpy_extras.object_utils import world_to_camera_view as w2c
sc=bpy.context.scene; SH=json.loads(sc['shots']); R=0.215; M=0.03; out={}
roots=[o for o in bpy.data.objects if o.type=='EMPTY' and o.get('chr')==o.name]
for r in sorted(roots,key=lambda o:o.name):
    shot=r.users_collection[0].name.replace('CHR_',''); cam=bpy.data.objects['cam_'+shot]; sc.camera=cam; f0,f1=SH[shot]
    hp=bpy.data.objects[r.name+'_hp']; body=next((o for o in bpy.data.objects if o.name.startswith(r.name+'_body')),None)
    heads=[o for o in bpy.data.objects if o.name.startswith(r.name+'_d_')]; need=[]; top=0
    for f in range(f0,f1+1,2):
        sc.frame_set(f); bpy.context.view_layer.update()
        if not any(not o.hide_render for o in heads): continue
        bp=w2c(sc,cam,body.matrix_world.translation)
        if not (bp.z>0 and 0<bp.x<1 and 0<bp.y<1): continue
        c=hp.matrix_world.translation+mathutils.Vector((0,0,0.12)); cx=(cam.matrix_world.to_3x3()@mathutils.Vector((1,0,0))); cx.z=0; cx.normalize()
        p=w2c(sc,cam,c); pl=w2c(sc,cam,c-cx*R); pr=w2c(sc,cam,c+cx*R); pt=w2c(sc,cam,c+mathutils.Vector((0,0,R)))
        mpx=(pr.x-pl.x)/(2*R)   # screen fraction per metre at this depth
        if pl.x<M: need.append((M-pl.x)/mpx)
        elif pr.x>1-M: need.append(-(pr.x-(1-M))/mpx)
        if pt.y>1-M: top+=1
    if need or top:
        s=max(need,key=abs) if need else 0.0; cx=(cam.matrix_world.to_3x3()@mathutils.Vector((1,0,0))); cx.z=0; cx.normalize()
        out[r.name]=(round(cx.x*s,3),round(cx.y*s,3),top)
print('NUDGE',json.dumps(out))
