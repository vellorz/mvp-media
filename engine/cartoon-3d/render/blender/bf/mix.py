# Mix (rule 188): VO studio-clean, bed constant ~20 dB under the VO, SFX 8-12 dB over the bed; master -14 LUFS, -2 dBTP, LRA <= 3.2
import subprocess, re, json, sys
A='/root/bf/audio/'; VO='/mnt/project-files/modern-vista-social/experiments/2026-11-18_rick-99-test/audio/vo_trim.wav'
END=1752/30
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
gs=gb+(4.0-float(np.median(offs)))   # r5b: with the bed riding only 14-17 dB under the VO, +10 over the bed put SFX peaks 2.6 LU under the VO; +4 keeps every SFX >= 8 LU under (rule 192, guide v1.2 'both soft'); loudest 50 ms of each event group at +10 dB over the bed RMS across its span
print('SFX raw offset median',round(float(np.median(offs)),2),'spread',round(min(offs),2),round(max(offs),2))
print('VO',vI,'bed',bI,'->gain',round(gb,2),'sfx',sI,'->gain',round(gs,2))
cmd=(f'ffmpeg -y -hide_banner -loglevel error -i {VO} -i {A}bed.wav -i {A}sfx.wav -filter_complex '
     f'"[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay=100|100,apad=whole_dur={END}[v];[1:a]volume={gb}dB[b];[2:a]volume={gs}dB[s];'
     f'[v][b][s]amix=inputs=3:normalize=0:duration=longest,atrim=0:{END}[m]" -map "[m]" -ar 48000 {A}premix.wav')
subprocess.run(cmd,shell=True,check=True)
pI,pL,pT=lufs(A+'premix.wav'); g=-14.0-pI
subprocess.run(f'ffmpeg -y -hide_banner -loglevel error -i {A}premix.wav -af "volume={g}dB,alimiter=limit=0.78:attack=2:release=60:level=disabled" -ar 48000 {A}mix.wav',shell=True,check=True)
I,LRA,TP=lufs(A+'mix.wav'); g+=-14.0-I
subprocess.run(f'ffmpeg -y -hide_banner -loglevel error -i {A}premix.wav -af "volume={g}dB,alimiter=limit=0.78:attack=2:release=60:level=disabled" -ar 48000 {A}mix.wav',shell=True,check=True)
I,LRA,TP=lufs(A+'mix.wav'); print(json.dumps({'I':I,'LRA':LRA,'TP':TP,'bed_under_vo':BED_UNDER,'sfx_under_vo':SFX_UNDER}))
