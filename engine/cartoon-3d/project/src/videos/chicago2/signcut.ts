import * as THREE from "three";
/** rule 64: 0 = sign fully out of frame (or too small to read), 1 = fully in frame, 2 = lettering cut by the frame edge.
 *  The board is sampled on a 9x3 grid; samples behind the lens count as out of frame. */
const V = new THREE.Vector3();
export const signState = (C: THREE.Camera, c: [number, number, number][], dy: number, minH = 0.02): 0 | 1 | 2 => {
  const [p0, p1, p2] = c; // p0 bottom-left, p1 bottom-right, p2 top-left (as recorded)
  let inn = 0, out = 0, y0 = 9, y1 = -9;
  for (let i = 0; i <= 8; i++) for (let j = 0; j <= 2; j++) {
    const u = i / 8, v = j / 2;
    V.set(p0[0] + (p1[0] - p0[0]) * u + (p2[0] - p0[0]) * v, p0[1] + (p1[1] - p0[1]) * u + (p2[1] - p0[1]) * v + dy, p0[2] + (p1[2] - p0[2]) * u + (p2[2] - p0[2]) * v);
    V.applyMatrix4(C.matrixWorldInverse);
    if (V.z > -0.05) { out++; continue; }
    V.applyMatrix4(C.projectionMatrix);
    if (Math.abs(V.x) <= 0.985 && Math.abs(V.y) <= 0.985) { inn++; y0 = Math.min(y0, V.y); y1 = Math.max(y1, V.y); } else out++;
  }
  if (!inn) return 0;
  if (!out) return 1;
  return y1 - y0 < minH * 0.5 ? 0 : 2;
};
