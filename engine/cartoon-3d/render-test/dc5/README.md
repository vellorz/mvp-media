# dc5: Washington DC Thanksgiving short, round 3 PC package after CAST GATE v4 PASS (shoulder pivots on the torso side outline; S03 and S08 pointing arms swing outward; arm cards follow BSY and cast no shadow, from Detroit b54a72c); supersedes dc3 and dc4 (their frames are void)
- dc.blend (packed, all textures inside), sha256 in dc.blend.sha256, 81053580 bytes. 21 shots, 2,199 frames (overlaps are dissolves; the timeline is 2,087 frames).
- Test frames first: `cd /d D:\AI\MVP-render\dc5` first (never write to C:), then `blender.exe -b dc.blend --python pctest.py -- D:\AI\MVP-render\dc5\test S05:455 S11:1200 S21:2060`
- Full render: `blender.exe -b dc.blend --python pcrender.py -- frames` (resume-safe, per shot, OptiX 8 spp)
- Encode: `blender.exe -b --python pcencode.py -- frames clips` then push clips/ and test/ to render-test/dc5/ on claude/project-thread-z0l0eh.
- Sources: engine/cartoon-3d/render/blender/dc/ (scene_dc.py builds the blend; post_dc.py, music_dc.py, mix_dc.py run in the cloud).
