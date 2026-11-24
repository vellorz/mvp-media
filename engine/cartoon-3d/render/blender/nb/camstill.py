# r9 (rule 302): camera moving on >= 85 % of frames, no fully still run over 30 f (1 s) except the ending hold.
# "moving" = image-plane motion >= 0.05 % of frame width per frame (Rick's slowest drift), from rotation, translation (at the target distance) and lens.
import bpy, json, math
sc=bpy.context.scene; SH=json.loads(sc['shots']); END=max(b for a,b in SH.values())
def owner(f):
    act=[n for n,(a,b) in SH.items() if a<=f<=b]; return act[-1]
prev=None; mv=[]
for f in range(0,END+1):
    n=owner(f); cam=bpy.data.objects['cam_'+n]; sc.frame_set(f)
    M=cam.matrix_world.copy(); tg=bpy.data.objects.get('tgt_'+n)
    dist=(tg.matrix_world.translation-M.translation).length if tg else 5.0
    fov=cam.data.angle_x if cam.data.sensor_fit!='VERTICAL' else cam.data.angle_x
    st=(n,M,cam.data.lens,dist,fov)
    if prev and prev[0]==n:
        q=prev[1].to_quaternion().rotation_difference(M.to_quaternion()); ang=abs(q.angle)
        rot=ang/fov*100; tr=(M.translation-prev[1].translation).length/(2*dist*math.tan(fov/2))*100
        zm=abs(st[2]-prev[2])/st[2]*50
        m=rot+tr+zm
    else: m=1.0   # a cut counts as a change
    mv.append(m); prev=st
mov=[m>=0.05 for m in mv]; share=sum(mov)/len(mov)*100
runs=[]; s=None
for f,v in enumerate(mov+[True]):
    if not v and s is None: s=f
    if v and s is not None: runs.append((s,f-1)); s=None
long=[r for r in runs if r[1]-r[0]+1>30 and r[1]<END-23]
print('CAMSTILL moving %.1f %%'%share,'still runs >30f (not ending):',[(a,b,owner(a)) for a,b in long])
print('CAMSTILL runs >8f:',[(a,b,owner(a)) for a,b in runs if b-a+1>8])
