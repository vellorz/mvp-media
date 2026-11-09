// "Fix it without fixing it": original ~69 s short about the Leaning Tower of Pisa for Modern Vista Prints (Wed Nov 11 2026).
// Same engine and camera grammar as the Eiffel short; the river town doubles as Pisa (river = Arno) with the Piazza dei
// Miracoli lawn, the Leaning Tower (tiers that stack, lean and curve per shot), the cathedral and the baptistery.
// Word times: pisa/voice/a.words.json.
export const FPS = 30;
export const VO_OFF = 0.2; // voice starts 0.2 s into the film
export const TOTAL = 2080;
export const POSTER_AT = 1917; // "And if you want one..." -> 2D poster end card
export const D0 = 6.0; // bank top + deck height (m)
export const HW = 6.5; // deck half width
export type V3 = [number, number, number];

export const clamp01 = (x: number) => Math.max(0, Math.min(1, x));
export const smooth = (x: number) => { const u = clamp01(x); return u * u * (3 - 2 * u); };
export const easeOut = (u: number) => 1 - (1 - clamp01(u)) ** 4;
export const W = (s: number) => s + VO_OFF; // word time -> film time
const F = (s: number) => Math.round(W(s) * FPS);

// ---------------- shots ----------------
export type Light = "day" | "golden";
export type Place = "london" | "desert" | "sea";
export type ShotDef = { id: number; a: number; b: number; light: Light; place: Place; sunAz?: number; sunEl?: number };
export const SHOTS: ShotDef[] = [
  { id: 1, a: 0, b: F(4.72), light: "day", place: "london" },          // hook: the leaning tower, closed 1990, engineers
  { id: 2, a: F(4.72), b: F(7.3), light: "day", place: "london" },     // "fix it... without fixing it"
  { id: 3, a: F(7.3), b: F(12.22), light: "day", place: "london" },    // 1178: builders on the 3-tier stub, it starts leaning
  { id: 4, a: F(12.22), b: F(16.48), light: "day", place: "london" },  // soft clay and sand / wet sponge
  { id: 5, a: F(16.48), b: F(22.42), light: "day", place: "london" },  // wars: Genoa, Lucca, Florence march; tools left
  { id: 6, a: F(22.42), b: F(27.82), light: "day", place: "london" },  // luckily: the soil packs down
  { id: 7, a: F(27.82), b: F(34.96), light: "day", place: "london" },  // builders back, crooked floors stack
  { id: 8, a: F(34.96), b: F(38.24), light: "day", place: "london" },  // curved like a banana
  { id: 9, a: F(38.24), b: F(41.06), light: "day", place: "london" },  // 1990: five and a half degrees
  { id: 10, a: F(41.06), b: F(44.74), light: "day", place: "london" }, // 870 tons of lead
  { id: 11, a: F(44.74), b: F(48.92), light: "day", place: "london" }, // drills pull the soil out
  { id: 12, a: F(48.92), b: F(53.6), light: "day", place: "london" },  // it settles back 45 cm
  { id: 13, a: F(53.6), b: F(58.96), light: "day", place: "london" },  // stopped on purpose / a straight tower is just a tower
  { id: 14, a: F(58.96), b: TOTAL, light: "golden", place: "london" }, // reopened 2001, tourists hold it up
];
export const XFADE: Record<number, number> = {};
export const CUT_X = 8;
const NO_ORBIT = new Set<number>([]);
export const FLASH_AT = F(7.3);
export const shotAt = (f: number) => SHOTS.find((s) => f >= s.a && f < s.b) ?? SHOTS[SHOTS.length - 1];
export type Layer = { id: number; alpha: number; pre?: number };
export const layersAt = (f: number): Layer[] => {
  const id = shotAt(f).id;
  for (const k of CAMS_REF()[id] ?? []) if (k.cut && f >= k.f && f < k.f + CUT_X) return [{ id, alpha: 1, pre: k.f }, { id, alpha: (f - k.f + 1) / (CUT_X + 1) }];
  return [{ id, alpha: 1 }];
};
const CAMS_REF = () => CAMS;
export const cutPre = (id: number, f: number, span = CUT_X): number | undefined => { for (const k of CAMS[id] ?? []) if (k.cut && f >= k.f && f < k.f + span) return k.f; return undefined; };

