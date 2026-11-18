# Cloud CPU 2K render of every shot, resume-safe (placeholders, no overwrite). blender -b bf.blend --python cloudrender.py -- OUTDIR [shot ...]
import bpy, sys, json, os, time
a=sys.argv[sys.argv.index('--')+1:]; out=a[0]; only=a[1:]
sc=bpy.context.scene; sc.cycles.device='CPU'; sc.render.threads_mode='AUTO'
SH=json.loads(sc['shots']); vl=bpy.context.view_layer
sc.render.use_overwrite=False; sc.render.use_placeholder=True; sc.render.resolution_percentage=100
for n in (only or list(SH)):
    for lc in vl.layer_collection.children:
        if lc.name.startswith('CHR_'): lc.exclude=(lc.name!='CHR_'+n)
    f0,f1=SH[n]; sc.camera=bpy.data.objects['cam_'+n]; sc.frame_start=f0; sc.frame_end=f1
    os.makedirs(f'{out}/{n}',exist_ok=True); sc.render.filepath=f'{out}/{n}/f_'; t=time.time()
    bpy.ops.render.render(animation=True)
    print('SHOT_DONE',n,f0,f1,round(time.time()-t,1),flush=True)
print('ALL_DONE',flush=True)
