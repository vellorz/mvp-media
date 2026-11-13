// 1850s downtown Chicago on the far bank: a planned grid of muddy streets with plank sidewalks, brick commercial rows on
// the river quay and on both sides of Lake Street, wooden houses on lawns further north, Lake Michigan to the east.
// Three buildings are their own groups so they can rise on jackscrews: the Tremont House, the 1858 building and the
// 1860 Lake Street block. Everything is laid out on the street grid: nothing stands on a road or a sidewalk.
import * as THREE from "three";
import { Batch, boxGeo, V, lam, quad, house, prop, Kit, inWayAll, setSight, Ray } from "./build";
import { ctex, facadeHD, planksHD, stoneHD, grassHD, rng, rep, brick } from "./paint";
import { facadeInk, mudInk, boardsInk, skylineInk } from "./hand";
import { NOINK } from "./ink";
import { D0, SW, LAKE_X, LAKE_Z, TRE, B58, BLK, SEWER, STEP_H } from "./story";

// ---------------- textures ----------------
const mudTex = (key: string, ruts: boolean) => { const t = ctex(key, 1024, 1024, (g, r) => {
  g.fillStyle = "#8a6a4c"; g.fillRect(0, 0, 1024, 1024);
  for (let i = 0; i < 60; i++) { const x = r() * 1024, y = r() * 1024, rad = 40 + r() * 160, gr = g.createRadialGradient(x, y, 0, x, y, rad);
    const c = r() < 0.5 ? "110,82,56" : "160,128,92"; gr.addColorStop(0, `rgba(${c},0.45)`); gr.addColorStop(1, `rgba(${c},0)`); g.fillStyle = gr; g.fillRect(x - rad, y - rad, rad * 2, rad * 2); }
  if (ruts) for (const y of [300, 380, 640, 720]) { // wheel ruts along u
    g.strokeStyle = "rgba(70,50,34,0.55)"; g.lineWidth = 16; g.beginPath();
    for (let x = 0; x <= 1024; x += 32) g.lineTo(x, y + 6 * Math.sin(x * 0.012 + y));
    g.stroke();
    g.strokeStyle = "rgba(190,160,120,0.35)"; g.lineWidth = 4; g.beginPath();
    for (let x = 0; x <= 1024; x += 32) g.lineTo(x, y - 10 + 6 * Math.sin(x * 0.012 + y));
    g.stroke();
  }
  for (let i = 0; i < 2600; i++) { g.fillStyle = r() < 0.5 ? "rgba(60,44,30,0.35)" : "rgba(200,170,130,0.35)"; g.beginPath(); g.arc(r() * 1024, r() * 1024, 1 + r() * 2.4, 0, 7); g.fill(); }
}); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 16; return t; };
const signTex = (s: string, bg: string, fg: string, w = 1024, h = 192) => ctex("sign" + s + bg, w, h, (g) => {
  g.fillStyle = bg; g.fillRect(0, 0, w, h);
  g.strokeStyle = fg; g.lineWidth = 10; g.strokeRect(14, 14, w - 28, h - 28);
  let size = h * 0.56;
  g.font = `bold ${size}px Georgia, 'Times New Roman', serif`;
  while (g.measureText(s).width > w - 90 && size > 20) { size -= 4; g.font = `bold ${size}px Georgia, 'Times New Roman', serif`; }
  g.fillStyle = fg; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(s, w / 2, h / 2 + 4);
});
const signMat = (s: string, bg = "#2f4a3a", fg = "#f2e3b8") => {
  const key = "signM" + s + bg;
  let m = SIGNS.get(key);
  if (!m) { m = new THREE.MeshBasicMaterial({ map: signTex(s, bg, fg) }); m.userData.full = m.map; m.userData.blank = signTex("", bg, fg); SIGNS.set(key, m); }
  return m;
};
/** rule 64: every lettered sign in the world, so a shot that would crop its lettering shows the board blank instead */
export type SignRec = { m: THREE.MeshBasicMaterial; c: [number, number, number][]; which?: "tre" | "b58" | "blk" };
export const SIGN_LIST: SignRec[] = [];
const SIGNS = new Map<string, THREE.MeshBasicMaterial>();

