# Black Friday / Philadelphia: change report after the 7-video clone run (2026-11-20)

> **THE THREE CORE FINDINGS, as of guide v1.3 (7 Rick videos frame by frame).**
> 1. **SCENE TIME.** Rick: 10 to 53 % of shots under 2 s, 20 to 47 % over 4 s, median 1.93 to 3.97 s. His long shots are packed one-takes of 9.5 to 14.7 s with 6 to 17 camera moves. Camera moving on 84 to 96 % of frames.
> 2. **MUSIC.** Bed mean 14.4 to 18.6 dB under the voice, mix -14.0 to -14.1 LUFS, no ducking, bed level standard deviation 2.3 to 4.0 dB.
> 3. **SETS AND BODIES.** Torso 1.00 head widths, legs 1.25 to 1.28, total 3.2 to 3.35, noodle arms, mitten hands, no fingers. Outline thin toward the light, about twice as thick away from it. Hero props carry heavy dark outlines [single measurer].

Status: PROPOSAL for the owner. Nothing in the Black Friday build was changed, deleted or re-rendered by this run. The round 6 video and the round 7 (bf11) clips stay as they are until the owner chooses.

What was measured: `final/round6/BlackFriday_Philadelphia_round6_small.mp4` (1,752 frames), with the same two camera trackers and the same cut detector used on Rick's videos. Files: `/root/work/bf6/` copied to `new-analysis-2/black-friday-round6/` (joins_r6.csv, camstatsA.json, camstatsB.json, cam_compare.json). Join list: 14 dissolves from the round 5 shots report (confirmed at the same frames by the automatic detector on round 6) plus 8 hard cuts found by a frame-difference scan of round 6 (before frames 89, 221, 868, 1283, 1320, 1405, 1647, 1689). Audio numbers are quoted from `final/round5/audio_report.md`; character numbers from `final/round6/visual_report.md`; the round 8 cast was read off `final/round8/round8_cast_rick-style_draft1.jpg` by pixel position (one reader, about ±5 %). Black Friday motion (pose timing) was NOT measured in this run.

Rick's values are from guide v1.3 sections w to ab. Status words: [rule-grade] = two measurers agree on 99 % or more; everything else is measured guidance.

## A. Already inside Rick's range: keep

| measure | Rick, 7 videos | Black Friday round 6 | source |
|---|---|---|---|
| median shot length | 1.93 to 3.97 s | 2.53 s (23 shots) | joins_r6.csv |
| shots under 2 s | 10 to 53 % | 26 % (6 of 23) | joins_r6.csv |
| hard cuts | 0 to 13 per video | 8 of 22 joins | frame-difference scan |
| dissolve length | per-video median 6 to 11 f | 5 to 11 f, median 7 | round 5 shots report, K4 |
| camera moving, share of frames | 84 to 96 % | 86 % and 84 % (two trackers) | camstatsA/B.json |
| camera moves per minute (tracker) | 21 to 34 | 25.7 and 26.7 | camstatsA/B.json |
| mix loudness | -14.0 to -14.1 LUFS | -14.1 LUFS | ffmpeg ebur128 on round 6 |
| bed under the voice | mean 14.4 to 18.6 dB | 16.0 dB | round 5 audio report, A4 |
| bed level movement (std of 3 s level) | 2.3 to 4.0 dB | 4.0 dB | round 5 audio report, A4 |
| narration speed | 3.37 to 3.85 words per s | 3.44 | RESUME.md |
| end after the last word starts | 0.27 to 0.89 s | 0.82 s | words.json, 1,752 f |
| payoff | poster inside the final scene, fully visible | kept | owner rule |

## B. Changes proposed (old, new, evidence), in priority order

### B1. Characters: rebuild to Rick's build (owner direction Nov 20; the largest change)
| part | round 6 | round 8 draft 1 | change to | Rick evidence |
|---|---|---|---|---|
| torso height | 0.63 to 1.07 head heights | about 0.70 head widths | 1.00 (0.92 to 1.18) | x.3: median 1.00 for both measurers, n = 78 and 76 |
| legs | 0.73 to 1.23 | about 0.98 | 1.25 to 1.3 | x.3: 1.28 and 1.25 |
| total height | not measured | about 2.7 | 3.2 to 3.35 | x.3: 3.22 and 3.34 |
| arms | one straight card (round 5 ledger) | two straight segments with an elbow | one curved "noodle" stroke with no fixed elbow, 5 to 6 % of head width thick | x.3: 85 of 113 visible arms are noodles, 17 are two-segment |
| head outline | one even line, 12 px at a 515 px head = 2.3 % | one even line, about 2.1 % | 3.1 to 3.7 % of head width toward the light, about 6 % away from it and under the chin; dark plum, maroon or navy, never pure black | x.3: lit side A 3.7 %, B 3.1 %; shaded side B 6.1 %, n = 54 |
| hands | round | round with a small thumb bump | plain round mitten, 12 % of head width, no bumps | x.3: no fingers, 148 of 149 [rule-grade] |
| feet | not measured | small ovals | about 15 % of head width | x.3 [single] |
| eyes | not measured | dots | height 12 to 13 % of head width, centres 27 % apart | x.3 |
The draft keeps the round head, flat white face and dark stick legs, which match. Rule 253 ("jointed limbs, always bent") and the round 5 lesson "arms must have elbows" are reversed by this evidence: see the rules revision.

