# ASSETS track: asset physics, v4 measurement loop

Scope: 414 logged assets in 7 videos, of which 412 have a hand-placed box. The three methods share one derivation, preregistered in PREREGISTERED_derivations.md (amendments 1 to 3).
- **A**: box tracking (LK and rotated-template NCC) with camA compensation.
- **B**: three-frame-difference blob, with camB and gradient-orientation rotation.
- **C**: method A with local ring-background camera compensation.

## Known answers (46 synthetic clips: evidence/known_score_run3.json, evidence/known_score_C.json)

| Method | v3 | v4 |
|---|---|---|
| A | 343/382 = 89.8 % | 253/288 = 87.8 % |
| B | 318/380 = 83.7 % | 230/285 = 80.7 % |
| C | 340/382 = 89.0 % | 253/288 = 87.8 % |

Known-answer weak spots for method A:
- fall g: 2/5
- rotation (v4): 5/10
- easing: 35/46

## Real-video agreement (evidence/agree_ABC.json, results.json), v3 / v4 in %

| field | n | A-M1 | A-M2 | B-M1 | C-M1 | C-M2 | A-B | M1-M2 baseline | status |
|---|---|---|---|---|---|---|---|---|---|
| start_f | 412 | 15.5/23.5 | 18.5/25.1 | 15.0/18.9 | 16.3/23.5 | 20.1/28.2 | 42.7/53.2 | 66.2/73.5 | [uncertain] |
| end_f | 412 | 13.6/20.9 | 17.8/23.6 | 14.5/17.4 | 11.4/18.2 | 17.0/22.6 | 51.2/60.4 | 54.0/64.4 | [uncertain] |
| easing | 412 | 22.6/22.6 | 30.7/30.7 | 23.0/23.0 | 21.4/21.4 | 28.2/28.2 | 33.5/33.5 | 46.5/46.5 | [uncertain] |
| class | 412 | 10.4/- | 12.4/- | 5.6/- | 8.5/- | 10.7/- | 36.7/- | 70.5/- | [uncertain] |
| travel_px | 412 | -/0.0 | -/0.0 | -/0.0 | -/0.0 | -/0.0 | -/7.8 | -/- | [uncertain] |
| rot_deg_per_f | 99 | 11.1/1.0 | 0.0/0.0 | 0.0/0.0 | 9.1/1.0 | 40.0/2.6 | 16.7/2.0 | 16.7/3.3 | [uncertain] |
| bounces | 412 | 92.0/92.0 | 92.6/92.6 | 74.6/74.6 | 90.5/90.5 | 91.1/91.1 | 74.8/74.8 | 98.2/98.2 | guidance* |
| overshoot | 412 | 66.3/- | 66.0/- | 42.1/- | 67.7/- | 67.3/- | 50.2/- | 97.0/- | [uncertain] |
| loop_f | 24 | -/0.0 | -/0.0 | -/0.0 | -/0.0 | -/0.0 | -/0.0 | 100/30.0 | [uncertain] |
| g_Hps2 | 21 | -/0.0 | -/0.0 | -/0.0 | -/0.0 | -/0.0 | -/0.0 | -/27.3 | [uncertain] |
| blur | 412 | 84.2/84.2 | 91.1/91.1 | 82.8/82.8 | 83.7/83.7 | 90.6/90.6 | 90.8/90.8 | 86.1/86.1 | guidance* |
| on_twos | 412 | 94.9/- | 95.4/- | 67.1/- | 96.4/- | 97.0/- | 65.3/- | 99.2/- | guidance* |

Notes on the table:
- **Overall:** A-M1 is 49.8 % (v3) / 38.3 % (v4). A-C is 84.1 / 77.3. The M1-M2 baseline is 77.0 / 70.8.
- **\* Majority-class agreement:** bounces, blur and on_twos agree mostly because both sides say "none". Method A finds a bounce rate of 6.6 % and a blur rate of 3.2 %.
- **travel_px:** the measurers log no travel, and under v4 a value that cannot be measured counts as a disagreement.

