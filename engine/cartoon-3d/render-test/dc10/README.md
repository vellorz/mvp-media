# dc10: Washington DC Thanksgiving short, round 8 PC package: dc9 (rig round 3, library cd3a329 + kepi3d, gate v6 PASS) + rule 335 (Rick warm skin on all 18, brows x1.6; library be340ee). Cast gate v7: castcheck 18/18, armprobe 0, facecheck PASS. Supersedes dc6-dc9 (never rendered)
- dc.blend (packed, all textures inside), sha256 in dc.blend.sha256, 92231957 bytes. 21 shots, 2,199 frames (overlaps are dissolves; the timeline is 2,087 frames).
- Test frames first: `cd /d D:\AI\MVP-render\dc10` first (never write to C:), then `blender.exe -b dc.blend --python pctest.py -- D:\AI\MVP-render\dc10\test S05:455 S11:1200 S21:2060`
- Full render: `blender.exe -b dc.blend --python pcrender.py -- frames` (resume-safe, per shot, OptiX 8 spp)
- Encode: `blender.exe -b --python pcencode.py -- frames clips` then push clips/ and test/ to render-test/dc10/ on claude/project-thread-z0l0eh.
- Sources: engine/cartoon-3d/render/blender/dc/ (scene_dc.py builds the blend; post_dc.py, music_dc.py, mix_dc.py run in the cloud).
