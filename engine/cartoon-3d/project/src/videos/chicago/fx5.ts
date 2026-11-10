// 2D cards for the Chicago short: a guest at a hotel window, cholera glass, labels that fit their text, the sewer plan,
// a "6 FT" measuring stick, rain, stink lines, OPEN sign, bread loaf, couch, scissor jack, screw lever, Pullman sleeping
// car, river arrow. Same ink + flat fill as toon.ts.
import { Pen, INK, bodyFront, Outfit, Expr } from "./toon";
type P2 = [number, number];
const rr = (x0: number, y0: number, x1: number, y1: number, r: number): P2[] => {
  const out: P2[] = [];
  const c: [number, number, number, number][] = [[x1 - r, y0 + r, -90, 0], [x1 - r, y1 - r, 0, 90], [x0 + r, y1 - r, 90, 180], [x0 + r, y0 + r, 180, 270]];
  for (const [cx, cy, a0, a1] of c) for (let i = 0; i <= 6; i++) { const a = ((a0 + ((a1 - a0) * i) / 6) * Math.PI) / 180; out.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); }
  return out;
};
const SANS = "'Arial Black', Arial, sans-serif";
/** centred text shrunk to fit maxW */
const fit = (p: Pen, s: string, x: number, y: number, size: number, maxW: number, fill: string, font = SANS, stroke = 0) => {
  const g = p.g;
  let z = size; g.font = `bold ${z}px ${font}`;
  while (g.measureText(s).width > maxW && z > 12) { z -= 3; g.font = `bold ${z}px ${font}`; }
  g.textAlign = "center"; g.textBaseline = "middle";
  if (stroke) { g.lineWidth = stroke; g.strokeStyle = INK; g.lineJoin = "round"; g.strokeText(s, x, y); }
  g.fillStyle = fill; g.fillText(s, x, y);
};

/** a guest at an open hotel window (the lower sash is up): room behind, waist-up character, trim + sill on top.
 *  Card = the window's trim box on the facade: 1.01 x 1.41 m -> 400 x 558 */
