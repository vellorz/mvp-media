# det7: Detroit Thanksgiving football, round 6 (rule 329 Rick-style bodies) - PC GPU render package, ALL 21 shots

Run after the Cape Cod job has finished (one GPU job at a time). Work in D:\AI\MVP-render\det7 with absolute D: paths only.

1. Join: `copy /b det.blend.part0+det.blend.part1 det.blend`; `certutil -hashfile det.blend SHA256` must equal `1c6898fc022d694dba2fc411bb647e83efcbcb4ed8775697c1e707534d67d4e6` (110875402 bytes).
2. Test frames: `blender.exe -b det.blend --python pctest.py -- D:\AI\MVP-render\det7\test S01:60 S08:560 S18:1400`
3. Render all shots (resume-safe): `blender.exe -b det.blend --python pcrender.py -- D:\AI\MVP-render\det7\frames`
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\det7\frames D:\AI\MVP-render\det7\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/det7/clips` and `render-test/det7/test` on branch `claude/project-thread-v5jm25`.

Changes vs det6: rule 329 (owner Nov 22). Every character is rebuilt on Rick's body: rounded capsule torso whose top sits behind the head (no square shoulders), filled tube legs, thicker arms with bigger mittens, head 0.03 m lower so it overlaps the torso. Camera tilts re-solved for the new face heights. Every shot changes, so render all 21.

Shoulder fix (owner's sheet comment, Nov 22): shoulder pivots moved down and out onto the torso's side outline (lib.py GEO shx 0.141/0.156/0.165, shz 0.86), so the arm grows out of the side outline instead of running as a second line inside it; arm cards cast no shadow. castcheck.py now fails any shoulder pivot more than 0.02 m off the outline or on the curved top.
