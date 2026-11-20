# JOINS track report (written by the orchestrator from the agent's hand-back, 2026-11-20); data in results.json and the files listed below
Third dissolve method M3 (blendtemporal.py: one shared blend curve per window, per-pixel in/out values with linear drift, no reference frames) passed its known-answer test on 63 synthetic clips (real shots, lengths 3 to 16 f plus 7 hard cuts, linear/smoothstep/ease-in/ease-out, x264 5.3 Mbit/s): length within 2 f 95.2 %, within 1 f 85.7 %, start within 2 f 96.8 %, cut vs dissolve 100 %, curve class 83.9 %, "join present" 86.7 %. The M1 (whole-frame fit) known-answer test was still running (scratch_joins/known_m1.log).
| field (n) | v3 (+-2 f) | v4 (+-1 f) | status |
|---|---|---|---|
| dissolve length M1 vs M2 (102) | 85.3 | 68.6 | guidance / uncertain |
| M1 vs M3 | 89.2 | 81.4 | guidance |
| M2 vs M3 | 82.4 | 63.7 | guidance / uncertain |
| all three | 76.5 | 56.9 | guidance / uncertain |
| at least two of three | 98.0 | 94.1 | guidance |
| each vs median of three (M1/M2/M3) | 99.0/90.2/91.2 | 93.1/75.5/88.2 | guidance |
| dissolve curve, three readings agree | 81.4 | | guidance |
| kind A-B / M3-A / M3-B (117) | 97.4/94.9/96.6 | instant-vs-gradual 100/98.3/98.3 | guidance |
| start A-B / M3-A / M3-B | 95.7/94.9/94.0 | 85.5/88.0/89.7 | guidance |
| found, majority of A, B, M3 equals verified list (129) | 95.3 | | guidance |
| placement start offset, verified vs first-measurer log (122) | 99.2 | 99.2 | NOT independent (shared start frames) |
| placement middle offset / sentence position | 90.2 / 91.8 | 84.4 | guidance |
| word start: transcript vs vocal-stem onset | 69.7 | 33.6 | uncertain |
Consensus dissolve length: median 8 f, 10th to 90th percentile 5 to 12 f; per video #03 10, #12 7, #04 8.5, #10 10.5, #14 6.5, #22 7, #24 4.5. Curve: smoothstep for 91 to 95 of 102.
Placement: hard cuts 11 of 15 land 0 to +2 f after a word start (chance 27 %), but 13 of 15 are #24 and with vocal-stem timing only 4 of 15 stay: [uncertain]. Dissolve starts are not tied to word starts (31 of 102 = chance); 21 of 102 begin on a sentence start (3.7 x chance, guidance). Payoff dissolves are longer (n 6, median 12 f, +3.2 f); longer incoming shots get longer dissolves (rho 0.28). No clear effect of sentence position, match vs plain, bridge object or camera motion. 20 dissolves are 11 f or longer: 5 payoff, 5 in 3 to 15 s, 12 match. Match dissolves spread evenly by thirds (14 each). Camera moving on the incoming side at 118 of 122 joins.
Failed or open: "join present" is weak (86.7 % on known answers); faster-whisper install was denied by the permission classifier, so vocal-stem onsets are the only second word-timing source.
Files: results.json, dissolve_three_methods.csv/.json, agree_three.json, consensus.json, kind_start_recheck.json, placement_table.csv, placement_raw.json, placement_stats.json, known_score_m3.json, known_m3.json, known_truth.json, negatives_m3.json; tools in new-analysis-3/_tools/.
