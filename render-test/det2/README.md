# det2: Detroit Thanksgiving football (Mon Nov 23 extra video), retimed to the faster take-3 voice-over - PC GPU render package

det1 is obsolete (stopped at 243 frames; take-1 timing). Render only det2. Work in D:\AI\MVP-render\det2 with absolute D: paths.

1. Join the parts (GitHub caps files at 100 MB):
   - Windows: `copy /b det.blend.part0+det.blend.part1 det.blend`
   - check: `certutil -hashfile det.blend SHA256` must equal `3697201f8267efe06ca2c8d77ce61f8d2962b4e2a3f8b1653e894e78ebd60b2a` (106,712,056 bytes)
2. Test frames first (GPU alpha / black-card check, PC_RENDER_NOTES N-003, N-011), output path absolute:
   `blender.exe -b det.blend --python pctest.py -- D:\AI\MVP-render\det2\test S04:330 S11:900 S16:1240 S21:1640`
3. Full render (21 shots, frames 0-1670, 1,728 frames incl. dissolve overlaps, resume-safe):
   `blender.exe -b det.blend --python pcrender.py -- D:\AI\MVP-render\det2\frames`
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\det2\frames D:\AI\MVP-render\det2\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/det2/clips` and `render-test/det2/test` on branch `claude/project-thread-v5jm25`.

pcrender.py, pcencode.py and pctest.py are byte-identical to det1 / bf13.
Probes on the retimed scene before packing: armprobe 0, check_scene floats 0 / walk clips 0, camstill 94.8 % moving (no still run over 30 f), camrules joincheck 0 (S16 low camera = accepted exception, scoreboard look-up), occprobe 1 frame at the 0.08 limit (S05 f406, background fan arm, accepted).
Retime: warp_det.py + warpmap.py (old take-1 word onsets -> take-3 onsets). Sources: engine/cartoon-3d/render/blender/det/.
