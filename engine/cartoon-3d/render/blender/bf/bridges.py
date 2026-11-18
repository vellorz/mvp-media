# Engineer dissolve bridges (rule K6): same shape at the same screen spot (+-5 %) across a dissolve.
# Moves only camera TARGETS on the listed side, with keys inside the overlap (plus optional hold keys). Saves bf.blend in place.
import bpy, json, numpy as np
from bpy_extras.object_utils import world_to_camera_view as w2c
from mathutils import Vector
sc=bpy.context.scene
SH={'S01':(0,170),'S02':(163,297),'S03':(292,432),'S04':(426,528),'S05':(520,652),'S06':(643,781),'S07':(775,866),'S08':(867,938),'S09':(931,1013),'S10':(1008,1057),'S11':(1051,1125),'S12':(1114,1218),'S13':(1210,1359),'S14':(1352,1487),'S15':(1481,1565),'S16':(1556,1752)}
def ob(n):
    c=[o for o in bpy.data.objects if o.name.startswith(n+'_d_')]
    return sorted(c,key=lambda o:o.name)[0] if c else bpy.data.objects[n]
def scr(shot,name,f):
    sc.frame_set(f); cam=bpy.data.objects['cam_'+shot]; o=ob(name)
    P=[w2c(sc,cam,o.matrix_world@Vector(c)) for c in o.bound_box]; xs=[p.x for p in P]; ys=[p.y for p in P]
    return np.array([(min(xs)+max(xs))/2,(min(ys)+max(ys))/2]),max(xs)-min(xs)
def tgt_at(shot,f):
    sc.frame_set(f); return bpy.data.objects['tgt_'+shot].location.copy()
def setkey(shot,f,v):
    t=bpy.data.objects['tgt_'+shot]; t.location=v; t.keyframe_insert('location',frame=f)
def solve(shot,name,goal,keys,frames_meas,holds=()):
    """shift target keys at `keys` by one common offset so `name` sits at `goal` (avg over frames_meas)"""
    for h in holds: setkey(shot,h,tgt_at(shot,h))
    base={k:tgt_at(shot,k) for k in keys}; off=Vector((0,0,0))
    cam=bpy.data.objects['cam_'+shot]
    def meas(o):
        for k in keys: setkey(shot,k,base[k]+o)
        return np.mean([scr(shot,name,f)[0] for f in frames_meas],0)
    for it in range(8):
        p=meas(off); e=goal-p
        if np.abs(e).max()<0.004: break
        sc.frame_set(keys[0]); M=cam.matrix_world.to_3x3(); r,u=M.col[0].normalized(),M.col[1].normalized()
        d=(base[keys[0]]-cam.matrix_world.translation).length; eps=0.01*d
        J=np.stack([(meas(off+r*eps)-p)/eps,(meas(off+u*eps)-p)/eps],1)
        s=np.linalg.lstsq(J,e,rcond=None)[0]; off=off+r*float(s[0])+u*float(s[1])
    meas(off); return off
# (join, side to move, A object, B object, goal for A side or None)
# S12 opens wider (orbit radius 7 -> 3.2 by f1153) so the exec's head matches the newsstand heads in size
import math
cS12=bpy.data.objects['cam_S12']; fcs=cS12.animation_data.action.fcurves
for i,f in enumerate(range(1114,1219,13)):
    R_={1114:5.6,1127:4.6,1140:3.8}.get(f,3.2); a_=math.radians(-38+i*9); FX=1500
    cS12.location=(FX+R_*math.sin(a_),1.5-R_*math.cos(a_),1.55+0.05*i+(0.25 if R_>3.2 else 0)); cS12.keyframe_insert('location',frame=f)
# S16 opens close on a crowd face (same size as the old cop's head) and pulls back to the crowd by f1620
cS16=bpy.data.objects['cam_S16']; sc.frame_set(1556); hw=ob('S16_x3_granny').matrix_world.translation.copy()
for f,d in ((1556,1.9),(1565,2.15)):
    cS16.location=hw+Vector((0.15,-d,0.05)); cS16.keyframe_insert('location',frame=f)
SPEC=[('S01','S02','B','podium','podium',None),
      ('S04','S05','AB','S04_x1_tourist','S05_sarge',(0.70,0.52)),
      ('S06','S07','AB','S06_owner','S07_owner',(0.30,0.46)),
      ('S08','S09','AB','S08_cop','S09_cop',(0.66,0.50)),
      ('S13','S14','-','ledger_cover','ledger_cover',None),
      ('S14','S15','B','S14_exec','S15_oldcop',None),
      ('S15','S16','B','S15_oldcop','S16_x3_granny',None),
      ('S11','S12','B','S11_x2_shopper','S12_exec',None)]
REP=[]
for A,B,side,oa,obn,goalA in SPEC:
    a,b=SH[B][0],SH[A][1]; mid=(a+b)//2; fm=[a,mid,b]
    if 'A' in side and goalA:
        holds=[]
        for h in holds: setkey(A,h,tgt_at(A,h))
        for k in fm: solve(A,oa,np.array(goalA),[k],[k])
    if 'B' in side:
        for k in fm: solve(B,obn,scr(A,oa,k)[0],[k],[k])
    rows=[]
    for f in fm:
        pa,wa=scr(A,oa,f); pb,wb=scr(B,obn,f); rows.append(dict(f=f,A=[round(x,3) for x in pa],B=[round(x,3) for x in pb],dx=round(abs(pa[0]-pb[0]),3),dy=round(abs(pa[1]-pb[1]),3),wA=round(wa,3),wB=round(wb,3)))
    REP.append(dict(join=f'{A}>{B}',A_obj=oa,B_obj=obn,meas=rows,max_err=max(max(r['dx'],r['dy']) for r in rows),bridged=all(max(r['dx'],r['dy'])<=0.05 for r in rows)))
    print('BRIDGE',REP[-1]['join'],REP[-1]['max_err'],REP[-1]['bridged'],flush=True)
# T7: the podium cop in S02 rides above the caption band while the crane starts
for k in (184,190):
    p0,_=scr('S02','S02_cop',k)
    if p0[1]<0.40: solve('S02','S02_cop',np.array([p0[0],0.42]),[k],[k])
for k,gx in ((198,0.30),(206,0.12),(216,-0.2),(228,-0.28),(240,-0.32),(252,-0.35)):
    p0,_=scr('S02','S02_cop',k); solve('S02','S02_cop',np.array([gx,max(0.40,p0[1])]),[k],[k])
json.dump(REP,open('/root/bf/bridge/bridges.json','w'),indent=1)
bpy.ops.wm.save_as_mainfile(filepath='/root/bf/blend/bf.blend'); print('BRIDGES_OK',sum(r['bridged'] for r in REP),'/14')
