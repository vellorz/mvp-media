# Two-person hand-labelled actions (loop 3, Track 2), 2026-11-20
Definitions: ../_agent-prompts/definitions_v5_2026-11-20.md. Windows: windows.json (100 x 36 frames, seed 2026112005, 7 videos). Labels: out/A_*, B_*, C_* (three blind Sonnet labellers; each labelled in two halves). Consensus: consensus_v5.json. Scoring: inline script in the session (matching by time overlap).
## Agreement (matched actions, tolerance in frames)
| pair | matched | start +-2 | end +-2 | start +-3 | end +-4 | same type |
|---|---|---|---|---|---|---|
| A vs B | 238 | 81.1 | 78.6 | 89.1 | 85.7 | 68.1 |
| A vs C | 254 | 80.3 | 77.6 | 85.0 | 85.4 | 70.5 |
| B vs C | 241 | 81.7 | 75.5 | 88.0 | 85.9 | 71.4 |
Actions found: A 302, B 282, C ~299; A vs B matched 78.8 % of A and 84.4 % of B; strict same-set rate 68.8 %. Window "has an action or not" agree A vs B 92 of 100. Overshoot: labellers said yes on 5 (A), 0 (B): not usable.
Status: start and end timing GUIDANCE at +-2 f (75.5 to 81.7 %, three pairs) for items both labellers found; NOT rule. Action type agreement 68 to 71 % (UNCERTAIN as a per-item field). Whether every small action is found: UNCERTAIN (about 69 %).
## Consensus (2 of 3 within 2 f on A's 302 actions): 164 items
Median travel f (p10 to p90): face change n 81: 3 (1 to 4.5); gesture 21: 4 (3 to 6); mouth change 17: 4.5 (2 to 35); tween 14: 6.5 (4 to 35); walk 14: 9.5 (5.5 to 35); fall 7: 9 (4 to 18); turn 3: 10; cycle 3: 11. snap n 1 (labellers rarely used "snap" for small pose changes: type vocabulary differs from the earlier first-measurer logs).
## Disclosures
- Labellers lost image context mid-run (request limits): A labelled w000 to w020 partly from notes, B w094 to w099 and parts of w000 to w049 from notes; labeller C wrote each window to disk right after viewing it (C is the most reliable). Disputes over 2 f affect 83 of 100 windows.
- Only 5 of the 20 "still camera" windows are truly still (15 are the stillest available), so a locked-camera rate cannot be given separately. Captions inside crops, and unseen dissolves, add noise.
- Models: Sonnet for all labellers, Opus built the packs. Not blind to the human first-measurer logs only in the sense that nobody opened them (stated by each agent).
