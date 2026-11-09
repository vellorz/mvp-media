// "The Bridge That Fell for a Song": our original 67 s short in the flat-characters-in-a-3D-toon-world style.
// One three.js world (world.ts) posed per frame from the story timeline (story.ts). Post chain (look-match pass):
//   InkPass (world ink lines, own pass) -> lens blur pre + main (thin-lens DOF per shot from dofAt) ->
//   [bloom (emissive only) + NEUTRAL tone mapping + colour grade] (one merged EffectPass), MSAA 4.
// Ink runs before the DOF so lines blur with what they belong to; bloom after the DOF so glows defocus with their
// source; the grade is display-referred, so it comes after tone mapping. Every pixel-sized parameter is specified at
// 1080x1920 and scaled with the output size, so stills at --scale 0.5 and the 1440x2560 final match.
// Place changes crossfade by stacking a second canvas for the fade frames; the hook ends on a 4-frame white flash.
import React, { useEffect, useMemo, useState } from "react";
import * as THREE from "three";
import { AbsoluteFill, continueRender, delayRender, getInputProps, useCurrentFrame } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import { useThree } from "@react-three/fiber";
import { EffectComposer } from "@react-three/postprocessing";
import { BlendFunction, BloomEffect, ToneMappingEffect, ToneMappingMode } from "postprocessing";
import { World, loadKit } from "./world";
import { InkPass, noInkFallback } from "./ink";
import { LensBlur, GrainEffect } from "./lensblur";
import { GradeEffect, GRADES, GRADE_STRENGTH, gradeFor } from "./grade";
import { Kit } from "./build";
import { SHOTS, POSTER_AT, dofAt, cutPre } from "./story";
import { NEW_TOTAL, NEW_FLASH_AT, NEW_POSTER_AT, SEGS, segLayers, oldOf } from "./remap";
import { Img, staticFile, interpolate, Easing } from "remotion";

export const HAVASU_FRAMES = NEW_TOTAL;

/** A/B switches for test stills only (Remotion inputProps `{ post: { ink: false, ... } }`); everything is on by default. */
type PostToggles = { ink: boolean; lens: boolean; pre: boolean; bloom: boolean; grade: boolean; grain: boolean };
const toggles = (): PostToggles => ({ ink: true, lens: true, pre: true, bloom: true, grade: true, grain: false, ...((getInputProps() as { post?: Partial<PostToggles> }).post ?? {}) });

/** Bloom for emissive sources only (depth.md 6.4). Its MIP chain always starts at 540x960 (half of 1080x1920),
 *  whatever the output size, so the glow keeps the same size relative to the frame (e-fold ~30 px at 1080p,
 *  ~1.5 % of the frame height) at 540, 1080 and 1440 widths. ADD blend: HDR-safe (SCREEN darkens values > 1). */
const makeBloom = () => {
  const b = new BloomEffect({ blendFunction: BlendFunction.ADD, intensity: 0.5, luminanceThreshold: 1.0, luminanceSmoothing: 0.2, mipmapBlur: true, levels: 6, radius: 0.6 });
  const mip = b.mipmapBlurPass;
  const setSize = mip.setSize.bind(mip);
  mip.setSize = (w: number, h: number) => setSize(Math.round((1920 * w) / Math.max(h, 1)), 1920);
  return b;
};

const fwd = new THREE.Vector3(), fpt = new THREE.Vector3();

const useKit = () => {
  const [kit, setKit] = useState<Kit | null>(null);
  const [handle] = useState(() => delayRender("havasu kit"));
  useEffect(() => { loadKit().then((k) => { setKit(k); continueRender(handle); }); }, [handle]);
  return kit;
};

/** The EffectComposer mounts AFTER @remotion/three's first advance(), so the first frame a canvas renders (every still,
 *  the first frame of every parallel render tab, and every crossfade overlay) came out blank. Hold the frame until the
 *  composer has drawn twice. */
const SettlePost: React.FC = () => {
  const { advance } = useThree();
  useEffect(() => {
    const h = delayRender("postprocessing settle");
    let n = 0;
    const tick = () => { advance(performance.now()); if (++n < 2) requestAnimationFrame(tick); else continueRender(h); };
    requestAnimationFrame(tick);
  }, [advance]);
  return null;
};

