// Our cast as lit flat sprites in the 3D world. Each frame every character asks for a drawing (a key + a draw call);
// the pool keeps one canvas per distinct drawing, so soldiers marching in step share canvases (7 head shapes x 4
// outfits). Characters are yaw-only billboards shaded by cardShade() (scene tint, bright floor, side gradient toward
// the sun, painted crescent in the drawing); standing ones get a soft multiply contact blob. Effects are unlit cards.
// Cards, effects and blobs live on the NOINK layer so the world ink pass never outlines their quads.
import * as THREE from "three";
import { Pen, bodyFront, bodySide, fxBurst, fxSplash, fxRing, fxShadow, fxContact, fxPuff, Outfit, Expr, FrontOpts, SideOpts, SKINS, INK } from "./toon";
import { FPS, D0, SHOTS, V3, smooth, clamp01 } from "./story";
import { LIGHTS } from "./lights";
import { NOINK } from "./ink";
import { cardShade, blobMaterial, CARD_K } from "./cardshade";

// ---------------- canvas pool ----------------
type Entry = { cv: HTMLCanvasElement; tex: THREE.CanvasTexture; w: number; h: number };
export type Req = { key: string; w: number; h: number; k: number; draw: (p: Pen) => void; tex?: THREE.CanvasTexture };
const makeEntry = (w: number, h: number): Entry => {
  const cv = document.createElement("canvas");
  cv.width = w; cv.height = h;
  const tex = new THREE.CanvasTexture(cv);
  tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  return { cv, tex, w, h };
};
export class Pool {
  private live = new Map<string, Entry>();
  private free: Entry[] = [];
  private reqs: Req[] = [];
  req(key: string, w: number, h: number, k: number, draw: (p: Pen) => void) {
    const r: Req = { key: `${w}x${h}|${key}`, w, h, k, draw };
    this.reqs.push(r);
    return r;
  }
  flush() {
    const want = new Map<string, Req[]>();
    for (const r of this.reqs) { const l = want.get(r.key); if (l) l.push(r); else want.set(r.key, [r]); }
    for (const [key, e] of this.live) if (!want.has(key)) { this.live.delete(key); this.free.push(e); }
    for (const [key, rs] of want) {
      let e = this.live.get(key);
      if (!e) {
        const r = rs[0], i = this.free.findIndex((x) => x.w === r.w && x.h === r.h);
        e = i >= 0 ? this.free.splice(i, 1)[0] : makeEntry(r.w, r.h);
        const g = e.cv.getContext("2d")!;
        g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, e.w, e.h); g.setTransform(r.k, 0, 0, r.k, 0, 0);
        r.draw(new Pen(g));
        e.tex.needsUpdate = true;
        this.live.set(key, e);
      }
      for (const r of rs) r.tex = e.tex;
    }
    this.reqs = [];
  }
}

// ---------------- sprite meshes ----------------
const blank = (() => { const c = document.createElement("canvas"); c.width = c.height = 2; return new THREE.CanvasTexture(c); })();
export const SU = 0.00216; // metres per design unit: 1000 units = 2.16 m
export const SU_SWING = 2.3 / 1830; // swing canvas: rope of 1830 units = 2.3 m
const BODY = (() => { const g = new THREE.PlaneGeometry(600 * SU, 1000 * SU); g.translate(0, (975 - 500) * SU, 0); return g; })();
const CARD = new THREE.PlaneGeometry(1, 1);
/** world roots that hold actors (to find the scene's sun when world.ts does not pass it) */
const ROOTS = new Set<THREE.Object3D>();

/** lit flat character: cardShade() material, receives shadows (dims to the bright floor only), casts its silhouette
 *  when world.ts says so (golden). Drawn after the contact blobs (renderOrder 1). */
