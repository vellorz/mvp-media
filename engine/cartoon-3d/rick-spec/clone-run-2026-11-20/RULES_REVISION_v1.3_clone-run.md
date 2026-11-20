# Rules revision after the 7-video clone run (2026-11-20): revisions to proposed rules 230 to 266, and new rules 280+

> **THE THREE CORE FINDINGS, as of guide v1.3.** 1. SCENE TIME: 10 to 53 % of shots under 2 s, 20 to 47 % over 4 s, median 1.93 to 3.97 s; long shots are packed one-takes; camera moving on 84 to 96 % of frames. 2. MUSIC: bed mean 14.4 to 18.6 dB under the voice, -14 LUFS, no ducking, bed level std 2.3 to 4.0 dB. 3. SETS AND BODIES: torso 1.00 head widths, legs 1.25 to 1.28, total 3.2 to 3.35, noodle arms, mitten hands, no fingers; outline thin toward the light and about twice as thick away from it; hero props heavily outlined [single].

Status: PROPOSAL, same standing as rules 230 to 266 (`experiments/2026-11-18_rick-99-test/RULES_PROPOSAL_230plus_from-rick-analysis.md`). Those are not in `RULES_CONSOLIDATED.md` yet; the Black Friday thread edits that file and holds draft rules 267 to 279, so new rules here start at 280. Evidence for every number: guide v1.3 sections w to ac and `research/rick-style-spec/new-analysis-2/`.
Owner standard applied: only a fact that two measurers agree on at 99 % or more (at least 20 compared fields) is written as a RULE. Everything else is GUIDANCE with its agreement rate.

## 1. New rules (rule-grade)
280. NO FINGERS. Hands are plain dark round mittens, about 12 % of head width. No fingers, no thumb bumps. One pointing index finger is allowed for a single pointing gag. (148 of 149 characters, two measurers 99.3 %.) Check: every cast sheet and every close-up.
281. EVERY MOVING ASSET IS ANIMATED ON ONES. Props, vehicles, particles and FX change on every frame while they move; no stepped "on twos" motion. (393 of 396, 99.2 %.) Check: frame-step any moving asset.
282. CAPTIONS ARE MEASURED BY ON-FRAME AND TEXT. The caption check compares each caption's first frame (within 1 f) and its text against the plan; this measurement is rule-grade (3,830 of 3,834, 99.9 %). Build target (guidance, from one transcript): the caption appears on the word or 1 f before it, never later than +2 f; hard swaps, no gaps, full opacity through dissolves.
283. MIX LEVELS AS A GROUP. Mix -14.0 to -14.1 LUFS, voice -14.2 to -14.4 LUFS, true peak -1.9 to -2.2 dBTP, bed mean 14.4 to 18.6 dB under the voice, bed level std (3 s windows) 2.3 to 4.0 dB. (Two tools, 56 of 56 fields on 7 videos; 7 values per field, so it passes as a group, not field by field.) Check: `audio.py` plus a second tool.

