// "Chicago lifted a hotel with the guests inside": original ~73 s short for Modern Vista Prints (Thu Nov 12 2026).
// Same engine and camera grammar as the Pisa short. The river town doubles as 1850s Chicago: the Chicago River along x,
// Lake Michigan east of x = 172, a muddy downtown grid on the far bank (Lake Street along x at z 96..108) with brick
// blocks that rise on jackscrews: the Tremont House, the 1858 building and the 1860 Lake Street block.
// Word times: chicago/voice/a.words.json (Drew, take a, tightened to 70.6 s).
export const FPS = 30;
export const VO_OFF = 0.2; // voice starts 0.2 s into the film
export const TOTAL = 2200;
export const D0 = 6.0; // ground level (m)
export const HW = 6.5;
export type V3 = [number, number, number];

export const clamp01 = (x: number) => Math.max(0, Math.min(1, x));
export const smooth = (x: number) => { const u = clamp01(x); return u * u * (3 - 2 * u); };
export const easeOut = (u: number) => 1 - (1 - clamp01(u)) ** 4;
export const W = (s: number) => s + VO_OFF; // word time -> film time
const F = (s: number) => Math.round(W(s) * FPS);
export const POSTER_AT = F(65.48); // "That's the river in our Chicago..." -> 2D poster end card

// ---------------- shots ----------------
export type Light = "day" | "golden";
export type Place = "london" | "desert" | "sea";
export type ShotDef = { id: number; a: number; b: number; light: Light; place: Place; sunAz?: number; sunEl?: number };
export const SHOTS: ShotDef[] = [
  { id: 1, a: 0, b: F(6.26), light: "day", place: "london", sunAz: 140 },          // hook: the Tremont House rises, a guest sips tea
  { id: 2, a: F(6.26), b: F(12.34), light: "day", place: "london" },   // built on a swamp / rain, mud, sewage
  { id: 3, a: F(12.34), b: F(15.3), light: "day", place: "london" },   // 1854 cholera, 6 %
  { id: 4, a: F(15.3), b: F(23.34), light: "day", place: "london" },   // sewers on top of the streets, the street rises
  { id: 5, a: F(23.34), b: F(29.04), light: "day", place: "london", sunAz: 140 },  // 1858: four-story brick building, 6 ft, 200 screws
  { id: 6, a: F(29.04), b: F(36.26), light: "day", place: "london", sunAz: 140 },  // 1860: Lake Street block, 600 men, shops open
  { id: 7, a: F(36.26), b: F(42.96), light: "day", place: "london", sunAz: 140 },  // the Tremont House / 500 men underneath
  { id: 8, a: F(42.96), b: F(48.96), light: "day", place: "london", sunAz: 140 },  // guests barely noticed / the steps get steeper
  { id: 9, a: F(48.96), b: F(52.52), light: "day", place: "london" },  // couch analogy
  { id: 10, a: F(52.52), b: F(57.38), light: "day", place: "london", sunAz: 140 }, // George Pullman / sleeping cars
  { id: 11, a: F(57.38), b: TOTAL, light: "golden", place: "london" }, // the river drains into the lake... then flows backwards
];
export const XFADE: Record<number, number> = {};
export const CUT_X = 8;
const NO_ORBIT = new Set<number>([7]);
export const FLASH_AT = F(6.26);
export const shotAt = (f: number) => SHOTS.find((s) => f >= s.a && f < s.b) ?? SHOTS[SHOTS.length - 1];
export type Layer = { id: number; alpha: number; pre?: number };
export const layersAt = (f: number): Layer[] => {
  const id = shotAt(f).id;
  for (const k of CAMS_REF()[id] ?? []) if (k.cut && f >= k.f && f < k.f + CUT_X) return [{ id, alpha: 1, pre: k.f }, { id, alpha: (f - k.f + 1) / (CUT_X + 1) }];
  return [{ id, alpha: 1 }];
};
const CAMS_REF = () => CAMS;
export const cutPre = (id: number, f: number, span = CUT_X): number | undefined => { for (const k of CAMS[id] ?? []) if (k.cut && f >= k.f && f < k.f + span) return k.f; return undefined; };

