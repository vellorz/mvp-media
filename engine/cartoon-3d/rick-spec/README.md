# Rick-spec QA scripts (Nov 17 2026)

Measurement tools behind the Rick Master Guide. The guide itself and all reference material stay private in the project folder `research/rick-style-spec/` (never commit reference frames or videos here).

| script | measures | Rick pass line (19 reference videos) |
|---|---|---|
| metrics.py video.mp4 out.csv | per-frame luma, saturation, edge density, motion (mean abs luma diff @270x480), p2/p98 | motion median >= 4.5; still frames (diff<1) <= 12 %; luma 0.33-0.56; sat 0.37-0.66; p2 >= 0.05; p98 >= 0.84; edge 0.20-0.35 |
| transitions.py video.mp4 out.csv | cuts and dissolves (blend fit + colour-histogram change) | 2-4.5 joins per 10 s |
| dissolve_curve.py video.mp4 mid... | visible dissolve length per join | every join 4-14 f (default 6-12 f) or <= 3 f fast join; <= 5 fast joins; lengths must vary |
| captions.py video.mp4 | burned-in caption box (white fill + black outline) | box bottom 71.7 % H, cap 2.8 % H (54 px @1920, 72 px @2560), centred, median width <= 50 % W |
| script_stats.py words_dir | narration words/s, word gaps, sentence length, hook, pivots | 3.4-4.1 words/s; <= 3 gaps > 0.8 s; max gap <= 1.2 s |
| sheets.py frames_dir out_dir | labelled 24-frame contact sheets of every frame | for frame-by-frame review |

Mix target: -14 LUFS integrated, -2 dBTP, LRA <= 3.2 (ffmpeg ebur128). Music bed about 20 dB under the VO, no ducking.
Run all of them on the preview before Gate 2 and report the numbers next to the pass lines (proposed rule 172, awaiting owner approval).
