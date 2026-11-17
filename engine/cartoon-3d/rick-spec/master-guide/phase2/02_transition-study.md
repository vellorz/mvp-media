# Phase 2 — supplementary transition and pacing study (Nov 17 2026)

Videos studied visually: #05 (mirror horse race), #12 (Japan "nothing" room), #13 (furniture burglar), #16 (knight loophole). For each, every auto-detected transition was viewed as a 9-frame strip (every 2nd frame, mid-8 to mid+8). Strips are in /root/work/strips (ephemeral; regenerate with scripts/transitions.py + the strip snippet in RESUME).
Measured on ALL 17 non-primary videos: dissolve opacity curves (scripts/dissolve_curve.py) at every detected join -> dissolve-lengths-17-videos.txt.

## Measured join lengths (visible blend span, frames @30 fps)
| video | joins | lengths |
|---|---|---|
| 01 | 14 | 0,5,8,8,9,10,10,10,10,10,11,11,13,13 |
| 02 | 13 | 4,6,7,9,9,9,9,9,10,11,11,11,15 |
| 03 | 13 | 8,8,8,9,9,10,10,10,10,10,11,14,14 |
| 04 | 12 | 6,7,8,8,8,9,10,10,11,12,13,14 |
| 05 | 14 | 1,2,2,2,4,9,9,9,9,10,10,11,11,12 |
| 06 | 14 | 7,8,8,9,9,9,10,10,11,11,11,11,12,19 |
| 07 | 12 | 1,4,6,6,6,8,9,9,10,11,13,14 |
| 08 | 35 | 5-15, median 10 |
| 09 | 19 | 3,7,8,8,8,9,9,10,10,10,10,11,11,11,12,12,13,14,15 |
| 11 | 12 | 6,6,8,8,9,9,9,10,10,11,11,12 |
| 12 | 19 | 4,5,5,6,6,7,7,8,8,8,8,8,9,9,9,10,10,12,15 |
| 13 | 18 | 3,3,4,4,8,8,9,10,10,10,10,10,10,11,11,12,13,14 |
| 15 | 11 | 2,5,6,6,7,7,8,11,13,14,17 |
| 16 | 14 | 2,2,3,3,3,5,5,5,6,7,7,8,8,11 |
| 17 | 11 | 0,4,5,7,7,7,7,7,8,12,15 |
| 18 | 7 | 6,8,8,9,9,9,12 |
| 19 | 10 | 4,5,6,6,6,6,6,7,8,9 |
| **all 17** | **248** | **median 9 f; 87.5 % in 5-14 f; 90.7 % in 4-14 f; the rest are 0-3 f fast joins** |
Primaries (exact, same method): #10 bell 17 dissolves, 5-14 f, median 11; #14 dragon 18 dissolves, 5-13 f, median 7.

## Transition types seen (all 4 videos + primaries)
1. **Cross-dissolve 6-12 f during camera motion (default, ~85 % of joins).** Linear core with soft shoulders (incoming weight .08 .17 .32 .47 .61 .75 .85 .92 .96 — #14 f404-412). Both shots moving. Captions on top, never fade.
2. **Shape/position-matched dissolve** (a round thing becomes a round thing at the same screen spot): face→clock (#12 f284), coin→priest's head (#16 f998), wife's head→bell (#10 f1578-1585), frog mouth→wine bowl (#14 f609-617), window→window (#10 f869-881). Roughly half of all dissolves have a bridge object.
3. **Time-of-day / mood dissolve**: same place or same object, grade flips (night→dawn #14 f1380-1386; day→dusk #05 f1582; #12 f1094 day office → night window).
4. **Iris / lens POV mask** (circular telescope / peephole vignette on black), in and out by 3-5 f dissolve: #05 f553-615 (telescope on the race, 3 round trips), #13 f660-706 (binocular on the police car).
5. **Foreground-object wipe**: camera trucks past a post, crate or parchment that fills the frame for 2-4 f and the new shot is behind it: #16 f111 (pardon document slides off), f162 (post), f191 (stacked crates). Counted as 0-3 f joins.
6. **Push-through**: camera flies through a window/lens into the next space with a 2 f micro-mix (#10 f1176-1183; #05 f395 through a ring).
7. **Hard cut on a punchline or reveal** (rare): #16 f893 and f942 (knight waiting → close smirk), #14 f92/93 (bookend), #10 f368/369 (same-setup jump). 0-2 per video except montage videos (#05 telescope trips, #16).
8. **In-shot "move transition"**: no join at all — a crane/orbit/dive carries the viewer to a new space (#14 f59-80 crane over the jar lid; f1857-1866 pedestal through the ground; #10 f49-92 up the bell string).
Not seen anywhere: whip pans with blur-cut as a default, slide/push wipes of the full frame, star/shape wipes, zoom-blur transitions, flashes to white, glitch, page curls (the calendar in #12 f860 is an in-world prop, not a page-curl transition).

## When Rick picks which
- Dissolve length follows mood: quiet/eerie/night stories run longer (#10 median 11 f), busy/comic stories shorter (#14 median 7 f, #19 median 6 f, #16 median 5 f).
- A shape match is used when the new scene shares a round/rectangular hero object; otherwise a plain dissolve keeps the subject in the same third of the frame.
- Iris POV is used only when a character is literally looking through something (telescope, peephole, binoculars).
- Hard cuts are kept for a comic snap (reaction smirk) or a bookend.
- Every join lands on a VO phrase onset (#10 T1 "he" f1124, T3 "he faked" f1206; #14 caption changes inside each dissolve f405, f540, f609, f679, f723).

## Pacing
Joins per 10 s across 17 videos: median 2.2 (range 1.6-4.5; #08 4.5 is a 78 s montage). Primaries: #10 3.0, #14 3.0 per 10 s (18 joins / 60-65 s). Shots average 3.3 s; longest single takes 6.7-8.5 s, but the camera never stops (no static hold > 1.5 s in either primary, all 10 logs).
