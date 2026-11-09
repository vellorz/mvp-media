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

// ---------------- the cast of the London Bridge short ----------------
export type Stage = { places: Place[]; fx: FxPlace[] };
import { fxBus, fxCar, fxHonk, fxForSale, fxBag, fxThought, fxTumble, fxBubble, fxFoam } from "./fx2";
import { W, HW, MAC1, MAC5, MAC17, SIGN_AT, OFFICIAL, DEAL_O, DEAL_M, BAG, BAG_T, HITS, PILE, ROAD_Z, FISHER, FRAMER, BUILD_T, truckX, shipX, World, pieceRange } from "./story";

const MAC: Outfit = { jacket: "#c8a46a", pants: "#6b5a45", boots: "#4a3426", hat: "cowboy", buttons: "#e8c45a", skin: SKINS[1] };
const OFF: Outfit = { jacket: "#2b2f3a", pants: "#2b2f3a", boots: INK, hat: "bowler", moustache: "#4a3020", build: "stout", buttons: "#e8c45a", skin: SKINS[0] };
const SUITS = ["#3b4256", "#5a5f6b", "#6b4f3a", "#2f3b52", "#4a5a4a"];
const londoner = (v: number): Outfit => v % 3 === 2
  ? { jacket: ["#f1e4c8", "#e8b0a0", "#b8d0e8"][v % 3], pants: "#3b3f52", boots: "#4a3426", hat: "hair", hair: ["#5a3b2a", "#d9a441", "#2a201a"][v % 3], dress: ["#d94f5c", "#3f8fb5", "#e2a13c"][v % 3], skin: SKINS[v % 4] }
  : { jacket: SUITS[v % 5], pants: SUITS[(v + 2) % 5], boots: INK, hat: "bowler", skin: SKINS[v % 4], moustache: v % 4 === 1 ? "#4a3426" : undefined };
const worker = (v: number): Outfit => ({ jacket: ["#e8752e", "#3f6fb5", "#d9a441", "#5d7a3a"][v % 4], pants: "#3b4a6b", boots: "#5a3b2a", hat: "hardhat", skin: SKINS[(v + 1) % 4], moustache: v % 3 === 1 ? "#4a3426" : undefined });
const tourist = (v: number): Outfit => ({ jacket: ["#2fb5a5", "#e85a7a", "#f2c230", "#7b5ac9", "#f08a2c"][v % 5], pants: ["#d8c49a", "#3b5b9a", "#f1e4c8"][v % 3], boots: "#f4f1ea",
  hat: v % 2 ? "sunhat" : "cap", cap: "#e2453c", skin: SKINS[v % 4] });
const FISH: Outfit = { jacket: "#5d7a3a", pants: "#6b5a45", boots: "#4a3426", hat: "bucket", cap: "#8f8a5c", skin: SKINS[2], moustache: "#4a3426" };
const FRAMEL: Outfit = { jacket: "#f1e4c8", pants: "#3b3f52", boots: "#8c3b4a", hat: "sunhat", dress: "#d94f5c", skin: SKINS[1] };

