#!/usr/bin/env python3
"""agree_total.py -> new-analysis-2/AGREEMENT_v3_totals.json : agreement per category and per field across the 7 videos."""
import json, csv, os
from collections import defaultdict
N='/mnt/project-files/modern-vista-social/research/rick-style-spec/new-analysis-2/'
V=['03_7xS87iActkU','12_0m6G8pDtzNs','04_Mz72MuPgnGY','10_GM9UKnZ6JFw','14_VS1Z_Q-Klt8','22_i4hYq1oSXTg','24_aD73kaL_PtY']
F=defaultdict(lambda:[0,0]); per={}
def kind(t): return 'cut' if 'cut' in t else ('dissolve' if 'dissolve' in t else t)
for v in V:
    a=json.load(open(N+v+'/agreement_joins_captions.json')); pv={}
    for r in a['joins']['rows']:
        A,B=r[0],r[1]
        F['joins.found'][1]+=1
        if A in (None,'None') or B in (None,'None'): continue
        c=r[2]; F['joins.found'][0]+=1
        for k,i in (('joins.start_within_2f',1),('joins.length_by_eye_or_whole_frame_within_2f',2),('joins.kind',3)):
            F[k][1]+=1; F[k][0]+=bool(c[i]) if not isinstance(c[i],str) else c[i]=='True'
    F['captions.fields'][0]+=a['captions']['ok']; F['captions.fields'][1]+=a['captions']['total']
    pv['joins_raw']=a['joins']['rate']; pv['captions']=a['captions']['rate']
    # dissolve length: static-patch fit (blendfit2) vs measurer B's fit
    bf=N+v+'/blendfit/joins_blendfit_auto.csv'; Bj=json.load(open(N+v+'/measurerB_joins.json'))['joins']
    if os.path.exists(bf):
        for r in csv.DictReader(open(bf)):
            if int(r['auto_len'])==0 and int(r['recorded_len'])==0: continue
            m=[b for b in Bj if abs(b['first_blend_frame']-int(r['auto_start']))<=8 and 'cut' not in b['type']]
            if not m: continue
            b=min(m,key=lambda b:abs(b['first_blend_frame']-int(r['auto_start']))); k='dissolve_len.patch_fit_vs_B_fit_within_2f'+('' if r['flag']=='ok' else '.lowquality')
            F[k][1]+=1; F[k][0]+=abs(b['len_f']-int(r['auto_len']))<=2
            k2='dissolve_len.patch_fit_vs_B_fit_within_1f'+('' if r['flag']=='ok' else '.lowquality'); F[k2][1]+=1; F[k2][0]+=abs(b['len_f']-int(r['auto_len']))<=1
    m=json.load(open(N+v+'/agreement_motion.json')) if os.path.exists(N+v+'/agreement_motion.json') else None
    if m:
        for k,x in m['fields'].items(): F['motion.'+k][0]+=x['ok']; F['motion.'+k][1]+=x['compared']
        pv['motion']={k:x['rate'] for k,x in m['categories'].items()}
    c=json.load(open(N+v+'/cam_agreement.json')) if os.path.exists(N+v+'/cam_agreement.json') else None
    if c:
        for k,x in c['per_field'].items(): F['camera_tools.'+k][0]+=x[0]; F['camera_tools.'+k][1]+=x[1]
        pv['camera_tools']=c['rate']
    per[v]=pv
au=json.load(open(N+'agreement_audio.json'))
for v,row in au['videos'].items():
    for k,x in row.items():
        if 'ok' in x: F['audio.'+k][0]+=x['ok']; F['audio.'+k][1]+=1
cats=defaultdict(lambda:[0,0])
for k,(o,t) in F.items():
    c=k.split('.')[0] if not k.startswith('motion.') else 'motion.'+k.split('.')[1]
    cats[c][0]+=o; cats[c][1]+=t
out=dict(fields={k:dict(ok=o,n=t,rate=round(100*o/t,2) if t else None,passes_99=bool(t>=20 and o/t>=0.99)) for k,(o,t) in sorted(F.items())},categories={k:dict(ok=o,n=t,rate=round(100*o/t,2) if t else None) for k,(o,t) in cats.items()},per_video=per)
json.dump(out,open(N+'AGREEMENT_v3_totals.json','w'),indent=1)
for k,x in out['categories'].items(): print('CAT',k,x)
for k,x in out['fields'].items(): print(f"{k:60s} {x['ok']:5d}/{x['n']:5d} {x['rate']} {'PASS' if x['passes_99'] else ''}")
