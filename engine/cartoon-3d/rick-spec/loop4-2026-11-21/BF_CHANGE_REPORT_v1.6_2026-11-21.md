# Black Friday: what the build must change after guide v1.6 (diff-style; nothing is rebuilt by the analysis thread) 2026-11-21
Sources: rick-master-guide.md v1.6 (sha 81da3999...), RENDER_SPEC_v1.5.md (new-analysis-5) with RENDER_SPEC_v1.4.md and RULES_CLONE_v2.md (new-analysis-3), earlier BF_CHANGE_REPORT_2026-11-20.md (new-analysis-2). Status words: GUIDANCE (75 %+), [INFERRED] (soft), UNCERTAIN (no target). Where a line here differs from the Nov 20 report, this one wins.
## Cast and bodies (round 8 cast, bf12)
- torso 1.0 H (keep); legs 1.1 to 1.3 H (was 1.25 to 1.3); total 2.9 to 3.35 H (was 3.2 to 3.35). Keep noodle arms with no elbow, chord/arc about 0.7 to 1.0; mitten hands about 10 to 12 % H, no fingers [RULE]. Outline 7 to 10 px lit, 13 to 16 px shaded at 1080 wide, ink #321c2a.
- No squash and stretch on any character; cutout parts rotate rigidly.
## Motion (replace generic timings)
- Use the named-action table in RENDER_SPEC_v1.5 section A: turn 4.5 f, react 5, point 5, lift 6, sit 6.5, stand 7, emote/talk 7 to 7.5, throw 8 with anticipation, pull 9, fall 10.5 ease-in no bounce, drop 13.5, push 13.5, recoil snap, catch 3. Window +-2 f. Holds median 26 f. Snap 1 to 4 f or tween 5 to 11 f stays.
- Anything Rick never shows (sneak, run, stumble, carry, wave) uses INFERRED_RECIPES.md; check by eye.
## Assets and FX
- Durations (f): drift 28.5, burst 14, fall 12.5 ease-in no bounce, rotate 9.5, slide 19, flow 29, loop 38, sway 25; flat FX 12 to 27. Everything on ones [RULE]. Gravity about 4.7 to 5.1 screen heights per s^2.
## Camera
- Moving on at least 85 % of frames, never fully still over 1 s except the ending hold; durations as v1.4 (push-in 23 to 142, pull-out 25 to 120, crash push 8 to 13, jolt 6 to 7). Scale targets soft: push-in 1.3 to 1.4, pull-out 0.6 to 0.8. No target for roll, layer shift or parallax: let the 3D scene provide it.
## Joins and timing (unchanged from v1.4)
- Dissolves 5 to 12 f median 8, smoothstep, payoff about 12 f, about 40 % match; hard cuts free; start dissolves on sentence starts; shortest shot 10 f; shots under 2 s 10 to 53 %, over 4 s 20 to 47 %.
## Audio
- -14.0 to -14.1 LUFS, true peak -1.9 to -2.2 dBTP; bed 14.4 to 18.6 dB under the voice, std 2.3 to 4.0 dB, no ducking; bed LOUDER into the payoff (+3 to +10 dB in 6 of 7 Rick videos) [GUIDANCE-level direction, UNCERTAIN size]. Music [INFERRED]: loop-based minor bed, 80 to 100 BPM, 6 to 11 s loops; the owner brief (melodic house / UK garage, punchy bass) wins.
## Rules to fold into RULES_CONSOLIDATED.md (BF thread owns it)
RULES_CLONE_v2.md KEEP/REVISE/RETIRE lists plus camera rules 302 to 305; check draft rules 267 to 279 and 288 to 294 against it; retire the unique-character look (S9, 184, 193, 205 numbers) as listed there.
## Round 7 verifier criticals still open (from the BF thread's own report): cop brows on the visor band, 8 hard cuts over the old maximum of 5 (that maximum is now retired: hard cuts are free), caption over walker faces in S02 f198-218, shopper row S16 f1646-1687.
