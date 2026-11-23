# cc6b: Cape Cod round 6b - PC GPU render package, FIVE SHOTS ONLY (rule 365e)

Work in D:\AI\MVP-render\cc6b with absolute D: paths only. One GPU job at a time; never stop another program; delete nothing.

1. Join: `copy /b cc.blend.part0+cc.blend.part1 cc.blend`; SHA256 must equal `5634b3e6b26eb3cd6da2efae0f4c01d34f0df6a8de6095d7e177654f38a1ca19` (64435089 bytes).
2. Test: `blender.exe -b cc.blend --python pctest.py -- D:\AI\MVP-render\cc6b\test S05:470 S08:690 S09:960 S17:1630`
3. Render ONLY these shots (resume-safe): `blender.exe -b cc.blend --python pcrender.py -- D:\AI\MVP-render\cc6b\frames S05 S08 S09 S10 S17` (767 frames, about 42 % of the film; the other 14 shots stay from cc5)
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\cc6b\frames D:\AI\MVP-render\cc6b\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/cc6b/clips` and `render-test/cc6b/test`.

New in cc6b: owner-approved coordinated motion library (rules 356-364; 19 combo moves of 14 kinds: panic clutch, talk tilt, glance shift, cheer, huff, laugh lean, scold, concede dip, eureka point, turn and point, laugh bob, point, startle recoil, wave), rule 354b rig fixes (separate card depths, feet lifted 17 mm, no ground-blob shadow), S10 right Nauset man inside the frame, S05 Pilgrim back on the forecastle deck. Gate: rigcheck 0, arm 0, cap 0, occ 0, no double push, limbcheck 54/54, head edges 40 brief frames. The blend is pruned (never-visible face/arm cards removed): visible-card sets match the full build.

cc6b over cc6 (round-5 verifier criticals): no face hidden behind a nearer head in S05/S08/S17 (new headover probe 0); S09 hand-back keeps both the carrier and the Wampanoag man in frame (second dolly pass stops at 930, framing 0.3 m left); S10 Nauset close-up face is wary, not sly. Gates re-run: arm 0, cap 0, occ 0, headover 0, rigcheck 0 on changed shots, limbcheck 54/54, moving 98.5 %.
