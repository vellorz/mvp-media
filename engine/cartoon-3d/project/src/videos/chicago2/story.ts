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
/** teardown gag timing: hold, a small anticipation dip, a fast move that overshoots, then a damped settle.
 *  u = 0..1 is the move; the settle runs on to u ~1.4 */
export const gag = (u: number) => {
  if (u <= 0) return 0;
  if (u < 0.1) return -0.06 * Math.sin((Math.PI * u) / 0.1);
  if (u < 1) { const x = (u - 0.1) / 0.9, c = 2.2; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2; }
  return 1 - 0.035 * Math.sin((u - 1) * 21) * Math.exp(-(u - 1) * 9);
};
/** a quick pop (steps, clods): 0 -> 1 over d seconds with overshoot and settle */
export const pop = (t: number, t0: number, d = 0.22) => gag((t - t0) / d);
const F = (s: number) => Math.round(W(s) * FPS);
export const POSTER_AT = F(65.48); // "That's the river in our Chicago..." -> 2D poster end card

// ---------------- shots ----------------
export type Light = "day" | "golden";
export type Place = "london" | "desert" | "sea";
export type ShotDef = { id: number; a: number; b: number; light: Light; place: Place; sunAz?: number; sunEl?: number };
// v2 (Nov 11 redesign, DETAIL_STANDARD G/H): 16 takes joined by bridged dissolves (remap DISSOLVE), no hard cuts, no flash.
const B = [0, 146, 197, 286, 373, 468, 580, 709, 880, 1097, 1298, 1355, 1478, 1585, 1730, 1823, TOTAL];
const LT: Light[] = ["day", "day", "day", "day", "golden", "day", "day", "day", "day", "day", "day", "day", "day", "day", "golden", "golden"];
const AZ: (number | undefined)[] = [140, undefined, undefined, undefined, undefined, undefined, undefined, 140, 140, 140, undefined, 140, undefined, 140, undefined, undefined];
export const SHOTS: ShotDef[] = LT.map((light, i) => ({ id: i + 1, a: B[i], b: B[i + 1], light, place: "london", sunAz: AZ[i] }));
// 1 hook: Tremont rises (crane up the facade)    2 tea at the window table       3 swamp            4 rain, mud, sewage
// 5 cholera (newspaper insert, dusk)             6 council: the plan             7 cross-section model on the council table
// 8 1858 building                                 9 1860 Lake Street block        10 Tremont House + 500 men under it
// 11 dining room, guests barely noticed           12 front steps, day after day   13 couch analogy (parlour)
// 14 George Pullman -> his sleeping car            15 sewage into the lake it drank from    16 1900: the river flows backwards
export const XFADE: Record<number, number> = {};
export const CUT_X = 9;
const NO_ORBIT = new Set<number>([]); // teardown: constant motion, every take drifts
/** v8: tight framings get a small orbit cap instead of none (steps, couch wide) so they still drift */
const ORB_CAP: Record<number, number> = { 12: 0.12, 13: 0.1 };
export const FLASH_AT = -100;
export const shotAt = (f: number) => SHOTS.find((s) => f >= s.a && f < s.b) ?? SHOTS[SHOTS.length - 1];
export type Layer = { id: number; alpha: number; pre?: number };
export const layersAt = (f: number): Layer[] => {
  const id = shotAt(f).id;
  for (const k of CAMS_REF()[id] ?? []) if (k.cut && f >= k.f && f < k.f + CUT_X) return [{ id, alpha: 1, pre: k.f }, { id, alpha: (f - k.f + 1) / (CUT_X + 1) }];
  return [{ id, alpha: 1 }];
};
const CAMS_REF = () => CAMS;
/** frames where take `id` hard-cuts (rule 64 decides sign lettering once per cut-to-cut shot) */
export const cutsOf = (id: number): number[] => (CAMS[id] ?? []).filter((k) => k.cut).map((k) => k.f);
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
export const DAYS = [W(46.36), W(47.52), W(48.24)]; // one more front step each day
/** v2 take ids: Tremont rises in take 1, sits raised after; 1858 building rises in take 8; Lake Street block in take 9 */
export const lift = (which: "tre" | "b58" | "blk", id: number, t: number): number => {
  if (which === "tre") {
    if (id === 1) return 0.25 + (6 * FT - 0.25) * gag((t - W(1.6)) / (W(4.4) - W(1.6)));
    if (id === 10) return 1.42 + 0.12 * clamp01((t - W(36.3)) / 6.6);
    if (id === 12) return STEP_H * (3 + DAYS.reduce((a, d) => a + pop(t, d), 0));
    return 6 * FT;
  }
  if (which === "b58") return id === 8 ? 6 * FT * gag((t - W(25.6)) / (W(27.2) - W(25.6))) : id > 8 ? 6 * FT : 0;
  return id === 9 ? 5 * FT * gag((t - W(31.2)) / (W(32.3) - W(31.2))) : id > 9 ? 5 * FT : 0;
};
/** visible Tremont front steps: one per 0.3 m of lift */
export const stepsOf = (id: number, t: number) => Math.min(6, Math.max(0, Math.round(lift("tre", id, t) / STEP_H)));
/** v2: the street fill and the sewer pipe are shown on the council-table model (take 7), not in the street */
export const fillTop = (_id: number, _t: number) => -0.3;
export const pipeDrop = (_id: number, _t: number) => 1;
/** the model on the council table: fill level 0..1 ("raise the whole city"), buildings 0..1 ("buildings had to follow") */
export const modelFill = (t: number) => Math.max(0, gag((t - W(19.3)) / (W(22.0) - W(19.3))));
export const modelLift = (t: number) => gag((t - W(22.1)) / (W(23.2) - W(22.1)));
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
    cur = k.cut ? full(k.s(f)) : mix(cur, full(k.s(f)), glide((f - k.f) / ((k.dur ?? 24) * DURX)));
    if (k.cut) { runStart = k.f; runIdx = i; }
  }
  return cur;
};
const WIDE_FOV = 54, ORBIT = 0.011, ORBIT_MAX = 0.6;
/** v3 motion pass (estimator /home/user/work/mot/est.mjs): long, even glides instead of fast lunges */
const DURX = 1.6;
const widen = (c: Cam): Cam => {
  if (c.fov >= WIDE_FOV) return c;
  const k = Math.tan((c.fov * Math.PI) / 360) / Math.tan((WIDE_FOV * Math.PI) / 360);
  return { ...c, fov: WIDE_FOV, pos: c.look.map((v, i) => v + (c.pos[i] - v) * k) as V3 };
};
const orbit = (c: Cam, ang: number): Cam => {
  const dx = c.pos[0] - c.look[0], dz = c.pos[2] - c.look[2], cs = Math.cos(ang), sn = Math.sin(ang);
  return { ...c, pos: [c.look[0] + dx * cs - dz * sn, c.pos[1], c.look[2] + dx * sn + dz * cs] };
};
const PUSH_GAIN = 7, PUSH_MAX = 0.5; // v5: cap the push so framing (hats, the model) survives
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
export const ONLOOK: V3 = [-11.4, D0, 104.0];
export const STUCK: V3 = [33.8, D0 - 0.34, 102.0]; // v6: sunk to the shins with the shorter legs
export const DOC: V3 = [40, Y, 109.7];
export const ENG: V3 = [63.4, D0, 160];
export const CREW58: V3 = [29, D0, 92.4];
export const SHOP: V3 = [-92.5, D0, 109.4];
export const GUEST: V3 = [-1.75, Y, 108.7]; // v6: beside the foot of the steps, so the steps stay in view
export const COUCH: V3 = [-560, D0, -700 + 3.5 - 1.0];
export const PULL: V3 = [8.2, Y, 108.7];
export const TEA: V3 = [TABLES[0][0], D0, TABLES[0][1] + 0.85];
export const PULL2: V3 = [STA.x + 5.8, PLAT.y, PLAT.z0 + 1.6];
/** v2 sets */
export const SWAMP = { x: -560, z: -900 };                       // take 3: marsh, plank shacks, the lake just below
export const COUNCIL = { x: -560, z: -980, w: 9, d: 7, h: 3.6 };  // takes 6-7: council room
export const CTAB: V3 = [COUNCIL.x, D0 + 0.76, COUNCIL.z];        // council table centre (top)
export const MODEL: V3 = [COUNCIL.x, D0 + 0.76, COUNCIL.z + 0.45]; // cross-section model standing on the table (faces -z)
export const NEWS: V3 = [42.3, Y + 1.45, 110.94]; // v17 (rule 64): moved 0.7 m so it stays fully out of the doctor shot (was cut at the left edge)                 // take 5: newspaper pasted on the north-row wall
export const PAPER: V3 = [33.6, D0 + 0.13, 99.2];                 // take 4: a soggy newspaper in the mud (bridge to take 5)
export const SHORE: V3 = [160, D0, 40];                           // take 15: man drinking lake water at the shore

