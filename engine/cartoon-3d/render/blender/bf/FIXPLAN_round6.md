# Fix plan for round 6 (from round-5 verifier reports, Nov 19 2026)
Round 5 result: FAIL. Visual 21/25 (L9, P3[C], R19[C], R21[C]), shots 18/21 (K4 as written [C] - superseded by guide l.9, K7, K8), text 13/13, payoff 22/22 (5 caveats), audio 23/23 under governing rules (A4, A6 fail only as written). Closeness to Rick ~72 %.
Owner must-haves: (1) shot shape PASS (22 shots, 22.7 % < 2 s, 18.2 % > 4 s, payoff 2.12 s); (2) music PASS (gap 16.0 dB, swing 14.1 dB); (3) sets FAIL (surface detail median 39.6 vs >= 75, 6/20 patches), bodies: torso OK 0.70-1.06, legs FAIL 0.64-0.90 (need 0.9-1.5).

## Critical
1. P3/R21 S16 1600-1687: shoppers still read as a frontal row before a flat facade. Restage as a diagonal crowd receding in depth (Rick #10 f1200 style), camera angled >= 30 deg to the facade, different heights/distances, no two heads on one horizontal line.
2. R19 payoff 1688-1751: p98 .62-.71, luma .22-.27. Brighten the bay (key + window light), warm highlights to p98 >= .84, luma >= .33.
3. Payoff empty while "we all show up": put crowd pressed to the window glass in the final shot (backs/profiles, never covering the poster), add real window glass (reflection card) so it reads as a store window.

## Owner must-haves
4. Painted surface detail >= 75 Laplacian var on walls/pavement/brick (office wall 10-15, pavement 17-19, brick 30 now): hi-res painted textures with brush grain, stains, panel detail, not more ink.
5. Legs 0.9-1.5 head heights (now 0.64-0.90): lengthen legs in cast.py, keep torso 0.7-1.05.

## Shots
6. K7: joins on phrase onsets 76 % -> <= 50 %: move some dissolves off phrase starts; cuts at 1404 and 1646 are mid-phrase without the picture being the word: either make them word-picture cuts or move.
7. K8: 4/9 move landings on nouns -> land moves on nouns within 3 f (379, 859, 959, 1313 class misses).
8. K6 S13>S14 (1355): ledger moves 7-9 % and scales 0.89, double "+ 18,240.00"; fix bridge (bridges.py must measure the visible ledger, not the hidden cover).
9. S14 1368-1398: TOTAL cut to "OTAL"; S10 1032 "ACK FRIDAY!!"; S12 1188-1212 monitor cut at edge.
10. Ledger totals appear in 3-char chunks (1298-1301, 1345-1347): one character per frame step (rule 202); hand leaves slower (>= 6 f).
11. Faces cut by edges: S03 312-384, S04 496-498, S05 564-588 + 630-642, S16 1572/1596/1650.
12. Rule 213 FG entering mid-shot: S01 cars 132-162 (also too close), S08 mailbox 870-930, S16 gift-box stack 1598-1686.
13. S03 dark box bottom-left reads as nothing; S04 462-474 squashed top-down cards; S12 no "1981" prop at 1133.
14. L9 foreground missing in S05 530-640 and S13 insert 1218-1281.
15. S10 washed out (luma .608, sat .207); S11 p98 .762; S01 crushed blacks 0-129.
16. Arms: bent elbows in held poses (f540, f960).

## Audio (not failing)
17. Bed key reads F major (r .772) vs intended D minor: stress the D tonic/bass. Pace 3.424 w/s is at the floor. Fix stale header comments in music.py/mix.py. bedcheck.py crash fixed (no-gap guard).

## From "Analyze Rick's newest videos" round-5 measurement (gap report sections I-K; 22/41 inside Rick's range, was 15)
18. Set surface detail 17.9 (two measurers) vs Rick 75+: biggest gap.
19. Arms: elbow 180 deg in all 18 characters (Rick 50-95 deg): give every arm a bent 2-segment pose; torso lean 3-8 deg; torso widest at the middle, not the hem.
20. Legs 0.74 head widths (Rick 0.93-1.31).
21. Events inside shots 1.27/s (Rick 1.49-1.78); visual changes 167.5/min (169+).
22. Joins within 3 f of phrase start 71 % (Rick 22-47 %); cuts per sentence 1.40 (max 1.36).
23. Caption dwell mean 0.37 s, P90 0.60 (Rick 0.32-0.35, 0.53-0.57): shorter cards.
24. Bed percussive:harmonic 0.09-0.19 (Rick 0.51-1.42): more percussion; <250 Hz 55.9 % (56+); check bed centres on D.
25. Small: shortest shot 1.23 s (max 1.20), share > 4 s 18 % (20-26 %), add one long packed take; tail 0.92 s (max 0.87).
## Round-6 progress
- S16: bay_light 700 + bay_fill 350 (payoff still p98 .885-.927 before grade); 3 glad shoppers at the bay sides on "we all show up"; 1590-1645 camera now oblique from the right so the crowd recedes in depth; 1646-1687 insert oblique from the left (CU shopper, crowd behind). Backups scene_r6a/b.py.
