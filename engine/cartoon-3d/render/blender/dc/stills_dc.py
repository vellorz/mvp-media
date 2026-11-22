# one low-res still per shot (or given shot:frame list): blender -b cc.blend --python stills_cc.py -- OUTDIR PCT [S01:60 ...]
import bpy, sys, json, os
a=sys.argv[sys.argv.index('--')+1:]; out,pct=a[0],int(a[1]); req=a[2:]
sc=bpy.context.scene; sc.cycles.device='CPU'; sc.cycles.samples=6; sc.render.resolution_percentage=pct
SH=json.loads(sc['shots']); vl=bpy.context.view_layer; os.makedirs(out,exist_ok=True)
items=[(x.split(':')[0],int(x.split(':')[1])) for x in req] if req else [(n,(f0+f1)//2) for n,(f0,f1) in SH.items()]
for n,f in items:
    for lc in vl.layer_collection.children:
        if lc.name.startswith('CHR_'): lc.exclude=(lc.name!='CHR_'+n)
    for lc in vl.layer_collection.children:
        if lc.name=='CHR_'+n:
            for ch_ in lc.children: ch_.exclude=False
    sc.camera=bpy.data.objects['cam_'+n]; sc.frame_set(f); sc.render.filepath=f'{out}/{n}_{f:04d}.png'
    bpy.ops.render.render(write_still=True); print('STILL',n,f,flush=True)
