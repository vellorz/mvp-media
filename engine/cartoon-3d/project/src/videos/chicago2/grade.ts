// Colour grade for the bridge short (post agent): references/grade/GradeEffect.ts (reports/grade.md) verbatim,
// plus GRADES / GRADE_STRENGTH / gradeFor() so the lead can re-fit the presets after the lighting merge.
// The presets were fitted to the OLD unlit stills: after the WORLD lighting lands they will over-correct; re-fit
// (grade.md 5.C) or lower GRADE_STRENGTH. Each Inner (crossfade layer) grades with its own shot's light, so the DOM
// crossfade at XFADE frames (shots 10->11, 13->14) cross-fades the presets as well.
// GradeEffect: the fitted reference-style colour grade as a postprocessing 6.37 Effect.
// Put it LAST in the EffectComposer, after ToneMappingEffect. It works on display-referred values: the input (linear,
// already tone-mapped to 0..1) is encoded to sRGB, graded exactly like scripts/grade.py (validated on our stills), and
// decoded back to linear for the composer's output encoding.
//   1. RGB tone curve: monotone cubic Hermite through 7 knots at x = 0, .1, .25, .5, .75, .9, 1
//   2. saturation around luma Y' (Rec.709 weights on the encoded values), separately for shadows / mids / highlights
//   3. 3-way tint (split tone): zero-luma RGB offsets in shadows, mids, highlights
//   4. vignette: x (1 - k * smoothstep(r0, 1, r)), r = elliptical radius, corners = 1
// `amount` blends the whole grade (0 = bypass) so it can be dialled back once lighting/albedo work brightens the render.
import { Effect, BlendFunction } from "postprocessing";
import { Uniform, Vector3, Vector2 } from "three";

const frag = /* glsl */ `
uniform float gradeKy[7];
uniform float gradeKm[7];
uniform vec3 gradeSat;      // x = shadows, y = mids, z = highlights
uniform vec3 gradeTintS;    // zero-luma RGB offsets (sRGB-encoded units)
uniform vec3 gradeTintM;
uniform vec3 gradeTintH;
uniform vec2 gradeVig;      // x = strength k, y = start radius r0
uniform float gradeAmount;

vec3 gradeEncode(vec3 c) {   // linear -> sRGB
  c = clamp(c, 0.0, 1.0);
  return mix(c * 12.92, 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055, step(vec3(0.0031308), c));
}
vec3 gradeDecode(vec3 c) {   // sRGB -> linear
  return mix(c / 12.92, pow((c + 0.055) / 1.055, vec3(2.4)), step(vec3(0.04045), c));
}
float gradeHermite(float v, float x0, float x1, float y0, float y1, float m0, float m1) {
  float h = x1 - x0, t = (v - x0) / h, t2 = t * t, t3 = t2 * t;
  return (2.0 * t3 - 3.0 * t2 + 1.0) * y0 + (t3 - 2.0 * t2 + t) * h * m0 + (-2.0 * t3 + 3.0 * t2) * y1 + (t3 - t2) * h * m1;
}
float gradeCurve(float v) {
  v = clamp(v, 0.0, 1.0);
  if (v < 0.1)  return gradeHermite(v, 0.0, 0.1, gradeKy[0], gradeKy[1], gradeKm[0], gradeKm[1]);
  if (v < 0.25) return gradeHermite(v, 0.1, 0.25, gradeKy[1], gradeKy[2], gradeKm[1], gradeKm[2]);
  if (v < 0.5)  return gradeHermite(v, 0.25, 0.5, gradeKy[2], gradeKy[3], gradeKm[2], gradeKm[3]);
  if (v < 0.75) return gradeHermite(v, 0.5, 0.75, gradeKy[3], gradeKy[4], gradeKm[3], gradeKm[4]);
  if (v < 0.9)  return gradeHermite(v, 0.75, 0.9, gradeKy[4], gradeKy[5], gradeKm[4], gradeKm[5]);
  return gradeHermite(v, 0.9, 1.0, gradeKy[5], gradeKy[6], gradeKm[5], gradeKm[6]);
}

void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor) {
  vec3 src = gradeEncode(inputColor.rgb);
  vec3 c = vec3(gradeCurve(src.r), gradeCurve(src.g), gradeCurve(src.b));
  const vec3 W = vec3(0.2126, 0.7152, 0.0722);
  float y = dot(c, W);
  float wS = 1.0 - smoothstep(0.0, 0.55, y);
  float wH = smoothstep(0.45, 1.0, y);
  float wM = 1.0 - wS - wH;
  float s = gradeSat.y + (gradeSat.x - gradeSat.y) * wS + (gradeSat.z - gradeSat.y) * wH;
  c = vec3(y) + s * (c - vec3(y));
  c += wS * gradeTintS + wM * gradeTintM + wH * gradeTintH;
  vec2 p = uv * 2.0 - 1.0;
  float r = length(p) * 0.70710678;
  c *= 1.0 - gradeVig.x * smoothstep(gradeVig.y, 1.0, r);
  c = clamp(c, 0.0, 1.0);
  outputColor = vec4(gradeDecode(mix(src, c, gradeAmount)), inputColor.a);
}`;

