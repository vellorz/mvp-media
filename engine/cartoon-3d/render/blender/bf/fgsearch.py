# round 5: grid search for an FG object position per S16 segment: stays at a frame edge (screen x in [-0.1,0.3] or [0.7,1.1], partly in), never sweeps, depth z small
import bpy, os, itertools, json
from bpy_extras.object_utils import world_to_camera_view as w2c
from mathutils import Vector
sc=bpy.context.scene; s=os.environ.get('SHOT','S16'); cam=bpy.data.objects['cam_'+s]
SEGS=json.loads(os.environ['SEGS']); HZ=float(os.environ.get('HZ','0.4')); HX_=float(os.environ.get('HXY','0.25'))
X0,X1,Y0,Y1=[float(v) for v in os.environ['GRID'].split(',')]
frames={}
for a,b in SEGS:
    for f in range(a,b+1,3): frames[f]=None
cache={}
for f in frames: sc.frame_set(f); cache[f]=cam.matrix_world.copy()
res=[]
x=X0
while x<=X1:
    y=Y0
    while y<=Y1:
        pts=[Vector((x+i*HX_,y+j*HX_,HZ+k*HZ)) for i,j,k in itertools.product((-1,1),repeat=3)]
        for a,b in SEGS:
            ok=True; xs=[]; ys=[]; zs=[]
            for f in range(a,b+1,3):
                cam.matrix_world=cache[f]; sc.frame_set(f)
                P=[w2c(sc,cam,p) for p in pts]; mnx,mxx=min(p.x for p in P),max(p.x for p in P); mny,mxy=min(p.y for p in P),max(p.y for p in P); mz=min(p.z for p in P)
                if mz<0.4: ok=False; break
                left= mxx>0.04 and mxx<0.3 and mnx<0.02
                right= mnx<0.96 and mnx>0.7 and mxx>0.98
                if not(left or right) or mxy<0.05: ok=False; break
                xs.append((round(mnx,2),round(mxx,2))); ys.append(round(mxy,2)); zs.append(round(mz,1))
            if ok: res.append(((a,b),round(x,2),round(y,2),xs[0],xs[-1],max(ys),min(zs)))
        y+=0.3
    x+=0.3
for r in res: print('CAND',r)
print('N',len(res))
