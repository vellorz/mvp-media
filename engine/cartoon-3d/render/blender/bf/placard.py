# Hand-held "BIG FRIDAY!" placard (S07/S08) and a front-view fist that grips its stick, cast style.
import sys; sys.path.insert(0,'/root/bf/src')
from PIL import Image, ImageDraw
import paint as P
T='/root/bf/tex/'; K=(30,22,20,255); SK=(252,246,236,255)
W,H=1024,512
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
d.rounded_rectangle([8,8,W-8,H-8],24,fill=(250,236,90,255),outline=K,width=16)
for x in range(40,W-40,64): d.rectangle([x,24,x+32,H-24],fill=(246,224,70,255))
d.rounded_rectangle([8,8,W-8,H-8],24,outline=K,width=16); d.rounded_rectangle([34,34,W-34,H-34],16,outline=(200,40,40,255),width=12)
P.text(d,(W/2,H*0.43),'BIG FRIDAY!',P.font(P.FS,150),(200,40,40),stroke=5,sf=(255,255,255))
P.text(d,(W/2,H*0.78),'SHOP DOWNTOWN',P.font(P.FSN,56),(40,40,90))
im.save(T+'placard.png')
f=Image.new('RGBA',(200,200),(0,0,0,0)); d=ImageDraw.Draw(f)
d.ellipse([20,30,180,180],fill=SK,outline=K,width=12)
for i in range(3): d.arc([40,40+i*38,170,110+i*38],200,340,fill=K,width=8)
f.save(T+'fist.png'); print('PLACARD_OK')
