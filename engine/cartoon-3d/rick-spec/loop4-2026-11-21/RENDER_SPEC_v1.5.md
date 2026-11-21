# RENDER_SPEC_v1.5 (adds to RENDER_SPEC_v1.4 in new-analysis-3; where they differ, v1.5 wins) 2026-11-21
Status words: GUIDANCE (75 %+), [INFERRED] (analogy, soft target), UNCERTAIN (no usable number). Frames at 30 fps.
## Core findings (carried in every doc)
1. SCENE TIME: 10 to 53 % of shots under 2 s, 20 to 47 % over 4 s, median 2.83 s; camera moving 80 to 98 % of frames; dissolves median 8 f. 2. MUSIC: bed 14.4 to 18.6 dB under VO, -14 LUFS, no ducking, bed std 2.3 to 4.0 dB; bed louder into the payoff in 6 of 7 videos. 3. SETS AND BODIES: torso 1.0 H, legs 1.1 to 1.3, total 2.9 to 3.35, noodle arms (chord/arc about 0.7 to 1.0), mitten hands, no fingers.
## A. Motion cheat sheet by named action (travel start to end, frames; ms = f x 33.3; all 2D-cutout rigid cards, no squash and stretch unless noted)
| action | travel | easing | notes |
|---|---|---|---|
| turn | 4.5 (3.5 to 7.5) | linear | head + torso |
| react | 5 (4.5 to 14) | ease-out | squash on 3 of 11 |
| point | 5 (3 to 24) | ease-out | lower arm + hand, no overshoot |
| lift | 6 (4.5 to 18) | ease-out | lower arm + hand, head follows |
| sit / stand | 6.5 / 7.25 | ease-out | head, torso, legs; overshoot on sit 2 of 3 |
| emote, talk | 7 / 7.5 | ease-out | arms with head; mouth shapes 2 to 2.5 f |
| throw | 8 | ease-in | anticipation (arm back) first, always |
| pull, push | 9 / 13.5 | linear / ease-in-out | arm-led, held object follows with 1 to 2 f lag |
| fall | 10.5 (7.5 to 20.5) | ease-in | legs, torso, arms; no bounce |
| recoil | 9.75 (1 to 14.5) | snap | head, torso, clothing |
| drop | 13.5 | ease-in | object falls ease-in |
| walk | step every 7.5 f [UNCERTAIN]; bodies may slide | linear | leg cycle on any moving root |
| catch | 3.25 | ease-out | arms rise and hold |
Timing window: start +-2 f and end +-2 f between two people on 80.7 % of items. Per-action medians have small samples (3 to 12). Holds between poses: median 26 f (loop 2).
## B. Inferred recipes for actions not seen (motion/INFERRED_RECIPES.md) [INFERRED]
sneak (walk at half speed, body lowered, hold 10 to 26 f), run (walk at twice speed, lean, sliding), stumble (8 to 12 f ease-in tip plus snap recoil), carry (lift 6 f then rigid object in the walk), wave (arm swing cycle 10 to 16 f, ease-in-out), cloth sway 25 f ease-in-out, crowd bob loops 12 to 16 f. Durations and limbs about 70 % reliable, easing a guess.
## C. Body mechanics
Arms: one curved noodle stroke (no elbow); anticipation 0 to 5.6 % except throws; overshoot 0 to 2.4 %, rare; squash and stretch none; feet move in walk, stand, fall; hair moves rarely. Joint angles, stride and cadence: no usable measurement (do not claim any).
## D. Asset physics
On ones [RULE]. Durations (frames): drift 28.5, particle burst 14, fall 12.5 (ease-in, no bounce), rotate 9.5, slide 19, flow 29, loop 38, sway 25 (ease-in-out), flat FX 12 to 27 (loop 3). Gravity about 4.7 to 5.1 screen heights per s^2. Bounces rare (9 items). Parallax class on 81.5 % of items agreed (none/slight/clear), no numbers.
## E. Camera (replaces camera scale lines of v1.4 where they differ)
Durations as v1.4 (push-in 23 to 142 f median 57, pull-out 25 to 120, crash push 8 to 13, jolt 6 to 7). Scale ratios soft: push-in 1.3 to 1.4, pull-out 0.6 to 0.8. Nothing stays locked on screen inside a shot (indicative). Layer shifts and parallax: use the 3D scene's own parallax; no measured target.
## F. Music and mood [INFERRED] (music/MUSIC_INFERENCE.md; the owner's brief wins)
Loop-based bed, 80 to 100 BPM, loops 6 to 11 s, minor (D minor most often), playful with an edge, louder into the payoff (+3 to +10 dB), no ducking, -14 LUFS.
## G. Scorecard additions
Action travel within the table +-3 f; throw has anticipation; no squash and stretch on walks; falls ease-in with no bounce; bed louder at payoff than at start; loop length 6 to 11 s; key minor.
