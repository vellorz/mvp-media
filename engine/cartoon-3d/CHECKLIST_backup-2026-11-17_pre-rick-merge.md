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

## Rules 73-76 (Nov 12 2026)
73. A crane or pan never sweeps past large near objects; leave out blurred kit trees at high-camera frame edges and flying-bird cards in blurred skies.
74. No block-shaped bushes, hedges or plants: rounded cartoon shapes or drawn cards only.
75. No object passes through a wall, quay, floor or any solid at any frame of its move; trace every moving object's path before rendering.
76. No person or prop passes through another object: clamp people to the footprint they stand in, keep rails behind bodies, use open-top frames.

## Rules 77-91 (owner review of Chicago v20, Nov 13 2026)

Apply these with rules 1-76 to every cartoon short, including the week-03 Fri-Sun videos.
Check them on stills AND on scrubbed camera moves before any full render. Re-check them on the final video before delivering.

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

## Rules 92-106 (owner review of Istanbul v3, Nov 13 2026)

Apply these with rules 1-91 to every cartoon short. Check them on stills and on scrubbed moves before any full render, and again on the final video.

92. **The voiceover is never cut.** When a take has to fit the picture, only silence may be removed or added.
    - Split only inside pauses quieter than -45 dB that last at least 150 ms, and keep 70 ms of the pause on each side.
    - Never drop a chunk, and never speed up the whole take.
    - Check that the voiced seconds (above -40 dB) of the fitted file equal the source take.
    - Retime the captions to the new word times. Ease the picture onto the narration (piecewise slope 0.85-1.15) and move the sound effects with the picture.
    - Istanbul v3 lost about 6 s of word starts and ends, and the voice dropped in and out.
93. **One mouth per face.** No costume part may sit as a dark oval or blob inside the face near the mouth or chin: scarf knots, collars, buttons, beards in a dark colour. The grandmother's scarf knot read as a second black mouth (0:04, 0:56).
94. **Props never pass through furniture.** A held, lowered or set-down prop stays above the surface at every frame. "Lowering" a newspaper means folding it down onto the table, never sinking it through (0:04). This extends rule 89.
95. **Map pieces follow the map.** Tokens on a map move only over the painted feature they stand for: ships on water, armies on land. Check token paths against the drawing's pixel coordinates, and frame the camera so the token and its goal are in shot (0:28).
96. **Every tool works on a visible target.** A brush, swab, hammer or shovel touches the material it works on at every frame. Nobody paints the air (0:35). This extends rule 65.
97. **Everything mounted is attached.**
    - Oars, rails, outriggers, torches, lamps and flags connect to a visible support: a bracket, sconce, pole or wall.
    - Nothing floats beside the object it belongs to.
    - On land, a galley's oars are stowed flat on deck, never standing upright in the air (0:37 oars, 0:48 torch).
98. **People keep clear of every vehicle in a convoy.** Workers ahead of one ship, cart or car must not stand inside the next one. Space the vehicles so the crew zone (bow + 0.8 m to the last hauler) ends at least 1 m before the next stern (0:38). This extends rule 76.
99. **No single-sided cloth.** Flags, banners, sails and pennants are double-sided. A flag seen from behind must never vanish (0:41).
100. **Gags show cause and effect in frame.**
    - Example: the guard watches the event through his spyglass, lowers it in shock, and it slips from his hand to the floor at his feet, where it stays.
    - A prop never appears or falls from mid-air, and never falls through a floor (0:43).
101. **Roofs are closed from every camera.** Houses get both roof slopes and their gable ends, so no sky shows through any roof (0:47).
102. **Walking means steps.** Anyone moving over the ground uses a walk cycle with the stride locked to the distance covered. Nobody glides, including someone carrying something (0:47).
103. **Feet sit on the tread they stand on.** On stairs, every foot rests on a real tread height at every frame. Walking down steps follows the step heights, never a ramp (1:00).
104. **A place must read in one second.** A story place shows unmistakable cues. A wedding chapel needs a flower garland on the door, petals, a bride in veil with a bouquet, and guests. If a viewer can't name the place at a glance, add cues (1:00).
105. **No filler shots.** Every shot shows what its narration line says, and a beat under 1.5 s must still read.
    - The "or set sail" beat is a boatman coiling his mooring line back up beside his boat, not a man with a fishing rod.
    - Props never cross a boat or wall (1:01).
106. **No shared faces.** Plinths, slabs, floors and decals never share a top or bottom face. Leave at least 2 cm between them. A chain or other object laid on a surface rests every link on the surface, never sinking into it (1:06). This extends rule 85.

