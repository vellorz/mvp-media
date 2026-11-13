const P: any = new Proxy(function () {}, { get: (_t, k) => (k === Symbol.toPrimitive ? () => 0 : k === "length" ? 0 : P), apply: () => P, construct: () => P, set: () => true });
(globalThis as any).document = { createElement: () => ({ width: 1, height: 1, getContext: () => P, style: {} }) };
(globalThis as any).window = globalThis; (globalThis as any).Image = function () { return P; };
import * as THREE from "three";
import { buildCity, SIGN_LIST } from "../../cart2/src/videos/chicago2/city";
import { setSight } from "../../cart2/src/videos/chicago2/build";
import { sightLines } from "../../cart2/src/videos/chicago2/world";
import { SHOTS, camAt, cutsOf, lift, D0, FPS } from "../../cart2/src/videos/chicago2/story";
const rays = sightLines("london"); setSight(rays);
const kit: any = new Proxy({}, { get: () => ({ scene: new THREE.Group() }) });
buildCity(new THREE.Group(), kit, rays);
console.error("signs", SIGN_LIST.length);
const C = new THREE.PerspectiveCamera(40, 9 / 16, 0.1, 2000), V = new THREE.Vector3();
const name = (m: any) => m.name || m.uuid.slice(0, 4);
const out: string[] = [];
for (const s of SHOTS) {
  const cuts = [s.a, ...cutsOf(s.id).filter((k) => k > s.a && k < s.b), s.b];
  for (let i = 0; i + 1 < cuts.length; i++) {
    const a = cuts[i], b = cuts[i + 1], cut = new Set<number>();
    for (let ff = a; ff < b; ff += 2) {
      const c = camAt(s.id, ff);
      C.position.set(...c.pos); C.up.set(0, 1, 0); C.lookAt(...c.look); C.rotateZ(c.roll); C.fov = c.fov; C.updateProjectionMatrix(); C.updateMatrixWorld();
      SIGN_LIST.forEach((r, j) => {
        const dy = r.which ? D0 + lift(r.which, s.id, ff / FPS) : 0;
        let inAll = true, lx = 0, rx = 0, by = 0, ty = 0, beh = 0;
        for (const [x, y, z] of r.c) { V.set(x, y + dy, z).applyMatrix4(C.matrixWorldInverse); if (V.z > -0.05) { beh++; inAll = false; continue; }
          V.applyMatrix4(C.projectionMatrix); if (Math.abs(V.x) > 0.985 || Math.abs(V.y) > 0.985) inAll = false;
          if (V.x < -1) lx++; if (V.x > 1) rx++; if (V.y < -1) by++; if (V.y > 1) ty++; }
        const n = r.c.length; if (!inAll && !(beh === n || lx === n || rx === n || by === n || ty === n)) cut.add(j);
      });
    }
    if (cut.size) out.push(`take ${s.id} ${a}-${b}: ` + [...cut].map((j) => `${j}@${SIGN_LIST[j].c[0].map((v) => v.toFixed(0)).join(",")}`).join(" "));
  }
}
console.log(out.join("\n"));
