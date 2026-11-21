# Inferred recipes ([INFERRED]; never guidance), 2026-11-21
Built by analogy to the observed actions in motion/REPORT.md. The held-out test (10 hidden actions) gave: travel within +-3 f or 30 % 7 of 10, limb set 7 of 10, easing 3 of 10. So: durations and limb sets are reasonable starting values; easing is a guess; check by eye in the render. All values in frames at 30 fps (ms = f x 33.3).
| action | evidence | recipe | built from |
|---|---|---|---|
| sneak (0 seen) | absent | Walk cycle at about half speed (step every 11 to 15 f), body lowered, head forward, arms held in; hold between steps 10 to 26 f; no bounce | walk (n 28 logged, travel median 14 f), hold (holds median 26 f, loop 2) |
| run (1 seen, video 14) | thin | Walk cycle at about twice the speed (step every 3 to 4 f), body leans forward, arms swing wide; characters often slide while legs cycle (Rick's walks slide) | walk, plus the "bodies slide while legs cycle" finding of v1.3 |
| stumble (1 seen, 12 f, linear) | thin | 8 to 12 f: leg catch (snap, 2 to 3 f), torso tips with ease-in, then a recoil snap back (2 to 4 f) | fall (10.5 f, ease-in), recoil (snap) |
| carry (1 seen, 14.5 f) | thin | Lift (6 f, ease-out) onto the arms, then the object stays rigid to the hand cards while the walk cycle plays; no object wobble | lift (6 f), walk, "attached props" rule |
| catch (2 seen, 3.25 f) | thin | Arms rise 3 to 4 f ease-out to the object, then hold; reverse of throw, anticipation none | throw (8 f), point (5 f), catch observed |
| wave (1 seen, a sign pump) | thin | Lower-arm swing cycle 10 to 16 f per cycle, ease-in-out, 2 to 3 cycles, hand card rotating with the arm | emote and point arm moves (5 to 7 f), cycle loop lengths of 12 to 16 f from asset loops |
| push (2 seen) / pull (8 seen) | thin/evident | Both are arm-led, 9 to 13.5 f, ease-in-out or linear; the pushed object follows the hand with 1 to 2 f lag | pull, push observed |
| drop (3 seen) | borderline | Hand opens (snap), object falls ease-in 8 to 14 f, no bounce | fall (ease-in), asset falls (ease-in 13 of 20) |
Assets with thin or no evidence: cloth/hair (11 records): 25 f sway cycle, ease-in-out; animals (9 records): move like characters (cutout parts, walk cycle), no extra physics; crowds (4 records): small bob or sway loops of 12 to 16 f, offset per figure; water and smoke: flows 29 f, drifts 28.5 f, linear.