## Rules 107-110 (owner review, Nov 13 2026: Istanbul v4, Chicago v21)
107. Buildings stay whole from every camera angle: domes, half-domes, drums and roofs meet cleanly, with no sliced shells, interpenetration or gaps. Scrub every move past a landmark (Istanbul 0:11, Hagia Sophia).
108. Every torch, lantern and lamp is held, or touches a visible bracket, post or wall. Check from the shot camera, at the bracket's depth (Istanbul 0:48-0:49).
109. No one vanishes in front of the camera mid-shot. Cull with the whole card, never pop a person near the lens (Chicago 0:32-0:33).
110. Small props rest on a floor or table top with a contact shadow, or sit in a hand (Chicago 0:55-0:56, case in front of Pullman).

## Rules 111-117 (owner review of the Munich still sheet, Nov 13 2026)
111. Undersides are closed: pedestals, ledges, balconies, arches and vaults seen from below have a bottom face; arches are one solid, never stepped slabs with gaps; no ground blob under figures on a high ledge seen from below.
112. Women read as women at a glance: long hair past the jaw or a bun/updo, soft centre-parted hair (no boyish scalloped fringe), two outer lashes per eye; a bride gets a subtle headpiece with the veil.
113. Food is 3D and lies flat on its plate, board or table, never an upright card; frame food 30-40 degrees from above.
114. Animals stand on the ground in every frame: place the lowest hoof or foot of each cycle phase on the ground line.
115. Crowds look alive: groups of 2-4 facing each other, couples, kids, walkers both ways at mixed speeds, spread across the width; never rows or single file. Festival streets have stalls both sides, rides on the skyline, garlands every 15-20 m and a used ground.
116. Landmarks are shown whole: frame famous buildings far enough back that the silhouette reads against the sky, with people in front; never let a patterned skin fill the frame.
117. No blank walls: every wall a shot dwells on has texture (courses, string course, niches, arches, crests), lower tower storeys included.

## Rules 118-141 (owner review of NYC + Munich, Nov 14 2026)
## Grounding and attachment
118. Animals (elephants, camels, horses, dogs) touch the ground in EVERY frame. Check the contact point of each animal sprite against the floor height under it on every shot (NYC 0 s, 42 s, 49 s, 56 s; Munich 20 s).
119. Structural parts (beams, cables, lamp posts, flag poles) are visibly attached at both ends to something solid. No floating beams, lamps or flags (NYC 0 s, 13 s, 30 s).
120. Bridge and street lamps stand INSIDE the walkway on its rail or deck, never outside the parapet.
121. Held props sit in the hand (the hand closes around the handle). No lamp hovering near a hand (NYC 0 s).
122. Shadows fall under the body, matching the scene's single light direction. A jumping character's shadow stays under them and shrinks as they rise, never drifting off to one side (NYC mattress).

## Surfaces and textures
123. No glitching or shimmering textures. Every large surface (deck, roadway, ground, walls) is checked in a moving 2K test clip for z-fighting, moiré and swimming tiles before the full render. Coplanar layers sit at least 0.015 m apart.
124. Floors and decks are opaque from every camera angle. Never see through a floor (NYC 68 s, 70 s).
125. Walls read as walls: drawn brick or stone with ink lines and lighting, distinct from the water and sky. No flat unpainted building sides (NYC 49 s right-hand building).
126. Landmark entrances and bridge approaches are drawn with full detail (the reference method: painted flat backdrop plus 3D hero props), not a bare box (NYC 7 s, 49 s, 52 s).

## Characters and crowds
127. Every on-screen person has a full face (eyes, brows, mouth). No eyeless or blank heads, even in the background (NYC 13 s).
128. No half-body cut-offs that read as a floating torso. A character is either framed naturally by the edge of the frame or a foreground object, or shown whole.
129. Crowds use distinct people: no visible repeats of the same face, outfit and hat within one shot, and at most 2 repeats across the video. Vary age, build, hair, hats, colours and expressions.
130. Crowds never stand in single-file rows or columns. Use clusters, couples and diagonals, with everyone acting differently (adds to rule 115).
131. Expression changes are motivated by the line or the action and stay in sync. A face swap must never change the sound effects or audio.
132. Animals (dog, horses) are drawn with the same ink detail and features as the people: eyes, texture, shading. No flat blobs.

