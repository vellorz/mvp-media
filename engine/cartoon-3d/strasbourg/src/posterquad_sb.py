# r5 (poster true colour): projected corners of the poster plane per S22 frame from the payoff cut on -> /root/sb/bridge/posterquad_sb.json (post.py pastes the shop file there)
import bpy, json
from bpy_extras.object_utils import world_to_camera_view as w2c
sc=bpy.context.scene; SH=json.loads(sc['shots']); cam=bpy.data.objects['cam_S22']; po=bpy.data.objects['poster']; out={}
for f in range(SH['S22'][0],SH['S22'][1]+1):
    sc.frame_set(f); out[f]=[[round(c,5) for c in w2c(sc,cam,po.matrix_world@v.co)[:2]] for v in po.data.vertices]
json.dump(out,open('/root/sb/bridge/posterquad_sb.json','w')); print('POSTERQUAD',len(out))