const Inner: React.FC<{ id: number; kit: Kit; pre?: number; of: number }> = ({ id, kit, pre, of }) => {
  const f = of;
  const { camera, scene } = useThree();
  const world = useMemo(() => new World(kit), [kit]);
  const target = useMemo(() => new THREE.Vector3(), []);
  const on = useMemo(toggles, []);
  const fx = useMemo(() => ({
    ink: new InkPass(scene, camera as THREE.PerspectiveCamera),
    lens: new LensBlur({ maxCoC: 24, nearScale: 1.2 }),
    bloom: makeBloom(),
    tone: new ToneMappingEffect({ mode: ToneMappingMode.NEUTRAL }),
    grade: new GradeEffect(GRADES.day, GRADE_STRENGTH.day),
    grain: new GrainEffect({ amount: 0.025, cellPx: 1.5 }), // film grain, OFF by default (inputProps post.grain): the reference measures no grain and it quadruples the file size
  }), [camera, scene]);
  useEffect(() => () => fx.ink.dispose(), [fx]);
  const post = useMemo(() => (
    <EffectComposer multisampling={4}>
      {on.ink ? <primitive object={fx.ink} dispose={null} /> : null}
      {on.lens && on.pre ? <primitive object={fx.lens.pre} dispose={null} /> : null}
      {on.lens ? <primitive object={fx.lens.main} dispose={null} /> : null}
      {on.bloom ? <primitive object={fx.bloom} dispose={null} /> : null}
      <primitive object={fx.tone} dispose={null} />
      {on.grade ? <primitive object={fx.grade} dispose={null} /> : null}
      {on.grain ? <primitive object={fx.grain} dispose={null} /> : null}
    </EffectComposer>
  ), [fx, on]);
  const cam = camera as THREE.PerspectiveCamera;
  target.copy(world.update(id, f, cam, scene, pre));
  noInkFallback(world.root);
  // thin-lens focus: distance along the view axis to the shot's focus point (default: the camera's look target)
  const d = dofAt(pre !== undefined ? Math.min(f, pre - 1) : f);
  cam.getWorldDirection(fwd);
  if (d.focus) fpt.set(...d.focus(f)); else fpt.copy(target);
  fx.lens.focus = Math.max(0.3, fpt.sub(cam.position).dot(fwd));
  fx.lens.cInf = d.cInf;
  gradeFor(fx.grade, SHOTS[id - 1].light);
  fx.grain.seed = f; // deterministic per frame
  return (
    <>
      <primitive object={world.root} dispose={null} />
      {post}
      <SettlePost />
    </>
  );
};

/** test stills only: inputProps `{ post: { dpr: 0.5 } }` forces the WebGL buffer size (R3F clamps dpr to >= 1 by default) */
const dprOverride = () => (getInputProps() as { post?: { dpr?: number } }).post?.dpr;
const ShotView: React.FC<{ id: number; kit: Kit; alpha: number; pre?: number; of: number }> = ({ id, kit, alpha, pre, of }) => (
  <AbsoluteFill style={{ opacity: alpha }}>
    <ThreeCanvas width={1080} height={1920} {...(dprOverride() ? { dpr: dprOverride() } : {})} shadows gl={{ antialias: false, stencil: false, powerPreference: "high-performance", toneMappingExposure: 1.0 }}
      camera={{ fov: 40, near: 0.2, far: 1500 }}>
      <Inner id={id} kit={kit} pre={pre} of={of} />
    </ThreeCanvas>
  </AbsoluteFill>
);