const L2 = 2 / FPS;
const at = (t: number, w: number) => t >= W(w) - L2;
/** one standing / strolling person; i = blink + head seed, k = outfit key */
const who = (i: number, o: Outfit, k: string) => ({ i, o, okey: k });
const stand = (out: Stage, cam: CamInfo, t: number, w: ReturnType<typeof who>, p: V3, fo: FrontOpts, sc = 1) => {
  out.places.push(person(cam, w, p[0], p[1], p[2], { side: false, mirror: false }, { mode: "stand", blink: lidAt(t, w.i), ...fo }, {}, sc));
  blob(out, p[0], p[1], p[2], sc);
};
const stroll = (out: Stage, cam: CamInfo, t: number, w: ReturnType<typeof who>, x: number, y: number, z: number, dz: number, sp: number, fo: FrontOpts = {}) => {
  const phase = q(((t * sp) / 1.4 + hh(w.i, 5)) % 1, 120), view = viewOf(cam, x, z, 0, dz);
  out.places.push(person(cam, w, x, y, z, view, { mode: "stroll", phase, blink: lidAt(t, w.i), ...fo }, { mode: "march", phase, stomp: 0.55, stride: 0.875 * view.fs, expr: fo.expr, blink: lidAt(t, w.i) }));
  blob(out, x, y, z);
};
const puff = (out: Stage, t: number, t0: number, x: number, y: number, z: number, s = 1, dur = 0.6) => {
  const u = (t - t0) / dur;
  if (u < 0 || u >= 1) return;
  out.fx.push({ key: `puff${q(u, 30)}`, cw: 300, ch: 300, draw: (p) => fxPuff(p, q(u, 30)), x, y: y + 0.4 * s, z, w: 1.6 * s, h: 1.6 * s });
};
const burst = (out: Stage, t: number, t0: number, x: number, y: number, z: number, s = 1) => {
  const u = (t - t0) / (5 / FPS);
  if (u < 0 || u >= 1) return;
  out.fx.push({ key: `burst${q(u, 30)}`, cw: 500, ch: 500, draw: (p) => fxBurst(p, q(u, 30)), x, y, z, w: s, h: s });
};
const hammerK = (t: number) => {
  let k = 1;
  for (const th of HITS) { const n = (t - th) * FPS; if (n >= -11 && n < -7) k = Math.min(k, 1 - smooth((n + 11) / 4)); else if (n >= -7 && n < 0) k = 0; }
  return k;
};
const CAR_COLS = ["#3f8fb5", "#e2a13c", "#5d7a3a", "#f1e4c8", "#8c3b4a", "#2f5f6a"];
/** London traffic jam on the bridge: cards facing +x (the camera side), crawling */
const traffic = (out: Stage, t: number) => {
  for (let lane = 0; lane < 2; lane++) {
    const dir = lane ? 1 : -1, x = lane ? 2.0 : -2.0;
    for (let k = 0; k < 7; k++) {
      const bus = (k + lane) % 3 === 0, len = bus ? 8.6 : 4.3, gap = 1.4;
      const z = -34 + k * 10 + lane * 4 + dir * 0.4 * Math.max(0, Math.sin(t * 0.9 + k));
      const h = bus ? 4.8 : 2.2, w = len * (dir > 0 ? -1 : 1); // canvas faces screen-right = world -z
      if (bus) out.fx.push({ key: "bus", cw: 1000, ch: 560, draw: fxBus, x, y: D0 + h / 2, z, w, h, yaw: Math.PI / 2 });
      else { const col = CAR_COLS[(k * 3 + lane) % CAR_COLS.length]; out.fx.push({ key: "car" + col, cw: 700, ch: 360, draw: (p) => fxCar(p, col), x, y: D0 + h / 2 - 0.05, z, w, h: h * 1.0, yaw: Math.PI / 2 }); }
      void gap;
    }
  }
  // honks
  for (const [t0, z] of [[W(11.6), -12], [W(12.2), 2], [W(12.6), -21]] as const) {
    const u = (t - t0) / 0.5;
    if (u >= 0 && u < 1) out.fx.push({ key: `honk${q(u, 30)}`, cw: 300, ch: 300, draw: (p) => fxHonk(p, q(u, 30)), x: 4, y: D0 + 3.6, z, w: 1.4, h: 1.4 });
  }
};
const crowd = (out: Stage, cam: CamInfo, t: number, spots: [number, number][], y: number, expr: (i: number) => Expr, i0 = 0) =>
  spots.forEach(([x, z], i) => stand(out, cam, t, who(i0 + i, londoner(i0 + i), "l" + ((i0 + i) % 15)), [x, y, z], { expr: expr(i), facing: 0 }));

