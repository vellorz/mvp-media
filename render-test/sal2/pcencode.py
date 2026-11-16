# Encode each shot's PNG frames into a near-lossless MP4 for transfer.  blender.exe -b --python pcencode.py -- FRAMEDIR OUTDIR
import bpy, sys, os, glob
a=sys.argv[sys.argv.index('--')+1:]; fr,out=a[0],a[1]; os.makedirs(out,exist_ok=True)
for n in sorted(os.listdir(fr)):
    fs=sorted(glob.glob(os.path.join(fr,n,'f_*.png')))
    if not fs: continue
    first=int(os.path.basename(fs[0])[2:6])
    sc=bpy.data.scenes.new('enc_'+n)
    sc.render.resolution_x=1440; sc.render.resolution_y=2560; sc.render.resolution_percentage=100; sc.render.fps=30
    se=sc.sequence_editor_create()
    st=se.sequences.new_image(n,fs[0],1,1)
    for f in fs[1:]: st.elements.append(os.path.basename(f))
    sc.frame_start=1; sc.frame_end=len(fs)
    r=sc.render; r.image_settings.file_format='FFMPEG'; r.ffmpeg.format='MPEG4'; r.ffmpeg.codec='H264'; r.ffmpeg.constant_rate_factor='PERC_LOSSLESS'
    r.ffmpeg.ffmpeg_preset='GOOD'; r.filepath=os.path.join(out,f'{n}_{first:04d}_.mp4')
    sc.view_settings.view_transform='Standard'
    bpy.ops.render.render(animation=True,scene=sc.name)
    print('ENC',n,len(fs),flush=True)
print('ENC_DONE',flush=True)