export class Actor {
  mesh: THREE.Mesh; mat: THREE.MeshLambertMaterial; dmat: THREE.MeshDepthMaterial; r: Req | null = null;
  constructor(parent: THREE.Object3D, geo: THREE.BufferGeometry = BODY) {
    this.mat = cardShade(new THREE.MeshLambertMaterial({ map: blank, alphaTest: 0.5, side: THREE.DoubleSide }));
    this.mat.alphaToCoverage = false; // A2C + MSAA left 1 px sky-depth seams on blurred far cards (POST)
    this.dmat = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking, map: blank, alphaTest: 0.5, side: THREE.DoubleSide });
    this.mesh = new THREE.Mesh(geo, this.mat);
    this.mesh.customDepthMaterial = this.dmat;
    // rim width is in output pixels: tell the card shader the render height (1920 = 1080 x 1920 frame)
    this.mesh.onBeforeRender = (r) => { const rt = r.getRenderTarget(); CARD_K.uPx.value = (rt ? rt.height : r.domElement.height) / 1920; };
    this.mesh.castShadow = false; this.mesh.receiveShadow = true; this.mesh.visible = false;
    this.mesh.rotation.order = "YXZ"; this.mesh.renderOrder = 1; this.mesh.layers.set(NOINK);
    parent.add(this.mesh);
    ROOTS.add(parent);
  }
  bind() { const t = this.r?.tex; if (t) { this.mat.map = t; this.dmat.map = t; } }
}
/** unlit effect card: hard cut-out (ink drawings), soft see-through (dust, mist) or a multiply ground blob */
export class Fx {
  mesh: THREE.Mesh; mat: THREE.MeshBasicMaterial; soft: THREE.MeshBasicMaterial; blob: THREE.MeshBasicMaterial; r: Req | null = null;
  constructor(parent: THREE.Object3D) {
    this.mat = new THREE.MeshBasicMaterial({ map: blank, alphaTest: 0.5, side: THREE.DoubleSide });
    this.mat.alphaToCoverage = false; // A2C + MSAA left 1 px sky-depth seams on blurred far cards (POST)
    this.soft = new THREE.MeshBasicMaterial({ map: blank, transparent: true, depthWrite: false, side: THREE.DoubleSide });
    this.blob = blobMaterial(blank);
    this.mesh = new THREE.Mesh(CARD, this.mat);
    this.mesh.visible = false; this.mesh.layers.set(NOINK);
    parent.add(this.mesh);
  }
  use(soft: boolean) { this.mesh.material = soft ? this.soft : this.mat; }
  bind() {
    const t = this.r?.tex;
    if (!t) return;
    if (this.r!.key.includes("|blob|")) {
      // no mipmaps: at grazing views the mip chain averages the blob with its white surround and it fades out
      if (t.generateMipmaps) { t.generateMipmaps = false; t.minFilter = THREE.LinearFilter; t.needsUpdate = true; }
      this.blob.map = t; this.mesh.material = this.blob; this.mesh.renderOrder = 0.5;
    }
    else { this.mat.map = t; this.soft.map = t; this.mesh.renderOrder = 0; }
  }
}

// ---------------- placements ----------------
export type Place = {
  key: string; draw: (p: Pen) => void; x: number; y: number; z: number;
  scale?: number; mirror?: boolean; yaw?: number; geo?: "body" | "swing"; roll?: number; size?: [number, number, number];
};
export type FxPlace = { key: string; cw: number; ch: number; draw: (p: Pen) => void; x: number; y: number; z: number; w: number; h: number; flat?: boolean; rot?: number; soft?: boolean; yaw?: number };
/** sun = world direction TOWARD the sun (optional: when absent the scene's shadow-casting light is used) */
export type CamInfo = { pos: THREE.Vector3; right: THREE.Vector3; sun?: THREE.Vector3 };

const hh = (i: number, s = 0) => { const v = Math.sin(i * 127.1 + s * 311.7) * 43758.5453; return v - Math.floor(v); };
const q = (v: number, n = 120) => Math.round(v * n) / n;
const vOf = (i: number) => (i * 7 + (i >> 2)) % 4;
/** head-shape seed: 7 shapes, so marching soldiers in step still share canvases */
const seedOf = (i: number) => ((i * 5 + 3) % 7) + 1;
/** drawing resolution by distance: [canvas w, h, scale from the 600 x 1000 design]; sized for the 1440 x 2560 final */
const tier = (d: number): [number, number, number] =>
  d < 3.2 ? [1800, 3000, 3.0] : d < 6.5 ? [1080, 1800, 1.8] : d < 16 ? [480, 800, 0.8] : [240, 400, 0.4];

