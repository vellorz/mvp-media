# Detroit: rule 319 check: each SFX group's loudest 50 ms vs the local bed RMS in the mix (>= +4 dB, payoff >= +6)
import numpy as np,wave,json,sys,re
L=open('/root/det/audio/mixlog.txt').read(); gb=float(re.search(r'bed \S+ ->gain (\S+)',L).group(1)); gs=float(re.search(r'sfx \S+ ->gain (\S+)',L).group(1))
def rd(p):
    with wave.open(p) as w: return np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2)[:,0]/32768.0
b=rd('/root/det/audio/bed.wav')*10**(gb/20); s=rd('/root/det/audio/sfx.wav')*10**(gs/20)
r=lambda a: float(np.sqrt(np.mean(a**2))+1e-12)
def pk(a):
    n=2400; return max(r(a[k:k+n]) for k in range(0,max(1,len(a)-n+1),600))
o=[(e['f'],round(20*np.log10(pk(s[e['i']:e['i']+e['w']])/r(b[e['i']:e['i']+e['w']])),1)) for e in json.load(open('/root/det/audio/sfx_events.json'))]
print('OVERBED',' '.join(f'{f}:{v}' for f,v in o)); print('OVERBED_MIN',min(v for f,v in o))