// ---------------- legacy story state (kept for the shared world code) ----------------
export const PIECES = 9;
export const BUILD_T: number[] = [];
export type World = { pieces: [number, number]; sink: number; fill: number; water: number; front: number; lake: boolean };
export const worldAt = (_id: number, _t: number): World => ({ pieces: [0, 0], sink: 0, fill: 1.2, water: 0, front: -2000, lake: true });
export const BAG_T = -10;
export const HITS: number[] = [];
export const SPANS: [number, number, number][] = [[-30, -19.2, 4.3], [-16.8, -7.2, 4.6], [-4.8, 4.8, 4.9], [7.2, 16.8, 4.6], [19.2, 30, 4.3]];
export const pieceRange = (i: number): [number, number] => (i % 2 === 0 ? [SPANS[i / 2][0], SPANS[i / 2][1]] : [SPANS[(i - 1) / 2][1], SPANS[(i + 1) / 2][0]]);
export const PILE: V3 = [9999, D0, 9999];
export const ROAD_Z = -95;
export const TOWN = { x: 150, z: -120 };
export const truckX = (_t: number, _k: number) => -9999;
export const shipX = (_t: number) => -9999;

// ---------------- the city (far bank) ----------------
export const SW = 0.15;                 // plank sidewalk height
export const LAKE_X = 172;              // Lake Michigan shore
export const LAKE_Z: [number, number] = [96, 108];  // Lake Street roadway
/** the Tremont House: front on the north sidewalk of Lake Street (faces -z), 30 x 20 m, six floors */
export const TRE = { x0: -15, x1: 15, z: 111, d: 20, h: 17.6 };
/** the 1858 building: south side of Lake Street (front faces +z at z 93), four floors */
export const B58 = { x0: 22, x1: 36, z: 93, d: 18, h: 12 };
/** the 1860 Lake Street block: north side between the streets at x -125 and -60 */
export const BLK = { x0: -117, x1: -68, z: 111, d: 20 };
/** the cross street where the sewer is laid and the street is raised (along z at x = 60) */
export const SEWER = { x: 60, z0: 151, z1: 197, r: 0.85 };
const FT = 0.3048;

/** how high each rising building sits above the street (m) */
export const STEP_H = 0.3;
export const DAYS = [W(46.36), W(47.52), W(48.24)]; // MON TUE WED: one more front step each day
export const lift = (which: "tre" | "b58" | "blk", id: number, t: number): number => {
  if (which === "tre") {
    if (id === 1) return 0.25 + (6 * FT - 0.25) * smooth((t - W(1.6)) / (W(4.4) - W(1.6)));
    if (id === 7) return 1.42 + 0.12 * clamp01((t - W(36.3)) / 6.6);
    if (id === 8) { const n = DAYS.filter((d) => t >= d - 2 / FPS).length; return STEP_H * (3 + n); }
    return 6 * FT;
  }
  if (which === "b58") return id === 5 ? 6 * FT * smooth((t - W(25.6)) / (W(27.2) - W(25.6))) : id > 5 ? 6 * FT : 0;
  return id === 6 ? 5 * FT * smooth((t - W(31.2)) / (W(32.3) - W(31.2))) : id > 6 ? 5 * FT : 0;
};
/** visible Tremont front steps: one per 0.3 m of lift */
export const stepsOf = (id: number, t: number) => Math.min(6, Math.round(lift("tre", id, t) / STEP_H));
/** the street fill over the sewer: top height above D0 (rises on "raise the whole city" -> "went up") */
export const fillTop = (id: number, t: number) => (id === 4 ? -0.3 + 2.25 * smooth((t - W(19.38)) / (W(21.9) - W(19.38))) : -0.3);
/** the sewer pipe drops in on "lay" */
export const pipeDrop = (id: number, t: number) => (id === 4 ? 1 - smooth((t - W(17.2)) / 0.45) : 1);
/** river flow: position of the texture along x (continuous), +x = into the lake, reverses on "flow backwards" */
export const FLIP_T = W(63.96);
export const flowPos = (t: number) => {
  const v = 2.2, ramp = 0.9; // m/s; velocity +v -> -v over the ramp
  if (t < FLIP_T) return v * t;
  const u = t - FLIP_T;
  return v * FLIP_T + (u < ramp ? v * u - (v * u * u) / ramp : -v * (u - ramp));
};
/** arrow heading on the river: 0 = +x (to the lake), PI = -x, spins on the flip */
export const arrowYaw = (t: number) => Math.PI * smooth((t - FLIP_T + 0.15) / 0.6);

