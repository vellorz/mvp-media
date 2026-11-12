import * as THREE from "three";
import { buildCity, SIGN_LIST } from "../../project/src/videos/chicago2/city";
import { signState } from "../../project/src/videos/chicago2/signcut";
import { setSight } from "../../project/src/videos/chicago2/build";
import { sightLines } from "../../project/src/videos/chicago2/world";
import { SHOTS, camAt, cutsOf, lift, D0, FPS } from "../../project/src/videos/chicago2/story";
const rays = sightLines("london"); setSight(rays);
const kit: any = new Proxy({}, { get: () => { const g: any = new THREE.Group(); g.scene = new THREE.Group(); return g; } });
buildCity(new THREE.Group(), kit, rays);
console.error("signs", SIGN_LIST.length);
const C = new THREE.PerspectiveCamera(40, 9 / 16, 0.1, 2000), V = new THREE.Vector3();
const name = (m: any) => m.name || m.uuid.slice(0, 4);
const out: string[] = []; const MINH = +(process.env.MINH ?? 0.02);
for (const s of SHOTS) {
  const cuts = [s.a, ...cutsOf(s.id).filter((k) => k > s.a && k < s.b), s.b];
  for (let i = 0; i + 1 < cuts.length; i++) {
    const a = cuts[i], b = cuts[i + 1], cut = new Set<number>();
    for (let ff = a; ff < b; ff += 2) {
      const c = camAt(s.id, ff);
      C.position.set(...c.pos); C.up.set(0, 1, 0); C.lookAt(...c.look); C.rotateZ(c.roll); C.fov = c.fov; C.updateProjectionMatrix(); C.updateMatrixWorld();
      SIGN_LIST.forEach((r, j) => {
        if (signState(C, r.c, r.which ? D0 + lift(r.which, s.id, ff / FPS) : 0, MINH) === 2) cut.add(j);
      });
    }
    if (cut.size) out.push(`take ${s.id} ${a}-${b}: ` + [...cut].map((j) => `${j}@${SIGN_LIST[j].c[0].map((v) => v.toFixed(0)).join(",")}`).join(" "));
  }
}
console.log(out.join("\n"));