// ---------------- light ----------------
const SUN = new THREE.Vector3(0.5, 0.75, -0.4).normalize();
const tmp = new THREE.Vector3();
let LNAME: "day" | "golden" = "day";
const sunOf = (root: THREE.Object3D) => {
  let s: THREE.DirectionalLight | null = null;
  root.traverse((o) => { if (!s && o instanceof THREE.DirectionalLight && o.castShadow) s = o; });
  return s as THREE.DirectionalLight | null;
};
/** the sun of the world that is calling: the attached root whose sun target sits on this camera's view axis */
const findSun = (cam: CamInfo, out: THREE.Vector3) => {
  if (cam.sun) return out.copy(cam.sun).normalize();
  let best: THREE.DirectionalLight | null = null, err = Infinity;
  for (const r of ROOTS) {
    if (!r.parent) continue;
    const s = sunOf(r);
    if (!s) continue;
    const d = tmp.copy(s.target.position).sub(cam.pos), e = Math.abs(d.dot(cam.right)) / (d.length() || 1);
    if (e < err) { err = e; best = s; }
  }
  return best ? out.copy(best.position).sub(best.target.position).normalize() : out;
};
/** canvas angle the sun comes FROM on an upright card facing the camera, in 45-degree steps (small texture cache) */
const light2D = (cam: CamInfo, mirror: boolean) => {
  const sx = SUN.dot(cam.right) * (mirror ? -1 : 1), sy = -SUN.y;
  return Math.round(Math.atan2(sy, sx) / (Math.PI / 4)) * (Math.PI / 4);
};

/** front / side view and mirroring for someone at (x, z) walking along (dx, dz); fs = foreshortening of the walk */
const viewOf = (cam: CamInfo, x: number, z: number, dx: number, dz: number) => {
  const tx = cam.pos.x - x, tz = cam.pos.z - z, tl = Math.hypot(tx, tz) || 1;
  const c = (tx * dx + tz * dz) / tl;
  return { side: c < 0.57, mirror: dx * cam.right.x + dz * cam.right.z < 0, fs: Math.round(Math.sqrt(Math.max(0, 1 - c * c)) * 20) / 20 };
};

// ---------------- life: blinks and reaction timing ----------------
/** reference expression and action changes land 0-3 f before the word onset */
const LEAD = 2 / FPS;
/** eyelid 0 open .. 1 shut. Reference: gaps 0.5-2.3 s, 4-frame blink half / shut / shut / half, plus a blink across
 *  every expression swap (the shut frames hide the swap) */
const LID = [0.5, 1, 1, 0.5];
const lidAt = (t: number, i: number, swaps: number[] = []) => {
  const f = Math.round(t * FPS);
  for (const ts of swaps) { const k = f - Math.round((ts - LEAD) * FPS) + 1; if (k >= 0 && k < 4) return LID[k]; }
  let s = Math.round(-60 * hh(i, 9));
  for (let n = 0; s <= f && n < 400; n++) {
    const k = f - s;
    if (k >= 0 && k < 4) return LID[k];
    s += Math.round(15 + 54 * hh(i * 31 + n, 13)); // next blink 0.5-2.3 s later
  }
  return 0;
};
const fkey = (o: object) => JSON.stringify(o, (_k, v) => (typeof v === "number" ? q(v) : v));

