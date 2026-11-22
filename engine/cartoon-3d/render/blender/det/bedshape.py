# r2 (audio verifier A4 / must-have 2: bed std 1.6-1.9 dB < 2.3): expand the bed's own level map by 30 % around its median
# (smoothed 1.5 s envelope, so the loop's beat is untouched; it only exaggerates the MAP swings music.py already wrote),
# and lift the final line (+2 dB from 'turkey' on) so the bed is louder into the payoff than at the start. Writes bed_pre.wav.
import numpy as np, wave, json
from scipy.ndimage import uniform_filter1d
A='/root/det/audio/'; SR=48000
w=wave.open(A+'bed_music.wav'); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2)[:,0]/32768.0
e=np.sqrt(uniform_filter1d(a**2,int(1.5*SR))+1e-12); d=20*np.log10(e); med=np.median(d)
x=np.clip(0.30*(d-med),-3,3)
W=json.load(open('/root/det/audio_r2/vo_final.wav.words.json')); t0=(W[-3][1]+0.1)   # 'turkey' onset in mix time
t=np.arange(len(a))/SR; x+=np.clip((t-t0)/0.6,0,1)*2.0
x[:int(3*SR)]-=1.0   # open a touch lower so the end clearly outruns it
y=a*10**(x/20)
y=y*np.sqrt(np.mean(a**2)/np.mean(y**2)); pk=np.abs(y).max(); comp=0.0
if pk>0.9: comp=20*np.log10(pk/0.9); y=y*0.9/pk
print('BEDSHAPE_COMP_DB',round(comp,2))
yy=(np.clip(y,-1,1)*32767).astype(np.int16)   # same overall RMS as the music bed, so the mix gains stay valid
with wave.open(A+'bed_pre.wav','wb') as o: o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes(np.stack([yy,yy],1).tobytes())
print('BEDSHAPE_OK turkey at',round(t0,2))
