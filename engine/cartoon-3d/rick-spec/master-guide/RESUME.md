# RESUME — Rick Master Guide run (thread "Build the Rick master guide", started 2026-11-17 04:39 UTC)

> **THE THREE CORE FINDINGS (owner: must be stated in every document; re-confirmed against the source tables on 2026-11-19).** BF = our Black Friday test video, round 3. Rick = his 5 newest videos, #21 to #25.
> 1. **SCENE TIME.** Our average shot length is fine (3.65 s; Rick 2.65 to 4.54 s). The shape is wrong: 6 % of our shots are under 2 s (Rick 20 to 53 %) and 50 % are over 4 s (Rick 20 to 26 %). Our ending is slow on both measures: a shot is visible for 3.00 s on average during the last sentence (Rick 0.93 to 2.98 s), and shots that start in the payoff average 6.37 s (Rick 1.57 to 5.37 s; 4 of 5 videos at 1.6 to 2.4 s). [Corrected 2026-11-19: an earlier summary line paired our 6.4 s with Rick's 0.9 to 3.0 s, which are two different measures.]
> 2. **MUSIC.** Rick's bed sits 14 to 18 dB under the voice (mean gap 14.4 to 18.5 dB) and swings 8 to 15 dB with the story (level range 7.8 to 15.0 dB). Ours is 19.1 dB under and flat (5.65 dB). The old rule "constant, about 20 dB under" was our measuring error and is superseded. Key: two independent tools that pass known-answer tests confirm a minor key for 4 of 7 Rick videos (#21 E minor, #22 D minor, #23 D minor, #10 D minor); the other 3 are not confirmed either way and none is confirmed major; ours is F major. [Corrected 2026-11-19: "minor key" was first stated for all of them from one tool.]
> 3. **SETS AND BODIES.** Rick's newest sets carry little edge ink (thin lines, median 2 px, in the surface's own dark colour, on some edges in about 8 of 20 frames; ours measured 7 px). The drawn feel is painted surface detail, where ours has 5 to 13 times less (Laplacian variance: ours 11; Rick 75 to 142 depending on the measurer). His torsos are short and round on long legs (torso 0.72 to 1.05 head widths, legs 0.93 to 1.31); ours are long coats on stubs (torso 1.19 to 1.69, legs 0.11 to 0.17).
>
> Everything else from the research (cutting, captions, mix, poses, FX, script) is in the sections below and in `research/rick-style-spec/new-analysis/`. Verification status of every field: `new-analysis/VERIFICATION_v2_2026-11-19.md`.

Read this first in any new thread. Brief = owner message in that thread (analysis only; NO video creation/render/schedule/post; do NOT edit live checklist or scheduled tasks; do not use the PC GPU while the Salzburg re-render runs).