/** teardown head sizes: move the camera along its line to the look point to k of the distance (medium 33-40 %, close 56-64 %) */
const nr = (pos: V3, at: V3, k: number): V3 => [at[0] + (pos[0] - at[0]) * k, at[1] + (pos[1] - at[1]) * k, at[2] + (pos[2] - at[2]) * k];
/** v3 body types (2.9 head-heights): faces sit ~0.26 m lower than the old 3.5 HH cast, so every eye-level camera
 *  (look point 1.1-1.9 m above the ground) drops with them */
const EYE_DROP = 0.24;
const eyeFix = (v: V3, ref: number): V3 => { const h = ref - D0; return h > 1.1 && h < 1.9 ? [v[0], v[1] - EYE_DROP, v[2]] : v; };
const look = (pos: V3, at: V3, fov: number, f0: number, rate = 0.0010, roll = 0) => {
  const p2 = eyeFix(pos, at[1]), a2 = eyeFix(at, at[1]);
  return (f: number): Shot => dolly(p2, a2, pushK(f, f0, rate), { fov, roll });
};
const [TX, , TZ] = TEA, [CX, CY, CZ] = CTAB;
const CAMS: Record<number, Key[]> = {
  1: [ // cold open in motion: low at the jackscrews, crane up the rising facade to a first-floor window
    { f: 0, s: look([-8.6, D0 + 0.55, 106.4], [-6.0, D0 + 0.95, 111], 52, 0, 0.0012, -0.04) },
    { f: 18, dur: 88, s: look([-7.4, D0 + 1.5, 101.2], [-4.0, D0 + 2.9, 111], 56, 18, 0.0006, 0.02) }, // v3: further back, slower crane (QA motion 24 at 30-60 px/f)
    { f: 106, cut: true, s: look([0.25, D0 + 6.3, 106.6], [0.0, D0 + 6.15, 111], 42, 92, 0.0012) },
  ],
  2: [ // through the window: the guest keeps sipping; push into the teacup
    { f: 136, s: look([TX + 0.55, D0 + 1.2, TZ - 2.25], [TX, D0 + 1.05, TZ], 46, 136, 0.0010) },
    { f: 168, dur: 30, s: look([TX + 0.32, D0 + 1.12, TZ - 1.35], [TX + 0.1, D0 + 1.0, TZ], 42, 168, 0.0012) },
  ],
  3: [ // swamp: top-down on a puddle, crane up and back to the shacks with the lake just below them
    { f: 190, s: look([SWAMP.x - 0.5, D0 + 0.38, SWAMP.z - 1.7], [SWAMP.x + 0.6, D0 + 0.22, SWAMP.z + 0.3], 44, 190, 0.0012) },
    { f: 220, dur: 90, s: look([SWAMP.x + 0.6, D0 + 2.4, SWAMP.z - 7.5], [SWAMP.x, D0 + 1.0, SWAMP.z + 8], 56, 202, 0.0007, 0.02) },
  ],
  4: [ // rain: low over a street puddle, rise to the man stuck in the mud, pan down to the gutter and the soggy paper
    { f: 278, s: look([32.0, D0 + 0.5, 99.4], [32.6, D0 - 0.1, 101.3], 50, 278, 0.0) },
    { f: 288, cut: true, s: look(nr([36.8, D0 + 1.5, 98.9], [33.8, D0 + 1.25, 102], 0.66), [33.8, D0 + 1.25, 102], 48, 288, 0.0012, 0.02) },
    { f: 336, cut: true, s: look([32.6, D0 + 1.0, 97.4], [PAPER[0], D0 + 0.05, PAPER[2]], 46, 336, 0.0010) },
  ],
  5: [ // 1854: the newspaper on the wall, pull back to the doctor in the dusk street
    { f: 365, s: look([NEWS[0] + 0.1, NEWS[1] + 0.05, NEWS[2] - 1.45], NEWS, 40, 365, 0.0008) },
    { f: 384, cut: true, s: look(nr([41.6, D0 + 1.75, 104.6], [40.1, D0 + 1.4, 109.7], 0.6), [40.1, D0 + 1.4, 109.7], 48, 384, 0.0012, -0.02) },
  ],
  6: [ // the council: the plan on the table, pull back to the engineer and the council; push to the covered model
    { f: 460, s: look([CX, CY + 0.72, CZ - 0.37], [CX, CY, CZ - 0.35], 46, 460, 0.0) },
    { f: 478, cut: true, s: look(nr([CX + 1.1, D0 + 2.1, CZ - 3.4], [CX, D0 + 1.1, CZ + 0.3], 0.8), [CX, D0 + 1.1, CZ + 0.3], 54, 478, 0.0008) },
    { f: 548, dur: 32, s: look([CX + 0.2, CY + 0.5, CZ - 2.15], [CX, CY + 0.38, MODEL[2]], 50, 548, 0.0008) },
  ],
  7: [ // the model: fill rises, buildings follow; pull back so the council leans over it
    { f: 572, s: look([CX + 0.2, CY + 0.5, CZ - 2.15], [CX, CY + 0.38, MODEL[2]], 50, 572, 0.0008) },
    { f: 676, dur: 44, s: look(nr([CX + 1.3, D0 + 1.85, CZ - 3.0], [CX + 0.35, D0 + 1.2, CZ + 0.4], 0.92), [CX + 0.35, D0 + 1.2, CZ + 0.4], 54, 676, 0.0006) },
  ],
  8: [ // 1858: the whole building, down to the screws as it rises, up to the flowerpot that never wobbles
    { f: 701, s: look([29, D0 + 5.0, 118], [29, D0 + 6.0, 93], 52, 701, 0.0008) },
    { f: 752, cut: true, s: look([28.0, D0 + 0.6, 96.6], [27.85, D0 + 1.0, 93.1], 54, 752, 0.0008, -0.03) },
    { f: 836, cut: true, s: look([29, D0 + 5.6, 97.2], [29, D0 + 5.5, 93], 44, 836, 0.0012) },
  ],
  9: [ // 1860: the shop window, a surging pull-back as the block rises; along the row of men; the shop still selling
    { f: 872, s: look([-92.5, D0 + 1.25, 103.6], [-92.5, D0 + 1.05, 111], 46, 872, 0.0006) },
    { f: 902, dur: 64, s: look([-62, D0 + 4.5, 92], [-92, D0 + 4.0, 111], 56, 902, 0.0005, 0.02) },
    { f: 985, cut: true, s: (f) => look([-114 + 0.09 * (f - 985), D0 + 1.7, 106.4], [-104 + 0.09 * (f - 985), D0 + 0.05, 109.6], 42, 985, 0.0)(f) }, // v8 (rule 64): looks down on the men so the shop names stay above the frame instead of being cut by its edges
    { f: 1052, cut: true, s: look(nr([SHOP[0] + 3.0 + (-0.35), D0 + 2.3, SHOP[2] - 6.6], [SHOP[0] + (-0.35), D0 + 2.0, SHOP[2]], 0.48), [SHOP[0] + (-0.35), D0 + 2.0, SHOP[2]], 50, 1052, 0.0003, -0.03) }, // v17 (rule 64): reframed and a gentler push so the OPEN sign stays whole
  ],
  10: [ // the Tremont: grand wide, down to street level, under the building among 500 men, push to one screw
    { f: 1089, s: look([22, D0 + 10.5, 100.5], [2, D0 + 5.2, 110], 60, 1089, 0.0004, 0.02) },
    { f: 1150, cut: true, s: look([7, D0 + 1.4, 104.2], [2.5, D0 + 1.0, 113], 56, 1150, 0.0006) },
    { f: 1196, cut: true, s: look([18.5, D0 + 0.8, 115.5], [2, D0 + 0.6, 115.5], 56, 1196, 0.0012) },
    { f: 1250, cut: true, s: look([8.4, D0 + 0.62, 116.4], [6.9, D0 + 0.5, 117.0], 46, 1250, 0.0012) },
  ],
  11: [{ f: 1290, s: look(nr([-555.2, D0 + 2.5, -624.0], [-561, D0 + 0.9, -618.5], 0.78), [-561, D0 + 0.9, -618.5], 56, 1290, 0.0008) },
    { f: 1326, cut: true, s: look([-559.0, D0 + 1.3, -621.0], [-560.6, D0 + 0.95, -619.0], 44, 1326, 0.0016) }],
  12: [{ f: 1347, s: look([-3.9, D0 + 1.25, 104.9], [-0.5, D0 + 0.95, 109.7], 52, 1347, 0.0008, -0.02) },
    { f: 1444, cut: true, s: look([1.55, D0 + 2.05, 108.0], [1.4, D0 + 1.7, 110.65], 40, 1444, 0.0008) }],
  13: [{ f: 1470, s: (f) => look(nr([COUCH[0] + 0.3, D0 + 1.9 + 0.018 * Math.max(0, f - 1470), COUCH[2] - 6.0], [COUCH[0], D0 + 0.85, COUCH[2]], 1.25), [COUCH[0], D0 + 0.85, COUCH[2]], 58, 1470, 0.0004)(f) }], // v8: slow crane up keeps the couch drifting without cropping the jack men
  14: [
    { f: 1577, s: look(nr([PULL[0] + 1.1, D0 + 1.75, PULL[2] - 4.6], [PULL[0] + 0.25, D0 + 1.05, PULL[2]], 0.64), [PULL[0] + 0.25, D0 + 1.05, PULL[2]], 52, 1577, 0.0012, -0.02) },
    { f: 1620, dur: 24, s: look([PULL[0] + 0.45, D0 + 1.45, PULL[2] - 1.4], [PULL[0] + 0.2, D0 + 1.25, PULL[2]], 44, 1620, 0.0012) },
    { f: 1650, cut: true, s: look(nr([-548.5, PLAT.y + 1.65, -792.6], [-554.6, PLAT.y + 1.4, -796.4], 0.55), [-554.6, PLAT.y + 1.4, -796.4], 56, 1650, 0.0010, 0.02) },
  ],
  15: [
    { f: 1722, s: look([-60, D0 + 60, -100], [150, D0 - 4, 10], 58, 1722, 0.0012) },
    { f: 1782, cut: true, s: look(nr([SHORE[0] - 2.6, D0 + 1.6, SHORE[2] - 3.4], [SHORE[0], D0 + 1.4, SHORE[2]], 0.63), [SHORE[0], D0 + 1.4, SHORE[2]], 50, 1782, 0.0016) },
  ],
  16: [
    { f: 1815, s: look([150, D0 + 4, -16], [90, D0 + 1, 10], 58, 1815, 0.0012, 0.02) }, // v8: look back up the river at the city (the lake view was empty water)
    { f: 1858, dur: 60, s: look([168, D0 + 16, -34], [80, D0 + 1, 12], 58, 1858, 0.0004) },
  ],
};

