#!/usr/bin/env python3
"""audio.py - music / VO / SFX measurements, identical for every video.
Usage: audio.py LABEL MIX.wav VOCALS.wav MUSIC.wav PACING.json OUTDIR [--sfx SFX.wav]
 MIX/VOCALS/MUSIC: for Rick videos = rea-video stems (original.wav, vocals.wav, music.wav; the 'music' stem = music + SFX, they cannot be separated further).
Tools: pyloudnorm (ITU-R BS.1770 K-weighted loudness), ffmpeg ebur128 (LRA, true peak), librosa (beat_track, tempo, chroma_cqt, onset_strength, HPSS, agglomerative segmentation), numpy.
Heuristic event classes (riser / impact / whoosh / break) are signal-level candidates and are tagged [heuristic] wherever reported.
"""
import sys, os, json, subprocess, re, argparse, warnings
warnings.filterwarnings('ignore')
import numpy as np, librosa, pyloudnorm as pyln, soundfile as sf
ap = argparse.ArgumentParser(); ap.add_argument('label'); ap.add_argument('mix'); ap.add_argument('vocals'); ap.add_argument('music'); ap.add_argument('pacing'); ap.add_argument('outdir'); ap.add_argument('--sfx', default=None)
a = ap.parse_args(); os.makedirs(a.outdir, exist_ok=True)
SR = 22050
def load(p):
    y, sr = sf.read(p, always_2d=True); return y.astype(np.float64), sr
def lufs(y, sr):
    try:
        v = pyln.Meter(sr).integrated_loudness(y); return round(float(v),2) if np.isfinite(v) else None
    except Exception: return None
def ebur(p):
    e = subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',p,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
    tail = e[e.rfind('Summary:'):] if 'Summary:' in e else ''
    g = lambda k: (float(re.search(k+r'\s*(-?[0-9.]+)',tail).group(1)) if re.search(k+r'\s*(-?[0-9.]+)',tail) else None)
    return dict(I_LUFS=g(r'I:'), LRA_LU=g(r'LRA:'), true_peak_dBTP=g(r'Peak:'))
def st_curve(y, sr, win=3.0, hop=0.5):
    m = pyln.Meter(sr, block_size=0.4); n = len(y); out=[]; t=0.0
    while t+win <= n/sr+1e-6:
        seg = y[int(t*sr):int((t+win)*sr)]
        try: v = m.integrated_loudness(seg)
        except Exception: v = -np.inf
        out.append((round(t+win/2,2), float(v) if np.isfinite(v) else -70.0)); t += hop
    return out
def env_db(y, sr, hop_s=0.05):
    mono = y.mean(axis=1); h = int(sr*hop_s); n = len(mono)//h
    r = np.sqrt((mono[:n*h].reshape(n,h)**2).mean(1)+1e-12); return 20*np.log10(r+1e-9)
mix, sr = load(a.mix); voc, _ = load(a.vocals); mus, _ = load(a.music)
DUR = len(mix)/sr
P = json.load(open(a.pacing)); FPS = P['fps']
res = dict(label=a.label, duration_s=round(DUR,3), tool='audio.py (pyloudnorm BS.1770, ffmpeg ebur128, librosa %s)' % librosa.__version__, stems=dict(mix=a.mix, vocals=a.vocals, music=a.music, sfx=a.sfx))
# ---------- loudness
res['loudness'] = dict(mix=ebur(a.mix), vo_stem_I_LUFS=lufs(voc,sr), music_stem_I_LUFS=lufs(mus,sr))
if a.sfx:
    sfx,_ = load(a.sfx); res['loudness']['sfx_stem_I_LUFS'] = lufs(sfx,sr)
    e = env_db(sfx,sr); res['loudness']['sfx_active_share'] = round(float((e>-50).mean()),3)
