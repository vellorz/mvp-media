// Round 2: the new voice-over (voice2/c.words.json, tightened + 1.12x) is retold in a new order with new beats, so the
// film is cut from the round-1 timeline: each segment of the new film plays one round-1 shot over a range of round-1
// frames, piecewise-linear through word anchors (new word time -> old word time). Everything in story/world/cast
// keeps running in round-1 ("old") frames; only this map, the dissolves, the captions and the end card see new frames.
const FPS = 30, OFF = 0.2;
const nf = (w: number) => (w + OFF) * FPS; // new word time -> new frame
const of = (w: number) => (w + OFF) * FPS; // old word time -> old frame
export type Seg = { shot: number; pts: [number, number][] }; // [newFrame, oldFrame] anchors, ascending in new frames
const S = (shot: number, pts: [number, number][]): Seg => ({ shot, pts });
// anchors: [new word s, old word s] (old values from voice/words.json or the round-1 shot frames /30 - 0.2)
const A = (n: number, o: number): [number, number] => [nf(n), of(o)];
const AF = (n: number, oFrame: number): [number, number] => [nf(n), oFrame];
export const SEGS: Seg[] = [
  S(1, [[0, 0], A(3.72, 2.38), A(5.02, 4.9), AF(5.8, 186)]),                     // hook: price, bridge parked in the desert
  S(2, [AF(5.8, 186), A(7.52, 8.3), AF(8.18, 306)]),                               // "You see, in 1968, London Bridge"
  S(3, [[nf(8.18) - 4, 406], AF(8.18, 406), [263, 399 + (263 - nf(8.18)) * (396 + (290 - nf(8.18)) * (452 - 396) / (nf(11.32) - nf(8.18)) - 399) / (290 - nf(8.18))], [290, 396 + (290 - nf(8.18)) * (452 - 396) / (nf(11.32) - nf(8.18))], AF(11.32, 452)]), // sinking (r3: starts on the pier cut, no bus flash; same mapping from frame 290)
  S(3, [AF(11.32, 312), AF(12.84, 392)]),                                          // couldn't handle the traffic (honks)
  S(4, [AF(12.84, 455), A(13.8, 16.24), A(15.06, 17.54), A(15.2, 17.72), A(15.78, 18.52), A(16.28, 18.98), AF(16.84, 583)]), // FOR SALE
  S(5, [AF(16.84, 583), A(17.84, 20.82), A(18.54, 21.6), A(18.62, 21.68), AF(20.04, 694)]), // McCulloch, chainsaw tycoon
  S(6, [AF(20.04, 697), AF(22.16, 758)]),                                          // brand new town by a lake
  S(7, [AF(22.16, 760), A(26.32, 27.1), AF(26.98, 838)]),                          // "craziest idea" ... bought it anyway (bag)
  S(8, [AF(26.98, 838), A(28.64, 29.94), AF(30.46, 956)]),                         // workers, numbered every stone
  S(9, [AF(30.46, 958), AF(32.28, 1011)]),                                         // Panama Canal
  S(10, [AF(32.28, 1012), AF(33.82, 1069)]),                                       // trucks across the desert
  S(11, [AF(33.82, 1072), A(34.08, 35.9), A(35.4, 37.44), AF(36.12, 1137)]),       // piece by piece
  S(12, [AF(36.12, 1140), A(36.3, 39.7), AF(38.04, 1237)]),                        // luckily, not sinking
  S(13, [AF(38.04, 1245), A(39.46, 43.58), A(39.9, 44.6), AF(42.16, 1393)]),       // unluckily, no water; built on dry land
  S(14, [AF(42.16, 1395), A(43.0, 48.9), A(44.32, 50.52), AF(45.08, 1538)]),       // dug a canal, flood
  S(15, [AF(45.08, 1539), A(46.94, 53.24), AF(47.76, 1625)]),                      // frame first, picture later
  S(16, [AF(47.76, 1626), A(50.52, 56.2), A(52.06, 58.2), AF(54.44, 1796)]),       // never the point, bait, people came
  S(17, [AF(54.44, 1797), A(58.2, 60.96), A(58.92, 61.7), A(60.32, 63.16), AF(61.02 + 0.2 * 0, 1927 - 6), [nf(61.02) + 1, 1927]]), // sold land, rumor
  S(17, [[nf(61.02) + 1, 1927], [nf(61.02) + 1 + 150, 2077]]),                     // end card
];
export const NEW_POSTER_AT = Math.round(nf(61.02)) + 1;
export const NEW_TOTAL = Math.round(nf(64.4) + 1.55 * FPS);
export const NEW_FLASH_AT = Math.round(nf(5.8));
export const SALE_UNTIL_OLD = (() => { const s = SEGS[17]; return interp(s.pts, nf(56.3)); })();

function interp(p: [number, number][], n: number) {
  if (n <= p[0][0]) { const [a, b] = [p[0], p[1]]; return a[1] + ((n - a[0]) * (b[1] - a[1])) / (b[0] - a[0]); }
  for (let i = 1; i < p.length; i++) if (n <= p[i][0]) { const a = p[i - 1], b = p[i]; return a[1] + ((n - a[0]) * (b[1] - a[1])) / (b[0] - a[0] || 1); }
  const a = p[p.length - 2], b = p[p.length - 1]; return b[1] + ((n - b[0]) * (b[1] - a[1])) / (b[0] - a[0]);
}
export const segAt = (n: number) => { for (let i = 0; i < SEGS.length; i++) if (n < SEGS[i].pts[SEGS[i].pts.length - 1][0] || i === SEGS.length - 1) return i; return SEGS.length - 1; };
export const oldOf = (i: number, n: number) => interp(SEGS[i].pts, n);
/** new frame -> layers to draw: [{segment, old frame, alpha}], with a 6-frame dissolve on every segment change
 *  (measured reference: dissolves of 6 frames are the most common, then 8) except into the white hook flash. */
export const DISSOLVE = 6;
export const segLayers = (n: number): { seg: number; old: number; alpha: number }[] => {
  const i = segAt(n), start = SEGS[i].pts[0][0];
  const jump = (k: number, at: number) => Math.abs(oldOf(k, at) - oldOf(k + 1, at)) > 2 || SEGS[k].shot !== SEGS[k + 1].shot;
  if (i > 0 && n < start + DISSOLVE / 2 + 0.5 && n >= start - DISSOLVE / 2 && Math.round(start) !== NEW_FLASH_AT && jump(i - 1, start)) {
    const a = (n - (start - DISSOLVE / 2) + 1) / (DISSOLVE + 1);
    return [{ seg: i - 1, old: oldOf(i - 1, n), alpha: 1 }, { seg: i, old: oldOf(i, n), alpha: a }];
  }
  const end = SEGS[i].pts[SEGS[i].pts.length - 1][0];
  if (i + 1 < SEGS.length && n >= end - DISSOLVE / 2 && Math.round(end) !== NEW_FLASH_AT && jump(i, end)) {
    const a = (n - (end - DISSOLVE / 2) + 1) / (DISSOLVE + 1);
    return [{ seg: i, old: oldOf(i, n), alpha: 1 }, { seg: i + 1, old: oldOf(i + 1, n), alpha: a }];
  }
  return [{ seg: i, old: oldOf(i, n), alpha: 1 }];
};
