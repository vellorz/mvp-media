# quick set previews for the rule 330 reference sheets: blender -b bcn_sets.blend -P setprev_bcn.py -- OUTDIR
import bpy, sys, math, os
OUT=sys.argv[sys.argv.index('--')+1]; os.makedirs(OUT,exist_ok=True); sc=bpy.context.scene
cd=bpy.data.cameras.new('pv'); cd.lens=24; co=bpy.data.objects.new('pv',cd); sc.collection.objects.link(co); sc.camera=co
tg=bpy.data.objects.new('pvt',None); sc.collection.objects.link(tg); c=co.constraints.new('TRACK_TO'); c.target=tg; c.track_axis='TRACK_NEGATIVE_Z'; c.up_axis='UP_Y'
r=sc.render; r.engine='CYCLES'; r.resolution_x=1440; r.resolution_y=2560; r.resolution_percentage=30; sc.cycles.samples=12; sc.cycles.use_denoising=True; sc.cycles.device='CPU'
sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Punchy'
for o in bpy.data.objects:
    if o.type=='LIGHT' and o.data.type!='SUN': o.visible_camera=False
V={'R_street_night':(60,(-1.0,-2.2,1.7),(0,6,2.6),26),'N_newsroom':(560,(299.6,-3.6,1.6),(300,2,1.4),24),'N_desk_paper':(100,(303.0,-2.3,1.4),(303,-1.6,0.78),34),
   'G_gym':(320,(600.5,-5.2,1.9),(600.5,1.5,1.3),22),'V_velodrome':(1000,(992,-24,8.5),(1000,0,0.5),22),'B_stadium':(1480,(1501,-22,12),(1500,10,6),22),
   'K_rambla_kiosk':(1700,(2005.0,-0.9,1.6),(2001.4,0.6,1.5),28),'K_rambla_wide':(250,(1976,-3.0,1.6),(1976,8,2.5),24)}
for n,(f,l,t,lens) in V.items():
    sc.frame_set(f); co.location=l; tg.location=t; cd.lens=lens; r.filepath=f'{OUT}/{n}.png'; bpy.ops.render.render(write_still=True); print('PV',n,flush=True)
