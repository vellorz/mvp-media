# rule 335a/355 probe, step 2: grade the probe stills with post_bcn's own solver/apply (per shot, from these frames) and take face medians in the faceboxes
# python3 skinratio_bcn.py DIR OUT.jpg
VMIN=0.30   # rule 355 says value > 0.50; night shots (S01, S09) have lit faces at 0.3-0.5, so the probe reaches down to 0.30
import sys, json, glob, os, numpy as np
from PIL import Image, ImageDraw, ImageFont
D,OUTJ=sys.argv[1],sys.argv[2]
sys.argv=['post_bcn.py','/nonexistent','/tmp/x.mp4','0.4']; sys.path.insert(0,'/root/bcn/src')
import post_bcn as P
bx=json.load(open(f'{D}/faceboxes.json'))
def faces(img,bl):
    out=[]
    for b in bl:
        h,w=img.shape[:2]; yy,xx=np.mgrid[0:h,0:w]; m=((xx-b['x'])**2+(yy-(b['y']+0.1*b['r']))**2)<(0.6*b['r'])**2
        px=img[m]; mx=px.max(1); mn=px.min(1); s=(mx-mn)/np.maximum(mx,1e-4)
        hue=np.degrees(np.arctan2(np.sqrt(3)*(px[:,1]-px[:,2]),2*px[:,0]-px[:,1]-px[:,2]))%360
        k=(hue>=2)&(hue<=42)&(s<0.40)&(mx>VMIN)
        if k.sum()<20: continue
        q=px[k]; out.append((float(np.median(q[:,1]/q[:,0])),float(np.median(q[:,2]/q[:,0])),int(k.sum())))
    return out
shots=sorted(set(k[:3] for k in bx)); rows=[]; res={}
for n in shots:
    ks=sorted(k for k in bx if k.startswith(n)); raws=[np.asarray(Image.open(f'{D}/{k}.png').convert('RGB'),np.float32)/255 for k in ks]
    P.PROT[0]=(n in P.SATPROT); smp=[r[::3,::3] for r in raws]; b=P.solve(smp,P.TINT[n],P.LT[n],P.VIG[n]); vk=P.VIG[n]
    if n in P.INTR:
        lo_,hi_=0.0,0.9
        for _ in range(14):
            k=(lo_+hi_)/2; rr=np.mean([P.vratio(P.vig(P.apply(q,b[1]),k)) for q in smp])
            if rr>0.38: lo_=k
            else: hi_=k
        vk=(lo_+hi_)/2; b=P.solve(smp,P.TINT[n],P.LT[n],vk)
    R=[];G=[]
    for k,raw in zip(ks,raws):
        g=P.vig(P.bloom(P.floor_(P.finish(P.apply(raw,b[1]))),P.BLOOM),vk)
        R+=faces(raw,bx[k]); G+=faces(g,bx[k])
        Image.fromarray((g*255+0.5).astype(np.uint8)).save(f'{D}/{k}_graded.jpg',quality=85)
    if not G: res[n]=dict(faces=0,note='no lit face in the probe frames'); continue
    rg=np.median([x[0] for x in R]); rb=np.median([x[1] for x in R]); gg=np.median([x[0] for x in G]); gb=np.median([x[1] for x in G])
    ok=abs(gg-0.92)<=0.04 and abs(gb-0.86)<=0.04 and abs(gg-rg)<=0.04 and abs(gb-rb)<=0.04
    res[n]=dict(faces=len(G),raw=[round(rg,3),round(rb,3)],graded=[round(gg,3),round(gb,3)],satk=round(float(b[1][3]),2),result='PASS' if ok else 'FAIL')
    print(n,res[n],flush=True)
json.dump(res,open(f'{D}/skin_ratios.json','w'),indent=1)
# sheet: first graded frame per shot with the numbers
FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
tiles=[]
for n in shots:
    k=sorted(k for k in bx if k.startswith(n))[1]; im=Image.open(f'{D}/{k}_graded.jpg'); s=640/im.height; im=im.resize((int(im.width*s),640)); d=ImageDraw.Draw(im)
    for b in bx[k]: d.ellipse([(b['x']-0.6*b['r'])*s,(b['y']-0.5*b['r'])*s,(b['x']+0.6*b['r'])*s,(b['y']+0.7*b['r'])*s],outline=(0,200,255),width=2)
    tiles.append((im,n,res[n]))
W=sum(t.width+12 for t,_,_ in tiles)+12; S=Image.new('RGB',(W,640+120),(250,248,244)); d=ImageDraw.Draw(S); x=12
for im,n,r in tiles:
    S.paste(im,(x,10)); t=f"{n} graded G/R {r['graded'][0]:.2f} B/R {r['graded'][1]:.2f}" if 'graded' in r else f'{n}: {r["note"]}'
    d.text((x,660),t,font=FB,fill=(20,20,20)); d.text((x,690),(f"raw {r['raw'][0]:.2f}/{r['raw'][1]:.2f}  {r['result']}" if 'raw' in r else ''),font=FB,fill=(20,120,40) if r.get('result')=='PASS' else (190,30,30)); x+=im.width+12
S.save(OUTJ,quality=85); print(json.dumps(res))
