// bundle story.ts to /tmp/story.js first (see p.mjs)
const { camAt, shotAt, TOTAL } = await import(process.env.STORY_JS || "/tmp/story.js");
const sub=(a,b)=>a.map((v,i)=>v-b[i]), dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2], cr=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]], nz=a=>{const l=Math.hypot(...a);return a.map(v=>v/l)};
const basis=c=>{const f=nz(sub(c.look,c.pos)), r=nz(cr(f,[0,1,0])), u=cr(r,f); return {f,r,u}};
const proj=(c,p)=>{const {f,r,u}=basis(c); const d=sub(p,c.pos), z=dot(d,f); const t=Math.tan(c.fov*Math.PI/360); return [dot(d,r)/z/(t*9/16)*90, dot(d,u)/z/t*160]};
const out=[]; let per={};
for(let f=0; f<TOTAL-1; f++){ const id=shotAt(f).id; if(shotAt(f+1).id!==id) continue;
  const c0=camAt(id,f), c1=camAt(id,f+1); if(Math.hypot(...sub(c1.pos,c0.pos))>3) continue; // cut
  const {f:F,r,u}=basis(c0), L=Math.hypot(...sub(c0.look,c0.pos)); let s=0,n=0;
  for(const D of [L, 2.5*L]) for(const a of [-0.6,0,0.6]) for(const b of [-0.6,0,0.6]){ const t=Math.tan(c0.fov*Math.PI/360)*D; const p=c0.pos.map((v,i)=>v+F[i]*D+r[i]*a*t*9/16+u[i]*b*t); const p0=proj(c0,p), p1=proj(c1,p); s+=Math.hypot(p1[0]-p0[0],p1[1]-p0[1]); n++; }
  out.push(s/n); (per[id]??=[]).push(s/n); }
const q=(a,k)=>{const b=[...a].sort((x,y)=>x-y);return b[Math.floor(k*(b.length-1))]};
console.log('ALL med',q(out,.5).toFixed(2),'p90',q(out,.9).toFixed(2),'max',q(out,1).toFixed(2));
for(const id in per) console.log(id,'med',q(per[id],.5).toFixed(2),'p90',q(per[id],.9).toFixed(2),'max',q(per[id],1).toFixed(2));