type Who = { i: number; o: Outfit; okey: string };
/** one character drawing in the 600 x 1000 design space, sized by distance, lit from the scene's sun */
const person = (cam: CamInfo, who: Who, x: number, y: number, z: number, view: { side: boolean; mirror: boolean }, fo: FrontOpts, so: SideOpts, scale = 1): Place & { tierKey: string } => {
  const d = cam.pos.distanceTo(tmp.set(x, y + 1.2, z)) / scale;
  const [w, h, k] = tier(d);
  const mirror = view.side && view.mirror, light = light2D(cam, mirror), seed = seedOf(who.i);
  const f2: FrontOpts = { ...fo, light, seed }, s2: SideOpts = { ...so, light, seed };
  const key = view.side ? `S|${who.okey}|${fkey(s2)}` : `F|${who.okey}|${fkey(f2)}`;
  return {
    key, x, y, z, scale, mirror, tierKey: `${w}`,
    draw: (p) => (view.side ? bodySide(p, who.o, s2) : bodyFront(p, who.o, f2)),
    size: [w, h, k],
  };
};

/** ground shadow under a standing / sitting card (review rounds 2-4), multiply, blue-violet: a TIGHT contact pool right under
 *  the feet (~.5 on screen at the core) so nobody floats, plus by day (cards cast no real shadow) a lighter soft tail
 *  stretched AWAY from the sun, length ~1.6 m / tan(sun elevation), capped. Golden: world.ts casts real card shadows. */
const CONTACT: Record<"day" | "golden", [number, number, number]> = { day: [0.2, 0.21, 0.33], golden: [0.24, 0.2, 0.33] };
const TAIL: [number, number, number] = [0.42, 0.44, 0.62];
const toSrgb = (v: number) => { const c = clamp01(v); return c <= 0.0031308 ? 12.92 * c : 1.055 * c ** (1 / 2.4) - 0.055; };
const hexOf = (c: [number, number, number], k: number) => "#" + c.map((v) => Math.round(255 * toSrgb(1 - (1 - v) * k)).toString(16).padStart(2, "0")).join("");
const blob = (out: Stage, x: number, y: number, z: number, sc = 1, k = 1) => {
  const hl = Math.hypot(SUN.x, SUN.z) || 1, ox = -SUN.x / hl, oz = -SUN.z / hl, rot = Math.atan2(-ox, -oz);
  if (LNAME === "day") {
    const el = Math.asin(Math.min(0.99, Math.max(0.1, SUN.y)));
    const len = Math.min(2.4, Math.max(0.5, 1.6 / Math.tan(el))) * sc, h = len + 0.55 * sc, c = 0.3 * h; // feet at v = .2 of the card
    const tc = hexOf(TAIL, k);
    out.fx.push({ key: `blob|shadow|${tc}`, cw: 128, ch: 256, draw: (p) => fxShadow(p, tc), x: x + ox * c, y: y + 0.018, z: z + oz * c,
      w: 0.72 * sc, h, flat: true, rot });
  }
  const cc = hexOf(CONTACT[LNAME], k);
  out.fx.push({ key: `blob|contact|${cc}`, cw: 128, ch: 128, draw: (p) => fxContact(p, cc), x: x + ox * 0.03 * sc, y: y + 0.022, z: z + oz * 0.03 * sc,
    w: 0.52 * sc, h: 0.4 * sc, flat: true, rot });
};

// ---------------- the cast of the Leaning Tower of Pisa short ----------------
export type Stage = { places: Place[]; fx: FxPlace[] };
import { fxCalendar } from "./fx3";
import { fxClip, fxClosed, fxLevel, fxSoil, fxSponge, fxCityFlag, fxBanana, fxAngle, fxTag, fxDrill, fxMound, fxTools, fxStop } from "./fx4";
import { W, World, TOWER, HOOK, BUILD, SOIL, WAR, ENG, LEAD as LEADP, STOP, TOUR, POPS, marchStart, warX } from "./story";

