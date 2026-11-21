# r8: 2D composite of each cast member as the 3D card rig places it (body, head, arms at a hanging pose), for side-by-side checks vs Rick refs
import json, math, sys
from PIL import Image
T='/root/bf/tex/'; C=json.load(open('/root/bf/src/cast.json'))
BSY={'tall':1.0,'short':1.0,'round':1.0}
GEO={'tall':(0.996,0.126,0.95),'short':(0.996,0.142,0.95),'round':(0.996,0.151,0.95)}; HS=0.43/0.586
PPM=500   # px per metre
def comp(kind,face=None,ang=-8):
    c=C[kind]; top,shx,shz=GEO[c['body']]; sy=BSY[c['body']]
    W,H=int(1.6*PPM),int(2.0*PPM); im=Image.new('RGBA',(W,H),(236,230,218,255))
    X=lambda x:int(W/2+x*PPM); Z=lambda z:int(H-0.1*PPM-z*PPM)
    def put(path,cx,cz,w,h,rot=0,flip=False):
        a=Image.open(path).convert('RGBA').resize((max(1,int(w*PPM)),max(1,int(h*PPM))))
        if rot: a=a.rotate(rot,resample=Image.BICUBIC,expand=True)
        im.alpha_composite(a,(X(cx)-a.size[0]//2,Z(cz)-a.size[1]//2))
    # arms (behind face, in front of body): drawn after body, before head
    put(f'{T}{kind}_body.png',0,-0.04+0.55*sy,0.8,1.1*sy)
    for sx in(-1,1):
        # card centre 0.242 below the pivot along the arm, rotated by ang (outward)
        a=math.radians(ang)*sx; cx=sx*shx-(-0.242)*math.sin(a)*-1; cz=shz-0.242*math.cos(a)
        cx=sx*shx+0.242*math.sin(-a)*-1 if False else sx*shx-0.242*math.sin(a)
        put(f'{T}{kind}_arm'+('_L' if sx<0 else '')+'.png',cx,cz,0.744,0.558,rot=-math.degrees(a))
    fk=face or [k for k in c['faces'] if k!='blink'][0]
    put(f'{T}{kind}_h_{fk}.png',0,top+0.2535*HS,0.75*HS,0.75*HS)
    return im
if __name__=='__main__':
    ks=sys.argv[1].split(',') if len(sys.argv)>1 else list(C)
    ims=[comp(k) for k in ks]; S=Image.new('RGB',(sum(i.size[0] for i in ims),ims[0].size[1]),(236,230,218)); x=0
    for i in ims: S.paste(i.convert('RGB'),(x,0)); x+=i.size[0]
    S.save(sys.argv[2] if len(sys.argv)>2 else '/root/bf/charsheet.jpg',quality=88); print('SHEET',ks)
