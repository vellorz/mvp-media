// r2 sets for the Chicago short (owner rules 16-19: new places, interiors, readable props, nothing empty):
//  DINING ROOM  the Tremont House dining room (S1c tea while the hotel rises, S8a the guests barely noticed)
//  DEPOT        a railway platform with a Pullman sleeping car (S10b "America's famous sleeping cars")
//  BOATS        tugs and a barge on the river that drift with the current and turn back with it (S11)
//  LANTERNS     lanterns hung under the Tremont floor so the 500 men underneath are seen (S7b)
import * as THREE from "three";
import { Batch, boxGeo, V, lam, house, prop, Kit, setSight, Ray } from "./build";
import { ctex, rng, grassHD } from "./paint";
import { D0, DINE, TAB_Y, TABLES, STA, CAR, PLAT, BOATS, TRE, PARLOR } from "./story";

const UP = V(0, 1, 0);
const UNIT = new THREE.BoxGeometry(1, 1, 1);
const box = (b: Batch, m: THREE.Material, x0: number, y0: number, z0: number, x1: number, y1: number, z1: number, tile = 0) =>
  b.add(boxGeo(V(Math.min(x0, x1), Math.min(y0, y1), Math.min(z0, z1)), V(Math.max(x0, x1), Math.max(y0, y1), Math.max(z0, z1)), tile), m);
const cyl = (b: Batch, m: THREE.Material, x: number, y: number, z: number, r0: number, r1: number, h: number, seg = 14) => {
  const g = new THREE.CylinderGeometry(r1, r0, h, seg); g.translate(x, y + h / 2, z); b.add(g, m);
};
const bar = (b: Batch, m: THREE.Material, a: THREE.Vector3, c: THREE.Vector3, r: number) => {
  const d = c.clone().sub(a), L = d.length();
  if (L < 1e-4) return;
  const q = new THREE.Quaternion().setFromUnitVectors(UP, d.normalize());
  b.add(UNIT, m, new THREE.Matrix4().compose(a.clone().add(c).multiplyScalar(0.5), q, V(2 * r, L, 2 * r)));
};
const pole = (b: Batch, m: THREE.Material, a: THREE.Vector3, c: THREE.Vector3, r: number, seg = 8) => {
  const d = c.clone().sub(a), L = d.length();
  if (L < 1e-4) return;
  const g = new THREE.CylinderGeometry(r, r, L, seg);
  const q = new THREE.Quaternion().setFromUnitVectors(UP, d.normalize());
  b.add(g, m, new THREE.Matrix4().compose(a.clone().add(c).multiplyScalar(0.5), q, V(1, 1, 1)));
};
const quad = (b: Batch, m: THREE.Material, a: THREE.Vector3, bb: THREE.Vector3, c: THREE.Vector3, d: THREE.Vector3, u = 1, v = 1) => {
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute([a, bb, c, a, c, d].flatMap((p) => [p.x, p.y, p.z]), 3));
  g.setAttribute("uv", new THREE.Float32BufferAttribute([0, 0, u, 0, u, v, 0, 0, u, v, 0, v], 2));
  g.computeVertexNormals(); b.add(g, m);
};
const floorQ = (b: Batch, m: THREE.Material, x0: number, x1: number, z0: number, z1: number, y: number, tile: number) =>
  quad(b, m, V(x0, y, z1), V(x1, y, z1), V(x1, y, z0), V(x0, y, z0), (x1 - x0) / tile, (z1 - z0) / tile);
const grp = (parent: THREE.Object3D, fill: (b: Batch) => void, cast = true) => { const g = new THREE.Group(), b = new Batch(); fill(b); b.build(g, cast); parent.add(g); return g; };
const matTex = (key: string, t: THREE.Texture, rx = 1, ry = 1) => lam(key, () => { const m = t; m.wrapS = m.wrapT = THREE.RepeatWrapping; m.repeat.set(rx, ry); return { map: m }; });
/** unlit glowing material (HDR: bloom picks it up) */
const glow = (key: string, r: number, g: number, bl: number) => {
  const m = GLOW.get(key) ?? new THREE.MeshBasicMaterial({ color: new THREE.Color(r, g, bl), toneMapped: true });
  GLOW.set(key, m); return m;
};
const GLOW = new Map<string, THREE.MeshBasicMaterial>();

const M = {
  wood: () => lam("cWood", () => ({ color: "#8a5a34" })),
  woodD: () => lam("cWoodD", () => ({ color: "#5a3a24" })),
  white: () => lam("cWhite", () => ({ color: "#f4f2ec" })),
  cloth: () => lam("cCloth", () => ({ color: "#f6f3ea" })),
  brass: () => lam("cBrass", () => ({ color: "#c9a04a" })),
  iron: () => lam("cIron", () => ({ color: "#33343a" })),
  steel: () => lam("cSteel", () => ({ color: "#7d838c" })),
  red: () => lam("cRed", () => ({ color: "#a8322c" })),
  plush: () => lam("cPlush", () => ({ color: "#8c2f3f" })),
  green: () => lam("cGreenP", () => ({ color: "#3f5a3a" })),
  cream: () => lam("cCream", () => ({ color: "#efe2bf" })),
  gravel: () => lam("cGravel", () => ({ map: gravelT() })),
  china: () => lam("cChina", () => ({ color: "#f8f6f0" })),
  blueC: () => lam("cBlueC", () => ({ color: "#3f6fb5" })),
};

