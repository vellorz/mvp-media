# Round 6 Blender test (coordinated combos, lib.combo): blender -b --python m6test.py -- OUTDIR [pct] [frames]
# Needs /root/det/src/cast.json = m6demo.json (+ "combos": true) and textures from cast.py (incl. btop/blegs and pose cards).
import sys, os, math
sys.path.insert(0, '/root/det/src')
import bpy
import lib as L
from lib import plane, flat, lin, cam, char, face, finish, kloc, look, combo
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = a[0] if a else '/root/det/out/m6test'; PCT = int(a[1]) if len(a) > 1 else 50
END = 120; sc = L.init(END)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (*lin((206, 196, 214)), 1); w.node_tree.nodes['Background'].inputs[1].default_value = 1.0
fl = plane('floor', (0, 0, 0), 12, 12, flat('floorm', lin((150, 128, 104)), 0.8), horiz=True)
bk = plane('back', (0, 2.2, 1.6), 12, 4, flat('backm', lin((120, 150, 170)), 0.9))
sd = bpy.data.lights.new('sun', 'SUN'); sd.energy = 3.0; so = bpy.data.objects.new('sun', sd); sc.collection.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(30))
co, tg = cam('T', 40, 11); kloc(co, 0, (0, -2.7, 1.05)); kloc(tg, 0, (0, 0, 1.0)); sc.camera = co
man = char('man', 'r5man', 'T', (-0.5, 0, 0), (0, END), face0='smug@F')
wom = char('wom', 'r5woman', 'T', (0.5, 0.15, 0), (0, END), face0='smile@F')
# man: turn toward the woman and point (head + torso same frame, arm 3 f later), talk tilt, then startle and dash (legs stride)
combo(man, 10, 'turn_and_point', side=1, face='grin')
combo(man, 44, 'tilt_talk', side=1, face='smug')
combo(man, 84, 'startle_dash', side=-1, face='surprise')
# woman: reach toward him (lean 18 over planted legs), big laugh leaning back, cheer
combo(wom, 14, 'lean_reach', side=-1, face='smile')
combo(wom, 46, 'laugh_lean_back', side=-1, face='laugh')
combo(wom, 86, 'victory_up', side=1, face='happy')
for ch in (man, wom): finish(ch)
L.render_setup(PCT, 8)
os.makedirs(OUT, exist_ok=True)
fr = [int(x) for x in a[2].split(',')] if len(a) > 2 else list(range(0, END + 1))
for f in fr:
    sc.frame_set(f); sc.render.filepath = f'{OUT}/f_{f:03d}.png'; bpy.ops.render.render(write_still=True); print('FRAME', f, flush=True)
print('ALL_DONE', flush=True)
