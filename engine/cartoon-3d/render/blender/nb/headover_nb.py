# r6: head-behind-head probe (shots r5: occprobe missed S05 pilB and S08 pil covered by a nearer head). Projects every visible
# head disc (radius 0.215 m * scale) to the camera; reports frames where a farther face disc overlaps a nearer head disc by >= 15 % of its area.
# blender -b cc.blend --python headover_cc.py [-- S05 S08]
import bpy, json, sys, math
from bpy_extras.object_utils import world_to_camera_view as w2c
sc=bpy.context.scene; SH=json.loads(sc['shots']); args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else list(SH)
def area_ov(a,b):
    (x1,y1,r1),(x2,y2,r2)=a,b; d=math.hypot(x1-x2,y1-y2)
    if d>=r1+r2: return 0.0
    if d<=abs(r1-r2): return min(r1,r2)**2*math.pi
    a1=r1*r1*math.acos((d*d+r1*r1-r2*r2)/(2*d*r1)); a2=r2*r2*math.acos((d*d+r2*r2-r1*r1)/(2*d*r2))
    return a1+a2-0.5*math.sqrt(max(0,(-d+r1+r2)*(d+r1-r2)*(d-r1+r2)*(d+r1+r2)))
tot=0; AR=1440/2560
for s in args:
    a,b=SH[s]; cam=bpy.data.objects['cam_'+s]; runs={}
    roots=[o for o in bpy.data.objects if o.type=='EMPTY' and o.name.startswith(s+'_') and any(c.type=='LOCKED_TRACK' for c in o.constraints)]
    for f in range(a,b+1,2):
        sc.frame_set(f); H=[]
        for r in roots:
            hp=bpy.data.objects.get(r.name+'_hp')
            if not hp or r.hide_render: continue
            fc=[o for o in bpy.data.objects if o.name.startswith(r.name+'_d_') and not o.hide_render]
            if not fc: continue
            c=fc[0].matrix_world.translation; p=w2c(sc,cam,c)
            if p.z<=0: continue
            sca=r.matrix_world.to_scale()[0]; e=w2c(sc,cam,c+cam.matrix_world.to_3x3()@__import__('mathutils').Vector((0.215*sca,0,0)))
            rad=abs(e.x-p.x); H.append((r.name,p.x,p.y*(1/AR),rad,p.z))
        for n1,x1,y1,r1,z1 in H:
            for n2,x2,y2,r2,z2 in H:
                if z2>=z1: continue   # n2 nearer than n1
                ov=area_ov((x1,y1,r1),(x2,y2,r2))/(math.pi*r1*r1)
                if ov>=0.15: runs.setdefault((n1,n2),[]).append((f,round(ov,2)))
    for (n1,n2),v in runs.items():
        print('HEADOVER',s,n1,'behind',n2,'frames',v[0][0],'-',v[-1][0],'n',len(v),'max',max(x[1] for x in v)); tot+=len(v)
print('HEADOVER_TOTAL',tot)
