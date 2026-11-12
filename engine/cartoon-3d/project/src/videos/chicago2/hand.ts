// Hand-drawn set painting (DETAIL_STANDARD 6A / G9): simple 3D boxes carry ILLUSTRATED textures with their own wobbly ink
// lines, painterly mottled fills and lots of small story detail, every window different, nothing tiled. Same option
// objects as paint.ts facadeHD so the city / houses swap over without layout changes.
import { ctex as ctex0, rng } from "./paint";
/** ctex seeds its random stream from the key length + first letter only: re-seed from a hash of the whole key */
const hash = (s: string) => { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return (h >>> 0) % 2147483000 + 1; };
const ctex = (key: string, w: number, h: number, draw: (g: CanvasRenderingContext2D, r: () => number) => void) => ctex0(key, w, h, (g) => draw(g, rng(hash(key))));
type R = () => number;
type G = CanvasRenderingContext2D;
type P = [number, number];
const U = (r: R, a: number, b: number) => a + (b - a) * r();
const pick = <T,>(r: R, a: T[]) => a[Math.floor(r() * a.length) % a.length];
export const HINK = "#2a1e24";

/** a hand-drawn line: the polyline is resampled and nudged so it never looks ruled */
export const wob = (g: G, r: R, pts: P[], lw: number, col = HINK, j = 1) => {
  g.strokeStyle = col; g.lineWidth = lw; g.lineCap = "round"; g.lineJoin = "round"; g.beginPath();
  for (let i = 0; i < pts.length; i++) {
    const [x, y] = pts[i];
    if (i === 0) { g.moveTo(x + U(r, -j, j), y + U(r, -j, j)); continue; }
    const [px, py] = pts[i - 1], n = Math.max(1, Math.round(Math.hypot(x - px, y - py) / 40));
    for (let k = 1; k <= n; k++) { const t = k / n; g.lineTo(px + (x - px) * t + U(r, -j, j), py + (y - py) * t + U(r, -j, j)); }
  }
  g.stroke();
};
export const wobRect = (g: G, r: R, x: number, y: number, w: number, h: number, lw: number, col = HINK, j = 1) =>
  wob(g, r, [[x, y], [x + w, y], [x + w, y + h], [x, y + h], [x, y]], lw, col, j);
/** painterly mottle: many short soft strokes in jittered tints of the base colour */
export const mottle = (g: G, r: R, x0: number, y0: number, w: number, h: number, n: number, len: number, tints: string[], a = 0.18) => {
  g.lineCap = "round";
  for (let i = 0; i < n; i++) {
    const x = x0 + r() * w, y = y0 + r() * h, ang = U(r, -0.5, 0.5), l = len * U(r, 0.4, 1.2);
    g.strokeStyle = pick(r, tints); g.globalAlpha = a * U(r, 0.5, 1); g.lineWidth = len * U(r, 0.15, 0.4);
    g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(ang) * l, y + Math.sin(ang) * l); g.stroke();
  }
  g.globalAlpha = 1;
};
const shadeRGB = (hex: string, k: number) => {
  const n = parseInt(hex.slice(1), 16), c = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) => Math.max(0, Math.min(255, Math.round(k >= 1 ? v + (255 - v) * (k - 1) : v * k))));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
};
/** scribbled "text" lines on a poster or paper */
const scribble = (g: G, r: R, x: number, y: number, w: number, rows: number, gap: number, col = "rgba(40,30,30,0.7)", lw = 2) => {
  for (let i = 0; i < rows; i++) { const l = w * U(r, 0.55, 1); wob(g, r, [[x + (w - l) / 2, y + i * gap], [x + (w + l) / 2, y + i * gap]], lw, col, 0.8); }
};
/** a pasted bill: title in block letters, scribbles, a torn corner */
const POSTERS = ["AUCTION", "LOST HOG", "TONIC", "TO LET", "CIRCUS", "NOTICE", "STEAMER", "WANTED", "LECTURE", "LAND SALE"];
const poster = (g: G, r: R, x: number, y: number, w: number, h: number) => {
  g.save(); g.translate(x + w / 2, y + h / 2); g.rotate(U(r, -0.06, 0.06)); g.translate(-w / 2, -h / 2);
  g.fillStyle = pick(r, ["#efe6cf", "#e8d9b2", "#f2e8d8", "#e3c9a0"]); g.fillRect(0, 0, w, h);
  g.fillStyle = "rgba(120,90,50,0.18)"; g.fillRect(0, h * 0.75, w, h * 0.25);
  const s = pick(r, POSTERS); let z = h * 0.2; g.font = `bold ${z}px Georgia, serif`;
  while (g.measureText(s).width > w * 0.86 && z > 6) { z -= 1; g.font = `bold ${z}px Georgia, serif`; }
  g.fillStyle = pick(r, ["#7a1f1c", "#2a2622", "#1f3a5a"]); g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(s, w / 2, h * 0.2);
  scribble(g, r, w * 0.12, h * 0.42, w * 0.76, 4, h * 0.11, "rgba(40,30,30,0.55)", Math.max(1, h * 0.02));
  g.fillStyle = "rgba(0,0,0,0)"; wobRect(g, r, 0, 0, w, h, Math.max(1.5, w * 0.02), "rgba(60,40,30,0.7)", 0.6);
  g.restore();
};
const flowerBox = (g: G, r: R, x: number, y: number, w: number, m: (v: number) => number) => {
  g.fillStyle = "#7a5034"; g.fillRect(x, y - m(0.16), w, m(0.16)); wobRect(g, r, x, y - m(0.16), w, m(0.16), m(0.018));
  for (let k = 0; k < 6; k++) {
    const fx = x + m(0.08) + (k * (w - m(0.16))) / 5, fy = y - m(0.2) - U(r, 0, m(0.1));
    g.fillStyle = "#4f6a3a"; g.beginPath(); g.ellipse(fx, fy + m(0.05), m(0.07), m(0.05), 0, 0, 7); g.fill();
    g.fillStyle = pick(r, ["#c0453a", "#e8d6a8", "#d98a3a", "#b85a8a"]); g.beginPath(); g.arc(fx, fy, m(0.045), 0, 7); g.fill();
  }
};

