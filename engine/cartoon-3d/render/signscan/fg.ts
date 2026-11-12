import * as THREE from "three";
import { camAt } from "../../project/src/videos/chicago2/story";
const E: [number, number, number, number, number, number, number, boolean][] = JSON.parse(process.env.E!);
const C = new THREE.PerspectiveCamera(40, 9 / 16, 0.1, 2000), V = new THREE.Vector3(), up = new THREE.Vector3(0, 1, 0);
for (const [tk, a, b, u, v, d, wf, flip] of E) {
  const c = camAt(tk, Math.round((a + Math.min(b, a + 60)) / 2));
  const F = new THREE.Vector3(c.look[0] - c.pos[0], c.look[1] - c.pos[1], c.look[2] - c.pos[2]).normalize(), R = new THREE.Vector3().crossVectors(F, up).normalize(), U = new THREE.Vector3().crossVectors(R, F);
  const hH = d * Math.tan((c.fov * Math.PI) / 360), hW = hH * (9 / 16), w = wf * 2 * hW, h = (w * 520) / 760;
  const ctr = new THREE.Vector3(...c.pos).addScaledVector(F, d).addScaledVector(R, u * hW).addScaledVector(U, v * hH);
  const bx0 = (flip ? 110 : 90) / 760 - 0.5, bx1 = (flip ? 670 : 650) / 760 - 0.5, by0 = 0.5 - 150 / 520, by1 = 0.5 - 470 / 520;
  let worst = "";
  for (let f = a; f < b; f += 3) {
    const k = camAt(tk, f); C.position.set(...k.pos); C.up.set(0, 1, 0); C.lookAt(...k.look); C.rotateZ(k.roll); C.fov = k.fov; C.updateProjectionMatrix(); C.updateMatrixWorld();
    const cr = new THREE.Vector3(1, 0, 0).applyQuaternion(C.quaternion), cu = new THREE.Vector3(0, 1, 0);
    const xs: number[] = [], ys: number[] = [];
    for (const [px, py] of [[bx0, by0], [bx1, by0], [bx0, by1], [bx1, by1]]) { V.copy(ctr).addScaledVector(cr, px * w).addScaledVector(cu, py * h).project(C); xs.push(V.x); ys.push(V.y); }
    const ok = Math.max(...xs.map(Math.abs), ...ys.map(Math.abs)) < 0.985;
    worst += ` ${f}[${Math.min(...xs).toFixed(2)},${Math.max(...xs).toFixed(2)} y${Math.min(...ys).toFixed(2)},${Math.max(...ys).toFixed(2)}]`;
  }
  console.log(tk, a, b, worst || "board fully in frame");
}
