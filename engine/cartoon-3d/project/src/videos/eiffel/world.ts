// Three places in one three.js scene, toggled per shot: London (the bank town from the bridge short + a dome on the
// skyline, river), the Arizona desert (sand, mesas, saguaros, a dry channel that is dug and flooded, a lake town,
// a road with trucks) and the open sea (ship). The stone arch bridge (5 arches, 4 piers) is shared by London and
// the desert and is built from 9 pieces so it can be taken apart and put back "piece by piece".
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { staticFile } from "remotion";
import { Batch, boxGeo, V, lam, buildTown, Kit, Ray, house, prop, setSight } from "./build";
import { bed, ctex, stoneHD, cobbleHD, grassHD, waterNear, waterFar, cloudHD, rng } from "./paint";
import { Pen } from "./toon";
import { LIGHTS, LOOK, LightPreset } from "./lights";
import { TONE, CHAR, LFB, twoTone, untone } from "./shade";
import { NOINK } from "./ink";
import { Pool, Actor, Fx, stage } from "./cast";
import { FPS, D0, HW, SHOTS, PIECES, SPANS, pieceRange, PILE, ROAD_Z, TOWN, camAt, worldAt, truckX, shipX, V3, ShotDef, TOWER, T_H, P1, P2, PTOP, legOff, PAINT } from "./story";

const KENNEY = ["tree_oak", "tree_default", "tree_detailed", "tree_fat", "tree_cone", "tree-high-round", "tree", "plant_bushLarge", "plant_bushDetailed",
  "plant_bush", "hedge", "flower_redA", "flower_yellowA", "flower_purpleA", "grass_large", "grass", "lily_large", "lantern", "cart", "stall-red",
  "stall-green", "stall-bench", "banner-red", "banner-green", "windmill", "canoe"];
let kitP: Promise<Kit> | null = null;
export const loadKit = () => {
  if (!kitP) {
    const loader = new GLTFLoader();
    kitP = Promise.all(KENNEY.map((n) => loader.loadAsync(staticFile(`bridge/kenney/${n}.glb`)).then((g) => [n, g.scene] as const).catch(() => [n, null] as const)))
      .then((list) => Object.fromEntries(list.filter((e) => e[1]).map(([n, s]) => [n, s!])) as Kit);
  }
  return kitP;
};

// ---------------- painted textures (new) ----------------
const sandTex = () => { const t = ctex("sandHD", 1024, 1024, (g, r) => {
  g.fillStyle = "#e9c88f"; g.fillRect(0, 0, 1024, 1024);
  for (let i = 0; i < 70; i++) { const x = r() * 1024, y = r() * 1024, rad = 40 + r() * 140; const gr = g.createRadialGradient(x, y, 0, x, y, rad);
    const c = r() < 0.5 ? "214,170,112" : "247,222,170"; gr.addColorStop(0, `rgba(${c},0.35)`); gr.addColorStop(1, `rgba(${c},0)`); g.fillStyle = gr; g.fillRect(x - rad, y - rad, rad * 2, rad * 2); }
  for (let i = 0; i < 26; i++) { // wind ripples
    const y = r() * 1024, x = r() * 1024, w = 80 + r() * 200; g.strokeStyle = "rgba(190,140,90,0.25)"; g.lineWidth = 3; g.beginPath();
    for (let k = 0; k <= 12; k++) { const xx = x + (w * k) / 12; g.lineTo(xx, y + 6 * Math.sin(k * 0.9)); } g.stroke(); }
  for (let i = 0; i < 1800; i++) { g.fillStyle = r() < 0.5 ? "rgba(150,105,70,0.35)" : "rgba(255,245,220,0.45)"; g.beginPath(); g.arc(r() * 1024, r() * 1024, 1 + r() * 2.2, 0, 7); g.fill(); }
}); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t; };
const rockTex = () => { const t = ctex("rockBands", 512, 512, (g, r) => {
  const cols = ["#c97f52", "#d9966a", "#b8693f", "#e0a878", "#c4744a", "#d38c5c"];
  let y = 0; while (y < 512) { const h = 14 + r() * 46; g.fillStyle = cols[Math.floor(r() * cols.length)]; g.fillRect(0, y, 512, h + 1); y += h; }
  for (let i = 0; i < 900; i++) { g.fillStyle = r() < 0.5 ? "rgba(120,60,30,0.25)" : "rgba(255,220,180,0.25)"; g.fillRect(r() * 512, r() * 512, 2 + r() * 6, 1 + r() * 2); }
}); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t; };
const roadTex = () => { const t = ctex("roadHD", 512, 512, (g, r) => {
  g.fillStyle = "#5d5a60"; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 2500; i++) { g.fillStyle = r() < 0.5 ? "rgba(40,38,44,0.35)" : "rgba(150,146,150,0.3)"; g.fillRect(r() * 512, r() * 512, 2, 2); }
  g.fillStyle = "#efe6c8"; g.fillRect(250, 0, 12, 200);
}); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t; };
/** desert road runs along x (u): dashed centre line along u at v = 0.5, solid cream edge lines (owner r3: "road half marked") */
const inTown = (x: number, z: number) => x > TOWN.x - 52 && x < 176 && Math.abs(z - ROAD_Z) < 46;
const roadTexX = () => { const t = ctex("roadHDx", 512, 512, (g, r) => {
  g.fillStyle = "#5d5a60"; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 2500; i++) { g.fillStyle = r() < 0.5 ? "rgba(40,38,44,0.35)" : "rgba(150,146,150,0.3)"; g.fillRect(r() * 512, r() * 512, 2, 2); }
  g.fillStyle = "#efe6c8"; g.fillRect(0, 249, 300, 14);
  g.fillStyle = "#e8e2d0"; g.fillRect(0, 30, 512, 9); g.fillRect(0, 473, 512, 9);
}); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t; };
const plainTex = (name: string, base: string, dots: string[]) => { const t = ctex(name, 256, 256, (g, r) => {
  g.fillStyle = base; g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 900; i++) { g.fillStyle = dots[i % dots.length]; g.fillRect(r() * 256, r() * 256, 2, 2); }
  g.fillStyle = "rgba(60,58,62,0.35)"; g.fillRect(0, 0, 256, 3); g.fillRect(0, 0, 3, 256); // slab joints
}); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t; };
export const numTex = (n: number) => ctex("num" + n, 512, 256, (g, r) => {
  const cols = ["#d6c4a8", "#cbb89c", "#decfb5", "#c2ae91"];
  g.fillStyle = cols[n % 4]; g.fillRect(0, 0, 512, 256);
  for (let i = 0; i < 300; i++) { g.fillStyle = r() < 0.6 ? "rgba(95,82,72,0.3)" : "rgba(255,255,255,0.3)"; g.beginPath(); g.arc(r() * 512, r() * 256, 1 + r() * 2, 0, 7); g.fill(); }
  g.fillStyle = "rgba(70,55,45,0.25)"; g.fillRect(0, 244, 512, 12); g.fillRect(500, 0, 12, 256);
  g.font = "bold 120px Arial, sans-serif"; g.textAlign = "center"; g.textBaseline = "middle";
  g.fillStyle = "#f7f5ee"; g.fillText(String(n), 256 + (r() - 0.5) * 20, 132);
  g.strokeStyle = "rgba(240,240,232,0.5)"; g.lineWidth = 3; g.strokeText(String(n), 256, 132);
});
const NUMS = [1047, 2312, 318, 4021, 776, 1590, 2864, 3305, 912, 4410, 128, 2071];