## Why it failed
- **Different motion segment:** the trackers measure a wider motion segment than the one humans logged. The median offset is -7 f at the start and +8 f at the end. 112 of 412 items span the whole window.
- **Mixed motion in the box:** the boxes also contain characters and parallax.
- **Fall g:** no real fall passes the R² >= 0.98 g fit.
- **Loops:** the loop values never coincide with the measurers'.
- **Replaced after failing known answers:** B1 dense flow (it drifts at rest) and Fourier-Mellin rotation (it fails on round outlines).
- **Blur:** not reliable under a moving camera.

## Per-class guidance (method A, evidence/guidance.json), [uncertain] because of the segment offset
- **All assets:** median duration 31 f (p10 14, p90 73).
- **Easing mix:** linear 154, ease-out 101, ease-in 90, ease-in-out 57, snap 9.
- **Rates:** bounce 6.6 %, overshoot 33 %, blur 3.2 %. Loop median 6.5 f (n = 10). Fall g: none measurable.
- **Median duration by class:** particle burst 29 f, stream 54 f, fall 28 f, rigid translate 27 f, scale pop 21.5 f, float/bob 43.5 f, loop cycle 51 f.

## Flat-FX recipes (evidence/fx_curves_v2.json), [uncertain], the curve tool has no known-answer test

| FX | n | Median duration | Frames to 90 % of the largest size |
|---|---|---|---|
| spark | 6 | 26.5 f | 3-22 |
| ring | 4 | 25.5 f | 5-17 |
| speed lines | 4 | 19.5 f | 0-12 |
| foam/splash | 5 | 18 f | 0-19 |
| flash | 5 | 21 f | 1-14 |

The curves never fade, because scene and camera change persists against the pre-FX reference. They give no usable opacity or fade curve.

## Amendment M2 (2026-11-20T20:47Z, AFTER seeing results; guidance with a stated window, never a rule) — orchestrator copy of the hand-back
Tolerance curves (% at +-1/2/3/4/6/8/12 f; denominator all 414, missing = disagreement): start M1-M2 (humans) 55/65/70/75/80/83/91 (75 % at +-4); end 46/56/62/66/71/76/87 (+-8); A-C start 74/80/85/86/89/94/97 (+-2), end 75/79/85/87/91/92/94 (+-2); A-M1 start 11/17/23/28/39/47/93 (+-12), end 10/15/21/24/32/41/91 (+-12); A-M2 start +-12, end never. Core window (speed >= 25 % of peak) shrinks the median offset to M1 from +7/-8 f to +2/-3 f but agreement at +-3 stays about 27 % (human ceiling 70.3 % start, 61.6 % end).
Easing agreement: A-C 71.3 % (core 63.5), A-M1 22.5, A-M2 29.2, M1-M2 44.4. Where A and C agree (295 items) M1 matches 64, M2 86. Easing mix where A and C agree: linear 104, ease-out 79, ease-in 70, ease-in-out 36.
Guidance (guidance_M2.json): core duration median 22 f (p10 5, p90 53); 20 f where A and C agree (n 271); 11.5 f where the humans agree (n 212). Bounce rate 3.7 % (A-C agree, n 382) vs 1.0 % (humans). Overshoot 28.3 % (A-C) vs 0.8 % (humans): the tools almost certainly count noise as overshoot, so use the human value. Loop period: no A-C pair agrees within +-1 f; humans median 11.5 f (n 6). Fall g (relaxed R2 >= 0.9, post-hoc): M1 median 4.7 H/s2 (n 24), M2 5.1 (n 12); tools n 5 and 6. Flat FX core duration / frames to 90 % size: spark 23/7, ring 27/10.5, speed lines 12/8, foam 24/5, flash 12/8 (n 4 to 6); human-logged durations are shorter (5 to 15.5 f).
