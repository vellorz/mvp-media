# count distinct face textures per character kind actually render-visible in the scene (rule 332: >=14 per video, >=4 per featured char)
import bpy, json, re
sc=bpy.context.scene; SH=json.loads(sc['shots']); per={}; allf=set()
for o in bpy.data.objects:
    m=re.match(r'(.+)_d_(.+)$',o.name)
    if not m or not o.active_material: continue
    im=[n.image.name for n in o.active_material.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]
    if not im: continue
    ad=o.animation_data; vis=True
    if ad and ad.action:
        fc=[c for c in ad.action.fcurves if c.data_path=='hide_render']
        vis=any(k.co[1]<0.5 for c in fc for k in c.keyframe_points) if fc else not o.hide_render
    else: vis=not o.hide_render
    if not vis: continue
    nm=im[0].rsplit('.',1)[0]; k=nm.split('_h_')[0]; f=nm.split('_h_')[-1]
    per.setdefault(k,set()).add(f); allf.add(f)
print('FACECOUNT distinct',len(allf),sorted(allf))
for k,v in sorted(per.items()): print('FACECOUNT',k,len(v),sorted(v))