const discTex = () => ctex("sunDisc", 128, 128, (g) => {
  const gr = g.createRadialGradient(64, 64, 58, 64, 64, 64); gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(1, "rgba(255,255,255,0)");
  g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
});
const haloTex = () => ctex("sunHalo", 256, 256, (g) => {
  const im = g.createImageData(256, 256);
  for (let y = 0; y < 256; y++) for (let x = 0; x < 256; x++) {
    const u = Math.hypot(x - 127.5, y - 127.5) / 128;
    const a = (0.55 * Math.exp(-((u / 0.25) ** 2)) + 0.35 * Math.exp(-((u / 0.6) ** 2))) * (1 - Math.min(1, Math.max(0, (u - 0.8) / 0.2)));
    const i = (y * 256 + x) * 4; im.data[i] = im.data[i + 1] = im.data[i + 2] = 255; im.data[i + 3] = Math.round(255 * Math.min(1, a));
  }
  g.putImageData(im, 0, 0);
});
const smokeTex = () => ctex("smoke", 256, 256, (g) => {
  const p = new Pen(g);
  for (const [x, y, r, c] of [[90, 150, 60, "#8f8d96"], [150, 120, 70, "#a3a1aa"], [170, 165, 55, "#8f8d96"], [120, 100, 50, "#b4b2ba"]] as const) p.ell(x, y, r, r * 0.85, c, 0);
});

const sightLines = (place: string): Ray[] => {
  const out: Ray[] = [];
  for (const s of SHOTS) {
    if (s.place !== place) continue;
    for (let f = s.a - 8; f < s.b + 8; f += 2) {
      const c = camAt(s.id, Math.max(0, f)), o = V(...c.pos), look = V(...c.look);
      const fw = look.clone().sub(o), len = fw.length();
      fw.normalize();
      const rt = fw.clone().cross(V(0, 1, 0)).normalize(), up = rt.clone().cross(fw);
      const ty = Math.tan((c.fov * Math.PI) / 360), tx = ty * (9 / 16);
      for (const [sx, sy] of [[0, 0], [-0.6, 0], [0.6, 0], [0, 0.6], [0, -0.4]])
        out.push({ o, d: fw.clone().addScaledVector(rt, sx * tx).addScaledVector(up, sy * ty), len, core: sx === 0 && sy === 0 });
    }
  }
  return out;
};

/** horizontal quad facing up at height y covering x0..x1, z0..z1, uv in tiles of `tile` m */
function quadY(x0: number, x1: number, z0: number, z1: number, y: number, tile: number) {
  const g = new THREE.BufferGeometry(), u = (x1 - x0) / tile, v = (z1 - z0) / tile;
  g.setAttribute("position", new THREE.Float32BufferAttribute([x0, y, z1, x1, y, z1, x1, y, z0, x0, y, z1, x1, y, z0, x0, y, z0], 3));
  g.setAttribute("normal", new THREE.Float32BufferAttribute(Array(6).fill([0, 1, 0]).flat(), 3));
  g.setAttribute("uv", new THREE.Float32BufferAttribute([0, 0, u, 0, u, v, 0, 0, u, v, 0, v], 2));
  return g;
}
/** vertical wall along x at z from y0 to y1 facing +z (dir 1) or -z (dir -1) */
function wallZ(x0: number, x1: number, z: number, y0: number, y1: number, dir: number) {
  const g = new THREE.BufferGeometry(), a = dir > 0 ? x0 : x1, b = dir > 0 ? x1 : x0;
  g.setAttribute("position", new THREE.Float32BufferAttribute([a, y0, z, b, y0, z, b, y1, z, a, y0, z, b, y1, z, a, y1, z], 3));
  g.setAttribute("normal", new THREE.Float32BufferAttribute(Array(6).fill([0, 0, dir]).flat(), 3));
  const u = Math.abs(x1 - x0) / 4, v = (y1 - y0) / 4;
  g.setAttribute("uv", new THREE.Float32BufferAttribute([0, 0, u, 0, u, v, 0, 0, u, v, 0, v], 2));
  return g;
}
const scaleUV = (g: THREE.BufferGeometry, k: number) => { const uv = g.attributes.uv as THREE.BufferAttribute; for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) * k, uv.getY(i) * k); return g; };

// ---------------- the stone arch bridge (Rennie's London Bridge, simplified: 5 arches, 4 piers) ----------------
const SPRING = 1.6;
const buildBridge = (kit: Kit): THREE.Group[] => {
  const stone = lam("bridgeStone", () => ({ map: stoneHD("towerHD") }));
  const cope = lam("bridgeCope", () => ({ map: stoneHD("copeHD") }));
  const road = lam("road", () => ({ map: roadTex() }));
  const pave = lam("pave", () => ({ map: cobbleHD() }));
  const groups: THREE.Group[] = [];
  for (let i = 0; i < PIECES; i++) {
    const b = new Batch(), [z0, z1] = pieceRange(i), grp = new THREE.Group();
    if (i % 2 === 0) {
      const yc = SPANS[i / 2][2], zm = (z0 + z1) / 2, half = (z1 - z0) / 2, rise = yc - SPRING;
      const sh = new THREE.Shape();
      sh.moveTo(z0, SPRING); sh.lineTo(z0, D0); sh.lineTo(z1, D0); sh.lineTo(z1, SPRING);
      for (let k = 1; k < 32; k++) { const a = (Math.PI * k) / 32; sh.lineTo(zm + half * Math.cos(a), SPRING + rise * Math.sin(a)); }
      sh.lineTo(z0, SPRING);
      const g = new THREE.ExtrudeGeometry(sh, { depth: 2 * HW, bevelEnabled: false, curveSegments: 32 });
      scaleUV(g, 0.25);
      g.applyMatrix4(new THREE.Matrix4().makeRotationY(-Math.PI / 2));
      g.translate(HW, 0, 0);
      b.add(g, stone);
      // the spandrel runs down into the water at both ends (abutments are part of the end pieces)
      if (i === 0) b.add(boxGeo(V(-HW, -0.6, z0 - 0.4), V(HW, SPRING + 0.01, z0 + 0.6), 4), stone);
      if (i === PIECES - 1) b.add(boxGeo(V(-HW, -0.6, z1 - 0.6), V(HW, SPRING + 0.01, z1 + 0.4), 4), stone);
    } else {
      const zc = (z0 + z1) / 2;
      b.add(boxGeo(V(-HW, -0.6, z0), V(HW, D0, z1), 4, false, 0.004), stone); // r3: end caps inset
      for (const s of [-1, 1]) {
        const cw = new THREE.BoxGeometry(1.697, SPRING + 1.2, 1.697); cw.rotateY(Math.PI / 4); scaleUV(cw, 0.4);
        b.add(cw, stone, new THREE.Matrix4().makeTranslation(s * HW, (SPRING + 1.2) / 2 - 0.6, zc));
        const cap = new THREE.ConeGeometry(1.2, 1.1, 4); cap.rotateY(0);
        b.add(cap, cope, new THREE.Matrix4().makeTranslation(s * HW, SPRING + 0.6 + 0.55, zc));
        // a pilaster up the face over each pier
        b.add(boxGeo(V(s > 0 ? HW : -HW - 0.35, SPRING + 1.1, z0 + 0.3), V(s > 0 ? HW + 0.35 : -HW, D0 - 0.35, z1 - 0.3), 4), cope);
      }
    }
    // deck: road, raised pavements, parapets with coping, string course under the parapet
    // r3: deck boxes get their z end caps inset 4 mm: at a seam between pieces the caps used to win the depth test on
    // edge pixels, and their sideways normals flashed as dotted ink lines while the camera moved
    const za = z0, zb = z1;
    b.add(quadY(-4.2, 4.2, za, zb, D0 + 0.005, 4), road);
    for (const s of [-1, 1]) {
      const xa = s < 0 ? -6.1 : 4.2, xb = s < 0 ? -4.2 : 6.1;
      b.add(boxGeo(V(xa, D0, za), V(xb, D0 + 0.14, zb), 4, false, 0.004), pave);
      const pa = s < 0 ? -HW : 6.1, pb = s < 0 ? -6.1 : HW;
      b.add(boxGeo(V(pa, D0, za), V(pb, D0 + 1.05, zb), 4, false, 0.004), stone);
      b.add(boxGeo(V(pa - 0.08, D0 + 1.05, za), V(pb + 0.08, D0 + 1.2, zb), 4, false, 0.004), cope);
      b.add(boxGeo(V(s < 0 ? -HW - 0.18 : HW, D0 - 0.4, za), V(s < 0 ? -HW : HW + 0.18, D0 - 0.15, zb), 4, false, 0.004), cope);
      if (i % 2 === 1) prop(b, kit, "lantern", s * 5.9, D0 + 1.2, (z0 + z1) / 2, 2.6);
    }
    b.build(grp);
    groups.push(grp);
  }
  return groups;
};

