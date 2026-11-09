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

// ---------------- the cast of the Eiffel Tower short ----------------
export type Stage = { places: Place[]; fx: FxPlace[] };
import { fxLetter, fxDemolish, fxContract, fxCalendar, fxAnemo, fxBall, fxRadio, fxWaves, fxStatic, fxTelegram, fxFlagFR, fxBucket, fxTable, fxWreck } from "./fx3";
import { W, World, TOWER, T_H, FOOT, EIFFEL2, ARTISTS, MAUP, DEAL, SCI, SHACK, GER, MARNE_Z, colX, MATA, GOLD, PAINT, HITS, P1Y, PTY } from "./story";

const EIF: Outfit = { jacket: "#2b2f3a", pants: "#3b3f52", boots: INK, hat: "tophat", beard: "#8a6a4a", buttons: "#e8c45a", skin: SKINS[0] };
const OFF: Outfit = { jacket: "#2b2f3a", pants: "#2b2f3a", boots: INK, hat: "bowler", moustache: "#4a3020", build: "stout", buttons: "#e8c45a", skin: SKINS[0] };
const artist = (v: number): Outfit => ({ jacket: ["#3f6fb5", "#c25a7a", "#5d7a3a", "#e2a13c"][v % 4], pants: ["#3b3f52", "#5a4a3a"][v % 2], boots: "#4a3426", hat: "beret",
  cap: ["#2b2830", "#8c2f3f", "#2d3f8a", "#2b2830"][v % 4], moustache: v % 2 ? "#4a3426" : undefined, skin: SKINS[(v + 1) % 4] });
const MAUPO: Outfit = { jacket: "#4a3a5a", pants: "#3b3f52", boots: INK, hat: "hair", hair: "#3a2a20", moustache: "#3a2a20", build: "stout", buttons: "#c9ccd2", skin: SKINS[0] };
const sci = (v: number): Outfit => ({ jacket: "#f4f2ec", pants: "#3b3f52", boots: INK, hat: "hair", hair: ["#9aa3ad", "#5a3b2a"][v % 2], moustache: v ? undefined : "#9aa3ad", buttons: "#c9ccd2", skin: SKINS[v % 4] });
const FRS: Outfit = { jacket: "#2d4fa0", pants: "#c8352e", boots: INK, hat: "kepi", phones: true, moustache: "#4a3426", buttons: "#e8c45a", skin: SKINS[1] };
const FRO: Outfit = { jacket: "#2d4fa0", pants: "#c8352e", boots: INK, hat: "kepi", buttons: "#e8c45a", sash: "#e8c45a", skin: SKINS[0], moustache: "#3a2a20" };
const GOP: Outfit = { jacket: "#6b7360", pants: "#5a6050", boots: INK, hat: "spike", phones: true, moustache: "#3a2a20", buttons: "#c9ccd2", skin: SKINS[0] };
const GSOL: Outfit = { jacket: "#6b7360", pants: "#5a6050", boots: INK, hat: "spike", rifle: true, belt: "#3a2a20", buttons: "#c9ccd2" };
const MATAO: Outfit = { jacket: "#e8c45a", pants: "#3b3f52", boots: "#8c3b4a", hat: "hair", hair: "#2a201a", dress: "#8c2f3f", skin: SKINS[2] };
const painter = (v: number): Outfit => ({ jacket: "#e8e2d0", pants: "#3b5b9a", boots: "#5a3b2a", hat: "cap", cap: ["#e2453c", "#3f6fb5"][v % 2], skin: SKINS[(v + 2) % 4], moustache: v ? "#4a3426" : undefined });
const crewO = (v: number): Outfit => ({ jacket: ["#6b4f3a", "#5a5f6b", "#7a5a3a"][v % 3], pants: "#3b3f52", boots: "#4a3426", hat: "cap", cap: "#5a5f6b", skin: SKINS[v % 4], moustache: v % 2 ? "#4a3426" : undefined });
const SUITS = ["#3b4256", "#5a5f6b", "#6b4f3a", "#2f3b52", "#4a5a4a"];
const parisian = (v: number): Outfit => v % 3 === 2
  ? { jacket: ["#f1e4c8", "#e8b0a0", "#b8d0e8"][v % 3], pants: "#3b3f52", boots: "#4a3426", hat: "hair", hair: ["#5a3b2a", "#d9a441", "#2a201a"][v % 3], dress: ["#d94f5c", "#3f8fb5", "#e2a13c"][v % 3], skin: SKINS[v % 4] }
  : { jacket: SUITS[v % 5], pants: SUITS[(v + 2) % 5], boots: INK, hat: v % 2 ? "bowler" : "tophat", skin: SKINS[v % 4], moustache: v % 4 === 1 ? "#4a3426" : undefined };

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
const hammerK = (t: number) => {
  let k = 1;
  for (const th of HITS) { const n = (t - th) * FPS; if (n >= -11 && n < -7) k = Math.min(k, 1 - smooth((n + 11) / 4)); else if (n >= -7 && n < 0) k = 0; }
  return k;
};
const flag = (out: Stage, t: number, x: number, z: number, h = 3.2, ph = 0) =>
  out.fx.push({ key: `flag${q((t * 3 + ph) % (Math.PI * 2), 8)}`, cw: 500, ch: 700, draw: (p) => fxFlagFR(p, q((t * 3 + ph) % (Math.PI * 2), 8)), x, y: D0 + h / 2, z, w: h * 0.714, h });
