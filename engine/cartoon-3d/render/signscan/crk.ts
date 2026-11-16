import * as THREE from "three";
import { camAt, D0 } from "../../project/src/videos/chicago2/story";
const C = new THREE.PerspectiveCamera(40, 9 / 16, 0.1, 2000), V = new THREE.Vector3();
for (const f of [1252, 1273, 1297]) {
  const c = camAt(10, f); C.position.set(...c.pos); C.up.set(0, 1, 0); C.lookAt(...c.look); C.rotateZ(c.roll); C.fov = c.fov; C.updateProjectionMatrix(); C.updateMatrixWorld();
  let k = 0; const o: string[] = [];
  for (const z of [112.2, 114.6, 117.0, 119.6]) for (const x of [-12.3, -9.9, -7.5, -5.1, -2.7, -0.3, 2.1, 4.5, 6.9, 9.3, 11.7]) {
    if ((k * 7) % 5 === 4) { k++; continue; }
    const xx = x + (z % 2 ? 0.2 : -0.2); V.set(xx, D0 + 1.4, z).applyMatrix4(C.matrixWorldInverse); const d = -V.z;
    V.set(xx, D0 + 1.4, z).project(C);
    if (d > 0.1 && Math.abs(V.x) < 2.5) o.push(`${20 + k}@${xx.toFixed(1)},${z} d${d.toFixed(2)} x${V.x.toFixed(2)}`);
    k++;
  }
  console.log(f, c.pos.map((v) => v.toFixed(2)).join(","), o.join(" | "));
}
