# CAST GATE sheet: Rick reference frames + full-body cast (castsheet_full.py output) + expression grid. usage: castgate_sheet.py OUT.png TITLE
import sys,json
sys.path.insert(0,'/root/dc/src15'); import expressions as X
from PIL import Image,ImageDraw,ImageFont
R='/mnt/project-files/modern-vista-social/research/rick-style-spec/frames'; CI=json.load(open('/root/dc/src15/cast.json'))
fs=[('10_GM9UKnZ6JFw',409),('10_GM9UKnZ6JFw',587),('10_GM9UKnZ6JFw',757),('14_VS1Z_Q-Klt8',219),('14_VS1Z_Q-Klt8',695),('14_VS1Z_Q-Klt8',857)]
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',30); F2=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
cast=Image.open('/root/dc/castgate/cast_full.png').convert('RGB'); W=2880
top=Image.new('RGB',(W,60+853+50),(236,228,216)); d=ImageDraw.Draw(top)
d.text((10,14),sys.argv[2]+' | RICK REFERENCE FRAMES (research/rick-style-spec/frames, video#frame):',fill=(40,24,36),font=F)
for i,(v,f) in enumerate(fs):
    im=Image.open(f'{R}/{v}/frames-540/{f:04d}.jpg').convert('RGB').resize((480,853)); top.paste(im,(i*480,60)); d.text((i*480+10,60+853+8),f'{v[:2]}#{f:04d}',fill=(40,24,36),font=F)
HP=150; ex=Image.new('RGB',(W,60+3*(HP+70)),(236,228,216)); de=ImageDraw.Draw(ex)
de.text((10,14),'EXPRESSIONS per character: neutral / shock (surprised) / grin (laughing), the same head cards as the scene',fill=(40,24,36),font=F)
for i,k in enumerate(CI):
    x0=(i%6)*480; y0=60+(i//6)*(HP+70)
    for j,fk in enumerate(['neutral','shock','grin']):
        h=Image.open(f'/root/dc/tex15/{k}_h_{fk}.png').convert('RGBA'); _pt=X.pads(CI[k])[0]; _s=HP/1024; h=h.resize((HP,int(h.size[1]*_s)),Image.LANCZOS); ex.paste(h,(x0+10+j*(HP+5),y0-int(_pt*_s)),h)   # round 3: taller head PNGs (pads) keep their scale, hat tops rise above the row
    de.text((x0+12,y0+HP+8),k,fill=(40,24,36),font=F2)
out=Image.new('RGB',(W,top.height+cast.height+ex.height),(236,228,216)); out.paste(top,(0,0)); out.paste(cast,(0,top.height)); out.paste(ex,(0,top.height+cast.height))
out.save(sys.argv[1]); print('GATESHEET',out.size)