vs = st_curve(voc,sr); ms = st_curve(mus,sr); xs = st_curve(mix,sr)
gap = [(t, v-m) for (t,v),(_,m) in zip(vs,ms) if v>-50 and m>-69]
g = np.array([x[1] for x in gap]) if gap else np.array([0.0])
mm = np.array([m for _,m in ms]); mmv = mm[mm>-69] if (mm>-69).any() else mm
res['music_to_vo_gap_dB'] = dict(mean=round(float(g.mean()),2), median=round(float(np.median(g)),2), min=round(float(g.min()),2), max=round(float(g.max()),2), std=round(float(g.std()),2),
    by_integrated=(round(res['loudness']['vo_stem_I_LUFS']-res['loudness']['music_stem_I_LUFS'],2) if res['loudness']['vo_stem_I_LUFS'] and res['loudness']['music_stem_I_LUFS'] else None),
    curve_3s_window=[(t, round(x,1)) for t,x in gap][::2])
res['music_level_curve_LUFS_3s'] = [(t, round(m,1)) for t,m in ms][::2]
res['vo_level_curve_LUFS_3s'] = [(t, round(v,1)) for t,v in vs][::2]
res['music_level_stability'] = dict(std_dB=round(float(mmv.std()),2), range_dB=round(float(mmv.max()-mmv.min()),2), max_step_per_0p5s_dB=round(float(np.abs(np.diff(mmv)).max()) if len(mmv)>1 else 0,2))
# ---------- ducking
ev, em = env_db(voc,sr), env_db(mus,sr); n = min(len(ev),len(em)); ev, em = ev[:n], em[:n]
vo_on = ev > (np.percentile(ev,90)-25)
k = 6; sm = np.convolve(em, np.ones(k)/k, 'same')
duck = dict(vo_active_share=round(float(vo_on.mean()),3),
    music_dB_while_vo=round(float(sm[vo_on].mean()),2) if vo_on.any() else None, music_dB_in_vo_gaps=round(float(sm[~vo_on].mean()),2) if (~vo_on).any() else None,
    envelope_correlation_vo_vs_music=round(float(np.corrcoef(ev,sm)[0,1]),3))
duck['duck_depth_dB'] = (round(duck['music_dB_in_vo_gaps']-duck['music_dB_while_vo'],2) if duck['music_dB_while_vo'] is not None and duck['music_dB_in_vo_gaps'] is not None else None)
duck['note'] = 'duck_depth > +3 dB with negative correlation = audible ducking/pumping; near 0 = constant bed. On separated stems, VO bleed into the music stem biases depth toward 0 or negative [uncertain +/-2 dB].'
res['ducking'] = duck
# ---------- music analysis on the music stem
y = librosa.load(a.music, sr=SR, mono=True)[0]
hop = 512
oenv = librosa.onset.onset_strength(y=y, sr=SR, hop_length=hop)
tempo, beats = librosa.beat.beat_track(onset_envelope=oenv, sr=SR, hop_length=hop)
tempo = float(np.atleast_1d(tempo)[0]); bt = librosa.frames_to_time(beats, sr=SR, hop_length=hop)
tg = librosa.feature.tempo(onset_envelope=oenv, sr=SR, hop_length=hop, aggregate=None)
tt = librosa.frames_to_time(np.arange(len(tg)), sr=SR, hop_length=hop)
tcurve = [(int(lo), round(float(np.median(tg[(tt>=lo)&(tt<lo+10)])),1)) for lo in range(0,int(DUR),10) if ((tt>=lo)&(tt<lo+10)).any()]
ac = librosa.autocorrelate(oenv, max_size=len(oenv)//2); 
tempi = librosa.feature.tempo(onset_envelope=oenv, sr=SR, hop_length=hop, aggregate=np.mean)
ibi = np.diff(bt) if len(bt)>2 else np.array([0.0])
res['tempo'] = dict(bpm_beat_track=round(tempo,1), bpm_tempogram_mean=round(float(np.atleast_1d(tempi)[0]),1), half_time=round(tempo/2,1), double_time=round(tempo*2,1), beats=len(bt),
    inter_beat_std_ms=round(float(ibi.std()*1000),1), bpm_per_10s=tcurve, bpm_change=('none (curve range <= 4 BPM)' if tcurve and max(x[1] for x in tcurve)-min(x[1] for x in tcurve) <= 4 else 'see bpm_per_10s (may be octave jumps of the estimator) [uncertain]'),
    note='octave ambiguity (x2 / /2) is inherent; the pulse felt is the value nearest 80-160')
yh, yp = librosa.effects.hpss(y)
chroma = librosa.feature.chroma_cqt(y=yh, sr=SR, hop_length=hop).mean(axis=1)
maj = np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88]); mnr = np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']; cand=[]
for i in range(12):
    cand.append((float(np.corrcoef(np.roll(maj,i),chroma)[0,1]), names[i]+' major')); cand.append((float(np.corrcoef(np.roll(mnr,i),chroma)[0,1]), names[i]+' minor'))
