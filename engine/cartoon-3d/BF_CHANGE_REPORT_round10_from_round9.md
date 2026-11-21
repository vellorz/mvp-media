# Change report for the next Black Friday-style render (written from round 9 / bf13, 2026-11-21)
Round 9 was approved by the owner at Gate 2 (with the 37 s double zoom as a known fault) and is being posted. No round 10 is being built now. This file is for whoever builds the next video: apply it to the next video, not to bf13. Rules are in RULES_CONSOLIDATED.md, "Round-9 lessons", rules 306-322. Evidence: final/round9/ROUND9_REPORT.md and final/round9/verify/ in the project folder.

## Do first (critical rules, would have been owner-visible)
1. 306: no double push across a join. Last 20 f of one shot and first 20 f of the next must not both move toward the camera (round 9: S11 crane end then S12 push-in at 1105-1139, plus a jump at 1126-1127). Run joincheck on every join.
2. 316: no card prop shows its blank back over 12 f (S07 placard 782-843).
3. 317: no flat near-black band (S13 1218-1262, up to 17 % of the frame).
4. 318: slow drift counts as still on Rick's trackers (S11 1055-1120, 0.04 % W/f): give walk-ups a real move.
5. 308: ink must stay dull plum in every shot (magenta in S05, crimson in S03, S09, S06-S14): protect ink from the shot tint.

## Then, to close the gap to Rick (guidance)
- 307 paint plain walls and floors to Laplacian variance >= 75 (round 9: 14-31): S03, S05, S12, S14.
- 309 medium-shot heads 28-36 % W (round 9 median 24 %) and 310 legs <= 1.40 H on screen (low cameras S01, S03, S09).
- 311 foreground layers in S03, S05, S16 booth; 312 one 8-12 s packed long take; 313 events per second >= 1.5.
- 314 caption dwell 0.32-0.35 s (3 f minimum on single words, more 2-word cards); 315 eased camera stops on nouns (12 of 14).
- 319 SFX at least +4 dB over the local bed, +6 dB in the payoff; 320 poster mean luma at least the frame mean.

## Order of work for the next build
Plan the long take and the join directions in the shot table first (306, 312), then paint and light (307, 308, 317), then frame (309, 310), then run the post probes (321) on one still per shot before the PC render.

## Tools
bedcheck.py and sfxcheck.py were reading stereo stems 3 dB hot; fixed (rule 322). New probes still to write: joincheck, camlanding, ink sampler, black-share, poster brightness, tracker-threshold camstill.
