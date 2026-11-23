# Detroit Thanksgiving video: findings for the loop docs

Video: "Why Detroit plays football every Thanksgiving" (Monday Nov 23 extra). Builder thread: "Build Detroit Thanksgiving video".
These findings are for the coordinator thread "Redesign weekly video schedule". It alone writes the rulebook, gap report, guide addendum, change report and lessons log. This file does not edit any of them.
Format for each finding: what happened, the cause, a proposed rule, a probe, and the adjustment made here.
Rounds:
- Round 1: det2, PC GPU, 70.7 min.
- Round 2: det3, PC GPU, 69.5 min.
- Round 3: det4, PC GPU.
- Rounds 4-9 (det5-det9): Rick cast rebuild (rule 329), shoulder-join fix, expression library merge (rules 330-334); det7 and det9 were posted through and kept as fallbacks (`fallback/`).
- Round 10: det10b, PC GPU (commit c54d7a5, clips fbac3f7), then a post-only r10b pass (captions, ink fringe, bed level, small-copy peak).
The verifier reports are in `verifier-reports/r1`, `r2`, `r3`, `r10` and `r10b` next to this file.

## Result (round 10b, for Gate 2)
- **Files:** `det_r10b_2k.mp4` (1440x2560, 1652 frames, 55.07 s, sha256 c9c393b1...e760) and `det_r10b_small.mp4` (720x1280, 8.0 MB, under 10 MB, -2.2 dBTP).
- **Passing:** payoff and poster (E1-E5, rule 320), scene-time must-have (3.43 w/s, 38 % of shots under 2 s, 24 % over 4 s, camera moving 88-94 %), -14.0 LUFS / -1.9 dBTP, 21 of 41 Rick ledger measures inside range, 32 distinct faces, every face card one per frame.
- **Fixed in r10b (post only):** caption baseline jump in S05/S06 (only 'baseball' stays off band), VO-to-bed gap (bed -0.6 dB: 15.2 dB 3 s mean, 14.57 integrated), small-copy true peak (-2.2 dBTP). The bedcheck 'ducking' +4.69 dB is the end hold after the last word (f1632-1652), the known F6 artifact.
- **Improved but still failing by the letter of the probe:** rule 308 ink. Dark-red line cores fell from 62-75 % to 36-49 % of rays in S01/S05/S13/S14/S20, near-black in S07 from 29 % to 8 %; the darkest-2 % ring still collects dark red background. Line bodies read plum at 2K.
- **Known exceptions going to the owner (need a re-render or a new VO):**
  1. R24: "Richards" twice and five numbers in the VO; $8,000 is disputed ($7,952 vs about $15,000).
  2. S01/S20 frontal eye-level sofa row (P3/R21).
  3. Work-touches-material props: painter's brush in the lowered hand, no pen on the calendar circle, cash never lifted, operator holds no plug.
  4. Short bodies under rule 336 (castcheck 0.88-0.89 / 1.12 / 3.00 head widths; on screen 0.79-0.85 / 0.96-1.06) and rule 336a limb width plus pear torso; arms read as straight sticks.
  5. Minor: 'baseball' caption sits at 76.5 % for 9 frames (a face fills the band), S16 whip pan, S11 6.92 s longest shot, payoff hit inaudible under the bed.

## Findings

### F1. VO pace missed on the first take; a faster take plus a retime fixed it
- **What happened.** Take 1 read at 2.9 w/s (Rick 3.4-4.1).
  - The owner chose a faster take plus a retime.
  - Take 2 read at 3.07 w/s.
  - Take 4 had stronger fast tags and read at the same pace as take 3. It was dropped.
  - Take 3 reaches 3.4 w/s only after its pauses are shortened.
- **Cause.** Drew on eleven_v4 with [energetic, playful storytelling] tags reads about 2.9-3.1 w/s raw. Tags alone do not move him to 3.4.
- **Proposed rule.** Measure pace by Rick's method (rule 179: whisper tokens divided by speech span) on the RAW take before building.
  - If the raw take is under 3.25 w/s, re-record before any build. Pause trimming can add about +0.25 w/s at most without cutting speech (see F2).
  - Script length is the lever: cut words, not pauses.
- **Probe.** `words.py` on the raw take, then tokens / (last end - first start).
- **Adjustment here.** Take 3 with silence-only pause cuts gives 186 tokens over 54.18 s = 3.43 w/s. By script word count it is 3.38, so the pass is marginal.

