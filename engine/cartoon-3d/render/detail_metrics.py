import sys,subprocess,numpy as np
from scipy import ndimage as ni
def run(v):
    w,h=180,320
    p=subprocess.Popen(['ffmpeg','-v','error','-i',v,'-vf',f'scale={w}:{h}','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    prev=None;D=[];E=[];L=[];Sa=[];C=[];hues=[]
    while True:
        b=p.stdout.read(w*h*3)
        if len(b)<w*h*3:break
        a=np.frombuffer(b,np.uint8).reshape(h,w,3).astype(np.float32)
        g=a.mean(2)
        if prev is not None:D.append(np.abs(g-prev).mean())
        prev=g
        if len(D)%5==0:
            e=np.hypot(ni.sobel(g,0),ni.sobel(g,1)); E.append((e>60).mean())
            L.append(g.mean()/255); mx=a.max(2);mn=a.min(2); Sa.append(((mx-mn)/(mx+1)).mean())
            # distinct colours: 4-bit/channel bins used by >0.2% pixels
            q=(a//32).astype(int); k=q[...,0]*64+q[...,1]*8+q[...,2]; cnt=np.bincount(k.ravel(),minlength=512); C.append((cnt>w*h*0.002).sum())
            hues.append(a.reshape(-1,3).mean(0))
    D=np.array(D);n=len(D)+1
    cuts=[i for i in range(2,len(D)-2) if D[i]>18 and D[i]>2.2*max(D[i-1],D[i+1])]
    hues=np.array(hues)
    # mood changes: big shifts in mean colour between samples 1s apart
    mood=sum(1 for i in range(6,len(hues),6) if np.abs(hues[i]-hues[i-6]).sum()>60)
    print(f'{v.split("/")[-1][:34]:34s} dur {n/30:5.1f}s hardcuts {len(cuts):2d} motion med {np.median(D):.2f} p90 {np.percentile(D,90):.1f} still(<0.5) {100*(D<0.5).mean():4.1f}% | edge {100*np.mean(E):.1f}% | luma {np.mean(L):.2f} sat {np.mean(Sa):.2f} colours {np.mean(C):.0f} | mood shifts {mood}')
for v in sys.argv[1:]: run(v)