// ---------------- grid ----------------
/** N-S streets (along z) and E-W streets (along x): centre, road half width; sidewalks 3 m either side */
const XS = [-125, -60, 60, 125], XH = 5;
const ZS: [number, number][] = [[(LAKE_Z[0] + LAKE_Z[1]) / 2, (LAKE_Z[1] - LAKE_Z[0]) / 2], [143, 5], [205, 5], [265, 5]];
const SWW = 3, CX0 = -185, CX1 = 168, CZ0 = 36.5, CZ1 = 330;
/** x bands between the N-S streets (building lines) */
const XB: [number, number][] = [[CX0, XS[0] - XH - SWW], [XS[0] + XH + SWW, XS[1] - XH - SWW], [XS[1] + XH + SWW, XS[2] - XH - SWW], [XS[2] + XH + SWW, XS[3] - XH - SWW], [XS[3] + XH + SWW, CX1 - 3]];
/** z bands between the E-W streets */
const ZB: [number, number][] = [[CZ0 + 0.5, ZS[0][0] - ZS[0][1] - SWW], [ZS[0][0] + ZS[0][1] + SWW, ZS[1][0] - ZS[1][1] - SWW],
  [ZS[1][0] + ZS[1][1] + SWW, ZS[2][0] - ZS[2][1] - SWW], [ZS[2][0] + ZS[2][1] + SWW, ZS[3][0] - ZS[3][1] - SWW], [ZS[3][0] + ZS[3][1] + SWW, CZ1]];

// ---------------- buildings ----------------
type Look = { wall: string; shutter: string; brick?: boolean; trim: string };
const LOOKS: Look[] = [
  { wall: "#c8643f", shutter: "#2f5f6a", brick: true, trim: "#e9dcc0" },
  { wall: "#e6d3ad", shutter: "#2f6a43", trim: "#8a5a3c" },
  { wall: "#c8643f", shutter: "#3b3f52", brick: true, trim: "#d9c7a4" },
  { wall: "#d8a95f", shutter: "#5a3b2a", trim: "#f0e2c4" },
  { wall: "#c8643f", shutter: "#8c3b4a", brick: true, trim: "#efe3c8" },
  { wall: "#cc9a6c", shutter: "#2f5f6a", trim: "#f0e2c4" },
];
const SHOPS = ["DRY GOODS", "HARDWARE", "BOOTS & SHOES", "BAKERY", "HATS", "BOOKS", "TEA & COFFEE", "GROCERY", "TAILOR", "PRINTER", "DRUGS", "SADDLERY"];
const SIGN_BG = ["#2f4a3a", "#5a2a2a", "#2a3550", "#3b2f24"];
const roofM = () => lam("tarRoof", () => ({ color: "#5d5560" }));
const trimL = (c: string) => lam("trim" + c, () => ({ color: c }));
const timberM = () => lam("timberC", () => ({ color: "#8a6a4a" }));
const ironM = () => lam("ironC", () => ({ color: "#4a4d55" }));
const plankM = () => lam("plankC", () => { const t = boardsInk(); t.wrapS = t.wrapT = THREE.RepeatWrapping; return { map: t }; });
let SI = 0;

/** flat-roofed commercial block: front plane at z = zf facing dir (+1 = +z, -1 = -z), x0..x1, depth d, height h.
 *  y = base height (the group's local origin for rising buildings). Returns false when a camera ray needs the space. */
