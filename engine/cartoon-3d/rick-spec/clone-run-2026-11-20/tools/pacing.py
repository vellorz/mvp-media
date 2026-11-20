#!/usr/bin/env python3
"""pacing.py - scene-time / visual-change / narration-alignment stats, measured identically for every video.
Usage: pacing.py VIDEO JOINS_CSV WORDS OUTDIR [--label NAME]
 JOINS_CSV : csv with header start_frame,len_f,... (1-based first blended frame, blend length in frames; len<=3 = fast join / hard cut)
 WORDS     : either words.tsv (start<TAB>word, punctuation in token if available) or json [[word,start,end],...]
Tools: ffmpeg (decode), OpenCV Farneback optical flow + estimateAffinePartial2D (camera vs object motion), numpy.
All thresholds are fixed constants below so every video is measured the same way.
"""
import sys, os, json, subprocess, re, argparse
import numpy as np, cv2
ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('joins'); ap.add_argument('words'); ap.add_argument('outdir'); ap.add_argument('--label', default=None)
a = ap.parse_args(); os.makedirs(a.outdir, exist_ok=True)
label = a.label or os.path.basename(a.video)
# ---------- constants (identical for all videos)
FW, FH = 135, 240           # flow resolution
CAM_THR = 0.12              # px/frame @135w mean model-flow magnitude -> camera "moving"
OBJ_PROM = 0.10             # prominence of residual (object) motion peaks
MIN_GAP = 6                 # frames between counted events
BAND = (0.655, 0.745)       # caption band (fraction of H); guide: box top 68.9 %, baseline 71.7 %
CAP_W = 0.5                 # XOR/union ratio above which the caption is counted as swapped
def probe(v):
    o = subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_frames','-of','json',v],capture_output=True,text=True).stdout
    s = json.loads(o)['streams'][0]; n,d = s['r_frame_rate'].split('/'); return int(s['width']),int(s['height']),float(n)/float(d)
W,H,FPS = probe(a.video)
def frames(vf, w, h, pix):
    c = 3 if pix!='gray' else 1
    raw = subprocess.run(['ffmpeg','-v','error','-i',a.video,'-vf',vf,'-f','rawvideo','-pix_fmt',pix,'-'],capture_output=True).stdout
    return np.frombuffer(raw,np.uint8).reshape(-1,h,w,c) if c==3 else np.frombuffer(raw,np.uint8).reshape(-1,h,w)
G = frames(f'scale={FW}:{FH}:flags=area', FW, FH, 'gray'); N = len(G); DUR = N/FPS
# ---------- joins -> shots
J = []
with open(a.joins) as f:
    hdr = f.readline().strip().split(',')
    for line in f:
        p = line.strip().split(',')
        if len(p) < 2 or not p[0]: continue
        J.append((int(float(p[0])), int(float(p[1]))))
J.sort()
mids = [s-1 + L/2.0 for s,L in J]            # 0-based frame position of the join midpoint
bounds = [0.0] + mids + [float(N)]
shots = []
for i in range(len(bounds)-1):
    s,e = bounds[i], bounds[i+1]
    shots.append(dict(n=i+1, start_f=int(round(s))+1, end_f=int(round(e)), start_s=round(s/FPS,3), end_s=round(e/FPS,3), dur_s=round((e-s)/FPS,3),
                      join_in=(dict(first_blend_frame=J[i-1][0], len_f=J[i-1][1], type='fast/hard' if J[i-1][1]<=3 else 'dissolve') if i>0 else None)))
D = np.array([s['dur_s'] for s in shots])
def stats(d):
    if len(d)==0: return None
    b = np.round(np.array(d)*2)/2; vals,cnt = np.unique(b, return_counts=True)
    return dict(n=int(len(d)), asl=round(float(np.mean(d)),3), median=round(float(np.median(d)),3), mode_0p5s_bin=float(vals[np.argmax(cnt)]), min=round(float(np.min(d)),3), max=round(float(np.max(d)),3),
                p10=round(float(np.percentile(d,10)),3), p90=round(float(np.percentile(d,90)),3),
                share_lt1=round(float(np.mean(np.array(d)<1)),3), share_lt2=round(float(np.mean(np.array(d)<2)),3), share_gt4=round(float(np.mean(np.array(d)>4)),3))
# ---------- words / sentences / phrases
words = []
if a.words.endswith('.json'):
    rows = [(float(s_), w_) for w_,s_,e_ in json.load(open(a.words))]
    for i,(s_,w_) in enumerate(rows):   # same end-time estimate as for caption-derived word lists, so phrases are split identically for every video
        e_ = min(rows[i+1][0], s_+0.45) if i+1 < len(rows) else s_+0.45
        words.append([w_,s_,e_])
