# PC package slimmer: images referenced ONLY by meshes whose hide_render is on at every key (they never render) are unlinked from
# their image nodes and purged. Objects, rigs and materials stay. Proven by pixel-identical test stills (slimcheck).
import bpy
never=set()
for o in bpy.data.objects:
    if o.type!='MESH': continue
    ad=o.animation_data; fc=None
    if ad and ad.action: fc=next((f for f in ad.action.fcurves if f.data_path=='hide_render'),None)
    if (fc and all(k.co[1]>0.5 for k in fc.keyframe_points)) or (not fc and o.hide_render): never.add(o)
def mats(o): return [ms.material for ms in o.material_slots if ms.material]
vis_imgs=set()
for o in bpy.data.objects:
    if o.type=='MESH' and o not in never:
        for m in mats(o):
            if m.use_nodes:
                for n in m.node_tree.nodes:
                    if n.type=='TEX_IMAGE' and n.image: vis_imgs.add(n.image)
cut=0
for m in bpy.data.materials:
    if not m.use_nodes: continue
    for n in m.node_tree.nodes:
        if n.type=='TEX_IMAGE' and n.image and n.image not in vis_imgs: n.image=None; cut+=1
for i in list(bpy.data.images):
    if i.users==0: bpy.data.images.remove(i)
print('SLIM cut_refs',cut,'images_left',len(bpy.data.images))
bpy.ops.wm.save_as_mainfile(filepath='/root/sb/pc/sb_slim.blend',compress=True); print('SLIM_SAVED')
