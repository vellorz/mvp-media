# rule 336/336a sheet measures from the body textures (H = head width 0.43 m; widths include the ink outline)
from PIL import Image
import numpy as np, json, os, sys
C=json.load(open('/root/dc/src/cast.json')); H=0.43; T='/root/dc/tex/'; bad=0; out=[]
for n,c in C.items():
    p=f'{T}{n}_body_noskirt.png'; A=np.array(Image.open(p if os.path.exists(p) else f'{T}{n}_body.png'))[:,:,3]>128
    h,w=A.shape; rows=np.nonzero(A.any(1))[0]; wid=A.sum(1)
    crotch=max(r for r in rows if wid[r]>0.22*w); top=rows[0]
    tor=wid[top:crotch+1]; wr=int(np.argmax(tor)); frac=wr/len(tor); tw=tor.max()/w*0.8/H; hem=wid[crotch-8]/w*0.8/H
    legy=(crotch+rows[-1])//2; segs=np.diff(np.concatenate([[0],A[legy].astype(int),[0]])); st=np.nonzero(segs==1)[0]; en=np.nonzero(segs==-1)[0]; lw=np.mean(en-st)/w*0.8/H*100
    a=np.array(Image.open(f'{T}{n}_arm.png'))[:,:,3]>128; ah,aw=a.shape; ths=[]
    for y in range(int(ah*0.15),int(ah*0.5),20):
        sg=np.diff(np.concatenate([[0],a[y].astype(int),[0]])); s_=np.nonzero(sg==1)[0]; e_=np.nonzero(sg==-1)[0]
        if len(s_): ths.append(min(e_-s_))
    arm=np.median(ths)/aw*0.744*0.91/H*100
    ok=0.6<=tw<=0.85 and 1/3<=frac<=2/3 and hem<tw-0.02 and 5<=lw<=8 and 5<=arm<=8
    bad+=not ok; out.append(f'{n:8s} {"PASS" if ok else "FAIL"} torso_w(widest) {tw:.2f} H at {frac:.2f} of torso height, hem {hem:.2f} H, leg {lw:.1f}% H, arm {arm:.1f}% H')
print('\n'.join(out)); print('RESULT',"PASS" if not bad else "FAIL")
