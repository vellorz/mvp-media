// v3 (Nov 11 teardown pass): FOREGROUND layer props. Every take keeps one recognisable period prop cropped by a frame
// edge, close to the lens and lens-blurred (teardown: a blurred near layer in every shot). Plus the dusk gas lamps that
// switch on as events (take 5) and small life props. Same flat fill + ink as toon.ts; nothing here carries text that
// has to be read except shop signs.
import { Pen, INK } from "./toon";
type P2 = [number, number];
const SERIF = "Georgia, 'Times New Roman', serif";

/** a cast-iron gas street lamp: post + four-pane lantern. 300 x 1000. lit 0..1 (glass glows, halo) */
export const fxLamp = (p: Pen, lit: number) => {
  const g = p.g;
  if (lit > 0) {
    const r = g.createRadialGradient(150, 150, 10, 150, 150, 150);
    r.addColorStop(0, `rgba(255,214,140,${0.75 * lit})`); r.addColorStop(1, "rgba(255,190,110,0)");
    g.fillStyle = r; g.fillRect(0, 0, 300, 300);
  }
  p.poly([[138, 250], [162, 250], [168, 960], [132, 960]], "#2f3540", 6);           // post
  p.poly([[112, 940], [188, 940], [196, 996], [104, 996]], "#2f3540", 6);           // base
  p.poly([[124, 560], [176, 560], [180, 600], [120, 600]], "#2f3540", 5);           // collar
  p.line([[100, 250], [200, 250]], "#2f3540", 10);                                    // ladder bar
  p.poly([[110, 240], [190, 240], [205, 110], [95, 110]], lit > 0.5 ? "#ffe2a0" : "#9fb0b8", 6); // glass
  p.stroke([[150, 110], [150, 240]], 4, "#2f3540");
  p.poly([[85, 110], [215, 110], [150, 60]], "#2f3540", 6);                           // cap
  p.dot(150, 52, 10, "#2f3540");
  if (lit > 0) p.ell(150, 185, 18, 26, `rgba(255,250,220,${lit})`, 0);
};

/** cattails and marsh reeds, a clump growing up from the bottom edge. 600 x 800 */
export const fxReeds = (p: Pen) => {
  const st: [number, number, number, number][] = [[80, 800, 40, 120], [160, 800, 190, 40], [230, 800, 260, 160], [300, 800, 330, 60], [380, 800, 430, 210], [470, 800, 520, 100], [540, 800, 590, 260]];
  for (const [x0, y0, x1, y1] of st) p.line([[x0, y0], [(x0 + x1) / 2 - 10, (y0 + y1) / 2], [x1, y1]], "#5f7a3a", 12);
  for (const [, , x1, y1] of st.filter((_, i) => i % 2 === 1)) { p.poly([[x1 - 16, y1 + 20], [x1 + 16, y1 + 20], [x1 + 16, y1 + 120], [x1 - 16, y1 + 120]], "#6a4028", 5); p.stroke([[x1, y1 + 20], [x1, y1 - 20]], 5); }
  for (const [x, a] of [[60, -0.5], [210, 0.4], [350, -0.3], [500, 0.5]] as const) p.poly([[x, 800], [x + 30, 800], [x + 15 + 260 * a, 380]], "#7a9447", 5);
};

/** a china teapot on a saucer (bottom-corner prop of the tea table). 600 x 500 */
export const fxTeapot = (p: Pen) => {
  p.ell(300, 455, 270, 40, "#f2ede2", 6);
  p.ell(300, 300, 190, 150, "#e8eef4", 7);
  p.arc(300, 300, 150, 110, 200, 340, 10, "#3f6fb5");
  for (const x of [220, 300, 380]) p.ell(x, 330, 26, 22, "#3f6fb5", 4);
  p.line([[470, 270], [560, 180], [585, 175]], "#e8eef4", 26);
  p.arc(120, 290, 70, 80, 90, 270, 18, "#e8eef4");
  p.ell(300, 160, 90, 26, "#e8eef4", 6); p.dot(300, 128, 16, "#3f6fb5");
};

