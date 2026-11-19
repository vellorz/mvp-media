<!-- TOP BLOCK added 2026-11-19 (verification run). The previous version follows byte for byte (sha256 cdb24545..., 13,773 bytes); the new ledger entry is at the end of the file. -->
> **THE THREE CORE FINDINGS (owner: must be stated in every document; re-confirmed against the source tables on 2026-11-19).** BF = our Black Friday test video, round 3. Rick = his 5 newest videos, #21 to #25.
> 1. **SCENE TIME.** Our average shot length is fine (3.65 s; Rick 2.65 to 4.54 s). The shape is wrong: 6 % of our shots are under 2 s (Rick 20 to 53 %) and 50 % are over 4 s (Rick 20 to 26 %). Our ending is slow on both measures: a shot is visible for 3.00 s on average during the last sentence (Rick 0.93 to 2.98 s), and shots that start in the payoff average 6.37 s (Rick 1.57 to 5.37 s; 4 of 5 videos at 1.6 to 2.4 s). [Corrected 2026-11-19: an earlier summary line paired our 6.4 s with Rick's 0.9 to 3.0 s, which are two different measures.]
> 2. **MUSIC.** Rick's bed sits 14 to 18 dB under the voice (mean gap 14.4 to 18.5 dB) and swings 8 to 15 dB with the story (level range 7.8 to 15.0 dB). Ours is 19.1 dB under and flat (5.65 dB). The old rule "constant, about 20 dB under" was our measuring error and is superseded. Key: two independent tools that pass known-answer tests confirm a minor key for 4 of 7 Rick videos (#21 E minor, #22 D minor, #23 D minor, #10 D minor); the other 3 are not confirmed either way and none is confirmed major; ours is F major. [Corrected 2026-11-19: "minor key" was first stated for all of them from one tool.]
> 3. **SETS AND BODIES.** Rick's newest sets carry little edge ink (thin lines, median 2 px, in the surface's own dark colour, on some edges in about 8 of 20 frames; ours measured 7 px). The drawn feel is painted surface detail, where ours has 5 to 13 times less (Laplacian variance: ours 11; Rick 75 to 142 depending on the measurer). His torsos are short and round on long legs (torso 0.72 to 1.05 head widths, legs 0.93 to 1.31); ours are long coats on stubs (torso 1.19 to 1.69, legs 0.11 to 0.17).
>
> Everything else from the research (cutting, captions, mix, poses, FX, script) is in the sections below and in `research/rick-style-spec/new-analysis/`. Verification status of every field: `new-analysis/VERIFICATION_v2_2026-11-19.md`.

---

# Gap report — Dresden and Salzburg scored against the Rick rubric (learning only, no redo)
Files scored: handoff/2026-11-17_salzburg-dresden/dresden_giant-stollen_small.mp4 (51.0 s) and salzburg_silent-night_small.mp4 (52.4 s), plus their VO mp3s. Same scripts and thresholds as the Rick test (phase4/04_rubric-and-test.md). "Rule" numbers point to rick-master-guide.md section a (quick card) unless a section letter is given.

