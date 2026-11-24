# rule 335 probe: on-screen face colour per shot. Projects each character's head-disc centre (cheek point, 0.22 H below and 0.18 H beside the centre)
# through the shot camera, renders the still, reads a 5x5 median of the graded-free raw frame. blender -b sb.blend --python skinprobe_sb.py -- OUT.txt PCT S01:60 ...
import bpy, sys, json, os, numpy as np
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view as w2c
a=sys.argv[sys.argv.index('--')+1:]; OUT,pct=a[0],int(a[1]); req=a[2:]
sc=bpy.context.scene; sc.cycles.device='CPU'; sc.cycles.samples=8; sc.render.resolution_percentage=pct; vl=bpy.context.view_layer
HS=0.43/0.586; lines=[]
for it in req:
    n,f=it.split(':'); f=int(f)
    for lc in vl.layer_collection.children:
        if lc.name.startswith('CHR_'): lc.exclude=(lc.name!='CHR_'+n)
    cam=bpy.data.objects['cam_'+n]; sc.camera=cam; sc.frame_set(f)
    fp=f'/tmp/skin_{n}_{f}.png'; sc.render.filepath=fp; bpy.ops.render.render(write_still=True)
    roots=[o for o in bpy.data.collections['CHR_'+n].objects if o.type=='EMPTY' and o.name+'_hp' in bpy.data.objects]
    for r in roots:
        hp=bpy.data.objects[r.name+'_hp']; s_=r.scale[2]
        if r.hide_render: continue
        c=hp.matrix_world@Vector((0,0,0)); c=c+Vector((0,0,(0.2535*HS-0.22*0.43)*s_))
        rt=(cam.matrix_world.to_quaternion()@Vector((1,0,0)))*0.18*0.43*s_; c=c+rt
        v=w2c(sc,cam,c)
        if not(0.02<v.x<0.98 and 0.02<v.y<0.98 and v.z>0): continue
        lines.append(f'{fp} {r.name} {v.x:.4f} {1-v.y:.4f}')
open(OUT,'w').write('\n'.join(lines)+'\n'); print('SKIN_OK',len(lines))
