// Our own flat 2D cartoon cast (riflemen, officer, townsfolk, kid, parent) + 2D effects, drawn on a canvas.
// Construction v2 (characters.md, our own cast): superellipse heads (pointed crown 1.75 / full jaw 2.3, chin taper,
// seeded side bulge + tilt), bean torsos, single-stroke limbs with ink-dot hands, a thick-thin plum outline weighted
// away from the light, soft painted crescents, deadpan lidded eyes, no blush, no catchlights.
// Design space 600 x 1000 units (soles at y = 975); the canvas transform scales it.
export const INK = "#241726";
export const SKIN = "#f6f0ec"; // v3: reference pale head tone
const WHITE = "#ffffff";
const MOUTH = "#5a1e28";
const TONGUE = "#e86e78";
type C3 = [number, number, number];
const SH_SKIN: C3 = [0.96, 0.86, 0.84]; // measured shadow/lit ratio on skin heads
const SH_CLOTH: C3 = [0.64, 0.66, 0.74]; // torsos: lit side -> far side ~0.65
const SH_FELT: C3 = [0.62, 0.62, 0.7];

export type Build = "adult" | "stout" | "kid";
export type Outfit = {
  jacket: string; pants: string; boots: string; hat?: string | null; belt?: string | null; buttons?: string; rifle?: boolean;
  sash?: string; sword?: boolean; moustache?: string; skin?: string; head?: number; cap?: string; hair?: string; dress?: string;
  build?: Build; beard?: string; phones?: boolean;
};
type P2 = [number, number];

const rad = (d: number) => (d * Math.PI) / 180;
const clamp = (x: number, a: number, b: number) => Math.max(a, Math.min(b, x));
export const mul = (c: string, m: C3) => {
  const n = parseInt(c.slice(1), 16);
  const ch = (v: number, k: number) => Math.min(255, Math.round(v * k)).toString(16).padStart(2, "0");
  return `#${ch((n >> 16) & 255, m[0])}${ch((n >> 8) & 255, m[1])}${ch(n & 255, m[2])}`;
};
export const shade = (c: string, k: number) => mul(c, [k, k, k]);
export const mix = (a: string, b: string, t: number) => {
  const A = parseInt(a.slice(1), 16), B = parseInt(b.slice(1), 16);
  const ch = (s: number) => Math.round(((A >> s) & 255) * (1 - t) + ((B >> s) & 255) * t).toString(16).padStart(2, "0");
  return `#${ch(16)}${ch(8)}${ch(0)}`;
};
/** deterministic per-character random in [0, 1) */
const rnd = (seed: number, k: number) => { const x = Math.sin(seed * 127.1 + k * 311.7) * 43758.5453; return x - Math.floor(x); };
const rotPts = (pts: P2[], a: number, cx: number, cy: number): P2[] =>
  pts.map(([x, y]) => [cx + (x - cx) * Math.cos(a) - (y - cy) * Math.sin(a), cy + (x - cx) * Math.sin(a) + (y - cy) * Math.cos(a)]);
const rotAbout = (q: P2, a: number, c: P2): P2 => rotPts([q], a, c[0], c[1])[0];
const lerp2 = (a: P2, b: P2, t: number): P2 => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];
/** smooth curve from a through (near) k to b, as a polyline */
const curve = (a: P2, k: P2, b: P2, n = 10): P2[] => {
  const c: P2 = [2 * k[0] - (a[0] + b[0]) / 2, 2 * k[1] - (a[1] + b[1]) / 2], out: P2[] = [];
  for (let i = 0; i <= n; i++) {
    const t = i / n, s = 1 - t;
    out.push([s * s * a[0] + 2 * s * t * c[0] + t * t * b[0], s * s * a[1] + 2 * s * t * c[1] + t * t * b[1]]);
  }
  return out;
};

export const RIFLEMAN: Outfit = { jacket: "#357650", pants: "#3d4440", boots: INK, hat: "shako", belt: "#f1efe6", buttons: "#d9dde0", rifle: true };
export const OFFICER: Outfit = { ...RIFLEMAN, hat: "shako_tall", buttons: "#e8c45a", sash: "#c0353a", sword: true, moustache: "#4a3020", rifle: false, belt: null, build: "stout" };
export const KID: Outfit = { jacket: "#f08a2c", pants: "#3b5b9a", boots: "#f4f1ea", hat: "cap", cap: "#e2453c", build: "kid" };
export const PARENT: Outfit = { jacket: "#7b5ac9", pants: "#3b3f52", boots: "#5a3b2a", hat: "hair", hair: "#5a3b2a" };
// v3: the references draw every head in one pale, near-white tone with cool shading (style, not ethnicity)
export const SKINS = ["#f6f0ec", "#f3ece8", "#f7f1ea", "#f1ebe9"];

export const soldier = (v = 0, extra: Partial<Outfit> = {}): Outfit => {
  const o: Outfit = { ...RIFLEMAN, skin: SKINS[v % 4] };
  if (v % 4 === 1) o.moustache = "#4a3426";
  if (v % 4 === 3) o.moustache = "#2a201a";
  return { ...o, ...extra };
};

export const townsfolk = (v = 0): Outfit => {
  const coats = ["#3f6fb5", "#8c3b4a", "#5d7a3a", "#b5653f", "#2f5f6a", "#7b5ac9"];
  const o: Outfit = { jacket: coats[v % 6], pants: "#3b3f52", boots: "#4a3426", skin: SKINS[v % 4] };
  return v % 2 ? { ...o, hat: "bonnet", dress: ["#d9a441", "#c25a7a", "#5a8fc2"][v % 3] } : { ...o, hat: "tophat" };
};

export class Pen {
  g: CanvasRenderingContext2D;
  ol = 12;
  /** [angle, cx, cy] rotation about (cx, cy), optional post-translation [.., dx, dy] */
  rot: number[] | null = null;
  constructor(g: CanvasRenderingContext2D) { this.g = g; }
  P(x: number, y: number): P2 {
    if (!this.rot) return [x, y];
    const r = this.rot, a = r[0], cx = r[1], cy = r[2], dx = r.length > 3 ? r[3] : 0, dy = r.length > 4 ? r[4] : 0, c = Math.cos(a), s = Math.sin(a);
    return [cx + (x - cx) * c - (y - cy) * s + dx, cy + (x - cx) * s + (y - cy) * c + dy];
  }
  path(pts: P2[], close: boolean) {
    const g = this.g;
    g.beginPath();
    pts.forEach((p, i) => { const [x, y] = this.P(p[0], p[1]); if (i) g.lineTo(x, y); else g.moveTo(x, y); });
    if (close) g.closePath();
  }
  /** filled shape with an ink outline; fill=null draws the outline only */
  poly(pts: P2[], fill: string | null, ol?: number) {
    const g = this.g, w = ol ?? this.ol;
    this.path(pts, true);
    if (fill) { g.fillStyle = fill; g.fill(); }
    if (w) { g.lineWidth = w; g.strokeStyle = INK; g.lineJoin = "round"; g.stroke(); }
  }
  ell(cx: number, cy: number, rx: number, ry: number, fill: string | null, ol?: number, a0 = 0, a1 = 360, rot = 0) {
    this.poly(ellPts(cx, cy, rx, ry, a0, a1, rot), fill, ol);
  }
  /** thick round-capped limb with an ink rim (effects, rope) */
  line(pts: P2[], fill: string, w: number, ink = true) {
    const g = this.g;
    g.lineCap = "round"; g.lineJoin = "round";
    if (ink) { this.path(pts, false); g.strokeStyle = INK; g.lineWidth = w + 2 * this.ol * 0.9; g.stroke(); }
    this.path(pts, false); g.strokeStyle = fill; g.lineWidth = w; g.stroke();
  }
  stroke(pts: P2[], w: number, fill = INK) {
    const g = this.g;
    g.lineCap = "round"; g.lineJoin = "round";
    this.path(pts, false); g.strokeStyle = fill; g.lineWidth = w; g.stroke();
  }
  arc(cx: number, cy: number, rx: number, ry: number, a0: number, a1: number, w: number, fill = INK) {
    const pts: P2[] = [];
    for (let i = 0; i <= 24; i++) pts.push([cx + rx * Math.cos(rad(a0 + ((a1 - a0) * i) / 24)), cy + ry * Math.sin(rad(a0 + ((a1 - a0) * i) / 24))]);
    this.stroke(pts, w, fill);
  }
  dot(cx: number, cy: number, r: number, fill = INK) {
    const [x, y] = this.P(cx, cy);
    this.g.beginPath(); this.g.arc(x, y, r, 0, Math.PI * 2); this.g.fillStyle = fill; this.g.fill();
  }
  /** draw with a closed shape as clip */
  clip(pts: P2[], fn: () => void) { const g = this.g; g.save(); this.path(pts, true); g.clip(); fn(); g.restore(); }
  /** flat fill + soft crescent on the side away from the light (light = canvas angle the light comes FROM).
   *  Radial ramp centred `shift` R toward the light: flat out to ~0.6 R on the far side, full shadow by ~0.8 R. */
  shadedFill(pts: P2[], base: string, shadow: string, light: number, R: number, shift = 0.45, r0 = 1.05, r1 = 1.25) {
    const g = this.g, n = pts.length;
    let cx = 0, cy = 0;
    for (const [x, y] of pts) { cx += x / n; cy += y / n; }
    const [gx, gy] = this.P(cx + Math.cos(light) * shift * R, cy + Math.sin(light) * shift * R);
    const gr = g.createRadialGradient(gx, gy, 0, gx, gy, r1 * R);
    gr.addColorStop(0, base); gr.addColorStop(r0 / r1, base); gr.addColorStop(1, shadow);
    this.path(pts, true); g.fillStyle = gr; g.fill();
  }
  /** broad gradient across a shape along the light: lit edge = base, far edge = shadow (torsos, coats) */
  gradFill(pts: P2[], base: string, shadow: string, light: number, flat = 0.22) {
    const g = this.g, dx = Math.cos(light), dy = Math.sin(light), n = pts.length;
    let cx = 0, cy = 0, lo = Infinity, hi = -Infinity;
    for (const [x, y] of pts) { cx += x / n; cy += y / n; const d = x * dx + y * dy; lo = Math.min(lo, d); hi = Math.max(hi, d); }
    const dc = cx * dx + cy * dy;
    const [ax, ay] = this.P(cx + dx * (hi - dc), cy + dy * (hi - dc)), [bx, by] = this.P(cx + dx * (lo - dc), cy + dy * (lo - dc));
    const gr = g.createLinearGradient(ax, ay, bx, by);
    gr.addColorStop(0, base); gr.addColorStop(flat, base); gr.addColorStop(1, shadow);
    this.path(pts, true); g.fillStyle = gr; g.fill();
  }
  /** thick-thin ink ring: w(θ) = w0 (1 + k cos(θ − thick)), θ from the contour centroid (canvas angles) */
  inkRing(pts: P2[], w0: number, thick: number, k = 0.45, col = INK) {
    const n = pts.length;
    let cx = 0, cy = 0;
    for (const [x, y] of pts) { cx += x / n; cy += y / n; }
    const out: P2[] = [], inn: P2[] = [];
    pts.forEach((q, i) => {
      const a = pts[(i + n - 1) % n], b = pts[(i + 1) % n];
      let nx = b[1] - a[1], ny = a[0] - b[0]; // outward normal for clockwise-on-screen contours
      const l = Math.hypot(nx, ny) || 1; nx /= l; ny /= l;
      const h = 0.5 * w0 * (1 + k * Math.cos(Math.atan2(q[1] - cy, q[0] - cx) - thick));
      out.push([q[0] + nx * h, q[1] + ny * h]); inn.push([q[0] - nx * h, q[1] - ny * h]);
    });
    const g = this.g;
    const trace = (r: P2[]) => { r.forEach(([x0, y0], i) => { const [x, y] = this.P(x0, y0); if (i) g.lineTo(x, y); else g.moveTo(x, y); }); g.closePath(); };
    g.beginPath(); trace(out); trace(inn.reverse());
    g.fillStyle = col; g.fill("evenodd");
  }
  /** flat strap with a thin ink rim (cross belts, sash, rifle, handles) */
  band(pts: P2[], fill: string, w: number, rim: number, cap: CanvasLineCap = "butt") {
    const g = this.g; g.lineCap = cap; g.lineJoin = "round";
    this.path(pts, false); g.strokeStyle = INK; g.lineWidth = w + 2 * rim; g.stroke();
    this.path(pts, false); g.strokeStyle = fill; g.lineWidth = w; g.stroke();
    g.lineCap = "round";
  }
}

const ellPts = (cx: number, cy: number, rx: number, ry: number, a0 = 0, a1 = 360, rot = 0, n = 48): P2[] => {
  const r = rad(rot), pts: P2[] = [];
  for (let i = 0; i <= n; i++) {
    const a = rad(a0 + ((a1 - a0) * i) / n), x = rx * Math.cos(a), y = ry * Math.sin(a);
    pts.push([cx + x * Math.cos(r) - y * Math.sin(r), cy + x * Math.sin(r) + y * Math.cos(r)]);
  }
  return pts;
};

const rrect = (x0: number, y0: number, x1: number, y1: number, r: number, n = 8): P2[] => {
  const pts: P2[] = [];
  for (const [cx, cy, a] of [[x1 - r, y0 + r, -90], [x1 - r, y1 - r, 0], [x0 + r, y1 - r, 90], [x0 + r, y0 + r, 180]])
    for (let i = 0; i <= n; i++) pts.push([cx + r * Math.cos(rad(a + (90 * i) / n)), cy + r * Math.sin(rad(a + (90 * i) / n))]);
  return pts;
};

/** tapered stroke, thick end at a: brows, moustache halves */
const taper = (p: Pen, a: P2, b: P2, wa: number, wb: number, col = INK) => {
  const dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1, nx = -dy / l, ny = dx / l;
  p.poly([[a[0] + nx * wa / 2, a[1] + ny * wa / 2], [b[0] + nx * wb / 2, b[1] + ny * wb / 2],
    [b[0] - nx * wb / 2, b[1] - ny * wb / 2], [a[0] - nx * wa / 2, a[1] - ny * wa / 2]], col, 0);
  p.dot(a[0], a[1], wa / 2, col); p.dot(b[0], b[1], wb / 2, col);
};

// ---------------- contours ----------------
export type Blob = { a: number; b: number; nTop: number; nBot: number; egg: number; asym: number; rot: number; noise: number; seed: number };

/** superellipse "bean": separate crown / jaw exponents, egg taper (neg = narrower chin), one-side bulge, soft noise.
 *  Points run right -> down -> left -> up (clockwise on screen). */
export const blobPts = (cx: number, cy: number, B: Blob, n = 72): P2[] => {
  const ph = [rnd(B.seed, 11), rnd(B.seed, 12), rnd(B.seed, 13)].map((v) => v * Math.PI * 2);
  const pts: P2[] = [];
  for (let i = 0; i < n; i++) {
    const t = (i / n) * Math.PI * 2, c = Math.cos(t), s = Math.sin(t), e = 2 / (s < 0 ? B.nTop : B.nBot);
    let X = Math.sign(c) * Math.abs(c) ** e;
    const Y = Math.sign(s) * Math.abs(s) ** e;
    X *= (1 + B.egg * Y) * (1 + B.asym * Math.sign(X));
    const r = 1 + B.noise * (Math.cos(2 * t + ph[0]) + 0.7 * Math.cos(3 * t + ph[1]) + 0.5 * Math.cos(4 * t + ph[2]));
    const x = B.a * X * r, y = B.b * Y * r;
    pts.push([cx + x * Math.cos(B.rot) - y * Math.sin(B.rot), cy + x * Math.sin(B.rot) + y * Math.cos(B.rot)]);
  }
  return pts;
};