/** the illustrated window: trim, panes, glass with a painted room behind, one of many dressings */
const windowInk = (g: G, r: R, cx: number, by: number, m: (v: number) => number, shutter: string, lit = false) => {
  const ww = m(0.85), wh = m(1.25), x0 = cx - ww / 2, y0 = by - wh, tr = m(0.09), lw = Math.max(1.6, m(0.022));
  // shutters: open flat, half-closed, closed, one hanging askew, or none
  const kind = r();
  const sw = m(0.44);
  if (kind < 0.8) for (const side of [-1, 1]) {
    const closed = kind > 0.7 && side < 0, sx = closed ? x0 : side < 0 ? x0 - tr - sw : x0 + ww + tr;
    const skew = kind > 0.62 && kind < 0.7 && side > 0 ? m(0.06) : 0;
    g.fillStyle = shutter;
    g.beginPath(); g.moveTo(sx, y0 + skew); g.lineTo(sx + sw, y0); g.lineTo(sx + sw, y0 + wh); g.lineTo(sx, y0 + wh + skew); g.closePath(); g.fill();
    mottle(g, r, sx, y0, sw, wh, 14, m(0.12), ["#000000", "#ffffff"], 0.08);
    for (let ly = y0 + m(0.07); ly < y0 + wh - m(0.05); ly += m(0.075)) wob(g, r, [[sx + m(0.05), ly], [sx + sw - m(0.05), ly]], Math.max(1, m(0.01)), "rgba(30,20,25,0.45)", 0.4);
    wob(g, r, [[sx, y0 + skew], [sx + sw, y0], [sx + sw, y0 + wh], [sx, y0 + wh + skew], [sx, y0 + skew]], lw, HINK, 0.8);
    if (closed) break;
  }
  // trim
  g.fillStyle = "#ece2cc"; g.fillRect(x0 - tr, y0 - tr, ww + 2 * tr, wh + 2 * tr);
  // glass / the room behind
  const room = lit ? ["#f2c46a", "#d99a4a"] : pick(r, [["#6a6f9a", "#3f4470"], ["#7a7290", "#4a4260"], ["#5f7088", "#3a4558"]]);
  const gr = g.createLinearGradient(0, y0, 0, y0 + wh); gr.addColorStop(0, room[0]); gr.addColorStop(1, room[1]);
  g.fillStyle = gr; g.fillRect(x0, y0, ww, wh);
  const dress = r();
  g.save(); g.beginPath(); g.rect(x0, y0, ww, wh); g.clip();
  if (dress < 0.18) { // somebody looking out (silhouette with a pale face)
    const hx = x0 + ww * U(r, 0.3, 0.7), hy = y0 + wh * 0.42;
    g.fillStyle = "rgba(40,30,40,0.75)"; g.beginPath(); g.ellipse(hx, hy + m(0.42), m(0.2), m(0.3), 0, 0, 7); g.fill();
    g.fillStyle = "#e8cdb0"; g.beginPath(); g.ellipse(hx, hy, m(0.12), m(0.14), 0, 0, 7); g.fill();
    g.fillStyle = HINK; g.beginPath(); g.arc(hx - m(0.04), hy, m(0.015), 0, 7); g.arc(hx + m(0.04), hy, m(0.015), 0, 7); g.fill();
  } else if (dress < 0.32) { // a lamp on a table
    g.fillStyle = "#3a3040"; g.fillRect(x0, y0 + wh * 0.72, ww, wh * 0.3);
    g.fillStyle = "#f2d27a"; g.beginPath(); g.ellipse(x0 + ww * 0.6, y0 + wh * 0.6, m(0.1), m(0.13), 0, 0, 7); g.fill();
  } else if (dress < 0.42) { // a cat on the inner sill
    g.fillStyle = pick(r, ["#2a2228", "#c98a4a", "#e8e0d0"]);
    g.beginPath(); g.ellipse(x0 + ww * 0.35, y0 + wh - m(0.12), m(0.16), m(0.1), 0, 0, 7); g.fill();
    g.beginPath(); g.arc(x0 + ww * 0.52, y0 + wh - m(0.22), m(0.08), 0, 7); g.fill();
    g.beginPath(); g.moveTo(x0 + ww * 0.47, y0 + wh - m(0.27)); g.lineTo(x0 + ww * 0.49, y0 + wh - m(0.36)); g.lineTo(x0 + ww * 0.53, y0 + wh - m(0.29)); g.fill();
  } else if (dress < 0.52) { // pot plant
    g.fillStyle = "#b8714a"; g.fillRect(x0 + ww * 0.55, y0 + wh - m(0.22), m(0.18), m(0.2));
    g.fillStyle = "#5a7a46"; g.beginPath(); g.arc(x0 + ww * 0.55 + m(0.09), y0 + wh - m(0.3), m(0.14), 0, 7); g.fill();
  } else if (dress < 0.6) { // a "ROOMS" card
    g.fillStyle = "#efe6cf"; g.fillRect(x0 + ww * 0.25, y0 + wh * 0.55, ww * 0.5, wh * 0.18);
    g.fillStyle = "#7a1f1c"; g.font = `bold ${m(0.1)}px Georgia, serif`; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("ROOMS", x0 + ww / 2, y0 + wh * 0.64);
  }
  // curtains (several kinds)
  const ck = r();
  if (ck < 0.55) {
    g.fillStyle = pick(r, ["#e8c9b8", "#efe2c4", "#c9d6c0", "#c98a8a", "#d8c8e0"]);
    if (ck < 0.3) { g.beginPath(); g.moveTo(x0, y0); g.lineTo(x0 + ww * 0.4, y0); g.quadraticCurveTo(x0 + ww * 0.1, y0 + wh * 0.4, x0, y0 + wh * 0.8); g.fill();
      g.beginPath(); g.moveTo(x0 + ww, y0); g.lineTo(x0 + ww * 0.6, y0); g.quadraticCurveTo(x0 + ww * 0.9, y0 + wh * 0.4, x0 + ww, y0 + wh * 0.8); g.fill(); }
    else g.fillRect(x0, y0, ww, wh * U(r, 0.2, 0.45)); // half-drawn blind
  }
  // glints
  g.fillStyle = "rgba(255,255,255,0.35)";
  g.save(); g.translate(x0 + ww * 0.3, y0 + wh * 0.5); g.rotate(Math.PI / 4); g.fillRect(-m(0.03), -wh, m(0.06), wh * 2); g.restore();
  g.restore();
  // muntins + ink
  g.fillStyle = "#ece2cc"; g.fillRect(cx - m(0.02), y0, m(0.04), wh); g.fillRect(x0, y0 + wh * 0.48, ww, m(0.04));
  wobRect(g, r, x0 - tr, y0 - tr, ww + 2 * tr, wh + 2 * tr, lw);
  wobRect(g, r, x0, y0, ww, wh, lw * 0.7);
  if (r() < 0.12) { wob(g, r, [[x0 + ww * 0.6, y0 + m(0.1)], [x0 + ww * 0.75, y0 + wh * 0.25], [x0 + ww * 0.68, y0 + wh * 0.4]], lw * 0.6, "rgba(255,255,255,0.8)", 0.5); } // cracked pane
  // sill + lintel, rain streak under the sill
  g.fillStyle = "#ddd2bc"; g.fillRect(x0 - tr - m(0.07), by + tr, ww + 2 * tr + m(0.14), m(0.08));
  wobRect(g, r, x0 - tr - m(0.07), by + tr, ww + 2 * tr + m(0.14), m(0.08), lw * 0.8);
  g.fillStyle = "#ddd2bc"; g.fillRect(x0 - tr - m(0.05), y0 - tr - m(0.12), ww + 2 * tr + m(0.1), m(0.12));
  wobRect(g, r, x0 - tr - m(0.05), y0 - tr - m(0.12), ww + 2 * tr + m(0.1), m(0.12), lw * 0.8);
  const st = g.createLinearGradient(0, by + tr, 0, by + tr + m(0.9)); st.addColorStop(0, "rgba(60,45,40,0.22)"); st.addColorStop(1, "rgba(60,45,40,0)");
  g.fillStyle = st; g.fillRect(x0 + ww * 0.1, by + tr + m(0.08), ww * 0.8, m(0.9));
  if (r() < 0.22) flowerBox(g, r, x0 - tr, by + tr, ww + 2 * tr, m);
};

