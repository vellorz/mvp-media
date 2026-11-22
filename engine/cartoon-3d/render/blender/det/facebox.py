# r3 (text verifier T7 round 2: pixel face detection missed lamp-lit and shaded faces in S06, S09, S11, S14, S17, S18):
# exact per-frame face boxes from the blend itself. For every visible face card, its disc (800/1024 of the card) is projected
# through the shot camera; boxes are written as fractions of the frame (x0, y0 from the TOP, x1, y1).
# blender -b det.blend --python facebox.py -- OUT.json   (r4: also prints FACECUT shot head nframes first last for faces partly out of frame)
import bpy, json, sys
from bpy_extras.object_utils import world_to_camera_view as w2c
from mathutils import Vector
out=sys.argv[sys.argv.index('--')+1]
sc=bpy.context.scene; SH=json.loads(sc['shots']); R={}; CUT={}
heads={}
for o in bpy.data.objects:
    if '_d_' in o.name and o.parent: heads.setdefault(o.parent.name,[]).append(o)
for n,(a,b) in SH.items():
    cam=bpy.data.objects['cam_'+n]; pre=n+'_'
    hs=[v for k,v in heads.items() if k.startswith(pre)]
    for f in range(a,b+1):
        sc.frame_set(f); bx=[]
        for cards in hs:
            vis=[c for c in cards if not c.hide_render]
            if not vis: continue
            c=vis[0]; M=c.matrix_world; bb=[Vector(v) for v in c.bound_box]; cen=sum(bb,Vector())/8; k=800/1024
            pts=[w2c(sc,cam,M@(cen+(v-cen)*k)) for v in bb]
            if any(p.z<=0 for p in pts): continue
            xs=[p.x for p in pts]; ys=[1-p.y for p in pts]
            if max(xs)<0 or min(xs)>1 or max(ys)<0 or min(ys)>1: continue
            bx.append([round(min(xs),4),round(min(ys),4),round(max(xs),4),round(max(ys),4)])
            if f>a+3 and f<b-3 and (min(xs)<-0.01 or max(xs)>1.01 or min(ys)<0): CUT.setdefault((n,c.parent.name),[]).append(f)
        R[f]=R.get(f,[])+bx
json.dump(R,open(out,'w')); print('FACEBOX_OK',len(R))
for (n,h),fs in sorted(CUT.items()): print('FACECUT',n,h,len(fs),fs[0],fs[-1])
