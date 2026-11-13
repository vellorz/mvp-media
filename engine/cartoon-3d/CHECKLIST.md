---
name: mvp-cartoon-checklist
description: Owner correction rules for cartoon-3d daily shorts (check every video before Gate 2 so corrections shrink)
metadata:
  type: feedback
  modified: 2026-11-08T22:56:39.766Z
---
Owner (Nov 8 2026) expects fewer corrections each round, so every correction becomes a rule. Check all of these on test stills before every full render:
1. Hats are drawn OVER brows/eyelashes (brows sit lower under a brim). Hats must sit on the head, not the forehead.
2. Props held by characters must be instantly readable and fit inside the card (no clipped rods/objects). Odd hats (fisherman) use a proper bucket hat.
3. Towns/cities look planned: houses never in roads, roads fully marked (dashes + edges), trees on lawns not pavement.
4. Never let the sight-line culler empty a shot (high aerials cull every house): exclude that shot's rays for the town, fill every block. Empty lawns = low quality.
11. Characters must be in frame: low camera looking slightly up, landmark whole behind them; check every still for people cut off or missing, signs half off-frame.
5. No zoom/push into a character's body on a narration beat; use a medium shot with the face.
6. Ink lines must not flicker in pans: inset end caps on abutting boxes (boxGeo capIn), keep the ink point-on-plane test.
7. Check crowd/bystander positions against every camera (no person 1 m from the lens).
8. Audio spec the owner approved: Drew VO, constant bed ~15-20 dB under, SFX under VO peaks, -14 LUFS. Don't let character noises spike.
9. Rick-style captions: 1-3 words, Montserrat 800 white with black stroke, lower third.
10. End on the poster shown whole (border + bottom text).
12. No sub-second shot flashes: when remapping/retiming, never start a segment inside an in-shot cut dissolve (CUT_X window); scrub every shot change frame by frame (owner caught a pier->bus->pier flash at 7 s, Nov 9).
**Why:** owner said "me having to correct you will decrease over time".
**How to apply:** go through this list on stills of every shot before each full render; add new corrections here.
Related: [[mvp-cartoon-3d-experiment]] [[mvp-poster-never-cropped]]

## Rules 13-24 (Eiffel review, Nov 9 2026)
13. Nothing floats. Every sign, calendar, table, prop and person must visibly rest on something (post, easel, wall, ground, held in hands) with a contact shadow. No free-floating pop-up cards (permit, calendar flips, code messages) in mid-air or mid-screen.
14. Hand-held big signs: no visible card/frame outline around the character's body; the sign is held by the hands.
15. Impact marks (hammer hits etc.) land exactly on the struck object.
16. Vary shots: not the same angle of the landmark over and over. Different environments, interiors, close-ups, low/high angles, moving cameras; a new place or angle at least every beat.
17. Landmarks must be detailed and well defined (lattice, levels, ornament), never a smooth low-detail shape.
18. Backgrounds never empty: fill with town, trees, people, props.
19. Props must read at first glance (e.g. a weather instrument = recognizable anemometer/barometer) and be attached correctly (a radio carried, never dragged on the floor).
20. Walking characters face their walk direction (side profile when walking sideways).
21. No stray lines on faces/hair (check hair partings, artifacts).
22. Costumes fit the role (a soldier looks like a soldier; no random clown colours).
23. Action scenes must show the action: painters touch the thing they paint, with brush contact and paint visible.
24. Text on any prop (letters, signs, boards) stays fully inside the prop's border: fit long words with measureText/maxWidth (owner, Nov 9: "MONSTROUS" spilled past the Eiffel letter edge). Small fixes: re-render only the affected frames and splice, don't redo the video.

