# rule 336(b): on-screen body proportions in head widths, per full-body character at the middle frame of its shot range (camera projection)
import bpy, sys, json, os
import numpy as np
sys.path.insert(0,'/root/dc/src')
import expressions as X
from bpy_extras.object_utils import world_to_camera_view as w2c
from mathutils import Vector
sc=bpy.context.scene; F=json.load(open('/root/dc/bridge/faces.json')); C=json.load(open('/root/dc/src/cast.json'))
RX,RY=sc.render.resolution_x,sc.render.resolution_y; H=0.43; rows={}
def texrows(k):
    if k in rows: return rows[k]
    p=f'/root/dc/tex/{k}_body_noskirt.png'; p=p if os.path.exists(p) else f'/root/dc/tex/{k}_body.png'
    im=bpy.data.images.load(p); w,h=im.size; A=np.array(im.pixels[:]).reshape(h,w,4)[::-1,:,3]
    r=np.nonzero(A.max(1)>0.5)[0]; wid=(A>0.5).sum(1); cr=max(x for x in r if wid[x]>0.22*w); rows[k]=(cr,r[-1],h,os.path.exists(f'/root/dc/tex/{k}_body_noskirt.png')); return rows[k]
out=[]; T=[];Lg=[]
for f in F:
    inst,k,shot=f['inst'],f['kind'],f['shot']; fr=(f['rng'][0]+f['rng'][1])//2; sc.frame_set(fr)
    cam=bpy.data.objects.get('cam_'+shot); b=bpy.data.objects.get(inst+'_body'); root=bpy.data.objects.get(inst)
    if not (cam and b and root): continue
    fc=[o for o in bpy.data.objects if o.name.startswith(inst+'_d_')]
    if not fc: continue
    s=root.matrix_world.to_scale()[0]; pt,pb=X.pads(C[k]); hc=max(o.matrix_world.translation.z for o in fc)-s*H*1024/800*(pt-pb)/2048
    hx=fc[0].matrix_world.translation
    cr,ft,h,dress=texrows(k); bh=b.dimensions.z*s if b.dimensions.z>0 else 1.0; z0=b.matrix_world.translation.z-bh/2
    zr=lambda r: z0+bh*(1-r/h)
    def P(z,dx=0): v=w2c(sc,cam,Vector((hx.x+dx,hx.y,z))); return v
    ht,hb,fe,cz=P(hc+s*H/2),P(hc-s*H/2),P(zr(ft)),P(zr(cr))
    # head width on screen: project left/right of the head centre along the camera's x axis
    ax=cam.matrix_world.to_3x3()@Vector((1,0,0)); l=w2c(sc,cam,Vector((hx.x,hx.y,hc))-ax*s*H/2); r_=w2c(sc,cam,Vector((hx.x,hx.y,hc))+ax*s*H/2)
    hw=abs(r_.x-l.x)*RX
    if hw<8 or not (0<=fe.y<=1 and 0<=ht.y<=1 and 0<=hx.x or True): pass
    if not (0<=fe.y<=1 and 0<=ht.y<=1 and 0<=l.x<=1 and 0<=r_.x<=1 and fe.z>0): continue
    tor=(hb.y-cz.y)*RY/hw; leg=(cz.y-fe.y)*RY/hw
    out.append(f'{shot} {inst:12s} f{fr} torso {tor:.2f} legs {leg:.2f} H{" (dress: legs exempt)" if dress else ""}'); T.append(tor)
    if not dress: Lg.append(leg)
print('\n'.join(out))
print('MEDIAN torso %.2f (>=0.90) legs %.2f (>=1.15) n=%d/%d'%(np.median(T),np.median(Lg),len(T),len(Lg)))
print('RESULT_336B', 'PASS' if np.median(T)>=0.90 and np.median(Lg)>=1.15 else 'FAIL')
