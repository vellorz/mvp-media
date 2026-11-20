
---
# VERSION 1.3 ADDENDUM — 2026-11-20 — clone run: 7 videos frame by frame (#03, #12, #04 new; #10, #14, #22, #24 re-done with the v3 brief)

Owner brief 2026-11-19 6:52 PM CT: CLONE Rick's style (graphic style, characters, assets, sets, motion, camera, timing, sound). Where our approach differs from Rick's, Rick wins. Appended only; v1.2 above is unchanged byte for byte.
Evidence keys added: `#03` = "Why Perfect Railroads Don't Work" (7xS87iActkU, 30,365,777 views, 1,955 f); `#12` = "The Job Nobody Wants in Japan" (0m6G8pDtzNs, 18,827,231 views, 1,815 f); `#04` = "Why Sailors Carried Storm Oil" (Mz72MuPgnGY, 16,853,441 views, 1,937 f). View counts: yt-dlp channel listing plus returnyoutubedislikeapi.com, read 2026-11-20 00:55 UTC.
Where everything is: `research/rick-style-spec/new-analysis-2/` (RESUME_new-analysis-2.md first). Per video: 5 frame logs (`frame-log_fAAAA-BBBB.md`) and data files, `merged.json`, `joins.verified.csv`, `joins_adjudication.md`, `measurerB_joins.json`, `measurerB_motion.json`, `agreement_*.json`, `pacing.json`, `audio_nonvocal/audio.json`, `camstatsA/B.json`, `blendfit/`. Cross-video numbers: `SYNTH_7videos.json` (tool `_tools/synth.py`). Agreement totals: `AGREEMENT_v3_totals.json` (tool `_tools/agree_total.py`). Definitions written before measuring: `_agent-prompts/definitions_v3_2026-11-20.md` (with amendments v3.1 and v3.2).
Coverage: 13,225 of 13,225 frames viewed by the first measurers (1,955 + 1,815 + 1,937 + 1,785 + 1,945 + 2,005 + 1,783; `frames_viewed` in each merged.json).

STATUS WORDS used below. **[rule-grade]** = two independent measurements agree on at least 99 % of at least 20 compared fields. **[guidance]** = measured, both measurers' values shown where there are two, but agreement is under 99 %, so it is NOT a rule and stays [uncertain] under the owner's standard. **[single]** = one measurer only (no second measurement was made); also [uncertain].

