# Round 6 Blender test (coordinated combos, lib.combo): blender -b --python m6test.py -- OUTDIR [pct] [frames]
# Needs /root/det/src/cast.json = m6demo.json (+ "combos": true) and textures from cast.py (incl. btop/blegs and pose cards).
import sys, os, math
sys.path.insert(0, '/root/det/src')
import bpy
import lib as L
from lib import plane, flat, lin, cam, char, face, finish, kloc, look, combo
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = a[0] if a else '/root/det/out/m7test'; PCT = int(a[1]) if len(a) > 1 else 50
END = 140; sc = L.init(END)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (*lin((206, 196, 214)), 1); w.node_tree.nodes['Background'].inputs[1].default_value = 1.0
fl = plane('floor', (0, 0, 0), 12, 12, flat('floorm', lin((150, 128, 104)), 0.8), horiz=True)
bk = plane('back', (0, 2.2, 1.6), 12, 4, flat('backm', lin((120, 150, 170)), 0.9))
sd = bpy.data.lights.new('sun', 'SUN'); sd.energy = 3.0; so = bpy.data.objects.new('sun', sd); sc.collection.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(30))
co, tg = cam('T', 40, 11); kloc(co, 0, (0, -2.7, 1.05)); kloc(tg, 0, (0, 0, 1.0)); sc.camera = co
man = char('man', 'r5man', 'T', (-0.75, 0, 0), (0, END), face0='neutral@F')
wom = char('wom', 'r5woman', 'T', (0.0, 0.15, 0), (0, END), face0='neutral@F')
hat = char('hat', 'r5hat', 'T', (0.75, 0.05, 0), (0, END), face0='smug@F')
# round 7 (owner review Nov 23): the reworked moves and the new runs
combo(man, 6, 'look_back_shrug', side=1, face='neutral', face2='skeptical')
combo(man, 52, 'clap', side=1, face='happy')
combo(man, 96, 'sprint', side=1, face='determined')
combo(wom, 8, 'startle_recoil', side=1, face='neutral', face2='sigh')
combo(wom, 50, 'cross_arms_huff', side=1, face='annoyed')
combo(wom, 100, 'jog', side=-1, face='determined')
combo(hat, 4, 'double_take', side=-1, face='neutral', face2='surprise')
combo(hat, 54, 'think_chin', side=-1, face='skeptical', face2='open_smile')
combo(hat, 104, 'turn_away_back', side=1, face='smug')
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
