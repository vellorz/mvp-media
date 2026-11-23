# usage: tiltfit.sh SHOTS...   rebuild + facebox only those shots
cd /root/dc && B=blender-4.2.3-linux-x64/blender
$B -b --python src/scene_dc.py > bl14.log 2>&1; grep -q SCENE_OK bl14.log || { tail -5 bl14.log; exit 1; }
$B -b blend/dc.blend --python src/facebox_dc.py -- /tmp/fb.json "$@" 2>/dev/null | grep -E "FACECUT|CAPCLASH|HEADW"