## Where things are (all private, never in public repo)
- videos/ : all 19 Rick reference mp4s (01-19; #20 has a transcript only, no video on the laptop). Source: laptop Desktop/ModernVistaPrints-Claude-Handoff/rick-reference.
- transcripts/ : 20 YouTube json3 caption files; transcripts/txt/*.words.tsv = word start times, *.txt = plain text.
- prior-analysis/ : earlier laptop study of videos 01-05 (STYLE_STUDY.md, audio measurements).
- frames/<video>/frames-540/ : EVERY frame of the two primaries (#10 bell 1785 f, #14 dragon 1945 f) at 540x960; frames/<video>/sheets/ : labelled 24-frame contact sheets.
- VOCABULARY.md : owner's mandatory design-term list handed to every agent.
- frame-logs/ : Phase 1 per-range agent logs (one file per range, written as each agent finishes).
- metrics/ : per-frame CSV metrics for all 19 videos (scripts/metrics.py).
- Older teardowns (evidence, same videos): ../reference-teardown-bell/, ../reference-teardown-dragon/.
- Our videos to score: handoff/2026-11-17_salzburg-dresden/.
- Shareable scripts: /root/scripts -> vellorz/mvp-media branch (see Phase 5).

## Phases
- [x] 0 Storage  - [x] 1 Frame-by-frame (#10, #14)  - [x] 2 Transitions (#05,#12,#13,#16 + all 17 measured)  - [x] 3 Scripts (all 20)  - [x] 4 Rubric + 95% test (99.4 %)  - [x] 5 Guide, gap report, checklist proposals, scripts pushed

## Work items
(updated below)

## Scores so far
Rick rubric (phase4): 14/14 dimensions >= 95 %, overall 99.4 % (script 95.0, transitions 97.2 lowest). Gap report: Dresden 31 %, Salzburg 28 %.

## Next exact step
see bottom of Work items
- DONE 0a: 19 videos + 20 transcripts copied; frames + sheets extracted for #10 and #14.
- RUNNING 1a: 10 Phase-1 agents (A1-A5 = #10 ranges f1-360, 361-720, 721-1080, 1081-1440, 1441-1785; B1-B5 = #14 ranges f1-384, 385-768, 769-1152, 1153-1560, 1561-1945). Each writes frame-logs/<video>_f<a>-<b>.md. If a log is missing after a restart, re-run only that range with the same prompt (prompt text in frame-logs/_agent-prompt.md).
- NEXT: when all 10 logs exist -> merge into 01_phase1_shot-table.md + measurements.
- DONE 1a (partial): frame logs written for #10 f361-720, f721-1080, f1081-1440, f1441-1785 and #14 f1153-1560. Waiting on #10 f1-360 and #14 f1-384, f385-768, f769-1152, f1561-1945.
- DONE 3a: narration stats for all 20 transcripts -> phase3/narration-stats.md (median 3.75 w/s, max word gap 0.6-1.16 s). Video titles + views in phase3 (to write). Our Dresden/Salzburg VOs transcribed -> our-scripts/ (123/131 words in 48 s = 2.6 w/s).
- DONE 2a: automatic transition detector (scripts/transitions.py, calibrated on #14 ground truth: 18/19 found, 0 false) run on all 19 -> transitions-auto/*.csv.
- 07:20 UTC: rate limit hit at 04:52 (5 agents interrupted) but all 10 Phase-1 logs were written completely (checked: every log states all frames viewed). PHASE 1 DONE.
- DONE Phase 2: phase2/02_transition-study.md (+ dissolve-lengths-17-videos.txt).
- DONE Phase 3: phase3/03_script-study.md + narration-stats.md.
- DONE cross-video measurements: metrics/summary.md (picture), captions on all 19 (caption box top 68.9 %, bottom 71.7 % H, 54 px in 19/19), loudness all 19 (-14.0..-15.1 LUFS, LRA 1.7-3.2), pitch.
- NEXT: write 04_rubric-and-test.md, then rick-master-guide.md, 05_gap-report.md, 06_checklist-proposals.md; push scripts/ to mvp-media branch.
- DONE Phase 4: phase4/04_rubric-and-test.md. Scores: transitions 97.2, pacing 100, character 100, lettering 100, colour 100, composition 99.6, lighting 100, camera 100, motion 100, expression 100, VO 100, music 100 (n=5), script 95.0, ending 100 → overall 99.4 %. 6 rules failed first test and were fixed (section C).
- NEXT: rick-master-guide.md (sections a-k), 05_gap-report.md, 06_checklist-proposals.md, push scripts/ to mvp-media.
- DONE 5: rick-master-guide.md (sections a-k), 05_gap-report.md, 06_checklist-proposals.md (rules 172-191 + changes, NOT applied; renumbered from 154-173 because live checklist ends at 171). Scripts pushed to vellorz/mvp-media branch claude/project-thread-vmgpzb (engine/cartoon-3d/rick-spec/, commit ef96ef1, no PR opened).
- STATUS (2026-11-17 ~08:10 UTC): ALL PHASES DONE. Waiting on owner: approve checklist proposals by number; answer the poster-ending question (06 file, last section). Nothing was rendered, scheduled or posted; live checklist and scheduled tasks untouched.
- NEXT (only after owner approval): apply approved rules to mvp-media CHECKLIST.md/DETAIL_STANDARD.md via PR, update memory checklist file, and point the task prompts at the guide.

## Added 2026-11-19 (appended; nothing above changed)
- Rick's channel: https://www.youtube.com/@RicksClips3000
- The master guide is now version 1.1: v1.0 text unchanged, plus an appended addendum (sections l to q) built from Rick's 5 newest videos (#21 to #25). Where they disagree the addendum wins; section l.9 lists the superseded v1.0 numbers. Read the addendum before building any video.
- The gap report has a new dated ledger entry (2026-11-19: Black Friday round 3 and originals #10/#14 against the newest five).
- All evidence, tools and the run's own resume file: new-analysis/ (start with new-analysis/RESUME_new-analysis.md).
- Hashes after this update: rick-master-guide.md sha256 b955df8d025ecdca55b768b26207f4341cb5bf6cd91f43b0dafb865536d46841 (73,626 bytes; first 33,719 bytes = v1.0, sha256 c96644d1...); 05_gap-report.md sha256 cdb24545af82de51cc5a3ef9ad2cca37cdccda5769e63f5a30f193f8bc2a1016 (13,773 bytes; first 5,409 bytes = previous version, sha256 265cce8a...). Dated copies of every version: versions/ (with SHA256SUMS.txt) and ../rick-style-spec_PROTECTED-COPY_2026-11-17/ledger-snapshots/2026-11-19/.
- The public repo copy (mvp-media, engine/cartoon-3d/rick-spec/master-guide/) still holds v1.0. It was NOT refreshed: publishing needs the owner's approval.
- Proposed rules 230 to 260 and the Black Friday retime table live in experiments/2026-11-18_rick-99-test/ (RULES_PROPOSAL_230plus_from-rick-analysis.md, RETIME_REDESIGN_from-rick-analysis.md). RULES_CONSOLIDATED.md itself is edited only by the Black Friday thread.

## Added 2026-11-19, 99 % verification run (appended; a core-findings block was also added under the title)
- The master guide is now version 1.2: a top block with the three core findings, then v1.1 byte for byte, then an appended addendum (sections r to v: corrections, method 1 values, status table, listening, process rules). Where it disagrees with v1.0 or v1.1, v1.2 wins.
- The gap report has a second 2026-11-19 ledger entry (verification outcome, corrections E, open fields F, what BF round 5 must close G).
- Full verification record: new-analysis/VERIFICATION_v2_2026-11-19.md. Definitions and amendments: new-analysis/_agent-prompts/definitions_v2_2026-11-19.md. Evidence and frozen tools: new-analysis/v2_2026-11-19/.
- Owner decisions on Nov 19: outline width and tempo are marked uncertain with no rule; method 1 values are included as the best available guidance. Owner approved refreshing the repo copy (mvp-media, branch claude/project-thread-4n9bof, engine/cartoon-3d/rick-spec/master-guide/, those files only, never Rick media).
- Hashes after this update are in versions/SHA256SUMS.txt (guide v1.2 and gap report 2026-11-19b) and in ../rick-style-spec_PROTECTED-COPY_2026-11-17/ledger-snapshots/2026-11-19/SHA256SUMS_2026-11-19b.txt.
- Method 1 values, kept at the owner's request (highest agreement of the three methods, still under 99 %, so [uncertain] and not rules):
  - Head outline width (ring scans, 17 of 18 heads = 94.4 %): medium shots 7 to 12 px, wide shots 4 to 5 px, close-ups 12 to 18 px (n = 2) at 1080 px frame width; 2 to 3.5 % of head width. Later methods (two tools, 48 heads): about 2.5 % of the head's skin-fill width (3 px small, 6 to 7 px medium, 10 to 11 px close). Working guidance: 2.5 to 3.5 % of head width, never under 2 %.
  - Tempo (beat tracking on the music stem, 7 of 8 videos = 87.5 %): #21 98.0 BPM, #22 75.6 (or about 113), #23 99.9, #24 86.1 (not corroborated), #25 92.0, #10 99.4, #14 97.3; ours 120.1. Later two-tool values: #23 100.0, #14 96.8, #10 66.7 (the same 7.2 s loop counted as 8 beats instead of 12), ours 120.0. Working guidance: 92 to 100 BPM, not 120.
- Status of every field after this run:
  - Verified: pacing statistics 141 of 141; loudness, voice-to-music gap, level range, duck depth, mix LUFS, true peak 66 of 66; shot boundaries 99.1 % raw with the dissolve tool at 17 of 17; caption cap height, baseline, text, head fill width, luma, camera counts 100 % (round 2); sets and bodies re-measured by a second agent with corrections applied.
  - [uncertain], not rules: bed loop length as a field (6 of 8; two-tool values #21 9.82 s, #22 6.35 s, #23 9.60 s, #10 7.20 s, #14 4.96 s, ours 8.00 s); tempo (three methods: 7 of 8, 5 of 8, 4 of 8); key beyond the four confirmed minor beds (signature 6 of 8, tonic 5 of 8); head outline width (three methods: 94.4 %, void, 77.5 %); instruments, genre, mood, SFX types (no listening tool passes its known answers).
- Listening: the owner proposed github.com/Leonxlnx/earshot. It was reviewed before install (safe: local, pinned weights, nothing uploaded) and tested on known answers. Route 1 (earshot): 0 of 8 instrument questions pass in a full mix; SFX type 58.7 % clean, 23.8 % under music; its tempo and key also fail. Route 2 (Demucs 6 stems plus measurements plus earshot on stems): 1 of 14 questions passes (choir, weak); SFX 60.5 % clean, 14.1 % under music. Route 3 (music taggers on real labelled music under a narrator): still running when this text was written; its result is in `research/rick-style-spec/new-analysis/VERIFICATION_v2_2026-11-19.md`, Addendum B. Nothing from it is used unless it passes its known answers.
- Proposed process rules 261 to 266 and the amended rule 246 are in experiments/2026-11-18_rick-99-test/RULES_PROPOSAL_230plus_from-rick-analysis.md. RULES_CONSOLIDATED.md is edited only by the Black Friday thread.
- Next: BF round 5 gets measured with the same tools and added as the next ledger entry.
- 2026-11-19 18:50 UTC: BF round 5 measured (third ledger entry of the day in 05_gap-report.md, sha256 8942a0bac6edc05533170c6c934f0e2323d186ea2fad0fac725764931bab1d4e): 22 of 41 measures inside Rick's range (round 3: 15). Scene-time shape and bed levels closed; still open: set surface detail 17.9 against 75+, straight arms and upright torsos, legs 0.74 against 0.93 to 1.31 head widths, events inside shots 1.27 per s. Evidence: new-analysis/black-friday-round5/.
