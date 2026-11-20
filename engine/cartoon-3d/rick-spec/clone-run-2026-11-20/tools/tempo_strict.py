import sys,json,numpy as np,librosa
out={}
for lab,p in [a.split('=') for a in sys.argv[1:]]:
    y,sr=librosa.load(p,sr=22050,mono=True)
    r={}
    for hop in (512,256):
        oe=librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
        t,b=librosa.beat.beat_track(onset_envelope=oe,sr=sr,hop_length=hop)
        bt=librosa.frames_to_time(b,sr=sr,hop_length=hop); ibi=np.diff(bt)
        r[f'beat_track_hop{hop}']=round(float(np.atleast_1d(t)[0]),2)
        r[f'median_ibi_bpm_hop{hop}']=round(60/float(np.median(ibi)),2) if len(ibi) else None
        r[f'ibi_std_ms_hop{hop}']=round(float(np.std(ibi)*1000),1) if len(ibi) else None
        r[f'feature_tempo_hop{hop}']=round(float(np.atleast_1d(librosa.feature.tempo(onset_envelope=oe,sr=sr,hop_length=hop))[0]),2)
        ac=librosa.autocorrelate(oe-oe.mean(),max_size=int(2.0*sr/hop)); lo=int(0.3*sr/hop)
        k=lo+int(np.argmax(ac[lo:])); r[f'autocorr_bpm_hop{hop}']=round(60/(k*hop/sr),2)
    out[lab]=r; print(lab,json.dumps(r),flush=True)
json.dump(out,open('/root/work/meas/tempo_strict.json','w'),indent=1)
