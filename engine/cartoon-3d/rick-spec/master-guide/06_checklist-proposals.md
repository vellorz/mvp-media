# Proposed corrections to the cartoon checklist (FOR OWNER APPROVAL — not applied)
Nothing here has been written to the live checklist (mvp-media engine/cartoon-3d/CHECKLIST.md, DETAIL_STANDARD.md, memory checklist files) or to the scheduled task prompts. Reply with the numbers you approve (e.g. "approve 172-188, 190") and a later thread will apply them. Each item cites the guide rule and the Rick evidence it comes from.

## New rules (172-191)
Numbered after the live checklist, which ends at rule 171 (rules 153-171 were added by the Salzburg thread on Nov 17). Live rule 170 says the owner gives direction separately on Dresden voice, music, Rick likeness, transitions and pacing; these proposals are that direction.
172. **Rick Master Guide is the build spec.** Every cartoon short is planned from research/rick-style-spec/rick-master-guide.md, and the 16-item pre-render checklist (phase4/04_rubric-and-test.md section D) must be all YES before a 2K render. (Guide k)
173. **Script template.** Hook = strange act or impossible rule in sentence 1, from t = 0; then "You see," world rule; a doubter with one quoted mocking line; 2-3 escalations with time markers; reveal at 50-85 % of runtime; payoff on the last word. (Guide a1, a3, g; 20/20 transcripts)
174. **No date-first or place-first openings, no "did you know".** Dates live inside the story. (20/20)
175. **Roles, not names.** "A young priest", "the king"; a real name at most once. (Rick never names; Dresden/Salzburg used 3 names)
176. **1-4 concrete numbers per script, never a list of statistics.** (Rick #03 "39 ft", #02 "15 minutes"; Dresden had 9)
177. **No "[place], on your wall" tag line or any CTA.** The last line is the payoff. (19/19 Rick endings)
178. **Poster ending [derived].** The poster appears inside the payoff scene as an in-world object (framed on the wall of the final room, a shop window, a station board). The final camera move lands on it with the whole poster visible, while the last line is spoken. The video ends ≤ 1.2 s after the last word starts. (Rick ending rule + owner "whole poster visible")
179. **VO pace.** 3.4-4.1 words/s (target 3.75, ≈ 225 words per 60 s); trim pauses so ≤ 3 gaps exceed 0.8 s and none exceeds 1.2 s; measure with faster-whisper word times before building scenes. (20/20; ours 2.5-2.7)
180. **Join grammar.** Every join is a dissolve of 4-14 f (default 6-12 f; 10-12 f for quiet/night stories, 6-8 f for busy/comic) or a fast join ≤ 3 f (push-through, FG wipe, punchline cut), with at most 5 fast joins. Never one fixed length for every join. (241/248 unseen; ours all 5 f)
181. **Bridge objects.** At least half the dissolves put a matching shape at the same screen spot (±5 %); each join sits on a phrase onset; both shots moving. (#10 14/17, #14 ≈ 10/18)
182. **Camera never stops.** No static camera over 1.5 s (Rick's longest still run is 7 f); preview motion median ≥ 4.5 (scripts/metrics.py "diff"). (19/19; ours 2.5-3.3, still runs 35-36 f)
183. **Camera hits on nouns.** Eased moves arrive on the spoken noun within ±3 f; one crash push of about 9 f on the key word of the climax. (#14 f1419-1427)
184. **Character construction.** Our own characters, but built Rick's way: flat drawn round head with a dark monoline outline 6-10 px @1080 in MS (≈ 2.5 % of head width), simple bean/stick body, one costume cue, drawn face; head 30-39 % W in MS. No shaded 3D figurine heads. Characters still sit in lit 3D sets with contact shadows. (101/101 sampled Rick frames; replaces the 3D-doll look of Dresden/Salzburg)
185. **Faces act.** A face change every 0.3-2 s on screen; ≥ 10 distinct expressions per video; blinks 1-3 f; reaction cascades staggered 2-7 f; lips move only on quoted lines. (10/10 logs)
186. **Caption spec.** Heavy rounded sans (Montserrat Black), white #FFFFFF, black outline 4-6 px @1080 (5-8 px @1440), shadow +3 px; cap height 2.8 % H (54 px @1920, 72 px @2560); box bottom at 71.7 % H; centred; 1-3 words; numerals as digits; hard swap 0-3 f before the word; tracking 0, single line; above every dissolve. (19/19 videos)
187. **Grade window.** Mean luma 0.33-0.56, saturation 0.37-0.66, p2 ≥ 0.05 (no crushed blacks), p98 ≥ 0.84; palette flips across each time/mood join. (19/19; Salzburg p2 0.004, p98 0.67)
188. **Mix and music.** Mix −14 LUFS, −2 dBTP, LRA ≤ 3.2; light plucked/mallet loop with a soft pulse, 80-160 BPM, constant ≈ 20 dB under the VO from frame 0 to the end, no ducking or swells; SFX 8-12 dB over the bed on moves, impacts and the payoff. (19/19 loudness, 5/5 stems)
189. **Facts in-world.** Facts appear on in-world props (signs, certificates, boards, labels), never as overlays, arrows or date cards (agrees with existing rule 6A). (#10 f1208-1244; 19/19 grids)
190. **Rubric gate.** Before Gate 2, run scripts/metrics.py, transitions.py, dissolve_curve.py and captions.py on the preview and report the 14 dimension scores next to Rick's pass lines; any dimension below its pass line is fixed before Gate 2. (phase4)
191. **Dynamic angles.** Use at least 4 of: low angle, high angle, top-down, macro/ECU of the hero prop, through-object framing, orbit, per video; no row of characters facing the camera in a frontal stage shot. (Rick grids; ours frontal)

## Changes to existing rules (conflicts where Rick wins)
- **Rule 137 / "Chicago v21 = transition benchmark" (Nov 14)** → replace the benchmark with Rick's measured grammar (rules 180-181). Chicago v21 stays a good example only where it matches.
- **DETAIL_STANDARD saturation 0.40-0.48** → widen to 0.37-0.66 (rule 187). Rick's own videos run 0.376-0.653 on the same per-frame HSV mean.
- **DETAIL_STANDARD "head ≥ 18 % of frame width in medium shots"** → 30-39 % in MS (rule 184). Rick measured 30-39 % in both primaries.
- **DETAIL_STANDARD "face change every 8-15 frames"** → every 0.3-2 s with bursts (rule 185). 8-15 f matches #14's busy scenes but not #10's calm ones.
- **Rule 134 "max ~4 s hold"** → keep for shot length, and add rule 182 (camera never still > 1.5 s).
- **VO tags (mvp-vo-delivery-tags)** → keep, and add rule 179's pace and pause limits. The Salzburg failure was pace and pauses as well as tags.
- **Existing caption settings in the engine** → replace with rule 186 (current output is 11-22 % too big and too wide).
- **Poster outro card ("X, on your wall")** → replace with rule 178.

## Open question for the owner
- Rule 178 (poster ending) has no Rick precedent, because Rick sells nothing. The guide derives it from his ending rule. If you prefer a dedicated 1-2 s poster beat after the payoff, say so; it would be the one place we knowingly differ from Rick.
