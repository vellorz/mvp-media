# det3: Detroit Thanksgiving football, round 2 (verifier fixes) - PC GPU render package

Replaces det2. Work in D:\AI\MVP-render\det3 with absolute D: paths only.

1. Join: `copy /b det.blend.part0+det.blend.part1 det.blend`; `certutil -hashfile det.blend SHA256` must equal `e075603b094f27c082877fa28b5dd0a0683aaaaba27490633c385917b007dbe2` (106,809,888 bytes).
2. Test frames: `blender.exe -b det.blend --python pctest.py -- D:\AI\MVP-render\det3\test S04:355 S10:712 S11:900 S21:1630`
3. Full render (21 shots, frames 0-1647, 1,703 frames incl. dissolve overlaps, resume-safe): `blender.exe -b det.blend --python pcrender.py -- D:\AI\MVP-render\det3\frames`
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\det3\frames D:\AI\MVP-render\det3\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/det3/clips` and `render-test/det3/test` on branch `claude/project-thread-v5jm25`.

Round-2 changes (from the round-1 verifiers): retime fixed (no pops at f0 or at shot starts/ends), cut points moved (5 shots over 4 s), new VO pause trim that never cuts speech (gapcut3, pace 3.41 w/s), staggered character rows (S01, S04, S08, S16, S20), painter's brush reaches the LIONS banner, lamppost off the banner, kiosk papers no longer overlap, cash goes hand to hand, door slides to reveal the Bears player, operator's plugs on the panel, gramps speaks the quoted line, lighter skirting (no near-black band), video ends 1.15 s after the last word starts.
Probes before packing: armprobe 0; check_scene floats 0 / walk clips 0; camstill 95.8 % moving, no still run over 30 f; camrules joincheck 0 (S16 low camera accepted); occprobe: S10 bear hidden behind the closed door 684-712 (intended), S05 f423 and S08 543-573 at the 0.08 limit.
pcrender.py, pcencode.py and pctest.py are byte-identical to det2.
