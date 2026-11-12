// r2 sets for the Chicago short (owner rules 16-19: new places, interiors, readable props, nothing empty):
//  DINING ROOM  the Tremont House dining room (S1c tea while the hotel rises, S8a the guests barely noticed)
//  DEPOT        a railway platform with a Pullman sleeping car (S10b "America's famous sleeping cars")
//  BOATS        tugs and a barge on the river that drift with the current and turn back with it (S11)
//  LANTERNS     lanterns hung under the Tremont floor so the 500 men underneath are seen (S7b)
import * as THREE from "three";
import { Batch, boxGeo, V, lam, house, prop, Kit, setSight, Ray } from "./build";
import { ctex, rng, grassHD } from "./paint";
import { wallpaperInk, hillsInk, mudInk } from "./hand";
import { NOINK } from "./ink";
import { D0, DINE, TAB_Y, TABLES, STA, CAR, PLAT, BOATS, TRE, PARLOR, SWAMP, COUNCIL, DOC } from "./story";

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
/** v8 drawn Victorian carpet (teardown: sets carry drawn textures): seamless 2.4 m tile, inked lattice, medallions,
 *  leaf scrolls and a fine weave hatch, so the floor reads as a real carpet and not a flat colour */
const carpetT = () => ctex("cCarpet8", 1024, 1024, (g, r) => {
  const INKC = "#2a1418";
  g.fillStyle = "#8c2f3f"; g.fillRect(0, 0, 1024, 1024);
  g.strokeStyle = "rgba(60,16,26,0.35)"; g.lineWidth = 2; for (let y = 3; y < 1024; y += 7) { g.beginPath(); g.moveTo(0, y); g.lineTo(1024, y + 2); g.stroke(); }
  // diamond lattice in gold with ink edges
  for (const [col, lw] of [[INKC, 14], ["#c9a04a", 8]] as const) { g.strokeStyle = col; g.lineWidth = lw;
    for (let k = -1024; k <= 2048; k += 256) { g.beginPath(); g.moveTo(k, 0); g.lineTo(k + 1024, 1024); g.stroke(); g.beginPath(); g.moveTo(k, 1024); g.lineTo(k + 1024, 0); g.stroke(); } }
  // medallions at the lattice cells: navy rosette, cream petals, ink outlines
  const ros = (x: number, y: number) => {
    for (let i = 0; i < 8; i++) { const a = (i * Math.PI) / 4; g.fillStyle = "#e8d6a8"; g.strokeStyle = INKC; g.lineWidth = 4;
      g.beginPath(); g.ellipse(x + Math.cos(a) * 34, y + Math.sin(a) * 34, 22, 11, a, 0, 6.29); g.fill(); g.stroke(); }
    g.fillStyle = "#2f3a5a"; g.beginPath(); g.arc(x, y, 26, 0, 6.29); g.fill(); g.stroke();
    g.fillStyle = "#c9a04a"; g.beginPath(); g.arc(x, y, 9, 0, 6.29); g.fill(); g.stroke();
  };
  for (let y = 0; y <= 1024; y += 256) for (let x = 0; x <= 1024; x += 256) ros(x, y);
  // small leaf sprigs in the other cells
  const leaf = (x: number, y: number) => { g.strokeStyle = INKC; g.lineWidth = 3;
    for (const sx of [-1, 1]) for (const sy of [-1, 1]) { g.fillStyle = "#4f6a3a"; g.beginPath(); g.ellipse(x + sx * 16, y + sy * 16, 14, 6, sx * sy * 0.8, 0, 6.29); g.fill(); g.stroke(); }
    g.fillStyle = "#e8b04a"; g.beginPath(); g.arc(x, y, 7, 0, 6.29); g.fill(); g.stroke(); };
  for (let y = 128; y < 1024; y += 256) for (let x = 128; x < 1024; x += 256) leaf(x, y);
  // wear: a few lighter scuffs
  for (let i = 0; i < 40; i++) { g.fillStyle = "rgba(255,230,200,0.06)"; g.beginPath(); g.ellipse(r() * 1024, r() * 1024, 30 + r() * 60, 8 + r() * 16, r() * 3, 0, 6.29); g.fill(); }
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
/** v8 drawn floorboards: 8 boards per 2.4 m, inked seams, staggered butt joints with nail pairs, grain and knots */
const plankT = () => ctex("cPlatPlanks8", 1024, 1024, (g, r) => {
  const tones = ["#a8743f", "#9a6a38", "#b07e48", "#a06e3c"];
  for (let i = 0; i < 8; i++) {
    const y = i * 128; g.fillStyle = tones[i % 4]; g.fillRect(0, y, 1024, 128);
    g.strokeStyle = "rgba(70,42,20,0.45)"; g.lineWidth = 2;
    for (let k = 0; k < 7; k++) { const yy = y + 12 + r() * 104; g.beginPath(); g.moveTo(0, yy); for (let x = 0; x <= 1024; x += 64) g.lineTo(x, yy + Math.sin(x / 90 + k) * 4); g.stroke(); }
    for (let k = 0; k < 2; k++) { const kx = r() * 1024, ky = y + 30 + r() * 68; g.fillStyle = "#6a4426"; g.beginPath(); g.ellipse(kx, ky, 14, 7, 0, 0, 6.29); g.fill();
      g.strokeStyle = "rgba(70,42,20,0.55)"; g.beginPath(); g.ellipse(kx, ky, 26, 13, 0, 0, 6.29); g.stroke(); }
    g.fillStyle = "#2e1c10"; g.fillRect(0, y + 124, 1024, 5);
    const jx = ((i * 389) % 1024); g.fillRect(jx, y, 5, 128);
    g.fillStyle = "#3a2414"; for (const nx of [jx - 14, jx + 18]) for (const ny of [y + 30, y + 96]) { g.beginPath(); g.arc(nx, ny, 3.5, 0, 6.29); g.fill(); }
  }
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

export type SetRefs = { boats: THREE.Group[]; lanterns: THREE.Group; depotGlow: THREE.Group; under: THREE.Group };

export const buildSets = (root: THREE.Object3D, kit: Kit, rays: Ray[], tre: THREE.Group): SetRefs => {
  setSight(rays);
  const S = {} as SetRefs;

  // ======== DINING ROOM ========
  {
    const R = DINE, b = new Batch();
    const x0 = R.x - R.w / 2, x1 = R.x + R.w / 2, z0 = R.z - R.d / 2, z1 = R.z + R.d / 2;
    room(b, x0, x1, D0, z0, z1, R.h, lam("cWallInkDine", () => ({ map: wallpaperInk("dine", "#c9b48a", "#8a4a5a", "#5a3a2e") })), matTex("cCarpetM", carpetT(), 1, 1),
      [{ at: R.x - 4.6, w: 1.6, y0: 0.7, y1: 3.1 }, { at: R.x - 0.8, w: 1.6, y0: 0.7, y1: 3.1 }, { at: R.x + 3.0, w: 1.6, y0: 0.7, y1: 3.1 }],
      lam("cStreetViewM", () => ({ map: streetViewT() })), lam("cCeilM", () => ({ map: ctex("cCeilT", 384, 384, (g) => {
      // v19: moulded plaster ceiling (was a flat colour): square panels with beaded frames and a rosette in each
      g.fillStyle = "#f2e8d0"; g.fillRect(0, 0, 384, 384);
      for (let i = 0; i < 2; i++) for (let j = 0; j < 2; j++) { const x = i * 192, y = j * 192;
        g.strokeStyle = "#a89878"; g.lineWidth = 5; g.strokeRect(x + 14, y + 14, 164, 164); g.strokeStyle = "#cbbd9c"; g.lineWidth = 3; g.strokeRect(x + 26, y + 26, 140, 140);
        g.fillStyle = "#8a7a5c"; for (let k = 0; k < 12; k++) for (const [px, py] of [[x + 20 + k * 13.5, y + 20], [x + 20 + k * 13.5, y + 172], [x + 20, y + 20 + k * 13.5], [x + 172, y + 20 + k * 13.5]]) { g.beginPath(); g.arc(px, py, 2, 0, 6.28); g.fill(); }
        const cx = x + 96, cy = y + 96; g.strokeStyle = "#8a7a5c"; g.lineWidth = 3;
        for (let k = 0; k < 8; k++) { const a = (k / 8) * 6.283; g.beginPath(); g.ellipse(cx + Math.cos(a) * 20, cy + Math.sin(a) * 20, 14, 7, a, 0, 6.28); g.stroke(); }
        g.beginPath(); g.arc(cx, cy, 9, 0, 6.28); g.stroke(); g.beginPath(); g.arc(cx, cy, 40, 0, 6.28); g.stroke(); }
    }) })));
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
      cyl(b, lam("cClothDamask", () => ({ map: (() => { const tx2 = ctex("cDamaskT", 1024, 512, (g) => { // v17: woven damask lattice + an embroidered hem band (teardown: drawn textures, lace)
        g.fillStyle = "#f6f3ea"; g.fillRect(0, 0, 1024, 512);
        g.strokeStyle = "#c9cdd6"; g.lineWidth = 4; for (let x = -512; x < 1024; x += 64) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x + 420, 420); g.moveTo(x + 420, 0); g.lineTo(x, 420); g.stroke(); }
        g.fillStyle = "#b9c0cc"; for (let y = 32; y < 420; y += 64) for (let x = 32; x < 1024; x += 64) { g.beginPath(); g.ellipse(x, y, 9, 13, 0, 0, 6.29); g.fill(); }
        g.fillStyle = "#3f6fb5"; g.fillRect(0, 430, 1024, 14); g.fillRect(0, 466, 1024, 8);
        for (let x = 0; x < 1024; x += 32) { g.fillStyle = "#a8322c"; g.beginPath(); g.arc(x + 16, 455, 7, 0, 6.29); g.fill(); g.strokeStyle = "#241726"; g.lineWidth = 2; g.stroke(); }
        g.fillStyle = "#f6f3ea"; for (let x = 0; x < 1024; x += 24) { g.beginPath(); g.arc(x + 12, 500, 10, 0, 3.15); g.fill(); g.stroke(); }
      }); tx2.wrapS = THREE.RepeatWrapping; tx2.repeat.set(2, 1); tx2.flipY = true; return tx2; })() })), tx, D0, tz, 0.62, 0.56, TAB_Y - D0, 24);
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
    room(b, x0, x1, D0, z0, z1, R.h, lam("cWallInkParl", () => ({ map: wallpaperInk("parl", "#b8c4a4", "#4a6a5a", "#6a4a34") })), floor, [{ at: R.x - 3.9, w: 1.4, y0: 0.8, y1: 2.8 }],
      lam("cStreetViewM", () => ({ map: streetViewT() })), lam("cCeilM", () => ({ map: ctex("cCeilT", 384, 384, (g) => {
      // v19: moulded plaster ceiling (was a flat colour): square panels with beaded frames and a rosette in each
      g.fillStyle = "#f2e8d0"; g.fillRect(0, 0, 384, 384);
      for (let i = 0; i < 2; i++) for (let j = 0; j < 2; j++) { const x = i * 192, y = j * 192;
        g.strokeStyle = "#a89878"; g.lineWidth = 5; g.strokeRect(x + 14, y + 14, 164, 164); g.strokeStyle = "#cbbd9c"; g.lineWidth = 3; g.strokeRect(x + 26, y + 26, 140, 140);
        g.fillStyle = "#8a7a5c"; for (let k = 0; k < 12; k++) for (const [px, py] of [[x + 20 + k * 13.5, y + 20], [x + 20 + k * 13.5, y + 172], [x + 20, y + 20 + k * 13.5], [x + 172, y + 20 + k * 13.5]]) { g.beginPath(); g.arc(px, py, 2, 0, 6.28); g.fill(); }
        const cx = x + 96, cy = y + 96; g.strokeStyle = "#8a7a5c"; g.lineWidth = 3;
        for (let k = 0; k < 8; k++) { const a = (k / 8) * 6.283; g.beginPath(); g.ellipse(cx + Math.cos(a) * 20, cy + Math.sin(a) * 20, 14, 7, a, 0, 6.28); g.stroke(); }
        g.beginPath(); g.arc(cx, cy, 9, 0, 6.28); g.stroke(); g.beginPath(); g.arc(cx, cy, 40, 0, 6.28); g.stroke(); }
    }) })));
    // a patterned rug under the couch, a framed picture over it, a lamp on a side table, a fern, a mantel clock
    box(b, matTex("cRugM", carpetT(), 2, 1.5), R.x - 2.4, D0 + 0.035, z1 - 5.2, R.x + 2.4, D0 + 0.05, z1 - 0.3); // v19: the rug runs on toward the lens (the bare near boards were the flattest part of the couch wide)
    box(b, M.brass(), R.x - 0.9, D0 + 1.85, z1 - 0.06, R.x + 0.9, D0 + 2.85, z1 - 0.02);
    box(b, lam("cPictureM", () => ({ map: streetViewT() })), R.x - 0.8, D0 + 1.93, z1 - 0.075, R.x + 0.8, D0 + 2.77, z1 - 0.06);
    const tx = R.x + 2.2, tz = z1 - 0.8;
    cyl(b, M.woodD(), tx, D0, tz, 0.05, 0.05, 0.62, 10); cyl(b, M.woodD(), tx, D0 + 0.62, tz, 0.3, 0.3, 0.04, 18);
    cyl(b, M.brass(), tx, D0 + 0.66, tz, 0.08, 0.03, 0.4, 10);
    { const sh = new THREE.CylinderGeometry(0.12, 0.24, 0.26, 16, 1, true); sh.translate(tx, D0 + 1.16, tz); b.add(sh, lam("cShade", () => ({ color: "#f2d48a", side: THREE.DoubleSide }))); }
    cyl(b, M.brass(), R.x + 3.6, D0, z1 - 0.6, 0.22, 0.28, 0.45, 14);
    for (let k = 0; k < 7; k++) { const a = (k / 7) * Math.PI * 2; const l = new THREE.ConeGeometry(0.12, 0.9, 5); l.rotateZ(0.9); l.rotateY(a); l.translate(R.x + 3.6 + Math.cos(a) * 0.25, D0 + 0.95, z1 - 0.6 - Math.sin(a) * 0.25); b.add(l, lam("cPalm", () => ({ color: "#4f8a4a" }))); }
    box(b, M.woodD(), x0 + 0.2, D0, z1 - 2.6, x0 + 0.75, D0 + 1.1, z1 - 1.0); // a dresser on the left wall
    // v17 (owner Nov 12: parlour needs more drawn objects; teardown parlour has 25+ props): oval portraits flanking the picture,
    // a wall clock, a plate shelf, an embroidered sampler, a coal stove, a footstool, a tea tray on the side table
    const portraitT = (k: number) => lam("cOvalP" + k, () => ({ map: ctex("cOvalPT" + k, 160, 200, (g) => {
      g.fillStyle = "#c9a04a"; g.fillRect(0, 0, 160, 200); g.fillStyle = ["#3b4a3a", "#4a3a4a"][k]; g.beginPath(); g.ellipse(80, 100, 66, 86, 0, 0, 6.29); g.fill();
      g.strokeStyle = "#241726"; g.lineWidth = 5; g.stroke(); g.fillStyle = "#efe0cc"; g.beginPath(); g.ellipse(80, 82, 26, 32, 0, 0, 6.29); g.fill(); g.stroke();
      g.fillStyle = ["#2a2420", "#5a3a5a"][k]; g.beginPath(); g.moveTo(36, 186); g.quadraticCurveTo(80, 104, 124, 186); g.fill(); g.stroke();
      g.fillStyle = "#241726"; for (const ex of [70, 90]) { g.beginPath(); g.arc(ex, 80, 3.5, 0, 6.29); g.fill(); }
      if (k === 0) { g.fillStyle = "#4a3426"; g.fillRect(66, 92, 28, 6); } else { g.fillStyle = "#3a2a24"; g.beginPath(); g.ellipse(80, 54, 30, 14, 0, 0, 6.29); g.fill(); }
    }) }));
    [-1.55, 1.55].forEach((dx, k) => { box(b, M.brass(), R.x + dx - 0.3, D0 + 1.95, z1 - 0.045, R.x + dx + 0.3, D0 + 2.7, z1 - 0.02); box(b, portraitT(k), R.x + dx - 0.26, D0 + 2.0, z1 - 0.06, R.x + dx + 0.26, D0 + 2.65, z1 - 0.045); });
    box(b, M.woodD(), R.x + 2.34, D0 + 1.99, z1 - 0.06, R.x + 2.86, D0 + 2.51, z1 - 0.02); // wall clock: case, dial, pendulum box
    box(b, lam("cClockFace", () => ({ map: ctex("cClockFaceT", 128, 128, (g) => { g.fillStyle = "#5a3a24"; g.fillRect(0, 0, 128, 128); g.fillStyle = "#f4ecd8"; g.beginPath(); g.arc(64, 64, 56, 0, 6.29); g.fill(); g.strokeStyle = "#241726"; g.lineWidth = 5; g.stroke(); for (let i = 0; i < 12; i++) { const a = (i / 12) * 6.283; g.lineWidth = 3; g.beginPath(); g.moveTo(64 + Math.cos(a) * 42, 64 + Math.sin(a) * 42); g.lineTo(64 + Math.cos(a) * 50, 64 + Math.sin(a) * 50); g.stroke(); } g.lineWidth = 5; g.beginPath(); g.moveTo(64, 64); g.lineTo(64, 26); g.moveTo(64, 64); g.lineTo(90, 70); g.stroke(); }) })), R.x + 2.36, D0 + 2.01, z1 - 0.07, R.x + 2.84, D0 + 2.49, z1 - 0.06);
    box(b, M.woodD(), R.x + 2.48, D0 + 1.3, z1 - 0.06, R.x + 2.72, D0 + 1.99, z1 - 0.02); box(b, M.brass(), R.x + 2.56, D0 + 1.36, z1 - 0.07, R.x + 2.64, D0 + 1.44, z1 - 0.06);
    box(b, M.woodD(), R.x - 3.2, D0 + 2.0, z1 - 0.22, R.x - 2.0, D0 + 2.05, z1 - 0.02); // plate shelf with plates on edge
    for (let k = 0; k < 4; k++) { const px = R.x - 3.05 + k * 0.3; box(b, lam("cPlate", () => ({ map: ctex("cPlateT", 96, 96, (g) => { g.fillStyle = "#cfe0c4"; g.fillRect(0, 0, 96, 96); g.fillStyle = "#f8f6f0"; g.beginPath(); g.arc(48, 48, 44, 0, 6.29); g.fill(); g.strokeStyle = "#3f6fb5"; g.lineWidth = 6; g.beginPath(); g.arc(48, 48, 34, 0, 6.29); g.stroke(); g.lineWidth = 3; g.beginPath(); g.arc(48, 48, 16, 0, 6.29); g.stroke(); g.strokeStyle = "#241726"; g.lineWidth = 4; g.beginPath(); g.arc(48, 48, 44, 0, 6.29); g.stroke(); }) })), px - 0.12, D0 + 2.05, z1 - 0.12, px + 0.12, D0 + 2.29, z1 - 0.1); }
    box(b, M.woodD(), R.x - 2.95, D0 + 1.25, z1 - 0.04, R.x - 2.25, D0 + 1.8, z1 - 0.02); // sampler: stitched letters and a little house
    box(b, lam("cSampler", () => ({ map: ctex("cSamplerT", 140, 110, (g) => { g.fillStyle = "#efe6cc"; g.fillRect(0, 0, 140, 110); g.fillStyle = "#a8322c"; g.font = "bold 22px Georgia, serif"; g.textAlign = "center"; g.fillText("HOME", 70, 32); g.strokeStyle = "#3f5a3a"; g.lineWidth = 3; g.strokeRect(50, 56, 40, 30); g.beginPath(); g.moveTo(44, 58); g.lineTo(70, 40); g.lineTo(96, 58); g.stroke(); for (let x = 8; x < 140; x += 10) { g.fillStyle = "#3f6fb5"; g.fillRect(x, 96, 5, 5); g.fillRect(x, 6, 5, 5); } }) })), R.x - 2.9, D0 + 1.3, z1 - 0.05, R.x - 2.3, D0 + 1.75, z1 - 0.04);
    cyl(b, M.iron(), x1 - 0.8, D0, z1 - 1.6, 0.32, 0.36, 0.95, 14); pole(b, M.iron(), V(x1 - 0.8, D0 + 0.95, z1 - 1.6), V(x1 - 0.8, D0 + R.h, z1 - 1.6), 0.08);
    box(b, glow("stoveDoor", 2.4, 1.2, 0.4), x1 - 1.14, D0 + 0.3, z1 - 1.72, x1 - 1.1, D0 + 0.5, z1 - 1.48);
    box(b, M.plush(), R.x - 1.6, D0 + 0.2, z1 - 3.0, R.x - 1.1, D0 + 0.36, z1 - 2.6); for (const [dx, dz] of [[-1.55, -2.95], [-1.15, -2.95], [-1.55, -2.65], [-1.15, -2.65]]) cyl(b, M.woodD(), R.x + dx, D0, z1 + dz, 0.025, 0.02, 0.2, 6);
    cyl(b, M.brass(), tx, D0 + 0.66, tz - 0.16, 0.12, 0.12, 0.012, 16); cyl(b, M.china(), tx - 0.05, D0 + 0.672, tz - 0.18, 0.05, 0.065, 0.11, 12); cyl(b, M.china(), tx + 0.08, D0 + 0.672, tz - 0.12, 0.03, 0.035, 0.05, 10);
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


  // ======== SWAMP (v2 take 3): reeds, pools, plank shacks on stilts, the lake right behind and barely lower ========
  {
    const b = new Batch(), r = rng(1830), X = SWAMP.x, Z = SWAMP.z;
    const mud = lam("cMarsh", () => ({ map: ctex("cMarshT", 512, 512, (g, rr) => {
      g.fillStyle = "#6f6a3e"; g.fillRect(0, 0, 512, 512);
      for (let i = 0; i < 900; i++) { g.fillStyle = ["#5e5a34", "#7d7746", "#6a5a36", "#857f52", "#59603a"][i % 5]; const x = rr() * 512, y = rr() * 512; g.fillRect(x, y, 3 + rr() * 14, 2 + rr() * 3); }
      g.strokeStyle = "rgba(40,36,20,0.5)"; g.lineWidth = 2; for (let i = 0; i < 60; i++) { const x = rr() * 512, y = rr() * 512; g.beginPath(); g.moveTo(x, y); g.lineTo(x + 4 - rr() * 8, y - 10 - rr() * 14); g.stroke(); }
    }) }));
    floorQ(b, lam("cMarshInk", () => ({ map: mudInk("marsh", false, ["#6f6a44", "#5e5a34", "#7d7746", "#6a5a36", "#857f52", "#59603a"]) })), X - 60, X + 60, Z - 50, Z + 21, D0 + 0.02, 16);
    { const ht = hillsInk("swamp", ["#a9b4b0", "#8a9a86", "#6f7f62"]); ht.repeat.set(2, 1);
      const hm = new THREE.Mesh(new THREE.CylinderGeometry(62, 62, 40, 64, 1, true), new THREE.MeshBasicMaterial({ map: ht, transparent: true, side: THREE.BackSide, fog: false, depthWrite: false }));
      hm.position.set(X, D0 - 6 + 20, Z); hm.layers.set(NOINK); hm.renderOrder = -0.5; root.add(hm); }
    // bank edge: a dark muddy lip, then the lake (a hand's width lower than the marsh)
    box(b, lam("cBank", () => ({ color: "#4a3e2a" })), X - 60, D0 - 0.2, Z + 21, X + 60, D0 + 0.03, Z + 21.6);
    const lakeM = lam("cSwampLake", () => ({ map: ctex("cSwampLakeT", 512, 256, (g, rr) => {
      g.fillStyle = "#6f8fa8"; g.fillRect(0, 0, 512, 256);
      for (let i = 0; i < 160; i++) { g.fillStyle = i % 2 ? "rgba(220,232,240,0.55)" : "rgba(70,96,120,0.5)"; g.fillRect(rr() * 512, rr() * 256, 20 + rr() * 50, 2); }
    }) }));
    floorQ(b, lakeM, X - 400, X + 400, Z + 21.6, Z + 700, D0 - 0.12, 12);
    // pools of black-green water among the reeds (each its own height step: no coplanar flicker)
    const poolM = lam("cPool", () => ({ map: ctex("cPoolT", 512, 512, (g, rr) => {
      g.fillStyle = "#3a4a3a"; g.fillRect(0, 0, 512, 512);
      // drawn still water: ripple arcs, reed reflections, scum flecks, floating twigs
      g.lineCap = "round";
      for (let i = 0; i < 90; i++) { const x = rr() * 512, y = rr() * 512, w = 14 + rr() * 40; g.strokeStyle = i % 3 ? "rgba(150,175,150,0.55)" : "rgba(20,28,22,0.7)"; g.lineWidth = 2.5; g.beginPath(); g.ellipse(x, y, w, w * 0.3, 0, Math.PI * 1.1, Math.PI * 1.9); g.stroke(); }
      for (let i = 0; i < 70; i++) { const x = rr() * 512, y = rr() * 512; g.strokeStyle = "rgba(90,110,60,0.6)"; g.lineWidth = 3; g.beginPath(); g.moveTo(x, y); g.lineTo(x + 3 - rr() * 6, y + 20 + rr() * 30); g.stroke(); }
      for (let i = 0; i < 260; i++) { g.fillStyle = ["#6f8a4a", "#8aa05a", "#2a3428"][i % 3]; g.beginPath(); g.arc(rr() * 512, rr() * 512, 1.5 + rr() * 3, 0, 6.28); g.fill(); }
      for (let i = 0; i < 18; i++) { const x = rr() * 512, y = rr() * 512, a = rr() * 3.14; g.strokeStyle = "#5a4630"; g.lineWidth = 4; g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * 30, y + Math.sin(a) * 30); g.stroke(); g.strokeStyle = "#1c1410"; g.lineWidth = 1.5; g.stroke(); }
    }) })), padM = lam("cPad", () => ({ color: "#5f8a3a" }));
    const pools: [number, number, number, number][] = [[0, 0, 1.6, 1.1], [-4.5, 3.5, 2.6, 1.4], [5.5, 4.5, 3.0, 1.6], [-8, 10, 3.6, 2.0], [7, 13, 4.2, 2.0], [-2.5, -5, 1.8, 1.0]];
    { const pm = (poolM as THREE.MeshLambertMaterial).map; if (pm) pm.repeat.set(4, 4); }
    pools.forEach(([dx, dz, rx, rz], k) => {
      const c = new THREE.CircleGeometry(1, 28); c.rotateX(-Math.PI / 2); c.scale(rx, 1, rz); c.translate(X + dx, D0 + 0.05 + 0.006 * k, Z + dz); b.add(c, poolM);
      for (let i = 0; i < 5; i++) { const a = r() * 6.28, rr = 0.3 + r() * 0.55; const pd = new THREE.CircleGeometry(0.14 + r() * 0.12, 10, 0.4, 5.6); pd.rotateX(-Math.PI / 2); pd.translate(X + dx + Math.cos(a) * rx * rr, D0 + 0.09 + 0.006 * k, Z + dz + Math.sin(a) * rz * rr); b.add(pd, padM); }
    });
    // reeds + cattails in clumps (never over the pools, never in front of the lens path along x = X)
    const reedM = lam("cReed", () => ({ color: "#7a8a44" })), reedD = lam("cReedD", () => ({ color: "#5a6a34" })), cattail = lam("cCattail", () => ({ color: "#5a3a24" }));
    for (let i = 0; i < 70; i++) {
      const cx = X - 30 + r() * 60, cz = Z - 8 + r() * 28;
      if (Math.abs(cx - X) < 2.2 && cz < Z + 2) continue;
      if (pools.some(([dx, dz, rx, rz]) => ((cx - X - dx) / (rx + 0.3)) ** 2 + ((cz - Z - dz) / (rz + 0.3)) ** 2 < 1)) continue;
      const n = 6 + Math.floor(r() * 10);
      for (let k = 0; k < n; k++) {
        const h = 0.7 + r() * 1.1, x = cx + (r() - 0.5) * 0.9, z = cz + (r() - 0.5) * 0.9;
        const tilt = (r() - 0.5) * 0.35, g = new THREE.ConeGeometry(0.025, h, 4); g.rotateZ(tilt); g.translate(x, D0 + h / 2, z); b.add(g, k % 3 ? reedM : reedD);
        // v20 (rule 67/71): the cattail head sits ON the tilted stem (it floated beside it when placed straight up)
        if (k % 4 === 0) { const hd = new THREE.CylinderGeometry(0.035, 0.035, 0.18, 6); hd.rotateZ(tilt); hd.translate(x - Math.sin(tilt) * h * 0.32, D0 + h / 2 + Math.cos(tilt) * h * 0.32, z); b.add(hd, cattail); }
      }
    }
    // a plank boardwalk on stilts, shacks on stilts, a rowboat, barrels, a laundry line, a crooked fence
    const plank = matTex("cSwampPl", plankT(), 1, 4);
    box(b, plank, X - 1.0, D0 + 0.35, Z + 4, X + 1.0, D0 + 0.42, Z + 19);
    for (let z = Z + 4.5; z < Z + 19; z += 2) for (const dx of [-0.9, 0.9]) cyl(b, M.woodD(), X + dx, D0 - 0.1, z, 0.06, 0.06, 0.46, 6);
    for (const [dx, dz, w, h, si] of [[-9, 14, 6, 4.2, 2], [-2.5, 16.5, 5, 3.6, 5], [6, 14.5, 7, 4.8, 1], [14, 17, 5, 3.4, 6], [-17, 17, 6, 4.0, 3]] as const) {
      for (const [ox, oz] of [[-w / 2 + 0.3, -1.4], [w / 2 - 0.3, -1.4], [-w / 2 + 0.3, 1.4], [w / 2 - 0.3, 1.4]]) cyl(b, M.woodD(), X + dx + ox, D0 - 0.1, Z + dz + oz, 0.09, 0.09, 0.7, 6);
      // a plank shack (not a town house): weathered board walls, tar-paper roof with overhang, a door, one window, a stovepipe
      const sx0 = X + dx - w / 2, sx1 = X + dx + w / 2, sz0 = Z + dz - 1.6, sz1 = Z + dz + 1.6, sy = D0 + 0.55, sh = h * 0.62;
      box(b, lam("cShackW" + (si % 3), () => ({ map: ctex("cShackWT" + (si % 3), 256, 256, (g, rr) => {
        const base = ["#7a6650", "#6e6458", "#857055"][si % 3]; g.fillStyle = base; g.fillRect(0, 0, 256, 256);
        for (let x = 0; x < 256; x += 21) { g.fillStyle = rr() < 0.3 ? "rgba(255,240,210,0.12)" : "rgba(0,0,0,0.08)"; g.fillRect(x, 0, 21, 256); g.fillStyle = "#2a2018"; g.fillRect(x, 0, 3, 256);
          for (let k = 0; k < 3; k++) { const y = rr() * 256; g.strokeStyle = "rgba(40,30,20,0.6)"; g.lineWidth = 1.5; g.beginPath(); g.moveTo(x + 6, y); g.quadraticCurveTo(x + 11, y + 14, x + 8, y + 34); g.stroke(); }
          g.fillStyle = "#2a2018"; g.beginPath(); g.ellipse(x + 10, 40 + rr() * 170, 3, 2, 0, 0, 6.28); g.fill(); }
        g.fillStyle = "#1c1612"; for (const y of [24, 232]) for (let x = 10; x < 256; x += 21) { g.beginPath(); g.arc(x, y, 2.2, 0, 6.28); g.fill(); }
        g.fillStyle = "#5a5048"; g.fillRect(150, 120, 60, 44); g.strokeStyle = "#1c1612"; g.lineWidth = 3; g.strokeRect(150, 120, 60, 44);
      }) })), sx0, sy, sz0, sx1, sy + sh, sz1);
      for (let bx = sx0 + 0.3; bx < sx1 - 0.1; bx += 0.32) box(b, M.woodD(), bx, sy, sz0 - 0.015, bx + 0.025, sy + sh, sz0);
      box(b, lam("cShackRoof" + (si % 2), () => ({ color: si % 2 ? "#4a4440" : "#5a4a3a" })), sx0 - 0.35, sy + sh, sz0 - 0.45, sx1 + 0.35, sy + sh + 0.18, sz1 + 0.3);
      box(b, M.woodD(), X + dx - 0.45, sy, sz0 - 0.04, X + dx + 0.45, sy + 1.9, sz0);
      box(b, lam("cShackWin", () => ({ color: "#2a2a30" })), X + dx + w * 0.22, sy + 1.1, sz0 - 0.03, X + dx + w * 0.22 + 0.8, sy + 1.8, sz0);
      box(b, M.cream(), X + dx + w * 0.22 - 0.06, sy + 1.04, sz0 - 0.06, X + dx + w * 0.22 + 0.86, sy + 1.1, sz0);
      cyl(b, M.iron(), sx1 - 0.6, sy + sh, Z + dz, 0.09, 0.09, 1.1, 8);
      box(b, M.woodD(), sx0 - 0.2, sy - 0.08, sz0 - 1.0, sx1 + 0.2, sy, sz0); // porch deck
    }
    { const bx = X + 3.2, bz = Z + 7; const hull = new THREE.SphereGeometry(1, 14, 8, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2); hull.scale(1.5, 0.35, 0.55); hull.translate(bx, D0 + 0.38, bz); b.add(hull, M.wood());
      bar(b, M.woodD(), V(bx - 0.4, D0 + 0.4, bz - 0.2), V(bx + 1.6, D0 + 0.55, bz + 0.6), 0.03); }
    for (const [dx, dz] of [[-3.2, 6.5], [-2.6, 6.9], [9.5, 9]]) cyl(b, M.wood(), X + dx, D0 + 0.02, Z + dz, 0.26, 0.26, 0.62, 12);
    for (let k = 0; k < 7; k++) { const x = X - 13 + k * 1.3; bar(b, M.woodD(), V(x, D0, Z + 8 + (k % 2) * 0.2), V(x + 0.1 * (k % 3 - 1), D0 + 1.0, Z + 8 + (k % 2) * 0.2), 0.035); }
    bar(b, M.woodD(), V(X - 13, D0 + 0.85, Z + 8.1), V(X - 5.2, D0 + 0.7, Z + 8.2), 0.025);
    pole(b, M.woodD(), V(X - 6, D0, Z + 13), V(X - 6, D0 + 2.6, Z + 13), 0.05); pole(b, M.woodD(), V(X + 1, D0, Z + 13.5), V(X + 1, D0 + 2.6, Z + 13.5), 0.05);
    bar(b, M.iron(), V(X - 6, D0 + 2.5, Z + 13), V(X + 1, D0 + 2.5, Z + 13.5), 0.008);
    ["#c9453a", "#f4f2ec", "#3f6fb5", "#e2b33c", "#f4f2ec"].forEach((c, k) => box(b, lam("cLaundry" + c, () => ({ color: c })), X - 5.4 + k * 1.3, D0 + 1.8, Z + 13.04 + k * 0.07, X - 4.8 + k * 1.3, D0 + 2.48, Z + 13.08 + k * 0.07));
    // far shore line and a few sails on the lake so the horizon is never empty
    for (let k = 0; k < 4; k++) { const sx = X - 60 + k * 38 + r() * 10, sz = Z + 160 + r() * 140; box(b, M.woodD(), sx - 1.6, D0 - 0.1, sz - 0.5, sx + 1.6, D0 + 0.4, sz + 0.5); const sl = new THREE.BufferGeometry(); sl.setAttribute("position", new THREE.Float32BufferAttribute([sx, D0 + 0.4, sz, sx, D0 + 4.4, sz, sx + 2.2, D0 + 0.5, sz], 3)); sl.computeVertexNormals(); b.add(sl, lam("cSail", () => ({ color: "#efe6d2", side: THREE.DoubleSide }))); }
    for (let k = 0; k < 9; k++) prop(b, kit, ["tree_oak", "tree_default", "tree_fat"][k % 3], X - 40 + k * 10 + r() * 4, D0, Z - 26 - r() * 10, 5 + r() * 3, r() * 6);
    b.build(root);
  }

  // ======== COUNCIL ROOM (v2 takes 6-7): long baize table, the plan, the model, portraits, a city map, gas lamps ========
  {
    const R = COUNCIL, b = new Batch(), r = rng(1855);
    const x0 = R.x - R.w / 2, x1 = R.x + R.w / 2, z0 = R.z - R.d / 2, z1 = R.z + R.d / 2;
    const paper = lam("cCouncilWall", () => ({ map: ctex("cCouncilPaper", 256, 512, (g) => {
      g.fillStyle = "#b7a27a"; g.fillRect(0, 0, 256, 512);
      for (let x = 0; x < 256; x += 32) { g.fillStyle = "#a8936c"; g.fillRect(x, 0, 12, 330); }
      g.fillStyle = "#8a6a44"; for (let y = 20; y < 330; y += 48) for (let x = 16; x < 256; x += 64) { g.beginPath(); g.arc(x, y, 5, 0, 6.28); g.fill(); }
      g.fillStyle = "#4a2e1e"; g.fillRect(0, 330, 256, 182); g.fillStyle = "#2e1c12"; g.fillRect(0, 326, 256, 10);
      g.strokeStyle = "#24160c"; g.lineWidth = 4; for (let x = 8; x < 256; x += 128) g.strokeRect(x, 352, 112, 140);
    }) }));
    room(b, x0, x1, D0, z0, z1, R.h, lam("cWallInkCouncil", () => ({ map: wallpaperInk("council", "#b7a27a", "#6a4a3a", "#4a2e1e") })), matTex("cCouncilFloor", plankT(), 1, 1),
      [{ at: R.x - 3.6, w: 1.3, y0: 0.9, y1: 3.0 }, { at: R.x + 2.3, w: 1.3, y0: 0.9, y1: 3.0 }],
      lam("cStreetViewM", () => ({ map: streetViewT() })), lam("cCeilM", () => ({ color: "#e8dcc0" })));
    for (const [ax, az, cx, cz] of [[x0, z0, x1, z0 + 0.15], [x0, z1 - 0.15, x1, z1], [x0, z0, x0 + 0.15, z1], [x1 - 0.15, z0, x1, z1]]) box(b, M.cream(), ax, D0 + R.h - 0.25, az, cx, D0 + R.h, cz);
    // the long table: green baize top, carved legs, papers, inkwells, quills, a bell, water carafe + glasses
    const tz0 = R.z - 1.0, tz1 = R.z + 1.0, tx0 = R.x - 1.9, tx1 = R.x + 1.9, ty = D0 + 0.76;
    // v8: drawn baize top: gilt-tooled leather border, a blotter, written papers, an ink blot (teardown: dense dressing)
    const baizeT = ctex("cBaize8", 2048, 1024, (g, rr) => {
      g.fillStyle = "#3f6a44"; g.fillRect(0, 0, 2048, 1024);
      for (let i = 0; i < 3000; i++) { g.fillStyle = rr() < 0.5 ? "rgba(20,40,24,0.18)" : "rgba(120,160,110,0.12)"; g.fillRect(rr() * 2048, rr() * 1024, 3, 3); }
      g.fillStyle = "#5a3a22"; g.fillRect(0, 0, 2048, 70); g.fillRect(0, 954, 2048, 70); g.fillRect(0, 0, 70, 1024); g.fillRect(1978, 0, 70, 1024);
      g.strokeStyle = "#d9b04a"; g.lineWidth = 5; g.strokeRect(84, 84, 1880, 856); g.setLineDash([14, 10]); g.strokeRect(40, 40, 1968, 944); g.setLineDash([]);
      g.strokeStyle = "#1e140e"; g.lineWidth = 6; g.strokeRect(70, 70, 1908, 884);
      for (const [x, y] of [[84, 84], [1964, 84], [84, 940], [1964, 940]]) { g.fillStyle = "#d9b04a"; g.beginPath(); g.arc(x, y, 16, 0, 6.29); g.fill(); g.stroke(); }
      for (const [x, y, w, h, a] of [[260, 160, 300, 220, -0.08], [1480, 620, 300, 220, 0.1], [300, 640, 260, 190, 0.05], [1500, 170, 280, 200, -0.06]]) {
        g.save(); g.translate(x + w / 2, y + h / 2); g.rotate(a); g.fillStyle = "#f2ead6"; g.fillRect(-w / 2, -h / 2, w, h); g.strokeStyle = "#2a1e24"; g.lineWidth = 4; g.strokeRect(-w / 2, -h / 2, w, h);
        g.strokeStyle = "rgba(40,30,50,0.75)"; g.lineWidth = 3; for (let ly = -h / 2 + 28; ly < h / 2 - 18; ly += 22) { g.beginPath(); g.moveTo(-w / 2 + 20, ly); for (let lx = -w / 2 + 20; lx < w / 2 - 20 - rr() * 60; lx += 12) g.lineTo(lx, ly + Math.sin(lx * 0.6) * 3); g.stroke(); }
        g.restore(); }
      g.fillStyle = "#1a1420"; g.beginPath(); g.ellipse(640, 470, 34, 22, 0.4, 0, 6.29); g.fill(); for (let i = 0; i < 7; i++) { g.beginPath(); g.arc(640 + (rr() - 0.5) * 120, 470 + (rr() - 0.5) * 80, 4 + rr() * 6, 0, 6.29); g.fill(); }
    });
    box(b, lam("cBaize8", () => ({ map: baizeT, emissive: new THREE.Color(0.42, 0.42, 0.42), emissiveMap: baizeT })), tx0, ty - 0.05, tz0, tx1, ty, tz1); // v8: the top sits in the room shadow; a little self-light keeps the drawn papers readable
    box(b, M.woodD(), tx0 - 0.04, ty - 0.12, tz0 - 0.04, tx1 + 0.04, ty - 0.05, tz1 + 0.04);
    for (const [lx, lz] of [[tx0 + 0.15, tz0 + 0.15], [tx1 - 0.15, tz0 + 0.15], [tx0 + 0.15, tz1 - 0.15], [tx1 - 0.15, tz1 - 0.15]]) cyl(b, M.woodD(), lx, D0, lz, 0.06, 0.08, ty - D0 - 0.12, 8);
    for (let k = 0; k < 9; k++) { const px = tx0 + 0.3 + r() * 3.2, pz = (k % 2 ? tz0 + 0.12 : tz1 - 0.42) + r() * 0.2; if (Math.abs(px - R.x) < 0.75) continue; box(b, M.white(), px - 0.15, ty + 0.002 + k * 0.0012, pz, px + 0.15, ty + 0.004 + k * 0.0012, pz + 0.3); }
    for (const ix of [tx0 + 0.5, tx1 - 0.6]) { cyl(b, M.iron(), ix, ty, tz0 + 0.25, 0.04, 0.035, 0.06, 10); bar(b, M.white(), V(ix + 0.01, ty + 0.05, tz0 + 0.25), V(ix + 0.08, ty + 0.25, tz0 + 0.3), 0.006); }
    cyl(b, lam("cGlassC", () => ({ color: "#bfd6e0" })), tx1 - 0.35, ty, tz1 - 0.3, 0.07, 0.05, 0.26, 12);
    for (const gx of [tx1 - 0.6, tx1 - 0.75]) cyl(b, lam("cGlassC", () => ({ color: "#bfd6e0" })), gx, ty, tz1 - 0.25, 0.035, 0.03, 0.1, 10);
    cyl(b, M.brass(), tx0 + 0.3, ty, tz1 - 0.3, 0.06, 0.03, 0.08, 10);
    // v19: a damask table runner across the table under the model and the drafting tools (the near strip the inserts look down
    // was a bare green field); burgundy with gold motifs, a woven border and gold fringe at both ends
    { const runT = ctex("cRunnerT", 256, 1024, (g) => {
        g.fillStyle = "#7a2430"; g.fillRect(0, 0, 256, 1024);
        g.strokeStyle = "#c9a24a"; g.lineWidth = 6; g.strokeRect(10, 10, 236, 1004); g.lineWidth = 2.5; g.strokeRect(22, 22, 212, 980);
        for (let y = 32; y < 1000; y += 14) { g.fillStyle = "#c9a24a"; g.beginPath(); g.arc(16, y, 2.2, 0, 6.28); g.arc(240, y, 2.2, 0, 6.28); g.fill(); }
        for (let row = 0; row < 9; row++) for (let col = 0; col < 2; col++) {
          const cx = 74 + col * 108 + (row % 2) * 0, cy = 70 + row * 110; g.strokeStyle = "#d9b45a"; g.fillStyle = "#9a3440"; g.lineWidth = 3;
          g.beginPath(); g.moveTo(cx, cy - 34); g.quadraticCurveTo(cx + 26, cy - 10, cx, cy + 34); g.quadraticCurveTo(cx - 26, cy - 10, cx, cy - 34); g.fill(); g.stroke();
          g.beginPath(); g.arc(cx, cy - 4, 7, 0, 6.28); g.stroke();
          for (const sx of [-1, 1]) { g.beginPath(); g.moveTo(cx + sx * 8, cy + 14); g.quadraticCurveTo(cx + sx * 30, cy + 10, cx + sx * 36, cy - 12); g.stroke(); }
        }
      });
      const rx0 = R.x - 0.42, rx1 = R.x + 0.78;
      box(b, lam("cRunner", () => ({ map: runT, emissive: new THREE.Color(0.3, 0.3, 0.3), emissiveMap: runT })), rx0, ty, tz0 - 0.02, rx1, ty + 0.0025, tz1 + 0.02);
      for (const z of [tz0 - 0.02, tz1 + 0.02]) for (let x = rx0 + 0.02; x < rx1; x += 0.045) bar(b, M.brass(), V(x, ty, z), V(x, ty - 0.07, z + (z < R.z ? -0.005 : 0.005)), 0.006);
    }
    // v17 (owner Nov 12: council room needs more drawn objects): ledgers, a book stack, a candlestick with a lit candle (visible
    // light source, D5), a gavel on its block, rolled plans, a pen tray, spectacles. Kept clear of the model (|x - R.x| > 0.8)
    const ledgerT = ctex("cLedgerT", 256, 160, (g) => { g.fillStyle = "#f2ead6"; g.fillRect(0, 0, 256, 160); g.fillStyle = "#5a2a24"; g.fillRect(124, 0, 8, 160); g.strokeStyle = "#5a6a8a"; g.lineWidth = 2; for (let y = 22; y < 150; y += 12) { g.beginPath(); g.moveTo(12, y); g.lineTo(116, y); g.moveTo(140, y); g.lineTo(244, y); g.stroke(); } g.strokeStyle = "#a8322c"; g.beginPath(); g.moveTo(40, 10); g.lineTo(40, 152); g.moveTo(168, 10); g.lineTo(168, 152); g.stroke(); g.strokeStyle = "#241726"; g.lineWidth = 4; g.strokeRect(2, 2, 252, 156); });
    for (const [lx, lz, a] of [[R.x - 1.35, tz0 + 0.45, 0.15], [R.x + 1.25, tz0 + 0.5, -0.2]] as const) { const g2 = new THREE.BoxGeometry(0.46, 0.025, 0.3); g2.rotateY(a); g2.translate(lx, ty + 0.0125, lz); b.add(g2, lam("cLedger", () => ({ map: ledgerT }))); }
    for (let k = 0; k < 3; k++) { const g2 = new THREE.BoxGeometry(0.3 - k * 0.02, 0.06, 0.22 - k * 0.01); g2.rotateY(0.2 * k - 0.1); g2.translate(tx1 - 0.35, ty + 0.03 + k * 0.06, tz0 + 0.35); b.add(g2, lam("cBook" + (k % 4), () => ({ color: ["#7a2a2a", "#2f4a6a", "#3f5a3a", "#8a6a3a"][k % 4] }))); }
    cyl(b, M.brass(), tx0 + 0.35, ty, tz0 + 0.5, 0.08, 0.05, 0.03, 12); cyl(b, M.brass(), tx0 + 0.35, ty + 0.03, tz0 + 0.5, 0.02, 0.025, 0.22, 8); cyl(b, M.white(), tx0 + 0.35, ty + 0.25, tz0 + 0.5, 0.018, 0.018, 0.12, 8);
    box(b, glow("candle", 3.0, 2.2, 1.0), tx0 + 0.34, ty + 0.37, tz0 + 0.49, tx0 + 0.36, ty + 0.42, tz0 + 0.51);
    box(b, M.woodD(), R.x + 0.95, ty, tz0 + 0.25, R.x + 1.15, ty + 0.03, tz0 + 0.38); bar(b, M.woodD(), V(R.x + 1.0, ty + 0.06, tz0 + 0.3), V(R.x + 1.35, ty + 0.06, tz0 + 0.42), 0.012); cyl(b, M.woodD(), R.x + 0.98, ty + 0.03, tz0 + 0.29, 0.035, 0.035, 0.1, 10);
    for (const [px, pz] of [[R.x - 1.05, tz1 - 0.25], [R.x - 0.95, tz1 - 0.15]] as const) { const g2 = new THREE.CylinderGeometry(0.035, 0.035, 0.6, 10); g2.rotateZ(Math.PI / 2); g2.translate(px, ty + 0.035, pz); b.add(g2, M.cream()); }
    box(b, M.brass(), tx0 + 0.7, ty, tz0 + 0.2, tx0 + 1.0, ty + 0.015, tz0 + 0.3); bar(b, M.white(), V(tx0 + 0.72, ty + 0.03, tz0 + 0.25), V(tx0 + 1.05, ty + 0.06, tz0 + 0.2), 0.006);
    for (const sx of [-1, 1]) { const g2 = new THREE.TorusGeometry(0.03, 0.005, 6, 14); g2.rotateX(Math.PI / 2); g2.translate(R.x + 1.5 + sx * 0.035, ty + 0.006, tz0 + 0.75); b.add(g2, M.iron()); }
    // v18: drafting tools in front of the model (the insert shot looks down this strip): brass dividers, a T-square, pencils,
    // a magnifying glass, a pounce pot; kept clear of the blueprint (x < R.x) and of the drape side
    { const zz = R.z - 0.45, y0 = ty + 0.004;
      bar(b, M.brass(), V(R.x + 0.18, y0, zz - 0.18), V(R.x + 0.3, y0 + 0.01, zz + 0.05), 0.006); bar(b, M.brass(), V(R.x + 0.42, y0, zz - 0.16), V(R.x + 0.3, y0 + 0.01, zz + 0.05), 0.006); cyl(b, M.brass(), R.x + 0.3, y0, zz + 0.05, 0.015, 0.015, 0.02, 8);
      // (v19 self-review: the T-square read as a loose dark bar and the pounce pot as a white blob at the frame edge; removed, rule 56)
      for (let k = 0; k < 3; k++) { const g2 = new THREE.CylinderGeometry(0.006, 0.006, 0.17, 6); g2.rotateZ(Math.PI / 2); g2.rotateY(0.3 + k * 0.25); g2.translate(R.x - 0.05 + k * 0.03, y0 + 0.006, zz - 0.22 + k * 0.02); b.add(g2, lam("cPencil" + k, () => ({ color: ["#d9a441", "#a8322c", "#3f6fb5"][k] }))); }
      { const g2 = new THREE.TorusGeometry(0.05, 0.009, 8, 18); g2.rotateX(Math.PI / 2); g2.translate(R.x + 0.55, y0 + 0.009, zz + 0.12); b.add(g2, M.brass());
        const lens = new THREE.CircleGeometry(0.046, 18); lens.rotateX(-Math.PI / 2); lens.translate(R.x + 0.55, y0 + 0.012, zz + 0.12); b.add(lens, lam("cLens", () => ({ color: "#cfe3ee" })));
        // handle runs INTO the brass rim (rule 58): ferrule at the rim, wooden grip outward
        bar(b, M.brass(), V(R.x + 0.575, y0 + 0.009, zz + 0.145), V(R.x + 0.605, y0 + 0.009, zz + 0.175), 0.011); bar(b, M.woodD(), V(R.x + 0.6, y0 + 0.009, zz + 0.17), V(R.x + 0.69, y0 + 0.009, zz + 0.26), 0.013); }
    }
    // chairs along the near side face the table (the camera looks over them)
    for (const cx of [R.x - 1.4, R.x + 1.4]) for (const cz of [tz0 - 0.5]) {
      box(b, M.woodD(), cx - 0.22, D0 + 0.44, cz - 0.22, cx + 0.22, D0 + 0.5, cz + 0.22); box(b, M.plush(), cx - 0.2, D0 + 0.5, cz - 0.2, cx + 0.2, D0 + 0.56, cz + 0.2);
      for (const [dx, dz] of [[-0.18, -0.18], [0.18, -0.18], [-0.18, 0.18], [0.18, 0.18]]) box(b, M.woodD(), cx + dx - 0.025, D0, cz + dz - 0.025, cx + dx + 0.025, D0 + 0.44, cz + dz + 0.025);
      box(b, M.woodD(), cx - 0.2, D0 + 0.56, cz - 0.24, cx + 0.2, D0 + 1.0, cz - 0.2);
    }
    // back wall: a big framed map of the city, two portraits, a clock, a flag, bookcases, gas lamps
    const mapT = ctex("cCityMap", 1024, 640, (g, rr) => {
      g.fillStyle = "#efe2bf"; g.fillRect(0, 0, 1024, 640);
      g.fillStyle = "#9cc3e6"; g.fillRect(860, 0, 164, 640); g.beginPath(); g.moveTo(0, 300); g.bezierCurveTo(300, 280, 500, 360, 860, 330); g.lineTo(860, 380); g.bezierCurveTo(500, 410, 300, 330, 0, 350); g.fill();
      g.strokeStyle = "#8a6a4a"; g.lineWidth = 3; for (let x = 40; x < 860; x += 56) { g.beginPath(); g.moveTo(x, 20); g.lineTo(x, 620); g.stroke(); } for (let y = 30; y < 620; y += 52) { g.beginPath(); g.moveTo(0, y); g.lineTo(860, y); g.stroke(); }
      g.fillStyle = "#c98a5a"; for (let i = 0; i < 70; i++) { const x = 44 + Math.floor(rr() * 15) * 56, y = 34 + Math.floor(rr() * 11) * 52; if (y > 280 && y < 400) continue; g.fillRect(x + 4, y + 4, 46, 42); }
      g.fillStyle = "#3b2416"; g.font = "bold 46px Georgia, serif"; g.textAlign = "center"; g.fillText("CITY OF CHICAGO", 430, 600); g.font = "italic 26px Georgia, serif"; g.fillText("Lake Michigan", 942, 80);
      g.strokeStyle = "#3b2416"; g.lineWidth = 10; g.strokeRect(5, 5, 1014, 630);
    });
    quad(b, lam("cCityMapM", () => ({ map: mapT })), V(R.x + 1.25, D0 + 1.3, z1 - 0.05), V(R.x - 1.25, D0 + 1.3, z1 - 0.05), V(R.x - 1.25, D0 + 2.86, z1 - 0.05), V(R.x + 1.25, D0 + 2.86, z1 - 0.05));
    box(b, M.brass(), R.x - 1.32, D0 + 1.23, z1 - 0.04, R.x + 1.32, D0 + 2.93, z1 - 0.02);
    for (const px of [R.x - 2.4, R.x + 3.4]) { box(b, M.brass(), px - 0.4, D0 + 1.6, z1 - 0.04, px + 0.4, D0 + 2.6, z1 - 0.02); box(b, lam("cPortrait", () => ({ map: ctex("cPortraitT", 128, 160, (g) => { g.fillStyle = "#3b3a30"; g.fillRect(0, 0, 128, 160); g.fillStyle = "#e8c8a0"; g.beginPath(); g.ellipse(64, 66, 26, 32, 0, 0, 6.28); g.fill(); g.fillStyle = "#2a2420"; g.fillRect(28, 108, 72, 52); g.fillStyle = "#5a4030"; g.fillRect(40, 84, 48, 14); }) })), px - 0.34, D0 + 1.66, z1 - 0.05, px + 0.34, D0 + 2.54, z1 - 0.04); }
    box(b, M.woodD(), x0 + 0.1, D0, z1 - 2.8, x0 + 0.5, D0 + 2.4, z1 - 0.6);
    for (let sy = 0; sy < 5; sy++) for (let k = 0; k < 12; k++) box(b, lam("cBook" + (k % 4), () => ({ color: ["#7a2a2a", "#2f4a6a", "#3f5a3a", "#8a6a3a"][k % 4] })), x0 + 0.5, D0 + 0.12 + sy * 0.46, z1 - 2.7 + k * 0.17, x0 + 0.52, D0 + 0.46 + sy * 0.46 - (k % 3) * 0.04, z1 - 2.56 + k * 0.17);
    box(b, M.woodD(), x1 - 0.5, D0, z1 - 2.2, x1 - 0.1, D0 + 2.1, z1 - 1.6);
    cyl(b, M.cream(), x1 - 0.52, D0 + 1.6, z1 - 1.9, 0.18, 0.18, 0.04, 16);
    pole(b, M.brass(), V(x1 - 0.8, D0, z1 - 0.5), V(x1 - 0.8, D0 + 2.4, z1 - 0.5), 0.025);
    box(b, lam("cFlagS", () => ({ color: "#c0353a" })), x1 - 0.79, D0 + 1.6, z1 - 0.5, x1 - 0.1, D0 + 2.35, z1 - 0.48);
    for (const lx of [R.x - 3.9, R.x + 3.9]) { bar(b, M.brass(), V(lx, D0 + 2.2, z1 - 0.05), V(lx, D0 + 2.2, z1 - 0.35), 0.02); box(b, glow("gaslamp", 2.6, 1.9, 0.9), lx - 0.07, D0 + 2.2, z1 - 0.42, lx + 0.07, D0 + 2.42, z1 - 0.28); }
    // hat stand with hats, a spittoon, a coal stove
    pole(b, M.woodD(), V(x0 + 0.6, D0, z0 + 0.8), V(x0 + 0.6, D0 + 1.8, z0 + 0.8), 0.03);
    for (const [dy, c] of [[1.78, "#2b2830"], [1.6, "#3a3638"]] as const) cyl(b, lam("cHat" + c, () => ({ color: c })), x0 + 0.6 + (dy > 1.7 ? 0 : 0.12), D0 + dy, z0 + 0.8, 0.13, 0.11, 0.16, 12);
    cyl(b, M.brass(), x0 + 1.0, D0, z1 - 0.4, 0.14, 0.1, 0.18, 12);
    cyl(b, M.iron(), x1 - 0.9, D0, z0 + 1.2, 0.3, 0.32, 0.9, 14); pole(b, M.iron(), V(x1 - 0.9, D0 + 0.9, z0 + 1.2), V(x1 - 0.9, D0 + R.h, z0 + 1.2), 0.07);
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
    // v17 (owner Nov 12: more drawn objects under the Tremont, teardown dense dressing): timber girders along every screw row
    // (the screw caps press into their undersides, rule 29) and joists across them every 0.6 m, so the dark ceiling reads as
    // a framed floor full of lines instead of a flat slab. Joist tops overlap the slab by 1 cm (no coplanar faces, rule 25).
    const gM = lam("cGirder", () => ({ color: "#6a4a30" })), jM = lam("cJoist", () => ({ color: "#7a5636" }));
    for (let z = TRE.z + 0.3 + 1.4; z < TRE.z + TRE.d - 0.3; z += 2.8) box(b, gM, TRE.x0 + 0.2, -0.4, z - 0.14, TRE.x1 - 0.2, -0.17, z + 0.14);
    for (let x = TRE.x0 + 0.5; x < TRE.x1 - 0.3; x += 0.6) box(b, jM, x - 0.05, -0.3, TRE.z + 0.4, x + 0.05, -0.16, TRE.z + TRE.d - 0.4);
    // cross braces between a few girders, chains and hooks hanging from them
    for (let x = TRE.x0 + 2.0; x < TRE.x1 - 1; x += 4.8) for (let z = TRE.z + 1.7; z < TRE.z + TRE.d - 3; z += 5.6) bar(b, gM, V(x, -0.38, z), V(x + 1.6, -0.38, z + 2.8), 0.05);
    for (const [x, z] of [[-8.5, 116.6], [-2.2, 119.8], [4.6, 116.4], [10.6, 120.2], [12.4, 116.8]] as const) { bar(b, M.iron(), V(x, -0.4, z), V(x, -1.1, z), 0.012); box(b, M.iron(), x - 0.05, -1.18, z - 0.02, x + 0.05, -1.1, z + 0.02); }
    for (const z of [113.4, 117.0, 123]) for (const x of [-10, -4, 2, 8]) {
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
    for (const z of [113.4, 117.0, 123]) for (const x of [-10, -4, 2, 8]) { const c = new THREE.CircleGeometry(1.7, 24); c.rotateX(-Math.PI / 2); c.translate(x, D0 + 0.07, z); b.add(c, pm); }
  }, false);
  // v17: the work floor under the Tremont (take 10 only): cribbing stacks, barrels, buckets, crates, coiled rope, shovels, planks,
  // kept to the rows the crankers do not use (z 120.4 / 122.6 / 125.2) plus a near cribbing stack as the foreground layer
  S.under = grp(root, (b) => {
    const r = rng(1858), tim = lam("cCrib", () => ({ color: "#8a6440" })), barrel = lam("cBarrel", () => ({ color: "#9a6a3a" })), rope = lam("cRope", () => ({ color: "#c9a873" }));
    const crib = (x: number, z: number, n: number) => { for (let l = 0; l < n; l++) for (let k = -1; k <= 1; k++) l % 2 ? box(b, tim, x + k * 0.26 - 0.09, D0 + l * 0.16, z - 0.5, x + k * 0.26 + 0.09, D0 + l * 0.16 + 0.15, z + 0.5) : box(b, tim, x - 0.5, D0 + l * 0.16, z + k * 0.26 - 0.09, x + 0.5, D0 + l * 0.16 + 0.15, z + k * 0.26 + 0.09); };
    const cask = (x: number, z: number) => { cyl(b, barrel, x, D0, z, 0.24, 0.24, 0.66, 14); for (const y of [0.1, 0.5]) cyl(b, M.iron(), x, D0 + y, z, 0.252, 0.252, 0.05, 14); cyl(b, M.woodD(), x, D0 + 0.66, z, 0.22, 0.22, 0.015, 14); };
    const pail = (x: number, z: number) => { cyl(b, M.steel(), x, D0, z, 0.11, 0.14, 0.24, 12); bar(b, M.iron(), V(x - 0.13, D0 + 0.24, z), V(x + 0.13, D0 + 0.24, z), 0.008); };
    const crate = (x: number, z: number, s2: number) => { box(b, M.wood(), x - s2, D0, z - s2, x + s2, D0 + 2 * s2 * 0.8, z + s2); for (const d of [-0.6, 0.6]) box(b, M.woodD(), x - s2 - 0.01, D0 + 0.05, z + d * s2 - 0.03, x + s2 + 0.01, D0 + 2 * s2 * 0.8 - 0.05, z + d * s2 + 0.03); };
    const coil = (x: number, z: number) => { for (let k = 0; k < 4; k++) { const t2 = new THREE.TorusGeometry(0.2 - k * 0.035, 0.025, 6, 20); t2.rotateX(Math.PI / 2); t2.translate(x, D0 + 0.03 + k * 0.04, z); b.add(t2, rope); } };
    const shovel = (x: number, z: number, a: number) => { bar(b, M.wood(), V(x, D0 + 0.05, z), V(x + 0.3 * Math.cos(a), D0 + 1.1, z + 0.3 * Math.sin(a)), 0.02); box(b, M.steel(), x - 0.1, D0, z - 0.02, x + 0.1, D0 + 0.26, z + 0.02); };
    const plank = (x: number, z: number, a: number) => { const g = new THREE.BoxGeometry(2.2, 0.05, 0.24); g.rotateY(a); g.translate(x, D0 + 0.026, z); b.add(g, tim); };
    const xs = [-12.3, -9.9, -7.5, -5.1, -2.7, -0.3, 2.1, 4.5, 6.9, 9.3, 11.7];
    xs.forEach((x, i) => {
      const k = i % 5, j = (x * 0.37 + r()) * 0.4;
      if (k === 0) crib(x, 120.4, 4); else if (k === 1) { cask(x - 0.3, 120.4); cask(x + 0.3, 120.5); } else if (k === 2) { crate(x, 120.4, 0.3); pail(x + 0.55, 120.2); } else if (k === 3) { coil(x, 120.5); shovel(x + 0.5, 120.3, 0.4); } else { plank(x, 120.5, 0.1 + j * 0.2); pail(x - 0.4, 120.3); }
      if ((i + 2) % 3 === 0) crib(x + 0.2, 122.6, 3); else if ((i + 2) % 3 === 1) cask(x, 122.6); else crate(x, 122.6, 0.35);
      if (i % 2 === 0) cask(x - 0.2, 125.2); else crib(x, 125.2, 5);
    });
    crib(13.6, 117.3, 3); cask(13.4, 114.0); pail(13.9, 114.5); plank(12.8, 115.0, 1.2); coil(14.0, 118.6);
    // v19f (edge floor): the trodden work floor is drawn (boot prints, wood chips, pebbles, wheel ruts, cracks), a flat
    // alpha-tested decal just over the mud so the plain ground under the hotel reads as a busy site
    { const dt = ctex("cWorkFloorT", 1024, 1024, (g, rr) => {
        g.clearRect(0, 0, 1024, 1024); g.lineCap = "round";
        g.strokeStyle = "#5a4028"; g.lineWidth = 5; for (const y0 of [300, 360]) { g.beginPath(); g.moveTo(0, y0); for (let x = 0; x <= 1024; x += 64) g.lineTo(x, y0 + Math.sin(x * 0.01) * 14); g.stroke(); }
        for (let k = 0; k < 40; k++) { const x = rr() * 1024, y = rr() * 1024, a = rr() * 6.28; g.save(); g.translate(x, y); g.rotate(a); g.fillStyle = "rgba(70,48,28,0.75)"; g.beginPath(); g.ellipse(0, 0, 9, 18, 0, 0, 6.29); g.fill(); g.beginPath(); g.ellipse(0, 26, 8, 9, 0, 0, 6.29); g.fill(); g.restore(); }
        for (let k = 0; k < 120; k++) { const x = rr() * 1024, y = rr() * 1024, a = rr() * 6.28, l = 10 + rr() * 22; g.strokeStyle = rr() < 0.5 ? "#d9b878" : "#a07a48"; g.lineWidth = 5; g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke(); }
        for (let k = 0; k < 90; k++) { const x = rr() * 1024, y = rr() * 1024, rd = 4 + rr() * 8; g.fillStyle = rr() < 0.5 ? "#b8ad9a" : "#8a8070"; g.strokeStyle = "#2a1e24"; g.lineWidth = 2.5; g.beginPath(); g.ellipse(x, y, rd * 1.3, rd, rr() * 3, 0, 6.29); g.fill(); g.stroke(); }
        g.strokeStyle = "#3a2a1c"; g.lineWidth = 3; for (let k = 0; k < 14; k++) { let x = rr() * 1024, y = rr() * 1024; g.beginPath(); g.moveTo(x, y); for (let j = 0; j < 4; j++) { x += (rr() - 0.5) * 60; y += 15 + rr() * 25; g.lineTo(x, y); } g.stroke(); }
      }); dt.wrapS = dt.wrapT = THREE.RepeatWrapping; dt.repeat.set(7, 5);
      const fl = new THREE.PlaneGeometry(30, 20); fl.rotateX(-Math.PI / 2); fl.translate(0, D0 + 0.012, 121); // inside the hotel footprint (TRE x -15..15, z 111..131)
      b.add(fl, lam("cWorkFloor", () => ({ map: dt, transparent: true, alphaTest: 0.35, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 }))); }
  });
  // v17 (owner Nov 12: more drawn objects on the water): the lake beyond the shore close-up and the river ending gets a pier on
  // pilings, moored schooners with sails, a lighthouse with a lit lamp, buoys and mooring posts (teardown: every layer dressed)
  grp(root, (b) => {
    const r = rng(1871), hullM = lam("cHull", () => ({ color: "#4a3a34" })), sailM = lam("cSail", () => ({ color: "#f2ead6", side: THREE.DoubleSide })), wl = -0.2;
    // pier from the shore out into the lake
    box(b, lam("cPierDeck", () => ({ map: plankT() })), 171, D0 + 0.55, 47, 203, D0 + 0.65, 50.2, 1);
    for (let x = 172; x <= 203; x += 2.6) for (const z of [47.2, 50]) { cyl(b, M.woodD(), x, wl - 0.5, z, 0.14, 0.14, D0 + 1.15 - wl + 0.5, 8); }
    for (let x = 172; x <= 203; x += 2.6) box(b, M.woodD(), x - 0.06, D0 + 0.85, 47.1, x + 0.06, D0 + 0.95, 50.1);
    bar(b, M.wood(), V(171, D0 + 1.1, 47.2), V(203, D0 + 1.1, 47.2), 0.04); bar(b, M.wood(), V(171, D0 + 1.1, 50), V(203, D0 + 1.1, 50), 0.04);
    for (const [x, z] of [[176, 48.6], [184, 48.4], [196, 48.8]] as const) { cyl(b, lam("cBarrel", () => ({ color: "#9a6a3a" })), x, D0 + 0.65, z, 0.24, 0.24, 0.66, 12); }
    // schooners at anchor
    const schooner = (x: number, z: number, L: number, yaw: number) => {
      const c = Math.cos(yaw), sn = Math.sin(yaw), P = (u: number, y: number, v: number) => V(x + u * c - v * sn, y, z + u * sn + v * c);
      const hull = new THREE.BoxGeometry(L, 1.1, L * 0.24); hull.rotateY(-yaw); hull.translate(x, wl + 0.2, z); b.add(hull, hullM); // v19: hull sunk 0.4 m into the water so it never reads as a slab sitting on it
      const rail = new THREE.BoxGeometry(L * 1.01, 0.12, L * 0.25); rail.rotateY(-yaw); rail.translate(x, wl + 0.77, z); b.add(rail, lam("cHullT", () => ({ color: "#d9c79a" })));
      for (const m of [-0.22, 0.2]) {
        const top = P(m * L, wl + L * 0.95, 0), bot = P(m * L, wl + 0.75, 0); pole(b, M.woodD(), bot, top, 0.07);
        const s0 = P(m * L + 0.3, wl + 1.3, 0), s1 = P(m * L + L * 0.3, wl + 1.3, 0), s2 = P(m * L + 0.3, wl + L * 0.85, 0);
        const g = new THREE.BufferGeometry().setFromPoints([s0, s1, s2]); g.setIndex([0, 1, 2]); g.computeVertexNormals(); b.add(g, sailM);
      }
      bar(b, M.woodD(), P(L * 0.5, wl + 0.75, 0), P(L * 0.75, wl + 1.45, 0), 0.04);
    };
    // the river for the ending (take 16 looks west up it): schooners moored along both quays, a lumber barge, mooring piles
    /* v19f: (146,-16) + (124,-15.5) removed, the ending crane swept over them as cut sails */ schooner(118, 24, 9, 0.1); schooner(140, 25, 11, -0.05);
    // v19: the ending camera (f1823-2200) looks NW across the river from x 108-144, z -19..-56: schooners moored on both quays in view
    schooner(95, 24.4, 10, 0.03); schooner(82, 24.6, 8, -0.04); schooner(104, -15.4, 9, -0.04); schooner(88, -15.6, 7, 0.06);
    // (v17 self-review: a lumber barge here read as grey boxes floating on the water at the ending, removed)
    for (let x = 96; x < 166; x += 4.5) { cyl(b, M.woodD(), x, wl - 0.4, -18.4, 0.16, 0.16, 2.2, 8); cyl(b, M.woodD(), x + 1.6, wl - 0.4, 27, 0.16, 0.16, 2.2, 8); }
    schooner(205, 78, 9, 0.5); schooner(232, 62, 11, -0.3); schooner(190, 105, 8, 1.1); schooner(260, 95, 12, 0.2); schooner(176, 70, 7, 2.6);
    // v19: the ending crane (f1880-1960) passes over the south quay top (z < -30.5): bollards along the parapet, barrels, crates,
    // a tarp-covered cargo pile and rope coils, all standing on the quay at D0
    { const G = D0 + 0.01, rope = lam("cRope3", () => ({ color: "#b89a6a" })), tarp = lam("cTarp", () => ({ color: "#6a6a4a" }));
      for (let x = 94; x <= 118; x += 4) { cyl(b, M.iron(), x, G, -31.0, 0.16, 0.2, 0.55, 10); cyl(b, M.iron(), x, G + 0.55, -31.0, 0.22, 0.22, 0.08, 10); }
      for (const [x, z] of [[97.2, -32.2], [97.9, -32.6], [97.5, -33.3], [109.4, -32.4], [110.1, -32.1]] as const) { cyl(b, lam("cBarrel", () => ({ color: "#9a6a3a" })), x, G, z, 0.3, 0.3, 0.85, 14); for (const y of [0.15, 0.68]) cyl(b, M.iron(), x, G + y, z, 0.31, 0.31, 0.05, 14); }
      for (const [x, z, s2, y0] of [[101.0, -32.4, 0.4, 0], [101.9, -32.6, 0.35, 0], [101.4, -32.5, 0.3, 0.8]] as const) { box(b, M.wood(), x - s2, G + y0, z - s2, x + s2, G + y0 + s2 * 2, z + s2); for (const d of [-0.55, 0.55]) box(b, M.woodD(), x - s2 - 0.01, G + y0 + 0.05, z + d * s2 - 0.03, x + s2 + 0.01, G + y0 + s2 * 2 - 0.05, z + d * s2 + 0.03); }
      box(b, tarp, 104.4, G, -33.6, 107.0, G + 0.9, -31.9); for (const x of [104.9, 105.7, 106.5]) bar(b, rope, V(x, G + 0.92, -33.62), V(x, G + 0.92, -31.88), 0.02);
      for (const [x, z] of [[99.4, -31.9], [112.5, -32.0], [115.6, -32.2]] as const) for (let k = 0; k < 4; k++) { const t2 = new THREE.TorusGeometry(0.3 - k * 0.05, 0.035, 6, 20); t2.rotateX(Math.PI / 2); t2.translate(x, G + 0.035 + k * 0.06, z); b.add(t2, rope); }
    }
    // lighthouse on a stone crib out in the lake
    box(b, lam("cCribStone", () => ({ color: "#8a8478" })), 236, wl - 0.5, 118, 244, D0 + 1.2, 126);
    cyl(b, M.white(), 240, D0 + 1.2, 122, 1.5, 1.1, 9, 16); for (const y of [3, 6]) cyl(b, M.red(), 240, D0 + 1.2 + y, 122, 1.4 - y * 0.04, 1.38 - y * 0.04, 0.8, 16);
    cyl(b, M.iron(), 240, D0 + 10.2, 122, 1.3, 1.3, 0.2, 16); box(b, glow("lighthouse", 3.2, 2.6, 1.4), 239.4, D0 + 10.4, 121.4, 240.6, D0 + 11.4, 122.6);
    { const cone = new THREE.ConeGeometry(1.1, 1.2, 16); cone.translate(240, D0 + 12.0, 122); b.add(cone, M.red()); }
    // v19 shore close-up dressing (take 15 orbits round SHORE; her glass sits screen-left at x -0.26). Props start screen-right
    // of her (x >= 0.1 at f1782) and drift right, or start off-frame left and stay left of x -0.9: never behind the glass (rule 59)
    { const G = D0 + 0.03, rope2 = lam("cRope2", () => ({ color: "#b89a6a" }));
      const hull = new THREE.SphereGeometry(1, 16, 8, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2); hull.scale(1.9, 0.5, 0.7); hull.rotateY(-0.918); hull.translate(163.66, G + 0.48, 46.68); b.add(hull, lam("cRowboat", () => ({ color: "#3f6a8a" })));
      { const rim = new THREE.TorusGeometry(1, 0.05, 6, 28); rim.rotateX(Math.PI / 2); rim.scale(1.9, 1, 0.7); rim.rotateY(-0.918); rim.translate(163.66, G + 0.5, 46.68); b.add(rim, lam("cHullT", () => ({ color: "#d9c79a" }))); }
      bar(b, M.woodD(), V(163.2, G + 0.5, 46.0), V(164.4, G + 0.62, 47.6), 0.035);
      // net drying rack: two posts, a rail and a hanging net with a drawn mesh
      const A = [165.84, 48.8], B2 = [163.7, 50.44];
      for (const [x, z] of [A, B2]) pole(b, M.woodD(), V(x, G, z), V(x, G + 2.2, z), 0.06);
      bar(b, M.woodD(), V(A[0], G + 2.15, A[1]), V(B2[0], G + 2.15, B2[1]), 0.04);
      { const net = new THREE.PlaneGeometry(2.5, 1.7); net.rotateY(-Math.atan2(B2[1] - A[1], B2[0] - A[0])); net.translate((A[0] + B2[0]) / 2, G + 1.3, (A[1] + B2[1]) / 2);
        b.add(net, lam("cNet", () => ({ map: ctex("cNetT", 256, 160, (g) => { g.clearRect(0, 0, 256, 160); g.strokeStyle = "#3a2e22"; g.lineWidth = 2.5; for (let x = -160; x < 256; x += 14) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x + 160, 160); g.stroke(); g.beginPath(); g.moveTo(x + 160, 0); g.lineTo(x, 160); g.stroke(); } g.lineWidth = 5; g.strokeRect(2, 2, 252, 156); for (let x = 20; x < 256; x += 40) { g.fillStyle = "#c9a24a"; g.beginPath(); g.arc(x, 152, 6, 0, 6.28); g.fill(); } }), transparent: true, alphaTest: 0.4, side: THREE.DoubleSide }))); }
      // a crate with two fish baskets beside it
      box(b, M.wood(), 161.9, G, 43.6, 162.65, G + 0.6, 44.35); for (const d of [0.15, 0.55]) box(b, M.woodD(), 161.89, G + 0.05, 43.6 + d * 0.75, 162.66, G + 0.55, 43.66 + d * 0.75);
      for (const [x, z] of [[162.0, 44.9], [162.5, 45.3]] as const) { cyl(b, lam("cBasket", () => ({ color: "#b08a50" })), x, G, z, 0.3, 0.24, 0.42, 12); for (const y of [0.12, 0.28]) cyl(b, lam("cBasketB", () => ({ color: "#6a5030" })), x, G + y, z, 0.29 - y * 0.12, 0.29 - y * 0.12, 0.03, 12); }
      // off-frame left at the start: a rope coil and an anchor
      for (let k = 0; k < 4; k++) { const t2 = new THREE.TorusGeometry(0.24 - k * 0.04, 0.03, 6, 20); t2.rotateX(Math.PI / 2); t2.translate(168.8, G + 0.03 + k * 0.05, 41.0); b.add(t2, rope2); }
      const ax = 169.7, az = 41.8; bar(b, M.iron(), V(ax, G + 0.05, az), V(ax, G + 0.9, az), 0.04); bar(b, M.iron(), V(ax - 0.4, G + 0.25, az), V(ax + 0.4, G + 0.25, az), 0.035);
      bar(b, M.iron(), V(ax - 0.5, G + 0.45, az), V(ax - 0.3, G + 0.08, az), 0.035); bar(b, M.iron(), V(ax + 0.5, G + 0.45, az), V(ax + 0.3, G + 0.08, az), 0.035);
    }
    // buoys and mooring posts
    for (let k = 0; k < 14; k++) { const x = 176 + r() * 70, z = 55 + r() * 70; if (Math.hypot(x - 240, z - 122) < 8) continue; k % 3 ? cyl(b, M.red(), x, wl - 0.1, z, 0.3, 0.12, 0.7, 10) : cyl(b, M.woodD(), x, wl - 0.3, z, 0.12, 0.12, 1.6, 8); }
  });
  // v17 (owner Nov 12: close-ups need more drawn objects behind the heads): the 1854 street behind the doctor gets a public
  // water pump with its trough (the cholera story's own prop), barrels, crates, a hand cart and a hitching rail, all on the ground
  grp(root, (b) => {
    const [dx, , dz] = DOC, G = D0 + 0.01, pumpM = lam("cPumpG", () => ({ color: "#3f5a4a" }));
    const px = dx + 1.5, pz = dz + 2.6; // behind his left shoulder (screen left), clear of the raised glass on the right
    box(b, M.woodD(), px - 0.25, G, pz - 0.25, px + 0.25, G + 0.12, pz + 0.25);
    cyl(b, pumpM, px, G + 0.12, pz, 0.13, 0.11, 1.25, 12); cyl(b, pumpM, px, G + 1.37, pz, 0.15, 0.15, 0.08, 12); { const c = new THREE.SphereGeometry(0.1, 10, 8); c.translate(px, G + 1.5, pz); b.add(c, pumpM); }
    bar(b, pumpM, V(px, G + 0.95, pz - 0.05), V(px, G + 0.85, pz - 0.45), 0.04); bar(b, M.iron(), V(px, G + 1.3, pz + 0.05), V(px - 0.2, G + 1.55, pz + 0.55), 0.025);
    // v19: trough moved to the pump's far side (screen right, hidden behind the doctor in the close-up) so the woman waiting
    // at the pump (cast take 5) stands clear of it; a pail sits under the spout
    box(b, M.wood(), px - 1.35, G, pz - 0.25, px - 0.35, G + 0.4, pz + 0.15); box(b, lam("cTroughW", () => ({ color: "#3a4a6a" })), px - 1.29, G + 0.3, pz - 0.2, px - 0.41, G + 0.38, pz + 0.1);
    cyl(b, M.steel(), px, G, pz - 0.42, 0.12, 0.15, 0.28, 12);
    for (const [bx, bz] of [[dx + 3.4, dz + 1.3], [dx + 3.9, dz + 1.6], [dx - 2.2, dz + 1.5]] as const) { cyl(b, lam("cBarrel", () => ({ color: "#9a6a3a" })), bx, G, bz, 0.26, 0.26, 0.7, 14); for (const y of [0.12, 0.55]) cyl(b, M.iron(), bx, G + y, bz, 0.27, 0.27, 0.05, 14); }
    for (const [cx, cz, s2] of [[dx - 3.1, dz + 1.2, 0.3], [dx - 3.0, dz + 1.25, 0.22]] as const) box(b, M.wood(), cx - s2, G + (s2 < 0.25 ? 0.6 : 0), cz - s2, cx + s2, G + (s2 < 0.25 ? 0.6 : 0) + s2 * 2, cz + s2);
    // hand cart with two big wheels, tipped on its legs
    const hx = dx + 5.0, hz = dz + 1.9;
    box(b, M.wood(), hx - 0.7, G + 0.55, hz - 0.45, hx + 0.7, G + 0.62, hz + 0.45); for (const sz of [-0.45, 0.45]) box(b, M.wood(), hx - 0.7, G + 0.62, hz + sz - 0.03, hx + 0.7, G + 0.85, hz + sz + 0.03);
    for (const sz of [-0.52, 0.52]) { const w = new THREE.TorusGeometry(0.45, 0.04, 8, 22); w.translate(hx, G + 0.45, hz + sz); b.add(w, M.woodD()); for (let k = 0; k < 4; k++) { const a = (k / 4) * Math.PI; bar(b, M.woodD(), V(hx + Math.cos(a) * 0.43, G + 0.45 + Math.sin(a) * 0.43, hz + sz), V(hx - Math.cos(a) * 0.43, G + 0.45 - Math.sin(a) * 0.43, hz + sz), 0.015); } }
    bar(b, M.wood(), V(hx - 0.7, G + 0.6, hz - 0.3), V(hx - 1.6, G + 0.05, hz - 0.3), 0.03); bar(b, M.wood(), V(hx - 0.7, G + 0.6, hz + 0.3), V(hx - 1.6, G + 0.05, hz + 0.3), 0.03);
    // (v18 self-review: a hitching rail read as a bar through the doctor's waist, removed)
    // (v19 self-review: barrels + crates tried in the yard beside the doctor touched his raised glass from below, rule 59: removed)
  });
  void TRE;
  setSight([]);
  return S;
};