// ---------------- textures ----------------
const wallpaperT = () => ctex("cWallpaper", 256, 512, (g) => {
  g.fillStyle = "#e9d8b0"; g.fillRect(0, 0, 256, 512);
  for (let x = 0; x < 256; x += 64) { g.fillStyle = "#dcc796"; g.fillRect(x + 26, 0, 12, 330); }
  g.fillStyle = "#c9a96a"; for (let y = 30; y < 330; y += 64) for (let x = 0; x < 256; x += 64) { g.beginPath(); g.moveTo(x + 32, y - 10); g.lineTo(x + 40, y); g.lineTo(x + 32, y + 10); g.lineTo(x + 24, y); g.fill(); }
  g.fillStyle = "#6a3a2a"; g.fillRect(0, 330, 256, 182); g.fillStyle = "#4a281c"; g.fillRect(0, 326, 256, 10);
  g.strokeStyle = "#3a2016"; g.lineWidth = 4; for (let x = 8; x < 256; x += 128) g.strokeRect(x, 352, 112, 140);
});
const carpetT = () => ctex("cCarpet", 256, 256, (g) => {
  g.fillStyle = "#8c2f3f"; g.fillRect(0, 0, 256, 256);
  g.strokeStyle = "#c9a04a"; g.lineWidth = 5; g.strokeRect(14, 14, 228, 228);
  g.fillStyle = "#6a1f2f"; for (const [x, y] of [[64, 64], [192, 64], [64, 192], [192, 192], [128, 128]]) { g.beginPath(); g.moveTo(x, y - 30); g.lineTo(x + 30, y); g.lineTo(x, y + 30); g.lineTo(x - 30, y); g.fill(); }
});
/** the street from the hotel's second floor: 1860s brick fronts across a muddy Lake Street */
const streetViewT = () => ctex("cStreetView", 1024, 512, (g, r) => {
  const sk = g.createLinearGradient(0, 0, 0, 300); sk.addColorStop(0, "#5f95dc"); sk.addColorStop(1, "#c8dcf0");
  g.fillStyle = sk; g.fillRect(0, 0, 1024, 512);
  for (const [x, y, s] of [[200, 70, 1], [760, 50, 1.2]]) { g.fillStyle = "#fbf8f1"; for (const [dx, dy, rr] of [[0, 0, 30], [32, 8, 24], [-30, 9, 22], [10, -16, 24]]) { g.beginPath(); g.arc(x + dx * s, y + dy * s, rr * s, 0, Math.PI * 2); g.fill(); } }
  let x = -10;
  while (x < 1024) {
    const w = 110 + r() * 80, h = 190 + r() * 110;
    g.fillStyle = ["#b85a3a", "#c98a5a", "#e3c08a", "#9a4a34", "#d9b48a"][Math.floor(r() * 5)]; g.fillRect(x, 420 - h, w, h);
    g.fillStyle = "#f4ead2"; g.fillRect(x - 3, 420 - h, w + 6, 10);
    g.fillStyle = "#2f4a6a"; for (let wy = 420 - h + 26; wy < 380; wy += 46) for (let wx = x + 12; wx < x + w - 22; wx += 30) { g.fillRect(wx, wy, 16, 26); g.fillStyle = "#2f5a43"; g.fillRect(wx - 6, wy, 5, 26); g.fillRect(wx + 17, wy, 5, 26); g.fillStyle = "#2f4a6a"; }
    g.fillStyle = "#3b2f24"; g.fillRect(x + w * 0.2, 386, w * 0.6, 22);
    x += w + 4;
  }
  g.fillStyle = "#8a6a4a"; g.fillRect(0, 420, 1024, 92);
  g.fillStyle = "#6f5238"; for (let i = 0; i < 40; i++) g.fillRect(r() * 1024, 430 + r() * 80, 30 + r() * 60, 3);
  g.fillStyle = "#c08a52"; g.fillRect(0, 414, 1024, 8);
});
const gravelT = () => { const t = ctex("cGravel", 256, 256, (g, r) => {
  g.fillStyle = "#9a8e7a"; g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 1400; i++) { g.fillStyle = ["#8a7e6a", "#aca08a", "#7a6e5c", "#b8ad98"][i % 4]; g.fillRect(r() * 256, r() * 256, 2 + r() * 3, 2 + r() * 3); }
}); t.repeat.set(1, 1); return t; };
const plankT = () => ctex("cPlatPlanks", 256, 256, (g, r) => {
  g.fillStyle = "#a8743f"; g.fillRect(0, 0, 256, 256);
  for (let y = 0; y < 256; y += 32) { g.fillStyle = y % 64 ? "#9a6a38" : "#b07e48"; g.fillRect(0, y, 256, 30); g.fillStyle = "#4a3020"; g.fillRect(0, y + 30, 256, 2); g.fillRect((y * 37) % 256, y, 2, 30); }
  for (let i = 0; i < 80; i++) { g.fillStyle = "rgba(60,40,20,0.25)"; g.fillRect(r() * 256, r() * 256, 18, 1); }
});
/** the sleeping car's side: Pullman green, cream letterboard, curtained windows */
const carSideT = () => ctex("cCarSide", 2048, 384, (g) => {
  g.fillStyle = "#3d5a3a"; g.fillRect(0, 0, 2048, 384);
  g.fillStyle = "#e8d6a0"; g.fillRect(0, 22, 2048, 70); g.fillStyle = "#b8955a"; g.fillRect(0, 22, 2048, 5); g.fillRect(0, 87, 2048, 5);
  g.fillStyle = "#3b2416"; g.font = "bold 58px Georgia, serif"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("P  U  L  L  M  A  N", 1024, 58);
  g.font = "bold 30px Georgia, serif"; g.fillText("SLEEPING CAR", 300, 58); g.fillText("No. 9", 1760, 58);
  for (let i = 0; i < 14; i++) {
    const x = 120 + i * 130;
    g.fillStyle = "#d9b04a"; g.fillRect(x - 6, 120, 72, 118);
    g.fillStyle = "#9cc3e6"; g.fillRect(x, 126, 60, 106);
    g.fillStyle = "#b8343a"; g.fillRect(x, 126, 60, 40); g.beginPath(); g.moveTo(x, 166); g.quadraticCurveTo(x + 30, 186, x + 60, 166); g.fill();
    g.fillStyle = "#2a3b28"; g.fillRect(x - 6, 250, 72, 4);
  }
  g.fillStyle = "#2a3b28"; for (const x of [70, 1978]) g.fillRect(x - 14, 110, 28, 260);
  g.fillStyle = "#d9b04a"; g.fillRect(0, 352, 2048, 6);
});
const depotWallT = () => ctex("cDepotWall", 512, 512, (g, r) => {
  g.fillStyle = "#a8523a"; g.fillRect(0, 0, 512, 512);
  for (let y = 0; y < 512; y += 16) for (let x = (y / 16) % 2 ? -16 : 0; x < 512; x += 32) { g.fillStyle = ["#a8523a", "#9a4a34", "#b85e40", "#a04c36"][Math.floor(r() * 4)]; g.fillRect(x + 1, y + 1, 30, 14); }
  g.fillStyle = "#e8d6b0"; g.fillRect(0, 0, 512, 22);
});
const depotSignT = () => ctex("cDepotSign", 1024, 160, (g) => {
  g.fillStyle = "#2f4a3a"; g.fillRect(0, 0, 1024, 160); g.strokeStyle = "#e8d6a0"; g.lineWidth = 10; g.strokeRect(10, 10, 1004, 140);
  g.fillStyle = "#f2e3b8"; g.font = "bold 84px Georgia, serif"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("UNION DEPOT", 512, 84);
});

