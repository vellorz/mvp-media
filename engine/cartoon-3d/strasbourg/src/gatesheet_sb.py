# Rule 329/330 cast gate sheet: Rick reference frames | whole cast from the real rig (castcheck render) | expression + turn grid | prop hands
import sys, json; sys.path.insert(0,'/root/sb/src')
from PIL import Image, ImageDraw, ImageFont
RICK='/mnt/project-files/modern-vista-social/research/rick-style-spec/frames/'
T='/root/sb/tex/'
CAST, OUT = sys.argv[1], sys.argv[2]
W=3000
try: FT=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',30); FS=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
except Exception: FT=FS=ImageFont.load_default()
rows=[]
# 1) Rick frames
refs=[('10_GM9UKnZ6JFw','0409'),('10_GM9UKnZ6JFw','0587'),('10_GM9UKnZ6JFw','0757'),('14_VS1Z_Q-Klt8','0219'),('14_VS1Z_Q-Klt8','0695'),('14_VS1Z_Q-Klt8','0857')]
ims=[Image.open(f'{RICK}{v}/frames-540/{f}.jpg').convert('RGB') for v,f in refs]
h=700; ims=[i.resize((int(i.width*h/i.height),h)) for i in ims]
r=Image.new('RGB',(W,h+50),(236,230,218)); d=ImageDraw.Draw(r); x=10
for (v,f),i in zip(refs,ims): r.paste(i,(x,50)); d.text((x,10),f'Rick {v[:2]}#{f}',fill=(40,30,40),font=FS); x+=i.width+10
d.text((x+20,300),'REFERENCE',fill=(40,30,40),font=FT); rows.append(r)
# 2) whole cast from the rig
c=Image.open(CAST).convert('RGBA'); c=c.resize((W,int(c.height*W/c.width)))
r=Image.new('RGB',(W,c.height+50),(236,230,218)); r.paste(c,(0,50),c); ImageDraw.Draw(r).text((10,10),'OUR CAST, built by lib.char() (body, both arm cards, face disc), rule 329',fill=(40,30,40),font=FT); rows.append(r)
# 3) expressions + turns
C=json.load(open('/root/sb/src/cast.json')); names=list(C)
EX=['neutral','angry','shock','grin','sad','smug','neutral@L2','neutral@R2','back']
cs=130; r=Image.new('RGB',(W,60+cs*len(names)),(236,230,218)); d=ImageDraw.Draw(r); d.text((10,10),'Expressions (library "all", 51 faces each) and head turns @L2/@R2 + back view',fill=(40,30,40),font=FT)
for j,n in enumerate(names):
    d.text((10,60+j*cs+50),n,fill=(40,30,40),font=FS)
    for i,e in enumerate(EX):
        try: im=Image.open(f'{T}{n}_h_{e}.png').convert('RGBA'); im=im.resize((cs,int(im.height*cs/im.width))); r.paste(im,(200+i*(cs+12),60+j*cs+cs-im.height),im)
        except FileNotFoundError: d.text((200+i*(cs+12),60+j*cs+50),'n/a',fill=(160,40,40),font=FS)
for i,e in enumerate(EX): d.text((200+i*(cs+12)+10,40),e,fill=(40,30,40),font=FS)
rows.append(r)
# 4) prop hands (rule 375: every held prop nameable at a glance)
P=[(n,p) for n in names for p in C[n].get('props',[])]
seen=set(); P=[(n,p) for n,p in P if not (p in seen or seen.add(p))]
cw=W//len(P); r=Image.new('RGB',(W,640),(236,230,218)); d=ImageDraw.Draw(r); d.text((10,10),'Prop hands (one per prop)',fill=(40,30,40),font=FT)
for i,(n,p) in enumerate(P):
    im=Image.open(f'{T}{n}_arm_{p}.png').convert('RGBA'); a=im.split()[3]; H_=im.height; bb=a.crop((0,int(H_*0.33),im.width,H_)).getbbox(); im=im.crop((bb[0]-20,int(H_*0.33)+bb[1]-20,bb[2]+20,int(H_*0.33)+bb[3]+20)); sz=min(cw-10,380); im.thumbnail((sz,sz))
    r.paste(im,(i*cw+5,70),im); d.text((i*cw+10,70+im.height+10),p,fill=(40,30,40),font=FS)
rows.append(r)
H=sum(x.height for x in rows); S=Image.new('RGB',(W,H),(236,230,218)); y=0
for x in rows: S.paste(x,(0,y)); y+=x.height
S.save(OUT); print('SHEET',S.size)
