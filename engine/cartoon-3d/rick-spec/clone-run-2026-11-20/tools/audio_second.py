#!/usr/bin/env python3
"""audio_second.py -> new-analysis-2/agreement_audio.json. Second, independent measurement of the mix-level audio fields with ffmpeg ebur128
(measurer B) against audio.py / pyloudnorm values in audio_nonvocal/audio.json (measurer A). Tolerances from definitions v3 section 10: 0.3 LU, 0.5 dB."""
import subprocess, json, re, os, numpy as np, soundfile as sf
N='/mnt/project-files/modern-vista-social/research/rick-style-spec/new-analysis-2/'
V=['03_7xS87iActkU','12_0m6G8pDtzNs','04_Mz72MuPgnGY','10_GM9UKnZ6JFw','14_VS1Z_Q-Klt8','22_i4hYq1oSXTg','24_aD73kaL_PtY']
def eb(p):
    r=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',p,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
    s=r[r.rfind('Summary:'):]; g=lambda k: float(re.search(k+r'\s*(-?[\d.]+)',s).group(1))
    # short-term (3 s) series for the level curve
    st=[float(x) for x in re.findall(r'S:\s*(-?[\d.]+)',r[:r.rfind('Summary:')])]
    return dict(I=g('I:'),LRA=g('LRA:'),TP=g('Peak:'),S=st)
res={}; ok=tot=0; miss=[]
for v in V:
    a=json.load(open(N+v+'/audio_nonvocal/audio.json')) if os.path.exists(N+v+'/audio_nonvocal/audio.json') else None
    if not a: continue
    st='/root/work/out/'+v+'/stems/'; m=eb(st+'original.wav'); vo=eb(st+'vocals.wav'); mu=eb(st+'nonvocal.wav')
    # gap curve from short-term values sampled each 0.5 s (ebur128 prints every 100 ms)
    n=min(len(vo['S']),len(mu['S'])); gs=[vo['S'][i]-mu['S'][i] for i in range(30,n,5) if vo['S'][i]>-40 and mu['S'][i]>-70]
    mus=[mu['S'][i] for i in range(30,n,5) if mu['S'][i]>-70]
    B=dict(mix_I=m['I'],mix_LRA=m['LRA'],mix_TP=m['TP'],vo_I=vo['I'],music_I=mu['I'],gap_by_integrated=round(vo['I']-mu['I'],2),gap_mean=round(float(np.mean(gs)),2),gap_min=round(min(gs),2),gap_max=round(max(gs),2),bed_range=round(max(mus)-min(mus),2),bed_std=round(float(np.std(mus)),2))
    lm=a['loudness']['mix']; A=dict(mix_I=lm.get('I_LUFS',lm.get('integrated_LUFS')),mix_LRA=lm.get('LRA'),mix_TP=lm.get('true_peak_dBTP',lm.get('TP')),vo_I=a['loudness']['vo_stem_I_LUFS'],music_I=a['loudness']['music_stem_I_LUFS'],gap_by_integrated=a['music_to_vo_gap_dB']['by_integrated'],gap_mean=a['music_to_vo_gap_dB']['mean'],gap_min=a['music_to_vo_gap_dB']['min'],gap_max=a['music_to_vo_gap_dB']['max'],bed_range=a['music_level_stability']['range_dB'],bed_std=a['music_level_stability']['std_dB'])
    tol=dict(mix_I=.3,mix_LRA=.5,mix_TP=.5,vo_I=.3,music_I=.3,gap_by_integrated=.5,gap_mean=.5,gap_min=.5,gap_max=.5,bed_range=.5,bed_std=.5); row={}
    for k in tol:
        if A.get(k) is None: row[k]=dict(A=None,B=B[k]); continue
        o=abs(A[k]-B[k])<=tol[k]; ok+=o; tot+=1; row[k]=dict(A=A[k],B=B[k],ok=bool(o))
        if not o: miss.append((v,k,A[k],B[k]))
    res[v]=row; print(v,{k:(r.get('A'),r['B'],r.get('ok')) for k,r in row.items()})
json.dump(dict(ok=ok,total=tot,rate=round(100*ok/max(tot,1),2),videos=res,misses=miss,raw_loudness_keys='see audio.json'),open(N+'agreement_audio.json','w'),indent=1)
print('AUDIO',ok,tot,round(100*ok/max(tot,1),2)); print(miss)
