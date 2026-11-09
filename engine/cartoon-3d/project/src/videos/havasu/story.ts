// "London Bridge Is Falling Down... to Arizona": original ~71 s short (experiment for Modern Vista Prints).
// Timeline (word times from havasu/voice/words.json + VO_OFF), story state per shot (which world, how much of the
// bridge stands, sand / water levels), and the camera grammar of the bridge short: smootherstep glides 18-40 f,
// cuts on big reframes, every hold creeps in, impact kicks flip sign every frame and decay over 7 f.
export const FPS = 30;
export const VO_OFF = 0.2; // voice starts 0.2 s into the film
export const TOTAL = 2130;
export const POSTER_AT = 1927; // "But if the famous one..." -> 2D poster end card
export const D0 = 6.0; // bank top + deck height (m)
export const HW = 6.5; // deck half width
export type V3 = [number, number, number];

export const clamp01 = (x: number) => Math.max(0, Math.min(1, x));
export const smooth = (x: number) => { const u = clamp01(x); return u * u * (3 - 2 * u); };
export const easeOut = (u: number) => 1 - (1 - clamp01(u)) ** 4;
export const W = (s: number) => s + VO_OFF; // word time -> film time

// ---------------- shots ----------------
export type Light = "day" | "golden";
export type Place = "london" | "desert" | "sea";
export type ShotDef = { id: number; a: number; b: number; light: Light; place: Place; sunAz?: number; sunEl?: number };
export const SHOTS: ShotDef[] = [
  { id: 1, a: 0, b: 190, light: "day", place: "desert" },      // hook: bridge in the desert
  { id: 2, a: 190, b: 310, light: "day", place: "london", sunAz: 120 }, // London aerial
  { id: 3, a: 310, b: 455, light: "day", place: "london" },    // traffic, sinking
  { id: 4, a: 455, b: 583, light: "day", place: "london" },    // FOR SALE
  { id: 5, a: 583, b: 697, light: "day", place: "london" },    // McCulloch + chainsaw
  { id: 6, a: 697, b: 760, light: "day", place: "desert" },    // new town by a lake
  { id: 7, a: 760, b: 838, light: "day", place: "london" },    // money bag
  { id: 8, a: 838, b: 958, light: "day", place: "london" },    // dismantling, numbered stones
  { id: 9, a: 958, b: 1012, light: "day", place: "sea" },      // ship
  { id: 10, a: 1012, b: 1070, light: "day", place: "desert" }, // trucks
  { id: 11, a: 1070, b: 1138, light: "day", place: "desert" }, // piece by piece
  { id: 12, a: 1138, b: 1239, light: "golden", place: "desert" }, // stood proudly
  { id: 13, a: 1239, b: 1395, light: "day", place: "desert" }, // fisherman, no water
  { id: 14, a: 1395, b: 1539, light: "day", place: "desert" }, // dig + flood
  { id: 15, a: 1539, b: 1626, light: "day", place: "desert" }, // empty frame
  { id: 16, a: 1626, b: 1797, light: "day", place: "desert" }, // tourists
  { id: 17, a: 1797, b: TOTAL, light: "day", place: "desert" }, // the rumor (3D runs under the poster card a moment)
];
// Dissolves (measured reference: almost no hard cuts, 6-10 frame crossfades on sentence starts): every shot change
// except the hook flash (shot 2) gets an 8-frame crossfade, and every in-shot camera cut becomes an 8-frame dissolve.
export const XFADE: Record<number, number> = {}; // round 2: shot dissolves happen in remap.ts (new timeline)
export const CUT_X = 8;
const NO_ORBIT = new Set<number>([]);
export const FLASH_AT = 190;
export const shotAt = (f: number) => SHOTS.find((s) => f >= s.a && f < s.b) ?? SHOTS[SHOTS.length - 1];
export type Layer = { id: number; alpha: number; pre?: number };
export const layersAt = (f: number): Layer[] => {
  for (const s of SHOTS) {
    const x = XFADE[s.id];
    if (x && f >= s.a - x / 2 && f < s.a + x / 2) return [{ id: s.id - 1, alpha: 1 }, { id: s.id, alpha: (f - (s.a - x / 2) + 1) / (x + 1) }];
  }
  const id = shotAt(f).id;
  for (const k of CAMS_REF()[id] ?? []) if (k.cut && f >= k.f && f < k.f + CUT_X) return [{ id, alpha: 1, pre: k.f }, { id, alpha: (f - k.f + 1) / (CUT_X + 1) }];
  return [{ id, alpha: 1 }];
};
const CAMS_REF = () => CAMS;
/** in-shot camera cut -> dissolve: the cut key frame if old frame f is inside its dissolve window */
export const cutPre = (id: number, f: number, span = CUT_X): number | undefined => { for (const k of CAMS[id] ?? []) if (k.cut && f >= k.f && f < k.f + span) return k.f; return undefined; };

