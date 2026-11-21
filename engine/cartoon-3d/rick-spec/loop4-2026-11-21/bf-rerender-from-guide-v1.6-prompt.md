<context>
You are the Black Friday / Philadelphia 99 % Rick-style test video thread (cartoon-3d, Blender Cycles, 2K master 1440x2560) for Modern Vista Prints. The owner has lifted the pause: re-render the video as close to Rick's style as possible. Owner direction (Nov 20): CLONE Rick's style completely (characters, sets, motion, camera, timing, audio); where our approach differs, Rick wins. Never copy his footage, lines or music. The mvp-media repo is PUBLIC: no Rick frames, media or transcripts in it.
Starting state: bf12 package (mvp-media commit 63df7d7, branch claude/project-thread-c13biq): Rick-build cast plus round-7 fixes, probes clear (ARMPROBE 0, CAPPROBE 0, occ 0, float 0, walkclip 0, ledger 0), round-7 verifiers 90/103, closeness to Rick about 70 %. Round-7 criticals still open: cop brows on the visor band, caption over walker faces S02 f198-218, S16 shopper row f1646-1687; "8 hard cuts" is no longer a fault.
Read first, in this order: research/rick-style-spec/RESUME.md; new-analysis-5/BF_CHANGE_REPORT_v1.6_2026-11-21.md (your change list); new-analysis-5/RENDER_SPEC_v1.5.md and new-analysis-3/RENDER_SPEC_v1.4.md; new-analysis-3/RULES_CLONE_v2.md; rick-master-guide.md v1.6 (sha256 81da39996fbf45bb08de9c9d00ca454513f64ccd1799ae7b9a8f26a174dc8b7b) as the evidence behind the numbers; 05_gap-report.md (entries O, P, Q). Status words: RULE 99 %+, GUIDANCE 75 %+, [INFERRED] soft target, UNCERTAIN no target.
Owner standing rules: auto-approve routine steps (render, encode, push, continue); for PC renders chain render, encode and push in one job and stay with it. Gate 2: the owner approves the finished video before anything is scheduled or posted. Scheduled tasks stay paused. Poster fully visible inside the payoff scene, no "on your wall" line. VO ElevenLabs Drew on eleven_v4; no chart songs.
</context>

<task>
Round 9 (bf13): apply the change list in BF_CHANGE_REPORT_v1.6 to the bf12 scene, then render and verify.
1. Fold RULES_CLONE_v2.md into RULES_CONSOLIDATED.md on your branch: KEEP/REVISE/RETIRE as written, camera rules 302 to 305, and check your drafts 267 to 279 and 288 to 294 against it. Retired rules stay listed in a Retired section with the date.
2. Cast and motion: legs 1.1 to 1.3 H, total 2.9 to 3.35 H, noodle arms, no squash and stretch; retime character actions to the named-action table (turn, react, point, lift, throw with anticipation, fall ease-in no bounce, and so on); use INFERRED_RECIPES.md for anything Rick never shows.
3. Camera and joins: moving on at least 85 % of frames, no still over 1 s except the ending hold, push-in/pull-out durations from the spec, soft scale targets; dissolves 5 to 12 f smoothstep, hard cuts free.
4. Audio: -14 LUFS, bed under the voice 14.4 to 18.6 dB with std 2.3 to 4.0 dB, no ducking, bed louder into the payoff; music loop-based minor bed, 80 to 100 BPM, 6 to 11 s loops, owner brief wins.
5. Fix the three open round-7 criticals; keep every probe at zero; run the verifiers (visual, shots, text, audio, payoff) and the scorecard in RENDER_SPEC_v1.5 section G; report the 41-row table against the v1.6 ranges as a new gap-report ledger entry (append only; tell the Rick analysis thread to merge it).
6. Render on the PC (chain render, encode, push), then QA, then stop at Gate 2 for the owner.
</task>

<constraints>
- Deliver only the above. No new styles, no unrelated refactors. Keep the guide and gap report append-only: NEVER delete, overwrite, shrink or compact them; stop and ask before deleting any file or touching scheduled tasks.
- Numbers marked UNCERTAIN or [INFERRED] are soft: do not fail the render on them; judge by eye and say so.
- Every claim of a count, score or "done" needs tool output behind it. Update your checklist as steps finish.
- Final reply: what changed (diff-style), probe results, verifier scores, scorecard table, files and sha256, what still differs from Rick, and the ask for Gate 2.
</constraints>
