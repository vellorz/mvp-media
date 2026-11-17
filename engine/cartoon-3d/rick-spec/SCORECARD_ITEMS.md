# Scored checklist (Rick 99 % test) - items
Accuracy = passed / total. Pass = >= 99 % AND zero FAIL on [C] items. All R items are [C].

Total items: 101

| ID | stage | C | item | evidence |
|---|---|---|---|---|
| S1 | script |  | First sentence states the oddity (strange act / impossible rule / challenge); no date/place-first, no "did you know" | script line 1 |
| S2 | script |  | "You see," world rule within 3-8 s | script + word times |
| S3 | script |  | Doubter with one quoted mocking line | script line |
| S4 | script |  | 2-3 escalations with time markers | script lines |
| S5 | script |  | Reveal starts at 50-85 % of runtime | reveal word time / runtime |
| S6 | script | C | Last sentence is the payoff; no "on your wall", no CTA, no place tag line | final script line |
| S7 | script |  | Roles not names (a real name at most once) | name count |
| S8 | script |  | 1-4 concrete numbers, numerals as digits in captions | number count |
| S9 | script |  | Story is true and tied to the poster place; facts sourced | sources list |
| S10 | script |  | Trend-led: trend named + true link, no logos/likeness/endorsement | trend note |
| V1 | vo | C | Drew voice_id q0IMILNRPxOgtBTS4taI on eleven_v4 | generation record (model_id) |
| V2 | vo |  | Open tag [energetic, playful storytelling]; no [warm]/[cozy]/[soft] tags | VO text with tags |
| V3 | vo | C | Pace 3.4-4.1 words/s | word times: words / speech span |
| V4 | vo | C | <= 3 gaps > 0.8 s and none > 1.2 s | word-gap list |
| V5 | vo |  | First word at t <= 0.2 s | word 1 start |
| V6 | vo |  | Never uniform-speed; only silence trimmed | fit log |
| P1 | plan |  | Every shot names its Rick reference shot (rule 141A) | shot list |
| P2 | plan |  | >= 4 dynamic angle types (low, high, top-down, macro, through-object, orbit) | shot list angle column |
| P3 | plan | C | No row of characters facing camera in a frontal stage shot | stills sheet |
| P4 | plan |  | >= 8 sets/places, >= 5 hero-prop close-ups | shot list |
| P5 | plan |  | Facts shown as in-world props, no overlays/arrows/date cards | stills |
| C1 | shots | C | Flat drawn round heads with monoline dark outline (no shaded 3D figurine heads) | stills per character |
| C2 | shots |  | Outline 8-13 px @1440 in MS (6-10 @1080) | pixel measure on MS still |
| C3 | shots |  | Head 30-39 % frame width in MS | pixel measure on MS stills |
| C4 | shots | C | Exactly one full face (eyes, brows, mouth) on every visible head, every frame | check_faces / frame scan |
| C5 | shots |  | Face change every 0.3-2 s on screen; >= 10 distinct expressions | face schedule |
| C6 | shots |  | Lips move only on quoted lines; narrator never lip-synced | face schedule |
| C7 | shots |  | Our own unique characters (no Rick characters) | cast sheet |
| C8 | shots |  | Walking means stepping; nobody pops in or glides | move list + strips |
| G1 | shots | C | No floating parts (check_float PASS) | check_float output |
| G2 | shots | C | No prop through body (check_clip PASS) | check_clip output |
| G3 | shots | C | Camera never passes through/grazes geometry (check_campath) | check_campath output |
| G4 | shots |  | No z-fight / coplanar flicker (scrub of moving clips) | flicker scan |
| G5 | shots |  | No face covered; main characters in frame | stills |
| G6 | shots |  | Signs/lettering whole, nothing crosses them | stills |
| K1 | render | C | No static camera > 1.5 s | metrics.py still runs |
| K2 | render |  | Motion median >= 4.5 (metrics.py diff) | metrics.py |
| K3 | render |  | Joins 2-4.5 per 10 s | transitions list |
| K4 | render | C | Every join a dissolve 4-14 f or fast join <= 3 f; <= 5 fast joins | transitions.py + dissolve_curve |
| K5 | render | C | Dissolve lengths varied (not one fixed length) | dissolve list |
| K6 | render |  | >= 50 % of dissolves bridged (same shape same spot +-5 %) | bridge table |
| K7 | render |  | Joins on phrase onsets | join vs word table |
| K8 | render |  | Eased moves land on nouns +-3 f; one ~9 f crash push on the climax word | hit table |
| K9 | render |  | No whip pans / slide wipes / zoom-blur / flash | transition census |
| L1 | render |  | Mean luma 0.33-0.56 | metrics.py |
| L2 | render |  | Mean saturation 0.37-0.66 | metrics.py |
| L3 | render |  | p2 >= 0.05 (no crushed blacks) | metrics.py |
| L4 | render |  | p98 >= 0.84 | metrics.py |
| L5 | render | C | Edge density average >= 28 % (render/qa/edge.py, 24 stills) | edge.py output |
| L6 | render |  | Edge 0.20-0.35 (metrics.py) | metrics.py |
| L7 | render |  | Palette flips across time/mood joins | stills pairs |
| L8 | render |  | Motivated key, contact shadows, bloom on emitters, DOF/haze | stills |
| L9 | render |  | FG/MG/BG layers in every shot; dense sets (>= 20 props wide) | stills |
| T1 | render |  | Caption box bottom 71.7 +-0.5 % H | captions.py |
| T2 | render |  | Cap/box 53-63 px @1920 equiv (70-84 @2560) | captions.py |
| T3 | render |  | Centred 50 +-0.5 % | captions.py |
| T4 | render |  | <= 3 words per caption; median width <= 50 % W | captions.py + caption list |
| T5 | render |  | Hard swap 0-3 f before the word; on screen >= 79 % of runtime | caption timing table |
| T6 | render |  | Montserrat Black white, 4-6 px@1080 black outline, +3 px shadow, above every dissolve | still crop |
| T7 | render | C | Caption never covers a face or the poster | stills scan |
| A1 | audio | C | Integrated -14 LUFS (+-0.5) | ffmpeg ebur128 |
| A2 | audio | C | True peak <= -2 dBTP (+0.1 tolerance) | ffmpeg ebur128 |
| A3 | audio | C | LRA <= 3.2 LU | ffmpeg ebur128 |
| A4 | audio | C | Music bed ~20 dB under VO (17-23), constant, no ducking (corr |r| <= 0.15) | stem measure |
| A5 | audio |  | Plucked/mallet loop + soft pulse, 80-160 BPM, frame 0 to end | synth params |
| A6 | audio |  | SFX 8-12 dB over bed on moves/impacts/payoff | stem measure |
| A7 | audio |  | Original cleared music, no chart songs | synth source |
| E1 | render | C | Poster is inside the payoff scene as an in-world object | final shot stills |
| E2 | render | C | Whole poster incl. border and bottom text visible, never cropped | final frames + bbox |
| E3 | render | C | Video ends <= 1.2 s after the last word starts; no end card/fade/logo | last word time vs duration |
| E4 | render |  | Final camera move lands on the poster while the last line is spoken | final shot timing |
| E5 | render |  | Poster artwork is the real shop poster file at true aspect | asset path + aspect |
| F1 | export | C | Master 1440x2560, 30 fps, H.264, AAC 48 kHz | ffprobe |
| F2 | export |  | Runtime 30-78 s (target 55-65) | ffprobe |
| F3 | export |  | No black/frozen/pop frames | frame QA scan |
| F4 | export |  | Post text: SEO title, keyword description, tags, hashtags only | post-text.md |
| F5 | export |  | Pinterest pins + up to 10 topics prepared; nothing scheduled | pins folder + schedule log |
| R01 | repeat | C | NOT REPEATED - Dresden/Salzburg: VO slower than 3.4 w/s (2.54-2.66) | V3 numbers |
| R02 | repeat | C | NOT REPEATED - Dresden/Salzburg: 15-16 VO gaps > 0.8 s, max 1.5-1.66 s | V4 gap list |
| R03 | repeat | C | NOT REPEATED - Salzburg: soft VO tags ([warm, intrigued]) made Drew dull; LRA 4.7 | VO tag list + A3 |
| R04 | repeat | C | NOT REPEATED - Dresden/Salzburg: static camera, motion median 2.45-3.34 | K2 number |
| R05 | repeat | C | NOT REPEATED - Dresden/Salzburg: still runs of 35-36 f, still frames 10-15 % | K1 still-run list |
| R06 | repeat | C | NOT REPEATED - Dresden/Salzburg: shaded 3D figurine heads, no outline | C1 stills |
| R07 | repeat | C | NOT REPEATED - Dresden/Salzburg: small faces in MS (< 30 % W) | C3 measures |
| R08 | repeat | C | NOT REPEATED - Dresden/Salzburg: static faces across held shots | C5 schedule |
| R09 | repeat | C | NOT REPEATED - Dresden/Salzburg: captions 11-22 % too big (box 61-66 px @1920) | T2 numbers |
| R10 | repeat | C | NOT REPEATED - Dresden/Salzburg: captions too wide (median 52-55 % W), 2-4 words | T4 numbers |
| R11 | repeat | C | NOT REPEATED - Dresden: numbers spelled out in captions | caption list |
| R12 | repeat | C | NOT REPEATED - Dresden/Salzburg: every dissolve the same 5 f linear ramp | K5 dissolve list |
| R13 | repeat | C | NOT REPEATED - Dresden/Salzburg: few bridge objects | K6 bridge table |
| R14 | repeat | C | NOT REPEATED - Dresden: date-first hook ("In 1730...") | S1 line |
| R15 | repeat | C | NOT REPEATED - Dresden/Salzburg: no doubter | S3 line |
| R16 | repeat | C | NOT REPEATED - Dresden/Salzburg: no escalation (list of quantities/names) | S4 lines |
| R17 | repeat | C | NOT REPEATED - Dresden/Salzburg: no reveal | S5 time |
| R18 | repeat | C | NOT REPEATED - Dresden/Salzburg: "X, on your wall" tag line / poster card CTA ending | S6 + E1 |
| R19 | repeat | C | NOT REPEATED - Salzburg: crushed blacks p2 0.004, dull p98 0.67; Dresden p98 0.77 | L3 L4 numbers |
| R20 | repeat | C | NOT REPEATED - Salzburg: edge density 0.197 (dark, sparse) | L5 L6 numbers |
| R21 | repeat | C | NOT REPEATED - Dresden/Salzburg: frontal eye-level stage shots, characters in a row | P2 P3 |
| R22 | repeat | C | NOT REPEATED - Dresden/Salzburg: flat even light, little DOF | L8 stills |
| R23 | repeat | C | NOT REPEATED - Dresden: wrong music style (owner) | A5 synth params |
| R24 | repeat | C | NOT REPEATED - Dresden: too many names/numbers (3 names, 9 numbers) | S7 S8 counts |
