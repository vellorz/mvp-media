# per shot: camera angular speed (deg/frame of view direction) and position speed; flag frames > 2.5x the shot median and > 0.8 deg/f
import bpy, json, numpy as np
sc=bpy.context.scene; SH=json.loads(sc['shots'])
out={}
for n,(a,b) in SH.items():
    cam=bpy.data.objects['cam_'+n]; D=[];P=[]
    for f in range(a,b+1):
        sc.frame_set(f); M=cam.matrix_world; D.append(np.array(M.to_3x3().col[2])); P.append(np.array(M.translation))
    D=np.array(D); P=np.array(P)
    ang=np.degrees(np.arccos(np.clip((D[1:]*D[:-1]).sum(1),-1,1))); sp=np.linalg.norm(P[1:]-P[:-1],axis=1)
    acc=np.abs(np.diff(ang)); med=np.median(ang)+1e-3
    bad=[int(a+1+i) for i in range(len(ang)) if ang[i]>0.8 and ang[i]>2.5*med]
    jerk=[int(a+2+i) for i in range(len(acc)) if acc[i]>0.6]
    out[n]=dict(med=round(float(med),2),max=round(float(ang.max()),2),at=int(a+1+ang.argmax()),bad=bad[:12],jerk=jerk[:12])
    print('CAM',n,out[n],flush=True)
