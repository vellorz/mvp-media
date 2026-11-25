# nb4: Nuremberg round 4, S08 only (rule 365e: smallest unit first)

Work in D:\AI\MVP-render\nb4 with absolute D: paths only. One GPU job at a time; never stop another program; delete nothing.

1. Join: `copy /b nb.blend.part0+nb.blend.part1 nb.blend`; SHA256 must equal `c53922681683619fc247ca6a6da94238e8aab18d5a23d1c83c2db23f97fedde7` (53724569 bytes).
2. Test: `blender.exe -b nb.blend --python pctest.py -- D:\AI\MVP-render\nb4\test S08:862 S08:876`
3. Render S08 only (resume-safe): `blender.exe -b nb.blend --python pcrender.py -- D:\AI\MVP-render\nb4\frames S08`
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\nb4\frames D:\AI\MVP-render\nb4\clips`
5. Pull/merge branch `claude/project-thread-7rv8u4`, then push `clips/*.mp4` and `test/*.png` to `render-test/nb4/clips` and `render-test/nb4/test`.

121 frames (S08 815-935), about 7 min at nb3 speed.
Why: round 3 owner's-eye and shots verifiers both found one critical (rule 374): the S08 flash fired with both of the photographer's hands at his waist
and the camera hidden behind his head. The tripod camera now stands beside him at hand height and his arm rests on it through both flashes (f852-881).
