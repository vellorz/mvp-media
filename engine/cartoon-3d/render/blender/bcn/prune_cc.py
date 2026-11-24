# r6: pack-size prune. Removes character cards (faces, arm/pose cards) that are never render-visible in the film, then purges
# orphan images. turns/poses 'all' made ~416 face cards per character; the packed blend was 619 MB. Render output is unchanged
# (only cards hidden on every frame are removed). blender -b cc.blend --python prune_cc.py -- OUT.blend
import bpy, sys
out=sys.argv[sys.argv.index('--')+1]
def never_visible(o):
    ad=o.animation_data
    fc=None
    if ad and ad.action: fc=next((c for c in ad.action.fcurves if c.data_path=='hide_render'),None)
    if fc is None: return o.hide_render
    return all(k.co[1]>0.5 for k in fc.keyframe_points) and o.hide_render
rm=[]
for o in bpy.data.objects:
    if o.type!='MESH' or not any(c.name.startswith('CHR_') for c in o.users_collection): continue
    if ('_d_' in o.name or '_arm' in o.name) and never_visible(o): rm.append(o)
print('PRUNE remove',len(rm),'of',len(bpy.data.objects))
for o in rm: bpy.data.objects.remove(o,do_unlink=True)
for _ in range(3): bpy.ops.outliner.orphans_purge(do_local_ids=True,do_linked_ids=True,do_recursive=True)
print('PRUNE images',len(bpy.data.images))
bpy.ops.file.pack_all(); bpy.ops.wm.save_as_mainfile(filepath=out,compress=True,copy=True); print('PRUNE_SAVED',out)
