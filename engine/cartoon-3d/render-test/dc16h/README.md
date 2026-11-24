# dc16h: Washington DC short, ROUND 3 FIX (rules 365, 372-378; payoff + visual verifier criticals and owner's-eye NOs on dc16g)
Re-render ONLY these shots: S01 S02 S03 S04 S07 S08 S10 S11 S12 S13 S14 S18 S19 S20 S21. The other shots keep their clips.
Fixes: S18 stamp hangs face-down and lands on a flat proclamation, red YES imprint appears under it; S04 mail heap is envelopes only (no boulder, no puffs);
mail sacks gathered neck + U.S. MAIL label; inkwell quill = the same feather quill; S02 bin top no longer flickers, letters land as crumpled balls;
writing fist lifted clear of the page; turkey redrawn (drumsticks, frills); S19 goatee -> chevron mustache; S20 edge-on plate removed; S19/S20 foreground chair; S14 close-up mitten smaller and flat.
Join in D:\AI\MVP-render\dc16h (never C:): copy /b dc.blend.part0+dc.blend.part1 dc.blend ; certutil -hashfile dc.blend SHA256 must equal dc.blend.sha256 (175573127 bytes).
Test: blender.exe -b dc.blend --python pctest.py -- D:\AI\MVP-render\dc16h\test S18:1700
Render: blender.exe -b dc.blend --python pcrender.py -- D:\AI\MVP-render\dc16h\frames S18 S04 S02 S19 S20 S21 S14 S01 S10 S13 S03 S11 S12 S07 S08
Encode: blender.exe -b --python pcencode.py -- frames clips ; push clips/ and test/ to render-test/dc16h/ on claude/project-thread-v5jm25.
