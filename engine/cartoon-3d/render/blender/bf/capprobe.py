# r8b rule (round-7 T7): no face disc may touch a caption box. blender -b bf.blend --python capprobe.py
import bpy, json, os
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view as w2c
sc=bpy.context.scene; SH=json.loads(sc['shots']); CB=json.load(open('/root/bf/bridge/capboxes.json'))
vl=bpy.context.view_layer; hits={}
def cap(f):
    for c in CB:
        if c[0]<=f<c[1]: return c
for shot,(f0,f1) in SH.items():
    cam=bpy.data.objects['cam_'+shot]; sc.camera=cam
    roots=[o for o in bpy.data.objects if o.type=='EMPTY' and o.get('chr')==o.name and o.users_collection and o.users_collection[0].name=='CHR_'+shot]
    for f in range(f0,f1+1,2):
        c=cap(f)
        if not c: continue
        sc.frame_set(f)
        for r in roots:
            hp=bpy.data.objects.get(r.name+'_hp')
            if not hp or r.scale.x<0.01: continue
            fs=[o for o in hp.children if '_d_' in o.name and not o.hide_render]
            if not fs: continue
            o=fs[0]; ctr=o.matrix_world.translation; rad=o.dimensions.x*0.39*r.scale.x if o.dimensions.x>0 else 0.2
            v=w2c(sc,cam,ctr); e=w2c(sc,cam,ctr+cam.matrix_world.to_3x3()@Vector((rad,0,0)))
            if v.z<=0: continue
            rr=abs(e.x-v.x); ry=rr*9/16*16/9   # x and y radii in their own normalised units
            ryn=rr*(1440/2560)
            if v.x+rr<c[2] or v.x-rr>c[3] or v.y+ryn<c[4] or v.y-ryn>c[5]: continue
            if not(0<v.x<1 and 0<v.y<1): continue
            k=(shot,r.name); hits.setdefault(k,[]).append((f,c[6]))
for k,v in hits.items(): print('CAPHIT',k[0],k[1],'f',v[0][0],'-',v[-1][0],'n',len(v),v[0][1])
print('CAPPROBE',len(hits))
