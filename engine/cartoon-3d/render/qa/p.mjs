// bundle the short's story.ts first: npx esbuild src/videos/<name>/story.ts --format=esm --outfile=/tmp/story.js
const S = await import(process.env.STORY_JS || "/tmp/story.js");
const sub=(a,b)=>a.map((v,i)=>v-b[i]), dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2], cr=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]], nz=a=>{const l=Math.hypot(...a);return a.map(v=>v/l)};
export const proj=(c,p)=>{const f=nz(sub(c.look,c.pos)), r=nz(cr(f,[0,1,0])), u=cr(r,f); const d=sub(p,c.pos), z=dot(d,f); const t=Math.tan(c.fov*Math.PI/360); return [+(dot(d,r)/z/(t*9/16)).toFixed(2), +(dot(d,u)/z/t).toFixed(2), +z.toFixed(2)]};
export {S};