// ---------------- r2 sets (sets.ts): interiors and the depot sit far from the city, south-west of the river ----------------
/** the Tremont dining room (S1c tea, S8a guests barely noticed); back wall (windows) at z1 */
export const DINE = { x: -560, z: -620, w: 12, d: 9, h: 3.8 };
/** a family parlour (S9 the couch analogy happens at home, not in the street) */
export const PARLOR = { x: -560, z: -700, w: 9, d: 7, h: 3.4 };
export const TAB_Y = D0 + 0.76; // dining table top
/** dining tables: [x, z] (round, r 0.55) */
export const TABLES: [number, number][] = [[-562.2, -617.4], [-560.4, -619.0], [-561.8, -621.4], [-557.4, -620.6]];
/** the railway depot (S10b): rails along x at z STA.z, platform on +z */
export const STA = { x: -560, z: -800 };
export const CAR = { x0: -569, x1: -551, z: -800, y: D0 + 1.05, h: 3.0 }; // Pullman sleeping car body (bottom y, height)
export const PLAT = { z0: -798.0, z1: -792.0, y: D0 + 0.95 };
/** river boats: lane z and phase (x = base + flow) */
export const BOATS: { z: number; x0: number; kind: "tug" | "barge" }[] = [{ z: 18, x0: 30, kind: "tug" }, { z: 22, x0: 62, kind: "barge" }, { z: 17.5, x0: 96, kind: "tug" }]; // beyond the far arrow lane (|z| 5-13): boats never cover the flow arrows
export const boatX = (i: number, t: number) => BOATS[i].x0 + 0.55 * flowPos(t);

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
const WIDE_FOV = 54, ORBIT = 0.0021, ORBIT_MAX = 0.2;
const widen = (c: Cam): Cam => {
  if (c.fov >= WIDE_FOV) return c;
  const k = Math.tan((c.fov * Math.PI) / 360) / Math.tan((WIDE_FOV * Math.PI) / 360);
  return { ...c, fov: WIDE_FOV, pos: c.look.map((v, i) => v + (c.pos[i] - v) * k) as V3 };
};
const orbit = (c: Cam, ang: number): Cam => {
  const dx = c.pos[0] - c.look[0], dz = c.pos[2] - c.look[2], cs = Math.cos(ang), sn = Math.sin(ang);
  return { ...c, pos: [c.look[0] + dx * cs - dz * sn, c.pos[1], c.look[2] + dx * sn + dz * cs] };
};
const PUSH_GAIN = 3.4, PUSH_MAX = 0.75;
const pushK = (f: number, f0: number, rate0: number, punch = 0, n = 35) => {
  const x = Math.max(0, f - f0), rate = rate0 * PUSH_GAIN;
  let s = Math.min(PUSH_MAX, rate * x);
  if (punch > rate) for (let i = 0; i < Math.min(x, n); i++) s += (punch - rate) * Math.max(0, Math.min(1, (i + 0.5) / 8, (n - i - 0.5) / 8));
  return Math.exp(-s);
};
const dolly = (pos: V3, look: V3, k: number, rest: Partial<Cam> = {}): Shot =>
  ({ pos: [look[0] + (pos[0] - look[0]) * k, look[1] + (pos[1] - look[1]) * k, look[2] + (pos[2] - look[2]) * k], look, ...rest });
const rolled = (s: (f: number) => Shot, roll: number) => (f: number): Shot => ({ ...s(f), roll });
const fw = (s: number) => Math.round(W(s) * FPS);
/** camera at pos looking toward far, but with a NEAR look point (a push then closes in on the foreground, never flies past it) */
const aim = (pos: V3, far: V3, dist: number, pitchDeg = 0): V3 => {
  const dx = far[0] - pos[0], dz = far[2] - pos[2], h = Math.hypot(dx, dz) || 1, p = (pitchDeg * Math.PI) / 180;
  return [pos[0] + (dx / h) * dist * Math.cos(p), pos[1] - dist * Math.sin(p), pos[2] + (dz / h) * dist * Math.cos(p)];
};

// ---- places (characters stand here) ----
const Y = D0 + SW; // sidewalk top
const winX = (i: number) => TRE.x0 + ((i + 0.5) * (TRE.x1 - TRE.x0)) / 13; // Tremont front windows (13 per floor)
/** a window on the Tremont front: [x, y centre of the glass, z] for floor fl (0 = street floor) */
export const treWin = (i: number, fl: number, id: number, t: number): V3 => [winX(i), D0 + lift("tre", id, t) + fl * 2.8 + 0.9 + 0.625, TRE.z - 0.03];
export const ONLOOK: V3 = [-11.4, D0, 104.0];           // S1 onlookers on the south sidewalk
export const STUCK: V3 = [33.8, D0 - 0.18, 102.0];     // S2 the townsman stuck in the mud (feet sunk)
export const DOC: V3 = [40, Y, 109.7];              // S3 the doctor on the north sidewalk
export const ENG: V3 = [63.4, D0, 160];             // S4 the engineer with the plan (on the cross street)
export const CREW58: V3 = [29, D0, 92.4];           // S5 crew at the 1858 building's front
export const SHOP: V3 = [-92.5, D0, 109.4];          // S6 the shop door in the Lake Street block (porch at the block's base)
export const GUEST: V3 = [0.1, Y, 108.25];          // S8 the guest at the foot of the Tremont steps
export const COUCH: V3 = [-560, D0, -700 + 3.5 - 1.0]; // S9 the couch against the parlour back wall
export const PULL: V3 = [8.2, Y, 108.7];            // S10 young George Pullman in front of the Tremont
export const TEA: V3 = [TABLES[0][0], D0, TABLES[0][1] + 0.85];   // S1c the guest sipping tea at the window table
export const PULL2: V3 = [STA.x + 5.8, PLAT.y, PLAT.z0 + 1.6];   // S10b Pullman on the depot platform

