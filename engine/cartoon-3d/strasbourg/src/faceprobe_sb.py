# every character root in its shot must show exactly one face disc (_d_*) on every probed frame (eye pass r1: S21 kid headless 1824-1866)
import bpy, json
sc=bpy.context.scene; SH=json.loads(sc['shots']); bad={}
for n,(a,b) in SH.items():
    col=bpy.data.collections.get('CHR_'+n)
    if not col: continue
    roots=[o for o in col.all_objects if o.type=='EMPTY' and o.name+'_hp' in bpy.data.objects]
    for f in range(a,b+1,3):
        sc.frame_set(f)
        for r in roots:
            if r.hide_render: continue
            if not any(not c.hide_render for c in r.children_recursive if c.type=='MESH' and ('_body' in c.name)): continue
            k=sum(1 for c in r.children_recursive if c.type=='MESH' and '_d_' in c.name and not c.hide_render)
            if k!=1: bad.setdefault((r.name,k),[]).append(f)
for (r,k),fs in sorted(bad.items()): print('FACEPROBE',r,'faces',k,'frames',fs[0],'-',fs[-1],'n',len(fs))
print('FACEPROBE_FAULTS',len(bad))
