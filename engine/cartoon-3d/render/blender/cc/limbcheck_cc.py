# Rule 329 missing-limb check + full-body cast sheet renders (Cape Cod).
# blender -b cc.blend --python limbcheck_cc.py -- OUTDIR      (opens read-only; never saves)
# For every character instance: head disc, neck, body card(s), arm pivots L/R each with cards, mitten in every arm texture,
# two legs + two feet in every body texture; parts render-visible on sampled frames of the instance's range; whole body in
# camera frame share; torso / legs / total in head widths from the body texture (H = head disc width 0.43 m).
import bpy, sys, os, json, math
import numpy as np
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view as w2c
OUT=sys.argv[sys.argv.index('--')+1]; os.makedirs(OUT,exist_ok=True)
sc=bpy.context.scene; SH=json.loads(sc['shots'])
H=0.43   # head width, m (lib.py HS: disc 800/1024 of a 0.75*HS card)
def tex_alpha(ob):
    for n in ob.active_material.node_tree.nodes:
        if n.type=='TEX_IMAGE' and n.image:
            im=n.image; w,h=im.size; a=np.array(im.pixels[:],np.float32).reshape(h,w,4)[::-1,:,3]   # row 0 = top
            return a
    return None
def runs(row):
    m=row>0.5; d=np.diff(np.r_[0,m.astype(int),0]); s=np.where(d==1)[0]; e=np.where(d==-1)[0]; return list(zip(s,e))
def body_measure(ob):
    a=tex_alpha(ob); h,w=a.shape; card_h=ob.dimensions.z if ob.dimensions.z>0.01 else ob.dimensions.y
    m_per_px=card_h/h
    rows=[r for r in range(h) if (a[r]>0.5).any()]
    top,bot=rows[0],rows[-1]
    # legs: rows with exactly 2 narrow runs; junction = first such row from the top after the garment
    widths=[(r,runs(a[r])) for r in range(top,bot+1)]
    legrows=[r for r,rr in widths if len(rr)==2 and max(e-s for s,e in rr)<0.12*w]
    junction=legrows[0] if legrows else None
    # feet: last rows have 2 runs (two feet) or 1 wide run
    # feet: the round foot blobs at the leg ends; stride cards put them at different heights, so count blobs in the lowest 12 % of the leg span
    y0=int(bot-0.35*(bot-(junction or top))); colany=(a[y0:bot+1]>0.5).any(0)
    xr=[(s_,e_) for s_,e_ in runs(colany.astype(np.float32)) if e_-s_>=8]
    feet2=len(xr)>=2   # two separate leg+foot columns in the lowest 35 % of the leg span (stride cards lift one foot)
    return dict(top_px=top,junction_px=junction,sole_px=bot,two_legs=len(legrows)>0.1*h,two_feet=feet2,m_per_px=m_per_px,
                torso_H=round((junction-top)*m_per_px/H,3) if junction else None, legs_H=round((bot-junction)*m_per_px/H,3) if junction else None)
def mitten(ob):
    a=tex_alpha(ob)
    if a is None: return False
    h,w=a.shape; # the round mitten: the widest alpha run in the lower 40 % is >= 1.8x the arm stroke width
    lo=[max([e-s for s,e in runs(a[r])] or [0]) for r in range(int(0.55*h),h)]
    mid=[max([e-s for s,e in runs(a[r])] or [0]) for r in range(int(0.15*h),int(0.45*h))]
    stroke=np.median([x for x in mid if x>0]) if any(mid) else 0
    return stroke>0 and max(lo)>=1.8*stroke
roots=[o for o in bpy.data.objects if o.type=='EMPTY' and o.get('chr')==o.name]
if not roots:   # fall back: empties that own a _head child
    roots=[o for o in bpy.data.objects if o.type=='EMPTY' and (o.name+'_hp') in bpy.data.objects]
def anc(o,r):
    while o.parent:
        o=o.parent
        if o==r: return True
    return False
