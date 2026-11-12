// 2D cards for the Leaning Tower of Pisa short: clipboard, CLOSED barrier, spirit level, soil cross-section, sponge,
// city flags (Genoa, Lucca, Florence), banana, angle badge, lead sign, drill rig, "45 cm" tag, tools on the grass.
// Same ink + flat fill as toon.ts.
import { Pen, INK } from "./toon";
type P2 = [number, number];
const rr = (x0: number, y0: number, x1: number, y1: number, r: number): P2[] => {
  const out: P2[] = [];
  const c: [number, number, number, number][] = [[x1 - r, y0 + r, -90, 0], [x1 - r, y1 - r, 0, 90], [x0 + r, y1 - r, 90, 180], [x0 + r, y0 + r, 180, 270]];
  for (const [cx, cy, a0, a1] of c) for (let i = 0; i <= 6; i++) { const a = ((a0 + ((a1 - a0) * i) / 6) * Math.PI) / 180; out.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); }
  return out;
};
const text = (p: Pen, s: string, x: number, y: number, size: number, fill: string, stroke = 0, font = "Georgia, 'Times New Roman', serif") => {
  const g = p.g; g.font = `bold ${size}px ${font}`; g.textAlign = "center"; g.textBaseline = "middle";
  if (stroke) { g.lineWidth = stroke; g.strokeStyle = INK; g.lineJoin = "round"; g.strokeText(s, x, y); }
  g.fillStyle = fill; g.fillText(s, x, y);
};
const SANS = "'Arial Black', Arial, sans-serif";

