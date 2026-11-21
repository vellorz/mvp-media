# Loop 4: motion by named action, body mechanics, asset physics (definitions v6 sections 3 to 6), 2026-11-21
Inputs: inventory/REPORT.md; 300 blind packs (176 action items a001-a176, 124 asset items s001-s124; seed 2026112103); labels in motion/out/ (A_*.jsonl pass A on full+crop sheets; B_*.jsonl pass B on full+crop+difference sheets; C_disputed_actions.jsonl third pass on 34 disputed actions); scoring scripts and tables in motion/an/ (analyze_actions.py, analyze_assets.py, inference_test.py, action_table.json, asset_table.json, inference_test.json). Models: Opus built packs; Sonnet (nine to eleven separate agents) did all labelling; orchestrator scored.
## Agreement, actions (176 items; A vs B; one primary action per item)
| field | A vs B | status |
|---|---|---|
| start within 2 f | 94.3 % (within 1 f 87.5, within 3 f 95.5) | GUIDANCE (near rule; not 99) |
| end within 2 f | 84.7 % (within 3 f 89.8) | GUIDANCE |
| start AND end within 2 f | 80.7 % (142 of 176) | GUIDANCE |
| travel within 2 f | 79.5 % | GUIDANCE |
| action word identical | 58.0 % | UNCERTAIN |
| easing class | 68.2 % | UNCERTAIN |
| construction (2D cutout / rigged / tweened) | 78.4 % | GUIDANCE |
| squash and stretch yes/no | 92.6 % | GUIDANCE |
| anticipation yes/no | 97.2 % | GUIDANCE |
| overshoot yes/no | 94.9 % | GUIDANCE |
| feet move yes/no | 94.9 %; hair 85.8 %; clothing 46.0 % | GUIDANCE (feet, hair), UNCERTAIN (clothing) |
| limb set exact / Jaccard 0.5 or more | 39.2 % / 91.5 % | UNCERTAIN (exact), GUIDANCE (overlap) |
| arm curvature within 0.1 (n 101 both gave it) | 89.1 % | GUIDANCE |
| joint angles within 15 degrees | neck 4/4, hip 5/7, knee 3/5, ankle 0 | too few pairs: UNCERTAIN |
| stride length (2 pairs), cadence (7 pairs, 3 within 1 f), loop length (6 pairs, 3 within 2 f) | | UNCERTAIN, not measurable from these strips |
Consensus (two of three within 2 f): 164 of 176 items (22 only through labeller C, whose first 16 items were labelled from memory: lower trust). The action word versus the first-measurer log matches only 34 % (A 34.1, B 33.0): the labellers and the old logs use different words (see inventory), so use the old inventory counts for "how often" and these tables for "how long".
## Per-action timing (consensus items, frames and ms; window cap of 48 f means p90 47 is a cap, not a measurement)
| action (log word) | n | travel median f (p10 to p90) | ms | easing (most common) | construction | limbs |
|---|---|---|---|---|---|---|
| lift | 12 | 6.0 (4.5 to 18) | 200 | ease-out | 2D cutout | lower arm, hand, head |
| turn | 11 | 4.5 (3.5 to 7.5) | 150 | linear | 2D cutout | head, torso |
| talk | 11 | 7.5 (3.5 to 46.5) | 250 | ease-out | 2D cutout | head, lower arm, hand |
| react | 11 | 5.0 (4.5 to 14) | 167 | ease-out | 2D cutout | head, torso, lower arm |
| stand | 10 | 7.25 (3 to 11) | 242 | ease-out | 2D cutout | head, torso, leg |
| emote | 9 | 7.0 (4 to 47) | 233 | ease-out | 2D cutout | arm, head |
| point | 9 | 5.0 (3 to 24) | 167 | ease-out | 2D cutout | lower arm, hand |
| hold | 9 | window-capped | | linear | 2D cutout | head, torso |
| walk | 8 | 14.0 (4 to 47) | 467 | linear | 2D cutout | head, leg, torso |
| pull | 8 | 9.0 (5 to 47) | 300 | linear | 2D cutout | head, upper arm |
| fall | 7 | 10.5 (7.5 to 20.5) | 350 | ease-in | 2D cutout | leg, torso, upper arm |
| throw | 6 | 8.0 (4 to 13) | 267 | ease-in (anticipation yes in 6 of 6 labels) | 2D cutout | upper arm, hand |
| recoil | 4 | 9.75 (1 to 14.5) | 325 | snap | 2D cutout | head, clothing, torso |
| sit | 3 | 6.5 | 217 | ease-out | 2D cutout | head, torso, leg |
| drop | 3 | 13.5 (7 to 17.5) | 450 | ease-in | 2D cutout | lower arm, hand |
| push (n 2) | | 13.5 | 450 | ease-in-out | tweened | upper arm, hand |
| catch (n 2) | | 3.25 | 108 | ease-out | 2D cutout | arm, hand |
| run, stumble, carry (n 1 each) | | 47 (cap), 12, 14.5 | | | 2D cutout | |
Everything is "2D cutout" in the labellers' reading (rigid card parts); squash and stretch appears in 0 to 3 labels per action, no action shows it consistently; anticipation shows consistently only for throw. These per-action rows are GUIDANCE for items where two labellers agreed (n small for most rows).
## Assets (124 items; A vs B)
Start and end both within 2 f 65.3 % (within 3 f 73.4, 4 f 77.4): UNCERTAIN at 2 f, GUIDANCE only at +-4 f (post-hoc window). Start alone within 2 f 88.7 %, end alone 71.0 %. Easing 66.9 % UNCERTAIN; asset type 79.0 % GUIDANCE; behaviour overlap 93.5 % GUIDANCE; bounce count equal 96.0 %; parallax class 81.5 %; "animated on ones" yes/no 87.1 % (A 115 yes, B 99 yes; the rule-grade fact stays from loop 2).
Numbers: gravity (only 6 of 124 items had values from both labellers: pairs 1.7/0.8, 3/3, 19/14, 7/7, 5/5.5, 2.5/3 screen heights per s^2; the earlier tool value 4.7 to 5.1 stays the reference), rotation (9 pairs, 3 within 15 degrees), scale pops (4 pairs, 2 within 10 %): UNCERTAIN, too few measurable cases. Bounces: 9 items (7 in video 24, 1 in 12, 1 in 04); bounce is rare outside one video.
Duration of consensus behaviours (frames median, p10 to p90; 47 is the cap): drifts 28.5 (10 to 47), particle bursts 14.25 (8 to 47), falls 12.5 (8 to 39; ease-in in 13 of 20), rotates 9.5 (5 to 31), slides 19.25, drives 47+, flows 29, loops 38, sways 25 (ease-in-out in 4 of 6), scale pop 3 items only. GUIDANCE where n is 14 or more, otherwise small-n values.
## Inference test (definitions v6 section 6): hide 10 observed actions, predict from others (seed 2026112102)
Predicting travel from the five nearest other-word consensus items (limb overlap): travel within +-3 f or 30 %: 7 of 10 (70 %); easing class: 3 of 10 (30 %); limb set exact: 7 of 10 (70 %). So an analogy recipe gives a usable duration and limb set about 70 % of the time and a wrong easing class most of the time: [INFERRED] recipes carry durations and limb sets; easing is a coin flip.
## Disclosures
Labellers lost image context repeatedly ("media removed" in their transcripts); several labelled from notes or memory, listed in each agent's final note: heavy among A a001-a030 and a089-a095, B a176-a175 and a088-a086, B s084/s083/s021, and 16 of C's 34. Windows are capped at 48 frames (53 items). The labellers could not see parallax-free backgrounds, so diff sheets show background edges on camera moves. Joint angles, stride, cadence, loop length and most asset numbers could not be read from the strips for most items (null): the question "how do joints and strides look" stays mostly unanswered; only arm curvature (101 pairs) and the coarse yes/no fields are measured. Asset physics extends only to behaviour classes and durations.
