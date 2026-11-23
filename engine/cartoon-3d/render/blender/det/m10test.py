# Round 10 Blender test (walk v2 + opposite arm swing: stroll / walk / brisk / toward camera, characters really travel), from the round 6-8 tests (coordinated combos, lib.combo): blender -b --python m6test.py -- OUTDIR [pct] [frames]
# Needs /root/det/src/cast.json = m6demo.json (+ "combos": true) and textures from cast.py (incl. btop/blegs and pose cards).
import sys, os, math
sys.path.insert(0, '/root/det/src')
import bpy
import lib as L
from lib import plane, flat, lin, cam, char, face, finish, kloc, look, combo
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = a[0] if a else '/root/det/out/m10test'; PCT = int(a[1]) if len(a) > 1 else 50
END = 150; sc = L.init(END)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (*lin((206, 196, 214)), 1); w.node_tree.nodes['Background'].inputs[1].default_value = 1.0
fl = plane('floor', (0, 0, 0), 12, 12, flat('floorm', lin((150, 128, 104)), 0.8), horiz=True)
bk = plane('back', (0, 2.2, 1.6), 12, 4, flat('backm', lin((120, 150, 170)), 0.9))
sd = bpy.data.lights.new('sun', 'SUN'); sd.energy = 3.0; so = bpy.data.objects.new('sun', sd); sc.collection.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(30))
co, tg = cam('T', 40, 11); kloc(co, 0, (0, -4.3, 1.15)); kloc(tg, 0, (0, 0, 1.05)); sc.camera = co
man = char('man', 'r5man', 'T', (-1.25, 0, 0), (0, END), face0='neutral@F')
wom = char('wom', 'r5woman', 'T', (0.0, 0.9, 0), (0, END), face0='neutral@F')
hat = char('hat', 'r5hat', 'T', (1.3, 0.3, 0), (0, END), face0='smug@F')
# round 9: walk v2. The combo walks in place; the scene slides the root at the stride speed (stance foot travel / step), so feet do not skate.
SPEED = {'st': 0.096 / 10, 'nm': 0.140 / 8, 'br': 0.186 / 6}   # m per frame = cast.WALK_STYLES stride px * 0.001 m / frames per step
def walk_move(ch, f, name, side, face, axis='x', **k):
    end = combo(ch, f, name, side=side, face=face, **k); st = L.MO.COMBOS[name]['walk_style']
    ev = [e for e in L.MO.COMBOS[name]['events'] if e['ch'] == 'legs']; a, b = f + ev[0]['at'], f + ev[-1]['at']
    r = ch['root']; p0 = tuple(r.location); d = SPEED[st] * (b - a)
    p1 = (p0[0] + side * d, p0[1], p0[2]) if axis == 'x' else (p0[0], p0[1] - d, p0[2])
    kloc(r, a, p0); kloc(r, b, p1)
    for fc in r.animation_data.action.fcurves:
        if fc.data_path == 'location':
            for kp in fc.keyframe_points:
                if kp.co[0] in (a, b): kp.interpolation = 'LINEAR'
    r.location = p1; return end
walk_move(man, 4, 'walk', 1, 'determined')
walk_move(man, 90, 'walk_stroll', -1, 'happy')
walk_move(hat, 10, 'walk_brisk', -1, 'determined')
walk_move(hat, 90, 'walk', 1, 'neutral')
walk_move(wom, 6, 'walk_toward', 1, 'happy', axis='y')
walk_move(wom, 84, 'walk_stroll', 1, 'happy')
for ch in (man, wom, hat): finish(ch)
# rule 354b: automatic rig check (coplanar cards, feet vs floor, shadow cards); stops before rendering when anything fails
if L.rigcheck(range(0, END + 1, 2)) and not os.environ.get('RIGCHECK_ONLY'): raise SystemExit('RIGCHECK failed')
if os.environ.get('RIGCHECK_ONLY'): raise SystemExit(0)
L.render_setup(PCT, 8)
os.makedirs(OUT, exist_ok=True)
fr = [int(x) for x in a[2].split(',')] if len(a) > 2 else list(range(0, END + 1))
for f in fr:
    sc.frame_set(f); sc.render.filepath = f'{OUT}/f_{f:03d}.png'; bpy.ops.render.render(write_still=True); print('FRAME', f, flush=True)
print('ALL_DONE', flush=True)
