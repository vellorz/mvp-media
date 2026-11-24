# Camera checks: moving share (>=85 % of frames, rule 318 drift counts), joins (rule 306: no push-in on both sides), pitch (rule 310: <=12 deg up), speed spikes.
import bpy, json, numpy as np, math
sc=bpy.context.scene; SH=json.loads(sc['shots']); K=list(SH)
res={}; mov=0; tot=0; T={}
for n,(a,b) in SH.items():
    cam=bpy.data.objects['cam_'+n]; tg=bpy.data.objects['tgt_'+n] if 'tgt_'+n in bpy.data.objects else None
    D=[];P=[];dist=[]
    for f in range(a,b+1):
        sc.frame_set(f); M=cam.matrix_world; d=-np.array(M.to_3x3().col[2]); D.append(d); P.append(np.array(M.translation))
    D=np.array(D);P=np.array(P)
    ang=np.degrees(np.arccos(np.clip((D[1:]*D[:-1]).sum(1),-1,1))); sp=np.linalg.norm(P[1:]-P[:-1],axis=1)
    moving=(ang>0.01)|(sp>0.0015)
    pitch=np.degrees(np.arcsin(np.clip(D[:,2],-1,1)))
    # push measure: forward component of camera motion (m/f), first/last 8 frames
    fw=((P[1:]-P[:-1])*D[1:]).sum(1)
    T[n]=dict(head=float(fw[:8].mean()),tail=float(fw[-8:].mean()),lens=cam.data.lens)
    res[n]=dict(moving=round(float(moving.mean())*100,1),pitch_max_up=round(float(pitch.max()),1),ang_med=round(float(np.median(ang)),3),ang_max=round(float(ang.max()),2),push_in=round(T[n]['head'],4),push_out=round(T[n]['tail'],4))
    mov+=int(moving.sum()); tot+=len(moving)
    print('CAM',n,res[n],flush=True)
fails=[]
for A,B in zip(K,K[1:]):
    pa=T[A]['tail']>0.004; pb=T[B]['head']>0.004
    if pa and pb: fails.append((A,B,round(T[A]['tail'],4),round(T[B]['head'],4)))
print('MOVING_SHARE',round(100*mov/tot,1))
print('PITCH_UP_FAILS',[n for n in res if res[n]['pitch_max_up']>12])
print('JOIN_306_DOUBLE_PUSH',fails)
json.dump(dict(shots=res,moving_share=round(100*mov/tot,1),double_push=fails),open('/root/nb/camcheck.json','w'),indent=1)
