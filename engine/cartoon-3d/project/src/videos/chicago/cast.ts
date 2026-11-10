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
    out.fx.push({ key: `blob|shadow|${tc}`, cw: 128, ch: 256, draw: (p) => fxShadow(p, tc), x: x + ox * c, y: y + 0.05, z: z + oz * c,
      w: 0.72 * sc, h, flat: true, rot });
  }
  const cc = hexOf(CONTACT[LNAME], k);
  out.fx.push({ key: `blob|contact|${cc}`, cw: 128, ch: 128, draw: (p) => fxContact(p, cc), x: x + ox * 0.03 * sc, y: y + 0.055, z: z + oz * 0.03 * sc,
    w: 0.52 * sc, h: 0.4 * sc, flat: true, rot });
};

// ---------------- the cast of the Chicago short ----------------
export type Stage = { places: Place[]; fx: FxPlace[] };
import { fxCalendar } from "./fx3";
import { fxWindow, fxGlass, fxLabel, fxPlan, fxRuler, fxRain, fxStink, fxOpen, fxLoaf, fxCouch, fxCouchBack, fxCouchFront, fxJack, fxLever, fxSleeper, fxArrow, fxTally, fxEasel, fxPosts } from "./fx5";
import { TABLES, TEA, PULL2, STA, PLAT } from "./story";
import { W, World, SW, TRE, B58, BLK, SEWER, treWin, ONLOOK, STUCK, DOC, ENG, SHOP, GUEST, COUCH, PULL, DAYS, lift, fillTop, flowPos, arrowYaw, FLIP_T } from "./story";
import { townsfolk, KID } from "./toon";

const Y = D0 + SW;
const WORK = (v: number): Outfit => ({ jacket: ["#8a6a4a", "#6b7a4a", "#a0603a", "#4f6a8a"][v % 4], pants: ["#5a4a3a", "#4a4a5a"][v % 2], boots: "#4a3426", hat: "cap",
  cap: ["#c9b48a", "#8c2f3f", "#5a6b8a", "#3b3f52"][v % 4], skin: SKINS[(v + 1) % 4], moustache: v % 3 === 1 ? "#4a3426" : undefined, belt: "#4a3426" });
const DOCO: Outfit = { jacket: "#2b2830", pants: "#3b3f52", boots: INK, hat: "tophat", moustache: "#5a4030", buttons: "#c9ccd2", skin: SKINS[0] };
const ENGO: Outfit = { jacket: "#3f4a6b", pants: "#4a4a5a", boots: INK, hat: "tophat", beard: "#6a4a30", buttons: "#d9b04a", skin: SKINS[1] };
const PULLO: Outfit = { jacket: "#5d7a3a", pants: "#3b3f52", boots: "#4a3426", hat: "bowler", buttons: "#d9b04a", skin: SKINS[0] };
const GUESTO: Outfit = { jacket: "#7b5ac9", pants: "#3b3f52", boots: "#4a3426", hat: "tophat", moustache: "#4a3426", buttons: "#d9b04a", skin: SKINS[2] };
const WIN_A: Outfit = { jacket: "#7b5ac9", pants: "#3b3f52", boots: "#4a3426", hat: "hair", hair: "#5a3b2a", moustache: "#4a3426", buttons: "#d9b04a", skin: SKINS[2] };
const WIN_B: Outfit = { jacket: "#c25a7a", pants: "#3b3f52", boots: "#4a3426", hat: "hair", hair: "#2a201a", dress: "#c25a7a", skin: SKINS[1] };
const WIN_C: Outfit = { jacket: "#2f6a43", pants: "#3b3f52", boots: "#4a3426", hat: "hair", hair: "#8a5a3c", buttons: "#d9b04a", skin: SKINS[3] };
const BAKER: Outfit = { jacket: "#f4f2ec", pants: "#4a4a5a", boots: "#4a3426", hat: "cap", cap: "#f4f2ec", moustache: "#4a3426", belt: "#c9b48a", skin: SKINS[1] };
const MOM: Outfit = { jacket: "#3f6fb5", pants: "#3b3f52", boots: "#4a3426", hat: "bonnet", dress: "#5a8fc2", skin: SKINS[0] };
const DAD: Outfit = { jacket: "#8c3b4a", pants: "#3b3f52", boots: "#4a3426", hat: "tophat", moustache: "#4a3426", skin: SKINS[0] };

