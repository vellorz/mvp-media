import json,sys,re
src,base=sys.argv[1],sys.argv[2]
d=json.load(open(src)); rows=[]
for ev in d.get('events',[]):
    t0=ev.get('tStartMs',0)
    for sg in ev.get('segs',[]) or []:
        w=sg.get('utf8','').strip()
        if not w or w=='\n': continue
        for k,tok in enumerate(w.split()):
            rows.append(((t0+sg.get('tOffsetMs',0))/1000.0, tok))
open(base+'.words.tsv','w').write(''.join(f"{t:.2f}\t{w}\n" for t,w in rows))
open(base+'.txt','w').write(' '.join(w for _,w in rows)+'\n')
print(base, len(rows), 'words')
