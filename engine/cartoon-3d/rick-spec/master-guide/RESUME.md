# RESUME — Rick Master Guide run (thread "Build the Rick master guide", started 2026-11-17 04:39 UTC)
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