## Scores
| dimension | Rick pass line | Dresden | Salzburg | guide rule that would have prevented it |
|---|---|---|---|---|
| 1 Transitions | dissolves 4-14 f, varied, ≥ 50 % bridged, on phrase onsets | 10 joins, **every one exactly 5 f** with an identical linear ramp (fit err 0.02) — technically inside the window but mechanical; bridge objects rare (sheet check) → **50 %** | 12 joins, 11 at 5 f, 1 at 7 f → **50 %** | a4 (length follows mood: 6-12 f default, 10-12 for quiet/night), a6 (bridge object), b (bridging recipe) |
| 2 Pacing | 2-4.5 joins/10 s, still frames ≤ 12 %, longest static ≤ 1.5 s | 2.0 joins/10 s ✓; still **15.2 %** ✗; longest still run 36 f (Rick 7 f) → **67 %** | 2.3 ✓; still 10.4 % ✓; still run 35 f → **83 %** | a5, a7 |
| 3 Character look | flat drawn head + monoline outline 6-10 px, head 30-39 % W in MS | shaded 3D figurine heads, no outline, small faces (gridOurs frames 2, 4, 6) → **0 %** | same, plus large CU of a 3D doll head (frame 1) → **0 %** | a9, a10, section c (owner: "character look not Rick's") |
| 4 Lettering | box bottom 71.7 %, cap 54 px @1920, ≤ 3 words, width ≤ 50 % W, digits | bottom 72.5 %, box 61 px (11 % too big), median width **54.8 %**, numbers spelled out ("three thousand six hundred eggs,") → **40 %** | bottom 72.7 %, box 66 px, width **52.0 %** → **40 %** | a12, a13, section d (case/numerals, 1-3 words) |
| 5 Colour + grade | luma 0.33-0.56, sat 0.37-0.66, p2 ≥ 0.05, p98 ≥ 0.84 | 0.399 ✓, 0.561 ✓, 0.051 ✓, **0.773** ✗ → **75 %** | **0.282** ✗, 0.579 ✓, **0.004** ✗, **0.667** ✗ → **25 %** | a14 (lifted blacks, bright highlights), a15 |
| 6 Composition | one focal subject, FG/MG/BG, caption never on a face, dynamic angles | captions clear of faces ✓; frontal eye-level stage shots, characters lined up in a row (frames 2, 4, 6) ✗ → **50 %** | caption clear ✓; mostly frontal, a row of figures (frame 7) ✗ → **50 %** | section e (composition, camera angles) |
| 7 Lighting + depth | edge 0.20-0.35, motivated key, contact shadows, bloom, DOF, haze | edge 0.252 ✓; flat even light, little DOF → **50 %** | edge **0.197** ✗; dark, crushed → **25 %** | section e (lighting, depth) |
| 8 Camera | motion median ≥ 4.5, eased hits on nouns | **2.45** ✗ → **0 %** | **3.34** ✗ → **0 %** | a7, a8 |
| 9 Motion design | pose-to-pose snaps, anticipation 3 f, reaction cascades | characters mostly stand still in medium shots (grid) → **[not measured frame by frame; visual: weak]** | same | section c (pose language) |
| 10 Expression | face change every 0.3-2 s, ≥ 10 expressions | static faces across held shots (grid frames show the same neutral faces) → **[visual: fail]** | same | a11 |
| 11 VO delivery | 3.4-4.1 w/s, ≤ 3 gaps > 0.8 s, none > 1.2 s, −14 LUFS, LRA ≤ 3.2 | **2.54 w/s**, **15 gaps**, max **1.66 s**, −14.6 LUFS ✓, LRA 2.5 ✓ → **40 %** | **2.66 w/s**, **16 gaps**, max **1.50 s**, −14.7 ✓, LRA **4.7** ✗ → **20 %** | a2, section f (trim pauses, tags; Salzburg's soft tags) |
| 12 Music | constant bed ~20 dB under VO, light plucked loop | owner: wrong music → **fail (owner review)** | owner: OK-ish → [not measured] | a17, a18 |
| 13 Script + hook | oddity in sentence 1, doubter, escalation, reveal 50-85 %, payoff last | hook is a date ("In 1730…") ✗, no doubter ✗, no escalation ✗, no reveal ✗, payoff = tag line ✗ → **0 %** | paradox hook ✓, no doubter ✗, chronological list ✗, no reveal ✗, tag line ✗ → **20 %** | a1, a3, section g template |
| 14 Ending | ≤ 1.2 s after last word, no CTA/end card | ends on a poster-on-wall card with "Dresden, on your wall." ✗ → **0 %** | same ✗ → **0 %** | a19, a20 [derived] |
| **Overall (mean of scored rows; rows 9-10 visual only, Salzburg music unmeasured)** | ≥ 95 % | **31 %** (12 rows) | **28 %** (11 rows) | |
Salzburg "felt unique" to the owner, and it is the one with a paradox hook, which is the only Rick script element either video had.

## The six owner complaints mapped to guide rules
1. **Drew's voicing** → 2.5-2.7 words/s with 15-16 long pauses (Rick 3.75 w/s, ≤ 3) and soft tags on Salzburg. Rules a2 and f.
2. **Music** → rules a17, a18: one light plucked loop with a soft pulse, constant ≈ 20 dB under the VO from frame 0 to the end.
3. **Character look** → 3D figurines with no outline instead of flat drawn heads with a 6-10 px monoline outline. Rules a9, a10, c.
4. **Scene pacing** → the camera is too slow (motion 2.5-3.3 vs ≥ 4.5) and holds still for up to 36 f (Rick 7 f). Join count is fine. Rules a5, a7, a8.
5. **Transitions** → every join was the same 5 f linear dissolve, without bridge objects or phrase-onset placement. Rule a4: 6-12 f, longer for quiet stories. Rule a6: bridge objects. Section b: the bridging recipe.
6. **Lettering** → captions are 11-22 % too large and too wide (2-4 words) and spell numbers out. Rules a12, a13, d.

---
# LEDGER ENTRY 2026-11-19 — Black Friday round 3 and originals #10/#14, re-measured against Rick's 5 newest videos

Appended entry; nothing above this line was changed. Scope set by the owner: compare our Black Friday (BF) test video, and the two originally dissected Rick videos (#10, #14), with Rick's 5 newest (#21 to #25). All 8 videos measured with the same code. Evidence: `new-analysis/COMPARISON_scene-time-and-audio.md`, `new-analysis/MUSIC_findings-and-spec.md`, `new-analysis/PRIORITY-AB_sets-and-bodies_rick-vs-bf.md` and `PRIORITY-AB_verification.md`. Guide sections cited are in the v1.1 addendum of rick-master-guide.md (sections l to q). BF file measured: `experiments/2026-11-18_rick-99-test/final/round3/BlackFriday_Philadelphia_round3_small.mp4` (58.4 s, 16 shots, true shot ranges from the build).

## Ledger summary (one row per video scored in this ledger)

| date | video | scored against | result | biggest gaps | entry |
|---|---|---|---|---|---|
| 2026-11-17 | Dresden (giant stollen) | guide v1.0 rubric | 31 % | script, camera, character look, ending | top of this file |
| 2026-11-17 | Salzburg (silent night) | guide v1.0 rubric | 28 % | same, plus grade | top of this file |
| 2026-11-19 | Black Friday round 3 | Rick's 5 newest, measured ranges (guide v1.1 l to n) | 15 of 41 measures inside Rick's range (table B below); five-verifier rubric score from the BF thread: 90/100, closeness about 70 % | shot-length shape, payoff speed, events inside shots, flat distant major-key music, flat set surfaces, long-coat bodies with rigid limbs | this entry |

## A. The two owner hunches

1. "Our scenes stay on screen too long versus Rick's." CONFIRMED in shape, not in average. BF's average shot (3.65 s) is inside Rick's range (2.65 to 4.54). The median is too long (3.64 s against 1.95 to 3.33), only 6 % of shots are under 2 s (Rick 20 to 53 %), 50 % are over 4 s (Rick 20 to 26 %), the first join comes at 5.55 s (3 of 5 Rick videos cut inside 3 s), and the payoff shot runs 6.37 s (Rick shows a payoff shot for 0.93 to 2.98 s on average).
2. "Our music lacks Rick's engaging quality." CONFIRMED. BF's bed is flat (5.65 dB range against 7.8 to 15.0), far from the voice (19.1 dB mean gap against 14.4 to 18.5; never closer than 14.2 dB where Rick reaches 5.4 to 9.8 in 4 of 5), in a major key (all 7 Rick beds are minor), at 120 BPM on a rigid grid (Rick 92 to 100 in 5 of 7), mid-register (42 % of energy under 250 Hz against 56 to 69 %), with 11 sound events (Rick: 29 word-pops in #21 and #23 plus action clusters).

## B. BF round 3 against Rick's newest five, measure by measure

"In" = inside the min-to-max range of #21 to #25.

| # | measure | Rick newest 5 | #10, #14 | BF round 3 | in? |
|---|---|---|---|---|---|
| 1 | average shot length s | 2.65 to 4.54 | 3.13, 3.09 | 3.65 | in |
| 2 | median shot length s | 1.95 to 3.33 | 2.37, 2.80 | 3.64 | OUT |
| 3 | shortest shot s | 0.07 to 1.20 | 0.87, 1.32 | 1.45 | OUT |
| 4 | longest shot s | 7.50 to 15.17 | 8.15, 7.00 | 6.37 | OUT (no packed long take) |
| 5 | P10 s | 0.87 to 1.52 | 1.09, 2.07 | 2.23 | OUT |
| 6 | shots per minute | 13.2 to 22.6 | 19.2, 19.4 | 16.4 | in |
| 7 | share under 2 s | 0.20 to 0.53 | 0.42, 0.10 | 0.06 | OUT |
| 8 | share over 4 s | 0.20 to 0.26 | 0.21, 0.19 | 0.50 | OUT |
| 9 | joins per 10 s | 2.03 to 3.60 | 3.03, 3.08 | 2.57 | in |
| 10 | first join inside 3 s | 3 of 5 | 0 of 2 | no | in (allowed), but see 11 |
| 11 | payoff: mean visible shot time s | 0.93 to 2.98 | 5.49, 2.28 | 3.00 | OUT |
| 12 | payoff: cuts per min | 9.9 to 39.6 | 0, 12.7 | 10.0 | in (lowest edge) |
| 13 | hard or fast joins | 0 to 19 | 1, 2 | 1 | in |
| 14 | dissolve median f | 6 to 8 | 11, 6 | 8 | in |
| 15 | character / prop / FX events per s | 1.49 to 1.78 | 1.13, 1.20 | 1.25 | OUT |
| 16 | camera events per min | 64 to 87 | 63, 79 | 68 | in |
| 17 | visual changes per min, no captions | 169 to 213 | 148, 169 | 158 | OUT |
| 18 | camera moving share | 0.43 to 0.85 | 0.76, 0.74 | 0.75 | in |
| 19 | caption cards per word | 0.77 to 0.85 | 0.77, 0.74 | 0.68 | OUT |
| 20 | caption dwell mean s | 0.32 to 0.35 | 0.35, 0.37 | 0.43 | OUT |
| 21 | caption dwell P90 s | 0.53 to 0.57 | 0.58, 0.53 | 0.70 | OUT |
| 22 | words per s | 3.59 to 3.83 | 3.71, 3.65 | 3.42 | OUT (locked take; inside guide a2's 3.4 to 4.1) |
| 23 | cuts per sentence | 0.75 to 1.36 | 1.12, 0.95 | 1.00 | in |
| 24 | joins within 3 f of a phrase start | 0.22 to 0.47 | 0.22, 0.30 | 0.93 | OUT (mechanical) |
| 25 | end after last word starts s | 0.37 to 0.87 | 0.58, 0.27 | 0.92 | OUT (by 0.05 s) |
| 26 | mix LUFS | -14.1 to -14.0 | -14.0, -14.1 | -14.3 | OUT (by 0.2) |
| 27 | LRA LU | 2.2 to 2.9 | 2.3, 2.1 | 2.3 | in |
| 28 | true peak dBTP | -2.1 to -1.7 | -1.9, -2.2 | -3.4 | OUT |
| 29 | VO stem LUFS | -14.4 to -14.2 | -14.3, -14.3 | -14.4 | in |
| 30 | VO minus music, mean dB | 14.4 to 18.5 | 15.9, 16.3 | 19.1 | OUT |
| 31 | closest approach dB | 5.4 to 14.3 | 5.7, 6.1 | 14.2 | in (edge; 4 of 5 are under 10) |
| 32 | bed level range dB | 7.8 to 15.0 | 16.7, 15.5 | 5.65 | OUT |
| 33 | ducking depth dB | -0.3 to 0.9 | 0.7, 1.1 | 1.4 | OUT (slightly) |
| 34 | key mode | minor, 5 of 5 | minor, 2 of 2 | major | OUT |
| 35 | tempo BPM | 92 to 100 (3 of 5); 2 uncertain | 99.4, 97.3 | 120.0 | OUT |
| 36 | energy under 250 Hz | 56 to 69 % | 28 %, 67 % | 42 % | OUT |
| 37 | percussive : harmonic | 0.51 to 1.42 | 0.18, 0.76 | 0.32 | OUT |
| 38 | caption cap height px / baseline % H | 53 to 56 / 71.67 | 53 to 54 / 71.7 | about 56 / 71.7 | in |
| 39 | fine surface detail on sets (Laplacian variance) | 75 to 142 | | 11 | OUT |
| 40 | set-edge line width px | median 2 (1 to 9) | 2 to 6 | 4 to 8 | in range, but on every edge and near black |
| 41 | torso height in head widths / visible legs | 0.72 to 1.05 / 0.93 to 1.31 | | 1.19 to 1.69 / 0.11 to 0.17 | OUT |

Count: 15 of 41 measures inside Rick's range (rows 1, 6, 9, 10, 12, 13, 14, 16, 18, 23, 27, 29, 31, 38, 40), 26 outside. Rows 31 and 40 are inside only at the edge. Four of the "outside" rows miss by a hair (25, 26, 33) or are fixed by the locked voice take (22). The clusters that matter: shot-length shape (2, 3, 5, 7, 8, 11), events inside shots (15, 17), captions (19 to 21, 24), music (30, 32, 34 to 37), sets (39) and bodies (41).

## C. What the originals (#10, #14) tell us about how Rick has changed

The v1.0 guide was built on #10 and #14. Re-measured with the same tools as the newest five:
- Hard cuts: 1 and 2 then; 0 to 19 now (4 of 5 use 8 or more).
- Payoff: slow then (0 to 1 join in the last sentence, 5.5 and 2.3 s per shot); fast now (1 to 3 joins, 0.9 to 3.0 s).
- Events inside shots: 1.13 and 1.20 per s then; 1.49 to 1.78 now. Camera activity did not rise.
- Captions: slightly slower then (dwell 0.35 to 0.37 s; now 0.32 to 0.35).
- Music: the same kind of mix then and now (mean gap 15.9 and 16.3 dB; rides of 15.5 and 16.7 dB; minor keys; no ducking). The v1.0 statement "constant bed, about 20 dB under" was a measuring error of ours, not a change by Rick.
- Sets: more edge ink then (5 of 8 crops) than now.
So BF round 3, which was built to v1.0, is closest to the OLD Rick on cutting (few hard cuts, calm payoff) and matches neither old nor new Rick on music.

## D. Lessons recorded (what would have prevented each gap)

| gap in BF round 3 | cause | guide v1.1 section / proposed rule |
|---|---|---|
| no short shots, half the shots over 4 s | storyboard gave one shot per sentence; v1.0 only said "1.5 to 8.5 s" | l.1; rule 230 |
| slow hook and slow payoff | no rule on section pacing | l.2; rules 232, 233 |
| calm long shots | no events-per-second target | l.3; rules 231, 237 |
| joins locked to commas | v1.0 said "on phrase onsets" | l.5; rule 236 |
| captions hold 2 to 3 words | v1.0 allowed 1 to 3 words with no dwell limit | l.4; rule 241 |
| flat, distant, cheerful bed | built to v1.0 a17/a18, which were wrong | n; rules 243 to 248 |
| sets read as clean CG | effort went into edge ink; surfaces left flat | m.1; rules 249, 250 |
| stiff long-coat bodies | proportions copied from costume silhouettes, limbs as single cards | m.2, m.3; rules 252 to 255 |
| two verification rounds lost | loose measuring definitions | p; rules 257 to 259 |

Next ledger entry: BF round 5 (first round built from these files), measured with the same tools, same table.


---
# LEDGER ENTRY 2026-11-19 (second entry of the day) — 99 % verification run: what stands, what was corrected, what is still open

Appended entry; nothing between the top block and this line was changed. No new video was scored. This entry re-tests the 2026-11-19 entry above against the owner's stricter standard (two blind measurements at 99 % or more, known-answer test for every tool, definitions written first). Full record: `new-analysis/VERIFICATION_v2_2026-11-19.md`. Guide: v1.2 addendum, sections r to v.

## Ledger summary row

| date | video | scored against | result | biggest gaps | entry |
|---|---|---|---|---|---|
| 2026-11-19 | Black Friday round 3 (re-check, no new score) | same table B, with rows 34 and 35 re-classed | 15 of 41 inside, 26 outside; rows 34 (key) and 35 (tempo) now compare against [uncertain] Rick ranges | unchanged: shot-length shape, payoff, flat distant bed, flat set surfaces, long-coat bodies | this entry |

## E. Corrections to the entry above (old value, new value, date 2026-11-19)

| where | old | new | why |
|---|---|---|---|
| A.1 "the payoff shot runs 6.37 s (Rick shows a payoff shot for 0.93 to 2.98 s on average)" | one mixed pair | two pairs: mean visible shot time in the last sentence 3.00 s against 0.93 to 2.98 s; average length of shots that start in the payoff 6.37 s against 1.57 to 5.37 s (4 of 5 at 1.57 to 2.40 s) | the sentence paired two rows of the comparison table. Table B row 11 was right |
| A.2 "all 7 Rick beds are minor"; B row 34 "minor, 5 of 5 / 2 of 2" | minor in all | minor confirmed by two validated tools for 4 of 7 (#21 E minor, #22 D minor, #23 D minor, #10 D minor); #24, #25, #14 unconfirmed; none confirmed major; ours F major (confirmed) | the first key tool confuses a minor key with its related major |
| A.2 "Rick 92 to 100 in 5 of 7"; B row 35 | a finding | [uncertain]: method 1 (7 of 8 agreement) gives 92 to 100 BPM for 5 of 7; two-tool values only for #23 (100.0), #14 (96.8), #10 (66.7), ours (120.0) | three methods, none at 99 % |
| B row 39 | 75 to 142 | unchanged; ours (11) exact in both measurements, Rick's value depends on the measurer (75 and 142); the lower value is the floor | source re-check |

## F. Fields under 99 % after three methods (owner decision, Nov 19: mark uncertain, no rule; include method 1 values)

Method 1 values, kept at the owner's request (highest agreement of the three methods, still under 99 %, so [uncertain] and not rules):
- Head outline width (ring scans, 17 of 18 heads = 94.4 %): medium shots 7 to 12 px, wide shots 4 to 5 px, close-ups 12 to 18 px (n = 2) at 1080 px frame width; 2 to 3.5 % of head width. Later methods (two tools, 48 heads): about 2.5 % of the head's skin-fill width (3 px small, 6 to 7 px medium, 10 to 11 px close). Working guidance: 2.5 to 3.5 % of head width, never under 2 %.
- Tempo (beat tracking on the music stem, 7 of 8 videos = 87.5 %): #21 98.0 BPM, #22 75.6 (or about 113), #23 99.9, #24 86.1 (not corroborated), #25 92.0, #10 99.4, #14 97.3; ours 120.1. Later two-tool values: #23 100.0, #14 96.8, #10 66.7 (the same 7.2 s loop counted as 8 beats instead of 12), ours 120.0. Working guidance: 92 to 100 BPM, not 120.

Status of every field after this run:
- Verified: pacing statistics 141 of 141; loudness, voice-to-music gap, level range, duck depth, mix LUFS, true peak 66 of 66; shot boundaries 99.1 % raw with the dissolve tool at 17 of 17; caption cap height, baseline, text, head fill width, luma, camera counts 100 % (round 2); sets and bodies re-measured by a second agent with corrections applied.
- [uncertain], not rules: bed loop length as a field (6 of 8; two-tool values #21 9.82 s, #22 6.35 s, #23 9.60 s, #10 7.20 s, #14 4.96 s, ours 8.00 s); tempo (three methods: 7 of 8, 5 of 8, 4 of 8); key beyond the four confirmed minor beds (signature 6 of 8, tonic 5 of 8); head outline width (three methods: 94.4 %, void, 77.5 %); instruments, genre, mood, SFX types (no listening tool passes its known answers).

Listening: the owner proposed github.com/Leonxlnx/earshot. It was reviewed before install (safe: local, pinned weights, nothing uploaded) and tested on known answers. Route 1 (earshot): 0 of 8 instrument questions pass in a full mix; SFX type 58.7 % clean, 23.8 % under music; its tempo and key also fail. Route 2 (Demucs 6 stems plus measurements plus earshot on stems): 1 of 14 questions passes (choir, weak); SFX 60.5 % clean, 14.1 % under music. Route 3 (music taggers on real labelled music under a narrator): still running when this text was written; its result is in `research/rick-style-spec/new-analysis/VERIFICATION_v2_2026-11-19.md`, Addendum B. Nothing from it is used unless it passes its known answers.

## G. What round 5 still has to close

BF measures still outside Rick's range. Last version measured with these tools: round 3 (rounds 4 and 5 are not yet measured with them; this is the list round 5 must close). 26 of 41 outside:
- Shot-length shape: median 3.64 s (Rick 1.95 to 3.33), shortest 1.45 s (0.07 to 1.20), longest 6.37 s with no packed long take (7.50 to 15.17), P10 2.23 s (0.87 to 1.52), share under 2 s 6 % (20 to 53 %), share over 4 s 50 % (20 to 26 %), payoff mean visible shot time 3.00 s (0.93 to 2.98), payoff shots 6.37 s (1.57 to 5.37).
- Events and captions: character/prop/FX events 1.25 per s (1.49 to 1.78), visual changes 158 per min (169 to 213), caption cards per word 0.68 (0.77 to 0.85), caption dwell mean 0.43 s (0.32 to 0.35) and P90 0.70 s (0.53 to 0.57), joins within 3 f of a phrase start 93 % (22 to 47 %).
- Narration and tail: 3.42 words per s (3.59 to 3.83; locked take), end 0.92 s after the last word starts (0.37 to 0.87).
- Mix and music: mix -14.3 LUFS (-14.1 to -14.0), true peak -3.4 dBTP (-2.1 to -1.7), voice minus music 19.1 dB (14.4 to 18.5), bed level range 5.65 dB (7.8 to 15.0), ducking 1.4 dB (-0.3 to 0.9), energy under 250 Hz 42 % (56 to 69 %), percussive to harmonic 0.32 (0.51 to 1.42). Key (F major against 4 confirmed minor beds) and tempo (120 against method-1 92 to 100) stay listed as outside, but both Rick ranges are [uncertain].
- Look: set surface detail 11 (75 to 142), torso 1.19 to 1.69 head widths (0.72 to 1.05), visible legs 0.11 to 0.17 (0.93 to 1.31).
The Black Friday thread reports its round-5 plan already targets these (21 shots, a D minor bed about 16 dB under with a 13 dB swing); that is its plan, not a measurement.

## H. Lessons recorded

| what went wrong | what would have prevented it | proposed rule |
|---|---|---|
| "minor key in all" and "92 to 100 BPM" stated from one tool | known-answer test with a narrator on top before the first measurement | 261, 262 |
| outline width read as 2 px by two tools | known answers with the videos' sharpening halo | 261, 262 |
| payoff sentence mixed two rows | check each summary sentence against its row | 265 |
| genre and instruments could not be heard | specify beds by measured quantities | 266 |

Next ledger entry: BF round 5, same table B, measured with the same tools.
