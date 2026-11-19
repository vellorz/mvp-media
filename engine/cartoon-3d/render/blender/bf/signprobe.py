# rule 197 probe: for every lettered plane (rects in letter_rects.json), per shot frame: is the lettering fully in, fully out or PARTIAL (cropped)?
# a sign is OK in a shot if it is never partial while the plane faces the camera and is nearer than FAR m. Prints partial runs.
import bpy, json, os
from bpy_extras.object_utils import world_to_camera_view as w2c
sc=bpy.context.scene; SH=json.loads(sc['shots']); R=json.load(open('/root/bf/src/letter_rects.json'))
FAR=float(os.environ.get('FAR','40')); STEP=int(os.environ.get('STEP','2')); ONLY=os.environ.get('SHOTS'); MINH=float(os.environ.get('MINH','0.02'))   # lettering shorter than 2 % H is texture, not a readable word
def img(o):
    for m in o.data.materials:
        if m and m.use_nodes:
            for n in m.node_tree.nodes:
                if n.type=='TEX_IMAGE' and n.image: return os.path.splitext(os.path.basename(n.image.filepath))[0]
cands=[]
for o in bpy.data.objects:
    if o.type=='MESH' and len(o.data.vertices)==4 and o.data.uv_layers:
        k=img(o)
        if k in R:
            rr_=R[k] if isinstance(R[k][0],list) else [R[k]]   # round 4: several lettered rects per texture (ledger totals)
            for q_,r_ in enumerate(rr_): cands.append((o,r_,f'{o.name}#{q_}'))
def P(o,u,v):
    me=o.data; uvs=[l.uv[:] for l in me.uv_layers.active.data]; vs=[me.vertices[l.vertex_index].co for l in me.loops]
    c={tuple(round(x) for x in uv):co for uv,co in zip(uvs,vs)}
    a,b,cc,d=c[(0,0)],c[(1,0)],c[(1,1)],c[(0,1)]
    return o.matrix_world@(a*(1-u)*(1-v)+b*u*(1-v)+cc*u*v+d*(1-u)*v)
out={}
CP={nm:[(u,v) for u in (r[0],(r[0]+r[2])/2,r[2]) for v in (r[1],r[3])] for o,r,nm in cands}
for s,(a,b) in SH.items():
    if ONLY and s not in ONLY.split(','): continue
    cam=bpy.data.objects['cam_'+s]; ST={nm:[] for o,_,nm in cands}
    for f in range(a,b+1,STEP):
        sc.frame_set(f); cp=cam.matrix_world.translation
        for o,_,nm in cands:
            if (o.matrix_world.translation-cp).length>FAR+10: ST[nm].append((f,'X')); continue
            n=(o.matrix_world.to_3x3()@o.data.polygons[0].normal)
            if n.dot(cp-o.matrix_world.translation)<=0: ST[nm].append((f,'X')); continue
            pts=[w2c(sc,cam,P(o,u,v)) for u,v in CP[nm]]
            if min(p.z for p in pts)<=0 or min(p.z for p in pts)>FAR: ST[nm].append((f,'X')); continue
            ins=[0<=p.x<=1 and 0<=p.y<=1 for p in pts]
            ov=min(p.x for p in pts)<1 and max(p.x for p in pts)>0 and min(p.y for p in pts)<1 and max(p.y for p in pts)>0
            hgt=max(p.y for p in pts)-min(p.y for p in pts)
            k='IN' if all(ins) else ('PART' if ov else 'OUT')
            if k=='PART' and hgt<MINH: k='SMALL'
            ST[nm].append((f,k))
    for nm,st in ST.items():
        parts=[f for f,k in st if k=='PART']
        if parts:
            ins=[f for f,k in st if k=='IN']
            out.setdefault(s,[]).append(dict(obj=nm,part=[parts[0],parts[-1]],n_part=len(parts),n_in=len(ins)))
            print('SIGN',s,nm,'partial',parts[0],'-',parts[-1],'n',len(parts),'in',len(ins),flush=True)
json.dump(out,open('/root/bf/bridge/signprobe.json','w'),indent=1); print('SIGNPROBE_DONE')