// ---------------- desert pieces ----------------
const cactus = (b: Batch, x: number, z: number, h: number, seed: number) => {
  const m = lam("cactus", () => ({ color: "#5f9a4c" })), r = rng(seed);
  const trunk = new THREE.CylinderGeometry(0.32 * h / 5, 0.36 * h / 5, h, 12); trunk.translate(0, h / 2, 0);
  const top = new THREE.SphereGeometry(0.32 * h / 5, 12, 8, 0, Math.PI * 2, 0, Math.PI / 2); top.translate(0, h, 0);
  b.add(trunk, m, new THREE.Matrix4().makeTranslation(x, D0, z)); b.add(top, m, new THREE.Matrix4().makeTranslation(x, D0, z));
  const arms = 1 + Math.floor(r() * 2);
  for (let k = 0; k < arms; k++) {
    const s = k ? -1 : 1, ay = h * (0.35 + 0.2 * r()), ah = h * (0.25 + 0.15 * r()), rad = 0.22 * h / 5, out = 0.9 * h / 5, yaw = r() * 3;
    const m4 = new THREE.Matrix4().makeRotationY(yaw).setPosition(x, D0, z);
    const hor = new THREE.CylinderGeometry(rad, rad, out, 10); hor.rotateZ(Math.PI / 2); hor.translate(s * out / 2, ay, 0);
    const ver = new THREE.CylinderGeometry(rad, rad, ah, 10); ver.translate(s * out, ay + ah / 2, 0);
    const cap = new THREE.SphereGeometry(rad, 10, 6, 0, Math.PI * 2, 0, Math.PI / 2); cap.translate(s * out, ay + ah, 0);
    const elb = new THREE.SphereGeometry(rad, 10, 8); elb.translate(s * out, ay, 0);
    for (const g of [hor, ver, cap, elb]) b.add(g, m, m4);
  }
};
const mesa = (b: Batch, x: number, z: number, w: number, h: number, d: number, yaw: number) => {
  const sh = new THREE.Shape(); sh.moveTo(-w / 2, 0); sh.lineTo(-w / 2 + h * 0.6, h * 0.55); sh.lineTo(-w / 2 + h * 0.7, h); sh.lineTo(w / 2 - h * 0.7, h); sh.lineTo(w / 2 - h * 0.5, h * 0.6); sh.lineTo(w / 2, 0); sh.lineTo(-w / 2, 0);
  const g = new THREE.ExtrudeGeometry(sh, { depth: d, bevelEnabled: false }); g.translate(0, 0, -d / 2); scaleUV(g, 1 / 60);
  b.add(g, lam("mesa", () => ({ map: rockTex() })), new THREE.Matrix4().makeRotationY(yaw).setPosition(x, D0 - 2, z));
};

// ---------------- ship + trucks ----------------
const buildShip = () => {
  const grp = new THREE.Group(), b = new Batch();
  const hullM = lam("hull", () => ({ color: "#2f3b55" })), redM = lam("hullRed", () => ({ color: "#b8463c" })), white = lam("shipWhite", () => ({ color: "#f1ebdf" }));
  const deckM = lam("shipDeck", () => ({ color: "#a8724a" })), funM = lam("funnel", () => ({ color: "#d0533f" })), black = lam("black", () => ({ color: "#2a2730" }));
  const sh = new THREE.Shape();
  sh.moveTo(-22, -4.5); sh.lineTo(12, -4.5); sh.quadraticCurveTo(20, -4.2, 24, 0); sh.quadraticCurveTo(20, 4.2, 12, 4.5); sh.lineTo(-22, 4.5); sh.quadraticCurveTo(-24, 0, -22, -4.5);
  const hull = new THREE.ExtrudeGeometry(sh, { depth: 4.2, bevelEnabled: false, curveSegments: 16 }); hull.rotateX(-Math.PI / 2); hull.translate(0, 0.0, 0);
  b.add(hull, hullM);
  const band = new THREE.ExtrudeGeometry(sh, { depth: 0.9, bevelEnabled: false, curveSegments: 16 }); band.rotateX(-Math.PI / 2); band.scale(1.005, 1, 1.01); band.translate(0, -0.6, 0);
  b.add(band, redM);
  const deck = new THREE.ShapeGeometry(sh, 16); deck.rotateX(-Math.PI / 2); deck.translate(0, 4.21, 0);
  b.add(deck, deckM);
  b.add(boxGeo(V(-21, 4.2, -4), V(-12, 8.6, 4)), white);
  b.add(boxGeo(V(-19.5, 8.6, -3.2), V(-13.5, 11, 3.2)), white);
  for (let k = 0; k < 6; k++) b.add(boxGeo(V(-12.02, 6.6, -3.4 + k * 1.3), V(-11.98, 7.4, -2.8 + k * 1.3)), black);
  const fun = new THREE.CylinderGeometry(1.2, 1.35, 4.2, 18); fun.translate(-17, 13.1, 0); b.add(fun, funM);
  const top = new THREE.CylinderGeometry(1.22, 1.22, 0.8, 18); top.translate(-17, 15.6, 0); b.add(top, black);
  for (const x of [16, -4]) { const mast = new THREE.CylinderGeometry(0.12, 0.16, 10, 8); mast.translate(x, 9.2, 0); b.add(mast, black); }
  b.build(grp);
  // cargo: numbered stone blocks
  const cb = new Batch();
  let k = 0;
  for (let x = -9; x < 13; x += 1.35) for (let z = -3.2; z <= 3.2; z += 1.6) for (let y = 0; y < 2; y++) {
    const n = NUMS[k++ % NUMS.length];
    cb.add(boxGeo(V(x, 4.2 + y * 0.66, z - 0.62), V(x + 1.25, 4.2 + y * 0.66 + 0.64, z + 0.62)), lam("num" + n, () => ({ map: numTex(n) })));
  }
  cb.build(grp);
  return grp;
};
const buildTruck = (col: string, k: number) => {
  const grp = new THREE.Group(), b = new Batch(), body = lam("truck" + col, () => ({ color: col })), dark = lam("tyre", () => ({ color: "#2b2830" }));
  const glass = lam("glass", () => ({ color: "#9cc4e0" })), bedM = lam("bedWood", () => ({ color: "#8a6a4a" }));
  b.add(boxGeo(V(5.0, 0.7, -1.25), V(7.3, 3.1, 1.25)), body);
  b.add(boxGeo(V(7.3, 0.7, -1.25), V(8.1, 1.9, 1.25)), body);
  b.add(boxGeo(V(6.4, 2.0, -1.1), V(7.32, 2.9, 1.1)), glass);
  b.add(boxGeo(V(-3.2, 1.0, -1.3), V(4.9, 1.4, 1.3)), bedM);
  for (const x of [-2.2, -0.6, 6.4]) for (const s of [-1, 1]) { const w = new THREE.CylinderGeometry(0.55, 0.55, 0.4, 16); w.rotateX(Math.PI / 2); w.translate(x, 0.55, s * 1.15); b.add(w, dark); }
  for (let i = 0; i < 6; i++) { const n = NUMS[(i + k * 3) % NUMS.length], x = -2.9 + (i % 3) * 2.5, z = i < 3 ? -0.6 : 0.6;
    b.add(boxGeo(V(x, 1.4, z - 0.55), V(x + 1.2, 2.0, z + 0.55)), lam("num" + n, () => ({ map: numTex(n) }))); }
  b.build(grp);
  return grp;
};


