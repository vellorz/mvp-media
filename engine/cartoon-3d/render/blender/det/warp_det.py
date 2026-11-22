# Detroit retime to the faster VO (owner Nov 22: pace 3.4-4.1 w/s): run at the end of scene_det.py, before saving.
# 1) shot ranges move with the old->new word-onset map (warpmap.json, piecewise linear), hard cuts stay hard cuts, then a few
#    cut points shift (ADJ) so the shot-length shape stays inside Rick's range;
# 2) every keyframe moves through the map. CONSTANT keys (visibility, face swaps, card swaps) land on whole frames and never collide.
#    Round 2 (shots verifier C8/F3/N-001: pops at f0, 353, 468, 665-668):
#    - frames outside the map (the vis() key at -1) keep their offset instead of clamping onto frame 0 (that hid the S01 family at f0);
#    - a hide_render key that sat exactly on an old shot start (a) or old shot end+1 (b+1) snaps to the NEW shot start / end+1,
#      so a cast never misses the first or last frames of its shot after rounding, hard-cut enforcement or ADJ;
#    - inside an ADJ-shifted shot every key of the shot's own objects is stretched affinely onto the new range (not only the camera).
import bpy, json, numpy as np
WM=json.load(open('/root/det/bridge/warpmap.json')); XO=np.array(WM['old'],float); XN=np.array(WM['new'],float); NEND=WM['end']
def m(f):
    if f<XO[0]: return float(XN[0]+(f-XO[0]))
    if f>XO[-1]: return float(XN[-1]+(f-XO[-1]))
    return float(np.interp(f,XO,XN))
ADJ={'S03':(0,8),'S04':(8,0),'S09':(0,-14),'S10':(-14,0),'S15':(0,-16),'S16':(-16,0)}   # round 2: 5 of 21 shots over 4 s by join midpoints (S03 4.3, S10 4.3, S11, S16 4.2, S18), Rick 20-47 %
def new_shots(SH):
    SH2={n:[int(round(m(a))),int(round(m(b)))] for n,(a,b) in SH.items()}
    names=list(SH)
    for p,q in zip(names,names[1:]):   # N-001: a hard cut stays a hard cut (no 1-frame overlap from rounding)
        if SH[q][0]==SH[p][1]+1: SH2[q][0]=SH2[p][1]+1
    for n,(da,db) in ADJ.items(): SH2[n]=[SH2[n][0]+da,SH2[n][1]+db]
    for p,q in zip(names,names[1:]):   # after ADJ, hard cuts again exact
        if SH[q][0]==SH[p][1]+1: SH2[q][0]=SH2[p][1]+1
    SH2[names[-1]][1]=NEND
    return SH2
def warp_action(act,fn,snap=None):
    for fc in act.fcurves:
        hr=fc.data_path=='hide_render'; prev=None
        for kp in list(fc.keyframe_points):
            x=kp.co[0]; nx=fn(x)
            if hr and snap and int(round(x)) in snap: nx=float(snap[int(round(x))])
            if kp.interpolation=='CONSTANT' or hr or (prev is not None and prev.interpolation=='CONSTANT'):
                nx=float(round(nx))
                if prev is not None and nx<=prev.co[0]: nx=prev.co[0]+1
            for h in (kp.handle_left,kp.handle_right): h[0]=fn(h[0]) if kp.interpolation!='CONSTANT' else nx
            kp.co[0]=nx; prev=kp
        fc.update()
def shot_of(ob):
    for c in ob.users_collection:
        if c.name.startswith('CHR_'): return c.name[4:]
    if ob.name.startswith(('cam_','tgt_')): return ob.name[4:]
    return None
def run(SH):
    SH2=new_shots(SH)
    snap={}
    for n,(a,b) in SH.items(): snap[int(a)]=SH2[n][0]; snap[int(b)+1]=SH2[n][1]+1
    base={n:[int(round(m(a))),int(round(m(b)))] for n,(a,b) in SH.items()}
    def fn_for(n):
        if n in ADJ:
            a0,b0=base[n]; a1,b1=SH2[n]
            return lambda x,a0=a0,b0=b0,a1=a1,b1=b1: a1+(m(x)-a0)*(b1-a1)/max(1,(b0-a0))
        return m
    done=set()
    for ob in bpy.data.objects:
        for ad in (ob.animation_data, getattr(ob.data,'animation_data',None) if ob.data else None):
            if ad and ad.action and ad.action.name not in done:
                done.add(ad.action.name); warp_action(ad.action,fn_for(shot_of(ob)),snap)
    for act in bpy.data.actions:   # anything not reached through an object (materials, node trees)
        if act.name not in done: done.add(act.name); warp_action(act,m,snap)
    sc=bpy.context.scene; sc['shots']=json.dumps(SH2); sc.frame_start=0; sc.frame_end=NEND
    json.dump(SH2,open('/root/det/bridge/shots.json','w'))
    print('WARP_OK end',NEND,SH2)
    return SH2
