# bcn3: Barcelona (Sat Nov 28 video) - PC GPU render package, all shots

Work in D:\AI\MVP-render\bcn3 with absolute D: paths only. One GPU job at a time; never stop another program; delete nothing.

1. Join: `copy /b bcn.blend.part0+bcn.blend.part1 bcn.blend`; SHA256 must equal `ac7a6c8c11aea1be575a197df85ab458c4c931907519632de354e93053aca8af` (80796625 bytes). Textures are packed.
2. Test: `blender.exe -b bcn.blend --python pctest.py -- D:\AI\MVP-render\bcn3\test S09:790 S12:960 S19:1600 S20:1740`
3. Render all shots (resume-safe): `blender.exe -b bcn.blend --python pcrender.py -- D:\AI\MVP-render\bcn3\frames`
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\bcn3\frames D:\AI\MVP-render\bcn3\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/bcn3/clips` and `render-test/bcn3/test` on claude/project-thread-icrzj6.

Same pcrender/pcencode/pctest as bcn2 (per-shot CHR_ collection, own camera, 8 spp + OptiX denoise on GPU). Skin balance uses the Cycles Attribute node.

## bcn3 (Nov 25, round 3: run lead approved one more batched render for the r2 render-level criticals)
Fixed in the scene and probed on the build before packing:
- frontal rows facing camera (visual P3): S09 three-quarter camera down the facade, arrivals walk in from both ends (two cycles, every start off frame) and turn in toward the hero; S10/S12 three-quarter views (S12 raised to 12 deg so the back row clears the front); S14/S16/S18 diagonals in depth with looks; S19 tourists forward
- S09 camera read still: slow arc + dolly
- S12 parallel bars through a character: bars moved
- black boxes fixed at the source: S05/S07 press block lighter iron, S19 kiosk interior wall card (shelves)
- S09 alley gaps beside the newspaper block showed a bare ink hull: infill houses
- gym sign resized so it is whole in S04 and S12; S14 e0 reframed; S14/S19 arm gestures turned away from neighbours' faces
- S10 skin blue lowered (rule 355)
Probes on the final build: signcut 0, headover 0 (S09/S14/S19) and 3 frames S12 0.16, rigcheck 0 faults, head-edge only on walk-ins entering frame, occprobe only brief walk-arm / cheer-arm passes (max 0.2 static).
