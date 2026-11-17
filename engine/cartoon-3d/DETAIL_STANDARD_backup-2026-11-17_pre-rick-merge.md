# Detail standard for cartoon-3d shorts (from the Nov 10 2026 reference teardown)

Owner, Nov 10 2026: "These videos are way more detailed than ours, so I want ours to become as detailed as theirs."
Source: frame-by-frame study of one 65 s reference short (private; full notes and frame sheets live only in the project folder
research/reference-teardown-dragon/, never in this public repo). Style lessons only: never copy its story, characters, shots or name it.
Read this file together with CHECKLIST.md before building any short. Numbers marked (1 video) come from this one study and should be
re-checked when more references are studied; numbers marked (consistent) also matched the earlier 5-video study.

## A. Targets, measured the same way on every render
Run `python3 engine/cartoon-3d/render/detail_metrics.py <video.mp4>` on the finished render and on stills while building.
| Metric | Reference | Our week-03 average | Target for new shorts |
|---|---|---|---|
| Frame-to-frame change, median | 7.0 | 2.9 | >= 5.0 |
| Edge density (drawn detail) | 34.6 % | 26 % | >= 32 %, and NOT from repeated tiles |
| Mean saturation | 0.41 | 0.59 | 0.40-0.48 |
| Hard cuts | 1 (0 in the second reference) | 2-4 | <= 1 |
| Shots | 27 in 65 s (19 in 59.5 s in the second) | ~14-18 | 19-28 per 60-70 s, see G2 |
| Distinct sets | 12 | 4-6 | >= 8 |
| Insert close-ups of objects | 6 | 0-1 | >= 5 |
| Props per wide shot | 25-30 | ~6 | >= 20 |

## B. Design rules
D1. SET DRESSING (1 video). Every wide or medium shot has at least 20 distinct props; every close-up at least 6. Write the prop list for each set
    in the shot plan BEFORE building. A set is never "a building on bare ground". Period-true props for the poster's place and year.
D2. THREE LAYERS (consistent). Every shot has a foreground object cut by the frame edge and out of focus (branch, banner, railing, lamp post,
    crate, shoulder), the acting plane, and a detailed far background (skyline, hills, street continuing). No shot is subject + flat sky.
D3. NO REPEATED TILES (1 video). Walls, roofs, roads and floors are drawn with variation: block sizes vary, some chipped/cracked/stained,
    windows differ (open, shuttered, curtain, flower box, lit, a person in one). No more than 3 identical neighbours anywhere.
D4. GROUND IS NEVER EMPTY. Roads have ruts, puddles, tufts, stones, droppings, litter of the period; lawns have flowers, paths, patches;
    floors have a carpet/pattern/planks with wear. The lower third of the frame (around the caption) must hold drawn detail.
D5. VISIBLE LIGHT SOURCES (1 video). Each set shows its light: sun disc with rays, moon with halo, lamps, candles, fires, lit windows.
    Each source throws a warm pool onto nearby surfaces and a soft glow. At least 2 sources in every interior and every night shot.
D6. SCENE PALETTES (1 video). Each set gets one dominant temperature plus one accent colour, greyed mid-tones, saturation only on accents.
    No pure #0000ff-type sky or uniform orange ground. Character skin and clothes are tinted by the scene light (lilac at night, pink at dusk).
    At least 4 lighting moods per short (e.g. noon, golden, night, interior lamp light); revisit a main set at a different time of day.
D7. CHARACTER SIZE (consistent). In medium shots the head is 18-22 % of frame width and the body runs out of the bottom of frame.
    Characters are small only in deliberate extreme wides, which last under 3 s unless the camera is travelling.
D8. ACTING (1 video). In any shot where a character is the subject: a new face every 8-15 frames while speaking or reacting, a blink every
    0.5-2 s, one clear gesture on the key word of each sentence, and a body reaction (lean, squash, sweat drop, jump). Background people
    react too and change expression when the mood turns.
D9. SHOW THE MECHANISM, DON'T LABEL IT (owner decision 2A). Explain with the object itself: cutaway, x-ray, cross-section, or camera inside
    the machine. NO overlay arrows, NO date cards/calendars on easels, NO diagram labels. Years and numbers live in the narration and captions,
    or on an object that would really carry them in that place (a carved cornerstone, a newspaper, a shop sign).
