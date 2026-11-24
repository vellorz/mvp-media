# rule 335a/355 probe, step 1 (blender): render shot frames and write head-disc boxes (faceboxes.json) for the skin ratio check.
# blender -b bcn.blend -P skinprobe_bcn.py -- OUTDIR PCT S01:40,S01:60,...
import bpy, sys, json, os, mathutils
from bpy_extras.object_utils import world_to_camera_view as w2c
a=sys.argv[sys.argv.index('--')+1:]; OUT=a[0]; PCT=int(a[1]); os.makedirs(OUT,exist_ok=True)
sc=bpy.context.scene; SH=json.loads(sc['shots']); sc.render.resolution_percentage=PCT; sc.cycles.samples=8
W=int(sc.render.resolution_x*PCT/100); H=int(sc.render.resolution_y*PCT/100); R=0.215; boxes={}
roots=[o for o in bpy.data.objects if o.type=='EMPTY' and o.get('chr')==o.name]
for job in a[2].split(','):
    shot,f=job.split(':'); f=int(f); cam=bpy.data.objects['cam_'+shot]; sc.camera=cam; sc.frame_set(f); bpy.context.view_layer.update()
    name=f'{shot}_{f:04d}'; sc.render.filepath=f'{OUT}/{name}.png'; bpy.ops.render.render(write_still=True); bl=[]
    cx=cam.matrix_world.to_3x3()@mathutils.Vector((1,0,0))
    for r in roots:
        if r.users_collection[0].name.replace('CHR_','')!=shot: continue
        heads=[o for o in bpy.data.objects if o.name.startswith(r.name+'_d_') and not o.hide_render]
        if not heads: continue
        c=bpy.data.objects[r.name+'_hp'].matrix_world.translation+mathutils.Vector((0,0,0.12))
        p=w2c(sc,cam,c); q=w2c(sc,cam,c+cx*R)
        if p.z<=0: continue
        rr=abs(q.x-p.x)*W; px,py=p.x*W,(1-p.y)*H
        if rr<6 or not (rr<px<W-rr and rr<py<H-rr): continue
        bl.append(dict(ch=r.name,x=round(px,1),y=round(py,1),r=round(rr,1)))
    boxes[name]=bl; print('BOX',name,len(bl),flush=True)
json.dump(boxes,open(f'{OUT}/faceboxes.json','w'),indent=1)
