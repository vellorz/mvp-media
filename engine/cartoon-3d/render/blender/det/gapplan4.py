# Plan for gapcut4: per pause, the longest run of silence (<= -45 dBFS) or breath (-45..-35 dBFS with < 50 % energy above 4 kHz),
# never sibilants (> 50 % energy above 4 kHz) or voice. Room = run - 2 guards - kept pause. Cuts chase the round-2 cumulative removal so
# every word onset stays as close as possible to its round-2 time (picture is not re-rendered).
import json,sys,numpy as np
sys.path.insert(0,'/root/det/src'); from voicedmap import load,SR
def plan(src,words,g3log,GUARD=0.015,KEEP=0.03):
    a=load(src); h=int(0.01*SR); n=len(a)//h
    x=a[:n*h].reshape(n,h).astype(np.float64)
    r=20*np.log10(np.sqrt((x**2).mean(1))+1e-9)
    X=np.abs(np.fft.rfft(x*np.hanning(h),axis=1))**2; fr=np.fft.rfftfreq(h,1/SR)
    hf=X[:,fr>4000].sum(1)/(X.sum(1)+1e-12)
    ok=(r<=-45)|((r<=-35)&(hf<=0.5))
    W=json.load(open(words)); G3={round(c[0],2):c[2] for c in json.load(open(g3log))['cuts']}
    cum3=0;cum4=0;P=[];err=[]
    for i in range(len(W)-1):
        g0,g1=W[i][2],W[i+1][1]
        i0,i1=int((g0-0.08)*100),int((g1+0.08)*100); best=(0,0);k=i0
        while k<i1:
            if ok[k]:
                j=k
                while j<i1 and ok[j]: j+=1
                if j-k>best[1]-best[0]: best=(k,j)
                k=j
            else: k+=1
        room=max(0,(best[1]-best[0])*0.01-2*GUARD-KEEP)
        cum3+=G3.get(round(g0,2),0)
        c=round(min(room,max(0,cum3-cum4)),3)
        if c>=0.01: P.append(dict(g0=g0,word=W[i][0],c0=round(best[0]*0.01+GUARD+((best[1]-best[0])*0.01-2*GUARD-c)/2,3),len=c)); cum4+=c
        err.append((W[i+1][0],round(cum3-cum4,3)))
    return P,err,cum3,cum4
if __name__=='__main__':
    P,err,c3,c4=plan('/root/det/audio3/vo_trim.wav','/root/det/audio3/vo_trim.wav.words.json','/root/det/audio_r2/vo_final.wav.gaplog.json')
    e=[abs(x[1]) for x in err]; print('cuts',len(P),'total r2',round(c3,3),'new',round(c4,3),'max word lag vs r2',max(e),'words over 0.05',sum(x>0.05 for x in e))
    print([x for x in err if abs(x[1])>0.05])