// BT.709 zero-luma chroma basis (sRGB-encoded units): unit Cb and unit Cr as RGB offsets with Y' unchanged
const E_CB: [number, number, number] = [0.0, -0.18733, 1.8556];
const E_CR: [number, number, number] = [1.5748, -0.46813, 0.0];
export const tintRGB = (cb: number, cr: number) =>
  new Vector3(cb * E_CB[0] + cr * E_CR[0], cb * E_CB[1] + cr * E_CR[1], cb * E_CB[2] + cr * E_CR[2]);

/** Fritsch-Carlson monotone tangents for the 7 fixed knots (same as scripts/grade.py `tangents`) */
export const KX = [0, 0.1, 0.25, 0.5, 0.75, 0.9, 1];
export function monoTangents(ky: number[]): number[] {
  const n = KX.length, h: number[] = [], d: number[] = [], m = new Array(n).fill(0);
  for (let k = 0; k < n - 1; k++) { h.push(KX[k + 1] - KX[k]); d.push((ky[k + 1] - ky[k]) / h[k]); }
  m[0] = d[0]; m[n - 1] = d[n - 2];
  for (let k = 1; k < n - 1; k++) {
    if (d[k - 1] * d[k] <= 0) { m[k] = 0; continue; }
    const w1 = 2 * h[k] + h[k - 1], w2 = h[k] + 2 * h[k - 1];
    m[k] = (w1 + w2) / (w1 / d[k - 1] + w2 / d[k]);
  }
  return m;
}

export type GradeParams = {
  ky: number[];                                  // 7 curve values at KX
  sat: [number, number, number];                 // shadows, mids, highlights
  tintS: [number, number]; tintM: [number, number]; tintH: [number, number];   // (Cb, Cr) per zone
  vig: [number, number];                         // strength, start radius
};

// __GRADES__ (fitted by scripts/fit2.py, written by scripts/emit_ts.py)
export const GRADE_DAY: GradeParams = {
  ky: [0.0345, 0.1828, 0.3812, 0.6605, 0.8814, 0.9631, 1],   // tangents: [1.4831, 1.4038, 1.2198, 0.9867, 0.6608, 0.4346, 0.3693]
  sat: [0.9831, 1.2727, 1.4573],
  tintS: [-0.0291, 0.0411], tintM: [0.0376, -0.0104], tintH: [0.0144, -0.0047],
  vig: [0.1, 0.45],
};
//   shadows tint: hue 20 deg, RGB offset (+16.5, -3.5, -13.8)/255
//   mids tint: hue 230 deg, RGB offset (-4.2, -0.6, +17.8)/255
//   highlights tint: hue 228 deg, RGB offset (-1.9, -0.1, +6.8)/255
export const GRADE_GOLDEN: GradeParams = {
  ky: [0.0311, 0.1877, 0.4017, 0.6754, 0.875, 0.9582, 1],   // tangents: [1.5667, 1.498, 1.2526, 0.9235, 0.6445, 0.4724, 0.4183]
  sat: [0.8316, 0.8799, 1.7061],
  tintS: [0.0528, 0.0004], tintM: [0.0583, -0.0003], tintH: [0, 0],
  vig: [0.16, 0.4],
};
//   shadows tint: hue 246 deg, RGB offset (+0.2, -2.6, +25.0)/255
//   mids tint: hue 245 deg, RGB offset (-0.1, -2.7, +27.6)/255
//   highlights tint: hue 0 deg, RGB offset (+0.0, -0.0, +0.0)/255

