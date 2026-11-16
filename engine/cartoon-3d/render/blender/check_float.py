"""Rule 142 check: no floating parts. Run inside Blender before any 2K render:
  blender -b scene.blend --python check_float.py -- [frame ...]
Every visible mesh must touch (<= TOL m) another visible mesh or the ground (z <= TOL).
Objects that are meant to be airborne carry the custom property fly=1 (birds, clouds, rain,
thrown props mid-air, sky cards). Exits 1 and lists offenders if anything floats."""
import bpy, sys
from mathutils.bvhtree import BVHTree
TOL = 0.02
argv = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
frames = [int(a) for a in argv] or [bpy.context.scene.frame_start]
def root_fly(o):
    while o:
        if o.get('fly'): return True
        o = o.parent
    return False
bad = {}
for f in frames:
    bpy.context.scene.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    objs = [o for o in bpy.context.scene.objects if o.type == 'MESH' and not o.hide_render
            and not o.name.startswith('hull_') and not o.name.endswith('_ink') and not root_fly(o)]
    trees = {}
    for o in objs:
        oe = o.evaluated_get(dg); m = oe.to_mesh()
        if len(m.vertices) == 0: oe.to_mesh_clear(); continue
        vs = [oe.matrix_world @ v.co for v in m.vertices]
        # sample face centres too: a flat card has only 4 corners, its middle may be what touches
        pts = vs + [oe.matrix_world @ p.center for p in m.polygons]
        trees[o.name] = (BVHTree.FromPolygons(vs, [p.vertices[:] for p in m.polygons]), pts)
        oe.to_mesh_clear()
    for n, (t, vs) in trees.items():
        if min(v.z for v in vs) <= TOL: continue
        touching = False
        step = max(1, len(vs)//400)
        for n2, (t2, _) in trees.items():
            if n2 == n: continue
            if t.overlap(t2): touching = True; break
            for v in vs[::step]:
                hit = t2.find_nearest(v, TOL)
                if hit[0] is not None: touching = True; break
            if touching: break
        if not touching: bad.setdefault(n, []).append(f)
for n, fs in sorted(bad.items()): print(f'FLOATING {n} frames {fs[:8]}')
print('CHECK_FLOAT', 'FAIL' if bad else 'PASS', len(bad))
if bad: sys.exit(1)
