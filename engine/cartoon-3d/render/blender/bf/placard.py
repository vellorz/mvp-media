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
fs_=150
while True:
    fnt=P.font(P.FS,fs_); bb=d.textbbox((0,0),'BIG FRIDAY!',font=fnt,stroke_width=5)
    if bb[2]-bb[0]<=W-150 or fs_<60: break
    fs_-=4
P.text(d,(W/2,H*0.43),'BIG FRIDAY!',fnt,(200,40,40),stroke=5,sf=(255,255,255)); print('PLACARD_FONT',fs_)
P.text(d,(W/2,H*0.78),'SHOP DOWNTOWN',P.font(P.FSN,56),(40,40,90))
im.save(T+'placard.png')
# back of the board: plain cardboard with tape and an ink outline, so the folded-away board still reads as a board
bk=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(bk)
d.rounded_rectangle([8,8,W-8,H-8],24,fill=(196,158,104,255),outline=K,width=16)
for x in range(60,W-60,90): d.line([x,30,x+20,H-30],fill=(182,144,92,255),width=10)
for (x0,y0) in ((40,40),(W-200,40),(40,H-110),(W-200,H-110)): d.rectangle([x0,y0,x0+160,y0+60],fill=(236,226,190,230),outline=(150,130,90,255),width=3)
bk.save(T+'placard_back.png')
f=Image.new('RGBA',(200,200),(0,0,0,0)); d=ImageDraw.Draw(f)
d.ellipse([100-35,100-35,100+35,100+35],fill=(44,22,40,255))   # r8b (Rick clone): plain dark mitten, 12 % of head width (0.0516 m = 69 px on the 0.15 m card), no fingers
f.save(T+'fist.png'); print('PLACARD_OK')