D10. ONE EXTRA GAG PER SET (1 video). A small true-to-period visual joke or life detail not in the narration (animal, mishap, time-passing
    cue like a cobweb). Never one that contradicts the facts.
D11. HERO PROP IN TRUE 3D (1 video). The 1-3 objects the story is about are modelled with real volume, a bump/pattern texture and
    highlights, and get an extreme close-up within the first 2 s and again at the payoff.
D12. PARTICLES. Interiors: floating dust motes. Impacts: dust puff + 2-3 scattering birds/leaves. Fires: sparks. Night: fireflies/stars.
    Keep them sparse and slow so QA does not read them as flicker.
D13. SCALE CONTRAST. Never two consecutive shots at the same scale. Alternate ECU / MS / wide; include one "how big" reveal (crowd, skyline).
D14. Existing brand rules still win: poster whole at the end, captions style, no logos/real people, checklist rules 1-50.

## C. Camera and transition recipes (frames at 30 fps)
T1. PUSH-TO-DETAIL: 10 f smootherstep from MS to ECU of the hero prop, motion blur on the middle 2-3 f. Use inside the first second.
T2. WHIP ARC inside one set: 16-28 f, blur on the middle third, 3-4 f overshoot settle. Camera travels past a foreground prop. Check
    rule 35/47 (nothing blocks the lens) on every frame of the move.
T3. CROSS-DISSOLVE at place/time jumps: 4-6 f, begins 2-4 f before the first word of the new sentence, both shots keep moving through it.
    Props of the incoming shot exist from its first blended frame (rule 46).
T4. MATCH-MOVE DOOR: fill the frame with an object (cup, cloud, window, poster, wall), then pull out of / pass through it into the next
    scene. At least 2 per short. Best one goes to the final pivot into our poster.
T5. CRANE REVEAL: start on a face, rise over the head to reveal the big thing, come back down. 3-4 s. Once per short.
T6. TIME-OF-DAY DISSOLVE on a locked composition (same set, new light) for "weeks later / that night / next morning".
T7. SNAP CUT: at most one or two hard cuts, used only to snap back to a speaker for a punch line.
T8. NO STATIC HOLDS: every shot has a creep (0.15-0.35 %/f) or drift; long shots (4-6 s) are continuous orbits/pull-backs that keep
    revealing new props.
T9. WORD SYNC: the physical event lands on the frame of its word (ball drops on "dropped"); emphasis words get a camera kick, speed
    lines or a face change within +-2 f.

## D. Asset requirements per short (build these before layout)
- Set sheet: >= 8 sets, each with palette (dominant, accent, shadow tint), light sources, >= 20 named props, foreground object, far background.
- Surface library drawn with variation: stone/brick/wood/plaster/road/grass/water for the period; no single tile repeated over a facade.
- Hero prop(s) in 3D with texture + ECU-ready detail.
- Face library per main character: >= 12 expressions incl. talk shapes, laugh, shock, smug, sad, sleep; per-scene skin tint.
- Extras: >= 3 distinct background characters per populated set, each with 2 moods.
- FX cards: dust motes, dust puff, glow/light pool, sun rays, sparks, sweat drop, speed lines, ZZZ, birds.

## E. QA checks added to the pre-render routine (after CHECKLIST rules 1-50)
Q1. Run detail_metrics.py: all Section A targets met, or the miss is explained in the Gate 2 note.
Q2. Stills sheet of every shot: count props (>= 20 wide / >= 6 close), confirm 3 layers, a visible light source, and that the lower third is not bare.
Q3. Tile check: no facade/ground with more than 3 identical neighbouring elements.
Q4. Character-size check on every MS: head >= 18 % of frame width.
Q5. Acting check: step through each character shot at 2 f intervals; fewer than 2 face changes per second = fix.
Q6. Transition census: list every shot change with its recipe (T1-T19); more than 1 hard cut, or more than 2 dissolves without a bridge object (T10), = rework.
Q7. Saturation check per set: mean saturation 0.40-0.48; any large flat pure-colour area (sky, ground) = repaint.
Q8. More props means more z-fight risk: re-run rule 43 (grass/ground flicker routine) and the heat-map scrub after dressing each set.

