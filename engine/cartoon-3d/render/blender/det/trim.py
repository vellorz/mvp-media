# Rule 92: remove silence only. Pauses < -45 dB lasting >= 150 ms are shortened to 140 ms (70 ms kept each side).
import subprocess,numpy as np,re,sys,json
src,dst=sys.argv[1],sys.argv[2]; SR=48000
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',src,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,np.float32).copy()
out=subprocess.run(['ffmpeg','-v','info','-i',src,'-af','silencedetect=n=-45dB:d=0.15','-f','null','-'],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',out)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',out)]
keep=[];pos=0;cut=0;log=[]
for s,e in zip(st,en):
    if s<0.05: continue  # leading silence handled below
    a0=int((s+0.07)*SR); a1=int((e-0.07)*SR)
    if a1>a0: keep.append(a[pos:a0]); log.append((round(s,3),round(e-s,3))); cut+=(a1-a0)/SR; pos=a1
keep.append(a[pos:]); y=np.concatenate(keep)
# leading silence: start <= 0.05 s
nz=np.where(np.abs(y)>10**(-45/20))[0]; y=y[max(0,nz[0]-int(0.02*SR)):]
v_src=(np.abs(a)>10**(-40/20)).sum()/SR; v_dst=(np.abs(y)>10**(-40/20)).sum()/SR
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-c:a','pcm_s24le',dst],input=y.astype(np.float32).tobytes())
json.dump(dict(cuts=log,removed_s=round(cut,3),voiced_src=round(v_src,3),voiced_dst=round(v_dst,3)),open(dst+'.trimlog.json','w'),indent=0)
print('removed',round(cut,2),'s; voiced src',round(v_src,3),'dst',round(v_dst,3),'len',round(len(y)/SR,2))
