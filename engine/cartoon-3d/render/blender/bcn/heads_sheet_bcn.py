from PIL import Image, ImageDraw, ImageFont
import os
FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',26); FR=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
T='/root/cc/tex/'
rows=[('Turns (rule 353a): hero boater at L3..R3',[('hero',f'happy@{l}') for l in ['L3','L2','L1','F','R1','R2','R3']]+[('hero','back@F')]),
      ('Hats tilted at 3/4 + approved facial hair',[('pal','smile@R2'),('engA','grin@L2'),('engB','smug@R1'),('german','proud@L1'),('locA','laugh@R2'),('keeper','determined@L2'),('vendor','smug@R2'),('tourM','grin@L1')]),
      ('Expression library range (rule 332/334): 14+ faces in the video',[('hero','shock'),('hero','worried'),('hero','determined'),('heroH','squint'),('heroH','deadpan'),('gymA','laugh'),('gymB','smug_grin'),('clerk','sleepy') ,('tourW','stunned'),('tourM','cry_laugh')]),
      ('Facial hair: pencil, walrus, toothbrush, chevron, curled, droop, stubble, goatee, king',[('hero','neutral'),('pal','neutral'),('engA','neutral'),('gymB','neutral'),('german','neutral'),('locA','neutral'),('locB','neutral'),('locD','neutral'),('clerk','neutral')])]
S=Image.new('RGB',(2450,60+len(rows)*300),(246,243,238)); d=ImageDraw.Draw(S); y=10
d.text((20,y),'Barcelona cast gate: heads from the expression library (cast.py textures used in the video)',font=FB,fill=(20,20,20)); y=50
missing=[]
for title,items in rows:
    d.text((20,y),title,font=FB,fill=(40,40,40)); x=20
    for k,fk in items:
        p=f'{T}{k}_h_{fk}.png'
        if not os.path.exists(p):
            alt=[f for f in os.listdir(T) if f.startswith(f'{k}_h_') and fk.split('@')[0] in f]
            if not alt: missing.append(p); continue
            p=T+sorted(alt)[0]
        im=Image.open(p).convert('RGBA'); s=220/im.height; im=im.resize((int(im.width*s),220))
        S.paste(im,(x,y+34),im); d.text((x,y+256),f'{k} {fk}',font=FR,fill=(70,70,70)); x+=max(im.width,200)+20
    y+=300
S.save('/root/bcn/gate/heads_sheet.jpg',quality=88); print(missing)