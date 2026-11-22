# r2 (audio verifier A6a/A6c, rules 319 + 192): per-event trim of the SFX stem AFTER music.py, with the mix gains held fixed.
# Each group: loudest 50 ms >= +4.5 dB over the local bed (payoff >= +6) AND K-weighted 400 ms momentary >= 8.5 LU under the VO.
# Where both cannot hold (payoff line), rule 192 wins on the SFX and the bed dips smoothly under that event instead (max 4 dB).
# python3 sfxlevel.py GB GS   (gains from mixlog); rewrites /root/det/audio/sfx.wav and bed.wav (originals kept as *_pre.wav)
import numpy as np, json, sys, wave, subprocess, shutil, os
from scipy.signal import lfilter
A='/root/det/audio/'; SR=48000; gb,gs=float(sys.argv[1]),float(sys.argv[2])
def rd(p):
    with wave.open(p) as w: return np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2)[:,0]/32768.0
def wr(p,x):
    y=(np.clip(x,-1,1)*32767).astype(np.int16); st=np.stack([y,y],1)
    with wave.open(p,'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
for n in ('sfx','bed'):
    if not os.path.exists(A+n+'_pre.wav'): shutil.copy(A+n+'.wav',A+n+'_pre.wav')
S=rd(A+'sfx_pre.wav').copy(); Bd=rd(A+'bed_pre.wav').copy()
v=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i','/root/det/audio_r2/vo_final.wav','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,np.float32).astype(np.float64)
v=np.concatenate([np.zeros(int(0.1*SR)),v]); v=np.pad(v,(0,max(0,len(S)-len(v))))[:len(S)]   # per-channel comparison, same convention as sfxcheck.py (rule 322)
b1=[1.53512485958697,-2.69169618940638,1.19839281085285]; a1=[1,-1.69065929318241,0.73248077421585]; b2=[1,-2,1]; a2=[1,-1.99004745483398,0.99007225036621]
K=lambda x: lfilter(b2,a2,lfilter(b1,a1,x)); vk=K(v); W=int(0.4*SR)
r=lambda a: float(np.sqrt(np.mean(a**2))+1e-12)
def pk(a,n=2400): return max(r(a[k:k+n]) for k in range(0,max(1,len(a)-n+1),600))
EV=json.load(open(A+'sfx_events.json')); END=len(S); PAY=max(e['f'] for e in EV)-30
for it in range(6):
    sg,bg=S*10**(gs/20),Bd*10**(gb/20); sk=K(sg); rep=[]
    for k,e in enumerate(EV):
        i,w=e['i'],e['w']; j=EV[k+1]['i'] if k+1<len(EV) else END
        ob=20*np.log10(pk(sg[i:i+w])/r(bg[i:i+w]))
        lu=max(10*np.log10(np.mean(sk[q:q+W]**2)+1e-12) for q in range(i,i+w,int(0.05*SR)))-10*np.log10(np.mean(vk[max(0,i-SR):i+2*SR]**2)+1e-12)
        tgt=6.0 if e['f']>=PAY else 4.5
        up=min(tgt-ob, -8.5-lu)          # rule 192 cap wins
        if abs(up)>0.15: S[i:j]*=10**(up/20)
        short=tgt-(ob+up)
        if short>0.2:                     # bed dip under this event only (smooth 0.25 s ramps), max 4 dB
            d=min(4.0,short); g=np.ones(END); a0,a1_=max(0,i-int(0.25*SR)),min(END,i+w+int(0.25*SR))
            ramp=np.ones(a1_-a0); rl=int(0.25*SR); ramp[:rl]=np.linspace(0,1,rl); ramp[-rl:]=np.linspace(1,0,rl)
            g[a0:a1_]=10**(-d*ramp/20); Bd*=g
        rep.append((e['f'],round(ob,1),round(lu,1)))
    print('iter',it,rep)
wr(A+'sfx.wav',S); wr(A+'bed.wav',Bd); print('SFXLEVEL_OK')