const doorInk = (g: G, r: R, cx: number, H: number, m: (v: number) => number) => {
  const dw = m(1.15), dh = m(2.2), lw = Math.max(1.6, m(0.024));
  g.fillStyle = "#ddd2bc"; g.fillRect(cx - dw / 2 - m(0.14), H - dh - m(0.2), dw + m(0.28), dh + m(0.2));
  g.fillStyle = pick(r, ["#6a3e28", "#3f4a3a", "#5a2a2a", "#2f3a4a"]); g.fillRect(cx - dw / 2, H - dh, dw, dh);
  mottle(g, r, cx - dw / 2, H - dh, dw, dh, 30, m(0.2), ["#000000", "#ffffff"], 0.07);
  for (const [px, py] of [[0.1, 0.08], [0.55, 0.08], [0.1, 0.52], [0.55, 0.52]]) wobRect(g, r, cx - dw / 2 + dw * px, H - dh + dh * py, dw * 0.35, dh * 0.38, lw * 0.6, "rgba(20,10,10,0.6)");
  g.fillStyle = "#c8a24a"; g.beginPath(); g.arc(cx + dw * 0.32, H - dh * 0.48, m(0.04), 0, 7); g.fill();
  wobRect(g, r, cx - dw / 2, H - dh, dw, dh, lw);
  wobRect(g, r, cx - dw / 2 - m(0.14), H - dh - m(0.2), dw + m(0.28), dh + m(0.2), lw);
  // fanlight
  g.fillStyle = "#6a6f9a"; g.fillRect(cx - dw / 2, H - dh - m(0.18), dw, m(0.16));
  // house number on a plate
  g.fillStyle = "#efe6cf"; g.fillRect(cx + dw / 2 + m(0.2), H - dh * 0.75, m(0.2), m(0.14)); wobRect(g, r, cx + dw / 2 + m(0.2), H - dh * 0.75, m(0.2), m(0.14), lw * 0.5);
};