// ---------------- story state ----------------
/** bridge pieces along z (0 = z -30 end .. 8 = z +30 end): spans and piers alternate */
export const PIECES = 9;
export const BUILD_T = [35.9, 36.04, 36.2, 36.36, 36.55, 36.74, 36.96, 37.18, 37.44].map(W); // "went back together, piece by piece"
export type World = { pieces: [number, number]; sink: number; fill: number; water: number; front: number; lake: boolean };
/** what stands where at film time t in shot id. pieces = [first, last) visible; fill = sand floor height under the
 *  arches (desert); water = canal water height (-9 = none); front = x of the flood front (water only for x > front) */
export const worldAt = (id: number, t: number): World => {
  const w: World = { pieces: [0, PIECES], sink: 0, fill: 1.2, water: 0, front: -2000, lake: true };
  const place = SHOTS[id - 1].place;
  if (id === 3) w.sink = -0.35 * smooth((t - 13.1) / 1.9);
  if (id === 8) w.pieces = [0, 5];
  if (id === 11) w.pieces = [0, BUILD_T.filter((b) => t >= b - 0.02).length];
  if (place === "desert") {
    if (id <= 13 || id === 6) { w.water = -9; w.fill = 1.2; }
    if (id === 14) {
      w.fill = 1.2 - 1.75 * smooth((t - 46.5) / 3.6);
      const ft = (t - W(50.2)) / 0.75;
      w.water = ft < 0 ? -9 : -0.45 + 0.45 * smooth(ft * 0.8);
      w.front = 260 - 700 * clamp01(ft) ** 1.4;
    }
    if (id >= 15) { w.fill = -0.6; w.water = 0; }
  }
  return w;
};
export const BAG_T = W(27.1); // money bag lands on "million"
export const HITS = [W(17.72), W(18.52), W(18.98)]; // hammer blows: "put", "up", "sale"

export const SPANS: [number, number, number][] = [[-30, -19.2, 4.3], [-16.8, -7.2, 4.6], [-4.8, 4.8, 4.9], [7.2, 16.8, 4.6], [19.2, 30, 4.3]]; // z0, z1, crown y
export const pieceRange = (i: number): [number, number] => (i % 2 === 0 ? [SPANS[i / 2][0], SPANS[i / 2][1]] : [SPANS[(i - 1) / 2][1], SPANS[(i + 1) / 2][0]]);

// ---------------- camera ----------------
export type Cam = { pos: V3; look: V3; fov: number; roll: number };
type Shot = Partial<Cam> & { pos: V3; look: V3 };
type Key = { f: number; dur?: number; cut?: boolean; s: (f: number) => Shot };
export const glide = (u: number) => { const x = clamp01(u); return x * x * x * (x * (6 * x - 15) + 10); };
const mix = (a: Cam, b: Cam, k: number): Cam => ({
  pos: a.pos.map((v, i) => v + (b.pos[i] - v) * k) as V3, look: a.look.map((v, i) => v + (b.look[i] - v) * k) as V3,
  fov: a.fov + (b.fov - a.fov) * k, roll: a.roll + (b.roll - a.roll) * k,
});
const full = (c: Shot): Cam => ({ fov: 40, roll: 0, ...c });
let runStart = 0, runIdx = 0;
const run = (keys: Key[], f: number, pre?: number) => {
  let cur = full(keys[0].s(f));
  runStart = keys[0].f; runIdx = 0;
  for (let i = 1; i < keys.length; i++) {
    const k = keys[i];
    if (f < k.f || (pre !== undefined && k.f >= pre)) break;
    cur = k.cut ? full(k.s(f)) : mix(cur, full(k.s(f)), glide((f - k.f) / (k.dur ?? 24)));
    if (k.cut) { runStart = k.f; runIdx = i; }
  }
  return cur;
};
/** measured reference: lens 50-90 deg vertical (ours 38-42), real 3D orbit drift 5-15 px/f. Widen narrow lenses while
 *  moving the camera in so the subject keeps its size (stronger perspective), and orbit slowly around the look point. */
