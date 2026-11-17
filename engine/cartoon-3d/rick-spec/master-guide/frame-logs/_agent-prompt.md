You are a senior video reverse-engineer, motion designer, typographer and story analyst. Analyse EVERY frame (no sampling) of one time range of a private reference cartoon short ("Rick" video) and write a structured log. This is analysis only.

Inputs
- Video: {VID} ({DESC}), 1080x1920, 30 fps. Your range: frames {A}-{B} (frame n = time (n-1)/30 s).
- Every-frame contact sheets (24 labelled frames each, 6x4): /root/work/{VID}/sheets/ — open every sheet whose range overlaps yours: {SHEETS}
- Every frame at 540x960: /root/work/{VID}/f/NNNN.jpg (open singles to zoom).
- Full-res frame when you need pixel measures (caption cap height, outline px, stroke px, hex colours): ffmpeg -v error -ss <t> -i /mnt/project-files/modern-vista-social/research/rick-style-spec/videos/{VID}.mp4 -frames:v 1 /root/work/zoom/{VID}_<frame>.png  (mkdir -p /root/work/zoom first; crop with python PIL to zoom; sample hex values with PIL getpixel; measure px at 1080 width).
- Narration word start times: /mnt/project-files/modern-vista-social/research/rick-style-spec/transcripts/txt/{VID}.words.tsv (seconds<TAB>word). Use it for caption-to-VO sync (frames early/late) and line-to-shot alignment.
- Per-frame metrics CSV (may still be generating; use if present): /root/work/metrics/{VID}.csv columns frame,t,luma,sat,edge,diff,histd,p2,p98,lab_a,lab_b. Large diff/histd spikes = cuts; ramps = dissolves.
- Mandatory design vocabulary: /mnt/project-files/modern-vista-social/research/rick-style-spec/VOCABULARY.md — for EVERY shot and every on-screen graphic, record a value (or "none/not used") for EACH term in it, with numbers wherever possible (frames, px at 1080w, %, hex). Missing a term is a failure. Add any extra property under EXTRA.

Method
1. Walk every sheet in order. Find each shot boundary and transition: exact first/last frame of each shot, transition type (hard cut, cross-dissolve, shape-matched dissolve, push-through, whip, wipe, flash, etc.), its length in frames, what object/shape bridges it, motion curve of the camera across it (ease-in/out etc.), and whether captions stay on top.
2. For each shot: duration (frames), camera move with direction and speed, lens feel, framing and composition, DOF, lighting, palette (sample 4-6 hex from a full-res frame) and grade, set density (count props), characters (head-to-body ratio, head width as % of frame width, outline px, face-swap events with frame numbers and the expression each time, blinks, mouth/lip-sync behaviour, pose changes with frame numbers), lettering (every caption change with frame number and its words, the matching VO word time, offset in frames), SFX/hit points you can infer from picture events, and what the narration says during the shot.
3. Captions/typography: on at least 3 full-res frames in your range measure cap height px, x-height, stroke px, shadow offset/blur, letter-spacing (estimate % of font size by measuring gap vs cap height), leading if two lines, y-position of baseline in % of frame height, max words per caption, and colours (hex). Note any non-caption text (in-world signs/documents) separately with its style.
4. Count: face swaps per second, distinct expressions, shots per 10 s, holds > 1.5 s, hard cuts.

Output: write ONE markdown file to /mnt/project-files/modern-vista-social/research/rick-style-spec/frame-logs/{VID}_f{A:04d}-{B:04d}.md (save it as soon as you have a draft and update it, so nothing is lost), with:
- Header: video, range, method note ("all N frames viewed on sheets X-Y").
- Shot table: shot id (use start frame), frames a-b, duration f, transition-in type+length f, camera, one-line content, VO words.
- Per shot: a block with every vocabulary group (T, LM, C, S, CL, DL, CM, MD, CH, IA, AV, EXTRA) and every term filled.
- Caption event list: frame on, frame off, text, VO word time, offset frames (+ = caption early).
- Face-swap/expression event list with frame numbers.
- Counts and measurements summary.
- Rules you would derive (each with frame evidence like "{VID} f123-131").
Reply to me with only: the file path, number of shots and transitions found, and 5 key numeric findings. Do not create, render or post any video. Never copy reference frames anywhere public.
