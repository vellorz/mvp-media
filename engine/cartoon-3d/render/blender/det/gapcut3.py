# gapcut v3 (Detroit round-1 audio verifier V6: v1 cut voiced speech at joins 2, 9, 14 because whisper's word edges are loose).
# Each pause over MAXG is shortened ONLY inside its longest unvoiced run (10 ms frames: rms <= -38 dBFS or zcr >= 0.12, i.e. silence or breath),
# with 20 ms guards on both sides; a pause whose unvoiced run is short gets a smaller cut. Speech is never cut or stretched.
# python3 gapcut3.py SRC WORDS DST MAXG
import json, sys, numpy as np, subprocess
sys.path.insert(0,'/root/det/src'); from voicedmap import load, voiced, SR
src,words,dst=sys.argv[1],sys.argv[2],sys.argv[3]; MAXG=float(sys.argv[4])
a=load(src); v,_,_=voiced(a); W=json.load(open(words)); keep=[]; pos=0; cut=0; log=[]; G=int(0.02*SR)
for i in range(len(W)-1):
    g0,g1=W[i][2],W[i+1][1]
    if g1-g0<=MAXG: continue
    L=g1-g0-MAXG; i0,i1=int((g0-0.1)*100),int((g1+0.1)*100); best=(0,0)
    k=i0
    while k<i1:
        if not v[k]:
            j=k
            while j<i1 and not v[j]: j+=1
            if j-k>best[1]-best[0]: best=(k,j)
            k=j
        else: k+=1
    r0,r1=best[0]*0.01,best[1]*0.01; room=r1-r0-0.04-MAXG*0.5   # keep at least half the target pause inside the silent run
    Le=max(0.0,min(L,room))
    if Le<0.01: log.append((round(g0,3),round(g1-g0,3),0.0,'no silent room')); continue
    c0=int(((r0+r1)/2-Le/2)*SR); c1=c0+int(Le*SR)
    if c0<pos+G: continue
    keep.append(a[pos:c0]); log.append((round(g0,3),round(g1-g0,3),round(Le,3),round(r1-r0,3))); cut+=Le; pos=c1
keep.append(a[pos:])
y=keep[0]; f=int(0.005*SR); rr=np.linspace(0,1,f,dtype=np.float32)
for k in keep[1:]:
    if len(y)>f and len(k)>f: y=np.concatenate([y[:-f],y[-f:]*(1-rr)+k[:f]*rr,k[f:]])
    else: y=np.concatenate([y,k])
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-c:a','pcm_s24le',dst],input=y.astype(np.float32).tobytes())
json.dump(dict(maxgap=MAXG,method='gapcut3: cut only inside the longest unvoiced run, 20 ms guards',cuts=log,removed_s=round(cut,3)),open(dst+'.gaplog.json','w'),indent=0)
vin=v.sum()*0.01; vout=voiced(y)[0].sum()*0.01
print('gapcut3 removed',round(cut,2),'s; len',round(len(y)/SR,2),'voiced frames in',round(vin,2),'s out',round(vout,2),'s')
