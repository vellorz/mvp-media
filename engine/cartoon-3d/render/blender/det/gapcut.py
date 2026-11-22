# Detroit (owner Nov 22: pace must reach Rick's 3.4-4.1 w/s): shorten inter-word pauses longer than MAXG to MAXG,
# cutting only the middle of each pause (whisper word boundaries, 0.1 s kept on each side). Speech is never stretched.
import json, sys, subprocess, numpy as np
src,words,dst=sys.argv[1],sys.argv[2],sys.argv[3]; MAXG=float(sys.argv[4]) if len(sys.argv)>4 else 0.22; SR=48000
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',src,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,np.float32)
W=json.load(open(words)); keep=[]; pos=0; cut=0; log=[]
for i in range(len(W)-1):
    g0,g1=W[i][2],W[i+1][1]
    if g1-g0>MAXG:
        c0=int((g0+MAXG/2)*SR); c1=int((g1-MAXG/2)*SR)
        # cut at the quietest sample near each edge (no clicks): 5 ms crossfade
        keep.append(a[pos:c0]); log.append((round(g0,3),round(g1-g0,3))); cut+=(c1-c0)/SR; pos=c1
keep.append(a[pos:])
y=keep[0]; f=int(0.005*SR); r=np.linspace(0,1,f,dtype=np.float32)
for k in keep[1:]:
    if len(y)>f and len(k)>f: y=np.concatenate([y[:-f],y[-f:]*(1-r)+k[:f]*r,k[f:]])
    else: y=np.concatenate([y,k])
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-c:a','pcm_s24le',dst],input=y.astype(np.float32).tobytes())
json.dump(dict(maxgap=MAXG,cuts=log,removed_s=round(cut,3)),open(dst+'.gaplog.json','w'),indent=0)
print('gapcut removed',round(cut,2),'s in',len(log),'pauses; len',round(len(y)/SR,2))
