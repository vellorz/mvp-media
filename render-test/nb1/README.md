# nb1: Nuremberg Christkindlesmarkt (Fri Nov 27) - PC GPU render package, all 18 shots

Work in D:\AI\MVP-render\nb1 with absolute D: paths only. One GPU job at a time; never stop another program; delete nothing.

1. Join: `copy /b nb.blend.part0+nb.blend.part1 nb.blend`; SHA256 must equal `4c625cdcdef6e2e09046ba2ecbbbb97937f96e6a98d60db063c58e09bfd73174` (54294878 bytes).
2. Test: `blender.exe -b nb.blend --python pctest.py -- D:\AI\MVP-render\nb1\test S04:420 S13:1370 S17:1750 S18:1830`
3. Render all shots (resume-safe): `blender.exe -b nb.blend --python pcrender.py -- D:\AI\MVP-render\nb1\frames`
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\nb1\frames D:\AI\MVP-render\nb1\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/nb1/clips` and `render-test/nb1/test` on branch `claude/project-thread-7rv8u4`.

Film: 1906 frames (0-1905), 18 shots, 1440x2560 @ 30 fps; each shot renders with only its own CHR_<shot> collection and its own camera.
Built from engine/cartoon-3d/render/blender/nb (Cape Cod cc rig + rule 367a/367c/373 rig patches; 14 approved combo moves of 12 kinds).
Gate: cast gate passed (castcheck 13/13, rule 329/330 sheets), contactcheck PASS (526 set meshes, 27 characters), rigcheck 0 on all 18 shots,
eye pass on stills (rule 378) critical fixed (S18 candles now leave frame with their holder). The blend is pruned (never-visible face/arm cards removed).
