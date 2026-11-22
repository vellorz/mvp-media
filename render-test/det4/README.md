# det4: Detroit Thanksgiving football, round 3 (round-2 verifier fixes) - PC GPU render package

Replaces det3. Work in D:\AI\MVP-render\det4 with absolute D: paths only.

1. Join: `copy /b det.blend.part0+det.blend.part1 det.blend`; `certutil -hashfile det.blend SHA256` must equal `da45631ae853128a5075a94c466acb52745eba0ce4ddfbcc7d27f4d36c53a578` (104,456,228 bytes).
2. Test frames: `blender.exe -b det.blend --python pctest.py -- D:\AI\MVP-render\det4\test S04:352 S08:560 S13:1052 S21:1630`
3. Full render (21 shots, frames 0-1652 incl. dissolve overlaps, resume-safe): `blender.exe -b det.blend --python pcrender.py -- D:\AI\MVP-render\det4\frames`
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\det4\frames D:\AI\MVP-render\det4\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/det4/clips` and `render-test/det4/test` on branch `claude/project-thread-v5jm25`.

Round-3 changes (from the round-2 verifiers): VO pauses cut only in silence and breaths (gapcut4; round 2 clipped final "s" sounds), scene re-timed to it; S01/S20 family staged in depth (dad close in front, three behind); S08 seen from a high diagonal with the speaking grandpa in the foreground; double face cards after the retime removed (sanitizer in warp_det.py); ON AIR, kiosk papers and the S09 calendar fully in or out of frame; SOLD OUT rolls down like a blind under the clerk's hand; calendar already circled when the camera arrives; painter brushes the final S of LIONS on camera; operator no longer mimes plugs; radio man stays in frame in S18; front characters' arms never cross the faces behind them.
Probes before packing: armprobe 0; check_scene floats 0 / walk clips 0; camstill 93.7 % moving, no still run over 30 f; camrules joincheck 0 (S16 low camera accepted); occprobe: depth overlaps in S01/S20 (kids partly behind the front dad, intended layering), S10 bear behind the closed door (intended).
pcrender.py, pcencode.py and pctest.py are byte-identical to det3.
