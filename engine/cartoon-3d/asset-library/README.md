# Cartoon asset library (shared by every run, reachable from any device)

Every reusable asset a video creates (set piece, prop, texture, character card, costume, SFX, music stem,
Blender collection) is stored under this folder and listed in `MANIFEST.json`.

## Owner policy (Nov 22 2026)
- Reuse a past asset only when it genuinely fits the new scene AND passes the current quality bar
  (rulebook + render spec). Quality first; efficiency counts only after quality passes.
- Never reuse an asset to save tokens. Never force an unrelated asset into a scene: build a new one.
- Every video stays visually unique: no asset may be the recognisable centrepiece of two videos.
  Generic dressing (crates, lamps, foliage, textures, crowd bodies) may repeat when restyled to the scene.

## Layout
    asset-library/<type>/<asset-id>/...      type = sets | props | textures | characters | audio | blender
    asset-library/MANIFEST.json

## Manifest entry
    {"id": "prop-streetlamp-1930s-01", "type": "props", "path": "props/prop-streetlamp-1930s-01/",
     "files": [{"name": "lamp.png", "sha256": "..."}], "tags": ["street", "night", "1930s", "usa"],
     "source_video": "bf13 Black Friday (Philadelphia)", "created": "2026-11-21",
     "fit_notes": "what scenes it suits and what it does NOT suit (era, place, palette, scale)",
     "quality": {"verdict": "pass", "checked_against": "RULES_CONSOLIDATED sha c9783819, RENDER_SPEC v1.5", "notes": ""},
     "reuse_log": [{"video": "...", "date": "...", "decision": "reused | rejected", "why": "..."}]}

## Rules for workers
- Before building, search the manifest by tags. Record every reuse decision (also rejections) in `reuse_log`.
- After a video passes the verifier, register its new assets (Sonnet tier upkeep task). Append entries;
  never delete an entry (mark `"retired": true` with a reason instead).
- Files over 95 MB do not go in the repo; note their location in `fit_notes`.
