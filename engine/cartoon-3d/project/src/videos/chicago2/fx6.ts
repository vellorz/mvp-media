// v2 in-world cards for the Chicago redesign (DETAIL_STANDARD F2: documents and mechanisms live IN the world, no labels,
// no arrows, no date cards). Muted, greyed palette (F3). Same ink + flat fill as toon.ts.
import { Pen, INK } from "./toon";
type P2 = [number, number];
const rr = (x0: number, y0: number, x1: number, y1: number, r: number): P2[] => {
  const out: P2[] = [];
  const c: [number, number, number, number][] = [[x1 - r, y0 + r, -90, 0], [x1 - r, y1 - r, 0, 90], [x0 + r, y1 - r, 90, 180], [x0 + r, y0 + r, 180, 270]];
  for (const [cx, cy, a0, a1] of c) for (let i = 0; i <= 6; i++) { const a = ((a0 + ((a1 - a0) * i) / 6) * Math.PI) / 180; out.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); }
  return out;
};
const SERIF = "Georgia, 'Times New Roman', serif";
const SANS = "'Arial Black', Arial, sans-serif";
const fit = (p: Pen, s: string, x: number, y: number, size: number, maxW: number, fill: string, font = SERIF) => {
  const g = p.g;
  let z = size; g.font = `bold ${z}px ${font}`;
  while (g.measureText(s).width > maxW && z > 10) { z -= 2; g.font = `bold ${z}px ${font}`; }
  g.textAlign = "center"; g.textBaseline = "middle"; g.fillStyle = fill; g.fillText(s, x, y);
};
const lines = (p: Pen, x0: number, x1: number, y0: number, y1: number, gap: number, col = "#8f8778", w = 4) => {
  let s = 3; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
  for (let y = y0; y < y1; y += gap) p.stroke([[x0, y], [x1 - rnd() * (x1 - x0) * 0.25, y]], w, col);
};
const k01 = (v: number) => Math.max(0, Math.min(1, v));

/** a city newspaper pasted on a brick wall, 1854, cholera headline. 500 x 680. The date lives on the masthead (F2). */
export const fxNews = (p: Pen) => {
  p.poly([[18, 22], [486, 10], [492, 668], [10, 662]], "#e9e1cc", 8);
  p.g.fillStyle = "rgba(160,140,100,0.18)"; p.g.fillRect(30, 30, 440, 620);
  fit(p, "THE CHICAGO DAILY", 250, 72, 46, 420, "#2a2622");
  p.stroke([[40, 104], [460, 104]], 4, "#2a2622"); p.stroke([[40, 136], [460, 136]], 2, "#2a2622");
  fit(p, "JULY 1854", 250, 120, 22, 200, "#2a2622");
  fit(p, "CHOLERA!", 250, 196, 104, 430, "#7a1f1c", SANS);
  fit(p, "SIX IN EVERY HUNDRED DEAD", 250, 262, 30, 420, "#2a2622");
  p.stroke([[40, 290], [460, 290]], 3, "#2a2622");
  // engraving: a water pump with a skull in the puddle
  p.poly([[70, 320], [240, 320], [240, 500], [70, 500]], "#d6cdb4", 4);
  p.poly([[130, 350], [170, 350], [170, 470], [130, 470]], "#5a5650", 5);
  p.line([[170, 365], [215, 345]], "#5a5650", 8); p.line([[130, 380], [100, 380], [100, 395]], "#5a5650", 8);
  p.ell(155, 485, 60, 10, "#8a9a7a", 4); p.ell(155, 478, 12, 10, "#f2ecd8", 3); p.dot(151, 477, 2.5); p.dot(159, 477, 2.5);
  lines(p, 260, 460, 330, 500, 22);
  lines(p, 40, 460, 530, 650, 22);
  // torn corner and paste stains
  p.poly([[492, 600], [492, 668], [430, 664]], "#7a4a3a", 0);
  p.g.fillStyle = "rgba(120,100,60,0.22)"; p.g.beginPath(); p.g.ellipse(380, 600, 60, 30, 0.3, 0, Math.PI * 2); p.g.fill();
};