else:
    rows = [l.rstrip('\n').split('\t') for l in open(a.words) if l.strip()]
    rows = [(float(r[0]), r[1]) for r in rows if len(r)>=2 and re.match(r'^[0-9.]+$', r[0])]
    for i,(s,w) in enumerate(rows):
        e = min(rows[i+1][0], s+0.45) if i+1 < len(rows) else s+0.45
        words.append([w,s,e])
sent, phr = [], []; cs, cp = [], []
for i,(w,s,e) in enumerate(words):
    cs.append(i); cp.append(i)
    gap = (words[i+1][1]-e) if i+1 < len(words) else 9
    endS = bool(re.search(r'[.!?]["\')\]]*$', w)); endP = endS or bool(re.search(r'[,;:—-]["\')\]]*$', w)) or gap >= 0.30
    if endS or i==len(words)-1: sent.append(cs); cs=[]
    if endP or i==len(words)-1: phr.append(cp); cp=[]
has_punct = any(re.search(r'[.!?]', w[0]) for w in words)
last_word_start, last_word_end = words[-1][1], words[-1][2]
payoff_start = words[sent[-1][0]][1] if has_punct and len(sent)>1 else max(15.0, last_word_end-6.0)
sections = [('hook_0-3s',0,3.0), ('3-15s',3.0,15.0), ('body',15.0,payoff_start), ('payoff',payoff_start,last_word_end), ('outro',last_word_end,DUR)]
join_t = np.array([m/FPS for m in mids])
def secstats(lo,hi):
    # shots clipped to the section window (time-overlap), plus cut rate in the window
    d = [min(s['end_s'],hi)-max(s['start_s'],lo) for s in shots if min(s['end_s'],hi)-max(s['start_s'],lo) > 0]
    full = [s['dur_s'] for s in shots if lo <= s['start_s'] < hi]
    nj = int(((join_t>=lo)&(join_t<hi)).sum()); L = max(hi-lo,1e-6)
    return dict(window_s=[round(lo,2),round(hi,2)], joins=nj, cuts_per_min=round(nj/L*60,2), seconds_per_cut=(round(L/nj,3) if nj else None),
                shots_starting_here=stats(full), shots_overlapping=len(d), mean_visible_shot_time=round(float(np.mean(d)),3) if d else None)
# ---------- optical flow: camera (global affine model) vs object (residual) motion
cam = np.zeros(N); obj = np.zeros(N); diff = np.zeros(N)
ys,xs = np.mgrid[8:FH:12, 8:FW:12]; pts = np.stack([xs.ravel(),ys.ravel()],1).astype(np.float32)
b0,b1 = int(BAND[0]*FH)-2, int(BAND[1]*FH)+2
keep = (pts[:,1] < b0) | (pts[:,1] > b1)
for i in range(1,N):
    fl = cv2.calcOpticalFlowFarneback(G[i-1],G[i],None,0.5,3,15,3,5,1.2,0)
    v = fl[pts[:,1].astype(int), pts[:,0].astype(int)]
    src = pts[keep]; dst = src + v[keep]
    M,_ = cv2.estimateAffinePartial2D(src,dst,method=cv2.RANSAC,ransacReprojThreshold=0.5)
    if M is None: M = np.array([[1,0,0],[0,1,0]],np.float32)
    model = (src @ M[:,:2].T + M[:,2]) - src
    cam[i] = np.linalg.norm(model,axis=1).mean(); obj[i] = np.linalg.norm(v[keep]-model,axis=1).mean()
    dd = np.abs(G[i].astype(np.int16)-G[i-1].astype(np.int16)); dd[b0:b1] = 0; diff[i] = dd.mean()
inj = np.zeros(N,bool)
for s,L in J: inj[max(s-3,0):min(s+L+2,N)] = True
camc = cam.copy(); objc = obj.copy(); camc[inj] = np.nan; objc[inj] = np.nan
def smooth(x,k=5):
    y = np.nan_to_num(x); return np.convolve(y,np.ones(k)/k,'same')
cs_, os_ = smooth(camc), smooth(objc)
moving = cs_ > CAM_THR
# camera events: move onsets (still->moving) + speed bursts (local maxima of camera speed at >= 2x the running median)
cam_on = [i for i in range(1,N) if moving[i] and not moving[i-1] and not inj[i]]
def peaks(x, prom, mind):
    out=[]; 
    for i in range(2,len(x)-2):
        if x[i]>=x[i-1] and x[i]>x[i+1]:
            lo = min(x[max(0,i-12):i].min(), x[i+1:i+13].min()) if i+1<len(x) else 0
            if x[i]-lo >= prom and (not out or i-out[-1] >= mind): out.append(i)
    return out
