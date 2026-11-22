import numpy as np, subprocess
SR=48000
def load(p): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,np.float32)
def voiced(a,h=int(0.01*SR)):
    n=len(a)//h; x=a[:n*h].reshape(n,h).astype(np.float64)
    r=20*np.log10(np.sqrt((x**2).mean(1))+1e-9); z=(np.abs(np.diff(np.sign(x),axis=1))>0).mean(1)
    return (r>-38)&(z<0.12), r, z