/** the same page lying soggy in the mud, seen from above, crumpled + brown water stains. 500 x 380 (flat card) */
export const fxSoggy = (p: Pen) => {
  p.poly([[30, 60], [250, 20], [470, 70], [455, 330], [260, 360], [40, 320]], "#d4cab0", 7);
  p.g.fillStyle = "rgba(90,70,40,0.35)"; for (const [x, y, a, b] of [[120, 280, 90, 50], [380, 110, 70, 40], [300, 300, 60, 30]]) { p.g.beginPath(); p.g.ellipse(x, y, a, b, 0.4, 0, Math.PI * 2); p.g.fill(); }
  p.g.save(); p.g.translate(250, 120); p.g.rotate(-0.08); fit(p, "CHOLERA!", 0, 0, 74, 330, "#6a2a24", SANS); p.g.restore();
  lines(p, 80, 420, 180, 300, 20, "#8a8070", 4);
  for (const [a, b] of [[[150, 40], [180, 340]], [[330, 45], [300, 350]]] as [P2, P2][]) p.stroke([a, b], 2.5, "#a89c80");
};

/** the sewer plan on the council table, seen from above: a street section; the pipe is DRAWN ON as "lay the new
 *  sewers" is spoken (k 0..1), then the new street line (k2 0..1). 700 x 500 (flat card) */
export const fxPlan2 = (p: Pen, k: number, k2: number) => {
  p.poly([[20, 30], [680, 18], [690, 480], [14, 488]], "#2f4f86", 8);
  const w = "#e3ebf7";
  p.g.globalAlpha = 0.25; for (let x = 60; x < 660; x += 40) p.stroke([[x, 40], [x, 470]], 1.5, w); for (let y = 60; y < 470; y += 40) p.stroke([[30, y], [680, y]], 1.5, w); p.g.globalAlpha = 1;
  fit(p, "CITY OF CHICAGO", 350, 70, 34, 420, w);
  fit(p, "SECTION OF STREET", 350, 108, 22, 300, w);
  // houses + old street line
  for (const x of [70, 520]) { p.poly([[x, 380], [x + 110, 380], [x + 110, 250], [x + 55, 200], [x, 250]], null, 0); p.g.strokeStyle = w; p.g.lineWidth = 4; p.g.beginPath(); p.g.moveTo(x, 380); p.g.lineTo(x, 250); p.g.lineTo(x + 55, 200); p.g.lineTo(x + 110, 250); p.g.lineTo(x + 110, 380); p.g.stroke(); }
  p.stroke([[40, 380], [660, 380]], 5, w);
  // the pipe drawn left to right
  if (k > 0) {
    const x1 = 190 + 330 * k01(k);
    p.stroke([[190, 336], [x1, 336]], 4, "#f2d27a"); p.stroke([[190, 372], [x1, 372]], 4, "#f2d27a");
    if (k >= 1) { p.g.strokeStyle = "#f2d27a"; p.g.lineWidth = 4; p.g.beginPath(); p.g.ellipse(190, 354, 9, 18, 0, 0, Math.PI * 2); p.g.stroke(); }
  }
  if (k2 > 0) { p.g.setLineDash([16, 10]); p.stroke([[40, 316], [40 + 620 * k01(k2), 316]], 4, "#f2d27a"); p.g.setLineDash([]); }
  // pencil + coffee ring
  p.g.strokeStyle = "rgba(120,80,40,0.45)"; p.g.lineWidth = 6; p.g.beginPath(); p.g.ellipse(600, 150, 34, 30, 0, 0, Math.PI * 2); p.g.stroke();
};

/** the cross-section model on the council table, drawn like a painted diorama (ref: cut-away earth layers with pebbles
 *  and a worm, grass on top, a painted sky behind the glass): the old street with the brick sewer lying on it, the new
 *  earth fill rising over it (fill 0..1) and two little houses jacked up on screws (lift 0..1). 800 x 520 */
