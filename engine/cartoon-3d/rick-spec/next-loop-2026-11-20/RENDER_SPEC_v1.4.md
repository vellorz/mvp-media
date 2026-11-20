# RENDER_SPEC_v1.4 — what a future Rick-clone render must follow (2026-11-20)
Sources: GUIDE_v1.4_addendum.md sections ad to am; per-track REPORT.md in this folder. Status words: RULE (99 %+), GUIDANCE (75 %+, window stated), UNCERTAIN (not a requirement; use as a soft target only).

## Core findings (every render document carries these)
1. SCENE TIME: 10 to 53 % of shots under 2 s, 20 to 47 % over 4 s, median 2.8 s; one-takes of 9.5 to 14.7 s; camera moving on 80 to 98 % of frames; dissolves median 8 f (5 to 12), smoothstep.
2. MUSIC: bed 14.4 to 18.6 dB under voice on average, mix -14.0 to -14.1 LUFS, no ducking, bed std 2.3 to 4.0 dB; full swing 7 to 12 dB (p95 minus p5), +-4 dB, UNCERTAIN.
3. SETS AND BODIES: torso about 1.0 head height (H), legs 1.1 to 1.3 H, total 2.9 to 3.35 H, curved noodle arms, mitten hands, no fingers (RULE), outline 7 to 10 px lit and 13 to 16 px shaded at 1080 wide (population level).

## A. Cast sheet
- Head: flat near-white #fbf4f1 round card facing camera; width 22 to 24 % of frame width on average (28 to 36 % in medium shots) [GUIDANCE]. Eyes 7 to 13 % H tall, spacing 24 to 27 % H, centred about 69 % up the head [GUIDANCE, population].
- Body: torso 1.0 H, width 0.73 to 0.89 H; legs 1.1 to 1.3 H; robes and dresses neck to hem 1.6 to 2.2 H with legs hidden.
- Arms: one curved noodle stroke, no fixed elbow, 12 to 14 px at 1080 wide. Hands: plain mittens 10 to 12 % H, no fingers, no thumb [RULE: no fingers].
- Line: ink #321c2a (never pure black), 7 to 10 px lit side, 13 to 16 px shaded side and under the chin. Hero props heavier [SINGLE].
- Do not copy Rick's named characters, frames or lines; copy the construction.

## B. Camera recipes (durations in frames at 30 fps unless noted)
| move | duration p10 / median / p90 | notes |
|---|---|---|
| slow push-in | 23 / 57 / 142 | linear or ease-in-out; scale ratio UNCERTAIN (median 1.38) |
| reveal pull-out | 25 / 57 / 120 | ease-out; ratio UNCERTAIN (median 0.58) |
| orbit / truck / pan | 11 / 27 / 70 | |
| drift | 5 / 11 / 34 | 0.05 to 0.2 % W per frame |
| crane / tilt-follow | 7 / 28 / 44 | |
| crash push | 8 / 12 / 13 | peak 0.9 % W per frame |
| impact jolt | 6 / 6 / 7 | one-frame punch-in +3 to +7 %, ease back 6 to 10 f |
Camera moving on at least 85 % of frames; never fully still over 1 s except the ending hold 23 to 86 f. Parallax FG to BG and roll sizes: not measurable, UNCERTAIN; use the 3D scene's own parallax.

## C. Motion cheat sheet (timing window +-3 f start, +-4 f end) [GUIDANCE, POST-HOC window]
- Snap pose change 1 to 4 f (median 2.5). Rigid tween 5 to 11 f (median 6). Cycle (walk, loop) median 22 f. Hold median 26 f (p10 8.5, p90 67.5).
- Overshoot 0 to 2.4 %, anticipation 0 to 5.6 %, no squash and stretch.
- Face events 1.4 to 2.5 per second; blink 1 to 3 f; mouth shape 2 to 2.5 f; bursts of 4 swaps in 4 f at a shock.
- Walking: a moving root gets a leg cycle; bodies may slide; armies may march in place.
- Assets move on ones [RULE]. Falls 4.7 to 5.1 screen heights per s^2, no bounce. Flat FX 12 to 27 f (spark 23, ring 27, speed lines 12, foam 24, flash 12).

## D. Join recipe [GUIDANCE]
Hard cuts are normal. Dissolves 5 to 12 f (median 8), smoothstep weight, camera moving through, about 40 % match dissolves; start a dissolve on a sentence start when the picture changes with the sentence; payoff dissolves about 12 f. Shortest shot 10 f.

## E. Audio spec
Mix -14.0 to -14.1 LUFS, true peak -1.9 to -2.2 dBTP [RULE as group]. Bed std 2.3 to 4.0 dB, not constant, no ducking, no pumping [GUIDANCE]. Tempo 75 to 104 BPM and loop 6 to 11 s are soft targets [UNCERTAIN]. Key: profile tools say D minor, bass tools say A minor [UNCERTAIN]; pick by ear. SFX gentle; per-event timing UNCERTAIN.

## F. Captions [RULE for the method]
On the word or 0 to 1 f before, never later than +2 f; hard swaps; 1 word per card in at least 75 %, 3 max; dwell median 10 f (4 to 16); 2.7 to 3.1 cards per second.

## G. Scorecard items for a render
Camera-moving share at least 85 %; no still run over 1 s; dissolve median 6 to 10 f; shots under 2 s between 10 and 53 %; shot over 4 s between 20 and 47 %; torso/head ratio 0.9 to 1.2 on full-body frames; no fingers; outline ink not black; mix -14 LUFS, true peak under -1.5 dBTP; caption lag at most +2 f.
