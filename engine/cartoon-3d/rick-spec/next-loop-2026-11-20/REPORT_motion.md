# MOTION track report (orchestrator copy of the agent's hand-back, 2026-11-20); data in results.json, agreement_motion_v4.json, disputes_motion.json (6,878 rows, none adjudicated), per_item_motion.json, guidance_motion.json, known_answer_score.json, locked_inventory.json
Tool timings did not reach the target and are NOT used as rules. 347 items (311 moving, 36 holds); only 12 locked-camera stretches exist and only 9 items lie fully inside one. A = LK point tracks with camera and parallax compensation; B = compensated frame-difference blobs; M1 = first measurer; M2 = blind second measurer.
Known-answer test (44 synthetic actions, camera at Rick's speed), A / B %: found 97.7/97.7; start +-2 65.9/84.1; end 52.3/70.5; travel 45.5/54.5; class 63.6/56.8; overshoot (A) 74.4; settle (A) 79.1.
Real data (v4 / v3 %), n about 310:
| field | A-B | A-M1 | A-M2 | M1-M2 | status |
|---|---|---|---|---|---|
| found | 98.4 | 100 | 98.1 | 98.1 | guidance |
| start | 48.2/42.1 | 22.5/18.0 | 24.2/17.7 | 71.6/63.5 | uncertain |
| end | 47.9/42.4 | 19.9/14.1 | 18.4/14.8 | 65.2/54.8 | uncertain |
| travel | 29.3 | 7.7/5.8 | 9.0/4.5 | 56.8/40.6 | uncertain |
| class v4 / motion_type v3 | 57.9/83.6 | 27.3/35.4 | 27.4/29.0 | 66.1/49.4 | uncertain |
| overshoot | | 56.9 | 55.5 | 94.5/96.1 | humans guidance |
| settle | | 56.9 | 57.1 | 92.3 | humans guidance |
| hold (n 36) | 94.4 (both tools say "moves") | 0 | 81.8 (n 11) | 18.2 (n 11) | uncertain |
Locked subset (n 9): A-M1 start 44 %, end 22 %. Why it failed: tool windows are about 10 f wider than human windows (continuous secondary motion, effects, parallax: the 1 px rule fires early and ends late); no hold confirmed by either tool; A cannot separate the overshoot phase. Rejected variants (dense-flow A, chained 1 px refinement, cumulative-difference B) did worse on known answers; no tolerance was changed.
Consensus guidance (all uncertain; pairwise travel agreement 21 %): snap n 28 median travel 3.5 f (p10/p90 1.5/4, agreement 41 %); tween n 227 10.5 f (5.5/17.5, 20 %); slow n 32 30.8 f (24/54, 16 %); cycle n 24 35.5 f (19/66, 17 %). Overshoot rate 1.6 %, anticipation rate 2.9 %.
Least certain: 03_010 boss lean-down (M1 424-431, M2 425-429, A 421-443, B 413-443); 03_022 tycoon lift (758-759, 755-760, 751-769, 747-771); 03_031 C5 drop (1069-1080, 1078-1085, 1061-1087, 1068-1087).

## Amendment M2 (logged 2026-11-20T20:40:40Z, AFTER seeing results; guidance with a stated window, never a rule; amendment_M2_log.json, guidance_motion_M2.json)
Honest timing statement: start known to +-3 f, end and travel to +-4 f, between the two human measurers only. The tools reach 75 % only at +-8 to +-20 f.
Agreement % at +-1/2/3/4/6 f: M1-M2 start 60/72/80/85/90, end 52/65/74/78/84, travel 41/57/67/76/82 (75 % at +-3/+-4/+-4); A-B start 39/48/54/61/72 (75 % at +-8), end 41/48/55/60/69 (+-8), travel 19/29/36/43/56 (+-15); A-M1 and A-M2 reach 75 % only at +-15 to +-20. The 2-of-4 consensus curve (50/67/75/82/100 start) is partly built to pass: upper bound only.
Items where M1 and M2 agree within 3 f on start and end: 197 of 304 (64.8 %). Guidance from those only (travel_f = mean of M1 and M2; biased toward short actions): snap n 93 median 2.5 f (p10/p90 1/4), overshoot 0 %; tween n 83 median 6.0 f (4.5/11), overshoot 2.4 %, anticipation 3.6 %; cycle n 18 median 22.5 f (10.6/49.9); slow n 3 (too thin). Holds from human logs: 36 holds median 26 f (p10/p90 8.5/67.5). Median consensus travel per video: #03 5.25, #04 11, #10 7.25, #12 5.25, #14 7.5, #22 12, #24 6.75.
