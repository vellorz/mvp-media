// 2D cards for the Eiffel Tower short: protest letter, demolition notice, contract, calendar, weather vane, falling
// ball, radio set, radio waves, static, telegram, flags, paint bucket, lunch table. Same ink + flat fill as toon.ts.
import { Pen, INK } from "./toon";
type P2 = [number, number];
const rr = (x0: number, y0: number, x1: number, y1: number, r: number): P2[] => {
  const out: P2[] = [];
  const c: [number, number, number, number][] = [[x1 - r, y0 + r, -90, 0], [x1 - r, y1 - r, 0, 90], [x0 + r, y1 - r, 90, 180], [x0 + r, y0 + r, 180, 270]];
  for (const [cx, cy, a0, a1] of c) for (let i = 0; i <= 6; i++) { const a = ((a0 + ((a1 - a0) * i) / 6) * Math.PI) / 180; out.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); }
  return out;
};
const text = (p: Pen, s: string, x: number, y: number, size: number, fill: string, stroke = 0, font = "Georgia, 'Times New Roman', serif", bold = true) => {
  const g = p.g; g.font = `${bold ? "bold " : ""}${size}px ${font}`; g.textAlign = "center"; g.textBaseline = "middle";
  if (stroke) { g.lineWidth = stroke; g.strokeStyle = INK; g.lineJoin = "round"; g.strokeText(s, x, y); }
  g.fillStyle = fill; g.fillText(s, x, y);
};
const PAPER = "#f4ead2";

