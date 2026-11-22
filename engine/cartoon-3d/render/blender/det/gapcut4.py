# gapcut v4 (Detroit round-2 audio verifier V6: gapcut3's voicing map counted sibilants (zero-crossing rate >= 0.12) as unvoiced,
# so it cut word-final "s" and "-ts" tails at 8 joins). v4 classifies 10 ms frames by full-band rms and the share of energy above 4 kHz:
# silence (<= -45 dBFS) and breath (-45..-35 dBFS, < 50 % above 4 kHz) may be cut; sibilants (> 50 % above 4 kHz) and voice never.
# Each pause is cut inside its longest cuttable run, 10 ms guards, at least 20 ms of it kept; cut lengths chase the round-2 cumulative
# removal (gapplan4.plan) so word onsets move as little as possible. 10 ms equal-power crossfade at every join.
# python3 gapcut4.py SRC WORDS GAPLOG3 DST
import json, sys, numpy as np, subprocess
sys.path.insert(0,'/root/det/src'); from voicedmap import load, SR; from gapplan4 import plan
src,words,g3,dst=sys.argv[1:5]
a=load(src); P,err,c3,c4=plan(src,words,g3,0.01,0.02)
f=int(0.01*SR); t=np.linspace(0,np.pi/2,f); fo=np.cos(t).astype(np.float32); fi=np.sin(t).astype(np.float32)
keep=[]; pos=0
for p in P:
    c0=int(p['c0']*SR); n=int(p['len']*SR)   # net removal = gap skipped (n-f) + crossfade overlap (f) = len
    keep.append(a[pos:c0+f//2]); pos=c0+f//2+n-f; 
keep.append(a[pos:])
y=keep[0]
for k in keep[1:]: y=np.concatenate([y[:-f],y[-f:]*fo+k[:f]*fi,k[f:]])
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-c:a','pcm_s24le',dst],input=y.astype(np.float32).tobytes())
json.dump(dict(method='gapcut4: silence/breath-only cuts (no sibilants, no voice), 10 ms guards, >=20 ms kept, 10 ms equal-power fade',cuts=P,removed_s=round(c4,3),round2_removed_s=round(c3,3),word_lag_vs_round2=err),open(dst+'.gaplog.json','w'),indent=0)
h=int(0.01*SR)
def loud(x): m=len(x)//h; q=20*np.log10(np.sqrt((x[:m*h].reshape(m,h).astype(np.float64)**2).mean(1))+1e-9); return round((q>-40).sum()*0.01,2)
print('gapcut4 removed',round(c4,3),'s; len',round(len(y)/SR,3),'loud(>-40 dBFS) in',loud(a),'out',loud(y))
