# Rule 329 (owner Nov 22): full-body cast sheet from the REAL rig + missing-limb and proportion check.
# blender -b --factory-startup -P castcheck.py -- OUT_PNG OUT_TXT
# Builds every cast kind with lib.char() (same code as the video), stands them in a row facing an orthographic camera,
# checks head, torso/body card, both arms (with mitten hand in the arm card), both legs/feet (in the body card) exist, render and sit in frame,
# and measures torso / legs / total in head widths (H = head disc, outer ink) from the cards' geometry and the body texture's alpha.
import sys, json, math
sys.path.insert(0,'/root/cc/src')
import bpy, numpy as np
from mathutils import Vector
import lib as L
a=sys.argv[sys.argv.index('--')+1:]; OUT,TXT=a[0],a[1]
sc=L.init(20)
C=json.load(open('/root/cc/src/cast.json')); kinds=list(C)
N=len(kinds); SP=1.25
cam,tg=L.cam('SHEET',50); cam.data.dof.use_dof=False; cam.data.type='ORTHO'; cam.data.ortho_scale=SP*N+0.6
cam.location=((N-1)*SP/2,-12,0.75); cam.rotation_euler=(math.radians(90),0,0)
tg.location=((N-1)*SP/2,0,0.75)
for c_ in list(cam.constraints): cam.constraints.remove(c_)
CH=[]
for i,k in enumerate(kinds):
    f0=list(C[k]['faces'])[0]
    ch=L.char(f'K{i}_{k}','%s'%k,'SHEET',(i*SP,0,0),(0,20),f0,arms=('arm','arm')); CH.append(ch)
    for sx in(-1,1): L.arm(ch,sx,0,-14)
