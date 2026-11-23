# dc12: Washington DC Thanksgiving short, round 10 PC package: dc11 + Cape Cod F25 skin method: skin texture 255,213,166 under AgX gives face 218-219,199-200,181-182 on screen (G/R 0.913, B/R 0.83; Rick 0.92/0.83). Head emit 1.0. Supersedes dc6-dc11 (never rendered)
- dc.blend (packed, all textures inside), sha256 in dc.blend.sha256, 92057770 bytes. 21 shots, 2,199 frames (overlaps are dissolves; the timeline is 2,087 frames).
- Test frames first: `cd /d D:\AI\MVP-render\dc12` first (never write to C:), then `blender.exe -b dc.blend --python pctest.py -- D:\AI\MVP-render\dc12\test S05:455 S11:1200 S21:2060`
- Full render: `blender.exe -b dc.blend --python pcrender.py -- frames` (resume-safe, per shot, OptiX 8 spp)
- Encode: `blender.exe -b --python pcencode.py -- frames clips` then push clips/ and test/ to render-test/dc12/ on claude/project-thread-z0l0eh.
- Sources: engine/cartoon-3d/render/blender/dc/ (scene_dc.py builds the blend; post_dc.py, music_dc.py, mix_dc.py run in the cloud).
