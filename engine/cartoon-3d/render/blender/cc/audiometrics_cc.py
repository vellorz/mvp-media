# Cape Cod audio gate: bed std (3 s windows, 0.5 s hop and non-overlap), |r| VO vs bed envelope (200/400 ms, dB), SFX-over-bed per event in the mix.  python3 audiometrics_cc.py BED_GAIN_DB SFX_GAIN_DB [sfx stem]
import numpy as np, json, subprocess, sys
from scipy.signal import lfilter
sr=48000; END=1817/30
def rd(p): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-af','pan=mono|c0=c0','-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout,np.float32).astype(np.float64)
gb,gs=float(sys.argv[1]),float(sys.argv[2])
n=int(END*sr); b=rd('/root/cc/audio/bed.wav')[:n]*10**(gb/20); s=rd(sys.argv[3] if len(sys.argv)>3 else '/root/cc/audio/sfx.wav')[:n]*10**(gs/20)
v=np.concatenate([np.zeros(int(0.1*sr)),rd('/root/cc/vo/vo_trim.wav')]); v=np.pad(v,(0,max(0,n-len(v))))[:n]
b1=[1.53512485958697,-2.69169618940638,1.19839281085285]; a1=[1,-1.69065929318241,0.73248077421585]; b2=[1,-2,1]; a2=[1,-1.99004745483398,0.99007225036621]
K=lambda x: lfilter(b2,a2,lfilter(b1,a1,x)); bk,vk=K(b),K(v)
L=lambda x: -0.691+10*np.log10(np.mean(x**2)+1e-12)
def win(x,w,h): W=int(w*sr);H=int(h*sr); return np.array([L(x[i:i+W]) for i in range(0,len(x)-W+1,H)])
for h in (0.5,3.0): print('BED_STD 3s hop',h, round(float(np.std(win(bk,3,h))),2))
gap=win(vk,3,0.5)-win(bk,3,0.5); print('GAP mean',round(float(np.mean(gap)),2))
for w in (0.2,0.4):
    a,c=win(vk,w,w),win(bk,w,w); m=a>-60; print('R',w,round(float(np.corrcoef(a[m],c[m])[0,1]),3))
st=win(bk,3,3); print('OPEN',round(float(st[0]-np.median(st)),2),'PAYOFF-START',round(float(np.mean(win(bk[int(57*sr):],3,1))-st[0]),2))
r=lambda a: float(np.sqrt(np.mean(a**2))+1e-12)
def pk(a): N=2400; return max(r(a[k:k+N]) for k in range(0,max(1,len(a)-N+1),600))
o=[]
for e in json.load(open('/root/cc/audio/sfx_events.json')):
    i,w=e['i'],e['w']; o.append((e['f'],round(20*np.log10(pk(s[i:i+w])/r(b[i:i+w])),1)))
print('SFX',o); x=[q for _,q in o]; print('SFX median',np.median(x),'min',min(x),'max',max(x),'in8-12',sum(8<=q<=12 for q in x),'/',len(x))