export const fxModel = (p: Pen, fill: number, lift: number) => {
  const g = p.g, base = 470, street = 372, fillTop = street - 118 * k01(fill), up = 118 * k01(lift);
  let s = 11; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
  // wooden base with drawn grain + a brass plate
  p.poly(rr(26, 436, 774, 512, 8), "#7a5034", 8);
  for (let k = 0; k < 4; k++) p.stroke([[40, 452 + k * 14], [760, 450 + k * 14 + (k % 2) * 3]], 2, "#5a3a24");
  p.poly(rr(330, 470, 470, 500, 4), "#c9a24a", 4); fit(p, "PLAN No. 1", 400, 485, 18, 120, "#3a2a1a");
  // painted sky + far roofs behind the glass
  const sky = g.createLinearGradient(0, 120, 0, street); sky.addColorStop(0, "#9fb4d8"); sky.addColorStop(1, "#e3d8c4");
  g.fillStyle = sky; g.fillRect(50, 120, 700, street - 120);
  for (let x = 60; x < 740; x += 46) { const h = 30 + rnd() * 40; g.fillStyle = "#b8b4c4"; g.fillRect(x, street - 46 - h, 40, h + 46); }
  for (const [cx, cy] of [[180, 170], [560, 150]]) { g.fillStyle = "#f6f3ee"; for (const [dx, r0] of [[0, 22], [22, 16], [-20, 14]]) { g.beginPath(); g.arc(cx + dx, cy, r0, 0, 7); g.fill(); } }
  // earth layers below the old street: topsoil, clay, sand + pebbles, a worm, wet blue clay at the bottom
  const layers: [number, number, string][] = [[street, street + 26, "#6a4a34"], [street + 26, street + 54, "#b0663e"], [street + 54, base - 14, "#c8a46a"], [base - 14, base, "#5a6a8a"]];
  for (const [a, b, c] of layers) { g.fillStyle = c; g.fillRect(50, a, 700, b - a); p.stroke([[50, b], [750, b]], 2.5, "#3a2a24"); }
  for (let i = 0; i < 40; i++) { const x = 60 + rnd() * 680, y = street + 30 + rnd() * 60; p.ell(x, y, 3 + rnd() * 4, 2 + rnd() * 3, ["#e8e0d0", "#9a948a", "#c8beb0"][i % 3], 1.5); }
  p.line([[140, street + 40], [150, street + 36], [160, street + 41], [170, street + 37]], "#d98a8a", 4);
  // the old (sunken) street surface: mud with ruts and tiny plank sidewalks
  g.fillStyle = "#8a7258"; g.fillRect(50, street - 8, 700, 8); p.stroke([[50, street - 8], [750, street - 8]], 3);
  // the sewer: a brick pipe lying ON the street, drawn bricks
  p.poly(rr(90, street - 52, 710, street - 8, 22), "#b06a4a", 6);
  for (let y = street - 46; y < street - 12; y += 9) for (let x = 100 + ((y / 9) % 2) * 9; x < 700; x += 18) p.stroke([[x, y], [x + 14, y]], 1.5, "#7a3a2a");
  p.ell(90, street - 30, 10, 22, "#2a2228", 4);
  // the new fill, drawn in front of the pipe: tipped earth with stones and a little wheelbarrow on top
  if (fill > 0) {
    g.fillStyle = "#9a7a52"; g.fillRect(50, fillTop, 700, street - fillTop);
    for (let i = 0; i < 26; i++) { const x = 60 + rnd() * 680, y = fillTop + 6 + rnd() * Math.max(4, street - fillTop - 12); p.ell(x, y, 3 + rnd() * 3, 2 + rnd() * 2, "#c8beb0", 1.2); }
    for (let i = 0; i < 6; i++) { const x = 70 + rnd() * 660; p.stroke([[x, fillTop + 4], [x + 20, fillTop + 10]], 2, "#6a5038"); }
    g.fillStyle = "#6f8a4a"; g.fillRect(50, fillTop - 5, 700, 7); p.stroke([[50, fillTop - 5], [750, fillTop - 5]], 3);
    if (fill > 0.6) { p.poly([[360, fillTop - 6], [400, fillTop - 6], [395, fillTop - 22], [355, fillTop - 22]], "#8a6a44", 3); p.ell(352, fillTop - 9, 6, 6, "#3a3a40", 2); }
  }
  // two houses on screws (left brick, right clapboard) with tiny people waving from the windows
  for (const [x, wdt, h, col, roofC] of [[62, 128, 170, "#b06a4a", "#5a4a4a"], [612, 124, 186, "#d9c08a", "#4a4a5a"]] as [number, number, number, string, string][]) {
    const y0 = street - 8 - up;
    if (up > 2) for (const sx of [x + 20, x + wdt - 20]) { p.stroke([[sx, street - 8], [sx, y0]], 8, "#4a4d55"); for (let yy = street - 14; yy > y0; yy -= 9) p.stroke([[sx - 6, yy], [sx + 6, yy - 4]], 2, "#a8aeb6"); }
    p.poly([[x, y0], [x + wdt, y0], [x + wdt, y0 - h], [x, y0 - h]], col, 6);
    for (let k = 0; k < (col === "#d9c08a" ? 9 : 0); k++) p.stroke([[x + 4, y0 - 12 - k * 19], [x + wdt - 4, y0 - 12 - k * 19]], 2, "#a8905a");
    p.poly([[x - 10, y0 - h], [x + wdt + 10, y0 - h], [x + wdt / 2, y0 - h - 56]], roofC, 6);
    p.poly([[x + wdt - 34, y0 - h - 30], [x + wdt - 20, y0 - h - 30], [x + wdt - 20, y0 - h - 62], [x + wdt - 34, y0 - h - 62]], "#7a4a3a", 4);
    for (let r0 = 0; r0 < 3; r0++) for (let c = 0; c < 2; c++) {
      const wx = x + 20 + c * 56, wy = y0 - h + 22 + r0 * 48;
      p.poly(rr(wx, wy, wx + 34, wy + 36, 3), "#e8dcb4", 3);
      if ((r0 + c) % 3 === 0) { p.ell(wx + 17, wy + 16, 7, 8, "#f1c9a6", 2); p.dot(wx + 14, wy + 15, 1.5); p.dot(wx + 20, wy + 15, 1.5); }
    }
    p.poly(rr(x + wdt / 2 - 14, y0 - 46, x + wdt / 2 + 14, y0, 3), "#5a3a2a", 3);
  }
  // glass box: frame, a reflection streak, ink
  g.fillStyle = "rgba(255,255,255,0.2)"; g.beginPath(); g.moveTo(96, 126); g.lineTo(150, 126); g.lineTo(82, 330); g.lineTo(60, 330); g.fill();
  // v19: an OPEN-topped diorama (the lifted houses rise above its sides, so a lid rail would cut through them): two corner
  // posts and the base edge only
  g.strokeStyle = "#2a1e24"; g.lineWidth = 9; g.beginPath(); g.moveTo(50, 120); g.lineTo(50, base); g.lineTo(750, base); g.lineTo(750, 120); g.stroke();
  for (const x of [50, 750]) p.stroke([[x, 116], [x, base]], 12, "#7a5034");
};