### B2. Motion (owner's highest priority; Black Friday not measured here, so these are build targets, not a scored gap)
- Pose changes: snap in 1 to 4 f (median 2) or a rigid whole-body tween in 5 to 11 f. No anticipation, no overshoot, no squash and stretch (0 f at the 90th percentile).
- Bodies hold 50 to 80 % of the time (holds median 24 f) while the face changes 1.4 to 2.5 times per second. Mouths 2 to 2.5 f per shape.
- Round 5 ledger: torsos upright (lean 0 to 1 degree) and 1.27 events per second inside shots. Rick: torso tilt median 5 degrees (n = 106), 1.2 to 1.9 picture events per second.
- All moving props and FX animated on ones [rule-grade, 393 of 396]. Falls accelerate (about 3.5 to 8.8 screen heights per s²) and land with no bounce.
All timing values above are guidance: two measurers agreed on 74.1 % of action fields.

### B3. Scene time: add packed long takes
- Round 6 has 3 of 23 shots over 4 s = 13 % (Rick 20 to 47 %), and its longest shot is 4.55 s (Rick has one-takes of 9.5 to 14.7 s in the openings and mid-story).
- Change: remove the hard cut before frame 89 (2.97 s) so the hook is one take of about 5.5 s with at least 3 eased camera beats (6 of 7 Rick videos have no join in the first 3 s). Join one more pair of short neighbours in the same set into a packed take, so 5 or more shots run over 4 s.
- This partly undoes round 5, which shortened shots to meet the older, narrower band (20 to 26 % over 4 s). The band was too narrow.

### B4. Camera: more big beats, no dead camera
- Fast zooms (scale change of ×1.5 or more inside 25 f): Rick 10 to 24 per minute by the same tracker, round 6 8.2 per minute (8 in 58 s). Add at least 3: one crash push on a punch word (9 to 25 f, ×1.8 or more) and one reveal pull-out (21 to 37 f) in each third of the video.
- The camera is fully still for the whole shot f1057-1123 (57 f, both trackers) and for 45 to 47 f inside f651-780. Add a slow drift of 0.05 to 0.2 % of frame width per frame; Rick's longest fully still run is 0 to 8 f by the pacing tool.
- On each impact, a one-frame punch-in of +3 to +7 % with a 6 to 10 f ease back.
Move sizes are single-measurer values (the two trackers agree on start frames 93 % of the time but on sizes only 25 to 42 %).

### B5. Sets and props
- Keep walls thin-lined. Give hero props (BIG FRIDAY sign, ledger, newspaper, poster frame) a heavy dark outline of about 5 to 10 px at 1080 wide [single measurer, guidance].
- Round 6 report still lists a dull payoff (p98 under 0.84 on f1534-1751) and no foreground layer in two shots; those stay on the Black Friday thread's list and are not changed by this run.

### B6. Audio
- True peak -1.8 dBTP against Rick's -1.9 to -2.2: lower the limiter ceiling by 0.2 dB.
- No other change. SFX per event is [uncertain] (three methods failed their known answers), so no SFX rule comes from this run.

### B7. Script
- No change proposed. 198 words at 3.44 words per second and the hook, doubter, escalations and reveal already follow the guide; nothing measured in this run contradicts the script.

## C. What this run does not support changing
Captions (1 to 3 words on the word, baseline 71.7 %), mix level, bed level and swing, dissolve lengths, share of short shots, the poster-inside-the-payoff ending.

## D. The choice for the owner
The round 7 clips (bf11) are rendered and pushed. Recommended: keep them as the baseline, and build round 8 on the clone spec (B1 to B4), re-rendering only the shots that change. Characters appear in nearly every shot, so B1 means most shots re-render. Nothing is discarded either way.
