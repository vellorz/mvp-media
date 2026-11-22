# r5: rules 243-245 on the actual mix stems: VO-to-bed gap (3 s short-term), bed swing, ducking (bed in VO gaps vs under VO), open/end lift
import numpy as np, json, subprocess, sys
from scipy.signal import lfilter
sr=48000
def _mono_filter(p):
    # r9 lesson: ffmpeg -ac 1 SUMS stereo at 0.707 per channel (+3.01 dB vs a mono stem); average the channels instead, and leave true mono files alone
    n=int(subprocess.run(['ffprobe','-v','error','-select_streams','a:0','-show_entries','stream=channels','-of','csv=p=0',p],capture_output=True).stdout.split()[0])
    return 'pan=mono|c0=0.5*c0+0.5*c1' if n==2 else 'pan=mono|c0=c0'
def rd(p): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-af',_mono_filter(p),'-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout,np.float32).astype(np.float64)
gb=float(sys.argv[1]); b=rd('/root/det/audio/bed.wav')*10**(gb/20)
v=rd('/root/det/audio/vo_trim.wav'); v=np.concatenate([np.zeros(int(0.1*sr)),v])
n=min(len(b),int(64.6*sr)); b=b[:n]; v=np.pad(v,(0,max(0,n-len(v))))[:n]
b1=[1.53512485958697,-2.69169618940638,1.19839281085285]; a1=[1,-1.69065929318241,0.73248077421585]; b2=[1,-2,1]; a2=[1,-1.99004745483398,0.99007225036621]
K=lambda x: lfilter(b2,a2,lfilter(b1,a1,x)); bk,vk=K(b),K(v)
L=lambda x: -0.691+10*np.log10(np.mean(x**2)+1e-12)
vI=L(vk[np.abs(v)>0.003]) if True else L(vk)
W=3*sr; st=[L(bk[i:i+W]) for i in range(0,n-W,sr//2)]; st=np.array(st)
print('VO speech loudness',round(vI,1),'| bed 3s mean',round(float(np.mean(st)),1),'gap',round(vI-float(np.mean(st)),1),'(rule 243: 14.5-17)')
print('bed 3s range',round(float(st.max()-st.min()),1),'dB (Rick swings 7.8-15)')
med=float(np.median(st)); print('open first 3s vs median',round(st[0]-med,1),'(+2..+6)','| end last 3s vs median',round(st[-1]-med,1),'(+5..+10)')
# ducking: 400 ms bed level when VO active vs in VO gaps (local, within 1.5 s)
w=int(0.4*sr); act=[];gap=[]
for i in range(0,n-w,w):
    vv=np.sqrt(np.mean(v[i:i+w]**2)); bb=L(bk[i:i+w]); (act if vv>0.01 else gap).append((i,bb))
d=[]
if not gap: print('no VO gaps >= 400 ms below 0.01 RMS: ducking not measurable by windows (no gaps to duck in)')
for i,bb in gap:
    near=[x for j,x in act if abs(j-i)<1.5*sr]
    if near: d.append(bb-np.mean(near))
if d: print('bed in VO gaps minus under VO (local):',round(float(np.mean(d)),2),'dB mean, max',round(float(np.max(np.abs(d))),2),'(rule 244: within 1.2 dB)')
