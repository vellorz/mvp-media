"""Rule 143 check: held props never pass through the body. Run before any 2K render:
  blender -b scene.blend --python check_clip.py -- PROP BODY1,BODY2,... START END
PROP = the held prop, or several comma-separated meshes (children are included).
BODY = the character meshes it must never enter (torso, head, legs; leave out the holding hand).
Tests every frame START..END (fast: no rendering). Reports frames where the prop overlaps a body
mesh or comes closer than MIN_GAP. Exits 1 on any hit."""
import bpy, sys
from mathutils.bvhtree import BVHTree
MIN_GAP = 0.01
a = sys.argv[sys.argv.index('--')+1:]
prop, bodies, s, e = a[0], a[1].split(','), int(a[2]), int(a[3])
def tree(o, dg):
    oe = o.evaluated_get(dg); m = oe.to_mesh()
    vs = [oe.matrix_world @ v.co for v in m.vertices]; ps = [p.vertices[:] for p in m.polygons]
    oe.to_mesh_clear(); return BVHTree.FromPolygons(vs, ps), vs
parts = []
for n in prop.split(','):
    P = bpy.data.objects[n]; parts += [P] + [c for c in P.children_recursive if c.type == 'MESH' and not c.name.endswith('_ink')]
hits = []
for f in range(s, e+1):
    bpy.context.scene.frame_set(f); dg = bpy.context.evaluated_depsgraph_get()
    pt = [tree(p, dg) for p in parts if p.type == 'MESH']
    for b in bodies:
        bt, _ = tree(bpy.data.objects[b], dg)
        for t, vs in pt:
            if t.overlap(bt) or any(bt.find_nearest(v, MIN_GAP)[0] is not None for v in vs[::max(1,len(vs)//300)]):
                hits.append((f, b)); break
for f, b in hits: print(f'CLIP frame {f}: {prop} hits {b}')
print('CHECK_CLIP', 'FAIL' if hits else 'PASS', len(hits))
if hits: sys.exit(1)
