# dc16b: Washington DC Thanksgiving short, SHOT FIX package (rule 365e: only the shots the dc16 verifiers failed)
Re-render ONLY S03, S04, S16, S19 and S20. Everything else stays the dc16 clips.
- S03: the clerk's straight point (rule 350) replaced by lean_reach.
- S04: double_take starts at f370 so the snap lands before the cut at 411.
- S19/S20: milder high three-quarter cameras (pitch ~17/16 deg, was ~27/26) so legs are not foreshortened under the rule 336 medians (coordinator ruling); S20 grandma and mom 0.35 m left so dad clears mom.
- S16: the townswoman stands on camera so her startle_recoil shows; S16 ground blobs use a lighter lit shadow texture (no flat plum band).
Join in D:\AI\MVP-render\dc16b (never C:): copy /b dc.blend.part0+dc.blend.part1 dc.blend ; certutil -hashfile dc.blend SHA256 must equal dc.blend.sha256 (174774293 bytes).
Test: blender.exe -b dc.blend --python pctest.py -- D:\AI\MVP-render\dc16b\test S03:198 S04:404 S16:1584 S19:1890 S20:1960
Render: blender.exe -b dc.blend --python pcrender.py -- D:\AI\MVP-render\dc16b\frames S03 S04 S16 S19 S20
Encode: blender.exe -b --python pcencode.py -- frames clips ; push clips/ and test/ to render-test/dc16b/ on claude/project-thread-v5jm25.
