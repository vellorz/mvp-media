# Render storyboard stills: blender -b X.blend --python stills.py -- OUTDIR PCT SHOT:frame,frame SHOT:frame ...
import bpy, sys, os, json
a=sys.argv[sys.argv.index('--')+1:]; out,pct=a[0],int(a[1]); os.makedirs(out,exist_ok=True)
sc=bpy.context.scene; sc.render.resolution_percentage=pct
vl=bpy.context.view_layer
def only(shot):
    for lc in vl.layer_collection.children:
        if lc.name.startswith('CHR_'): lc.exclude=(lc.name!='CHR_'+shot)
    sc.camera=bpy.data.objects['cam_'+shot]
for spec in a[2:]:
    shot,fr=spec.split(':')
    only(shot)
    for f in fr.split(','):
        sc.frame_set(int(f)); sc.render.filepath=f'{out}/{shot}_{int(f):04d}.png'; bpy.ops.render.render(write_still=True)
        print('STILL',shot,f,flush=True)
