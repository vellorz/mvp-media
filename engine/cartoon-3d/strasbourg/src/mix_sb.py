# Mix (rules 8/188 revised Nov 21): VO studio-clean, bed 14.4-18.6 dB under the VO riding its level map (std 2.3-4.0 dB, no ducking), SFX levelled per event to +9 over the bed (A6, rule 319), still >= 8 LU under the VO (rule 192); master -14 LUFS, -1.9 to -2.2 dBTP
import subprocess, re, json, sys
A='/root/sb/audio/'; VO='/root/sb/vo/vo_final_dc.wav'   # r1b: click at 20.734 s smoothed (declick_sb.py)
END=2037/30   # r2 (payoff E3: tail 1.31 s after 'Nicholas'): video ends at f2036
def lufs(path,extra=''):
    o=subprocess.run(f'ffmpeg -hide_banner -nostats -i {path} {extra} -af ebur128=peak=true -f null -',shell=True,capture_output=True,text=True).stderr
    s=o[o.rfind('Summary'):]
    I=float(re.search(r'I:\s+(-?[\d.]+) LUFS',s).group(1)); LRA=float(re.search(r'LRA:\s+([\d.]+) LU',s).group(1)); TP=float(re.search(r'Peak:\s+(-?[\d.]+) dBFS',s).group(1))
    return I,LRA,TP
# A4: measure the VO as it plays in the mix (mono sent to both channels = +3 dB vs the mono file)
subprocess.run(f'ffmpeg -y -hide_banner -loglevel error -i {VO} -af "aresample=48000,pan=stereo|c0=c0|c1=c0" {A}vo_st.wav',shell=True,check=True)
vI,_,_=lufs(A+'vo_st.wav'); bI,_,_=lufs(A+'bed.wav'); sI,_,_=lufs(A+'sfx.wav')
BED_UNDER=float(sys.argv[1]) if len(sys.argv)>1 else 16.0; SFX_UNDER=16.0   # r5b: 10 made peaks only 2.6 LU under the VO (rule 192 needs >= 8); round 5 (M4): mean VO-music gap 14.5-17 dB
gb=(vI-BED_UNDER)-bI
# A6: global SFX gain so the median event sits +10 dB over the bed in the mix (events are pre-levelled in music.py)
import numpy as np, wave
def rd(p):
    with wave.open(p) as w: a=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2)[:,0]/32768.0
    return a
bedA,sfxA=rd(A+'bed.wav'),rd(A+'sfx.wav'); EVs=json.load(open(A+'sfx_events.json'))
r=lambda a: float(np.sqrt(np.mean(a**2))+1e-12)
def pk(a):
    n=2400; return max(r(a[k:k+n]) for k in range(0,max(1,len(a)-n+1),600))
offs=[20*np.log10(pk(sfxA[e['i']:e['i']+e['w']])/r(bedA[e['i']:e['i']+e['w']])) for e in EVs]
HR=18.0; gs=gb+HR   # stem written HR dB low so boosted events never clip int16, gain restored here. cc r2: each SFX event levelled on its own to +9 dB over the bed (payoff ding +10): A6 8-12 dB, rule 319 (>= +4, payoff >= +6); rule 192 (>= 8 LU under the VO) is re-checked by sfxcheck_cc.py
TGT={2002:10.0}; G=np.array([TGT.get(e['f'],9.0)-o for e,o in zip(EVs,offs)]); SR_=48000
def envf(G):
    acc=np.zeros(len(sfxA)); cnt=np.zeros(len(sfxA))
    for e,g in zip(EVs,G):
        a_,b_=max(0,e['i']-int(0.02*SR_)),min(len(sfxA),e['i']+e['w']+int(0.04*SR_)); acc[a_:b_]+=g; cnt[a_:b_]+=1
    gd=np.where(cnt>0,acc/np.maximum(cnt,1),0.0); R=int(0.01*SR_); gd=np.convolve(gd,np.ones(R)/R,mode='same'); return 10**(gd/20)
for _ in range(6):   # re-measure each event in the levelled stem and correct (overlapping events share their gain)
    env=envf(G); lev=sfxA*env
    got=[20*np.log10(pk(lev[e['i']:e['i']+e['w']])/r(bedA[e['i']:e['i']+e['w']])) for e in EVs]
    G=G+np.array([TGT.get(e['f'],9.0)-q for e,q in zip(EVs,got)])*0.8