## Shots and story
133. Every shot has a clear purpose the viewer gets in 1 second. If a shot's point can't be said in one line, cut it or redesign it (NYC 7 s front-of-bridge).
134. No shot holds longer than about 4 s without new action or a camera move; crowd beats max 3 s (NYC staircase sat for 6 s or more).
135. The picture matches the narration. When the VO names a new subject (for example the trend tie-in), the shot shows it or a clear stand-in, never an unrelated view (NYC League of Legends line).
136. The camera never passes through walls, floors or railings, and never swings round through the lens. Check the camera path for distance to geometry and for degrees per frame before rendering.
137. Shot changes follow the references and Chicago: bridged dissolves that match the same object in the same spot on screen. No sudden shifts or one-frame jumps (Munich 7 s).
138. Characters never overlap or pass through props or set pieces behind them (Munich 11 s, rule 76).
139. Actions land where they are aimed: a stamp, brush or tool touches exactly the spot where its mark appears (Munich 37 s, rule 96).
140. Gate 2 compares the video side by side with the references (rule 141 below). A video that only "passes the checklist" is not finished.

## Reference-first method (owner, Nov 14 2026)
Rick's reference videos are the SOLE master guide for how our cartoon shorts look and move. The 140 rules are a safety net, not the method. Chicago v21 is the house benchmark for transitions and scene flow, because it is the one built closest to the references.

## Why NYC and Munich went wrong (my analysis)
1. I built them as 3D worlds (a bridge, streets, a meadow) and checked them against the rulebook, not against the reference frames. The references use hand-painted flat backdrops on parallax cards, with 3D only for hero props. A modelled 3D bridge is exactly where the glitching textures, see-through decks, floating lamps and floating animals came from.
2. Both were built in parallel under deadline, from the Chicago code but not with Chicago's shot grammar. Transitions and pacing drifted.
3. QA was technical (black and frozen frames, loudness, edge density, a dropout scan), and those checks passed. Nobody watched the full video in motion next to a reference before Gate 2. Sheets of stills hide floating, texture shimmer and camera paths.
4. The cast generator reused a small set of faces and outfits, and crowds were laid out in rows.
5. The task prompts list the teardowns as "read if needed", 117 rules deep. The reference method got diluted by the checklist.

## The method from now on (rule 141, applies to every video)
A. Before writing shot lists: open the reference teardowns (research/reference-teardown-dragon, research/reference-teardown-bell; private, never published) and Chicago v21. Pick for every planned shot the reference shot it is modelled on, and write that in the shot list ("shot 4 = dragon shot 9: painted backdrop, close-up prop, dissolve on the jar").
B. Build each set the reference way: a painted flat backdrop plus 3D hero props. A big modelled structure (bridge, stadium, street) is only allowed when the reference does the same thing.
C. Every still sheet and the final video get a side-by-side page: our frame next to the matched reference frame (kept private), with a one-line verdict on detail, grounding, faces and lighting.
D. Before Gate 2, watch the full 2K video in motion (ffmpeg contact strips every 3 frames for each shot), not just still sheets. Check grounding, attachment, textures, the camera path and the picture matching the VO.
E. If a shot can't match its reference, redesign it. Don't ship it. Say so in the Gate 2 note.

## Rules 142-143 (owner, Nov 16 2026, review of the Blender Venice proof)
142. NO FLOATING PARTS. Every object is attached to, or resting on, something: statues on their plinths, ornaments on the building, lamps on their posts, props on a surface. The Venice proof had small statues and finials hanging in the air around the Salute church. Only things that really fly (birds, clouds, rain, a thrown prop mid-air) may be off the ground, and they carry the custom property `fly=1`. Anything that flies must read as itself at a glance: a bird is big enough to show a body, head and two wings (at least ~25 px long at 1440 wide), never a white fleck. The Venice gulls were tiny white bars and read as debris floating around the church.
    - Check: `render/blender/check_float.py` on the first, middle and last frame of every shot before any 2K render. It must print CHECK_FLOAT PASS (tested on the Venice proof: it flagged the dome ribs, gulls and props resting on a hidden water plane, 210 objects).
143. HELD PROPS NEVER PASS THROUGH THE BODY. A swung tool (mallet, oar, shovel) stays in front of or beside the body on every frame of the swing; it never sweeps through the torso, head or legs, or vanishes behind the back. The Venice proof's mallet went through the worker at 4-5 s.
    - Plan swings so the arc stays on the camera side of the body (wind-up beside the shoulder, not over and behind the head).
    - Check: `render/blender/check_clip.py` on every frame of every swing in a fast pass before any 2K render. It must print CHECK_CLIP PASS (tested on the Venice proof: it flagged the mallet inside the body on frames 80-86 and 107-119). Then watch the swing in a workbench preview at full frame rate.

