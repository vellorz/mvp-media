# GPU render test. Run: blender.exe -b flo_C.blend --python gputest.py -- <outdir> <tag> [frames...]
import bpy, sys, time
a=sys.argv[sys.argv.index('--')+1:]; out,tag=a[0],a[1]; frames=[int(x) for x in a[2:]] or [170,230,280]
p=bpy.context.preferences.addons['cycles'].preferences
for kind in ('OPTIX','CUDA'):
    try:
        p.compute_device_type=kind; p.get_devices()
        devs=[d for d in p.devices if d.type==kind]
        if devs: break
    except Exception as e: print('DEV_ERR',kind,e)
for d in p.devices: d.use=(d.type==p.compute_device_type)
print('DEVICE',p.compute_device_type,[d.name for d in p.devices if d.use])
sc=bpy.context.scene; sc.cycles.device='GPU'
def camfor(f): return 'camA' if f<92 else 'camB' if f<146 else 'camC' if f<256 else 'camD'
for f in frames:
    sc.frame_set(f); sc.camera=bpy.data.objects[camfor(f)]; sc.render.filepath=f'{out}/{tag}_{f:04d}.png'
    t=time.time(); bpy.ops.render.render(write_still=True); print('TIME',tag,f,round(time.time()-t,2),flush=True)
