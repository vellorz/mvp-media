# dc14 rule 344 probe (from Detroit facebox.py; DC padded head cards: the disc is measured, never the card).
# blender -b dc.blend --python facebox_dc.py -- OUT.json [S19 S20 ...]   prints CAPCLASH (face disc meets the caption column 0.37-0.63 W and reaches below 0.665 H)
# and FACECUT (face disc cut by the frame edge away from shot edges), plus head width % W per instance (rule 345/309)
import bpy, json, sys
sys.path.insert(0,'/root/dc/src'); import expressions as X
from bpy_extras.object_utils import world_to_camera_view as w2c
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]; out=a[0]; only=set(a[1:])
CI=X.expand(json.load(open('/root/dc/src/cast.json')))
sc=bpy.context.scene; SH=json.loads(sc['shots']); R={}; CUT={}; CLASH={}; HW={}
heads={}
for o in bpy.data.objects:
    if '_d_' in o.name and o.parent: heads.setdefault(o.parent.name,[]).append(o)
def kind_of(c): return c.active_material.name.split('_h_')[0]
for n,(a0,b0) in SH.items():
    if only and n not in only: continue
    cam=bpy.data.objects['cam_'+n]; pre=n+'_'
    hs={k:v for k,v in heads.items() if k.startswith(pre)}
    for f in range(a0,b0+1):
        sc.frame_set(f); bx=[]
        for hn,cards in hs.items():
            vis=[c for c in cards if not c.hide_render]
            if not vis: continue
            c=vis[0]; pt,pb=X.pads(CI[kind_of(c)]); M=c.matrix_world; bb=[Vector(v) for v in c.bound_box]
            xs_=[v.x for v in bb]; ys_=[v.y for v in bb]; zs_=[v.z for v in bb]
            w=max(xs_)-min(xs_); hgt=max(max(ys_)-min(ys_),max(zs_)-min(zs_)); up=2 if (max(zs_)-min(zs_))>=(max(ys_)-min(ys_)) else 1
            cen=Vector(((min(xs_)+max(xs_))/2,(min(ys_)+max(ys_))/2,(min(zs_)+max(zs_))/2)); cen[up]-=hgt*(pt-pb)/(2*(1024+pt+pb))
            r=w*0.5*800/1024; pts=[]
            for dx,dz in ((-r,-r),(r,-r),(r,r),(-r,r)):
                v=cen.copy(); v.x+=dx; v[up]+=dz; pts.append(w2c(sc,cam,M@v))
            if any(p.z<=0 for p in pts): continue
            xs=[p.x for p in pts]; ys=[1-p.y for p in pts]
            if max(xs)<0 or min(xs)>1 or max(ys)<0 or min(ys)>1: continue
            b=[round(min(xs),4),round(min(ys),4),round(max(xs),4),round(max(ys),4)]; bx.append(b)
            HW.setdefault((n,hn),[]).append(b[2]-b[0])
            if f>a0+3 and f<b0-3 and (b[0]<-0.01 or b[2]>1.01 or b[1]<-0.01 or b[3]>1.01): CUT.setdefault((n,hn),[]).append(f)
            if b[0]<0.63 and b[2]>0.37 and b[3]>0.665 and b[1]<0.80: CLASH.setdefault((n,hn),[]).append(f)
        R[f]=R.get(f,[])+bx
json.dump(R,open(out,'w')); print('FACEBOX_OK',len(R))
for (n,h),fs in sorted(CUT.items()): print('FACECUT',n,h,len(fs),fs[0],fs[-1])
for (n,h),fs in sorted(CLASH.items()): print('CAPCLASH',n,h,len(fs),fs[0],fs[-1])
for (n,h),ws in sorted(HW.items()): print('HEADW',n,h,'min',round(min(ws)*100,1),'max',round(max(ws)*100,1),'%W')