const S1a = (f: number) => dolly([-21, D0 + 1.3, 96.2], [-3, D0 + 9.0, 111], pushK(f, 0, 0.0004), { fov: 74, roll: -0.03 });
const S1b = (f: number) => dolly([TEA[0] + 0.7, D0 + 1.3, TEA[2] - 3.9], [TEA[0] - 0.05, D0 + 1.05, TEA[2]], pushK(f, fw(4.68), 0.0012), { fov: 56 });
const S2a = (f: number) => dolly([-125, D0 + 36, 12], [40, D0 - 4, 100], pushK(f, F(6.26), 0.0011), { fov: 58, roll: 0.02 });
const S2b = (f: number) => dolly([41, D0 + 1.75, 100.5], [23, D0 + 1.4, 103.5], pushK(f, fw(9.22), 0.0016, 0.005, 22), { fov: 56 });
const S3a = (f: number) => dolly([DOC[0] + 0.5, D0 + 1.7, DOC[2] - 5.6], [DOC[0] + 0.2, D0 + 1.45, DOC[2]], pushK(f, F(12.34), 0.0018), { fov: 56, roll: 0.03 });
const S4a = (f: number) => dolly([ENG[0] - 1.4, D0 + 1.6, ENG[2] - 5.4], [ENG[0] - 0.2, D0 + 1.35, ENG[2]], pushK(f, F(15.3), 0.0018), { fov: 56 });
const S4b = (f: number) => dolly([SEWER.x + 6.5, D0 + 7.0, 140], [SEWER.x - 0.5, D0 + 0.4, 176], pushK(f, fw(17.16), 0.0012), { fov: 58, roll: -0.02 });
const S5a = (f: number) => dolly([45, D0 + 1.7, 109.6], [29, D0 + 6.4, 93], pushK(f, F(23.34), 0.0005), { fov: 58, roll: 0.02 });
const S5b = (f: number) => dolly([B58.x1 + 4.5, D0 + 0.5, B58.z + 6.5], [B58.x1 - 5, D0 + 6.2, B58.z - 1], pushK(f, fw(26.5), 0.0007), { fov: 62, roll: -0.04 });
const S6a = (f: number) => dolly([-58, D0 + 2.0, 91.5], [-92.5, D0 + 6.2, 112], pushK(f, F(29.04), 0.0004), { fov: 58 });
const S6c = (f: number) => dolly([-104.5, D0 + 1.0, 106.4], [-90, D0 + 0.85, 109.2], pushK(f, fw(32.83), 0.001), { fov: 56, roll: 0.03 });
const S6b = (f: number) => dolly([SHOP[0] + 3.4, D0 + 2.3, SHOP[2] - 6.6], [SHOP[0] + 0.4, D0 + 2.0, SHOP[2]], pushK(f, fw(34.98), 0.0016), { fov: 56, roll: -0.03 });
const S7a = (f: number) => dolly([22, D0 + 10.5, 100.5], [2, D0 + 5.2, 110], pushK(f, F(36.26), 0.0003), { fov: 62, roll: 0.02 });
const S7b = (f: number) => dolly([18.5, D0 + 0.75, 117.5], [2, D0 + 0.55, 116.2], pushK(f, fw(39.54), 0.0012), { fov: 58 });
const S8a = (f: number) => dolly([-555.2, D0 + 1.9, -624.0], [-561, D0 + 0.9, -618.5], pushK(f, F(42.96), 0.0008), { fov: 58 });
const S8b = (f: number) => dolly([-4.6, D0 + 1.3, 103.6], [0.3, D0 + 1.25, 109.4], pushK(f, fw(44.9), 0.0012), { fov: 56, roll: -0.02 });
const S9a = (f: number) => dolly([COUCH[0] + 0.3, D0 + 1.45, COUCH[2] - 6.4], [COUCH[0] + 0.0, D0 + 1.0, COUCH[2]], pushK(f, F(48.96), 0.0012), { fov: 62 });
const S10a = (f: number) => dolly([PULL[0] + 1.1, D0 + 1.7, PULL[2] - 5.0], [PULL[0] + 0.25, D0 + 1.5, PULL[2]], pushK(f, F(52.52), 0.0016), { fov: 56, roll: -0.02 });
const S10b = (f: number) => dolly([-548.5, PLAT.y + 1.65, -792.6], [-558.5, PLAT.y + 1.25, -798.6], pushK(f, fw(55.4), 0.0008), { fov: 58, roll: 0.02 });
const S11a = (f: number) => dolly([-60, D0 + 60, -100], [150, D0 - 4, 10], pushK(f, F(57.38), 0.0010), { fov: 58 });
const S11b = (f: number) => dolly([86, D0 + 5, -27], [125, D0 - 4, 6], pushK(f, fw(60.5), 0.0004), { fov: 58, roll: 0.02 });