## F. Owner decisions, Nov 10 2026 (answered with side-by-side pictures; these override anything softer above)
1A. Set dressing at full reference density: >= 20 props per wide shot, >= 6 per close-up. Not a reduced version.
2A. No arrows and no date cards. Show the mechanism instead (rule D9). This retires the calendar-on-easel device used in week 03;
    checklist rules about easels/calendars/diagram arrows now only matter if the owner asks for one again.
3A. Greyed scene palettes like the reference (rule D6, saturation 0.40-0.48), not the old vivid pure-colour look.
4A. Characters big and constantly acting (rules D7, D8), not a calmer version.
5A. Small invented sight gags are allowed (rule D10) as long as they never change or contradict the facts of the story.
6A. BACKDROPS ARE HAND-DRAWN FLAT ART. Build each set as illustrated artwork (Canvas2D paintings with their own ink lines, drawn
    with variation) placed on flat cards and simple boxes at several depths so the camera gets parallax: far card (skyline/hills), mid
    cards (facades, walls), near cards (props, foreground). True 3D geometry is kept for the 1-3 hero props and for anything the camera
    must orbit or fly through. No more procedurally tiled 3D buildings. How the reference builds its sets is inferred, not confirmed,
    so the first short made this way goes to Gate 2 with a note on what worked and what did not.
    Engineering cautions: stagger cards >= 0.25 m apart in depth (z-fight), keep world ink off painted cards (NOINK layer, they carry
    their own lines), paint at >= 2x the on-screen size of the closest camera so close-ups stay sharp, and plan camera moves so a card
    is never seen edge-on.

## G. Second teardown, Nov 11 2026 (night-story reference, 59.5 s, every one of its 1,785 frames logged)
Private notes and frame logs: project folder `research/reference-teardown-bell/`. No reference frames in this repo.
What both teardowns agree on is a RULE. What only one does is a CHOICE that depends on the story.

### G1. Consistent across both references (treat as rules)
| Item | Day story (first teardown) | Night story (this one) | Rule for us |
|---|---|---|---|
| Frame-to-frame change, median | 7.0 | 7.1 | >= 5.0 stays the floor, 7.0 is the goal |
| Hard cuts | 1 | 0 | <= 1. Replaces "<= 2" in section A |
| Still frames | under 1 % | 0.4 % | no frozen frame anywhere |
| Opening | in motion on frame 1 | in motion on frame 1, no cut for 3.4 s | cold open inside a camera move, no title |
| Ending | on the last word | 16 frames after the last word starts, held smirk, hard stop | no outro, no fade, no call to action |
| Words per second | about 3.7 | 3.7 | unchanged |
| Loudness | | -14.0 LUFS, range 2.3 LU, peak -1.9 dBFS | -14 LUFS, range <= 3 LU |
| Character acting | pose-to-pose | pose-to-pose | G3 below |

### G2. Depends on the story (choose per short, say which in the Gate 2 note)
- Transition family. CORRECTED Nov 11 after the every-frame pass of the day story (section H): both references are carried by
  bridged cross-dissolves (T10). The day story has 1 hard cut, 2 joins made by a camera move inside one set, and about 18 shape-matched
  dissolves of 4-8 f; no whip pan was found. So bridged dissolves are the default for every short. Whips (T2) stay allowed inside one
  set but are not what the reference does. Dissolve length is the story choice: 4-8 f for a busy or comic story, 7-12 f for a quiet one.
- Shot count. 22 takes in 65 s (day; 27 when its long takes are split by subject) against 19 in 59.5 s (night). The night story has four one-take shots of 5-8.5 s that visit
  3-5 subjects each. Target is now 19-28 shots, and a shot longer than 4 s must visit at least 3 subjects.
