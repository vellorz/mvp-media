# Cloud CPU 2K render, resume-safe (placeholders, no overwrite), with per-shot set culling.
# blender -b cc.blend --python cloudrender_cc.py -- OUTDIR PCT SAMPLES [shot[:f0-f1] ...]
# Culling: every non-cast object whose world bounding-box centre lies > CULL m (in x) from the shot camera's start is hidden;
# sets sit 600-700 m apart inside their own sky domes, so no culled object can reach the shot's frame.
import bpy, sys, json, os, time
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]; out=a[0]; pct=int(a[1]); spp=int(a[2]); only=a[3:]
CULL=420
sc=bpy.context.scene; sc.cycles.device='CPU'; sc.render.threads_mode='AUTO'; sc.cycles.samples=spp
SH=json.loads(sc['shots']); vl=bpy.context.view_layer
sc.render.use_overwrite=False; sc.render.use_placeholder=True; sc.render.resolution_percentage=pct
chr_objs=set(o.name for c in bpy.data.collections if c.name.startswith('CHR_') for o in c.all_objects)
sc.frame_set(0)
ctr={}
for o in sc.objects:
    if o.name in chr_objs: continue
    if o.type=='MESH': ctr[o.name]=(o.matrix_world@(sum((Vector(b) for b in o.bound_box),Vector())/8)).x
    elif o.type=='LIGHT' and o.data.type!='SUN': ctr[o.name]=o.matrix_world.translation.x
orig={n:bpy.data.objects[n].hide_render for n in ctr}
for item in (only or list(SH)):
    n,_,rg=item.partition(':'); f0,f1=SH[n]
    if rg: f0,f1=map(int,rg.split('-'))
    for lc in vl.layer_collection.children:
        if lc.name.startswith('CHR_'): lc.exclude=(lc.name!='CHR_'+n)
    for lc in vl.layer_collection.children:   # cc r2: re-enable shared dressing (R_1741, R_today); excluding a parent leaves its children flagged excluded, so shared sets vanished in every shot after the first
        if lc.name=='CHR_'+n:
            for ch_ in lc.children: ch_.exclude=False
    sc.camera=bpy.data.objects['cam_'+n]; sc.frame_set(f0); cx=sc.camera.matrix_world.translation.x
    hid=0
    for nm,x in ctr.items():
        o=bpy.data.objects[nm]
        if abs(x-cx)>CULL:
            if not(o.animation_data and o.animation_data.action and any(fc.data_path=='hide_render' for fc in o.animation_data.action.fcurves)):
                o.hide_render=True; hid+=1
        else: o.hide_render=orig[nm]
    sc.frame_start=f0; sc.frame_end=f1
    os.makedirs(f'{out}/{n}',exist_ok=True); sc.render.filepath=f'{out}/{n}/f_'; t=time.time()
    print('SHOT_START',n,f0,f1,'culled',hid,flush=True)
    bpy.ops.render.render(animation=True)
    print('SHOT_DONE',n,f0,f1,round(time.time()-t,1),flush=True)
print('ALL_DONE',flush=True)