/** a painted dust sheet over the model with folds, a fringe and shadowed hollows, pulled off to the right (k 0..1). 800 x 520 */
export const fxSheet = (p: Pen, k: number) => {
  const dx = 900 * k01(k) ** 1.6;
  if (dx > 880) return;
  const g = p.g;
  const top = (x: number) => 110 + 26 * Math.sin(x * 0.012) - 10 * Math.sin(x * 0.031);
  const pts: P2[] = [];
  for (let x = 30; x <= 780; x += 25) pts.push([x + dx * (0.5 + 0.5 * (1 - x / 780)), top(x) - (x < 120 ? (120 - x) * 0.4 : 0)]);
  const outline: P2[] = [[30 + dx, 505], ...pts, [785 + dx * 0.5, 505]];
  p.poly(outline, "#e3dccb", 0);
  // fold shading: vertical soft bands, hollows darker
  for (let i = 0; i < 9; i++) {
    const x = 70 + i * 82 + dx * (0.5 + 0.5 * (1 - (70 + i * 82) / 780)), w = 30 + (i % 3) * 10;
    const gr = g.createLinearGradient(x - w, 0, x + w, 0); gr.addColorStop(0, "rgba(120,110,140,0)"); gr.addColorStop(0.5, "rgba(120,110,140,0.32)"); gr.addColorStop(1, "rgba(120,110,140,0)");
    g.save(); p.path(outline, true); g.clip(); g.fillStyle = gr; g.fillRect(x - w, 0, 2 * w, 520); g.restore();
    p.stroke([[x + 4, top(x - dx) + 30], [x - 6 + (i % 2) * 10, 300], [x + 2, 490]], 3, "rgba(90,80,110,0.6)");
  }
  // fringe along the bottom
  for (let x = 40 + dx; x < 780 + dx * 0.5; x += 14) p.stroke([[x, 500], [x + 2, 516]], 3, "#c8b88a");
  p.poly(outline, null, 9);
};

/** terracotta flowerpot with a red geranium (sits on the 1858 sill and never wobbles). 200 x 240 */
export const fxPot = (p: Pen) => {
  for (const [x, y] of [[70, 70], [110, 50], [140, 85], [95, 100]]) p.ell(x, y, 26, 24, "#b84a40", 6);
  p.stroke([[100, 120], [100, 150]], 6, "#4a6a3a");
  p.ell(70, 130, 30, 14, "#5a7a46", 5); p.ell(132, 130, 30, 14, "#5a7a46", 5);
  p.poly([[40, 150], [160, 150], [145, 232], [55, 232]], "#b8714a", 7);
  p.poly(rr(32, 140, 168, 166, 6), "#a5633f", 6);
};

