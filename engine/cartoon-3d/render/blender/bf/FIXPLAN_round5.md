# Round 4 verification result (Nov 19 2026, video bf_r4_2k.mp4, GPU render bf8)
Items: visual 19/23, shots 18/21, text 13/13, audio 21/25 (rows incl. v1.1 views), payoff 23/23 = 94/105 (89.5 %). FAIL.
Critical fails: P3/R21 (S16 frontal shopper line-up 1596-1690, no FG), R13 (only 3/14 dissolves bridged within 5 %).
Closeness to Rick ~72 % (r3 70 %).
## Fix list for round 5 (on top of the round-5 build already in progress)
1 [P3/R21/L9] S16 crowd: depth stagger, 3/4 turns, varied gestures, FG layer; also S04 480-510 FG; S05 528-600 frontal two-shot.
2 [R13/K6] bridges: >= half of dissolves same shape/spot within 5 % (round 5 bridges.py: check BRIDGES_OK count on the new 22-shot cut).
3 [K8] crash push timing vs nouns; move landings on nouns +-3 f (5/9 now).
4 S14 unplanned hard cut 1403->1404 mid-phrase "was the day" -> round 5 cut list must put it on a phrase/word by design (v1.1 allows cuts off phrase starts but it must be planned).
5 S13 writing: red total, labels, TOTAL appear with no pen near; caption covers TOTAL 1345-1373 -> pen writes each, keep total line above 66 % H.
6 Lettering cut by frame edge: S12 calendar 1134-1152, wall chart 1158-1212, S14 ledger left page 1362-1403.
7 Heads cut by frame edge: S03 318-384, S06 744-774, S16 1578-1590, 1704-1716. FG cars too close S01 138-150, S02 226-240; S08 mailbox slides out 870-930.
8 S15 flat pure-black pole on left edge 1488-1554 (2.9-7.1 %); cop glove gap.
9 Payoff: poster partly hidden 1593-1679 (bay post, frame edge, granny head); poster washed (grey 137 vs 117); readable hold only 0.83 s; payoff dim (luma 0.25).
10 S10 nearly blank white blur (edge 0.107).
11 Audio v1.1: bed 14-18 dB under with 8-15 dB swings (round-5 music/mix already target this; re-measure), BPM 92-100, >= 55 % energy < 250 Hz; whistle f8 2-5 kHz +16 dB over bed: soften. sfxcheck.py BUG: stereo SFX downmix adds +3 dB vs mono VO -> fix channel handling. Record the exact generated VO tags (V2).
12 Captions v1.1 tempo: 2.8-3.1 swaps/s, mean 0.32-0.36 s, P90 <= 0.57 (round-5 post.py: 162 cards mean 0.36 P90 0.54, re-measure). "CANCELLED" -> "CANCELED". Script punctuation ("game, so cars").
13 Style gaps: painted wall detail (0.9-8.5 vs >= 75), bodies (torso 1.24 H, legs stubs, elbows 180 deg) -> round-5 cast/paint changes; shot shape (v1.1): <2 s >= 20 %, >4 s <= 26 %, one shot < 1.3 s, >= 2 joins in last tenth.
