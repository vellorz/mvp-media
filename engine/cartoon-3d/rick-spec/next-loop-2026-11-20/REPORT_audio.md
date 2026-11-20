# AUDIO track report (orchestrator copy of the agent's hand-back, 2026-11-20); data in results.json and evidence/report_out.txt; definitions PREREG_audio_v4.md (amendments A1 to A3 dated with reasons)
Bottom line: every audio field ends [uncertain]. The cause of the bed-swing disagreement was found and fixed (the two tools now agree on 7 of 7), but every bed, key and SFX method fails known-answer tests with the voice on top. Tempo (T2, T3) and loop (L1, L3) pass known answers 7 of 7 but agree on only 5 of 7 real videos.
Known-answer set: 7 mixes we made (6 synthetic beds plus our BF bed) with known key, tempo, loop, gain swing, 12 SFX each; narration 15 to 17 dB over the bed; AAC 128k; same separators as the real stems.
| field | n | before v3/v4 | after v3 | after v4 | known answer | status |
|---|---|---|---|---|---|---|
| bed range max-min | 7 | 57.1/71.4 | 100 | 100 | 2 of 7 within 1 dB | uncertain |
| bed range p95-p5 | 7 | | 100 | 100 | A 3/7, C 0/7, Demucs 2/7 | uncertain |
| closest gap min / p5 | 7 | 57.1/71.4 | 100 | 100 | 1 of 7 | uncertain |
| key K1 vs K2 | 7 | v2 2 of 4 | 85.7 | 85.7 | K1 4/7, K2 5/7, K3 6/7, K4 5/7 | uncertain |
| tempo T2 vs T3 (same beat level) | 7 | v2 2 of 4 | 71.4 | 71.4 | T1 6/7, T2 7/7, T3 7/7 | uncertain |
| loop L1 vs L3 | 7 | v2 3 of 4 | 100 (x2 allowed) | 71.4 | L1 7/7, L2 4/7, L3 7/7 | uncertain |
| SFX onset S1 vs S2 (+-2 f) | 703 | 64.2 (+-1 f) / 68.5 (+-2 f) | | 9.4 | held-out F S1 0.41, S2 0.35, v3 tool 0.59 | uncertain |
Bed swing: the old tool A gated inside each 3 s window (short bursts read 1.7 to 2.7 dB louder at the maximum, #10 and #22); the tools also used different voice gates (-50 vs -40 LUFS) and time grids. With one ungated definition they agree within 0.32 dB on every video. Still not valid: both separators move part of a quiet bed into the vocal stem; range errors -3.8 to +3.1 dB, closest gap up to 4.9 dB too large. Values with about +-4 dB each (p95-p5 / max-min / closest gap p5, dB): #03 8.7/11.7/12.2; #12 7.0/13.3/14.8; #04 7.3/11.8/15.0; #10 11.8/14.3/9.4; #14 10.9/15.5/8.9; #22 10.7/12.1/8.3; #24 8.7/11.1/10.4.
Key (K1/K2/K3, all fail known answers): D minor / D minor / A minor on #12, #04, #10, #22, #24; #14 D minor on all four methods; #03 E minor / D major / A minor. Profile methods confuse relative major/minor (D minor read as F major on a known mix); bass-tonic methods read the dominant.
Tempo T1/T2/T3 (folded to 60-130 BPM): #03 118.8/78.4/78.6; #12 105.5/100.0/104.0; #04 123.1/79.5/80.3; #10 99.4/100.0/66.7 (3:2 split); #14 97.5/96.8/96.8; #22 112.4/75.5/75.7; #24 123.1/87.0/87.0. Raw T2 reads exactly 2x on 5 videos (octave equivalents, not counted).
Loop L1/L3 (s): #03 6.108/6.104; #12 18.473/9.237; #04 5.975/5.967; #10 7.199/14.402; #14 9.938/9.929; #22 6.354/6.352; #24 11.038/11.045 (both misses exact 2x). Beats per loop (L1 x T2): 8, 31, 8, 12, 16, 8, 16.
SFX: S1, S2 and the v3 tool all fail; 19 of 63 short known SFX lose 6 dB or more into the vocal stem; S1 class accuracy 88.9 % vs a 90 % pass mark, so no classes. Lag to picture: 51 picture events have an agreed SFX within +-6 f, median lag 0 f, but a random shift gives about 42 matches (indistinguishable from chance).
