# bcn1: Barcelona (Sat Nov 28 video) - PC GPU render package, all shots

Work in D:\AI\MVP-render\bcn1 with absolute D: paths only. One GPU job at a time; never stop another program; delete nothing.

1. Join: `copy /b bcn.blend.part0+bcn.blend.part1 bcn.blend`; SHA256 must equal `b7a803399334b01645d7e00d063d9947eedb51da27f80cf6dfaed3de94a6ee2d` (82817149 bytes). Textures are packed.
2. Test: `blender.exe -b bcn.blend --python pctest.py -- D:\AI\MVP-render\bcn1\test S04:400 S10:860 S18:1440 S20:1740`
3. Render all shots (resume-safe): `blender.exe -b bcn.blend --python pcrender.py -- D:\AI\MVP-render\bcn1\frames` (20 shots, 1833 frames incl. dissolve overlaps)
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\bcn1\frames D:\AI\MVP-render\bcn1\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/bcn1/clips` and `render-test/bcn1/test` on claude/project-thread-icrzj6.

Same pcrender/pcencode/pctest as Cape Cod cc6 (per-shot CHR_ collection, own camera, 8 spp + OptiX denoise on GPU).
Gates passed in the cloud before packing: cast gate cleared by the run lead (rules 329/330/336, turns 353a, skin 355/335a on graded probes, ink plum), rigcheck 0 faults, head-edge 36 sampled frames (walk-ins only), poster quad whole in S20.
New in this build: per-shot skin balance on head materials (object property "skb", Attribute node) - renders correctly only in Cycles, which is what the PC uses.