/** protest letter held up: parchment with a red wax seal and "USELESS / & MONSTROUS", 600 x 760 */
export const fxLetter = (p: Pen) => {
  p.poly([[40, 40], [560, 30], [570, 720], [30, 730]], PAPER, 12);
  text(p, "USELESS", 300, 170, 96, "#2b2830");
  text(p, "&", 300, 270, 70, "#2b2830");
  text(p, "MONSTROUS", 300, 370, 86, "#2b2830");
  for (let i = 0; i < 5; i++) p.stroke([[90, 470 + i * 40], [510 - (i % 2) * 60, 470 + i * 40]], 6, "#8a8070");
  p.ell(440, 650, 52, 52, "#b8322c", 8);
  p.ell(440, 650, 26, 26, null, 5);
};
/** demolition notice on a post: "DEMOLITION 1909", 600 x 900 (post foot at the bottom) */
export const fxDemolish = (p: Pen) => {
  p.poly(rr(270, 380, 330, 900, 6), "#8a5a34", 9);
  p.poly(rr(30, 50, 570, 430, 22), "#f2c230", 12);
  for (let i = -2; i < 7; i++) p.poly([[60 + i * 80, 60], [100 + i * 80, 60], [40 + i * 80, 120], [0 + i * 80, 120]].map(([x, y]) => [Math.max(42, Math.min(558, x)), y] as P2), "#2b2830", 0);
  text(p, "DEMOLITION", 300, 220, 74, "#2b2830");
  text(p, "1909", 300, 340, 120, "#c8352e", 10);
};
/** contract scroll: "20 YEARS" with a signature, 700 x 500 */
export const fxContract = (p: Pen) => {
  p.poly(rr(60, 40, 640, 460, 16), PAPER, 12);
  p.ell(60, 250, 30, 215, "#e2d4b0", 10); p.ell(640, 250, 30, 215, "#e2d4b0", 10);
  text(p, "PERMIT", 350, 110, 64, "#2b2830");
  text(p, "20 YEARS", 350, 230, 96, "#c8352e", 9);
  p.stroke([[170, 360], [220, 330], [250, 380], [300, 340], [340, 370], [390, 335]], 7, "#2d3f8a");
  p.stroke([[150, 400], [550, 400]], 5, "#8a8070");
};
/** desk calendar showing a year, 500 x 560 (two rings on top) */
export const fxCalendar = (p: Pen, year: string, flip = 0) => {
  p.poly(rr(40, 70, 460, 540, 24), "#ffffff", 12);
  p.poly(rr(40, 70, 460, 190, 24).map(([x, y]) => [x, Math.min(y, 190)] as P2), "#c8352e", 12);
  for (const x of [150, 350]) { p.ell(x, 70, 20, 34, null, 9); }
  const k = Math.max(0, Math.min(1, flip));
  text(p, year, 250, 360 - 40 * k, 150, "#2b2830");
  if (k > 0 && k < 1) p.poly([[40, 190], [460, 190], [460, 190 + 350 * (1 - k)], [40, 190 + 350 * (1 - k)]], "#f4f2ec", 10);
};
/** cup anemometer + wind vane on a pole, 500 x 700 (pole foot at the bottom) */
export const fxAnemo = (p: Pen, spin: number) => {
  p.band([[250, 700], [250, 230]], "#7d848c", 16, 5);
  for (let i = 0; i < 3; i++) {
    const a = spin + (i * Math.PI * 2) / 3, x = 250 + 150 * Math.cos(a), y = 200 + 40 * Math.sin(a);
    p.stroke([[250, 200], [x, y]], 8);
    p.ell(x, y, 34, 30, "#c9ccd2", 8, 0, 360);
  }
  p.ell(250, 200, 18, 18, "#2b2830", 0);
  p.poly([[250, 420], [430, 400], [470, 360], [400, 420], [470, 480], [430, 440]], "#c8352e", 8);
  p.poly([[250, 400], [250, 440], [140, 420]], "#c8352e", 8);
};
/** a heavy ball (falling-object experiment), 200 x 200 */
export const fxBall = (p: Pen) => { p.ell(100, 100, 80, 80, "#3a3d47", 10); p.ell(72, 70, 20, 14, "#9aa3ad", 0); };
/** wooden radio set with dials and a spark gap, 700 x 460 */
export const fxRadio = (p: Pen, glow = 0) => {
  p.poly(rr(40, 120, 660, 440, 18), "#8a5a34", 12);
  p.poly(rr(80, 160, 620, 400, 10), "#2b2830", 8);
  for (const x of [170, 300]) { p.ell(x, 280, 50, 50, "#e8d6a8", 8); p.stroke([[x, 280], [x + 30, 250]], 7, "#c8352e"); }
  p.poly(rr(400, 210, 580, 350, 8), glow > 0 ? "#ffe58a" : "#4a5a4a", 7);
  p.stroke([[600, 120], [600, 20]], 10); p.ell(600, 20, 14, 14, "#c9ccd2", 6);
};
/** expanding radio wave arcs (soft card), 800 x 800 */
export const fxWaves = (p: Pen, t: number) => {
  const g = p.g; g.lineCap = "round";
  for (let i = 0; i < 4; i++) {
    const r = 70 + ((t * 300 + i * 90) % 360), a = Math.max(0, 1 - r / 430);
    g.strokeStyle = `rgba(255,236,150,${a})`; g.lineWidth = 22;
    g.beginPath(); g.arc(400, 400, r, 0, Math.PI * 2); g.stroke();
    g.strokeStyle = `rgba(36,23,38,${a * 0.8})`; g.lineWidth = 5;
    g.beginPath(); g.arc(400, 400, r + 13, 0, Math.PI * 2); g.stroke();
  }
};
/** jagged static bolt (jamming), 500 x 300 */
export const fxStatic = (p: Pen, t: number) => {
  const j = (k: number) => 30 * Math.sin(t * 40 + k * 2.3);
  const pts: P2[] = [[20, 150], [90, 70 + j(1)], [160, 230 + j(2)], [240, 60 + j(3)], [320, 240 + j(4)], [400, 80 + j(5)], [480, 150]];
  p.stroke(pts, 30, INK); p.stroke(pts, 16, "#ffe14a");
};
/** telegram strip "STOP H-21 STOP", 900 x 300 */
export const fxTelegram = (p: Pen) => {
  p.poly([[20, 60], [880, 40], [890, 250], [30, 270]], PAPER, 12);
  p.stroke([[60, 92], [840, 76]], 4, "#8a8070");
  text(p, "AGENT H-21", 450, 165, 110, "#2b2830", 0, "'Courier New', Courier, monospace");
  p.stroke([[60, 238], [840, 222]], 4, "#8a8070");
};
/** French tricolour on a pole, 500 x 700 (pole foot at the bottom) */
export const fxFlagFR = (p: Pen, wave: number) => {
  p.band([[60, 700], [60, 40]], "#7d848c", 14, 5);
  const fx = (x: number, y: number): P2 => [x, y + 18 * Math.sin(wave + x / 70)];
  const cols = ["#2d4fa0", "#f6f2ea", "#d23b33"];
  for (let i = 0; i < 3; i++) {
    const x0 = 68 + i * 140, x1 = x0 + 140;
    p.poly([fx(x0, 60), fx(x1, 60), fx(x1, 340), fx(x0, 340)], cols[i], 0);
  }
  p.poly([fx(68, 60), fx(208, 60), fx(348, 60), fx(488, 60), fx(488, 340), fx(348, 340), fx(208, 340), fx(68, 340)], null, 10);
};
/** paint bucket with a dripping brush, 300 x 300 */
export const fxBucket = (p: Pen) => {
  p.poly([[60, 90], [240, 90], [220, 280], [80, 280]], "#9aa3ad", 10);
  p.ell(150, 90, 90, 22, "#7a5a3a", 8);
  p.arc(150, 90, 100, 90, 200, 340, 6);
};
/** bistro table with a plate, a glass and a bread loaf, seen from the front, 700 x 520 (feet at the bottom) */
export const fxTable = (p: Pen) => {
  p.poly([[330, 230], [370, 230], [380, 500], [320, 500]], "#3a3d47", 8);
  p.poly([[230, 500], [470, 500], [440, 470], [260, 470]], "#3a3d47", 6);
  p.poly(rr(40, 190, 660, 250, 14), "#f6f2ea", 10);
  for (let i = 0; i < 6; i++) p.poly([[60 + i * 100, 250], [110 + i * 100, 250], [100 + i * 100, 300], [70 + i * 100, 300]], i % 2 ? "#d23b33" : "#f6f2ea", 5);
  p.ell(300, 180, 110, 22, "#ffffff", 7); p.ell(300, 176, 60, 10, "#c98a4a", 0);
  p.poly([[480, 100], [530, 100], [520, 190], [490, 190]], "#bfe0f2", 6);
  p.poly([[480, 130], [530, 130], [525, 175], [485, 175]], "#8c2f3f", 0);
  p.ell(150, 170, 70, 20, "#d9a441", 7, 0, 360, -10);
};
/** wrecking ball, 400 x 400 */
export const fxWreck = (p: Pen) => { p.ell(200, 220, 160, 160, "#3a3d47", 12); p.ell(150, 160, 40, 26, "#7d848c", 0); p.ell(200, 50, 30, 30, "#7d848c", 10); };
