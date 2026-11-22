# Rule 329 full-body cast sheet renders: every character kind WHOLE, stand pose + one scene pose, transparent PNGs.
# blender -b cc.blend --python castsheet_cc.py -- OUTDIR     (never saves the blend)
import bpy, sys, os, json, math
from mathutils import Vector
OUT=sys.argv[sys.argv.index('--')+1]; os.makedirs(OUT,exist_ok=True)
sc=bpy.context.scene; SH=json.loads(sc['shots'])
for lc in bpy.context.view_layer.layer_collection.children:
    lc.exclude=False
    for c in lc.children: c.exclude=False
roots=sorted([o for o in bpy.data.objects if o.type=='EMPTY' and o.get('chr')==o.name],key=lambda o:o.name)
def kind_of(inst):
    b=bpy.data.objects.get(inst+'_body')
    return b.active_material.name.rsplit('_body',1)[0] if b and b.active_material else None
pick={}
for r in roots:
    k=kind_of(r.name)
    if k and k not in pick: pick[k]=r
def mute_all_vis(keep):
    for o in bpy.data.objects:
        if o.name in keep: continue
        ad=o.animation_data
        if ad and ad.action:
            for fc in ad.action.fcurves:
                if fc.data_path=='hide_render': fc.mute=True
        o.hide_render=True
cam=bpy.data.objects.new('sheetcam',bpy.data.cameras.new('sheetcam')); sc.collection.objects.link(cam)
cam.data.type='ORTHO'; cam.data.ortho_scale=1.9; sc.camera=cam
sc.render.resolution_x=600; sc.render.resolution_y=900; sc.render.resolution_percentage=100; sc.render.film_transparent=True
sc.cycles.samples=16
sun=next(o for o in bpy.data.objects if o.type=='LIGHT' and o.data.type=='SUN')
done={}
ORIG={o.name:o.hide_render for o in bpy.data.objects}
for k,r in pick.items():
    inst=r.name; shot=r.users_collection[0].name.replace('CHR_','')
    keep={o.name for o in bpy.data.objects if o.name==inst or o.name.startswith(inst+'_')}|{'sheetcam',sun.name}
    mute_all_vis(keep)
    f0,f1=SH[shot]
    # scene pose: a frame in the shot where the arm pivots are rotated the most (a real action pose)
    pa=[bpy.data.objects[f'{inst}_ap{sx}'] for sx in (-1,1)]
    best=(f0+f1)//2; bv=-1
    for f in range(f0,f1+1,3):
        sc.frame_set(f)
        if not any(not o.hide_render for o in bpy.data.objects if o.name.startswith(inst+'_d_')): continue
        v=sum(abs(p.rotation_euler.y) for p in pa)
        if v>bv: bv,best=v,f
    for tag in ('stand','scene'):
        for p in pa:
            ad=p.animation_data
            if ad and ad.action:
                for fc in ad.action.fcurves: fc.mute=(tag=='stand')
        sc.frame_set(best)
        if tag=='stand':
            for sx,p in zip((-1,1),pa): p.rotation_euler=(0,math.radians(-8)*sx,0)
        # point the card rig at our camera: put the camera in front of the root along its current facing
        rw=r.matrix_world; fwd=(rw.to_3x3()@Vector((0,-1,0))).normalized(); s_=r.scale.z
        base=rw.translation; cam.location=base+fwd*4.0+Vector((0,0,0.72*s_)); cam.data.ortho_scale=1.9*s_
        cam.rotation_euler=(math.radians(90),0,math.atan2(fwd.x,-fwd.y)+math.pi)
        bpy.context.view_layer.update()
        # aim exactly at the body centre
        d=(base+Vector((0,0,0.72*s_)))-cam.location; cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
        sc.render.filepath=f'{OUT}/{k}_{tag}.png'; bpy.ops.render.render(write_still=True)
    for p in pa:
        ad=p.animation_data
        if ad and ad.action:
            for fc in ad.action.fcurves: fc.mute=False
    for o in bpy.data.objects:
        ad=o.animation_data
        if ad and ad.action:
            for fc in ad.action.fcurves:
                if fc.data_path=='hide_render': fc.mute=False
        o.hide_render=ORIG.get(o.name,False)
    done[k]=dict(inst=inst,shot=shot,scene_frame=best)
    print('SHEET',k,inst,best,flush=True)
json.dump(done,open(OUT+'/sheet_index.json','w'),indent=1)
print('SHEET_DONE',len(done))