const WIDE_FOV = 54, ORBIT = 0.0021, ORBIT_MAX = 0.2; // rad/frame, rad
const widen = (c: Cam): Cam => {
  if (c.fov >= WIDE_FOV) return c;
  const k = Math.tan((c.fov * Math.PI) / 360) / Math.tan((WIDE_FOV * Math.PI) / 360);
  return { ...c, fov: WIDE_FOV, pos: c.look.map((v, i) => v + (c.pos[i] - v) * k) as V3 };
};
const orbit = (c: Cam, ang: number): Cam => {
  const dx = c.pos[0] - c.look[0], dz = c.pos[2] - c.look[2], cs = Math.cos(ang), sn = Math.sin(ang);
  return { ...c, pos: [c.look[0] + dx * cs - dz * sn, c.pos[1], c.look[2] + dx * sn + dz * cs] };
};
// measured reference: pushes run 0.7-1.2 %/frame (ours were 0.2-0.25 %/f) -> PUSH_GAIN, capped so long holds don't collapse
const PUSH_GAIN = 3.4, PUSH_MAX = 0.75;
const pushK = (f: number, f0: number, rate0: number, punch = 0, n = 35) => {
  const x = Math.max(0, f - f0), rate = rate0 * PUSH_GAIN;
  let s = Math.min(PUSH_MAX, rate * x);
  if (punch > rate) for (let i = 0; i < Math.min(x, n); i++) s += (punch - rate) * Math.max(0, Math.min(1, (i + 0.5) / 8, (n - i - 0.5) / 8));
  return Math.exp(-s);
};
const dolly = (pos: V3, look: V3, k: number, rest: Partial<Cam> = {}): Shot =>
  ({ pos: [look[0] + (pos[0] - look[0]) * k, look[1] + (pos[1] - look[1]) * k, look[2] + (pos[2] - look[2]) * k], look, ...rest });
const zoom = (pos: V3, look: V3, fov: number, k: number, rest: Partial<Cam> = {}): Shot =>
  ({ pos, look, fov: (360 / Math.PI) * Math.atan(Math.tan((fov * Math.PI) / 360) * k), ...rest });
const rolled = (s: (f: number) => Shot, roll: number) => (f: number): Shot => ({ ...s(f), roll });
const fw = (s: number) => Math.round(W(s) * FPS); // word time -> frame

// ---- places ----
export const MAC1: V3 = [14.0, D0, -37.0];     // McCulloch in front of the desert bridge (hook)
export const SIGN_AT: V3 = [2.25, D0, -30.9]; // FOR SALE sign at the bridge's near end
export const OFFICIAL: V3 = [3.35, D0, -31.55];
export const MAC5: V3 = [1.0, D0, -12.0];     // McCulloch on the London bridge
export const DEAL_O: V3 = [-0.8, D0, -14.5], DEAL_M: V3 = [0.8, D0, -14.5], BAG: V3 = [0, D0, -14.0];
export const PILE: V3 = [14, D0, -33.2];      // numbered stones on the near quay
export const ROAD_Z = -95;                    // desert road
export const truckX = (t: number, k: number) => -40 + 11 * (t - 33.8) - k * 16;
export const shipX = (t: number) => 2.4 * (t - 32.8);
export const FISHER: V3 = [3.0, 1.2, -0.6];   // under the middle arch, on the dry floor
export const FRAMER: V3 = [0.6, D0, -1.0];
export const MAC17: V3 = [0.8, D0, -8.0];
export const TOWN = { x: 150, z: -120 };      // new town by the lake (lake at x > 170)