const ENGO = (v: number): Outfit => ({ jacket: ["#e2702c", "#3f6fb5"][v % 2], pants: "#3b3f52", boots: INK, hat: "hardhat", buttons: "#c9ccd2", skin: SKINS[v % 4], moustache: v % 2 ? undefined : "#4a3426" });
const BLD = (v: number): Outfit => ({ jacket: ["#8a6a4a", "#6b7a4a", "#a0603a"][v % 3], pants: ["#5a4a3a", "#4a4a5a"][v % 2], boots: "#4a3426", hat: "cap", cap: ["#c9b48a", "#8c2f3f", "#5a6b8a"][v % 3], skin: SKINS[(v + 1) % 4], moustache: v % 2 ? "#4a3426" : undefined, belt: "#4a3426" });
const SOLD = (city: number, v: number): Outfit => ({ jacket: ["#f1ece0", "#d23b33", "#f1ece0"][city], pants: ["#d23b33", "#f1ece0", "#d23b33"][city], boots: "#4a3426", hat: "cap", cap: "#9aa3ad", skin: SKINS[(v + city) % 4], moustache: v % 2 ? "#4a3426" : undefined, belt: "#4a3426" });
const TOURO = (v: number): Outfit => v % 2
  ? { jacket: ["#3fa0c8", "#e2453c", "#7ab648"][v % 3], pants: "#3b5b9a", boots: "#f4f2ec", hat: "sunhat", skin: SKINS[v % 4] }
  : { jacket: ["#f2c230", "#c25a7a", "#5d7a3a"][v % 3], pants: "#e8d6a8", boots: "#4a3426", hat: "cap", cap: ["#e2453c", "#3f6fb5", "#2b2830"][v % 3], skin: SKINS[(v + 2) % 4] };

const L2 = 2 / FPS;
const at = (t: number, w: number) => t >= W(w) - L2;
const who = (i: number, o: Outfit, k: string) => ({ i, o, okey: k });
const stand = (out: Stage, cam: CamInfo, t: number, w: ReturnType<typeof who>, p: V3, fo: FrontOpts, sc = 1) => {
  out.places.push(person(cam, w, p[0], p[1], p[2], { side: false, mirror: false }, { mode: "stand", blink: lidAt(t, w.i), ...fo }, {}, sc));
  blob(out, p[0], p[1], p[2], sc);
};
/** marching along +x (side view when seen from the side) */
const marchX = (out: Stage, cam: CamInfo, t: number, w: ReturnType<typeof who>, x: number, y: number, z: number, sp: number, fo: FrontOpts = {}) => {
  const phase = q(((t * sp) / 1.6 + hh(w.i, 5) * 0.05) % 1, 120), view = viewOf(cam, x, z, 1, 0);
  out.places.push(person(cam, w, x, y, z, view, { mode: "march", phase, blink: lidAt(t, w.i), ...fo }, { mode: "march", phase, stomp: 1, stride: view.fs, expr: fo.expr, blink: lidAt(t, w.i) }));
  blob(out, x, y, z);
};
const burst = (out: Stage, t: number, t0: number, x: number, y: number, z: number, s = 1) => {
  const u = (t - t0) / (5 / FPS);
  if (u < 0 || u >= 1) return;
  out.fx.push({ key: `burst${q(u, 30)}`, cw: 500, ch: 500, draw: (p) => fxBurst(p, q(u, 30)), x, y, z, w: s, h: s });
};
const puff = (out: Stage, t: number, t0: number, x: number, y: number, z: number, s = 1, dur = 0.6) => {
  const u = (t - t0) / dur;
  if (u < 0 || u >= 1) return;
  out.fx.push({ key: `puff${q(u, 30)}`, cw: 300, ch: 300, draw: (p) => fxPuff(p, q(u, 30)), x, y: y + 0.4 * s, z, w: 1.6 * s, h: 1.6 * s });
};
const flag = (out: Stage, t: number, city: 0 | 1 | 2, x: number, z: number, h = 3.2, ph = 0) =>
  out.fx.push({ key: `cflag${city}_${q((t * 3 + ph) % (Math.PI * 2), 8)}`, cw: 500, ch: 700, draw: (p) => fxCityFlag(p, city, q((t * 3 + ph) % (Math.PI * 2), 8)), x, y: D0 + h / 2, z, w: h * 0.714, h });
const card = (out: Stage, key: string, cw: number, ch: number, draw: (p: Pen) => void, x: number, y: number, z: number, w: number, rot = 0) =>
  out.fx.push({ key, cw, ch, draw, x, y, z, w, h: (w * ch) / cw, rot });
