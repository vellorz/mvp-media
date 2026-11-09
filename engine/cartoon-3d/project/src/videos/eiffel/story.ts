// "The Tower Paris Tried to Tear Down": original ~65 s short for Modern Vista Prints (Tue Nov 10 2026).
// Same engine and camera grammar as the London Bridge short; the London world doubles as 1889-1914 Paris (river =
// Seine, the stone bridge = Pont d'Iena) with the Eiffel Tower on the far bank. Word times: eiffel/voice/a.words.json.
export const FPS = 30;
export const VO_OFF = 0.2; // voice starts 0.2 s into the film
export const TOTAL = 1962;
export const POSTER_AT = 1782; // "And if you'd rather look at it..." -> 2D poster end card
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
  { id: 1, a: 0, b: F(4.58), light: "day", place: "london" },          // hook: demolition crew at the tower foot
  { id: 2, a: F(4.58), b: F(8.28), light: "day", place: "london" },    // 1889 World's Fair, Eiffel proud
  { id: 3, a: F(8.28), b: F(13.58), light: "day", place: "london" },   // artists hate it, the letter
  { id: 4, a: F(13.58), b: F(17.8), light: "day", place: "london" },   // Maupassant's lunch on the first floor
  { id: 5, a: F(17.8), b: F(20.88), light: "day", place: "london" },   // "Why?" tower over Paris, then his view
  { id: 6, a: F(20.88), b: F(25.26), light: "day", place: "london" },  // the deal: permit + calendar
  { id: 7, a: F(25.26), b: F(31.32), light: "day", place: "london" },  // scientists at the top, dropping things
  { id: 8, a: F(31.32), b: F(36.3), light: "day", place: "london", sunAz: 140 },   // radio: waves from the top
  { id: 9, a: F(36.3), b: F(40.48), light: "day", place: "london" },   // French operator loves it / German hears it
  { id: 10, a: F(40.48), b: F(46.88), light: "day", place: "london" }, // the Marne: German column jammed, stopped
  { id: 11, a: F(46.88), b: F(51.98), light: "day", place: "london" }, // telegram H-21, Mata Hari
  { id: 12, a: F(51.98), b: F(56.1), light: "golden", place: "london" }, // the tower protecting the city
  { id: 13, a: F(56.1), b: TOTAL, light: "day", place: "london" },     // painters on ropes (3D runs under the end card a moment)
];
export const XFADE: Record<number, number> = {};
export const CUT_X = 8;
const NO_ORBIT = new Set<number>([]);
export const FLASH_AT = F(4.58);
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
export const HITS = [W(2.7), W(3.2), W(3.62)]; // sledgehammer blows into the hook
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
/** the tower: centre of the four feet; 1:2 scale (150 m to the antenna tip), leg offset from the axis at height y */
export const TOWER: V3 = [0, D0, 210];
export const T_H = 150, T_L0 = 32, P1 = 28, P2 = 58, PTOP = 136;
export const legOff = (y: number) => T_L0 * Math.pow(Math.max(0, 1 - y / T_H), 1.7);
const TX = TOWER[0], TZ = TOWER[2];
export const P1Y = D0 + P1 + 1.25, PTY = D0 + PTOP + 0.4; // walkable deck heights
export const FOOT: V3 = [TX + 6, D0, TZ - 125];      // hook: crew at the south-west foot
export const EIFFEL2: V3 = [TX + 1.2, D0, 50];       // Eiffel at the fair
export const ARTISTS: V3 = [TX, D0, 46];             // the artists' group centre
export const MAUP: V3 = [TX - 3, P1Y, TZ - 25.4];   // Maupassant's table on the first floor (front edge)
export const DEAL: V3 = [TX + 2, D0, 48];
export const SCI: V3 = [TX + 1.2, PTY, TZ - 3.2];    // scientists on the top deck
export const SHACK: V3 = [TX + 24, D0, 52];          // radio shack at the foot (French operator)
export const GER: V3 = [-220, D0, -210];             // German field radio near the Marne
export const MARNE_Z = -236;
export const colX = (t: number) => -262 + 1.3 * (Math.min(t, W(46.1)) - W(40.48)); // column front walks east, stops on "stopped"
export const MATA: V3 = [40, D0, -33.6];             // Mata Hari on the quay
export const GOLD: V3 = [TX, D0, 44];
export const PAINT: V3 = [TX - 33.6, D0 + 12.2, TZ - 33.6]; // painters' plank on the south-west leg
// legacy places used by the shared world code
export const PILE: V3 = [9999, D0, 9999];
export const ROAD_Z = -95;
export const TOWN = { x: 150, z: -120 };
export const truckX = (_t: number, _k: number) => -9999;
export const shipX = (_t: number) => -9999;