/** clipboard with a tower sketch, 400 x 520 */
export const fxClip = (p: Pen) => {
  p.poly(rr(30, 40, 370, 500, 18), "#a8743f", 12);
  p.poly(rr(60, 80, 340, 470, 8), "#ffffff", 8);
  p.poly(rr(140, 20, 260, 80, 12), "#9aa3ad", 8);
  p.poly([[175, 420], [225, 420], [245, 150], [195, 150]], "#efe7d6", 6);
  for (let i = 0; i < 6; i++) p.stroke([[178 + i * 11 - 3, 410 - i * 44], [226 + i * 3.7, 410 - i * 44]], 4, "#8a8070");
  p.stroke([[100, 440], [300, 440]], 5, "#c8352e");
};
/** striped barrier with a CLOSED sign, 900 x 600 (feet at the bottom) */
export const fxClosed = (p: Pen) => {
  for (const x of [120, 780]) p.poly([[x - 60, 600], [x + 60, 600], [x + 18, 330], [x - 18, 330]], "#c8352e", 9);
  p.poly(rr(40, 300, 860, 400, 14), "#ffffff", 11);
  for (let i = 0; i < 8; i++) p.poly([[70 + i * 105, 302], [120 + i * 105, 302], [80 + i * 105, 398], [30 + i * 105, 398]].map(([x, y]) => [Math.max(46, Math.min(854, x)), y] as P2), "#c8352e", 0);
  p.poly(rr(40, 300, 860, 400, 14), null, 11);
  p.poly(rr(200, 40, 700, 270, 20), "#f2c230", 11);
  text(p, "CLOSED", 450, 125, 104, "#2b2830", 0, SANS);
  text(p, "1990", 450, 220, 70, "#c8352e", 0, SANS);
};
/** spirit level, bubble offset k in -1..1, 700 x 200 */
export const fxLevel = (p: Pen, k: number) => {
  p.poly(rr(20, 50, 680, 160, 18), "#f2c230", 11);
  p.poly(rr(250, 70, 450, 140, 24), "#bfe8a0", 8);
  p.stroke([[330, 70], [330, 140]], 5); p.stroke([[370, 70], [370, 140]], 5);
  p.ell(350 + 70 * Math.max(-1, Math.min(1, k)), 105, 22, 18, "#ffffff", 5);
};
/** ground cross-section: grass, soft clay, wet sand, water drops; packed (0..1) squeezes the layers and adds arrows. 800 x 560 */
export const fxSoil = (p: Pen, packed = 0) => {
  const c = Math.max(0, Math.min(1, packed)), y1 = 150 + 30 * c;
  p.poly(rr(30, 40, 770, 540, 26), "#a9744a", 12);
  p.poly([[42, 52], [758, 52], [758, y1 - 40], [42, y1 - 40]], "#6fbf4a", 0);
  p.poly([[42, y1 - 40], [758, y1 - 40], [758, 330], [42, 330]], "#8c6248", 0);
  p.poly([[42, 330], [758, 330], [758, 528], [42, 528]], "#e0c084", 0);
  for (let i = 0; i < 14; i++) p.ell(80 + ((i * 97) % 640), 370 + ((i * 53) % 140), 9, 13, "#7cc4ee", 4);
  text(p, "CLAY", 400, 240, 70, "#f4ead2", 8, SANS);
  text(p, "SAND", 400, 430, 70, "#f4ead2", 8, SANS);
  p.poly(rr(30, 40, 770, 540, 26), null, 12);
  if (c > 0) for (const x of [180, 620]) { p.stroke([[x, 60], [x, 60 + 120 * c]], 22, INK); p.poly([[x - 36, 50 + 120 * c], [x + 36, 50 + 120 * c], [x, 105 + 120 * c]], "#ffe14a", 8); }
};
/** wet kitchen sponge, squish 0..1 flattens it, 700 x 400 (bottom edge at the bottom) */
export const fxSponge = (p: Pen, squish = 0) => {
  const s = Math.max(0, Math.min(1, squish)), top = 120 + 140 * s;
  p.poly(rr(40, top, 660, 380, 30), "#f2d23a", 12);
  p.poly(rr(40, top, 660, top + 50, 24), "#3f9a52", 10);
  for (let i = 0; i < 12; i++) p.ell(90 + ((i * 131) % 520), top + 90 + ((i * 47) % Math.max(20, 270 - 140 * s - 90)), 14, 10 - 4 * s, "#c9a51e", 0);
  for (let i = 0; i < 5; i++) p.ell(120 + i * 120, 392, 12, 7, "#7cc4ee", 4);
};
/** city flag on a pole: Genoa (red cross on white), Lucca (white over red), Florence (red lily on white). 500 x 700 */
export const fxCityFlag = (p: Pen, city: 0 | 1 | 2, wave: number) => {
  p.band([[60, 700], [60, 40]], "#7d848c", 14, 5);
  const fx = (x: number, y: number): P2 => [x, y + 16 * Math.sin(wave + x / 70)];
  const poly = (pts: P2[], c: string) => p.poly(pts.map(([x, y]) => fx(x, y)), c, 0);
  poly([[68, 60], [468, 60], [468, 330], [68, 330]], city === 1 ? "#f6f2ea" : "#f6f2ea");
  if (city === 0) { poly([[228, 60], [308, 60], [308, 330], [228, 330]], "#d23b33"); poly([[68, 160], [468, 160], [468, 230], [68, 230]], "#d23b33"); }
  if (city === 1) poly([[68, 195], [468, 195], [468, 330], [68, 330]], "#d23b33");
  if (city === 2) { const [cx, cy] = fx(268, 190); p.poly([[cx, cy - 90], [cx + 30, cy - 10], [cx + 90, cy - 50], [cx + 40, cy + 40], [cx + 70, cy + 90], [cx, cy + 50], [cx - 70, cy + 90], [cx - 40, cy + 40], [cx - 90, cy - 50], [cx - 30, cy - 10]], "#d23b33", 6); }
  p.poly([fx(68, 60), fx(268, 60), fx(468, 60), fx(468, 330), fx(268, 330), fx(68, 330)], null, 10);
};
/** a banana standing on its end with the same curve as the tower, 400 x 1000 */
export const fxBanana = (p: Pen) => {
  const L: P2[] = [], R: P2[] = [];
  for (let i = 0; i <= 20; i++) { const u = i / 20, y = 960 - 900 * u, x = 200 - 150 * Math.sin(u * 1.2) + 120 * u * u, w = 70 * Math.sin(Math.PI * Math.min(1, 0.12 + u * 0.9)) + 14; L.push([x - w, y]); R.push([x + w, y]); }
  p.poly([...L, ...R.reverse()], "#f6d43a", 12);
  p.stroke(L.map(([x, y]) => [x + 40, y] as P2).slice(3, 18), 6, "#c9a51e");
  p.poly([[L[20][0] + 40, 60], [L[20][0] + 90, 60], [L[20][0] + 80, 20], [L[20][0] + 50, 20]], "#6b4a2a", 8);
  p.ell(200 - 0 + 20, 958, 36, 14, "#4a3426", 0);
};
/** angle badge: a vertical line, the leaning line and the arc, with a label, 600 x 600 */
export const fxAngle = (p: Pen, label: string) => {
  p.ell(300, 300, 270, 270, "#ffffff", 12);
  p.stroke([[300, 520], [300, 110]], 10, "#8a8070");
  p.stroke([[300, 520], [372, 110]], 14, "#c8352e");
  p.arc(300, 520, 300, 300, 260, 280, 8);
  text(p, label, 300, 420, 110, "#2b2830", 0, SANS);
};
/** big hanging tag with text, 800 x 360 */
export const fxTag = (p: Pen, s: string, fill = "#f2c230", ink = "#2b2830") => {
  p.poly(rr(30, 60, 770, 330, 26), fill, 12);
  p.ell(400, 40, 22, 22, null, 8);
  text(p, s, 400, 198, s.length > 7 ? 110 : 140, ink, 0, SANS);
};
/** drilling rig: frame, motor, spinning auger (spin = phase), 500 x 800 (feet at the bottom) */
export const fxDrill = (p: Pen, spin: number) => {
  p.poly([[60, 800], [110, 800], [230, 80], [200, 80]], "#d9822b", 9);
  p.poly([[440, 800], [390, 800], [270, 80], [300, 80]], "#d9822b", 9);
  p.poly(rr(170, 40, 330, 150, 14), "#c8352e", 10);
  p.poly(rr(220, 150, 280, 780, 8), "#9aa3ad", 8);
  for (let i = 0; i < 9; i++) { const y = 190 + ((i * 70 + spin * 70) % 590); p.stroke([[214, y], [286, y + 34]], 9, "#5a6068"); }
  p.poly([[90, 790], [410, 790], [380, 760], [120, 760]], "#5a4a3a", 6);
};
/** a mound of dug soil, 500 x 300 */
export const fxMound = (p: Pen) => { p.poly([[20, 290], [480, 290], [400, 150], [300, 80], [190, 100], [90, 180]], "#8c6248", 11); p.ell(240, 160, 30, 16, "#a87a58", 0); p.ell(350, 210, 24, 12, "#a87a58", 0); };
/** abandoned tools in the grass: hammer, spirit level, trowel, 700 x 260 */
export const fxTools = (p: Pen) => {
  p.poly(rr(40, 150, 360, 200, 12), "#f2c230", 9);
  p.stroke([[420, 220], [600, 120]], 16, "#8a5a34"); p.poly([[560, 80], [660, 130], [640, 170], [540, 120]], "#5a6068", 8);
  p.poly([[120, 240], [240, 230], [180, 120]], "#9aa3ad", 8); p.stroke([[180, 120], [200, 60]], 12, "#8a5a34");
};
/** "STOP" hand sign held up, 400 x 500 */
export const fxStop = (p: Pen) => {
  const o: P2[] = []; for (let i = 0; i < 8; i++) { const a = ((i + 0.5) / 8) * Math.PI * 2; o.push([200 + 170 * Math.cos(a), 200 + 170 * Math.sin(a)]); }
  p.stroke([[200, 360], [200, 500]], 16, "#7d848c"); p.poly(o, "#c8352e", 12);
  text(p, "STOP", 200, 205, 96, "#ffffff", 0, SANS);
};