const pop = (t: number, w0: number, d = 0.18) => smooth((t - W(w0)) / d); // a card scales in on its word

export const stage = (id: number, t: number, _ws: World, cam: CamInfo): Stage => {
  const out: Stage = { places: [], fx: [] };
  const s = SHOTS[id - 1];
  LNAME = s.light;
  findSun(cam, SUN);
  const [TX, , TZ] = TOWER;
  switch (id) {
    case 1: case 2: { // closed in 1990: two engineers with clipboards in front of the barrier
      stand(out, cam, t, who(1, ENGO(0), "eng0"), [HOOK[0] - 0.9, D0, HOOK[2]], { expr: id === 2 ? (at(t, 6.0) ? "nervous" : at(t, 5.48) ? "grin" : "stern") : at(t, 3.7) ? "shock" : "stern", facing: 1 });
      stand(out, cam, t, who(2, ENGO(1), "eng1"), [HOOK[0] + 1.0, D0, HOOK[2] + 0.4], { expr: at(t, 3.7) ? "nervous" : "neutral", facing: -1 });
      card(out, "clip", 400, 520, fxClip, HOOK[0] - 0.55, D0 + 1.12, HOOK[2] - 0.3, 0.34, 0.12);
      card(out, "closed", 900, 600, fxClosed, HOOK[0] + 0.3, D0 + 0.75, HOOK[2] + 3.2, 2.3);
      break;
    }
    case 3: { // 1178: three builders at the stub; the level's bubble runs off as it starts to lean
      [[-1.0, 0.4], [0, 0], [1.05, 0.6]].forEach(([dx, dz], i) =>
        stand(out, cam, t, who(10 + i, BLD(i), "bld" + i), [BUILD[0] + dx, D0, BUILD[2] + dz], { expr: at(t, 8.34) ? (i === 1 ? "shock" : "nervous") : "smile", facing: dx < 0 ? 1 : dx > 0 ? -1 : 0 }));
      const k = smooth((t - W(8.34)) / 1.4);
      card(out, `lvl${q(k, 20)}`, 700, 200, (p) => fxLevel(p, q(k, 20) * 0.95), BUILD[0], D0 + 1.25, BUILD[2] - 0.35, 0.9);
      const sc = pop(t, 8.62);
      if (sc > 0) card(out, "cal1178", 500, 560, (p) => fxCalendar(p, "1178", 0), BUILD[0] - 3.0, D0 + 1.6, BUILD[2] - 1.2, 1.1 * sc);
      break;
    }
    case 4: { // soft clay and sand... like a wet sponge: a builder on a sponge that squishes
      if (t < W(14.74) - 0.05) card(out, "soil0", 800, 560, (p) => fxSoil(p, 0), SOIL[0] + 0.2, D0 + 1.15, SOIL[2] + 0.2, 1.9 * Math.max(0.01, pop(t, 12.32)));
      else {
        const sq = q(clamp01(0.5 + 0.5 * Math.sin((t - W(15.4)) * 9)) * smooth((t - W(15.4)) / 0.2), 12);
        card(out, `sponge${sq}`, 700, 400, (p) => fxSponge(p, sq), SOIL[0] + 0.2, D0 + 0.4, SOIL[2] + 0.3, 1.8);
        stand(out, cam, t, who(11, BLD(1), "bld1"), [SOIL[0] + 0.2, D0 + 0.62 - 0.28 * sq, SOIL[2] + 0.2], { expr: sq > 0.3 ? "shock" : "nervous", facing: 0 });
      }
      break;
    }
    case 5: { // three armies march across with their flags; the builders drop their tools and follow
      if (t < W(20.1) - 0.05) {
        for (let g = 0; g < 3; g++) {
          if (t < marchStart(g)) continue;
          const x0 = warX(t, g), z0 = WAR[2] + 3.0 * g - 2.0;
          for (let k = 0; k < 3; k++) marchX(out, cam, t, who(30 + g * 3 + k, SOLD(g, k), `s${g}${k}`), x0 - k * 1.3, D0, z0 + (k % 2) * 0.5, 1.2, { expr: "stern" });
          flag(out, t, g as 0 | 1 | 2, x0 + 0.7 - 0.9 * g, z0 - 0.3, 2.9 + 0.7 * g, g);
        }
        [[-3.0, 2.5], [3.2, 3.0]].forEach(([dx, dz], i) => stand(out, cam, t, who(10 + i, BLD(i), "bld" + i), [BUILD[0] + dx, D0, BUILD[2] + dz - 10], { expr: at(t, 19.8) ? "shock" : "nervous", facing: 0 }));
      } else {
        card(out, "tools", 700, 260, fxTools, BUILD[0] + 0.1, D0 + 0.22, BUILD[2] + 1.0, 1.7);
        const fl = clamp01((t - W(21.26)) / 0.4), yr = fl >= 1 ? "1272" : "1178";
        card(out, `cal${yr}${q(fl, 10)}`, 500, 560, (p) => fxCalendar(p, yr, fl > 0 && fl < 1 ? q(fl, 10) : 0), BUILD[0] - 1.0, D0 + 1.05, BUILD[2] + 2.2, 0.9);
      }
      break;
    }
    case 6: { // luckily: nobody builds, the ground packs down
      if (t >= W(25.56) - 0.05) { const k = q(smooth((t - W(25.9)) / 1.4), 12); card(out, `soilp${k}`, 800, 560, (p) => fxSoil(p, k), SOIL[0] + 0.2, D0 + 1.15, SOIL[2] + 0.2, 1.9); }
      break;
    }
    case 7: { // the builders come back and stack crooked floors
      if (at(t, 28.82)) [[-2.2, 0], [0, 0.6], [2.2, 0.2]].forEach(([dx, dz], i) => {
        const x = Math.min(BUILD[0] + dx, BUILD[0] + dx - 12 + 8 * (t - W(28.82)));
        if (x < BUILD[0] + dx) marchX(out, cam, t, who(10 + i, BLD(i), "bld" + i), x, D0, BUILD[2] - 12 + dz, 1.1, { expr: "grin" });
        else stand(out, cam, t, who(10 + i, BLD(i), "bld" + i), [x, D0, BUILD[2] - 12 + dz], { expr: "grin", facing: 0, wave: i === 1 && at(t, 31.4) ? 0.8 : undefined });
      });
      for (const p of POPS) if (t >= p && t < p + 0.6) puff(out, t, p, TX + 3 + 2 * POPS.indexOf(p), D0 + 24 + 6.8 * POPS.indexOf(p), TZ - 6, 4.5, 0.6);
      break;
    }
    case 8: { // like a banana
      const sc = pop(t, 37.4, 0.22);
      if (sc > 0) card(out, "banana", 400, 1000, fxBanana, TX + 12, D0 + 11.5 * sc, TZ - 4, 9 * sc);
      break;
    }
    case 9: { // 1990: engineers measure five and a half degrees
      stand(out, cam, t, who(1, ENGO(0), "eng0"), [ENG[0] - 0.9, D0, ENG[2]], { expr: at(t, 39.46) ? "shock" : "stern", facing: 1 });
      stand(out, cam, t, who(2, ENGO(1), "eng1"), [ENG[0] + 1.0, D0, ENG[2] + 0.4], { expr: "nervous", facing: -1 });
      card(out, "clip", 400, 520, fxClip, ENG[0] - 0.55, D0 + 1.12, ENG[2] - 0.3, 0.34, 0.12);
      const sc = pop(t, 39.46);
      if (sc > 0) card(out, "ang55", 600, 600, (p) => fxAngle(p, "5.5°"), ENG[0] + 0.1, D0 + 2.75, ENG[2] + 0.6, 1.25 * sc);
      break;
    }
    case 10: { // 870 tons of lead on the high side
      stand(out, cam, t, who(1, ENGO(0), "eng0"), [LEADP[0] - 4.2, D0, LEADP[2] - 5.0], { expr: at(t, 43.38) ? "grin" : "stern", facing: 1, wave: at(t, 43.98) ? 0.8 : undefined });
      const sc = pop(t, 41.92);
      if (sc > 0) card(out, "t870", 800, 360, (p) => fxTag(p, "870 TONS", "#c9ccd2"), LEADP[0] - 2.5, D0 + 7.2, LEADP[2] - 3, 3.2 * sc);
      break;
    }
    case 11: { // drills pull the soil out from under the high side, a little at a time
      for (const [dx, dz, ph] of [[-3.2, -3.4, 0], [-1.0, -6.0, 0.5]]) {
        const sp = q((t * 2.4 + ph) % 1, 12);
        card(out, `drill${sp}`, 500, 800, (p) => fxDrill(p, sp), LEADP[0] + dx, D0 + 1.6, LEADP[2] + dz, 2.0);
      }
      const m = clamp01((t - W(45.12)) / 3);
      card(out, `mound${q(m, 6)}`, 500, 300, fxMound, LEADP[0] - 5.2, D0 + 0.3 + 0.35 * m, LEADP[2] - 5.4, 1.0 + 1.2 * q(m, 6));
      stand(out, cam, t, who(1, ENGO(0), "eng0"), [LEADP[0] - 6.4, D0, LEADP[2] - 4.0], { expr: "stern", facing: 1, prop: ["hold", "shovel", q((t * 1.2) % 1, 20)] });
      if (at(t, 45.82)) puff(out, t, W(45.82), LEADP[0] - 3.0, D0, LEADP[2] - 3.2, 1.0);
      if (at(t, 47.34)) puff(out, t, W(47.34), LEADP[0] - 0.9, D0, LEADP[2] - 5.8, 1.0);
      break;
    }
    case 12: { // it settles back 45 cm, to how it leaned in 1838
      const a = pop(t, 50.4), b = pop(t, 52.2);
      if (a > 0 && b < 1) card(out, "t45", 800, 360, (p) => fxTag(p, "45 cm"), TX - 5, D0 + 44, TZ - 8, 11 * a);
      if (b > 0) card(out, "t1838", 800, 360, (p) => fxTag(p, "1838", "#f4ead2"), TX - 5, D0 + 44, TZ - 8, 11 * b);
      break;
    }
    case 13: { // they stopped on purpose / a straight tower is just a tower
      if (t < W(55.56) - 0.05) {
        stand(out, cam, t, who(2, ENGO(1), "eng1"), STOP, { expr: at(t, 55.16) ? "smile" : "stern", facing: 0, wave: 0.85 });
        if (at(t, 54.36)) card(out, "stop", 400, 500, fxStop, STOP[0] + 0.5, D0 + 1.72, STOP[2] - 0.3, 0.48 * pop(t, 54.36, 0.12));
      } else {
        [[-1.6, 0.4], [0, 0], [1.6, 0.5]].forEach(([dx, dz], i) =>
          stand(out, cam, t, who(60 + i, TOURO(i), "tour" + i), [TOUR[0] + dx, D0, TOUR[2] + dz], { expr: i === 1 ? "pained" : "neutral", facing: dx < 0 ? 1 : dx > 0 ? -1 : 0, prop: i === 2 ? ["hold", "camera", 0] : null }));
      }
      break;
    }
    case 14: { // reopened in 2001: tourists hold it up for the photo
      [[-1.8, 0.5], [0, 0], [1.9, 0.6]].forEach(([dx, dz], i) =>
        stand(out, cam, t, who(60 + i, TOURO(i), "tour" + i), [TOUR[0] + dx, D0, TOUR[2] + dz], { expr: i === 1 ? "grin" : "smile", facing: dx < 0 ? 1 : dx > 0 ? -1 : 0,
          wave: i !== 1 ? 0.95 : undefined, prop: i === 1 ? ["hold", "camera", 0] : null }));
      const sc = pop(t, 59.66);
      if (sc > 0 && t < W(62.4)) card(out, "y2001", 800, 360, (p) => fxTag(p, "2001", "#f4ead2"), TOUR[0] + 0.2, D0 + 3.1, TOUR[2] + 1.0, 1.7 * sc);
      break;
    }
  }
  return out;
};
export { FPS };
