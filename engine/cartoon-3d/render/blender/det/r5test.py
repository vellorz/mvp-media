# Round 5 Blender test (353a/354a): one stepped turn per character + gestures, plain set. blender -b --python r5test.py -- OUTDIR [pct]
# Needs /root/det/src/cast.json = r5demo.json and textures from cast.py.
import sys, os, math
sys.path.insert(0, '/root/det/src')
import bpy
import lib as L
from lib import plane, flat, lin, cam, char, face, finish, kloc, turn, look, gesture
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
OUT = a[0] if a else '/root/det/out/r5test'; PCT = int(a[1]) if len(a) > 1 else 50
END = 100; sc = L.init(END)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (*lin((206, 196, 214)), 1); w.node_tree.nodes['Background'].inputs[1].default_value = 1.0
fl = plane('floor', (0, 0, 0), 12, 12, flat('floorm', lin((150, 128, 104)), 0.8), horiz=True)
bk = plane('back', (0, 2.2, 1.6), 12, 4, flat('backm', lin((120, 150, 170)), 0.9))
sd = bpy.data.lights.new('sun', 'SUN'); sd.energy = 3.0; so = bpy.data.objects.new('sun', sd); sc.collection.objects.link(so); so.rotation_euler = (math.radians(50), 0, math.radians(30))
co, tg = cam('T', 40, 11); kloc(co, 0, (0, -2.7, 1.05)); kloc(tg, 0, (0, 0, 1.0)); sc.camera = co
man = char('man', 'r5man', 'T', (-0.48, 0, 0), (0, END), face0='smug@R3')
wom = char('wom', 'r5woman', 'T', (0.5, 0.15, 0), (0, END), face0='worried@L2')
# man: strong 3/4 right -> front in steps (353a b), raising his right forearm on the same beat (353a d)
e = turn(man, 18, 'smug', 3, 0, tilt=6); gesture(man, 1, 18, 'raise', inb=True, settle=1)
look(man, 50, 'grin', 0); gesture(man, 1, 52, 'hang')
turn(man, 62, 'grin', 0, -2); gesture(man, -1, 62, 'point_out', inb=False, anticip=2)
# woman: left 3/4 -> right 3/4 through a front frame, both arms to a shrug on the same frame
turn(wom, 24, 'worried', -2, 2); gesture(wom, -1, 24, 'shrug'); gesture(wom, 1, 24, 'shrug')
gesture(wom, -1, 58, 'hang'); look(wom, 60, 'smile', 2); gesture(wom, 1, 60, 'akimbo', settle=2)
for ch in (man, wom): finish(ch)
L.render_setup(PCT, 8)
sc.render.filepath = OUT + '/f_'; os.makedirs(OUT, exist_ok=True)
fr = [int(x) for x in a[2].split(',')] if len(a) > 2 else list(range(0, END + 1))
for f in fr:
    sc.frame_set(f); sc.render.filepath = f'{OUT}/f_{f:03d}.png'; bpy.ops.render.render(write_still=True); print('FRAME', f, flush=True)
