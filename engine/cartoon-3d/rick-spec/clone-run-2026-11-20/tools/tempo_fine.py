import sys,json,numpy as np,librosa
out={}
for lab,p in [a.split('=') for a in sys.argv[1:]]:
    y,sr=librosa.load(p,sr=22050,mono=True); r={}
    for hop in (512,256,128):
        oe=librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
        # fine tempo: autocorrelation of onset envelope, parabolic-interpolated peak in 70-140 BPM, plus comb score
        ac=librosa.autocorrelate(oe-oe.mean()); f=sr/hop
        lo,hi=int(f*60/140),int(f*60/70)
        k=lo+int(np.argmax(ac[lo:hi])); a,b,c=ac[k-1],ac[k],ac[k+1]; d=0.5*(a-c)/(a-2*b+c)
        r[f'acf_peak_bpm_hop{hop}']=round(float(60*f/(k+d)),2)
        t,bf=librosa.beat.beat_track(onset_envelope=oe,sr=sr,hop_length=hop)
        bt=librosa.frames_to_time(bf,sr=sr,hop_length=hop)
        s=np.polyfit(np.arange(len(bt)),bt,1)[0]; r[f'beat_regress_bpm_hop{hop}']=round(float(60/s),2)
    out[lab]=r; print(lab,json.dumps(r),flush=True)
json.dump(out,open('/root/work/meas/tempo_fine.json','w'),indent=1)