const block = (b: Batch, x0: number, x1: number, zf: number, dir: 1 | -1, d: number, h: number, look: Look, o: { y?: number; sign?: string; signBg?: string; cull?: boolean; under?: boolean; awning?: string; key?: string } = {}) => {
  const y = o.y ?? D0, w = x1 - x0, za = dir > 0 ? zf - d : zf, zb = dir > 0 ? zf : zf + d;
  if (o.cull !== false && inWayAll(x0 - 0.4, x1 + 0.4, y, y + h + 1.2, za - 0.4, zb + 0.4)) return false;
  const k = o.key ?? `${SI++}`;
  const front = lam(`cf${k}`, () => ({ map: facadeInk(`cf${k}_${w}_${h}`, w, h, { wall: look.wall, shutter: look.shutter, door: true, brick: look.brick, posters: k !== "tremont" /* v17 rule 63: its real 3D windows sit on other spacing and covered a poster */ }) }));
  const side = lam(`cs${look.wall}${look.brick ? "b" : ""}_${d}_${h}`, () => ({ map: facadeInk(`cs${look.wall}${look.brick ? "b" : ""}_${d}_${h}`, d, h, { wall: look.wall, shutter: look.shutter, brick: look.brick }) }));
  const back = lam(`cb${look.wall}${look.brick ? "b" : ""}_${w}_${h}`, () => ({ map: facadeInk(`cb${look.wall}${look.brick ? "b" : ""}_${w}_${h}`, w, h, { wall: look.wall, shutter: look.shutter, brick: look.brick }) }));
  const zF = zf, zB = dir > 0 ? za : zb;
  if (dir > 0) {
    b.add(quad(V(x0, y, zF), V(x1, y, zF), V(x1, y + h, zF), V(x0, y + h, zF)), front);
    b.add(quad(V(x1, y, zB), V(x0, y, zB), V(x0, y + h, zB), V(x1, y + h, zB)), back);
    b.add(quad(V(x0, y, zB), V(x0, y, zF), V(x0, y + h, zF), V(x0, y + h, zB)), side);
    b.add(quad(V(x1, y, zF), V(x1, y, zB), V(x1, y + h, zB), V(x1, y + h, zF)), side);
  } else {
    b.add(quad(V(x1, y, zF), V(x0, y, zF), V(x0, y + h, zF), V(x1, y + h, zF)), front);
    b.add(quad(V(x0, y, zB), V(x1, y, zB), V(x1, y + h, zB), V(x0, y + h, zB)), back);
    b.add(quad(V(x1, y, zB), V(x1, y, zF), V(x1, y + h, zF), V(x1, y + h, zB)), side);
    b.add(quad(V(x0, y, zF), V(x0, y, zB), V(x0, y + h, zB), V(x0, y + h, zF)), side);
  }
  b.add(boxGeo(V(x0 + 0.02, y + h - 0.1, za + 0.02), V(x1 - 0.02, y + h + 0.05, zb - 0.02)), roofM());
  const tm = trimL(look.trim), out = 0.35;
  // cornice + parapet on the front, a thin cornice band round the sides
  b.add(boxGeo(V(x0 - 0.15, y + h - 0.55, dir > 0 ? zF - 0.4 : zF - out), V(x1 + 0.15, y + h + 0.6, dir > 0 ? zF + out : zF + 0.4)), tm);
  for (const sx of [x0, x1]) b.add(boxGeo(V(sx - 0.12, y + h - 0.45, za), V(sx + 0.12, y + h - 0.15, zb)), tm);
  b.add(boxGeo(V(x0 - 0.06, y - 0.05, za - 0.06), V(x1 + 0.06, y + 0.45, zb + 0.06), 2), lam("plinthC", () => ({ map: stoneHD("copeHD") })));
  // floor bands between storeys on the front
  const floors = Math.max(1, Math.floor(h / 2.8));
  // (bands overhang the side walls by 6 cm: flush end caps z-fought with the sides and flickered black)
  for (let fl = 1; fl < floors; fl++) b.add(boxGeo(V(x0 - 0.06, y + fl * 2.8 - 0.16, dir > 0 ? zF - 0.05 : zF - 0.2), V(x1 + 0.06, y + fl * 2.8 + 0.04, dir > 0 ? zF + 0.2 : zF + 0.05)), tm); // deeper: thin edge-on faces inked as dashes (rule 47)
  if (o.under) b.add(boxGeo(V(x0 + 0.03, y - 0.18, za + 0.03), V(x1 - 0.03, y - 0.02, zb - 0.03), 2, true), timberM()); // floor beams seen when raised
  if (o.sign) { // shop sign board over the street-floor windows (unlit so it stays readable)
    // v21 rule 84 (owner): the floor band (out to 0.2 m) crossed the DRY GOODS lettering; that board now stands in front of it
    const sw = Math.min(w - 1.2, 7.5), zz = zF + dir * (o.key === "b58" ? 0.24 : 0.17), cx = (x0 + x1) / 2;
    const g = dir > 0 ? quad(V(cx - sw / 2, y + 2.5, zz), V(cx + sw / 2, y + 2.5, zz), V(cx + sw / 2, y + 3.4, zz), V(cx - sw / 2, y + 3.4, zz))
      : quad(V(cx + sw / 2, y + 2.5, zz), V(cx - sw / 2, y + 2.5, zz), V(cx - sw / 2, y + 3.4, zz), V(cx + sw / 2, y + 3.4, zz));
    b.add(g, signMat(o.sign, o.signBg));
    SIGN_LIST.push({ m: signMat(o.sign, o.signBg), c: [[cx - sw / 2, y + 2.5, zz], [cx + sw / 2, y + 2.5, zz], [cx - sw / 2, y + 3.4, zz], [cx + sw / 2, y + 3.4, zz]], which: o.key === "b58" ? "b58" : o.key?.startsWith("blk") ? "blk" : undefined });
    // v6: the frame box stops 3 cm BEHIND the sign face on both street sides (on north-row blocks, dir -1, it used to
    // stick out in front and hide every sign behind a blank cream board with inked dashes)
    const zIn = zz - dir * 0.03;
    b.add(boxGeo(V(cx - sw / 2 - 0.08, y + 2.42, Math.min(zF, zIn)), V(cx + sw / 2 + 0.08, y + 3.48, Math.max(zF, zIn))), tm);
  }
  // canvas awning over the shop windows, sloping out to the sidewalk; dropped when any camera ray needs that space
  // (the block's own cull box stops at the facade, so awnings used to block the start of S5a and S7a)
  if (o.awning && !inWayAll(x0, x1, y + 1.6, y + 2.5, Math.min(zF, zF + dir * 1.8), Math.max(zF, zF + dir * 1.8))) {
    const z0 = zF, z1 = zF + dir * 1.6, a = lam("awn" + o.awning, () => ({ color: o.awning!, side: THREE.DoubleSide }));
    // v21 rule 86 (owner): on the Lake Street block the canopy hung across the doors (front edge 1.95 m, doors 2.4 m with
    // their surround); there it mounts under the sign board and its lowest edge stays above the door head
    const blk = !!o.key?.startsWith("blk"), yt = y + (blk ? 2.49 : 2.35), yf = y + (blk ? 2.43 : 1.95), vh = blk ? 0.0 : 0.2;
    const g = dir > 0 ? quad(V(x0 + 0.4, yt, z0), V(x0 + 0.4, yf, z1), V(x1 - 0.4, yf, z1), V(x1 - 0.4, yt, z0))
      : quad(V(x1 - 0.4, yt, z0), V(x1 - 0.4, yf, z1), V(x0 + 0.4, yf, z1), V(x0 + 0.4, yt, z0));
    b.add(g, a);
    if (vh > 0) b.add(boxGeo(V(x0 + 0.4, yf - vh, Math.min(z1, z1 - dir * 0.08)), V(x1 - 0.4, yf, Math.max(z1, z1 - dir * 0.08))), a);
    else b.add(boxGeo(V(x0 + 0.4, yf - 0.02, Math.min(z1, z1 - dir * 0.08)), V(x1 - 0.4, yf + 0.06, Math.max(z1, z1 - dir * 0.08))), a);
  }
  return true;
};
/** fill a frontage x0..x1 with blocks of 9-15 m, heights 3-4 storeys */
const row = (b: Batch, r: () => number, x0: number, x1: number, zf: number, dir: 1 | -1, d: number, signs: boolean, skip?: [number, number]) => {
  let x = x0;
  while (x < x1 - 6) {
    let w = [9, 11, 12, 14][Math.floor(r() * 4)];
    if (x + w > x1 - 5) w = x1 - x;
    if (skip && x < skip[1] && x + w > skip[0]) { x = skip[1] + 0.3; continue; }
    if (skip && x < skip[0] && x + w > skip[0]) w = skip[0] - 0.3 - x;
    if (w < 6) { x += w + 0.3; continue; }
    const fl = 3 + Math.floor(r() * 2), look = LOOKS[Math.floor(r() * LOOKS.length)];
    const sign = signs ? SHOPS[Math.floor(r() * SHOPS.length)] : undefined;
    block(b, x, x + w, zf, dir, d, fl * 2.8 + 0.5, look, { sign, signBg: SIGN_BG[Math.floor(r() * 4)], awning: signs && r() < 0.45 ? ["#e8d6a8", "#b8553a", "#4f7a5a", "#d9a441"][Math.floor(r() * 4)] : undefined });
    x += w + 0.25;
  }
};

