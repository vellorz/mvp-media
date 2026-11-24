from PIL import Image, ImageDraw, ImageFont
import glob, os
FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',30); FR=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
fs=sorted(glob.glob('/root/bcn/gate/castcheck.png/*.png'))
tiles=[]
for f in fs:
    im=Image.open(f).convert('RGB'); bb=Image.eval(im.convert('L'),lambda v:255 if v<170 else 0).getbbox()
    im=im.crop((max(0,bb[0]-20),max(0,bb[1]-20),min(im.width,bb[2]+20),min(im.height,bb[3]+20)))
    s=520/im.height; tiles.append((im.resize((int(im.width*s),520)),os.path.basename(f)[3:-4]))
W=sum(t.width+10 for t,_ in tiles[:12])+20
rk=['r10_f606','r10_f771','r23_f665','r22_f1293']
rt=[Image.open(f'/root/bcn/rick/{r}.jpg').convert('RGB') for r in rk]; rt=[r.resize((int(r.width*620/r.height),620)) for r in rt]
W=max(W,sum(r.width+10 for r in rt)+20)
H=60+2*(520+40)+40+620+60
S=Image.new('RGB',(W,H),(246,243,238)); d=ImageDraw.Draw(S)
d.text((20,14),'Barcelona cast gate: all 24 kinds WHOLE from the real rig (lib.char, rule 336 build: torso 1.00 / legs 1.29 / total 3.29 H, castcheck PASS)',font=FB,fill=(20,20,20))
y=60
for row in (tiles[:12],tiles[12:]):
    x=20
    for t,n in row: S.paste(t,(x,y)); d.text((x+4,y+522),n,font=FR,fill=(50,50,50)); x+=t.width+10
    y+=560
d.text((20,y),'Rick reference frames: '+', '.join(rk),font=FB,fill=(20,20,20)); y+=40; x=20
for r in rt: S.paste(r,(x,y)); x+=r.width+10
S.save('/root/bcn/gate/cast_sheet.jpg',quality=88); print(S.size)