// ---------------- dining room ----------------
type Win = { at: number; w: number; y0: number; y1: number };
const room = (b: Batch, x0: number, x1: number, y: number, z0: number, z1: number, h: number, wall: THREE.Material, floor: THREE.Material, wins: Win[], view: THREE.Material, ceil: THREE.Material) => {
  floorQ(b, floor, x0, x1, z0, z1, y + 0.015, 2.4);
  quad(b, ceil, V(x0, y + h, z0), V(x1, y + h, z0), V(x1, y + h, z1), V(x0, y + h, z1), (x1 - x0) / 3, (z1 - z0) / 3);
  let x = x0, wi = 0;
  const seg = (a: number, c: number, ya: number, yb: number) => { if (c - a > 0.01 && yb - ya > 0.01) quad(b, wall, V(c, ya, z1), V(a, ya, z1), V(a, yb, z1), V(c, yb, z1), (c - a) / 2.4, (yb - ya) / h); };
  for (const w of [...wins].sort((p, q) => p.at - q.at)) {
    seg(x, w.at, y, y + h); seg(w.at, w.at + w.w, y, y + w.y0); seg(w.at, w.at + w.w, y + w.y1, y + h);
    x = w.at + w.w;
    box(b, M.white(), w.at - 0.1, y + w.y0 - 0.1, z1 - 0.14, w.at + w.w + 0.1, y + w.y0, z1 + 0.08);
    bar(b, M.white(), V(w.at + w.w / 2, y + w.y0, z1), V(w.at + w.w / 2, y + w.y1, z1), 0.03);
    for (const k of [0.35, 0.7]) bar(b, M.white(), V(w.at, y + w.y0 + (w.y1 - w.y0) * k, z1), V(w.at + w.w, y + w.y0 + (w.y1 - w.y0) * k, z1), 0.025);
    for (const xx of [w.at, w.at + w.w]) bar(b, M.white(), V(xx, y + w.y0, z1), V(xx, y + w.y1, z1), 0.05);
    bar(b, M.white(), V(w.at, y + w.y1, z1), V(w.at + w.w, y + w.y1, z1), 0.05);
    // red drapes either side, on a brass rod
    bar(b, M.brass(), V(w.at - 0.5, y + w.y1 + 0.18, z1 - 0.12), V(w.at + w.w + 0.5, y + w.y1 + 0.18, z1 - 0.12), 0.025);
    for (const xx of [w.at - 0.45, w.at + w.w + 0.05]) box(b, M.plush(), xx, y + 0.05, z1 - 0.2, xx + 0.4, y + w.y1 + 0.2, z1 - 0.1);
    const zv = z1 + 4 + 0.3 * wi++, ex = 4; // staggered: overlapping coplanar view planes z-fight (black flicker)
    quad(b, view, V(w.at + w.w + ex, y + w.y0 - 3.2, zv), V(w.at - ex, y + w.y0 - 3.2, zv), V(w.at - ex, y + w.y1 + 2.4, zv), V(w.at + w.w + ex, y + w.y1 + 2.4, zv));
  }
  seg(x, x1, y, y + h);
  quad(b, wall, V(x0, y, z0), V(x1, y, z0), V(x1, y + h, z0), V(x0, y + h, z0), (x1 - x0) / 2.4, 1);
  quad(b, wall, V(x0, y, z1), V(x0, y, z0), V(x0, y + h, z0), V(x0, y + h, z1), (z1 - z0) / 2.4, 1);
  quad(b, wall, V(x1, y, z0), V(x1, y, z1), V(x1, y + h, z1), V(x1, y + h, z0), (z1 - z0) / 2.4, 1);
};
const teacup = (b: Batch, x: number, y: number, z: number) => {
  cyl(b, M.china(), x, y, z, 0.075, 0.075, 0.008, 16);
  cyl(b, M.china(), x, y + 0.008, z, 0.03, 0.045, 0.05, 14);
  const h = new THREE.TorusGeometry(0.018, 0.005, 6, 10); h.translate(x + 0.05, y + 0.035, z); b.add(h, M.china());
};