const S1a = (f: number) => dolly([FOOT[0] - 0.6, D0 + 1.0, FOOT[2] - 9.0], [FOOT[0] + 0.4, D0 + 2.4, FOOT[2] + 4], pushK(f, 0, 0.0026), { fov: 46, roll: -0.04 });
const S1b = (f: number) => zoom([TX - 70, D0 + 6, TZ - 118], [TX, D0 + 62, TZ], 46, pushK(f, F(2.7), 0.0022));
const S2a = (f: number) => dolly([EIFFEL2[0] + 1.6, D0 + 1.0, EIFFEL2[2] - 6.5], [EIFFEL2[0] - 0.4, D0 + 2.3, EIFFEL2[2] + 4], pushK(f, F(4.58), 0.0012), { fov: 48, roll: 0.03 });
const S3a = (f: number) => dolly([ARTISTS[0] + 0.5, D0 + 1.0, ARTISTS[2] - 10.0], [ARTISTS[0] + 0.4, D0 + 2.3, ARTISTS[2]], pushK(f, F(8.28), 0.0012), { fov: 42 });
const S3b = (f: number) => dolly([ARTISTS[0] + 1.35, D0 + 1.6, ARTISTS[2] - 3.4], [ARTISTS[0] + 1.2, D0 + 1.45, ARTISTS[2] + 0.15], pushK(f, F(12.0), 0.0022, 0.006, 30), { fov: 40, roll: -0.04 });
const S4a = (f: number) => dolly([MAUP[0] + 1.0, MAUP[1] + 1.9, MAUP[2] + 5.6], [MAUP[0] + 0.3, MAUP[1] + 1.0, MAUP[2]], pushK(f, F(13.58), 0.0025), { fov: 44 });
const S5a = (f: number) => zoom([TX - 30, D0 + 9, -62], [TX, D0 + 58, TZ], 50, pushK(f, F(17.8), 0.003));
const S5b = (f: number) => dolly([MAUP[0] + 2.4, MAUP[1] + 1.7, MAUP[2] + 2.6], [MAUP[0] - 1.6, MAUP[1] + 0.9, MAUP[2] - 5.0], pushK(f, F(19.4), 0.0022), { fov: 50 });
const S6a = (f: number) => dolly([DEAL[0] + 0.4, D0 + 1.0, DEAL[2] - 7.0], [DEAL[0] + 0.2, D0 + 2.2, DEAL[2]], pushK(f, F(20.88), 0.0012), { fov: 42 });
const S6b = (f: number) => dolly([DEAL[0] + 2.6, D0 + 1.6, DEAL[2] - 3.6], [DEAL[0] + 2.9, D0 + 1.4, DEAL[2] - 0.4], pushK(f, F(22.1), 0.0022, 0.006, 25), { fov: 40, roll: 0.04 });
const S7a = (f: number) => dolly([SCI[0] + 3.6, SCI[1] + 2.0, SCI[2] - 5.6], [SCI[0] - 0.6, SCI[1] + 1.2, SCI[2]], pushK(f, F(25.26), 0.0025), { fov: 46 });
const S7b = (f: number) => ({ pos: [SCI[0] + 12, SCI[1] - 2, SCI[2] - 12] as V3, look: [SCI[0] + 2.2, SCI[1] - 3, SCI[2] - 0.6] as V3, fov: 50 - 4 * clamp01((f - F(30.0)) / 30), roll: 0.05 });
const S8a = (f: number) => zoom([TX - 160, D0 + 40, -70], [TX, D0 + 92, TZ], 46, pushK(f, F(31.32), 0.0024));
const S9a = (f: number) => dolly([SHACK[0] - 2.4, D0 + 1.0, SHACK[2] - 5.0], [SHACK[0] - 0.6, D0 + 2.1, SHACK[2]], pushK(f, F(36.3), 0.0012), { fov: 42 });
const S9b = (f: number) => dolly([GER[0] + 1.2, D0 + 1.6, GER[2] - 4.6], [GER[0] + 0.3, D0 + 1.4, GER[2]], pushK(f, F(38.0), 0.0024, 0.006, 25), { fov: 42, roll: -0.04 });
const S10a = (f: number) => { const x = colX(f / FPS); return dolly([x + 9, D0 + 2.2, MARNE_Z - 11], [x - 2, D0 + 1.5, MARNE_Z], pushK(f, F(40.48), 0.0018), { fov: 44 }); };
const S10b = (f: number) => { const x = colX(f / FPS); return dolly([x + 4.5, D0 + 1.7, MARNE_Z - 5.6], [x + 0.2, D0 + 1.5, MARNE_Z], pushK(f, F(45.6), 0.002, 0.006, 25), { fov: 42, roll: 0.04 }); };
const S11a = (f: number) => dolly([SHACK[0] + 0.2, D0 + 1.8, SHACK[2] - 3.6], [SHACK[0] + 0.4, D0 + 1.35, SHACK[2] - 0.6], pushK(f, F(46.88), 0.0024), { fov: 40 });
const S11b = (f: number) => dolly([MATA[0] + 0.8, D0 + 1.7, MATA[2] - 5.4], [MATA[0] - 0.2, D0 + 1.5, MATA[2]], pushK(f, F(50.32), 0.0025, 0.006, 25), { fov: 42 });
const S12a = (f: number) => dolly([GOLD[0] + 2.4, D0 + 0.9, GOLD[2] - 8], [GOLD[0], D0 + 2.6, GOLD[2] + 6], pushK(f, F(51.98), 0.0012), { fov: 54, roll: -0.02 });
const S13a = (f: number) => dolly([PAINT[0] - 4.4, PAINT[1] + 1.6, PAINT[2] - 6.6], [PAINT[0] + 0.3, PAINT[1] + 1.2, PAINT[2]], pushK(f, F(56.1), 0.0025), { fov: 44 });

