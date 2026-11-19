# round 4 (E2): fraction of the poster covered (ray grid 9x9) and whether its whole frame is inside the shot, per frame of S16
import bpy, json
from bpy_extras.object_utils import world_to_camera_view as w2c
sc=bpy.context.scene; vl=bpy.context.view_layer
for lc in vl.layer_collection.children:
    if lc.name.startswith('CHR_'): lc.exclude=(lc.name!='CHR_S16')
cam=bpy.data.objects['cam_S16']; sc.camera=cam; po=bpy.data.objects['poster']; fr=bpy.data.objects['poster_frame']
bad=[]
for f in range(1640,1752):
    sc.frame_set(f); dg=bpy.context.evaluated_depsgraph_get(); cp=cam.matrix_world.translation
    M=po.matrix_world; vs=[M@v.co for v in po.data.vertices]; o_,ex,ey=vs[0],vs[1]-vs[0],vs[3]-vs[0]
    sp=[w2c(sc,cam,fr.matrix_world@__import__('mathutils').Vector(c)) for c in fr.bound_box]
    inside=all(0<=p.x<=1 and 0<=p.y<=1 and p.z>0 for p in sp)
    cov=0; who=set()
    for i in range(9):
        for j in range(9):
            p=o_+ex*(0.05+0.1125*i)+ey*(0.05+0.1125*j); d=p-cp; L_=d.length; d.normalize()
            ok,loc,n,idx,ob,m=sc.ray_cast(dg,cp,d,distance=L_-0.01)
            if ok and ob.name not in ('poster',) and not ob.name.startswith('poster_frame') and not ('glow' in ob.name or 'pool' in ob.name):
                src=bpy.data.objects.get(ob.name)
                if src and not src.hide_render: cov+=1; who.add(ob.name)
    if f>=1690 and cov: bad.append((f,round(cov/81,3),sorted(who)[:2]))
    if f%6==0 or (f>=1690 and cov): print('POSTER',f,'inside',inside,'cov',round(cov/81,3),sorted(who)[:3],flush=True)
print('POSTER_BAD',bad)