const L2 = 2 / FPS;
/** chair k (0 = far side, 1 = near side) at dining table i: the seat a guest sits on */
/** table 1 guests sit side-on to the S8a camera (rule 40): their chairs are drawn on their profile cards (sets.ts has none there) */
const DINE_A = 0.81;
const chairAt = (i: number, k: number): V3 => { const a = (i === 1 ? DINE_A : Math.PI * 0.5 + i) + k * Math.PI, r = i === 1 ? 0.95 : 0.85; return [TABLES[i][0] + Math.cos(a) * r, D0, TABLES[i][1] + Math.sin(a) * r]; };
const towardTable = (i: number, k: number): [number, number] => { const a = DINE_A + k * Math.PI; return [-Math.cos(a), -Math.sin(a)]; };
/** the street crowd: bystanders on the south sidewalk of Lake Street (and a few in the road) */
const CROWD: [number, number, number][] = [[-14.5, 103.2, 0], [-11.2, 102.4, 1], [-8.4, 104.0, 2], [-4.0, 102.6, 3], [-0.6, 103.8, 4], [3.6, 102.2, 5], [7.8, 103.6, 6], [11.4, 102.6, 7], [-6.2, 100.4, 8], [5.8, 99.8, 9]];
const crowd = (out: Stage, cam: CamInfo, t: number, base: number, n = CROWD.length) => CROWD.slice(0, n).forEach(([x, z, v], k) =>
  stand(out, cam, t, who(base + k, townsfolk(v), "crowd" + v), [x, z < 97 ? D0 + SW : D0, z], { expr: (["smile", "shock", "neutral", "grin"] as Expr[])[(k + Math.floor(t / 1.7)) % 4], facing: x < 0 ? 1 : -1, wave: k === 3 && Math.floor(t) % 3 === 0 ? 0.8 : undefined }));

