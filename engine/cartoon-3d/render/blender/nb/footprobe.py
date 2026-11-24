# Feet on the ground (rules 142/158 adapted for terrain): every character root vs the set surface under it, every 4th frame.
# Ray cast straight down from 1.5 m above the root, ignoring cast and shot-only props of other shots. Flags |gap| > 0.05 m (sinking < 0, floating > 0).
import bpy, json
from mathutils import Vector
sc=bpy.context.scene; SH=json.loads(sc['shots'])
chr_names=set(o.name for c in bpy.data.collections if c.name.startswith('CHR_') for o in c.all_objects)
bad=0; n=0
for s,(a,b) in SH.items():
    C=bpy.data.collections['CHR_'+s]
    roots=[o for o in C.objects if o.type=='EMPTY' and any(ch.name.endswith('_hp') for ch in o.children)]
    for f in range(a,b+1,4):
        sc.frame_set(f); dg=bpy.context.evaluated_depsgraph_get()
        for r in roots:
            p=r.matrix_world.translation; o_=p+Vector((0,0,1.5)); gap=None
            for k in range(30):
                ok,loc,nrm,i,ob,m=sc.ray_cast(dg,o_,Vector((0,0,-1)))
                if not ok: break
                o_=loc+Vector((0,0,-0.001))
                if ob.name in chr_names or ob.hide_render or ob.name.endswith('_ink') or ob.get('noink') and ob.data and len(ob.data.vertices)<=4: continue
                gap=p.z-loc.z; break
            n+=1
            if gap is None or abs(gap)>0.05: bad+=1; print('FOOT',s,f,r.name,'gap',None if gap is None else round(gap,3),ob.name if gap is not None else '-')
print('FOOTPROBE',bad,'of',n)