const CAMS: Record<number, Key[]> = {
  1: [{ f: 0, s: S1a }, { f: F(2.7), cut: true, s: S1b }],
  2: [{ f: F(4.58), s: S2a }],
  3: [{ f: F(8.28), s: S3a }, { f: F(12.0), cut: true, s: S3b }],
  4: [{ f: F(13.58), s: S4a }],
  5: [{ f: F(17.8), s: S5a }, { f: F(19.4), cut: true, s: S5b }],
  6: [{ f: F(20.88), s: S6a }, { f: F(22.1), cut: true, s: S6b }],
  7: [{ f: F(25.26), s: S7a }, { f: F(30.0), cut: true, s: S7b }],
  8: [{ f: F(31.32), s: S8a }],
  9: [{ f: F(36.3), s: S9a }, { f: F(38.0), cut: true, s: S9b }],
  10: [{ f: F(40.48), s: S10a }, { f: F(45.6), cut: true, s: S10b }],
  11: [{ f: F(46.88), s: S11a }, { f: F(50.32), cut: true, s: S11b }],
  12: [{ f: F(51.98), s: S12a }],
  13: [{ f: F(56.1), s: S13a }],
};

const KICKS: [number, number][] = [...HITS.map((h) => [h, 0.6] as [number, number]), [W(24.56), 0.8], [W(33.0), 0.9], [W(42.12), 0.7], [W(46.1), 0.8], [W(56.78), 0.5]];
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
  { f: 0, cInf: 12, focus: () => [FOOT[0] + 0.6, D0 + 1.6, FOOT[2]] },
  { f: F(2.7), cInf: 0 },
  { f: F(4.58), cInf: 6, focus: eyes(EIFFEL2) },
  { f: F(8.28), cInf: 6, focus: eyes(ARTISTS) },
  { f: F(12.0), cInf: 13, focus: () => [ARTISTS[0] + 1.2, D0 + 1.45, ARTISTS[2] + 0.15] },
  { f: F(13.58), cInf: 12, focus: eyes(MAUP) },
  { f: F(17.8), cInf: 0 },
  { f: F(19.4), cInf: 6, focus: eyes(MAUP) },
  { f: F(20.88), cInf: 6, focus: eyes(DEAL) },
  { f: F(22.1), cInf: 13, focus: () => [DEAL[0] + 2.9, D0 + 1.4, DEAL[2] - 0.4] },
  { f: F(25.26), cInf: 9, focus: eyes(SCI) },
  { f: F(30.0), cInf: 0 },
  { f: F(36.3), cInf: 6, focus: eyes(SHACK) },
  { f: F(38.0), cInf: 12, focus: eyes(GER) },
  { f: F(40.48), cInf: 6 },
  { f: F(45.6), cInf: 10 },
  { f: F(46.88), cInf: 13, focus: () => [SHACK[0] + 0.4, D0 + 1.35, SHACK[2] - 0.6] },
  { f: F(50.32), cInf: 12, focus: eyes(MATA) },
  { f: F(51.98), cInf: 4 },
  { f: F(56.1), cInf: 10, focus: () => [PAINT[0], PAINT[1] + 1.5, PAINT[2]] },
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