export type FacadeOpts = { wall: string; shutter: string; door?: boolean; timber?: boolean; brick?: boolean; posters?: boolean };
/** the illustrated facade (drop-in for facadeHD): same window grid (nWin = floor(w / 2.2), sill fl * 2.8 + 0.9) */
export const facadeInk = (key: string, wm: number, hm: number, o: FacadeOpts) => {
  const PX = Math.min(80, 2048 / Math.max(wm, hm));
  const W = Math.round(wm * PX), H = Math.round(hm * PX), m = (v: number) => v * PX;
  return ctex("facInk" + key, W, H, (g, r) => {
    const base = o.brick ? "#b9694a" : o.wall;
    g.fillStyle = base; g.fillRect(0, 0, W, H);
    // light from the top, grime toward the street
    const sh = g.createLinearGradient(0, 0, 0, H); sh.addColorStop(0, "rgba(255,250,240,0.10)"); sh.addColorStop(0.7, "rgba(0,0,0,0)"); sh.addColorStop(1, "rgba(60,40,30,0.25)");
    g.fillStyle = sh; g.fillRect(0, 0, W, H);
    mottle(g, r, 0, 0, W, H, Math.round(wm * hm * 14), m(0.22), [shadeRGB(base, 0.88), shadeRGB(base, 1.08), shadeRGB(base, 0.94)], 0.12);
    if (o.brick) { // drawn bricks in patches and courses that fade in and out (never a full tiled wall)
      const bw = m(0.25), bh = m(0.085);
      for (let y = 0, row = 0; y < H; y += bh, row++) {
        if (r() < 0.35) wob(g, r, [[0, y], [W, y]], Math.max(1, m(0.008)), "rgba(240,215,180,0.35)", 0.5);
        for (let x = -(row % 2) * bw / 2; x < W; x += bw) {
          const n = Math.sin(x * 0.004 + row * 0.7) + Math.sin(x * 0.0017 - row * 0.3);
          if (n < 0.05) continue; // v3: denser drawn brick (teardown edge density)
          g.fillStyle = shadeRGB(pick(r, ["#b9694a", "#a85a40", "#c47a55", "#9a5038"]), U(r, 0.9, 1.08)); g.fillRect(x + 1, y + 1, bw - 2, bh - 2);
          g.strokeStyle = "rgba(60,30,25,0.45)"; g.lineWidth = Math.max(1, m(0.008)); g.strokeRect(x + 1, y + 1, bw - 2, bh - 2);
        }
      }
    } else { // plaster: drawn ashlar block courses (v3 edge density), a few patches fallen off showing brick, hairline cracks
      const ch = m(0.5), cw = m(1.1);
      for (let y = H - m(0.45), row = 0; y > 0; y -= ch, row++) {
        wob(g, r, [[0, y], [W, y]], Math.max(1, m(0.012)), "rgba(70,50,40,0.42)", 0.5);
        for (let x = (row % 2) * cw / 2; x < W; x += cw * U(r, 0.85, 1.15)) wob(g, r, [[x, y], [x, y - ch]], Math.max(1, m(0.01)), "rgba(70,50,40,0.36)", 0.4);
      }
      for (let i = 0; i < Math.round(wm * hm / 90); i++) {
        const px = U(r, 0, W), py = U(r, H * 0.2, H * 0.9), pw = m(U(r, 0.5, 1.2)), ph = m(U(r, 0.3, 0.6));
        g.fillStyle = "#a85a40"; g.beginPath(); g.ellipse(px, py, pw / 2, ph / 2, U(r, -0.3, 0.3), 0, 7); g.fill();
        for (let k = 0; k < 4; k++) { const yy = py - ph / 3 + k * ph / 5; wob(g, r, [[px - pw / 3, yy], [px + pw / 3, yy]], Math.max(1, m(0.01)), "rgba(240,215,180,0.6)", 0.3); }
        g.beginPath(); g.ellipse(px, py, pw / 2, ph / 2, 0, 0, 7); g.strokeStyle = "rgba(60,40,30,0.55)"; g.lineWidth = Math.max(1, m(0.015)); g.stroke();
      }
    }
    for (let i = 0; i < 3 + Math.round(wm / 6); i++) { let x = U(r, 0, W), y = U(r, 0, H * 0.8); const pts: P[] = [[x, y]]; for (let k = 0; k < 4; k++) { x += m(U(r, -0.1, 0.1)); y += m(U(r, 0.05, 0.14)); pts.push([x, y]); } wob(g, r, pts, Math.max(1, m(0.012)), "rgba(50,35,35,0.55)", 0.4); }
    if (o.timber) { const t = m(0.18); for (const x of [0, W - t]) { g.fillStyle = "#6e4a30"; g.fillRect(x, 0, t, H); wobRect(g, r, x, 0, t, H, m(0.02)); } }
    const floors = Math.max(1, Math.floor(hm / 2.8)), nWin = Math.max(1, Math.floor(wm / 2.2));
    // string course + plinth drawn
    for (let fl = 1; fl < floors; fl++) wob(g, r, [[0, H - m(fl * 2.8) + m(0.05)], [W, H - m(fl * 2.8) + m(0.05)]], Math.max(1.5, m(0.02)), "rgba(42,30,36,0.7)", 0.6);
    g.fillStyle = "rgba(70,55,45,0.3)"; g.fillRect(0, H - m(0.45), W, m(0.45)); wob(g, r, [[0, H - m(0.45)], [W, H - m(0.45)]], Math.max(1.5, m(0.02)));
    // posters pasted low on the walls, a drainpipe, a gas-lamp bracket
    // v8 (rule 63): posters only on the wall piers BETWEEN window/door columns, so a door or shop window never cuts one
    if (o.posters !== false) { const nW = Math.max(1, Math.floor(wm / 2.2)), col = W / nW;
      for (let i = 1; i < nW; i++) if (r() < 0.6) { const pw = Math.min(m(U(r, 0.45, 0.6)), col - m(2.02)); /* v17 (owner rule 63): clear of the open shutters too (window + shutters = 1.91 m wide) */ if (pw > m(0.28)) poster(g, r, i * col - pw / 2, H - m(U(r, 1.7, 2.3)), pw, pw * U(r, 1.25, 1.45)); } }
    if (r() < 0.8) { const x = r() < 0.5 ? m(0.25) : W - m(0.35); g.fillStyle = "#5a5a62"; g.fillRect(x, 0, m(0.1), H); wob(g, r, [[x, 0], [x, H]], m(0.015)); wob(g, r, [[x + m(0.1), 0], [x + m(0.1), H]], m(0.015)); for (let y = m(1.5); y < H; y += m(2.2)) { g.fillStyle = "#3a3a40"; g.fillRect(x - m(0.04), y, m(0.18), m(0.05)); } }
    for (let fl = 0; fl < floors; fl++) for (let i = 0; i < nWin; i++) {
      const cx = ((i + 0.5) * W) / nWin, by = H - m(fl * 2.8 + 0.9);
      if (o.door && fl === 0 && i === Math.floor(nWin / 2)) { doorInk(g, r, cx, H, m); continue; }
      windowInk(g, r, cx, by, m, o.shutter, r() < 0.08);
    }
    // outer ink edge (the wall's silhouette is also inked by the world pass)
    wobRect(g, r, 1, 1, W - 2, H - 2, Math.max(2, m(0.03)), "rgba(42,30,36,0.8)", 0.8);
  });
};