## w. The three core findings, re-checked on these 7 videos (owner: must be in every document)
1. **SCENE TIME.** Holds, and the Rick range is wider than v1.2 said. Share of shots under 2 s: 10 to 53 % (#14 10, #04 12, #03 20, #12 25, #24 30, #10 39, #22 53). Share over 4 s: 20 to 47 % (#12 20, #24 20, #14 25, #22 26, #10 28, #04 29, #03 47). Median shot 1.93 to 3.97 s; all 7 videos together: median 2.83 s, 10th percentile 1.33 s, 90th 6.8 s, longest 14.7 s (n = 129 shots; `SYNTH_7videos.json` shot_len_s; joins from joins.verified.csv). New: the long shots are not rests. They are one-take sequences with 6 to 17 eased camera moves inside (section x.2).
2. **MUSIC.** Holds. Bed mean 14.4 to 18.6 dB under the voice in all 7 (two tools agree within 0.5 dB on 7 of 7: `agreement_audio.json`), integrated mix −14.0 to −14.1 LUFS, voice −14.2 to −14.4 LUFS, true peak −1.9 to −2.2 dBTP. The bed level moves: standard deviation of the 3 s level 2.3 to 4.0 dB (two tools agree 7 of 7). The size of the full swing (range) is 10.9 to 16.7 dB by tool A and 11.1 to 13.6 dB by tool B; the two tools agree on only 4 of 7 videos, so the range number is [guidance]. No ducking: bed level while the voice speaks minus level in voice gaps is −0.3 to +1.3 dB.
3. **SETS AND BODIES.** Bodies hold with two measurers: torso height median 1.00 head widths for both measurers (A n = 78, B n = 76), legs median 1.28 (A) and 1.25 (B), total height median 3.22 (A) and 3.34 (B). Robed and dress characters are outside the old 0.72 to 1.05 torso band on purpose: neck to hem 1.6 to 2.2 head widths with the legs hidden (#14 inventor 2.0, #10 widow 2.2). Sets: walls stay thin-lined (2 to 6 px), but v1.2's "little edge ink" needs a correction for HERO PROPS, which carry heavy dark outlines: #12 desks and props 10 to 29 px navy, #10 post 12 px and coffin rim 27 to 30 px, #04 galley edges 6 to 9 px, #14 bronze props 5 to 7 px [single, 5 analysts on 4 videos].

## x. What the 7-video run adds (numbers to build from)
### x.1 Joins and dissolves
- 122 verified joins in 7 videos: 102 dissolves, of which 42 (41 %) are match dissolves with a bridge object at the same screen spot; 17 hard cuts (13 of them in #24, 3 in #03, 1 in #14); 1 push-through; 1 iris through a pupil (#24 f1301-1307); 1 foreground wipe by a wiper blade (#24 f1742-1745). Kind of join agrees between the two measurers on 114 of 117 = 97.4 % [guidance].
- #24 is the outlier and shows the second mode: an action video cut almost entirely on hard cuts (13 of 19), each cut landing 0 to +2 f after a word start, with the incoming camera already moving.
- Dissolve length by blend-weight fit (frames with incoming weight 3 to 97 %): all 7 videos median 8 f, 10th percentile 5, 90th 11 (n = 90 fits; `SYNTH_7videos.json` dissolve_len_fit_ok). Per video median: #03 10, #12 6.5, #04 8.5, #10 11, #14 7, #22 7, #24 6. Two independent fits (static patch vs whole frame) agree within 2 f on 78 of 88 = 88.6 % and within 1 f on 71.6 %; length by eye agrees within 2 f on 82.1 %. Dissolve length is therefore [guidance]: build 6 to 11 f, shorter (4 to 7 f) in fast build-ups, longer (10 to 12 f) at the climax and payoff (#22: 5-6 f mid-story, 10-12 f at the end).
- The camera is moving on at least one side of nearly every dissolve, and often speeds up INTO it: #14 tilt rises 0.32 to 5.4 % W per frame over f1442-1459 and the dissolve starts at peak speed; #10 f812-881 is a 70 f accelerating push that continues through a 12 f match dissolve [single].
- Bridge offsets up to 0.19 of frame width were logged for match dissolves (#10 bell to bell); the v1.0 "within 5 %" rule is too tight [single].
- Hook: 0 joins in the first 3 s in 6 of 7 videos (#12 has one at 2.5 s).
- In-take edits that are NOT joins and that the automatic detector reports as joins: 1-frame relights (#10 f369), day to dusk relights over 16 to 18 f (#24 f436-454; #10 f1558-1575), lightning flashes (#04), rack focus (below), props that fade in over 2 to 3 f, a costume swap in 1 f (#22 f916). Three same-framing jump cuts are tagged [uncertain] and not counted (#03 f1322; #14 f1170, f1258).

### x.2 Camera (highest value for cloning)
- **The camera almost never stops.** Share of frames with background motion at or above 0.05 % of frame width per frame: tool A 86 to 96 %, tool B 84 to 95 % per video (`camstatsA/B.json` moving_share). First measurers' per-shot hold share: median 0.03, 90th percentile 0.24 (n = 98 complete shots). Longest fully still run per video: 0 to 8 f (`pacing.json`). Between big moves the camera DRIFTS at 0.05 to 0.2 % W per frame (a slow linear push of ×1.04 to ×1.18 over 28 to 53 f).
- **One-take sequences.** Openings: #24 f1-284 (9.5 s, 10 camera phases), #04 f1-176, #22 f1-140 (6 beats), #10 f2-93 (5.2× dive, then a tilt-up following the string). Mid-story: #22 f425-866 is one 14.7 s take with 17 eased moves and no join; #04 f563-692 follows a thrown grappling hook for 130 f.
- **Move vocabulary** (416 logged rows): push-in 132, pull-out 42, compound 52, drift 40, shake/jolt 25, orbit 23, tilt 23, crane 18, pan 18, truck 11, object-follow 8 as primary type; 48 % of rows follow a character or object. Duration median 24 f (10th percentile 9, 90th 55).
- **Easing** by the first measurers: linear 29 %, ease-in-out 29 %, ease-out 22 %, ease-in 11 %, snap 6 %. Two automatic trackers agree on ease class for 148 of 175 matched moves = 84.6 % and on start frame within 2 f for 93.1 % [guidance]. Sizes (scale, pan, tilt) agree on only 25 to 42 %, because a true 3D camera with parallax has no single background; every move SIZE below is [single].
- **Recipes** (frame-evidenced, [single] unless said):
  - Crash push on the punch word: 9 to 25 f, ×1.8 to ×5, ease-in-out, peak speed on the word ±3 f (#14 f1419-1427 ×2.12 in 9 f, peak on "pile"; #22 f1272-1296 ×1.77 in 25 f; #14 f20-31 ×3.57 in 12 f; #12 4× in 13 f).
  - Reveal pull-out: to 0.24 to 0.5 scale in 21 to 37 f, eased, peak 4 to 12 % W per frame (#04 f611-631; #24 f463-499; #14 f623-659 9.6× in 37 f; #10 f111-141).
  - Impact jolt: one frame of punch-in, +3 to +7 % scale and about 1 to 1.4 % W of tilt, on or 1 f after the contact frame, then a 6 to 10 f ease-out (#14 f1405, f570; #22 f1138; #24 f825, f1229, f1259; #24 shot f361-516 has 8 such kicks in 5.2 s).
  - Slap/impact stack (#22 f775-783): ×1.094 push in 1 f, 1 f freeze, 1 f smear, 6 f shake of ±1 to 3.4 % W, flat shockwave ring over 4 f.
  - Orbit around a character or prop: 24 to 54 f, 43 to 80 % W of background travel, ease-in-out, pivot object locked (#24 f561-614, f891-914; #22 f1009-1034; #14 f227-315).
  - Follow a falling or thrown object: the camera tilts with it (#03 gravity-fit tilt, R² 0.99996; #14 f1023; #04 hook follow at 5 % W per frame).
  - Rack focus as an in-take edit: 2 to 4 f snaps on a spoken word (#10 f1150-1152 and f1160-1162; #12), or 9 f with an all-soft middle (#10).
  - Roll exists: +13° over 31 f on a fly-over (#22 f1835-1866), up to 9° in an orbit (#24), −75° top-down turn (#14 f1493-1533). v1.0 "no roll" is wrong.
  - Ending: the camera stops and holds for the last 23 to 86 f (#22 23 f; #04 86 f) while a face or FX still changes; the video ends 0.27 to 0.89 s after the last word starts.
- Parallax FG:BG speed ratio: median 2.5, middle half 1.9 to 4.0 (n = 31 shots) [single].

### x.3 Character build (clone sheet)
All ratios are in head widths (H = width of the head fill). Two measurers' medians are shown as A / B; per-character agreement is 63.1 % (590 of 935 fields), so these are [guidance] except where marked.
| part | value | n (A / B) |
|---|---|---|
| head | flat near-white fill (most common #fbf7f4, #ffffff, #f5f5f5); takes the scene tint (lavender #d8d7e9 in shade, blue-lit at night) | 145 |
| head size on screen | median 21.7 % of frame width; MS 28 to 36 %, CU 45 to 57 %, wides 2 to 12 % | 131 |
| head outline, lit side | 3.7 % / 3.1 % of H (about 7 to 10 px at a 300 px head); dark plum, maroon or navy, tinted by the light, never pure black | 84 / 93 |
| head outline, shaded side and under the chin | about 2 times thicker: B median 6.1 % of H (n = 54); logged independently by 12 first-measurer ranges in 6 videos (#03, #12, #04, #10, #14, #22) | 54 |
| eyes | height or diameter 12 % / 13 % of H; centre spacing 27 % / 27.3 % of H | 56-58 / 70 |
| torso | bean or pear, height 1.00 / 1.00 H (middle half A 0.92 to 1.18), width 0.77 / 0.89 H | 78, 73 / 76, 71 |
| robe or dress body | neck to hem 1.6 to 2.2 H, legs hidden | [single] |
| legs | 1.28 / 1.25 H (middle half A 0.94 to 1.36) | 53 / 35 |
| total height | 3.22 / 3.34 H (A 10th to 90th percentile 2.8 to 3.47) | 52 / 15 |
| limbs | single dark stroke, 5.9 % / 5.0 % of H thick; arms are curved "noodles" with no fixed elbow (85 of 113 visible arms), 2-segment in 17; legs straight sticks or noodles | 53 / 38 |
| hands | dark round mitten, 12 % / 12 % of H | 46 / 11 |
| fingers | none: 147 of 149 design sheets; both measurers agree on 148 of 149 = 99.3 % **[rule-grade]**. The 2 exceptions are one pointing index finger (#04, #14) | 149 |
| feet | 15.5 % of H (A; 8 to 24 %) | 24 |
| shading | flat fill; some torsos carry one cel shadow band and a gloss stripe; hats and props are 3D-shaded on the flat head; some heads carry a soft lavender shade band about 17 % of H wide (#24, #04 pirate) | [single] |
| in the set | flat card facing the camera; whole-body rigid leans and turns by redraw | [single] |
The v1.0 word "monoline" for the head outline is withdrawn: the line is thin toward the light and thick away from it.

### x.4 Motion (owner's highest priority)
Agreement: actions 74.1 % (1,898 of 2,561 fields, 7 videos), so every timing below is [guidance] unless marked. What the two measurers DO agree on: an action exists where logged (98.1 %), overshoot length (98.1 %, value 0), anticipation length (95.9 %, value 0), settle length (94.3 %, value 0 to 1). What they do not agree on: exact start and end frames within ±1 to 2 f (54 to 64 %) and whether a move is a "snap" or a "tween" (49.2 %).
- 347 body actions in 7 videos. First measurers' classes: snap 125, tween 108, redraw 47, cycle 31, other 36.
- **Snap pose change:** travel median 2 f (10th to 90th percentile 1 to 4 f).
- **Rigid tween** (whole-body lean, stand-up, sit, slide): travel median 7 f (middle half 5 to 11 f, 90th percentile 21 f). The body moves as one rigid piece; limbs do not deform.
- **No anticipation, no overshoot, no squash and stretch** as the default: anticipation 0 f at the 90th percentile, overshoot 0 f in about 98 % of actions, settle 0 f median and 1 f at the 90th percentile. Exceptions are single gags (#14 startled rise overshoots 0.17 H for 1 f then settles 6 f; #10 jump with a 9 f crouch).
- **Holds:** 285 logged holds of 6 f or more; median 24 f, 90th percentile 64 f, longest 171 f. A visible character's body is in a hold for 51 to 83 % of each video while the FACE keeps changing.
- **Faces:** 1.4 to 2.5 face events per second per video (median 2.1). Bursts of 4 swaps in 4 f at a shock (#24 f17-20; #22 f1779-1782). Faces can also hold 83 to 191 f on a deadpan character. Blinks 1 to 3 f; a few have a half-closed in-between.
- **Lip-sync:** median 2.25 f per mouth shape (range 1.5 to 4; 26 runs), on 0 to 12 % of a video's frames. Mouths also move on reported speech and on narration in #04, #10, #14, #22 (v1.0 "lips move only on quoted lines" is wrong) [single].
- **Walks:** rare and mostly hidden (legs behind grass, robes or desks). 23 cadence values, median 7.5 f per step, range 3.3 to 27; only 5 of 10 compared values agree within 1 f. Bodies slide while legs cycle; armies march in place. Do not build a rule from this.
- **Secondary motion** is rare: hair spikes on a jump, hat tilt as the whole gesture (#04 chef's hat rotates about 40° in 3 f and is held 57 f).
- **Smears** exist but are rare: 1-frame multi-image smear on a fast prop (#22 f58), 2 f white smear on an axe swing (#24 f952-953), cross-faded leg drawings during a 2 f snap (#24 f7-9).

### x.5 Asset physics
414 moving props, vehicles, particles and FX logged. Agreement 79.3 % overall (2,829 of 3,568 fields).
- Animated on ones: 411 of 414; the two measurers agree on 393 of 396 = 99.2 % **[rule-grade]**. Build every moving asset on ones.
- No squash and stretch on any asset (0 of 414) [single field, B was not asked]. Overshoot on 12 (2.9 %; agreement 97.0 %), bounce on 10 (2.4 %; agreement 98.2 %), motion blur on 54 (13 %; agreement 86.1 %) [guidance].
- Falls accelerate like real gravity and land dead: 24 fitted falls with R² at or above 0.98, median 4.9 screen heights per s² (middle half 3.5 to 8.8). No bounce, no squash, settle within 3 f (#14 balls 2.2 to 6.1; #10 dirt clods 3.8; #24 tree 9.5).
- Prop slam-in: appears at about 120 % size and reaches 100 % in 3 f, with a camera kick on the landing frame (#24 f390-393, f407-410). Scale pops otherwise reach full size in 2 to 5 f without overshoot.
- Flat 2D FX last 4 to 11 f: spark bursts 6 f, spiky burst 2 f up and gone by 4 f, shockwave ring 4 f, foam puffs 6 f, speed lines 7 f.
- Loops: median 13 f (8 to 16 f): bell swing 8 to 19 f, wiper cycle 14 to 15 f, crank 16 f, rocking chair 11 f ("fast") and 27 f ("slow") in time with the narration.
- Lightning flash recipe (#04): on 2 f, dip 1 f, on 2 f, then 8 f linear decay, peaks about +80 % luma, every 38 to 40 f, 1 to 2 f before a caption swap.
- Light as a beat: a window lights over 5 f on a word (#10 f380-384); a gold edge glow on the noun's object (#22 f428-445 "the wood"); relight ramps of 16 to 18 f.
- Vehicles in #24 are realistic soft-body 3D models that crumple; the car pitches 90° in 4 f, sways on its nose with a 12 f period, topples in 4 f and bounces once.

### x.6 Timing structure
- Narration 3.37 to 3.85 words per second (219 to 247 words in 59 to 67 s), 14 to 21 sentences.
- Joins per sentence 0.78 to 1.36. The MIDDLE of a join sits within 3 f of a word start for 58 to 90 % of joins.
- Camera moves start on word starts and peak on the stressed word (0 to 3 f) [single].
- Payoff joins per minute: 0 (#12, #10, the last shot is one long take of 6.8 to 10.9 s) to 32 to 40 (#03, #22, #24). Two endings exist: one long reveal take, or a burst of short shots.
- Visual changes without captions: 151 to 214 per minute.

### x.7 Captions
- 1,278 caption events, both measurers: 3,830 of 3,834 fields agree = 99.9 % **[rule-grade]** for on-frame (±1 f) and text.
- Words per caption: 1 in at least 75 % of captions, 2 at the 90th percentile, 3 is the normal maximum (one 8-word outlier in #22). Rate 2.73 to 3.06 captions per second. Dwell median 10 f (10th to 90th percentile 4 to 16 f; longest 30 f). Hard swaps, no gaps, full opacity through every dissolve. Baseline 71.6 to 71.7 % of frame height, cap height 53 to 54 px at 1080 × 1920.
- Offset to the spoken word (caption frame minus word start from the transcript): per-video median −1.0 to 0.0 f in 6 videos (#12 −0.2, #04 −0.6, #10 0.0, #14 −0.4, #22 −1.0, #24 −1.0), with 77 to 95 % of captions within ±2 f. #03 reads −4.4 f, which is a transcript timing bias, not the edit. Corrects v1.0 rule 12 "0 to 3 f before": build 0 to 1 f before the word, never later than +2 f. The word times come from one transcript, so this is [guidance].
- Numbers can be spelled as spoken ("at two" for "2:00", #10).

### x.8 Graphic style, grade, sets [single]
- Sets are true 3D with painted surface detail. Day interiors can run bright (luma 0.75 to 0.76: #12 corridor, #04 soup insert), night storms dark (luma 0.25 to 0.33, p98 0.55 to 0.79, saturation 0.70 to 0.78). The v1.1 grade bands are too narrow for night and insert shots.
- Faces keep their highlights in dark shots (p98 0.86 to 0.97 while scene luma is 0.17 to 0.35).
- Palette changes inside a take (blue day to lilac dusk during an orbit, #22 f705-712).
- Some backdrops are flat inked illustration while hero props are glossy 3D (#14 throne hall).
- Depth of field is used as a cut: the background drops out of focus in 2 f with no camera move (#10 f152-154).

### x.9 Audio
- Mix-level fields: see w.2. Loop period of the bed: #03 about 12.2 s (three estimates 12.21, 12.21, 12.26).
- Key by one tool: D minor for #12, #04, #10, #14, #24 (and #22, low confidence), E minor for #03. Only #10 and #22 have a second tool from v1.2, so key for the three new videos is [single]. Tempo by one tool 96 to 123 BPM [single].
- **SFX per event is [uncertain] and produces no rule.** Three detection methods were tested against 60 synthetic effects of known time, level and class mixed under our own bed and narration: method 1 scored 39 and 33 of 80 fields, method 2 87.5 % and 85.0 %, method 3 93.3 % and 92.9 % (definitions v3 amendment v3.2). None reached 99 %. What can be said from the picture logs: 1.2 to 1.9 picture events per second that call for a sound (661 logged), and impact pictures trail the narrated verb by 3 to 5 f (#04 "clangs", #22 "slam").

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

## aa. Corrections to earlier sections (old, new, why)
| where | old | new | evidence |
|---|---|---|---|
| a.9, c | head outline "monoline 6-10 px, 2.5 % of head width" | thin on the lit side (about 3.1 to 3.7 % of H), about 2 times thicker on the shaded side and under the chin (about 6.1 %) [guidance] | x.3 |
| a.11 | lips move only on quoted lines | also on reported speech and narration in 4 of 7 videos [single] | x.4 |
| a.11 | a face change every 0.3 to 2 s | 1.4 to 2.5 face events per second on average, but deadpan faces hold 83 to 191 f | x.4 |
| a.12 | caption 0 to 3 f before the word | 0 to 1 f before, never later than +2 f [guidance] | x.7 |
| a.5 | shots 1.5 to 8.5 s | one-take sequences of 9.5 to 14.7 s exist with 10 to 17 camera moves inside | x.2 |
| a.7 | no static hold over 1.5 s | holds over 1.5 s do occur (48 f #24 f1591-1638; 65 f #14 f1307-1378 by definition; 86 f final hold #04), always with a face, light or FX still changing | x.2 |
| a.4 | at most 5 fast joins per video | #24 has 13 hard cuts; hard-cut editing is a valid second mode for action stories | x.1 |
| b | push-through join 2 f | 11 f push-through dissolve (#10 f515-525) | x.1 |
| b | bridge object within 5 % of the same spot | offsets up to 19 % W logged | x.1 |
| e, m | no camera roll | roll up to 13° on fly-overs, 9° in orbits | x.2 |
| m | character bodies never smear | rare 1 to 2 f smears exist | x.4 |
| m | set-edge ink thin everywhere | walls thin, hero props heavy (5 to 30 px) [single] | w.3 |
| m | grade bands | night down to luma 0.25, bright inserts up to 0.76 [single] | x.8 |
| c | feet at most 12 % of H | 15.5 % median (8 to 24 %) [single] | x.3 |
| c | total height 2.4 to 3.2 H | 3.2 to 3.35 median, up to 3.6 | x.3 |

## ab. Clone spec: build values (all [guidance] unless marked; use until a later run reaches 99 %)
1. Camera moving on at least 85 % of frames; no fully still run over 8 f except the ending hold; idle drift 0.05 to 0.2 % W per frame.
2. First 3 s: no join; open on a one-take with at least 3 eased camera beats.
3. Every 10 to 15 s: one crash push (9 to 25 f, ×1.8 or more, peak on the word) and one reveal pull-out (21 to 37 f, to 0.25-0.5 scale).
4. Every impact: 1-frame punch-in of +3 to +7 % scale, 6 to 10 f ease-out return.
5. Dissolves 6 to 11 f, camera moving through them; about 40 % carry a same-spot bridge object. Action passages may use hard cuts on word starts.
6. Characters per the x.3 table: 1.0 H bean torso, 1.3 H legs, 3.2 to 3.35 H total, noodle arms 5 to 6 % H, mitten hands 12 % H, no fingers [rule-grade], outline thin toward the light and 2 to 3 times thicker away from it.
7. Pose changes: snap in 1 to 4 f (median 2) or rigid tween in 5 to 11 f; 0 f anticipation, 0 f overshoot, settle at most 1 f; no squash and stretch.
8. Bodies hold 50 to 80 % of the time (holds median 24 f) while faces change 1.4 to 2.5 times per second; mouths 2 to 2.5 f per shape.
9. All moving assets on ones [rule-grade]; falls accelerate at about 3.5 to 8.8 screen heights per s² and land with no bounce; flat FX 4 to 11 f.
10. Captions: 1 word (2 at most often, 3 max), 2.7 to 3.1 per second, on the word or 1 f before it [on-frame method rule-grade], dwell 4 to 16 f, hard swap, no gaps.
11. Mix: −14 LUFS, voice −14.2 to −14.4, bed mean 14.4 to 18.6 dB under the voice with a level standard deviation of 2.3 to 4.0 dB, no ducking, true peak about −2 dBTP [rule-grade as a group].
12. End 0.3 to 0.9 s after the last word starts, on a held frame with one last face or FX change.

## ac. Process notes from this run
- Usage: 16 Opus analysts in parallel hit the account's 5-hour limit twice; agents were resumed after each reset and no work was lost. Run fewer at once next time.
- The every-frame brief works for coverage (13,225 of 13,225) but two careful measurers still disagree on pose timing at ±1 to 2 f. A next loop that could reach 99 % for motion would measure fewer, cleaner items: one tracked point per action on locked-camera shots only, with the track as the measurement.
- Camera size cannot be verified with 2D trackers on a 3D camera. A next loop would fit a 3D camera (structure from motion) per shot, or measure only screen-space speed profiles.
- The automatic join detector both misses joins and reports relights, flashes and focus pulls; every join was confirmed by eye.
