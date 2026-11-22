import bpy,sys
from mathutils import Vector
a=sys.argv[sys.argv.index('--')+1:]; shot=a[0]; f=int(a[1]); pts=[(float(p.split(',')[0]),float(p.split(',')[1])) for p in a[2:]]
sc=bpy.context.scene; sc.frame_set(f); cam=bpy.data.objects['cam_'+shot]; sc.camera=cam
# hide other shots' CHR collections
own=set(o.name for o in bpy.data.collections['CHR_'+shot].all_objects)
other=set(o.name for c in bpy.data.collections if c.name.startswith('CHR_') for o in c.all_objects)-own
dg=bpy.context.evaluated_depsgraph_get()
fr=[cam.matrix_world@v for v in cam.data.view_frame(scene=sc)]  # tr, br, bl, tl
org=cam.matrix_world.translation
for (u,v) in pts:
    top=fr[3].lerp(fr[0],u); bot=fr[2].lerp(fr[1],u); p=bot.lerp(top,v)
    hits=[];o_=org.copy(); d=(p-org).normalized()
    for k in range(40):
        ok,loc,n,i,ob,m=sc.ray_cast(dg,o_,d)
        if not ok: break
        o_=loc+d*0.01
        if ob.name in other or ob.hide_render: continue
        hits.append((ob.name,round((loc-org).length,2)))
    print('PICK',u,v,hits)
