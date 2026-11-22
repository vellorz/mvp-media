# det5: Detroit Thanksgiving football, round 4 (round-3 verifier fixes) - PC GPU render package

Replaces det4. Work in D:\AI\MVP-render\det5 with absolute D: paths only.

1. Join: `copy /b det.blend.part0+det.blend.part1 det.blend`; `certutil -hashfile det.blend SHA256` must equal `dd94475a30f1364aa8ec466bd948d0168f0a70d6b206396761f9d9ac91fc574b` (110,788,763 bytes).
2. Test frames: `blender.exe -b det.blend --python pctest.py -- D:\AI\MVP-render\det5\test S01:60 S04:352 S18:1400 S21:1630`
3. Full render (21 shots, frames 0-1652 incl. dissolve overlaps, resume-safe): `blender.exe -b det.blend --python pcrender.py -- D:\AI\MVP-render\det5\frames`
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\det5\frames D:\AI\MVP-render\det5\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/det5/clips` and `render-test/det5/test` on branch `claude/project-thread-v5jm25`.

Round-4 changes (from the round-3 verifiers): body cards 0.91 tall about the feet (torso and legs measured long); S01/S20 family on a receding diagonal seen from a raised camera; S18 year calendars restored (an edit had dropped them); S11 faces keyed again (same cause); per-shot camera tilt so faces clear the 71.7 % caption band; calendar circled from the start of S10; the final S of LIONS brushed on in three stages beside the brush; banded cash on the desk in S03; S12 wider lens and S18 shorter push keep faces in frame; ON AIR clear of the pillar.
Probes before packing: armprobe 0; check_scene floats 0 / walk clips 0; camstill 94.1 % moving, no still run over 30 f; camrules joincheck 0 (S16 low camera accepted); occprobe: S08 kid 0.12 behind dad's arm card edge, S10 bear behind the closed door (intended).
pcrender.py, pcencode.py and pctest.py are byte-identical to det4.
