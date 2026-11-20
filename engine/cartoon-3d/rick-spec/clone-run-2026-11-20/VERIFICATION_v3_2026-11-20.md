# Verification record v3 — 7-video clone run — 2026-11-20

> **THE THREE CORE FINDINGS, as of guide v1.3.** 1. SCENE TIME: 10 to 53 % of shots under 2 s, 20 to 47 % over 4 s, median 1.93 to 3.97 s; long shots are packed one-takes; camera moving on 84 to 96 % of frames. 2. MUSIC: bed mean 14.4 to 18.6 dB under the voice, -14 LUFS, no ducking, bed level std 2.3 to 4.0 dB. 3. SETS AND BODIES: torso 1.00 head widths, legs 1.25 to 1.28, total 3.2 to 3.35, noodle arms, mitten hands, no fingers; outline thin toward the light and about twice as thick away from it; hero props heavily outlined [single].

Definitions were written before measuring: `_agent-prompts/definitions_v3_2026-11-20.md` (amendments v3.1 camera, v3.2 SFX, each with reason and time). Tolerances were not changed after results. A field passes alone only with at least 20 compared values and 99 % or more agreement.
Tools: `_tools/` (join_agree.py, motion_agree.py, cam_agree.py, audio_second.py, agree_total.py, synth.py). Totals: `AGREEMENT_v3_totals.json`. Blind check: `blind_check_heldout_shots.json`, `blind_check_predictions.json`, `blind_check_results.json`.

## Coverage
13,225 of 13,225 frames viewed by the first measurers: #03 1,955, #12 1,815, #04 1,937, #10 1,785, #14 1,945, #22 2,005, #24 1,783 (`frames_viewed` in each merged.json; frame counts from ffprobe in each rea-video package).

## Agreement per video (percent of compared fields in agreement)
| video | joins, raw | captions | actions | characters | assets | camera (2 trackers) |
|---|---|---|---|---|---|---|
| #03 | 76.79 | 100.0 | 75.7 | 58.0 | 81.2 | 59.69 |
| #12 | 90.48 | 100.0 | 80.9 | 65.0 | 77.8 | 75.77 |
| #04 | 81.25 | 100.0 | 70.9 | 64.1 | 78.7 | 60.64 |
| #10 | 80.56 | 100.0 | 71.5 | 63.6 | 79.1 | 69.27 |
| #14 | 73.91 | 100.0 | 76.1 | 66.4 | 84.7 | 68.56 |
| #22 | 94.44 | 99.3 | 68.2 | 62.6 | 77.5 | 57.75 |
| #24 | 97.37 | 100.0 | 75.7 | 63.3 | 77.4 | 68.8 |

