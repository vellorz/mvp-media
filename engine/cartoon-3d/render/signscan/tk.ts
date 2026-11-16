import { layersFor } from "/home/user/cart2/src/videos/chicago2/layers";
let prev = "";
for (let n = 0; n < 2200; n++) { const L = layersFor(n); const k = L.map(l => l.id).join("+"); if (k !== prev) { console.log(n, k, L.map(l => Math.round(l.of)).join(",")); prev = k; } }
