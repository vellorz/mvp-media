# det1: Detroit Thanksgiving football (Mon Nov 23 extra video) - PC GPU render package

1. Join the parts (GitHub caps files at 100 MB):
   - Windows: `copy /b det.blend.part0+det.blend.part1 det.blend`
   - check: `certutil -hashfile det.blend SHA256` must equal `05caf1c19b48670b542dadbeb8144ac179642c260d8217dd0a6c9ae98452a160` (106,714,834 bytes)
2. Test frames first (GPU alpha / black-card check, PC_RENDER_NOTES N-003, N-011):
   `blender.exe -b det.blend --python pctest.py -- test S04:375 S11:1060 S16:1460 S21:1900`
3. Full render (21 shots, frames 0-1940, 2,016 frames incl. dissolve overlaps, resume-safe):
   `blender.exe -b det.blend --python pcrender.py -- frames`
4. Encode: `blender.exe -b --python pcencode.py -- frames clips` (60-frame chunks, perceptually lossless H.264)
5. Push `clips/*.mp4` and `test/*.png` to `render-test/det1/clips` and `render-test/det1/test` on branch `claude/project-thread-v5jm25`.

pcrender.py, pcencode.py and pctest.py are byte-identical to render-test/bf13 (BF round 9).
Probes clean before packing: armprobe 0, occprobe 0 at MIN 0.08, check_scene floats 0 / walk clips 0, camstill 94.0 % moving (no still run over 30 f), camrules joincheck 0, no negative-scale objects, no camera-parented props.
Sources: engine/cartoon-3d/render/blender/det/.