### F2. Pause trimming cut speech twice (gapcut1, then gapcut3)
- **gapcut1 (round 1).** It cut at whisper word boundaries, and those boundaries are loose by up to 0.1 s. It clipped voiced speech at 3 joins.
- **gapcut3 (round 2).** It cut only in "unvoiced" runs. Its voicing map treated a high zero-crossing rate as unvoiced, so it removed sibilants.
  - Word-final "s"/"ts" disappeared at 8 joins: "champs" was heard as "champ", plus "bucks" and others.
  - Loud audio (>-40 dBFS) fell from 48.56 s to 47.69 s.
- **Proposed rule.** Pause cuts may remove only:
  - silence (10 ms frames at or below -45 dBFS);
  - breath (-45 to -35 dBFS with under 50 % of energy above 4 kHz).
  - Never remove sibilants (over 50 % of energy above 4 kHz) or voice.
  - Leave at least 20 ms of silence, use 10 ms guards and a 10 ms equal-power crossfade.
- **Probe.** "Loud audio in vs out":
  - seconds above -40 dBFS before and after the cut, which must not drop more than breaths account for;
  - a whisper re-transcription of the cut file that hears every final "s".
- **Adjustment here.** gapcut4 plus gapplan4.
  - Loud audio is 48.56 s in and 48.35 s out; the 0.21 s is breaths.
  - Whisper hears "champs," again.

### F3. The retime (keyframe warp) created pops and double faces
- **What happened.** Moving every keyframe through an old-to-new word-onset map:
  - clamped the -1 visibility key onto frame 0, which hid the family at f0;
  - caused 1-frame pops at shot boundaries after rounding;
  - in round 2, showed two face cards for 1 frame when two CONSTANT keys of one card rounded onto the same frame. The warp bumped one of them +1 (S08 grandpa, f555/564/569).
- **Proposed rule.** A retime must:
  - extrapolate outside the map;
  - snap visibility keys that sat on an old shot boundary to the new boundary;
  - then re-key every mutually exclusive card group (faces, arm cards, stride bodies) from its per-frame state so that exactly one card shows.
- **Probe.** `warp_det.sanitize()` prints the frames it fixed (1 in round 3). The shots verifier's face-count check samples every frame.
- **Adjustment here.** Done in `warp_det.py` (round 2: extrapolation and snapping; round 3: sanitizer).

### F4. Ink colour must be keyed on the RAW render, not the graded frame
- **What happened.** Card ink rendered bright magenta in lamp-lit shots and near-black in daylight. Ink fix v1 was keyed on the graded frame and left magenta in S17/S18.
- **Adjustment.** v2 keys on the raw render (plum hue 165+-15, s > 0.16, v 0.035-0.52) and sets RGB (58,34,50). The visual verifier measured (57,32,49) in every shot from round 2 on.
- **Proposed rule.** Rule 308's fix runs on raw frames.
- **Probe.** `inkring.py`, which takes the darkest 2 % of head rings. Hair, helmets and DOF blur read as OUT, so check those with crops.

### F5. Rule 319 (SFX over the bed) vs rule 192 (SFX under the VO) conflict at the payoff and on tonal dings
- **What happened.** Round 2 dipped the bed under the payoff event. Applied once per levelling pass, the dip compounded to 6.3 dB and then a +14.6 dB swell, which broke the owner's "smooth constant bed, no pumping".
- **Proposed rule.** Never dip the bed for an SFX. Where 319 [G] and 192 [C] cannot both hold, 192 and the owner brief win, and the shortfall is reported.
  - Prefer low or low-passed sounds (a ding an octave down, a low-passed whoosh): K-weighting penalises highs, so these clear the bed more under the same LU cap.
- **Probe.** `sfxlevel.py` prints, per group, the dB over the bed and the LU vs the VO. `sfxoverbed.py` gives OVERBED_MIN.
- **Adjustment here.** No dip. 10 groups (10.9 per minute, rule 192 about 10-12).
  - The map ding is an octave lower and the payoff whoosh is low-passed.
  - Map ding +2.4 dB and payoff +3.2/+2.7 dB over the bed: rule 319 shortfall, reported.

### F6. bedcheck's "bed in VO gaps vs under VO" reads the end hold as a gap
- **What happened.** With pause cuts, the only gap over 0.3 s is the hold after the last word, where the payoff lift plays. The metric then reports 6-8 dB, which is not ducking.
- **Proposed rule.** Exclude the end hold from that metric (rule 322: name the metric behind every number).

### F7. Rule 320 probe sampled every 6th frame
- **What happened.** postprobe's "last 10 frames" were really the last 10 SAMPLED frames (spanning about 50 frames), which included the poster's colour ramp-in.
  - On the true last 10 frames, the poster sat 0.004 under the rest of the frame.
