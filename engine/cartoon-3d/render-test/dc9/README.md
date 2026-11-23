# dc9: Washington DC Thanksgiving short, round 7 PC package: rig round 3 + growing library (v7vnb2 cd3a329), rules 333c/334: tophat3d, flatcap3d, kepi3d (DC library addition, Rick refs 15_022_0 + 02_006_0), fullbeard/king/goatee + approved mustaches, bowl/bangs/messy/sidepart hair, 16 of 18 turned with off-centre mouths. Cast gate v6: castcheck 18/18, armprobe 0, facecheck PASS, rule 333/334 scan PASS. Supersedes dc6-dc8 (never rendered)
- dc.blend (packed, all textures inside), sha256 in dc.blend.sha256, 91795358 bytes. 21 shots, 2,199 frames (overlaps are dissolves; the timeline is 2,087 frames).
- Test frames first: `cd /d D:\AI\MVP-render\dc9` first (never write to C:), then `blender.exe -b dc.blend --python pctest.py -- D:\AI\MVP-render\dc9\test S05:455 S11:1200 S21:2060`
- Full render: `blender.exe -b dc.blend --python pcrender.py -- frames` (resume-safe, per shot, OptiX 8 spp)
- Encode: `blender.exe -b --python pcencode.py -- frames clips` then push clips/ and test/ to render-test/dc9/ on claude/project-thread-z0l0eh.
- Sources: engine/cartoon-3d/render/blender/dc/ (scene_dc.py builds the blend; post_dc.py, music_dc.py, mix_dc.py run in the cloud).
