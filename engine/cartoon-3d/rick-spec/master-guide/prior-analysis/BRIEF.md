# Frame-by-frame production analysis brief

Goal: a private style study of YouTube Shorts from @RicksClips3000, to learn HOW they are made (so the owner can make original videos in a similar production style for their own business, ModernVistaPrints). Never re-upload or share the media.

## Your inputs (folder rick-reference/analysis/NN/)
- `data.md` — metadata, cut timestamps (scene detection misses crossfades!), loudness per 0.5s, auto-caption transcript with word start times. READ THIS FIRST.
- `sheets/sheet_NNN.jpg` — contact sheets covering EVERY frame. Sheet N = second N-1..N, 30 frames, 6 cols x 5 rows, read left-to-right then top-to-bottom. Each tile is labelled with frame number (fNNN) and timestamp. The yellow label is ours, NOT part of the video.
- `cuts/` — full-resolution frames at detected hard cuts.
- Source video: rick-reference/NN_<id>.mp4 (1080x1920, 30fps). If a tile is too small to judge something (caption font, UI text, texture, a character's face), extract the full-res frame yourself:
  `& "C:\Users\artem\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe" -v error -ss <seconds> -i <video> -frames:v 1 <scratch_out>.jpg` (PowerShell), writing into rick-reference/analysis/NN/zoom/ .

## Do
Open and look at EVERY sheet in your assigned range (no skipping, no sampling). Then write your report (markdown) to the path given in your task. Report:

1. **Shot log** — a row per shot/beat: start–end time (frame-accurate where possible), what is on screen, camera move (static / push-in / pan / orbit / whip / shake, speed), transition into it (hard cut / crossfade with duration in frames / whip / zoom / match cut), and the narration line it covers. Note any shot that holds still > 1.5 s.
2. **Visual production**: what the backgrounds are made from (game engine? which game it looks like, e.g. Planet Coaster / Cities Skylines / Minecraft / Unreal, stock footage, AI images), how the 2D character(s) are drawn and composited (outline, shading, shadow, scale, how they're animated: puppet / frame-by-frame / static pose swaps, lip-sync or not, number of poses/expressions), props, overlays, diagrams, on-screen text, arrows, highlights, zoom-ins, freeze frames.
3. **Captions**: font look (weight, family guess, case), size and position as % of frame height, words per caption, colour/stroke/shadow, highlight colour, animation in/out, sync to the word timings in data.md.
4. **Pacing**: average shot length, visual change rate (how often something new appears), how image changes line up with narration beats and with the loudness data, hook (first 3 s frame by frame), ending/loop (last 3 s, and whether the last frame flows into the first).
5. **Audio inferences** from data.md + visuals: narration delivery pace (words/sec), music presence, SFX cues implied by visuals (impacts, whooshes), loudness target.
6. **Story structure**: the narrative template (setup → conflict → twist → science explanation → payoff), and where each beat lands in seconds.
7. **How to reproduce**: a concrete toolchain and step list you infer (e.g. "record game footage in X with free camera, composite PNG stick character in CapCut/After Effects with drop shadow, auto-captions style Y"). Mark each item as OBSERVED (seen in frames) vs INFERRED.
8. Anything surprising or distinctive.

Be specific with frame numbers as evidence. Keep the report under ~1500 words. Your final message back should be a ~200-word summary plus the report path.
