# r5 (owner Nov 22: "I don't like the music"): three alternative synthesized beds, all original, $0, nothing licensed.
# Each fills the same tracks as music.py (mal, plk, bass, kick, hat, pad) so the level map, SFX levelling and mix stay unchanged.
import numpy as np
def build(style,T,put,SR,DUR,rng,mtof,env,mallet,pluck):
    P={'house':dict(bpm=100,ch=[(45,[57,60,64,67,71]),(41,[57,60,64,65,69]),(48,[55,60,64,67,72]),(43,[55,59,62,64,67])]),
       'garage':dict(bpm=96,ch=[(41,[56,60,63,67,68]),(37,[53,56,60,61,65]),(44,[51,56,60,63,67]),(39,[51,55,58,62,63])]),
       'disco':dict(bpm=100,ch=[(43,[55,59,62,67,71]),(40,[55,59,64,67,71]),(36,[55,60,64,67,72]),(38,[54,57,62,66,69])])}[style]
    B=60/P['bpm']; S16=B/4; bars=int(DUR/(4*B))+1
    def epiano(m,dur):   # FM electric piano: warm bell-ish attack, soft body
        n=int(dur*SR); t=np.arange(n)/SR; f=mtof(m); mod=np.sin(2*np.pi*f*t)*1.6*np.exp(-t*6)
        return np.sin(2*np.pi*f*t+mod)*np.exp(-t*2.2)*np.minimum(1,t/0.003)
    def organ(m,dur):   # chopped garage organ stab: odd harmonics, short gate
        n=int(dur*SR); t=np.arange(n)/SR; f=mtof(m)
        x=sum(np.sin(2*np.pi*f*h*t)/h for h in(1,2,3,4,6)); return x*np.minimum(1,t/0.004)*np.exp(-t*9)
    def strings(m,dur):  # soft detuned saw stab for disco
        n=int(dur*SR); t=np.arange(n)/SR; f=mtof(m)
        x=sum(((t*f*(1+d))%1*2-1) for d in(-0.004,0,0.004))/3; k=int(SR/(4*f))+1; x=np.convolve(x,np.ones(k)/k,'same')
        return x*np.minimum(1,t/0.02)*np.minimum(1,(dur-t)/0.05)
    def sub(m,dur,saw=0.0,slide=0):
        n=int(dur*SR); t=np.arange(n)/SR; f=mtof(m)*(1+slide*np.minimum(1,t/0.08))
        ph=2*np.pi*np.cumsum(np.full(n,1.0)*f)/SR
        return (np.sin(ph)+saw*np.sin(2*ph)/2+saw*np.sin(3*ph)/3)*env(n,0.004,4.0)
    def kick(punch=1.0):
        n=int(0.3*SR); t=np.arange(n)/SR
        x=np.sin(2*np.pi*(45*t+(150-45)*(1-np.exp(-t*35))/35))*np.exp(-t*9)
        cl=rng.normal(0,1,int(0.004*SR))*0.4*punch; x[:len(cl)]+=cl; return x
    def hat(open_=False):
        n=int((0.16 if open_ else 0.05)*SR); return np.diff(rng.normal(0,1,n),prepend=0)*np.exp(-np.linspace(0,4 if open_ else 9,n))
    def clap():
        n=int(0.18*SR); x=np.zeros(n)
        for k,o in enumerate((0,0.011,0.022)):
            i=int(o*SR); m=n-i; x[i:]+=rng.normal(0,1,m)*np.exp(-np.linspace(0,14 if k<2 else 7,m))
        return np.diff(x,prepend=0)*0.6
    K=kick(1.3 if style!='garage' else 1.0); HC=hat(); HO=hat(True); CL=clap()
    for bi in range(bars):
        t0=bi*4*B; root,ch=P['ch'][bi%4]; var=(bi//4)%2
        if style=='house':
            for k in range(4): put('kick',t0+k*B,K,0.95)
            for k in range(4): put('hat',t0+k*B+B/2,HO,0.16)
            for k in (1,3): put('hat',t0+k*B,CL,0.30)
            for k,off in enumerate((0,1.5,2.5,3.25)):   # offbeat chord stabs
                for m in ch[:4]: put('pad',t0+off*B,epiano(m,0.9),0.11)
            for k in range(8):   # rolling 8th bass, octave on the offbeats
                m=root+(12 if k%2 else 0); put('bass',t0+k*B/2,sub(m,0.32,saw=0.35),0.85 if k%2==0 else 0.55)
            MEL=[[76,0,0,74,72,0,69,0],[72,0,0,74,76,0,0,0],[79,0,76,0,74,0,72,74],[71,0,0,72,74,0,0,0]][bi%4]
            for k,m in enumerate(MEL):
                if m and (var or k<4): put('mal',t0+k*2*S16,mallet(m,0.5),0.38)
        if style=='garage':
            for off in (0,1.75,2.5): put('kick',t0+off*B,K,0.9)   # 2-step kick
            for k in (1,3): put('hat',t0+k*B,CL,0.34)
            for k in range(16):
                if k%2: put('hat',t0+k*S16+0.04,HC,0.14 if k%4==3 else 0.09)
            for off in (0.75,1.5,3.0,3.5):   # chopped organ stabs
                for m in ch[1:4]: put('pad',t0+off*B,organ(m,0.25),0.1)
            for off,m,dur,sl in ((0,root,0.6,0),(1.0,root,0.3,0),(1.75,root+12,0.25,-0.05),(2.5,root+7,0.5,0),(3.5,root+10,0.4,0.06)):
                put('bass',t0+off*B,sub(m,dur,saw=0.6,slide=sl),0.9)
            MEL=[[75,0,72,0,0,75,77,0],[72,0,0,68,0,0,0,0],[75,0,77,79,0,77,75,0],[74,0,0,0,70,0,0,0]][bi%4]
            for k,m in enumerate(MEL):
                if m: put('plk',t0+k*2*S16,pluck(m,0.35,bright=0.6,decay=0.994),0.36)
        if style=='disco':
            for k in range(4): put('kick',t0+k*B,K,0.9)
            for k in (1,3): put('hat',t0+k*B,CL,0.32)
            for k in range(8): put('hat',t0+k*B/2+B/4,HC,0.1)
            for k in range(8):   # octave disco bass, 8ths
                m=root+(12 if k%2 else 0); put('bass',t0+k*B/2,sub(m,0.22,saw=0.5),0.8)
            for off in (0.5,2.5):
                for m in ch[:4]: put('pad',t0+off*B,strings(m,1.2),0.09)
            for k in range(8):   # bright pluck arpeggio
                m=ch[(k*2)%5]+12; put('plk',t0+k*2*S16,pluck(m,0.3,bright=0.8,decay=0.992),0.3 if var else 0.22)
    return B
