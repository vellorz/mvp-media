# dc16c: Washington DC short, S20-ONLY fix (supersedes the S20 clip of dc16b)
S20 dad's face had a flat dark band from the eye line down: his D3 light stubble was drawn as one translucent band. Now approved stubble dots (333b). Same cameras and staging as dc16b.
Join in D:\AI\MVP-render\dc16c (never C:): copy /b dc.blend.part0+dc.blend.part1 dc.blend ; certutil -hashfile dc.blend SHA256 must equal dc.blend.sha256 (174744690 bytes).
Test: blender.exe -b dc.blend --python pctest.py -- D:\AI\MVP-render\dc16c\test S20:1960
Render: blender.exe -b dc.blend --python pcrender.py -- D:\AI\MVP-render\dc16c\frames S20
Encode: blender.exe -b --python pcencode.py -- frames clips ; push clips/ and test/ to render-test/dc16c/ on claude/project-thread-v5jm25.
