# Music bed + SFX for the Nuremberg Christkindlesmarkt short (nb, from the Cape Cod music_cc) (all synthesized here, nothing licensed). Built on the BF music.py engine; new key, tempo, chords, melody, level map and SFX list.
# Bed (rules 8/188 revised Nov 21): loop-based E-minor garage bed, 92 BPM, 4-bar loop = 10.4 s (Rick 6-11 s), level rides the MAP (not constant), louder into the payoff
# (no swells, no ducking). Owner taste honoured inside it: melodic house feel, rounded sub bass, shuffled garage hats.
import numpy as np, wave, json, sys
SR=48000; END_F=1906; DUR=END_F/30+0.6; N=int(SR*DUR); rng=np.random.default_rng(7)
BPM=92; B=60/BPM; S16=B/4   # round 5 (C2): 92-100 BPM
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
# round 5 (C1): D minor, i-VI-III-VII (Dm7, Bbmaj7, Fmaj7, C7): tense, sly, forward-moving
# cc: E minor, i-VI-III-VII (Em7, Cmaj7, Gmaj7, D): sea-air, playful with an edge; 4-bar loop = 10.4 s at 92 BPM
CH=[(40,[64,67,71,74]),(36,[60,64,67,71]),(43,[62,67,71,74]),(38,[62,66,69,72])]
MEL=[[76,0,79,78,76,0,74,76],[72,0,76,74,72,0,71,72],[74,0,71,74,79,0,78,76],[74,0,78,81,78,0,76,74]]
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
# round 5: level map from the Rick music study (section 7), dB relative to the bed median; layers thin out in dips (S6)
MAP=[(0.0,3),(3.0,3.6),(4.6,-1.0),(9.0,3.2),(13.6,-3.2),(17.0,2.0),(19.6,-2.4),(22.6,1.8),(25.6,-2.0),(29.8,1.0),(33.2,-2.4),(36.4,3.6),(38.6,0.4),(42.6,-2.8),(45.6,2.2),(48.0,-2.6),(51.6,1.2),(53.0,3.4),(55.6,0.2),(58.4,4.0),(60.2,6),(61.6,8),(64.0,8)]   # nb: cc map re-timed to this VO; dip under the quoted line (14.1-16.6 s), lift on the 1678 reveal (52.2 s), +8 into the payoff
tt=np.arange(N)/SR-0.1   # VO plays 0.1 s late in the mix
mk=np.array([m[0] for m in MAP]); mv=np.array([m[1] for m in MAP],float)
gdb=np.interp(tt,mk,mv)
k_=int(0.7*SR); gdb=np.convolve(np.pad(gdb,(k_//2,k_-k_//2-1),mode='edge'),np.ones(k_)/k_,mode='valid')   # rides take ~0.7 s (M8)
gl=10**(gdb/20)
# cc r2: stop-time on the payoff hit (mix time 59.74-60.10 s, ding at f1793): the bed drops 12 dB for the ding with 40 ms ramps, then returns at full payoff level (rule 319 payoff >= +6 over the local bed while rule 192 keeps it >= 8 LU under the VO)
_tm=np.arange(N)/SR; _r=0.04; _st=np.clip(np.minimum((_tm-62.57)/_r,(63.25-_tm)/_r),0,1); pass   # r2 (audio verifier, rule 342 [C]: the bed is never lowered for an effect): no stop-times; the dings land just after their words instead   # nb: stop-time on the 1678 reveal ding too (f1565); payoff ding at f1878 ("short")
thin=np.clip((gdb+1.0)/4.0,0,1)   # melody and plucks drop out in the -3..-5 dips, return on rises
bed=(T['mal']*0.9*thin+T['plk']*0.6*(0.4+0.6*thin)+T['bass']*0.62+T['kick']*0.7+T['pad']*1.0)*gl
# gentle bus compression for a constant level (no pumping: slow, light)
bed=np.tanh(bed*0.9)/0.9
# round 5 (S5): no fade, the bed ends with the last frame
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
def whistle(dur=0.5,f=2900):
    n=int(dur*SR); t=np.arange(n)/SR; vib=1+0.03*np.sign(np.sin(2*np.pi*28*t)); x=np.sin(2*np.pi*np.cumsum(f*vib)/SR)*0.7+0.15*rng.normal(0,1,n)
    return x*np.minimum(1,t/0.01)*np.minimum(1,(dur-t)/0.04)
def whoosh(dur=0.5,up=True):
    n=int(dur*SR); t=np.arange(n)/SR; x=noise(dur,lp=1200); e=np.sin(np.pi*t/dur)**0.5; return x*e
def thump(f=70,dur=0.3):
    n=int(dur*SR); t=np.arange(n)/SR; return (np.sin(2*np.pi*f*t)*np.exp(-t*18)+0.6*noise(dur,hp=1)*np.exp(-t*60))
def click(): n=int(0.03*SR); return noise(0.03,hp=1)*np.exp(-np.linspace(0,12,n))
def ding(m=88,dur=1.2): return mallet(m,dur,d=3.0)
def chalk(dur=0.12): n=int(dur*SR); return noise(dur,hp=1)*(0.5+0.5*np.sign(np.sin(2*np.pi*35*np.arange(n)/SR)))*np.minimum(1,np.arange(n)/400)
def crowd(dur):
    x=noise(dur,lp=700); n=len(x); return x*np.minimum(1,np.arange(n)/(0.3*SR))*np.minimum(1,(n-np.arange(n))/(0.3*SR))
from scipy.signal import butter as _bt, sosfilt as _sf
def soft(x,fc=2600):   # every SFX is low-passed (4th order) so nothing shrill lands in the ear's 2-5 kHz peak (owner Nov 18: the 8 s screech)
    return _sf(_bt(4,fc,'lp',fs=SR,output='sos'),x)
def whoosh2(dur=0.45):
    n=int(dur*SR); t=np.arange(n)/SR; x=soft(rng.normal(0,1,n),900); e=np.sin(np.pi*t/dur)**1.5; return x/np.abs(x).max()*e
# Rick master guide: SFX are SPARSE, in the bed bus, well under the VO: whoosh on fast camera moves, thud on impacts, a bigger hit on the payoff.
EV=[]
EV+=[(100,whoosh2(0.5),0.6),                        # S01 swing up on "birthday"
     (140,whoosh2(0.35),0.45),                        # S02 push down onto the ink blot
     (684,soft(click(),1100),0.45),(712,soft(click(),1100),0.45),   # the 2, then the 7, tried on over the smudge
     (862,soft(click(),1200),0.6),(871,soft(click(),1200),0.6),     # two photo flashes
     (1376,soft(thump(160,0.14),1800),0.9),(1380,whoosh2(0.35),0.5),        # the banner string snaps, the banner swings down
     (1491,soft(ding(88,0.7),3000),0.35),             # eureka on "blob"
     (1580,soft(ding(83,0.9),3000),0.45),             # the 7 shows through: 1678
     (1730,whoosh2(0.4),0.45),                        # crane up to the Christkind
     (1889,soft(ding(83,1.4),3000),0.45),(1889,soft(ding(88,1.4),3000),0.32)]   # payoff push lands on "short"
# A6: level every SFX event against the bed under it so each lands at the same offset over the bed
# (one common offset; mix.py then sets the global SFX gain so the median offset is +10 dB in the mix)
BEDW=bed/np.abs(bed).max()*0.7
def rms(a): return float(np.sqrt(np.mean(a**2))+1e-9)
# A6 levelling, measured the strict way: onsets within 8 f form one group; a group's span runs from its first onset to its
# last onset + 0.3 s (at least 0.3 s of bed); the group's loudest 50 ms must sit 8-12 dB over the bed RMS across that span.
def pk50(a):
    n=int(0.05*SR); return max(rms(a[k:k+n]) for k in range(0,max(1,len(a)-n+1),n//4))
evs=sorted(EV,key=lambda e:e[0]); G=[]
for f,x,g in evs:
    if G and f-G[-1]['f0']<=8: G[-1]['ev'].append((f,x,g)); G[-1]['f1']=f
    else: G.append(dict(f0=f,f1=f,ev=[(f,x,g)]))
for gr in G:
    gr['i']=int(gr['f0']/30*SR); gr['w']=min(int((gr['f1']-gr['f0'])/30*SR)+int(0.3*SR),N-gr['i']); gr['k']=1.0
    tr=np.zeros(N)
    for f,x,g in gr['ev']:
        # gentle 2:1 compression inside each sound so its peak and body sit close together
        h=int(0.05*SR); n=len(x); env=np.array([rms(x[k:k+h]) for k in range(0,n,h)]); emax=env.max()
        gk=np.clip((np.maximum(env,emax*10**(-14/20))/emax)**-0.65,1,10**(7/20)); y=x*g*np.interp(np.arange(n),np.arange(len(env))*h+h/2,gk)
        i=int(f/30*SR); j=min(N,i+n); tr[i:j]+=y[:j-i]
    gr['tr']=tr*rms(BEDW[gr['i']:gr['i']+gr['w']])/pk50(tr[gr['i']:gr['i']+gr['w']])*10**(16/20)
for it in range(12):   # overlapping tails add up: re-level every group against the summed track until all sit at +16 (stem units)
    S[:]=sum(gr['tr']*gr['k'] for gr in G)
    for gr in G:
        i,w=gr['i'],gr['w']   # robust: average of three comparison spans (span, span+0.2 s, fixed 0.5 s)
        vv=[20*np.log10(pk50(S[i:i+ww])/rms(BEDW[i:i+ww])) for ww in (w,w+int(0.2*SR),int(0.5*SR))]; po=(min(vv)+max(vv))/2; gr['k']*=10**((16-po)/20*0.8)
ATT={1889:-6.8,1491:-5.0,1580:-5.0,100:-1.5}   # tonal dings read louder than their RMS (K-weighting): keep every SFX >= 8 LU under the VO
for gr in G: gr['k']*=10**(ATT.get(gr['f0'],0.0)/20)
S[:]=sum(gr['tr']*gr['k'] for gr in G)
evlog=[dict(f=gr['f0'],f1=gr['f1'],i=gr['i'],w=gr['w']) for gr in G]
json.dump(evlog,open('/root/nb/audio/sfx_events.json','w'))
def w(path,x):
    x=np.clip(x,-1,1); y=(x*32767).astype(np.int16); st=np.stack([y,y],1)
    with wave.open(path,'wb') as fh: fh.setnchannels(2); fh.setsampwidth(2); fh.setframerate(SR); fh.writeframes(st.tobytes())
w('/root/nb/audio/bed.wav',bed/np.abs(bed).max()*0.7); w('/root/nb/audio/sfx.wav',S/np.abs(S).max()*0.7); print('MUSIC_OK',DUR)
