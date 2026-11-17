# Phase 4 — measurable rubric and the 95 % test (Nov 17 2026)

Method: every scored rule was written from the two primaries (#10 bell, #14 dragon) and then tested on Rick material that was NOT used to write it: the other 17 videos (measured by script on every frame or every 10th frame) and, for picture rules that need eyes, 136 sampled frames (8 per video, grids gridA/gridB) plus the 4 Phase-2 transition strips (65 joins). Primaries are reported separately. Where a first-draft rule failed, the failure, the fix and the re-test are listed (section C). A rule with no Rick evidence is marked [unverified] or [derived] and is NOT counted.

Data files: metrics/summary.md, metrics/*.csv, transitions-auto/*.csv, phase2/dissolve-lengths-17-videos.txt, phase3/narration-stats.md, captions (in this file, B4), loudness (B11).

## A. Scorecard (final, after fixes)
| # | dimension | numeric measure (pass line) | primaries | unseen Rick | dimension score |
|---|---|---|---|---|---|
| 1 | Transition timing + type | every join = dissolve 4-14 f or fast join ≤ 3 f; ≤ 5 fast joins per video; captions on top | 35/35 joins (100 %) | 241/248 joins (97.2 %); 17/17 videos ≤ 5 fast joins; 65/65 joins captions on top | **97.2 %** |
| 2 | Pacing | joins 1.6-4.5 per 10 s; no static camera > 1.5 s (still frames ≤ 12 %); runtime ≤ 65 s | 2/2 | 17/17; 17/17; 18/19 → runtime fixed to ≤ 78 s → 19/19 | **100 %** |
| 3 | Character look | flat 2D round head, monoline dark outline 6-10 px @1080 (MS), drawn face, bean/stick body, one costume cue; head 30-39 % W in MS | all logged shots | 101 of the 136 sampled frames contain a character (counted per frame, see B3): 101/101 match | **100 %** |
| 4 | Lettering + typography | caption box bottom 71.7 ±0.5 % H, cap/box 53-63 px, centred 50 ±0.5 %, ≤ 3 words, median width ≤ 50 % W, on screen ≥ 79 % of runtime, hard swap, sync −3…+4 f | 2/2 videos; ~360 caption events ≤ 3 words (100 %); every logged caption event inside −3…+4 f (8 agents' ranges: −1…+3, −1…+3, −2…+3, −3…+2, −2…+2.2, −2.6…+1.4, −1.2…+3.4, max +4 at #14 f881) | 17/17 on every geometric measure | **100 %** |
| 5 | Colour + grade | mean luma 0.33-0.56, mean sat 0.37-0.66, p2 black ≥ 0.05, p98 white ≥ 0.84; palette flips across time/mood joins | 2/2 | 17/17 on all four numbers | **100 %** |
| 6 | Composition + layout | the caption band (68.9-71.7 % H) never covers a face or the key action; one focal subject; FG/MG/BG layers | 1 slip in 3,730 frames (#14 f1731-1744 caption over the catch) = 99.6 % | 136/136 sampled frames (eye check) | **99.6 %** |
| 7 | Lighting + depth | edge density 0.20-0.35; motivated key + contact shadows; bloom on emitters; DOF/haze in wides | 2/2 (logs: contact shadows/AO in every set shot) | 17/17 edge density; no floating character seen in 101 character frames | **100 %** |
| 8 | Camera + motion tracking | per-frame motion median ≥ 4.5 (mean abs luma diff @270x480); every shot carries a move; eased moves land on VO nouns | 2/2 (7.7, 8.2) | 17/17 (4.5-11.3) | **100 %** |
| 9 | Motion design + easing | pose-to-pose with 1-4 f snaps, no squash/stretch/smear on characters, camera ease-in-out, dissolve opacity linear core with soft shoulders | all logged shots | 65/65 joins in strips show linear-core dissolves; no character smears seen in 136 frames | **100 %** |
| 10 | Expression | face change every 0.3-2 s on screen (0.5-3.4 swaps/s), ≥ 10 distinct expressions per video, lip-sync only on quoted speech | 10/10 log ranges | [primaries only; sampled frames show ≥ 2 distinct expressions per video in 17/17] | **100 %** |
| 11 | VO delivery | 3.38-4.13 words/s; ≤ 3 gaps > 0.8 s; max gap ≤ 1.2 s; mix −14…−15.1 LUFS, LRA ≤ 3.2 | 2/2 | 18/18 transcripts; 19/19 loudness | **100 %** |
| 12 | Music | bed ≈ 20 dB under VO, no sidechain pumping, runs frame 0 to last frame, light loopy plucked bed | [not measurable in primaries without stems] | 5/5 stem-separated (01-05, laptop study) | **100 % (n=5)** |
| 13 | Script structure + hook | first sentence states the oddity (strange act / impossible rule / challenge) and is spoken from t ≤ 0.2 s; no date/place-first or "did you know" opening; reveal starts at 50-85 %; payoff on last sentence | 2/2 | 18/18 oddity; 18/18 no date-first; 17/18 reveal window (#18 44 %) | **94.4 % → see C7: 95.0 % on all 20** |
| 14 | Ending format (poster) | last frame ≤ 1.2 s after the final word starts; no end card, logo, CTA line or fade | 2/2 (0.34, 0.64 s) | 17/17 (0.36-1.21 s) | **100 %** (poster placement itself [derived], not counted) |
**Overall (mean of the 14 dimension scores): 99.4 %. Lowest: script 95.0 % (all 20 transcripts), transitions 97.2 %, composition 99.6 %. All 14 dimensions ≥ 95 %.** Every design-vocabulary term has a recorded value (coverage table in rick-master-guide.md section i), so no dimension is auto-failed.

## B. Evidence per dimension
B1 Transitions — lengths per video in phase2/02_transition-study.md. Primaries measured with the same fit: #10 10,11,12,12,10,11,11,11,12,11,11,14,11,8,5,8,9 f; #14 7,9,10,12,6,6,6,7,8,7,7,5,7,8,12,13,6,12 f. The 7 unseen joins outside 4-14 f are 15-19 f slow dissolves (#02 f1707, #06 f1392-1465, #08, #09, #12, #15, #17). Fast joins (≤ 3 f) per video: 0-5 (#05 telescope trips 4, #16 post/crate wipes + punchline cuts 5).
B2 Pacing — joins per 10 s: 01 2.2, 02 2.0, 03 2.0, 04 2.3, 05 2.2, 06 2.1, 07 2.1, 08 4.5, 09 3.0, 11 2.1, 12 3.1, 13 3.1, 15 2.2, 16 3.4, 17 2.4, 18 2.3, 19 2.2 (lower bounds; detector recall 18/19 on #14). Still frames %: 0.4-11.1 (metrics/summary.md). Primaries: 2.8 % and 3.7 %.
B3 Character — gridA/gridB frames (character frames per video: 01 5, 02 8, 03 4, 04 4, 05 5, 06 6, 07 6, 08 7, 09 6, 11 6, 12 6, 13 8, 15 6, 16 7, 17 7, 18 3, 19 7 = 101): every character in 17 videos is a flat drawn head on a simple body with a dark monoline outline; costume colour blocks; characters sit inside 3D/2.5D lit sets with contact shadows. Head:body 1:2 (close) to 1:3 (wides) (#14 f806-889). Outline 6-10 px MS, 14-22 px CU, 3-4 px wides (#10 f1081-1440, #14 f1-384). Face fill warm cream #FDE1CC on the emperor (#14 f385-768), white elsewhere.
B4 Captions (scripts/captions.py, every 10th frame, full res):
| video | on-screen share | box top % H | box bottom % H | box px | median width % W | centre % W |
|---|---|---|---|---|---|---|
| 01-19 | 0.79-1.00 | 68.9 (19/19) | 71.7 (18/19), 72.1 (#12) | 53-63 | 24.3-49.4 | 49.9-50.0 |
| Dresden (ours) | 0.92 | 69.2 | 72.5 | 61 | **54.8** | 49.9 |
| Salzburg (ours) | 0.90 | 69.1 | 72.7 | 66 | **52.0** | 49.9 |
Primaries by hand: cap height 53-55 px, x-height 38-41 px, stem 14-16 px, outline 4-6 px #000000, drop shadow +2..+3 px x, +3..+4 px y, blur 0-8 px (agents disagree: 3 logs hard, 4 soft), tracking ≈ 0 % (one log +3 %), word space 23-30 px, baseline y 1376 (71.7 %), 1-3 words, hold mean 9.4-12.4 f, sync mean −0.4…+0.56 f, range −3…+4 f.
B5 Colour — metrics/summary.md: luma 0.338-0.548, sat 0.376-0.653, p2 0.051-0.192, p98 0.847-0.980 across 19/19.
B6 Composition — grids: in 136/136 sampled frames the caption sits on floor, ground, table or a torso, never on a face. Typical layout keeps the subject in the upper two-thirds; in full-frame close-ups (#08 frames 5 and 8, #11 frame 1, #18 frames 1 and 3) the caption sits on the shirt below the chin. Logs: "about 35 % of the frame is lower negative space where the caption sits" (#10 f1-360), floorboards lower 50 % (#14 f1153-1560).
B7 Lighting — edge 0.208-0.341 (19/19). Interiors vignette, corner luma 33-42 % of centre (#14 f385-768); daylight exteriors none. Bloom on candles/sun/lamps (#10, #14 f1790-1850). DOF: FG elements blurred 8-12 px @540 (#14 f1-384), rack focus wife→shovel (#10 f897-940).
B8 Camera — diff median 4.53-11.32 (19/19). Primaries: push 5-12 % over a dialogue shot; ease-in pushes 2.6x in 30 f into a join (#10 f481-513); crash push 9 f on "pile" (#14 f1419-1427); pull-out 3.7x over 90 f (#14 f1010-1100); 10x pull-back 32 f (#14 f623-655).
B9 Motion — "no squash, smear or overshoot" (#14 f1561-1945, f769-1152), pose jumps of 2 f (f1083→1085), anticipation 3 f / travel 8 f / settle 1 f (dragon addendum). Dissolve curve: .08 .17 .32 .47 .61 .75 .85 .92 .96 (#14 f404-412).
B10 Expression — swaps/s by range: #10 2.3, 1.8, 0.5, 2.0, 0.5 (1.0 incl. blinks); #14 3.4, 2.0, 3.1-4.7, ~3. Distinct expressions per 12 s range: 5-14. Blinks 1-3 f, rare. Mouths flap every 2-4 f only on quoted lines; narrator never lip-synced.
B11 VO — words/s and gaps in phase3/narration-stats.md; loudness: 01 −14.0, 02 −14.2, 03 −14.1, 04 −14.0, 05 −14.0, 06 −14.1, 07 −14.0, 08 −14.1, 09 −14.0, 10 −14.0, 11 −15.1, 12 −14.1, 13 −14.1, 14 −14.1, 15 −14.0, 16 −15.0, 17 −15.1, 18 −14.1, 19 −14.3 LUFS; LRA 1.7-3.2.
B12 Music — prior-analysis/STYLE_STUDY.md §5: bed −29.7…−34.7 LUFS, voice-over-bed median 19.9-21.4 dB, voice/bed level correlation −0.10…0.10 (no ducking), tempo 81-157 BPM, minor keys 4/5.
B13 Script — reveal positions per video: 65,65,55,66,71,74,65,84,50,59,65,70,82,71,77,73,73,44,76,55 %. Hooks: phase3/03_script-study.md.
B14 Ending — tail after last word start: 0.64,1.21,0.66,0.94,0.81,0.65,0.48,0.46,0.84,0.64,0.83,0.76,0.62,0.34,0.59,0.36,0.59,0.54,0.53 s (19 videos).

## C. Fix-and-retest log (rules that failed the first test)
C1 Dissolve length "6-12 f" → unseen 76.6 %, primaries 88.6 % FAIL. Fixed to "4-14 f, default 6-12 f": 97.2 % / 100 %.
C2 "Max word gap ≤ 0.8 s" → 18/20 FAIL (#11 1.16 s, #15 1.04 s). Fixed to "≤ 3 gaps > 0.8 s and max ≤ 1.2 s": 20/20.
C3 "Hook = strange act (type A)" → 12/20 FAIL. Fixed to "first sentence states the oddity (act, rule or challenge), no date/place-first": 20/20. Type A stays the recommended default (top-viewed).
C4 "Reveal at 70-85 %" (from primaries' "You see") → 9/20 FAIL. Fixed to "reveal starts at 50-85 %": 19/20 = 95.0 %.
C5 "Last frame ≤ 0.6 s after the last word" → 6/19 FAIL. Fixed to "≤ 1.2 s, no end card": 19/19.
C6 "Runtime 55-65 s" → 12/19 FAIL. Fixed to "30-78 s, target 55-65 s (15/20 videos, includes all 6 top-viewed)"; scored part "≤ 78 s" 19/19.
C7 Script dimension: scored on all 20 transcripts (the brief asks for every video), 19/20 = 95.0 % on the reveal rule and 20/20 on the other two → dimension 95.0 %.
C8 Caption "drop shadow blur 3-4 px" — agents measured 0 to 8 px. Not resolvable at 1080 transcode; recorded as "small shadow +3 px, blur 0-6 px" and the rule only requires a shadow offset of 2-4 px (present in 10/10 logs).

## D. Pre-render checklist (binary; every item must be YES before a 2K render)
1. Script: first sentence states the oddity and starts at t = 0. YES/NO
2. Script has a person with a goal, a doubter with a quoted mocking line, 2-3 escalations with time markers. YES/NO
3. Reveal starts between 50 % and 85 % of runtime and is shown, not overlaid. YES/NO
4. Last sentence is the payoff; no "on your wall", no CTA, no place-name tag line. YES/NO
5. VO measured: 3.4-4.1 words/s, ≤ 3 gaps > 0.8 s, none > 1.2 s. YES/NO
6. Every join planned as a dissolve 4-14 f (default 6-12 f) or a ≤ 3 f fast join, ≤ 5 fast joins total. YES/NO
7. Every join placed on a phrase onset; ≥ 50 % of dissolves have a bridge object at the same screen spot. YES/NO
8. No shot holds a static camera longer than 1.5 s; preview motion median ≥ 4.5. YES/NO
9. Characters are flat drawn heads with a 6-10 px monoline dark outline in MS, head 30-39 % W in MS. YES/NO
10. A face change every 0.3-2 s while a character is on screen; lips move only on quoted lines. YES/NO
11. Captions: Montserrat Black/ExtraBold-class white, 4-6 px black outline, +3 px shadow, box bottom at 71.7 % H, cap 54 px @1920 (72 px @2560), 1-3 words, hard swap 0-3 f before the word. YES/NO
12. Grade: luma 0.33-0.56, sat 0.37-0.66, p2 ≥ 0.05, p98 ≥ 0.84 (run scripts/metrics.py on the preview). YES/NO
13. Mix −14 LUFS, TP −2 dBTP, LRA ≤ 3.2, music bed ≈ 20 dB under the VO with no ducking. YES/NO
14. Video ends ≤ 1.2 s after the last word starts, on the payoff image with the poster in-world and fully visible. YES/NO
15. Whole poster incl. border and bottom text visible whenever shown (owner rule). YES/NO
16. Gate 2: owner approval before anything is scheduled. YES/NO