res={}; fails=[]
for r in sorted(roots,key=lambda o:o.name):
    inst=r.name; shot=r.users_collection[0].name.replace('CHR_','') if r.users_collection else '?'
    kids=[o for o in bpy.data.objects if o.name.startswith(inst+'_')]
    heads=[o for o in kids if o.name.startswith(inst+'_d_')]; neck=bpy.data.objects.get(inst+'_head')
    bodies=[o for o in kids if o.name.startswith(inst+'_body')]
    arms={sx:[o for o in kids if o.name.startswith(f'{inst}_arm{sx}_')] for sx in (-1,1)}
    piv={sx:bpy.data.objects.get(f'{inst}_ap{sx}') for sx in (-1,1)}
    d=dict(shot=shot,heads=len(heads),neck=neck is not None,bodies=len(bodies),arm_L=len(arms[-1]),arm_R=len(arms[1]),
           piv_L=piv[-1] is not None and anc(piv[-1],r),piv_R=piv[1] is not None and anc(piv[1],r))   # r6: combo rig puts pivots under root>whole>lean
    d['mitten_L']=all(mitten(o) for o in arms[-1] if 'arm_pose' not in o.name) and len(arms[-1])>0; d['mitten_R']=all(mitten(o) for o in arms[1] if 'arm_pose' not in o.name) and len(arms[1])>0
    bm=[body_measure(b) for b in bodies]; d['body']=bm[0] if bm else None
    d['two_legs']=all(b['two_legs'] for b in bm) and bool(bm); d['two_feet']=all(b['two_feet'] for b in bm) and bool(bm)
    # visibility on sampled frames of the shot
    f0,f1=SH.get(shot,(0,0)); cam=bpy.data.objects.get('cam_'+shot); bad=[]; inframe=0; n=0
    for f in range(f0,f1+1,6):
        sc.frame_set(f)
        if r.hide_render: continue
        vh=[o for o in heads if not o.hide_render]; vb=[o for o in bodies if not o.hide_render]; _tp=bpy.data.objects.get(inst+'_btop'); vt=bool(_tp and not _tp.hide_render)
        vL=[o for o in arms[-1] if not o.hide_render]; vR=[o for o in arms[1] if not o.hide_render]
        if not (vh or vb or vL or vR): continue   # character not on screen yet (enters later in the shot): nothing to check
        if len(vh)!=1 or len(vb)!=1 or len(vL)!=1 or len(vR)!=1 or (vt and not any('_blegs' in o.name for o in vb)): bad.append((f,len(vh),len(vb),len(vL),len(vR)))   # r6: split torso (btop) + one legs card counts as one body
        if cam and vb:
            n+=1; b=vb[0]; mw=b.matrix_world
            pts=[w2c(sc,cam,mw@Vector(c)) for c in b.bound_box]+[w2c(sc,cam,o.matrix_world.translation) for o in vh]
            if all(0<=p.x<=1 and 0<=p.y<=1 and p.z>0 for p in pts): inframe+=1
    d['vis_bad']=bad[:6]; d['vis_bad_n']=len(bad); d['whole_in_frame_share']=round(inframe/max(n,1),2)
    b=d['body']; tot=None
    if b and b['torso_H'] is not None: tot=round(b['torso_H']+b['legs_H']+1.0,3)   # + head (1 H)
    d['total_H']=tot
    ok=(d['heads']>=1 and d['neck'] and d['bodies']>=1 and d['arm_L']>=1 and d['arm_R']>=1 and d['piv_L'] and d['piv_R'] and d['mitten_L'] and d['mitten_R'] and d['two_legs'] and d['two_feet'] and not bad)
    d['PASS']=bool(ok); res[inst]=d
    if not ok: fails.append(inst)
kinds={}
for k,v in res.items(): kinds.setdefault(k,v)
json.dump(res,open(OUT+'/limbcheck.json','w'),indent=1,default=str)
B=[v['body'] for v in res.values() if v['body'] and v['body']['torso_H']]
print('LIMBCHECK instances',len(res),'fail',len(fails),fails[:20])
if B:
    t=[b['torso_H'] for b in B]; l=[b['legs_H'] for b in B]
    print('LIMBCHECK torso_H median',round(float(np.median(t)),3),'range',min(t),max(t),' legs_H median',round(float(np.median(l)),3),'range',min(l),max(l))
print('LIMBCHECK_DONE')