/** a frog in the swamp, sitting (0) or mid-hop (1). 220 x 180 */
export const fxFrog = (p: Pen, hop: number) => {
  const g = p.g; g.save(); g.translate(110, 120 - 60 * hop); g.rotate(-0.3 * hop);
  p.ell(0, 10, 62, 40, "#6f8a4a", 7);
  p.ell(-30, -26, 18, 18, "#6f8a4a", 6); p.ell(30, -26, 18, 18, "#6f8a4a", 6);
  p.dot(-30, -28, 6); p.dot(30, -28, 6);
  p.arc(0, 8, 26, 12, 20, 160, 4);
  if (hop > 0.3) { p.line([[-50, 30], [-90, 60], [-120, 70]], "#6f8a4a", 12); p.line([[50, 30], [90, 60], [120, 70]], "#6f8a4a", 12); }
  else { p.ell(-58, 40, 26, 14, "#6f8a4a", 6); p.ell(58, 40, 26, 14, "#6f8a4a", 6); }
  g.restore();
};

/** milk bottle left on a step each morning. 110 x 260 */
export const fxMilk = (p: Pen) => {
  p.poly([[20, 250], [90, 250], [92, 120], [72, 80], [72, 30], [38, 30], [38, 80], [18, 120]], "#f2f0ea", 7);
  p.poly(rr(34, 14, 76, 36, 6), "#c4b48a", 5);
  p.g.fillStyle = "rgba(255,255,255,0.6)"; p.g.fillRect(30, 130, 10, 100);
};

/** floating debris for the river (flat card from above): 0 crate, 1 log, 2 barrel, 3 bottle. 300 x 200 */
export const fxDebris = (p: Pen, kind: number) => {
  if (kind === 0) { p.poly([[60, 40], [240, 30], [250, 170], [70, 175]], "#8a6a44", 7); p.stroke([[65, 100], [245, 98]], 4); p.stroke([[150, 35], [158, 172]], 4); }
  else if (kind === 1) { p.poly(rr(20, 80, 280, 130, 24), "#6a5038", 7); p.ell(270, 105, 16, 24, "#a88a60", 5); p.stroke([[60, 95], [200, 92]], 3, "#4a3a28"); }
  else if (kind === 2) { p.ell(150, 100, 80, 80, "#7a5a3a", 7); p.ell(150, 100, 60, 60, null, 4); p.ell(150, 100, 30, 30, "#5a4028", 5); }
  else { p.poly(rr(90, 80, 230, 120, 18), "#5a7a5a", 6); p.poly(rr(225, 90, 270, 110, 6), "#5a7a5a", 5); }
};

/** ripple ring around floating debris (flat, soft), ph 0..1. 300 x 300 */
export const fxRipple = (p: Pen, ph: number) => {
  p.g.strokeStyle = `rgba(230,240,245,${0.5 * (1 - ph)})`; p.g.lineWidth = 6;
  p.g.beginPath(); p.g.ellipse(150, 150, 60 + 80 * ph, 60 + 80 * ph, 0, 0, Math.PI * 2); p.g.stroke();
};

/** a brass bell / gavel strike burst is reused from toon.fxBurst. A "SLEEPING CAR" contract on Pullman's clipboard,
 *  front view, 360 x 460 */
export const fxContract = (p: Pen) => {
  p.poly(rr(20, 30, 340, 450, 14), "#8a6440", 9);
  p.poly(rr(46, 70, 314, 430, 6), "#efe8d6", 6);
  p.poly(rr(130, 14, 230, 64, 10), "#9aa3ad", 6);
  fit(p, "CONTRACT", 180, 110, 34, 230, "#2a2622");
  // a tiny sleeping-car doodle
  p.poly(rr(80, 150, 280, 220, 12), "#3f5a4a", 5);
  for (let i = 0; i < 4; i++) p.poly(rr(96 + i * 46, 162, 126 + i * 46, 190, 4), "#e8d49a", 3);
  p.ell(120, 230, 12, 12, "#2b2830", 3); p.ell(240, 230, 12, 12, "#2b2830", 3);
  lines(p, 70, 290, 270, 390, 22);
  p.line([[180, 405], [210, 392], [240, 410], [280, 395]], "#2a2a5a", 4);
};
