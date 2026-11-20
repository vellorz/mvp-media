# Build labelled contact sheets of EVERY frame: 6 cols x 4 rows = 24 frames/sheet
import sys,os,glob
from PIL import Image,ImageDraw,ImageFont
src,out=sys.argv[1],sys.argv[2]; os.makedirs(out,exist_ok=True)
fs=sorted(glob.glob(src+'/*.jpg')); W,H=270,480; C,R=6,4
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22) if os.path.exists('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf') else ImageFont.load_default()
for s in range(0,len(fs),C*R):
    sh=Image.new('RGB',(C*W,R*H),'black'); d=ImageDraw.Draw(sh)
    for i,f in enumerate(fs[s:s+C*R]):
        n=int(os.path.basename(f)[1:5]); im=Image.open(f).resize((W,H))
        x,y=(i%C)*W,(i//C)*H; sh.paste(im,(x,y))
        lab=f"f{n} {((n-1)/30):.2f}s"; d.rectangle([x,y,x+170,y+28],fill='black'); d.text((x+4,y+2),lab,fill='yellow',font=font)
    a=int(os.path.basename(fs[s])[1:5]); b=int(os.path.basename(fs[min(s+C*R,len(fs))-1])[1:5])
    sh.save(f"{out}/sheet_f{a:04d}-{b:04d}.jpg",quality=82)
print(len(fs))