cam_burst = [i for i in peaks(cs_, max(0.25, 0.0), MIN_GAP) if not inj[i]]
obj_ev = [i for i in peaks(os_, OBJ_PROM, MIN_GAP) if not inj[i]]
def dedup(ev):
    ev = sorted(set(ev)); out=[]
    for e in ev:
        if not out or e-out[-1] >= MIN_GAP: out.append(e)
    return out
cam_ev = dedup(cam_on + cam_burst)
# still runs (no camera and no object motion)
still = (np.nan_to_num(cam) < 0.04) & (np.nan_to_num(obj) < 0.04) & (diff < 0.35); still[0]=False
runs=[]; r=0
for i in range(N):
    if still[i]: r+=1
    else:
        if r: runs.append(r); r=0
if r: runs.append(r)
# ---------- caption swaps (text pops) in the caption band
bw, bh = 270, int(round((BAND[1]-BAND[0])*480))
C = frames(f'scale=270:480:flags=area,crop=270:{bh}:0:{int(BAND[0]*480)}', 270, bh, 'rgb24')
mask = (C.min(axis=3) > 232)
mask[:, :, :20] = False; mask[:, :, -20:] = False
area = mask.reshape(N,-1).sum(1)
cap_on = area > 40
swaps=[]; cur_start=None; dwell=[]
for i in range(1,N):
    u = (mask[i]|mask[i-1]).sum(); x = (mask[i]^mask[i-1]).sum()
    changed = (u>40) and (x/u > CAP_W) and (cap_on[i] or cap_on[i-1])
    if changed and (not swaps or i-swaps[-1] >= 2):
        if cur_start is not None and cap_on[i-1]: dwell.append((i-cur_start)/FPS)
        swaps.append(i); cur_start = i if cap_on[i] else None
dw = np.array(dwell) if dwell else np.array([0.0])
# ---------- narration alignment
w_on = np.array([w[1] for w in words]); p_on = np.array([words[p[0]][1] for p in phr]); s_on = np.array([words[s[0]][1] for s in sent])
def nearest(t, arr): return float(arr[np.argmin(np.abs(arr-t))]-t) if len(arr) else None
al = []
for (s,L),m in zip(J,mids):
    t0 = (s-1)/FPS; tm = m/FPS
    al.append(dict(first_blend_frame=s, len_f=L, mid_s=round(tm,3), start_to_word_onset_f=round(nearest(t0,w_on)*FPS,1), start_to_phrase_onset_f=round(nearest(t0,p_on)*FPS,1), start_to_sentence_onset_f=round(nearest(t0,s_on)*FPS,1), to_word_onset_f=round(nearest(tm,w_on)*FPS,1), to_phrase_onset_f=round(nearest(tm,p_on)*FPS,1), to_sentence_onset_f=round(nearest(tm,s_on)*FPS,1)))
def within(key,k): return round(float(np.mean([abs(x[key])<=k for x in al])),3) if al else None
per_sent = [int(((join_t>=words[s[0]][1])&(join_t<(words[sent[i+1][0]][1] if i+1<len(sent) else DUR))).sum()) for i,s in enumerate(sent)]
per_phr = [int(((join_t>=words[p[0]][1])&(join_t<(words[phr[i+1][0]][1] if i+1<len(phr) else DUR))).sum()) for i,p in enumerate(phr)]
# ---------- pacing curve (10 equal time deciles + 5 s bins)
def curve(edges):
    out=[]
    for lo,hi in zip(edges[:-1],edges[1:]):
        f0,f1 = int(lo*FPS), max(int(hi*FPS),int(lo*FPS)+1); L=hi-lo
        nj = int(((join_t>=lo)&(join_t<hi)).sum())
        ce = sum(1 for e in cam_ev if f0<=e<f1); oe = sum(1 for e in obj_ev if f0<=e<f1); sw = sum(1 for e in swaps if f0<=e<f1)
        out.append(dict(t=[round(lo,2),round(hi,2)], joins=nj, cuts_per_min=round(nj/L*60,1), cam_events=ce, obj_events=oe, caption_swaps=sw,
                        changes_per_s_no_captions=round((nj+ce+oe)/L,2), changes_per_s_all=round((nj+ce+oe+sw)/L,2),
                        cam_speed=round(float(np.nanmean(camc[f0:f1])) if np.isfinite(camc[f0:f1]).any() else 0,3), obj_motion=round(float(np.nanmean(objc[f0:f1])) if np.isfinite(objc[f0:f1]).any() else 0,3)))
    return out