/** end card: the London poster, whole (border and bottom line always visible), over a blurred still of the last shot */
const EndCard: React.FC<{ f: number }> = ({ f }) => {
  const k = f - POSTER_AT;
  const rise = interpolate(k, [0, 20], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(0.2, 0.9, 0.25, 1.08) });
  const bg = interpolate(k, [0, 14], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const push = 1 + 0.0006 * Math.max(0, k - 20);
  const word = interpolate(k, [22, 36], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const PW = 860, PH = Math.round((PW * 1536) / 1024);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: bg }}>
        <Img src={staticFile("havasu/endbg.jpg")} style={{ width: "100%", height: "100%", objectFit: "cover", filter: "blur(18px) brightness(0.62) saturate(0.9)", transform: "scale(1.08)" }} />
      </AbsoluteFill>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
        <div style={{ transform: `translateY(${-70 + rise * 1500}px) rotate(${-5 * rise}deg) scale(${push})`, width: PW, height: PH,
          boxShadow: "0 30px 70px rgba(10,8,20,0.55), 0 6px 16px rgba(10,8,20,0.35)", background: "#f3e7cf" }}>
          <Img src={staticFile("havasu/london.jpg")} style={{ width: PW, height: PH, display: "block" }} />
        </div>
        <div style={{ position: "absolute", top: 1920 / 2 - 70 + PH / 2 + 46, width: "100%", textAlign: "center", opacity: word, color: "#f6ecd8",
          fontFamily: "Georgia, 'Times New Roman', serif", fontSize: 34, letterSpacing: 12 }}>MODERN VISTA PRINTS</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---- narration captions (measured reference: 1-2 words, hard swaps, white heavy rounded sans, thin black stroke +
// drop shadow, ~3 % of frame height, baseline ~70 % down, 0-6 frames ahead of the word). Over the end card they move
// below the poster so the poster stays fully visible.
import CAPS from "./captions.json";
let fontReady: Promise<void> | null = null;
const useCaptionFont = () => {
  const [h] = useState(() => delayRender("caption font"));
  useEffect(() => {
    fontReady ??= new FontFace("CapSans", `url(${staticFile("havasu/fonts/Montserrat.ttf")}) format("truetype")`, { weight: "100 900" })
      .load().then((ff) => { (document.fonts as unknown as { add: (x: FontFace) => void }).add(ff); });
    fontReady.then(() => continueRender(h), () => continueRender(h));
  }, [h]);
};
const Captions: React.FC<{ f: number }> = ({ f }) => {
  const c = (CAPS as [string, number, number][]).find(([, a, b]) => f >= a && f < b);
  if (!c) return null;
  const y = f >= NEW_POSTER_AT ? 1765 : 1375; // baseline
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 40, right: 40, top: y - 74, height: 90, lineHeight: "90px", textAlign: "center", fontFamily: "CapSans",
        fontWeight: 800, fontSize: 74, color: "#ffffff", WebkitTextStroke: "10px #050505", paintOrder: "stroke fill",
        textShadow: "4px 4px 3px #000000", whiteSpace: "nowrap" }}>{c[0]}</div>
    </AbsoluteFill>
  );
};

export const HavasuShort: React.FC = () => {
  const n = useCurrentFrame();
  const kit = useKit();
  useCaptionFont();
  if (!kit) return null;
  const flash = n >= NEW_FLASH_AT && n < NEW_FLASH_AT + 4 ? [1, 0.75, 0.45, 0.2][n - NEW_FLASH_AT] : 0;
  const end = n >= NEW_POSTER_AT + 14; // once the end card covers the frame, the 3D world stops rendering
  // layers: segment dissolves from the new timeline; inside one segment, in-shot camera cuts dissolve too
  type L = { id: number; of: number; alpha: number; pre?: number };
  const segs = segLayers(Math.min(n, NEW_POSTER_AT + 13));
  let layers: L[] = segs.map((l) => ({ id: SEGS[l.seg].shot, of: l.old, alpha: l.alpha }));
  if (layers.length === 1) {
    const { id, of } = layers[0], si = segs[0].seg;
    // cut dissolve lasts 6 new frames whatever the local speed of the old timeline
    const rate = Math.max(0.2, oldOf(si, n + 1) - oldOf(si, n)), pre = cutPre(id, of, 6 * rate);
    if (pre !== undefined) layers = [{ id, of, alpha: 1, pre }, { id, of, alpha: Math.min(1, (of - pre) / (6 * rate) + 1 / 7) }];
  }
  const fEnd = POSTER_AT + (n - NEW_POSTER_AT);
  return (
    <AbsoluteFill style={{ background: "#cfe3f2" }}>
      {!end && layers.map((l, i) => <ShotView key={i ? "over" : "base"} id={l.id} kit={kit} alpha={l.alpha} pre={l.pre} of={l.of} />)}
      {flash > 0 && <AbsoluteFill style={{ background: "#ffffff", opacity: flash }} />}
      {n >= NEW_POSTER_AT && <EndCard f={fEnd} />}
      <Captions f={n} />
    </AbsoluteFill>
  );
};
