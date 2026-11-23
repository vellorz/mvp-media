# cc4: Cape Cod Pilgrims (Tue) round 4 - PC GPU render package, all shots

Work in D:\AI\MVP-render\cc4 with absolute D: paths only. One GPU job at a time; never stop another program; delete nothing.

1. Join: `copy /b cc.blend.part0+cc.blend.part1 cc.blend`; `certutil -hashfile cc.blend SHA256` must equal `a170cf803456c48c5d3ffc34e442fcc57cbe56946709e6bf9e9dbefc31385424` (119435400 bytes).
2. Test: `blender.exe -b cc.blend --python pctest.py -- D:\AI\MVP-render\cc4\test S16:1540 S10:1110 S04:300 S19:1790`
3. Render all shots (resume-safe): `blender.exe -b cc.blend --python pcrender.py -- D:\AI\MVP-render\cc4\frames`
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\cc4\frames D:\AI\MVP-render\cc4\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/cc1/clips_r4` and `render-test/cc4/test`.

Adds: expression library (v7vnb2 be340ee) with rig round 3 and rule 335 (owner-approved 00:20Z Nov 23): Rick warm skin, pre-compensated for AgX Punchy (255,214,178 texture, reads Rick's warm hue on screen), Nauset keep their own tones; Rick-sized eyes/brows/mouth; turned faces with matched off-centre mouths; hats tilted 5-9 deg; trucker, goatee, fullbeard, walrus, chevron, curled, pencil, whitebeard, stubbledots, sidepart, curly. Gate: limbcheck 55/55, castcheck 15/15, arm/cap probes 0, 25 distinct faces.
