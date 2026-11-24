# list candidate bridge shapes (heads + named rectangles) on screen at each dissolve midpoint
import bpy, sys, json
from bpy_extras.object_utils import world_to_camera_view as w2c
from mathutils import Vector
sys.path.insert(0,'/root/bf/src')
sc=bpy.context.scene
SH={'S01':(0,170),'S02':(163,297),'S03':(292,432),'S04':(426,528),'S05':(520,652),'S06':(643,781),'S07':(775,866),'S08':(867,938),'S09':(931,1013),'S10':(1008,1057),'S11':(1051,1125),'S12':(1114,1218),'S13':(1210,1359),'S14':(1352,1487),'S15':(1481,1565),'S16':(1556,1752)}
K=list(SH); RECT=('board','ledger','paper','banner','poster','sign','frame','window','screen','cal','stand','dept','facade','door','lamp','wanted','map','sheet','roller','podium','desk','register')
def items(shot,f):
    sc.frame_set(f); cam=bpy.data.objects['cam_'+shot]; out=[]
    for o in sc.objects:
        if o.type!='MESH' or o.hide_render: continue
        cols=[c.name for c in o.users_collection]
        isc=any(c.startswith('CHR_') for c in cols)
        if isc and not any(c=='CHR_'+shot for c in cols): continue
        n=o.name
        if isc and '_d_' in n:
            pass
        elif not isc and any(r in n.lower() for r in RECT): pass
        else: continue
        bb=[o.matrix_world@Vector(c) for c in o.bound_box]; P=[w2c(sc,cam,p) for p in bb]
        if min(p.z for p in P)<0.05: continue
        xs=[p.x for p in P]; ys=[p.y for p in P]
        x0,x1,y0,y1=max(0,min(xs)),min(1,max(xs)),max(0,min(ys)),min(1,max(ys))
        if x1<=x0 or y1<=y0: continue
        w,h=(max(xs)-min(xs)),(max(ys)-min(ys))
        if w*h<0.002: continue
        out.append(dict(n=n,cx=round((min(xs)+max(xs))/2,3),cy=round((min(ys)+max(ys))/2,3),w=round(w,3),h=round(h,3),head=isc))
    return sorted(out,key=lambda d:-d['w']*d['h'])[:60]
R=[]
for A,B in zip(K,K[1:]):
    a,b=SH[B][0],SH[A][1]
    if b<a: continue
    m=(a+b)//2; R.append(dict(join=f'{A}>{B}',frames=[a,b],mid=m,A=items(A,m),B=items(B,m)))
json.dump(R,open('/root/bf/bridge/probe.json','w'),indent=1)
print('PROBE_OK',len(R))
