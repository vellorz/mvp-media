# cc6: Cape Cod round 6 - PC GPU render package, all shots

Work in D:\AI\MVP-render\cc6 with absolute D: paths only. One GPU job at a time; never stop another program; delete nothing.

1. Join: `copy /b cc.blend.part0+cc.blend.part1 cc.blend`; SHA256 must equal `f12b31e0a20fe991aea029dab3cc2279032b64440c406fc765048de9572ce38e` (64697857 bytes).
2. Test: `blender.exe -b cc.blend --python pctest.py -- D:\AI\MVP-render\cc6\test S08:690 S10:1050 S17:1630 S19:1790`
3. Render all shots (resume-safe): `blender.exe -b cc.blend --python pcrender.py -- D:\AI\MVP-render\cc6\frames`
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\cc6\frames D:\AI\MVP-render\cc6\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/cc6/clips` and `render-test/cc6/test`.

New in cc6: owner-approved coordinated motion library (rules 356-364; 19 combo moves of 14 kinds: panic clutch, talk tilt, glance shift, cheer, huff, laugh lean, scold, concede dip, eureka point, turn and point, laugh bob, point, startle recoil, wave), rule 354b rig fixes (separate card depths, feet lifted 17 mm, no ground-blob shadow), S10 right Nauset man inside the frame, S05 Pilgrim back on the forecastle deck. Gate: rigcheck 0, arm 0, cap 0, occ 0, no double push, limbcheck 54/54, head edges 40 brief frames. The blend is pruned (never-visible face/arm cards removed): visible-card sets match the full build.
