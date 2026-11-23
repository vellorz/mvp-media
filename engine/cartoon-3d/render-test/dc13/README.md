# dc13: Washington DC Thanksgiving short, round 11 PC package: dc12 + rules 336/336a bodies (BSY 1.045: torso 1.02, legs 1.30, total 3.31 head widths; torso 0.80 wide, widest mid-height, narrower round hem; limbs 6.6-7.0 % incl. ink; dress neck-to-hem 2.14; shoulder pivots re-seated). On-screen medians torso 0.96, legs 1.15. Supersedes dc6-dc12 (never rendered)
- dc.blend (packed, all textures inside), sha256 in dc.blend.sha256, 92097324 bytes. 21 shots, 2,199 frames (overlaps are dissolves; the timeline is 2,087 frames).
- Test frames first: `cd /d D:\AI\MVP-render\dc13` first (never write to C:), then `blender.exe -b dc.blend --python pctest.py -- D:\AI\MVP-render\dc13\test S05:455 S11:1200 S21:2060`
- Full render: `blender.exe -b dc.blend --python pcrender.py -- frames` (resume-safe, per shot, OptiX 8 spp)
- Encode: `blender.exe -b --python pcencode.py -- frames clips` then push clips/ and test/ to render-test/dc13/ on claude/project-thread-z0l0eh.
- Sources: engine/cartoon-3d/render/blender/dc/ (scene_dc.py builds the blend; post_dc.py, music_dc.py, mix_dc.py run in the cloud).
