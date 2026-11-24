# C4 probe: head disc cut by the frame edge (or behind camera) while the character's body is on screen.
# blender -b cc.blend --python headedge_cc.py [-- S03 S05 ...]
import bpy, json, sys, mathutils
from bpy_extras.object_utils import world_to_camera_view as w2c
sc=bpy.context.scene; SH=json.loads(sc['shots']); only=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
R=0.215   # head half width, m
roots=[o for o in bpy.data.objects if o.type=='EMPTY' and o.get('chr')==o.name]
tot=0
for r in sorted(roots,key=lambda o:o.name):
    shot=r.users_collection[0].name.replace('CHR_','')
    if only and shot not in only: continue
    cam=bpy.data.objects['cam_'+shot]; sc.camera=cam; f0,f1=SH[shot]
    hp=bpy.data.objects[r.name+'_hp']; body=bpy.data.objects.get(r.name+'_body') or next((o for o in bpy.data.objects if o.name.startswith(r.name+'_body')),None)
    heads=[o for o in bpy.data.objects if o.name.startswith(r.name+'_d_')]; cut=[]
    for f in range(f0,f1+1,2):
        sc.frame_set(f); bpy.context.view_layer.update()
        if not any(not o.hide_render for o in heads): continue
        cx=cam.matrix_world.to_3x3()@mathutils.Vector((1,0,0)); cy=cam.matrix_world.to_3x3()@mathutils.Vector((0,1,0))
        c=hp.matrix_world.translation+mathutils.Vector((0,0,0.12))
        pts=[w2c(sc,cam,c+cx*dx*R+cy*dy*R) for dx,dy in ((-1,0),(1,0),(0,1),(0,-1))]
        bp=w2c(sc,cam,body.matrix_world.translation) if body else None
        body_in=bp is not None and bp.z>0 and 0<bp.x<1 and 0<bp.y<1
        inside=[p.z>0 and 0<=p.x<=1 and 0<=p.y<=1 for p in pts]
        if body_in and not all(inside): cut.append(f)
    if cut: tot+=len(cut); print('HEADEDGE',r.name,shot,len(cut),'frames',cut[0],'-',cut[-1])
print('HEADEDGE_TOTAL',tot)
