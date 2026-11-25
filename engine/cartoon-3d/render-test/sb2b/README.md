# sb2b: Strasbourg PATCH render (14 of 22 shots). Round 2 verifiers + eye pass found render-level criticals in these shots only; the other 8 shots keep their sb2 clips.
Shots to render (pass them on the command line): S02 S03 S06 S07 S08 S09 S10 S11 S12 S14 S15 S16 S18 S22 = 1,383 frames. Same settings as sb2 (8 spp, OPTIX).
Fixes: S07 pulpit rail is an open band (was the 'lid'); S02 kid no longer passes the camera's end point; S08/S18 three-quarter views (no frontal rows); S03/S10/S11/S12/S15 framing (main characters in frame); S09 lips only on the quote; S14/S18 skirted characters lean less (no dress tear); S15 window glass in front of its frame; S16 no sunglasses; S22 centre mug off the poster's border.
Join in D:\AI\MVP-render\sb2b (never C:): copy /b sb.blend.part0+sb.blend.part1 sb.blend ; certutil -hashfile sb.blend SHA256 must equal sb.blend.sha256 (99051518 bytes).
Test: blender.exe -b sb.blend --python pctest.py -- D:\AI\MVP-render\sb2b\test S07:640 S02:245 S08:750 S12:1070 S18:1640
  Check: S07 the preacher stands inside an open gold ring (no solid top); S02 no big head in the lower right; S08 three councillors at a 3/4 angle; S12 kid in red, woman in blue and a seller all whole; S18 mother, girl and green boy by the tree.
Render: blender.exe -b sb.blend --python pcrender.py -- D:\AI\MVP-render\sb2b\frames S02 S03 S06 S07 S08 S09 S10 S11 S12 S14 S15 S16 S18 S22
Encode: blender.exe -b --python pcencode.py -- frames clips ; push clips/ and test/ to render-test/sb2b/ on claude/project-thread-v5jm25.
Expected frame counts: S02 133, S03 108, S06 59, S07 153, S08 98, S09 60, S10 91, S11 68, S12 153, S14 61, S15 101, S16 46, S18 131, S22 121 = 1,383.
