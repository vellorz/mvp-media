# dc11: Washington DC Thanksgiving short, round 9 PC package: dc10 (gate v7 PASS) + on-screen warm-skin lift asked at gate v7: head cards emit 1.0 (was 0.25) and skin pre-warmed 255,226,186 so AgX shows ~217,205,190 (was 206,194,181). Supersedes dc6-dc10 (never rendered)
- dc.blend (packed, all textures inside), sha256 in dc.blend.sha256, 92285821 bytes. 21 shots, 2,199 frames (overlaps are dissolves; the timeline is 2,087 frames).
- Test frames first: `cd /d D:\AI\MVP-render\dc11` first (never write to C:), then `blender.exe -b dc.blend --python pctest.py -- D:\AI\MVP-render\dc11\test S05:455 S11:1200 S21:2060`
- Full render: `blender.exe -b dc.blend --python pcrender.py -- frames` (resume-safe, per shot, OptiX 8 spp)
- Encode: `blender.exe -b --python pcencode.py -- frames clips` then push clips/ and test/ to render-test/dc11/ on claude/project-thread-z0l0eh.
- Sources: engine/cartoon-3d/render/blender/dc/ (scene_dc.py builds the blend; post_dc.py, music_dc.py, mix_dc.py run in the cloud).