/** measured head: H/W 0.94, slightly pointed crown (1.75), fuller jaw (2.3), chin taper -0.12, 8 % bulge to the facing side */
export const headBlob = (seed: number, a = 118, facing = 0): Blob => ({
  a, b: a * (0.94 + 0.08 * (rnd(seed, 1) - 0.5)),
  nTop: 1.75 + 0.3 * (rnd(seed, 2) - 0.5), nBot: 2.3 + 0.3 * (rnd(seed, 3) - 0.5),
  egg: -0.12 + 0.06 * (rnd(seed, 4) - 0.5),
  asym: (0.06 + 0.04 * rnd(seed, 5)) * (facing || (rnd(seed, 6) < 0.5 ? -1 : 1)),
  rot: rad(8 * (rnd(seed, 7) - 0.5)), noise: 0.008, seed,
});

/** thickest outline direction: away from the light, pulled toward the ground (64 deg measured for upper-left light) */
export const thickAngle = (light: number) => Math.atan2(-Math.sin(light) + 0.8, -Math.cos(light));
const DEF_LIGHT = rad(-120);

// ---------------- faces ----------------
export type Expr = "neutral" | "stern" | "grin" | "laugh" | "whistle" | "nervous" | "shock" | "relief" | "relief_open" | "dazed"
  | "pained" | "smile" | "smile_closed" | "lick";
type EyeK = "dot" | "small" | "lid" | "slit" | "happy" | "dash" | "squeeze" | "shock" | "shockHalf" | "spiral";
type MouthK = "dash" | "frown" | "smirk" | "smile" | "smileWide" | "grin" | "laugh" | "o" | "O" | "wave" | "teeth" | "lick";
/** eyes [back, front], brows [inner, outer] offsets in u (+ = down), mouth kind */
const FACE: Record<Expr, { eye: [EyeK, EyeK]; brow: [number, number]; mouth: MouthK }> = {
  neutral: { eye: ["lid", "lid"], brow: [0, -1], mouth: "dash" },
  stern: { eye: ["lid", "lid"], brow: [3, -2], mouth: "frown" },
  grin: { eye: ["happy", "happy"], brow: [-3, -3], mouth: "grin" },
  laugh: { eye: ["squeeze", "squeeze"], brow: [-4, -4], mouth: "laugh" },
  whistle: { eye: ["dash", "dash"], brow: [-2, -4], mouth: "o" },
  nervous: { eye: ["small", "small"], brow: [-3, 2], mouth: "wave" },
  shock: { eye: ["shock", "shock"], brow: [-7, -6], mouth: "O" },
  relief: { eye: ["happy", "happy"], brow: [-2, 1], mouth: "smileWide" },
  relief_open: { eye: ["happy", "happy"], brow: [-2, 1], mouth: "grin" },
  dazed: { eye: ["spiral", "spiral"], brow: [-3, 2], mouth: "wave" },
  pained: { eye: ["squeeze", "lid"], brow: [-3, 2], mouth: "teeth" },
  smile: { eye: ["dot", "dot"], brow: [0, -1], mouth: "smirk" },
  smile_closed: { eye: ["happy", "happy"], brow: [0, -1], mouth: "smile" },
  lick: { eye: ["dot", "dot"], brow: [0, -1], mouth: "lick" },
};
const halfLid = (k: EyeK): EyeK => (k === "dot" || k === "small" ? "lid" : k === "lid" ? "slit" : k === "shock" ? "shockHalf" : k);
const eyeKind = (k: EyeK, lid: number): EyeK =>
  lid >= 1 && k !== "happy" && k !== "squeeze" && k !== "spiral" ? "dash" : lid > 0 ? halfLid(k) : k;
const lidOf = (b: boolean | number | undefined) => (b === true ? 1 : Number(b) || 0);

const eye = (p: Pen, kind: EyeK, x: number, ey: number, u: number, side: number, look: number, skin: string) => {
  const lx = x + look * 3 * u, lw = 3.8 * u;
  switch (kind) {
    case "dot": p.ell(lx, ey, 3.8 * u, 5.5 * u, INK, 0); break;
    case "small": p.ell(lx, ey, 3 * u, 4.4 * u, INK, 0); break;
    case "lid": p.ell(lx, ey - u, 7 * u, 6 * u, INK, 0, 0, 180); p.stroke([[x - 9 * u, ey - u], [x + 9 * u, ey - u]], lw); break;
    case "slit": p.ell(lx, ey, 7 * u, 2.6 * u, INK, 0, 0, 180); p.stroke([[x - 9 * u, ey], [x + 9 * u, ey]], lw); break;
    case "happy": p.arc(x, ey + 3 * u, 8 * u, 6 * u, 200, 340, lw); break;
    case "dash": p.stroke([[x - 8.5 * u, ey], [x + 8.5 * u, ey]], lw); break;
    case "squeeze": p.stroke([[x + 6 * u * side, ey - 5 * u], [x - 6 * u * side, ey], [x + 6 * u * side, ey + 5 * u]], lw); break;
    case "shock": case "shockHalf":
      p.ell(x, ey, 11 * u, 11 * u, WHITE, 2.6 * u); p.dot(lx - side * 1.5 * u, ey + 1.5 * u, 3 * u);
      if (kind === "shockHalf") { p.ell(x, ey, 11 * u, 11 * u, skin, 0, 180, 360); p.stroke([[x - 11 * u, ey], [x + 11 * u, ey]], 2.6 * u); }
      break;
    default: {
      const s: P2[] = [];
      for (let t = 1; t < 15; t++) s.push([x + Math.cos(t * 0.9) * t * 0.55 * u, ey + Math.sin(t * 0.9) * t * 0.55 * u]);
      p.stroke(s, 2.4 * u);
    }
  }
};

/** open "D" mouth with a white teeth band (+ tongue) */
const dmouth = (p: Pen, mx: number, y: number, rx: number, ry: number, u: number, tongue = false) => {
  p.ell(mx, y, rx, ry, MOUTH, 0, 0, 180);
  p.clip([[mx - rx, y], [mx + rx, y], [mx + rx, y + 3 * u], [mx - rx, y + 3 * u]], () => p.ell(mx, y, rx, ry, WHITE, 0, 0, 180));
  if (tongue) p.ell(mx + 2 * u, y + 0.62 * ry, 0.4 * rx, 0.28 * ry, TONGUE, 0);
  p.ell(mx, y, rx, ry, null, 3 * u, 0, 180);
};

const mouth = (p: Pen, kind: MouthK, mx: number, my: number, u: number, k = 1) => {
  const mw = 4 * u;
  switch (kind) {
    case "dash": p.stroke([[mx - 5.5 * u * k, my], [mx + 5.5 * u * k, my - 0.8 * u]], mw); break;
    case "frown": p.arc(mx, my + 3 * u, 6.5 * u * k, 3.5 * u, 200, 340, mw); break;
    case "smirk": p.arc(mx + u, my - 3 * u, 7 * u * k, 4 * u, 10, 150, mw); break;
    case "smile": p.arc(mx, my - 3 * u, 8 * u * k, 4.5 * u, 20, 160, mw); break;
    case "smileWide": p.arc(mx, my - 4 * u, 11 * u * k, 6 * u, 15, 165, mw); break;
    case "grin": dmouth(p, mx, my - u, 12 * u * k, 8 * u, u); break;
    case "laugh": dmouth(p, mx, my, 16 * u * k, 11 * u, u, true); break;
    case "o": p.ell(mx + 4 * u, my, 3.5 * u, 4 * u, MOUTH, 2.8 * u); break;
    case "O": p.ell(mx, my + 2 * u, 9 * u * k, 11 * u, MOUTH, 3.2 * u); break;
    case "wave": { const s: P2[] = []; for (let i = 0; i <= 12; i++) s.push([mx - 9 * u * k + i * 1.5 * u * k, my + 1.5 * u * Math.sin(i * 1.3)]); p.stroke(s, 3 * u); break; }
    case "teeth":
      p.poly([[mx - 12 * u * k, my - 4 * u], [mx + 12 * u * k, my - 4 * u], [mx + 11 * u * k, my + 4 * u], [mx - 11 * u * k, my + 4 * u]], WHITE, 3 * u);
      for (const j of [-1, 0, 1]) p.stroke([[mx + j * 6 * u * k, my - 4 * u], [mx + j * 6 * u * k, my + 4 * u]], 1.5 * u);
      break;
    case "lick": p.arc(mx, my - 3 * u, 8 * u * k, 4.5 * u, 20, 160, mw); p.ell(mx + 6 * u * k, my + 3 * u, 3.6 * u, 4.6 * u, TONGUE, 2.4 * u); break;
  }
};

/** face v2 (front / 3-4). u = 1 % of the head path width W. Eyes 26u apart on the centre line, brows 20u up, mouth 20u
 *  down, everything slid toward the facing side. No blush, no catchlights. */
const faceFront = (p: Pen, cx: number, cy: number, W: number, expr: Expr, facing: number, look: number, lid: number, brim: boolean,
  skin: string, moustache?: string, stout = false) => {
  const u = W / 100, F = FACE[expr], fx = cx + 7 * u * facing;
  const ex = (F.eye[0] === "shock" ? 12 : 13) * u, ey = cy;
  for (const side of [-1, 1]) {
    const x = fx + side * ex;
    const kind = eyeKind(F.eye[(facing ? side === facing : side > 0) ? 1 : 0], lid);
    eye(p, kind, x, ey, u, side, look, skin);
    const [dI, dO] = F.brow, by = ey - (brim ? 12.5 : 20) * u;
    if (kind === "shock" || kind === "shockHalf") p.arc(x, by - 6 * u, 9 * u, 3 * u, 200, 340, 4 * u);
    else taper(p, [x - side * 8.5 * u, by + dI * u], [x + side * 8.5 * u, by + dO * u], 5 * u, 2.5 * u);
  }
  const mx = cx + 8 * u * facing, my = cy + 20 * u;
  mouth(p, F.mouth, mx, my, u);
  if (moustache) for (const s of [-1, 1])
    taper(p, [mx + s * 1.5 * u, cy + 12.5 * u], [mx + s * (stout ? 19 : 15) * u, cy + (stout ? 10.5 : 15) * u], stout ? 5.5 * u : 4.5 * u, 1.6 * u, moustache);
  if (expr === "nervous") p.ell(cx + 40 * u * (facing || 1), cy - 22 * u, 3 * u, 5 * u, "#9fd4ff", 2 * u);
};

/** profile face (facing screen-right): one eye, brow, nose tick, mouth near the front edge; no skin bump nose, no ear */
const faceSide = (p: Pen, hx: number, hy: number, W: number, expr: Expr, lid: number, brim: boolean, skin: string, moustache?: string, stout = false) => {
  const u = W / 100, F = FACE[expr], ex = hx + 27 * u, ey = hy;
  const kind = eyeKind(F.eye[1], lid);
  eye(p, kind, ex, ey, u, 1, 0.6, skin);
  const by = ey - (brim ? 12.5 : 20) * u, [dI, dO] = F.brow;
  if (kind === "shock" || kind === "shockHalf") p.arc(ex, by - 6 * u, 9 * u, 3 * u, 200, 340, 4 * u);
  else taper(p, [ex + 8 * u, by + dI * u], [ex - 7 * u, by - u + dO * u], 5 * u, 2.5 * u);
  p.stroke([[hx + 44 * u, hy + 4 * u], [hx + 47.5 * u, hy + 9 * u], [hx + 43 * u, hy + 10 * u]], 3 * u);
  mouth(p, F.mouth, hx + 33 * u, hy + 21 * u, u, 0.62);
  if (moustache) taper(p, [hx + 41 * u, hy + 13.5 * u], [hx + 25 * u, hy + (stout ? 11.5 : 16) * u], stout ? 5.5 * u : 4.5 * u, 1.6 * u, moustache);
  if (expr === "nervous") p.ell(hx - 30 * u, hy - 24 * u, 3 * u, 5 * u, "#9fd4ff", 2 * u);
};

// ---------------- hats ----------------
const BONNET = "#e9cf8f", BONNET_BRIM = "#d6b46a";
/** parts of a hat that sit behind the head (bonnet) */
const hatBehind = (p: Pen, o: Outfit, H: Blob, cx: number, hc: number, light: number, thick: number, ow: number, side: boolean) => {
  if (o.hat !== "bonnet_old") return;
  const bb = blobPts(cx - (side ? 12 : 0) * (H.a / 50), hc - 0.07 * 2 * H.b, { ...H, a: H.a * 1.17, b: H.b * 1.13, asym: 0, egg: 0.04, seed: H.seed + 3 });
  p.shadedFill(bb, BONNET, mul(BONNET, SH_CLOTH), light, H.a * 1.17);
  p.inkRing(bb, ow * 0.85, thick);
};