## Rules 25-42 (Eiffel/Pisa/Chicago review, Nov 9-10 2026)
25. NO BLACK GLITCHES. Owner hates black streaks/flicker (ink z-fighting) on grass, ground, water, building floor lines, distant buildings. Coplanar or near-coplanar surfaces (lawn on ground, floor bands on walls, water vs wall end) must be offset/merged; scrub pans and pull-outs for ink shimmer on far geometry before render.
26. One landmark per scene: never two copies visible (e.g. two windows each showing the Eiffel Tower).
27. Wall props (calendars, posters) hang on a wall/nail/hook; no odd extra decorations (stray circles, hovering objects) on them.
28. Easels: legs stand BEHIND or beside the board, never drawn across the board face. Diagram lines (angles, leans) stay outside the drawn object they measure.
29. Tool actions touch their target: a shovel digs into soil, a chute/tube connects to its machine, a jack screw is under the beam it lifts, a lift mechanism attaches to what it lifts.
30. Hands hold props: glasses, bread, clipboards are gripped by a hand (no levitating props). Clipboards show a readable paper (lines of text), not hash marks.
31. Eyelashes/brows sit above the eye and under the hair; no stray lines across hair or forehead.
32. Caps: brim attached to the crown, clearly shaped like a cap peak. Women's hats must be recognizable period hats (bonnet, brimmed hat with band).
33. Crouching = clearly bent knees, lowered hips, back leaning; not stiff stick legs.
34. Stools/chairs/furniture must read as what they are (seat + legs). Furniture belongs indoors or in a believable place (no couch in the middle of a street).
35. Camera never passes through or is blocked by objects in a pan or dolly (posts, walls, beige boards). Check every frame of a move, not just the start/end.
36. Shop signs and lettering never crossed by building lines/trim.
37. Labels/signs that reiterate narration must be fully in frame while the line is spoken.
38. Diagram overlays (river-flow arrows) must not be covered by boats or props.
39. Small fixes: re-render only the named moments and splice; keep content and unmentioned parts unchanged.
40. SEATED people: show them SIDE-ON in profile with the seat drawn on the card (thighs level on the seat, shins straight down, soles flat on the floor, back against a visible chair back, hands on the desk), camera roughly perpendicular to their facing. Or hide the legs behind a table/couch front that is clearly in front. Never splayed legs, a chair in front of the body, or no seat.
41. (Nov 10 01:18) NO hair parting strokes and no brows drawn on hair, in every toon (pisa/eiffel/chicago fixed: hair counts as a brim, hair cut crown+0.27HH). Ground layers: never two road/paving quads at the same height (Pisa cobble vs slab both 0.035 flickered).
42. Side-profile heads (asym 0.12) look like the face juts out: owner dislikes. Owner approved (Nov 10) and wants BOTH varied: rounder head ("round") and 3/4 face ("q34") on side bodies (eiffel toon SideOpts head "round"/"q34"); show the owner a pose reference sheet before re-rendering a redesigned pose.
Engineering fixes found Nov 9 (apply in every new short): black flicker = (a) ground quads 2-6 mm apart (keep >= 2.5 cm between layers, contact blobs above the top layer), (b) window view planes overlapping at one depth (stagger each by 0.25 m), (c) facade bands flush with side walls (overhang 6 cm), (d) abutting water quads (overlap them). Awnings must be sight-line culled on their own. Toon additions: chicago cap/bonnet/kneel+crank/held props; pisa shovel+soil heap; eiffel+chicago bodySide "sit" (seat chair/crate) + cast sitSide().

