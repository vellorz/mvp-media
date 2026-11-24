# nb extras: year signs (rule 327), the "not born yet" ghost outline, cake top, string-light bulb glow
import sys; sys.path.insert(0,'/root/nb/src')
from paint_nb import *
from PIL import Image, ImageDraw
def ghost(name='ghost_outline',W=800,H=1400):
    """dashed ink outline of an empty bean figure (the girl who was not born yet); our own drawing, Rick-style dashed 'missing' outline"""
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); K=(60,40,70,235)
    pts=[]
    cx,cy,r=W/2,330,250
    for k in range(0,360,4): a=math.radians(k); pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
    body=[(W/2-200,620),(W/2-230,1120),(W/2-120,1150),(W/2-110,1360),(W/2-40,1360),(W/2-30,1150),(W/2+30,1150),(W/2+40,1360),(W/2+110,1360),(W/2+120,1150),(W/2+230,1120),(W/2+200,620)]
    def dash(poly,closed):
        P=poly+([poly[0]] if closed else [])
        seg=[];
        for a,b in zip(P,P[1:]):
            L_=math.dist(a,b); n=max(1,int(L_/14))
            for i in range(n): seg.append((a[0]+(b[0]-a[0])*i/n,a[1]+(b[1]-a[1])*i/n))
        for i in range(0,len(seg)-4,7): d.line(seg[i:i+4],fill=K,width=28)
    # nb eyepass r1 (outline read as scattered dashes): a faint lavender fill makes the empty figure read as a person-shaped gap
    fl=Image.new('RGBA',(W,H),(0,0,0,0)); fd=ImageDraw.Draw(fl); FC=(196,182,230,95)
    fd.ellipse([cx-r,cy-r,cx+r,cy+r],fill=FC); fd.polygon(body+[(W/2+200,620)],fill=FC); im.alpha_composite(fl); d=ImageDraw.Draw(im)
    dash(pts,True); dash(body,False)
    d.text((W/2-40,250),'?',fill=K,font=font(FS,260))
    im.save(T+name+'.png')
if __name__=='__main__':
    card_text('sign_1628q',[('1628 ?',170)],(236,226,200),(60,40,50),W=1024,H=384,border=(110,80,60))
    card_text('sign_1678',[('1678',190)],(236,226,200),(60,40,50),W=1024,H=384,border=(110,80,60))
    card_text('sign_heute',[('2026',190)],(32,64,96),(246,236,210),W=1024,H=384,border=(236,228,200),wood=False)
    ghost()
    im=wash(512,512,(250,244,236),0.05,9); d=ImageDraw.Draw(im)
    for k in range(10): a=k/10*2*math.pi; d.ellipse([256+190*math.cos(a)-26,256+190*math.sin(a)-26,256+190*math.cos(a)+26,256+190*math.sin(a)+26],fill=(220,60,70))
    im.save(T+'cake_top.png'); print('EXTRA_OK')
def shadowblob(name='shadow',W=512,H=232):
    """character ground blob (one shadow system, rule 367c): soft dark ellipse, alpha only"""
    import numpy as np
    y,x=np.mgrid[0:H,0:W]; r=np.sqrt(((x-W/2)/(W*0.46))**2+((y-H/2)/(H*0.42))**2)
    a=np.clip((1.0-r)/0.35,0,1)**1.2*0.55; im=np.zeros((H,W,4),np.uint8); im[...,0]=40; im[...,1]=30; im[...,2]=46; im[...,3]=(a*255).astype(np.uint8)
    Image.fromarray(im).save(T+name+'.png')
if __name__=='__main__': shadowblob(); print('SHADOW_OK')
def window_winter(name='window_winter',W=640,H=880):
    """window card: white frame, four panes with a snowy roofscape and dusk sky (our own drawing)"""
    im=Image.new('RGB',(W,H),(236,232,224)); d=ImageDraw.Draw(im)
    sk=Image.open(T+'sky_winter.png').convert('RGB').resize((W-80,H-80)); im.paste(sk,(40,40))
    for k in range(6):
        x=40+k*110; d.polygon([(x,H-40),(x,H-260+((k*37)%60)),(x+55,H-330+((k*53)%70)),(x+110,H-260+((k*37)%60)),(x+110,H-40)],fill=(150+(k%3)*20,110,90))
        d.polygon([(x,H-260+((k*37)%60)),(x+55,H-330+((k*53)%70)),(x+110,H-260+((k*37)%60)),(x+80,H-250),(x+30,H-250)],fill=(246,248,252))
        d.rectangle([x+30,H-200,x+50,H-170],fill=(255,214,120))
    d.rectangle([0,0,W-1,H-1],outline=(60,40,50),width=14); d.rectangle([30,30,W-30,H-30],outline=(236,232,224),width=22)
    d.line([W//2,30,W//2,H-30],fill=(236,232,224),width=22); d.line([30,H//2,W-30,H//2],fill=(236,232,224),width=22)
    d.rectangle([30,30,W-30,H-30],outline=(60,40,50),width=6); im.save(T+name+'.png')
def balcdoor(name='balcdoor',W=640,H=1000):
    """open church balcony doorway: stone arch, warm-lit inside, two open wooden leaves, candle glow (our own drawing)"""
    im=Image.new('RGB',(W,H),(150,104,84)); d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/H; d.line([0,y,W,y],fill=(int(255-40*t),int(196-50*t),int(110-40*t)))
    d.rectangle([120,180,W-120,H],fill=(255,214,140)); d.ellipse([120,60,W-120,300],fill=(255,214,140))
    for x0 in (60,W-180): d.rectangle([x0,200,x0+120,H],fill=(120,70,44)); d.rectangle([x0+12,220,x0+108,H-20],outline=(70,40,28),width=8)
    d.arc([120,60,W-120,300],180,360,fill=(60,40,50),width=14); d.line([120,180,120,H],fill=(60,40,50),width=14); d.line([W-120,180,W-120,H],fill=(60,40,50),width=14)
    for cx in (230,W-230):
        d.rectangle([cx-10,620,cx+10,720],fill=(250,244,226)); d.ellipse([cx-12,590,cx+12,624],fill=(255,240,160))
    d.rectangle([0,0,W-1,H-1],outline=(60,40,50),width=10); im.save(T+name+'.png')
if __name__=='__main__': window_winter(); balcdoor(); print('EXTRA2_OK')