const hatOn = (p: Pen, o: Outfit, hp: P2[], H: Blob, cx: number, hc: number, light: number, seed: number, facing: number, side: boolean) => {
  const W = 2 * H.a, HH = 2 * H.b, u = W / 100, crown = hc - H.b, ow = 0.85 * 2.9 * u;
  const a = H.rot + rad(4 * (rnd(seed, 20) - 0.5)); // tilt with the head, +-2 deg extra
  const R = (pts: P2[]) => rotPts(pts, a, cx, hc);
  const sag = (yb: number, wb: number): P2[] => {
    const base: P2[] = [];
    for (let i = 0; i <= 12; i++) { const t = i / 12; base.push([cx + wb * (2 * t - 1), yb + 3 * u * (1 - (2 * t - 1) ** 2)]); }
    return base;
  };
  if (o.hat === "shako" || o.hat === "shako_tall") {
    const tall = o.hat === "shako_tall", yb = crown + 0.25 * HH, ht = (tall ? 0.66 : 0.56) * HH, wb = 46 * u, wt = 52 * u;
    const body = R([...sag(yb, wb).reverse(), [cx - wt, yb - ht], [cx + wt, yb - ht]]);
    p.shadedFill(body, "#3a3d47", "#24262d", light, wt, 0.4);
    if (tall) p.clip(body, () => p.band(R([[cx - wt - 5 * u, yb - ht + 0.07 * HH], [cx + wt + 5 * u, yb - ht + 0.07 * HH]]), "#e8c45a", 0.06 * HH, 1.5 * u));
    p.poly(body, null, ow);
    const deg = (a * 180) / Math.PI;
    if (side) {
      p.poly(R([[cx + 36 * u, yb - 1 * u], [cx + 60 * u, yb + 8 * u], [cx + 34 * u, yb + 6 * u]]), "#16171b", 2.5 * u);
      const [tx, ty] = R([[cx + 24 * u, yb - ht - 6 * u]])[0];
      p.ell(tx, ty, 7 * u, 7 * u, "#2b7a4b", 2.5 * u);
    } else {
      const [px, py] = R([[cx + 3 * u * facing, yb + 3 * u]])[0];
      p.ell(px, py, 34 * u, 0.045 * HH, "#16171b", 2.5 * u, 0, 180, deg); // peak
      const [bx, by] = R([[cx, yb - 0.45 * ht]])[0];
      p.ell(bx, by, 7 * u, 6 * u, tall ? "#e8c45a" : "#c9ccd2", 2 * u, 0, 360, deg); // badge plate
      p.arc(bx, by, 3.5 * u, 2.8 * u, 200, 500, 1.6 * u);
      const [tx, ty] = R([[cx, yb - ht - 6 * u]])[0];
      p.ell(tx, ty, 7 * u, 7 * u, "#2b7a4b", 2.5 * u); // green tuft
    }
  } else if (o.hat === "cap" || o.hat === "hair") {
    const cut = crown + (o.hat === "cap" ? 0.25 : 0.27) * HH;
    const keep = (x: number, y: number) => y < cut || (side && o.hat === "hair" && x < cx - 6 * u && y < hc + 0.42 * H.b);
    // start the arc at the first kept point after a dropped one, so the kept run is contiguous and the cut closes it
    const n = hp.length, startIdx = Math.max(0, hp.findIndex(([x, y], i) => keep(x, y) && !keep(hp[(i + n - 1) % n][0], hp[(i + n - 1) % n][1])));
    const arc = [...hp.slice(startIdx), ...hp.slice(0, startIdx)].filter(([x, y]) => keep(x, y))
      .map(([x, y]) => [cx + (x - cx) * 1.03, hc + (y - hc) * 1.03] as P2);
    if (arc.length < 3) return;
    if (o.hat === "hair") { // scalloped lower edge
      const [x0, y0] = arc[arc.length - 1], [x1, y1] = arc[0];
      for (let i = 1; i < 6; i++) arc.push([x0 + ((x1 - x0) * i) / 6, y0 + ((y1 - y0) * i) / 6 + (i % 2 ? 4 * u : 0)]);
    }
    const col = o.hat === "cap" ? o.cap! : o.hair!;
    p.shadedFill(arc, col, mul(col, SH_FELT), light, H.a, 0.35);
    p.poly(arc, null, ow);

    if (o.hat === "cap") {
      const vc = shade(col, 0.62);
      const top = arc.reduce((m, q) => (q[1] < m[1] ? q : m), arc[0]);
      p.clip(arc, () => { // two crown seams meeting at the button
        for (const dx of [-0.5, 0.5]) p.stroke([[top[0], top[1]], [cx + dx * H.a, cut]], 1.4 * u, shade(col, 0.55));
        p.band([[cx - H.a * 1.2, cut - 4 * u], [cx + H.a * 1.2, cut - 4 * u]], shade(col, 0.8), 7 * u, 1 * u); // band
      });
      p.poly(arc, null, ow);
      p.ell(top[0], top[1] + 2 * u, 5 * u, 3.5 * u, vc, 1.6 * u); // button
      if (side) p.poly(R([[cx + 30 * u, cut - 5 * u], [cx + 58 * u, cut - 1 * u], [cx + 80 * u, cut + 6 * u], [cx + 56 * u, cut + 9 * u], [cx + 30 * u, cut + 5 * u]]), vc, ow);
      else { // visor: a curved peak hanging from the band, wider at the front, overlapping the band so it is joined
        const s = facing ? facing * 0.35 : 0, vw = 42 * u, vd = 0.085 * HH, ox = cx + s * 10 * u, vis: P2[] = [];
        for (let i = 0; i <= 16; i++) { const x = -1 + i / 8; vis.push([ox + vw * x, cut - 5 * u + 2 * u * x * x]); }
        for (let i = 16; i >= 0; i--) { const x = -1 + i / 8; vis.push([ox + vw * 1.05 * x, cut - 5 * u + vd * (1 - 0.55 * x * x)]); }
        p.poly(R(vis), vc, ow);
        p.stroke(R(Array.from({ length: 9 }, (_, i) => { const x = -0.8 + i * 0.2; return [ox + vw * x, cut - 5 * u + vd * 0.55 * (1 - 0.6 * x * x)] as P2; })), 1.1 * u, shade(col, 0.45));
      }
    }
  } else if (o.hat === "tophat") {
    const yb = crown + 0.22 * HH, ht = 0.8 * HH, wb = 0.31 * W, wt = 0.33 * W, col = "#2e2a36";
    const body = R([...sag(yb, wb).reverse(), [cx - wt, yb - ht], [cx + wt, yb - ht]]);
    p.shadedFill(body, col, mul(col, SH_FELT), light, wt, 0.4);
    p.clip(body, () => p.band(R([[cx - wt - 4 * u, yb - 0.13 * HH], [cx + wt + 4 * u, yb - 0.13 * HH]]), shade(o.jacket, 0.9), 0.14 * HH, 0.8 * u));
    p.poly(body, null, ow);
    const [bx, by] = R([[cx, yb + 1 * u]])[0];
    p.ell(bx, by, 0.45 * W, 0.05 * HH, "#1d1b22", ow, 0, 360, (a * 180) / Math.PI);
  } else if (o.hat === "bowler" || o.hat === "hardhat") {
    const hard = o.hat === "hardhat", col = hard ? "#f2c230" : "#2b2830", yb = crown + (hard ? 0.3 : 0.34) * HH, ht = (hard ? 0.44 : 0.52) * HH, wb = (hard ? 0.56 : 0.57) * W;
    const dome: P2[] = [];
    for (let i = 0; i <= 24; i++) { const a = Math.PI + (Math.PI * i) / 24; dome.push([cx + wb * 0.92 * Math.cos(a), yb + ht * Math.sin(a)]); }
    const body = R(dome);
    p.shadedFill(body, col, mul(col, SH_FELT), light, wb, 0.4);
    if (!hard) p.clip(body, () => p.band(R([[cx - wb - 4 * u, yb - 0.08 * HH], [cx + wb + 4 * u, yb - 0.08 * HH]]), "#5a2a2e", 0.08 * HH, 0.8 * u));
    else p.clip(body, () => p.band(R([[cx, yb - ht - 4 * u], [cx, yb]]), shade(col, 0.85), 0.12 * W, 0.8 * u));
    p.poly(body, null, ow);
    const [bx, by] = R([[cx, yb + 1 * u]])[0];
    p.ell(bx, by, wb * (hard ? 1.12 : 1.08), 0.045 * HH, hard ? shade(col, 0.9) : "#1d1b22", ow, 0, 360, (a * 180) / Math.PI);
  } else if (o.hat === "cowboy" || o.hat === "sunhat") {
    const cow = o.hat === "cowboy", col = cow ? "#c9a26a" : "#efd59a", yb = crown + 0.33 * HH, ht = (cow ? 0.62 : 0.42) * HH, wb = 0.53 * W, wt = (cow ? 0.46 : 0.44) * W;
    const top: P2[] = cow ? [[cx - wt, yb - ht], [cx - wt * 0.35, yb - ht * 0.88], [cx, yb - ht * 0.78], [cx + wt * 0.35, yb - ht * 0.88], [cx + wt, yb - ht]]
      : Array.from({ length: 13 }, (_, i) => { const a = Math.PI + (Math.PI * i) / 12; return [cx + wt * Math.cos(a), yb - ht * 0.3 + ht * 0.7 * Math.sin(a)] as P2; });
    const body = R([...sag(yb, wb).reverse(), ...top]);
    p.shadedFill(body, col, mul(col, SH_FELT), light, wt, 0.4);
    p.clip(body, () => p.band(R([[cx - wt - 4 * u, yb - 0.1 * HH], [cx + wt + 4 * u, yb - 0.1 * HH]]), cow ? "#5a3b2a" : "#d0453a", 0.09 * HH, 0.8 * u));
    p.poly(body, null, ow);
    const bw = (cow ? 0.98 : 1.02) * W, brim: P2[] = [];
    for (let i = 0; i <= 24; i++) { const x = -1 + (2 * i) / 24; brim.push([cx + bw * x, yb + 2 * u - (cow ? 9 * u * x ** 4 : 2 * u * x * x)]); }
    for (let i = 24; i >= 0; i--) { const x = -1 + (2 * i) / 24; brim.push([cx + bw * x, yb + 2 * u + 0.05 * HH * (1 - x * x) - (cow ? 9 * u * x ** 4 : 2 * u * x * x) + 3 * u]); }
    p.poly(R(brim), shade(col, 0.92), ow);
  } else if (o.hat === "beret") {
    // flat painter's beret, tipped to one side, with the little stalk on top
    const col = o.cap ?? "#2b2830", s = facing || 1, yb = crown + 0.2 * HH;
    const top: P2[] = Array.from({ length: 25 }, (_, i) => { const t = Math.PI + (Math.PI * i) / 24; return [cx + s * 6 * u + 0.6 * W * Math.cos(t), yb - 0.06 * HH + 0.2 * HH * Math.sin(t)] as P2; });
    const body = R([...top, [cx + s * 6 * u + 0.6 * W, yb + 0.02 * HH], [cx - 0.5 * W + s * 6 * u, yb + 0.05 * HH]]);
    p.shadedFill(body, col, mul(col, SH_FELT), light, 0.6 * W, 0.4);
    p.poly(body, null, ow);
    const [tx, ty] = R([[cx + s * 10 * u, yb - 0.27 * HH]])[0];
    p.stroke([[tx, ty + 3 * u], [tx + s * 3 * u, ty - 5 * u]], 3.4 * u);
  } else if (o.hat === "kepi" || o.hat === "spike") {
    const kepi = o.hat === "kepi", yb = crown + 0.3 * HH, wb = 0.5 * W, wt = kepi ? 0.42 * W : 0.47 * W, ht = kepi ? 0.42 * HH : 0.36 * HH;
    const col = kepi ? "#c8352e" : "#3a3f3a";
    const top: P2[] = kepi ? [[cx - wt, yb - ht], [cx + wt, yb - ht]]
      : Array.from({ length: 13 }, (_, i) => { const t = Math.PI + (Math.PI * i) / 12; return [cx + wt * Math.cos(t), yb - ht * 0.15 + ht * 0.85 * Math.sin(t)] as P2; });
    const body = R([...sag(yb, wb).reverse(), ...top]);
    p.shadedFill(body, col, mul(col, SH_FELT), light, wt, 0.4);
    if (kepi) p.clip(body, () => p.band(R([[cx - wb - 4 * u, yb - 0.09 * HH], [cx + wb + 4 * u, yb - 0.09 * HH]]), "#2d3f8a", 0.16 * HH, 0.8 * u));
    p.poly(body, null, ow);
    if (!kepi) { // spike, plate
      const [sx0, sy0] = R([[cx, yb - ht]])[0], [sx1, sy1] = R([[cx, yb - ht - 0.3 * HH]])[0];
      p.poly([[sx0 - 6 * u, sy0 + 2 * u], [sx0 + 6 * u, sy0 + 2 * u], [sx1, sy1]], "#c9a24a", 2.4 * u);
      const [bx, by] = R([[cx + 3 * u * (facing || 0), yb - 0.17 * HH]])[0];
      p.ell(bx, by, 9 * u, 8 * u, "#c9a24a", 2 * u, 0, 360, (a * 180) / Math.PI);
    }
    const s = facing || 1, [px, py] = R([[cx + s * 5 * u, yb + 2 * u]])[0];
    p.ell(px, py, 30 * u, 0.05 * HH, "#1d1b22", ow, 0, 180, (a * 180) / Math.PI); // visor
  } else if (o.hat === "bucket") {
    // fisherman's bucket hat: soft crown, band, wide brim that slopes DOWN all round
    const col = o.cap ?? "#9a9466", yb = crown + 0.31 * HH, ht = 0.4 * HH, wb = 0.52 * W, wt = 0.38 * W;
    const top: P2[] = Array.from({ length: 13 }, (_, i) => { const t = Math.PI + (Math.PI * i) / 12; return [cx + wt * Math.cos(t), yb - ht * 0.45 + ht * 0.55 * Math.sin(t)] as P2; });
    const body = R([...sag(yb, wb).reverse(), ...top]);
    p.shadedFill(body, col, mul(col, SH_FELT), light, wt, 0.4);
    p.clip(body, () => p.band(R([[cx - wb - 4 * u, yb - 0.07 * HH], [cx + wb + 4 * u, yb - 0.07 * HH]]), shade(col, 0.72), 0.07 * HH, 0.8 * u));
    p.poly(body, null, ow);
    const bw = 0.72 * W, brimP: P2[] = [];
    for (let i = 0; i <= 24; i++) { const x = -1 + (2 * i) / 24; brimP.push([cx + wb * 0.98 * x, yb - 1 * u + 2 * u * (1 - x * x)]); }
    for (let i = 24; i >= 0; i--) { const x = -1 + (2 * i) / 24; brimP.push([cx + bw * x, yb + 0.1 * HH * (1 - 0.35 * x * x) + 4 * u * x * x]); }
    p.poly(R(brimP), shade(col, 0.9), ow);
    p.stroke(R(Array.from({ length: 13 }, (_, i) => { const x = -1 + i / 6; return [cx + (wb + (bw - wb) * 0.55) * x, yb + 0.06 * HH * (1 - 0.35 * x * x) + 3 * u * x * x] as P2; })), 1.1 * u, shade(col, 0.6)); // brim stitching
  } else if (o.hat === "bonnet") {
    // a lady's day hat of the 1850s: small round crown, a brim tipped forward, a ribbon band and a flower
    const col = "#e8d29a", rib = shade(o.dress ?? o.jacket, 0.9), yb = crown + 0.21 * HH, ht = 0.3 * HH, wt = 0.36 * W, wb = 0.4 * W;
    const top: P2[] = Array.from({ length: 13 }, (_, i) => { const t = Math.PI + (Math.PI * i) / 12; return [cx + wt * Math.cos(t), yb - ht * 0.25 + ht * 0.75 * Math.sin(t)] as P2; });
    const body = R([...sag(yb, wb).reverse(), ...top]);
    p.shadedFill(body, col, mul(col, SH_FELT), light, wt, 0.4);
    p.clip(body, () => p.band(R([[cx - wt - 4 * u, yb - 0.07 * HH], [cx + wt + 4 * u, yb - 0.07 * HH]]), rib, 0.08 * HH, 0.8 * u));
    p.poly(body, null, ow);
    const bw = 0.66 * W, brim: P2[] = [];
    for (let i = 0; i <= 24; i++) { const x = -1 + (2 * i) / 24; brim.push([cx + bw * x, yb + 1 * u - 3 * u * x * x]); }
    for (let i = 24; i >= 0; i--) { const x = -1 + (2 * i) / 24; brim.push([cx + bw * x, yb + 1 * u + 0.07 * HH * (1 - x * x) + 2 * u]); }
    p.poly(R(brim), shade(col, 0.9), ow);
    const fs = side ? 1 : facing || 1, [fx, fy] = R([[cx + fs * 0.24 * W, yb - 0.1 * HH]])[0];
    for (let k = 0; k < 5; k++) { const a2 = (k / 5) * Math.PI * 2; p.ell(fx + Math.cos(a2) * 4.5 * u, fy + Math.sin(a2) * 4.5 * u, 4 * u, 4 * u, "#e8708a", 1.2 * u); }
    p.ell(fx, fy, 3 * u, 3 * u, "#f2c230", 1 * u);
  }
};

// ---------------- bodies ----------------
export type Arms = [P2[], P2[]];
/** held prop; for the hammer the number is the strike 0 (raised) .. 1 (struck) */
export type HoldKind = "frame" | "chainsaw" | "shovel" | "rod" | "camera" | "brush";
export type Prop = null | "icecream" | "teacup" | "glass" | "glassUp" | "loaf" | "clipboard" | "shako" | ["hammer", number] | ["hold", HoldKind, number];

