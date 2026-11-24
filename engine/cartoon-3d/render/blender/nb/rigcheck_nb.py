# rule 354b gate: L.rigcheck per shot on the built blend (blender -b cc.blend --python rigcheck_cc.py)
import bpy, json, sys
sys.path.insert(0,'/root/nb/src')
import lib as L
L.sc=bpy.context.scene
L.AIR=set(tuple(x) for x in json.loads(bpy.context.scene.get('air','[]')))
SH=json.loads(bpy.context.scene['shots']); tot=0
import os
ONLY=[x for x in os.environ.get('SHOTS','').split(',') if x]
for k,(a,b) in SH.items():
    if ONLY and k not in ONLY: continue
    n=L.rigcheck(range(a,b+1,2)); print('SHOT',k,n); tot+=n
print('RIGCHECK_FAULTS',tot)