/** the back of a seated councilman: top hat + shoulders, dark wool (over-the-shoulder foreground). 700 x 700 */
export const fxBackHat = (p: Pen) => {
  p.poly([[20, 700], [60, 520], [200, 450], [500, 450], [640, 520], [680, 700]], "#2e2b33", 8);
  p.ell(350, 400, 150, 140, "#7a5a40", 8);                       // back of the head: hair
  p.poly([[200, 310], [500, 310], [520, 280], [180, 280]], "#1e1c22", 7); // brim
  p.poly([[230, 285], [470, 285], [455, 40], [245, 40]], "#26232a", 8);
  p.poly([[236, 250], [464, 250], [462, 220], [238, 220]], "#5a3a40", 0);
  p.stroke([[350, 470], [350, 700]], 4, "#1a181e");
};

/** an oak barrel (street clutter, bottom corner). 500 x 620 */
export const fxBarrel = (p: Pen) => {
  p.poly([[60, 60], [440, 60], [480, 310], [440, 580], [60, 580], [20, 310]], "#8a5a34", 8);
  for (const x of [130, 200, 270, 340, 410]) p.stroke([[x, 64], [x + (x - 250) * 0.12, 310], [x, 578]], 3, "#5e3a20");
  for (const y of [120, 250, 380, 510]) p.line([[30 + Math.abs(310 - y) * 0.12, y], [470 - Math.abs(310 - y) * 0.12, y]], "#3c3f46", 18);
  p.ell(250, 62, 190, 30, "#6e4628", 6);
};

/** a hanging shop sign on an iron bracket. 760 x 520. words on the board (Lake Street trades) */
export const fxSign = (p: Pen, word: string, col = "#2f4f3a", flip = false, W = 760) => {
  // flip: the iron bracket comes in from the RIGHT card edge (the wall is off-frame right) and the lettering stays readable;
  // W > 760 lengthens the bracket arm (board moved away from the wall end) so a push-in keeps the wall end off-frame
  const S = W - 760, X = (x: number) => { const o = x === 0 ? 0 : x + S; return flip ? W - o : o; }, Q = (pts: [number, number][]) => pts.map(([x, y]) => [X(x), y] as [number, number]);
  p.line(Q([[0, 40], [700, 40]]), "#2f3540", 14);
  if (flip) p.arc(X(560), 40, 120, 120, 90, 180, 8, "#2f3540"); else p.arc(560 + S, 40, 120, 120, 0, 90, 8, "#2f3540");
  for (const x of [140, 600]) p.stroke(Q([[x, 40], [x, 150]]), 5, "#2f3540");
  p.poly(Q([[90, 150], [650, 150], [650, 470], [90, 470]]), col, 8);
  p.stroke(Q([[115, 175], [625, 175], [625, 445], [115, 445], [115, 175]]), 5, "#d9b04a");
  const g = p.g; let z = 120; g.font = `bold ${z}px ${SERIF}`;
  while (g.measureText(word).width > 470 && z > 20) { z -= 4; g.font = `bold ${z}px ${SERIF}`; }
  g.textAlign = "center"; g.textBaseline = "middle"; g.fillStyle = "#f0dca0"; g.fillText(word, X(370), 312);
};

/** a clay pot of red geraniums (sill / steps prop). 520 x 520 */
export const fxGeranium = (p: Pen) => {
  p.poly([[130, 300], [390, 300], [360, 510], [160, 510]], "#b45a3a", 7);
  p.poly([[110, 290], [410, 290], [410, 330], [110, 330]], "#c96a46", 6);
  for (const [x, y, r] of [[120, 230, 70], [260, 180, 80], [400, 230, 70], [190, 120, 60], [340, 110, 62]] as const) p.ell(x, y, r, r * 0.8, "#4f7a3a", 6);
  for (const [x, y] of [[180, 90], [270, 60], [360, 80], [230, 150], [320, 170], [150, 190], [400, 180]] as const) p.ell(x, y, 30, 28, "#d23a3a", 5);
};

