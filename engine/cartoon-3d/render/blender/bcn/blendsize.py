import bpy
im=bpy.data.images; print('IMAGES',len(im),'packed',sum(1 for i in im if i.packed_file),'packedMB',round(sum(i.packed_file.size for i in im if i.packed_file)/1e6,1))
me=sorted(bpy.data.meshes,key=lambda m:-len(m.vertices)); print('MESHES',len(me),'verts',sum(len(m.vertices) for m in me)); print([(m.name,len(m.vertices)) for m in me[:8]])
print('OBJ',len(bpy.data.objects),'MAT',len(bpy.data.materials),'ACT',len(bpy.data.actions),'FCURVE keys',sum(len(fc.keyframe_points) for a in bpy.data.actions for fc in a.fcurves))