export const BUILD: Record<Build, { a: number; torso: number; legs: number; tw: number }> = {
  // v3 (owner Nov 11: the references' body types): ~2.9 head-heights, big head, a long straight-sided garment
  // with a flat hem, short stick legs below it (was 3.5 HH with long legs)
  adult: { a: 118, torso: 1.35, legs: 0.62, tw: 0.86 },
  stout: { a: 118, torso: 1.4, legs: 0.58, tw: 0.98 },
  kid: { a: 112, torso: 1.0, legs: 0.48, tw: 0.78 },
};

export type FrontOpts = {
  phase?: number; expr?: Expr; mode?: "march" | "stroll" | "stand" | "sit" | "fall"; look?: number; blink?: boolean | number; lift?: number;
  prop?: Prop; tilt?: number; headTilt?: number; wave?: number;
  /** canvas angle the key light comes FROM (painted crescent + thick outline side) */
  light?: number; facing?: -1 | 0 | 1; seed?: number;
};

const footStroke = (p: Pen, a: P2, b: P2, w: number, col: string) => {
  if (col !== INK) p.stroke([a, b], w + 3, INK);
  p.stroke([a, b], w, col);
};

/** both hands for a held prop: [left, right] arm polylines (shoulder, elbow, hand) */
const holdArms = (kind: HoldKind, k: number, sh: (s: number) => P2, tcx: number, ta: number, chin: number, HH: number, u: number): [P2, P2, P2][] => {
  const L = sh(-1), Rr = sh(1);
  const arm = (S: P2, Hd: P2, side: number): [P2, P2, P2] => [S, [(S[0] + Hd[0]) / 2 + side * 10 * u, (S[1] + Hd[1]) / 2 + 0.12 * HH], Hd];
  if (kind === "frame") { const y = chin + 0.42 * HH; return [arm(L, [tcx - 1.28 * ta, y], -1), arm(Rr, [tcx + 1.28 * ta, y], 1)]; }
  if (kind === "chainsaw") { const j = 1.5 * u * Math.sin(k * 40); return [arm(L, [tcx + 0.2 * ta, chin + 0.62 * HH + j], -1), arm(Rr, [tcx + 0.95 * ta, chin + 0.86 * HH + j], 1)]; }
  if (kind === "shovel") { const d = 0.1 * HH * Math.sin(k * Math.PI * 2); return [arm(L, [tcx - 0.15 * ta, chin + 0.6 * HH + d], -1), arm(Rr, [tcx + 0.45 * ta, chin + 1.1 * HH + d], 1)]; }
  if (kind === "rod") return [arm(L, [tcx + 0.2 * ta, chin + 0.72 * HH], -1), arm(Rr, [tcx + 0.7 * ta, chin + 0.62 * HH], 1)];
  if (kind === "camera") return [arm(L, [tcx - 0.4 * ta, chin + 0.45 * HH], -1), arm(Rr, [tcx + 0.4 * ta, chin + 0.45 * HH], 1)];
  // brush: left hangs, right paints up-right
  const S = sh(1), a = Math.sin(k * Math.PI * 2);
  return [[sh(-1), [tcx - 1.1 * ta, sh(-1)[1] + 0.48 * HH], [tcx - 1.15 * ta, chin + 1.0 * HH]], [S, [tcx + 1.2 * ta + 8 * u, S[1] + 0.2 * HH], [tcx + 1.4 * ta + 18 * u + 6 * u * a, S[1] - 0.1 * HH - 8 * u * a]]];
};
const GOLD = "#d9a83a";
const drawHold = (p: Pen, kind: HoldKind, k: number, tcx: number, ta: number, chin: number, HH: number, u: number, hands: P2[]) => {
  if (kind === "frame") {
    const cx = tcx, cy = chin + 0.42 * HH, fw = 1.28 * ta, fh = 0.62 * HH, b = 10 * u;
    const outer: P2[] = [[cx - fw, cy - fh], [cx + fw, cy - fh], [cx + fw, cy + fh], [cx - fw, cy + fh]];
    const inner: P2[] = [[cx - fw + b, cy - fh + b], [cx - fw + b, cy + fh - b], [cx + fw - b, cy + fh - b], [cx + fw - b, cy - fh + b]];
    const g = p.g; g.beginPath(); p.path(outer, true); const g2 = g; // even-odd ring
    inner.forEach(([x, y], i) => { if (i) g2.lineTo(x, y); else g2.moveTo(x, y); }); g2.closePath();
    g.fillStyle = GOLD; g.fill("evenodd"); g.lineWidth = 2.2 * u; g.strokeStyle = INK; g.stroke();
    p.poly([[cx - fw + b * 0.45, cy - fh + b * 0.45], [cx + fw - b * 0.45, cy - fh + b * 0.45], [cx + fw - b * 0.45, cy + fh - b * 0.45], [cx - fw + b * 0.45, cy + fh - b * 0.45]], null, 1.2 * u);
    return;
  }
  const [hl, hr] = hands;
  if (kind === "chainsaw") {
    // classic saw: orange motor block, black top-handle loop, long grey guide bar with a toothed chain ring
    const j = 1.5 * u * Math.sin(k * 40), x0 = hr[0] - 8 * u, y0 = hr[1] - 16 * u + j, BL = 112 * u;
    const bar: P2[] = [[x0 + 30 * u, y0 + 2 * u], [x0 + BL, y0 + 4 * u], [x0 + BL + 9 * u, y0 + 11 * u], [x0 + BL, y0 + 18 * u], [x0 + 30 * u, y0 + 20 * u]];
    // chain teeth (small triangles on the top and bottom edges)
    const off = (Math.round(k * 24) % 2) * 3 * u;
    for (let x = x0 + 34 * u + off; x < x0 + BL - 2 * u; x += 7 * u) {
      p.poly([[x, y0 + 2.5 * u], [x + 3.5 * u, y0 - 2.5 * u], [x + 6 * u, y0 + 2.8 * u]], "#3a3440", 0.9 * u);
      p.poly([[x, y0 + 19.6 * u], [x + 3.5 * u, y0 + 24.5 * u], [x + 6 * u, y0 + 19.4 * u]], "#3a3440", 0.9 * u);
    }
    p.poly(bar, "#cfd3d9", 2.2 * u);
    p.stroke([[x0 + 36 * u, y0 + 11 * u], [x0 + BL - 4 * u, y0 + 11.5 * u]], 1.3 * u, "#8d939b");
    // motor body with a darker side panel and a pull-cord grip
    const body: P2[] = [[x0 - 26 * u, y0 - 10 * u], [x0 + 24 * u, y0 - 12 * u], [x0 + 34 * u, y0 - 2 * u], [x0 + 34 * u, y0 + 24 * u], [x0 - 26 * u, y0 + 26 * u]];
    p.poly(body, "#ef7a25", 2.4 * u);
    p.poly([[x0 - 18 * u, y0 + 2 * u], [x0 + 18 * u, y0 + 1 * u], [x0 + 18 * u, y0 + 16 * u], [x0 - 18 * u, y0 + 17 * u]], "#2b2830", 1.4 * u);
    p.band([[x0 - 34 * u, y0 + 10 * u], [x0 - 26 * u, y0 + 10 * u]], "#2b2830", 6 * u, 1 * u, "round");
    // top handle loop (black)
    p.arc(x0 + 2 * u, y0 - 10 * u, 20 * u, 15 * u, 180, 360, 6 * u, "#2b2830");
    p.arc(x0 + 2 * u, y0 - 10 * u, 23 * u, 18 * u, 180, 360, 1.4 * u);
    return;
  }
  if (kind === "shovel") {
    // long ash handle with a D-grip at the top and a broad pointed steel spade at the bottom (clipped at the ground line)
    p.g.save(); p.g.beginPath(); p.g.rect(-2000, -2000, 5000, chin + 2.5 * HH + 2000); p.g.clip();
    const a = hl, b = hr, dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L;
    const nx = -uy, ny = ux, top: P2 = [a[0] - ux * 26 * u, a[1] - uy * 26 * u], bot: P2 = [b[0] + ux * 104 * u, b[1] + uy * 104 * u];
    p.band([top, bot], "#a8743f", 4.2 * u, 1.3 * u, "round");
    const gc: P2 = [top[0] - ux * 9 * u, top[1] - uy * 9 * u];
    p.poly([[top[0] + nx * 10 * u, top[1] + ny * 10 * u], [gc[0] + nx * 11 * u - ux * 9 * u, gc[1] + ny * 11 * u - uy * 9 * u], [gc[0] - nx * 11 * u - ux * 9 * u, gc[1] - ny * 11 * u - uy * 9 * u], [top[0] - nx * 10 * u, top[1] - ny * 10 * u]], null, 3.2 * u);
    const P = (s: number, t: number): P2 => [bot[0] + nx * s * u + ux * t * u, bot[1] + ny * s * u + uy * t * u];
    p.poly([P(-6, -4), P(6, -4), P(7, 4), P(-7, 4)], "#6d737b", 1.5 * u); // socket
    p.poly([P(-17, 2), P(17, 2), P(18, 26), P(10, 40), P(0, 48), P(-10, 40), P(-18, 26)], "#a9b0b8", 2.2 * u);
    p.stroke([P(0, 8), P(0, 36)], 1.2 * u, "#7d848c");
    p.g.restore();
    // the blade digs into a soil heap at his feet (rule 29: tools touch what they work on); soil rides up on the blade
    const lift = Math.sin(k * Math.PI * 2); // +1 = lowest (blade in the heap)
    const tip = P(0, 48), sole = chin + 2.5 * HH, hx = tip[0] - lift * 0.06 * HH * ux, hw = 34 * u, hh = 18 * u;
    if (lift < -0.2) p.ell(P(0, 30)[0], P(0, 30)[1] - 6 * u, 15 * u, 9 * u, "#7a5232", 1.6 * u);
    const heap: P2[] = [];
    for (let i = 0; i <= 16; i++) { const t2 = Math.PI * (i / 16); heap.push([hx - hw * Math.cos(t2), sole - hh * Math.sin(t2) * (1 - 0.15 * Math.cos(3 * t2))]); }
    p.poly(heap, "#8a6038", 2.2 * u);
    for (const [dx, dy] of [[-0.4, 0.35], [0.1, 0.55], [0.45, 0.3]] as const) p.dot(hx + dx * hw, sole - dy * hh, 2.4 * u, "#6a4528");
    return;
  }
  if (kind === "rod") {
    // steep rod that stays inside the 600-wide card, big reel at the grip, slack line down to a float lying on the dry ground
    const tip: P2 = [Math.min(585, hr[0] + 80 * u), hr[1] - 230 * u + 8 * u * k], mid: P2 = [hr[0] + 46 * u, hr[1] - 120 * u];
    p.band([[hl[0] - 8 * u, hl[1] + 16 * u], [hr[0] + 6 * u, hr[1] - 8 * u]], "#2e2420", 7 * u, 1.4 * u, "round"); // grip
    p.stroke(curve([hr[0], hr[1]], mid, tip), 6.5 * u, INK);
    p.stroke(curve([hr[0], hr[1]], mid, tip), 3.6 * u, "#c4823a");
    for (const f of [0.35, 0.6, 0.82]) { const q = curve([hr[0], hr[1]], mid, tip)[Math.round(f * (curve([hr[0], hr[1]], mid, tip).length - 1))]; p.ell(q[0], q[1], 3 * u, 3 * u, "#c9ccd2", 1.2 * u); } // line guides
    const rx = hl[0] + 6 * u, ry = hl[1] + 12 * u;
    p.ell(rx, ry, 15 * u, 15 * u, "#c9ccd2", 2.2 * u); p.ell(rx, ry, 8 * u, 8 * u, "#8d939b", 1.4 * u); p.dot(rx, ry, 2.6 * u);
    p.stroke([[rx, ry], [rx - 14 * u, ry + 10 * u]], 2.2 * u); p.dot(rx - 14 * u, ry + 10 * u, 3.4 * u); // reel handle
    const fy = 958, fx = Math.min(560, tip[0] - 20 * u);
    const sagPt: P2 = [tip[0] + 6 * u, (tip[1] + fy) / 2];
    p.stroke(curve(tip, sagPt, [fx + 8 * u, fy - 4 * u]), 1.2 * u, "#4a4550");
    // float lying on its side on the sand
    p.ell(fx, fy, 13 * u, 8 * u, "#f4f2ec", 1.8 * u);
    p.clip([[fx - 15 * u, fy - 10 * u], [fx, fy - 10 * u], [fx, fy + 10 * u], [fx - 15 * u, fy + 10 * u]], () => p.ell(fx, fy, 13 * u, 8 * u, "#d8392f", 0));
    p.ell(fx, fy, 13 * u, 8 * u, null, 1.8 * u);
    return;
  }
  if (kind === "camera") {
    const cx = (hl[0] + hr[0]) / 2, cy = hl[1] - 6 * u;
    p.poly([[cx - 26 * u, cy - 15 * u], [cx + 26 * u, cy - 15 * u], [cx + 26 * u, cy + 15 * u], [cx - 26 * u, cy + 15 * u]], "#3a3d47", 2 * u);
    p.poly([[cx - 20 * u, cy - 15 * u], [cx - 8 * u, cy - 15 * u], [cx - 8 * u, cy - 21 * u], [cx - 20 * u, cy - 21 * u]], "#3a3d47", 1.6 * u);
    p.ell(cx + 2 * u, cy, 11 * u, 11 * u, "#9cc4e0", 2.2 * u); p.ell(cx + 2 * u, cy, 5 * u, 5 * u, "#2b2830", 0);
    return;
  }
  // paintbrush: wooden handle, silver ferrule, cream bristles dipped in white paint
  const h = hr, ang = Math.atan2(-30, 22), cs = Math.cos(ang), sn = Math.sin(ang);
  const Q = (t: number, s: number): P2 => [h[0] + cs * t * u - sn * s * u, h[1] + sn * t * u + cs * s * u];
  p.band([Q(-14, 0), Q(26, 0)], "#b0402f", 4.5 * u, 1.2 * u, "round");
  p.poly([Q(24, -5), Q(36, -6), Q(36, 6), Q(24, 5)], "#c9ccd2", 1.5 * u);
  p.poly([Q(36, -7), Q(52, -6), Q(58, 0), Q(52, 6), Q(36, 7)], "#e8d6a8", 1.6 * u);
  p.poly([Q(47, -6), Q(53, -5), Q(58, 0), Q(53, 5), Q(47, 6)], "#ffffff", 1.2 * u);
};

/** v6 (edge density + reference costume detail): lapels, a placket seam, a darker hem band with stitches, pocket flaps,
 *  and per-person cloth patterns (pinstripe / check / plain), all drawn inside the torso clip */