const S1a = (f: number) => dolly([MAC1[0] + 2.4, D0 + 1.6, MAC1[2] - 6.0], [MAC1[0] - 2.2, D0 + 1.9, MAC1[2] + 4.0], pushK(f, 0, 0.0028), { fov: 40, roll: -0.03 });
const S1b = (f: number) => zoom([92, 15, -44], [0, 3.2, 0], 40, pushK(f, fw(2.38), 0.0022));
const S1c = (f: number) => dolly([95, 60, -95], [0, 0, 0], pushK(f, fw(4.9), 0.0015), { fov: 44 });
const S2a = (f: number) => zoom([46, 24, -64], [0, 4, 0], 42, pushK(f, 186, 0.002));
const S2b = (f: number) => dolly([34, 5.5, -22], [0, 3.2, 2], pushK(f, fw(8.3), 0.0025), { fov: 42 });
const S3a = (f: number) => dolly([17, D0 + 4.5, -22], [0, D0 + 1.0, -4], pushK(f, 310, 0.0025), { fov: 40 });
const S3b = (f: number) => dolly([21, 1.3, -14], [4.5, 1.8, -6], pushK(f, fw(13.06), 0.002, 0.005, 30), { fov: 40, roll: 0.035 });
const S4a = (f: number) => dolly([8.5, D0 + 2.1, -42.5], [2.4, D0 + 1.4, -32.5], pushK(f, 455, 0.0025), { fov: 42 });
const S4b = (f: number) => zoom([1.0, D0 + 1.6, -37.0], [2.8, D0 + 1.3, -31.4], 42, pushK(f, fw(17.54), 0.0025, 0.004, 24));
const S5a = (f: number) => dolly([MAC5[0] + 1.6, D0 + 1.85, MAC5[2] - 5.4], [MAC5[0], D0 + 1.5, MAC5[2]], pushK(f, 583, 0.0025), { fov: 38 });
const S5b = (f: number) => dolly([MAC5[0] + 0.6, D0 + 1.65, MAC5[2] - 3.4], [MAC5[0] + 0.1, D0 + 1.45, MAC5[2]], pushK(f, fw(21.6), 0.002, 0.006, 30), { fov: 36, roll: 0.04 });
// r3: aim past the town at the lake, so the sight-line culler keeps the houses and the whole planned grid is in frame
const S6a = (f: number) => dolly([TOWN.x - 72, 42, ROAD_Z + 62], [TOWN.x + 48, 0, ROAD_Z - 18], pushK(f, 697, 0.0022), { fov: 44 });
const S7a = (f: number) => dolly([0.3, D0 + 1.8, -21.8], [0, D0 + 1.25, -14.5], pushK(f, 760, 0.0025), { fov: 40 });
const S8a = (f: number) => zoom([30, D0 + 7, -52], [4, D0 - 1, -14], 42, pushK(f, 838, 0.002));
// r3: was a 4 m punch-in that filled the frame with the painter's body; now a medium shot of the painter and the numbered pallets
const S8b = (f: number) => dolly([PILE[0] + 3.2, D0 + 3.9, -25.2], [PILE[0] - 0.2, D0 + 0.6, PILE[2] + 0.4], pushK(f, fw(29.9), 0.0018), { fov: 46 });
const S9a = (f: number) => { const x = shipX(f / FPS); return dolly([x + 34, 17, -50], [x - 3, 2.5, 0], pushK(f, 958, 0.002), { fov: 42 }); };
const S10a = (f: number) => { const x = truckX(f / FPS, 0); return dolly([x + 9, D0 + 1.4, ROAD_Z - 9.5], [x - 4, D0 + 1.2, ROAD_Z], pushK(f, 1012, 0.002), { fov: 42, roll: -0.03 }); };
const S11a = (f: number) => zoom([44, 9, -16], [0, 3.4, 0], 44, pushK(f, 1070, 0.0025));
const S12a = (f: number) => dolly([9, D0 + 2.6, -33], [0.5, D0 + 1.8, -15.5], pushK(f, 1134, 0.0022), { fov: 42 });
const S12b = (f: number) => dolly([2.4, D0 + 1.75, -22.8], [0.3, D0 + 1.55, -16], pushK(f, fw(39.9), 0.0015, 0.005, 30), { fov: 40, roll: 0.035 });
const S13a = (f: number) => dolly([FISHER[0] + 12, 2.6, FISHER[2] - 1.0], [FISHER[0] - 0.5, 2.9, FISHER[2]], pushK(f, 1239, 0.002), { fov: 42 });
const S13b = (f: number) => dolly([FISHER[0] + 5.6, 2.25, FISHER[2] - 1.2], [FISHER[0], 2.35, FISHER[2]], pushK(f, fw(43.58), 0.002, 0.006, 30), { fov: 38, roll: 0.04 });
const S14a = (f: number) => dolly([17, 3.6, 2.5], [2, 1.0, 0], pushK(f, 1395, 0.0025), { fov: 42 });
const S14b = (f: number) => dolly([75, 34, -46], [0, -1, 0], pushK(f, fw(48.9), 0.0018), { fov: 44 });
const S15a = (f: number) => dolly([FRAMER[0] + 0.9, D0 + 1.65, FRAMER[2] - 4.6], [FRAMER[0], D0 + 1.5, FRAMER[2]], pushK(f, 1539, 0.0025), { fov: 38 });
const S15b = (f: number) => dolly([FRAMER[0] + 0.4, D0 + 1.6, FRAMER[2] - 3.3], [FRAMER[0], D0 + 1.5, FRAMER[2]], pushK(f, fw(52.4), 0.002), { fov: 36, roll: -0.035 });
const S16a = (f: number) => dolly([1.9, D0 + 1.8, -16], [0, D0 + 1.4, -8], pushK(f, 1626, 0.0025), { fov: 40 });
const S16b = (f: number) => dolly([22, 4.0, -30], [0, 3.0, 0], pushK(f, fw(56.2), 0.002), { fov: 42 });
const CRANE: V3[] = [[40, 30, -60], [110, 70, -120], [0, 0, 0]];
const S16c = (f: number): Shot => {
  const a = S16b(fw(58.2)), s = glide((f - fw(58.2)) / 45), r = 1 - s, [C, B, L] = CRANE;
  return { pos: [0, 1, 2].map((i) => r * r * a.pos[i] + 2 * s * r * C[i] + s * s * B[i]) as V3,
    look: [0, 1, 2].map((i) => a.look[i] + (L[i] - a.look[i]) * s) as V3, fov: (a.fov ?? 42) + (46 - (a.fov ?? 42)) * s, roll: 0 };
};
const S17a = (f: number) => dolly([MAC17[0] + 0.9, D0 + 2.0, MAC17[2] - 6.4], [MAC17[0] - 0.5, D0 + 2.0, MAC17[2]], pushK(f, 1797, 0.0022), { fov: 40 });
const S17b = (f: number) => dolly([MAC17[0] + 0.5, D0 + 1.8, MAC17[2] - 3.6], [MAC17[0], D0 + 1.75, MAC17[2]], pushK(f, fw(62.86), 0.002, 0.006, 30), { fov: 38, roll: -0.04 });

