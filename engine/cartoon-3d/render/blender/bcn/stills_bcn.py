# quick shot stills: blender -b bcn.blend -P stills_bcn.py -- OUTDIR PCT [frames as shot:f,...]
import bpy, sys, json, os
a=sys.argv[sys.argv.index('--')+1:]; OUT=a[0]; PCT=int(a[1]); os.makedirs(OUT,exist_ok=True)
sc=bpy.context.scene; SH=json.loads(sc['shots']); sc.render.resolution_percentage=PCT; sc.cycles.samples=6
jobs=[]
if len(a)>2: jobs=[(x.split(':')[0],int(x.split(':')[1])) for x in a[2].split(',')]
else:
    for n,(s,e) in SH.items(): jobs+= [(n,int(s+(e-s)*0.3)),(n,int(s+(e-s)*0.8))]
for n,f in jobs:
    sc.camera=bpy.data.objects['cam_'+n]
    for c in bpy.data.collections:
        if c.name.startswith('CHR_'):
            lc=[l for l in bpy.context.view_layer.layer_collection.children if l.name==c.name]
            if lc: lc[0].exclude=(c.name!='CHR_'+n)
    sc.frame_set(f); sc.render.filepath=f'{OUT}/{n}_{f:04d}.png'; bpy.ops.render.render(write_still=True); print('STILL',n,f,flush=True)
