#!/bin/bash
# one tracked cloud render chunk (<= 7000 s), resume-safe: drop 0-byte placeholders left by a killed frame first
OUT=/root/dc/render/2k
mkdir -p $OUT; find $OUT -name 'f_*.png' -size 0 -delete
cd /root/dc && timeout 7000 ./blender-4.2.3-linux-x64/blender -b blend/dc.blend --python src/cloudrender_dc.py -- $OUT 100 4 "$@" 2>&1 | grep -E "SHOT_|ALL_DONE|Error|Fra:.*Saved" | grep -v "^Fra" ; find $OUT -name 'f_*.png' -size +0 | wc -l
