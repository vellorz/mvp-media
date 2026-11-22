# Rule 329 cast sheet: whole characters assembled exactly as lib.char() builds them (body card, both arm cards on their
# shoulder pivots at the rest pose -8 deg, face disc on the neck pivot), 300 px/m, plus per-character proportion measures.
import json,math,sys
from PIL import Image,ImageDraw,ImageFont
T='/root/dc/tex/'; CI=json.load(open('/root/dc/src/cast.json'))
HS=0.43/0.586; GEO={'tall':(0.996,0.126,0.95),'short':(0.996,0.142,0.95),'round':(0.996,0.151,0.95)}
ARM_W,ARM_H,ARM_OFF=0.744,0.558,0.242; S=300
SCALE={'kidT':0.8}
FACE=sys.argv[1] if len(sys.argv)>1 else 'neutral'
def card(name,wm,hm):
    im=Image.open(T+name+'.png').convert('RGBA'); return im.resize((round(wm*S),round(hm*S)),Image.LANCZOS)
def assemble(kind):
    c=CI[kind]; top,shx,shz=GEO[c['body']]
    W,H=int(1.6*S),int(1.75*S); ox,oz=W//2,int(1.65*S)   # canvas origin: x centre, ground at oz
    cv=Image.new('RGBA',(W,H),(0,0,0,0))
    def put(im,cx,cz):  # cx,cz = world centre of card
        cv.alpha_composite(im,(round(ox+cx*S-im.width/2),round(oz-cz*S-im.height/2)))
    put(card(kind+'_body',0.8,1.1),0,-0.04+0.55)
    for sx in (-1,1):
        tk=kind+'_arm'+('_L' if sx<0 else '')
        a=card(tk,ARM_W,ARM_H); px,py=a.width/2,a.height/2-ARM_OFF*S   # pivot pixel inside the card
        big=Image.new('RGBA',(a.width*2,a.height*2),(0,0,0,0)); big.alpha_composite(a,(round(a.width-px),round(a.height-py)))
        big=big.rotate(8*sx,resample=Image.BICUBIC,center=(a.width,a.height))   # rest pose: hand swings 8 deg outward
        cv.alpha_composite(big,(round(ox+sx*shx*S-a.width),round(oz-shz*S-a.height)))
    f=FACE if FACE in c['faces'] else list(c['faces'])[0]
    put(card(f'{kind}_h_{f}',0.75*HS,0.75*HS),0,top+0.2535*HS)
    return cv,(ox,oz)
def measure(cv,ox,oz):
    a=cv.split()[3]; bb=a.getbbox(); Hm=0.43   # head width = H
    rows=[(y,[x for x in range(a.width) if a.getpixel((x,y))>128]) for y in range(bb[1],bb[3],2)]
    return dict(total_H=round((bb[3]-bb[1])/S/Hm,2))
if __name__=='__main__':
    kinds=list(CI); cols=6; cw,ch=int(1.6*S),int(1.75*S)+40
    sheet=Image.new('RGB',(cols*cw,((len(kinds)+cols-1)//cols)*ch+60),(236,228,216)); d=ImageDraw.Draw(sheet)
    try: fnt=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',26)
    except: fnt=None
    d.text((10,14),'thu-washington-dc FULL-BODY cast sheet (rule 329): assembled exactly as in the scene rig, rest pose, 300 px/m',fill=(40,24,36),font=fnt)
    M={}
    for i,k in enumerate(kinds):
        cv,(ox,oz)=assemble(k); x,y=(i%cols)*cw,(i//cols)*ch+60
        sc_=SCALE.get(k,1.0)
        if sc_!=1.0:   # in-scene root scale (scene_dc.py): shrink about the feet
            nw,nh=round(cv.width*sc_),round(cv.height*sc_); sm=cv.resize((nw,nh),Image.LANCZOS); cv=Image.new('RGBA',cv.size,(0,0,0,0)); cv.alpha_composite(sm,((cv.width-nw)//2,oz-round(oz*sc_)))
        sheet.paste(cv,(x,y),cv); M[k]=measure(cv,ox,oz)
        L={'D1':'D1 clean-shaven','D2':'D2 slim mustache','D3':'D3 light stubble','M1':'M1 side-part bob','M2':'M2 ponytail','M3':'M3 top bun'}[CI[k]['look']]
        d.text((x+10,y+ch-44),f'{k}: {L}',fill=(40,24,36),font=fnt)
    out=sys.argv[2] if len(sys.argv)>2 else '/root/dc/castgate/cast_full.png'
    sheet.save(out); json.dump(M,open('/root/dc/castgate/cast_measures.json','w'),indent=1); print('SHEET',out,sheet.size)
