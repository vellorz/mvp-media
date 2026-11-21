# PC render notes (append-only lessons log)

Written by the PC render session (RTX 3070, Blender 4.2.23, OptiX). **Append new entries at the bottom; never edit or delete old ones.**
Purpose: every lesson found while rendering or checking videos is recorded here as soon as it is found, so the rulebook, gap report and master guide threads can fold it in.
Each entry: date, package, what was seen, cause (CONFIRMED or SUSPECTED), the rule or check to apply, how a future render should adjust.

---

## 2026-11-21 entries (rounds bf3 to bf13, Black Friday test video)

### N-001 Overlapping shot frame ranges play twice (SUSPECTED cause of the 37 s double zoom)
- Seen: owner reported the camera zooming in twice around 37 s (frames ~1105-1125).
- Facts (CONFIRMED from `sc['shots']` in the blends): shot ranges overlap by 4-12 frames at every boundary, for example S11 1051-1125 and S12 1114-1218; S01 0-170 and S02 163-297; S03 292-432 and S04 426-528.
- Cause (SUSPECTED): if clips are joined whole, the overlap frames play twice, which reads as a repeated zoom or jump.
- Rule: when joining shots, trim each clip to its own frame range so that no global frame number plays twice, unless the overlap is a deliberate dissolve.
- Check: list global frame numbers across all clips after assembly; any number appearing twice outside a declared dissolve is a fail.
- Future render: keep unique ranges per shot or declare dissolves explicitly in the shot table.

### N-002 Camera-parented prop shows as a black blob (CONFIRMED, bf9 S03)
- Seen: dark blurred box in the bottom-left of S03 from ~9.7 s that moved with the camera.
- Cause (CONFIRMED by ray cast): `truck_mirror` (and `truck_mirror_ink`) were parented to `cam_S03` at local offset (-0.13, -0.22, -0.6), 0.6 m in front of the lens, so they rode with the camera and were out of focus.
- Rule: no prop may be parented to a camera unless it is deliberately a lens overlay.
- Check: scan every object whose parent is a camera or whose parent chain reaches one.
- Future render: place framing props in the world, not on the camera. Fixed in bf10 (mirror removed).

### N-003 Black quad where an arm should be (SUSPECTED cause, bf10 S04 f510)
- Seen: a big black rectangle in front of the granny's torso at ~17 s.
- Facts (CONFIRMED): the ray hit `S04_x0_granny_arm-1_arm`, a flat ribbon (dims 0.74 x 0 x 0.56 m, zero thickness in Y). A scan of all 210 arm objects found no arm stretched more than about 1.3x its median size, so it is not a scale blow-up.
- Cause (SUSPECTED, not proven): a zero-thickness arm ribbon seen broadside renders its back side black.
- Rule: arm meshes need thickness (for example solidify about 0.03) or a double-sided material, and must never render as a black plane.
- Check: render one test frame per shot at several poses and flag large near-black regions that belong to arm objects.

### N-004 Held props are parented to pivots or bodies, not hands (CONFIRMED object names, bf10)
- Seen: sign-holder at ~26 s with detached limbs; officer with newspaper at ~49 s with glitching arms.
- Facts (CONFIRMED): `S07_owner_placard`/`S08_owner_placard` are parented to `S07/S08_owner_bpiv`; `S15_paper` is parented to `S15_oldcop`. They do not follow the hands.
- Rule: a held prop is attached to a hand attach point, and both arms reach its grip points.
- Check: for each held prop, measure the distance from each hand to its nearest grip point on every frame; fail above a small threshold.

### N-005 Arm/hand through own face (REPORTED, not traced)
- Seen in the opening officer and other characters.
- Rule: hands never enter the head or torso volume. Check: per-frame distance of each hand to the head sphere.

### N-006 Ledger text outside the ruled lines (REPORTED, not traced)
- Seen on the S14 desk ledger. Rule: text stays inside the page's ruled area. Check: compare text bounds to the page's line bounds.

### N-007 Redundant establishing shot at 6-8 s (REPORTED, design call, not traced)
- The traffic reveal repeats traffic already visible behind the officer. Rule: a shot may not show only what the previous shot already showed.

### N-008 Tool lesson: stereo stems read 3 dB hot (owner note, scripts not seen here)
- `bedcheck.py` and `sfxcheck.py` read stereo stems 3 dB hot. Calibrate before comparing to loudness thresholds.

### N-009 Operations: texture-load crash is memory pressure (CONFIRMED, bf13)
- Seen: Blender died during texture upload with `UNKNOWN EXCEPTION`, then `Malloc returns null` (about 1.4 GB). The known-good bf11 blend failed the same way, so it was not the new package.
- Cause (CONFIRMED by control test): a Hermes router python process used about 6 GB and the commit charge was nearly full (about 4.5 GB of the 51 GB limit free). Fixed by a PC restart (5.4 GB RAM and 20.7 GB commit free afterwards).
- Rule: before starting a render, require at least 5 GB free RAM and at least 15 GB free commit. Crash dumps land in `D:\AI\MVP-render\tmp\bf.crash.txt`. If the crash is at the texture load, run a control with a previously good blend before blaming the new one.

### N-010 Operations: Blender can hang after ALL_DONE (CONFIRMED, bf10)
- The render process stayed alive after printing `ALL_DONE`, holding the GPU, which slowed the encode. The chain script now waits for `ALL_DONE`, gives the process 60 s to exit, then stops it. Never stop it before `ALL_DONE`.
- The harmless line `Error: Not freed memory blocks` at exit does not mean a failure.

### N-011 Operations: how a package is run on this PC
- Download `render-test/bfN` at the named commit into `D:\AI\MVP-render\bfN`, check size (and hash when given), confirm pcrender.py and pcencode.py match the previous package, then run `chain.ps1`: render, encode, push clips to `render-test/bfN/clips` on `claude/project-thread-c13biq`. Typical total is about 1,867 frames, about 40 clips (each under 11 MB), about 55-70 min render. Pushes come from the worktree `D:\AI\MVP-render\wt-bf`.
- Test frames: `pctest.py ... S03:330 S16:1660 S12:1190` run first and pushed to `render-test/bfN/test`.

### N-012 Operations: upload limits for posting
- The browser upload tool only reads files in the session's allowed folders. Put the posting file in a shared folder or ask for the folder to be added before scheduling. Pinterest blocks fetching a file from another origin (CSP), so a URL fetch inside the page does not work.
