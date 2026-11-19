import bpy,sys,json
out=sys.argv[sys.argv.index('--')+1]
sc=bpy.context.scene; D={}
for f in (100,700,1300):
    sc.frame_set(f)
    for o in sc.objects: D[f'{o.name}@{f}']=[round(x,4) for x in list(o.matrix_world.translation)+list(o.dimensions)]+[o.hide_render]
json.dump(D,open(out,'w'))
