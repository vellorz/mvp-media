# Every SFX group: K-weighted 400 ms momentary loudness in the mix vs the VO's loudness around it (rule: >= 8 LU under the VO); HF (2-5 kHz) share
import numpy as np, json, subprocess, re
from scipy.signal import lfilter, butter, sosfilt
sr=48000
def rd(p): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout,np.float32).astype(np.float64)
s=rd('/root/bf/audio/sfx.wav'); v=rd('/mnt/project-files/modern-vista-social/experiments/2026-11-18_rick-99-test/audio/vo_trim.wav')
d=int(0.1*sr); v=np.concatenate([np.zeros(d),v]); v=np.pad(v,(0,max(0,len(s)-len(v))))[:len(s)]
gs=float(re.findall(r"sfx \S+ ->gain (\S+)",subprocess.run(['python3','-c','print(open("/root/bf/audio/mixlog.txt").read())'],capture_output=True,text=True).stdout or 'sfx 0 ->gain -14.56')[0]) if False else None
import sys; gs=float(sys.argv[1]) if len(sys.argv)>1 else -14.56
s=s*10**(gs/20)
b1=[1.53512485958697,-2.69169618940638,1.19839281085285]; a1=[1,-1.69065929318241,0.73248077421585]; b2=[1,-2,1]; a2=[1,-1.99004745483398,0.99007225036621]
K=lambda x: lfilter(b2,a2,lfilter(b1,a1,x)); sk,vk=K(s),K(v); W=int(0.4*sr)
hf=sosfilt(butter(4,[2000,5000],'bp',fs=sr,output='sos'),s)
mom=lambda x,i: -0.691+10*np.log10(np.mean(x[i:i+W]**2)+1e-12)
worst=-99
for e in json.load(open('/root/bf/audio/sfx_events.json')):
    i=e['i']; best=max(mom(sk,k) for k in range(i,i+e['w'],int(0.05*sr)))
    vs=-0.691+10*np.log10(np.mean(vk[max(0,i-sr):i+2*sr]**2)+1e-12); hs=10*np.log10(np.mean(hf[i:i+e['w']]**2)/np.mean(s[i:i+e['w']]**2)+1e-12)
    worst=max(worst,best-vs); print('SFX f',e['f'],'LU vs VO',round(best-vs,1),'HF share dB',round(hs,1))
print('SFX_WORST',round(worst,1),'PASS' if worst<=-8 else 'FAIL')
