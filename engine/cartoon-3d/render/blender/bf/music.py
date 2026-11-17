# Music bed + SFX for the Black Friday short (all synthesized here, nothing licensed).
# Bed (rule 188): light plucked/mallet loop with a soft four-on-the-floor pulse, 120 BPM, constant from frame 0 to the end
# (no swells, no ducking). Owner taste honoured inside it: melodic house feel, rounded sub bass, shuffled garage hats.
import numpy as np, wave, json, sys
SR=48000; END_F=1752; DUR=END_F/30+0.6; N=int(SR*DUR); rng=np.random.default_rng(7)
BPM=120; B=60/BPM; S16=B/4
def mtof(m): return 440*2**((m-69)/12)
def env(n,a=0.004,d=8.0):
    t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t*d)
def mallet(m,dur=0.6,d=6.0):
    n=int(dur*SR); t=np.arange(n)/SR; f=mtof(m)
    x=np.sin(2*np.pi*f*t)*np.exp(-t*d)+0.35*np.sin(2*np.pi*f*3.93*t)*np.exp(-t*d*3)+0.12*np.sin(2*np.pi*f*9.2*t)*np.exp(-t*d*6)
    return x*np.minimum(1,t/0.002)
def ks(m,dur=0.5,bright=0.7,decay=0.995):
    f=mtof(m); n=int(dur*SR); p=max(2,int(SR/f)); buf=rng.uniform(-1,1,p)*bright+(1-bright)*np.sin(np.linspace(0,2*np.pi,p,endpoint=False))
    out=np.empty(n);
    for i in range(n):
        j=i%p; out[i]=buf[j]; buf[j]=decay*0.5*(buf[j]+buf[(j+1)%p])
    return out
KC={}
def pluck(m,dur=0.5,**k):
    key=(m,dur,tuple(sorted(k.items())))
    if key not in KC: KC[key]=ks(m,dur,**k)
    return KC[key]
T={k:np.zeros(N) for k in ['mal','plk','bass','kick','hat','pad']}
def put(tr,t,x,g=1.0):
    i=int(t*SR)
    if i>=N or i+len(x)<0: return
    j=min(N,i+len(x)); T[tr][i:j]+=x[:j-i]*g
