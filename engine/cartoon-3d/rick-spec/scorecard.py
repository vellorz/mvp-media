# Rick-99 scored checklist. Every item is binary PASS/FAIL with named evidence.
# Usage: python3 scorecard.py items            -> writes SCORECARD_ITEMS.md (the empty checklist)
#        python3 scorecard.py score results.json -> writes SCORECARD.md with score; results = {"ID": {"pass": true, "evidence": "..."}}
# Accuracy = passed / total. Target >= 99 % AND zero failures on items marked C (critical). Missing result = FAIL.
import sys, json
I = []  # (id, stage, critical, item, evidence required)
def a(i, st, c, item, ev): I.append((i, st, c, item, ev))
# ---- S: script stage
a('S1','script',0,'First sentence states the oddity (strange act / impossible rule / challenge); no date/place-first, no "did you know"','script line 1')
a('S2','script',0,'"You see," world rule within 3-8 s','script + word times')
a('S3','script',0,'Doubter with one quoted mocking line','script line')
a('S4','script',0,'2-3 escalations with time markers','script lines')
a('S5','script',0,'Reveal starts at 50-85 % of runtime','reveal word time / runtime')
a('S6','script',1,'Last sentence is the payoff; no "on your wall", no CTA, no place tag line','final script line')
a('S7','script',0,'Roles not names (a real name at most once)','name count')
a('S8','script',0,'1-4 concrete numbers, numerals as digits in captions','number count')
a('S9','script',0,'Story is true and tied to the poster place; facts sourced','sources list')
a('S10','script',0,'Trend-led: trend named + true link, no logos/likeness/endorsement','trend note')
# ---- V: VO
a('V1','vo',1,'Drew voice_id q0IMILNRPxOgtBTS4taI on eleven_v4','generation record (model_id)')
a('V2','vo',0,'Open tag [energetic, playful storytelling]; no [warm]/[cozy]/[soft] tags','VO text with tags')
a('V3','vo',1,'Pace 3.4-4.1 words/s','word times: words / speech span')
a('V4','vo',1,'<= 3 gaps > 0.8 s and none > 1.2 s','word-gap list')
a('V5','vo',0,'First word at t <= 0.2 s','word 1 start')
a('V6','vo',0,'Never uniform-speed; only silence trimmed','fit log')
# ---- P: picture / plan
a('P1','plan',0,'Every shot names its Rick reference shot (rule 141A)','shot list')
a('P2','plan',0,'>= 4 dynamic angle types (low, high, top-down, macro, through-object, orbit)','shot list angle column')
a('P3','plan',1,'No row of characters facing camera in a frontal stage shot','stills sheet')
a('P4','plan',0,'>= 8 sets/places, >= 5 hero-prop close-ups','shot list')
a('P5','plan',0,'Facts shown as in-world props, no overlays/arrows/date cards','stills')
# ---- C: characters
a('C1','shots',1,'Flat drawn round heads with monoline dark outline (no shaded 3D figurine heads)','stills per character')
a('C2','shots',0,'Outline 8-13 px @1440 in MS (6-10 @1080)','pixel measure on MS still')
a('C3','shots',0,'Head 30-39 % frame width in MS','pixel measure on MS stills')
a('C4','shots',1,'Exactly one full face (eyes, brows, mouth) on every visible head, every frame','check_faces / frame scan')
a('C5','shots',0,'Face change every 0.3-2 s on screen; >= 10 distinct expressions','face schedule')
a('C6','shots',0,'Lips move only on quoted lines; narrator never lip-synced','face schedule')
a('C7','shots',0,'Our own unique characters (no Rick characters)','cast sheet')
a('C8','shots',0,'Walking means stepping; nobody pops in or glides','move list + strips')
# ---- G: geometry / defects
a('G1','shots',1,'No floating parts (check_float PASS)','check_float output')
a('G2','shots',1,'No prop through body (check_clip PASS)','check_clip output')
a('G3','shots',1,'Camera never passes through/grazes geometry (check_campath)','check_campath output')
a('G4','shots',0,'No z-fight / coplanar flicker (scrub of moving clips)','flicker scan')
a('G5','shots',0,'No face covered; main characters in frame','stills')
a('G6','shots',0,'Signs/lettering whole, nothing crosses them','stills')
# ---- K: camera / transitions / pacing (measured on render)
a('K1','render',1,'No static camera > 1.5 s','metrics.py still runs')
a('K2','render',0,'Motion median >= 4.5 (metrics.py diff)','metrics.py')
a('K3','render',0,'Joins 2-4.5 per 10 s','transitions list')
a('K4','render',1,'Every join a dissolve 4-14 f or fast join <= 3 f; <= 5 fast joins','transitions.py + dissolve_curve')
a('K5','render',1,'Dissolve lengths varied (not one fixed length)','dissolve list')
a('K6','render',0,'>= 50 % of dissolves bridged (same shape same spot +-5 %)','bridge table')
a('K7','render',0,'Joins on phrase onsets','join vs word table')
a('K8','render',0,'Eased moves land on nouns +-3 f; one ~9 f crash push on the climax word','hit table')
a('K9','render',0,'No whip pans / slide wipes / zoom-blur / flash','transition census')
# ---- L: look
a('L1','render',0,'Mean luma 0.33-0.56','metrics.py')
a('L2','render',0,'Mean saturation 0.37-0.66','metrics.py')
a('L3','render',0,'p2 >= 0.05 (no crushed blacks)','metrics.py')
a('L4','render',0,'p98 >= 0.84','metrics.py')
a('L5','render',1,'Edge density average >= 28 % (render/qa/edge.py, 24 stills)','edge.py output')
a('L6','render',0,'Edge 0.20-0.35 (metrics.py)','metrics.py')
a('L7','render',0,'Palette flips across time/mood joins','stills pairs')
a('L8','render',0,'Motivated key, contact shadows, bloom on emitters, DOF/haze','stills')
a('L9','render',0,'FG/MG/BG layers in every shot; dense sets (>= 20 props wide)','stills')
# ---- T: captions
a('T1','render',0,'Caption box bottom 71.7 +-0.5 % H','captions.py')
a('T2','render',0,'Cap/box 53-63 px @1920 equiv (70-84 @2560)','captions.py')
a('T3','render',0,'Centred 50 +-0.5 %','captions.py')
a('T4','render',0,'<= 3 words per caption; median width <= 50 % W','captions.py + caption list')
a('T5','render',0,'Hard swap 0-3 f before the word; on screen >= 79 % of runtime','caption timing table')
a('T6','render',0,'Montserrat Black white, 4-6 px@1080 black outline, +3 px shadow, above every dissolve','still crop')
a('T7','render',1,'Caption never covers a face or the poster','stills scan')
# ---- A: audio
a('A1','audio',1,'Integrated -14 LUFS (+-0.5)','ffmpeg ebur128')
a('A2','audio',1,'True peak <= -2 dBTP (+0.1 tolerance)','ffmpeg ebur128')
a('A3','audio',1,'LRA <= 3.2 LU','ffmpeg ebur128')
a('A4','audio',1,'Music bed ~20 dB under VO (17-23), constant, no ducking (corr |r| <= 0.15)','stem measure')
a('A5','audio',0,'Plucked/mallet loop + soft pulse, 80-160 BPM, frame 0 to end','synth params')
a('A6','audio',0,'SFX 8-12 dB over bed on moves/impacts/payoff','stem measure')
a('A7','audio',0,'Original cleared music, no chart songs','synth source')
# ---- E: ending / poster
a('E1','render',1,'Poster is inside the payoff scene as an in-world object','final shot stills')
a('E2','render',1,'Whole poster incl. border and bottom text visible, never cropped','final frames + bbox')
a('E3','render',1,'Video ends <= 1.2 s after the last word starts; no end card/fade/logo','last word time vs duration')
a('E4','render',0,'Final camera move lands on the poster while the last line is spoken','final shot timing')
a('E5','render',0,'Poster artwork is the real shop poster file at true aspect','asset path + aspect')
# ---- F: file / delivery
a('F1','export',1,'Master 1440x2560, 30 fps, H.264, AAC 48 kHz','ffprobe')
a('F2','export',0,'Runtime 30-78 s (target 55-65)','ffprobe')
a('F3','export',0,'No black/frozen/pop frames','frame QA scan')
a('F4','export',0,'Post text: SEO title, keyword description, tags, hashtags only','post-text.md')
a('F5','export',0,'Pinterest pins + up to 10 topics prepared; nothing scheduled','pins folder + schedule log')
# ---- R: repeat-mistake section (one item per ledger gap; ALL critical)
REP = [
 ('R01','Dresden/Salzburg: VO slower than 3.4 w/s (2.54-2.66)','V3 numbers'),
 ('R02','Dresden/Salzburg: 15-16 VO gaps > 0.8 s, max 1.5-1.66 s','V4 gap list'),
 ('R03','Salzburg: soft VO tags ([warm, intrigued]) made Drew dull; LRA 4.7','VO tag list + A3'),
 ('R04','Dresden/Salzburg: static camera, motion median 2.45-3.34','K2 number'),
 ('R05','Dresden/Salzburg: still runs of 35-36 f, still frames 10-15 %','K1 still-run list'),
 ('R06','Dresden/Salzburg: shaded 3D figurine heads, no outline','C1 stills'),
 ('R07','Dresden/Salzburg: small faces in MS (< 30 % W)','C3 measures'),
 ('R08','Dresden/Salzburg: static faces across held shots','C5 schedule'),
 ('R09','Dresden/Salzburg: captions 11-22 % too big (box 61-66 px @1920)','T2 numbers'),
 ('R10','Dresden/Salzburg: captions too wide (median 52-55 % W), 2-4 words','T4 numbers'),
 ('R11','Dresden: numbers spelled out in captions','caption list'),
 ('R12','Dresden/Salzburg: every dissolve the same 5 f linear ramp','K5 dissolve list'),
 ('R13','Dresden/Salzburg: few bridge objects','K6 bridge table'),
 ('R14','Dresden: date-first hook ("In 1730...")','S1 line'),
 ('R15','Dresden/Salzburg: no doubter','S3 line'),
 ('R16','Dresden/Salzburg: no escalation (list of quantities/names)','S4 lines'),
 ('R17','Dresden/Salzburg: no reveal','S5 time'),
 ('R18','Dresden/Salzburg: "X, on your wall" tag line / poster card CTA ending','S6 + E1'),
 ('R19','Salzburg: crushed blacks p2 0.004, dull p98 0.67; Dresden p98 0.77','L3 L4 numbers'),
 ('R20','Salzburg: edge density 0.197 (dark, sparse)','L5 L6 numbers'),
 ('R21','Dresden/Salzburg: frontal eye-level stage shots, characters in a row','P2 P3'),
 ('R22','Dresden/Salzburg: flat even light, little DOF','L8 stills'),
 ('R23','Dresden: wrong music style (owner)','A5 synth params'),
 ('R24','Dresden: too many names/numbers (3 names, 9 numbers)','S7 S8 counts'),
]
for i,t,ev in REP: a(i,'repeat',1,'NOT REPEATED - '+t,ev)
def items_md():
    out=['# Scored checklist (Rick 99 % test) - items','Accuracy = passed / total. Pass = >= 99 % AND zero FAIL on [C] items. All R items are [C].','',f'Total items: {len(I)}','','| ID | stage | C | item | evidence |','|---|---|---|---|---|']
    for i,st,c,it,ev in I: out.append(f'| {i} | {st} | {"C" if c else ""} | {it} | {ev} |')
    return '\n'.join(out)+'\n'
def score(res):
    rows=[];p=0;cf=[]
    for i,st,c,it,ev in I:
        r=res.get(i,{}); ok=bool(r.get('pass')); p+=ok
        if c and not ok: cf.append(i)
        rows.append(f'| {i} | {st} | {"C" if c else ""} | {"PASS" if ok else "FAIL"} | {it} | {r.get("evidence","(no evidence = FAIL)")} |')
    acc=100*p/len(I)
    head=[f'# SCORECARD - {p}/{len(I)} = {acc:.1f} %  | critical failures: {len(cf)} {cf if cf else ""}', 'VERDICT: '+('PASS (>= 99 %, 0 critical)' if acc>=99 and not cf else 'NOT YET'),'','| ID | stage | C | result | item | evidence |','|---|---|---|---|---|---|']
    return '\n'.join(head+rows)+'\n', acc, cf
if __name__=='__main__':
    if sys.argv[1]=='items': open('SCORECARD_ITEMS.md','w').write(items_md()); print(len(I),'items')
    else:
        md,acc,cf=score(json.load(open(sys.argv[2]))); open('SCORECARD.md','w').write(md); print(f'{acc:.2f}% critical_fail={cf}')
