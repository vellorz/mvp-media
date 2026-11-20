#!/usr/bin/env python3
"""merge.py VID -> new-analysis-2/VID/merged.json + joins.verified.csv + blind item lists for measurer B"""
import sys, json, glob, os, random
vid = sys.argv[1]; S = f'/mnt/project-files/modern-vista-social/research/rick-style-spec/new-analysis-2/{vid}/'
files = sorted(glob.glob(S+'data_f*.json')); M = dict(video=vid, parts=[], joins=[], shots=[], camera_moves=[], characters=[], actions=[], holds=[], faces=[], lipsync=[], assets=[], caption_events=[], sound_picture_events=[], frames_viewed=0)
for f in files:
    d = json.load(open(f)); a, b = d['range']; M['parts'].append(dict(file=os.path.basename(f), range=[a, b], frames_viewed=d.get('frames_viewed')))
    M['frames_viewed'] += d.get('frames_viewed') or 0
    for j in d.get('joins', []):
        if a <= j['first_blend_frame'] <= b: M['joins'].append(j)
    for k in ('camera_moves', 'characters', 'actions', 'holds', 'faces', 'lipsync', 'assets', 'sound_picture_events'):
        for x in d.get(k, []): x['_part'] = f'{a}-{b}'; M[k].append(x)
    for c in d.get('caption_events', []):
        if a <= c['on'] <= b: M['caption_events'].append(c)
    for s in d.get('shots', []): s['_part'] = f'{a}-{b}'; M['shots'].append(s)
M['joins'].sort(key=lambda j: j['first_blend_frame'])
# de-duplicate joins reported by two neighbouring ranges (within 6 f)
J = []
for j in M['joins']:
    if J and abs(j['first_blend_frame']-J[-1]['first_blend_frame']) <= 6: continue
    J.append(j)
M['joins'] = J
json.dump(M, open(S+'merged.json', 'w'), indent=1)
open(S+'joins.agentA.csv', 'w').write('start_frame,len_f,type\n'+'\n'.join(f"{j['first_blend_frame']},{j['len_f']},{j['type']}" for j in J))
# blind lists for measurer B (no measured values)
random.seed(20261120)
acts = [dict(id=i, shot_start=a.get('shot_start'), character=a['character'], **{'class': a['class']}, window=[max(a['start_f']-12, 1), a['end_f']+12], note=(a.get('note') or '')[:0]) for i, a in enumerate(M['actions']) if a.get('class') not in ('hold',)]
chars = [dict(id=i, label=c['label'], measure_frame=c.get('measure_frame')) for i, c in enumerate(M['characters']) if c.get('measure_frame')]
ass = [dict(id=i, shot_start=a.get('shot_start'), object=a['object'], window=[max(a['start_f']-12, 1), a['end_f']+12]) for i, a in enumerate(M['assets'])]
json.dump(dict(video=vid, actions=acts, characters=chars, assets=ass), open(S+'blind_items_for_B.json', 'w'), indent=1)
print(vid, 'parts', len(files), 'frames_viewed', M['frames_viewed'], 'joins', len(J), 'cam', len(M['camera_moves']), 'chars', len(M['characters']), 'actions', len(M['actions']), 'holds', len(M['holds']), 'faces', len(M['faces']), 'assets', len(M['assets']), 'captions', len(M['caption_events']), 'sound', len(M['sound_picture_events']))
for j in J: print('  join', j['first_blend_frame'], j['len_f'], j['type'])
