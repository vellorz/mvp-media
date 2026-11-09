import subprocess, numpy as np, scipy.io.wavfile as wf, sys
src, dst, tempo = sys.argv[1], sys.argv[2], float(sys.argv[3])
sr=48000
x = np.frombuffer(subprocess.run(["ffmpeg","-v","quiet","-i",src,"-ac","1","-ar",str(sr),"-f","f32le","-"],capture_output=True).stdout,np.float32)
hop=480; n=len(x)//hop
rms=np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2)) for i in range(n)])
db=20*np.log10(rms+1e-9); sil=db<-45
out=[]; i=0; MAXG=int(0.26*sr/hop)
# leading silence trim to 0.1s
while i<n and sil[i]: i+=1
out.append(np.zeros(int(0.08*sr),np.float32))
while i<n:
    j=i
    while j<n and sil[j]==sil[i]: j+=1
    seg=x[i*hop:j*hop]
    if sil[i] and (j-i)>MAXG:
        keep=MAXG*hop if j<n else int(0.4*sr)
        h=keep//2; seg=np.concatenate([seg[:h],seg[-(keep-h):]]) if j<n else seg[:keep]
    out.append(seg); i=j
y=np.concatenate(out)
wf.write("/tmp/_t.wav",sr,y)
subprocess.run(["ffmpeg","-y","-v","quiet","-i","/tmp/_t.wav","-af",f"atempo={tempo}","-ar",str(sr),"-ac","1","-c:a","pcm_s16le",dst])
print(len(x)/sr, len(y)/sr, len(y)/sr/tempo)
