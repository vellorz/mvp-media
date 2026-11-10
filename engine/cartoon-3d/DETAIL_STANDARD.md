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
| Hard cuts | 1 | 2-4 | <= 2 |
| Shots | 27 in 65 s | ~14-18 | 22-28 per 60-70 s |
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
Q6. Transition census: list every shot change with its recipe (T1-T7); more than 2 hard cuts or more than half plain dissolves = rework.
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