const garment = (p: Pen, tcx: number, chin: number, bot: number, Ta: number, HH: number, u: number, col: string, seed: number, facing: number, dress: boolean) => {
  const dk = shade(col, 0.62), lt = shade(col, 1.18), top = chin - 0.25 * HH;
  const pat = seed % 3;
  // v8: on dark cloth the weave is drawn lighter than the cloth, otherwise it vanishes (black coats read as flat blobs)
  const hx = col.replace("#", ""), lum = hx.length >= 6 ? (0.3 * parseInt(hx.slice(0, 2), 16) + 0.59 * parseInt(hx.slice(2, 4), 16) + 0.11 * parseInt(hx.slice(4, 6), 16)) / 255 : 0.5;
  const pc = lum < 0.28 ? shade(col, 1.9) : dk;
  p.g.save(); p.g.globalAlpha = lum < 0.28 ? 0.5 : 0.55;
  if (pat === 0) for (let x = tcx - Ta * 1.6; x < tcx + Ta * 1.2; x += 11 * u) { p.stroke([[x, top], [x + 0.6 * (bot - top), bot]], 1.1 * u, pc); }
  if (pat === 1) for (let x = tcx - Ta * 1.1; x < tcx + Ta * 1.1; x += 9 * u) p.stroke([[x, top], [x, bot]], 1.3 * u, pc);
  if (pat === 2) { for (let x = tcx - Ta * 1.1; x < tcx + Ta * 1.1; x += 14 * u) p.stroke([[x, top], [x, bot]], 1.6 * u, pc); for (let y = top; y < bot; y += 14 * u) p.stroke([[tcx - Ta * 1.2, y], [tcx + Ta * 1.2, y]], 1.6 * u, pc); }
  p.g.restore();
  // hem band + stitches
  const hb = 0.13 * HH;
  p.poly([[tcx - Ta * 1.3, bot - hb], [tcx + Ta * 1.3, bot - hb], [tcx + Ta * 1.3, bot + 20 * u], [tcx - Ta * 1.3, bot + 20 * u]], dk, 0);
  p.stroke([[tcx - Ta * 1.3, bot - hb], [tcx + Ta * 1.3, bot - hb]], 2.2 * u);
  for (let x = tcx - Ta * 1.2; x < tcx + Ta * 1.2; x += 7 * u) p.stroke([[x, bot - hb * 0.5], [x + 3.5 * u, bot - hb * 0.5]], 1.2 * u, lt);
  if (dress) return;
  // lapels (a V from the shoulders to mid chest) + placket seam
  const vx = tcx + 2 * u * facing, vy = chin + 0.42 * HH;
  p.poly([[vx - 0.62 * Ta, chin - 0.02 * HH], [vx, vy], [vx - 0.18 * Ta, chin - 0.02 * HH]], lt, 1.8 * u);
  p.poly([[vx + 0.62 * Ta, chin - 0.02 * HH], [vx, vy], [vx + 0.18 * Ta, chin - 0.02 * HH]], lt, 1.8 * u);
  p.stroke([[vx - 4 * u, vy], [vx - 4 * u, bot - hb]], 1.8 * u);
  // pocket flaps
  for (const sd of [-1, 1]) { const px = tcx + sd * 0.5 * Ta, py = bot - 0.42 * HH; p.poly([[px - 0.22 * Ta, py], [px + 0.22 * Ta, py], [px + 0.2 * Ta, py + 0.07 * HH], [px - 0.2 * Ta, py + 0.07 * HH]], dk, 1.6 * u); }
};