cand.sort(reverse=True)
res['key'] = dict(best=cand[0][1], score=round(cand[0][0],3), second=cand[1][1], second_score=round(cand[1][0],3), confidence=('ok' if cand[0][0]-cand[1][0] > 0.05 and cand[0][0] > 0.6 else '[uncertain]'), chroma_profile={n:round(float(c),3) for n,c in zip(names,chroma/chroma.max())})
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop))**2; fr = librosa.fft_frequencies(sr=SR, n_fft=2048); tot = S.sum()+1e-12
band = lambda lo,hi: round(float(S[(fr>=lo)&(fr<hi)].sum()/tot),3)
res['timbre'] = dict(energy_share=dict(sub_lt60=band(0,60), bass_60_250=band(60,250), lowmid_250_1k=band(250,1000), mid_1k_4k=band(1000,4000), high_gt4k=band(4000,12000)),
    spectral_centroid_hz=round(float(librosa.feature.spectral_centroid(S=np.sqrt(S), sr=SR).mean()),0), percussive_to_harmonic_energy=round(float((yp**2).sum()/((yh**2).sum()+1e-12)),3),
    spectral_flatness=round(float(librosa.feature.spectral_flatness(y=y).mean()),4), note='instrument names cannot be measured from these numbers; instrumentation lines in the reports are [uncertain] unless stated otherwise')
on = librosa.onset.onset_detect(onset_envelope=oenv, sr=SR, hop_length=hop, units='time')
onf = librosa.onset.onset_detect(onset_envelope=oenv, sr=SR, hop_length=hop)
ostr = oenv[onf] if len(onf) else np.array([0.0]); thr = np.percentile(ostr,80) if len(ostr) else 0
strong = on[ostr>=thr] if len(on) else np.array([])
res['onsets'] = dict(n=len(on), per_s=round(len(on)/DUR,2), strong_n=int(len(strong)), strong_per_10s=round(len(strong)/DUR*10,2))
# off-grid strong onsets = SFX candidates (music+SFX share the stem)
if len(bt) > 2:
    period = np.median(ibi); grid = np.concatenate([bt + k*period/4 for k in range(4)])
    offg = np.array([o for o in strong if np.min(np.abs(grid-o)) > 0.045])
