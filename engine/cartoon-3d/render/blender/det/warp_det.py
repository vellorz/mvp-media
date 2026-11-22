# Detroit retime to the take-3 VO (owner Nov 22: pace 3.4-4.1 w/s): run at the end of scene_det.py, before saving.
# 1) every keyframe in the file moves through the old->new word-onset map (warpmap.json, piecewise linear);
#    CONSTANT keys (visibility, face swaps, card swaps) land on whole frames and never collide;
# 2) shot ranges move with the map, then a few cut points shift so the shot-length shape stays inside Rick's range
#    (over 4 s 20-47 %): the camera keys of a shifted shot are stretched affinely onto its new range (no still frames).
import bpy, json, numpy as np
WM=json.load(open('/root/det/bridge/warpmap.json')); XO=np.array(WM['old']); XN=np.array(WM['new']); NEND=WM['end']
m=lambda f: float(np.interp(f,XO,XN))
def warp_action(act,fn):
    for fc in act.fcurves:
        kps=list(fc.keyframe_points); prev=None
        for kp in kps:
            x=kp.co[0]; nx=fn(x)
            if kp.interpolation=='CONSTANT' or (prev is not None and prev.interpolation=='CONSTANT'):
                nx=float(round(nx))
                if prev is not None and nx<=prev.co[0]: nx=prev.co[0]+1
            for h in (kp.handle_left,kp.handle_right): h[0]=fn(h[0]) if kp.interpolation!='CONSTANT' else nx
            kp.co[0]=nx; prev=kp
        fc.update()
def run(SH):
    seen=set()
    for act in bpy.data.actions:
        if act.name in seen: continue
        seen.add(act.name); warp_action(act,m)
    SH2={n:[int(round(m(a))),int(round(m(b)))] for n,(a,b) in SH.items()}
    names=list(SH)
    for p,q in zip(names,names[1:]):   # N-001: a hard cut stays a hard cut (no 1-frame overlap from rounding)
        if SH[q][0]==SH[p][1]+1: SH2[q][0]=SH2[p][1]+1
    # shape fixes (see FINDINGS): S10 and S16 over 4 s, S15 slides earlier so the S15/S16 dissolve stays 8 f
    ADJ={'S09':(0,-4),'S10':(-4,0),'S14':(0,-5),'S15':(-5,-5),'S16':(-5,0)}
    for n,(da,db) in ADJ.items():
        a0,b0=SH2[n]; a1,b1=a0+da,b0+db
        if (a1,b1)!=(a0,b0):
            f=lambda x,a0=a0,b0=b0,a1=a1,b1=b1: a1+(x-a0)*(b1-a1)/max(1,(b0-a0))
            for ob in (bpy.data.objects['cam_'+n],bpy.data.objects['tgt_'+n]):
                if ob.animation_data and ob.animation_data.action: warp_action(ob.animation_data.action,f)
            cd=bpy.data.objects['cam_'+n].data
            if cd.animation_data and cd.animation_data.action: warp_action(cd.animation_data.action,f)
        SH2[n]=[a1,b1]
    SH2[list(SH2)[-1]][1]=NEND
    sc=bpy.context.scene; sc['shots']=json.dumps(SH2); sc.frame_start=0; sc.frame_end=NEND
    json.dump(SH2,open('/root/det/bridge/shots.json','w'))
    print('WARP_OK end',NEND,SH2)
    return SH2
