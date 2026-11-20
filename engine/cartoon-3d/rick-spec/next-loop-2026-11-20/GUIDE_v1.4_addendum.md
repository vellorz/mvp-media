---
# VERSION 1.4 ADDENDUM — 2026-11-20 — next loop: the uncertain fields measured again (v4 definitions, 6 tracks, 3 or more methods each)

Owner order 2026-11-20 12:50 PM CT: get the still-uncertain fields down (motion timing, camera move sizes, dissolve length, bed swing, sound effects, key and tempo, all action types, tracked points, asset physics, character proportions, two camera trackers); a field under 99 % is useful guidance at 75 % or more; Black Friday paused. Appended only; v1.3 above is unchanged byte for byte.
Where everything is: `research/rick-style-spec/new-analysis-3/` (RESUME_new-analysis-3.md first). Definitions written before measuring: `_agent-prompts/definitions_v4_2026-11-20.md` (+ per-track PREREG files). Per track: `joins/ characters/ motion/ camera/ assets/ audio/`, each with REPORT.md and results.json. Rules: `RULES_CLONE_v2.md`. Render-facing specs: `RENDER_SPEC_v1.4.md`. Verification: `VERIFICATION_v4_2026-11-20.md`.
STATUS WORDS (changed by the owner on Nov 20): **[RULE]** = two independent measurers at 99 % or more, n at least 20. **[GUIDANCE]** = 75 to 98.9 % per item, OR a population-level number whose independent measurers' medians agree, stated with its window. **[POST-HOC]** = a number produced by an amendment (M2) written AFTER the per-item results were seen; always guidance with its window, never a rule. **[UNCERTAIN]** = under 75 % after three methods; the three results are shown. **[SINGLE]** = one measurer.

