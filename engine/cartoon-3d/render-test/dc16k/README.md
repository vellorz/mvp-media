# dc16k: Washington DC short, 4-shot follow-up after the owner's-eye pass on dc16j
Re-render ONLY S02 S04 S11 S18 (578 frames). Fixes: S02/S11 the thrown letter is a crumpled ball for its whole arc and lands in an OPEN wastebasket (no flat-letter-to-ball pop, no lid);
S04 one bag only (the one in his hand), no second sack popping in; S18 Lincoln holds the stamp from the first frame (no envelope-to-stamp pop), stamp held above the page until the strike.
Join in D:\AI\MVP-render\dc16k (never C:): copy /b dc.blend.part0+dc.blend.part1 dc.blend ; certutil -hashfile dc.blend SHA256 must equal dc.blend.sha256 (174952225 bytes).
Test: blender.exe -b dc.blend --python pctest.py -- D:\AI\MVP-render\dc16k\test S02:130
Render: blender.exe -b dc.blend --python pcrender.py -- D:\AI\MVP-render\dc16k\frames S18 S02 S04 S11
Encode: blender.exe -b --python pcencode.py -- frames clips ; push clips/ and test/ to render-test/dc16k/ on claude/project-thread-v5jm25.