const KICKS: [number, number][] = [...DAYS.map((d) => [d, 0.35] as [number, number]), [FLIP_T, 0.6], [W(32.2), 0.35], [W(27.1), 0.3]];
export const kickAt = (t: number) => {
  let a = 0;
  for (const [t0, g] of KICKS) {
    const n = Math.floor((t - t0) * FPS + 1e-6);
    if (n >= 0 && n < 7) a += g * (n % 2 ? -1 : 1) * (1 - n / 7) ** 1.5;
  }
  return a;
};
export const camAt = (id: number, f: number, pre?: number): Cam => {
  const c0 = run(CAMS[id], f, pre), dir = (id + runIdx) % 2 ? 1 : -1, oa = dir * Math.min(ORB_CAP[id] ?? ORBIT_MAX, ORBIT * Math.max(0, f - runStart));
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
/** v8 (teardown): focus blur only indoors (council, dining, parlour, couch); outdoor takes stay sharp: cInf 1.5 keeps the set crisp (<=1.5 px) while a
 *  near foreground prop at ~1.4 m still softens to ~4-5 px, like the reference's blurred lantern / snow mound */
export type Dof = { f: number; dur?: number; cInf: number; focus?: (f: number) => V3 };
const eyes = (p: V3, h = 1.2) => (): V3 => [p[0], p[1] + h, p[2]];
export const DOF: Dof[] = [
  { f: 0, cInf: 1.5, focus: () => [-6, D0 + 0.8, 111] },
  { f: 40, dur: 30, cInf: 1.5 },
  { f: 100, dur: 20, cInf: 1.5, focus: () => treWin(6, 1, 1, 4.6) },
  { f: 146, cInf: 3.5, /* v18 (owner: avg edge >= 28 %): indoor focus blur ~40 % lighter so the drawn sets read */ focus: () => [TX, D0 + 1.0, TZ] },
  { f: 197, cInf: 1.5, focus: () => [SWAMP.x, D0, SWAMP.z] },
  { f: 215, dur: 30, cInf: 1.5 },
  { f: 286, cInf: 1.5, focus: eyes(STUCK, 1.4) },
  { f: 373, cInf: 1.5, focus: () => NEWS },
  { f: 390, dur: 30, cInf: 1.5, focus: eyes(DOC) },
  { f: 468, cInf: 3, focus: () => [CX, CY, CZ - 0.35] },
  { f: 485, dur: 30, cInf: 3, focus: () => [CX, D0 + 1.5, CZ + 1.3] },
  { f: 580, cInf: 3.5, focus: () => MODEL },
  { f: 709, cInf: 1.5 },
  { f: 760, dur: 20, cInf: 1.5, focus: () => [27.2, D0 + 0.9, 93.2] },
  { f: 836, dur: 20, cInf: 1.5, focus: () => [29, D0 + 5.4, 93] },
  { f: 880, cInf: 1.5, focus: () => [-92.5, D0 + 3.0, 111] },
  { f: 905, dur: 30, cInf: 1.5 },
  { f: 985, cInf: 1.5, focus: () => [-92, D0 + 0.7, 108.8] },
  { f: 1052, cInf: 1.5, focus: () => [SHOP[0], D0 + 1.5 + 2.0, SHOP[2]] },
  { f: 1097, cInf: 1.5 },
  { f: 1196, cInf: 1.5, focus: () => [9.3, D0 + 0.5, 117] },
  { f: 1250, dur: 20, cInf: 2.5, focus: () => [6.9, D0 + 0.5, 117] },
  { f: 1298, cInf: 3, focus: () => [TABLES[1][0], D0 + 1.0, TABLES[1][1]] },
  { f: 1355, cInf: 1.5, focus: eyes(GUEST) },
  { f: 1478, cInf: 2, focus: () => [COUCH[0], D0 + 1.1, COUCH[2]] },
  { f: 1585, cInf: 1.5, focus: eyes(PULL) },
  { f: 1650, cInf: 1.5, focus: eyes(PULL2) },
  { f: 1730, cInf: 1.5 },
  { f: 1782, cInf: 1.5, focus: eyes(SHORE) },
  { f: 1823, cInf: 1.5 },
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
