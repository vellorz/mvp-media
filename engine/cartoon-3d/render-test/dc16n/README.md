# dc16n: Washington DC short, S02 + S11 only (eye-pass B1/B3: paper balls appeared mid-air)
Re-render ONLY S02 S11 (368 frames). Fix: each crumpled paper ball is born in the thrower's mitten at the start of the throw, rides the hand, and flies one arc into the open bin.
Join in D:\AI\MVP-render\dc16n (never C:): copy /b dc.blend.part0+dc.blend.part1 dc.blend ; certutil -hashfile dc.blend SHA256 must equal dc.blend.sha256 (174764623 bytes).
Test: blender.exe -b dc.blend --python pctest.py -- D:\AI\MVP-render\dc16n\test S02:101
Render: blender.exe -b dc.blend --python pcrender.py -- D:\AI\MVP-render\dc16n\frames S02 S11
Encode: blender.exe -b --python pcencode.py -- frames clips ; push clips/ and test/ to render-test/dc16n/ on claude/project-thread-v5jm25.