const CAMS: Record<number, Key[]> = {
  1: [{ f: 0, s: S1a }, { f: fw(2.38), cut: true, s: S1b }, { f: fw(4.9), dur: 40, s: S1c }],
  2: [{ f: 186, s: S2a }, { f: fw(8.3), dur: 36, s: S2b }],
  3: [{ f: 310, s: S3a }, { f: fw(13.06), cut: true, s: S3b }],
  4: [{ f: 455, s: S4a }, { f: fw(17.54), cut: true, s: S4b }],
  5: [{ f: 583, s: S5a }, { f: fw(21.6), dur: 22, s: S5b }],
  6: [{ f: 697, s: S6a }],
  7: [{ f: 760, s: S7a }],
  8: [{ f: 838, s: S8a }, { f: fw(29.9), cut: true, s: S8b }],
  9: [{ f: 958, s: S9a }],
  10: [{ f: 1012, s: S10a }],
  11: [{ f: 1070, s: S11a }],
  12: [{ f: 1134, s: S12a }, { f: fw(39.9), dur: 26, s: S12b }],
  13: [{ f: 1235, s: S13a }, { f: fw(43.58), cut: true, s: S13b }],
  14: [{ f: 1395, s: S14a }, { f: fw(48.9), cut: true, s: S14b }],
  15: [{ f: 1539, s: S15a }, { f: fw(52.4), dur: 24, s: S15b }],
  16: [{ f: 1626, s: S16a }, { f: fw(56.2), cut: true, s: S16b }, { f: fw(58.2), cut: true, s: S16c }],
  17: [{ f: 1797, s: S17a }, { f: fw(62.86), dur: 20, s: S17b }],
};

