# dc16: Washington DC Thanksgiving short, PC package (cast gate v11 PASS, Nov 23 2026): dc15 + owner-approved motion round 8 (d5lr4u 714b4e0: think_chin, double_take, clap at the chin, cross_arms_huff with a light rim on presD's crossed arms, startle_recoil, look_back_shrug; walk off). Supersedes dc15.
dc14b + approved motion library (d5lr4u ec45d35: 19 coordinated combos, inferred combos off), rule 354b rig (FOOT_LIFT, ARM_Y, POSE_DY, FACE_Y, no blob-shadow cards; lib.rigcheck 0 faults), dc14c verifier render fixes (S16 box shadow, S19 heads spread in depth, lighter wainscot so arms read, S04 mailman walk), presC toothbrush mustache (333b). Supersedes dc14b.
- The blend is split in two parts (GitHub 100 MB limit). Join on the PC first, in D:\AI\MVP-render\dc16 (never C:):
  `copy /b dc.blend.part0+dc.blend.part1 dc.blend` then `certutil -hashfile dc.blend SHA256` must equal dc.blend.sha256 (174742464 bytes).
- Test frames first: `blender.exe -b dc.blend --python pctest.py -- D:\AI\MVP-render\dc16\test S06:552 S11:1166 S19:1818 S21:2060`
- Full render: `blender.exe -b dc.blend --python pcrender.py -- D:\AI\MVP-render\dc16\frames` (resume-safe, per shot, OptiX 8 spp)
- Encode: `blender.exe -b --python pcencode.py -- frames clips` then push clips/ and test/ to render-test/dc16/ (same branch the Detroit thread used for dc14b clips).
- Sources: engine/cartoon-3d/render/blender/dc/ (scene_dc.py builds the blend; post_dc.py, music_dc.py, mix_dc.py run in the cloud).
