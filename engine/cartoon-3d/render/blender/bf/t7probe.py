# T7: caption never on a face or on the poster. Face = inner 80 % of the face card. Every 2nd frame.
import bpy, json
from bpy_extras.object_utils import world_to_camera_view as w2c
from mathutils import Vector
sc=bpy.context.scene
SH={'S01':(0,170),'S02':(163,297),'S03':(292,432),'S04':(426,528),'S05':(520,652),'S06':(643,781),'S07':(775,866),'S08':(867,938),'S09':(931,1013),'S10':(1008,1057),'S11':(1051,1125),'S12':(1114,1218),'S13':(1210,1359),'S14':(1352,1487),'S15':(1481,1565),'S16':(1556,1752)}
CAP=json.load(open('/root/bf/bridge/caprects.json'))
faces={}
for o in bpy.data.objects:
    if '_d_' in o.name and o.type=='MESH':
        inst=o.name.split('_d_')[0]; faces.setdefault(inst,o)
def rect(cam,o,shrink):
    P=[w2c(sc,cam,o.matrix_world@Vector(c)) for c in o.bound_box]
    if min(p.z for p in P)<0.05: return None
    xs=[p.x for p in P]; ys=[p.y for p in P]; cx,cy=(min(xs)+max(xs))/2,(min(ys)+max(ys))/2; hw,hh=(max(xs)-min(xs))/2*shrink,(max(ys)-min(ys))/2*shrink
    return cx-hw,cx+hw,cy-hh,cy+hh
hits=[]
for f in range(0,1753,2):
    c=[c for c in CAP if c['a']<=f<c['b']]
    if not c: continue
    c=c[0]; sc.frame_set(f)
    for shot,(a,b) in SH.items():
        if not a<=f<=b: continue
        cam=bpy.data.objects['cam_'+shot]
        objs=[(i,o,0.8) for i,o in faces.items() if i.startswith(shot+'_')]
        if shot=='S16': objs.append(('poster',bpy.data.objects['poster'],1.0))
        for i,o,sh in objs:
            r=rect(cam,o,sh)
            if not r: continue
            x0,x1,y0,y1=r
            if x1<0 or x0>1 or y1<0 or y0>1: continue
            # faces are discs: test the inscribed circle (pixel space, 1440x2560) against the caption box
            cx,cy,rx=(x0+x1)/2*1440,(y0+y1)/2*2560,(x1-x0)/2*1440
            nx=min(max(cx,c['x0']*1440),c['x1']*1440); ny=min(max(cy,c['y0']*2560),c['y1']*2560)
            disc_hit=(i=='poster') or ((nx-cx)**2+(ny-cy)**2<rx*rx)
            if disc_hit and x0<c['x1'] and x1>c['x0'] and y0<c['y1'] and y1>c['y0']:
                ov=(min(x1,c['x1'])-max(x0,c['x0']))*(min(y1,c['y1'])-max(y0,c['y0']))/((x1-x0)*(y1-y0))
                hits.append(dict(f=f,shot=shot,obj=i,cap=c['txt'],face_frac=round(ov,3)))
json.dump(hits,open('/root/bf/bridge/t7.json','w'),indent=1)
from collections import Counter
print('T7_HITS',len(hits),Counter((h['shot'],h['obj']) for h in hits).most_common(30))
