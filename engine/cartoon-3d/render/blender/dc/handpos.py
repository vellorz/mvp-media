# dc14 rule 346 probe: world position of a character's mitten (from the arm card's texture geometry) at given frames.
# blender -b dc.blend --python handpos.py -- INST SX CARDKEY BEND F1 F2 ...
import bpy, sys, math
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]; inst,sx,key,bend=a[0],int(a[1]),a[2],float(a[3]); fr=[int(x) for x in a[4:]]
sc=bpy.context.scene; o=bpy.data.objects[f'{inst}_arm{sx}_{key}']
hx=600+(712-330)*math.sin(math.radians(bend)); hy=330+(712-330)*math.cos(math.radians(bend))
if sx<0: hx=1200-hx
bb=[Vector(v) for v in o.bound_box]; xs=[v.x for v in bb]; ys=[v.y for v in bb]; zs=[v.z for v in bb]
loc=Vector((min(xs)+(max(xs)-min(xs))*hx/1200, (min(ys)+max(ys))/2, max(zs)-(max(zs)-min(zs))*hy/900))
if max(ys)-min(ys)>max(zs)-min(zs): loc=Vector((min(xs)+(max(xs)-min(xs))*hx/1200, max(ys)-(max(ys)-min(ys))*hy/900,(min(zs)+max(zs))/2))
for f in fr:
    sc.frame_set(f); p=o.matrix_world@loc; print('HAND',inst,f,round(p.x,3),round(p.y,3),round(p.z,3))
