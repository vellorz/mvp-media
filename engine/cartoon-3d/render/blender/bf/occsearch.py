# round 5: brute-force search of one extra's ground offset using the occprobe ray test as the score (props, arms, bodies, poles all count).
# env SHOT, INST (root name), F0/F1, STEP, R (radius m), N (grid n x n). Prints the best offset and its score (sum of covered fractions >= 0.08).
import bpy, json, os
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view as w2c
sc=bpy.context.scene; SH=json.loads(sc['shots']); vl=bpy.context.view_layer
s=os.environ['SHOT']; inst=os.environ['INST']; a,b=SH[s]; a=int(os.environ.get('F0',a)); b=int(os.environ.get('F1',b)); STEP=int(os.environ.get('STEP','4'))
R=float(os.environ.get('R','1.0')); NG=int(os.environ.get('N','5'))
for lc in vl.layer_collection.children:
    if lc.name.startswith('CHR_'): lc.exclude=(lc.name!='CHR_'+s)
cam=bpy.data.objects['cam_'+s]; sc.camera=cam; root=bpy.data.objects[inst]
faces={}
for o in bpy.data.objects:
    if '_d_' in o.name and o.type=='MESH' and o.name.startswith(s+'_'): faces.setdefault(o.name.split('_d_')[0],[]).append(o)
def owner(o):
    while o.parent: o=o.parent
    return o.name
def score():
    tot=0.0
    for f in range(a,b+1,STEP):
        sc.frame_set(f); dg=bpy.context.evaluated_depsgraph_get(); cp=cam.matrix_world.translation
        for nm,cards in faces.items():
            vis_=[c for c in cards if not c.hide_render]
            if not vis_: continue
            fc=vis_[0]; M=fc.matrix_world; vs=[M@v.co for v in fc.data.vertices]; own=owner(fc)
            sp_=[w2c(sc,cam,v) for v in vs]
            if min(p.z for p in sp_)<=0 or max(p.x for p in sp_)-min(p.x for p in sp_)<0.06: continue
            if max(p.x for p in sp_)<0 or min(p.x for p in sp_)>1 or max(p.y for p in sp_)<0 or min(p.y for p in sp_)>1: continue
            if min(p.x for p in sp_)<0 or max(p.x for p in sp_)>1: tot+=0.3   # face sliced by the frame edge
            o_,ex,ey=vs[0],vs[1]-vs[0],vs[3]-vs[0]; cov=0
            for i in range(4):
                for j in range(4):
                    p=o_+ex*(0.22+0.19*i)+ey*(0.22+0.19*j); d=(p-cp); L_=d.length; d.normalize(); org=cp.copy()
                    for _ in range(8):
                        ok,loc,nrm,idx,ob,mat=sc.ray_cast(dg,org,d,distance=L_-(org-cp).length-0.003)
                        if not ok: break
                        src=bpy.data.objects.get(ob.name)
                        if src is None or src.hide_render or owner(src)==own or src.name.endswith('_shadow') or 'glow' in src.name or 'pool' in src.name: org=loc+d*0.002; continue
                        cov+=1; break
            if cov/16>=0.08: tot+=cov/16
    return tot
base=root.delta_location.copy(); best=None
for i in range(NG):
    for j in range(NG):
        dx=-R+2*R*i/(NG-1); dy=-R+2*R*j/(NG-1)
        root.delta_location=base+Vector((dx,dy,0)); sc_=score()
        if best is None or sc_<best[0]: best=(sc_,dx,dy)
        print('TRY',round(dx,2),round(dy,2),round(sc_,2),flush=True)
print('BEST',inst,round(best[1],2),round(best[2],2),round(best[0],2))
