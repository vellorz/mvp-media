// New 2D cards for the London Bridge short: traffic (bus, cars), FOR SALE sign, money bag, thought bubble with a
// Tower Bridge doodle, tumbleweed, bubbles, foam, honk lines. Same ink and flat-fill language as toon.ts.
import { Pen, INK } from "./toon";
type P2 = [number, number];
const rr = (x0: number, y0: number, x1: number, y1: number, r: number): P2[] => {
  const out: P2[] = [];
  const c: [number, number, number, number][] = [[x1 - r, y0 + r, -90, 0], [x1 - r, y1 - r, 0, 90], [x0 + r, y1 - r, 90, 180], [x0 + r, y0 + r, 180, 270]];
  for (const [cx, cy, a0, a1] of c) for (let i = 0; i <= 6; i++) { const a = ((a0 + ((a1 - a0) * i) / 6) * Math.PI) / 180; out.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); }
  return out;
};
const wheel = (p: Pen, x: number, y: number, r: number) => { p.ell(x, y, r, r, "#2b2830", 8); p.ell(x, y, r * 0.45, r * 0.45, "#c9ccd2", 6); };

/** red double-decker bus, side view facing right, on a 1000 x 560 canvas (wheels touch y 540) */
export const fxBus = (p: Pen) => {
  const RED = "#d23b33";
  p.poly(rr(40, 40, 960, 470, 50), RED, 12);
  for (const y of [80, 280]) for (let i = 0; i < 6; i++) p.poly(rr(110 + i * 132, y, 220 + i * 132, y + 120, 16), "#bfe0f2", 7);
  p.poly(rr(860, 300, 940, 470, 10), "#bfe0f2", 7);
  p.band([[40, 240], [960, 240]], "#f3eddc", 18, 5);
  p.poly(rr(40, 440, 960, 478, 10), "#2b2830", 0);
  wheel(p, 210, 480, 62); wheel(p, 780, 480, 62);
  p.ell(940, 430, 16, 16, "#ffe58a", 5);
};
/** small car, side view facing right, 700 x 360 canvas */
export const fxCar = (p: Pen, col: string) => {
  p.poly([[40, 290], [40, 200], [120, 180], [200, 90], [460, 90], [560, 180], [650, 200], [660, 290]], col, 11);
  p.poly([[225, 110], [330, 110], [330, 180], [165, 180]], "#bfe0f2", 7);
  p.poly([[350, 110], [450, 110], [530, 180], [350, 180]], "#bfe0f2", 7);
  p.ell(650, 230, 12, 14, "#ffe58a", 4);
  wheel(p, 170, 290, 52); wheel(p, 530, 290, 52);
};
/** honk lines (3 strokes fanning out), 300 x 300 */
export const fxHonk = (p: Pen, t: number) => {
  const j = 8 * Math.sin(t * 30);
  for (const a of [-28, 0, 28]) { const b = (a * Math.PI) / 180; p.stroke([[60 + 60 * Math.cos(b), 150 + 60 * Math.sin(b) + j], [60 + 200 * Math.cos(b), 150 + 200 * Math.sin(b) + j]], 14); }
};
/** FOR SALE sign on a post, 600 x 900 (post foot at the bottom) */
export const fxForSale = (p: Pen) => {
  p.poly(rr(270, 380, 330, 900, 6), "#8a5a34", 9);
  p.poly(rr(40, 60, 560, 420, 26), "#f6ecd2", 12);
  p.poly(rr(64, 84, 536, 396, 16), null, 5);
  const g = p.g;
  g.font = "bold 128px Georgia, 'Times New Roman', serif"; g.textAlign = "center"; g.textBaseline = "middle";
  g.lineWidth = 10; g.strokeStyle = INK; g.fillStyle = "#cf2f2f";
  g.strokeText("FOR", 300, 168); g.fillText("FOR", 300, 168);
  g.strokeText("SALE", 300, 300); g.fillText("SALE", 300, 300);
  for (const x of [80, 520]) p.dot(x, 100, 9, "#7d848c");
};
/** money sack with a dollar sign, 400 x 440 (bottom at 430) */
export const fxBag = (p: Pen, squash = 0) => {
  const sx = 1 + 0.18 * squash, sy = 1 - 0.18 * squash, cx = 200, by = 430;
  const P = (x: number, y: number): P2 => [cx + (x - cx) * sx, by + (y - by) * sy];
  const body: P2[] = [];
  for (let i = 0; i <= 40; i++) { const a = (i / 40) * Math.PI * 2; body.push(P(200 + 165 * Math.cos(a), 300 + 130 * Math.sin(a) * (Math.sin(a) > 0 ? 1 : 1.1))); }
  p.poly(body, "#c99a5a", 12);
  p.poly([P(140, 180), P(260, 180), P(290, 110), P(110, 110)], "#c99a5a", 12);
  p.band([P(130, 182), P(270, 182)], "#8a5a34", 18, 5);
  const g = p.g; g.font = "bold 170px Georgia, serif"; g.textAlign = "center"; g.textBaseline = "middle";
  const [tx, ty] = P(200, 312); g.lineWidth = 10; g.strokeStyle = INK; g.fillStyle = "#3f7d3a"; g.strokeText("$", tx, ty); g.fillText("$", tx, ty);
};
/** thought bubble with a doodle of Tower Bridge, 760 x 640; the small trail bubbles run to the bottom-left corner */
export const fxThought = (p: Pen) => {
  const lobes: [number, number, number][] = [[250, 230, 120], [380, 170, 140], [520, 220, 125], [600, 320, 100], [470, 380, 120], [300, 370, 120], [180, 320, 95]];
  for (const [x, y, r] of lobes) p.ell(x, y, r, r * 0.85, null, 14);
  for (const [x, y, r] of lobes) p.ell(x, y, r - 4, r * 0.85 - 4, "#ffffff", 0);
  p.ell(120, 520, 36, 30, "#ffffff", 10); p.ell(60, 600, 20, 17, "#ffffff", 8);
  // the doodle
  const STONE = "#d9c7a6", BLUE = "#6f9cc9";
  p.poly([[160, 395], [640, 395], [640, 412], [160, 412]], "#6fb0d8", 0);
  for (const x of [300, 500]) {
    p.poly([[x - 34, 400], [x + 34, 400], [x + 30, 220], [x - 30, 220]], STONE, 7);
    p.poly([[x - 36, 222], [x + 36, 222], [x, 160]], "#8a96a8", 7);
    for (const dx of [-30, 30]) p.poly([[x + dx - 9, 224], [x + dx + 9, 224], [x + dx, 196]], "#8a96a8", 5);
    p.poly(rr(x - 13, 300, x + 13, 350, 10), "#3a3d47", 0);
  }
  p.band([[334, 245], [466, 245]], BLUE, 12, 5);
  p.band([[334, 330], [400, 318]], BLUE, 12, 5); p.band([[400, 318], [466, 330]], BLUE, 12, 5);
  p.stroke([[266, 240], [190, 330], [170, 335]], 8, BLUE); p.stroke([[534, 240], [610, 330], [630, 335]], 8, BLUE);
  p.band([[170, 340], [266, 336]], BLUE, 10, 4); p.band([[534, 336], [630, 340]], BLUE, 10, 4);
};
/** tumbleweed, 300 x 300 */
export const fxTumble = (p: Pen) => {
  const g = p.g; g.strokeStyle = "#a07440"; g.lineWidth = 9; g.lineCap = "round";
  for (let i = 0; i < 26; i++) {
    const a0 = i * 2.39, r0 = 40 + ((i * 37) % 90);
    g.beginPath(); g.arc(150 + 20 * Math.cos(a0), 150 + 20 * Math.sin(a0), r0, a0, a0 + 2.2); g.stroke();
  }
  g.strokeStyle = "rgba(36,23,38,0.8)"; g.lineWidth = 3;
  for (let i = 0; i < 10; i++) { const a0 = i * 1.7, r0 = 60 + ((i * 53) % 70); g.beginPath(); g.arc(150, 150, r0, a0, a0 + 1.6); g.stroke(); }
};
/** rising bubble, 120 x 120 */
export const fxBubble = (p: Pen) => { p.ell(60, 60, 44, 44, "#d8f0ff", 7); p.ell(46, 44, 10, 8, "#ffffff", 0); };
/** foam streak (top-down, flat), 600 x 200 */
export const fxFoam = (p: Pen, t: number) => {
  for (let i = 0; i < 7; i++) { const x = 60 + i * 75 + 20 * Math.sin(t * 3 + i), w = 50 + 20 * Math.sin(i * 1.7 + t * 2); p.ell(x, 100 + 30 * Math.sin(i * 2.1), w, 22, `rgba(250,253,255,${0.85 - i * 0.09})`, 0); }
};
/** a soft speed line card (motion), 400 x 120 */
export const fxSpeed = (p: Pen) => { for (let i = 0; i < 3; i++) p.stroke([[20 + i * 40, 30 + i * 30], [380 - i * 60, 30 + i * 30]], 10); };
