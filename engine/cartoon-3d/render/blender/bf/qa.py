# Full QA on a finished video: rick-spec metrics, transitions, dissolve curves, captions, owner's edge metric, loudness, black/frozen frames.
# python3 qa.py VIDEO.mp4 OUTDIR
import sys, os, subprocess, json, csv, re, numpy as np
V,O=sys.argv[1],sys.argv[2]; os.makedirs(O,exist_ok=True)
RS='/home/user/mvp-media/engine/cartoon-3d/rick-spec'
def run(c): return subprocess.run(c,shell=True,capture_output=True,text=True)
R={}
run(f'python3 {RS}/metrics.py {V} {O}/metrics.csv')
rows=list(csv.DictReader(open(f'{O}/metrics.csv')))
col=lambda k: np.array([float(r[k]) for r in rows])
luma,sat,edge,diff,p2,p98=col('luma'),col('sat'),col('edge'),col('diff'),col('p2'),col('p98')
d=diff[1:]
R['metrics']=dict(frames=len(rows),luma=round(float(luma.mean()),3),sat=round(float(sat.mean()),3),p2=round(float(np.median(p2)),3),p98=round(float(np.median(p98)),3),
    edge=round(float(edge.mean()),3),motion_median=round(float(np.median(d)),2),still_frames_pct=round(float((d<1).mean()*100),1))
# longest static run (diff<1) in frames
run_=0; mx=0
for x in d:
    run_=run_+1 if x<1 else 0; mx=max(mx,run_)
R['metrics']['longest_static_run_f']=int(mx)
t=run(f'python3 {RS}/transitions.py {V} {O}/transitions.csv'); R['transitions_raw']=t.stdout.strip()[-400:]
c=run(f'python3 {RS}/captions.py {V}'); R['captions']=c.stdout.strip()
# owner's edge metric on 24 evenly spaced stills
os.makedirs(f'{O}/edge24',exist_ok=True); n=len(rows)
for i,f in enumerate(np.linspace(5,n-6,24).astype(int)):
    run(f'ffmpeg -v error -y -i {V} -vf "select=eq(n\\,{f})" -vsync 0 -frames:v 1 {O}/edge24/e{i:02d}_f{f:04d}.png')
e=run(f'python3 /root/bf/src/edge.py {O}/edge24/*.png').stdout.split('\n'); vals=[float(x.split()[1]) for x in e if x.strip()]
R['edge24']=dict(values=vals,average=round(float(np.mean(vals)),1),minimum=min(vals))
o=run(f'ffmpeg -hide_banner -nostats -i {V} -af ebur128=peak=true -f null -').stderr; s=o[o.rfind('Summary'):]
R['loudness']=dict(I=float(re.search(r'I:\s+(-?[\d.]+) LUFS',s).group(1)),LRA=float(re.search(r'LRA:\s+([\d.]+) LU',s).group(1)),TP=float(re.search(r'Peak:\s+(-?[\d.]+) dBFS',s).group(1)))
b=run(f'ffmpeg -hide_banner -nostats -i {V} -vf blackdetect=d=0.05:pix_th=0.06 -an -f null -').stderr; R['black_segments']=len(re.findall('black_start',b))
fz=run(f'ffmpeg -hide_banner -nostats -i {V} -vf freezedetect=n=0.001:d=1.5 -an -f null -').stderr; R['frozen_segments']=len(re.findall('freeze_start',fz))
p=run(f'ffprobe -v error -show_entries stream=width,height,r_frame_rate,codec_name,bit_rate:format=duration,size -of json {V}').stdout; R['probe']=json.loads(p)
json.dump(R,open(f'{O}/QA_REPORT.json','w'),indent=1); print(json.dumps({k:v for k,v in R.items() if k!='probe'},indent=1))