// ---------------- the Eiffel Tower (1:2 scale, 150 m to the antenna tip) ----------------
/** painted wrought-iron lattice: bronze-brown with darker X bracing and cross struts, seams painted in (no alpha) */
const latticeTex = () => { const t = ctex("eiffelLat", 512, 512, (g, r) => {
  g.fillStyle = "#86644a"; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 1600; i++) { g.fillStyle = r() < 0.5 ? "rgba(60,40,30,0.25)" : "rgba(170,130,96,0.25)"; g.fillRect(r() * 512, r() * 512, 3, 3); }
  g.strokeStyle = "#4a3428"; g.lineCap = "square";
  g.lineWidth = 26; g.strokeRect(13, 13, 486, 486);
  g.lineWidth = 16; g.beginPath(); g.moveTo(20, 20); g.lineTo(492, 492); g.moveTo(492, 20); g.lineTo(20, 492); g.stroke();
  g.lineWidth = 12; g.beginPath(); g.moveTo(0, 256); g.lineTo(512, 256); g.stroke();
  g.strokeStyle = "rgba(200,160,120,0.45)"; g.lineWidth = 5;
  g.beginPath(); g.moveTo(36, 26); g.lineTo(492, 482); g.stroke();
}); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 16; return t; };
/** tapered square tube between two centres (four side faces, lattice UVs ~ 1 tile per 6 m) */
const frust = (c0: THREE.Vector3, w0: number, c1: THREE.Vector3, w1: number) => {
  const pos: number[] = [], nor: number[] = [], uv: number[] = [];
  const corners = (c: THREE.Vector3, w: number) => [[-w, -w], [w, -w], [w, w], [-w, w]].map(([x, z]) => new THREE.Vector3(c.x + x, c.y, c.z + z));
  const A = corners(c0, w0), B = corners(c1, w1), len = c0.distanceTo(c1);
  for (let i = 0; i < 4; i++) {
    const a0 = A[i], a1 = A[(i + 1) % 4], b0 = B[i], b1 = B[(i + 1) % 4];
    const n = new THREE.Vector3().subVectors(a1, a0).cross(new THREE.Vector3().subVectors(b0, a0)).normalize().multiplyScalar(-1);
    const wu = Math.max(1, Math.round((2 * w0) / 6)), wv = Math.max(1, Math.round(len / 6));
    for (const [v, u0, v0] of [[a0, 0, 0], [a1, wu, 0], [b1, wu, wv], [a0, 0, 0], [b1, wu, wv], [b0, 0, wv]] as const) { pos.push(v.x, v.y, v.z); nor.push(n.x, n.y, n.z); uv.push(u0, v0); }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute("normal", new THREE.Float32BufferAttribute(nor, 3)); g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2));
  return g;
};
const buildTower = (kit: Kit) => {
  void kit;
  const grp = new THREE.Group(), b = new Batch();
  const lat = lam("eiffelLat", () => ({ map: latticeTex() })), iron = lam("eiffelIron", () => ({ color: "#6e5240" })), deck = lam("eiffelDeck", () => ({ color: "#8a6a50" }));
  const cream = lam("eiffelCab", () => ({ color: "#e8dcc0" }));
  const [TX, , TZ] = TOWER, Y = (y: number) => D0 + y;
  const lw = (y: number) => 4.6 - 2.4 * Math.min(1, y / P2); // leg half width
  // four legs from the ground to the second floor, bent inward
  const steps = [0, 7, 14, 21, P1, 36, 44, 51, P2];
  for (const [sx, sz] of [[-1, -1], [1, -1], [1, 1], [-1, 1]]) {
    for (let i = 0; i + 1 < steps.length; i++) {
      const y0 = steps[i], y1 = steps[i + 1];
      b.add(frust(V(TX + sx * legOff(y0), Y(y0), TZ + sz * legOff(y0)), lw(y0), V(TX + sx * legOff(y1), Y(y1), TZ + sz * legOff(y1)), lw(y1)), lat);
    }
    b.add(boxGeo(V(TX + sx * legOff(0) - 5.4, D0, TZ + sz * legOff(0) - 5.4), V(TX + sx * legOff(0) + 5.4, D0 + 1.2, TZ + sz * legOff(0) + 5.4), 4), lam("eiffelPlinth", () => ({ map: stoneHD("copeHD") })));
  }
  // decorative arches between the feet, under the first floor
  for (let k = 0; k < 4; k++) {
    const R = legOff(0) - 4.2, arc = new THREE.TorusGeometry(R, 0.55, 8, 40, Math.PI);
    arc.scale(1, 0.62, 1);
    const m = new THREE.Matrix4().makeRotationY((k * Math.PI) / 2).multiply(new THREE.Matrix4().makeTranslation(0, P1 - 9.5 - 0.62 * R + 6.5, -legOff(10) + 0.5));
    b.add(arc, iron, new THREE.Matrix4().makeTranslation(TX, D0 + 2.6, TZ).multiply(m));
  }
  // first floor: deck + gallery band; second floor: deck + band
  const fl = (y: number, h: number, th: number, band: number) => {
    b.add(boxGeo(V(TX - h, Y(y) - th, TZ - h), V(TX + h, Y(y), TZ + h), 4, true), deck);
    b.add(frust(V(TX, Y(y) - th - 0.2, TZ), h + 0.35, V(TX, Y(y) + band, TZ), h + 0.35), lat);
  };
  fl(P1, legOff(P1) + lw(P1) + 1.2, 1.0, 1.25);
  fl(P2, legOff(P2) + lw(P2) + 0.6, 0.8, 1.1);
  // the shaft: second floor to the top, one tapering column
  const sh = [P2, 72, 88, 104, 120, PTOP];
  for (let i = 0; i + 1 < sh.length; i++) {
    const w0 = legOff(sh[i]) + lw(Math.min(sh[i], P2)) * (sh[i] <= P2 ? 1 : 0.4) + 0.6, w1 = Math.max(1.4, legOff(sh[i + 1]) + 1.2);
    b.add(frust(V(TX, Y(sh[i]), TZ), i ? Math.max(1.4, legOff(sh[i]) + 1.2) : w0, V(TX, Y(sh[i + 1]), TZ), w1), lat);
  }
  // top: walkable deck, cream cabin with windows, lantern, antenna mast
  b.add(boxGeo(V(TX - 4.4, Y(PTOP) - 0.5, TZ - 4.4), V(TX + 4.4, Y(PTOP) + 0.4, TZ + 4.4), 4, true), deck);
  b.add(frust(V(TX, Y(PTOP) + 0.4, TZ), 4.4, V(TX, Y(PTOP) + 1.4, TZ), 4.4), lat);
  b.add(boxGeo(V(TX - 1.8, Y(PTOP) + 0.4, TZ + 0.2), V(TX + 1.8, Y(PTOP) + 4.0, TZ + 3.8), 2), cream);
  b.add(boxGeo(V(TX - 2.1, Y(PTOP) + 4.0, TZ - 0.1), V(TX + 2.1, Y(PTOP) + 4.6, TZ + 4.1), 2), iron);
  const mast = new THREE.CylinderGeometry(0.25, 0.55, T_H - PTOP - 4.6, 10); mast.translate(TX, Y(PTOP) + 4.6 + (T_H - PTOP - 4.6) / 2, TZ + 2); b.add(mast, iron);
  // radio aerial wires from the top down to anchors in the Champ de Mars (thin, read as lines from afar)
  for (const ax of [-26, -9, 9, 26]) {
    const top = V(TX, Y(T_H - 2), TZ + 2), foot = V(TX + ax, D0 + 0.4, TZ + 160), d = foot.clone().sub(top), L = d.length();
    const w = new THREE.CylinderGeometry(0.09, 0.09, L, 5); w.translate(0, L / 2, 0);
    w.applyQuaternion(new THREE.Quaternion().setFromUnitVectors(V(0, 1, 0), d.clone().normalize())); w.translate(top.x, top.y, top.z);
    b.add(w, iron);
  }
  // painters' plank on the south-west leg (shot 13): plank + two ropes up into the lattice
  const pl = PAINT;
  b.add(boxGeo(V(pl[0] - 2.2, pl[1] - 0.12, pl[2] - 0.35), V(pl[0] + 2.2, pl[1], pl[2] + 0.35), 2), lam("plank", () => ({ color: "#a07a4a" })));
  for (const dx of [-2.0, 2.0]) { const rope = new THREE.CylinderGeometry(0.035, 0.035, 9, 5); rope.translate(pl[0] + dx, pl[1] + 4.5, pl[2]); b.add(rope, lam("rope", () => ({ color: "#d8c49a" }))); }
  b.build(grp);
  return grp;
};

