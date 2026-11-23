# det10: Detroit Thanksgiving football, owner-approved Rick look (rules 329-333b) - PC GPU render package, ALL 21 shots

Work in D:\AI\MVP-render\det10 with absolute D: paths only. One GPU job at a time.

1. Join: `copy /b det.blend.part0+det.blend.part1+det.blend.part2 det.blend`; `certutil -hashfile det.blend SHA256` must equal `9d29dcf7982ff3eba8c75d96390d4265b371c6e4adc8797a5dc34a24d5602ccc` (128864594 bytes).
2. Test frames: `blender.exe -b det.blend --python pctest.py -- D:\AI\MVP-render\det10\test S02:126 S03:260 S08:560`
3. Render all shots (resume-safe): `blender.exe -b det.blend --python pcrender.py -- D:\AI\MVP-render\det10\frames`
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\det10\frames D:\AI\MVP-render\det10\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/det10/clips` and `render-test/det10/test` on branch `claude/project-thread-v5jm25`.

Supersedes det9 (kept as fallback). Adds owner-approved round 4 (00:20Z Nov 23): Rick skin preset rick_warm on every character (neck matches) and Rick-sized features (feat_scale rick: eyes x1.4, brows x1.6, mouth x1.3). Rig round 3 merged (v7vnb2 5d8d84e, owner approved Nov 22 5:52 PM CT). Rick-style looks: radioman/Richards bowler3d + pencil mustache; seller flatcap3d + walrus; fanman bowler3d + chevron; fanold flatcap3d + droop; newsboy flatcap3d + messy hair; kid34 flatcap3d; gramps whitebeard; dad34 sidepart + curled; dadM sidepart + chevron; kidM cowlick; operator topknot; clerk stubbledots. Old cloche/visor/leather helmets kept, tilted. Turns 0.35-0.5 with off-centre mouths, face variety pass (32 distinct faces), Rick bodies with shoulder joins on the outline.

det10b (Nov 22 ~7 PM CT): skin texture pre-compensated to 255,214,178 for AgX Punchy (Cape Cod F25: raw rick_warm renders grey). Measured on a 32-sample preview: S02 face 221,203,189 (G/R 0.92, B/R 0.86; Rick warm 0.92/0.83).
