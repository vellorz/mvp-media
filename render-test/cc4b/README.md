# cc4b: Cape Cod round 4, S16 only (framing fix)

Same as cc4 except S16: the three diggers now stay inside the frame for the whole truck (cc4 test S16:1540 had one half out left, one off right, one behind the camera). Work in D:\AI\MVP-render\cc4b; never touch cc4.

1. Join: `copy /b cc.blend.part0+cc.blend.part1 cc.blend`; SHA256 must equal `e3bd09e0a9623318678ec1f95ebb4f2e0acf5fe322a918320537d6072cb450ee` (119435479 bytes).
2. Render S16 only: `blender.exe -b cc.blend --python pcrender.py -- D:\AI\MVP-render\cc4b\frames S16`
3. Encode: `blender.exe -b --python pcencode.py -- D:\AI\MVP-render\cc4b\frames D:\AI\MVP-render\cc4b\clips`
4. Push `clips/S16.mp4` to `render-test/cc4b/clips`.
