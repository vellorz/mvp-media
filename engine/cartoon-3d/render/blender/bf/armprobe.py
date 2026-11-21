# r7 rules 268-269: hands and forearms never cover a face (own or anyone else's).
# blender -b bf.blend --python armprobe.py   [env SHOTS=S01,S04 STEP=2]
import bpy, os, json, math, re
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view as w2c
sc=bpy.context.scene; SH=json.loads(sc['shots']); STEP=int(os.environ.get('STEP','2'))
only=[s for s in os.environ.get('SHOTS','').split(',') if s]
BEND={'arm':18,'armS':4,'pennant':0,'megaphone':15,'paper':20,'bag':20,'box':25,'camera':25,'chalk':30,'pen':30,'redpen':30}
ARM_W,ARM_H=0.744,0.558; HEAD_R=0.215   # r9: head disc radius of the Rick build (0.43 m wide); was 0.28 for the rounds 1-7 head
if os.environ.get('BENDS'): BEND.update(json.loads(os.environ['BENDS']))
def card_pts(o):
    k=o.name.split('_',)[-1]; m=re.search(r'_arm-?1_(.+)$',o.name); key=m.group(1) if m else 'arm'
    d=BEND.get(key.replace('arm_',''),BEND.get(key,18)); left='_arm-1_' in o.name
    pts=[]
    for t in (0.5,1.0):
        px=600+386*t*math.sin(math.radians(d)); py=330+386*t*math.cos(math.radians(d))
        x=(px-600)/1200*ARM_W; x=-x if left else x; z=(450-py)/900*ARM_H
        pts.append(o.matrix_world@Vector((x,0,z)))   # plane() bakes the upright rotation into the mesh: local x right, z up
    return pts
def ndc(cam,p): v=w2c(sc,cam,p); return Vector((v.x*9/16,v.y)),v.z
bad=[]
vl=bpy.context.view_layer
for shot,(f0,f1) in SH.items():
    if only and shot not in only: continue
    cam=bpy.data.objects['cam_'+shot]; sc.camera=cam
    for lc in vl.layer_collection.children:
        if lc.name.startswith('CHR_'): lc.exclude=(lc.name!='CHR_'+shot)
    roots=[o for o in bpy.data.objects if o.type=='EMPTY' and o.get('chr')==o.name and o.users_collection and o.users_collection[0].name=='CHR_'+shot]
    for f in range(f0,f1+1,STEP):
        sc.frame_set(f)
        heads=[]
        for r in roots:
            hp=bpy.data.objects.get(r.name+'_hp')
            if not hp or r.scale.x<0.01: continue
            faces=[o for o in hp.children if '_d_' in o.name and not o.hide_render]
            if not faces: continue
            c=faces[0].matrix_world.translation; e=c+cam.matrix_world.to_3x3()@Vector((HEAD_R*r.scale.x,0,0))
            (cn,cd),(en,_)=ndc(cam,c),ndc(cam,e)
            if cd<=0 or not(-0.1<cn.x*16/9<1.1 and -0.1<cn.y<1.1): continue
            heads.append((r.name,cn,(en-cn).length,cd))
        for r in roots:
            for o in r.children_recursive:
                if not re.search(r'_arm-?1_',o.name) or o.hide_render: continue
                for i,p in enumerate(card_pts(o)):
                    pn,pd=ndc(cam,p)
                    if pd<=0: continue
                    for hn,cn,rr,cd in heads:
                        own=(hn==r.name)
                        if (pn-cn).length<rr*0.92 and (own or pd<cd-0.02):
                            bad.append((shot,f,o.name,'hand' if i else 'forearm',hn,'OWN' if own else 'OTHER',round((pn-cn).length/rr,2)))
seen=set()
for b in bad:
    k=(b[0],b[2],b[4])
    if k in seen: continue
    seen.add(k); n=sum(1 for x in bad if (x[0],x[2],x[4])==k)
    print('ARMHIT',b[0],'f',b[1],b[2],b[3],'over',b[4],b[5],'d/r',b[6],'frames~',n*STEP)
print('ARMPROBE',len(bad),'samples',len(seen),'pairs')