export type City = { tre: THREE.Group; b58: THREE.Group; blk: THREE.Group; screws: { g: THREE.Group; which: "tre" | "b58" | "blk" }[]; steps: THREE.Mesh[];
  pipe: THREE.Group; fill: THREE.Mesh; puddles: THREE.Group; skyline?: THREE.Mesh };

/** jackscrews on timber pads under a footprint; the group is scaled in y to the lift (unit height 1 m) */
const screwGrid = (x0: number, x1: number, z0: number, z1: number, sx: number, sz: number) => {
  const g = new THREE.Group(), pads = new Batch(), cols = new Batch();
  for (let x = x0 + sx / 2; x < x1; x += sx) for (let z = z0 + sz / 2; z < z1; z += sz) {
    pads.add(boxGeo(V(x - 0.3, D0, z - 0.3), V(x + 0.3, D0 + 0.22, z + 0.3)), timberM());
    const c = new THREE.CylinderGeometry(0.1, 0.13, 1, 10); c.translate(x, 0.5, z); cols.add(c, ironM());
    const cap = new THREE.CylinderGeometry(0.2, 0.2, 0.06, 10); cap.translate(x, 0.97, z); cols.add(cap, ironM());
  }
  const pg = new THREE.Group(); pads.build(pg);
  const cg = new THREE.Group(); cols.build(cg); cg.position.y = D0 + 0.22;
  g.add(pg, cg);
  return { g, cols: cg };
};