/** painted street mud, 2048 px = 16 m: drawn ruts, hoofprints, straw, stones with ink, puddle rims, cabbage leaves */
export const mudInk = (key: string, ruts: boolean, pal = ["#8a7258", "#6f5a44", "#9a8266", "#7d6650", "#a08a6c", "#5f5040"]) => ctex("mudInk" + key, 2048, 2048, (g, r) => {
  const S = 2048, m = (v: number) => (v * S) / 16;
  g.fillStyle = pal[0]; g.fillRect(0, 0, S, S);
  mottle(g, r, 0, 0, S, S, 2600, m(0.5), pal.slice(1), 0.22);
  if (ruts) for (const y of [0.3, 0.37, 0.63, 0.7]) {
    const pts: P[] = []; for (let x = 0; x <= S; x += 64) pts.push([x, y * S + 10 * Math.sin(x * 0.01 + y * 9)]);
    wob(g, r, pts, m(0.12), "rgba(70,52,38,0.55)", 2); wob(g, r, pts.map(([x, yy]) => [x, yy - m(0.08)] as P), m(0.03), "rgba(200,175,140,0.45)", 1.5);
  }
  for (let i = 0; i < 160; i++) { // hoofprints
    const x = r() * S, y = r() * S; g.strokeStyle = "rgba(50,36,28,0.75)"; g.lineWidth = m(0.025);
    g.beginPath(); g.arc(x, y, m(0.09), 0.3, Math.PI * 2 - 0.3); g.stroke();
  }
  for (let i = 0; i < 260; i++) { // straw
    const x = r() * S, y = r() * S, a = r() * 6, l = m(U(r, 0.08, 0.2));
    g.strokeStyle = pick(r, ["#d9b860", "#c9a050"]); g.lineWidth = m(0.012); g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke();
  }
  for (let i = 0; i < 140; i++) { // stones
    const x = r() * S, y = r() * S, rr = m(U(r, 0.03, 0.08));
    g.fillStyle = pick(r, ["#a89c8c", "#8a8278", "#bdb3a2"]); g.beginPath(); g.ellipse(x, y, rr, rr * 0.7, r() * 3, 0, 7); g.fill();
    g.strokeStyle = "rgba(42,30,36,0.7)"; g.lineWidth = m(0.012); g.stroke();
  }
  for (let i = 0; i < 18; i++) { // drying puddle stains with ink rims
    const x = r() * S, y = r() * S, rx = m(U(r, 0.4, 1.0)), ry = rx * U(r, 0.4, 0.7);
    g.fillStyle = "rgba(100,84,66,0.22)"; g.beginPath(); g.ellipse(x, y, rx, ry, 0, 0, 7); g.fill();
    g.strokeStyle = "rgba(42,30,36,0.25)"; g.lineWidth = m(0.015); g.stroke();
  }
  // v8 (teardown: dense drawn ground): wandering cart tracks, puddles with sky in them and an ink rim, plank scraps
  for (let i = 0; i < 6; i++) {
    let x = r() * S, y = r() * S, a = r() * 6; const pts: P[] = [];
    for (let k = 0; k < 40; k++) { pts.push([x, y]); a += U(r, -0.08, 0.08); x += Math.cos(a) * 52; y += Math.sin(a) * 52; }
    for (const off of [-m(0.7), m(0.7)]) wob(g, r, pts.map(([px, py]) => [px - Math.sin(a) * off, py + Math.cos(a) * off] as P), m(0.05), "rgba(58,42,32,0.7)", 1.5);
  }
  for (let i = 0; i < 26; i++) {
    const x = r() * S, y = r() * S, rx = m(U(r, 0.18, 0.45)), ry = rx * U(r, 0.35, 0.6);
    g.fillStyle = "rgba(70,62,58,0.55)"; g.beginPath(); g.ellipse(x, y, rx, ry, 0, 0, 7); g.fill(); // wet dark mud, not a white blob
    g.strokeStyle = "rgba(200,210,225,0.55)"; g.lineWidth = m(0.02); g.beginPath(); g.ellipse(x - rx * 0.2, y - ry * 0.2, rx * 0.5, ry * 0.3, 0, 3.6, 5.2); g.stroke();
    g.strokeStyle = "rgba(42,30,36,0.75)"; g.lineWidth = m(0.025); g.beginPath(); g.ellipse(x, y, rx, ry, 0, 0, 7); g.stroke();
  }
  for (let i = 0; i < 8; i++) {
    const x = r() * S, y = r() * S, a = r() * 6, l = m(U(r, 0.3, 0.6)), w = m(0.09);
    g.save(); g.translate(x, y); g.rotate(a); g.fillStyle = pick(r, ["#9a7a58", "#86684a"]); g.fillRect(-l / 2, -w / 2, l, w);
    g.strokeStyle = "rgba(42,30,36,0.8)"; g.lineWidth = m(0.02); g.strokeRect(-l / 2, -w / 2, l, w); g.restore();
  }
  // v8: the green weed ovals read as loose green blobs on near ground, removed
});

