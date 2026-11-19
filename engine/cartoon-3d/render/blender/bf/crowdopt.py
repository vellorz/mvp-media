# random-search the S16 crowd extras' ground offsets (delta_location) so no face is covered by a nearer face (>15 %),
# no face sits in the caption band, extras keep >= 0.85 m spacing. Prints best offsets as JSON.
import bpy, json, random, math, os
from bpy_extras.object_utils import world_to_camera_view as w2c
from mathutils import Vector
sc=bpy.context.scene; SH=json.loads(sc['shots']); shot=os.environ.get('SHOT','S16'); a,b=SH[shot]; a=int(os.environ.get('F0',a)); b=int(os.environ.get('F1',b))
cam=bpy.data.objects['cam_'+shot]; N=int(os.environ.get('N','10'))
import re
roots=sorted([o for o in bpy.data.objects if re.fullmatch(shot+r'_x\d+_[a-z0-9]+',o.name)],key=lambda o:int(o.name.split('_x')[1].split('_')[0]))
faces={r.name:[o for o in bpy.data.objects if o.name.startswith(r.name+'_d_')] for r in roots}
mains=[o for o in bpy.data.objects if '_d_' in o.name and o.name.startswith(shot+'_') and '_x' not in o.name]
frames=list(range(a,b+1,4)); ROW=float(os.environ.get('ROW','0'))
# cache per-frame: camera matrices and the visible face card per root (face cards are children: local box fixed)
def vis_face(r):
    for o in faces[r.name]:
        if not o.hide_render: return o
cache=[]
# round 4: props, arms, poles also cover faces (crowdopt used to score face-on-face only)
xr=tuple(r.name for r in roots)
arms={r.name:[o for o in bpy.data.objects if o.name.startswith(r.name+'_arm') and o.type=='MESH'] for r in roots}
OCCN=('arm','fist','stick','placard','pole','post','sign','lamp','mb','cool','bin','register','pc_')
def is_occ(o):
    if o.type!='MESH' or o.name.startswith(xr) or '_d_' in o.name or 'glow' in o.name or 'pool' in o.name: return False
    return any(k in o.name.lower() for k in OCCN)
occs=[o for o in bpy.data.objects if is_occ(o)]
def sbox(M,bb,d=Vector((0,0,0))):
    P=[w2c(sc,cam,M@Vector(c)+d) for c in bb]
    if min(p.z for p in P)<0.05: return None
    return (min(p.x for p in P),max(p.x for p in P),min(p.y for p in P),max(p.y for p in P),sum(p.z for p in P)/8)
for f in frames:
    sc.frame_set(f)
    row={r.name:(vis_face(r).matrix_world.copy() if vis_face(r) else None) for r in roots}
    ob=[]
    for o in occs:
        if o.hide_render or not o.visible_get(): continue
        b_=sbox(o.matrix_world,o.bound_box)
        if b_ and b_[1]>0 and b_[0]<1 and b_[3]>0 and b_[2]<1 and (b_[1]-b_[0])*(b_[3]-b_[2])<0.2: ob.append(b_)
    am={r.name:[(o.matrix_world.copy(),[Vector(c) for c in o.bound_box]) for o in arms[r.name] if not o.hide_render] for r in roots}
    cache.append((f,row,[o.matrix_world.copy() for o in mains if not o.hide_render],ob,am))
PO=bpy.data.objects.get('poster'); PB={}
if PO:
    for f in frames:
        sc.frame_set(f); P=[w2c(sc,cam,PO.matrix_world@Vector(c)) for c in PO.bound_box]
        PB[f]=(min(p.x for p in P),max(p.x for p in P),min(p.y for p in P),max(p.y for p in P))
