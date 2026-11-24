# head width as % of frame width per shot (rule 309: medium-shot heads 28-36% W). Max head on screen, sampled every 6 f.
import bpy, json, sys
from bpy_extras.object_utils import world_to_camera_view as w2c
from mathutils import Vector
HS=0.43/0.586
sc=bpy.context.scene; SH=json.loads(sc['shots'])
for s,(a,b) in SH.items():
    cam=bpy.data.objects['cam_'+s]; hps=[o for o in bpy.data.collections['CHR_'+s].all_objects if o.name.endswith('_hp')]
    best=[]
    for f in range(a,b+1,6):
        sc.frame_set(f); mx=0
        R=cam.matrix_world.to_quaternion()@Vector((1,0,0))
        for h in hps:
            fc=[c for c in h.children if '_d_' in c.name]
            if not fc or all(c.hide_render for c in fc): 
                if h.parent and any(ch.hide_render for ch in h.parent.children_recursive if '_body' in ch.name and False): pass
            c=h.matrix_world@Vector((0,0,0.2535*HS)); r=0.75*HS*0.39*h.matrix_world.to_scale()[0]
            p0=w2c(sc,cam,c); p1=w2c(sc,cam,c+R*r)
            if p0.z<=0 or not(-0.1<p0.x<1.1 and -0.1<p0.y<1.1): continue
            mx=max(mx,2*abs(p1.x-p0.x))
        best.append(mx)
    best.sort(); print('HEAD',s,'median %.0f%% max %.0f%%'%(100*best[len(best)//2],100*best[-1]))
