import sys,json
from faster_whisper import WhisperModel
m=WhisperModel('small.en',device='cpu',compute_type='int8')
import subprocess,numpy as np
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',sys.argv[1],'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
segs,_=m.transcribe(a,word_timestamps=True,language='en',initial_prompt='Detroit, George Richards, Lions, Tigers, NBC, NFL, Chicago Bears, Thanksgiving.')
W=[]
for s in segs:
    for w in s.words: W.append([w.word.strip(),round(w.start,2),round(w.end,2)])
json.dump(W,open(sys.argv[1]+'.words.json','w')); print(len(W)); print(' '.join(w[0] for w in W))
