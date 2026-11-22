# r8b (round-7 T7: caption covered walker faces in S02): caption boxes in normalised frame coords (x right, y up, like world_to_camera_view)
import json, sys
from PIL import ImageFont
FONT='/home/user/mvp-media/engine/cartoon-3d/project/public/havasu/fonts/Montserrat.ttf'
d=json.load(open(sys.argv[1])); px=d['font_px']; f=ImageFont.truetype(FONT,px); f.set_variation_by_name('Black')
W,H=1440,2560; BOT=0.717*H; out=[]
for f0,t,f1 in d['captions']:
    w=f.getlength(t)+40   # + outline/shadow margin
    x0=(W-w)/2/W; x1=(W+w)/2/W; yb=BOT+18; yt=BOT-px*0.80-18
    out.append([f0,f1,x0,x1,1-yb/H,1-yt/H,t])
json.dump(out,open('/root/cc/bridge/capboxes.json','w')); print('CAPBOXES',len(out))
