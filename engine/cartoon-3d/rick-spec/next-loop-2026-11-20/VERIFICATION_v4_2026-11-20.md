# VERIFICATION v4 — 2026-11-20
Scope: 7 videos (#03, #12, #04, #10, #14, #22, #24), six tracks (joins, characters, motion, camera, assets, audio). Definitions fixed before measuring: _agent-prompts/definitions_v4_2026-11-20.md. Each track: REPORT.md + results.json in its folder.
## Result
- RULE grade (99 %+): four facts, unchanged: caption frame and text, no fingers, assets animated on ones, mix levels as a group.
- GUIDANCE (75 %+ or population-level with window): camera pan 77.6 %, tilt 75.5 %, camera type/ease/timing/segmentation, dissolve length at +-2 f (all three fits 76.5 %, at least two 98.0 %), dissolve curve 81.4 %, join kind/start/found, head fill width 77.8 % (A vs A2) and 78.9 % (A vs B), human motion timing at +-3 f start / +-4 f end, human asset timing at +-4 / +-8 f, population character medians (post-hoc).
- UNCERTAIN (under 75 % after three methods): camera scale 70.3 %, roll 62.0 %, foreground layer and parallax; per-item character build fields; motion tools (18 to 48 %); asset easing and tool timing; bed swing (+-4 dB), key, tempo, loop, SFX onsets (9.4 %).
- Camera total two-tracker agreement 74.1 %, just under 75.
## Honest limits
Three M2 amendments (characters, motion, assets) were written after per-item results were seen; they give guidance with stated windows only and no tolerance in the earlier definitions was changed. Both v3 and v4 numbers are reported in GUIDE_v1.4_addendum.md section ae. Sub-agents could not write REPORT.md; the orchestrator saved each hand-back verbatim. Motion tools failed known answers and are not used.
## Models
Opus: measuring and tool building. Sonnet: blind crop measurers. Fable orchestrator: adjudication, synthesis, rules. The platform may have substituted models; track reports state what ran.
