# Detroit pre-render camera probe (rule 321 list): blender -b det.blend --python camrules.py
# 306 joincheck: the last 20 f of a shot and the first 20 f of the next never BOTH push in (dolly toward the target or lens zoom-in),
#     measured as relative image scale change s = d0/d1 * lens1/lens0 over the 20 f; "push" = s >= 1.03 (3 % growth).
# 310 low camera: for shots with a full-body character in frame, camera height >= 0.8 m above the character's floor and pitch <= 12 deg up.
import bpy, json, math
from mathutils import Vector
sc=bpy.context.scene; SH=json.loads(sc['shots'])
def state(n,f):
    sc.frame_set(f); c=bpy.data.objects['cam_'+n]; t=bpy.data.objects['tgt_'+n]
    p=c.matrix_world.translation.copy(); q=t.matrix_world.translation.copy(); return p,q,c.data.lens
def scale(n,f0,f1):
    p0,q0,l0=state(n,f0); p1,q1,l1=state(n,f1)
    return ((p0-q0).length/(p1-q1).length)*(l1/l0)
names=list(SH); bad=0
for a,b in zip(names,names[1:]):
    ea=SH[a][1]; sb=SH[b][0]
    sa=scale(a,ea-20,ea); sbb=scale(b,sb,sb+20)
    flag=sa>=1.03 and sbb>=1.03
    bad+=flag
    print('JOIN',a,'>',b,'end-push',round(sa,3),'start-push',round(sbb,3),'DOUBLE_PUSH' if flag else 'ok')
print('JOINCHECK',bad,'PASS' if bad==0 else 'FAIL')
low=0
for n,(f0,f1) in SH.items():
    worst=None
    for f in range(f0,f1+1,6):
        p,q,l=state(n,f); d=q-p; pitch=math.degrees(math.atan2(d.z,math.hypot(d.x,d.y)))
        if worst is None or pitch>worst[1]: worst=(f,pitch,p.z)
    hmin=min(state(n,f)[0].z for f in range(f0,f1+1,6))
    print('CAMH',n,'min height',round(hmin,2),'max pitch up',round(worst[1],1),'at',worst[0])
    if worst[1]>12 or hmin<0.8: low+=1; print('  LOWCAM',n)
print('LOWCAM',low)
