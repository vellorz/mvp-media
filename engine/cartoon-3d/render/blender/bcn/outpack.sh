#!/bin/bash
# outpack.sh R  -> /root/cc/out/cc_rR_small.mp4 (<10 MB), out/rR/f6/f_NNN.png (every 6th frame, 360x640), out/rR/sheet_N.jpg
R=$1; O=/root/cc/out; M=$O/cc_r${R}_2k.mp4; D=$O/r$R; mkdir -p $D/f6
ffmpeg -v error -y -i $M -vf scale=540:960:flags=lanczos -c:v libx264 -preset slow -b:v 1050k -maxrate 1300k -bufsize 2600k -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart $O/cc_r${R}_small.mp4
ffmpeg -v error -y -i $M -vf "select=not(mod(n\,6)),scale=360:640:flags=lanczos" -vsync vfr $D/f6/f_%03d.png
python3 - $D <<'PY'
import sys,glob,os
from PIL import Image, ImageDraw, ImageFont
D=sys.argv[1]; fs=sorted(glob.glob(D+'/f6/f_*.png'))
for i,f in enumerate(fs): os.rename(f, D+'/f6/f_%03d.png.tmp'%i)
for f in sorted(glob.glob(D+'/f6/*.tmp')): os.rename(f,f[:-4])
fs=sorted(glob.glob(D+'/f6/f_*.png')); F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18); per=48; cols=8; tw,th=180,320
for si in range(0,len(fs),per):
    ch=fs[si:si+per]; rows=(len(ch)+cols-1)//cols; S=Image.new('RGB',(cols*tw,rows*(th+22)),'white'); d=ImageDraw.Draw(S)
    for j,f in enumerate(ch):
        n=int(f.split('_')[-1][:3])*6; im=Image.open(f).convert('RGB').resize((tw,th)); x=(j%cols)*tw; y=(j//cols)*(th+22); S.paste(im,(x,y)); d.text((x+4,y+th+2),f'f{n}',fill='black',font=F)
    S.save(f'{D}/sheet_{si//per}.jpg',quality=85)
print('frames',len(fs),'sheets',(len(fs)+per-1)//per)
PY
ls -la $O/cc_r${R}_small.mp4
