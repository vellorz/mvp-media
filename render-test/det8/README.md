# det8: Detroit Thanksgiving football, round 7 (owner Nov 22: Rick expression library) - PC GPU render package, ALL 21 shots

Run after det7 has finished (one GPU job at a time). Work in D:\AI\MVP-render\det8 with absolute D: paths only.

1. Join: `copy /b det.blend.part0+det.blend.part1 det.blend` (add +det.blend.part2 if present); `certutil -hashfile det.blend SHA256` must equal `c0aa57933b217934fb6c10bb126783bf29870e1d85549aa6115f4d047332babe` (111801070 bytes).
2. Test frames: `blender.exe -b det.blend --python pctest.py -- D:\AI\MVP-render\det8\test S01:60 S03:260 S18:1400`
3. Render all shots (resume-safe): `blender.exe -b det.blend --python pcrender.py -- D:\AI\MVP-render\det8\frames`
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\det8\frames D:\AI\MVP-render\det8\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/det8/clips` and `render-test/det8/test` on branch `claude/project-thread-v5jm25`.

Changes vs det7: expression library (claude/project-thread-v7vnb2 16bb1d7) merged. Every face uses the Rick library recipes (cheer->laugh, wow->surprise, grit->angry_squint, idea->manic_grin, eyeroll->side_eye, shrug->stunned); each character has a face turn (+-0.25..0.4) with an off-centre lopsided mouth on the turned side, and hats tilt 6-10 deg toward it. Hair and facial hair stay on rule 326 D1-D3 / M1-M3 until the owner picks from the benchmark sheet.