export const bodyFront = (p: Pen, o: Outfit, opts: FrontOpts) => {
  const { phase = 0, expr = "neutral", mode = "march", look = 0, blink = false, lift = 60, prop = null, tilt = 0, headTilt = 0, wave,
    light = DEF_LIGHT, facing = 0, seed = 1 } = opts;
  const Bd = BUILD[o.build ?? "adult"], skin = o.skin ?? SKIN, two = Math.PI * 2, lid = lidOf(blink);
  const H = headBlob(seed, Bd.a, facing), W = 2 * H.a, HH = 2 * H.b, u = W / 100;
  const tall = (1 + Bd.torso + Bd.legs) * HH, sole = 975;
  // body bob 5 % (march) / 3 % (stroll) of the height, lowest at contact (phase 0 and 0.5)
  const bob = mode === "march" ? 0.025 * tall * Math.cos(2 * two * phase) : mode === "stroll" ? 0.015 * tall * Math.cos(2 * two * phase) : 0;
  // sit: placed at FLOOR level; hips at chair-seat height, thighs toward the viewer, shins down to feet on the floor
  const torsoBot = mode === "sit" ? sole - 0.98 * HH : sole - Bd.legs * HH + bob; // seat height stays at real chair height
  const chin = torsoBot - Bd.torso * HH, hc = chin - H.b, crown = hc - H.b, hipY = torsoBot - 0.12 * HH;
  const thick = thickAngle(light), ow = 2.9 * u; // v3: reference character outline ~6-8 px at 1080
  const legCol = mix(o.pants, INK, 0.55), armCol = mix(o.jacket, INK, 0.5), footCol = o.boots;
  const legW = 5.8 * u, footW = 7.5 * u;
  // ---- legs + feet (not rotated) ----
  p.rot = null;
  if (mode === "sit") {
    for (const side of [-1, 1]) {
      const k: P2 = [300 + side * 17 * u, torsoBot + 0.06 * HH], f: P2 = [300 + side * 19 * u, sole - 6 * u];
      p.stroke([k, f], legW, legCol);
      p.dot(k[0], k[1], legW * 0.75, legCol); // knee pointing at the viewer
      footStroke(p, [f[0] - side * 4 * u, f[1] + 2 * u], [f[0] + side * 8 * u, f[1] + 4 * u], footW * 1.15, footCol);
    }
  } else if (mode === "fall") {
    const legs: [P2, P2, P2][] = [
      [[300 - 15 * u, hipY], [300 - 46 * u, hipY + 0.5 * HH], [300 - 70 * u, hipY + 0.72 * HH]],
      [[300 + 15 * u, hipY], [300 + 50 * u, hipY + 0.45 * HH], [300 + 76 * u, hipY + 0.22 * HH]],
    ];
    legs.forEach(([h, k, f], i) => {
      p.stroke(curve(h, k, f), legW, legCol);
      footStroke(p, f, [f[0] + (i ? 14 : -14) * u, f[1] + (i ? -6 : 4) * u], footW, footCol);
    });
  } else if (o.dress) {
    for (const side of [-1, 1]) {
      const fx = 300 + side * 12 * u, fy = sole - 4 * u;
      p.stroke([[fx, sole - 0.4 * HH], [fx + side * u, fy]], legW, legCol);
      footStroke(p, [fx - side * 3 * u, fy], [fx + side * 12 * u, fy + u], footW, footCol);
    }
  } else {
    const L = mode === "march" ? lift * 1.25 : mode === "stroll" ? lift * 0.55 : 0;
    for (const [side, ph] of [[-1, 0], [1, 0.5]] as const) {
      const up = Math.max(0, Math.sin(two * (phase + ph))) * L;
      const hx = 300 + side * 15 * u, fx = 300 + side * 22 * u, fy = sole - 4 * u - up;
      const k: P2 = [(hx + fx) / 2 + side * (1.5 * u + up * 0.16), (hipY + fy) / 2 - up * 0.08];
      p.stroke(curve([hx, hipY], k, [fx, fy]), legW, legCol);
      footStroke(p, [fx - side * 3 * u, fy], [fx + side * 13 * u, fy + 0.5 * u], footW, footCol);
    }
  }
  // ---- upper body: rotates about the hips (tilt + a small weight-shift sway on every step) ----
  const sway = mode === "march" ? 1.6 * Math.sin(two * phase) : mode === "stroll" ? 1.0 * Math.sin(two * phase) : 0;
  const A = tilt + sway;
  p.rot = A ? [rad(A), 300, hipY] : null;
  const dress = !!o.dress && mode !== "sit" && mode !== "fall";
  const T: Blob = { a: ((Bd.tw / 2) * W) / 1.06, b: 0.5 * (torsoBot - (chin - 0.25 * HH)), nTop: 2.6, nBot: 4.4, egg: o.build === "stout" ? 0.17 : 0.12,
    asym: 0.04 * facing, rot: 0, noise: 0.006, seed: seed + 7 };
  const tcx = 300 + 3 * u * facing, tcy = torsoBot - T.b, tp = blobPts(tcx, tcy, T);
  const sh = (side: number): P2 => [tcx + side * 0.85 * T.a, chin + 0.12 * HH];
  const hang = (side: number, fwd: number): [P2, P2, P2] => {
    const S = sh(side), ex = tcx + side * (1.12 * T.a + 4 * u);
    const hx = ex + side * 3 * u - side * 6 * u * Math.max(0, fwd) + side * 4 * u * Math.max(0, -fwd);
    return [S, [ex, S[1] + 0.48 * HH], [hx, chin + 1.04 * HH - Math.abs(fwd) * 9 * u]];
  };
  const sw = mode === "march" || mode === "stroll" ? Math.sin(two * phase) : 0;
  // rifle at the order: butt by the right hip, held by the hanging right hand, muzzle past the crown
  const R0: P2 = [300 + 47 * u, torsoBot + 0.12 * HH], R1: P2 = [300 + 64 * u, crown - 0.32 * HH];
  const rifle = !!o.rifle && (mode === "march" || mode === "stand" || mode === "stroll");
  type Arm = { pts: [P2, P2, P2]; front: boolean };
  const arms: Arm[] = [];
  if (mode === "sit") for (const side of [-1, 1]) {
    if (side > 0 && (prop === "teacup" || prop === "glass" || prop === "loaf" || prop === "clipboard")) { const S = sh(1); arms.push({ pts: [S, [tcx + 1.05 * T.a + 4 * u, S[1] + 0.45 * HH], [tcx + 0.5 * T.a, S[1] + 0.4 * HH]], front: true }); continue; }
    arms.push({ pts: [sh(side), [tcx + side * (1.05 * T.a + 4 * u), sh(side)[1] + 0.45 * HH], [tcx + side * 0.62 * T.a, torsoBot - 0.02 * HH]], front: true }); // hands on the knees
  }
  else if (mode === "fall") for (const side of [-1, 1]) arms.push({ pts: [sh(side), [tcx + side * (1.15 * T.a + 12 * u), sh(side)[1] - 0.25 * HH], [tcx + side * (1.3 * T.a + 24 * u), sh(side)[1] - 0.68 * HH]], front: false });
  else {
    arms.push({ pts: prop === "shako" ? hang(-1, 0) : hang(-1, -sw), front: false });
    if (rifle) {
      const G = lerp2(R0, R1, 0.1);
      arms.push({ pts: [sh(1), [tcx + 1.12 * T.a + 5 * u, sh(1)[1] + 0.45 * HH], G], front: false });
    } else if (wave !== undefined) {
      const S = sh(1);
      arms.push({ pts: [S, [tcx + 1.1 * T.a + 10 * u + 3 * u * wave, S[1] - 0.22 * HH], [tcx + 1.18 * T.a + 16 * u + 12 * u * wave, S[1] - 0.6 * HH]], front: false });
    } else if (prop === "clipboard") { // rule 49: held low at the waist, the board's top stays below the chin
      const S = sh(1);
      arms.push({ pts: [S, [tcx + 1.1 * T.a + 4 * u, S[1] + 0.4 * HH], [tcx + 0.45 * T.a, S[1] + 0.66 * HH]], front: true }); // v5: chest height, out of the caption band
    } else if (prop === "glassUp") { // held up and out to the side, showing it: the glass stays clear of the face (owner Nov 11)
      const S = sh(1);
      arms.push({ pts: [S, [tcx + 1.3 * T.a + 16 * u, S[1] + 0.22 * HH], [tcx + 1.5 * T.a + 26 * u, S[1] - 0.08 * HH]], front: true });
    } else if (prop === "icecream" || prop === "teacup" || prop === "glass" || prop === "loaf") {
      const S = sh(1);
      arms.push({ pts: [S, [tcx + 1.05 * T.a + 4 * u, S[1] + 0.45 * HH], [tcx + 0.5 * T.a, S[1] + 0.4 * HH]], front: true });
    } else if (Array.isArray(prop) && prop[0] === "hold") {
      holdArms(prop[1], prop[2], sh, tcx, T.a, chin, HH, u).forEach((pts) => arms.push({ pts, front: true }));
      arms.shift();
    } else if (Array.isArray(prop)) {
      const S = sh(1), k = clamp(prop[1] as number, 0, 1);
      const E = lerp2([tcx + 1.1 * T.a + 10 * u, S[1] - 0.15 * HH], [tcx + 1.2 * T.a + 10 * u, S[1] + 0.3 * HH], k);
      const Hd = lerp2([tcx + 1.15 * T.a + 14 * u, S[1] - 0.55 * HH], [tcx + 1.45 * T.a + 22 * u, S[1] + 0.35 * HH], k);
      arms.push({ pts: [S, E, Hd], front: true });
    } else arms.push({ pts: hang(1, sw), front: false });
  }
  const drawArm = (a: Arm) => { p.stroke(curve(a.pts[0], a.pts[1], a.pts[2]), 5.2 * u, armCol); p.dot(a.pts[2][0], a.pts[2][1], 5.5 * u); };
  // behind the body: rifle, sword, arms
  if (rifle) {
    p.band([R0, R1], "#7a4b2a", 5 * u, 1.5 * u, "round");
    p.band([lerp2(R0, R1, 0.6), R1], "#8d949c", 2.4 * u, 1.2 * u, "round");
  }
  if (o.sword && mode !== "sit") {
    const s0: P2 = [tcx - 0.75 * T.a, torsoBot - 0.2 * HH];
    p.band([s0, [s0[0] - Math.sin(rad(25)) * 0.8 * HH, s0[1] + Math.cos(rad(25)) * 0.8 * HH]], "#c9ccd2", 3 * u, 1.2 * u, "round");
  }
  for (const a of arms) if (!a.front) drawArm(a);
  // torso / dress: shaded fill -> clothing clipped to it -> thick-thin ink ring
  if (dress) {
    const D: Blob = { a: 0.5 * W * 0.98, b: 0.5 * ((sole - 0.35 * HH) - (chin - 0.2 * HH)), nTop: 2.0, nBot: 3.0, egg: 0.35, asym: 0.03 * facing, rot: 0, noise: 0.006, seed: seed + 9 };
    const dp = blobPts(300, sole - 0.35 * HH - D.b, D);
    p.gradFill(dp, o.dress!, mul(o.dress!, SH_CLOTH), light);
    p.inkRing(dp, ow, thick);
    const Sw: Blob = { a: 0.37 * W, b: 0.3 * HH, nTop: 2.2, nBot: 2.4, egg: 0.1, asym: 0, rot: 0, noise: 0.006, seed: seed + 8 };
    const sp = blobPts(300, chin + 0.12 * HH, Sw);
    p.gradFill(sp, o.jacket, mul(o.jacket, SH_CLOTH), light);
    p.inkRing(sp, ow * 0.9, thick);
  } else {
    p.gradFill(tp, o.jacket, mul(o.jacket, SH_CLOTH), light);
    p.clip(tp, () => {
      garment(p, tcx, chin, torsoBot, T.a, HH, u, o.jacket, seed, facing, dress);
      if (o.belt) {
        for (const s of [-1, 1]) p.band([[tcx - s * 0.75 * T.a, chin - 0.05 * HH], [tcx + s * 0.8 * T.a, torsoBot - 0.1 * HH]], o.belt!, 5.5 * u, 1.8 * u);
        const xc = tcx + 0.025 * T.a, yc = chin - 0.05 * HH + (torsoBot - 0.1 * HH - (chin - 0.05 * HH)) * (0.75 / 1.55);
        p.poly([[xc - 3.5 * u, yc - 3.5 * u], [xc + 3.5 * u, yc - 3.5 * u], [xc + 3.5 * u, yc + 3.5 * u], [xc - 3.5 * u, yc + 3.5 * u]], "#d9dde0", 1.5 * u);
      }
      if (o.sash) p.band([[tcx - 1.3 * T.a, torsoBot - 0.32 * HH], [tcx + 1.3 * T.a, torsoBot - 0.32 * HH]], o.sash, 0.13 * HH, 1.8 * u);
      for (let i = 0; i < 4; i++) {
        const y = chin + 0.12 * HH + i * 0.2 * HH;
        if (o.sash && Math.abs(y - (torsoBot - 0.32 * HH)) < 0.08 * HH) continue;
        p.dot(tcx + 2 * u * facing, y, 2.2 * u + 0.8 * u, INK); p.dot(tcx + 2 * u * facing, y, 2.2 * u, o.buttons ?? shade(o.jacket, 0.7));
      }
    });
    if (o.sash) { const s = facing || 1; p.poly([[tcx + s * 0.55 * T.a, torsoBot - 0.3 * HH], [tcx + s * 0.75 * T.a, torsoBot + 0.05 * HH], [tcx + s * 0.45 * T.a, torsoBot + 0.02 * HH]], o.sash, 1.6 * u); }
    p.inkRing(tp, ow, thick);
  }
  // seated: the lap (thighs coming toward the viewer) in front of the torso bottom, knees as two rounded ends
  if (mode === "sit") {
    p.rot = null;
    const ly0 = torsoBot - 0.1 * HH, ly1 = torsoBot + 0.1 * HH, lx = 0.95 * T.a + 2 * u, pc = o.pants;
    for (const side of [-1, 1]) {
      const cx2 = 300 + side * lx * 0.5;
      const th: P2[] = [];
      for (let i = 0; i <= 16; i++) { const a2 = (i / 16) * Math.PI * 2; th.push([cx2 + Math.cos(a2) * lx * 0.52, (ly0 + ly1) / 2 + Math.sin(a2) * (ly1 - ly0) * 0.55]); }
      p.shadedFill(th, pc, mul(pc, SH_CLOTH), light, lx * 0.5);
      p.poly(th, null, 3.6 * u);
    }
    if (o.dress) { // rule 68: a seated lady keeps her skirt: it drapes over the lap and falls to mid-shin
      const sk: P2[] = [[300 - lx * 1.02, ly0 - 0.04 * HH], [300 + lx * 1.02, ly0 - 0.04 * HH], [300 + lx * 1.12, torsoBot + 0.5 * HH], [300 - lx * 1.12, torsoBot + 0.5 * HH]];
      p.shadedFill(sk, o.dress, mul(o.dress, SH_CLOTH), light, lx);
      p.poly(sk, null, 3.6 * u);
      p.stroke([[300, ly0 + 0.04 * HH], [300, torsoBot + 0.46 * HH]], 1.8 * u, mul(o.dress, SH_CLOTH));
    }
    p.rot = A ? [rad(A), 300, hipY] : null;
  }
  // ---- head: rotates with the body, plus its own tilt about the chin ----
  const Ah = A + headTilt, [cpx, cpy] = rotAbout([300, chin], rad(A), [300, hipY]);
  p.rot = Ah ? [rad(Ah), 300, chin, cpx - 300, cpy - chin] : null;
  hatBehind(p, o, H, 300, hc, light, thick, ow, false);
  const hp = blobPts(300, hc, H);
  p.shadedFill(hp, skin, mul(skin, SH_SKIN), light, H.a);
  p.inkRing(hp, ow, thick);
  // hats go on AFTER the face so brows/lashes sit under the brim (owner fix r3); hair stays under the face
  const brim = !!o.hat; // brows sit low, between the eyes and the hairline/hat (never on the hair)
  if (!brim) hatOn(p, o, hp, H, 300, hc, light, seed, facing, false);
  faceFront(p, 300, hc, W, expr, facing, look, lid, brim, skin, o.moustache, o.build === "stout");
  if (o.beard) { // full beard over the chin and mouth (Eiffel): a rounded shape hanging from the cheeks
    const u = W / 100, fx = 300 + 7 * u * facing, cy = hc;
    const bd: P2[] = [];
    for (let i = 0; i <= 20; i++) { const t = (i / 20) * Math.PI; bd.push([fx - 34 * u * Math.cos(t), cy + 10 * u + 42 * u * Math.sin(t) * (0.8 + 0.2 * Math.sin(t))]); }
    bd.push([fx + 30 * u, cy + 6 * u], [fx + 10 * u, cy + 14 * u], [fx - 10 * u, cy + 14 * u], [fx - 30 * u, cy + 6 * u]);
    p.shadedFill(bd, o.beard, mul(o.beard, SH_FELT), light, 30 * u, 0.35); p.poly(bd, null, 3.2 * u);
    p.ell(fx, cy + 18 * u, 9 * u, 4.5 * u, "#7a3b3b", 2.4 * u); // mouth peeking through
  }
  if (brim) hatOn(p, o, hp, H, 300, hc, light, seed, facing, false);
  if (o.phones) { // radio headphones over the hat/head: band + two ear cups
    const u = W / 100;
    p.arc(300, hc - 4 * u, 0.56 * W, 0.62 * HH, 195, 345, 5 * u, "#2b2830");
    for (const s2 of [-1, 1]) p.ell(300 + s2 * 0.53 * W, hc + 2 * u, 9 * u, 15 * u, "#2b2830", 2.5 * u);
  }
  // rule 66 (owner Nov 12): held props and the hands holding them are the TOP layer, drawn after the head, so a cup or
  // glass raised near the chin overlaps the face instead of hiding behind it
  p.rot = A ? [rad(A), 300, hipY] : null;
  // in front of the body: hands holding props
  if (Array.isArray(prop) && prop[0] === "hold") drawHold(p, prop[1], prop[2], tcx, T.a, chin, HH, u, arms.map((a) => a.pts[2]));
  for (const a of arms) if (a.front) {
    drawArm(a);
    const [hx, hy] = a.pts[2];
    if (prop === "teacup") { // china cup on a saucer, held at the chest
      p.ell(hx + 2 * u, hy - 4 * u, 17 * u, 4.5 * u, "#f4f2ec", 2 * u);
      // v8 (rule 58): the handle is drawn first and both ends run INTO the cup wall, so the cup body overlaps them: never a
      // floating C beside the cup. Wall runs (14,-26) -> (11,-8); the handle leaves it at y -23 and rejoins at y -12.
      const hw = (y: number) => 14 - (3 * (y + 26)) / 18;
      const H: P2[] = [[hw(-23) - 2, -23], [18, -24.5], [21.5, -21], [21.5, -15.5], [18, -12], [hw(-12) - 2, -12]].map(([x, y]) => [hx + x * u, hy + y * u] as P2);
      p.stroke(H, 6.2 * u); p.stroke(H, 2.6 * u, "#f4f2ec");
      p.poly([[hx - 10 * u, hy - 26 * u], [hx + 14 * u, hy - 26 * u], [hx + 11 * u, hy - 8 * u], [hx - 7 * u, hy - 8 * u]], "#f4f2ec", 2 * u);
      p.ell(hx + 2 * u, hy - 26 * u, 12 * u, 3 * u, "#a8743f", 1.6 * u);
      p.stroke([[hx - 6 * u, hy - 18 * u], [hx + 8 * u, hy - 18 * u]], 2.2 * u, "#3f6fb5");
      p.dot(hx, hy, 5.5 * u);
    } else if (prop === "glass" || prop === "glassUp") { // a tall glass of murky lake water with grinning germs, gripped round its base
      const G: P2[] = [[hx - 15 * u, hy - 58 * u], [hx + 15 * u, hy - 58 * u], [hx + 12 * u, hy + 6 * u], [hx - 12 * u, hy + 6 * u]];
      p.poly(G, "#e8f3f6", 2.4 * u);
      p.poly([[hx - 14 * u, hy - 44 * u], [hx + 14 * u, hy - 44 * u], [hx + 12 * u, hy + 5 * u], [hx - 12 * u, hy + 5 * u]], "#8f9a4a", 0);
      for (const [dx, dy, r] of [[-5, -32, 5], [5, -18, 5.5], [-4, -6, 4.5]] as const) { p.ell(hx + dx * u, hy + dy * u, r * u, r * u, "#6fbf4a", 1.2 * u); p.dot(hx + (dx - 1.6) * u, hy + (dy - 1) * u, 0.9 * u); p.dot(hx + (dx + 1.6) * u, hy + (dy - 1) * u, 0.9 * u); }
      p.poly(G, null, 2.4 * u);
      p.dot(hx - 10 * u, hy - 2 * u, 5.5 * u); p.dot(hx - 6 * u, hy - 10 * u, 5.5 * u);
    } else if (prop === "loaf") { // a long loaf held in the hand, resting on the forearm
      p.poly([[hx - 40 * u, hy + 2 * u], [hx + 30 * u, hy + 2 * u], [hx + 34 * u, hy - 8 * u], [hx + 22 * u, hy - 20 * u], [hx - 5 * u, hy - 24 * u], [hx - 32 * u, hy - 20 * u], [hx - 44 * u, hy - 8 * u]], "#d9963f", 2.2 * u);
      for (const x of [-24, -4, 16]) p.stroke([[hx + (x - 5) * u, hy - 16 * u], [hx + (x + 5) * u, hy - 7 * u]], 2 * u, "#f2c98a");
      p.dot(hx, hy, 5.5 * u);
    } else if (prop === "clipboard") { // a clipboard with a written page (lines of notes + a little sketch of a raised house)
      const x0 = hx - 30 * u, y0 = hy - 70 * u, x1 = hx + 18 * u, y1 = hy + 4 * u;
      p.poly([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], "#a8743f", 2.2 * u);
      p.poly([[x0 + 4 * u, y0 + 6 * u], [x1 - 4 * u, y0 + 6 * u], [x1 - 4 * u, y1 - 4 * u], [x0 + 4 * u, y1 - 4 * u]], "#ffffff", 1.4 * u);
      p.poly([[hx - 14 * u, y0 - 3 * u], [hx + 2 * u, y0 - 3 * u], [hx + 2 * u, y0 + 6 * u], [hx - 14 * u, y0 + 6 * u]], "#9aa3ad", 1.4 * u);
      for (let i = 0; i < 3; i++) p.stroke([[x0 + 9 * u, y0 + (15 + i * 7) * u], [x1 - (9 + (i % 2) * 8) * u, y0 + (15 + i * 7) * u]], 1.3 * u, "#5a6a8a");
      const bx = hx - 6 * u, by = y1 - 12 * u; // the house on its screws
      p.poly([[bx - 12 * u, by - 22 * u], [bx + 12 * u, by - 22 * u], [bx + 12 * u, by - 8 * u], [bx - 12 * u, by - 8 * u]], null, 1.3 * u);
      p.poly([[bx - 14 * u, by - 22 * u], [bx, by - 31 * u], [bx + 14 * u, by - 22 * u]], null, 1.3 * u);
      for (const dx of [-9, 0, 9]) p.stroke([[bx + dx * u, by - 8 * u], [bx + dx * u, by]], 1.3 * u, "#c8352e");
      p.dot(hx + 14 * u, hy - 4 * u, 5.5 * u);
    } else if (prop === "icecream") {
      p.poly([[hx - 8 * u, hy - 12 * u], [hx + 8 * u, hy - 12 * u], [hx, hy + 7 * u]], "#e0a35a", 1.8 * u);
      p.ell(hx, hy - 19 * u, 11 * u, 10 * u, "#f7c6d9", 2.2 * u);
      p.dot(hx, hy, 5.5 * u);
    } else if (Array.isArray(prop) && prop[0] === "hammer") {
      const ang = rad(-70 + 105 * clamp(prop[1], 0, 1));
      const Rh = (pts: P2[]) => rotPts(pts, ang, hx, hy);
      p.band(Rh([[hx, hy + 14 * u], [hx, hy - 52 * u]]), "#a8743f", 5.5 * u, 1.5 * u, "round");
      // claw hammer head: round striking face on one side, curved split claw on the other
      p.poly(Rh([[hx - 10 * u, hy - 70 * u], [hx + 26 * u, hy - 70 * u], [hx + 30 * u, hy - 66 * u], [hx + 30 * u, hy - 50 * u], [hx + 26 * u, hy - 46 * u], [hx - 10 * u, hy - 46 * u]]), "#8d949c", 2.4 * u);
      p.poly(Rh([[hx - 10 * u, hy - 68 * u], [hx - 30 * u, hy - 72 * u], [hx - 40 * u, hy - 62 * u], [hx - 24 * u, hy - 60 * u], [hx - 10 * u, hy - 50 * u]]), "#8d949c", 2.2 * u);
      p.dot(hx, hy, 5.5 * u);
    }
  }
  if (prop === "shako") { // carried by the left hand
    const [hx, hy] = arms[0].pts[2];
    p.poly([[hx - 14 * u, hy + 3 * u], [hx + 14 * u, hy + 3 * u], [hx + 16 * u, hy + 30 * u], [hx - 16 * u, hy + 30 * u]], "#3a3d47", 2.2 * u);
    p.ell(hx, hy + 31 * u, 3.5 * u, 3.5 * u, "#2b7a4b", 1.5 * u);
    p.dot(hx, hy, 5.5 * u);
  }
  p.rot = null;
};

export type SideOpts = {
  phase?: number; expr?: Expr; mode?: "march" | "stand" | "swing" | "push" | "kneel" | "sit"; blink?: boolean | number; stomp?: number; pose?: number;
  /** step length as a multiple of 0.8 m (370 units): matches 1.6 m/s at 2 steps/s; scale by the view's foreshortening */
  stride?: number; light?: number; seed?: number;
  /** sit mode: what he sits on, drawn in the card under the hips (owner rule 40: seated people must read as seated) */
  seat?: "chair" | "crate" | "none";
  /** kneel mode: turning a jackscrew lever (phase 0..1); the screw post + lever are drawn in front of him */
  crank?: number;
  /** kneel + crank: height of the screw head above the soles in design units (default: at the hands) */
  screwTop?: number;
  /** push mode: where the hands land at pose 1, in final canvas units (e.g. the swing kid's back) */
  hand?: [number, number];
};

/** seat under a profile sitter (facing +x): seat top at y `st`, hips at x 300, knees at 300 + l1.
 *  chair = bentwood cafe chair (round seat seen edge-on, 2 near + 2 far legs, ring stretcher, curved back behind the spine);
 *  crate = a wooden ammunition box with planks + rope handle. Floor at `sole`. */