// ---------------- story state (the bridge stays whole; kept for the shared world code) ----------------
export const PIECES = 9;
export const BUILD_T: number[] = [];
export type World = { pieces: [number, number]; sink: number; fill: number; water: number; front: number; lake: boolean };
export const worldAt = (_id: number, _t: number): World => ({ pieces: [0, PIECES], sink: 0, fill: 1.2, water: 0, front: -2000, lake: true });
export const BAG_T = -10;
export const HITS: number[] = [];
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
/** the Leaning Tower: base centre; tiers stack from here; lean tips the top toward +x */
export const TOWER: V3 = [0, D0, 120];
const TX = TOWER[0], TZ = TOWER[2];
export const TIER_H = [11, 6.8, 6.8, 6.8, 6.8, 6.8, 6.8, 5.6]; // ground arcade, six loggias, belfry
export const T_R = 7.6;
const STUB_H = 11 + 6.8 * 2;
/** tower pose per shot/time: visible tiers, base lean (deg, visual), extra counter-tilt per tier above the 3rd (banana) */
export type Pose = { tiers: number; lean: number; kink: number };
const LEAN = 7, LEAN_SET = 5.8, KINK = 0.75;
export const POPS = [W(31.86), W(32.6), W(33.14), W(34.02), W(34.6)]; // new floors land
export const towerPose = (id: number, t: number): Pose => {
  switch (id) {
    case 3: return { tiers: 3, lean: 2 * smooth((t - W(8.34)) / 1.4), kink: 0 };
    case 4: case 5: case 6: return { tiers: 3, lean: 2, kink: 0 };
    case 7: { const n = POPS.filter((p) => t >= p).length; return { tiers: 3 + n, lean: 2 + (LEAN - 2) * (n / 5), kink: KINK }; }
    case 12: return { tiers: 8, lean: LEAN - (LEAN - LEAN_SET) * smooth((t - W(49.3)) / 2.4), kink: KINK };
    case 13: return t >= W(55.56) - 0.05 ? { tiers: 8, lean: 0, kink: 0 } : { tiers: 8, lean: LEAN_SET, kink: KINK };
    case 14: return { tiers: 8, lean: LEAN_SET, kink: KINK };
    default: return { tiers: 8, lean: LEAN, kink: KINK };
  }
};
export const HOOK: V3 = [TX - 2, D0, TZ - 64];       // engineers + barrier in front of the closed tower
export const BUILD: V3 = [TX + 1, D0, TZ - 20];      // 1178 builders at the stub's foot
export const SOIL: V3 = [TX - 5, D0, TZ - 22];       // soil card / sponge
export const WAR: V3 = [TX, D0, TZ - 34];            // the armies march across
export const marchStart = (g: number) => W(17.4) + g * 0.72;   // Genoa, Lucca, Florence enter
export const warX = (t: number, g: number) => -1.6 + 1.2 * Math.max(0, t - marchStart(g));
export const ENG: V3 = [TX - 3, D0, TZ - 40];        // 1990 engineers measuring
export const LEAD: V3 = [TX - 10, D0, TZ];           // lead on the high side
export const STOP: V3 = [TX + 1, D0, TZ - 46];
export const TOUR: V3 = [TX + 1, D0, TZ - 66];       // tourists (straight-tower gag, then the 2001 reopening)
// legacy places used by the shared world code
export const PILE: V3 = [9999, D0, 9999];
export const ROAD_Z = -95;
export const TOWN = { x: 150, z: -120 };
export const truckX = (_t: number, _k: number) => -9999;
export const shipX = (_t: number) => -9999;

