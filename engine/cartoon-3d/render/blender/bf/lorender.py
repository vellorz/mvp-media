# Cloud low-res preview of every frame (for motion/transition/caption QA before the 2K arrives)
import bpy, sys, json, os
a=sys.argv[sys.argv.index('--')+1:]; out,pct=a[0],int(a[1]); only=a[2:]
sc=bpy.context.scene; sc.cycles.device='CPU'; sc.cycles.samples=4; sc.render.resolution_percentage=pct
SH=json.loads(sc['shots']); vl=bpy.context.view_layer
sc.render.use_overwrite=False; sc.render.use_placeholder=True
for n in (only or list(SH)):
    for lc in vl.layer_collection.children:
        if lc.name.startswith('CHR_'): lc.exclude=(lc.name!='CHR_'+n)
    f0,f1=SH[n]; sc.camera=bpy.data.objects['cam_'+n]; sc.frame_start=f0; sc.frame_end=f1
    os.makedirs(f'{out}/{n}',exist_ok=True); sc.render.filepath=f'{out}/{n}/f_'
    bpy.ops.render.render(animation=True); print('SHOT_DONE',n,flush=True)
print('ALL_DONE',flush=True)
