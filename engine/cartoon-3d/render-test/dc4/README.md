# dc4: Washington DC Thanksgiving short, round 2 PC package after CAST GATE v3 PASS (rule 329 Rick-measured bodies, bigger faces, ankle skirts, child 0.8, real 0443 poster in post); supersedes dc3 (dc3 frames are void)
- dc.blend (packed, all textures inside), sha256 in dc.blend.sha256, 81060380 bytes. 21 shots, 2,199 frames (overlaps are dissolves; the timeline is 2,087 frames).
- Test frames first: `blender.exe -b dc.blend --python pctest.py -- test S05:455 S11:1200 S21:2060`
- Full render: `blender.exe -b dc.blend --python pcrender.py -- frames` (resume-safe, per shot, OptiX 8 spp)
- Encode: `blender.exe -b --python pcencode.py -- frames clips` then push clips/ and test/ to render-test/dc4/ on claude/project-thread-z0l0eh.
- Sources: engine/cartoon-3d/render/blender/dc/ (scene_dc.py builds the blend; post_dc.py, music_dc.py, mix_dc.py run in the cloud).