export const stage = (id: number, t: number, ws: World, cam: CamInfo): Stage => {
  const out: Stage = { places: [], fx: [] };
  const s = SHOTS[id - 1];
  LNAME = s.light;
  findSun(cam, SUN);
  switch (id) {
    case 1: {
      stand(out, cam, t, who(1, MAC, "mac"), MAC1, { expr: t < W(2.3) ? "smile" : "grin", facing: -1 });
      const u = (t - 3.4) / 2.5;
      if (u > 0 && u < 1) out.fx.push({ key: "tumble", cw: 300, ch: 300, draw: fxTumble, x: 30 - 40 * u, y: D0 + 0.55 + 0.25 * Math.abs(Math.sin(u * 12)), z: -40, w: 1.1, h: 1.1, rot: -u * 14 });
      break;
    }
    case 2: {
      for (let i = 0; i < 10; i++) stroll(out, cam, t, who(40 + i, londoner(i), "l" + i), (i % 2 ? 5.1 : -5.1), D0 + 0.14, -26 + i * 5.5, i % 2 ? 1 : -1, 0.6 + hh(i) * 0.4, { expr: "neutral" });
      traffic(out, t);
      break;
    }
    case 3: {
      traffic(out, t);
      for (let i = 0; i < 8; i++) {
        const z = -20 + i * 4 + (i % 2 ? 1 : -1) * 0.5 * (t - 10.3);
        stroll(out, cam, t, who(60 + i, londoner(i + 3), "l" + ((i + 3) % 15)), 5.15, D0 + 0.14, z, i % 2 ? 1 : -1, 0.6 + hh(i, 3) * 0.4, { expr: at(t, 12.1) ? "nervous" : "neutral", look: 0 });
      }
      if (t > W(12.9)) for (let k = 0; k < 10; k++) { // bubbles at the sinking pier
        const u = ((t * 0.9 + hh(k, 4) * 3) % 1.4) / 1.4, x = 7.4 + hh(k) * 1.5, z = -7.4 + hh(k, 2) * 2.6;
        out.fx.push({ key: "bubble", cw: 120, ch: 120, draw: fxBubble, x, y: -0.05 + u * 0.35, z, w: 0.22 * (0.5 + u), h: 0.22 * (0.5 + u) });
        out.fx.push({ key: `ring${q(u, 30)}`, cw: 600, ch: 600, draw: (p) => fxRing(p, q(u, 30)), x, y: 0.03, z, w: 1.4, h: 1.4, flat: true });
      }
      break;
    }
    case 4: {
      const shock = (i: number): Expr => (at(t, 16.24) && t < W(17.4) ? (i % 2 ? "shock" : "nervous") : at(t, 17.4) ? (i % 3 ? "shock" : "dazed") : "neutral");
      crowd(out, cam, t, [[0.2, -33.6], [-1.3, -34.6], [4.9, -33.9], [6.1, -35.2], [-1.8, -37.8], [5.4, -37.3], [-2.6, -36.2]], D0, shock, 20);
      const sign = at(t, 17.6);
      if (sign) out.fx.push({ key: "forsale", cw: 600, ch: 900, draw: fxForSale, x: SIGN_AT[0], y: D0 + 1.1, z: SIGN_AT[2], w: 1.45, h: 2.2, rot: t < HITS[0] + 0.05 ? 0.12 : t < HITS[1] + 0.05 ? 0.06 : 0 });
      stand(out, cam, t, who(99, OFF, "off"), OFFICIAL, { expr: "stern", prop: ["hammer", q(hammerK(t), 30)], facing: 1 });
      for (const h of HITS) burst(out, t, h, 2.85, D0 + 1.7, -31.0, 0.9);
      break;
    }
    case 5: {
      const rev = at(t, 21.68);
      stand(out, cam, t, who(1, MAC, "mac"), MAC5, { expr: at(t, 20.6) ? "grin" : "smile", prop: ["hold", "chainsaw", rev ? q(t, 30) : 0], facing: 0 });
      if (rev) for (let k = 0; k < 4; k++) puff(out, t, W(21.68) + k * 0.35, MAC5[0] + 0.55, D0 + 0.9, MAC5[2] - 0.1, 0.45, 0.5);
      crowd(out, cam, t, [[-2.6, -6.5], [3.4, -4.8], [-4.3, -2.0]], D0 + 0.14, () => (rev ? "shock" : "neutral"), 30);
      break;
    }
    case 7: {
      const land = t >= BAG_T;
      stand(out, cam, t, who(99, OFF, "off"), DEAL_O, { expr: !land ? "smile" : t < BAG_T + 0.5 ? "shock" : "grin", facing: 1 });
      stand(out, cam, t, who(1, MAC, "mac"), DEAL_M, { expr: t < BAG_T - 1.3 ? "laugh" : t < BAG_T - 0.4 ? "shock" : "grin", facing: -1 });
      const fall = clamp01((t - (BAG_T - 0.45)) / 0.45), y = D0 + 3.6 * (1 - fall * fall), sq = land ? Math.max(0, 1 - (t - BAG_T) / 0.18) : 0;
      if (t > BAG_T - 0.45) out.fx.push({ key: `bag${q(sq, 10)}`, cw: 400, ch: 440, draw: (p) => fxBag(p, q(sq, 10)), x: BAG[0], y: y + 0.54, z: BAG[2], w: 1.0, h: 1.1 });
      puff(out, t, BAG_T, BAG[0], D0, BAG[2] - 0.2, 1.3, 0.7);
      burst(out, t, BAG_T, BAG[0], D0 + 0.4, BAG[2] - 0.3, 1.4);
      break;
    }
    case 8: {
      // workers at the cut end of the bridge (pieces 0-4 stand: the end is at z = 4.8), and at the stone pile
      const zc = pieceRange(ws.pieces[1] - 1)[1] - 1.2;
      [[-3.2, zc], [-0.6, zc - 0.6], [2.6, zc - 0.2]].forEach(([x, z], i) =>
        stand(out, cam, t, who(70 + i, worker(i), "w" + i), [x, D0, z], { expr: "stern", prop: ["hammer", q(((t * 1.6 + i * 0.33) % 1) < 0.7 ? 1 : 0, 2)], facing: 0 }));
      stand(out, cam, t, who(74, worker(3), "w3"), [PILE[0] + 0.3, D0, PILE[2] + 1.2], { expr: at(t, 30.1) ? "grin" : "neutral", prop: ["hold", "brush", q(t * 1.3, 30)], facing: -1 });
      stand(out, cam, t, who(75, worker(1), "w1"), [PILE[0] + 4.2, D0, PILE[2] + 1.9], { expr: "smile_closed", facing: 0 });
      break;
    }
    case 9: {
      const x = shipX(t);
      for (const [dx, dz, s2] of [[22, -4.4, 1], [22, 4.4, 1], [-23, 0, 1.6]] as const)
        out.fx.push({ key: `foam${q(t % 2, 10)}`, cw: 600, ch: 200, draw: (p) => fxFoam(p, q(t % 2, 10)), x: x + dx - (dx < 0 ? 10 : 2), y: 0.05, z: dz, w: 14 * s2, h: 4.5 * s2, flat: true });
      break;
    }
    case 10: {
      for (let k = 0; k < 3; k++) for (let n = 0; n < 4; n++) {
        const t0 = Math.floor(t * 3) / 3 - n * 0.18;
        puff(out, t, t0, truckX(t0, k) - 4, D0, ROAD_Z + (k % 2 ? 1.6 : -1.6), 1.4, 0.9);
      }
      break;
    }
    case 11: {
      BUILD_T.forEach((b, i) => { const [z0, z1] = pieceRange(i); puff(out, t, b, 6.8, D0 - 0.5, (z0 + z1) / 2, 2.4, 0.7); });
      break;
    }
    case 12: {
      stand(out, cam, t, who(1, MAC, "mac"), [0.4, D0, -17.5], { expr: at(t, 39.9) ? "laugh" : "grin", wave: at(t, 39.6) ? q(Math.sin(t * 9), 30) : undefined, facing: 0 });
      [[-2.6, -16.4], [2.8, -16.2], [-1.4, -14.4], [1.8, -14.0]].forEach(([x, z], i) =>
        stand(out, cam, t, who(70 + i, worker(i), "w" + i), [x, D0, z], { expr: i % 2 ? "laugh" : "grin", wave: at(t, 39.7) && i % 2 === 0 ? q(Math.sin(t * 8 + i), 30) : undefined, facing: 0 }));
      break;
    }
    case 13: {
      const sad = at(t, 43.58);
      stand(out, cam, t, who(80, FISH, "fish"), [FISHER[0], ws.fill, FISHER[2]], { expr: !sad ? "smile_closed" : at(t, 45.3) ? "neutral" : "nervous", prop: ["hold", "rod", q(Math.sin(t * 2) * 0.5, 20)], facing: -1 });
      const u = (t - W(44.6)) / 1.9;
      if (u > 0 && u < 1) out.fx.push({ key: "tumble", cw: 300, ch: 300, draw: fxTumble, x: FISHER[0] + 9 - 16 * u, y: ws.fill + 0.45 + 0.2 * Math.abs(Math.sin(u * 10)), z: FISHER[2] - 2.2, w: 0.9, h: 0.9, rot: u * 12 });
      break;
    }
    case 14: {
      const y = ws.fill;
      [[0.5, -2.8], [3.2, -1.2], [5.6, -3.0], [1.4, 1.6], [4.6, 2.4], [-1.8, 0.2]].forEach(([x, z], i) => {
        const ph = (t * 1.1 + hh(i, 6)) % 1;
        stand(out, cam, t, who(70 + i, worker(i), "w" + (i % 4)), [x, y, z], { expr: i % 2 ? "stern" : "smile_closed", prop: ["hold", "shovel", q(ph, 12)], facing: 0 });
        puff(out, t, Math.floor(t * 1.1 + hh(i, 6)) / 1.1 - hh(i, 6) / 1.1 + 0.35, x + 0.6, y, z - 0.2, 0.9, 0.6);
      });
      if (ws.water > -5) for (let k = 0; k < 6; k++) {
        const u = ((t * 2 + k * 0.17) % 1);
        out.fx.push({ key: `splash${q(u, 30)}`, cw: 800, ch: 800, draw: (p) => fxSplash(p, q(u, 30)), x: Math.max(ws.front, -60) + 3, y: 3.2, z: -25 + k * 10, w: 10, h: 10 });
      }
      break;
    }
    case 15: {
      stand(out, cam, t, who(85, FRAMEL, "framel"), FRAMER, { expr: at(t, 53.24) ? "grin" : "smile_closed", prop: ["hold", "frame", 0], facing: 0 });
      break;
    }
    case 16: {
      for (let i = 0; i < 18; i++) {
        const sp = 0.55 + hh(i) * 0.5, x = (i % 2 ? 1 : -1) * (1 + hh(i, 3) * 3.6), z = -4 + (i / 18) * 30 + hh(i, 2) * 1.5 - sp * (t - 54) * (i % 3 ? 1 : -1);
        const prop = i % 5 === 1 ? (["hold", "camera", 0] as const) : null;
        stroll(out, cam, t, who(100 + i, tourist(i), "t" + (i % 10)), x, D0, z, i % 3 ? -1 : 1, sp, { expr: (["smile", "grin", "smile_closed", "laugh"] as Expr[])[i % 4], prop: prop as FrontOpts["prop"] });
      }
      break;
    }
    case 17: {
      const deny = at(t, 62.86), shake = deny && t < W(63.7) ? 6 * Math.sin((t - W(62.86)) * 26) : 0;
      // "McCulloch sold them land while they were there": the FOR SALE sign is back, now in the desert
      if (t * FPS < SALE_UNTIL_OLD) out.fx.push({ key: "forsale", cw: 600, ch: 900, draw: fxForSale, x: MAC17[0] + 1.15, y: D0 + 1.1, z: MAC17[2] + 0.3, w: 1.3, h: 1.95 });
      stand(out, cam, t, who(1, MAC, "mac"), MAC17, { expr: deny ? "stern" : at(t, 61.6) ? "grin" : "smile", headTilt: q(shake, 2), facing: 0 });
      const t0 = W(61.0), t1 = W(62.86);
      if (t > t0 && t < t1) {
        const g = Math.min(1, (t - t0) / 0.3), s2 = g < 1 ? 1.15 * Math.sin(g * Math.PI * 0.75) / Math.sin(Math.PI * 0.75) : 1;
        out.fx.push({ key: "thought", cw: 760, ch: 640, draw: fxThought, x: MAC17[0] - 0.95, y: D0 + 3.15, z: MAC17[2] + 0.2, w: 1.5 * s2, h: 1.26 * s2 });
      }
      burst(out, t, t1, MAC17[0] - 0.95, D0 + 3.15, MAC17[2] + 0.2, 1.8);
      break;
    }
  }
  return out;
};
export { FPS, HW, MAC17, ROAD_Z };
import { SALE_UNTIL_OLD } from "./remap";
