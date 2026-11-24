import sys; sys.path.insert(0,'/root/sb/src')
import bpy, lib as L
L.sc=bpy.context.scene
import json
for a_ in json.loads(L.sc.get('air','[]')): L.AIR.add(tuple(a_))   # planned airborne frames (hops) are not FOOT faults
n=L.rigcheck(range(0,2041,6)); print('RIGCHECK_FAULTS',n)
