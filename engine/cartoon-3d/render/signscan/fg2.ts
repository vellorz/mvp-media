import * as THREE from "three";
import { camAt } from "../../project/src/videos/chicago2/story";
// [tk,a,b,u,v,d,wf,cw,ch,bx0,bx1,by0,by1]
const E: number[][] = JSON.parse(process.env.E!);
const C = new THREE.PerspectiveCamera(40, 9 / 16, 0.1, 2000), V = new THREE.Vector3(), up = new THREE.Vector3(0, 1, 0);
for (const [tk, a, b, u, v, d, wf, cw, ch, X0, X1, Y0, Y1] of E) {
  const c = camAt(tk, Math.round((a + Math.min(b, a + 60)) / 2));
  const F = new THREE.Vector3(c.look[0] - c.pos[0], c.look[1] - c.pos[1], c.look[2] - c.pos[2]).normalize(), R = new THREE.Vector3().crossVectors(F, up).normalize(), U = new THREE.Vector3().crossVectors(R, F);
  const hH = d * Math.tan((c.fov * Math.PI) / 360), hW = hH * (9 / 16), w = wf * 2 * hW, h = (w * ch) / cw;
  const ctr = new THREE.Vector3(...c.pos).addScaledVector(F, d).addScaledVector(R, u * hW).addScaledVector(U, v * hH);
  let s = `${tk} ${a}-${b} u${u} v${v} wf${wf}:`;
  for (let f = a; f < b; f += 6) {
    const k = camAt(tk, f); C.position.set(...k.pos); C.up.set(0, 1, 0); C.lookAt(...k.look); C.rotateZ(k.roll); C.fov = k.fov; C.updateProjectionMatrix(); C.updateMatrixWorld();
    const cr = new THREE.Vector3(1, 0, 0).applyQuaternion(C.quaternion);
    const P = (px: number, py: number) => V.copy(ctr).addScaledVector(cr, (px / cw - 0.5) * w).addScaledVector(up, (0.5 - py / ch) * h).project(C).clone();
    const b0 = P(X0, Y1), b1 = P(X1, Y0), wl = P(cw, 40), wr = P(0, 40);
    s += ` ${f}[b ${b0.x.toFixed(2)}..${b1.x.toFixed(2)} y${b0.y.toFixed(2)}..${b1.y.toFixed(2)} walls ${wr.x.toFixed(2)}/${wl.x.toFixed(2)}]`;
  }
  console.log(s);
}
