# Black Friday 99% test: round-2 results and round-3 fix plan (Nov 18 2026)
Build under audit: bf_v7_2k.mp4 (bf6 blend, PC clips 7a8c72b). Reports: /root/bf/verify/round2/*.md
Scores: audio 21/21, payoff+script 19/21, visual 17/23 (critical P3, R07, R21; closeness ~70%), shots 18/21, text 13/14 => 88/100 items, 3 critical fails. NOT PASSED.

## Already fixed in post / docs (no re-render)
- Poster colour clipping (PAY-R): separate payoff grade from f1690 (no highlight stretch), poster clip 62% -> ~0.2% on f1751.
- Vignette (L9): interiors auto-calibrated to corner/centre 0.38; exterior post vignette 0.35 -> 0.10.
- S9: 1981 Inquirer citation added to script.md (backup /root/bf/script_backup_r2.md).

## Post fixes still to do
- T1 margin: BASE -> 0.717*H. Caption text clean-up (Army-Navy hyphen, "Big Friday!", quote marks, no capital after mid-sentence period).
- Keep captions off hero headlines: S10 1038-1046, S15 1482-1503, ledger TOTAL 1296-1330 (move the prop, not the caption).

## Scene fixes (PC re-render)
Critical:
- P3/R21 S06: camera 30-40 deg off the wall, slightly high; owners staggered in depth, three-quarter toward each other / phone / register.
- P3 S16 1644-1662: break the 4-person kerb line (depth stagger, three-quarter turns).
- R07/C3 S11: push in so vendor head = 32-35% W; f1420 and S05 f560 foreground cop back to 37-38%.
Shots:
- S02 camera whip 242-251 + snap at 252 (K9/F3): ease into the 251 key, re-render S02 whole.
- S12 lurch 1126-1127; duplicate frame 866 (render S07 through 866).
- C8: S11 paperboy and S16 crowd walk sideways while facing camera -> profile cards when walking or walk toward/away.
- S03 pennant: double-sided, attached to hand, clear of face (357-372).
- S07 placard: no bare T-bar 780-846 (open off-screen or show board edge-on readable), pole behind board, text inside the border.
- Signs fully in/out: TOYS/DRUGS (show DRUGS whole once), DINER, chalk BLACK FRIDAY 630-642, news-stand signs, NOV 1981 calendar, HARTWELL.
- Chalk letters reveal under the chalk, no 3-letter pops (626-628).
- S08 blue foreground blob -> a readable object (mailbox detail).
- S14 head cut at top 1408-1412; S16 overlapping heads 1676-1690; S02 single-file sidewalk crowd 252-290.
- Monitor figures must add up (TOTAL); 1981 paper dated Nov 28.
Visual closeness (~70% -> target 99%):
- Set density + ink linework: S05 wall, S07 facade, S15 skyline, S16 blank panels to 20+ props with ink lines.
- Lighting: emissive lamp bulbs + warm light pools / window beams in S05, S12, S14; glow on screen and poster window (scene-side; post bloom halos faces, so it stays off).
- Stronger background DOF in medium shots S07, S09, S11; light aerial haze on streets.
- Foreground layer in S07 and S15. S10 newspaper: add a colour accent.
- Outlines near-black (protect ink from black lift).
