# round 4: is any face covered by a PROP or another character? ray-cast from the camera to a 5x5 grid on the visible face card, per frame.
# Hits on the same character (its other expression cards, own hat) are ignored; render-hidden objects are skipped. Prints runs where >= MIN of the grid is covered.
import bpy, json, os
from mathutils import Vector
sc=bpy.context.scene; SH=json.loads(sc['shots']); vl=bpy.context.view_layer
ONLY=os.environ.get('SHOTS'); STEP=int(os.environ.get('STEP','2')); MIN=float(os.environ.get('MIN','0.12'))
faces={}
for o in bpy.data.objects:
    if '_d_' in o.name and o.type=='MESH': faces.setdefault(o.name.split('_d_')[0],[]).append(o)
def owner(o):
    while o.parent: o=o.parent
    return o.name
out={}
for s,(a,b) in SH.items():
    if ONLY and s not in ONLY.split(','): continue
    for lc in vl.layer_collection.children:
        if lc.name.startswith('CHR_'): lc.exclude=(lc.name!='CHR_'+s)
    cam=bpy.data.objects['cam_'+s]; sc.camera=cam
    runs={}
    for f in range(a,b+1,STEP):
        sc.frame_set(f); dg=bpy.context.evaluated_depsgraph_get(); cp=cam.matrix_world.translation
        for inst,cards in faces.items():
            if not inst.startswith(s+'_'): continue
            vis_=[c for c in cards if not c.hide_render]
            if not vis_: continue
            fc=vis_[0]; me=fc.data; M=fc.matrix_world; vs=[M@v.co for v in me.vertices]
            mn=Vector([min(v[i] for v in vs) for i in range(3)]); own=owner(fc)
            from bpy_extras.object_utils import world_to_camera_view as w2c
            sp_=[w2c(sc,cam,v) for v in vs]
            if min(p.z for p in sp_)<=0 or max(p.x for p in sp_)-min(p.x for p in sp_)<float(os.environ.get('MINW','0.06')): continue   # tiny background heads: depth layering, not a covered face
            if max(p.x for p in sp_)<0 or min(p.x for p in sp_)>1 or max(p.y for p in sp_)<0 or min(p.y for p in sp_)>1: continue
            # grid over the card's central 60 % (the drawn head disc)
            o_,ex,ey=vs[0],vs[1]-vs[0],vs[3]-vs[0]
            n=0; cov=0; who=set()
            for i in range(5):
                for j in range(5):
                    p=o_+ex*(0.2+0.15*i)+ey*(0.2+0.15*j); d=(p-cp); L_=d.length; d.normalize(); org=cp.copy(); hit_bad=None
                    for _ in range(8):
                        ok,loc,nrm,idx,ob,mat=sc.ray_cast(dg,org,d,distance=L_-(org-cp).length-0.003)
                        if not ok: break
                        src=bpy.data.objects.get(ob.name)
                        if src is None or src.hide_render or owner(src)==own or src.name.endswith('_shadow') or 'glow' in src.name or 'pool' in src.name: org=loc+d*0.002; continue
                        hit_bad=src.name; break
                    n+=1
                    if hit_bad: cov+=1; who.add(hit_bad)
            if n and cov/n>=MIN: runs.setdefault(inst,[]).append((f,round(cov/n,2),sorted(who)[:3]))
    for inst,r in runs.items():
        print('OCC',s,inst,r[0][0],'-',r[-1][0],'n',len(r),'max',max(x[1] for x in r),r[0][2],flush=True)
        out.setdefault(s,[]).append(dict(inst=inst,f=[r[0][0],r[-1][0]],n=len(r),mx=max(x[1] for x in r),by=r[0][2]))
json.dump(out,open('/root/cc/bridge/occprobe.json','w'),indent=1); print('OCCPROBE_DONE')