else: offg = strong
res['sfx_candidates'] = dict(strong_onsets_off_16th_grid=int(len(offg)), per_10s=round(len(offg)/DUR*10,2), times_s=[round(float(x),2) for x in offg], tag='[heuristic] music and SFX share one stem; listen-check needed')
# low impacts, risers, whooshes, breaks  [heuristic]
rms = librosa.feature.rms(y=y, hop_length=hop)[0]; rt = librosa.frames_to_time(np.arange(len(rms)), sr=SR, hop_length=hop); rdb = 20*np.log10(rms+1e-9)
low = 10*np.log10(S[(fr<150)].sum(0)+1e-9); lenv = np.maximum(0,np.diff(low,prepend=low[0])); lo_on = librosa.onset.onset_detect(onset_envelope=lenv, sr=SR, hop_length=hop, units='time', delta=6.0, wait=6); lo_on = np.array([t for t in lo_on if low[min(int(t*SR/hop)+2,len(low)-1)] > np.percentile(low,75)])
hi = 10*np.log10(S[(fr>3000)].sum(0)+1e-12); k=int(0.7*SR/hop); ris=[]
for i in range(k, len(hi)-1, max(k//4,1)):
    seg = hi[i-k:i]; sl = np.polyfit(np.arange(k), seg, 1)[0]*k
    if sl > 9 and np.corrcoef(np.arange(k),seg)[0,1] > 0.8 and (not ris or rt[i]-ris[-1] > 1.0): ris.append(float(rt[i]))
flat = librosa.feature.spectral_flatness(S=np.sqrt(S))[0]; wh=[]; run=0
for i,f in enumerate(flat):
    if f > 0.12 and rdb[i] > np.median(rdb)-6: run += 1
    else:
        if 0.15 <= run*hop/SR <= 1.0: wh.append(float(rt[i-run]))
        run = 0
med = np.median(rdb); br=[]; run=0
for i,v in enumerate(rdb):
    if v < med-12: run += 1
    else:
        if run*hop/SR >= 0.25: br.append((round(float(rt[i-run]),2), round(run*hop/SR,2)))
        run = 0
res['events_heuristic'] = dict(low_impacts_n=len(lo_on), low_impacts_s=[round(float(x),2) for x in lo_on][:80], risers_end_s=[round(x,2) for x in ris], noise_bursts_whoosh_candidates_s=[round(x,2) for x in wh][:80], breaks_start_dur_s=br, silence_share_music_below_minus12dB_rel=round(float((rdb<med-12).mean()),3), tag='[heuristic]')
# energy curve + structure
res['energy_curve_music_dB_per_s'] = [round(float(rdb[(rt>=s)&(rt<s+1)].mean()),1) for s in range(int(DUR))]
ym = librosa.load(a.mix, sr=SR, mono=True)[0]; rm = 20*np.log10(librosa.feature.rms(y=ym, hop_length=hop)[0]+1e-9)
res['energy_curve_mix_dB_per_s'] = [round(float(rm[(rt[:len(rm)]>=s)&(rt[:len(rm)]<s+1)].mean()),1) for s in range(int(DUR))]
try:
    feat = np.vstack([librosa.feature.chroma_cqt(y=y, sr=SR, hop_length=hop), librosa.feature.mfcc(y=y, sr=SR, hop_length=hop, n_mfcc=13)])
    fs = librosa.util.sync(feat, beats) if len(beats) > 16 else feat
    kseg = 6; bnd = librosa.segment.agglomerative(fs, kseg)
    btimes = (bt[np.clip(bnd,0,len(bt)-1)] if len(beats) > 16 else librosa.frames_to_time(bnd, sr=SR, hop_length=hop))
    secs=[]; bl = list(btimes)+[DUR]
    for i in range(len(btimes)):
        m = (rt>=bl[i])&(rt<bl[i+1]); secs.append(dict(start_s=round(float(bl[i]),2), end_s=round(float(bl[i+1]),2), mean_dB=round(float(rdb[m].mean()),1) if m.any() else None, onset_per_s=round(float(((on>=bl[i])&(on<bl[i+1])).sum()/max(bl[i+1]-bl[i],1e-6)),2)))
    res['structure_sections'] = secs
    # loop length: best beat-synchronous chroma self-similarity lag (in beats)
    if len(beats) > 40:
        cs = librosa.util.normalize(librosa.util.sync(librosa.feature.chroma_cqt(y=yh, sr=SR, hop_length=hop), beats), axis=0); best=[]
        for lag in (4,8,12,16,24,32):
            if cs.shape[1] > lag+8: best.append((round(float((cs[:,lag:]*cs[:,:-lag]).sum(0).mean()),3), lag))
        best.sort(reverse=True); res['loop'] = dict(similarity_by_lag_beats=best, most_likely_loop_beats=best[0][1] if best else None, loop_seconds=round(best[0][1]*float(np.median(ibi)),2) if best else None, tag='[heuristic]')
except Exception as e: res['structure_sections'] = 'failed: %s' % e
# ---------- first 3 seconds
first = {}
for lo,hi_ in ((0,0.25),(0.25,0.5),(0.5,1),(1,2),(2,3)):
    m = (rt>=lo)&(rt<hi_); first['music_dB_%s-%ss'%(lo,hi_)] = round(float(rdb[m].mean()),1)
first['music_median_dB_whole'] = round(float(med),1); first['first_music_onset_s'] = round(float(on[0]),3) if len(on) else None
first['time_music_reaches_median_minus3dB_s'] = round(float(rt[np.argmax(rdb >= med-3)]),3)
first['first_strong_onset_s'] = round(float(strong[0]),3) if len(strong) else None
ev50 = env_db(voc,sr,0.01); first['vo_first_sound_s'] = round(float(np.argmax(ev50 > np.percentile(ev50,90)-25)*0.01),2)
res['first_3s'] = first
# ---------- sync of cuts / camera events / caption swaps to beats and strong onsets
rng = np.random.default_rng(7)
def sync(times, ref, tol=2/30.0):
    times = np.array(times, float); ref = np.array(ref, float)
    if len(times)==0 or len(ref)==0: return None
    d = np.array([np.min(np.abs(ref-t)) for t in times]); hit = float((d<=tol).mean())
    ch = np.mean([np.mean([np.min(np.abs(ref-((t+s)%DUR)))<=tol for t in times]) for s in rng.uniform(0.3,DUR-0.3,200)])
    return dict(n=len(times), within_2f=round(hit,3), chance=round(float(ch),3), lift=round(hit/max(ch,1e-6),2), median_abs_offset_f=round(float(np.median(d)*30),1))
jt = [j['mid_s'] for j in P['join_alignment']]; js = [(j['first_blend_frame']-1)/FPS for j in P['join_alignment']]
ce = [(f-1)/FPS for f in P['events']['camera_event_frames']]; oe = [(f-1)/FPS for f in P['events']['object_event_frames']]; cp = [(f-1)/FPS for f in P['events']['caption_swap_frames']]
res['sync'] = dict(tolerance='+/-2 frames (0.067 s); lift = hit share / chance share (200 random time shifts); lift ~1 = no sync',
    join_mid_to_beat=sync(jt,bt), join_start_to_beat=sync(js,bt), join_mid_to_strong_onset=sync(jt,strong), join_start_to_strong_onset=sync(js,strong), join_mid_to_any_onset=sync(jt,on),
    camera_event_to_strong_onset=sync(ce,strong), camera_event_to_beat=sync(ce,bt), object_event_to_strong_onset=sync(oe,strong), caption_swap_to_beat=sync(cp,bt), caption_swap_to_strong_onset=sync(cp,strong),
    join_mid_to_low_impact=sync(jt,lo_on), join_mid_to_sfx_candidate=sync(jt,offg))
res['beats_s'] = [round(float(x),3) for x in bt]; res['strong_onsets_s'] = [round(float(x),3) for x in strong]
json.dump(res, open(os.path.join(a.outdir,'audio.json'),'w'), indent=1)
show = {k:res[k] for k in ['label','loudness','music_to_vo_gap_dB','music_level_stability','ducking','tempo','key','timbre','onsets','sfx_candidates','first_3s','sync']}
show['music_to_vo_gap_dB'] = {k:v for k,v in show['music_to_vo_gap_dB'].items() if k!='curve_3s_window'}; show['key'] = {k:v for k,v in show['key'].items() if k!='chroma_profile'}; show['tempo'] = {k:v for k,v in show['tempo'].items()}
print(json.dumps(show, indent=1))
