# det6: Detroit Thanksgiving football, round 5 (owner notes, rule 326) - PC GPU render package, 12 shots only

Run after det5 has finished. Work in D:\AI\MVP-render\det6 with absolute D: paths only.

1. Join: `copy /b det.blend.part0+det.blend.part1 det.blend`; `certutil -hashfile det.blend SHA256` must equal `1431f2042be0c0865750380b975c22acbd462d2053a2a087787b05a00aa3bc59` (110,642,372 bytes).
2. Test frames: `blender.exe -b det.blend --python pctest.py -- D:\AI\MVP-render\det6\test S01:60 S03:260 S12:1015`
3. Render ONLY these shots (resume-safe): `blender.exe -b det.blend --python pcrender.py -- D:\AI\MVP-render\det6\frames S01 S03 S04 S05 S07 S08 S12 S13 S14 S19 S20 S21`
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\det6\frames D:\AI\MVP-render\det6\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/det6/clips` and `render-test/det6/test` on branch `claude/project-thread-v5jm25`.

Changes vs det5: rule 326 (owner Nov 22): the big beard and the long-hair slab are gone. Dad has a slim mustache and mom a side-part bob; the seller, the old fan and grandpa have slim mustaches; the fan lady has a bob. The other 9 shots are unchanged and come from det5.
