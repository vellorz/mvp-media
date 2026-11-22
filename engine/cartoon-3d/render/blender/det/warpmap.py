# Detroit retime (take 3 VO): old->new frame map from aligned word onsets (difflib on normalised tokens), piecewise linear.
import json, difflib, re, numpy as np
O=json.load(open('/root/det/audio/vo_trim.wav.words.json')); N=json.load(open('/root/det/audio_r3/vo_final.wav.words.json'))
norm=lambda w: re.sub(r'[^a-z0-9]','',w.lower())
a=[norm(w[0]) for w in O]; b=[norm(w[0]) for w in N]
sm=difflib.SequenceMatcher(None,a,b,autojunk=False); P=[]
for i,j,n in sm.get_matching_blocks():
    for k in range(n): P.append(((O[i+k][1]+0.1)*30,(N[j+k][1]+0.1)*30))
P=[(0.0,0.0)]+P
OEND,NLAST=(O[-1][2]+0.1)*30,(N[-1][2]+0.1)*30
NEND=int(round((N[-1][1]+0.1+1.15)*30))   # round 2 (payoff verifier E3 / audio L6): the video ends 1.15 s after the last word STARTS
HOLD=NEND-NLAST; P.append((OEND,NLAST)); P.append((1940.0,NEND))
xo=np.array([p[0] for p in P]); xn=np.array([p[1] for p in P])
keep=np.concatenate([[True],np.diff(xo)>0.5]); xo,xn=xo[keep],xn[keep]
json.dump(dict(old=xo.tolist(),new=xn.tolist(),end=NEND),open('/root/det/bridge/warpmap.json','w'))
m=lambda f: float(np.interp(f,xo,xn))
if __name__=='__main__':
    print('pairs',len(P),'matched',sum(n for *_,n in sm.get_matching_blocks()),'of',len(a),len(b),'END',NEND)
    SH=json.load(open('/root/det/bridge/shots.json'))
    for k,(s,e) in SH.items(): print(k,s,e,'->',round(m(s)),round(m(e)),'len',round((m(e)-m(s)+1)/30,2),'s')