export const buildCity = (root: THREE.Object3D, kit: Kit, rays: Ray[]) => {
  let skyRing: THREE.Mesh | undefined;
  setSight(rays);
  const b = new Batch(), r = rng(1858);
  const mud = lam("mudC", () => ({ map: mudInk("mud", false) })), roadX = lam("roadMudX", () => ({ map: mudInk("roadX", true) }));
  const roadZ = lam("roadMudZ", () => { const t = mudInk("roadZ", true); t.rotation = Math.PI / 2; return { map: t }; });
  const lawn = lam("lawnC", () => ({ map: grassHD() }));
  const qy = (x0: number, x1: number, z0: number, z1: number, y: number, tile: number) => {
    const g = quad(V(x0, y, z1), V(x1, y, z1), V(x1, y, z0), V(x0, y, z0), (x1 - x0) / tile, (z1 - z0) / tile);
    return g;
  };
  // ground: mud everywhere in town, streets with ruts, lawns on the house blocks
  b.add(qy(CX0, LAKE_X, CZ0, CZ1, D0 + 0.0, 16), mud);
  for (const [zc, hz] of ZS) b.add(qy(CX0, CX1, zc - hz, zc + hz, D0 + 0.03, 16), roadX);
  for (const xc of XS) for (const [za, zb] of [[CZ0, ZS[0][0] - ZS[0][1]], ...ZS.slice(0, -1).map(([zc, hz], i) => [zc + hz, ZS[i + 1][0] - ZS[i + 1][1]]), [ZS[3][0] + ZS[3][1], CZ1]] as [number, number][])
    b.add(qy(xc - XH, xc + XH, za, zb, D0 + 0.03, 16), roadZ);
  for (let zi = 2; zi < ZB.length; zi++) for (const [xa, xb] of XB) b.add(qy(xa, xb, ZB[zi][0], ZB[zi][1], D0 + 0.03, 4), lawn);
  // plank sidewalks (raised 15 cm) along every street side; they stop at the crossings
  const pk = plankM();
  for (const [zc, hz] of ZS) for (const [xa, xb] of XB) for (const s of [-1, 1]) {
    const z0 = s < 0 ? zc - hz - SWW : zc + hz, z1 = s < 0 ? zc - hz : zc + hz + SWW;
    b.add(boxGeo(V(xa - SWW, D0, z0), V(xb + SWW, D0 + SW, z1), 4, false, 0.004), pk);
  }
  for (const xc of XS) for (const [za, zb] of ZB) for (const s of [-1, 1]) {
    const x0 = s < 0 ? xc - XH - SWW : xc + XH, x1 = s < 0 ? xc - XH : xc + XH + SWW;
    b.add(boxGeo(V(x0, D0, za), V(x1, D0 + SW, zb), 4, false, 0.004), pk);
  }
  // shore strip to the lake
  b.add(qy(CX1, LAKE_X, CZ0, CZ1, D0 + 0.03, 6), lam("shoreC", () => ({ map: ctex("cShoreSandT", 512, 512, (g, rr) => {
    // v19: drawn lake beach (sand ripples, pebbles, shells, driftwood twigs, wet patches), was a flat colour
    g.fillStyle = "#cdb48a"; g.fillRect(0, 0, 512, 512);
    for (let i = 0; i < 26; i++) { g.fillStyle = "rgba(150,120,80,0.28)"; g.beginPath(); g.ellipse(rr() * 512, rr() * 512, 30 + rr() * 60, 10 + rr() * 20, rr() * 3, 0, 6.28); g.fill(); }
    g.lineCap = "round";
    for (let i = 0; i < 70; i++) { const x = rr() * 512, y = rr() * 512, w = 20 + rr() * 50; g.strokeStyle = "rgba(120,92,58,0.6)"; g.lineWidth = 2.5; g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + w / 2, y - 6, x + w, y); g.stroke(); }
    for (let i = 0; i < 220; i++) { const x = rr() * 512, y = rr() * 512, rd = 2 + rr() * 5; g.fillStyle = ["#9a8a74", "#7a6e62", "#b8a894", "#6a5a4a"][i % 4]; g.beginPath(); g.ellipse(x, y, rd, rd * 0.7, rr() * 3, 0, 6.28); g.fill(); g.strokeStyle = "#2a2018"; g.lineWidth = 1.2; g.stroke(); }
    for (let i = 0; i < 14; i++) { const x = rr() * 512, y = rr() * 512; g.fillStyle = "#f2ead8"; g.beginPath(); g.arc(x, y, 6, Math.PI, 0); g.fill(); g.strokeStyle = "#2a2018"; g.lineWidth = 1.5; g.stroke(); for (const a of [-0.6, 0, 0.6]) { g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.sin(a) * 6, y - Math.cos(a) * 6); g.stroke(); } }
    for (let i = 0; i < 12; i++) { const x = rr() * 512, y = rr() * 512, a = rr() * 3.14, L = 24 + rr() * 30; g.strokeStyle = "#8a6a48"; g.lineWidth = 5; g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * L, y + Math.sin(a) * L); g.stroke(); g.strokeStyle = "#2a2018"; g.lineWidth = 1.5; g.stroke(); }
  }) })));

  // ---- commercial rows (B0 quay + Lake south, B1 Lake north) ----
  for (const [xa, xb] of XB) {
    row(b, r, xa, xb, ZB[0][0] + 0.5, -1, 15, false);                                             // river quay fronts (face the river)
    row(b, r, xa, xb, ZB[0][1], 1, 17, true, xa < B58.x0 && xb > B58.x1 ? [B58.x0, B58.x1] : undefined); // Lake Street, south side
    if (xa === BLK.x0) continue;                                                                      // the 1860 block is its own group
    row(b, r, xa, xb, ZB[1][0], -1, 18, true, xa < TRE.x0 && xb > TRE.x1 ? [TRE.x0, TRE.x1] : undefined); // Lake Street, north side
  }
  // ---- wooden houses on lawns (B2-B4): rows facing the E-W streets and the N-S streets ----
  for (let zi = 2; zi < ZB.length; zi++) {
    const [za, zb] = ZB[zi];
    for (const [xa, xb] of XB) {
      for (const [zf, yaw] of [[za + 3, 0], [zb - 3, Math.PI]] as const) { // fronts 3 m behind the sidewalk
        if (zf > CZ1 - 4) continue;
        let x = xa + 12;
        while (x < xb - 12) {
          const w = [7, 8, 9][Math.floor(r() * 3)], h = [5.6, 7, 8.4][Math.floor(r() * 3)], zc = yaw === 0 ? zf + 4 : zf - 4;
          // houses face their street: yaw 0 = front +z... the street is behind zf, so turn them to face it
          house(b, x + w / 2, zc, yaw === 0 ? Math.PI : 0, w, 8, h, Math.floor(r() * 8));
          if (r() < 0.35) prop(b, kit, ["tree_oak", "tree_default", "tree_fat"][Math.floor(r() * 3)], x + w / 2, D0, yaw === 0 ? zf + 13 : zf - 13, 7 + r() * 3, r() * 6);
          x += w + 2.5 + r() * 2;
        }
      }
      for (const [xf, yaw] of [[xa + 3, -Math.PI / 2], [xb - 3, Math.PI / 2]] as const) {
        if (xf < CX0 + 4 || xf > CX1 - 6) continue;
        let z = za + 2;
        while (z < zb - 9) {
          const w = [7, 8, 9][Math.floor(r() * 3)], h = [5.6, 7, 8.4][Math.floor(r() * 3)], xc = yaw < 0 ? xf + 4 : xf - 4;
          house(b, xc, z + w / 2, yaw, w, 8, h, Math.floor(r() * 8));
          z += w + 2 + r() * 2;
        }
      }
    }
  }
  // street dressing: lanterns at the sidewalk edges, a few carts in Lake Street
  for (let x = -176; x < 160; x += 18) for (const zl of [ZB[0][1] + SWW - 0.4, ZB[1][0] - SWW + 0.4]) {
    if (XS.some((xc) => Math.abs(x - xc) < XH + 3.5)) continue;
    if (Math.abs(x) < 17 || (x > 18 && x < 46) || (x > -98 && x < -86)) continue; // keep the Tremont, 1858, doctor and shop fronts clear // keep the Tremont + 1858 fronts clear
    prop(b, kit, "lantern", x, D0 + SW, zl, 2.9);
  }
  for (const [x, z, yaw] of [[-38, 100.5, 0.2], [84, 104.5, 3.0], [-150, 101, 1.4], [110, 99.5, 0.1]] as const) prop(b, kit, "cart", x, D0, z, 2.3, yaw);
  // street clutter (DETAIL_STANDARD: 20+ props in every wide): barrels, crates, sacks, hitching rails, water troughs, a
  // wheelbarrow, sign boards; kept off the fronts the story needs and out of every camera's sight line
  {
    const pr = rng(1861), wood = lam("clutWood", () => ({ color: "#8a6a48" })), woodD = lam("clutWoodD", () => ({ color: "#5e4632" })),
      sack = lam("clutSack", () => ({ color: "#c8b48a" })), iron = ironM(), water = lam("clutWater", () => ({ color: "#6f8aa8" }));
    const clear = (x: number) => Math.abs(x) < 16 || (x > 20 && x < 44) || (x > -97 && x < -88) || XS.some((xc) => Math.abs(x - xc) < XH + 3.5);
    for (const zs of [ZB[0][1] + 0.6, ZB[1][0] - 0.6]) for (let x = -178; x < 160; x += 2.2 + pr() * 3.2) {
      if (clear(x)) continue;
      const z = zs + (pr() - 0.5) * 0.8, k = pr(), y = D0 + SW;
      if (inWayAll(x - 0.8, x + 0.8, y, y + 1.4, z - 0.8, z + 0.8)) continue;
      if (k < 0.3) { const c = new THREE.CylinderGeometry(0.3, 0.27, 0.85, 12); c.translate(x, y + 0.425, z); b.add(c, wood);
        for (const hy of [0.15, 0.7]) { const h = new THREE.CylinderGeometry(0.31, 0.31, 0.05, 12); h.translate(x, y + hy, z); b.add(h, iron); } }
      else if (k < 0.5) { const sz = 0.45 + pr() * 0.3; b.add(boxGeo(V(x - sz / 2, y, z - sz / 2), V(x + sz / 2, y + sz, z + sz / 2)), wood);
        if (pr() < 0.5) b.add(boxGeo(V(x - sz / 3, y + sz, z - sz / 3), V(x + sz / 3, y + sz * 1.6, z + sz / 3)), woodD); }
      else if (k < 0.65) { for (let i = 0; i < 3; i++) { const sg = new THREE.SphereGeometry(0.28, 10, 8); sg.scale(1, 0.75, 0.8); sg.translate(x + i * 0.42 - 0.42, y + 0.2 + (i === 1 ? 0.3 : 0), z); b.add(sg, sack); } }
      else if (k < 0.78) { for (const dx of [-0.9, 0.9]) b.add(boxGeo(V(x + dx - 0.06, y, z - 0.06), V(x + dx + 0.06, y + 1.0, z + 0.06)), woodD); b.add(boxGeo(V(x - 1.0, y + 0.92, z - 0.05), V(x + 1.0, y + 1.0, z + 0.05)), woodD); }
      else if (k < 0.86) { b.add(boxGeo(V(x - 0.9, y, z - 0.3), V(x + 0.9, y + 0.55, z + 0.3)), woodD); b.add(boxGeo(V(x - 0.82, y + 0.4, z - 0.22), V(x + 0.82, y + 0.5, z + 0.22)), water); }
      else { b.add(boxGeo(V(x - 0.4, y, z - 0.03), V(x + 0.4, y + 1.1, z + 0.03)), sack); b.add(boxGeo(V(x - 0.45, y + 0.6, z - 0.05), V(x + 0.45, y + 1.15, z + 0.05)), woodD); }
    }
  }
  b.build(root);
  // painted far backdrop (6A): a ring of hazy rooftops / spires / smoke around the town, open toward the lake in the east
  {
    const tex = skylineInk("city", ["#b4b8c8", "#9ea2b8"]); tex.repeat.set(3, 1);
    const ring = new THREE.CylinderGeometry(330, 330, 95, 96, 1, true, Math.PI * 0.62, Math.PI * 1.55);
    const m = new THREE.Mesh(ring, new THREE.MeshBasicMaterial({ map: tex, transparent: true, side: THREE.BackSide, fog: false, depthWrite: false }));
    m.position.set(0, D0 - 9.5 + 95 / 2, 170); m.layers.set(NOINK); m.renderOrder = -0.5; root.add(m); skyRing = m;
  }

  // ---- rising buildings ----
  const tre = new THREE.Group(), b58 = new THREE.Group(), blk = new THREE.Group();
  {
    const tb = new Batch();
    const look: Look = { wall: "#e9d6ae", shutter: "#2f5a43", trim: "#f4ead2" };
    block(tb, TRE.x0, TRE.x1, TRE.z, -1, TRE.d, TRE.h, look, { y: 0, cull: false, under: true, key: "tremont" });
    // name board on the parapet + a flag
    const zz = TRE.z - 0.42;
    tb.add(quad(V(7, TRE.h + 0.2, zz), V(-7, TRE.h + 0.2, zz), V(-7, TRE.h + 1.9, zz), V(7, TRE.h + 1.9, zz)), signMat("TREMONT HOUSE", "#f4ead2", "#2b2830"));
    SIGN_LIST.push({ m: signMat("TREMONT HOUSE", "#f4ead2", "#2b2830"), c: [[7, TRE.h + 0.2, zz], [-7, TRE.h + 0.2, zz], [-7, TRE.h + 1.9, zz], [7, TRE.h + 1.9, zz]], which: "tre" });
    tb.add(boxGeo(V(-7.2, TRE.h + 0.1, zz + 0.02), V(7.2, TRE.h + 2.0, zz + 0.25)), trimL("#8a5a3c"));
    const pole = new THREE.CylinderGeometry(0.07, 0.07, 6, 8); pole.translate(0, TRE.h + 3, TRE.z + 6); tb.add(pole, ironM());
    tb.add(boxGeo(V(0.07, TRE.h + 4.4, TRE.z + 5.98), V(2.6, TRE.h + 5.9, TRE.z + 6.02)), lam("flagRed", () => ({ color: "#c8352e", side: THREE.DoubleSide })));
    // door canopy over the entrance
    tb.add(boxGeo(V(-1.6, 2.35, TRE.z - 1.2), V(1.6, 2.5, TRE.z)), trimL("#8a5a3c"));
    tb.build(tre);
  }
  {
    const bb = new Batch();
    block(bb, B58.x0, B58.x1, B58.z, 1, B58.d, B58.h, LOOKS[0], { y: 0, cull: false, under: true, key: "b58", sign: "DRY GOODS", signBg: "#2a3550" });
    bb.build(b58);
  }
  {
    const kb = new Batch(), rr = rng(1860);
    let x = BLK.x0, i = 0;
    for (const w of [9, 11, 9, 10, 9.5]) {
      const look = LOOKS[(i * 2 + 1) % LOOKS.length];
      block(kb, x, Math.min(BLK.x1, x + w), BLK.z, -1, BLK.d, (3 + (i % 2)) * 2.8 + 0.5, look, { y: 0, cull: false, under: true, key: "blk" + i,
        sign: i === 2 ? "BAKERY" : SHOPS[(i * 5 + 1) % SHOPS.length], signBg: SIGN_BG[i % 4], awning: i % 2 ? undefined : ["#e8d6a8", "#b8553a", "#4f7a5a"][i % 3] });
      x += w + 0.25; i++;
    }
    void rr;
    // the temporary plank porch along the raised fronts (rises with the block)
    kb.add(boxGeo(V(BLK.x0, SW - 0.22, BLK.z - 1.9), V(BLK.x1, SW + 0.025, BLK.z), 2, true), plankM()); // v21 rule 85: 2.5 cm above the plank sidewalk (coplanar boards flickered on the pan) // v8 (rule 60): porch top level with the plank sidewalk, so nobody stands sunk in it
    kb.build(blk);
  }
  tre.position.set(0, D0, 0); b58.position.set(0, D0, 0); blk.position.set(0, D0, 0);
  root.add(tre, b58, blk);
  const screws: City["screws"] = [];
  for (const [which, x0, x1, z0, z1] of [["tre", TRE.x0, TRE.x1, TRE.z, TRE.z + TRE.d], ["b58", B58.x0, B58.x1, B58.z - B58.d, B58.z], ["blk", BLK.x0, BLK.x1, BLK.z, BLK.z + BLK.d]] as const) {
    const s = screwGrid(x0 + 0.3, x1 - 0.3, z0 + 0.3, z1 - 0.3, 2.4, 2.8);
    root.add(s.g); screws.push({ g: s.cols, which });
  }
  // the Tremont's front steps (one more per 30 cm of lift), each its own mesh so world.ts can pose them
  const steps: THREE.Mesh[] = [];
  const stepM = lam("stepC", () => ({ map: stoneHD("copeHD") }));
  for (let k = 0; k < 6; k++) {
    const m = new THREE.Mesh(boxGeo(V(-1.25, 0, -0.35), V(1.25, 1, 0), 0, false, 0.004), stepM);
    m.position.set(0, D0 + SW, TRE.z - 0.35 * k); m.castShadow = true; m.receiveShadow = true;
    root.add(m); steps.push(m);
  }
  void STEP_H;
  // the sewer pipe and the street fill on the cross street (S4)
  const pipe = new THREE.Group();
  {
    const pb = new Batch();
    const c = new THREE.CylinderGeometry(SEWER.r, SEWER.r, SEWER.z1 - SEWER.z0, 24, 1, false); c.rotateX(Math.PI / 2);
    c.translate(SEWER.x, SEWER.r, (SEWER.z0 + SEWER.z1) / 2);
    pb.add(c, lam("pipeBrick", () => ({ map: rep(brick(), 6, 1) })));
    for (let z = SEWER.z0 + 2; z < SEWER.z1; z += 6) { const ring = new THREE.CylinderGeometry(SEWER.r + 0.06, SEWER.r + 0.06, 0.25, 24); ring.rotateX(Math.PI / 2); ring.translate(SEWER.x, SEWER.r, z); pb.add(ring, timberM()); }
    pb.build(pipe);
  }
  pipe.position.y = D0; root.add(pipe);
  const fill = new THREE.Mesh(boxGeo(V(SEWER.x - XH, 0, SEWER.z0 - 3), V(SEWER.x + XH, 1, SEWER.z1 + 3), 0, false, 0.004), lam("fillC", () => ({ map: mudTex("fillHD", true) })));
  fill.castShadow = true; fill.receiveShadow = true; root.add(fill);
  // puddles on Lake Street (S2 rain beat only)
  const puddles = new THREE.Group();
  {
    const pb = new Batch(), pr = rng(9);
    const pw = lam("puddleC", () => ({ color: "#7d93b5" })), ps = lam("sewageC", () => ({ color: "#6f6a3c" }));
    { const g = new THREE.CircleGeometry(1, 20); g.rotateX(-Math.PI / 2); g.scale(1.7, 1, 0.9); g.translate(31, D0 + 0.065, 99.6); pb.add(g, ps); } // the sewage pool (S2)
    for (let i = 0; i < 26; i++) {
      const x = 4 + pr() * 46, z = LAKE_Z[0] + 0.8 + pr() * (LAKE_Z[1] - LAKE_Z[0] - 1.6), rx = 0.6 + pr() * 1.4, rz = 0.4 + pr() * 0.8;
      const g = new THREE.CircleGeometry(1, 20); g.rotateX(-Math.PI / 2); g.scale(rx, 1, rz); g.translate(x, D0 + 0.06 + i * 0.002, z);
      pb.add(g, i % 5 === 0 ? ps : pw);
    }
    pb.build(puddles, false);
  }
  root.add(puddles);
  setSight([]);
  return { tre, b58, blk, screws, steps, pipe, fill, puddles, skyline: skyRing } as City;
};