- **Adjustment.**
  - The probe now reads the true last 10 frames.
  - Paste gain raised from 1.09 to 1.12.
  - Bay dim changed from 0.88 to 0.86.

### F8. Captions on faces: pixel face detection fails; project the faces from the scene
- **What happened.** Detection of near-white blobs missed lamp-lit and shaded faces (v 136-168) and merged faces with white collars.
  - In round 2, 6 shots still had captions on faces (T7 [C]).
- **Proposed rule.** Export exact face discs from the blend: `facebox.py`, which projects each visible face card through the shot camera. Each card then takes the first baseline that clears every face it is shown over.
  - Order: 71.7 %, 76.5 %, 65.5 %, 60 %, 78.5 %, 52 %, 45 %, 38 %.
  - S21 cards sit above the poster at 19.5 %.
- **Probe.** The overlap of caption box and face box per card, printed by post (CAPBASE).
- **Trade-off.** T1, the baseline at 71.7 %, now has about 30 cards off-band. T7 is [C] and T1 is not, so the move wins.

### F9. Staging: depth rows must READ as depth (P3/R21)
- **What happened.** Staggering characters by 0.3-0.5 m in depth did not read: head sizes came out 15.6 vs 17.2 % W.
- **Rule proposed.** In a group shot, put one character within about 2 m of the camera (head 28-36 % W, rule 309) and the rest at least 1 m further back.
  - A table seen frontally becomes a high diagonal view (camera about 2.4 m up, about 35-40 degrees off axis), with the speaker in the foreground.
  - A front character's raised arms must never cross a face behind it. Use low pumps for the front figure, and raise arms only on the side away from neighbours.
- **Probe.**
  - armprobe (0 pairs in round 3);
  - occprobe: partial body overlaps are now expected, and face overlap is what counts;
  - quick Cycles previews (`preview.py`, 6 samples, about 5 s per frame on CPU) of each restaged shot before packing.

### F10. "Work touches material" with 2D cards: show the result, or design the contact
- **What happened.** Hands on cards could not be made to touch:
  - plugs to jacks;
  - a pen to a calendar;
  - cash passed hand to hand;
  - a hand on the SOLD OUT sign;
  - a painter's brush.
  Each became a pop (F3 rule) or a "hand away" fail.
- **Adjustments.**
  - The calendar is already circled when the camera arrives.
  - The operator talks into the headset.
  - The radio man holds the cash up, with no pass.
  - SOLD OUT rolls down as a blind under the clerk's raised hand.
  - The painter brushes only the last letter, which sits beside his hand.
- **Rule proposed.** Script only contact beats that a card rig can sell: the prop is parented to the hand, or the material is within reach of a fixed pose. Otherwise show the before and after across a camera move.

### F11. Signs and lettering cut by the frame edge (G6)
- **What happened.** ON AIR, the kiosk papers and the S09 calendar sat half in frame for whole shots.
- **Cause.** Framing maths used the camera x instead of the look-at ray.
- **Rule proposed.** Before packing, check each sign's projected box against the frame on the first, middle and last frame of its shot. It must be fully in or fully out. (A probe like facebox.py, for signs, is worth adding.)

### F12. Body proportions: two verifiers measured opposite errors
- **Measurements.** Visual verifier: legs 1.35, total 3.45 head widths. Shots verifier: legs 1.21, total 3.12. The design is 1.27 / 3.25.
- **Cause.** The measurement method (head width vs height, outline in or out, perspective).
- **Recommendation.** Fix one measuring method, the same one used on Rick, before treating must-have 3 as pass or fail.
- **Adjustment here.** No rig change.

### F13. Script-level exceptions (need a new VO, reported to the owner)
- **R24.** Five numbers (1934, 8,000, 94, 26,000, 19-16) and "Richards" spoken twice. The limits are 1-4 numbers and one name.
- **S9.** "About eight thousand bucks" is contested. The Detroit Historical Society and Fox 2 give $7,952.08; Wikipedia and the NY Sun give about $15,000 including debts.
- **Rule proposed.** Check R24 and two-source facts at the script gate, before VO.

### F14. PC and cloud operations
- PC memory gate passed every time: 6.9 GB free RAM and 19.0 GB commit (det2); 6.6 / 18.2 GB (det3 and det4).
- Render times:
  - det2: 70.7 min, 1,726 frames.
  - det3: 69.5 min, 1,703 frames.
  - Encode takes about 5 min.
- The first PC test run wrote to C:\test by mistake. The PC must use absolute D: paths only; the empty C:\test folder is still there.
- Cloud post (`post.py`, 2K, about 1,650 frames) takes about 55 min, longer than the 30-minute default background limit. Run it with a 2-hour timeout.

