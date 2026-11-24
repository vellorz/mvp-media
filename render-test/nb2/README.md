# nb2: Nuremberg Christkindlesmarkt (Fri Nov 27) - round 2 PC GPU render package, all 18 shots

Work in D:\AI\MVP-render\nb2 with absolute D: paths only. One GPU job at a time; never stop another program; delete nothing.

1. Join: `copy /b nb.blend.part0+nb.blend.part1 nb.blend`; SHA256 must equal `8bb773c3dafdccbd9488cc5907a13709a25a5a38ab4493c3a2c0548a354e5999` (53693510 bytes).
2. Test: `blender.exe -b nb.blend --python pctest.py -- D:\AI\MVP-render\nb2\test S04:450 S11:1230 S17:1690 S18:1830`
3. Render all shots (resume-safe): `blender.exe -b nb.blend --python pcrender.py -- D:\AI\MVP-render\nb2\frames`
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\nb2\frames D:\AI\MVP-render\nb2\clips`
5. Pull/merge branch `claude/project-thread-7rv8u4`, then push `clips/*.mp4` and `test/*.png` to `render-test/nb2/clips` and `render-test/nb2/test`.

Film: 1906 frames (0-1905), 18 shots, 1440x2560 @ 30 fps; each shot renders with only its own CHR_<shot> collection and its own camera.
S04 (332-505) holds three camera setups with hard cuts inside the shot (A 332-422, B 423-476, C 477-505; constant keys at 422/476). Render it as one shot as usual.

Round 2 (rule 365: one batched render after the nb1 verifier round). Changes: every cast skin regenerated to (248,230,214) (rule 355);
captions never move (rule 344), heads kept out of the caption band by staging (frameprobe2: 0 band hits); S03 magnifier/box stand;
S04 split into three setups (K1) with partyC removed (she hid behind a nearer head or sat cut at an edge in every placement);
S09 hand off the table; S12/S16 signs hung from bars; S12 ghost outline + lavender fill; S13/S04 party pair out of the desk;
S16 smaller recipient; S17 crane opens with the crowd under the caption band; S18 candles arm drops after "candles"; stall fill light.
Checks on the built scene: contactcheck PASS (0 faults), rigcheck 0 on the changed shots, frameprobe2 band 0 / edge only the S17 crane exit and the S18 exit.