res = dict(label=label, video=os.path.basename(a.video), width=W, height=H, fps=FPS, frames=N, duration_s=round(DUR,3),
    tool='pacing.py (ffmpeg decode; joins from JOINS_CSV; OpenCV Farneback flow + RANSAC partial-affine camera model; caption-band white-mask XOR)',
    joins=dict(n=len(J), per_10s=round(len(J)/DUR*10,2), dissolves=sum(1 for _,L in J if L>3), fast_or_hard=sum(1 for _,L in J if L<=3), dissolve_len_median_f=(float(np.median([L for _,L in J if L>3])) if any(L>3 for _,L in J) else None)),
    shots_all=dict(stats(D), shots_per_min=round(len(D)/DUR*60,2)),
    sections={k:secstats(lo,hi) for k,lo,hi in sections if hi>lo},
    captions=dict(swaps=len(swaps), swaps_per_s=round(len(swaps)/DUR,2), dwell_s=dict(mean=round(float(dw.mean()),3), median=round(float(np.median(dw)),3), p10=round(float(np.percentile(dw,10)),3), p90=round(float(np.percentile(dw,90)),3), max=round(float(dw.max()),3)), caption_on_share=round(float(cap_on.mean()),3)),
    visual_change=dict(joins=len(J), camera_events=len(cam_ev), object_events=len(obj_ev), caption_swaps=len(swaps),
        changes_per_min_no_captions=round((len(J)+len(cam_ev)+len(obj_ev))/DUR*60,1), changes_per_min_all=round((len(J)+len(cam_ev)+len(obj_ev)+len(swaps))/DUR*60,1),
        mean_gap_between_changes_s_no_captions=round(DUR/max(len(J)+len(cam_ev)+len(obj_ev),1),3),
        camera_moving_share=round(float(np.nanmean((camc>CAM_THR)[~inj])),3), camera_speed_median=round(float(np.nanmedian(camc)),3), camera_speed_p90=round(float(np.nanpercentile(camc,90)),3),
        object_motion_median=round(float(np.nanmedian(objc)),3), still_frame_share=round(float(still.mean()),3), longest_still_run_f=int(max(runs) if runs else 0), still_runs_over_15f=int(sum(1 for r in runs if r>15))),
    narration=dict(words=len(words), words_per_s=round(len(words)/max(last_word_end-words[0][1],1e-6),2), sentences=len(sent), phrases=len(phr), punctuation_in_transcript=has_punct,
        cuts_per_sentence=round(len(J)/max(len(sent),1),2), cuts_per_phrase=round(len(J)/max(len(phr),1),2), sentences_with_0_cuts=int(sum(1 for x in per_sent if x==0)), max_cuts_in_one_sentence=int(max(per_sent) if per_sent else 0),
        seconds_per_sentence=round((last_word_end-words[0][1])/max(len(sent),1),2), seconds_per_phrase=round((last_word_end-words[0][1])/max(len(phr),1),2),
        join_start_within_2f_of_word_onset=within('start_to_word_onset_f',2), join_start_within_3f_of_phrase_onset=within('start_to_phrase_onset_f',3), join_start_within_6f_of_phrase_onset=within('start_to_phrase_onset_f',6), join_start_within_6f_of_sentence_onset=within('start_to_sentence_onset_f',6), chance_within_2f_of_word_onset=round(min(1.0, len(words)*(5/FPS)/max(last_word_end-words[0][1],1e-6)),3),
        join_mid_within_3f_of_word_onset=within('to_word_onset_f',3), join_mid_within_3f_of_phrase_onset=within('to_phrase_onset_f',3), join_mid_within_6f_of_phrase_onset=within('to_phrase_onset_f',6), join_mid_within_6f_of_sentence_onset=within('to_sentence_onset_f',6),
        last_word_start_s=round(last_word_start,3), end_after_last_word_start_s=round(DUR-last_word_start,3), payoff_start_s=round(payoff_start,3)),
    pacing_curve_deciles=curve(list(np.linspace(0,DUR,11))), pacing_curve_5s=curve(list(np.arange(0,DUR,5.0))+[DUR]),
    shots=shots, join_alignment=al, per_sentence_cuts=per_sent, events=dict(camera_event_frames=[int(e)+1 for e in cam_ev], object_event_frames=[int(e)+1 for e in obj_ev], caption_swap_frames=[int(e)+1 for e in swaps]))
json.dump(res, open(os.path.join(a.outdir,'pacing.json'),'w'), indent=1)
np.savetxt(os.path.join(a.outdir,'motion_per_frame.csv'), np.stack([np.arange(1,N+1),cam,obj,diff,cap_on.astype(int)],1), fmt=['%d','%.4f','%.4f','%.3f','%d'], delimiter=',', header='frame,camera_speed,object_motion,framediff,caption_on', comments='')
print(json.dumps({k:res[k] for k in ['label','frames','duration_s','joins','shots_all','captions','visual_change']}, indent=1)); print(json.dumps(res['narration'])); print({k:(v['joins'],v['cuts_per_min']) for k,v in res['sections'].items()})
