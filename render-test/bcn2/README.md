# bcn2: Barcelona (Sat Nov 28 video) - PC GPU render package, all shots

Work in D:\AI\MVP-render\bcn2 with absolute D: paths only. One GPU job at a time; never stop another program; delete nothing.

1. Join: `copy /b bcn.blend.part0+bcn.blend.part1 bcn.blend`; SHA256 must equal `9532d732a83c679014e2dface6899c8cd391b4392cdd6d33db9d5181090ef815` (81263948 bytes). Textures are packed.
2. Test: `blender.exe -b bcn.blend --python pctest.py -- D:\AI\MVP-render\bcn2\test S04:400 S10:860 S18:1440 S20:1740`
3. Render all shots (resume-safe): `blender.exe -b bcn.blend --python pcrender.py -- D:\AI\MVP-render\bcn2\frames` (20 shots, 1838 frames incl. dissolve overlaps)
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\bcn2\frames D:\AI\MVP-render\bcn2\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/bcn2/clips` and `render-test/bcn2/test` on claude/project-thread-icrzj6.

Same pcrender/pcencode/pctest as Cape Cod cc6 (per-shot CHR_ collection, own camera, 8 spp + OptiX denoise on GPU).
Gates passed in the cloud before packing: cast gate cleared by the run lead (rules 329/330/336, turns 353a, skin 355/335a on graded probes, ink plum), rigcheck 0 faults, head-edge 36 sampled frames (walk-ins only), poster quad whole in S20.
New in this build: per-shot skin balance on head materials (object property "skb", Attribute node) - renders correctly only in Cycles, which is what the PC uses.

## bcn2 (Nov 24, round 2: the ONE re-render under rule 365)
Render-level criticals from the r1 verifiers, fixed in the scene and checked on the build before packing:
- one shadow system (rule 367c): character cards, limbs and held props cast no lamp shadow; the ground blob is the only one
- faces covered by nearer heads (S03, S04, S09, S10/S12, S19): restaged; headover 0 on screen (only off-frame waiting walkers), occprobe max 0.4 on short arm swings
- S17 joggers slid 1.7 m after their run cycle: jog cycles now run to the end of the shot
- signs cut by the frame edge (rule 206/64): signcut probe 0 on every shot (S01 moved to the next lamp, S09/S11 reframed, signs compacted, board only in S15)
- S15 whip pan replaced by a hard cut at 1226; payoff dissolve S19/S20 12 f (S19 now ends 1645)
- props redrawn: folded newspaper held by its top edge, iron dumbbells with grey plates; press box out of the S02/S06 inserts
rigcheck 0 faults. Head-edge cuts only on walk-ins/walk-outs.
