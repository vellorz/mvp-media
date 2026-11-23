# Render all shots on the PC GPU, resume-safe.  blender.exe -b cc.blend --python pcrender.py -- OUTDIR [shot ...]
# Each shot renders with only its own CHR_<shot> collection enabled (other shots' cast are excluded) and its own camera.
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
# Cape Cod cc1: the blend carries cloud-CPU speed settings (4 spp); on the GPU restore the BF quality settings
sc.cycles.samples=8; sc.cycles.max_bounces=4; sc.cycles.diffuse_bounces=2; sc.cycles.transparent_max_bounces=16
print('DEVICE',pr.compute_device_type,[d.name for d in pr.devices if d.use],flush=True)
SH=json.loads(sc['shots']); vl=bpy.context.view_layer
order=only or list(SH.keys())
sc.render.use_overwrite=False; sc.render.use_placeholder=True; sc.render.resolution_percentage=100
for n in order:
    for lc in vl.layer_collection.children:
        if lc.name.startswith('CHR_'): lc.exclude=(lc.name!='CHR_'+n)
    for lc in vl.layer_collection.children:   # cc r2: re-enable shared dressing (R_1741, R_today); excluding a parent leaves its children flagged excluded, so shared sets vanished in every shot after the first
        if lc.name=='CHR_'+n:
            for ch_ in lc.children: ch_.exclude=False
    f0,f1=SH[n]; sc.camera=bpy.data.objects['cam_'+n]; sc.frame_start=f0; sc.frame_end=f1
    os.makedirs(f'{out}/{n}',exist_ok=True)
    sc.render.filepath=f'{out}/{n}/f_'; t=time.time()
    bpy.ops.render.render(animation=True)
    print('SHOT_DONE',n,f0,f1,round(time.time()-t,1),flush=True)
print('ALL_DONE',flush=True)
