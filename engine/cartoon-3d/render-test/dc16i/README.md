# dc16i: Washington DC short, S18-ONLY follow-up to dc16h (render right AFTER dc16h)
Re-render ONLY S18 (1638-1732, 95 frames). Fix: the 'present' move after the stamp stretched his free arm flat along the desk (PC test f1700); removed, the free arm now hangs.
Join in D:\AI\MVP-render\dc16i (never C:): copy /b dc.blend.part0+dc.blend.part1 dc.blend ; certutil -hashfile dc.blend SHA256 must equal dc.blend.sha256 (175021280 bytes).
Test: blender.exe -b dc.blend --python pctest.py -- D:\AI\MVP-render\dc16i\test S18:1700
Render: blender.exe -b dc.blend --python pcrender.py -- D:\AI\MVP-render\dc16i\frames S18
Encode: blender.exe -b --python pcencode.py -- frames clips ; push clips/ and test/ to render-test/dc16i/ on claude/project-thread-v5jm25.
