# DEFINITIONS v6, written 2026-11-20 6:50 PM CT BEFORE any v6 measuring (loop 4: named actions, body mechanics, asset physics, camera layers retry, music choice and mood)
Inherits definitions v5 (new-analysis-4/_agent-prompts/definitions_v5_2026-11-20.md) and COMMON_RULES. Status words: RULE (99 %+, n>=20), GUIDANCE (75 to 98.9 %, or population number with window), [INFERRED] (built by analogy; never above guidance), UNCERTAIN (under 75 % after three methods, results shown). Amendments only appended at the end with reason and time; hard samples never dropped.

## 1. One action vocabulary (fixed now; labellers and first-measurer logs are mapped to it)
Locomotion: walk, run, sneak, stumble, turn. Object handling: push, pull, carry, hold, lift, drop, throw, catch. Body: point, wave, sit, stand, fall, recoil, react, talk, emote. Other: any action not on this list gets its own name from the labeller, written once in the inventory. Sub-actions (face change, mouth change, blink, gesture, snap, tween) are recorded as "manner" tags on the action, not as the action. Evident = at least 3 occurrences in the 7 videos in at least 2 videos; thin = 1 to 2; absent = 0.

## 2. Inventory (new-analysis-5/inventory)
Built from the first-measurer frame logs and data JSON, then spot-verified by viewing frames for at least 30 randomly drawn entries (seed 2026112101) with a blind viewer; precision of the log mapping reported. Output: per named action, count, videos, frame ranges.

## 3. Motion by named action (evident actions)
Per occurrence two blind vision labellers (Sonnet; each writes each item to disk right after viewing it) plus method B (one labeller on zoomed crops of the moving part and a frame-difference check inside the character region). Fields and tolerances: found (time overlap); start and end within +-2 f; travel within +-2 f; hold length within +-3 f; limb set (upper arm, lower arm, hand, leg, foot, torso, head, hair, clothing: exact set match); easing class (linear, ease-in, ease-out, ease-in-out, snap): exact; loop length within +-2 f; construction (2D cutout, rigged, tweened): exact. Frames and milliseconds both reported (ms = frames x 1000/30). Pass marks: RULE 99 % at the tolerances above, GUIDANCE 75 %.

## 4. Body mechanics
Joint angle where a joint exists (neck, hip, knee, ankle; noodle arms: curvature as chord/arc ratio): within +-15 degrees (angle) or +-0.1 (ratio); stride length within +-0.25 head widths; cadence within +-1 f per step; squash and stretch yes/no exact; anticipation and overshoot yes/no exact and size within +-1.5 % of travel; settle length within +-3 f; feet, hair, clothing: moves yes/no and timing lag within +-2 f. Parts that never move are reported with their count. Same two-method rule and pass marks.

## 5. Asset physics
Inventory first (props, vehicles, animals, objects, particles, cloth, smoke, water, crowds). For evident assets: gravity (screen heights per s^2) within +-20 %; bounce count exact and height ratio within +-20 %; rotation within +-15 degrees per 10 f; scale pop (peak ratio within +-10 %, duration +-2 f); parallax (near:far shift ratio within +-20 %, only if camera layers pass their known answers). Two methods: human vision labelling on strips and tool tracking from loop 3 (A, C) with its known-answer marks 87.8 %.

## 6. Inferred recipes ([INFERRED])
For named actions or assets with absent or thin evidence: a written recipe built from the nearest observed actions, listing source actions and the change applied. Inference test (written now): hide 10 observed actions (seed 2026112102, stratified by action class); predict start-to-end travel, easing class and limb set from the remaining ones only; scored travel within +-3 f (or +-30 %, whichever is larger), easing exact, limb set exact. The score is printed with the recipes; recipes never become guidance.

## 7. Camera and layers, second attempt
Known-answer set first: at least 60 synthetic moves, 100 to 300 f, with whip pans, cuts in the tracked layer, moving characters, a character plane about 12 % of the frame, three focal lengths. Tool pass marks: scale +-5 % on 90 %+, roll +-0.5 degrees on 90 %+, pan and tilt +-5 % on 90 %+, layer ranking correct on 90 %+, parallax near:far +-10 % on 90 %+. Real-data method: chain short segments (30 f or less), focal length estimated from the footage. Two independent solvers must agree: scale within 10 %, roll within 1.0 degree, pan and tilt within 10 % or 0.5 % W, layer ranking identical, parallax within 20 %. Also report: what stays locked inside a shot (region fixed vs moving, per shot) and speed-curve class (linear, ease-in, ease-out, ease-in-out) from screen-space profiles. Loop-3 numbers repeated beside the new ones.

## 8. Music choice and mood
Fields per video: genre family, instrumentation list, mood (from a fixed list: tense, playful, warm, mysterious, epic, calm, melancholic, comic), tempo (+-3 BPM), key and mode, bed loop length (+-0.3 s), and per story beat (start, build-up, climax, payoff) whether the music changes (energy, density). Tools must first pass a known-answer set (own synthetic music beds with a voice on top and Rick-like sharpening and compression; at least 20 clips): key and mode correct on 90 %+, tempo within 3 BPM on 90 %+, mood class correct on 75 %+, instrument list recall 75 %+. Fields that fail stay UNCERTAIN and go onto a listening sheet for the owner (at most 6 questions). Two tools agree = within the tolerances above on 75 %+ of the 7 videos (GUIDANCE) or 99 % (RULE).

## Models
Opus for tools and measuring, Sonnet for labellers, Fable (orchestrator) for adjudication and synthesis. Each report states what ran.
## Amendments
(none yet)

### Amendment C7-a (section 7, post-hoc, appended 2026-11-21 01:32 UTC by the camera measurer; no mark, tolerance or field changed)
Operational choices and three development-only changes (synthetic whip blur, S1 whip/focal/labelling rules, S2 rebuilt on segment trajectories) are in new-analysis-5/camera/PREREG_camera_v6.md (written 00:50-01:05 UTC before any tool output; amendments A1-A3 written after dev clips d58-d60 only, before any test clip or real video was run). Reason: dev clips showed phase correlation and per-pair layering failing on whip pans and slow parallax.
