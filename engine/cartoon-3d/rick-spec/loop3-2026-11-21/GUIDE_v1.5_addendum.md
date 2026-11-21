---
# VERSION 1.5 ADDENDUM — 2026-11-21 — loop 3: 3D camera solve and two-person hand-labelled actions (definitions v5, written before measuring)

Owner order 2026-11-20 5:15 PM CT: do the proper 3D camera solve and the two-person hand-labelled set of actions. Appended only; v1.4 above is unchanged byte for byte. Files: `research/rick-style-spec/new-analysis-4/` (`_agent-prompts/definitions_v5_2026-11-20.md`, `camera3d/REPORT.md`, `labels/REPORT.md`).

## ap. Results in one table (agreement; v5 definition)
| field | result | status |
|---|---|---|
| camera scale, S1 vs S2 on 192 real moves | 47.4 % (S1 passed its known answer 90.4 %, S2 failed 86.5 %) | UNCERTAIN (still) |
| camera roll | 46.4 % (both tools passed known answers) | UNCERTAIN |
| camera pan, tilt | 27.6 %, 27.6 % (known answers 100 %, 98 to 100 %) | UNCERTAIN; the loop-2 band trackers (77.6, 75.5 %) stay the reference for pan and tilt |
| layer ranking, parallax near:far, depth ratio | 12.5, 15.6, 4.1 %; both tools failed their known-answer tests | UNCERTAIN, not used |
| scale on short moves (30 f or less), post-hoc split | 75.8 % (roll 69.7, pan 47.0, tilt 48.5) | UNCERTAIN (post-hoc) |
| hand-labelled actions, start within 2 f, matched items, 3 labeller pairs | 81.1, 80.3, 81.7 % | GUIDANCE |
| end within 2 f | 78.6, 77.6, 75.5 % | GUIDANCE |
| start within 3 f / end within 4 f | 85.0 to 89.1 / 85.4 to 85.9 % | GUIDANCE (wider windows, post-hoc) |
| action type, matched items | 68.1, 70.5, 71.4 % | UNCERTAIN |
| same set of actions found (A vs B, strict) | 68.8 % (78.8 % of A, 84.4 % of B) | UNCERTAIN |
| window has an action or not, A vs B | 92 of 100 | GUIDANCE |
| overshoot | A said yes 5 times, B 0 | UNCERTAIN |
Rule-grade facts remain four. Nothing in this loop reached 99 %.

## aq. 3D camera solve (camera3d/REPORT.md)
- Four synthetic clips with three flat cards at known depths, 52 moves, Rick-like sharpening and compression, were the known-answer test. Method S1 (essential matrix and homography chain with bundle adjustment) passes scale 90.4, roll 100, pan 100, tilt 98.1; S2 (per-layer similarity fits plus parallax) passes roll, pan, tilt and fails scale (86.5); S3 (photometric alignment) fails everything. No tool passed layer ranking (75.0, 60.0), parallax (72.9, 50.0) or depth ratio (70.0, 35.0).
- On Rick's 192 real moves the two solvers agree far worse than on the synthetic set: scale 47.4, roll 46.4, pan 27.6, tilt 27.6, layer ranking 12.5. Agreement falls with move length (scale 75.8 up to 30 f, 44.3 for 31 to 60 f, 21.5 above 60 f). A true 3D solve of Rick's long moves is therefore NOT achieved; the parallax number (near:far) cannot be given.
- Likely reasons (untested): the synthetic set is easier than the footage; the two tools mean different things by "far layer"; the character plane is only about 12 % of the frame; focal length is unknown.
- Useful table (S1 scale ratio p10 / median / p90, all UNCERTAIN): push-in 0.61 / 1.28 / 4.33 (n 85); pull-out 0.17 / 0.56 / 1.12 (52); orbit/truck/pan 0.61 / 1.01 / 1.08; drift 1.00 / 1.01 / 1.04; crane 0.98 / 1.02 / 1.06; crash push 1.04 / 1.09 / 2.35; jolt about 1.003. S2's medians are close (push-in 1.25, pull-out 0.79). Soft build targets: push-in about 1.25 to 1.3x, pull-out about 0.6 to 0.8x (v1.4 table said 1.38 and 0.58; both within noise).

## ar. Hand-labelled actions (labels/REPORT.md)
- 100 windows of 36 frames (seed 2026112005, 7 videos, 14 or 15 each), every frame shown with a counter. Three blind Sonnet labellers (A, B, C), each did all 100. Items both found (matched by time overlap): A to B 238, A to C 254, B to C 241.
- Timing: start within 2 f 80.3 to 81.7 %, end within 2 f 75.5 to 78.6 % in all three pairs; within 3 f start 85.0 to 89.1 %, within 4 f end 85.4 to 85.9 %. So the ±3/±4 f window of v1.4 is now ±2 f for items that both people found [GUIDANCE]. But only 68.8 % of the actions are found by both, and the action type agrees only 68 to 71 %.
- Consensus (two of three within 2 f on 164 of A's 302 actions): median travel in frames, face change 3 (p10 1, p90 4.5, n 81), gesture 4 (3 to 6, n 21), mouth change 4.5 (2 to 35, n 17), tween 6.5 (4 to 35, n 14), walk 9.5 (5.5 to 35, n 14), fall 9 (n 7), turn 10, cycle 11. The labellers hardly used "snap" (1 of 164), unlike the first measurers: the vocabulary differs, so the earlier snap/tween numbers stand but this set does not confirm them.
- Only 5 of the 20 planned still-camera windows are truly still; the locked-camera question is therefore not answerable from this set.

## as. Corrections and clone spec impact
| where | old | new |
|---|---|---|
| ai (v1.4) motion window | ±3 f start, ±4 f end (humans, 75 %) | ±2 f for both, 75.5 to 81.7 %, items both people found (GUIDANCE) |
| ag (v1.4) camera scale ratios | push-in median 1.38, pull-out 0.58 | push-in about 1.28, pull-out about 0.56 to 0.79; all UNCERTAIN |
| ag (v1.4) "pan and tilt guidance 77.6 / 75.5" | kept | the new 3D pair agrees only 27.6 % on pan and tilt; the loop-2 numbers were band-tracker agreement, not proof of 3D truth. Keep as guidance for screen-space sizes only |
| new | face change travel 3 f (1 to 4.5), gesture 4 f, mouth 4.5 f | GUIDANCE (three labellers) |
No render rule is added or removed. Camera rules 302 to 305 stay.

## at. Blind check on this version
Not run in this loop (no new build values beyond the table above).

## au. Disclosures
- Models: Opus built the packs and ran the camera solve; Sonnet did all three labelling passes (the first two labellers lost image context during their runs and labelled some windows from notes: A w000 to w020, B w094 to w099 and parts of w000 to w049; labeller C saved each window right after viewing it). Orchestrator did the scoring in-session (script output in this session; consensus in labels/consensus_v5.json).
- Amendments T1-a and T1-b (camera3d) were written after the known-answer work began, labelled post-hoc; no pre-registered pass mark changed. Both amendments, the dev-clip fixes (A1) and the S3 change are in the definitions file.
- The 99 % standard was not met by any field here. The labels agree at guidance level only for timing of items both labellers found; the action list itself is not stable (68.8 %).
- Next loop: shorter-move 3D solve (30 frames or fewer) with a real focal-length estimate; a fourth labeller with a smaller type list (face / body / mouth / object); only frame-differenced still windows for locked-camera timing.
