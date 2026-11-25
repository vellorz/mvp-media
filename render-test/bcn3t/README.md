# bcn3t: Barcelona fix package (5 shots) spliced into the bcn3s render

Run lead approved this single package (S15, S10, S12, S19, S01, about 455 frames). No other full render.
Work in D:\AI\MVP-render\bcn3t with absolute D: paths only. One GPU job at a time; never stop another program; delete nothing.

1. Join: `copy /b bcn.blend.part0+bcn.blend.part1 bcn.blend`; SHA256 must equal `9a8e0f0ba31e1da7bdb80f1a0dcda67c38d18c43bf7a3850cac2747de905d735` (81025853 bytes).
2. Test: `blender.exe -b bcn.blend --python pctest.py -- D:\AI\MVP-render\bcn3t\test S15:1206 S12:970 S19:1590 S01:40`
3. Render ONLY these shots (resume-safe): `blender.exe -b bcn.blend --python pcrender.py -- D:\AI\MVP-render\bcn3t\frames S15 S10 S12 S19 S01` (about 455 frames, ~20 min)
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\bcn3t\frames D:\AI\MVP-render\bcn3t\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/bcn3t/clips` and `render-test/bcn3t/test` on claude/project-thread-icrzj6.

Fixes (checked on the build: headover 0, headedge 0, signcut 0, rigcheck 0, lamp-over-sign probe 0, ball screen path traced per frame):
- S15: ball keyed on every frame (the shared CONSTANT-keys helper `onone()` stepped curves between sparse keys; now bakes every frame first); net gives on impact.
- S10/S12: bench removed under the standing front row; pendants re-projected clear of GIMNASIO; S12 camera 2.75 m (S10 2.4 m), hero closer (head 27-29 % W, whole head in frame); hero skin balanced per object (rule 355).
- S19: tourist's vest desaturated (source 0.84; graded rule 355/367b). S01: skin blue balance raised.