### F15. Code swallowed by an appended comment (three dropped statements in round 3)
- **What happened.** Round-3 edits appended a `# note` to a line that still had code after it. Python read the rest as comment:
  - S11 `ALL+=[rm11,op]`: the two characters were never finished, so they had no face keys (shots R08 critical, "frozen faces");
  - S18 `+[f'cal{y}' ...]+['cal2026']`: the year calendars were never built (text in-world critical);
  - S01 the kid/mom/grandma cheers, S13 the clerk bob, S08 the kid's faces.
- **Proposed rule.** Never append a comment by replacing a line prefix. After every scripted edit, run a lint that flags code-like text after `#` (`ALL+=`, `+[`, a call with `;`), and assert list lengths that must match (calendars vs ranges).
- **Probe.** The regex scan in this thread; `assert len(CR)==len(cals)` now in scene_det.py.
- **Adjustment here.** All five restored in round 4.

### F16. Caption band vs faces: tilt the camera per shot instead of moving the caption
- **What happened.** F8 moved 31 of 164 cards off the 71.7 % band to clear faces. The text verifier then failed T1 (29 baseline jumps, S18 bouncing every 4-6 frames, a card across the S06 headline).
- **Cause.** Faces sat in the band because push-ins end on close-ups with the face low in frame (S06, S17, S18 down to 0.94 of the height).
- **Proposed rule.** Stage so every face whose box meets the centre caption column (0.37-0.63 W) ends above 0.665 H. Fix by tilting the shot camera, not by moving the caption.
- **Probe.** `tiltcalc.py` reads faceboxes.json and writes tilt.json (per-shot frame shift); `lib.path()` lowers each target by shift x 36/lens x distance. Two passes converge.
- **Adjustment here.** 14 shots tilted 0.005-0.197 of the frame height. S05 capped at 0.12 (a larger tilt cut the BALL PARK sign); its last 17 frames still need the fallback baseline.

### F17. Faces cut by the frame edge: print them by name before packing
- **Probe.** `facebox.py` now prints `FACECUT shot head first last` for any face partly outside the frame away from the shot edges.
- **Adjustment here.** S12 lens 34 to 28 mm and a shorter push; S18 Richards moved 0.15 m in and the push shortened. Remaining cuts are exits during camera moves (S04 truck, S10/S11 pans, S16 game action, S21 push past the family).

### F18. Props that must read on screen
- **S03 cash.** The arm card with cash hung behind the desk; nothing showed for "$8,000". Round 4 puts banded stacks of bills on the desk for the whole shot.
- **S04 lettering.** The final S now fills in three top-to-bottom stages (lions4s0-2.png) over 9 frames while the painter, moved up the ladder, brushes beside it.
- **S10 calendar.** Circled from the first frame of S10, so the circle never pops on in view.

### F19. Body proportions, round 4
- **Measurements in round 3.** Visual verifier: torso 1.10, legs 1.36, total 3.48 head widths. Shots verifier: total 3.37 (S07) and 3.10 (S19). lib.py comments give the design as 3.25.
- **Adjustment here.** Body cards, shoulder pivots, head pivot and arm cards are scaled 0.91 about the feet (BSY in lib.py). Visual-method target about 3.26. F12 still applies: one measuring method has to be fixed.

## Reuse decisions (Black Friday pipeline -> Detroit)
- Reused unchanged: post.py grade/dissolve/caption/poster pipeline, mix.py, bedcheck.py, sfxcheck.py, postprobe.py, facebox.py, the PC package pattern (split parts + sha + README) and the six-slice verifier prompts.
- Rebuilt for Detroit: cast.py bodies (rule 329), lib.py GEO shoulder pivots, castcheck.py (shoulder-join check, disc-centre head, rule 336 bands), expressions.py library (from the expression thread, branch v7vnb2), the finish() variety pass, facecount.py.

## New assets for the library
- Characters (cast.json det10b): radioman (bowler + pencil mustache), seller (flat cap + walrus), fanman (bowler + chevron), fanold (flat cap + droop), newsboy (flat cap + messy hair), kid34 (flat cap), gramps (white beard), dad34 (side part + curled), dadM (side part + chevron), kidM (cowlick), operator (top knot), clerk (stubble dots). All items from the approved library (rules 333b/c, 334).
- Sets: radio office, ball park sign, ticket booth with SOLD OUT blind, year calendars 1934-2026, payoff sideboard wall with gilt frame.
- Faces used: 32 distinct across 89 heads (rule 332 floor 14); the full per-character list is in verifier-reports/r10/shots_report.md.

