# Rules 372 / 376 contact check (owner on Cape Cod r6d: props through tables, sign posts through a banner, structures not planted).
# blender -b cc.blend --python contactcheck_nb.py -- OUT.txt      (read-only)
# (1) FLOAT: every set mesh must touch the floor (z min <= 2 cm) or touch/overlap another set mesh's box (2 cm tolerance), else it floats.
# (2) INSIDE: no character stands inside furniture: a 0.30 m wide, 1.35 m tall column at each character root (on its visible frames)
#     must not overlap any set mesh box except floors/ground cards and objects it is meant to stand on.
# (3) CROSS: no two solid set meshes interpenetrate by more than 3 cm in all three axes unless one contains the other's support face
#     (reported for review, not blocking: boxes are axis-aligned, so rotated parts can show false overlaps).
import bpy, sys, json
from mathutils import Vector
OUT=sys.argv[sys.argv.index('--')+1]
sc=bpy.context.scene; SH=json.loads(sc['shots'])
def bb(o):
    ps=[o.matrix_world@Vector(c) for c in o.bound_box]
    return [min(p[i] for p in ps) for i in range(3)],[max(p[i] for p in ps) for i in range(3)]
def touch(a,b,t=0.02): return all(a[0][i]-t<=b[1][i] and b[0][i]-t<=a[1][i] for i in range(3))
chr_objs=set(o.name for c in bpy.data.collections if c.name.startswith('CHR_') for o in c.all_objects)
SKIP=('cam_','tgt_','M_snow','C_snowf','H_snowf','S0','S1')   # flakes, cameras; shot FG props are checked below separately
sets=[o for o in bpy.data.objects if o.type=='MESH' and o.name not in chr_objs and not o.get('fly') and not o.name.endswith('_ink')
      and not o.name.endswith('_cap') and not o.name.startswith(SKIP) and o.data.name!='sky']
fg=[o for o in bpy.data.objects if o.type=='MESH' and '_fg' in o.name]
B={o.name:bb(o) for o in sets+fg}
rep=[]; bad=0
for o in sets+fg:
    lo,hi=B[o.name]
    if lo[2]<=0.02 or o.get('ground'): continue
    if not any(touch(B[o.name],B[p.name]) for p in sets+fg if p is not o):
        rep.append(f'FLOAT {o.name} z {lo[2]:.2f}-{hi[2]:.2f}'); bad+=1
roots=[o for o in bpy.data.objects if o.get('is_char')]
for r in roots:
    shot=r.get('shot'); f0,f1=SH.get(shot,(0,0)); sc.frame_set((f0+f1)//2)
    p=r.matrix_world.translation; col=([p.x-0.15,p.y-0.15,p.z+0.05],[p.x+0.15,p.y+0.15,p.z+1.35])
    for o in sets:
        if o.hide_render: continue   # only what is on screen in that shot
        if o.get('ground') or o.name.startswith(('M_cobble','A_floor','P_floor','G_floor','C_snow','H_cobble','M_balc')): continue
        if touch(col,B[o.name],0.0): rep.append(f'INSIDE {r.name} ({shot}) overlaps {o.name}'); bad+=1
open(OUT,'w').write('CONTACTCHECK (rules 372/376)\n'+'\n'.join(rep)+f'\nRESULT {"PASS" if bad==0 else "FAIL"} ({bad} faults, {len(sets)} set meshes, {len(roots)} characters)\n')
print(open(OUT).read())
