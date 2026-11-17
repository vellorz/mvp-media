"""Rule 168 check: every visible character head shows exactly ONE face decal on every frame.
  blender -b scene.blend --python check_faces.py      (reads sc['shots'])
Characters = objects named <char>_head with decals <char>_d_<face>. Prints FACE_BAD lines; exits 1 on any."""
import bpy,json,sys
sc=bpy.context.scene; S=json.loads(sc['shots']); O=bpy.data.objects
chars=[o.name[:-5] for o in O if o.name.endswith('_head') and not o.name.endswith('_ink')]
dec={c:[o for o in O if o.name.startswith(c+'_d_') and not o.name.endswith('_ink')] for c in chars}
bad=0
for n,(a,b) in S.items():
    for f in range(a,b+1):
        sc.frame_set(f)
        for c in chars:
            h=O[c+'_head']
            if h.hide_render or not dec[c]: continue
            k=sum(1 for d in dec[c] if not d.hide_render)
            if k!=1: bad+=1; print('FACE_BAD',n,f,c,k) if bad<40 else None
print('CHECK_FACES','FAIL' if bad else 'PASS',bad); sys.exit(1 if bad else 0)
