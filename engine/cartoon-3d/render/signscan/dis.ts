import { layersFor } from "/home/user/cart2/src/videos/chicago2/layers";
import { TOTAL } from "/home/user/cart2/src/videos/chicago2/story";
const out: [number, number][] = [];
for (let n = 0; n < (TOTAL as number); n++) { const L = layersFor(n); if (L.length > 1) out.push([n, L[1].alpha]); }
console.log(JSON.stringify(out));