## y. Agreement per category (owner standard: 99 % or it is not a rule)
Source: `AGREEMENT_v3_totals.json`. Second measurers were blind (they saw item lists and windows, never the first measurer's values). Motion, proportions and assets: Opus vs Opus. Joins and captions: the second measurer was requested as Sonnet; for #03 and #12 Sonnet ran, for #04, #10, #14, #22, #24 the platform substituted Opus because Sonnet was not available.
| category | agree / compared | rate | status |
|---|---|---|---|
| captions (on-frame ±1 f, text) | 3,830 / 3,834 | 99.9 % | PASS |
| character has fingers yes/no | 148 / 149 | 99.3 % | PASS |
| asset animated on twos yes/no | 393 / 396 | 99.2 % | PASS |
| mix loudness, voice level, bed level, true peak, mean and max gap, bed level std (2 tools, 7 videos, 8 fields) | 56 / 56 | 100 % | PASS as a group (7 per field) |
| bed level range, closest gap (extremes) | 8 / 14 | 57 % | [uncertain] |
| joins, all fields, before adjudication | 439 / 480 | 91.5 % | [uncertain] |
| joins found by both | 117 / 129 | 90.7 % | adjudicated one by one (joins_adjudication.md) |
| join start within 2 f | 112 / 117 | 95.7 % | [uncertain] |
| join kind | 114 / 117 | 97.4 % | [uncertain] |
| dissolve length, two fits within 2 f | 78 / 88 | 88.6 % | [uncertain] |
| actions (timing, type, angles) | 1,898 / 2,561 | 74.1 % | [uncertain] |
| action overshoot length | 309 / 315 | 98.1 % | just under |
| character proportions and line | 590 / 935 | 63.1 % | [uncertain] |
| asset physics | 2,829 / 3,568 | 79.3 % | [uncertain] |
| asset bounce count | 389 / 396 | 98.2 % | just under |
| camera, two trackers, all fields | 978 / 1,483 | 65.9 % | [uncertain] |
| camera move start within 2 f | 163 / 175 | 93.1 % | [uncertain] |
| camera scale / pan / tilt size | 43, 73, 62 / 175 | 25 to 42 % | [uncertain] |
| SFX per event (known answers) | best 93.3 % | — | [uncertain], three methods failed |
| graphic style, grade per shot, parallax, lip-sync, faces | no second measurement | — | [single] |
Motion totals cover all 7 videos. Disclosure: the #22 second motion measurer reported that many of its asset fields were filled in without a frame check, so the #22 asset agreement (77.5 %) may be overstated.
Honest reading: by the owner's standard, this run adds only four rule-grade facts (caption timing and text, no fingers, assets on ones, mix levels). Everything else is measured guidance with its agreement rate shown. Per-item frame timing of hand-animated poses does not reach ±1 to 2 f between two careful measurers.

## z. Blind check
Method. 70 shots (10 per video, random seed 2026112001, drawn before this addendum was written: `blind_check_heldout_shots.json`) were given to a fresh agent as video, start frame, end frame and length only. The agent read this addendum and nothing else, and predicted 7 fields per shot as intervals of a fixed maximum width (dissolve length 6 f, camera moves 3, hold share 0.30, captions per second 1.5, most words 2, median dwell 8 f). A script scored the predictions against the first measurers' data (`blind_check_predictions.json`, `blind_check_results.json`).
Limit, stated plainly: the 70 shots were not removed from the statistics in sections w and x, so this tests whether the guide is specific enough to describe a given Rick shot, not whether it predicts unseen videos. The predictor read the draft of this addendum before two all-video numbers were refreshed (dissolve median 7 then, 8 now; motion totals for 6 videos then, 7 now).
| field | inside the predicted interval | rate |
|---|---|---|
| how the shot ends (dissolve or hard cut) | 62 / 65 | 95.4 % |
| outgoing dissolve length | 46 / 53 | 86.8 % |
| number of camera moves in the shot | 61 / 70 | 87.1 % |
| camera hold share | 62 / 68 | 91.2 % |
| captions per second | 57 / 70 | 81.4 % |
| most words in one caption | 69 / 70 | 98.6 % |
| median caption dwell | 65 / 70 | 92.9 % |
| **all fields** | **422 / 466** | **90.6 %** |
Result: 90.6 %, under the 99 % bar. The guide describes Rick's averages well but is not yet specific enough to predict a single shot. What the predictor said the guide lacks, which is the work list for the next loop: (1) no rule for WHERE hard cuts fall, only counts per video; (2) dissolve length only as a per-video median, with no way to tell a build-up join from a payoff join; (3) no stated camera-move rate per second, and no statement whether drift and jolts count as moves (from the data: 416 logged moves in 13,225 frames, about one per 32 f); (4) hold share only as an all-video median; (5) caption rate, word count and dwell only per whole video, not by shot position; (6) the guide does not say whether a shot boundary sits at the start, middle or end of a dissolve (in this run: the middle, definitions v3).


## Disclosures
- Second measurer for joins and captions was requested as Sonnet. Sonnet ran for #03 and #12. For #04, #10, #14, #22 and #24 the platform substituted Opus because Sonnet was not available, so on those five the two measurers are the same model family (still independent and blind).
- The #22 second motion measurer reported filling in many asset fields without a frame check; #22 asset agreement (77.5 %) may be overstated.
- SFX per event: three detection methods were tested on 60 synthetic effects of known time, level and class under our own bed and voice. Results 39 and 33 of 80 fields; 87.5 % and 85.0 %; 93.3 % and 92.9 %. None reached 99 %. SFX stays [uncertain] and produces no rule.
- Camera move sizes: the two trackers agree on 25 to 42 %, so every size is a single-measurer value.
- The account's 5-hour usage limit was hit twice with 16 analysts running; agents were resumed after each reset. No log was lost; three rea-video packages were re-run.
- Blind check limit: the 70 held-out shots were not removed from the statistics, and the predictor read the addendum draft before two all-video numbers were refreshed (see guide section z).
- Adjudicated joins: 122 verified joins after one-by-one review (`joins_adjudication.md` in #12, #04, #10, #14); three same-framing jump cuts stay [uncertain] and are not counted.

## What could not reach 99 %
Join start, kind and length; dissolve length; pose timing and motion type; character proportions per field; asset timing; camera sizes, type and hold share; bed swing range and closest gap; SFX; and every single-measurer field (graphic style, grade per shot, parallax, lip-sync, faces, key and tempo of the three new videos).
