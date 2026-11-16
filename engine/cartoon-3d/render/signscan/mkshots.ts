import { SHOTS, cutsOf } from "../../cart2/src/videos/chicago2/story";
import * as fs from "fs";
const d: [number, number][] = JSON.parse(fs.readFileSync("/home/user/cart2/out/c2/final20/dissolves.json", "utf8"));
const shots: any[] = []; for (const s of SHOTS) { const c = [s.a, ...cutsOf(s.id).filter((k) => k > s.a && k < s.b), s.b]; for (let i = 0; i + 1 < c.length; i++) shots.push({ id: s.id, a: c[i], b: c[i + 1] }); }
const fr = d.map((x) => x[0]).sort((a, b) => a - b), xf: [number, number][] = [];
for (const f of fr) { const l = xf[xf.length - 1]; if (l && f <= l[1] + 1) l[1] = f; else xf.push([f, f]); }
fs.writeFileSync("/home/user/cart2/out/c2/final20/shots.json", JSON.stringify({ shots, xfade: xf.map(([a, b]) => [a, b + 1]) }));
console.log(shots.length, xf.length);
