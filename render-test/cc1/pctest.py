# GPU alpha check (rule 203): render single test frames on the GPU before the full run.
# blender.exe -b cc.blend --python pctest.py -- OUTDIR S03:330 S16:1660 ...   -> OUTDIR/test_<shot>_<frame>.png
import bpy, sys, json, os
a=sys.argv[sys.argv.index('--')+1:]; out=a[0]; os.makedirs(out,exist_ok=True)
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
vl=bpy.context.view_layer; sc.render.resolution_percentage=100
for t in a[1:]:
    n,f=t.split(':'); f=int(f)
    for lc in vl.layer_collection.children:
        if lc.name.startswith('CHR_'): lc.exclude=(lc.name!='CHR_'+n)
    sc.camera=bpy.data.objects['cam_'+n]; sc.frame_set(f)
    sc.render.filepath=os.path.join(out,f'test_{n}_{f:04d}.png'); bpy.ops.render.render(write_still=True)
    print('TEST_DONE',n,f,flush=True)