## ad. The three core findings after the v4 loop (must be in every document)
1. **SCENE TIME.** Unchanged from v1.3 and now with dissolve detail: shots under 2 s 10 to 53 %, over 4 s 20 to 47 %, median 1.93 to 3.97 s (all 7: 2.83 s); packed one-takes of 9.5 to 14.7 s; camera moving on 80 to 98 % of frames (two trackers, per video) with 18.6 to 28.3 moves per minute. Dissolves: three fits give a consensus median of 8 f (p10 5, p90 12; per video #03 10, #12 7, #04 8.5, #10 10.5, #14 6.5, #22 7, #24 4.5); the curve is smoothstep in 91 to 95 of 102; dissolves in the payoff sentence are longer (median 12 f, n 6).
2. **MUSIC.** Mean gap 14.4 to 18.6 dB, mix -14.0 to -14.1 LUFS, no ducking, bed std 2.3 to 4.0 dB (v1.3, two tools). Correction: the full swing is about 7 to 12 dB (p95 minus p5) or 11 to 15.5 dB (max minus min), each with about +-4 dB uncertainty because the stems the tools read leak part of a quiet bed into the vocal stem [UNCERTAIN]. The cause of the old tool disagreement was a gating difference inside the 3 s window (fixed: the two tools now agree within 0.32 dB on 7 of 7).
3. **SETS AND BODIES.** Torso about 1.0 H (vision measurers, A, B and both old measurers agree on the median; the pixel tools read torsos about half too small), legs 1.1 to 1.3 H, total height 2.9 to 3.35 H, curved noodle arms, mitten hands, no fingers [RULE 148 of 149], outline about 7 to 10 px lit side and 13 to 16 px shaded side at 1080 wide [GUIDANCE, population level], hero props heavy-outlined [SINGLE].

## ae. Agreement before and after, per category (v3 definition unless marked; "v4" = the v4 tolerance)
| category | field | before (v3 loop) | after | status |
|---|---|---|---|---|
| captions | frame and text | 99.9 % | unchanged | RULE |
| characters | no fingers | 99.3 % | unchanged | RULE |
| assets | animated on ones | 99.2 % | unchanged | RULE |
| audio | mix levels as a group | 56 of 56 | unchanged | RULE (as group) |
| camera | pan, L vs D (n 192) | 41.7 % | 77.6 % (v4) | GUIDANCE |
| camera | tilt | 35.4 % | 75.5 % (v4) | GUIDANCE |
| camera | scale | 24.6 % | 70.3 % (v4), 45.8 % (v3) | UNCERTAIN |
| camera | roll | not measured | 62.0 % (v4) | UNCERTAIN |
| camera | move type / ease class / peak frame +-2 f / speed-profile correlation | 74.9 / 84.6 / – / – | 86.5 / 93.2 / 85.3 / 91.5 | GUIDANCE |
| camera | own segmentation start / end / hold share / number of moves | 93.1 / – / 79.8 / 82.2 | 97.6 / 91.5 / 93.8 / 92.2 | GUIDANCE |
| camera | total, two trackers | 65.9 % | 74.1 % | just under 75 |
| camera | foreground layer, parallax FG to BG, layer ranking | – | 63 to 66, 33 to 44, 59 to 70 (fail known answers) | UNCERTAIN, not used |
| joins | dissolve length, three fits within 2 f / within 1 f | 88.6 / 71.6 (two fits) | all three 76.5 / 56.9; at least two 98.0 / 94.1 | GUIDANCE (2 f), UNCERTAIN (1 f, three-way) |
| joins | each fit vs the median of three, 2 f | – | 99.0 / 90.2 / 91.2 | GUIDANCE |
| joins | kind, start, found | 97.4 / 95.7 / 90.7 | 94.9 to 97.4 / 94.0 to 95.7 / 95.3 (majority of three vs verified) | GUIDANCE |
| joins | curve, three readings agree | – | 81.4 % | GUIDANCE |
| characters | head fill width H, A vs A2 (v4) | 62.7 % per-character overall | 77.8 % (n 108); A vs B 78.9 % | GUIDANCE |
| characters | every other build field, per item (A, A2, B) | 20 to 62 % | 4 to 67 % | UNCERTAIN (three methods shown) |
| characters | population medians (post-hoc M2): H, eye spacing, outline lit and shaded, hand | – | five sources agree within tolerance in 8/10, 8/10, 6/10, 6/6, 6/10 source pairs | GUIDANCE, POST-HOC |
| characters | at least two of three methods agree per item: eye size, outline shaded, outline lit | – | 83.8, 82.8, 75.0 % | GUIDANCE, POST-HOC |
| motion | tools vs humans, start/end within 2 f | 54 to 62 (humans) | tools 18 to 48 % | UNCERTAIN, tools not used |
| motion | humans M1 vs M2: start / end / travel within +-3 f; +-4 f | 71.6 / 65.2 / 56.8 (+-2) | 80 / 74 / 67; 85 / 78 / 76 | GUIDANCE with window (POST-HOC) |
| motion | action found; overshoot; settle (humans) | 97.9 / 98.6 / 94.2 | 98.1 / 94.5 / 92.3 | GUIDANCE |
| assets | tools vs humans, start/end within 2 f | 54 to 66 (humans) | 15 to 25 (tools); core window 27 at +-3 | UNCERTAIN |
| assets | humans start / end within +-4 / +-8 f; A vs C start/end within 2 f | – | 75 / 75 ; 80 / 79 | GUIDANCE, POST-HOC |
| assets | easing class, A vs C / M1 vs M2 / tool vs human | 46.4 % | 71.3 / 44.4 / 22 to 29 | UNCERTAIN |
| audio | bed range and closest gap, two tools | 57.1 % | 100 % (but known-answer error +-4 dB) | UNCERTAIN |
| audio | key K1 vs K2 / tempo T2 vs T3 / loop L1 vs L3 | 2 of 4 / 2 of 4 / 3 of 4 | 85.7 / 71.4 / 71.4 (100 with octave) | UNCERTAIN (known answers fail for key; tempo and loop pass 7 of 7) |
| audio | SFX onsets, two methods within 2 f | 64.2 to 68.5 % (v3 tool pair) | 9.4 % (new pair, 703 events) | UNCERTAIN |
Rule-grade facts remain four. New GUIDANCE facts: camera pan and tilt sizes (with scale and roll excluded), camera type, ease and timing, dissolve length at +-2 f, dissolve curve, kind/start/found of joins, head width, and the post-hoc population numbers above.

## af. Joins and dissolves (joins/REPORT.md)
- Third fit (blendtemporal.py, one shared blend curve per window, no reference frames) passed a known-answer test of 63 synthetic clips (length within 2 f 95.2 %, within 1 f 85.7 %, curve 83.9 %, cut vs dissolve 100 %). Consensus (median of three fits): median 8 f, p10 5, p90 12, longer for the payoff and for longer incoming shots (rho 0.28, p 0.004); no clear effect of sentence position, match vs plain, bridge object or camera motion (all p > 0.2).
- Dissolve starts do not sit on word starts (31 of 102 = chance) but on a sentence start 21 of 102 = 3.7 times chance (p < 1e-6) [GUIDANCE]. Hard cuts: 11 of 15 land 0 to +2 f after a word start (chance 27 %), 13 of 15 are in #24, and the vocal-stem timing keeps only 4 of 15 there: [UNCERTAIN]. Transcript word times and vocal-stem onsets agree per join only 69.7 % within 2 f, so no timing finer than +-2 f can be claimed.
- 20 dissolves are 11 f or longer (5 payoff, 5 in the 3 to 15 s stretch, 12 match). Match dissolves spread evenly (14 per third). Camera moving on the incoming side at 118 of 122 joins.

## ag. Camera (camera/REPORT.md)
- Trackers L (LK flow) and D (DIS flow) passed the known-answer test on the far band (96.3 % sizes, 100 % timing); the old tracker A failed (75.9 %).
- Pan and tilt sizes are guidance, scale and roll are [UNCERTAIN] (push-in scale agrees on 65 %, pull-out 56 %). Use the recipe table with its scale column marked uncertain:
| move | n | duration f p10 / median / p90 | scale ratio p10 / median / p90 [UNCERTAIN] | peak speed % W per frame |
|---|---|---|---|---|
| slow push-in | 85 | 23 / 57 / 142 | 1.10 / 1.38 / 3.14 | 0.33 / 1.9 / 8.2 |
| reveal pull-out | 52 | 25 / 57 / 120 | 0.34 / 0.58 / 0.92 | 0.73 / 3.1 / 8.1 |
| orbit, truck, pan | 17 | 11 / 27 / 70 | about 1.0 | 0.10 / 0.29 / 2.8 |
| drift | 17 | 5 / 11 / 34 | about 1.0 | 0.06 / 0.11 / 0.37 |
| crane, tilt-follow | 13 | 7 / 28 / 44 | about 1.0 | 0.11 / 0.62 / 1.5 |
| crash push | 5 | 8 / 12 / 13 | 1.06 / 1.13 / 1.82 | 0.34 / 0.93 / 5.2 |
| impact jolt | 3 | 6 / 6 / 7 | about 1.0 | about 0.17 |
- Eases: push-in linear 29 and ease-in-out 27; pull-out ease-out 20. Moving share 0.80 to 0.98, longest fully still run 10 to 101 f by tracker (#10: L 31, D 101; #04: L 44, D 10), so "no still run over 8 f" from v1.3 is now [UNCERTAIN] and the safe build value is "never still over 1 s except the ending hold". Parallax FG:BG and the foreground layer could not be measured.

## ah. Character build (characters/REPORT.md)
- Pixel methods A and A2 passed a synthetic known-answer set (A 13 of 17 fields) but disagree on real frames; blind method B (crop pack, 190 pairs, two Sonnet measurers) was added as the third method. Per item only head fill width reaches guidance (A vs A2 77.8 %, A vs B 78.9 %). Everything else per item is [UNCERTAIN]; the three results are in the report. The pixel tools under-read torsos by about half (they stop at belts, coats and sleeves), so torso, leg and total height come from the vision measurers.
- Population medians (five sources: A, A2, B, first, second measurer; bootstrap 2000, seed 2026112004; POST-HOC): head fill width 22.2 to 24.3 % of frame width; eye spacing 24.1 to 27.5 % H; outline lit 6.6 to 10.0 px; outline shaded 13.0 to 16.0 px; hand 9.5 to 17.2 % H; eye size 7.3 to 13.0 % H; torso height A 0.57 / A2 0.55 / B 1.00 / first 1.00 / second 1.01; torso width 0.35 to 0.89; leg 0.85 to 1.28; total height 2.14 to 3.34 (B 2.91, n 66).
- Eyes sit at 69 % of the head height above the chin; arms 66 of 71 curved noodle; head colour #fbf4f1, outline ink #321c2a.

## ai. Motion (motion/REPORT.md)
- Point-tracking tools (A: LK with camera and parallax compensation; B: compensated frame difference) failed the known answer on every timing field except B's start (84.1 %), and on real data agree with the human measurers 8 to 48 % (start/end within 2 f). Tool windows run about 10 f wider than the human windows. Only 12 locked-camera stretches exist (9 items inside one), which confirms that "locked camera" cannot be the measuring condition for Rick.
- What stands (humans, POST-HOC window statement): timing known to +-3 f for start and +-4 f for end and travel between two blind human measurers (75 % reached at those tolerances). 197 of 304 items agree within 3 f on both start and end; from those only: snap n 93 median travel 2.5 f (p10 1, p90 4), tween n 83 median 6.0 f (4.5 / 11), cycle n 18 median 22.5 f (10.6 / 49.9), slow n 3; overshoot 0 to 2.4 %; anticipation 0 to 5.6 %; holds (36, first measurer) median 26 f (p10 8.5, p90 67.5). Bias: the agreeing subset leans toward short actions.
- Median consensus travel per video (f): #03 5.25, #04 11, #10 7.25, #12 5.25, #14 7.5, #22 12, #24 6.75.

## aj. Asset physics (assets/REPORT.md)
- 412 assets tracked by A (box with camA), B (frame-difference blob) and C (A with local ring background); known answers 87.8 % (A, C) and 80.7 % (B). The tools measure the whole motion, the humans a shorter segment (median offset -7 f start, +8 f end). Start/end vs humans [UNCERTAIN]; humans agree at +-4 f (start) and +-8 f (end); A and C agree within 2 f on 80 % / 79 %.
- Easing is [UNCERTAIN] (A vs C 71.3 %, humans 44.4 %). Where A and C agree: linear 104, ease-out 79, ease-in 70, ease-in-out 36. Core duration (speed at least 25 % of peak) median 22 f (p10 5, p90 53); humans' agreed segments median 11.5 f. Bounce rate 1.0 % (humans) to 3.7 % (tools); overshoot 0.8 % (humans); the tools' 28 % is noise, use the human value. Falls (relaxed R2 0.9, POST-HOC): humans 4.7 to 5.1 screen heights per s^2 (n 24 and 12). Flat FX core duration f: spark 23, ring 27, speed lines 12, foam 24, flash 12 (n 4 to 6); frames to 90 % size 5 to 10.

## ak. Audio (audio/REPORT.md)
- Bed swing: see ad.2 and the per-video table in the report (p95 minus p5 7.0 to 11.8 dB; max minus min 11.1 to 15.5; closest gap p5 8.3 to 15.0; each +-4 dB).
- Key: profile tools read D minor on #12, #04, #10, #22, #24, #14 (all four methods), E minor / D major on #03; bass-tonic tools read A minor. All fail known answers with a voice on top [UNCERTAIN]. Tempo (T2/T3, same beat level, known-answer 7 of 7, agree 5 of 7): #03 78.5, #12 100 to 104, #04 80, #10 100 (T3 66.7), #14 96.8, #22 75.6, #24 87.0 BPM [UNCERTAIN, near guidance]. Loop length (L1/L3, s): #03 6.11, #12 9.24 or 18.47, #04 5.97, #10 7.20 or 14.40, #14 9.93, #22 6.35, #24 11.04; the two misses are exact 2x. SFX per event [UNCERTAIN]; picture-sound lag cannot be told from chance.

## al. Corrections to v1.3 (old, new, why)
| where | old | new | evidence |
|---|---|---|---|
| ad.2 / w.2 | bed swing 10.9 to 16.7 dB (tool A), 11.1 to 13.6 (tool B) | p95 minus p5 7.0 to 11.8, max minus min 11.1 to 15.5, each +-4 dB | audio |
| x.3 legs, total | legs 1.28 / 1.31, total 3.22 / 3.35 | legs 1.1 to 1.3, total 2.9 to 3.35 (B reads 1.11 and 2.91) | characters M2 |
| x.4 snap and tween travel | snap median 2 f, tween 7 f (first measurers) | snap 2.5 f, tween 6.0 f from items two humans agree on (within 3 f) | motion M2 |
| x.4 overshoot | about 98 % none | humans 94.5 % agreement; tool overshoot (28 %) is noise | motion, assets |
| x.5 loop median 13 f | 13 f (8 to 16) | humans 11.5 f (n 6); tools disagree | assets |
| x.1 dissolve median | 7 f (n 60 clean fits) | 8 f consensus of three fits, p10 5, p90 12 | joins |
| x.2 still run | longest fully still run 0 to 8 f | tracker-dependent 10 to 101 f; say "under 1 s" | camera |
| x.9 key | D minor for 5 of 7 [single] | profile tools D minor, bass tools A minor: [UNCERTAIN] | audio |
| x.9 tempo | 96 to 123 BPM [single] | 75.6 to 104 BPM at one beat level, two tools agree on 5 of 7 | audio |
| w.1 camera moving 84 to 96 % | 84 to 96 % | 80 to 98 % (two new trackers) | camera |

## am. Clone spec v2: build values (use these for the next render; status in brackets)
1. Camera: moving on at least 85 % of frames, idle drift 0.05 to 0.2 % W per frame, never fully still over 1 s except the ending hold [GUIDANCE]; push-ins 23 to 142 f (median 57), pull-outs 25 to 120 f, crash push 8 to 13 f, jolt 6 to 7 f [GUIDANCE for durations; scale ratios UNCERTAIN]; pan and tilt sizes may use the recipe table [GUIDANCE].
2. Joins: dissolves 5 to 12 f (median 8), smoothstep, camera moving through them; payoff dissolves about 12 f; about 40 % match dissolves; hard cuts allowed freely [GUIDANCE].
3. Characters per ah and RENDER_SPEC_v1.4.md: no fingers [RULE]; torso 1.0 H; legs 1.1 to 1.3 H; total 2.9 to 3.35 H; noodle arms; mitten hands 10 to 12 % H; outline 7 to 10 px lit and 13 to 16 px shaded at 1080 wide [GUIDANCE].
4. Motion: snap 1 to 4 f (median 2.5) or rigid tween 5 to 11 f (median 6); holds median 26 f; timing window +-3/+-4 f [GUIDANCE with window].
5. Assets on ones [RULE]; falls 4.7 to 5.1 screen heights per s^2; FX 12 to 27 f; no bounce on falls [GUIDANCE].
6. Captions on the word or 0 to 1 f before [RULE for the method]; mix levels [RULE as group]; bed std 2.3 to 4.0 dB; no ducking.

## an. Blind check on this version
BLIND_CHECK_V14_PLACEHOLDER

## ao. Disclosures and process notes
- Models: Opus for all six measuring tracks; Sonnet for the two blind crop measurers (method B for characters); Fable (this orchestrator) for adjudication, synthesis and the rulebook. The platform may substitute models; each report states what ran.
- The measuring harness blocked sub-agents from writing REPORT.md files; the orchestrator saved each hand-back as the track's REPORT.md. Each is a verbatim summary of the agent's numbers, not a re-measurement.
- Three amendments labelled M2 (characters, motion, assets) were added AFTER per-item results were seen. They produce guidance with a stated window or population-level numbers only; no earlier number or tolerance changed. A permission block stopped one agent from installing a speech-timing package; vocal-stem onsets were the only second word-timing source.
- The synthetic known-answer clips for the camera and assets were built from reference frames as textures; they stay private in the container and are not in the repo.
- Limits: per-item agreement under 75 % for most character, asset-timing and audio fields means those numbers describe populations, not any single shot. The 99 % standard is met by four facts only.
- Next loop: (1) a 3D camera solve (structure from motion) for push/pull scale and the foreground layer; (2) hand-label a locked set of 100 actions with frame strips by two people to settle the +-3 f window; (3) a clean stem from the platform (music-only export is impossible, so re-derive the bed with a known-bed overlay test); (4) a listening panel for key and SFX.