export class GradeEffect extends Effect {
  constructor(p: GradeParams, amount = 1) {
    super("GradeEffect", frag, {
      blendFunction: BlendFunction.NORMAL,
      uniforms: new Map<string, Uniform>([
        ["gradeKy", new Uniform(p.ky.slice())],
        ["gradeKm", new Uniform(monoTangents(p.ky))],
        ["gradeSat", new Uniform(new Vector3(...p.sat))],
        ["gradeTintS", new Uniform(tintRGB(...p.tintS))],
        ["gradeTintM", new Uniform(tintRGB(...p.tintM))],
        ["gradeTintH", new Uniform(tintRGB(...p.tintH))],
        ["gradeVig", new Uniform(new Vector2(...p.vig))],
        ["gradeAmount", new Uniform(amount)],
      ]),
    });
  }
  /** switch preset per shot (day <-> golden) or blend two presets during a crossfade/time-of-day change */
  set(p: GradeParams, q?: GradeParams, t = 0) {
    const L = (a: number, b: number) => a + (b - a) * t;
    const r: GradeParams = q ? {
      ky: p.ky.map((v, i) => L(v, q.ky[i])),
      sat: [L(p.sat[0], q.sat[0]), L(p.sat[1], q.sat[1]), L(p.sat[2], q.sat[2])],
      tintS: [L(p.tintS[0], q.tintS[0]), L(p.tintS[1], q.tintS[1])], tintM: [L(p.tintM[0], q.tintM[0]), L(p.tintM[1], q.tintM[1])],
      tintH: [L(p.tintH[0], q.tintH[0]), L(p.tintH[1], q.tintH[1])], vig: [L(p.vig[0], q.vig[0]), L(p.vig[1], q.vig[1])],
    } : p;
    const u = this.uniforms;
    u.get("gradeKy")!.value = r.ky.slice();
    u.get("gradeKm")!.value = monoTangents(r.ky);
    (u.get("gradeSat")!.value as Vector3).set(...r.sat);
    u.get("gradeTintS")!.value = tintRGB(...r.tintS);
    u.get("gradeTintM")!.value = tintRGB(...r.tintM);
    u.get("gradeTintH")!.value = tintRGB(...r.tintH);
    (u.get("gradeVig")!.value as Vector2).set(...r.vig);
  }
  get amount() { return this.uniforms.get("gradeAmount")!.value as number; }
  set amount(v: number) { this.uniforms.get("gradeAmount")!.value = v; }
}

/** Presets per light (plain objects: edit / re-fit freely). */
// Round-2 re-fit on the relit world (WORLD agent, 2026-10-31). The fitted presets above brighten (they were fitted to
// the old dark stills) and washed the new lighting out; these are gentle S-curves at full strength instead.
//   day: mid knot .60 for median Y' ~.57, darks pressed (.1 -> .085), a hint of violet in shadows.
//   golden: stronger S (darks .1 -> .09, mids .5 -> .54), blue-violet shadow tint, orange highlight tint, heavier vignette.
// Round 3 (2026-11-08, Modern Vista experiment): fitted to the measured reference (5 shorts, every 10th frame):
// luma p5/p50/p95 34/109/214 (ours were 59/152/225) and Lab C* mean/p90 30/53 (ours 22.7/39.8); shadows coloured
// violet/plum (never grey), neutrals a hair magenta + cool, corners ~0.71 of the centre. The curve is the old day curve
// pushed through the measured percentile map (.231->.133, .596->.427, .882->.839).
export const GRADE_DAY2: GradeParams = {
  ky: [0, 0.058, 0.172, 0.433, 0.771, 0.925, 1],
  sat: [0.72, 0.76, 0.7], // v2 (F3 greyed palette): measured HSV S ~.62-.75 at 1.4 -> target .40-.48
  tintS: [0.028, 0.02], tintM: [0.004, 0.006], tintH: [0.004, 0.002],
  vig: [0.32, 0.32],
};
export const GRADE_GOLDEN2: GradeParams = {
  ky: [0, 0.06, 0.17, 0.43, 0.75, 0.91, 1],
  sat: [0.82, 0.86, 0.8], // v2: dusk/night two-colour scenes target .48-.55
  tintS: [0.035, 0.022], tintM: [0.004, 0.006], tintH: [-0.012, 0.006],
  vig: [0.34, 0.32],
};
export const GRADES: Record<"day" | "golden", GradeParams> = { day: GRADE_DAY2, golden: GRADE_GOLDEN2 };
/** One strength (0..1, the effect's `amount`) per preset, set against the NEW world (bridge_world, 2026-10-31): full-strength
 *  presets overshot (day median Y' .59-.67 vs target .571, golden .58 vs .52); day 0.65 / golden 0.45 land at
 *  .54-.62 / ~.52. Re-fit the presets (grade.md 5.C) after the merge and raise these again. */
