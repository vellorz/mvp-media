# quick workbench preview of chosen frames: blender -b det.blend --python preview.py -- S01:50 S08:560 ...
import bpy,sys
sc=bpy.context.scene; sc.render.engine='CYCLES'; sc.cycles.samples=int(__import__('os').environ.get('PSAMP','6')); sc.cycles.use_denoising=False; sc.cycles.device='CPU'; sc.render.use_persistent_data=True; sc.render.resolution_x=360; sc.render.resolution_y=640; sc.render.resolution_percentage=100
for a in sys.argv[sys.argv.index('--')+1:]:
    s,f=a.split(':'); f=int(f)
    for c in bpy.data.collections:
        if c.name.startswith('CHR_'):
            lc=sc.view_layers[0].layer_collection.children.get(c.name)
            if lc: lc.exclude=(c.name!='CHR_'+s)
    sc.camera=bpy.data.objects['cam_'+s]; sc.frame_set(f)
    sc.render.filepath=f'/root/det/verify/prev/{s}_{f}.png'; bpy.ops.render.render(write_still=True)
