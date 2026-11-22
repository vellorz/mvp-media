# dc6: Washington DC Thanksgiving short, round 4 PC package: dc5 (cast gate v4 PASS, first frames PASS) + Rick expression library (34 distinct faces, facecheck PASS); supersedes dc3, dc4 and dc5 (dc5 was never rendered)
- dc.blend (packed, all textures inside), sha256 in dc.blend.sha256, 84518713 bytes. 21 shots, 2,199 frames (overlaps are dissolves; the timeline is 2,087 frames).
- Test frames first: `cd /d D:\AI\MVP-render\dc6` first (never write to C:), then `blender.exe -b dc.blend --python pctest.py -- D:\AI\MVP-render\dc6\test S05:455 S11:1200 S21:2060`
- Full render: `blender.exe -b dc.blend --python pcrender.py -- frames` (resume-safe, per shot, OptiX 8 spp)
- Encode: `blender.exe -b --python pcencode.py -- frames clips` then push clips/ and test/ to render-test/dc6/ on claude/project-thread-z0l0eh.
- Sources: engine/cartoon-3d/render/blender/dc/ (scene_dc.py builds the blend; post_dc.py, music_dc.py, mix_dc.py run in the cloud).
