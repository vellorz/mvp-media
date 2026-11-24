# cc6c: Cape Cod round 6c - PC GPU render package, TWO SHOTS ONLY (rule 365e)

Work in D:\AI\MVP-render\cc6c with absolute D: paths only. One GPU job at a time; never stop another program; delete nothing.

1. Join: `copy /b cc.blend.part0+cc.blend.part1 cc.blend`; SHA256 must equal `9b3e7fd5684c668bbdfbbe600bdb1f08bd12ba63ebf2f1c36407c8394ddbf6c8` (64483503 bytes).
2. Test: `blender.exe -b cc.blend --python pctest.py -- D:\AI\MVP-render\cc6c\test S08:720 S10:1060`
3. Render ONLY these shots (resume-safe): `blender.exe -b cc.blend --python pcrender.py -- D:\AI\MVP-render\cc6c\frames S08 S10` (248 frames, about 10 min; the other 17 shots stay as they are)
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\cc6c\frames D:\AI\MVP-render\cc6c\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/cc6c/clips` and `render-test/cc6c/test` on claude/project-thread-v5jm25.

cc6c over cc6b (round-6 verifier criticals): S10 keeps two staggered Nauset men; the near man whose head was cut by the frame edge as the push passed him (1053-1061) is gone (every in-frame spot either hid him behind the close-up man or stacked him under the far one). S08: the sailor's lips move on his quoted line again (a lipsync call had been lost). Gates on S08/S10: occ 0, arm 0, cap 0, headover 0, rigcheck 0, head edge only S08_pil 758-764 (4 frames, exit at the shot end, unchanged).
