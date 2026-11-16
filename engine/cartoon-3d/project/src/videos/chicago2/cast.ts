// Our cast as lit flat sprites in the 3D world. Each frame every character asks for a drawing (a key + a draw call);
// the pool keeps one canvas per distinct drawing, so soldiers marching in step share canvases (7 head shapes x 4
// outfits). Characters are yaw-only billboards shaded by cardShade() (scene tint, bright floor, side gradient toward
// the sun, painted crescent in the drawing); standing ones get a soft multiply contact blob. Effects are unlit cards.
// Cards, effects and blobs live on the NOINK layer so the world ink pass never outlines their quads.
import * as THREE from "three";
import { Pen, bodyFront, bodySide, fxBurst, fxSplash, fxRing, fxShadow, fxContact, fxPuff, Outfit, Expr, FrontOpts, SideOpts, SKINS, INK } from "./toon";
import { FPS, D0, SHOTS, V3, smooth, clamp01, TOTAL as TOTAL_F } from "./story";
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
const LEAD = 0; // teardown: picture lands 0 to +1 frame after its word
/** eyelid 0 open .. 1 shut. Reference: gaps 0.5-2.3 s, 4-frame blink half / shut / shut / half, plus a blink across
 *  every expression swap (the shut frames hide the swap) */
const LID = [0.6, 1, 0.6]; // teardown: 2-3 frame blinks
const lidAt = (t: number, i: number, swaps: number[] = []) => {
  const f = Math.round(t * FPS);
  for (const ts of swaps) { const k = f - Math.round((ts - LEAD) * FPS) + 1; if (k >= 0 && k < LID.length) return LID[k]; }
  let s = Math.round(-60 * hh(i, 9));
  for (let n = 0; s <= f && n < 400; n++) {
    const k = f - s;
    if (k >= 0 && k < LID.length) return LID[k];
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

// ---------------- v3 foreground layer (teardown: a cropped, lens-blurred near prop in every shot) ----------------
import { fxMud, fxNewsWall, fxLantern, fxLamp, fxReeds, fxTeapot, fxBackHat, fxBarrel, fxSign, fxGeranium, fxCandle, fxFern, fxTrunk, fxScrew, fxGull, fxInkwell, fxDrape } from "./fx7";
import { camAt } from "./story";
type FgK = "lamp" | "reeds" | "teapot" | "backhat" | "barrel" | "sign" | "signR" | "signDG" | "geranium" | "candle" | "fern" | "trunk" | "screw" | "gull" | "inkwell" | "drape";
const FGART: Record<FgK, [number, number, (p: Pen, t: number) => void]> = {
  lamp: [300, 1000, (p) => fxLamp(p, 0)], reeds: [600, 800, (p) => fxReeds(p)], teapot: [600, 500, (p) => fxTeapot(p)],
  backhat: [700, 700, (p) => fxBackHat(p)], barrel: [500, 620, (p) => fxBarrel(p)], sign: [760, 520, (p) => fxSign(p, "HARDWARE", "#6a2f2f")], signR: [1000, 520, (p) => fxSign(p, "HARDWARE", "#6a2f2f", true, 1000)],
  signDG: [760, 520, (p) => fxSign(p, "DRY GOODS", "#2f4f3a", true)], geranium: [520, 520, (p) => fxGeranium(p)], candle: [520, 760, (p) => fxCandle(p)],
  fern: [700, 800, (p) => fxFern(p)], trunk: [760, 520, (p) => fxTrunk(p)], screw: [500, 900, (p) => fxScrew(p)],
  gull: [500, 300, (p, t) => fxGull(p, t)], inkwell: [640, 600, (p) => fxInkwell(p)], drape: [400, 1000, (p) => fxDrape(p)],
};
/** [take, from frame, to frame, prop, u, v, d, width share]: anchored in the WORLD where the camera was at `from`
 *  (so it parallaxes as the camera moves); u/v = screen position -1..1 (right / up), d = metres from the lens */
/** optional 9th/10th: floor height + real height (rule 79, owner v21): a grounded prop stands ON that floor at its true size */
const FG: [number, number, number, FgK, number, number, number, number, number?, number?][] = [
  [1, 0, 92, "lamp", -0.88, 0.1, 1.7, 0.3], [1, 92, 146, "geranium", 0.72, -0.82, 1.3, 0.5],
  [2, 136, 197, "teapot", 0.74, -0.8, 1.1, 0.5],
  /* v19: the f190-220 reed card showed only cattail heads on stubs at this low lens (rule 56): removed */ [3, 220, 286, "reeds", 0.78, -0.74, 2.0, 0.7],
  [4, 286, 373, "barrel", -0.62, -0.6, 2.6, 0.45, D0, 0.95] /* v21 rule 79: a real barrel standing in the mud (it floated in the air on pans) */,
  [5, 410, 468, "lamp", -1.0, 0.0, 1.7, 0.3],

  /* v21 rule 81 (owner): the take-7 curtain covered the model, removed */
  /* v20 rules 64+73: the f701 and f872 hanging-sign cards swept across the frame (lettering cut on the way): removed */ [8, 752, 836, "barrel", 0.82, -0.72, 1.4, 0.45], [8, 836, 880, "signR", 0.64, 0.62, 2.4, 0.66] /* v20 rule 64: board fully in frame through the push-in, wall end of the bracket off-frame right */,
  [9, 985, 1052, "barrel", -0.86, -0.7, 1.2, 0.42], [9, 1052, 1097, "barrel", 0.8, -0.74, 1.2, 0.42] /* v17 rule 59: the lamp crossed the baker after the reframe */,
  [10, 1089, 1150, "gull", 0.45, 0.45, 3.5, 0.32], [10, 1150, 1196, "lamp", 0.84, 0.0, 2.2, 0.3], [10, 1196, 1250, "screw", -0.82, -0.3, 1.5, 0.42], /* v20: the f1250 screw card stood in front of the reframed worker's lever (rule 59): removed */
  /* v21 rule 81 (owner): the take-11 curtain on the right read as out of place, removed */
  [12, 1347, 1444, "lamp", 0.86, 0.0, 1.6, 0.3], [12, 1444, 1478, "geranium", -0.8, -0.82, 0.8, 0.5],
  // take 13 fern FG card removed (owner Nov 13: levitating plant in a pot; rule 79)
  [14, 1577, 1620, "lamp", -0.86, 0.0, 2.0, 0.3], [14, 1650, 1730, "trunk", 0.74, -0.8, 1.2, 0.55],
  [15, 1722, 1782, "gull", -0.4, 0.5, 4.0, 0.3], [15, 1782, 1823, "reeds", -0.78, -0.74, 1.2, 0.65],
  /* v19f: take-16 gulls read as a grey blurred saucer in the sunset sky, removed */
];
const fgF = new THREE.Vector3(), fgR = new THREE.Vector3(), fgU = new THREE.Vector3(), fgUp = new THREE.Vector3(0, 1, 0);
const foreground = (out: Stage, id: number, t: number) => {
  const f = Math.round(t * FPS);
  for (const [tk, a, b, k, u, v, d, wf, gy, gh] of FG) {
    if (tk !== id || f < a || f >= b) continue;
    const c = camAt(id, Math.round((a + Math.min(b, a + 60)) / 2));
    fgF.set(c.look[0] - c.pos[0], c.look[1] - c.pos[1], c.look[2] - c.pos[2]).normalize();
    fgR.crossVectors(fgF, fgUp).normalize(); fgU.crossVectors(fgR, fgF);
    const hH = d * Math.tan((c.fov * Math.PI) / 360), hW = hH * (9 / 16);
    const [cw, ch, draw] = FGART[k], w = wf * 2 * hW;
    let du = u, dv = v, ph = 0;
    if (k === "gull") { const s = (f - a) / FPS; du = u + 0.16 * s * (u < 0 ? 1 : -1); dv = v + 0.05 * Math.sin(s * 2); ph = q(((s * 2.4) % 1 + 1) % 1, 8); }
    const x = c.pos[0] + fgF.x * d + fgR.x * du * hW + fgU.x * dv * hH, y = c.pos[1] + fgF.y * d + fgR.y * du * hW + fgU.y * dv * hH, z = c.pos[2] + fgF.z * d + fgR.z * du * hW + fgU.z * dv * hH;
    // v8 (rule 62): a street lamp is a real 3.2 m post standing ON the sidewalk (base at D0 + SW), never a camera-pinned
    // card whose foot hangs in the air; the camera anchor only chooses where it stands
    if (k === "lamp") { out.fx.push({ key: `fg|lamp|0`, cw, ch, draw: (p) => draw(p, ph), x, y: D0 + SW + 1.6, z, w: 0.96, h: 3.2 }); continue; }
    if (gy !== undefined && gh !== undefined) { out.fx.push({ key: `fg|${k}|${ph}`, cw, ch, draw: (p) => draw(p, ph), x, y: gy + gh / 2, z, w: (gh * cw) / ch, h: gh }); continue; }
    out.fx.push({ key: `fg|${k}|${ph}`, cw, ch, draw: (p) => draw(p, ph), x, y, z, w, h: (w * ch) / cw });
  }
};
/** take 5 dusk: gas lamps along the north kerb switch on one after another, each on its word (lights as events) */
const LAMPS: [number, number][] = [[37.0, 13.38], [43.6, 13.82], [33.4, 14.34], [47.2, 15.0]];
const dusk = (out: Stage, t: number) => {
  for (const [x, w0] of LAMPS) {
    const k = clamp01((t - W(w0)) * FPS / 2), lit = k > 0 ? Math.min(1, k * 1.3) : 0, flick = lit > 0 && t - W(w0) < 0.1 ? 1.25 : 1;
    out.fx.push({ key: `lamp|${q(lit * flick, 8)}`, cw: 300, ch: 1000, draw: (p) => fxLamp(p, Math.min(1.2, lit * flick)), x, y: D0 + SW + 1.6, z: 110.95, w: 0.96, h: 3.2 });
  }
};

// ---------------- the cast of the Chicago short ----------------
export type Stage = { places: Place[]; fx: FxPlace[] };
import { fxCalendar } from "./fx3";
import { fxWindow, fxGlass, fxLabel, fxPlan, fxRuler, fxRain, fxStink, fxOpen, fxLoaf, fxCouch, fxCouchBack, fxCouchFront, fxJack, fxLever, fxSleeper, fxArrow, fxTally, fxEasel, fxPosts } from "./fx5";
import { TABLES, TEA, PULL2, STA, PLAT } from "./story";
import { W, World, SW, TRE, B58, BLK, SEWER, treWin, ONLOOK, STUCK, DOC, ENG, SHOP, GUEST, COUCH, PULL, DAYS, lift, fillTop, flowPos, arrowYaw, FLIP_T } from "./story";
import { townsfolk, KID, headBlob, BUILD } from "./toon";

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

const L2 = 0; // teardown sync: on the word, never early
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
  out.places.push(person(cam, w, p[0], p[1], p[2], { side: false, mirror: false }, { mode: "stand", blink: lidAt(t, w.i, takeSw()), ...fo }, {}, sc));
  blob(out, p[0], p[1], p[2], sc);
};
const sit = (out: Stage, cam: CamInfo, t: number, w: ReturnType<typeof who>, p: V3, fo: FrontOpts, sc = 1, shadow = true) => {
  out.places.push(person(cam, w, p[0], p[1], p[2], { side: false, mirror: false }, { mode: "sit", blink: lidAt(t, w.i, takeSw()), ...fo }, {}, sc));
  if (shadow) blob(out, p[0], p[1], p[2], sc);
};
/** seated in PROFILE on a chair drawn in the card (rule 40): soles on the floor at p.y, facing (dx, dz) toward the table */
const sitSide = (out: Stage, cam: CamInfo, t: number, w: ReturnType<typeof who>, p: V3, dx: number, dz: number, fo: FrontOpts, seat: "chair" | "crate", hand?: [number, number]) => {
  const view = viewOf(cam, p[0], p[2], dx, dz);
  out.places.push(person(cam, w, p[0], p[1], p[2], { side: true, mirror: view.mirror }, { mode: "sit", ...fo }, { mode: "sit", seat, hand, expr: fo.expr, blink: lidAt(t, w.i, takeSw()) }));
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
const cranker = (out: Stage, cam: CamInfo, t: number, i: number, p: V3, sc = 0.85, shadow = true, topY?: number, yaw?: number) => {
  // kneeling side view, both hands on the lever of his own jackscrew (screw + lever drawn in the card, rule 29/33).
  // Owner rule 44: p is the SCREW's spot (under the building's edge); the screw runs from its pad up to the building
  // underside topY, and the card shifts sideways so the drawn screw lands exactly on p.
  const w = who(40 + i, WORK(i), "wk" + i), crank = q(((t * 0.55 + i * 0.37) % 1 + 1) % 1, 12), mir = i % 2 === 1;
  const off = (mir ? -1 : 1) * 170 * SU * sc, x = p[0] - cam.right.x * off, z = p[2] - cam.right.z * off;
  const screwTop = topY === undefined ? undefined : Math.round(Math.max(40, Math.min(960, (topY - p[1]) / (SU * sc))) / 6) * 6;
  const pl = person(cam, w, yaw === undefined ? x : p[0] + off * Math.cos(yaw - Math.PI), p[1], yaw === undefined ? z : p[2], { side: true, mirror: mir }, {}, { mode: "kneel", crank, screwTop, expr: i % 3 === 0 ? "stern" : i % 3 === 1 ? "grin" : "neutral", blink: lidAt(t, w.i) }, sc);
  // a card along a wall is locked parallel to it (a camera-facing card cut into the facade on oblique angles)
  out.places.push(yaw === undefined ? pl : { ...pl, yaw });
  if (shadow) blob(out, x, p[1], z, sc * 1.3);
};
const window = (out: Stage, t: number, o: Outfit, key: string, i: number, wp: V3, expr: Expr) => {
  const bl = lidAt(t, i);
  out.fx.push({ key: `win|${key}|${expr}|${q(bl)}`, cw: 400, ch: 558, draw: (p) => fxWindow(p, o, expr, bl, (i % 7) + 1), x: wp[0], y: wp[1] - 0.015, z: wp[2], w: 1.01, h: 1.41, yaw: Math.PI });
};

// ---------------- v2 staging (16 continuous takes, DETAIL_STANDARD A-H) ----------------
import { fxNews, fxSoggy, fxPlan2, fxModel, fxSheet, fxPot, fxFrog, fxMilk, fxDebris, fxRipple } from "./fx6";
import { SWAMP, COUNCIL, CTAB, MODEL, NEWS, PAPER, SHORE, modelFill, modelLift } from "./story";
/** pose-to-pose acting: the expression of the last cue whose word has started (cue lands 2 f early) */
/** cue times of the last act() call: the next stand/sit consumes them so every pose change hides behind a blink */
let cueSw: number[] = [];
const takeSw = () => { const r = cueSw; cueSw = []; return r; };
const act = (t: number, base: Expr, cues: [number, Expr][]) => { cueSw = cues.map(([w]) => W(w)); let e = base; for (const [w, x] of cues) if (at(t, w)) e = x; return e; };
/** background acting: a held face that swaps every 8-15 frames among a few (never static, never flickering) */
const idle = (t: number, i: number, xs: Expr[]) => {
  const f = Math.floor(t * FPS);
  let s = Math.round(-20 * hh(i, 4)), n = 0;
  while (n < 400) { const d = 8 + Math.round(7 * hh(i * 17 + n, 6)); if (s + d > f) break; s += d; n++; }
  return xs[(n + i) % xs.length];
};
const COUNCILO = (v: number): Outfit => ({ ...townsfolk(v), hat: v % 2 ? "tophat" : "hair", hair: ["#5a3b2a", "#8a8a8a", "#2a201a"][v % 3], moustache: v % 3 === 2 ? undefined : "#5a4a3a", jacket: ["#3b3a40", "#4a3f36", "#2f3a4a", "#3f4038"][v % 4], buttons: "#c9b48a" });

/** a busy street: townsfolk on both plank sidewalks and a few crossing the road, seeded, each acting on its own clock */
/** zN: north-side walkers' z (default 109.4-109.9). v21 rule 88 (owner): under the raised Lake Street porch (front at
 *  z 109.1) their heads went into the boards and one hat slid along them, so take 9 keeps them in front of the porch */
const street = (out: Stage, cam: CamInfo, t: number, base: number, x0: number, x1: number, step = 3.2, zN = 109.4) => {
  let k = 0;
  for (let x = x0; x < x1; x += step) {
    const r1 = hh(base + k, 1), r2 = hh(base + k, 2), side = r1 < 0.42 ? 0 : r1 < 0.84 ? 1 : 2;
    const z = side === 0 ? zN + 0.5 * r2 : side === 1 ? 94.6 - 0.5 * r2 : 98 + 8 * r2, y = side === 2 ? D0 : Y;
    const xx = x + step * 0.8 * (r2 - 0.5);
    if (Math.hypot(xx - cam.pos.x, z - cam.pos.z) > 6.5) stand(out, cam, t, who(base + k, townsfolk(k % 8), "st" + (k % 8)), [xx, y, z],
      { expr: idle(t, base + k, (["smile", "neutral", "grin", "shock", "dazed"] as Expr[]).slice(k % 3, k % 3 + 3)), facing: r2 < 0.5 ? 1 : -1, wave: k % 7 === 3 && Math.floor(t * 1.3 + k) % 3 === 0 ? 0.8 : undefined });
    k++;
  }
};
export const stage = (id: number, t: number, _ws: World, cam: CamInfo): Stage => {
  const out: Stage = { places: [], fx: [] };
  const s = SHOTS[id - 1];
  LNAME = s.light;
  findSun(cam, SUN);
  switch (id) {
    case 1: { // cold open in motion: the Tremont House rises, crankers under the front, a guest sips tea at a first-floor window
      const L = lift("tre", id, t);
      for (const [k, x] of [[0, -11.5], [1, -9.5], [2, -7.5], [3, -5.5], [4, -3.5], [5, 3.5], [6, 5.5], [7, 7.5], [8, 9.5]] as const) cranker(out, cam, t, k, [x, Y, TRE.z - 0.45], 0.85, true, D0 + L, Math.PI);
      stand(out, cam, t, who(1, townsfolk(0), "on0"), ONLOOK, { expr: act(t, "neutral", [[1.78, "shock"], [2.32, "dazed"], [3.48, "shock"], [4.3, "laugh"]]), facing: 1 });
      stand(out, cam, t, who(2, townsfolk(1), "on1"), [ONLOOK[0] + 1.8, D0, ONLOOK[2] + 0.7], { expr: act(t, "smile", [[1.78, "nervous"], [2.86, "shock"], [3.8, "grin"]]), facing: 1, wave: at(t, 3.8) ? 0.8 : undefined });
      crowd(out, cam, t, 60, 8);
      street(out, cam, t, 320, -40, -14, 3.6);
      street(out, cam, t, 340, 14, 40, 3.6);
      // guests at the windows keep living their lives as the whole front climbs
      window(out, t, WIN_A, "tw" + idle(t, 3, ["smile_closed", "smile"]), 3, treWin(6, 1, id, t), act(t, "smile_closed", [[3.48, "smile"], [4.3, "smile_closed"]]));
      window(out, t, WIN_B, "tw2", 4, treWin(3, 1, id, t), idle(t, 4, ["smile", "neutral", "smile_closed"]));
      window(out, t, WIN_C, "tw3", 5, treWin(9, 2, id, t), idle(t, 5, ["grin", "smile"]));
      for (const x of [-11.5, -5.5, 5.5]) if (t > W(1.7)) puff(out, t, W(1.7) + (x + 12) * 0.03, x, Y, TRE.z - 0.5, 0.8, 0.5);
      break;
    }
    case 2: { // inside: the tea never spills; other diners, a waiter with a tray
      sit(out, cam, t, who(3, WIN_A, "tea"), [TEA[0], D0, TEA[2]], { expr: act(t, "smile_closed", [[5.06, "smile"], [5.46, "smile_closed"], [5.64, "grin"]]), facing: 0, prop: "teacup" }, 1, false);
      sitSide(out, cam, t, who(4, WIN_B, "d1"), chairAt(1, 0), ...towardTable(1, 0), { expr: idle(t, 4, ["smile", "laugh", "smile_closed"]) }, "chair", [480, 615]);
      sitSide(out, cam, t, who(5, WIN_C, "d2"), chairAt(1, 1), ...towardTable(1, 1), { expr: idle(t, 5, ["grin", "neutral", "smile"]) }, "chair", [480, 615]);
      stand(out, cam, t, who(21, BAKER, "waiter"), [-562.0, D0, -620.3], { expr: idle(t, 21, ["smile", "smile_closed"]), facing: -1 });
      break;
    }
    case 3: { // the swamp: a frog hops off a lily pad on "swamp"; settlers on the boardwalk; the lake barely lower
      const X = SWAMP.x, Z = SWAMP.z, hop = smooth((t - W(7.46) + L2) / 0.35), land = smooth((t - W(7.46) - 0.35) / 0.25);
      const fx0 = X + 0.4 + 1.2 * hop, fz = Z + 0.2 + 0.4 * hop;
      card(out, `frog${q(hop * (1 - land), 10)}`, 220, 180, (p) => fxFrog(p, q(hop * (1 - land), 10)), fx0, D0 + 0.16 + 0.5 * Math.sin(Math.PI * hop) * (1 - land), fz, 0.32);
      if (at(t, 7.46)) puff(out, t, W(7.46), X + 0.4, D0 + 0.06, Z + 0.2, 0.4, 0.4);
      stand(out, cam, t, who(50, WORK(0), "fisher"), [X - 0.4, D0 + 0.42, Z + 9], { expr: act(t, "neutral", [[7.46, "grin"], [8.32, "nervous"], [8.74, "dazed"]]), facing: 1, prop: ["hold", "rod", 0] });
      stand(out, cam, t, who(51, MOM, "laundry"), [X - 3.0, D0, Z + 12.6], { expr: idle(t, 51, ["smile", "neutral", "stern"]), facing: -1 });
      stand(out, cam, t, who(52, WORK(1), "wader"), [X + 4.2, D0 - 0.25, Z + 6.2], { expr: act(t, "pained", [[8.56, "shock"], [9.0, "pained"]]), facing: -1, prop: ["hold", "shovel", q((t * 0.8) % 1, 20)] });
      for (const [dx, dz, k] of [[-6, 4, 0], [3.5, 10.5, 1], [-1.5, 2.8, 2]] as const) card(out, `frogS${k}`, 220, 180, (p) => fxFrog(p, 0), X + dx, D0 + 0.14, Z + dz, 0.26);
      break;
    }
    case 4: { // rain: mud to the shins, sewage with nowhere to go, the newspaper going soggy in the gutter
      { const dx = cam.pos.x - STUCK[0], dz = cam.pos.z - STUCK[2], L = Math.hypot(dx, dz) || 1; // v21 rule 80: mud ring in front of his shins
        card(out, "mud", 600, 220, fxMud, STUCK[0] + (dx / L) * 0.14, D0 + 0.1, STUCK[2] + (dz / L) * 0.14, 0.95); }
      stand(out, cam, t, who(5, townsfolk(2), "stuck"), STUCK, { expr: act(t, "nervous", [[10.2, "stern"], [10.46, "pained"], [11.42, "dazed"], [11.78, "pained"]]), facing: 1 });
      // v20 QA (rule 56): in the f336 tilt down to the paper her head was cut off by the top edge: she leaves before it
      if (!(t >= 336 / FPS && cam.pos.z < 99.5)) stand(out, cam, t, who(6, townsfolk(3), "walk2"), [36.4, D0 - 0.12, 103.6], { expr: act(t, "neutral", [[10.94, "shock"], [11.26, "pained"]]), facing: -1 });
      stand(out, cam, t, who(53, WORK(2), "plank"), [29.0, Y, 109.2], { expr: idle(t, 53, ["stern", "nervous"]), facing: 1, prop: ["hold", "shovel", q((t * 0.7) % 1, 20)] });
      if (at(t, 10.94)) { const k = q((t * 1.5) % 1, 12); card(out, `stink${k}`, 300, 360, (p) => fxStink(p, k), 31.0, D0 + 0.55, 99.9, 0.8 * pop(t, 10.94)); }
      card(out, "soggy", 500, 380, fxSoggy, PAPER[0], PAPER[1], PAPER[2], 0.9, Math.PI + 0.3, { flat: true });
      const ph = q((t * 2.4) % 1, 12), fwd = [cam.right.z, -cam.right.x];
      out.fx.push({ key: `rain${ph}`, cw: 512, ch: 900, draw: (p) => fxRain(p, ph), x: cam.pos.x + fwd[0] * 3, y: cam.pos.y - 0.1, z: cam.pos.z + fwd[1] * 3, w: 3.3, h: 5.8, soft: true });
      break;
    }
    case 5: { // 1854: the same headline pasted on a wall; the doctor holds up a glass of the drinking water
      card(out, "news", 500, 680, fxNews, NEWS[0], NEWS[1], NEWS[2] - 0.02, 0.62, 0, { yaw: Math.PI });
      // v21: a brick wall card behind the paper, only for the insert camera (never in the doctor shot)
      if (Math.hypot(cam.pos.x - NEWS[0], cam.pos.z - NEWS[2]) < 2.8) card(out, "newsWall", 800, 1120, fxNewsWall, NEWS[0], NEWS[1] + 0.2, NEWS[2] + 0.02, 3.2, 0, { yaw: Math.PI });
      stand(out, cam, t, who(7, DOCO, "doc"), DOC, { expr: act(t, "stern", [[13.38, "nervous"], [13.82, "stern"], [14.34, "shock"], [15.0, "pained"]]), facing: 1, prop: "glassUp" });
      stand(out, cam, t, who(54, townsfolk(5), "cough"), [DOC[0] + 2.2, Y, DOC[2] - 0.6], { expr: idle(t, 54, ["pained", "dazed", "pained", "nervous"]), facing: -1 });
      // v19: a woman waits at the water pump with her jug (on-story: the pump water), in the close-up only, fully in frame
      stand(out, cam, t, who(56, townsfolk(2), "pumpw"), [DOC[0] + 1.5 + 0.6, D0, DOC[2] + 2.6 - 0.1], { expr: idle(t, 56, ["neutral", "nervous", "neutral"]), facing: 1 });
      sit(out, cam, t, who(55, MOM, "stoop"), [DOC[0] - 2.6, Y + 0.2, DOC[2] + 0.4], { expr: act(t, "nervous", [[14.34, "pained"]]), facing: 1 }, 0.95);
      break;
    }
    case 6:
    case 7: { // the council room: the plan, the wild decision, the engineer pulls the sheet off the model; fill rises, houses follow
      const [CX, CY, CZ] = CTAB;
      const lay = smooth((t - W(17.26) + L2) / (W(18.74) - W(17.26))), top = smooth((t - W(18.74)) / 0.5);
      card(out, `plan${q(lay, 20)}${q(top, 10)}`, 700, 500, (p) => fxPlan2(p, q(lay, 20), q(top, 10)), CX, CY + 0.004, CZ - 0.35, 0.82, Math.PI + 0.04, { flat: true });
      const sheet = smooth((t - W(19.38) + L2) / 0.45), mw = 1.25, mh = (mw * 520) / 800;
      const mf = q(modelFill(t), 30), ml = q(modelLift(t), 30);
      card(out, `model${mf}|${ml}`, 800, 520, (p) => fxModel(p, mf, ml), MODEL[0], CY + mh / 2, MODEL[2], mw, 0, { yaw: Math.PI });
      if (sheet < 1) card(out, `sheet${q(sheet, 20)}`, 800, 520, (p) => fxSheet(p, q(sheet, 20)), MODEL[0], CY + mh / 2 + 0.02, MODEL[2] - 0.05, mw * 1.04, 0, { yaw: Math.PI });
      // v8: take 7 is a tight insert on the model (it fills the frame): the councilmen and engineer only ever peeked round
      // its edges there, so they act in take 6 only
      if (id === 6) { // one councilman clear of the sheet-covered model (never behind it), reacting to the plan
        sit(out, cam, t, who(57, COUNCILO(1), "cm1"), [CX - 2.15, D0, CZ + 1.0], { expr: act(t, "stern", [[16.34, "shock"], [16.64, "dazed"], [17.76, "nervous"], [18.6, "stern"]]), facing: 1 }, 1, false);
      }
      break;
    }
    case 8: { // 1858: four floors on 200 screws; the flowerpot on the sill never wobbles
      const L = lift("b58", id, t);
      // v21 rule 90 (owner): the crankers stood 12 cm from the facade and their camera-facing cards cut into the wall;
      // now 0.2 m out (screw still at the sill edge, rule 44) with the card locked parallel to the wall (rule 53)
      for (const [k, x] of [[0, 23.2], [1, 25.4], [2, 27.6], [3, 29.8], [4, 32.0], [5, 34.4]] as const) cranker(out, cam, t, 3 + k, [x, Y, B58.z + 0.2], 0.85, true, D0 + L, 0);
      stand(out, cam, t, who(9, townsfolk(4), "w58"), [37.5, D0, 101.6], { expr: act(t, "neutral", [[25.7, "shock"], [26.92, "dazed"], [28.12, "grin"], [28.64, "laugh"]]), facing: -1 });
      street(out, cam, t, 280, 12, 46, 3.6);
      stand(out, cam, t, who(59, ENGO, "fore58"), [21.0, D0, 99.8], { expr: act(t, "stern", [[26.0, "nervous"], [27.9, "relief"], [28.64, "grin"]]), facing: 1, prop: "clipboard" });
      const wp: V3 = [29, D0 + L + 4.15, B58.z + 0.04];
      out.fx.push({ key: `win58|${act(t, "smile_closed", [[28.3, "smile"]])}|${q(lidAt(t, 60))}`, cw: 400, ch: 558, draw: (p) => fxWindow(p, MOM, act(t, "smile_closed", [[28.3, "smile"]]), lidAt(t, 60), 3), x: wp[0], y: wp[1], z: wp[2], w: 1.01, h: 1.41, yaw: 0 });
      card(out, "pot", 200, 240, fxPot, wp[0] + 0.28, wp[1] - 0.705 + 0.03 + 0.13, wp[2] + 0.14, 0.22, 0, { yaw: 0 });
      card(out, "pot2", 200, 240, fxPot, wp[0] - 0.3, wp[1] - 0.705 + 0.03 + 0.13, wp[2] + 0.14, 0.22, 0, { yaw: 0 });
      break;
    }
    case 9: { // 1860: the Lake Street block rises with the shops open; a row of men; the baker keeps selling
      const L = lift("blk", id, t);
      for (let k = 0; k < 16; k++) if (Math.abs(-114 + k * 2.75 - SHOP[0]) > 1.2) cranker(out, cam, t, 6 + k, [-114 + k * 2.75, Y, BLK.z - 1.75], 0.8, true, D0 + SW + L - 0.22); // v8: no jack under the shop door, so the baker is never hidden
      stand(out, cam, t, who(10, ENGO, "fore"), [-68.5, D0, 97.0], { expr: act(t, "stern", [[31.4, "grin"], [32.86, "stern"], [33.76, "shock"], [34.56, "grin"]]), facing: 1, prop: "clipboard" });
      const py = D0 + SW + 0.025 + L; // v8 (rule 60): feet on the porch boards (v21: porch top 2.5 cm above the sidewalk)
      stand(out, cam, t, who(12, BAKER, "baker"), [SHOP[0], py, BLK.z - 0.9], { expr: act(t, "grin", [[31.2, "shock"], [32.18, "grin"], [35.32, "laugh"], [35.9, "grin"]]), facing: 1, prop: "loaf" });
      card(out, "open", 400, 260, fxOpen, SHOP[0] - 1.25, py + 1.75, BLK.z - 0.08, 0.75, 0, { yaw: Math.PI });
      stand(out, cam, t, who(13, MOM, "cust"), [SHOP[0] + 1.75, Y, BLK.z - 2.6], { expr: act(t, "neutral", [[31.4, "shock"], [35.66, "smile"]]), facing: -1 });
      stand(out, cam, t, who(61, KID, "cust2"), [SHOP[0] + 2.6, Y, BLK.z - 2.9], { expr: idle(t, 61, ["laugh", "grin", "shock"]), facing: -1 }, 0.8);
      crowd(out, cam, t, 70, 6);
      street(out, cam, t, 200, -120, -64, 3.2, 108.1);
      break;
    }
    case 10: { // the Tremont House: guests at every window, then under it among 500 men
      const L = lift("tre", id, t);
      if (t < W(39.64) - 0.05) {
        for (const [k, x] of [[0, -11.5], [1, -9.5], [2, -7.5], [3, -5.5], [4, 5.5], [5, 7.5], [6, 9.5], [7, 11.5], [8, -1.5], [9, 1.5], [10, 3.5]] as const) cranker(out, cam, t, 12 + k, [x, Y, TRE.z - 0.45], 0.85, true, D0 + L, Math.PI);
        for (const [i, fl, o, k] of [[2, 1, WIN_A, 3], [5, 2, WIN_B, 4], [8, 1, WIN_C, 5], [10, 3, WIN_A, 6], [4, 3, WIN_C, 7]] as [number, number, Outfit, number][])
          window(out, t, o, `tw${i}${fl}`, k, treWin(i, fl, id, t), idle(t, k, ["smile", "smile_closed", "grin", "neutral"]));
        stand(out, cam, t, who(14, townsfolk(5), "p7a"), [11.2, Y, 108.9], { expr: act(t, "neutral", [[36.92, "shock"], [38.24, "dazed"]]), facing: -1 });
        stand(out, cam, t, who(15, townsfolk(6), "p7b"), [13.2, Y, 108.6], { expr: idle(t, 15, ["smile", "grin"]), facing: -1 });
        crowd(out, cam, t, 60);
        street(out, cam, t, 240, -40, 40);
      } else {
        let k = 0;
        for (const z of [112.2, 114.6, 117.0, 119.6]) for (const x of [-12.3, -9.9, -7.5, -5.1, -2.7, -0.3, 2.1, 4.5, 6.9, 9.3, 11.7]) {
          if ((k * 7) % 5 === 4) { k++; continue; }
          cranker(out, cam, t, 20 + k, [x + (z % 2 ? 0.2 : -0.2), D0 + 0.01, z], 0.78, false, D0 + L); k++;
        }
        // warm work lanterns hung from the beams along the aisle (the one warm emitter in the dark, teardown G)
        for (const x of [13.2, 8.1, 3.3, -1.5, -6.3, -11.1]) card(out, "lantern", 200, 520, fxLantern, x, D0 + L - 0.65, 115.5, 0.38);
      }
      break;
    }
    case 11: { // the guests barely noticed
      // (v19 self-review: the tea guest at the back table sat right behind the near diner, head stacked over head with his
      // body hidden: removed from this wide; he has his own close-up in take 2)
      sitSide(out, cam, t, who(4, WIN_B, "d1"), chairAt(1, 0), ...towardTable(1, 0), { expr: act(t, "smile", [[43.66, "laugh"], [44.32, "smile_closed"]]) }, "chair", [480, 615]);
      sitSide(out, cam, t, who(5, WIN_C, "d2"), chairAt(1, 1), ...towardTable(1, 1), { expr: idle(t, 5, ["grin", "laugh", "smile"]) }, "chair", [480, 615]);
      stand(out, cam, t, who(21, BAKER, "waiter"), [-562.0, D0, -620.3], { expr: act(t, "smile", [[44.02, "grin"]]), facing: -1 });
      break;
    }
    case 12: { // one guest: the front steps get one step taller every morning (milk bottle each morning, a puff of dust)
      const n = DAYS.filter((d) => t >= d - L2).length;
      stand(out, cam, t, who(16, GUESTO, "guest"), GUEST, { expr: act(t, "neutral", [[45.68, "smile"], [46.36, "nervous"], [47.2, "stern"], [47.52, "pained"], [48.24, "dazed"], [48.52, "pained"]]), facing: 1 });
      for (let i = 0; i < n; i++) card(out, "milk", 110, 260, fxMilk, 1.18 - i * 0.15, D0 + lift("tre", id, t) + 0.13, TRE.z - 0.17, 0.12, 0, { yaw: Math.PI }); // rule 67: on the top step (x -1.25..1.25, z TRE.z-0.35..TRE.z), never past its edge
      for (const d of DAYS) if (t >= d && t < d + 0.6) puff(out, t, d, 0, D0 + 0.3, TRE.z - 0.6, 1.2, 0.5);
      break;
    }
    case 13: { // like lifting the couch an inch at a time while the whole family sits on it
      const n = Math.max(0, Math.min(8, Math.floor((t - W(50.16) + L2) / 0.3) + 1)), up = 0.03 * n;
      const base = D0 + 0.3 + up, cw2 = 2.4, chh = (cw2 * 520) / 900, CZ = COUCH[2];
      card(out, "couchB", 900, 520, fxCouchBack, COUCH[0], base + chh / 2, CZ + 0.25, cw2, 0, { yaw: Math.PI });
      // rule 68 (owner Nov 12, pose C): hips ON the seat top, lap + shins + shoes in front of the cushion (feet dangle: the couch is jacked up);
      // dad and mom lean in toward the kid. Seat top = fxCouchBack seat line (design y 300 of 520).
      const seatTop = base + (chh * (520 - 300)) / 520, hipH = (o: Outfit, seed: number, sc: number) => 0.98 * 2 * headBlob(seed, BUILD[o.build ?? "adult"].a, 0).b * SU * sc;
      const KD = { ...KID, skin: SKINS[0] }, SZ = CZ - 0.17;
      sit(out, cam, t, who(17, DAD, "dad"), [COUCH[0] - 0.52, seatTop - hipH(DAD, 17, 1), SZ], { expr: act(t, "smile_closed", [[50.16, "nervous"], [51.3, "grin"], [52.34, "laugh"]]), facing: 1, tilt: 6, look: 1 }, 1, false);
      sit(out, cam, t, who(18, KD, "kid"), [COUCH[0] + 0.02, seatTop - hipH(KD, 18, 0.85), SZ + 0.01], { expr: act(t, "smile", [[50.32, "shock"], [51.0, "grin"], [51.96, "laugh"]]), facing: 0 }, 0.85, false);
      sit(out, cam, t, who(19, MOM, "mom"), [COUCH[0] + 0.53, seatTop - hipH(MOM, 19, 1), SZ], { expr: act(t, "smile_closed", [[50.52, "nervous"], [51.3, "smile"], [52.22, "laugh"]]), facing: -1, tilt: -6, look: -1 }, 1, false);
      card(out, "couchF", 900, 520, fxCouchFront, COUCH[0], base + chh / 2, CZ - 0.1, cw2, 0, { yaw: Math.PI });
      blob(out, COUCH[0], D0, CZ, 2.6);
      const fx = (810 - 450) * (cw2 / 900), top = (0.3 + up) / SU;
      for (const sd of [-1, 1] as const) {
        const w = who(43 + (sd > 0 ? 1 : 0), WORK(2 + (sd > 0 ? 1 : 0)), "jackman" + sd), crank = q(((t * 0.9 + (sd > 0 ? 0.5 : 0)) % 1 + 1) % 1, 12);
        const jx = COUCH[0] + sd * (fx + 0.367); // rule 65: he faces the couch, his jack stands under its corner foot
        out.places.push(person(cam, w, jx, D0, CZ - 0.32, { side: true, mirror: viewOf(cam, jx, CZ - 0.32, -sd, 0).mirror }, {}, { mode: "kneel", crank, screwTop: top, expr: idle(t, 43 + sd, ["grin", "stern"]), blink: lidAt(t, w.i) }, 1));
        blob(out, COUCH[0] + sd * (fx + 0.7), D0, CZ - 0.32, 1.2);
      }
      break;
    }
    case 14: { // young George Pullman runs the crews with a clipboard; years later, his sleeping car at the depot
      if (t < W(54.8)) {
        stand(out, cam, t, who(20, PULLO, "pull"), PULL, { expr: act(t, "smile", [[53.42, "stern"], [53.94, "grin"], [54.3, "smile"]]), facing: 1, prop: "clipboard" });
        for (const [k, x] of [[0, 4.5], [1, 11.5], [2, -4.5], [3, 2.5]] as const) cranker(out, cam, t, 30 + k, [x, Y, TRE.z - 0.12], 0.85, true, D0 + lift("tre", id, t));
        stand(out, cam, t, who(62, WORK(1), "runner"), [PULL[0] + 2.1, Y, PULL[2] - 0.5], { expr: idle(t, 62, ["nervous", "grin", "stern"]), facing: -1 });
      } else {
        stand(out, cam, t, who(20, PULLO, "pull2"), PULL2, { expr: act(t, "smile", [[55.8, "grin"], [56.68, "laugh"]]), facing: -1, wave: at(t, 56.68) ? 0.8 : undefined });
        // v8: the porter and two passengers only ever showed as a head over the crates or hid behind Pullman as the camera
        // swings round him, so they are left out (rule 56)
      }
      break;
    }
    case 15: { // the raised city still drains into the lake; a man at the shore drinks from it
      if (t >= W(59.2)) stand(out, cam, t, who(63, townsfolk(7), "shore"), SHORE, { expr: act(t, "smile", [[59.94, "smile_closed"], [60.2, "pained"]]), facing: 1, prop: "glass" });
      break;
    }
    case 16: { // 1900: the river flows backwards; debris drifts toward the lake, stops, and comes back
      const fp = flowPos(t);
      for (let i = 0; i < 14; i++) {
        const x = -60 + ((((i * 19 + fp) % 250) + 250) % 250), z = [-9, 7, -4, 11, -12, 3, 9][i % 7];
        if (x > 166) continue;
        card(out, `deb${i % 4}`, 300, 200, (p) => fxDebris(p, i % 4), x, 0.1, z, i % 4 === 1 ? 5.0 : 3.4, 0.6 * i, { flat: true });
        const ph = q(((t * 0.8 + i * 0.37) % 1 + 1) % 1, 12);
        card(out, `rip${ph}`, 300, 300, (p) => fxRipple(p, ph), x, 0.08, z, 7.0, 0, { flat: true, soft: true });
      }
      break;
    }
  }
  if (id === 5) dusk(out, t);
  foreground(out, id, t);
  return out;
};
export { FPS };