const KICKS: [number, number][] = [[BAG_T, 1.4], ...HITS.map((h) => [h, 0.5] as [number, number]), ...BUILD_T.map((b) => [b, 0.35] as [number, number]), [W(50.75), 0.8]];
export const kickAt = (t: number) => {
  let a = 0;
  for (const [t0, g] of KICKS) {
    const n = Math.floor((t - t0) * FPS + 1e-6);
    if (n >= 0 && n < 7) a += g * (n % 2 ? -1 : 1) * (1 - n / 7) ** 1.5;
  }
  return a;
};
export const camAt = (id: number, f: number, pre?: number): Cam => {
  const c0 = run(CAMS[id], f, pre), dir = (id + runIdx) % 2 ? 1 : -1, oa = dir * Math.min(ORBIT_MAX, ORBIT * Math.max(0, f - runStart));
  const c = orbit(widen(c0), NO_ORBIT.has(id) ? 0 : oa), a = kickAt(f / FPS);
  if (!a) return c;
  const d: V3 = [c.look[0] - c.pos[0], c.look[1] - c.pos[1], c.look[2] - c.pos[2]];
  const L = Math.hypot(...d), h = Math.hypot(d[0], d[2]) || 1;
  const m = (3 / 640) * Math.tan((c.fov * Math.PI) / 360) * L * a;
  return { ...c, look: [c.look[0] - (d[2] / h) * m, c.look[1] + 0.6 * m, c.look[2] + (d[0] / h) * m], roll: c.roll + a * 0.004 };
};

// ---------------- lens ----------------
export type Dof = { f: number; dur?: number; cInf: number; focus?: (f: number) => V3 };
const eyes = (p: V3, h = 1.6) => (): V3 => [p[0], p[1] + h, p[2]];
export const DOF: Dof[] = [
  { f: 0, cInf: 14, focus: eyes(MAC1) },
  { f: fw(2.38), cInf: 0 },
  { f: 310, cInf: 8 },                              // traffic MS
  { f: fw(13.06), cInf: 6 },                        // pier at the water
  { f: 455, cInf: 8, focus: () => [2.6, D0 + 1.6, -32.4] },
  { f: fw(17.54), cInf: 12, focus: eyes(OFFICIAL) },
  { f: 583, cInf: 12, focus: eyes(MAC5) },
  { f: 697, cInf: 0 },
  { f: 760, cInf: 11, focus: () => [0, D0 + 1.5, -14.5] },
  { f: 838, cInf: 0 },
  { f: fw(29.9), cInf: 13, focus: () => [PILE[0], D0 + 0.9, PILE[2]] },
  { f: 958, cInf: 0 },
  { f: 1138, cInf: 5 },
  { f: 1239, cInf: 12, focus: eyes(FISHER, 1.5) },
  { f: 1395, cInf: 6 },
  { f: fw(48.9), cInf: 0 },
  { f: 1539, cInf: 13, focus: eyes(FRAMER) },
  { f: 1626, cInf: 8 },
  { f: fw(56.2), cInf: 0 },
  { f: 1797, cInf: 13, focus: eyes(MAC17) },
];
export const dofAt = (f: number) => {
  let i = 0; while (i + 1 < DOF.length && f >= DOF[i + 1].f) i++;
  const d = DOF[i], p = DOF[Math.max(0, i - 1)];
  const k = d.dur ? Math.min(1, (f - d.f) / d.dur) : 1;
  return { cInf: p.cInf + (d.cInf - p.cInf) * k, focus: d.focus };
};
export const keyEnd = (id: number, f: number) => {
  let e = 0;
  for (const k of CAMS[id]) if (f >= k.f) e = k.f + (k.cut ? 0 : k.dur ?? 24);
  return Math.max(f, e);
};
export type Fg = { a: number; b: number; kit: string; pos: V3; s?: number; yaw?: number };
export const FOREGROUND: Fg[] = [];
export const fwPublic = fw;
export { rolled };