export const GRADE_STRENGTH: Record<"day" | "golden", number> = { day: 1, golden: 1 };
/** Apply the preset of a light to the effect (only touches uniforms when the light changes). */
export function gradeFor(fx: GradeEffect, light: "day" | "golden") {
  const tag = fx as unknown as { _light?: string };
  if (tag._light !== light) { fx.set(GRADES[light]); tag._light = light; }
  fx.amount = GRADE_STRENGTH[light];
}

/** v3 teardown: time of day by colour. Take 12 ("a little steeper every single day"): before each day's step the
 *  picture dips to blue night, warms through a pink dawn, then lands on day as the step pops. */
export const GRADE_NIGHT: GradeParams = { ky: [0, 0.03, 0.09, 0.24, 0.46, 0.6, 0.7], sat: [0.5, 0.5, 0.45], tintS: [0.09, -0.02], tintM: [0.08, -0.03], tintH: [0.05, -0.02], vig: [0.45, 0.28] };
export const GRADE_DAWN: GradeParams = { ky: [0, 0.05, 0.15, 0.4, 0.72, 0.88, 0.97], sat: [0.75, 0.8, 0.75], tintS: [0.04, 0.03], tintM: [-0.04, 0.06], tintH: [-0.06, 0.05], vig: [0.36, 0.3] };
const lerpG = (p: GradeParams, q: GradeParams, t: number): GradeParams => {
  const L = (a: number, b: number) => a + (b - a) * t;
  return { ky: p.ky.map((v, i) => L(v, q.ky[i])), sat: [L(p.sat[0], q.sat[0]), L(p.sat[1], q.sat[1]), L(p.sat[2], q.sat[2])],
    tintS: [L(p.tintS[0], q.tintS[0]), L(p.tintS[1], q.tintS[1])], tintM: [L(p.tintM[0], q.tintM[0]), L(p.tintM[1], q.tintM[1])],
    tintH: [L(p.tintH[0], q.tintH[0]), L(p.tintH[1], q.tintH[1])], vig: [L(p.vig[0], q.vig[0]), L(p.vig[1], q.vig[1])] };
};
const tri = (x: number) => Math.max(0, 1 - Math.abs(x));
/** day frames (film) of the step pops; night peaks 8 f before, dawn 3 f before */
export function todFor(fx: GradeEffect, days: number[], f: number) {
  let n = 0, d = 0;
  for (const df of days) { n = Math.max(n, tri((f - (df - 9)) / 6)); d = Math.max(d, tri((f - (df - 3)) / 4)); }
  const tag = fx as unknown as { _light?: string };
  if (n <= 0 && d <= 0) { if (tag._light !== "day") { fx.set(GRADE_DAY2); tag._light = "day"; } return; }
  const base = lerpG(GRADE_DAY2, GRADE_NIGHT, n * n * (3 - 2 * n));
  fx.set(lerpG(base, GRADE_DAWN, d * 0.85)); tag._light = "tod";
}
