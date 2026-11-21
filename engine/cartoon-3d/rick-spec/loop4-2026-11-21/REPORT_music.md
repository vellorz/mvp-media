# Loop 4: music choice and mood (definitions v6 section 8), 2026-11-21. Opus measurer hand-back saved by the orchestrator. Files here: PREREG_music_v6.md (written before tool output, amendment A1 on genre mapping before scoring), known_answer/, real_values.json/.txt, results.json, storybeats.json, LISTENING_SHEET.md, _tools/.
## Bottom line
Every field ends UNCERTAIN; none goes into the guide as guidance. Known-answer set: 24 own MIDI beds (8 melodic house, 4 UK garage, 4 orchestral, 3 cartoon, 5 others; all 8 moods x3; 11 of 12 tonics) mixed under our own narration at a 14 to 19 dB gap, Rick-like chain (compressor, treble shelf, -14 LUFS, limiter, AAC 128k), two separators.
| field | mark | methods that pass the known answer | best failing |
|---|---|---|---|
| key and mode | 90 % | none (9 methods) | 70.8 % with voice, 75 % clean |
| tempo | 90 % | T3 (1.00/.958/1.00), TC Essentia | TA .875 |
| loop length | 90 % | L1, L3 | L2 .833 |
| mood | 75 % | none | .208 |
| genre | 75 % | none | .375 |
| instruments | 75 % | none | .582 |
| beat energy change | 75 % | EA .903, EC .847, EB .764 | |
| beat density | 75 % | none | .611 |
## Rick's 7 videos (two passing methods)
tempo T3 vs TC within 3 BPM 4/7 (57.1 %); loop L1 vs L3 5/7 (71.4 %); beat-energy change 5/7 (71.4 %, per boundary 19/21); key KC vs KE 6/7 (both failed known answers); mood, genre, instruments 0/7 (failed known answers). All UNCERTAIN.
Per video tempo T3/TC BPM: #03 78.6/78.3; #12 104.0/103.9; #04 80.3/118.0; #10 66.7/99.5; #14 96.8/96.4; #22 75.7/112.5; #24 87.0/86.2. The three tempo disagreements (#04, #10, #22) are exact 3:2 ratios (beat level ambiguity, perhaps a triplet or swung feel). Loop L1/L3 s: #03 6.11; #12 18.47/9.24 and #10 7.20/14.40 (exact 2x); #04 5.98; #14 9.94; #22 6.35; #24 11.04.
Beat energy (bed level change into the payoff, UVR/Demucs dB): #03 +7.5/+6.3; #12 +3.8/+4.3; #04 +8.6/+10.7; #14 +8.5/+9.2; #22 +4.3/+4.5; #24 +3.0/+3.4; #10 -2.3/-3.1: the bed gets LOUDER at the payoff in 6 of 7 videos (UNCERTAIN under the strict rule; two videos sit near the 3 dB threshold). Climax starts 38.4 to 54.4 s, payoff 53.9 to 63.4 s (storybeats.json).
Key by profile tools: D minor on 5 of 7 (#12, #04, #10, #14 partly, #24), E minor on #03; confuses D minor with F major. Mood: Essentia says calm/mysterious, CLAP says comic/melancholic: no agreement. Genre: Essentia ambient (5 of 7), CLAP UK garage (4 of 7): no agreement.
## Listening sheet for the owner: LISTENING_SHEET.md (6 questions: beat speed, seconds until the music repeats, minor or major and home note, mood word, genre and instruments, louder/quieter/busier at build-up, climax, payoff; timestamps for all 7 videos).
## Disclosures
Opus ran everything; essentia-tensorflow, CLAP (laion larger_clap_music_and_speech) and fluidsynth installed free, none blocked. Own GM-soundfont beds may be a poor test for learned models. EC cannot run on Rick's videos (voice gaps too short in the start beat).
