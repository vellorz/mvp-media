# Mix (rule 188): VO studio-clean, bed constant ~20 dB under the VO, SFX 8-12 dB over the bed; master -14 LUFS, -2 dBTP, LRA <= 3.2
import subprocess, re, json, sys
A='/root/bf/audio/'; VO='/mnt/project-files/modern-vista-social/experiments/2026-11-18_rick-99-test/audio/vo_trim.wav'
END=1752/30
def lufs(path,extra=''):
    o=subprocess.run(f'ffmpeg -hide_banner -nostats -i {path} {extra} -af ebur128=peak=true -f null -',shell=True,capture_output=True,text=True).stderr
    s=o[o.rfind('Summary'):]
    I=float(re.search(r'I:\s+(-?[\d.]+) LUFS',s).group(1)); LRA=float(re.search(r'LRA:\s+([\d.]+) LU',s).group(1)); TP=float(re.search(r'Peak:\s+(-?[\d.]+) dBFS',s).group(1))
    return I,LRA,TP
vI,_,_=lufs(VO); bI,_,_=lufs(A+'bed.wav'); sI,_,_=lufs(A+'sfx.wav')
BED_UNDER=float(sys.argv[1]) if len(sys.argv)>1 else 20.0; SFX_UNDER=10.0
gb=(vI-BED_UNDER)-bI; gs=(vI-SFX_UNDER)-sI
print('VO',vI,'bed',bI,'->gain',round(gb,2),'sfx',sI,'->gain',round(gs,2))
cmd=(f'ffmpeg -y -hide_banner -loglevel error -i {VO} -i {A}bed.wav -i {A}sfx.wav -filter_complex '
     f'"[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay=100|100,apad=whole_dur={END}[v];[1:a]volume={gb}dB[b];[2:a]volume={gs}dB[s];'
     f'[v][b][s]amix=inputs=3:normalize=0:duration=longest,atrim=0:{END}[m]" -map "[m]" -ar 48000 {A}premix.wav')
subprocess.run(cmd,shell=True,check=True)
pI,pL,pT=lufs(A+'premix.wav'); g=-14.0-pI
subprocess.run(f'ffmpeg -y -hide_banner -loglevel error -i {A}premix.wav -af "volume={g}dB,alimiter=limit=0.70:attack=2:release=60:level=disabled" -ar 48000 {A}mix.wav',shell=True,check=True)
I,LRA,TP=lufs(A+'mix.wav'); g+=-14.0-I
subprocess.run(f'ffmpeg -y -hide_banner -loglevel error -i {A}premix.wav -af "volume={g}dB,alimiter=limit=0.70:attack=2:release=60:level=disabled" -ar 48000 {A}mix.wav',shell=True,check=True)
I,LRA,TP=lufs(A+'mix.wav'); print(json.dumps({'I':I,'LRA':LRA,'TP':TP,'bed_under_vo':BED_UNDER,'sfx_under_vo':SFX_UNDER}))
