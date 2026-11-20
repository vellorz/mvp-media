# CHARACTERS track report (orchestrator copy of the agent's hand-back, 2026-11-20); data in results.json, agreement_characters.json, clone_sheet.json
Result of the pixel phase: only head-fill width H reached guidance (77.8 %, n 108, v4). Every other build and line field is [uncertain] after A vs A2. Both pixel methods passed the synthetic known-answer set (A 13 of 17 fields, A2 7) but disagree on Rick's real frames. A measured on two frames of the same shot agrees with itself 47 %. Against the old vision measurers at their own frames the pixel methods agree only 16 to 22 % (H 48 to 49 %; 81 to 82 % on identity-checked items).
Pre-registration: PREREGISTRATION.md (selection amendments S1, S2 before measuring; A2 amendment M1 after the first real run, earlier results kept). Frame selection: 149 items, 68 full-body, 72 partial, 9 none; 24 failed identity check; 32 shared a head with another item.
| field | n | v3 % | v4 % | status | 1st vs 2nd measurer v4 % |
|---|---|---|---|---|---|
| H | 108 | 62.0 | 77.8 | guidance | 79.0 |
| head aspect | 108 | 36.1 | 37.0 | uncertain | 31.4 |
| torso h / w | 108 | 33.3 / 30.6 | 36.1 / 31.5 | uncertain | 40.2 / 31.9 |
| leg length / total height | 22 | 4.5 / 4.5 | 4.5 / 9.1 | uncertain | 29.0 / 22.6 |
| arm thickness | 88 | 3.4 | 6.8 (literal v4 51.1) | uncertain | 9.3 |
| leg thickness | 34 | 0 | 0 | uncertain | none |
| hand / foot | 41 / 34 | 7.3 / 2.9 | same | uncertain | 11.8 / 4.0 |
| eye size / spacing | 85 | 44.7 / 44.7 | same | uncertain | 23.7 / 31.9 |
| outline lit / shaded | 103 | 38.8 / 33.0 | 47.6 / 50.5 | uncertain | 27.0 / n.a. |
| arm / leg class | 88 / 34 | 61.4 / 11.8 | same | uncertain | 61.1 / 55.7 |
Clone sheet values from A (only H is guidance): head fill width median 24.2 % of frame width (P10 14.8, P90 40.3); eye centre at 69 % of head height above the chin; outline lit 7.8 px, shaded 15.9 px at 1080 wide [uncertain]; head aspect 0.73 [uncertain]; eyes 10.3 % H, spacing 27.0 % H [uncertain]; arms: 66 of 71 curved noodle; head colour #fbf4f1, outline ink #321c2a.
Why it failed: synthetic set too clean (no hair, hats, tinted faces, occlusion); about 12 % of selected heads are props or hats; frame-selection "full body" is a geometric guess.
Method B: crop pack of 190 pairs in /root/work/scratch_characters/crops/ (private), instructions measurerB_instructions.md; two blind Sonnet measurers launched (parts 1 and 2); scoring via char_agree.py afterwards = the third method.

## Method B (blind vision on crops) and amendment M2 (added 2026-11-20 ~20:30 UTC, AFTER per-item results; population-level guidance only, never a rule)
Method B: two Sonnet agents measured all 190 crop pairs blind (38 and 31 fully visible; 7 and 9 with no measurable character; 18 and 26 byte-identical crops measured once and copied). Per-item agreement (char_agree.py): A vs B H 78.9 % (guidance), head aspect 66.8, torso h 10.0, torso w 3.7, leg 3.9, total 7.8, arm thickness 16.8 (literal 50.9), eye size 53.8 (literal 83.3), eye spacing 58.7 (74.8), outline lit 32.1, shaded 36.9, arm class 40.4, leg class 16.7. A2 vs B lower (H 69.7). Three methods done: everything except H stays [uncertain] per item.
Population medians (m2_population.json; bootstrap 2000, seed 2026112004): H 22.2 to 24.3 % of frame width (5 sources, 8 of 10 pairs within v4); eye spacing 24.1 to 27.5 % H (8/10); outline lit 6.6 to 10.0 px (6/10); outline shaded 13.0 to 16.0 px (6/6); eye size 7.3 to 13.0 % H (5/10); hand 9.5 to 17.2 % H (6/10); torso height A 0.57, A2 0.55 vs B 1.00, first 1.00, second 1.01 (4/10); torso width 0.35, 0.44 vs 0.73, 0.77, 0.89 (1/10); total height 2.14 to 3.34 (3/10); leg 0.85 to 1.28 (3/10). The pixel tools under-read torsos by about half (blob stops at belts, coats, sleeves), so torso, leg and total heights come from B and the two old vision measurers (torso about 1.0 H, total about 2.9 to 3.3 H).
At least two of A, A2, B agree per item: eye size 83.8 %, outline shaded 82.8 %, outline lit 75.0 %, eye spacing 73.7 %, total height 53.3 %, hand 50.0 %, torso h 43.6 %, torso w 36.1 %, leg 33.3 %, arm thickness 33.0 %, foot 5.3 %. Consensus medians: eye size 9.0 % H, outline shaded 14.6 px, outline lit 7.7 px, eye spacing 27.1 % H.
