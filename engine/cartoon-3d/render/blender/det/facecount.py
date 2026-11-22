# rule 332 probe: distinct faces per video / per character, from the face cards' render visibility in the blend
import bpy, json, collections
sc=bpy.context.scene; SH=json.loads(sc['shots'])
use=collections.defaultdict(collections.Counter)
cards=[o for o in bpy.data.objects if '_d_' in o.name and o.parent]
for o in cards:
    inst=o.parent.name[:-3] if o.parent.name.endswith('_hp') else o.parent.name
    face=o.name.split('_d_',1)[1]
    shot=inst.split('_')[0]
    if shot not in SH: continue
    a,b=SH[shot]; fc=None
    ad=o.animation_data
    if ad and ad.action:
        for c in ad.action.fcurves:
            if c.data_path=='hide_render': fc=c
    n=0
    for f in range(a,b+1):
        hid=fc.evaluate(f)>0.5 if fc else o.hide_render
        if not hid: n+=1
    if n: use[inst][face]+=n
allf=collections.Counter()
for inst,c in sorted(use.items()):
    for k,v in c.items(): allf[k]+=v
    tot=sum(c.values()); top=c.most_common(1)[0]
    print('FC',inst,len(c),sorted(c),f'top {top[0]} {top[1]/tot:.0%}')
agg=collections.defaultdict(collections.Counter)
for inst,c in use.items():
    nm=inst.split('_',1)[1]
    if not nm.startswith('x'): agg[nm].update(c)
for nm,c in sorted(agg.items()):
    tot=sum(c.values()); lib_=[k for k in c if not k.startswith('talk') and k!='blink']; top=max(((v,k) for k,v in c.items() if k not in ('blink','deadpan') and not k.startswith('talk')),default=(0,''))
    print('FCHAR',nm,'faces',len(lib_),'top',top[1],f'{top[0]/tot:.0%}')
print('FACECOUNT distinct',len(allf),sorted(allf))
