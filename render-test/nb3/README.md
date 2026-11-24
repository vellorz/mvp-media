# nb3: Nuremberg round 3 shot-level fix package, 8 shots only (rule 365e: smallest unit first)

Work in D:\AI\MVP-render\nb3 with absolute D: paths only. One GPU job at a time; never stop another program; delete nothing.

1. Join: `copy /b nb.blend.part0+nb.blend.part1 nb.blend`; SHA256 must equal `a136d1204e933cfb2847d93bdff9fc23fb19af66452595e9711490bae5e3805e` (53699386 bytes).
2. Test: `blender.exe -b nb.blend --python pctest.py -- D:\AI\MVP-render\nb3\test S04:470 S11:1165 S18:1850`
3. Render these 8 shots only (resume-safe): `blender.exe -b nb.blend --python pcrender.py -- D:\AI\MVP-render\nb3\frames S01 S04 S05 S07 S08 S11 S17 S18`
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\nb3\frames D:\AI\MVP-render\nb3\clips`
5. Pull/merge branch `claude/project-thread-7rv8u4`, then push `clips/*.mp4` and `test/*.png` to `render-test/nb3/clips` and `render-test/nb3/test`.

About 990 frames (S01 131, S04 174, S05 164, S07 91, S08 121, S11 89, S17 125, S18 106); nb2 ran about 18 frames a minute, so about 55 min.
Post takes these 8 shots from nb3 and the other 10 from nb2.
Why: round 2 verifiers (fri-nuremberg/verify/r2 reports) found shot-level criticals: captions over faces (S01, S07) and over story text (S05, S11, S17 banner),
the S01 cheer mitten over a face, a 53-frame still camera in S04 setup B, the S08 flash with no hand on the camera, candles alone at the S18 edge,
red ink in S18 from the warm stall fill, and the S11 church book reading as a loose sheet (now an open book with gutter and facing page).
