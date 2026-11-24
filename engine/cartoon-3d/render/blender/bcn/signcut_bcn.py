# bcn r2: is any sign/board partly in frame (cut by the frame edge)? Projects the 8 bbox corners of every sign/board card per frame.
# blender -b bcn.blend --python signcut_bcn.py [-- S01 S09]
import bpy, json, sys
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view as w2c
sc=bpy.context.scene; SH=json.loads(sc['shots']); args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else list(SH)
OBJ=[o for o in bpy.data.objects if o.type=='MESH' and any(k in o.name.lower() for k in ('sign','score')) and not o.name.endswith('_ink') and 'post' not in o.name]
tot=0
for n in args:
    a,b=SH[n]; cam=bpy.data.objects['cam_'+n]
    sc.camera=cam; runs={}
    for f in range(a,b+1,2):
        sc.frame_set(f)
        for o in OBJ:
            if o.hide_render: continue
            cs=[w2c(sc,cam,o.matrix_world@Vector(c)) for c in o.bound_box]
            if any(c.z<=0 for c in cs): continue
            inside=[0<=c.x<=1 and 0<=c.y<=1 for c in cs]
            xs=[c.x for c in cs]; ys=[c.y for c in cs]
            overlap=max(xs)>0 and min(xs)<1 and max(ys)>0 and min(ys)<1
            if overlap and not all(inside):
                ex=max(0,-min(xs))+max(0,max(xs)-1)+max(0,-min(ys))+max(0,max(ys)-1)
                runs.setdefault(o.name,[]).append((f,round(ex,3)))
    for k,v in runs.items():
        print('SIGNCUT',n,k,'frames',v[0][0],'-',v[-1][0],'n',len(v),'max_out',max(e for _,e in v)); tot+=len(v)
print('SIGNCUT_TOTAL',tot)
