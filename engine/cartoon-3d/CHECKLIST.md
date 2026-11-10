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