/** plank sidewalk boards, drawn: 2048 px = 4 m, boards across, ink seams, knots, nails, worn middle */
export const boardsInk = () => ctex("boardsInk", 2048, 2048, (g, r) => {
  const S = 2048, B = 128;
  for (let y = 0; y < S; y += B) {
    g.fillStyle = pick(r, ["#9a7a58", "#8f7052", "#a6845e", "#88684a"]); g.fillRect(0, y, S, B);
    mottle(g, r, 0, y, S, B, 120, 60, ["#6a5038", "#b89470", "#7a5e44"], 0.25);
    for (let k = 0; k < 4; k++) { const yy = y + U(r, 15, B - 15), pts: P[] = []; for (let x = 0; x <= S; x += 128) pts.push([x, yy + U(r, -4, 4)]); wob(g, r, pts, 2.5, "rgba(55,36,24,0.6)", 1); }
    if (r() < 0.5) { const x = r() * S; g.strokeStyle = "rgba(60,40,28,0.6)"; g.lineWidth = 3; g.beginPath(); g.ellipse(x, y + B / 2, 18, 8, 0, 0, 7); g.stroke(); }
    for (const x of [r() * S * 0.5, S * 0.5 + r() * S * 0.5]) { wob(g, r, [[x, y], [x, y + B]], 5, "rgba(42,30,36,0.85)", 0.8); g.fillStyle = "#3a2a20"; g.beginPath(); g.arc(x + 14, y + 22, 5, 0, 7); g.arc(x + 14, y + B - 22, 5, 0, 7); g.fill(); }
    wob(g, r, [[0, y], [S, y]], 6, "rgba(42,30,36,0.9)", 1.2);
  }
});