## Rules 153-171 (owner, Nov 17 2026, review of Salzburg v2 and the scrapped Dresden short)
153. THE CAMERA NEVER PASSES THROUGH OR GRAZES GEOMETRY. Salzburg v2 walked through a fir tree (1 s of black at 0:17), and its crane shot ended against a house wall at 0:10, which gave an awkward viewpoint. Keep every camera path at least 1 m from walls and trees for its whole move, and move the set piece, not the story beat.
    - Check: `render/blender/check_campath.py` must print no NEAR line for a visible object.
154. MAIN CHARACTERS ARE IN FRAME. When the shot is about two people, both are fully readable: heads and upper bodies in frame, not cropped by a too-tight lens. Dresden 0:11 was too zoomed in and lost both of them. Check the first, middle and last frame of every shot for each named character.
155. WORK IS VISIBLE AND TOUCHES ITS MATERIAL. Hands doing a job are in view, and the hand or tool touches the thing being worked on: dough, ingredients, paper, strings. Dresden 0:14 had bakers "baking" with their hands out of view, not touching the table.
156. EFFECTS ARRIVE ON THE BEAT OF THEIR OBJECT. A glow, beam or highlight appears on the same frame as the object or moment it belongs to, never about a second late (Dresden 0:22, the yellow beam).
157. SIGNS READ WHOLE. No post, pole, prop or character cuts through sign lettering in the camera view. Mount boards above or beside their posts (Dresden 0:25).
158. CHARACTERS NEVER WALK THROUGH OBJECTS. Every moving character and cart keeps clear of tents, stalls, tables and other characters on every frame (Dresden 0:30-0:32 and 0:40). Run check_clip.py with each mover's body meshes against nearby set pieces over the whole move.
159. NO FACE IS COVERED. In the camera view, no prop or set piece covers a character's face while the character matters to the beat (Dresden 0:34). Check that the camera's sightline from the lens to each named face is clear on sampled frames.
160. BODIES ARE MODELLED, NOT BOXES. No character gets a square or box body that reads as a glitch or placeholder (Dresden 0:36). Use the cast's tall, round or short body shapes, and check every new cast member in a turnaround still.
161. LONG HAIR READS AS HAIR. Long hair runs continuously from the crown to behind the shoulders, in the hair colour, framing the face. It never sits as a separate lump under the chin that reads as a beard (Dresden 0:45). Check women in a front still.
162. WALKING MEANS STEPPING. Any character whose root moves steps its feet, with alternating shoes and legs locked to the stride (blib `walk()`). It never slides (Salzburg 0:36; Dresden 0:40 slid sideways). Movers walk the way they face, not backwards.
163. NO OVERLAPPING COPLANAR SURFACES. Two meshes never share a face plane: overlapping lobes of one object (the guitar body) are joined into one mesh, and walls never butt into a tower face at the same depth. Salzburg 0:01-0:02 and 0:25 had guitar texture flicker, and 0:07 had flicker at the church base. Check a moving 2K test clip of every close-up prop.
164. DOORS FIT THEIR DOORWAY. A door has a frame, the leaf is no bigger than the opening, and opening it reveals a lit or dark interior, never a flat wall (Salzburg 0:18).
165. NOBODY POPS IN. Characters enter by walking in: out of a doorway, from behind a set piece or from the edge of frame. They never appear in place within a frame (Salzburg 0:18, Gruber).
166. WRITING TOUCHES THE PAGE. A quill or pen tip rests on the paper while writing, with small strokes across it. Solve the arm pose against the table height, and lower the table if the arm can't reach (Salzburg 0:20). Verify the tip-to-paper distance in Blender.
167. INSTRUMENTS ARE PLAYED. A guitarist's strumming hand sits over the sound hole and makes quick, small, regular strokes. The fretting hand stays on the neck, with no big uncoordinated arm swings (Salzburg 0:25).
168. EXACTLY ONE FACE, EVERY FRAME. Every visible head shows exactly one face decal on every frame (Salzburg 0:22 and 0:30 had faces vanishing). The schedule is sorted, missing faces fall back to a near face (blib `FACE_FALLBACK`), touching ranges are merged, and faces only show while the body does.
    - Check: `render/blender/check_faces.py` must print CHECK_FACES PASS.
169. BUILDINGS SIT IN THE GROUND. A building's base goes below the terrain surface, into the snow or mound, never resting on top of a curved surface with gaps (Salzburg 0:47 chapel). check_float covers objects, so also look at the base line in a low-angle still.
170. GENERAL NOTES FROM THE SCRAPPED DRESDEN (context; the owner gives direction separately): voice, music, characters unlike Rick's references, scene choice, transitions, and pacing that was too slow.
171. RE-RECORDS KEEP THE ANIMATION. When a VO is re-recorded, warp every keyframe through an old-to-new word-time map (salwarp.py) instead of rebuilding the scene by hand. Re-run all checks afterwards.