const at = (t: number, w: number) => t >= W(w) - L2;
const who = (i: number, o: Outfit, k: string) => ({ i, o, okey: k });
const stand = (out: Stage, cam: CamInfo, t: number, w: ReturnType<typeof who>, p: V3, fo: FrontOpts, sc = 1) => {
  out.places.push(person(cam, w, p[0], p[1], p[2], { side: false, mirror: false }, { mode: "stand", blink: lidAt(t, w.i), ...fo }, {}, sc));
  blob(out, p[0], p[1], p[2], sc);
};
const sit = (out: Stage, cam: CamInfo, t: number, w: ReturnType<typeof who>, p: V3, fo: FrontOpts, sc = 1, shadow = true) => {
  out.places.push(person(cam, w, p[0], p[1], p[2], { side: false, mirror: false }, { mode: "sit", blink: lidAt(t, w.i), ...fo }, {}, sc));
  if (shadow) blob(out, p[0], p[1], p[2], sc);
};
/** seated in PROFILE on a chair drawn in the card (rule 40): soles on the floor at p.y, facing (dx, dz) toward the table */
const sitSide = (out: Stage, cam: CamInfo, t: number, w: ReturnType<typeof who>, p: V3, dx: number, dz: number, fo: FrontOpts, seat: "chair" | "crate", hand?: [number, number]) => {
  const view = viewOf(cam, p[0], p[2], dx, dz);
  out.places.push(person(cam, w, p[0], p[1], p[2], { side: true, mirror: view.mirror }, { mode: "sit", ...fo }, { mode: "sit", seat, hand, expr: fo.expr, blink: lidAt(t, w.i) }));
  blob(out, p[0] + dx * 0.08, p[1], p[2] + dz * 0.08, 1.15);
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
const card = (out: Stage, key: string, cw: number, ch: number, draw: (p: Pen) => void, x: number, y: number, z: number, w: number, rot = 0, extra: Partial<FxPlace> = {}) =>
  out.fx.push({ key, cw, ch, draw, x, y, z, w, h: (w * ch) / cw, rot, ...extra });
const pop = (t: number, w0: number, d = 0.18) => smooth((t - W(w0)) / d); // a card scales in on its word
/** what a board stands on (owner: nothing floats): "easel" from the ground gy to under the board, "posts" for big
 *  outdoor boards, or { yaw } = fixed flat on a wall facing that way */
type Mount = { easel: number } | { posts: number } | { yaw: number };
const mount = (out: Stage, m: Mount, x: number, yb: number, z: number, w: number, k: number) => {
  if (k < 0.02) return;
  if ("easel" in m) { const h = yb - m.easel + 0.08; card(out, "easel", 400, 800, fxEasel, x, m.easel + h / 2, z + 0.03, Math.min(0.9, w * 0.85), 0, { h }); blob(out, x, m.easel, z, 0.9); }
  else if ("posts" in m) { const h = yb - m.posts + 0.1; card(out, "posts", 600, 800, fxPosts, x, m.posts + h / 2, z + 0.05, w * 0.9, 0, { h }); }
};
const cal = (out: Stage, t: number, s: string, w0: number, x: number, y: number, z: number, w = 1.0, m: Mount = { easel: D0 }) => {
  // owner rule 46: the easel/posts stand from the first frame of the shot; only the board pops in on its word
  const k = pop(t, w0), h = (w * 560) / 500;
  mount(out, m, x, y - h / 2 + 0.06, z, w, 1);
  if (k <= 0) return;
  const yc = "yaw" in m ? y : y - h / 2 + (h * k) / 2; // rule 50: a popping board grows UP from its easel/posts, never floats off them
  card(out, "cal" + s, 500, 560, (p) => fxCalendar(p, s, 0), x, yc, z, w * k, 0, "yaw" in m ? { yaw: m.yaw } : {});
};
const label = (out: Stage, t: number, lines: string[], w0: number, x: number, y: number, z: number, w: number, fill = "#f2c230", ink = "#2b2830", m: Mount = { easel: D0 }) => {
  const k = pop(t, w0);
  mount(out, m, x, y - (w * 360) / 800 / 2 + 0.06, z, w, 1);
  if (k <= 0) return;
  const H = (w * 360) / 800, yc = "yaw" in m ? y : y - H / 2 + (H * k) / 2;
  card(out, "lab" + lines.join("|") + fill, 800, 360, (p) => fxLabel(p, lines, fill, ink), x, yc, z, w * k, 0, "yaw" in m ? { yaw: m.yaw } : {});
};
/** a crouched worker turning a jackscrew: lever card swings back and forth beside him */
const cranker = (out: Stage, cam: CamInfo, t: number, i: number, p: V3, sc = 0.85, shadow = true, topY?: number) => {
  // kneeling side view, both hands on the lever of his own jackscrew (screw + lever drawn in the card, rule 29/33).
  // Owner rule 44: p is the SCREW's spot (under the building's edge); the screw runs from its pad up to the building
  // underside topY, and the card shifts sideways so the drawn screw lands exactly on p.
  const w = who(40 + i, WORK(i), "wk" + i), crank = q(((t * 0.55 + i * 0.37) % 1 + 1) % 1, 12), mir = i % 2 === 1;
  const off = (mir ? -1 : 1) * 170 * SU * sc, x = p[0] - cam.right.x * off, z = p[2] - cam.right.z * off;
  const screwTop = topY === undefined ? undefined : Math.round(Math.max(40, Math.min(960, (topY - p[1]) / (SU * sc))) / 6) * 6;
  out.places.push(person(cam, w, x, p[1], z, { side: true, mirror: mir }, {}, { mode: "kneel", crank, screwTop, expr: i % 3 === 0 ? "stern" : i % 3 === 1 ? "grin" : "neutral", blink: lidAt(t, w.i) }, sc));
  if (shadow) blob(out, x, p[1], z, sc * 1.3);
};
const window = (out: Stage, t: number, o: Outfit, key: string, i: number, wp: V3, expr: Expr) => {
  const bl = lidAt(t, i);
  out.fx.push({ key: `win|${key}|${expr}|${q(bl)}`, cw: 400, ch: 558, draw: (p) => fxWindow(p, o, expr, bl, (i % 7) + 1), x: wp[0], y: wp[1] - 0.015, z: wp[2], w: 1.01, h: 1.41, yaw: Math.PI });
};

export const stage = (id: number, t: number, _ws: World, cam: CamInfo): Stage => {
  const out: Stage = { places: [], fx: [] };
  const s = SHOTS[id - 1];
  LNAME = s.light;
  findSun(cam, SUN);
  switch (id) {
    case 1: { // 1861: the Tremont House rises six feet, a guest keeps sipping his tea
      if (t < W(4.68) - 0.05) {
        stand(out, cam, t, who(1, townsfolk(0), "on0"), ONLOOK, { expr: at(t, 1.78) ? "shock" : "neutral", facing: 1 });
        stand(out, cam, t, who(2, townsfolk(1), "on1"), [ONLOOK[0] + 1.8, D0, ONLOOK[2] + 0.7], { expr: at(t, 2.86) ? "shock" : "smile", facing: 1 });
        cal(out, t, "1861", 0.22, ONLOOK[0] - 0.9, D0 + 1.75, ONLOOK[2] + 1.6, 0.8);
        for (const [k, x] of [[0, -9.5], [1, -5.5], [2, 5.5]] as const) cranker(out, cam, t, k, [x, Y, TRE.z - 0.12], 0.85, true, D0 + lift("tre", id, t));
        crowd(out, cam, t, 60, 6);
        const r = pop(t, 3.48);
        if (r > 0) card(out, "ruler", 220, 760, fxRuler, TRE.x0 - 0.75, Y + 1.14 * r, TRE.z - 0.5, 0.66 * r);
      } else { // inside the dining room the tea never spills
        sit(out, cam, t, who(3, WIN_A, "tea"), [TEA[0], D0, TEA[2]], { expr: "smile_closed", facing: 0, prop: "teacup" }, 1, false);
      }
      break;
    }
    case 2: {
      if (t < W(9.22) - 0.05) {
        // (map labels in the sky removed: owner rule 13, nothing floats)
      } else { // rain, mud, sewage
        stand(out, cam, t, who(5, townsfolk(2), "stuck"), STUCK, { expr: at(t, 10.46) ? "pained" : "nervous", facing: 1 });
        stand(out, cam, t, who(6, townsfolk(3), "walk2"), [21.5, Y, 109.4], { expr: "dazed", facing: -1 });
        if (at(t, 10.94)) { const k = q((t * 1.5) % 1, 12); card(out, `stink${k}`, 300, 360, (p) => fxStink(p, k), 31, D0 + 0.9, 99.6, 1.3 * pop(t, 10.94)); }
        const ph = q((t * 2.4) % 1, 12), fwd = [cam.right.z, -cam.right.x];
        out.fx.push({ key: `rain${ph}`, cw: 512, ch: 900, draw: (p) => fxRain(p, ph), x: cam.pos.x + fwd[0] * 3, y: cam.pos.y - 0.1, z: cam.pos.z + fwd[1] * 3, w: 3.3, h: 5.8, soft: true });
      }
      break;
    }
    case 3: { // 1854: cholera in the drinking water
      stand(out, cam, t, who(7, DOCO, "doc"), DOC, { expr: at(t, 14.34) ? "shock" : at(t, 13.38) ? "nervous" : "stern", facing: 1, prop: "glass" });
      cal(out, t, "1854", 12.44, DOC[0] - 0.75, Y + 1.6, DOC[2] + 0.3, 0.8, { easel: Y });
      label(out, t, ["6%"], 14.34, DOC[0] + 0.95, Y + 1.5, DOC[2] + 0.3, 0.85, "#c8352e", "#ffffff", { easel: Y });
      break;
    }
    case 4: { // the plan, the sewer on the street, the street rises over it
      const ft = Math.max(0, fillTop(id, t)), yy = D0 + ft;
      if (t < W(17.16) - 0.05) {
        stand(out, cam, t, who(8, ENGO, "eng"), ENG, { expr: at(t, 16.34) ? "grin" : "stern", facing: -1 });
        card(out, "plan", 600, 420, fxPlan, ENG[0] - 0.42, D0 + 1.02, ENG[2] - 0.35, 0.66);
      } else {
        stand(out, cam, t, who(8, ENGO, "eng"), [ENG[0], yy, ENG[2] + 6], { expr: at(t, 19.38) ? "grin" : "stern", facing: -1 });
        for (const [k, x, z] of [[0, 63.4, 166], [1, 62.6, 178]] as const) // both on the camera side of the pipe, blades in the ground (rule 45)
          stand(out, cam, t, who(41 + k, WORK(k + 1), "dig" + k), [x, yy, z], { expr: k ? "grin" : "stern", facing: k ? -1 : 1, prop: ["hold", "shovel", q((t * 1.1 + k * 0.4) % 1, 20)] });
        if (at(t, 17.62)) puff(out, t, W(17.62), SEWER.x, D0, 162, 3.0, 0.7);
      }
      break;
    }
    case 5: { // 1858: four floors of brick go up six feet on 200 jackscrews, not one crack
      for (const [k, x] of [[0, 24.6], [1, 29.2], [2, 33.6]] as const) cranker(out, cam, t, 3 + k, [x, Y, B58.z + 0.12], 0.85, true, D0 + lift("b58", id, t));
      stand(out, cam, t, who(9, townsfolk(4), "w58"), [37.5, D0, 101.6], { expr: at(t, 28.12) ? "grin" : at(t, 25.7) ? "shock" : "neutral", facing: -1 });
      cal(out, t, "1858", 23.58, 36.4, D0 + 1.7, 100.4, 0.75);
      const r = pop(t, 26.0);
      if (r > 0) card(out, "ruler", 220, 760, fxRuler, B58.x1 + 0.7, Y + 1.14 * r, B58.z + 0.45, 0.66 * r);
      if (t < W(28.12) - 0.05) label(out, t, ["200", "JACKSCREWS"], 26.92, 31, D0 + 9.6 + lift("b58", id, t), B58.z + 0.08, 5.2, "#f2c230", "#2b2830", { yaw: 0.0001 });
      else label(out, t, ["NO CRACKS!"], 28.12, 31, D0 + 9.6 + lift("b58", id, t), B58.z + 0.08, 5.2, "#7ab648", "#2b2830", { yaw: 0.0001 });
      break;
    }
    case 6: { // 1860: the Lake Street block goes up five feet, 600 men, 6,000 screws, shops stay open
      const L = lift("blk", id, t);
      if (t < W(34.98) - 0.05) {
        [-112, -104.5, -97, -88, -80.5, -73].forEach((x, k) => cranker(out, cam, t, 6 + k, [x, Y, BLK.z - 1.8], 0.85, true, D0 + L - 0.22)); // under the porch's front edge
        cal(out, t, "1860", 29.22, -70.2, D0 + 1.9, 99.8, 1.1);
        stand(out, cam, t, who(10, ENGO, "fore"), [-68.5, D0, 97.0], { expr: at(t, 31.4) ? "grin" : "stern", facing: 1, prop: "clipboard" });
        // on an easel in front of the crankers, inside the low S6c frame while the numbers are spoken (rule 37)
        if (t < W(33.76) - 0.05) label(out, t, ["600 MEN"], 32.86, -92.5, D0 + 1.9, 107.6, 2.2, "#f2c230", "#2b2830", { easel: D0 });
        else label(out, t, ["6,000", "JACKSCREWS"], 33.76, -92.5, D0 + 1.9, 107.6, 2.2, "#f2c230", "#2b2830", { easel: D0 });
      } else {
        const py = D0 + L;
        stand(out, cam, t, who(12, BAKER, "baker"), [SHOP[0], py, BLK.z - 0.9], { expr: "grin", facing: 1, prop: "loaf" });
        card(out, "open", 400, 260, fxOpen, SHOP[0] - 1.25, py + 1.75, BLK.z - 0.08, 0.75, 0, { yaw: Math.PI });
        stand(out, cam, t, who(13, MOM, "cust"), [SHOP[0] + 1.75, Y, BLK.z - 2.6], { expr: at(t, 35.66) ? "smile" : "neutral", facing: -1 });
      }
      break;
    }
    case 7: { // the Tremont House / 500 men crouched underneath, turning screws a tiny bit at a time
      if (t < W(39.54) - 0.05) {
        for (const [k, x] of [[0, -9.5], [1, -5.5], [2, 5.5], [3, 9.5]] as const) cranker(out, cam, t, 12 + k, [x, Y, TRE.z - 0.12], 0.85, true, D0 + lift("tre", id, t));
        stand(out, cam, t, who(14, townsfolk(5), "p7a"), [11.2, Y, 108.9], { expr: "shock", facing: -1 });
        stand(out, cam, t, who(15, townsfolk(6), "p7b"), [13.2, Y, 108.6], { expr: "smile", facing: -1 });
        crowd(out, cam, t, 60);
      } else {
        let k = 0;
        for (const z of [112.2, 114.6, 117.0, 119.6]) for (const x of [-12.3, -9.9, -7.5, -5.1, -2.7, -0.3, 2.1, 4.5, 6.9, 9.3, 11.7]) {
          if ((k * 7) % 5 === 4) { k++; continue; }
          cranker(out, cam, t, 20 + k, [x + (z % 2 ? 0.2 : -0.2), D0 + 0.01, z], 0.78, false, D0 + lift("tre", id, t)); k++;
        }
        label(out, t, ["500 MEN"], 39.64, 5.4, D0 + 1.0, TRE.z + 5.3, 1.3, "#f2c230", "#2b2830", { easel: D0 });
      }
      break;
    }
    case 8: { // the guests barely noticed / the front steps got steeper every single day
      if (t < W(44.9) - 0.05) {
        const e: Expr = at(t, 44.02) ? "smile_closed" : "smile";
        sit(out, cam, t, who(3, WIN_A, "tea"), [TEA[0], D0, TEA[2]], { expr: "smile_closed", facing: 0, prop: "teacup" }, 1, false);
        sitSide(out, cam, t, who(4, WIN_B, "d1"), chairAt(1, 0), ...towardTable(1, 0), { expr: e }, "chair", [480, 615]);
        sitSide(out, cam, t, who(5, WIN_C, "d2"), chairAt(1, 1), ...towardTable(1, 1), { expr: "grin" }, "chair", [480, 615]);
        stand(out, cam, t, who(21, BAKER, "waiter"), [-562.0, D0, -620.3], { expr: "smile", facing: -1 });
      } else {
        const n = DAYS.filter((d) => t >= d - L2).length;
        stand(out, cam, t, who(16, GUESTO, "guest"), GUEST, { expr: n >= 3 ? "dazed" : n >= 2 ? "pained" : n >= 1 ? "nervous" : "neutral", facing: -1 });
        if (n > 0) { const d = ["MON", "TUE", "WED"][n - 1], k = smooth((t - DAYS[n - 1]) / 0.15);
          card(out, "cal" + d, 500, 560, (p) => fxCalendar(p, d, 0), 1.0, D0 + lift("tre", id, t) + 2.0, TRE.z - 0.06, 0.9 * (n === 1 ? k : 1), 0, { yaw: Math.PI }); }
        for (const d of DAYS) if (t >= d && t < d + 0.6) puff(out, t, d, 0, D0 + 0.3, TRE.z - 0.6, 1.2, 0.5);
      }
      break;
    }
    case 9: { // like lifting the couch an inch at a time while the whole family sits on it (in their parlour, rule 34)
      const n = Math.max(0, Math.min(8, Math.floor((t - W(50.16) + L2) / 0.3) + 1)), up = 0.03 * n;
      const base = D0 + 0.3 + up, cw2 = 2.4, chh = (cw2 * 520) / 900, CZ = COUCH[2];
      // couch back -> family seated on the cushion -> couch front: the cushion edge crosses their laps, so they SIT on it
      card(out, "couchB", 900, 520, fxCouchBack, COUCH[0], base + chh / 2, CZ + 0.25, cw2, 0, { yaw: Math.PI });
      const sy = base + 0.15;
      sit(out, cam, t, who(17, DAD, "dad"), [COUCH[0] - 0.62, sy, CZ + 0.05], { expr: at(t, 51.3) ? "grin" : "smile_closed", facing: 1 }, 1, false);
      sit(out, cam, t, who(18, { ...KID, skin: SKINS[0] }, "kid"), [COUCH[0] + 0.02, sy + 0.07, CZ + 0.03], { expr: at(t, 51.96) ? "laugh" : "smile", facing: 0 }, 0.85, false);
      sit(out, cam, t, who(19, MOM, "mom"), [COUCH[0] + 0.64, sy, CZ + 0.05], { expr: at(t, 51.3) ? "smile" : "smile_closed", facing: -1 }, 1, false);
      card(out, "couchF", 900, 520, fxCouchFront, COUCH[0], base + chh / 2, CZ - 0.12, cw2, 0, { yaw: Math.PI });
      blob(out, COUCH[0], D0, CZ, 2.6);
      // two workers kneel at the ends, each turning the jackscrew under a couch foot (screw head = the foot)
      const fx = (810 - 450) * (cw2 / 900), top = (0.3 + up) / SU;
      for (const sd of [-1, 1] as const) {
        const w = who(43 + (sd > 0 ? 1 : 0), WORK(2 + (sd > 0 ? 1 : 0)), "jackman" + sd), crank = q(((t * 0.9 + (sd > 0 ? 0.5 : 0)) % 1 + 1) % 1, 12);
        out.places.push(person(cam, w, COUCH[0] + sd * (fx + 0.367), D0, CZ - 0.32, { side: true, mirror: sd > 0 }, {}, { mode: "kneel", crank, screwTop: top, expr: "grin", blink: lidAt(t, w.i) }, 1));
        blob(out, COUCH[0] + sd * (fx + 0.7), D0, CZ - 0.32, 1.2);
      }
      break;
    }
    case 10: { // a young George Pullman ran part of it; later he built the famous sleeping cars
      stand(out, cam, t, who(20, PULLO, "pull"), PULL, { expr: at(t, 55.8) ? "grin" : "smile", facing: 1, prop: "clipboard" });
      if (t >= W(55.4) - 0.05) { // years later: his sleeping car at the depot
        stand(out, cam, t, who(20, PULLO, "pull"), PULL2, { expr: at(t, 56.68) ? "grin" : "smile", facing: -1, wave: at(t, 56.68) ? 0.8 : undefined });
        stand(out, cam, t, who(44, WORK(3), "porter"), [STA.x + 3.4, PLAT.y, PLAT.z0 + 2.4], { expr: "smile", facing: -1 });
        stand(out, cam, t, who(19, MOM, "pass1"), [STA.x + 2.4, PLAT.y, PLAT.z0 + 0.9], { expr: "smile", facing: -1 });
        stand(out, cam, t, who(17, DAD, "pass2"), [STA.x + 1.5, PLAT.y, PLAT.z0 + 0.6], { expr: "grin", facing: -1 });
        break;
      }
      for (const [k, x] of [[0, 4.5], [1, 11.5], [2, -4.5]] as const) cranker(out, cam, t, 30 + k, [x, Y, TRE.z - 0.12], 0.85, true, D0 + lift("tre", id, t));
      label(out, t, ["GEORGE", "PULLMAN"], 53.94, PULL[0] + 0.9, Y + 1.75, PULL[2] + 0.3, 1.15, "#f2c230", "#2b2830", { easel: Y });
      break;
    }
    case 11: { // the city drained into the lake it drank from... in 1900 the river was made to flow backwards
      const fp = flowPos(t), yaw = arrowYaw(t);
      for (let i = 0; i < 10; i++) {
        const x = -60 + ((((i * 25 + fp) % 250) + 250) % 250), z = i % 2 ? -9 : 9;
        if (x > 166) continue;
        const dc = Math.hypot(x - cam.pos.x, z - cam.pos.z), ks = Math.max(0, Math.min(1, (dc - 26) / 14));
        if (ks <= 0.02) continue;
        out.fx.push({ key: "arrow", cw: 600, ch: 300, draw: (p) => fxArrow(p, "#e8a33a"), x, y: 0.06, z, w: 16 * ks, h: 8 * ks, flat: true, rot: yaw });
      }
      if (t < W(60.5) - 0.05) label(out, t, ["DRINKING", "WATER"], 59.64, 167, D0 + 11, 8, 20, "#7cc4ee", "#2b2830", { posts: D0 });
      else if (t < W(63.0)) cal(out, t, "1900", 60.92, 118, D0 + 4.6, 33.5, 5, { posts: D0 });
      if (t >= FLIP_T && t < FLIP_T + 0.2) burst(out, t, FLIP_T, 110, 4, 0, 14);
      break;
    }
  }
  return out;
};
export { FPS };