export type SetRefs = { boats: THREE.Group[]; lanterns: THREE.Group; depotGlow: THREE.Group };

export const buildSets = (root: THREE.Object3D, kit: Kit, rays: Ray[], tre: THREE.Group): SetRefs => {
  setSight(rays);
  const S = {} as SetRefs;

  // ======== DINING ROOM ========
  {
    const R = DINE, b = new Batch();
    const x0 = R.x - R.w / 2, x1 = R.x + R.w / 2, z0 = R.z - R.d / 2, z1 = R.z + R.d / 2;
    room(b, x0, x1, D0, z0, z1, R.h, lam("cWallM", () => ({ map: wallpaperT() })), matTex("cCarpetM", carpetT(), 1, 1),
      [{ at: R.x - 4.6, w: 1.6, y0: 0.7, y1: 3.1 }, { at: R.x - 0.8, w: 1.6, y0: 0.7, y1: 3.1 }, { at: R.x + 3.0, w: 1.6, y0: 0.7, y1: 3.1 }],
      lam("cStreetViewM", () => ({ map: streetViewT() })), lam("cCeilM", () => ({ color: "#f2e8d0" })));
    // ceiling cornice + two chandeliers (brass ring, glowing candles)
    for (const [ax, az, cx, cz] of [[x0, z0, x1, z0 + 0.15], [x0, z1 - 0.15, x1, z1], [x0, z0, x0 + 0.15, z1], [x1 - 0.15, z0, x1, z1]]) box(b, M.cream(), ax, D0 + R.h - 0.25, az, cx, D0 + R.h, cz);
    for (const cx of [R.x - 2.5, R.x + 2.5]) {
      const cy = D0 + R.h - 1.0, cz = R.z - 0.5;
      pole(b, M.brass(), V(cx, cy, cz), V(cx, D0 + R.h, cz), 0.02);
      const ring = new THREE.TorusGeometry(0.42, 0.03, 8, 24); ring.rotateX(Math.PI / 2); ring.translate(cx, cy, cz); b.add(ring, M.brass());
      for (let k = 0; k < 8; k++) { const a = (k / 8) * Math.PI * 2, px = cx + Math.cos(a) * 0.42, pz = cz + Math.sin(a) * 0.42; cyl(b, M.white(), px, cy, pz, 0.018, 0.018, 0.12, 6); const fl = new THREE.SphereGeometry(0.03, 8, 6); fl.scale(1, 1.6, 1); fl.translate(px, cy + 0.16, pz); b.add(fl, glow("candle", 2.4, 1.7, 0.7)); }
    }
    // tables: white cloth to the floor, plates, cups, a vase with flowers
    TABLES.forEach(([tx, tz], i) => {
      cyl(b, M.cloth(), tx, D0, tz, 0.62, 0.56, TAB_Y - D0, 24);
      for (let k = 0; k < 3; k++) { const a = (k / 3) * Math.PI * 2 + i; cyl(b, M.china(), tx + Math.cos(a) * 0.32, TAB_Y, tz + Math.sin(a) * 0.32, 0.13, 0.13, 0.012, 18); }
      teacup(b, tx + 0.18, TAB_Y, tz - 0.3); teacup(b, tx - 0.25, TAB_Y, tz + 0.12);
      const vx = tx + (i === 0 ? 0.36 : 0), vz = tz + (i === 0 ? 0.1 : 0);
      cyl(b, M.blueC(), vx, TAB_Y, vz, 0.05, 0.035, 0.18, 10);
      for (let k = 0; k < 5; k++) { const f = new THREE.SphereGeometry(0.045, 8, 6); f.translate(tx + Math.cos(k * 1.3) * 0.06, TAB_Y + 0.24 + (k % 2) * 0.04, tz + Math.sin(k * 1.3) * 0.06); f.translate(vx - tx, 0, vz - tz); b.add(f, k % 2 ? M.red() : lam("cFlowerY", () => ({ color: "#f2c230" }))); }
      // chairs: plush seat + back, behind each table toward the room
      for (const a of i === 0 ? [Math.PI * 0.5] : i === 1 ? [] : [Math.PI * 0.5 + i, Math.PI * 1.5 + i]) { // table 1: guests' chairs are on their cards
        const cx = tx + Math.cos(a) * 0.85, cz = tz + Math.sin(a) * 0.85;
        box(b, M.woodD(), cx - 0.22, D0 + 0.44, cz - 0.22, cx + 0.22, D0 + 0.5, cz + 0.22);
        box(b, M.plush(), cx - 0.2, D0 + 0.5, cz - 0.2, cx + 0.2, D0 + 0.56, cz + 0.2);
        for (const [dx, dz] of [[-0.18, -0.18], [0.18, -0.18], [-0.18, 0.18], [0.18, 0.18]]) box(b, M.woodD(), cx + dx - 0.025, D0, cz + dz - 0.025, cx + dx + 0.025, D0 + 0.44, cz + dz + 0.025);
        // a real chair back: two uprights, a top rail and a plush panel between them (not a stool on a stick)
        // rule 48: the window guest's chair back stays low and behind him (its top rail crossed his face at 0:43)
        const bo = i === 0 ? 0.3 : 0.2, bt = i === 0 ? 0.88 : 1.05;
        const bx = cx + Math.cos(a) * bo, bz = cz + Math.sin(a) * bo, px = -Math.sin(a) * 0.18, pz = Math.cos(a) * 0.18;
        for (const sg of [-1, 1]) bar(b, M.woodD(), V(bx + sg * px, D0 + 0.5, bz + sg * pz), V(bx + sg * px, D0 + bt, bz + sg * pz), 0.025);
        bar(b, M.woodD(), V(bx - px * 1.15, D0 + bt, bz - pz * 1.15), V(bx + px * 1.15, D0 + bt, bz + pz * 1.15), 0.035);
        { const g = new THREE.BoxGeometry(0.34, bt - 0.69, 0.04); g.rotateY(-a + Math.PI / 2); g.translate(bx, D0 + 0.5 + (bt - 0.5) / 2, bz); b.add(g, M.plush()); }
      }
    });
    // sideboard with a silver tea service, a big gilt mirror, palms in pots, a grandfather clock
    box(b, M.woodD(), x0 + 0.15, D0, R.z - 1.6, x0 + 0.7, D0 + 0.95, R.z + 1.6);
    for (let k = 0; k < 4; k++) cyl(b, lam("cSilver", () => ({ color: "#c9ccd2" })), x0 + 0.42, D0 + 0.95, R.z - 1.0 + k * 0.6, 0.09, 0.07, 0.22 - k * 0.03, 12);
    box(b, M.brass(), x0 + 0.02, D0 + 1.25, R.z - 1.2, x0 + 0.08, D0 + 2.9, R.z + 1.2);
    box(b, lam("cMirror", () => ({ color: "#bcd0e2" })), x0 + 0.08, D0 + 1.35, R.z - 1.1, x0 + 0.1, D0 + 2.8, R.z + 1.1);
    for (const [px, pz] of [[x1 - 0.6, z1 - 0.6], [x0 + 0.6, z1 - 0.6], [x1 - 0.6, z0 + 0.8]]) {
      cyl(b, M.brass(), px, D0, pz, 0.22, 0.28, 0.45, 14);
      for (let k = 0; k < 7; k++) { const a = (k / 7) * Math.PI * 2; const l = new THREE.ConeGeometry(0.12, 0.9, 5); l.rotateZ(0.9); l.rotateY(a); l.translate(px + Math.cos(a) * 0.25, D0 + 0.95, pz - Math.sin(a) * 0.25); b.add(l, lam("cPalm", () => ({ color: "#4f8a4a" }))); }
    }
    box(b, M.woodD(), x1 - 0.55, D0, R.z - 0.3, x1 - 0.1, D0 + 2.2, R.z + 0.3);
    b.build(root);
  }

  // ======== PARLOUR (S9 the couch) ========
  {
    const R = PARLOR, b = new Batch();
    const x0 = R.x - R.w / 2, x1 = R.x + R.w / 2, z0 = R.z - R.d / 2, z1 = R.z + R.d / 2;
    const paper = lam("cParlourWall", () => ({ map: ctex("cParlourPaper", 256, 512, (g) => {
      g.fillStyle = "#cfe0c4"; g.fillRect(0, 0, 256, 512);
      for (let x = 0; x < 256; x += 32) { g.fillStyle = "#b8cfa8"; g.fillRect(x, 0, 14, 330); }
      g.fillStyle = "#5a3a2a"; g.fillRect(0, 330, 256, 182); g.fillStyle = "#3e2618"; g.fillRect(0, 326, 256, 10);
      g.strokeStyle = "#33200f"; g.lineWidth = 4; for (let x = 8; x < 256; x += 128) g.strokeRect(x, 352, 112, 140);
    }) }));
    const floor = matTex("cParlourFloor", plankT(), 1, 1);
    room(b, x0, x1, D0, z0, z1, R.h, paper, floor, [{ at: R.x - 3.9, w: 1.4, y0: 0.8, y1: 2.8 }],
      lam("cStreetViewM", () => ({ map: streetViewT() })), lam("cCeilM", () => ({ color: "#f2e8d0" })));
    // a patterned rug under the couch, a framed picture over it, a lamp on a side table, a fern, a mantel clock
    box(b, matTex("cRugM", carpetT(), 2, 1), R.x - 2.4, D0 + 0.035, z1 - 3.4, R.x + 2.4, D0 + 0.05, z1 - 0.3);
    box(b, M.brass(), R.x - 0.9, D0 + 1.85, z1 - 0.06, R.x + 0.9, D0 + 2.85, z1 - 0.02);
    box(b, lam("cPictureM", () => ({ map: streetViewT() })), R.x - 0.8, D0 + 1.93, z1 - 0.075, R.x + 0.8, D0 + 2.77, z1 - 0.06);
    const tx = R.x + 2.2, tz = z1 - 0.8;
    cyl(b, M.woodD(), tx, D0, tz, 0.05, 0.05, 0.62, 10); cyl(b, M.woodD(), tx, D0 + 0.62, tz, 0.3, 0.3, 0.04, 18);
    cyl(b, M.brass(), tx, D0 + 0.66, tz, 0.08, 0.03, 0.4, 10);
    { const sh = new THREE.CylinderGeometry(0.12, 0.24, 0.26, 16, 1, true); sh.translate(tx, D0 + 1.16, tz); b.add(sh, lam("cShade", () => ({ color: "#f2d48a", side: THREE.DoubleSide }))); }
    cyl(b, M.brass(), R.x + 3.6, D0, z1 - 0.6, 0.22, 0.28, 0.45, 14);
    for (let k = 0; k < 7; k++) { const a = (k / 7) * Math.PI * 2; const l = new THREE.ConeGeometry(0.12, 0.9, 5); l.rotateZ(0.9); l.rotateY(a); l.translate(R.x + 3.6 + Math.cos(a) * 0.25, D0 + 0.95, z1 - 0.6 - Math.sin(a) * 0.25); b.add(l, lam("cPalm", () => ({ color: "#4f8a4a" }))); }
    box(b, M.woodD(), x0 + 0.2, D0, z1 - 2.6, x0 + 0.75, D0 + 1.1, z1 - 1.0); // a dresser on the left wall
    for (let k = 0; k < 3; k++) box(b, M.brass(), x0 + 0.74, D0 + 0.25 + k * 0.3, z1 - 1.9, x0 + 0.77, D0 + 0.29 + k * 0.3, z1 - 1.7);
    b.build(root);
  }

  // ======== DEPOT ========
  {
    const b = new Batch(), r = rng(1864);
    const gx0 = STA.x - 70, gx1 = STA.x + 70, gz0 = STA.z - 70, gz1 = STA.z + 40;
    floorQ(b, M.gravel(), gx0, gx1, gz0, gz1, D0 + 0.03, 6);
    // track: ties + two rails along x
    for (let x = gx0; x < gx1; x += 0.9) box(b, M.woodD(), x - 0.13, D0, STA.z - 1.3, x + 0.13, D0 + 0.14, STA.z + 1.3);
    for (const dz of [-0.72, 0.72]) box(b, M.steel(), gx0, D0 + 0.14, STA.z + dz - 0.04, gx1, D0 + 0.26, STA.z + dz + 0.04);
    // a second track behind (empty) for depth
    for (let x = gx0; x < gx1; x += 0.9) box(b, M.woodD(), x - 0.13, D0, STA.z - 6.3, x + 0.13, D0 + 0.14, STA.z - 3.7);
    for (const dz of [-5.72, -4.28]) box(b, M.steel(), gx0, D0 + 0.14, STA.z + dz - 0.04, gx1, D0 + 0.26, STA.z + dz + 0.04);
    // platform: stone edge + planks
    box(b, lam("cPlatEdge", () => ({ color: "#bcae94" })), STA.x - 30, D0, PLAT.z0, STA.x + 30, PLAT.y, PLAT.z0 + 0.4);
    box(b, matTex("cPlatPl", plankT(), 6, 1), STA.x - 30, D0, PLAT.z0 + 0.4, STA.x + 30, PLAT.y, PLAT.z1);
    // depot building behind the platform: brick, arched doors, a sign, a canopy on iron posts
    const bz = PLAT.z1, bh = 6.5;
    box(b, matTex("cDepotW", depotWallT(), 8, 2), STA.x - 22, D0, bz, STA.x + 22, D0 + bh, bz + 9);
    box(b, M.cream(), STA.x - 22.3, D0 + bh, bz - 0.3, STA.x + 22.3, D0 + bh + 0.4, bz + 9.3);
    const rf = new THREE.BufferGeometry();
    { const y = D0 + bh + 0.4, xa = STA.x - 22.3, xb = STA.x + 22.3, za = bz - 0.3, zb = bz + 9.3, ym = y + 2.6, zm = (za + zb) / 2;
      rf.setAttribute("position", new THREE.Float32BufferAttribute([xa, y, za, xb, y, za, xb, ym, zm, xa, y, za, xb, ym, zm, xa, ym, zm, xb, y, zb, xa, y, zb, xa, ym, zm, xb, y, zb, xa, ym, zm, xb, ym, zm], 3)); rf.computeVertexNormals(); }
    b.add(rf, lam("cDepotRoof", () => ({ color: "#5d5560", side: THREE.DoubleSide })));
    quad(b, lam("cDepotSignM", () => ({ map: depotSignT() })), V(STA.x + 5, D0 + bh - 1.6, bz - 0.04), V(STA.x - 5, D0 + bh - 1.6, bz - 0.04), V(STA.x - 5, D0 + bh - 0.05, bz - 0.04), V(STA.x + 5, D0 + bh - 0.05, bz - 0.04));
    for (let k = -3; k <= 3; k++) {
      const dx = STA.x + k * 5.6;
      box(b, M.woodD(), dx - 0.8, PLAT.y, bz - 0.06, dx + 0.8, PLAT.y + 2.6, bz - 0.01);
      box(b, lam("cDoorGlass", () => ({ color: "#f2d48a" })), dx - 0.6, PLAT.y + 1.5, bz - 0.08, dx + 0.6, PLAT.y + 2.4, bz - 0.06);
      if (k !== 0) { box(b, M.cream(), dx - 1.6 - 0.65, PLAT.y + 1.1, bz - 0.06, dx - 1.6 + 0.65, PLAT.y + 2.6, bz - 0.01); }
    }
    // canopy
    for (let k = -4; k <= 4; k++) { const px = STA.x + k * 5; pole(b, M.iron(), V(px, PLAT.y, PLAT.z0 + 1.4), V(px, PLAT.y + 3.6, PLAT.z0 + 1.4), 0.07); bar(b, M.iron(), V(px, PLAT.y + 3.6, PLAT.z0 + 1.4), V(px, PLAT.y + 3.0, bz), 0.04); }
    box(b, lam("cCanopy", () => ({ color: "#6a4a3a", side: THREE.DoubleSide })), STA.x - 21, PLAT.y + 3.6, PLAT.z0 + 1.0, STA.x + 21, PLAT.y + 3.72, bz);
    // benches, trunks on a luggage cart, lamp posts, a water tower down the line
    for (const bx of [STA.x - 12, STA.x + 9]) { box(b, M.wood(), bx - 1, PLAT.y + 0.42, bz - 0.9, bx + 1, PLAT.y + 0.48, bz - 0.4); box(b, M.wood(), bx - 1, PLAT.y + 0.48, bz - 0.42, bx + 1, PLAT.y + 0.95, bz - 0.36); for (const dx of [-0.9, 0.9]) box(b, M.iron(), bx + dx - 0.04, PLAT.y, bz - 0.9, bx + dx + 0.04, PLAT.y + 0.42, bz - 0.4); }
    { const lx = STA.x + 4.6, lz = PLAT.z0 + 2.6; box(b, M.wood(), lx - 1.0, PLAT.y + 0.35, lz - 0.5, lx + 1.0, PLAT.y + 0.45, lz + 0.5);
      for (const dx of [-0.75, 0.75]) { const w = new THREE.CylinderGeometry(0.17, 0.17, 0.06, 12); w.rotateX(Math.PI / 2); w.translate(lx + dx, PLAT.y + 0.17, lz - 0.52); b.add(w, M.iron()); const w2 = w.clone(); w2.translate(0, 0, 1.04); b.add(w2, M.iron()); }
      box(b, lam("cTrunkA", () => ({ color: "#7a4a2a" })), lx - 0.9, PLAT.y + 0.45, lz - 0.4, lx - 0.05, PLAT.y + 0.95, lz + 0.4);
      box(b, lam("cTrunkB", () => ({ color: "#3f5a7a" })), lx + 0.05, PLAT.y + 0.45, lz - 0.35, lx + 0.8, PLAT.y + 0.85, lz + 0.35);
      box(b, lam("cTrunkC", () => ({ color: "#a8743f" })), lx - 0.6, PLAT.y + 0.95, lz - 0.3, lx + 0.1, PLAT.y + 1.3, lz + 0.3); }
    for (const lx of [STA.x - 16, STA.x - 6, STA.x + 14]) { pole(b, M.iron(), V(lx, PLAT.y, PLAT.z0 + 0.8), V(lx, PLAT.y + 3.1, PLAT.z0 + 0.8), 0.05); box(b, M.iron(), lx - 0.18, PLAT.y + 3.1, PLAT.z0 + 0.62, lx + 0.18, PLAT.y + 3.5, PLAT.z0 + 0.98); }
    { const wx = STA.x - 34, wz = STA.z - 12; for (const [dx, dz] of [[-1.6, -1.6], [1.6, -1.6], [-1.6, 1.6], [1.6, 1.6]]) pole(b, M.woodD(), V(wx + dx, D0, wz + dz), V(wx + dx * 0.8, D0 + 6, wz + dz * 0.8), 0.14);
      cyl(b, M.wood(), wx, D0 + 6, wz, 2.2, 2.2, 3.2, 18); const cone = new THREE.ConeGeometry(2.5, 1.4, 18); cone.translate(wx, D0 + 9.9, wz); b.add(cone, lam("cTankRoof", () => ({ color: "#5d5560" }))); }
    // town behind the far track: houses + trees so the frame is never empty
    for (let x = gx0 + 6; x < gx1 - 6; x += 10 + r() * 3) {
      house(b, x, STA.z - 16 - r() * 3, 0, 8, 8, [5.6, 7, 8.4][Math.floor(r() * 3)], Math.floor(r() * 8));
      if (r() < 0.5) prop(b, kit, ["tree_oak", "tree_default", "tree_fat"][Math.floor(r() * 3)], x + 5, D0, STA.z - 9.5, 6 + r() * 3, r() * 6);
    }
    for (let x = gx0 + 3; x < gx1; x += 14) house(b, x, STA.z - 34, 0, 9, 8, 9.8, Math.abs(x | 0) % 8);
    b.build(root);
  }
  // the Pullman sleeping car on the near track
  {
    const b = new Batch(), C = CAR, z = C.z, w = 1.55;
    const side = lam("cCarSideM", () => ({ map: carSideT() }));
    box(b, M.green(), C.x0, C.y, z - w, C.x1, C.y + C.h, z + w);
    quad(b, side, V(C.x0, C.y, z + w + 0.012), V(C.x1, C.y, z + w + 0.012), V(C.x1, C.y + C.h, z + w + 0.012), V(C.x0, C.y + C.h, z + w + 0.012));
    quad(b, side, V(C.x1, C.y, z - w - 0.012), V(C.x0, C.y, z - w - 0.012), V(C.x0, C.y + C.h, z - w - 0.012), V(C.x1, C.y + C.h, z - w - 0.012));
    // roof: lower deck + clerestory with small lit windows, overhanging ends
    box(b, lam("cCarRoof", () => ({ color: "#2f2d33" })), C.x0 - 0.5, C.y + C.h, z - w - 0.12, C.x1 + 0.5, C.y + C.h + 0.16, z + w + 0.12);
    box(b, M.green(), C.x0 + 0.6, C.y + C.h + 0.16, z - 0.8, C.x1 - 0.6, C.y + C.h + 0.62, z + 0.8);
    for (let x = C.x0 + 1.2; x < C.x1 - 1; x += 1.1) for (const s of [-1, 1]) box(b, glow("clere", 1.5, 1.3, 0.8), x - 0.3, C.y + C.h + 0.28, z + s * 0.81 - 0.01, x + 0.3, C.y + C.h + 0.5, z + s * 0.81 + 0.01);
    box(b, lam("cCarRoof", () => ({ color: "#2f2d33" })), C.x0 + 0.4, C.y + C.h + 0.62, z - 1.0, C.x1 - 0.4, C.y + C.h + 0.72, z + 1.0);
    // end platforms with brass railings and steps
    for (const [xa, s] of [[C.x0, -1], [C.x1, 1]] as const) {
      box(b, M.iron(), xa, C.y - 0.1, z - w, xa + s * 1.1, C.y + 0.05, z + w);
      for (const dz of [-w + 0.05, w - 0.05]) { bar(b, M.brass(), V(xa + s * 1.05, C.y + 0.05, z + dz), V(xa + s * 1.05, C.y + 1.05, z + dz), 0.025); }
      bar(b, M.brass(), V(xa + s * 1.05, C.y + 1.05, z - w + 0.05), V(xa + s * 1.05, C.y + 1.05, z + w - 0.05), 0.025);
      for (let k = 0; k < 2; k++) box(b, M.iron(), xa + s * 0.15, C.y - 0.35 - k * 0.3, z + w - 0.05, xa + s * 0.95, C.y - 0.3 - k * 0.3, z + w + 0.35);
    }
    // underframe, trucks with wheels on the rails
    box(b, M.iron(), C.x0 + 0.5, C.y - 0.3, z - w + 0.2, C.x1 - 0.5, C.y, z + w - 0.2);
    for (const tx of [C.x0 + 3, C.x1 - 3]) {
      box(b, M.iron(), tx - 1.3, D0 + 0.45, z - 1.0, tx + 1.3, D0 + 0.75, z + 1.0);
      for (const dx of [-0.8, 0.8]) for (const dz of [-0.72, 0.72]) { const wh = new THREE.CylinderGeometry(0.46, 0.46, 0.1, 18); wh.rotateX(Math.PI / 2); wh.translate(tx + dx, D0 + 0.26 + 0.46 - 0.02, z + dz); b.add(wh, M.iron());
        const hub = new THREE.CylinderGeometry(0.12, 0.12, 0.12, 10); hub.rotateX(Math.PI / 2); hub.translate(tx + dx, D0 + 0.7, z + dz + Math.sign(dz) * 0.02); b.add(hub, M.brass()); }
    }
    b.build(root);
  }

  // ======== BOATS ========
  S.boats = BOATS.map((bt) => grp(root, (b) => {
    if (bt.kind === "tug") {
      const hull = new THREE.BoxGeometry(9, 1.6, 3.4); hull.translate(0, 0.3, 0); b.add(hull, lam("cTugHull", () => ({ color: "#8c2f2a" })));
      const bow = new THREE.ConeGeometry(1.7, 2.6, 4, 1); bow.rotateZ(-Math.PI / 2); bow.rotateX(Math.PI / 4); bow.scale(1, 0.62, 1); bow.translate(5.8, 0.3, 0); b.add(bow, lam("cTugHull", () => ({ color: "#8c2f2a" })));
      box(b, lam("cTugDeck", () => ({ color: "#c9b48a" })), -4.5, 1.1, -1.7, 4.5, 1.2, 1.7);
      box(b, M.white(), -2.6, 1.2, -1.1, 1.4, 3.0, 1.1);
      for (let k = 0; k < 3; k++) box(b, lam("cTugWin", () => ({ color: "#2f4a6a" })), -2.2 + k * 1.2, 2.1, 1.11, -1.6 + k * 1.2, 2.7, 1.12);
      box(b, M.iron(), -2.8, 3.0, -1.3, 1.6, 3.15, 1.3);
      cyl(b, M.iron(), -0.4, 3.15, 0, 0.42, 0.42, 2.1, 14); cyl(b, M.red(), -0.4, 4.6, 0, 0.44, 0.44, 0.3, 14);
      const tyre = new THREE.TorusGeometry(0.35, 0.12, 8, 14); tyre.translate(1.5, 0.6, 1.75); b.add(tyre, M.iron());
    } else {
      box(b, lam("cBarge", () => ({ color: "#6a4a30" })), -9, -0.5, -2.6, 9, 1.0, 2.6);
      for (let k = 0; k < 4; k++) { const s = new THREE.SphereGeometry(1.6, 12, 6, 0, Math.PI * 2, 0, Math.PI / 2); s.scale(1.4, 0.6, 1); s.translate(-6 + k * 4, 1.0, 0); b.add(s, lam("cCoal", () => ({ color: "#3a3638" }))); }
      box(b, M.white(), 7, 1.0, -1.0, 8.6, 2.6, 1.0);
    }
  }));

  // ======== LANTERNS under the Tremont floor (hang from the hotel, rise with it) ========
  S.lanterns = grp(tre, (b) => {
    for (const z of [113.4, 118.2, 123]) for (const x of [-10, -4, 2, 8]) {
      bar(b, M.iron(), V(x, -0.02, z), V(x, -0.32, z), 0.01);
      box(b, M.iron(), x - 0.1, -0.36, z - 0.1, x + 0.1, -0.32, z + 0.1);
      box(b, glow("lantern", 2.8, 1.9, 0.8), x - 0.08, -0.56, z - 0.08, x + 0.08, -0.36, z + 0.08);
      box(b, M.iron(), x - 0.1, -0.6, z - 0.1, x + 0.1, -0.56, z + 0.1);
    }
  }, false);
  S.lanterns.position.y = 0; // tre group is at D0 + lift: local y 0 = the floor underside
  // warm light pools on the mud under each lantern
  S.depotGlow = grp(root, (b) => {
    const pm = new THREE.MeshBasicMaterial({ color: new THREE.Color(0.55, 0.36, 0.12), transparent: true, opacity: 0.55, blending: THREE.AdditiveBlending, depthWrite: false });
    for (const z of [113.4, 118.2, 123]) for (const x of [-10, -4, 2, 8]) { const c = new THREE.CircleGeometry(1.7, 24); c.rotateX(-Math.PI / 2); c.translate(x, D0 + 0.07, z); b.add(c, pm); }
  }, false);
  void TRE;
  setSight([]);
  return S;
};
