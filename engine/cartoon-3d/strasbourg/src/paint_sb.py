# Painted textures for the Strasbourg short (sun-strasbourg). PIL only, our own designs. Output /root/sb/tex/
# Reuses only the generic painter helpers (paint.py wash/strokes/paintdetail, paint_cc planks/stone/sky): every texture here is new.
import sys; sys.path.insert(0,'/root/sb/src')
import paint as P
P.T='/root/sb/tex/'; T=P.T
import paint_cc as PC
PC.T=T
import numpy as np, random, math
from PIL import Image, ImageDraw, ImageFilter
from paint import wash, strokes, paintdetail, noise, jl, jr, mul, text, font, FS, INK
K=(50,28,42)
def det(im,base,seed,dens=1.0): return paintdetail(im,Image.new('L',im.size,255),base,seed,1,dens=dens)
def cobbles(name,base=(150,140,132),seed=1,W=1024,H=1024,snow=0.0):
    im=wash(W,H,mul(base,0.55),0.06,seed); d=ImageDraw.Draw(im); r=random.Random(seed); s=64
    for j in range(H//s+1):
        off=(j%2)*s/2
        for i in range(-1,W//s+2):
            x=i*s+off+r.uniform(-4,4); y=j*s+r.uniform(-4,4); c=mul(base,r.uniform(0.82,1.15))
            d.rounded_rectangle([x+4,y+4,x+s-4,y+s-4],18,fill=c,outline=mul(base,0.45),width=3)
            d.arc([x+10,y+8,x+s-14,y+s-20],200,290,fill=mul(c,1.18),width=4)
    if snow:
        for _ in range(int(900*snow)):
            x,y=r.uniform(0,W),r.uniform(0,H); rr=r.uniform(8,34); d.ellipse([x-rr,y-rr*0.6,x+rr,y+rr*0.6],fill=(236,240,248))
    det(im,base,seed+900).save(T+name+'.png')
def timber(name,plaster,beam,seed,W=1024,H=1536,floors=3,boxes=True,snow=False,lit=False):
    """Alsatian half-timbered front: plaster panels, dark beams with braces and St Andrew's crosses, small-paned windows, window boxes"""
    im=wash(W,H,plaster,0.07,seed); d=ImageDraw.Draw(im); r=random.Random(seed); fh=H/floors; bw=26
    for f in range(floors+1):
        y=int(f*fh); d.rectangle([0,y-bw//2,W,y+bw//2],fill=beam); jl(d,[(0,y-bw//2),(W,y-bw//2)],4,K,f)
    for f in range(floors):
        y0=int(f*fh); y1=int((f+1)*fh); cols=4
        for c in range(cols+1):
            x=int(c*W/cols); d.rectangle([x-bw//2,y0,x+bw//2,y1],fill=beam)
        for c in range(cols):
            x0=int(c*W/cols)+bw//2; x1=int((c+1)*W/cols)-bw//2
            if (c+f+seed)%3==0 and f>0:   # St Andrew's cross panel
                d.line([x0,y0+bw,x1,y1-bw],fill=beam,width=bw); d.line([x1,y0+bw,x0,y1-bw],fill=beam,width=bw)
            else:   # window with small panes and shutters
                wx0,wx1=x0+40,x1-40; wy0,wy1=y0+70,y1-90
                glass=(255,210,120) if lit else (120,150,176)
                d.rectangle([wx0,wy0,wx1,wy1],fill=glass,outline=K,width=8)
                for k in range(1,3): xx=wx0+(wx1-wx0)*k/3; d.line([xx,wy0,xx,wy1],fill=mul(beam,1.2),width=6)
                yy=(wy0+wy1)/2; d.line([wx0,yy,wx1,yy],fill=mul(beam,1.2),width=6)
                for sx in (-1,1):
                    xa=wx0-48 if sx<0 else wx1+4; d.rectangle([xa,wy0,xa+44,wy1],fill=mul((60,100,80),r.uniform(0.9,1.1)),outline=K,width=5)
                    for k in range(1,5): d.line([xa+4,wy0+(wy1-wy0)*k/5,xa+40,wy0+(wy1-wy0)*k/5],fill=K,width=3)
                if boxes:
                    d.rectangle([wx0-10,wy1+4,wx1+10,wy1+40],fill=(110,70,40),outline=K,width=5)
                    for k in range(9):
                        fx_=wx0+k*(wx1-wx0)/8; col=(220,60,70) if not snow else (60,110,60)
                        d.ellipse([fx_-14,wy1-14,fx_+14,wy1+14],fill=col,outline=K,width=3)
                if snow: d.rectangle([wx0-12,wy1+40,wx1+12,wy1+52],fill=(240,244,250))
    # ground floor door
    d.rounded_rectangle([W*0.38,H-fh+60,W*0.62,H+40],60,fill=(96,60,36),outline=K,width=8); d.ellipse([W*0.57,H-fh/2,W*0.59,H-fh/2+20],fill=(214,180,80))
    im=strokes(im,900,mul(plaster,0.85),seed+3,6,20,2,60)
    det(im,plaster,seed+900,0.8).save(T+name+'.png')
def cathedral(name,W=2048,H=3072,seed=21,night=False):
    """pink-sandstone Gothic west front, our own drawing (not traced): three portals, a big rose window, tall lancets and lacy vertical tracery"""
    base=(198,122,112) if not night else (150,92,96)
    im=wash(W,H,base,0.10,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for x in range(0,W,22): d.line([x,0,x,H],fill=mul(base,0.86),width=3)   # the 'harp strings' of free tracery
    for k in range(4): xx=k*W/3; d.rectangle([xx-50,0,xx+50,H],fill=mul(base,0.78),outline=K,width=6)   # buttresses
    # portals
    for cx,w in ((W/2,420),(W/6+20,260),(5*W/6-20,260)):
        y0=H-900 if w>300 else H-700
        d.polygon([(cx-w/2,H),(cx-w/2,y0+w/2),(cx,y0-w*0.35),(cx+w/2,y0+w/2),(cx+w/2,H)],fill=mul(base,0.55),outline=K)
        for j in range(5): ww=w/2-j*28; d.line([(cx-ww,H),(cx-ww,y0+w/2+j*10),(cx,y0-w*0.35+j*40),(cx+ww,y0+w/2+j*10),(cx+ww,H)],fill=mul(base,0.75+0.06*j),width=8,joint='curve')
        d.rectangle([cx-w/2+60,H-380,cx+w/2-60,H],fill=(96,60,40) if not night else (255,200,120),outline=K,width=8)
        d.polygon([(cx,y0-w*0.35-120),(cx-w/2-30,y0+40),(cx+w/2+30,y0+40)],outline=K,fill=None); d.line([(cx-w/2-30,y0+40),(cx,y0-w*0.35-140),(cx+w/2+30,y0+40)],fill=K,width=8)
    # rose window
    cx,cy,R=W/2,H*0.45,360
    d.ellipse([cx-R-30,cy-R-30,cx+R+30,cy+R+30],fill=mul(base,0.7),outline=K,width=10)
    glass=[(60,80,160),(170,40,50),(220,170,60),(50,120,90)] if not night else [(255,200,90),(255,150,70),(250,220,140),(240,170,80)]
    d.ellipse([cx-R,cy-R,cx+R,cy+R],fill=glass[0],outline=K,width=8)
    for k in range(16):
        a=2*math.pi*k/16; x=cx+R*0.62*math.cos(a); y=cy+R*0.62*math.sin(a)
        d.ellipse([x-80,y-80,x+80,y+80],fill=glass[1+k%3],outline=K,width=6); d.line([cx,cy,cx+R*math.cos(a),cy+R*math.sin(a)],fill=mul(base,0.8),width=10)
    d.ellipse([cx-90,cy-90,cx+90,cy+90],fill=glass[2],outline=K,width=8)
    # lancet windows up high and a gallery of statues (plain niches)
    for k in range(6):
        x=W*0.12+k*W*0.152; y0=300; d.polygon([(x-50,y0+700),(x-50,y0+120),(x,y0),(x+50,y0+120),(x+50,y0+700)],fill=glass[0] if not night else (255,210,120),outline=K)
    for k in range(14):
        x=120+k*(W-240)/13; d.rounded_rectangle([x-36,H-1240,x+36,H-1060],30,fill=mul(base,0.62),outline=K,width=5); d.ellipse([x-16,H-1230,x+16,H-1198],fill=mul(base,1.1))
    im=strokes(im,2600,mul(base,0.8),seed+4,6,24,2,70)
    det(im,base,seed+900,0.9).save(T+name+'.png')
def nick_board(name,W=768,H=1024,seed=31):
    """painted fair sign: a jolly bishop-saint figure in folk-art style (red robe, white beard, mitre, staff, sack of toys); no text"""
    im=wash(W,H,(240,224,186),0.06,seed); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W-1,H-1],outline=(120,70,40),width=36); d.rectangle([36,36,W-37,H-37],outline=K,width=6)
    cx=W/2
    d.polygon([(cx-210,H-90),(cx-150,380),(cx+150,380),(cx+210,H-90)],fill=(190,40,40),outline=K); d.line([(cx-210,H-90),(cx-150,380),(cx+150,380),(cx+210,H-90),(cx-210,H-90)],fill=K,width=10)
    d.rectangle([cx-18,400,cx+18,H-90],fill=(230,190,90))
    d.ellipse([cx-130,170,cx+130,420],fill=(250,232,212),outline=K,width=10)
    d.polygon([(cx-120,360),(cx+120,360),(cx+60,560),(cx,600),(cx-60,560)],fill=(250,250,250),outline=K)
    d.polygon([(cx-110,210),(cx,40),(cx+110,210)],fill=(230,190,90),outline=K); d.line([(cx-110,210),(cx,40),(cx+110,210),(cx-110,210)],fill=K,width=10); d.line([cx,60,cx,200],fill=(190,40,40),width=14)
    for sx in (-1,1): d.ellipse([cx+sx*50-14,270,cx+sx*50+14,300],fill=K)
    d.arc([cx-50,300,cx+50,350],20,160,fill=K,width=8)
    d.line([cx+250,180,cx+250,H-90],fill=(214,180,80),width=20); d.arc([cx+190,120,cx+290,240],180,360,fill=(214,180,80),width=20)
    d.ellipse([cx-300,620,cx-120,820],fill=(140,100,60),outline=K,width=8)
    for k,(x,y,c) in enumerate(((cx-250,600,(60,120,180)),(cx-170,590,(230,190,60)),(cx-210,560,(200,50,50)))): d.rectangle([x-30,y-30,x+30,y+30],fill=c,outline=K,width=5)
    im=strokes(im,500,(200,180,150),seed,6,18,2,50); im.save(T+name+'.png')
def awning(name,c1,c2,W=1024,H=512,stripes=8):
    im=Image.new('RGB',(W,H),c1); d=ImageDraw.Draw(im)
    for k in range(stripes):
        if k%2: d.rectangle([k*W/stripes,0,(k+1)*W/stripes,H],fill=c2)
    for k in range(stripes*2): x=k*W/(stripes*2); d.chord([x,H-60,x+W/(stripes*2),H+20],0,180,fill=c1 if k%2==0 else c2,outline=K,width=4)
    im=strokes(im,500,mul(c1,0.85),3,6,20,2,50); im.save(T+name+'.png')
def chronicle(name,W=2048,H=1400,seed=41):
    """an open old chronicle on a desk: left page scribble lines (no real words), right page an ink sketch of a fir tree hung with roses and apples"""
    im=Image.new('RGB',(W,H),(110,70,44)); d=ImageDraw.Draw(im); r=random.Random(seed); pg=(240,226,190)
    for sx,x0 in ((0,60),(1,W//2+10)): d.rounded_rectangle([x0,60,x0+W//2-70,H-60],30,fill=pg,outline=K,width=10)
    d.line([W//2,60,W//2,H-60],fill=mul(pg,0.6),width=14)
    for k in range(18):   # handwriting-like squiggle lines (not letters)
        y=150+k*58; x=120
        while x<W//2-110:
            w=r.uniform(30,110); pts=[(x+t,y+6*math.sin(t*0.5+r.random()*6)) for t in range(0,int(w),4)]; d.line(pts,fill=(70,50,40),width=5); x+=w+r.uniform(14,26)
    d.text((140,90),'',fill=K)
    cx=W*0.75; base=H-200
    d.rectangle([cx-30,base-30,cx+30,base+60],fill=(120,80,50),outline=K,width=6); d.polygon([(cx-90,base+60),(cx+90,base+60),(cx+70,base+120),(cx-70,base+120)],fill=(150,100,60),outline=K)
    for t in range(6):
        w=300-t*44; y=base-60-t*150; d.polygon([(cx-w,y),(cx,y-230),(cx+w,y)],fill=(70,120,70),outline=K)
    for k in range(14):
        a=r.uniform(-1,1); y=r.uniform(base-900,base-120); w=(y-(base-1000))*0.3; x=cx+a*w
        if k%2: d.ellipse([x-22,y-22,x+22,y+22],fill=(200,40,40),outline=K,width=4)
        else:
            for rr in (26,16): d.ellipse([x-rr,y-rr,x+rr,y+rr],fill=(230,90,110) if rr>20 else (250,150,170),outline=K,width=4)
    im=strokes(im,700,(200,180,150),seed,6,18,2,40); im.save(T+name+'.png')
def fir(name,seed=51,W=1024,H=1024,snow=False):
    im=wash(W,H,(46,96,60),0.10,seed); d=ImageDraw.Draw(im); r=random.Random(seed)
    for _ in range(2600):
        x,y=r.uniform(0,W),r.uniform(0,H); L=r.uniform(14,40); a=r.uniform(-0.6,0.6)+math.pi/2*r.choice([0.6,1.4])
        d.line([x,y,x+L*math.cos(a),y+L*math.sin(a)],fill=mul((46,96,60),r.uniform(0.6,1.4)),width=3)
    if snow:
        for _ in range(260): x,y=r.uniform(0,W),r.uniform(0,H); d.ellipse([x-18,y-8,x+18,y+8],fill=(236,240,248))
    im.save(T+name+'.png')
def plaster(name,base,seed,beams=True,W=1024,H=1024):
    im=wash(W,H,base,0.07,seed); d=ImageDraw.Draw(im)
    if beams:
        bc=(86,56,36)
        for x in (0,W//2): d.rectangle([x,0,x+40,H],fill=bc,outline=K,width=4)
        d.line([40,H*0.1,W//2,H*0.9],fill=bc,width=36)
    det(strokes(im,900,mul(base,0.86),seed,6,20,2,60),base,seed+900).save(T+name+'.png')
def snowflake(name='snow'):
    im=Image.new('RGBA',(128,128),(0,0,0,0)); d=ImageDraw.Draw(im); d.ellipse([20,20,108,108],fill=(250,250,255,255),outline=(180,190,210,255),width=6); im.save(T+name+'.png')
def glow(name='bulb',col=(255,214,120)):
    a=np.zeros((256,256,4),np.uint8); yy,xx=np.mgrid[0:256,0:256]; rr=np.hypot(xx-128,yy-128)/128
    a[...,0],a[...,1],a[...,2]=col; a[...,3]=np.clip((1-rr)*255*1.4,0,255).astype(np.uint8); Image.fromarray(a).save(T+name+'.png')
if __name__=='__main__':
    cobbles('cobble',(150,140,132),1); cobbles('cobble_snow',(140,136,138),2,snow=1.0)
    for i,(pl,bm) in enumerate([((236,222,190),(92,58,36)),((232,196,160),(74,48,32)),((214,222,200),(96,62,40)),((240,214,170),(70,50,40))]):
        timber(f'timber{i}',pl,bm,10+i); timber(f'timber{i}_snow',pl,bm,10+i,snow=True); timber(f'timber{i}_night',mul(pl,0.62),mul(bm,0.7),10+i,snow=True,lit=True)
    cathedral('cathedral'); cathedral('cathedral_night',night=True)
    PC.stone('sandstone',(196,120,110),22); PC.stone('sandstone_dark',(150,92,92),23); PC.stone('greystone',(170,164,156),24)
    nick_board('nickboard')
    awning('awn_red',(200,50,50),(246,238,224)); awning('awn_green',(50,120,80),(246,238,224)); awning('awn_blue',(50,90,150),(246,238,224))
    PC.planks('stallwood',(150,104,64),30); PC.planks('chalet',(170,120,74),31,vertical=True); PC.planks('panel',(118,76,48),32,vertical=True); PC.planks('floorw',(140,96,62),33); PC.planks('pew',(110,70,44),34)
    PC.sky('sky_winter',(120,150,196),(232,226,222),17,6,(246,246,250)); PC.sky('sky_snow',(140,150,170),(214,214,220),18,9,(226,228,234)); PC.sky('sky_night',(14,20,52),(60,52,96),19,3,(70,70,100))
    chronicle('chronicle'); fir('fir',51); fir('fir_snow',52,snow=True)
    plaster('plaster_room',(232,214,180),60); plaster('plaster_council',(214,200,170),61,beams=False)
    snowflake(); glow('bulb'); glow('candleglow',(255,190,90))
    from PIL import Image as _I
    _I.open('/mnt/project-files/modern-vista-social/handoff/2026-11-22_schedule-redesign/run-a/posters/strasbourg.png').convert('RGB').save(T+'poster.png')
    print('PAINT_OK')
# ground blob for lib.char (the texture was packed in earlier blends, no generator in the repo): plum ellipse, soft edge [INFERRED]
def shadow_blob():
    import numpy as _np
    W,H=512,230; y,x=_np.mgrid[0:H,0:W]; rr=_np.sqrt(((x-W/2)/(W/2))**2+((y-H/2)/(H/2))**2)
    a=_np.zeros((H,W,4),_np.uint8); a[...,0],a[...,1],a[...,2]=50,28,42; a[...,3]=(_np.clip((1-rr)/0.35,0,1)*120).astype(_np.uint8)
    Image.fromarray(a).save(T+'shadow.png')
if __name__=='__main__' and 'shadow' in sys.argv: shadow_blob()