export const fxWindow = (p: Pen, o: Outfit, expr: Expr, blink: number, seed: number) => {
  const g = p.g, gx0 = 32, gy0 = 32, gx1 = 368, gy1 = 526;
  p.poly([[0, 0], [400, 0], [400, 558], [0, 558]], "#f7f2e8", 0);
  const gr = g.createLinearGradient(0, gy0, 0, gy1); gr.addColorStop(0, "#4a3f5c"); gr.addColorStop(1, "#2e2a40");
  g.fillStyle = gr; g.fillRect(gx0, gy0, gx1 - gx0, gy1 - gy0);
  g.fillStyle = "rgba(240,200,140,0.18)"; for (let x = gx0 + 20; x < gx1; x += 46) g.fillRect(x, gy0, 14, gy1 - gy0); // wallpaper stripes
  g.save(); g.beginPath(); g.rect(gx0, gy0 + 34, gx1 - gx0, gy1 - gy0 - 34); g.clip();
  const k = 0.855; g.translate(200 - 300 * k, gy0 + 4 - 175 * k); g.scale(k, k);
  bodyFront(p, o, { mode: "stand", expr, blink, prop: "teacup", facing: 0, seed });
  g.restore();
  // raised sash at the top, curtains, trim, sill
  g.fillStyle = "#8d9cdb"; g.fillRect(gx0, gy0, gx1 - gx0, 34);
  g.fillStyle = "#f7f2e8"; g.fillRect(gx0, gy0 + 30, gx1 - gx0, 10);
  g.fillStyle = "#c25a7a"; g.beginPath(); g.moveTo(gx0, gy0 + 40); g.lineTo(gx0 + 52, gy0 + 40); g.lineTo(gx0, gy0 + 280); g.fill();
  g.beginPath(); g.moveTo(gx1, gy0 + 40); g.lineTo(gx1 - 52, gy0 + 40); g.lineTo(gx1, gy0 + 280); g.fill();
  g.strokeStyle = INK; g.lineWidth = 6; g.strokeRect(gx0, gy0, gx1 - gx0, gy1 - gy0);
  g.fillStyle = "#ebe3d4"; g.fillRect(8, gy1, 384, 26); g.strokeRect(8, gy1, 384, 26);
};
/** glass of murky water with grinning germs, 300 x 420 */
export const fxGlass = (p: Pen) => {
  p.poly([[40, 40], [260, 40], [235, 400], [65, 400]], "#e8f3f6", 10);
  p.poly([[48, 120], [252, 120], [235, 392], [65, 392]], "#9a9a5a", 0);
  p.poly([[40, 40], [260, 40], [235, 400], [65, 400]], null, 10);
  for (const [x, y, r] of [[110, 200, 26], [190, 260, 30], [130, 330, 22], [200, 170, 18]] as const) {
    const pts: P2[] = []; for (let i = 0; i < 16; i++) { const a = (i / 16) * Math.PI * 2, rr2 = r * (i % 2 ? 1 : 1.35); pts.push([x + Math.cos(a) * rr2, y + Math.sin(a) * rr2]); }
    p.poly(pts, "#6fbf4a", 4);
    p.dot(x - r * 0.3, y - r * 0.15, 3.5); p.dot(x + r * 0.3, y - r * 0.15, 3.5); p.arc(x, y + r * 0.15, r * 0.4, r * 0.25, 10, 170, 3);
  }
};
/** label board with one or two lines, fitted, 800 x 360 */
export const fxLabel = (p: Pen, lines: string[], fill = "#f2c230", ink = "#2b2830") => {
  p.poly(rr(30, 40, 770, 330, 26), fill, 12);
  if (lines.length === 1) fit(p, lines[0], 400, 190, 150, 680, ink);
  else { fit(p, lines[0], 400, 130, 108, 680, ink); fit(p, lines[1], 400, 250, 108, 680, ink); }
};
/** the sewer plan: blueprint with a street section, pipe on top, new street over it, 600 x 420 */
export const fxPlan = (p: Pen) => {
  p.poly(rr(20, 30, 580, 400, 14), "#2d5aa8", 10);
  const w = "#e8f0ff";
  p.stroke([[60, 330], [540, 330]], 5, w);
  p.stroke([[60, 230], [540, 230]], 5, w);
  p.stroke([[60, 230], [60, 330]], 3, w); p.stroke([[540, 230], [540, 330]], 3, w);
  p.g.setLineDash([14, 10]); p.stroke([[60, 300], [540, 300]], 3, w); p.g.setLineDash([]);
  p.ell(300, 300, 38, 30, null, 0); p.g.strokeStyle = w; p.g.lineWidth = 5; p.g.beginPath(); p.g.ellipse(300, 300, 38, 30, 0, 0, Math.PI * 2); p.g.stroke();
  for (const x of [150, 450]) { p.stroke([[x, 320], [x, 245]], 5, w); p.stroke([[x - 14, 260], [x, 240], [x + 14, 260]], 5, w); }
  fit(p, "RAISE CITY", 300, 120, 70, 480, w);
};
/** measuring stick with foot marks and a "6 FT" tag, 220 x 760 (bottom = ground) */
export const fxRuler = (p: Pen) => {
  p.poly([[70, 140], [150, 140], [150, 750], [70, 750]], "#f2c230", 8);
  for (let i = 0; i <= 6; i++) { const y = 750 - (i * 610) / 6; p.stroke([[70, y], [i % 2 ? 110 : 130, y]], 6); }
  p.poly(rr(10, 20, 210, 130, 18), "#c8352e", 8);
  fit(p, "6 FT", 110, 76, 70, 170, "#ffffff");
};
/** falling rain streaks, soft card, 512 x 900; ph shifts the streaks down */
export const fxRain = (p: Pen, ph: number) => {
  const g = p.g; g.lineCap = "round";
  let s = 7;
  const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
  for (let i = 0; i < 90; i++) {
    const x = rnd() * 560 - 20, y0 = ((rnd() * 900 + ph * 900) % 900) - 60, L = 40 + rnd() * 50;
    g.strokeStyle = `rgba(225,238,255,${0.35 + 0.35 * rnd()})`; g.lineWidth = 2.5 + rnd() * 2;
    g.beginPath(); g.moveTo(x, y0); g.lineTo(x - L * 0.18, y0 + L); g.stroke();
  }
};
/** wavy stink lines, 300 x 360 */
export const fxStink = (p: Pen, ph: number) => {
  for (let k = 0; k < 3; k++) {
    const x0 = 70 + k * 80, pts: P2[] = [];
    for (let i = 0; i <= 16; i++) { const y = 340 - i * 19; pts.push([x0 + 18 * Math.sin(i * 0.8 + ph * 6 + k), y]); }
    p.line(pts, "#9bbf4a", 10);
  }
};
/** hanging OPEN sign, 400 x 260 */
export const fxOpen = (p: Pen) => {
  p.stroke([[120, 10], [80, 90]], 5); p.stroke([[280, 10], [320, 90]], 5); p.dot(200, 12, 9);
  p.poly(rr(30, 80, 370, 240, 18), "#f4ead2", 10);
  fit(p, "OPEN", 200, 162, 110, 300, "#c8352e", "Georgia, 'Times New Roman', serif");
};
/** bread loaf, 300 x 170 */
export const fxLoaf = (p: Pen) => {
  p.poly([[20, 140], [280, 140], [285, 100], [250, 40], [150, 20], [50, 40], [15, 100]], "#d9963f", 9);
  for (const x of [90, 150, 210]) p.stroke([[x - 20, 60], [x + 20, 90]], 7, "#f2c98a");
};
/** red velvet couch, front view, 900 x 520 (feet at the bottom) */
export const fxCouch = (p: Pen) => {
  p.poly(rr(70, 40, 830, 330, 60), "#b8463c", 11);           // back
  p.poly(rr(20, 180, 160, 470, 40), "#a33c34", 11);           // arms
  p.poly(rr(740, 180, 880, 470, 40), "#a33c34", 11);
  p.poly(rr(130, 300, 770, 440, 26), "#c9574a", 11);          // seat cushion
  p.stroke([[450, 305], [450, 435]], 7);
  for (const x of [230, 670]) p.ell(x, 175, 10, 10, "#8c2f2a", 5); // buttons
  for (const x of [90, 810]) p.poly([[x - 20, 470], [x + 20, 470], [x + 14, 515], [x - 14, 515]], "#6e4a30", 7);
};
/** scissor jack under the couch with its crank, open 0..1 (taller), 500 x 360 */
/** the couch split in two so the family sits ON it: back + arms + seat top behind them (900 x 520) ... */
export const fxCouchBack = (p: Pen) => {
  p.poly(rr(70, 40, 830, 330, 60), "#b8463c", 11);
  for (const x of [230, 670]) p.ell(x, 175, 10, 10, "#8c2f2a", 5);
  p.poly(rr(130, 290, 770, 360, 22), "#c9574a", 11);          // seat top
};
/** ... and the seat front, arm fronts and the two feet in front of their legs (900 x 520) */
export const fxCouchFront = (p: Pen) => {
  p.poly(rr(130, 330, 770, 440, 22), "#c0503f", 11);           // seat cushion front
  p.poly(rr(150, 430, 750, 496, 10), "#a33c34", 9);            // skirt under the cushion (hides the sitters' feet)
  for (let x = 190; x < 740; x += 40) p.stroke([[x, 448], [x, 488]], 3, "#7a2a24");
  p.stroke([[450, 336], [450, 434]], 7);
  p.poly(rr(20, 180, 160, 470, 40), "#a33c34", 11);           // arms
  p.poly(rr(740, 180, 880, 470, 40), "#a33c34", 11);
  for (const x of [90, 810]) p.poly([[x - 22, 470], [x + 22, 470], [x + 16, 516], [x - 16, 516]], "#6e4a30", 7);
};
export const fxJack = (p: Pen, open: number) => {
  const h = 140 + 120 * Math.max(0, Math.min(1, open)), cy = 340 - h / 2, w = 180 - 50 * open;
  p.poly([[100, 340], [400, 340], [380, 316], [120, 316]], "#5a5f68", 7);
  p.poly([[250 - w, cy], [250, 340 - 20], [250 + w, cy], [250, 340 - h + 20]], null, 0);
  p.line([[250 - w, cy], [250, 322]], "#c8352e", 14); p.line([[250, 322], [250 + w, cy]], "#c8352e", 14);
  p.line([[250 - w, cy], [250, 340 - h + 18]], "#c8352e", 14); p.line([[250, 340 - h + 18], [250 + w, cy]], "#c8352e", 14);
  p.poly([[160, 340 - h], [340, 340 - h], [330, 340 - h + 22], [170, 340 - h + 22]], "#5a5f68", 7);
  p.line([[250 + w, cy], [470, cy - 10]], "#8d949c", 9); p.ell(475, cy - 10, 14, 14, "#2b2830", 4);
};
/** iron lever bar for turning a jackscrew, 420 x 70 (rotate the card) */
export const fxLever = (p: Pen) => {
  p.line([[30, 35], [390, 35]], "#7d848c", 18);
  p.ell(210, 35, 26, 26, "#4a4d55", 7);
};
/** Pullman sleeping car, side view, with sleepy faces in the windows and a moon, 1000 x 520 */
export const fxSleeper = (p: Pen) => {
  p.ell(880, 90, 60, 60, "#f7e9a8", 8); p.ell(905, 75, 48, 48, "#cfe0f2", 0);
  p.poly(rr(40, 170, 960, 430, 30), "#2f5a43", 12);
  p.poly([[60, 170], [940, 170], [900, 130], [100, 130]], "#3b3f52", 10);
  p.poly(rr(60, 330, 940, 360, 8), "#d9a441", 6);
  fit(p, "PULLMAN", 500, 395, 52, 400, "#d9a441", "Georgia, 'Times New Roman', serif");
  for (let i = 0; i < 7; i++) {
    const x = 110 + i * 120;
    p.poly(rr(x, 200, x + 80, 300, 10), "#f2d38a", 6);
    p.ell(x + 40, 262, 22, 20, "#f1c9a6", 4); p.arc(x + 32, 258, 6, 3, 20, 160, 3); p.arc(x + 48, 258, 6, 3, 20, 160, 3);
    p.poly([[x + 16, 248], [x + 64, 248], [x + 52, 228], [x + 28, 228]], "#e8e2d0", 3); // nightcap
  }
  for (const x of [180, 300, 700, 820]) { p.ell(x, 450, 46, 46, "#2b2830", 8); p.ell(x, 450, 14, 14, "#8d949c", 4); }
  fit(p, "Z z z", 620, 100, 70, 220, "#f4f2ec", SANS, 8);
};
/** big flat arrow pointing +u, 600 x 300 */
export const fxArrow = (p: Pen, col = "#7a5a3a") => {
  p.poly([[30, 110], [380, 110], [380, 30], [570, 150], [380, 270], [380, 190], [30, 190]], col, 14);
};
/** clipboard with a tally of screws, 400 x 520 */
export const fxTally = (p: Pen) => {
  p.poly(rr(30, 40, 370, 500, 18), "#a8743f", 12);
  p.poly(rr(60, 80, 340, 470, 8), "#ffffff", 8);
  p.poly(rr(140, 20, 260, 80, 12), "#9aa3ad", 8);
  for (let r = 0; r < 4; r++) for (let k = 0; k < 5; k++) p.stroke([[100 + k * 18, 140 + r * 80], [100 + k * 18, 190 + r * 80]], 6);
  for (let r = 0; r < 4; r++) p.stroke([[90, 185 + r * 80], [196, 145 + r * 80]], 6, "#c8352e");
};
/** wooden easel (A-frame + back leg + ledge) that a board or calendar stands on, 400 x 800 (feet at the bottom) */
export const fxEasel = (p: Pen) => {
  p.poly([[180, 20], [222, 20], [250, 800], [212, 800]], "#6b4a30", 7); // back leg (darker, behind)
  p.poly([[150, 0], [186, 0], [66, 800], [26, 800]], "#9a6a3e", 8);
  p.poly([[214, 0], [250, 0], [374, 800], [334, 800]], "#9a6a3e", 8);
  p.poly([[40, 560], [360, 560], [360, 596], [40, 596]], "#9a6a3e", 7);
  p.poly([[20, 0], [380, 0], [380, 40], [20, 40]], "#8a5a34", 7); // ledge under the board
};
/** two sign posts with a cross rail, 600 x 800 (feet at the bottom) */
export const fxPosts = (p: Pen) => {
  for (const x of [110, 450]) p.poly([[x, 0], [x + 46, 0], [x + 46, 800], [x, 800]], "#8a5a34", 9);
  p.poly([[90, 300], [510, 300], [510, 340], [90, 340]], "#8a5a34", 7);
};
