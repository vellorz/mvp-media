# Loop 4: camera and layers, second attempt (definitions v6 section 7), 2026-11-21. Opus hand-back saved by the orchestrator. Files: PREREG_camera_v6.md (written before tool output; amendments A1 to A3 post-hoc on dev clips only), results.json, per_move.csv, agreement_s1_s2.json, known_answer/, real_outputs/, _tools/.
## Bottom line
No camera field passes. Agreement on the 192 real moves (v6 / loop 3): scale 53.1 % (47.4), roll 43.2 % (46.4), pan 27.1 % (27.6), tilt 27.6 % (27.6), layer ranking 12.0 % (12.5), parallax 49.5 % at the v6 20 % tolerance and 31.5 % at 10 % (15.6), speed-curve class 64.9 %. All UNCERTAIN. Recipe scale ratios are reported but not usable as numbers; parallax is not reported.
Focal length from footage: self-calibration found the true focal within 1.5 % on 8 of 8 synthetic clips, but found 0 qualifying segments in Rick's 7 videos (so S1 used the default 1.3 W). Agent's reading (not tested): Rick's camera may not be a single 3D pinhole camera.
## Known-answer set (8 clips, 64 moves of 100 to 300 f, 21 with whip pans, 18 with cuts in the tracked layer, 3 focal lengths; character plane only 6 to 11 % of the frame, below the 12 % target)
| field (mark 90 %) | S1 | S2 |
|---|---|---|
| scale +-5 % | 56.2 | 21.9 |
| roll +-0.5 degrees | 67.2 | 54.7 |
| pan +-5 % W | 50.0 | 64.1 |
| tilt +-5 % H | 84.4 | 95.3 PASS |
| layer ranking | 60.4 | 0.0 |
| parallax +-10 % | 26.6 | 10.9 |
Whip pans broke both solvers (S1 pan 4.8 %, scale 23.8 % on whip moves; on non-whip moves scale 72.1, pan 72.1, roll 81.4, tilt 90.7). Locked-region test: L1 passed 1.2 % of 82 shots, L2 82.9 %; both fail the mark.
## By move length (v6): up to 30 f scale 78.8, roll 72.7, pan 45.5, tilt 51.5; 31 to 60 f scale 45.9, pan 21.3; over 60 f scale 33.8, pan 13.8. Per video scale 21.7 to 71.0, pan 8.7 to 38.2. Even comparing any layer of one solver with any layer of the other, dx agrees on only 106 of 185 moves (post-hoc).
## Recipe table (UNCERTAIN) scale ratio p10 / median / p90 S1 | S2: push-in (85) 1.04 / 1.43 / 3.21 | 0.98 / 1.13 / 1.70 (agree 33 of 85); pull-out (52) 0.38 / 0.81 / 1.38 | 0.26 / 0.68 / 1.15 (agree 20 of 52); orbit/truck/pan 0.90 / 1.02 / 1.07; drift about 1.01; crane about 1.03; crash push median 1.07; jolt 1.00. Speed-curve class: push-ins mostly linear (30) or ease-in-out (25); pull-outs ease-out (22) or ease-in-out (18).
## Locked regions: 129 shots on a 6x10 grid: median locked share 0 for both methods; at least one locked cell found in only 11 (L1) and 9 (L2) shots, mostly #14 and #24 (#14 f1314-1378, #24 f1746-1754); 25 % of cells unmeasurable. Indicative only (tools failed): almost nothing stays still on screen inside a Rick shot.
## Disclosures: Opus only; whip pans under-measured by 15 to 35 %; the 12 % character-plane target was missed; no pass mark changed.
