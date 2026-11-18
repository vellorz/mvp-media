# per frame: every face card in the active shot -> screen box, width %W, depth; flags edge cut, bottom 20 % zone, top cut, face-face occlusion
import bpy, json, sys, os
from bpy_extras.object_utils import world_to_camera_view as w2c
from mathutils import Vector
sc=bpy.context.scene
SH=json.loads(sc['shots'])
want=os.environ.get('SHOTS','').split(',') if os.environ.get('SHOTS') else list(SH)
FR=os.environ.get('FRAMES')
step=int(os.environ.get('STEP','3'))
faces={}
for o in bpy.data.objects:
    if '_d_' in o.name and o.type=='MESH': faces.setdefault(o.name.split('_d_')[0],[]).append(o)
def box(cam,o):
    P=[w2c(sc,cam,o.matrix_world@Vector(c)) for c in o.bound_box]
    if min(p.z for p in P)<0.05: return None
    xs=[p.x for p in P]; ys=[p.y for p in P]; return min(xs),max(xs),min(ys),max(ys),sum(p.z for p in P)/8
out=[]
for shot in want:
    a,b=SH[shot]; cam=bpy.data.objects['cam_'+shot]
    frames=range(a,b+1,step) if not FR else [int(x) for x in FR.split(',') if a<=int(x)<=b]
    for f in frames:
        sc.frame_set(f); row=[]
        for i,os_ in faces.items():
            if not i.startswith(shot+'_'): continue
            vs=[o for o in os_ if not o.hide_render]
            if not vs: continue
            o=vs[0]
            r=box(cam,o)
            if not r: continue
            x0,x1,y0,y1,z=r
            if x1<0 or x0>1 or y1<0 or y0>1: continue
            main='_x' not in i
            row.append(dict(i=i[len(shot)+1:],main=main,w=round((x1-x0)*100,1),cx=round((x0+x1)/2,3),cy=round((y0+y1)/2,3),x0=x0,x1=x1,y0=y0,y1=y1,z=round(z,2)))
        fl=[]
        for d in row:
            hx=0.12*(d['x1']-d['x0']); hy=0.12*(d['y1']-d['y0'])   # the drawn head is ~76 % of its card
            if d['x0']+hx<0 or d['x1']-hx>1 or d['y1']-hy>1 or d['y0']+hy<0: fl.append('CUT:'+d['i'])
            if d['cy']<0.2: fl.append('LOW:'+d['i'])
        for d in row:
            for e in row:
                if e is d or e['z']>=d['z']: continue   # e nearer than d
                ox=min(d['x1'],e['x1'])-max(d['x0'],e['x0']); oy=min(d['y1'],e['y1'])-max(d['y0'],e['y0'])
                if ox>0 and oy>0:
                    frac=ox*oy/((d['x1']-d['x0'])*(d['y1']-d['y0']))
                    if frac>0.25: fl.append(f"OCC:{d['i']}<{e['i']}:{frac:.2f}")
        out.append(dict(shot=shot,f=f,faces=[{k:v for k,v in d.items() if k not in('x0','x1','y0','y1')} for d in row],flags=fl))
json.dump(out,open(os.environ.get('OUT','/root/bf/probe/faces.json'),'w'),indent=0)
for r in out:
    m=[d for d in r['faces'] if d['main']]
    print(r['shot'],r['f'],' '.join(f"{d['i']}:{d['w']}@({d['cx']},{d['cy']})" for d in m),'|',' '.join(r['flags']))
