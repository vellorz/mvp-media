# Narration stats from YouTube json3 word timings. Usage: python3 script_stats.py <txt-dir> > out.md
import sys,glob,os,re,statistics as st
d=sys.argv[1]; rows=[]
PIV=['you see','well,','but then','except','so,','turns out','here\'s the thing','wait','imagine','because','that\'s why','which is why','the reason']
for f in sorted(glob.glob(d+'/*.words.tsv')):
    n=os.path.basename(f)[:2]
    W=[(float(l.split('\t')[0]),l.split('\t')[1].strip()) for l in open(f) if l.strip()]
    W=[(t,w) for t,w in W if w!='[music]']
    txt=open(f.replace('.words.tsv','.txt')).read().replace('[music] ','').replace(' [music]','')
    dur=W[-1][0]-W[0][0]+0.35; wps=len(W)/dur
    gaps=[W[i+1][0]-W[i][0] for i in range(len(W)-1)]
    sents=[s for s in re.split(r'(?<=[.?!])\s+',txt) if s.strip()]
    sl=[len(s.split()) for s in sents]
    first3=' '.join(w for t,w in W if t<3.0)
    hook=sents[0]
    q=len(re.findall(r'"',txt))//2
    piv=[]
    for p in PIV:
        for m in re.finditer(re.escape(p),txt.lower()):
            # approx time via word index
            idx=len(txt[:m.start()].split()); piv.append((p,round(W[min(idx,len(W)-1)][0],1)))
    piv=sorted(piv,key=lambda x:x[1])
    you=len(re.findall(r"\byou(r|'re|'d|'ll)?\b",txt.lower()))
    nums=len(re.findall(r'\d',txt))
    rows.append(dict(n=n,words=len(W),dur=round(dur,1),wps=round(wps,2),gmed=round(st.median(gaps),2),gp95=round(sorted(gaps)[int(.95*len(gaps))],2),gmax=round(max(gaps),2),
        nsent=len(sents),slmean=round(st.mean(sl),1),slmed=st.median(sl),slmax=max(sl),first3=first3,hook=hook,hookw=len(hook.split()),quotes=q,you=you,piv=piv,last=sents[-1],qmarks=txt.count('?')))
print('| # | words | dur s | w/s | gap med | gap p95 | gap max | sentences | mean words/sent | median | max | hook words | quoted lines | "you" | ? |')
print('|'+'---|'*15)
for r in rows: print(f"| {r['n']} | {r['words']} | {r['dur']} | {r['wps']} | {r['gmed']} | {r['gp95']} | {r['gmax']} | {r['nsent']} | {r['slmean']} | {r['slmed']} | {r['slmax']} | {r['hookw']} | {r['quotes']} | {r['you']} | {r['qmarks']} |")
for k in ['words','dur','wps','gmax','slmean','hookw']:
    v=[r[k] for r in rows]; print(f"\n{k}: median {st.median(v)} min {min(v)} max {max(v)}",end='')
print('\n\n## Per video: first 3 s / hook / pivots / last line')
for r in rows:
    print(f"\n### {r['n']}\n- first 3 s: {r['first3']}\n- hook sentence: {r['hook']}\n- pivots (word, s): {r['piv']}\n- last sentence: {r['last']}")
