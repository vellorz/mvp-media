# Render all shots on the PC GPU, resume-safe.  blender.exe -b sal_C.blend --python pcrender.py -- OUTDIR [shot ...]
import bpy, sys, json, os, time
a=sys.argv[sys.argv.index('--')+1:]; out=a[0]; only=a[1:]
pr=bpy.context.preferences.addons['cycles'].preferences
for dev in ('OPTIX','CUDA'):
    try:
        pr.compute_device_type=dev; pr.get_devices()
        if any(d.type==dev for d in pr.devices): break
    except Exception: pass
for d in pr.devices: d.use=(d.type==pr.compute_device_type)
sc=bpy.context.scene; sc.cycles.device='GPU'
if pr.compute_device_type=='OPTIX': sc.cycles.denoiser='OPTIX'
print('DEVICE',pr.compute_device_type,[d.name for d in pr.devices if d.use],flush=True)
SH=json.loads(sc['shots'])
order=only or list(SH.keys())
sc.render.use_overwrite=False; sc.render.use_placeholder=True
for n in order:
    f0,f1=SH[n]; sc.camera=bpy.data.objects['cam_'+n]; sc.frame_start=f0; sc.frame_end=f1
    os.makedirs(f'{out}/{n}',exist_ok=True)
    sc.render.filepath=f'{out}/{n}/f_'; t=time.time()
    bpy.ops.render.render(animation=True)
    print('SHOT_DONE',n,f0,f1,round(time.time()-t,1),flush=True)
print('ALL_DONE',flush=True)
