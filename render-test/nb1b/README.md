# nb1b: Nuremberg fix package, shots S04 and S07 only (partyC stubble band)

Work in D:\AI\MVP-render\nb1b with absolute D: paths only. Run after nb1 has finished. One GPU job at a time; never stop another program; delete nothing.

1. Join: `copy /b nb.blend.part0+nb.blend.part1 nb.blend`; SHA256 must equal `8a6414b7ca3c6eb80a152337dcd8d303ccd1cccd274ac22fc468481d3871f255` (54600727 bytes).
2. Test: `blender.exe -b nb.blend --python pctest.py -- D:\AI\MVP-render\nb1b\test S04:420 S07:770`
3. Render the two shots (resume-safe): `blender.exe -b nb.blend --python pcrender.py -- D:\AI\MVP-render\nb1b\frames S04 S07`
4. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\nb1b\frames D:\AI\MVP-render\nb1b\clips`
5. Push `clips/*.mp4` and `test/*.png` to `render-test/nb1b/clips` and `render-test/nb1b/test` on branch `claude/project-thread-7rv8u4` (pull/merge the branch first).

Why: the nb1 PC test frame S04:420 showed a flat horizontal band across partyC's lower face (the D3 stubble was a flat-topped chord). It is now a feathered jaw crescent that follows the chin. partyC appears only in S04 (332-505, 174 f) and S07 (725-815, 91 f): 265 frames. Post takes S04/S07 from nb1b and every other shot from nb1.