## Rules 43-50 (Chicago review, Nov 10 2026)
43. GRASS FLICKER ROUTINE (owner: "make this a routine ... without me having to tell you"): grass/lawn glitched in nearly every grass shot (0:07, 0:26-0:42, 0:45-0:48, 0:53-0:55). Before every render, automatically: list every grass/lawn/ground quad and confirm >= 2.5 cm vertical gap from every other ground layer, no lawn coplanar with road/sidewalk/curb tops, polygonOffset on ground layers, and scrub every grass shot (pans/dollies) frame by frame (frame-diff ink-only pass) for shimmer. Never wait for the owner to report it.
44. Jack screws must be physically under the building's beam/sill (screw head touching the timber), visibly connected; a worker kneeling beside a free-standing screw is wrong.
45. Shovels dig INTO ground/soil heaps (blade buried, soil at the blade); never shoveling air.
46. Set props (easels, signs) must exist from the first frame of a scene cut; no prop popping in ~0.5 s after the cut (check cut + dissolve frames).
47. Camera moves into a scene must not pass through/behind building ledges, cornices or wall bands near the lens; check the first 2 s of every entry move. Ink lines of near geometry must not stripe the frame.
48. Seated side bodies: chair back must stay behind the torso and below the head (never crossing the face).
49. Held clipboards sit at chest/waist height, below the chin, never overlapping the face.
50. Signs on posts: the board is attached to its posts (posts reach the board's edges), at every frame incl. pop-in animation.

## Rule 51 (owner, Nov 10 2026): DETAIL STANDARD
51. "These videos are way more detailed than ours, so I want ours to become as detailed as theirs." Before building and before rendering, apply every rule, recipe and QA check in engine/cartoon-3d/DETAIL_STANDARD.md (>= 20 props per wide shot, three depth layers, no repeated tiles, no bare ground, visible light sources, scene palettes at 0.40-0.48 saturation, big acting characters, >= 5 object close-ups, travelling transitions, >= 8 sets) and run engine/cartoon-3d/render/detail_metrics.py on the render. Report the numbers in the Gate 2 note.

## Rule 52 (owner, Nov 10 2026): BIGGER FRAMES, SECOND TEARDOWN
52. "I want it to be higher quality, meaning each frame will be bigger in size and the video size will therefore also be larger." The master of every short is 2K (1440x2560, `--scale 1.3333 --crf 16`), and the full-quality file is what gets scheduled wherever the upload path allows. Apply DETAIL_STANDARD.md section G as well: at most 1 hard cut, pick a transition family, bridged dissolves, pose-to-pose acting with no tweened faces, one warm light source in every night shot, facts shown as in-world documents, cold open in motion, no outro. Run QA checks Q9-Q14.

## Rules 53-71 (Chicago remake, Nov 11-12 2026)
The new rules from the Chicago remake. They are owner corrections plus findings from my own reviews. Reference build: project/src/videos/chicago2 (composition ChicagoV2). QA tools: render/qa/ (edge.py, p.mjs projection, est.mjs motion, sheet17.py contact sheets, stills.mjs).
53. No character card may cut into a wall. People working at a wall stand at least 0.4 m out from the plinth, and their card is yaw-locked parallel to the wall (cranker(..., yaw)). Check every still for half-hidden bodies at walls, tables and counters.
54. ZERO object mistakes. That means no glitches and nothing appearing where it shouldn't (floating pencils, blobs, half bodies). It also means nothing changed by the environment when it shouldn't be (rain, fog or lights on cards), or the reverse. Held props never cross faces and stay out of the caption band (about 65-75% of the height). Before sending any sheet, review every still at full size against all rules and send a written list with the sheet.
55. Style follows the references 100% (never their characters):
    - About 2.9 head-heights: big head, straight-sided garment with a flat hem, short stick legs.
    - Character outline about 6-8 px at 1080.
    - One pale near-white head tone with cool shading.
    - Motion (est.mjs): median 1.2-1.5 px/f at 180 w, p90 at most 3, no lunges. Big moves become soft dissolves.
56. In a tight insert where a prop fills the frame, nobody peeks round it. Characters at a frame edge are fully in or clearly out for the whole move (check with p.mjs). Foreground decor must read as a thing. The subject sits in the upper 55% of the frame, never under the caption.
57. Focus blur is used only indoors. Outdoor takes use cInf 1.5. Indoor close-ups use 2.5-3.5 when the set is detailed (the drawn detail must survive).
58. Every handle, strap, string or loop joins the object it belongs to: draw it first, with its ends running into the body.
59. A held prop reads against a clear background. No post, pole, lamp, edge or card crosses or touches its silhouette at any frame. Check with p.mjs over the whole shot.
60. Soles sit exactly on the surface under them: sidewalk, porch, platform, or raised floor plus lift. Surfaces that meet are level or visibly stepped.
61. Anyone under or beside a raised floor, beam or table fits under it with clearance at every frame of a lift.
62. Grounded foreground objects (lamp posts, barrels, plants) stand on the real floor, or have the base cropped by the frame bottom. Never use a camera-pinned card with its foot in the air.
63. Signs and posters are never cut by doors, windows or frames. Their text is whole. Hanging signs: both cords meet at one hook on a visible bracket.
64. Signs, shop names and logos are fully in frame or fully out. Never crop lettering.
65. A tool points AT its target (jack under the object it lifts, worker facing it). No tool part crosses a body. Pick the facing per camera (viewOf).
66. Held props and the hands holding them are the TOP layer, drawn after the head.
67. Every small prop stands inside the footprint of the surface it rests on. Check x/z against the surface bounds, not just y.
68. Seated front-on people show lap, shins and feet (kids' feet dangle) in front of the seat, with hips at the seat top. Show the owner a pose-options sheet before re-rendering a new seated pose.
69. No background rail, fence, beam, belt strap or table edge runs behind a character at waist or chest height in a close or medium shot. Move it, lower it below the knees, or leave it out.
70. The owner's goal is ZERO corrections after the final render:
    - Before any full render: every still at full size against ALL rules.
    - After the render: frame QA of the whole video (black, frozen and pop frames, loudness) plus a spot still from every shot.
    - Fix everything found before delivering. Renders run in the cloud, one at a time, in chunks under 2 h.
71. No frame, lid, rail or rod is drawn across an object that moves past it (the model's glass-box lid cut through the lifted houses, so it became an open-top diorama). Small table props must read as a named thing at full size. Extras must not stack head-over-head behind a nearer character.

## Rule 72 (owner, Nov 12 2026): EDGE-DENSITY FLOOR
72. Measure the edge density of 24 evenly spread stills (render/qa/edge.py: 180x320 grey, sobel > 60).
    - The average must be **at least 28%**, the lower of the two reference videos (references per frame: min 8-14, median 27-33, mean 28-35).
    - Going higher where it makes a scene richer is welcome.
    - Quiet close-ups and the ending may sit at 12-18, like the references, as long as the average holds.
    - Raise weak shots with more DRAWN OBJECTS that belong to the place and story (props, set dressing, drawn textures on flat surfaces such as water, sand, ceilings and plank walls), never noise.
    - Every added object passes rules 53-71.
73. A crane or pan never sweeps past large near objects (sails swept through the frame bottom). Kit trees near a high camera read as blurred green balls at the frame edge: skip them by region and keep the rng draws. A flying-bird card in a blurred sky reads as a grey saucer: leave it out.
74. Sign lettering is fully in frame or fully out for a whole cut-to-cut shot (rule 64, automated in chicago2):
    - World signs are listed in `SIGN_LIST` (city.ts). `World.signsFor` (world.ts) samples every second frame of the shot; any sign the frame edge cuts (signcut.ts, 9x3 grid) shows its blank board for the whole shot.
    - Foreground hanging-sign cards must keep the whole board in frame for every frame of the shot and keep the bracket's wall end off-frame. Check with render/signscan/fg2.ts. A card that sweeps across the frame is removed (rule 73).
    - Before a final render, run render/signscan/scan.ts to list the shots that blank signs and spot-check them.
75. 2K final render (see render/run_2k_final.sh):
    - Use `SCALE=1.3333333333333333` exactly.
    - Run at most 2 browsers, concurrency 1 each, every frame single-layer (`ONLY=base`).
    - Render the dissolve over-layers as PNGs (scripts/overframes.mjs) and blend them in render/assemble.py, which also logs the edge average of the real video.
    - Background jobs die after 2 h, so run.sh is resumable: re-run it until both workers print DONE.

## Rules 77-91 (owner review of Chicago v20, Nov 13 2026)

77. **Clean cuts.** No orphan camera key may show a different framing for 1-5 frames around a cut or dissolve. Chicago 0:09 showed a stray 2-frame blurry puddle shot between the swamp and the rain.
    - Every shot lasts at least 18 frames.
    - Check the frame-diff at every cut ±3 frames.
    - Look at those frames one by one.
78. **Inserts hold long enough.** A poster, newspaper or document insert stays fully visible for at least 1.0 s, not counting the dissolves. Never flash a readable insert for a fraction of a second (Chicago 0:12, the CHOLERA poster).
79. **Grounded foreground props stand on the floor.** Barrels, pots, plants, crates and stools used as foreground must stand on the real floor at their spot. Never use camera-pinned cards in the air: they float when the camera pans (Chicago 0:09 barrel, 0:50 fern pot). This extends rule 62 to every grounded prop.
80. **Sinking reads as sinking.** A character sunk in mud, water or snow shows that material around the legs (a mud ring or splash at the shins), so it never reads as legs cut off.
81. **Frame with drapes only from the edge, never over the subject.**
    - A curtain or drape foreground card may frame the edge of the frame, at no more than about 12% of the width, and never over the subject.
    - When in doubt, leave it out. The owner called the 0:20 and 0:44 curtains distracting.
82. **Models face the camera.** Models, plans, maps and displays are shot front-on, with the camera within about 20° of the face's normal. Never side-on.
83. **Wall decor stays off glass.** Posters, pictures and frames never overlap windows, doors or glass. The Chicago 0:20 picture showed inside the window glass. Place decor on clear wall piers and check every interior wall.
84. **Nothing crosses sign lettering.** Floor bands, beams, awnings and posts stay clear of a sign board. Either draw the board in front, or cut the band around it (Chicago 0:24, DRY GOODS).
85. **No coplanar surfaces.**
    - Porches, sidewalks, floors and decals at the same height get at least 2 cm of separation plus polygonOffset.
    - Scrub every pan across boards frame by frame for flicker (Chicago 0:29 porch).
    - This extends rule 43.
86. **Awnings sit above doors.** An awning or canopy mounts above the door head, with its lowest edge at least 0.15 m above the door top. It must never sit across the door (Chicago 0:29).
87. **The camera never enters geometry.** Sample every camera path every frame:
    - Keep it at least 0.3 m from walls, awnings, ceilings and floors.
    - Indoors, keep it below the ceiling at every frame; above the ceiling the room opens to the sky.
    - Chicago faults: 0:32, the camera went through an awning and into a building; 0:51, it rose above the parlour ceiling.
88. **No body crosses a floor, porch, ceiling or beam.**
    - Anyone under a raised floor fits under it, with at least 5 cm of head clearance at every frame of a lift.
    - People on a lower street near a raised sidewalk are fully visible or fully hidden: no hats sliding along the boards.
    - Chicago faults: 0:32, a hat slid along the boards; 0:33, a woman's head was inside the porch.
89. **Props rest on their supports.** Cups sit on saucers or plates with the bottom at the plate top, and plates sit on the table. Check every prop's base against its support (Chicago 0:44, a cup sank into its plate). This extends rule 67.
90. **Workers at walls stay out of the wall.** Rule 53 applies to every take, including wides: yaw-lock the card parallel to the wall and keep it at least 0.4 m out (Chicago 0:24).
91. **Fix only what the owner names.** When the owner lists issues by timestamp, fix only those parts, re-render only the affected segments, and keep everything else frame-identical. Turn every item into a rule here.
    - The 0:51 "stool glitch" was a parlour footstool standing inside the right-hand jack worker (rule 76): it was removed.