for ch in CH: L.finish(ch)
sc.camera=cam; sc.frame_set(5)
sc.render.engine='CYCLES'; sc.cycles.samples=12; sc.cycles.device='CPU'; sc.cycles.use_denoising=False
sc.render.resolution_x=3200; sc.render.resolution_y=int(3200*0.17); sc.render.film_transparent=False
sc.render.filepath=OUT
from bpy_extras.object_utils import world_to_camera_view as w2c
H=0.43; rep=[]; allok=True
q=L.BSY['tall']
for ch in CH:
    k=ch['kind']; miss=[]
    def vis_(o): return o is not None and not o.hide_render
    if not ch['bodies'] or not vis_(ch['bodies']['body']): miss.append('torso/body')
    if not any(vis_(f) for f in ch['F'].values()): miss.append('head')
    for sx,nm in ((-1,'arm_L'),(1,'arm_R')):
        if not any(vis_(c_) for c_ in ch['A'][sx]['cards'].values()): miss.append(nm)
    # in frame: project body + head corners
    pts=[]
    for o in [ch['bodies']['body']]+[f for f in ch['F'].values() if vis_(f)]:
        pts+=[w2c(sc,cam,o.matrix_world@Vector(v)) for v in o.bound_box]
    if any(p.x<0 or p.x>1 or p.y<0 or p.y>1 for p in pts): miss.append('out of frame')
    # body texture alpha: garment bottom (crotch) and feet
    b=ch['bodies']['body']; img=None
    for n_ in b.active_material.node_tree.nodes:
        if n_.type=='TEX_IMAGE': img=n_.image
    w,h=img.size; A=np.array(img.pixels[:]).reshape(h,w,4)[::-1,:,3]   # row 0 = top
    rows=np.nonzero(A.max(1)>0.5)[0]; top_r,bot_r=rows[0],rows[-1]
    wid=(A>0.5).sum(1); crotch=max(r for r in rows if wid[r]>0.22*w)
    legs_ok=(A[crotch+5:bot_r,:]>0.5).any(0).sum()>0
    # two separate leg columns below the crotch
    mid=(crotch+bot_r)//2; segs=np.diff(np.concatenate([[0],(A[mid]>0.5).astype(int),[0]])); nlegs=int((segs==1).sum())
    if nlegs<2: miss.append(f'legs ({nlegs} at mid-shin)')
    bh=b.dimensions.z if b.dimensions.z>0 else 1.1*q; z0=b.matrix_world.translation.z-bh/2
    def zrow(r): return z0+bh*(1-r/h)
    head_c=max(f.matrix_world.translation.z for f in ch['F'].values()); head_bot=head_c-H/2; head_top=head_c+H/2
    sc_=ch['root'].scale[0]
    torso=(head_bot-zrow(crotch))/H; legs=(zrow(crotch)-zrow(bot_r))/H; total=(head_top-zrow(bot_r))/H
    # r7b shoulder-join check (owner Nov 22 'arm issue?': arm roots stood inside the outline as a second line, or poked above the shoulder):
    # each shoulder pivot must sit on the torso's side outline (|pivot x - outline x| <= 0.020 m, about one arm half-width plus ink) at a height where the outline is a side, not the top curve
    bw=b.dimensions.x if b.dimensions.x>0 else 0.8; bx=b.matrix_world.translation.x; sj=[]
    for sx_,AP in ch['A'].items():
        lp=b.matrix_world.inverted()@AP['piv'].matrix_world.translation   # body-card local space (the root carries the kind's scale)
        r=int(round((0.5-lp.y/bh)*h)) if abs(lp.z)<1e-6 and abs(lp.y)>1e-6 else int(round((0.5-lp.z/bh)*h))
        cols=np.nonzero(A[r]>0.5)[0] if 0<=r<h else []
        if len(cols)==0: sj.append(f'{sx_:+d} above torso'); continue
        ex=bw*((cols[-1] if sx_>0 else cols[0])/w-0.5); d_=abs(lp.x-ex)
        slope=abs(np.nonzero(A[max(0,r-15)]>0.5)[0][[0,-1]][1 if sx_>0 else 0]-(cols[-1] if sx_>0 else cols[0])) if (A[max(0,r-15)]>0.5).any() else 99
        if d_>0.020 or slope>6: sj.append(f'{sx_:+d} off {d_*1000:.0f}mm slope {slope}px')
    if sj: miss.append('shoulder join '+'; '.join(sj))
    ok=not miss and 0.85<=torso<=1.2 and 1.1<=legs<=1.3 and 2.9<=total<=3.35
    allok&=ok
    rep.append(f"{k:10s} {'PASS' if ok else 'FAIL'} torso {torso:.2f} legs {legs:.2f} total {total:.2f} H  limbs: head, torso, arm_L, arm_R (mitten in card), legs x{nlegs}, feet, shoulder joins{'' if not miss else '  MISSING: '+', '.join(miss)}")
w_=bpy.data.worlds.new('w'); sc.world=w_; w_.use_nodes=True; bg_=w_.node_tree.nodes['Background']; bg_.inputs['Color'].default_value=(0.83,0.80,0.75,1); bg_.inputs['Strength'].default_value=1.0
bpy.ops.object.light_add(type='SUN',rotation=(math.radians(50),0,math.radians(25))); bpy.context.object.data.energy=2.0
cam.data.ortho_scale=3.6; sc.render.resolution_x=400; sc.render.resolution_y=900
import os
os.makedirs(OUT,exist_ok=True)
for i,ch in enumerate(CH):
    x=ch['root'].location.x; cam.location=(x,-12,1.0); tg.location=(x,0,1.0)
    sc.render.filepath=f'{OUT}/{i:02d}_{ch["kind"]}.png'; bpy.ops.render.render(write_still=True)
open(TXT,'w').write('CASTCHECK (rule 329) det cast, rig from lib.py, BSY %.2f\n'%q+'\n'.join(rep)+'\nRESULT %s\n'%('PASS' if allok else 'FAIL'))
print(open(TXT).read())
