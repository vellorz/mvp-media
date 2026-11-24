# cc6d: Cape Cod round 6d - PC GPU render package, ONE SHOT ONLY (S08)

Work in D:\AI\MVP-render\cc6d with absolute D: paths only. One GPU job at a time; never stop another program; delete nothing.

1. Join: `copy /b cc.blend.part0+cc.blend.part1 cc.blend`; SHA256 must equal `6f0d66e9ca34af0b0b299a5f7127877f7780f05c5d634897cd326cd9e2c410f4` (64477915 bytes).
2. Test: `blender.exe -b cc.blend --python pctest.py -- D:\AI\MVP-render\cc6d\test S08:762`
3. Render ONLY S08 (resume-safe): `blender.exe -b cc.blend --python pcrender.py -- D:\AI\MVP-render\cc6d\frames S08` (112 frames, about 5 min)
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\cc6d\frames D:\AI\MVP-render\cc6d\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/cc6d/clips` and `render-test/cc6d/test` on claude/project-thread-v5jm25.

cc6d over cc6c: the S08 Pilgrim stands 0.12 m further toward frame centre, so his head is no longer clipped by the left edge at 758-765 (rule 56, targeted r6c verifier). cc6c lipsync kept. Gates on S08: head edge 0, headover 0, occ 0, arm 0, cap 0, rigcheck 0.
