# bcn3s: Barcelona fix package (9 shots) spliced into the bcn3 render

Run lead approved one package for the r3 render-level criticals (spliced into r3; no other full render).
Work in D:\AI\MVP-render\bcn3s with absolute D: paths only. One GPU job at a time; never stop another program; delete nothing.

1. Join: `copy /b bcn.blend.part0+bcn.blend.part1 bcn.blend`; SHA256 must equal `d69a735a246debaf254a2f4bc1c0ddf906b9710b9203646f9f891f47d4e56c87` (80995996 bytes).
2. Test: `blender.exe -b bcn.blend --python pctest.py -- D:\AI\MVP-render\bcn3s\test S09:780 S12:970 S15:1206 S16:1300`
3. Render ONLY these shots (resume-safe): `blender.exe -b bcn.blend --python pcrender.py -- D:\AI\MVP-render\bcn3s\frames S15 S09 S10 S12 S03 S06 S14 S16 S18` (about 800 frames, ~30 min)
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\bcn3s\frames D:\AI\MVP-render\bcn3s\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/bcn3s/clips` and `render-test/bcn3s/test` on claude/project-thread-icrzj6.

Fixes (checked on the build: signcut 0, headover 0, head-edge only walk-ins, rigcheck 0 faults):
- S15 [C]: the ball never went in. Camera now on the field side facing the goal; the ball flies past the keeper into a new net, drops and rests in the goal; recoil timed to it.
- S09 [C] K1/318 and rule 345: the hero waits in the foreground (head 24-29 % W, under the caption band); a high arc around him reads as clear camera motion; arrivals gather behind.
- S10/S12 rule 345: high three-quarter view (2.4 m), the hero standing in front as speaker; lamp moved off the GIMNASIO sign; S10 skin balance lowered (rule 355).
- S14: e1 crosses his arms (the akimbo arm crossed e2's face). S16: edge-cut player reframed. S18: middle runner off the field line. S06: masthead stays whole. S03: kiosk-set trees cast no sun shadow (shadows from trees never in frame).