const crowd = (out: Stage, cam: CamInfo, t: number, spots: [number, number][], y: number, expr: (i: number) => Expr, i0 = 0, wave?: (i: number) => number | undefined) =>
  spots.forEach(([x, z], i) => stand(out, cam, t, who(i0 + i, parisian(i0 + i), "p" + ((i0 + i) % 15)), [x, y, z], { expr: expr(i), facing: 0, wave: wave?.(i) }));

export const stage = (id: number, t: number, _ws: World, cam: CamInfo): Stage => {
  const out: Stage = { places: [], fx: [] };
  const s = SHOTS[id - 1];
  LNAME = s.light;
  findSun(cam, SUN);
  void T_H; void TOWER;
  switch (id) {
    case 1: { // demolition crew at the south-west foot, hammers into the hook
      const k = q(hammerK(t), 30);
      [[-0.9, 0.6], [0.9, 1.2], [2.6, 0.2]].forEach(([dx, dz], i) =>
        stand(out, cam, t, who(10 + i, crewO(i), "crew" + i), [FOOT[0] + dx, D0, FOOT[2] + dz], { expr: at(t, 3.3) ? "grin" : "stern", prop: ["hammer", (k + i * 0.15) % 1], facing: i === 1 ? -1 : 1 }));
      out.fx.push({ key: "demolish", cw: 600, ch: 900, draw: fxDemolish, x: FOOT[0] - 0.1, y: D0 + 1.1, z: FOOT[2] + 2.2, w: 1.45, h: 2.2 });
      for (const h of HITS) burst(out, t, h, FOOT[0] + 1.0, D0 + 2.2, FOOT[2] + 3.4, 1.2);
      const sw = Math.sin(t * 1.7) * 0.5;
      void sw; // (the floating wrecking ball was cut: no crane to hang it from)
      break;
    }
    case 2: { // 1889: Eiffel proud, flags, cheering crowd
      stand(out, cam, t, who(1, EIF, "eif"), EIFFEL2, { expr: at(t, 5.86) ? "grin" : "smile", facing: 0, wave: at(t, 6.5) ? 0.6 : undefined });
      flag(out, t, EIFFEL2[0] - 3.4, EIFFEL2[2] + 2.5, 3.4, 0); flag(out, t, EIFFEL2[0] + 3.8, EIFFEL2[2] + 3.5, 3.4, 1.4);
      crowd(out, cam, t, [[-5.5, 80], [-3.2, 82], [4.6, 81], [6.6, 79.5], [-7.5, 77]].map(([x, z]) => [EIFFEL2[0] + x, EIFFEL2[2] - 74 + z] as [number, number]), D0, () => "grin", 30, (i) => (i % 2 ? 0.4 * Math.sin(t * 6 + i) + 0.4 : undefined));
      break;
    }
    case 3: { // the artists: "useless and monstrous"
      const loud = at(t, 12.1);
      [[-2.1, 0.8], [-0.9, 0.2], [1.2, 0.4], [2.3, 1.0]].forEach(([dx, dz], i) => {
        const lead = i === 2;
        stand(out, cam, t, who(40 + i, artist(i), "art" + i), [ARTISTS[0] + dx, D0, ARTISTS[2] + dz], { expr: loud ? (lead ? "shock" : "pained") : at(t, 8.48) ? "stern" : "neutral", facing: dx < 0 ? 1 : -1,
          prop: lead ? ["hold", "frame", 0] : null, wave: !lead && loud && i % 2 ? 0.5 + 0.3 * Math.sin(t * 9 + i) : undefined });
      });
      out.fx.push({ key: "letter", cw: 600, ch: 760, draw: fxLetter, x: ARTISTS[0] + 1.2, y: D0 + 1.42, z: ARTISTS[2] + 0.15, w: 0.74, h: 0.94, rot: 0.04 * Math.sin(t * 7) });
      break;
    }
    case 4: case 5: { // Maupassant's lunch on the first floor
      const eat = (Math.floor(t * 2.2) % 2) === 0;
      const expr: Expr = id === 5 ? "smile" : at(t, 16.5) ? (eat ? "lick" : "smile_closed") : "smile_closed";
      stand(out, cam, t, who(5, MAUPO, "maup"), MAUP, { expr, facing: id === 5 ? 1 : -1 });
      out.fx.push({ key: "table", cw: 700, ch: 520, draw: fxTable, x: MAUP[0] + 0.55, y: MAUP[1] + 0.52, z: MAUP[2] + 0.75, w: 1.4, h: 1.04 });
      break;
    }
    case 6: { // the deal: permit for twenty years, calendar 1889 -> 1909
      stand(out, cam, t, who(1, EIF, "eif"), [DEAL[0] - 0.9, D0, DEAL[2]], { expr: at(t, 24.36) ? "nervous" : "smile", facing: 1 });
      stand(out, cam, t, who(99, OFF, "off"), [DEAL[0] + 0.9, D0, DEAL[2]], { expr: at(t, 24.36) ? "smile" : "stern", facing: -1 });
      out.fx.push({ key: "contract", cw: 700, ch: 500, draw: fxContract, x: DEAL[0], y: D0 + 1.35, z: DEAL[2] - 0.35, w: 0.84, h: 0.6 });
      const fl = clamp01((t - W(22.4)) / 0.4), yr = fl >= 1 ? "1909" : "1889";
      out.fx.push({ key: `cal${yr}${q(fl, 10)}`, cw: 500, ch: 560, draw: (p) => fxCalendar(p, yr, fl > 0 && fl < 1 ? q(fl, 10) : 0), x: DEAL[0] + 2.9, y: D0 + 1.45, z: DEAL[2] - 0.4, w: 0.9, h: 1.0 });
      break;
    }
    case 7: { // scientists on the top deck: bolt the instruments on, drop things off
      stand(out, cam, t, who(60, sci(0), "sci0"), SCI, { expr: at(t, 28.26) ? "grin" : "smile", prop: at(t, 28.0) && t < W(29.6) ? ["hammer", q((t * 3) % 1, 30)] : null, facing: -1 });
      out.fx.push({ key: `anemo${q((t * 4) % 6.28, 6)}`, cw: 500, ch: 700, draw: (p) => fxAnemo(p, q((t * 4) % 6.28, 6)), x: SCI[0] - 1.3, y: SCI[1] + 0.63, z: SCI[2] + 0.3, w: 0.9, h: 1.26 });
      const B: V3 = [SCI[0] + 2.2, SCI[1], SCI[2] - 0.6];
      stand(out, cam, t, who(61, sci(1), "sci1"), B, { expr: at(t, 30.16) ? "grin" : "smile", facing: 1, wave: at(t, 29.9) ? 0.2 : undefined });
      const t0 = W(30.16), dt = t - t0, fy = dt < 0 ? B[1] + 1.5 : B[1] + 1.5 - 0.5 * 14 * dt * dt;
      if (fy > D0) out.fx.push({ key: "ball", cw: 200, ch: 200, draw: fxBall, x: B[0] + 0.6 + (dt > 0 ? 0.8 : 0), y: fy, z: B[2] - (dt > 0 ? 1.2 : 0.3), w: 0.42, h: 0.42 });
      break;
    }
    case 8: { // radio: rings out of the antenna
      const u = t - W(32.9);
      if (u > 0) out.fx.push({ key: `waves${q(u % 4, 15)}`, cw: 800, ch: 800, draw: (p) => fxWaves(p, q(u % 4, 15)), x: TOWER[0], y: D0 + T_H - 2, z: TOWER[2], w: 150, h: 150, soft: true });
      break;
    }
    case 9: { // French operator loves it / German operator hears it
      if (t < W(38.0) - 0.05) {
        stand(out, cam, t, who(70, FRS, "frs"), SHACK, { expr: at(t, 36.86) ? "grin" : "smile", facing: 0, wave: at(t, 37.16) ? 0.9 : undefined });
        out.fx.push({ key: "radio0", cw: 700, ch: 460, draw: (p) => fxRadio(p, 1), x: SHACK[0] + 0.1, y: D0 + 0.95, z: SHACK[2] - 0.7, w: 1.05, h: 0.69 });
        stand(out, cam, t, who(71, FRO, "fro"), [SHACK[0] - 1.6, D0, SHACK[2] + 1.0], { expr: "grin", facing: 1, wave: at(t, 37.2) ? 0.9 : undefined });
      }
      if (t >= W(38.0) - 0.15) {
        stand(out, cam, t, who(80, GOP, "gop"), GER, { expr: at(t, 39.48) ? "dazed" : at(t, 38.0) ? "shock" : "stern", facing: 0 });
        out.fx.push({ key: "radio1", cw: 700, ch: 460, draw: (p) => fxRadio(p, 0), x: GER[0] + 0.1, y: D0 + 0.95, z: GER[2] - 0.7, w: 1.05, h: 0.69 });
        if (at(t, 39.3)) out.fx.push({ key: `stat${q(t % 1, 15)}`, cw: 500, ch: 300, draw: (p) => fxStatic(p, q(t % 1, 15)), x: GER[0] + 0.5, y: D0 + 2.3, z: GER[2] - 0.8, w: 1.2, h: 0.72 });
      }
      break;
    }
    case 10: { // the Marne: the column marches east, the radio fills with static, they stop
      const stop = at(t, 46.1), x0 = colX(t);
      for (let r = 0; r < 3; r++) for (let c = 0; c < 4; c++) {
        const i = r * 4 + c, x = x0 - c * 1.6 - (r % 2) * 0.3, z = MARNE_Z - 1.1 + r * 1.1;
        if (!stop) marchX(out, cam, t, who(100 + i, GSOL, "gs"), x, D0, z, 1.15, { expr: at(t, 42.12) ? "nervous" : "stern" });
        else stand(out, cam, t, who(100 + i, GSOL, "gs"), [x, D0, z], { expr: i % 3 ? "dazed" : "nervous", facing: 0 });
      }
      const rx = x0 + 1.8;
      stand(out, cam, t, who(90, GOP, "gop"), [rx, D0, MARNE_Z - 1.6], { expr: at(t, 42.12) ? "dazed" : "stern", facing: -1 });
      out.fx.push({ key: "radio1", cw: 700, ch: 460, draw: (p) => fxRadio(p, 0), x: rx + 0.7, y: D0 + 0.5, z: MARNE_Z - 2.1, w: 0.9, h: 0.6 });
      if (at(t, 42.12)) for (let k = 0; k < 3; k++) out.fx.push({ key: `stat${q((t + k * 0.3) % 1, 15)}`, cw: 500, ch: 300, draw: (p) => fxStatic(p, q((t + k * 0.3) % 1, 15)),
        x: rx - k * 2.4, y: D0 + 2.6 + 0.3 * k, z: MARNE_Z - 1.8 + k * 0.8, w: 1.4, h: 0.84 });
      if (stop) puff(out, t, W(46.1), x0 + 0.5, D0, MARNE_Z, 1.2);
      break;
    }
    case 11: { // the coded message, then Mata Hari
      if (t < W(50.32) - 0.05) {
        stand(out, cam, t, who(70, FRS, "frs"), SHACK, { expr: at(t, 48.9) ? "shock" : "stern", facing: 0 });
        out.fx.push({ key: "radio0", cw: 700, ch: 460, draw: (p) => fxRadio(p, 1), x: SHACK[0] - 0.25, y: D0 + 0.95, z: SHACK[2] - 0.7, w: 1.05, h: 0.69 });
        if (at(t, 47.66)) out.fx.push({ key: "telegram", cw: 900, ch: 300, draw: fxTelegram, x: SHACK[0] + 0.45, y: D0 + 1.32, z: SHACK[2] - 0.75, w: 0.95, h: 0.32, rot: -0.05 });
      } else {
        stand(out, cam, t, who(95, MATAO, "mata"), MATA, { expr: at(t, 51.12) ? "shock" : "smile", facing: 0 });
        stand(out, cam, t, who(96, FRO, "fro"), [MATA[0] - 1.5, D0, MATA[2] + 0.5], { expr: "stern", facing: 1, wave: at(t, 50.48) ? 0.15 : undefined });
        stand(out, cam, t, who(97, FRO, "fro"), [MATA[0] + 1.5, D0, MATA[2] + 0.6], { expr: "stern", facing: -1 });
      }
      break;
    }
    case 12: { // golden: the same artists now admire it
      [[-2.1, 0.8], [-0.9, 0.2], [1.2, 0.4], [2.3, 1.0]].forEach(([dx, dz], i) =>
        stand(out, cam, t, who(40 + i, artist(i), "art" + i), [GOLD[0] + dx, D0, GOLD[2] + dz], { expr: i % 2 ? "relief" : "smile_closed", facing: dx < 0 ? 1 : -1 }));
      flag(out, t, GOLD[0] - 4.5, GOLD[2] + 4, 3.4, 0.6);
      break;
    }
    case 13: { // painters on a plank on the south-west leg
      [[-0.8, 0], [0.9, 0.1]].forEach(([dx, dz], i) =>
        stand(out, cam, t, who(120 + i, painter(i), "pnt" + i), [PAINT[0] + dx, PAINT[1], PAINT[2] + dz], { expr: at(t, 56.78) ? "grin" : "whistle", prop: ["hold", "brush", q((t * 1.4 + i * 0.5) % 1, 30)], facing: i ? -1 : 1 }));
      for (const dx of [-1.6, 1.8]) out.fx.push({ key: "bucket", cw: 300, ch: 300, draw: fxBucket, x: PAINT[0] + dx, y: PAINT[1] + 0.22, z: PAINT[2] - 0.3, w: 0.44, h: 0.44 });
      void fxBall;
      break;
    }
  }
  void P1Y; void PTY;
  return out;
};
export { FPS };
