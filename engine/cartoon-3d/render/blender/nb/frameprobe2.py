# r2 framing probe (every 3rd frame): per shot head width % W (min/med/max), heads inside the caption band (y from top 0.66-0.75), heads cut by an edge (centre x<0.07 or >0.93, y<0.05 or >0.95 while partly visible)
import bpy, json, statistics as st
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view as w2c
sc=bpy.context.scene; SH=json.loads(sc['shots']); roots=[o for o in bpy.data.objects if o.get('is_char')]
tot_band=tot_edge=0
for n,(a,b) in SH.items():
    cam=bpy.data.objects['cam_'+n]; W=[]; band=[]; edge=[]
    rs=[r for r in roots if r.get('shot')==n]
    for f in range(a,b,3):
        sc.frame_set(f); right=cam.matrix_world.to_3x3()@Vector((1,0,0))
        for r in rs:
            if r.hide_render: continue
            hp=bpy.data.objects.get(r.name+'_hp')
            if not hp: continue
            c=hp.matrix_world.translation+Vector((0,0,0.20)); p=w2c(sc,cam,c)
            if p.z<=0: continue
            w=abs(w2c(sc,cam,c+right*0.43).x-p.x); y=1-p.y; nm=r.name.split('_',1)[1]
            if -0.1<p.x<1.1 and -0.1<y<1.1:
                if 0.0<=p.x<=1 and 0<=y<=1: W.append(w*100)
                if 0.64<=y<=0.77 and 0<p.x<1: band.append((f,nm,round(y,2)))
                if (p.x-w/2<0.0 or p.x+w/2>1.0 or y-w*0.3<0 or y+w*0.5>1.0) and (p.x+w/2>0 and p.x-w/2<1): edge.append((f,nm))
    tot_band+=len(band); tot_edge+=len(edge)
    print('FP2',n,'headW%%',(round(min(W)),round(st.median(W)),round(max(W))) if W else None,'band',len(band),band[:3],'edge',len(edge),edge[:3])
print('FP2_TOTAL band',tot_band,'edge',tot_edge)
