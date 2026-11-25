# r1b: smooth the VO click at 20.734 s (audio verifier: 10 ms jump -57 -> -33 dB, sample step 0.0376) and the small tick at 55.64 s:
# replace 6 ms around each with a cubic-free linear crossfade between the neighbouring samples. Writes vo_final_dc.wav.
import wave, numpy as np
w=wave.open('/root/sb/vo/vo_final.wav'); p=w.getparams(); x=np.frombuffer(w.readframes(p.nframes),np.int16).reshape(-1,p.nchannels).astype(np.float64); sr=p.framerate
for t0 in (20.734,55.64):
    c=int(t0*sr); seg=x[c-int(0.01*sr):c+int(0.01*sr),0]; d=np.abs(np.diff(seg)); k=c-int(0.01*sr)+int(np.argmax(d))
    a,b=k-int(0.003*sr),k+int(0.003*sr)
    for ch in range(p.nchannels): x[a:b,ch]=np.linspace(x[a,ch],x[b,ch],b-a)
    if t0<30:   # r2b (audio verifier: the 20.73 s tick still 25 dB over the bed above 3 kHz): 1 ms moving average over 24 ms around it
        a2,b2=k-int(0.012*sr),k+int(0.012*sr); kk=int(0.001*sr)
        for ch in range(p.nchannels): x[a2:b2,ch]=np.convolve(x[a2-kk:b2+kk,ch],np.ones(2*kk+1)/(2*kk+1),mode='same')[kk:-kk]
    print('declick',t0,'at',round(k/sr,4),'max step before',int(d.max()))
o=wave.open('/root/sb/vo/vo_final_dc.wav','wb'); o.setparams(p); o.writeframes(np.clip(x,-32768,32767).astype(np.int16).tobytes()); print('DECLICK_OK')