/** painted far backdrop for the city: hazy rooftops, church spires, chimneys with smoke, trees, a few masts. 4096 x 1024,
 *  drawn so it repeats around a ring; the bottom 15 % is ground haze. */
export const skylineInk = (key: string, tint: [string, string], lakeSide = false) => ctex("sky" + key, 4096, 1024, (g, r) => {
  const W = 4096, H = 1024;
  g.clearRect(0, 0, W, H);
  const layer = (base: number, hmin: number, hmax: number, col: string, ink: string, n: number) => {
    let x = -40;
    while (x < W + 40) {
      const w = U(r, 50, 140), h = U(r, hmin, hmax), y = base - h;
      g.fillStyle = col; g.fillRect(x, y, w, h + 200);
      g.beginPath(); g.moveTo(x - 8, y); g.lineTo(x + w / 2, y - U(r, 20, 50)); g.lineTo(x + w + 8, y); g.closePath(); g.fill();
      wob(g, r, [[x - 8, y], [x + w / 2, y - 30], [x + w + 8, y]], 2, ink, 1);
      for (let k = 0; k < Math.floor(w / 26); k++) for (let j = 0; j < Math.floor(h / 40); j++) { g.fillStyle = ink; g.globalAlpha = 0.35; g.fillRect(x + 8 + k * 26, y + 14 + j * 40, 9, 14); g.globalAlpha = 1; }
      if (r() < 0.12) { g.fillStyle = col; g.fillRect(x + w / 2 - 10, y - 160, 20, 160); g.beginPath(); g.moveTo(x + w / 2 - 18, y - 160); g.lineTo(x + w / 2, y - 250); g.lineTo(x + w / 2 + 18, y - 160); g.fill(); wob(g, r, [[x + w / 2 - 18, y - 160], [x + w / 2, y - 250], [x + w / 2 + 18, y - 160]], 2, ink, 1); }
      if (r() < 0.2) { g.fillStyle = col; g.fillRect(x + w * 0.7, y - 50, 12, 50); for (let s = 0; s < 6; s++) { g.fillStyle = `rgba(230,225,220,${0.35 - s * 0.05})`; g.beginPath(); g.arc(x + w * 0.7 + 6 + s * 14, y - 60 - s * 22, 14 + s * 5, 0, 7); g.fill(); } }
      if (r() < 0.25) { g.fillStyle = shadeRGB(col.startsWith("#") ? col : "#9aa0b0", 0.9); g.beginPath(); g.arc(x + w + 10, base - 30, U(r, 30, 60), 0, 7); g.fill(); }
      x += w + U(r, -10, 20);
    }
    void n;
  };
  layer(H * 0.9, 330, 600, tint[0], "rgba(70,70,100,0.35)", 0);
  layer(H * 0.95, 180, 380, tint[1], "rgba(50,45,70,0.55)", 0);
  if (lakeSide) for (let i = 0; i < 10; i++) { const x = r() * W; g.fillStyle = tint[1]; g.fillRect(x, H * 0.7, 4, 160); g.beginPath(); g.moveTo(x + 4, H * 0.72); g.lineTo(x + 60, H * 0.8); g.lineTo(x + 4, H * 0.8); g.fill(); }
  const hz = g.createLinearGradient(0, H * 0.75, 0, H); hz.addColorStop(0, "rgba(220,225,235,0)"); hz.addColorStop(1, "rgba(220,225,235,0.6)");
  g.fillStyle = hz; g.fillRect(0, H * 0.75, W, H * 0.25);
});

