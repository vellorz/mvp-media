import json,sys
PP=float(sys.argv[1]); FP=float(sys.argv[2])
ws=json.load(open('/home/user/havasu/voice2/c.words.json'))
FIX={'stone':'stones'}
out=[]
for x in ws:
    if out and x['w'].startswith('.') and out[-1]['w'].startswith('$'):
        out[-1]={'w':out[-1]['w']+x['w'],'s':out[-1]['s'],'e':x['e']}
    else: out.append(dict(x))
for k,o in enumerate(out):
    if o['w']=='stone' and k>0 and out[k-1]['w']=='The': o['w']='stones'
    if o['w']=='that\'s' and k>0 and out[k-1]['w']=='said,': o['w']='"That\'s'
    if o['w']=='heard.' and k>0 and out[k-1]['w']=='ever': o['w']='heard."'
FN={'the','a','an','of','to','and','by','in','at','on','for','from'}
W=[o['w'] for o in out]; n=len(W)
bare=lambda w: w.strip('.,?!').lower()
def cost(i,j):
    g=W[i:j]; c=1.0
    if any(x[-1] in '.,?!' for x in g[:-1]): return 1e9
    if len(g)>=2:
        if len(' '.join(g))>14: return 1e9
        if out[j-1]['s']-out[i]['e']>0.6: c+=3
        c+=PP*(len(g)-1)
        if len(' '.join(g))<=9: c-=0.25
        if len(g)==3 and len(' '.join(g))<=13: c-=0.3
    if len(g)==1 and bare(g[0]) in FN: c+=FP
    if j<n and g[-1][0].isupper() and W[j][0].isupper() and g[-1][-1] not in '.,?!': c+=2
    return c-1.0*len(g)*0  # per chunk
best=[1e18]*(n+1); prv=[0]*(n+1); best[0]=0
for j in range(1,n+1):
    for L in (1,2,3):
        i=j-L
        if i<0: continue
        v=best[i]+cost(i,j)
        if v<best[j]: best[j]=v; prv[j]=i
seg=[]; j=n
while j>0: seg.append((prv[j],j)); j=prv[j]
seg.reverse()
FPS=30; OFF=0.2; LEAD=1; res=[]
for k,(i,j) in enumerate(seg):
    f0=round((out[i]['s']+OFF)*FPS)-LEAD
    nxt=round((out[seg[k+1][0]]['s']+OFF)*FPS)-LEAD if k+1<len(seg) else 10**9
    res.append([' '.join(W[i:j]),f0,min(nxt,round((out[j-1]['e']+OFF)*FPS)+6)])
json.dump(res,open('/home/user/cart/src/videos/havasu/captions.json','w'))
from collections import Counter; import statistics
c=Counter(len(r[0].split()) for r in res); t=len(res); print({k:round(v/t,2) for k,v in c.items()}, t, 'median dur', statistics.median(r[2]-r[1] for r in res))
print(' | '.join(r[0] for r in res[:45]))