const CAMS: Record<number, Key[]> = {
  1: [{ f: 0, s: S1a }, { f: fw(4.68), cut: true, s: S1b }],
  2: [{ f: F(6.26), s: S2a }, { f: fw(9.22), cut: true, s: S2b }],
  3: [{ f: F(12.34), s: S3a }],
  4: [{ f: F(15.3), s: S4a }, { f: fw(17.16), cut: true, s: S4b }],
  5: [{ f: F(23.34), s: S5a }, { f: fw(26.5), cut: true, s: S5b }],
  6: [{ f: F(29.04), s: S6a }, { f: fw(32.83), cut: true, s: S6c }, { f: fw(34.98), cut: true, s: S6b }],
  7: [{ f: F(36.26), s: S7a }, { f: fw(39.54), cut: true, s: S7b }],
  8: [{ f: F(42.96), s: S8a }, { f: fw(44.9), cut: true, s: S8b }],
  9: [{ f: F(48.96), s: S9a }],
  10: [{ f: F(52.52), s: S10a }, { f: fw(55.4), cut: true, s: S10b }],
  11: [{ f: F(57.38), s: S11a }, { f: fw(60.5), cut: true, s: S11b }],
};

const KICKS: [number, number][] = [[W(17.3), 0.6], ...DAYS.map((d) => [d, 0.4] as [number, number]), [FLIP_T, 0.7], [W(32.2), 0.4], [W(27.1), 0.35]];
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
/** true for the high aerials: the sight-line culler must ignore them (it would empty the city) */
export const isAerial = (id: number, f: number) => camAt(id, f).pos[1] > D0 + 12;

// ---------------- lens ----------------
export type Dof = { f: number; dur?: number; cInf: number; focus?: (f: number) => V3 };
const eyes = (p: V3, h = 1.5) => (): V3 => [p[0], p[1] + h, p[2]];
export const DOF: Dof[] = [
  { f: 0, cInf: 0 },
  { f: fw(4.68), cInf: 11, focus: () => [TEA[0], D0 + 1.1, TEA[2]] },
  { f: F(6.26), cInf: 0 },
  { f: fw(9.22), cInf: 6, focus: eyes(STUCK, 1.4) },
  { f: F(12.34), cInf: 12, focus: eyes(DOC) },
  { f: F(15.3), cInf: 11, focus: eyes(ENG) },
  { f: fw(17.16), cInf: 0 },
  { f: F(23.34), cInf: 0 },
  { f: F(29.04), cInf: 0 },
  { f: fw(32.83), cInf: 6, focus: () => [-92, D0 + 0.7, 108.8] },
  { f: fw(34.98), cInf: 9, focus: () => [SHOP[0], D0 + 1.5 + 2.0, SHOP[2]] },
  { f: F(36.26), cInf: 0 },
  { f: fw(39.54), cInf: 4, focus: () => [9.3, D0 + 0.5, 117] },
  { f: F(42.96), cInf: 6, focus: () => [TABLES[1][0], D0 + 1.0, TABLES[1][1]] },
  { f: fw(44.9), cInf: 8, focus: eyes(GUEST) },
  { f: F(48.96), cInf: 12, focus: () => [COUCH[0], D0 + 1.1, COUCH[2]] },
  { f: F(52.52), cInf: 12, focus: eyes(PULL) },
  { f: fw(55.4), cInf: 7, focus: eyes(PULL2) },
  { f: F(57.38), cInf: 0 },
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
// legacy exports the shared files still import (Pisa tower): unused here
export const TOWER: V3 = [0, -999, 0];
export const TIER_H: number[] = [];
export const T_R = 1;
export const towerPose = (_id: number, _t: number) => ({ tiers: 0, lean: 0, kink: 0 });