/** a far landscape band: rolling hills, tree lines, a far shore (swamp, river) */
export const hillsInk = (key: string, cols: string[]) => ctex("hills" + key, 4096, 1024, (g, r) => {
  const W = 4096, H = 1024;
  g.clearRect(0, 0, W, H);
  cols.forEach((c, k) => {
    const base = H * (0.55 + k * 0.12), amp = 80 - k * 15, pts: P[] = [];
    for (let x = 0; x <= W; x += 64) pts.push([x, base - amp * (0.5 + 0.5 * Math.sin(x * 0.0021 * (k + 1) + k * 2) * Math.sin(x * 0.0007 + k))]);
    g.fillStyle = c; g.beginPath(); g.moveTo(0, H); pts.forEach(([x, y]) => g.lineTo(x, y)); g.lineTo(W, H); g.closePath(); g.fill();
    for (let i = 0; i < 90; i++) { const x = r() * W, y = pts[Math.min(pts.length - 1, Math.floor(x / 64))][1]; g.fillStyle = shadeRGB(c, 0.85); g.beginPath(); g.arc(x, y, U(r, 10, 26), Math.PI, 0); g.fill(); }
    wob(g, r, pts, 2.5, "rgba(50,40,60,0.45)", 1.5);
  });
});

/** wallpaper + wainscot for interiors, drawn: a damask motif in ink-tinted paint, picture frames, a skirting rail */
export const wallpaperInk = (key: string, paper: string, motif: string, wains: string) => ctex("wp" + key, 1024, 2048, (g, r) => {
  const W = 1024, H = 2048;
  g.fillStyle = paper; g.fillRect(0, 0, W, H);
  mottle(g, r, 0, 0, W, H, 900, 60, [shadeRGB(paper, 0.9), shadeRGB(paper, 1.08)], 0.2);
  // v3 (teardown edge density): drawn stripes + inked damask motifs
  for (let x = 0; x < W; x += 150) { wob(g, r, [[x + 75, 0], [x + 75, H * 0.64]], 3, shadeRGB(paper, 0.72), 1); wob(g, r, [[x + 83, 0], [x + 83, H * 0.64]], 2, shadeRGB(paper, 0.78), 1); }
  for (let y = 60; y < H * 0.62; y += 150) for (let x = (y / 150) % 2 ? 0 : 75; x < W + 40; x += 150) {
    g.fillStyle = motif; g.globalAlpha = 0.8;
    g.beginPath(); g.moveTo(x, y - 34); g.quadraticCurveTo(x + 28, y, x, y + 34); g.quadraticCurveTo(x - 28, y, x, y - 34); g.fill();
    g.globalAlpha = 1; g.strokeStyle = shadeRGB(motif, 0.55); g.lineWidth = 3; g.stroke();
    g.fillStyle = shadeRGB(motif, 0.6); g.beginPath(); g.arc(x, y, 8, 0, 7); g.fill();
    g.strokeStyle = shadeRGB(motif, 0.65); g.lineWidth = 2.5; g.beginPath(); g.arc(x - 22, y + 30, 10, 0, 4); g.stroke(); g.beginPath(); g.arc(x + 22, y + 30, 10, Math.PI - 1, Math.PI * 2 - 0.2); g.stroke();
  }
  const wy = H * 0.64;
  g.fillStyle = wains; g.fillRect(0, wy, W, H - wy);
  mottle(g, r, 0, wy, W, H - wy, 300, 50, [shadeRGB(wains, 0.85), shadeRGB(wains, 1.15)], 0.25);
  for (let x = 24; x < W; x += 250) wobRect(g, r, x, wy + 70, 200, H - wy - 160, 5, "rgba(30,20,20,0.7)");
  // v19f (edge floor): raised-panel bevels, carved rosettes and grain inside each wainscot panel
  for (let x = 24; x < W; x += 250) {
    wobRect(g, r, x + 22, wy + 92, 156, H - wy - 204, 3, shadeRGB(wains, 1.6));
    wobRect(g, r, x + 34, wy + 104, 132, H - wy - 228, 3, "rgba(30,20,20,0.6)");
    for (let k = 0; k < 5; k++) wob(g, r, [[x + 50 + k * 25, wy + 130], [x + 50 + k * 25 + (k % 2 ? 6 : -6), H - 160]], 2, shadeRGB(wains, 0.7), 1);
    const cx = x + 100, cy = wy + 110 + (H - wy - 228) / 2;
    g.fillStyle = shadeRGB(wains, 1.35); g.beginPath(); g.arc(cx, cy, 30, 0, 7); g.fill(); g.strokeStyle = HINK; g.lineWidth = 4; g.stroke();
    for (let k = 0; k < 8; k++) { const a = k * Math.PI / 4; g.beginPath(); g.moveTo(cx, cy); g.lineTo(cx + Math.cos(a) * 26, cy + Math.sin(a) * 26); g.lineWidth = 2.5; g.stroke(); }
  }
  for (let x = 0; x < W; x += 40) wob(g, r, [[x, wy + 34], [x, wy + 62]], 2.5, HINK, 1); // dentil band under the dado rail
  wob(g, r, [[0, wy], [W, wy]], 10, HINK, 1); wob(g, r, [[0, wy + 30], [W, wy + 30]], 4, HINK, 1);
  wob(g, r, [[0, H - 50], [W, H - 50]], 6, HINK, 1);
});