const S1a = (f: number) => zoom([TX + 26, D0 + 1.4, TZ - 104], [TX - 2, D0 + 24, TZ], 50, pushK(f, 0, 0.0024), { roll: -0.03 });
const S1b = (f: number) => dolly([HOOK[0] + 0.6, D0 + 1.0, HOOK[2] - 8.5], [HOOK[0] + 0.2, D0 + 2.5, HOOK[2] + 4], pushK(f, F(1.34), 0.0016), { fov: 46 });
const S2a = (f: number) => dolly([HOOK[0] - 0.9, D0 + 1.55, HOOK[2] - 3.4], [HOOK[0] - 0.9, D0 + 1.45, HOOK[2]], pushK(f, F(4.72), 0.0022, 0.006, 25), { fov: 42, roll: 0.03 });
const S3a = (f: number) => dolly([BUILD[0] - 0.4, D0 + 1.0, BUILD[2] - 11], [BUILD[0] - 0.2, D0 + 2.5, BUILD[2] + 6], pushK(f, F(7.3), 0.0006), { fov: 48 });
const S3b = (f: number) => zoom([TX + 30, D0 + 2.5, TZ - 62], [TX, D0 + STUB_H / 2, TZ], 44, pushK(f, F(10.86), 0.002), { roll: 0.03 });
const S4a = (f: number) => dolly([SOIL[0] + 0.4, D0 + 1.4, SOIL[2] - 7.2], [SOIL[0] + 0.2, D0 + 1.3, SOIL[2]], pushK(f, F(12.22), 0.002), { fov: 44 });
const S5a = (f: number) => dolly([WAR[0], D0 + 1.4, WAR[2] - 20], [WAR[0], D0 + 3.0, WAR[2] + 6], pushK(f, F(16.48), 0.0008), { fov: 50 });
const S5b = (f: number) => dolly([BUILD[0] + 0.6, D0 + 1.0, BUILD[2] - 4.2], [BUILD[0] - 0.2, D0 + 0.8, BUILD[2] + 1.4], pushK(f, F(20.1), 0.0018), { fov: 46, roll: -0.03 });
const S6a = (f: number) => zoom([TX - 22, D0 + 2.2, TZ - 66], [TX, D0 + STUB_H / 2, TZ], 46, pushK(f, F(22.42), 0.002));
const S6b = (f: number) => dolly([SOIL[0] + 0.4, D0 + 1.3, SOIL[2] - 5.2], [SOIL[0] + 0.2, D0 + 1.1, SOIL[2]], pushK(f, F(25.56), 0.002), { fov: 44, roll: 0.03 });
const S7a = (f: number) => zoom([TX + 14, D0 + 2.2, TZ - 92], [TX + 2, D0 + 25, TZ], 52, pushK(f, F(27.82), 0.0012));
const S8a = (f: number) => zoom([TX - 6, D0 + 2.0, TZ - 108], [TX + 7, D0 + 27, TZ], 50, pushK(f, F(34.96), 0.0022), { roll: 0.02 });
const S9a = (f: number) => dolly([ENG[0] + 0.6, D0 + 0.9, ENG[2] - 7.5], [ENG[0] + 0.2, D0 + 3.4, ENG[2] + 6], pushK(f, F(38.24), 0.0014), { fov: 48, roll: -0.03 });
const S10a = (f: number) => dolly([LEAD[0] - 18, D0 + 2.2, LEAD[2] - 20], [LEAD[0] + 1.0, D0 + 4.0, LEAD[2]], pushK(f, F(41.06), 0.0018), { fov: 46 });
const S11a = (f: number) => dolly([LEAD[0] - 15, D0 + 1.6, LEAD[2] - 11], [LEAD[0] - 3.0, D0 + 2.2, LEAD[2] - 3.4], pushK(f, F(44.74), 0.002), { fov: 46, roll: 0.03 });
const S12a = (f: number) => zoom([TX + 4, D0 + 2.0, TZ - 100], [TX + 3, D0 + 27, TZ], 50, pushK(f, F(48.92), 0.0016));
const S13a = (f: number) => dolly([STOP[0] + 0.1, D0 + 1.5, STOP[2] - 4.0], [STOP[0] + 0.15, D0 + 1.5, STOP[2]], pushK(f, F(53.6), 0.0022, 0.006, 25), { fov: 42 });
const S13b = (f: number) => dolly([TOUR[0] + 0.2, D0 + 1.0, TOUR[2] - 10.0], [TOUR[0] + 0.1, D0 + 2.5, TOUR[2] + 4], pushK(f, F(55.56), 0.0014), { fov: 48 });
const S14a = (f: number) => dolly([TOUR[0] - 0.2, D0 + 1.0, TOUR[2] - 10.5], [TOUR[0] + 0.1, D0 + 2.5, TOUR[2] + 4], pushK(f, F(58.96), 0.0012), { fov: 48, roll: -0.02 });

