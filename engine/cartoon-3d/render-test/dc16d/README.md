# dc16d: Washington DC short, 12-SHOT FIX ROUND (rules 365, 372-378; owner's-eye pass on dc16f)
Re-render ONLY these shots: S01 S03 S04 S07 S09 S10 S13 S14 S16 S18 S19 S20 (1,167 frames). The other 9 shots keep their dc16/dc16b clips.
Fixes: one writing setup (hand-held quill, tip on the page, words appear behind it) in S01 S10 S13 S14; S16 mailman walks with steps (walk v3 toward camera) and an unlit stance-sized shadow blob; S07 lamb trots; mail bag, rubber stamp and printer's apron redrawn; spilled letters (S04); S09 printer out of the press; S18 stamp lands on the proclamation; S19/S20 edge-on plate and tiny fork removed; S03 reach arm curved (rule 350); character cards cast no lamp shadows (367c).
Join in D:\AI\MVP-render\dc16d (never C:): copy /b dc.blend.part0+dc.blend.part1 dc.blend ; certutil -hashfile dc.blend SHA256 must equal dc.blend.sha256 (176417238 bytes).
Test: blender.exe -b dc.blend --python pctest.py -- D:\AI\MVP-render\dc16d\test S14:1420
Render: blender.exe -b dc.blend --python pcrender.py -- D:\AI\MVP-render\dc16d\frames S01 S03 S04 S07 S09 S10 S13 S14 S16 S18 S19 S20
Encode: blender.exe -b --python pcencode.py -- frames clips ; push clips/ and test/ to render-test/dc16d/ on claude/project-thread-v5jm25.
