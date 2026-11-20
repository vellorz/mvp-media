#!/usr/bin/env python3
"""synth.py -> new-analysis-2/SYNTH_7videos.json + SYNTH_7videos.md : cross-video numbers for the guide addendum.
Every number comes from the per-video files named in each section."""
import json, csv, os, statistics as st, re
from collections import defaultdict, Counter
N = '/mnt/project-files/modern-vista-social/research/rick-style-spec/new-analysis-2/'
V = ['03_7xS87iActkU', '12_0m6G8pDtzNs', '04_Mz72MuPgnGY', '10_GM9UKnZ6JFw', '14_VS1Z_Q-Klt8', '22_i4hYq1oSXTg', '24_aD73kaL_PtY']
def J(p):
    try: return json.load(open(p))
    except Exception: return None
def q(xs, d=2):
    xs = sorted(x for x in xs if isinstance(x, (int, float)))
    if not xs: return None
    g = lambda p: round(xs[min(len(xs)-1, int(p*(len(xs)-1)+0.5))], d)
    return dict(n=len(xs), min=round(xs[0], d), p10=g(.1), p25=g(.25), median=round(st.median(xs), d), p75=g(.75), p90=g(.9), max=round(xs[-1], d), mean=round(st.mean(xs), d))
out = dict(videos={}); allc = defaultdict(list); md = []
words = {}
for v in V:
    M = J(N+v+'/merged.json'); 
    if not M: continue
    R = dict(frames=M['frames_viewed']); nf = M['frames_viewed']
    # joins
    jv = N+v+'/joins.verified.csv'; jr = list(csv.DictReader(open(jv))) if os.path.exists(jv) else [dict(start_frame=j['first_blend_frame'], len_f=j['len_f'], type=j['type']) for j in M['joins']]
    kinds = Counter('hard cut' if 'cut' in r['type'] else ('match dissolve' if 'match' in r['type'] else ('dissolve' if 'dissolve' in r['type'] else r['type'])) for r in jr)
    R['joins'] = dict(n=len(jr), kinds=dict(kinds), verified=os.path.exists(jv))
    bf = N+v+'/blendfit/joins_blendfit_auto.csv'
    if os.path.exists(bf):
        rows = list(csv.DictReader(open(bf))); L = [int(r['auto_len']) for r in rows if r['flag'] == 'ok' and 'cut' not in (r.get('type') or '')]
        R['dissolve_len_fit_ok'] = q(L, 1); allc['dissolve_len_fit_ok'] += L; R['dissolve_len_fit_list'] = L
    Le = [int(r['len_f']) for r in jr if 'dissolve' in r['type']]; R['dissolve_len_eye_A'] = q(Le, 1); allc['dissolve_len_eye_A'] += Le
    starts = [1]+[int(r['start_frame'])+int(r['len_f'])//2 for r in jr]+[nf+1]; sl = [(b-a)/30 for a, b in zip(starts, starts[1:])]
    R['shot_len_s'] = q(sl); R['shot_len_list'] = [round(x, 2) for x in sl]; allc['shot_len_s'] += sl
    R['first_shot_s'] = round(sl[0], 2); R['last_shot_s'] = round(sl[-1], 2); R['share_lt2'] = round(sum(x < 2 for x in sl)/len(sl), 3); R['share_gt4'] = round(sum(x > 4 for x in sl)/len(sl), 3)
    # pacing / audio / camera
    P = J(N+v+'/pacing.json')
    if P: R['pacing'] = dict(shots=P['shots_all'], narration={k: P['narration'][k] for k in ('words', 'words_per_s', 'sentences', 'end_after_last_word_start_s', 'join_mid_within_3f_of_word_onset', 'join_start_within_6f_of_phrase_onset', 'cuts_per_sentence')}, captions=P['captions'], sections={k: s for k, s in P['sections'].items()}, visual={k: P['visual_change'][k] for k in ('changes_per_min_no_captions', 'still_frame_share', 'longest_still_run_f')})
    for tag in ('audio_nonvocal', 'audio_musiconly'):
        A = J(N+v+'/'+tag+'/audio.json')
        if A: R[tag] = dict(mix=A['loudness']['mix'], vo=A['loudness']['vo_stem_I_LUFS'], music=A['loudness']['music_stem_I_LUFS'], gap={k: A['music_to_vo_gap_dB'][k] for k in ('mean', 'median', 'min', 'max', 'std')}, stability=A['music_level_stability'], duck=A['ducking']['duck_depth_dB'], tempo=A['tempo']['bpm_beat_track'], key=A['key']['best'], key_score=A['key']['score'], key_conf=A['key']['confidence'])
    for t in 'AB':
        C = J(N+v+'/camstats'+t+'.json')
        if C: R['cam'+t] = dict(moving_share=C['moving_share'], n_moves=sum(len(s.get('moves', [])) for s in C['shots']))
    CA = J(N+v+'/cam_agreement.json')
    if CA: R['cam_agreement'] = dict(rate=CA['rate'], per_field=CA['per_field'])
    # camera moves from analysts
    cm = M['camera_moves']; R['cam_moves_A'] = dict(n=len(cm), types=dict(Counter(re.split(r'[ +/,(]', (m.get('type') or '?').lower())[0] for m in cm).most_common(12)), easing=dict(Counter((m.get('easing') or '?').lower().split(' ')[0].split('(')[0] for m in cm).most_common(8)), dur_f=q([m['end_f']-m['start_f']+1 for m in cm if m.get('end_f') and m.get('start_f')], 0), scale_in=q([m['scale_ratio'] for m in cm if (m.get('scale_ratio') or 0) > 1.0]), scale_out=q([m['scale_ratio'] for m in cm if 0 < (m.get('scale_ratio') or 0) < 1.0]), follows=sum(1 for m in cm if m.get('follows')))
    for m in cm:
        if m.get('end_f') and m.get('start_f'): allc['cam_move_dur_f'].append(m['end_f']-m['start_f']+1)
        s = m.get('scale_ratio') or 0
        if s > 1: allc['cam_scale_in'].append(s)
        elif 0 < s < 1: allc['cam_scale_out'].append(s)
        allc['cam_ease'].append((m.get('easing') or '?').lower().split(' ')[0].split('(')[0]); allc['cam_follow'].append(bool(m.get('follows')))
    sh = [s for s in M['shots'] if s.get('complete_in_range')]; hs = [s['hold_frames']/(s['hold_frames']+s['moving_frames']) for s in sh if (s.get('hold_frames') is not None and s.get('moving_frames'))]
    R['hold_share_per_shot_A'] = q(hs, 3); allc['hold_share_A'] += hs
    pr = [s['parallax_ratio'] for s in M['shots'] if s.get('parallax_ratio')]; R['parallax_A'] = q(pr); allc['parallax'] += pr
    # characters
    ch = M['characters']; R['characters_n'] = len(ch); B = J(N+v+'/measurerB_motion.json'); Bc = {c['id']: c for c in (B or {}).get('characters', [])}
    for i, c in enumerate(ch):
        for f in ('head_aspect', 'torso_h_H', 'torso_w_H', 'leg_len_H', 'total_h_H', 'hand_pct_H', 'foot_pct_H', 'eye_size_pct_H', 'eye_spacing_pct_H'):
            if isinstance(c.get(f), (int, float)): allc['A.'+f].append(c[f])
            b = Bc.get(i, {}).get(f)
            if isinstance(b, (int, float)): allc['B.'+f].append(b)
        H = c.get('H_px')
        if H: allc['A.H_pct_W'].append(100*H/1080)
        if H and c.get('arm_thick_px'): allc['A.limb_pct_H'].append(100*c['arm_thick_px']/H)
        if H and c.get('outline_px'): allc['A.outline_pct_H'].append(100*c['outline_px']/H)
        b = Bc.get(i, {})
        if b.get('H_px') and b.get('arm_thick_px'): allc['B.limb_pct_H'].append(100*b['arm_thick_px']/b['H_px'])
        if b.get('H_px') and b.get('outline_px'): allc['B.outline_pct_H'].append(100*b['outline_px']/b['H_px'])
        if b.get('H_px') and b.get('outline_px_shaded'): allc['B.outline_shaded_pct_H'].append(100*b['outline_px_shaded']/b['H_px'])
        allc['A.arm_class'].append(nc := re.sub(r'\s*[\(,;].*', '', str(c.get('arm_class')).lower())); allc['A.leg_class'].append(re.sub(r'\s*[\(,;].*', '', str(c.get('leg_class')).lower())); allc['A.fingers'].append(bool(c.get('fingers'))); allc['A.shading'].append(str(c.get('shading')).lower()[:30])
        for k2 in ('head', 'outline'):
            hx = (c.get('palette') or {}).get(k2)
            if isinstance(hx, str) and re.match(r'#[0-9a-fA-F]{6}$', hx.strip()[:7]): allc['A.hex_'+k2].append(hx.strip()[:7].lower())
    # actions
    ac = M['actions']; R['actions_n'] = len(ac); R['action_classes'] = dict(Counter(re.sub(r'\s*\(.*', '', a['class'].lower()) for a in ac).most_common(15)); R['motion_types'] = dict(Counter(str(a.get('motion_type')).lower().split(' ')[0].split('/')[0].split('(')[0] for a in ac))
    for a in ac:
        mt = str(a.get('motion_type')).lower()
        for f in ('anticipation_f', 'travel_f', 'overshoot_f', 'settle_f'):
            if isinstance(a.get(f), (int, float)): allc['act.'+f+('.snap' if 'snap' in mt else '.tween' if 'tween' in mt else '.other')].append(a[f])
        for f in ('elbow_deg', 'knee_deg', 'torso_tilt_deg', 'squash_stretch', 'cadence_f', 'poses_per_step', 'stride_H', 'bob_pct_H'):
            if isinstance(a.get(f), (int, float)): allc['act.'+f].append(a[f])
    hd = [h['end_f']-h['start_f']+1 for h in M['holds'] if h.get('end_f') and h.get('start_f')]; R['holds'] = q(hd, 0); allc['hold_len_f'] += hd; R['hold_share_of_video'] = round(sum(hd)/nf, 3)
    fc = M['faces']; R['faces_n'] = len(fc); R['face_swaps_per_s'] = round(len(fc)/(nf/30), 2); allc['faces_per_s'].append(R['face_swaps_per_s'])
    bl = [f for f in fc if 'blink' in str(f.get('expression')).lower()]; R['blinks_n'] = len(bl)
    ls = M['lipsync']; R['lipsync'] = dict(runs=len(ls), frames_per_shape=q([l['frames_per_shape'] for l in ls if l.get('frames_per_shape')]), share=round(sum(l['end_f']-l['start_f']+1 for l in ls)/nf, 3)); allc['lip_fps'] += [l['frames_per_shape'] for l in ls if l.get('frames_per_shape')]
    # assets
    asx = M['assets']; R['assets_n'] = len(asx); R['asset_classes'] = dict(Counter(re.sub(r'\s*[\(/].*', '', str(a.get('class')).lower()) for a in asx).most_common(12)); R['asset_flags'] = dict(overshoot=sum(bool(a.get('overshoot')) for a in asx), bounce=sum((a.get('bounces') or 0) > 0 for a in asx), blur=sum(bool(a.get('blur')) for a in asx), on_twos=sum(bool(a.get('on_twos')) for a in asx), squash=sum(1 for a in asx if a.get('squash_stretch') not in (None, 1, 1.0)))
    for a in asx:
        for k2 in ('overshoot', 'blur', 'on_twos'): allc['asset.'+k2].append(bool(a.get(k2)))
        allc['asset.bounce'].append((a.get('bounces') or 0) > 0); allc['asset.squash'].append(a.get('squash_stretch') not in (None, 1, 1.0))
        if a.get('loop_f'): allc['asset.loop_f'].append(a['loop_f'])
        fs = a.get('fall_samples') or []
        if len(fs) >= 5:
            import numpy as np
            t = np.array([p[0] for p in fs], float)/30; y = np.array([p[1] for p in fs], float)/1920; co = np.polyfit(t-t[0], y, 2); g = 2*co[0]; res = y-np.polyval(co, t-t[0]); r2 = 1-res.var()/max(y.var(), 1e-12)
            R.setdefault('falls', []).append(dict(object=a['object'][:40], n=len(fs), g_screen_h_per_s2=round(float(g), 2), r2=round(float(r2), 4), start=a['start_f']))
            if r2 >= 0.98: allc['fall_g'].append(abs(float(g)))
    # captions
    ce = M['caption_events']; dw = [c['off']-c['on']+1 for c in ce if c.get('off') and c.get('on') and c['off'] >= c['on']]; R['caption'] = dict(n=len(ce), dwell_f=q(dw, 0), per_s=round(len(ce)/(nf/30), 2), words=q([len(c['text'].split()) for c in ce], 0)); allc['cap_dwell_f'] += dw; allc['cap_words'] += [len(c['text'].split()) for c in ce]
    wp = f'/mnt/project-files/modern-vista-social/research/rick-style-spec/transcripts/txt/{v}.words.tsv'
    if os.path.exists(wp):
        W = [(float(l.split('\t')[0]), re.sub(r'[^a-z0-9]', '', l.split('\t')[1].lower())) for l in open(wp).read().strip().split('\n') if '\t' in l]; off = []; used = set()
        for c in ce:
            w0 = re.sub(r'[^a-z0-9]', '', c['text'].split()[0].lower()) if c['text'].split() else ''; tc = (c['on']-1)/30
            m = [(abs(t-tc), i) for i, (t, w) in enumerate(W) if w == w0 and abs(t-tc) < 0.34 and i not in used]
            if m: _, i = min(m); used.add(i); off.append(round((tc-W[i][0])*30, 1))
        R['caption_offset_f'] = q(off, 1); allc['cap_offset_f'] += off; R['caption_offset_share_within'] = dict(pm2=round(sum(abs(o) <= 2 for o in off)/max(len(off), 1), 3), early_or_on=round(sum(o <= 0.5 for o in off)/max(len(off), 1), 3))
    R['sound_events_per_s'] = round(len(M['sound_picture_events'])/(nf/30), 2)
    out['videos'][v] = R
S = {}
for k, xs in allc.items():
    if xs and isinstance(xs[0], bool): S[k] = dict(n=len(xs), true=sum(xs), share=round(sum(xs)/len(xs), 3))
    elif xs and isinstance(xs[0], str): S[k] = dict(n=len(xs), top=Counter(xs).most_common(10))
    else: S[k] = q(xs)
out['all'] = S; json.dump(out, open(N+'SYNTH_7videos.json', 'w'), indent=1, default=str)
for k in sorted(S): print(k, S[k])
