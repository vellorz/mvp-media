# Cartoon 3D daily-short engine (Modern Vista Prints)

The daily video format from Nov 9 2026: a ~60-70 s true story told with flat cartoon characters in a painted 3D world,
Drew voice-over, Rick-style captions, original music bed, ending on the whole poster. Built with the
`cartoon-3d-short` skill (three.js inside Remotion). This folder is the working state after three shipped shorts.

| Short | Composition | Poster | Status |
|---|---|---|---|
| London Bridge to Arizona | `HavasuShort` (src/videos/havasu) | 0245 London | posted Mon Nov 9 2026 |
| The tower Paris tried to tear down | `EiffelShort` (src/videos/eiffel) | 0495 Paris | Tue Nov 10, Gate 2 pending |
| Pisa: fix it without fixing it | `PisaShort` (src/videos/pisa) | 0351 Pisa | Wed Nov 11, Gate 2 pending |

## Restore on a fresh box
```bash
cp -r engine/cartoon-3d/project ~/cart && cd ~/cart && npm ci     # pinned Remotion 4.0.541 / three 0.187
mkdir -p ~/rtmp && export REMOTION_TMP=~/rtmp
npx tsc --noEmit
npx remotion still src/index.ts PisaShort out/s.jpg --frame=400 --scale=0.5 --gl=swangle
```
Python audio side: `pip install numpy scipy pillow`, ffmpeg. Audio scripts per short in `audio/<name>/`
(synth_*.py = original music, mix_*.py = mix to -14 LUFS, caps.py = caption chunks from ElevenLabs word timings).
Voice-over wavs are not stored here (regenerate with ElevenLabs Drew `q0IMILNRPxOgtBTS4taI`).

## New short = copy the newest folder
`src/videos/pisa` -> `src/videos/<name>`, register a `<Composition>` in `src/Root.tsx`, then edit story.ts (shots,
cameras, places), world.ts / build.ts (landmark + town), cast.ts (characters), fx*.ts (2D prop cards).

## Render (cloud box, 4 cores, software GL)
`render/render_comp.sh <Comp> <outdir> <frames> <mix.wav> <final.mp4>` renders 300-frame chunks (~25-30 min each,
~3 h per 66 s video), concatenates and muxes audio. `render/queue.sh` runs several in a row.
- ONE render at a time (two renders + stills ran Chrome out of memory).
- Every chunk re-bundles src/: never leave any composition uncompilable while a render runs.
- Patch a few frames instead of re-rendering: render `--frames=a-b`, re-encode with `-video_track_timescale 90000`, splice, concat `-c copy`.

## Quality checklist
`CHECKLIST.md` = every owner correction so far. Check stills of every shot against it before each full render,
and scrub every shot change frame by frame in the final.