# I-vi-IV-V in F: Fmaj7, Dm7, Bbmaj7, C(sus)
CH=[(41,[65,69,72,76]),(38,[62,65,69,72]),(46,[62,65,70,74]),(36,[60,64,67,70])]
MEL=[[77,0,72,74,77,0,79,77],[74,0,72,69,72,74,0,72],[74,77,0,74,70,72,74,0],[72,0,76,79,76,0,74,72]]
bars=int(DUR/(4*B))+1
for bi in range(bars):
    t0=bi*4*B; root,tri=CH[bi%4]; var=(bi//4)%2
    # sub bass: root on 1, octave pops on the "and" of 2 and 4 (garage bounce)
    for off,m,g in [(0,root,1.0),(1.5,root+12,0.55),(2.0,root,0.8),(3.5,root+12,0.55)]:
        n=int(0.45*SR); t=np.arange(n)/SR; x=np.sin(2*np.pi*mtof(m)*t)+0.25*np.sin(2*np.pi*mtof(m)*2*t); put('bass',t0+off*B,x*env(n,0.006,5.0)*g)
    # mallet melody (8ths), pluck counter-arpeggio (16ths, light)
    for k,m in enumerate(MEL[bi%4]):
        if m: put('mal',t0+k*2*S16,mallet(m+(12 if var and k%4==0 else 0)),0.5)
    for k in range(16):
        if k%4==3: continue
        m=tri[(k*3)%4]+(12 if k%8>3 else 0); put('plk',t0+k*S16,pluck(m,0.3,bright=0.75,decay=0.993),0.28 if k%2 else 0.4)
    # pad: soft detuned triangle chord, constant level across the bar
    n=int(4*B*SR); t=np.arange(n)/SR
    pad=sum(2/np.pi*np.arcsin(np.sin(2*np.pi*mtof(m)*t*(1+d))) for m in tri[:3] for d in(-0.002,0.002))
    put('pad',t0,pad*np.minimum(1,t/0.08)*np.minimum(1,(4*B-t)/0.08),0.05)
    # shuffled garage hats (swung 16ths)
    for k in range(16):
        if k%2==0 and k%4!=2: continue
        sw=0.035 if k%2 else 0.0; n=int(0.05*SR); h=np.diff(rng.normal(0,1,n),prepend=0)*np.exp(-np.linspace(0,9,n)); put('hat',t0+k*S16+sw,h,0.22 if k%4==2 else 0.12)
# soft kick: short sine sweep, rounded (pulse, not a thump)
n=int(0.22*SR); t=np.arange(n)/SR; KICK=np.sin(2*np.pi*(48*t+ (110-48)*(1-np.exp(-t*40))/40))*np.exp(-t*14)*np.minimum(1,t/0.002)
T['kick'][:]=0
for bi in range(bars):
    for k in range(4): put('kick',bi*4*B+k*B,KICK,0.9)
bed=T['mal']*0.9+T['plk']*0.6+T['bass']*0.55+T['kick']*0.7+T['hat']*0.35+T['pad']*1.0
# gentle bus compression for a constant level (no pumping: slow, light)
bed=np.tanh(bed*0.9)/0.9
fade=np.ones(N); fo=int(0.35*SR); fade[N-fo:]=np.linspace(1,0,fo); bed*=fade
# ---------------- SFX ----------------
S=np.zeros(N)
def sput(f,x,g=1.0):
    t=(f/30); i=int(t*SR); j=min(N,i+len(x)); S[i:j]+=x[:j-i]*g
def tone(f0,f1,dur,shape='sin'):
    n=int(dur*SR); t=np.arange(n)/SR; fr=np.linspace(f0,f1,n); ph=2*np.pi*np.cumsum(fr)/SR
    return np.sin(ph) if shape=='sin' else np.sign(np.sin(ph))*0.6
def noise(dur,lp=0.0,hp=0.0):
    n=int(dur*SR); x=rng.normal(0,1,n)
    if lp: a=np.exp(-2*np.pi*lp/SR); y=np.empty(n); s=0.0
    if lp:
        for i in range(n): s=a*s+(1-a)*x[i]; y[i]=s
        x=y/ (np.abs(y).max()+1e-9)
    if hp: x=np.diff(x,prepend=0)
    return x
def horn(dur=0.35,f=330):
    n=int(dur*SR); t=np.arange(n)/SR; x=(np.sign(np.sin(2*np.pi*f*t))+np.sign(np.sin(2*np.pi*f*1.26*t)))*0.3
    x=np.convolve(x,np.ones(12)/12,'same'); return x*np.minimum(1,t/0.01)*np.minimum(1,(dur-t)/0.03)
def whistle(dur=0.5):
    n=int(dur*SR); t=np.arange(n)/SR; vib=1+0.03*np.sign(np.sin(2*np.pi*28*t)); x=np.sin(2*np.pi*np.cumsum(2900*vib)/SR)*0.7+0.15*rng.normal(0,1,n)
    return x*np.minimum(1,t/0.01)*np.minimum(1,(dur-t)/0.04)
def whoosh(dur=0.5,up=True):
    n=int(dur*SR); t=np.arange(n)/SR; x=noise(dur,lp=1200); e=np.sin(np.pi*t/dur)**2; return x*e
def thump(f=70,dur=0.3):
    n=int(dur*SR); t=np.arange(n)/SR; return (np.sin(2*np.pi*f*t)*np.exp(-t*18)+0.6*noise(dur,hp=1)*np.exp(-t*60))
def click(): n=int(0.03*SR); return noise(0.03,hp=1)*np.exp(-np.linspace(0,12,n))
def ding(m=88,dur=1.2): return mallet(m,dur,d=3.0)
def chalk(dur=0.12): n=int(dur*SR); return noise(dur,hp=1)*(0.5+0.5*np.sign(np.sin(2*np.pi*35*np.arange(n)/SR)))*np.minimum(1,np.arange(n)/400)
def crowd(dur):
    x=noise(dur,lp=700); n=len(x); return x*np.minimum(1,np.arange(n)/(0.3*SR))*np.minimum(1,(n-np.arange(n))/(0.3*SR))
EV=[]
for f in (8,62,140): EV.append((f,whistle(0.45),0.55))
for f,fr in [(20,330),(75,392),(110,294),(150,349),(156,262),(443,311),(449,370),(455,277)]: EV.append((f,horn(0.3,fr),0.5))
EV+= [(128,whoosh(0.7),0.6),(240,whoosh(0.5),0.5),(300,crowd(3.8),0.22),(308,click(),0.7),(355,crowd(1.6),0.3),(483,whoosh(0.25),0.55),(489,thump(240,0.12),0.45),
      (574,thump(60,0.35),1.0),(645,whoosh(0.4),0.35),(842,whoosh(0.3),0.5),(851,ding(84,0.9),0.45),(851,ding(91,0.9),0.35),
      (904,tone(700,180,0.6),0.35),(958,tone(1800,2400,0.25),0.15),(977,tone(1900,2600,0.25),0.15),(1116,whoosh(0.6),0.45),(1184,click(),0.9),
      (1467,ding(96,0.5),0.5),(1471,ding(100,0.9),0.45),(1468,thump(180,0.12),0.4),(1646,crowd(2.0),0.35),(1640,noise(0.6,lp=300)*np.hanning(int(0.6*SR)),0.3),
      (1699,whoosh(0.3),0.75),(1709,thump(90,0.25),0.6),(1727,ding(84,1.6),0.4),(1727,ding(89,1.6),0.3),(1727,ding(96,1.6),0.25)]
for f in range(606,628,3): EV.append((f,chalk(0.09),0.35))
for f in range(1270,1300,4): EV.append((f,chalk(0.07),0.2))
for f in range(1306,1346,4): EV.append((f,chalk(0.07),0.2))
for f in range(1010,1056,6): EV.append((f,thump(150,0.08),0.35))
for f,x,g in EV: sput(f,x,g)
def w(path,x):
    x=np.clip(x,-1,1); y=(x*32767).astype(np.int16); st=np.stack([y,y],1)
    with wave.open(path,'wb') as fh: fh.setnchannels(2); fh.setsampwidth(2); fh.setframerate(SR); fh.writeframes(st.tobytes())
w('/root/bf/audio/bed.wav',bed/np.abs(bed).max()*0.7); w('/root/bf/audio/sfx.wav',S/np.abs(S).max()*0.7); print('MUSIC_OK',DUR)
