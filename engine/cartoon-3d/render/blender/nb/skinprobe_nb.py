# r2 skin probe (rule 355 / 335a, run lead r2 condition): renders one frame per character shot with the r2 cast textures,
# grades it with post_nb's own per-shot grade (calibrated on that frame), then reads face B/R and G/R on skin pixels around each head.
# stage 1 (blender): blender -b cc.blend --python skinprobe_nb.py -- OUTDIR PCT SAMPLES S01:100 ...   -> OUTDIR/<shot>_<f>.png + heads.json
# stage 2 (python):  python3 skinprobe_nb.py OUTDIR                                                  -> per-shot table (raw and graded)
import sys, json, os
if 'bpy' in sys.modules or os.path.basename(sys.argv[0]).startswith('blender'):
    import bpy
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view as w2c
    a=sys.argv[sys.argv.index('--')+1:]; out,pct,spp=a[0],int(a[1]),int(a[2]); req=[(x.split(':')[0],int(x.split(':')[1])) for x in a[3:]]
    sc=bpy.context.scene; sc.cycles.device='CPU'; sc.cycles.samples=spp; sc.render.resolution_percentage=pct
    vl=bpy.context.view_layer; os.makedirs(out,exist_ok=True); heads={}
    for n,f in req:
        for lc in vl.layer_collection.children:
            if lc.name.startswith('CHR_'): lc.exclude=(lc.name!='CHR_'+n)
        cam=bpy.data.objects['cam_'+n]; sc.camera=cam; sc.frame_set(f); key=f'{n}_{f:04d}'
        right=cam.matrix_world.to_3x3()@Vector((1,0,0)); hs=[]
        for r in [o for o in bpy.data.objects if o.get('is_char') and o.get('shot')==n and not o.hide_render]:
            hp=bpy.data.objects.get(r.name+'_hp')
            if not hp: continue
            c=hp.matrix_world.translation+Vector((0,0,0.20)); p=w2c(sc,cam,c)
            if p.z<=0 or not (0<p.x<1 and 0<p.y<1): continue
            w=abs(w2c(sc,cam,c+right*0.43).x-p.x); hs.append((r.name.split('_',1)[1],p.x,1-p.y,w))
        heads[key]=hs; sc.render.filepath=f'{out}/{key}.png'; bpy.ops.render.render(write_still=True); print('SKINSTILL',key,len(hs),flush=True)
    json.dump(heads,open(f'{out}/heads.json','w'))
elif sys.argv[1]=='--video':
    import numpy as np
    from PIL import Image
    d,hj=sys.argv[2],sys.argv[3]; heads=json.load(open(hj)); allg=[]
    for key,hs in sorted(heads.items()):
        fp=f'{d}/{key}.png'
        if not os.path.exists(fp): continue
        g=np.asarray(Image.open(fp).convert('RGB'),np.float32)/255; H_,W_=g.shape[:2]
        for nm,x,y,w in hs:
            r=max(3,int(w*W_*0.45)); cx,cy=int(x*W_),int(y*H_); p=g[max(0,cy-r):cy+r,max(0,cx-r):cx+r].reshape(-1,3)
            R,G,B=p[:,0],p[:,1],p[:,2]; sat=(R-B)/np.maximum(R,1e-4)
            m=(R>0.25)&(R>=G)&(G>=B)&(sat<0.45)&(sat>0.04)
            if m.sum()<12: continue
            q=p[m]; br=float(np.median(q[:,2]/q[:,0])); gr=float(np.median(q[:,1]/q[:,0])); ok=abs(br-0.86)<=0.04 and abs(gr-0.92)<=0.04
            allg.append((br,gr,ok)); print(f"{key:11s} {nm:13s} B/R {br:.3f}  G/R {gr:.3f}  {'PASS' if ok else 'FAIL'}")
    print('SKIN_VIDEO median B/R',round(float(np.median([a[0] for a in allg])),3),'G/R',round(float(np.median([a[1] for a in allg])),3),'pass',sum(a[2] for a in allg),'/',len(allg))
else:
    import numpy as np
    from PIL import Image
    out=sys.argv[1]; sys.argv=['post_nb.py','none','none']; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
    import post_nb as pn
    heads=json.load(open(f'{out}/heads.json')); rows=[]
    def faces(img,hs):
        H_,W_=img.shape[:2]; res=[]
        for nm,x,y,w in hs:
            r=max(3,int(w*W_*0.45)); cx,cy=int(x*W_),int(y*H_)
            p=img[max(0,cy-r):cy+r,max(0,cx-r):cx+r].reshape(-1,3)
            if len(p)==0: continue
            R,G,B=p[:,0],p[:,1],p[:,2]
            m=(R>0.25)&(R>=G)&(G>=B)&((R-B)/np.maximum(R,1e-4)<0.45)&((R-B)/np.maximum(R,1e-4)>0.04)   # skin-like: warm, light, not saturated hair/garments
            if m.sum()<12: continue
            q=p[m]; res.append((nm,float(np.median(q[:,2]/q[:,0])),float(np.median(q[:,1]/q[:,0])),int(m.sum())))
        return res
    print('SHOT FRAME  face          raw B/R  raw G/R  graded B/R  graded G/R  verdict')
    allg=[]
    for key,hs in sorted(heads.items()):
        n=key.split('_')[0]; x=np.asarray(Image.open(f'{out}/{key}.png').convert('RGB'),np.float32)/255
        pn.PROT[0]=(n in pn.SATPROT); pn.CUR[0]=n if os.environ.get('SKC','1')=='1' else ''; smp=[x[::2,::2]]
        b=pn.solve(smp,pn.TINT[n],pn.LT[n],pn.VIG[n])
        if n in pn.INTR:
            lo_,hi_=0.0,0.9
            for _ in range(14):
                k=(lo_+hi_)/2; rr=pn.vratio(pn.vig(pn.apply(smp[0],b[1]),k))
                if rr>0.38: lo_=k
                else: hi_=k
            pn.VIG[n]=round((lo_+hi_)/2,3); b=pn.solve(smp,pn.TINT[n],pn.LT[n],pn.VIG[n])
        g=pn.vig(pn.bloom(pn.floor_(pn.finish(pn.apply(x,b[1]))),pn.BLOOM),pn.VIG[n])
        Image.fromarray((g*255+0.5).astype(np.uint8)).save(f'{out}/{key}_graded.png')
        fr=dict((a[0],a) for a in faces(x,hs)); fg=faces(g,hs)
        for nm,br,gr,cnt in fg:
            r0=fr.get(nm); ok=abs(br-0.86)<=0.04 and abs(gr-0.92)<=0.04
            allg.append((br,gr,ok)); rows.append((key,nm,r0[1] if r0 else None,r0[2] if r0 else None,br,gr,ok))
            print(f"{key:11s} {nm:13s} {r0[1] if r0 else float('nan'):7.3f}  {r0[2] if r0 else float('nan'):7.3f}  {br:9.3f}  {gr:9.3f}   {'PASS' if ok else 'FAIL'}")
    if allg: print('SKIN_GRADED median B/R',round(float(np.median([a[0] for a in allg])),3),'G/R',round(float(np.median([a[1] for a in allg])),3),'pass',sum(a[2] for a in allg),'/',len(allg))
    json.dump(rows,open(f'{out}/skin_table.json','w'),indent=1)
# stage 3 (video): python3 skinprobe_nb.py --video FRAMEDIR HEADS.json  -> faces on frames taken from the finished graded video (captions included)