const CAMS: Record<number, Key[]> = {
  1: [{ f: 0, s: S1a }, { f: F(1.34), cut: true, s: S1b }],
  2: [{ f: F(4.72), s: S2a }],
  3: [{ f: F(7.3), s: S3a }, { f: F(10.86), cut: true, s: S3b }],
  4: [{ f: F(12.22), s: S4a }],
  5: [{ f: F(16.48), s: S5a }, { f: F(20.1), cut: true, s: S5b }],
  6: [{ f: F(22.42), s: S6a }, { f: F(25.56), cut: true, s: S6b }],
  7: [{ f: F(27.82), s: S7a }],
  8: [{ f: F(34.96), s: S8a }],
  9: [{ f: F(38.24), s: S9a }],
  10: [{ f: F(41.06), s: S10a }],
  11: [{ f: F(44.74), s: S11a }],
  12: [{ f: F(48.92), s: S12a }],
  13: [{ f: F(53.6), s: S13a }, { f: F(55.56), cut: true, s: S13b }],
  14: [{ f: F(58.96), s: S14a }],
};

const KICKS: [number, number][] = [...POPS.map((p) => [p, 0.5] as [number, number]), [W(37.62), 0.6], [W(43.38), 0.6], [W(54.36), 0.7]];
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
  { f: 0, cInf: 0 },
  { f: F(1.34), cInf: 6, focus: eyes(HOOK) },
  { f: F(4.72), cInf: 13, focus: () => [HOOK[0] - 0.9, D0 + 1.45, HOOK[2]] },
  { f: F(7.3), cInf: 6, focus: eyes(BUILD) },
  { f: F(10.86), cInf: 0 },
  { f: F(12.22), cInf: 11, focus: () => [SOIL[0] + 0.2, D0 + 1.1, SOIL[2]] },
  { f: F(16.48), cInf: 5, focus: () => [WAR[0], D0 + 1.6, WAR[2]] },
  { f: F(20.1), cInf: 9, focus: () => [BUILD[0] + 0.4, D0 + 0.5, BUILD[2] + 1] },
  { f: F(22.42), cInf: 0 },
  { f: F(25.56), cInf: 11, focus: () => [SOIL[0] + 0.2, D0 + 1.1, SOIL[2]] },
  { f: F(27.82), cInf: 0 },
  { f: F(38.24), cInf: 6, focus: eyes(ENG) },
  { f: F(41.06), cInf: 4 },
  { f: F(48.92), cInf: 0 },
  { f: F(53.6), cInf: 13, focus: eyes(STOP) },
  { f: F(55.56), cInf: 6, focus: eyes(TOUR) },
  { f: F(58.96), cInf: 5, focus: eyes(TOUR) },
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