/** a brass candlestick and a wine glass (dining table corner). 520 x 760 */
export const fxCandle = (p: Pen) => {
  const g = p.g, r = g.createRadialGradient(150, 110, 4, 150, 110, 90); r.addColorStop(0, "rgba(255,220,150,.8)"); r.addColorStop(1, "rgba(255,200,120,0)");
  g.fillStyle = r; g.fillRect(40, 0, 220, 220);
  p.poly([[132, 140], [168, 140], [168, 420], [132, 420]], "#f4efe0", 6);
  p.ell(150, 120, 12, 26, "#ffd27a", 3);
  p.poly([[100, 420], [200, 420], [170, 470], [130, 470]], "#c9a24a", 6);
  p.poly([[138, 470], [162, 470], [168, 690], [132, 690]], "#c9a24a", 6);
  p.ell(150, 710, 90, 30, "#c9a24a", 6);
  p.poly([[330, 360], [480, 360], [460, 500], [350, 500]], "rgba(220,235,245,0.55)", 6);
  p.poly([[340, 440], [470, 440], [460, 500], [350, 500]], "#7a1f2c", 0);
  p.stroke([[405, 500], [405, 690]], 8, "#9fb0b8"); p.ell(405, 700, 70, 18, "rgba(220,235,245,0.7)", 6);
};

/** a potted fern on a stand (parlour corner). 700 x 800 */
export const fxFern = (p: Pen) => {
  p.poly([[250, 560], [450, 560], [420, 760], [280, 760]], "#7a4a6a", 7);
  for (const [a, l] of [[-150, 330], [-125, 380], [-100, 400], [-75, 390], [-50, 340], [-30, 300], [-170, 260], [-10, 250]] as const) {
    const ar = (a * Math.PI) / 180, x1 = 350 + Math.cos(ar) * l, y1 = 560 + Math.sin(ar) * l;
    p.line([[350, 560], [x1, y1]], "#4f7a3a", 8);
    for (let i = 1; i < 9; i++) { const u = i / 9, cx = 350 + (x1 - 350) * u, cy = 560 + (y1 - 560) * u, s = 26 * (1 - u * 0.6);
      p.ell(cx + Math.sin(ar) * s, cy - Math.cos(ar) * s, s, s * 0.45, "#5f8f45", 3, 0, 360, ar * 57 + 90);
      p.ell(cx - Math.sin(ar) * s, cy + Math.cos(ar) * s, s, s * 0.45, "#5f8f45", 3, 0, 360, ar * 57 + 90); }
  }
};

/** a travel trunk with leather straps and brass corners (station platform). 760 x 520 */
export const fxTrunk = (p: Pen) => {
  p.poly([[40, 120], [720, 120], [720, 500], [40, 500]], "#5a6b8a", 8);
  p.poly([[40, 60], [720, 60], [740, 130], [20, 130]], "#4a5a78", 8);
  for (const x of [200, 560]) p.poly([[x - 26, 60], [x + 26, 60], [x + 26, 500], [x - 26, 500]], "#7a4a2a", 5);
  for (const [x, y] of [[40, 120], [720, 120], [40, 500], [720, 500]] as const) p.ell(x, y, 34, 34, "#c9a24a", 5);
  p.poly([[340, 150], [420, 150], [420, 210], [340, 210]], "#c9a24a", 5);
  p.poly([[460, 300], [640, 290], [650, 380], [470, 390]], "#e9e1cc", 4); // luggage label, blank
};

/** a heavy timber cribbing beam with a jackscrew standing on it (under the building). 500 x 900 */
export const fxScrew = (p: Pen) => {
  p.poly([[0, 760], [500, 740], [500, 900], [0, 900]], "#7a5634", 8);
  for (const y of [790, 840]) p.stroke([[10, y], [490, y - 12]], 3, "#5e3a20");
  p.poly([[170, 740], [330, 740], [300, 640], [200, 640]], "#4a4e58", 7);
  p.poly([[218, 640], [282, 640], [282, 140], [218, 140]], "#6a707c", 7);
  for (let y = 160; y < 640; y += 28) p.stroke([[218, y], [282, y + 14]], 5, "#3c3f46");
  p.poly([[150, 140], [350, 140], [350, 80], [150, 80]], "#4a4e58", 7);
  p.line([[250, 110], [470, 60]], "#3c3f46", 18);
  p.poly([[120, 80], [380, 80], [380, 0], [120, 0]], "#7a5634", 7);
};