## 2. Revisions to proposed rules 230 to 266 (old text stays in the proposal file; this is the amendment)
| rule | change | evidence |
|---|---|---|
| 230 shot-length shape | Widen: median 1.9 to 4.0 s; at least 10 % of shots under 2 s; 20 to 47 % over 4 s is Rick's range, so "at most 26 % over 4 s" is withdrawn. | w.1 |
| 231 long takes packed | Keep and strengthen: one-takes of 9.5 to 14.7 s carry 6 to 17 eased camera moves. | x.2 |
| 232 hook | Replace "a join or 3 events in the first 3 s" with: no join is needed in the first 3 s (6 of 7 videos have none); open on a one-take with at least 3 eased camera beats. | x.1, x.2 |
| 233 payoff is fast | Two endings are valid: a burst of short shots (32 to 40 joins per minute) or one long reveal take of 6.8 to 10.9 s. "The last shot is not the longest" is withdrawn. | x.6 |
| 234 hard cuts | Keep. Dissolves 3 to 14 f, per-video median 6 to 11 f, all videos median 8 f. Length is guidance (two fits agree within 2 f on 88.6 %). | x.1 |
| 236 joins and words | Keep. The middle of a join is within 3 f of a word start for 58 to 90 % of joins. | x.6 |
| 237 events in shots | Lower bound for visual changes per minute becomes 151 (range 151 to 214). | x.6 |
| 240 in-shot relight | Add: 1-frame relights and 16 to 18 f ramps both occur. | x.1 |
| 241 caption grouping | Add: 2.73 to 3.06 captions per second, dwell median 10 f (4 to 16 f), 1 word in at least 75 % of captions, 3 the normal maximum. | x.7 |
| 243 bed rides | Keep the mean gap (now 14.4 to 18.6 dB). The full swing "11 to 15 dB" becomes guidance: two tools agree on only 4 of 7 videos. Use the std of 2.3 to 4.0 dB as the check. | w.2 |
| 246 bed character | Tempo guidance "92 to 100, never 120" is withdrawn: one tool reads 96 to 123 BPM on these 7 [single]. Key: D minor for 5, E minor for 1 by one tool [single]. | x.9 |
| 247 SFX layers | Stays guidance only. Three more detection methods failed their known answers (best 93.3 %). | x.9 |
| 248 final mix | True peak -1.9 to -2.2 dBTP. | w.2 |
| 250 set-edge lines | Walls and large surfaces stay thin-lined. Hero props may carry heavy dark outlines of 5 to 30 px [single, guidance]. | w.3 |
| 251 dark scenes | Night down to luma 0.25 to 0.33, bright inserts up to 0.76 [single]. | x.8 |
| 252 body proportions | Torso 1.00 head widths (0.92 to 1.18), width 0.77 to 0.89; legs 1.25 to 1.3 (0.94 to 1.36); total 3.2 to 3.35. Robes and dresses 1.6 to 2.2 neck to hem with legs hidden. Guidance (63.1 % per-field agreement; the medians of the two measurers match). | x.3 |
| 253 jointed limbs, always bent | REVERSED. Arms are one curved stroke with no fixed elbow (85 of 113 visible arms); two-segment arms are the minority (17). Thickness 5 to 6 % of head width. Legs are straight sticks or noodles. | x.3 |
| 254 lean | Standing tilt median 5 degrees (n = 106). The 15 to 45 degree effort range stays unverified. | SYNTH act.torso_tilt_deg |
| 255 hold, then snap | Holds median 24 f (90th percentile 64). Snap in 1 to 4 f, or a rigid whole-body tween in 5 to 11 f. No anticipation, no overshoot, settle at most 1 f, no squash and stretch. Guidance (74.1 %). | x.4 |
| 256 impact FX | "At most 3 shake moments" is withdrawn (#24 has 8 camera kicks in 5.2 s). Impact = one-frame punch-in of +3 to +7 %, then a 6 to 10 f ease back. | x.2 |
| 235, 238, 239, 242, 244, 245, 249, 257 to 266 | Unchanged. | |

## 3. Guidance for the clone build (NOT rules; agreement under 99 % or one measurer)
G1. Camera moving on at least 85 % of frames; idle drift 0.05 to 0.2 % of frame width per frame; no fully still run over 8 f except the ending hold.
G2. Every 10 to 15 s one crash push (9 to 25 f, ×1.8 or more, peak on the word) and one reveal pull-out (21 to 37 f, to 0.25 to 0.5 scale).
G3. About 40 % of dissolves carry a bridge object in the same screen spot (offsets up to 19 % of width occur); the camera moves through the dissolve.
G4. Head outline 3.1 to 3.7 % of head width toward the light, about 6 % away from it; dark plum, maroon or navy, never pure black.
G5. Faces change 1.4 to 2.5 times per second while bodies hold; mouths 2 to 2.5 f per shape.
G6. Falls accelerate at about 3.5 to 8.8 screen heights per s² and land with no bounce; flat 2D FX last 4 to 11 f.
G7. End 0.3 to 0.9 s after the last word starts, on a held frame with one last face or FX change.

## 4. New process rules
284. JOINS ARE CONFIRMED BY EYE. The automatic detector both misses joins and reports relights, flashes and focus pulls. Every join in a reference log is confirmed on a frame strip, and disputed ones are adjudicated one by one in writing.
285. A 2D TRACKER CANNOT SIZE A 3D CAMERA MOVE. Use trackers for when a move starts and whether it eases (93 % and 85 % agreement), never for how big it is (25 to 42 %).
286. BLIND CHECK BEFORE A GUIDE VERSION IS CALLED COMPLETE. A fresh agent that reads only the guide predicts held-out shots as intervals of fixed width; the score is printed in the guide (v1.3: 422 of 466 = 90.6 %).
287. MEASURE FEWER, CLEANER ITEMS FOR MOTION. Two careful measurers do not agree on hand-animated pose timing at ±1 to 2 f. Motion fields meant to become rules are measured as tracked points on locked-camera shots.
