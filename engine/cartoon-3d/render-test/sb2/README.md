# sb2: Strasbourg Sunday short (Sun Nov 29), the one rule-365 re-render (round 1 verifiers found render-level criticals in sb1).
22 shots, frames 0-2040 (2,041 frames), 1440x2560, Cycles GPU. pcrender.py sets 8 spp and the OPTIX denoiser, the same as sb1. Shot table unchanged, so every shot re-renders.
The package is slim: face images that never render were dropped. The slim blend renders pixel-identical to the source blend (check frames S07/S18/S21: max diff 0, 1 and 5 of 255; mean under 0.07/255).
Join in D:\AI\MVP-render\sb2 (never C:): copy /b sb.blend.part0+sb.blend.part1 sb.blend ; certutil -hashfile sb.blend SHA256 must equal sb.blend.sha256 (98388380 bytes).
Test: blender.exe -b sb.blend --python pctest.py -- D:\AI\MVP-render\sb2\test S07:620 S18:1630 S21:1885 S22:1950 S22:2030
  Check: no black or missing cards. S07: the preacher stands INSIDE the open pulpit (no lid cutting his torso). S18: mother, small boy and green boy all in frame with red/pink ornaments on the tree. S21: the yellow-jacket kid in front right with a face. S22 1950: the visitor fully in frame pointing at the poster, no vendor. S22 2030: the poster whole in its frame.
Render: blender.exe -b sb.blend --python pcrender.py -- D:\AI\MVP-render\sb2\frames
Encode: blender.exe -b --python pcencode.py -- frames clips ; push clips/ and test/ to render-test/sb2/ on claude/project-thread-v5jm25.
Expected frame counts per shot (dissolve overlaps included): S01 131, S02 133, S03 108, S04 74, S05 101, S06 59, S07 153, S08 98, S09 60, S10 91, S11 68, S12 153, S13 119, S14 61, S15 101, S16 46, S17 88, S18 131, S19 122, S20 57, S21 110, S22 121 = 2,185.
