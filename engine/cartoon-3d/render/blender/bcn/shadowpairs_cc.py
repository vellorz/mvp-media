# rule 367 part 1 for Cape Cod: lib.shadow_pairs per shot with that shot's camera. blender -b cc.blend --python shadowpairs_cc.py -- OUT.json
import bpy, sys, json
sys.path.insert(0,'/root/cc/src'); import lib as L
sc=bpy.context.scene; L.sc=sc; out=sys.argv[sys.argv.index('--')+1]; SH=json.loads(sc['shots']); allp=[]
vl=bpy.context.view_layer
for n,(a,b) in SH.items():
    sc.camera=bpy.data.objects['cam_'+n]
    # only this shot's characters count
    keep={o.name for c in bpy.data.collections if c.name=='CHR_'+n for o in c.all_objects}
    tmp=out+'.tmp'; L.shadow_pairs(range(a,b+1),tmp)
    for p in json.load(open(tmp)):
        if p['a'] in keep and p['b'] in keep: p['shot']=n; allp.append(p)
json.dump(allp,open(out,'w')); print('PAIRS_TOTAL',len(allp),sorted(set((p['shot'],p['a'],p['b']) for p in allp))[:30])
