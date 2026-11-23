# dc14 rule 354 probe (interim): neighbours in a shot never share a named arm move; no character repeats a raise more than twice; work loops exempt.
import json, collections
M=json.load(open('/root/dc/bridge/motion.json')); WORK={'write','press','carry','eat'}
fail=0; by=collections.defaultdict(list); cnt=collections.Counter()
for a in M['acts']:
    by[a['shot']].append(a)
    if a['act'] not in WORK: cnt[(a['kind'],a['act'])]+=1
for s,L in sorted(by.items()):
    insts=collections.defaultdict(set)
    for a in L: insts[a['inst']].add(a['act'])
    names=list(insts)
    for i in range(len(names)):
        for j in range(i+1,len(names)):
            sh=(insts[names[i]]&insts[names[j]])-WORK
            if sh: print('SHARED',s,names[i],names[j],sorted(sh)); fail+=1
    print('SHOT',s,{k:sorted(v) for k,v in insts.items()})
for (k,a),n in sorted(cnt.items()):
    if n>2: print('REPEAT',k,a,n); fail+=1
print('ARMVARIETY',len(M['acts']),'actions',len(set(a['act'] for a in M['acts'])),'kinds of move','FAIL',fail)
T=M['turns']; print('TURNS',len(T),'changes over',len(set(t['inst'] for t in T)),'characters')
