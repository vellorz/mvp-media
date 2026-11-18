# screen box (x0,x1, y-from-top 0..1) of a UV sub-rect of a textured plane, per frame. env: SHOT OBJ U0 V0 U1 V1 (v=0 bottom) F0 F1 STEP
import bpy, os
from bpy_extras.object_utils import world_to_camera_view as w2c
from mathutils import Vector
sc=bpy.context.scene; E=os.environ
shot,ob=E['SHOT'],bpy.data.objects[E['OBJ']]; u0,v0,u1,v1=[float(E[k]) for k in ('U0','V0','U1','V1')]
vl=bpy.context.view_layer
for lc in vl.layer_collection.children:
    if lc.name.startswith('CHR_'): lc.exclude=(lc.name!='CHR_'+shot)
cam=bpy.data.objects['cam_'+shot]; me=ob.data
uvs=[l.uv[:] for l in me.uv_layers.active.data]; vs=[me.vertices[l.vertex_index].co.copy() for l in me.loops]
# bilinear map from uv to local (planes: 4 loops)
def P(u,v):
    # find corners by uv
    c={tuple(round(x) for x in uv):co for uv,co in zip(uvs,vs)}
    a,b,cc,d=c[(0,0)],c[(1,0)],c[(1,1)],c[(0,1)]
    return a*(1-u)*(1-v)+b*u*(1-v)+cc*u*v+d*(1-u)*v
for f in range(int(E['F0']),int(E['F1'])+1,int(E.get('STEP','3'))):
    sc.frame_set(f); M=ob.matrix_world
    pts=[w2c(sc,cam,M@P(u,v)) for u in (u0,u1) for v in (v0,v1)]
    xs=[p.x for p in pts]; ys=[1-p.y for p in pts]
    print('REG',f,round(min(xs),3),round(max(xs),3),round(min(ys),3),round(max(ys),3),flush=True)