- Saturation and edge density. Day 0.41 / 34.6 %. Night 0.52 / 28.1 %. Night scenes are two-colour pictures: a deep blue-violet world
  (about #1B2A9E to #3B2FA8) plus ONE warm emitter (about #FFC463 to #F5A03C). Section A saturation 0.40-0.48 applies to daylight sets.
  Night sets are allowed 0.48-0.55 when the picture is the blue + one warm source scheme, and edge density >= 28 %.
- Depth of field. Outdoors everything is sharp. Indoors at night the background is blurred and focus is pulled between subjects in 4-7 f.

### G3. Character acting (measured)
- Face and pose changes are single-frame swaps, held 6-16 f. No in-between drawings and no motion blur on characters, even on a jump.
- One payoff expression per short may get 4 in-between frames. Everything else pops.
- Blinks last 2-3 f and sit on or just before a pose change, which hides the swap.
- Anticipation is the only part that ramps: crouch 8 f, jump 2 f, hang 2 f, land. Dig: raise 2 f, contact 1 f, squash 1 f, pop 3 f,
  overshoot to about 130 % for 1 f, settle with two small bobs over 8 f.
- Deadpan contrast: in a two-character shot one acts every 1-2 f while the other is frozen except blinks and eye darts.
- Background characters react 1-2 f AFTER the lead's line, never on the same frame.
- A quoted in-world phrase may be mouthed by the character (5 mouth shapes, each held 2-7 f, starting 3-4 f after the word).
- Character outline is about twice the weight of the set outline (about 6-8 px against 3-4 px at 1080 wide), fills are flat.
  The scene's colour grade tints the card (skin goes lilac at night); the card is never left in its daylight colours.

### G4. Dissolve-family recipes (frames at 30 fps)
T10. BRIDGED DISSOLVE. 7-12 f, linear. Both cameras are already moving: the incoming shot starts its move 10 f before it is visible.
     One bridge object sits at the same screen position in both shots (within about 2-10 % of frame width): bell to bell, head to head,
     shovel to shovel, held paper to the notice on a door, lit window to a face. Replaces T3's "4-6 f" for this family.
     A dissolve with no bridge object is allowed at most twice per short.
T11. REALITY SWAP. Match-dissolve on a locked hero prop (7 f), hold 10 f, then pull back 24 f to show the prop now sits in a
     different world (a model on a table, a picture on a wall).
T12. FOLLOW THE LINE. A bright cord, pipe, rope or road stays in frame and the camera travels along it from subject A to subject B
     in about 36 f (ease in 3, ease out 7).
T13. THROUGH THE GLASS. Accelerating push at a window (1.5 to 4 % per frame). The next scene fades up inside the panes first, then
     fills the frame. Or fly through the sash with 4 f of blur and bring a new foreground prop in from the edge within 2 f.
T14. INSERT TO REVEAL. Start on a document or small prop filling 98 % of the width, pull straight back with ease-out for about 26 f
     until the whole situation is in frame.
T15. ORDERED EDGE REVEAL. One pull-back of about 40 f in which story items cross the frame edge one at a time, 2-5 f apart, in the
     order the narration needs them.
T16. PARK, THEN DISSOLVE. Empty the frame of characters, hold 18 f on one prop during a narration pause, then T10 on that prop.
T17. POINTING ONE-TAKE. One room, the camera trucks between 3 subjects, each arrival lands on its noun, focus pulled 3-5 f ahead.
T18. STILLNESS BEAT. Hold dead still for 10 f on a one-word line ("Wait."), then an accelerating push to an extreme close-up of
     the clue. Legible hand-written detail in the texture at 2x so the push pays off.
T19. GRADE RAMP. Time passing = the whole picture changes colour over about 17 f on a locked wide, starting on the time word.
     Same room, two paint sets (night and day) also serves as a flashback with no caption.

### G5. Light and effects (measured)
- Every night shot has a visible warm emitter (window, candle, lantern, stove, doorway) with a soft halo and a glow pool on the
  ground. Lights switch on as the event of a wide shot: each ramps over 3 f, near to far, 1-2 f apart.
- The warm source may leave the frame during a move so the picture turns single-colour just before a reveal.
- A fixed light shaft (soft additive quad from a window) crosses props and later the character's eyes. Use it to tag the clue.
- During a push-in, darken everything except the destination.
- Impacts leave fallout: 8-30 particles with gravity plus one puff that grows for 8 f and fades over 18 f. The fallout keeps
  falling through the next action.
- Pendulum props: 1 f kick, peak in 2 f, then damped swings (35, 30, 20, 10, 5 degrees, about 9 f per half swing).
- A static hold gets one small independent mover: a bird, chimney smoke, falling snow in two sizes.

### G6. Timing against the voice (measured over about 150 word events)
- Picture event lands 0 to +1 f from the noun it shows. Camera moves start on a word. Background lights lead by 2-6 f.
- First picture change after a sentence break may lead the word by 2-3 f.
- Sound effects sit in the gaps between words. The music bed is about 20-28 dB under the voice (estimate). The story's own sound
  (here a bell) returns in the last ten seconds.

### G7. In-world documents instead of overlays (supports owner decision 2A)
Every fact that we used to put on a card is a drawn object in the scene: a nameplate with dates, a certificate with typeset text and
a stamp, a notice nailed to a door, tally marks and chalk dates on a wall, a price tag on a shovel. Text is real type, readable at the
closest camera, and present in the set from the first frame.

### G8. Output size and quality (owner, Nov 10: bigger frames, larger files)
- The reference copies are 1080x1920, 30 fps, 4.6-5.2 Mbps (35-43 MB): that is the platform's re-encode, not the maker's master.
- Our week-03 files were already 1080x1920 at 7.7-10.6 Mbps (69-100 MB). So file size was never the gap; drawn detail per frame is.
- From the next short the master is 2K: 1440x2560, 30 fps, H.264 High, `--scale 1.3333 --crf 16`, audio AAC 320 kbps 48 kHz.
  Expect about 130-250 MB per minute and roughly 1.8x the render time (estimate). Every pixel-sized post value scales with height / 1920.
- Schedule the 2K master wherever the platform and tool accept it. A reduced copy is made only when an upload path has a size cap,
  and it is never below 1080x1920 at 8 Mbps unless the cap forces it. Say in the Gate 2 note which file went where.
- Paint textures, documents and character cards at 2x the size they reach in the closest 2K camera.

### G9. Note on owner decision 6A (flat backdrops)
The night-story reference shows true perspective change on houses, rooms, posts and windows during orbits and push-throughs, so its
sets are simple 3D shapes carrying hand-drawn textures, with flat 2D characters. That fits 6A as written (flat art on cards and simple
boxes, real 3D where the camera orbits or flies through). In practice: any room the camera trucks across, and any building the
camera pushes into, is a box set with painted walls, not a single card.

### G10. QA checks added
Q9.  Transition census names the family (G2) and the bridge object of every dissolve; more than 2 unbridged dissolves = rework.
Q10. Step every character shot frame by frame: any tweened face, or motion blur on a character = fix (G3).
Q11. Every night shot: one warm emitter visible, halo and ground pool present, card tinted by the grade.
Q12. Word-sync table for at least 20 events: picture within 0 to +1 f of its noun.
Q13. First frame is already moving; last frame is within 20 f of the last word's start; no fade.
Q14. ffprobe the master: 1440x2560, 30 fps, and report size and bitrate in the Gate 2 note.

## H. Every-frame pass of the first reference (day story, all 1,945 frames logged Nov 11 2026)
The first teardown looked at every 6th frame. This pass logged every frame and corrects or adds the following. Logs: project folder
`research/reference-teardown-dragon/frame-logs/`.

### H1. Corrections to sections A-C
- 22 takes, 21 shot changes: 1 hard cut (at 3.1 s, inside the hook), 2 camera-move joins, about 18 shape-matched dissolves of 4-8 f.
  T2 (whip arc) and T7 (snap cut) are optional devices, not reference practice. T10 is the default.
- The bridge can be a SHAPE, not only the same object: round head to head cluster, throne arch to gate arch, sun disc to jar dome,
  sun to moon, dust plume to an interior of the same orange, lawn crack to street crack. Same screen zone, within about 5 % of frame.
- Before a dissolve the camera travels to the bridge shape and parks on it for about 4 f, or fills the frame with it (28 f tilt
  into a dust plume), and only then mixes.
- The caption layer sits above both shots and never fades. Captions change 0-6 f before the word (median 2), never after.
- Sets are real 3D rooms and props with painted textures; people are flat cards. Same finding as G9.
- Ending: hard stop 7 f after the last word starts, mid-move, no fade.

### H2. New recipes
T20. ZOOM PUNCH. 4 f accelerating push with radial blur into a 3D hero prop, then 6 f ease-out on the close-up. Used at 0.7 s.
T21. CRASH ZOOM. About 2.7x in 10 f, ease in-out, no blur, landing on the noun. Near cards slide out of frame by parallax.
T22. OBJECT TOUR. One descend + orbit + tilt around the 3D hero prop; each named part is centred on the frame its word is spoken.
     The prop itself does not animate. Phases of a long move start within 1 f of a caption change.
T23. CRANE AND RETURN. Rise over the speaker to the big view, hold for exactly one caption (about 19 f), come back down for the
     punch line. Ease in 6 f, cruise 18 f, ease out 18 f. A pre-blurred foreground slab (10-25 % of width) gives the fastest parallax.
T24. HAND-OVER. Change speaker by pushing the camera past speaker 1 (who becomes a blurred foreground wipe) onto speaker 2 in 24 f,
     starting on the last word of line 1 and landing on the first word of line 2.
T25. SURGING PULL-BACK. One pull-back of about 95 f whose speed rises exactly when a story event needs more frame and idles between.
T26. GOING UNDERGROUND. Tilt down at 5-6 % per frame so a perspective street is swapped for a flat cut-away drawing, with the crack
     staying at the same x. A flare then climbs the crack at about 3.5 % of frame height per frame.
T27. OCCLUDER APPROACH. Bars or a gate close to the lens; a tiny card grows from 3 % to 36 % head width in 50 f by moving along z,
     with a bob every 2 f and a 2 f overshoot on arrival.

### H3. Showing ideas without overlays (supports owner decision 2A)
- A "what would happen" is a ghost: a flat 50 % opacity copy of the object with a dotted outline that performs the action in 11 f
  while the real object stays put.
- Time passing in one held shot is a stack of small cues staggered 2-5 f apart: passers-by as a smear, a cobweb line growing, a
  pigeon fading in on a head, stubble dots, the light shaft brightening, the grade cooling. No calendar, no text.
- Teach, then repeat: show the mechanism once in close-up, once wide, then all copies at once offset 1-3 f each.
- A state stays visible: a caught ball leaves a glowing mouth for the rest of the shot.
- Far-away destruction is 4 cheap parts: a rigid card rotating 90 degrees in 8 f, round dust puffs, a column of circles reaching
  the top of frame in 5 f, a dust band travelling toward camera over 12 f. Birds leave a tree 21 f after the first lean.

### H4. Acting and reaction details
- Emotion stack on one card, in this order: 1 f eye snap, sweat drop pops, card mirror-flips, white speed lines redrawn every frame
  for 12 f, 7 f camera push.
- Small event, big vocabulary: 3 f hang, 7 f accelerating fall with one smear frame, white dash ring for 8 f, a 1 f camera kick of
  3 %, reactions 1 f apart (bird, eyes, body), then sparkles and a slow feather to stretch the silence.
- Fixed chain constants, reused so the rhythm is recognised: anticipate 3 f, travel 8 f, settle 1 f, react 5 f later.
- Startle: swap to the new pose, 115 % scale and 7 % up for 1 f, settle over 4 f. Fright jump: up 7 % in 2 f, down in 2-3 f, plus
  a ground dust ring fading over 8 f.
- Laugh: blush, 2 f head tip back, mouth opens, body leans, crown or hat lags. Side characters join 1-4 f later, out of phase.
- Lips move only when the narration quotes speech: 3 mouth shapes on 2 f holds, bigger "o" on stressed vowels. Under plain
  narration the mouth stays shut.
- Pose and prop swaps are hidden in a blink or on the first frame of a dissolve. An arm may exist only for the frames it gestures.
- A walk toward camera on a locked shot: card grows about 0.45 % per frame, rocks 2 degrees per step, one incidental event (a
  kicked pebble) keeps a 2 s walk alive, and a carried light drags a glow pool on the ground.
- Light is tint and glow, not shading: per-card colour multiply, additive radial sprites at each light, ray wedges fanned from the sun.

### H5. Where the reference does NOT spend effort (so we need not either)
3D props never animate except the one moving part. A crowd or army is a static painting sold by a camera crane. Tears fade by
opacity. One-frame pops with no travel-in are accepted when they land on an impact frame. Small continuity slips pass at speed.
Spend the saved time on the bridges, the timing and the density.

### H6. QA checks added
Q15. Every dissolve: name the bridge shape and give its screen position in both shots; the caption layer is not inside the fade.
Q16. No lip movement under plain narration; lips only on quoted speech.
Q17. Each idea that used to need an overlay is listed with the device from H3 that replaced it.

