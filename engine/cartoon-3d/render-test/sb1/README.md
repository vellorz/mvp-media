# sb1: Strasbourg Sunday short (Sun Nov 29), full render. Queue it AFTER D.C., Nuremberg and Barcelona.
22 shots, frames 0-2040 (2,041 frames, 67.5 s at 30 fps), 1440x2560, Cycles GPU. pcrender.py sets 8 spp and the OPTIX denoiser, the same as D.C.
The package is slim: face images that never render were dropped (6,090 of 6,887). The full pack needed about 11 GB of RAM just to load them.
The slim blend renders pixel-identical to the source blend on 5 of 7 check frames; S20 and S21 differ by under 0.1/255 on average (sampling noise).
Join in D:\AI\MVP-render\sb1 (never C:): copy /b sb.blend.part0+sb.blend.part1 sb.blend ; certutil -hashfile sb.blend SHA256 must equal sb.blend.sha256 (100599625 bytes).
Test: blender.exe -b sb.blend --python pctest.py -- D:\AI\MVP-render\sb1\test S07:634 S12:1072 S18:1589 S21:1872 S22:2000
  Check: no black or missing cards; preacher in the carved pulpit with the red cloth (S07); the tree lit underneath (S21); the poster whole in its frame (S22).
Render: blender.exe -b sb.blend --python pcrender.py -- D:\AI\MVP-render\sb1\frames
Encode: blender.exe -b --python pcencode.py -- frames clips ; push clips/ and test/ to render-test/sb1/ on claude/project-thread-v5jm25.
Expected frame counts per shot (dissolve overlaps included): S01 131, S02 133, S03 108, S04 74, S05 101, S06 59, S07 153, S08 98, S09 60, S10 91, S11 68, S12 153, S13 119, S14 61, S15 101, S16 46, S17 88, S18 131, S19 122, S20 57, S21 110, S22 121 = 2,185.