export class World {
  root = new THREE.Group();
  private pool = new Pool();
  private actors: Actor[] = [];
  private fxs: Fx[] = [];
  private hemi: THREE.HemisphereLight; private sun: THREE.DirectionalLight;
  private sky: THREE.Mesh; private skyMat: THREE.ShaderMaterial;
  private fog = new THREE.Fog("#bccbec", 25, 420);
  private WU: Record<string, THREE.IUniform>;
  private sunDisc: THREE.Sprite; private sunHalo: THREE.Sprite;
  private sunCache = new Map<number, THREE.Vector3>();
  private cloudMaps: Record<"day" | "golden", THREE.Texture[]>;
  private clouds: THREE.Mesh[] = [];
  private london = new THREE.Group(); private desert = new THREE.Group(); private sea = new THREE.Group();
  private bridge = new THREE.Group(); private pieces: THREE.Group[];
  private water: THREE.Mesh; private fill: THREE.Mesh; private pile = new THREE.Group();
  private ship: THREE.Group; private trucks: THREE.Group[] = [];
  private smoke: { m: THREE.Mesh; mat: THREE.MeshLambertMaterial; top: V3; k: number }[] = [];
  private frustum = new THREE.Frustum();
  private m4 = new THREE.Matrix4(); private v = new THREE.Vector3(); private sph = new THREE.Sphere();