/** a gull gliding past the lens (aerial takes). 500 x 300, wing phase 0..1 */
export const fxGull = (p: Pen, ph: number) => {
  const up = Math.sin(ph * Math.PI * 2) * 60;
  p.poly([[250, 160], [60, 120 - up], [10, 140 - up], [200, 190]], "#f4f2ec", 6);
  p.poly([[250, 160], [440, 120 - up], [490, 140 - up], [300, 190]], "#f4f2ec", 6);
  p.ell(250, 175, 70, 30, "#f4f2ec", 6); p.poly([[310, 168], [350, 175], [310, 182]], "#e0a020", 4); p.dot(296, 170, 4);
  p.poly([[60, 120 - up], [10, 140 - up], [40, 132 - up]], "#3c3f46", 0); p.poly([[440, 120 - up], [490, 140 - up], [460, 132 - up]], "#3c3f46", 0);
};

/** an inkwell with a quill and a stack of ledgers (council table corner). 640 x 600 */
export const fxInkwell = (p: Pen) => {
  for (const [y, c] of [[470, "#7a2f2f"], [400, "#2f4f6a"], [330, "#5a4a2a"]] as const) { p.poly([[40, y], [400, y - 10], [410, y + 70], [30, y + 80]], c, 7); p.stroke([[50, y + 55], [395, y + 47]], 3, "#e9e1cc"); }
  p.poly([[440, 470], [600, 470], [590, 580], [450, 580]], "#2a2830", 7);
  p.ell(520, 470, 80, 18, "#1a181e", 5);
  p.line([[520, 470], [620, 60]], "#f4f2ec", 8);
  p.poly([[600, 140], [640, 40], [620, 30], [570, 150]], "#f4f2ec", 5);
};

/** a heavy velvet drape gathered at a window edge (interior frame edge). 400 x 1000 */
export const fxDrape = (p: Pen, col = "#7a2f3f") => {
  p.poly([[0, 0], [400, 0], [330, 420], [260, 520], [320, 1000], [0, 1000]], col, 8);
  for (const x of [70, 150, 230]) p.stroke([[x, 0], [x * 0.85, 480], [x * 0.95, 1000]], 5, "#4a1a24");
  // tieback: a braided gold cord wrapped round the pinch of the drape, with a hanging tassel (no loose square)
  p.poly([[0, 452], [282, 436], [290, 470], [0, 492]], "#b8892e", 5);
  for (let x = 20; x < 280; x += 28) p.stroke([[x, 446 - x * 0.05], [x + 14, 482 - x * 0.07]], 3, "#7a5a1a");
  p.stroke([[270, 470], [276, 560]], 4, "#7a5a1a");
  p.poly([[256, 560], [296, 560], [304, 640], [248, 640]], "#c9993a", 4);
};

/** a lamplighter's long pole tip with a small flame (moves lamp to lamp, take 5). 120 x 600 */
export const fxPole = (p: Pen) => {
  p.line([[60, 600], [60, 40]], "#6a4a2a", 12);
  p.ell(60, 28, 12, 22, "#ffd27a", 3);
};

/** a white picket fence corner with a post cap (residential frame edge). 800 x 600 */
export const fxPicket = (p: Pen) => {
  p.line([[0, 260], [800, 240]], "#e9e4d8", 26); p.line([[0, 460], [800, 440]], "#e9e4d8", 26);
  for (let x = 20; x < 800; x += 110) p.poly([[x, 600], [x + 60, 600], [x + 60, 140], [x + 30, 100], [x, 140]], "#f2eee4", 6);
};