const seatSide = (p: Pen, kind: "chair" | "crate", st: number, l1: number, HH: number, u: number, sole: number, ow: number, thick: number, light: number) => {
  const wood = "#8a5530", woodD = mix("#8a5530", INK, 0.35), xr = 300 - 0.36 * HH, xf = 300 + 0.72 * l1;
  if (kind === "crate") {
    const box: P2[] = [[xr, st], [xf, st], [xf, sole], [xr, sole]];
    p.gradFill(box, "#9a7a4a", mul("#9a7a4a", [0.72, 0.7, 0.78]), light);
    for (let i = 1; i < 3; i++) p.stroke([[xr, st + ((sole - st) * i) / 3], [xf, st + ((sole - st) * i) / 3]], 2.2 * u, mix("#9a7a4a", INK, 0.5));
    p.stroke([[xr + 7 * u, st + 5 * u], [xr + 7 * u, sole - 4 * u]], 2.2 * u, mix("#9a7a4a", INK, 0.5));
    p.stroke([[xf - 7 * u, st + 5 * u], [xf - 7 * u, sole - 4 * u]], 2.2 * u, mix("#9a7a4a", INK, 0.5));
    p.stroke([[xr + 7 * u, st + 5 * u], [xf - 7 * u, sole - 4 * u]], 2.6 * u, mix("#9a7a4a", INK, 0.5)); // diagonal brace: a crate, not a case
    p.inkRing(box, ow, thick);
    return;
  }
  const sy = st + 6 * u, legW = 4.6 * u;
  // far legs (lighter, offset back), ring stretcher, near legs, seat, back
  for (const [x0, x1] of [[xr + 12 * u, xr + 6 * u], [xf + 4 * u, xf + 10 * u]]) p.line([[x0, sy], [x1, sole]], woodD, legW * 0.85, true);
  p.line([[xr + 2 * u, sy + 0.55 * (sole - sy)], [xf - 2 * u, sy + 0.55 * (sole - sy)]], woodD, 3 * u, true);
  for (const [x0, x1] of [[xr + 4 * u, xr - 4 * u], [xf - 4 * u, xf + 2 * u]]) p.line([[x0, sy], [x1, sole]], wood, legW, true);
  const seat: P2[] = [[xr - 6 * u, st - 2 * u], [xf + 6 * u, st - 2 * u], [xf + 4 * u, st + 7 * u], [xr - 4 * u, st + 7 * u]];
  p.poly(seat, wood, ow * 0.8);
  // bentwood back: post from the rear of the seat, curving up behind the spine, closing in a loop
  const top = st - 0.98 * HH;
  p.line(curve([xr - 2 * u, st], [xr - 10 * u, st - 0.5 * HH], [xr - 4 * u, top]), wood, legW, true);
  p.line(curve([xr - 4 * u, top], [xr + 6 * u, top - 10 * u], [xr + 14 * u, top + 6 * u]), wood, legW, true);
  p.line(curve([xr - 5 * u, st - 0.42 * HH], [xr - 1 * u, st - 0.7 * HH], [xr + 12 * u, top + 8 * u]), wood, 3 * u, true);
};

/** two-bone leg, knee bending forward (+x) */
const ik = (hip: P2, ank: P2, l1: number, l2: number): P2 => {
  const dx = ank[0] - hip[0], dy = ank[1] - hip[1], d = clamp(Math.hypot(dx, dy), 1, l1 + l2 - 0.01);
  const A = Math.acos(clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1, 1)), k = Math.atan2(dy, dx) - A;
  return [hip[0] + l1 * Math.cos(k), hip[1] + l1 * Math.sin(k)];
};

/** hip height of the seated kid in `swing` mode (design units); swingKid seats the torso bottom on the plank */
const SWING_HIP = 733;

/** side view facing screen-right; march footfalls land at phase 0 (near foot) and 0.5 (far foot), like the front view.
 *  The stance foot is planted: it slides back at exactly the walking speed while the hip rises and falls over it. */
export const bodySide = (p: Pen, o: Outfit, opts: SideOpts) => {
  const { phase = 0, expr = "neutral", mode = "march", blink = false, stomp = 1, pose = 0, stride = 1, light = DEF_LIGHT, seed = 1 } = opts;
  if (mode === "kneel" && opts.crank !== undefined && !(opts as any)._shifted) { // shift left so the screw in front fits the card
    p.g.save(); p.g.translate(-130, 0); bodySide(p, o, { ...opts, _shifted: true } as SideOpts); p.g.restore(); return;
  }
  const Bd = BUILD[o.build ?? "adult"], skin = o.skin ?? SKIN, two = Math.PI * 2, lid = lidOf(blink);
  const H: Blob = { ...headBlob(seed, Bd.a, 1), asym: 0.12, rot: rad(3 + 3 * (rnd(seed, 7) - 0.5)) };
  const W = 2 * H.a, HH = 2 * H.b, u = W / 100, sole = 975, ankY = sole - 4 * u;
  const thick = thickAngle(light), ow = 2.9 * u; // v3: reference character outline ~6-8 px at 1080
  const legLen = ((opts.mode === "sit" || opts.mode === "kneel" ? Math.max(Bd.legs, 0.95) : Bd.legs) + 0.12) * HH - 4 * u, l1 = legLen / 2, l2 = legLen / 2;
  const nearCol = mix(o.pants, INK, 0.55), farCol = mix(o.pants, INK, 0.75), footCol = o.boots;
  type LegS = { ank: P2; pitch: number; near: boolean; knee?: P2 };
  const legs: LegS[] = [];
  let hipY = ankY - legLen * 0.995, lean = 0, nearFwd = 0;
  if (mode === "march") {
    const S = 370 * stride, liftH = Math.max(22, 40 + 70 * (stomp - 1));
    const st = (ph: number) => {
      const c = (((phase + ph) % 1) + 1) % 1;
      if (c < 0.5) { const s = c / 0.5; return { x: S / 2 - S * s, h: 0, stance: true, s }; }
      const s = (c - 0.5) / 0.5; // swing: cycloid in world space, so the foot leaves and lands at zero ground speed
      return { x: -S / 2 + S * s - (S / Math.PI) * Math.sin(2 * Math.PI * s), h: liftH * Math.sin(Math.PI * s), stance: false, s };
    };
    const nL = st(0), fL = st(0.5), stance = nL.stance ? nL : fL;
    const Leff = legLen * (1 - 0.035 * Math.sin(Math.PI * stance.s));
    hipY = ankY - Math.sqrt(Math.max(1, Leff * Leff - stance.x * stance.x));
    for (const [L, near] of [[fL, false], [nL, true]] as const)
      legs.push({ ank: [300 + L.x, ankY - L.h], pitch: L.stance ? 0 : rad(35 * Math.sin(Math.PI * L.s) * (1 - 1.6 * L.s)), near });
    lean = 4 + 3 * Math.cos(2 * two * phase); // 7 deg at contact, 1 deg at passing
    nearFwd = nL.x / (S / 2);
  } else if (mode === "push") {
    hipY = ankY - 0.87 * legLen;
    legs.push({ ank: [300 - 0.5 * legLen, ankY], pitch: rad(-8), near: false }, { ank: [300 + 0.32 * legLen, ankY], pitch: 0, near: true });
    lean = 14 * pose;
  } else if (mode === "kneel") {
    // one knee on the ground (near leg, shin flat, toes tucked), the far foot planted forward with its knee up
    hipY = ankY - 0.52 * legLen;
    legs.push({ ank: [300 + 0.46 * legLen, ankY], pitch: 0, near: false },
      { ank: [300 - 0.36 * legLen, ankY - 7 * u], knee: [300 + 0.1 * legLen, ankY - 5 * u], pitch: rad(-70), near: true });
    lean = 16 + 4 * pose;
  } else if (mode === "swing") {
    hipY = SWING_HIP;
    const a = rad(60 * pose);
    for (const [dx, near] of [[-6, false], [0, true]] as const) {
      const knee: P2 = [300 + l1 * 0.98 + dx * u, hipY + 6 * u];
      legs.push({ ank: [knee[0] + l2 * Math.sin(a), knee[1] + l2 * Math.cos(a)], pitch: -a * 0.5, near });
    }
  } else if (mode === "sit") {
    // seated in profile: thighs level on the seat, shins straight down, both soles flat on the floor
    hipY = ankY - l2;
    legs.push({ ank: [300 + l1 - 4 * u, ankY], pitch: 0, near: false }, { ank: [300 + l1 + 3 * u, ankY], pitch: 0, near: true });
    lean = 6;
  } else {
    legs.push({ ank: [300 - 4 * u, ankY], pitch: 0, near: false }, { ank: [300 + 4 * u, ankY], pitch: 0, near: true });
  }
  const torsoBot = mode === "sit" ? hipY + 4 * u : hipY + 0.12 * HH, chin = torsoBot - Bd.torso * HH, hc = chin - H.b, crown = hc - H.b, hip: P2 = [300, hipY];
  p.rot = null;
  if (mode === "sit" && opts.seat !== "none") seatSide(p, opts.seat ?? "chair", hipY + 3 * u, l1, HH, u, sole, ow, thick, light);
  for (const L of legs) {
    const knee = L.knee ?? (mode === "swing" ? ([300 + l1 * 0.98 + (L.near ? 0 : -6 * u), hipY + 6 * u] as P2) : ik(hip, L.ank, l1, l2));
    const hp0: P2 = [300 + (L.near ? 0 : -5 * u), hipY];
    p.stroke([hp0, knee, L.ank], 5.8 * u, L.near ? nearCol : farCol);
    const c = Math.cos(L.pitch), s = Math.sin(L.pitch);
    footStroke(p, [L.ank[0] - 3 * u * c, L.ank[1] - 3 * u * s], [L.ank[0] + 13 * u * c, L.ank[1] + 13 * u * s + 0.5 * u],
      7.5 * u, L.near ? footCol : footCol === INK ? INK : shade(footCol, 0.82));
  }
  if (mode === "sit" && o.dress) { // seated lady in profile: the skirt drapes over the lap and falls past the knee
    const kx = 300 + l1, sk: P2[] = [[300 - 0.3 * HH, hipY - 0.16 * HH], [300 + 0.1 * HH, hipY - 0.1 * HH], [kx + 2 * u, hipY - 6 * u], [kx + 9 * u, hipY + 2 * u],
      [kx + 12 * u, hipY + 0.6 * l2], [kx - 14 * u, hipY + 0.62 * l2], [kx - 16 * u, hipY + 8 * u], [300 - 0.32 * HH, hipY + 8 * u]];
    p.gradFill(sk, o.dress, mul(o.dress, SH_CLOTH), light); p.inkRing(sk, ow, thick);
  }
  // ---- upper body leans about the hip ----
  p.rot = lean ? [rad(lean), 300, hipY] : null;
  const T: Blob = { a: (o.build === "stout" ? 0.38 : 0.33) * W, b: 0.5 * (torsoBot - (chin - 0.25 * HH)), nTop: 2.6, nBot: 4.4, egg: 0.1, asym: 0.06,
    rot: 0, noise: 0.006, seed: seed + 7 };
  const tcx = 300 + 2 * u, tcy = torsoBot - T.b, tp = blobPts(tcx, tcy, T);
  const armCol = mix(o.jacket, INK, 0.5), farArm = mix(o.jacket, INK, 0.68);
  const S: P2 = [tcx + 0.05 * T.a, chin + 0.14 * HH], aLen = 0.95 * HH;
  const swingArm = (ang: number): [P2, P2, P2] => {
    const e: P2 = [S[0] + Math.sin(ang) * aLen * 0.5, S[1] + Math.cos(ang) * aLen * 0.5], a2 = ang + rad(16) * Math.sign(ang || 1);
    return [S, e, [e[0] + Math.sin(a2) * aLen * 0.5, e[1] + Math.cos(a2) * aLen * 0.5]];
  };
  const rifle = !!o.rifle && (mode === "march" || mode === "stand");
  const B0: P2 = [tcx + 0.72 * T.a, chin + 0.58 * HH], B1: P2 = [tcx - 0.95 * T.a - 22 * u, crown - 0.4 * HH];
  let near: [P2, P2, P2], far: [P2, P2, P2] | null;
  if (mode === "swing") { near = [S, [S[0] + 12 * u, S[1] - 0.16 * HH], [300 + 6 * u, chin - 0.3 * HH]]; far = [S, [S[0] + 8 * u, S[1] - 0.18 * HH], [300 + 2 * u, chin - 0.36 * HH]]; }
  else if (mode === "push" || mode === "kneel") {
    const reach = mode === "kneel" ? 0.62 * HH + 0.1 * HH * Math.sin(two * (opts.crank ?? 0)) : 0.55 * HH + 0.45 * HH * pose;
    let hN: P2 = [S[0] + reach, S[1] + 0.06 * HH];
    if (opts.hand) {
      // target is in final canvas units; the arm is drawn inside the lean rotation, so undo it
      const th = -rad(lean), dx = opts.hand[0] - 300, dy = opts.hand[1] - hipY;
      const tg: P2 = [300 + dx * Math.cos(th) - dy * Math.sin(th), hipY + dx * Math.sin(th) + dy * Math.cos(th)];
      hN = [hN[0] + (tg[0] - hN[0]) * pose, hN[1] + (tg[1] - hN[1]) * pose];
    }
    near = [S, [(S[0] + hN[0]) / 2, (S[1] + hN[1]) / 2 + 0.06 * HH], hN];
    far = [S, [(S[0] + hN[0]) / 2 - 4 * u, (S[1] + hN[1]) / 2 - 0.02 * HH], [hN[0] - 6 * u, hN[1] - 0.08 * HH]];
  } else if (mode === "sit") {
    // forearms forward onto the table in front (opts.hand = near hand in final canvas units)
    let hN: P2 = [S[0] + 0.78 * aLen, S[1] + 0.22 * HH];
    if (opts.hand) { const th = -rad(lean), dx = opts.hand[0] - 300, dy = opts.hand[1] - hipY; hN = [300 + dx * Math.cos(th) - dy * Math.sin(th), hipY + dx * Math.sin(th) + dy * Math.cos(th)]; }
    near = [S, [S[0] + 0.12 * aLen, S[1] + 0.45 * aLen], hN];
    far = [S, [S[0] + 0.06 * aLen, S[1] + 0.42 * aLen], [hN[0] - 9 * u, hN[1] - 3 * u]];
  } else if (rifle) { near = [S, [S[0] - 4 * u, S[1] + 0.42 * HH], B0]; far = mode === "march" ? swingArm(rad(30) * nearFwd) : swingArm(0); }
  else { near = swingArm(rad(-30) * nearFwd); far = mode === "march" ? swingArm(rad(30) * nearFwd) : null; }
  if (far) { p.stroke(curve(far[0], far[1], far[2]), 5.2 * u, farArm); p.dot(far[2][0], far[2][1], 5.5 * u); }
  p.gradFill(tp, o.jacket, mul(o.jacket, SH_CLOTH), light);
  p.clip(tp, () => {
    // owner Nov 12 (couch jack men): a strap running down the side-view body read as a beam through him. In profile the belt is
    // a level waist belt with a buckle at the front, never a long diagonal strap
    if (o.belt) { const by = torsoBot - 0.2 * HH; p.band([[tcx - 1.4 * T.a, by], [tcx + 1.4 * T.a, by]], o.belt!, 6 * u, 1.8 * u); p.poly([[tcx + 0.55 * T.a, by - 5 * u], [tcx + 0.75 * T.a, by - 5 * u], [tcx + 0.75 * T.a, by + 5 * u], [tcx + 0.55 * T.a, by + 5 * u]], "#c9a24a", 1.4 * u); }
    if (o.sash) p.band([[tcx - 1.3 * T.a, torsoBot - 0.32 * HH], [tcx + 1.3 * T.a, torsoBot - 0.32 * HH]], o.sash, 0.13 * HH, 1.8 * u);
    if (!o.dress) for (let i = 0; i < 3; i++) { const y = chin + 0.16 * HH + i * 0.24 * HH; p.dot(tcx + 0.8 * T.a, y, 3 * u, INK); p.dot(tcx + 0.8 * T.a, y, 2.2 * u, o.buttons ?? shade(o.jacket, 0.7)); }
  });
  p.inkRing(tp, ow, thick);
  if (rifle) {
    p.band([B0, B1], "#7a4b2a", 5 * u, 1.5 * u, "round");
    p.band([lerp2(B0, B1, 0.6), B1], "#8d949c", 2.4 * u, 1.2 * u, "round");
  }
  p.stroke(curve(near[0], near[1], near[2]), 5.2 * u, armCol); p.dot(near[2][0], near[2][1], 5.5 * u);
  if (mode === "kneel" && opts.crank !== undefined) {
    // jackscrew in front of him: timber pad, threaded iron post, cap; the lever bar runs from the cap into his hands
    p.rot = null;
    const th = rad(lean), toG = (q: P2): P2 => { const dx = q[0] - 300, dy = q[1] - hipY; return [300 + dx * Math.cos(th) - dy * Math.sin(th), hipY + dx * Math.sin(th) + dy * Math.cos(th)]; };
    const hG = toG(near[2]), sx = 600, top = opts.screwTop !== undefined ? sole - opts.screwTop : hG[1] - 4 * u; // screw at card x 470
    p.poly([[sx - 34 * u, sole - 16 * u], [sx + 34 * u, sole - 16 * u], [sx + 34 * u, sole], [sx - 34 * u, sole]], "#8a6a4a", 3 * u);
    p.poly([[sx - 9 * u, sole - 16 * u], [sx - 7 * u, top + 8 * u], [sx + 7 * u, top + 8 * u], [sx + 9 * u, sole - 16 * u]], "#4a4f5a", 3 * u);
    for (let y = sole - 26 * u; y > top + 14 * u; y -= 9 * u) p.stroke([[sx - 7 * u, y + 3 * u], [sx + 7 * u, y - 3 * u]], 1.6 * u, "#2b2f38");
    p.poly([[sx - 16 * u, top + 10 * u], [sx + 16 * u, top + 10 * u], [sx + 16 * u, top - 2 * u], [sx - 16 * u, top - 2 * u]], "#3a3f4a", 3 * u);
    // the bar goes into the screw: at the head when the head is below his hands, else through a collar at hand height
    const ay = top + 4 * u < hG[1] ? hG[1] + 2 * u : top + 4 * u;
    if (ay !== top + 4 * u) p.poly([[sx - 13 * u, ay - 7 * u], [sx + 13 * u, ay - 7 * u], [sx + 13 * u, ay + 7 * u], [sx - 13 * u, ay + 7 * u]], "#3a3f4a", 3 * u);
    p.band([[sx + 6 * u, ay], [hG[0] - 10 * u, hG[1] + 2 * u]], "#6d737b", 4.5 * u, 1.6 * u, "round");
    p.dot(hG[0], hG[1], 5.5 * u); p.dot(hG[0] - 7 * u, hG[1] - 3 * u, 5.5 * u);
    p.rot = lean ? [rad(lean), 300, hipY] : null;
  }
  // ---- head ----
  const hx = 300 + 4 * u;
  hatBehind(p, o, H, hx, hc, light, thick, ow, true);
  const hp = blobPts(hx, hc, H);
  p.shadedFill(hp, skin, mul(skin, SH_SKIN), light, H.a);
  p.inkRing(hp, ow, thick);
  const brim = !!o.hat; // brows sit low, between the eyes and the hairline/hat (never on the hair)
  if (!brim) hatOn(p, o, hp, H, hx, hc, light, seed, 1, true);
  faceSide(p, hx, hc, W, expr, lid, brim, skin, o.moustache, o.build === "stout");
  if (brim) hatOn(p, o, hp, H, hx, hc, light, seed, 1, true);
  p.rot = null;
};