## Token and time notes
- PC GPU (3070, OPTIX): det10b full film about 70-75 min; Cape Cod cc4 75.6 min for 1,936 frames (2.34 s/frame).
- Cloud post.py on 2K: about 40 min per pass (tracked background task).
- Verifiers: six slices in parallel, 8-24 min each, about 1.3 M subagent tokens per full round; a focused re-check of fixed items is about a sixth of that.


### F20. Rounding the torso top moved where the arms must join (owner "arm issue?")
- **What happened.** After the r7 capsule torso, old shoulder pivots left arm roots inside the outline (a second line) and stubs above the shoulder; the owner pinned three left shoulders.
- **Proposed rule.** Any torso width or shape change re-places the shoulder pivots ON the side outline, below the top curve.
- **Probe.** castcheck.py shoulder-join check in body-card local space (pivot within 0.020 m of the outline, outline slope at most 6 px there). Negative test: 19/19 fail on the old geometry.
- **Adjustment here.** GEO shoulder x 0.141/0.156/0.165, z 0.86; arm cards visible_shadow=False.

### F21. castcheck measured padded heads from the face-card centre
- **Cause.** Padded cards (tall hats, hair, beards) shift the card centre up while the head disc stays put.
- **Adjustment here.** castcheck measures from the disc centre (head pivot + 0.2535*HS) and uses rule 336 bands. Detroit reads 0.88-0.89 / 1.12 / 3.00 either way, so the fail is real; DC's rig fix (z0l0eh 09eca41: BSY 1.045, ARM_Q 0.91, new GEO, WK, hem, LW 30, AW 50) is to be merged for the next Detroit render.

### F22. Expression library in Blender: PIL import and texture count
- expressions.py imported PIL at module level; Blender's Python has none. Wrapped in try/except (mirrored upstream in 71361bd).
- "library":"all" generated 1007 face textures; named lists per character cut it to 315.

### F23. Variety pass (rule 332) first did nothing
- **Cause.** The alternate index could equal the current face, and repeated face entries split holds so none reached 40 f.
- **Adjustment here.** Merge repeated faces into one hold, cycle k/alternate in 22-36 f pieces, rotate a returning face to the next SAFE family item. Result 32 distinct faces, longest hold 50 f.

### F24. Rick warm skin rendered grey without AgX compensation (rule 335a)
- Raw rick_warm read 218,208,199 on screen. 255,214,178 pre-compensated reads about 224,206,193 (G/R 0.92, B/R 0.86). The neck plane must take the same skin colour.

### F25. Ink fringe: rule 308's darkest-2 % probe catches a 1-3 px dark-red edge
- **What happened.** r10 line bodies were plum, but the antialiased edge against red/brown/green backgrounds read (65,24,24) or near-black, so the [C] probe failed in 6-8 shots (a regression from round 3, when backgrounds were lighter).
- **Adjustment here.** Pass 1: a 2 px ring of dark pixels (value under 0.30) around the keyed line; the re-check showed almost no effect, because the line CORE itself reads dark red (61,22,22) on warm-lit lower outlines. Pass 2: thin dark strokes (black-hat 13 px on raw value, red-to-plum hue, value under 0.45) grown only along strokes connected to the plum-keyed line, so bleacher stripes and furniture slats stay. Core dark-red share fell about 25 points; still failing the [C] probe.
- **Proposed rule.** Fix ink at render time: the line material should be emissive (unlit) plum, so lamp light cannot push it red. Post keys are a patch.

### F26. Caption fallback: test the glyph box, not the padded box (but the T7 probe uses the padded box, so 'town,' grazes a face box by up to 7x7 px at f425-430; glyphs 47 px clear: minor), and shift a card start by 1 f before moving the baseline
- 'town,' moved only because its padding grazed a face (glyph-box contact under 0.1e-4 of the frame); 'the Tigers' touched a face only on its first frame (f430, the last S05 frame). r10b keeps both on the band ('the Tigers' starts at the S06 cut, +1 f lag inside T5). Only 'baseball' (real overlap) stays off band.

### F27. Stale mixlog fed sfxoverbed.py the wrong bed gain
- mixlog.txt (Nov 22 13:24) predates the final mix; sfxoverbed.py read -12.47 dB instead of -14.07. The probe should read the gain from the mix call (env BED_GAIN) or refit it from the stems, and mix.py should rewrite mixlog.txt on every run.

### F28. Verifier body targets disagreed with the cast rule
- The six-slice prompts used the v1.7 rendered-frame ranges (legs 1.25-1.28) while the cast was built to rule 331. Rule 336 and the verifier addendum (Nov 22) now separate build targets from rendered-frame floors; COMMON.md must carry the addendum every round.