/** wet cobble kerb with a cast-iron drain grate and running water (rain take). 800 x 400 */
export const fxDrain = (p: Pen) => {
  p.poly([[0, 120], [800, 80], [800, 400], [0, 400]], "#6a6560", 7);
  for (let i = 0; i < 9; i++) p.ell(60 + i * 90, 300 + (i % 2) * 40, 40, 22, "#7a756e", 4);
  p.poly([[300, 200], [520, 190], [530, 260], [300, 270]], "#2a2830", 6);
  for (let x = 320; x < 520; x += 24) p.stroke([[x, 200], [x, 262]], 6, "#4a4e58");
  p.g.fillStyle = "rgba(160,190,210,0.45)"; p.g.fillRect(0, 140, 800, 40);
};

export const _ink = INK; // keep the import used (shared palette)
export type { P2 };

/** a hanging work lantern on a short chain, lit, with a warm halo. 200 x 520 (chain top at y 0) */
export const fxLantern = (p: Pen) => {
  const g = p.g, r = g.createRadialGradient(100, 360, 10, 100, 360, 100);
  r.addColorStop(0, "rgba(255,210,130,0.85)"); r.addColorStop(1, "rgba(255,190,110,0)");
  g.fillStyle = r; g.fillRect(0, 260, 200, 200);
  p.stroke([[100, 0], [100, 250]], 6, "#3c3f46");
  p.poly([[60, 270], [140, 270], [150, 300], [50, 300]], "#2f3540", 5);
  p.poly([[62, 300], [138, 300], [146, 420], [54, 420]], "#ffe2a0", 6);
  p.ell(100, 370, 14, 22, "#fff6d8", 0);
  p.poly([[50, 420], [150, 420], [140, 450], [60, 450]], "#2f3540", 5);
  p.arc(100, 262, 22, 18, 180, 360, 6, "#3c3f46");
};

/** v21 (owner rule 80): a ring of churned mud round a sunk man's shins, so the legs read as IN the mud. 600 x 220 */
export const fxMud = (p: Pen) => {
  p.poly([[20, 200], [60, 120], [140, 90], [230, 70], [300, 82], [380, 66], [470, 92], [550, 125], [585, 200]], "#6b4a2c", 7);
  p.poly([[90, 140], [170, 108], [250, 96], [330, 104], [420, 96], [500, 128], [470, 150], [380, 136], [300, 146], [210, 138], [130, 158]], "#87613b", 0);
  p.g.fillStyle = "#4a3220"; for (const [x, y, r] of [[160, 175, 14], [260, 160, 10], [420, 170, 16], [500, 180, 9], [90, 185, 8], [340, 185, 12]] as const) { p.g.beginPath(); p.g.ellipse(x, y, r * 1.6, r, 0, 0, Math.PI * 2); p.g.fill(); }
  p.g.fillStyle = "#7a5634"; for (const [x, y, r] of [[40, 70, 9], [560, 60, 8], [120, 40, 6], [480, 35, 7], [300, 30, 5]] as const) { p.g.beginPath(); p.g.arc(x, y, r, 0, Math.PI * 2); p.g.fill(); }
};

/** v21 (rule 78/79): the brick wall the CHOLERA paper is pasted on, so the insert never hangs in the open street */
export const fxNewsWall = (p: Pen) => {
  const g = p.g; g.fillStyle = "#8a4a3c"; g.fillRect(0, 0, 800, 1120);
  for (let r = 0; r < 28; r++) for (let c = -1; c < 6; c++) {
    const x = c * 160 + (r % 2 ? 80 : 0), y = r * 40, k = (r * 7 + c * 13) % 5;
    g.fillStyle = ["#93503f", "#84463a", "#9a5844", "#7c4136", "#8e4c3d"][k]; g.fillRect(x + 3, y + 3, 154, 34);
  }
  g.strokeStyle = "#3a2226"; g.lineWidth = 3;
  for (let r = 0; r <= 28; r++) { g.beginPath(); g.moveTo(0, r * 40); g.lineTo(800, r * 40); g.stroke(); for (let c = -1; c < 6; c++) { const x = c * 160 + (r % 2 ? 80 : 0); g.beginPath(); g.moveTo(x, r * 40); g.lineTo(x, r * 40 + 40); g.stroke(); } }
};
