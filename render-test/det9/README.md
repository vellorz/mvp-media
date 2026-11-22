# det9: Detroit Thanksgiving football, owner-approved Rick look (rules 329-333b) - PC GPU render package, ALL 21 shots

Work in D:\AI\MVP-render\det9 with absolute D: paths only. One GPU job at a time.

1. Join: `copy /b det.blend.part0+det.blend.part1+det.blend.part2 det.blend`; `certutil -hashfile det.blend SHA256` must equal `574f96352800b4c4fccffe3e03a78321a71637674f9e495d93e7110c34b4ed85` (123022092 bytes).
2. Test frames: `blender.exe -b det.blend --python pctest.py -- D:\AI\MVP-render\det9\test S02:126 S03:260 S08:560`
3. Render all shots (resume-safe): `blender.exe -b det.blend --python pcrender.py -- D:\AI\MVP-render\det9\frames`
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\det9\frames D:\AI\MVP-render\det9\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/det9/clips` and `render-test/det9/test` on branch `claude/project-thread-v5jm25`.

Supersedes det8 (never rendered). Rig round 3 merged (v7vnb2 5d8d84e, owner approved Nov 22 5:52 PM CT). Rick-style looks: radioman/Richards bowler3d + pencil mustache; seller flatcap3d + walrus; fanman bowler3d + chevron; fanold flatcap3d + droop; newsboy flatcap3d + messy hair; kid34 flatcap3d; gramps whitebeard; dad34 sidepart + curled; dadM sidepart + chevron; kidM cowlick; operator topknot; clerk stubbledots. Old cloche/visor/leather helmets kept, tilted. Turns 0.35-0.5 with off-centre mouths, face variety pass (32 distinct faces), Rick bodies with shoulder joins on the outline.