/** rope + seat + seated kid on a 700 x 2300 canvas; the pivot is design (350, 20); kid drawn at 0.92 scale */
export const swingKid = (p: Pen, o: Outfit, kick: number, expr: Expr, light = DEF_LIGHT, blink: number = 0) => {
  const rope = 1830, k = 1.1, HH = 2 * headBlob(5, BUILD[o.build ?? "adult"].a, 1).b;
  // two ropes from the pivot to the ends of a wide plank, the kid framed between them: a single rope behind the kid
  // ended at the cap and read as a hanging. Far rope behind the kid, near rope drawn over (clear of the face).
  const seat = rope + 18, x0 = 150, x1 = 550;
  p.line([[350, 20], [x0 + 16, seat + 4]], "#a07a4c", 10);
  p.poly(rrect(x0, seat, x1, seat + 36, 10), "#b5653f", 9);
  const g = p.g;
  g.save();
  g.translate(350 - 300 * k, rope + 18 - (SWING_HIP + 0.12 * HH) * k);
  g.scale(k, k);
  bodySide(new Pen(g), o, { expr, mode: "swing", pose: kick, light, seed: 5, blink });
  g.restore();
  p.line([[350, 20], [x1 - 16, seat + 4]], "#a07a4c", 10);
};

// ---------------- effects ----------------
export const fxNote = (p: Pen, kind: number, col = "#1f2a44") => {
  p.ell(70, 200, 46, 34, col, 8, 0, 360, -20);
  p.stroke([[110, 190], [110, 40]], 14);
  if (kind === 0) p.poly([[110, 40], [170, 70], [170, 110], [110, 82]], col, 8);
  else {
    p.ell(150, 170, 40, 30, col, 8, 0, 360, -20);
    p.stroke([[186, 160], [186, 20]], 14);
    p.poly([[110, 40], [186, 20], [186, 50], [110, 70]], col, 8);
  }
};

/** spark / impact star on a 500 x 500 canvas; t in 0..1 */
export const fxBurst = (p: Pen, t: number, col = "#fff3b0", rays = 10, r0 = 40, r1 = 230) => {
  const c = 250, e = 1 - (1 - t) ** 3;
  for (let i = 0; i < rays; i++) {
    const a = rad((i * 360) / rays + 7 * (i % 2)), ra = r0 + (r1 - r0) * e * (0.75 + 0.25 * (i % 2));
    p.poly([[c + r0 * 0.5 * Math.cos(a + 0.18), c + r0 * 0.5 * Math.sin(a + 0.18)], [c + ra * Math.cos(a), c + ra * Math.sin(a)],
      [c + r0 * 0.5 * Math.cos(a - 0.18), c + r0 * 0.5 * Math.sin(a - 0.18)]], col, Math.max(3, 8 * (1 - t)));
  }
  if (t < 0.5) p.ell(c, c, r0 * (1.4 - t), r0 * (1.4 - t), WHITE, 8);
};

/** water splash crown on an 800 x 800 canvas; t in 0..1 */
export const fxSplash = (p: Pen, t: number) => {
  const c = 400, size = 800, rise = Math.sin(Math.min(1, t * 1.3) * Math.PI);
  const blue = "#bfe8ff", deep = "#6cc0f0";
  if (rise > 0.02) {
    const pts: P2[] = [];
    for (let i = 0; i < 19; i++) {
      const h = (i % 2 ? 260 : 130) * rise * (0.7 + 0.3 * Math.sin(i * 1.7));
      pts.push([c - 330 + (660 * i) / 18, size - 120 - h]);
    }
    p.poly([...pts, [c + 330, size - 90], [c - 330, size - 90]], blue, 10);
    p.ell(c, size - 100, 360, 46, deep, 10);
  }
  for (let i = 0; i < 8; i++) {
    const a = rad(200 + i * 18), d = 120 + 380 * t, y = size - 160 + d * Math.sin(a) + 520 * t * t, r = 26 * (1 - t) + 6;
    if (t > 0.08 && y < size - 40) p.ell(c + d * Math.cos(a), y, r, r * 1.25, blue, 7);
  }
};

/** dust puff on a 300 x 300 canvas; t in 0..1 */
export const fxPuff = (p: Pen, t: number) => {
  for (let i = 0; i < 5; i++) {
    const a = rad(160 + i * 55), d = 40 + 70 * t, r = (34 + 20 * (i % 2)) * (1 - 0.6 * t);
    p.ell(150 + d * Math.cos(a), 180 + d * 0.45 * Math.sin(a), r, r * 0.8, `rgba(238,225,205,${(1 - t).toFixed(3)})`, 0);
  }
};

/** circling stars on a 420 x 210 canvas */
export const fxStars = (p: Pen, t: number) => {
  for (let i = 0; i < 4; i++) {
    const a = t * Math.PI * 2 + (i * Math.PI) / 2, x = 210 + 150 * Math.cos(a), y = 110 + 40 * Math.sin(a), pts: P2[] = [];
    for (let k = 0; k < 10; k++) { const r = k % 2 ? 14 : 34, b = rad(k * 36 - 90); pts.push([x + r * Math.cos(b), y + r * Math.sin(b)]); }
    p.poly(pts, "#ffd84a", 6);
  }
};

/** three jittering strain ticks on a 300 x 300 canvas */
export const fxCreak = (p: Pen, t: number) => {
  const j = 6 * Math.sin(t * 40);
  for (const a of [-30, 0, 30]) {
    const b = rad(a - 90);
    p.stroke([[150 + 70 * Math.cos(b) + j, 230 + 70 * Math.sin(b)], [150 + 100 * Math.cos(b) + 10 + j, 230 + 100 * Math.sin(b)],
      [150 + 130 * Math.cos(b) + j, 230 + 130 * Math.sin(b)]], 10);
  }
};

/** flat water ring (drawn top-down) on a 600 x 600 canvas; t in 0..1 */
export const fxRing = (p: Pen, t: number) => {
  // thin light water rings (white crest, pale blue trailing rings), thinning as they spread
  const g = p.g;
  for (let k = 0; k < 3; k++) {
    const u = t - k * 0.22;
    if (u <= 0 || u >= 1) continue;
    g.beginPath(); g.ellipse(300, 300, 60 + 230 * u, 60 + 230 * u, 0, 0, Math.PI * 2);
    g.strokeStyle = k === 0 ? "#f6fcff" : "#cfe8fa"; g.lineWidth = 9 * (1 - u) + 3; g.stroke();
  }
};

/** text-free sign on a 700 x 520 canvas: "no marching in step on the bridge". A bridge (deck + arch + piers), four
 *  identical pairs of marching legs in the same stride (in step), a bold red X over all of it. */
export const fxSign = (p: Pen) => {
  const g = p.g, RED = "#d42f2f";
  p.poly(rrect(14, 14, 686, 506, 40), "#f6ecd2", 0);
  p.poly(rrect(14, 14, 686, 506, 40), null, 14);
  // bridge: deck, stone arch underneath, two piers
  p.poly(rrect(70, 352, 630, 384, 8), "#8a5a3a", 9);
  g.beginPath(); g.moveTo(112, 470); g.quadraticCurveTo(350, 300, 588, 470);
  g.strokeStyle = INK; g.lineWidth = 16; g.lineCap = "round"; g.stroke();
  for (const x of [88, 612]) p.poly(rrect(x - 16, 384, x + 16, 470, 4), "#8a5a3a", 9);
  // four identical soldiers' legs mid-stride: same leg forward on every one = in step
  for (const x of [150, 278, 406, 534]) {
    p.poly(rrect(x - 30, 150, x + 30, 214, 14), "#357650", 9);                  // coat hem
    p.stroke([[x - 8, 210], [x + 34, 262], [x + 46, 338]], 15, INK);           // front leg
    p.stroke([[x + 6, 210], [x - 12, 274], [x - 36, 336]], 15, INK);           // back leg
    p.poly(rrect(x + 30, 330, x + 74, 350, 9), INK, 0);                          // boots point forward
    p.poly(rrect(x - 52, 328, x - 8, 348, 9), INK, 0);
  }
  // big red X
  for (const [a, b] of [[[96, 70], [604, 452]], [[604, 70], [96, 452]]] as [[number, number], [number, number]][]) {
    p.stroke([a, b], 58, "#ffffff");
    p.stroke([a, b], 42, RED);
  }
};

/** soft cartoon cloud on a 600 x 300 canvas */
export const fxCloud = (p: Pen, seed: number) => {
  const blobs: [number, number, number][] = [[150, 190, 80], [250, 150, 105], [360, 160, 95], [450, 195, 70], [300, 210, 90]];
  for (const [x, y, r] of blobs) p.ell(x + ((seed * 37) % 20) - 10, y, r, r * 0.8, "#ffffff", 0);
  p.ell(300, 235, 230, 40, "#ffffff", 0);
};

/** cast shadow on a 128 x 256 canvas: dark soft contact pool at the feet (y 205) and a softer tail that runs up the
 *  canvas = away from the sun, fading with distance; multiply colour (sRGB-encoded linear ratio), white = no change */
export const fxShadow = (p: Pen, col: string) => {
  const g = p.g;
  g.fillStyle = WHITE; g.fillRect(0, 0, 128, 256);
  g.save(); g.filter = "blur(9px)";
  const lg = g.createLinearGradient(0, 205, 0, 22);
  lg.addColorStop(0, mix(col, WHITE, 0.08)); lg.addColorStop(0.55, mix(col, WHITE, 0.3)); lg.addColorStop(1, mix(col, WHITE, 0.85));
  g.fillStyle = lg;
  g.beginPath(); g.moveTo(40, 205); g.bezierCurveTo(36, 120, 46, 50, 64, 30); g.bezierCurveTo(82, 50, 92, 120, 88, 205); g.closePath(); g.fill();
  g.fillStyle = col; g.beginPath(); g.ellipse(64, 205, 30, 17, 0, 0, Math.PI * 2); g.fill();
  g.restore();
};

/** tight contact shadow right under the feet on a 128 x 128 canvas: dark core, short fall-off (multiply colour) */
export const fxContact = (p: Pen, col: string) => {
  const g = p.g;
  g.fillStyle = WHITE; g.fillRect(0, 0, 128, 128);
  const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  for (const [r, k] of [[0, 0], [0.32, 0.02], [0.5, 0.22], [0.66, 0.58], [0.82, 0.88], [1, 1]] as const) gr.addColorStop(r, mix(col, WHITE, k));
  g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
};

/** floating wooden plank, side-on, on a 320 x 110 canvas */
export const fxPlank = (p: Pen) => {
  p.poly(rrect(14, 30, 306, 78, 10), "#a8744a", 9);
  p.line([[40, 46], [150, 44], [270, 50]], "#7d5234", 4);
  p.line([[60, 62], [200, 64], [284, 60]], "#7d5234", 4);
  p.dot(36, 54, 5, INK); p.dot(284, 54, 5, INK);
};

/** floating marching drum (no text) on a 260 x 240 canvas: white shell, red hoops, ink zig-zag cord */
export const fxDrum = (p: Pen) => {
  p.poly(rrect(40, 70, 220, 190, 16), "#f1ece0", 9);
  p.poly(rrect(32, 58, 228, 86, 12), "#c9373a", 8);
  p.poly(rrect(32, 176, 228, 204, 12), "#c9373a", 8);
  p.line([[52, 88], [82, 172], [112, 88], [142, 172], [172, 88], [202, 172]], INK, 6);
  p.ell(130, 58, 98, 18, "#f7f3ea", 8);
};

/** soft ground contact blob on a 128 x 128 canvas, multiply colour (sRGB-encoded linear ratio) in the centre */
export const fxBlob = (p: Pen, col: string) => {
  const g = p.g;
  g.fillStyle = WHITE; g.fillRect(0, 0, 128, 128);
  // soft contact shadow: flat core, then a long smooth (roughly gaussian) fall-off to white = no change
  const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  for (const [r, k] of [[0, 0], [0.5, 0.04], [0.64, 0.18], [0.76, 0.42], [0.87, 0.72], [0.95, 0.92], [1, 1]] as const) gr.addColorStop(r, mix(col, WHITE, k));
  g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
};