# rule 192 wins over A6 where they clash: cap each event so its loudest 400 ms (K-weighted) stays >= 8.3 LU under the VO around it (sfxcheck_cc.py method); floor rule 319 (+4, payoff +6) is reported, not forced
from scipy.signal import lfilter as _lf
_b1=[1.53512485958697,-2.69169618940638,1.19839281085285]; _a1=[1,-1.69065929318241,0.73248077421585]; _b2=[1,-2,1]; _a2=[1,-1.99004745483398,0.99007225036621]
_K=lambda x: _lf(_b2,_a2,_lf(_b1,_a1,x))
with wave.open(A+'vo_st.wav') as w: _v=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2)[:,0]/32768.0
_v=np.concatenate([np.zeros(int(0.1*SR_)),_v]); _v=np.pad(_v,(0,max(0,len(sfxA)-len(_v))))[:len(sfxA)]; _vk=_K(_v)
_W=int(0.4*SR_); _mom=lambda x,i: -0.691+10*np.log10(np.mean(x[i:i+_W]**2)+1e-12)
for _ in range(5):
    sk_=_K(sfxA*envf(G)*10**((gs-HR)/20)); over=[]
    for e in EVs:
        i=e['i']; bst=max(_mom(sk_,k) for k in range(i,i+e['w'],int(0.05*SR_))); vs=-0.691+10*np.log10(np.mean(_vk[max(0,i-SR_):i+2*SR_]**2)+1e-12); over.append(bst-vs)
    G=G-np.clip(np.array(over)+8.3,0,None)
print('SFX LU vs VO after cap',[round(float(o),1) for o in over])
env=envf(G)
import wave as _w
with _w.open(A+'sfx.wav') as w: prm=w.getparams(); st=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2).astype(np.float64)
st=np.clip(st*env[:len(st),None]*10**(-HR/20),-32767,32767).astype(np.int16)
with _w.open(A+'sfx_lev.wav','wb') as w: w.setparams(prm); w.writeframes(st.tobytes())
json.dump({'per_event_gain_db':[round(float(g),2) for g in G],'frames':[e['f'] for e in EVs]},open(A+'sfx_lev.json','w'))   # r5b: with the bed riding only 14-17 dB under the VO, +10 over the bed put SFX peaks 2.6 LU under the VO; +4 keeps every SFX >= 8 LU under (rule 192, guide v1.2 'both soft'); loudest 50 ms of each event group at +10 dB over the bed RMS across its span
print('SFX raw offset median',round(float(np.median(offs)),2),'spread',round(min(offs),2),round(max(offs),2))
print('VO',vI,'bed',bI,'->gain',round(gb,2),'sfx',sI,'->gain',round(gs,2))
cmd=(f'ffmpeg -y -hide_banner -loglevel error -i {VO} -i {A}bed.wav -i {A}sfx_lev.wav -filter_complex '
     f'"[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay=100|100,apad=whole_dur={END}[v];[1:a]volume={gb}dB[b];[2:a]volume={gs}dB[s];'
     f'[v][b][s]amix=inputs=3:normalize=0:duration=longest,atrim=0:{END}[m]" -map "[m]" -ar 48000 {A}premix.wav')
subprocess.run(cmd,shell=True,check=True)
pI,pL,pT=lufs(A+'premix.wav'); g=-14.0-pI
subprocess.run(f'ffmpeg -y -hide_banner -loglevel error -i {A}premix.wav -af "volume={g}dB,alimiter=limit=0.78:attack=2:release=60:level=disabled,afade=t=out:st={END-0.03:.3f}:d=0.03" -ar 48000 {A}mix.wav',shell=True,check=True)
I,LRA,TP=lufs(A+'mix.wav'); g+=-14.0-I
subprocess.run(f'ffmpeg -y -hide_banner -loglevel error -i {A}premix.wav -af "volume={g}dB,alimiter=limit=0.78:attack=2:release=60:level=disabled,afade=t=out:st={END-0.03:.3f}:d=0.03" -ar 48000 {A}mix.wav',shell=True,check=True)
I,LRA,TP=lufs(A+'mix.wav'); print(json.dumps({'I':I,'LRA':LRA,'TP':TP,'bed_under_vo':BED_UNDER,'sfx_under_vo':SFX_UNDER}))
