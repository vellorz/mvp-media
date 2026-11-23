# cc5: Cape Cod round 5 - PC GPU render package, all shots

Work in D:\AI\MVP-render\cc5 with absolute D: paths only. One GPU job at a time; never stop another program; delete nothing.

1. Join: `copy /b cc.blend.part0+cc.blend.part1 cc.blend`; SHA256 must equal `87640cb4da458e2b15961a9ae88095fcdad29c6c58cdc6f29e87bf02869d9786` (119346358 bytes).
2. Test: `blender.exe -b cc.blend --python pctest.py -- D:\AI\MVP-render\cc5\test S10:1050 S16:1520 S09:820 S05:480`
3. Render all shots (resume-safe): `blender.exe -b cc.blend --python pcrender.py -- D:\AI\MVP-render\cc5\frames`
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\cc5\frames D:\AI\MVP-render\cc5\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/cc5/clips` and `render-test/cc5/test`.

Fixes round-4 verifier criticals: no grass tufts behind the Nauset men (S10); S16 two diggers, front digger shovels with the outer hand (no covered faces); per-character nudges so heads stay inside the frame (C4, 145 -> 44 edge frames); S05 lens 31 and a shorter hop; S09 opening not pushed in; S08/S15 cameras pull out from the start (rule 306). Gate: arm 0, cap 0, occ 0, no double push, castcheck 15/15, limbcheck 54/54, 25 distinct faces. Skin/ink grade fixes are in post (not in this blend).
