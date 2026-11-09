import sys, json
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8")
import subprocess, numpy as np
raw = subprocess.run(["ffmpeg","-v","quiet","-i",sys.argv[1],"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout
segs, _ = m.transcribe(np.frombuffer(raw,np.float32), word_timestamps=True, beam_size=5)
words = []
for s in segs:
    for w in s.words: words.append({"w": w.word.strip(), "s": round(w.start,3), "e": round(w.end,3)})
json.dump(words, open(sys.argv[2], "w"), indent=0)
print(" ".join(w["w"] for w in words))