  constructor(kit: Kit) {
    const R = this.root;
    this.skyMat = new THREE.ShaderMaterial({
      uniforms: { c0: { value: new THREE.Color() }, c1: { value: new THREE.Color() }, c2: { value: new THREE.Color() },
        c3: { value: new THREE.Color() }, c4: { value: new THREE.Color() }, e: { value: new THREE.Vector4() } },
      vertexShader: "varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }",
      fragmentShader: `uniform vec3 c0, c1, c2, c3, c4; uniform vec4 e; varying vec3 vP;
        void main(){ float el = asin(clamp(normalize(vP).y, -1.0, 1.0));
          vec3 c = mix(c0, c1, smoothstep(0.0, e.x, el));
          c = mix(c, c2, smoothstep(e.x, e.y, el));
          c = mix(c, c3, smoothstep(e.y, e.z, el));
          c = mix(c, c4, smoothstep(e.z, e.w, el));
          gl_FragColor = vec4(c, 1.0); }`,
      side: THREE.BackSide, depthWrite: false, fog: false,
    });
    this.sky = new THREE.Mesh(new THREE.SphereGeometry(1100, 48, 24), this.skyMat);
    this.sky.renderOrder = -1; this.sky.frustumCulled = false; this.sky.layers.set(NOINK);
    R.add(this.sky);
    this.sunDisc = new THREE.Sprite(new THREE.SpriteMaterial({ map: discTex(), color: new THREE.Color(6.0, 4.4, 2.4), fog: false, depthWrite: false }));
    this.sunHalo = new THREE.Sprite(new THREE.SpriteMaterial({ map: haloTex(), color: new THREE.Color(1, 1, 1), fog: false, depthWrite: false, depthTest: true,
      transparent: true, blending: THREE.AdditiveBlending }));
    this.sunDisc.renderOrder = -0.5; this.sunHalo.renderOrder = 5;
    for (const m of [this.sunDisc, this.sunHalo]) { m.frustumCulled = false; m.layers.set(NOINK); R.add(m); }
    this.hemi = new THREE.HemisphereLight("#cfe6ff", "#6c5c8c", 1.1);
    this.sun = new THREE.DirectionalLight("#fff0d6", 2.6);
    this.sun.castShadow = true;
    this.sun.shadow.mapSize.set(4096, 4096);
    R.add(this.hemi, this.sun, this.sun.target);
    this.cloudMaps = { day: [0, 1, 2, 3].map((k) => cloudHD(k, LOOK.day.cloud)), golden: [0, 1, 2, 3].map((k) => cloudHD(k, LOOK.golden.cloud)) };
    for (let i = 0; i < 9; i++) {
      const a = (i / 9) * Math.PI * 2 + 0.3, d = 620 + (i % 3) * 60;
      const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: this.cloudMaps.day[i % 4], color: new THREE.Color(1.1, 1.1, 1.1), transparent: true, depthWrite: false, fog: false }));
      const w = 130 + (i % 4) * 30;
      m.position.set(Math.cos(a) * d, 120 + (i % 4) * 38, Math.sin(a) * d); m.scale.set(w, w / 2, 1);
      m.layers.set(NOINK);
      this.clouds.push(m); R.add(m);
    }
    R.add(this.london, this.desert, this.sea, this.bridge);

    // ---- London: grass banks, quays, embankment walls, river bed, the town ----
    {
      const b = new Batch();
      const grass = lam("grassHD", () => ({ map: grassHD() })), cob = lam("cobbleHD", () => ({ map: cobbleHD() }));
      const wall = lam("wallHD", () => ({ map: stoneHD("wallHD") })), cope = lam("copeHD", () => ({ map: stoneHD("copeHD") }));
      for (const s of [-1, 1]) {
        const zn = s * 30, zf = s * 900;
        b.add(s < 0 ? quadY(-900, 900, zf, -36.5, D0, 4) : quadY(-900, 900, 36.5, zf, D0, 4), grass);
        b.add(s < 0 ? quadY(-160, 160, -36.5, zn, D0 + 0.012, 4) : quadY(-160, 160, zn, 36.5, D0 + 0.012, 4), cob);
        b.add(s < 0 ? quadY(-6, 6, -170, -36.5, D0 + 0.012, 4) : quadY(-6, 6, 36.5, 170, D0 + 0.012, 4), cob);
        b.add(wallZ(-900, 900, zn, -0.6, D0, s < 0 ? 1 : -1), wall);
        for (const [x0, x1] of [[-600, -HW - 0.2], [HW + 0.2, 600]]) b.add(boxGeo(V(x0, D0, s < 0 ? -30.5 : 30), V(x1, D0 + 0.75, s < 0 ? -30 : 30.5), 2), cope);
      }
      b.add(quadY(-900, 900, -30, 30, -0.6, 8), lam("bed", () => ({ map: bed() })));
      // a domed cathedral on the far skyline
      const dome = lam("domeGold", () => ({ color: "#d9b34a" })), st = lam("towerstone", () => ({ map: stoneHD("tstoneHD") }));
      const dx = -125, dz = 300; // a gilded dome behind the Champ de Mars (reads as Les Invalides)
      b.add(boxGeo(V(dx - 30, D0, dz - 12), V(dx + 30, D0 + 22, dz + 12), 4), st);
      const drum = new THREE.CylinderGeometry(13, 13, 14, 32); drum.translate(dx, D0 + 29, dz); b.add(drum, st);
      const hemi = new THREE.SphereGeometry(13.5, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2); hemi.scale(1, 1.25, 1); hemi.translate(dx, D0 + 36, dz); b.add(hemi, dome);
      const lan = new THREE.CylinderGeometry(2, 2.4, 6, 12); lan.translate(dx, D0 + 55, dz); b.add(lan, st);
      const sp = new THREE.ConeGeometry(1.6, 5, 12); sp.translate(dx, D0 + 60.5, dz); b.add(sp, dome);
      for (const tx of [dx - 26, dx + 26]) { const t = new THREE.CylinderGeometry(3.2, 3.2, 34, 12); t.translate(tx, D0 + 17, dz - 10); b.add(t, st); const c = new THREE.ConeGeometry(3.6, 7, 12); c.translate(tx, D0 + 37.5, dz - 10); b.add(c, dome); }
      b.build(this.london);
      buildTown(this.london, kit, sightLines("london"));
      this.london.add(buildTower(kit));
      // numbered stones on the quay (shot 8)
      const pb = new Batch();
      let k = 0;
      // separate low pallets (2 stones wide, 2 high) in a stone yard with walkways, not one stepped wall
      const palletM = lam("pallet", () => ({ color: "#a8743f" }));
      for (const px of [-4.8, -1.6, 1.6, 4.8]) for (const pz of [0, -2.6]) {
        const bx = PILE[0] + px - 1.25, bz = PILE[2] + pz;
        pb.add(boxGeo(V(bx - 0.08, D0, bz - 0.68), V(bx + 2.58, D0 + 0.14, bz + 0.68)), palletM);
        for (let i = 0; i < 2; i++) for (let y = 0; y < (px === 4.8 && pz < 0 ? 1 : 2); y++) {
          const n = NUMS[k++ % NUMS.length];
          pb.add(boxGeo(V(bx + i * 1.26, D0 + 0.14 + y * 0.64, bz - 0.6), V(bx + i * 1.26 + 1.22, D0 + 0.14 + y * 0.64 + 0.62, bz + 0.6)), lam("num" + n, () => ({ map: numTex(n) })));
        }
      }
      pb.build(this.pile);
      this.london.add(this.pile);
      const smokeT = smokeTex();
      for (const [top, n] of [[[-22, D0 + 30.6, -77], 7], [[-80, D0 + 24.6, 93], 6]] as const)
        for (let i = 0; i < n; i++) {
          const mat = new THREE.MeshLambertMaterial({ map: smokeT, transparent: true, depthWrite: false });
          const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), mat);
          m.layers.set(NOINK);
          this.smoke.push({ m, mat, top: top as unknown as V3, k: i / n }); this.london.add(m);
        }
    }

    // ---- desert: sand, sandstone banks, the dry channel floor, mesas, saguaros, the lake town, a road ----
    {
      setSight(sightLines("desert"));
      const b = new Batch();
      const sand = lam("sand", () => ({ map: sandTex() })), rock = lam("rock", () => ({ map: rockTex() }));
      (sand.map as THREE.Texture).repeat.set(1, 1);
      for (const s of [-1, 1]) {
        b.add(s < 0 ? quadY(-900, 172, -900, -30, D0, 10) : quadY(-900, 172, 30, 900, D0, 10), sand);
        b.add(scaleUV(wallZ(-900, 172, s * 30, -0.6, D0, s < 0 ? 1 : -1), 0.25), rock);
      }
      b.add(quadY(172, 1500, -1500, 1500, -0.6, 10), sand); // lake bed
      for (const [z0, z1] of [[-900, -30], [30, 900]]) {
        const g = new THREE.BufferGeometry(); const x = 172;
        g.setAttribute("position", new THREE.Float32BufferAttribute([x, -0.6, z0, x, -0.6, z1, x, D0, z1, x, -0.6, z0, x, D0, z1, x, D0, z0], 3));
        g.setAttribute("normal", new THREE.Float32BufferAttribute(Array(6).fill([1, 0, 0]).flat(), 3));
        g.setAttribute("uv", new THREE.Float32BufferAttribute([0, 0, (z1 - z0) / 4, 0, (z1 - z0) / 4, 1.6, 0, 0, (z1 - z0) / 4, 1.6, 0, 1.6], 2));
        b.add(g, rock);
      }
      b.add(quadY(-900, 172, ROAD_Z - 3.5, ROAD_Z + 3.5, D0 + 0.02, 7), lam("roadDx", () => ({ map: roadTexX() })));
      const r = rng(5);
      ([[-480, -450, 260, 80, 120, 0.3], [-170, -620, 340, 95, 140, -0.2], [320, -580, 280, 75, 120, 0.5], [640, -190, 230, 66, 110, 1.2], [580, 400, 300, 90, 130, 0.8],
        [-580, 320, 280, 82, 120, -0.6], [-670, -60, 220, 70, 110, 1.5], [160, 640, 340, 86, 130, 0.1], [-320, 600, 260, 78, 120, 0.4]] as const)
        .forEach(([x, z, w, h, d, yaw]) => mesa(b, x, z, w, h, d, yaw));
      for (let i = 0; i < 90; i++) {
        const x = (r() - 0.5) * 360, z = (r() < 0.5 ? -1 : 1) * (36 + r() * 170);
        if (Math.abs(z - ROAD_Z) < 7 || inTown(x, z)) continue;
        const h = 3.5 + r() * 3.5;
        if (this.blocked(x, z, h)) continue;
        cactus(b, x, z, h, i * 13 + 1);
      }
      for (let i = 0; i < 40; i++) {
        const x = (r() - 0.5) * 300, z = (r() < 0.5 ? -1 : 1) * (34 + r() * 120);
        if (Math.abs(z - ROAD_Z) < 6 || inTown(x, z)) continue;
        prop(b, kit, r() < 0.5 ? "plant_bush" : "plant_bushDetailed", x, D0, z, 0.8 + r() * 0.6);
      }
      // the new lake town (r3 rebuild): a planned grid. Main road through the middle, two cross streets, sidewalks,
      // lawns, houses set back facing the street, trees only in yards. Nothing sits on a road or a sidewalk.
      {
        const SIDE = 2.2, X0 = TOWN.x - 48, X1 = 171, XS = [TOWN.x - 22, TOWN.x + 4]; // cross streets (run along z)
        const Z0 = ROAD_Z - 42, Z1 = ROAD_Z + 42;
        const lawn = lam("lawnHD", () => ({ map: grassHD() })), walk = lam("walkHD", () => ({ map: plainTex("walkHD", "#cfc6b4", ["rgba(120,112,100,0.25)", "rgba(255,255,255,0.25)"]) }));
        const roadZ = lam("roadZ", () => ({ map: roadTex() }));
        // lawns: one quad per block, between streets
        const xb = [X0, XS[0] - 3.5 - SIDE, XS[0] + 3.5 + SIDE, XS[1] - 3.5 - SIDE, XS[1] + 3.5 + SIDE, X1];
        for (let k = 0; k < 3; k++) for (const [za, zb] of [[Z0, ROAD_Z - 3.5 - SIDE], [ROAD_Z + 3.5 + SIDE, Z1]])
          b.add(quadY(xb[2 * k], xb[2 * k + 1], za, zb, D0 + 0.01, 4), lawn);
        // sidewalks along the main road and along both sides of each cross street
        for (const s2 of [-1, 1]) b.add(quadY(X0, X1, s2 < 0 ? ROAD_Z - 3.5 - SIDE : ROAD_Z + 3.5, s2 < 0 ? ROAD_Z - 3.5 : ROAD_Z + 3.5 + SIDE, D0 + 0.03, 2), walk);
        for (const xs of XS) {
          for (const [za, zb] of [[Z0, ROAD_Z - 3.5], [ROAD_Z + 3.5, Z1]]) b.add(quadY(xs - 3.5, xs + 3.5, za, zb, D0 + 0.025, 7), roadZ);
          for (const s2 of [-1, 1]) for (const [za, zb] of [[Z0, ROAD_Z - 3.5 - SIDE], [ROAD_Z + 3.5 + SIDE, Z1]])
            b.add(quadY(s2 < 0 ? xs - 3.5 - SIDE : xs + 3.5, s2 < 0 ? xs - 3.5 : xs + 3.5 + SIDE, za, zb, D0 + 0.03, 2), walk);
        }
        // houses: two rows each side of the main road, fronts to the street, 11 m apart, yard trees between them
        let hi = 0;
        for (let k = 0; k < 3; k++) {
          const xa = xb[2 * k] + 6, xe = xb[2 * k + 1] - 6;
          for (let x = xa; x <= xe + 0.01; x += 11) for (const [zr, yaw] of [[ROAD_Z - 3.5 - SIDE - 9, Math.PI], [ROAD_Z - 3.5 - SIDE - 27, 0], [ROAD_Z + 3.5 + SIDE + 9, 0], [ROAD_Z + 3.5 + SIDE + 27, Math.PI]] as const) {
            house(b, x, zr, yaw, 8, 7, 3.3, hi++);
            if (hi % 3 === 0 && x + 5.5 < xe + 5) prop(b, kit, "tree_cone", x + 5.5, D0, zr + (zr < ROAD_Z ? -3 : 3), 5 + r() * 2, r() * 6);
          }
        }
      }
      b.build(this.desert);
      setSight([]);
      this.fill = new THREE.Mesh(quadY(-900, 172, -30, 30, 0, 10), sand);
      this.fill.receiveShadow = true;
      this.desert.add(this.fill);
    }

    // ---- water: one dynamic quad (river / canal / sea) + the lake ----
    const wNear = waterNear(), wFar = waterFar();
    for (const t of [wNear, wFar]) { t.colorSpace = THREE.NoColorSpace; t.anisotropy = 16; t.needsUpdate = true; }
    this.WU = {
      wNearC: { value: new THREE.Color() }, wMidC: { value: new THREE.Color() }, wFarC: { value: new THREE.Color() },
      wCrest: { value: new THREE.Color() }, wTrough: { value: new THREE.Color() }, wGlint: { value: new THREE.Color() },
      wShade: { value: new THREE.Vector3(0.5, 0.56, 0.72) }, wNearTex: { value: wNear }, wFarTex: { value: wFar }, wTime: { value: 0 },
    };
    const waterM = new THREE.MeshLambertMaterial({ color: 0xffffff });
    waterM.onBeforeCompile = (sh) => {
      Object.assign(sh.uniforms, this.WU);
      sh.vertexShader = sh.vertexShader
        .replace("#include <common>", "#include <common>\nvarying vec3 vWP;")
        .replace("#include <project_vertex>", "#include <project_vertex>\nvWP = (modelMatrix * vec4(transformed, 1.0)).xyz;");
      sh.fragmentShader = sh.fragmentShader
        .replace("#include <common>", WATER_DECL)
        .replace("#include <map_fragment>", WATER_COL)
        .replace("#include <lights_fragment_begin>", "float sunVis = 1.0;\n" + LFB)
        .replace("#include <lights_fragment_end>", "#include <lights_fragment_end>\n  reflectedLight.directDiffuse = diffuseColor.rgb * mix(wShade, vec3(1.0), sunVis);\n  reflectedLight.indirectDiffuse = vec3(0.0);");
    };
    waterM.customProgramCacheKey = () => "river1";
    this.water = new THREE.Mesh(quadY(0, 1, 0, 1, 0, 1), waterM);
    this.water.receiveShadow = true; this.water.frustumCulled = false;
    R.add(this.water);
    const lake = new THREE.Mesh(quadY(172, 1500, -1500, 1500, 0, 1), waterM); lake.receiveShadow = true;
    this.desert.add(lake);

    // ---- bridge, ship, trucks ----
    this.pieces = buildBridge(kit);
    for (const g of this.pieces) this.bridge.add(g);
    this.ship = buildShip(); this.sea.add(this.ship);
    ["#c9453a", "#e2b33c", "#3f6fb5"].forEach((c, k) => { const t = buildTruck(c, k); this.trucks.push(t); this.desert.add(t); });
  }

  /** a cactus must not stand in front of any desert lens */
  private blocked(x: number, z: number, h: number) {
    for (const s of SHOTS) if (s.place === "desert") for (let f = s.a; f < s.b; f += 6) {
      const c = camAt(s.id, f), dx = c.look[0] - c.pos[0], dz = c.look[2] - c.pos[2], L = Math.hypot(dx, dz) || 1;
      const px = x - c.pos[0], pz = z - c.pos[2], along = (px * dx + pz * dz) / L, perp = Math.abs(px * dz - pz * dx) / L;
      if (along > -2 && along < L + 4 && perp < 3 + along * 0.45 && c.pos[1] < D0 + h + 3) return true;
    }
    return false;
  }

  private shotSun(id: number, s: ShotDef, L: LightPreset) {
    let v = this.sunCache.get(id);
    if (v) return v;
    let fx = 0, fz = 0;
    for (let f = s.a; f < s.b; f += 3) {
      const c = camAt(id, f), x = c.look[0] - c.pos[0], z = c.look[2] - c.pos[2], n = Math.hypot(x, z) || 1;
      fx += x / n; fz += z / n;
    }
    const n = Math.hypot(fx, fz) || 1; fx /= n; fz /= n;
    const az = THREE.MathUtils.degToRad(s.sunAz ?? L.az), el = THREE.MathUtils.degToRad(s.sunEl ?? L.el);
    const hx = fx * Math.cos(az) - fz * Math.sin(az), hz = fz * Math.cos(az) + fx * Math.sin(az);
    v = new THREE.Vector3(hx * Math.cos(el), Math.sin(el), hz * Math.cos(el)).normalize();
    this.sunCache.set(id, v);
    return v;
  }
  private actor(i: number) { while (this.actors.length <= i) this.actors.push(new Actor(this.root)); return this.actors[i]; }
  private fx(i: number) { while (this.fxs.length <= i) this.fxs.push(new Fx(this.root)); return this.fxs[i]; }

  update(id: number, f: number, cam: THREE.PerspectiveCamera, scene: THREE.Scene, pre?: number) {
    const t = f / FPS, s = SHOTS[id - 1], L = LIGHTS[s.light], ws = worldAt(id, t);
    const c = camAt(id, f, pre);
    cam.position.set(...c.pos); cam.up.set(0, 1, 0); cam.lookAt(...c.look); cam.rotateZ(c.roll);
    cam.fov = c.fov; cam.near = 0.2; cam.far = 1500; cam.updateProjectionMatrix(); cam.updateMatrixWorld();
    const focus = V(...c.look), dist = cam.position.distanceTo(focus);
    cam.layers.enable(NOINK);
    const K = LOOK[s.light], sunDir = this.shotSun(id, s, L);
    this.hemi.color.set(L.sky); this.hemi.groundColor.set(L.ground); this.hemi.intensity = L.hemiI;
    this.sun.color.set(L.sunCol); this.sun.intensity = L.sunI;
    let Rr = THREE.MathUtils.clamp(dist * 1.15 + 7, 12, 95);
    if (s.light === "golden") Rr = Math.max(Rr, 30);
    this.sun.position.copy(focus).addScaledVector(sunDir, 220); this.sun.target.position.copy(focus);
    const sc = this.sun.shadow.camera;
    sc.left = -Rr; sc.right = Rr; sc.top = Rr; sc.bottom = -Rr; sc.near = 20; sc.far = 480; sc.updateProjectionMatrix();
    this.sun.shadow.bias = L.bias; this.sun.shadow.normalBias = L.normalBias * (Rr / 12);
    TONE.uLitCol.value.set(...L.lit); TONE.uShadeCol.value.set(...L.shade); TONE.uShadeLift.value.set(...L.lift);
    TONE.uLambert.value = L.lambert; TONE.uSideK.value = L.sideK; TONE.uTerm.value = L.term; TONE.uBounce.value.set(...LOOK[s.light].bounce); TONE.uSat.value = LOOK[s.light].sat;
    CHAR.uCharTint.value.set(...L.charTint); CHAR.uCharShade.value = L.charShade; CHAR.uGrad.value = L.charGrad;
    CHAR.uBodyGrad.value = L.bodyGrad; CHAR.uSideTint.value.set(...L.sideTint);
    // sky: the desert horizon is a warmer, paler blue
    const su = this.skyMat.uniforms;
    K.sky.c.forEach((h, i) => untone(s.place === "desert" && s.light === "day" && i < 2 ? ["#dfe6ea", "#c2d6ee"][i] : h, su["c" + i].value));
    const e = K.sky.e.map((deg) => THREE.MathUtils.degToRad(deg));
    su.e.value.set(e[1], e[2], e[3], e[4]);
    this.sky.position.copy(cam.position);
    untone(s.place === "desert" && s.light === "day" ? "#dfe4e6" : L.fog, this.fog.color);
    this.fog.near = s.place === "desert" ? 120 : L.fogNear; this.fog.far = s.place === "desert" ? 1400 : L.fogFar;
    scene.fog = this.fog; scene.background = null;
    const showSun = s.light === "golden";
    this.sunDisc.visible = this.sunHalo.visible = showSun;
    if (showSun) {
      this.sunDisc.position.copy(cam.position).addScaledVector(sunDir, 900);
      this.sunDisc.scale.setScalar(2 * 900 * Math.tan(THREE.MathUtils.degToRad(1.7)));
      this.sunHalo.position.copy(this.sunDisc.position); this.sunHalo.scale.setScalar(2 * 900 * Math.tan(THREE.MathUtils.degToRad(24)));
      (this.sunHalo.material as THREE.SpriteMaterial).color.set(L.sunDisc).multiplyScalar(1.3);
    }
    for (let i = 0; i < this.clouds.length; i++) {
      const m = this.clouds[i], mat = m.material as THREE.MeshBasicMaterial;
      m.lookAt(cam.position.x, m.position.y, cam.position.z);
      mat.map = this.cloudMaps[s.light][i % 4];
    }
    const Wu = this.WU, wc = K.water;
    untone(wc.near, Wu.wNearC.value); untone(wc.mid, Wu.wMidC.value); untone(wc.far, Wu.wFarC.value);
    untone(wc.crest, Wu.wCrest.value); untone(wc.trough, Wu.wTrough.value); untone(wc.glint, Wu.wGlint.value);
    Wu.wShade.value.set(...wc.shade); Wu.wTime.value = t;
    // ---- places ----
    this.london.visible = s.place === "london"; this.desert.visible = s.place === "desert"; this.sea.visible = s.place === "sea";
    this.bridge.visible = s.place !== "sea";
    this.pile.visible = false; // (London Bridge short only)
    this.pieces.forEach((g, i) => { g.visible = i >= ws.pieces[0] && i < ws.pieces[1]; });
    this.bridge.position.y = ws.sink;
    this.fill.position.y = ws.fill;
    // water quad
    const wp = this.water.geometry.attributes.position as THREE.BufferAttribute;
    let x0 = -900, x1 = 900, z0 = -30, z1 = 30, y = 0;
    if (s.place === "sea") { x0 = -1500; x1 = 1500; z0 = -1500; z1 = 1500; }
    if (s.place === "desert") { x0 = Math.max(-900, ws.front); x1 = 172.5; y = ws.water; }
    this.water.visible = !(s.place === "desert" && (ws.water < -5 || x0 >= x1));
    const arr = [x0, y, z1, x1, y, z1, x1, y, z0, x0, y, z1, x1, y, z0, x0, y, z0];
    for (let i = 0; i < 6; i++) wp.setXYZ(i, arr[i * 3], arr[i * 3 + 1], arr[i * 3 + 2]);
    wp.needsUpdate = true;
    // ship + trucks
    if (s.place === "sea") {
      this.ship.position.set(shipX(t), -0.9 + 0.12 * Math.sin(t * 1.3), 0);
      this.ship.rotation.set(0.02 * Math.sin(t * 1.1), 0, 0.012 * Math.sin(t * 0.8 + 1));
    }
    this.trucks.forEach((tr, k) => { tr.visible = false; tr.position.set(truckX(t, k), D0 + 0.02 + 0.03 * Math.max(0, Math.sin(t * 9 + k * 2)), ROAD_Z + (k % 2 ? 1.6 : -1.6)); });
    for (const sm of this.smoke) {
      const u = (t * 0.11 + sm.k) % 1, sz = 3 + u * 9;
      sm.m.position.set(sm.top[0] - u * 18, sm.top[1] + u * 13 + u * u * 4, sm.top[2] + u * 3);
      sm.m.scale.set(sz, sz, 1); sm.m.quaternion.copy(cam.quaternion);
      sm.mat.opacity = 0.85 * (1 - u) ** 1.2;
    }
    // ---- cast + effects ----
    const right = V(0, 0, 0).setFromMatrixColumn(cam.matrixWorld, 0);
    const st = stage(id, t, ws, { pos: cam.position, right });
    this.frustum.setFromProjectionMatrix(this.m4.multiplyMatrices(cam.projectionMatrix, cam.matrixWorldInverse));
    let ai = 0;
    const used: Actor[] = [];
    for (const p of st.places) {
      const sc2 = p.scale ?? 1;
      if (!this.frustum.intersectsSphere(this.sph.set(this.v.set(p.x, p.y + 1.1 * sc2, p.z), 3.5 * Math.max(1, sc2)))) continue;
      const a = this.actor(ai++);
      const [w, h, k] = p.size ?? [300, 500, 0.5];
      a.r = this.pool.req(p.key, w, h, k, p.draw);
      a.mesh.visible = true;
      a.mesh.position.set(p.x, p.y, p.z);
      a.mesh.rotation.set(0, p.yaw ?? Math.atan2(cam.position.x - p.x, cam.position.z - p.z), p.roll ?? 0);
      a.mesh.scale.set(p.mirror ? -sc2 : sc2, sc2, sc2);
      a.mesh.castShadow = L.actorShadow;
      used.push(a);
    }
    for (let i = ai; i < this.actors.length; i++) this.actors[i].mesh.visible = false;
    let fi = 0;
    const fused: Fx[] = [];
    for (const p of st.fx) {
      if (!this.frustum.intersectsSphere(this.sph.set(this.v.set(p.x, p.y, p.z), Math.max(p.w, p.h)))) continue;
      const e = this.fx(fi++);
      e.r = this.pool.req(p.key, p.cw, p.ch, 1, p.draw);
      e.use(!!p.soft);
      e.mesh.visible = true;
      e.mesh.position.set(p.x, p.y, p.z);
      if (p.flat) e.mesh.rotation.set(-Math.PI / 2, 0, p.rot ?? 0);
      else if (p.yaw !== undefined) e.mesh.rotation.set(0, p.yaw, p.rot ?? 0);
      else { e.mesh.quaternion.copy(cam.quaternion); e.mesh.rotateZ(p.rot ?? 0); }
      e.mesh.scale.set(p.w, p.h, 1);
      fused.push(e);
    }
    for (let i = fi; i < this.fxs.length; i++) this.fxs[i].mesh.visible = false;
    this.pool.flush();
    for (const a of used) a.bind();
    for (const e of fused) e.bind();
    return focus;
  }
}

const WATER_DECL = `#include <common>
varying vec3 vWP;
uniform vec3 wNearC, wMidC, wFarC, wCrest, wTrough, wGlint, wShade;
uniform sampler2D wNearTex, wFarTex;
uniform float wTime;`;
const WATER_COL = `
  vec3 wV = vWP - cameraPosition;
  float wd = length(wV);
  float wDep = asin(clamp(-wV.y / wd, 0.0, 1.0));
  float wf = 1.0 - smoothstep(0.0, 0.42, wDep);
  vec3 wc = mix(mix(wNearC, wMidC, smoothstep(0.0, 0.55, wf)), wFarC, smoothstep(0.55, 1.0, wf));
  vec2 wp = vWP.xz + vec2(0.35 * wTime, 0.0);
  vec4 mk = mix(texture2D(wNearTex, wp / 8.0), texture2D(wFarTex, wp / 40.0 + 0.37), smoothstep(25.0, 90.0, wd));
  wc = mix(wc, wTrough, mk.g * 0.6);
  wc = mix(wc, wCrest, mk.r * 0.7);
  wc = mix(wc, wGlint, mk.b * (0.3 + 0.5 * wf));
  diffuseColor.rgb = wc;`;
