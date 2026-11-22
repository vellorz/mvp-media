# dc7: Washington DC Thanksgiving short, round 5 PC package: dc6 (expression library, facecheck PASS) + rig round 2 from v7vnb2 16bb1d7 (off-centre lopsided mouths on all 18, tilted hats on 7, printer 3D flat cap); cast gate v5 castcheck 18/18, armprobe 0. Supersedes dc6 (never rendered)
- dc.blend (packed, all textures inside), sha256 in dc.blend.sha256, 84518713 bytes. 21 shots, 2,199 frames (overlaps are dissolves; the timeline is 2,087 frames).
- Test frames first: `cd /d D:\AI\MVP-render\dc7` first (never write to C:), then `blender.exe -b dc.blend --python pctest.py -- D:\AI\MVP-render\dc7\test S05:455 S11:1200 S21:2060`
- Full render: `blender.exe -b dc.blend --python pcrender.py -- frames` (resume-safe, per shot, OptiX 8 spp)
- Encode: `blender.exe -b --python pcencode.py -- frames clips` then push clips/ and test/ to render-test/dc7/ on claude/project-thread-z0l0eh.
- Sources: engine/cartoon-3d/render/blender/dc/ (scene_dc.py builds the blend; post_dc.py, music_dc.py, mix_dc.py run in the cloud).