corners=[Vector(c) for c in roots[0].children[0].bound_box] if False else None
fb={r.name:[Vector(c) for c in faces[r.name][0].bound_box] for r in roots}
mb=[Vector(c) for c in mains[0].bound_box] if mains else []
base={r.name:r.matrix_world.translation.copy() for r in roots}
def score(off,verbose=False):
    pen=0.0
    names=[r.name for r in roots]
    for i in range(len(names)):
        for j in range(i+1,len(names)):
            p=base[names[i]]+Vector((*off[i],0)); q=base[names[j]]+Vector((*off[j],0))
            dd=(p-q).length
            if dd<0.85: pen+=50*(0.85-dd)
            dx_,dy_=abs(p.x-q.x),abs(p.y-q.y)
            if ROW and dx_<2.2 and dy_<0.7: pen+=ROW*(0.7-dy_)   # rule P3: neighbours staggered in depth, no line-ups
    for f,row,mm,ob,am in cache:
        sc.frame_set(f)
        boxes=[]
        for k,nm in enumerate(names):
            M=row[nm]
            if M is None: continue
            d=Vector((*off[k],0))
            P=[w2c(sc,cam,M@c+d) for c in fb[nm]]
            if min(p.z for p in P)<0.05: continue
            x0,x1=min(p.x for p in P),max(p.x for p in P); y0,y1=min(p.y for p in P),max(p.y for p in P)
            if x1<0 or x0>1 or y1<0 or y0>1: continue
            if x0<0 or x1>1 or y0<0 or y1>1: pen+=float(os.environ.get('EDGE','0'))   # round 4: no face sliced by the frame edge
            if PB.get(f) and f>=1686:
                q=PB[f]; ox=min(x1,q[1])-max(x0,q[0]); oy=min(y1,q[3])-max(y0,q[2])
                if ox>0 and oy>0: pen+=20*ox*oy/((x1-x0)*(y1-y0))+5   # round 4 E2: no head over the poster
            boxes.append((nm,x0,x1,y0,y1,sum(p.z for p in P)/8))
            # caption band (y from bottom 0.27-0.325, centre third+)
            ix=0.1*(x1-x0); iy=0.1*(y1-y0)
            ox=min(x1-ix,0.78)-max(x0+ix,0.22); oy=min(y1-iy,0.325)-max(y0+iy,0.27)
            if ox>0 and oy>0: pen+=5
        for M in mm:
            P=[w2c(sc,cam,M@c) for c in mb]
            if min(p.z for p in P)<0.05: continue
            boxes.append(('main',min(p.x for p in P),max(p.x for p in P),min(p.y for p in P),max(p.y for p in P),sum(p.z for p in P)/8))
        occb=[('occ',)+b_ for b_ in ob]
        for k,nm in enumerate(names):
            d=Vector((*off[k],0))
            for M,bb in am.get(nm,[]):
                b_=sbox(M,bb,d)
                if b_: occb.append(('arm:'+nm,)+b_)
        for d_ in boxes:
            for e in occb:
                if e[0]=='arm:'+d_[0] or e[5]>=d_[5]: continue
                ox=min(d_[2],e[2])-max(d_[1],e[1]); oy=min(d_[4],e[4])-max(d_[3],e[3])
                if ox>0 and oy>0:
                    fr=ox*oy/((d_[2]-d_[1])*(d_[4]-d_[3]))
                    if fr>0.06: pen+=2*fr
                    if verbose and fr>0.06: print('OCCP',f,d_[0],'<',e[0],round(fr,2))
        for d_ in boxes:
            for e in boxes:
                if e is d_ or e[5]>=d_[5]: continue
                ox=min(d_[2],e[2])-max(d_[1],e[1]); oy=min(d_[4],e[4])-max(d_[3],e[3])
                if ox>0 and oy>0:
                    fr=ox*oy/((d_[2]-d_[1])*(d_[4]-d_[3]))
                    if fr>0.15: pen+=fr*(3 if d_[0]=='main' else 1)
                    if verbose and fr>0.15: print('OCC',f,d_[0],'<',e[0],round(fr,2))
    return pen
R=random.Random(int(os.environ.get('SEED','1'))); lim=float(os.environ.get('LIM','0.7'))
best=[(0.0,0.0)]*len(roots); bs=score(best); print('START',round(bs,2),flush=True)
for it in range(int(os.environ.get('IT','300'))):
    cand=list(best); k=R.randrange(len(cand)); cand[k]=(max(-lim,min(lim,cand[k][0]+R.gauss(0,0.25))),max(-lim,min(lim,cand[k][1]+R.gauss(0,0.25))))
    s=score(cand)
    if s<bs: best,bs=cand,s; print('IT',it,round(bs,3),flush=True)
    if bs<0.01: break
score(best,True)
print('BEST',json.dumps({r.name:[round(x,2),round(y,2)] for r,(x,y) in zip(roots,best)}),round(bs,3))
