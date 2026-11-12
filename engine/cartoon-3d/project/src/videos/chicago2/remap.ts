// Tuesday short: the voice-over was recorded for this picture, so the film runs straight on its own timeline (one
// segment per shot, identity mapping). Kept in the remap shape so the shared composition code stays the same.
import { SHOTS, TOTAL, POSTER_AT, FLASH_AT } from "./story";
export type Seg = { shot: number; pts: [number, number][] };
export const SEGS: Seg[] = SHOTS.map((s) => ({ shot: s.id, pts: [[s.a, s.a], [s.b, s.b]] }));
export const NEW_POSTER_AT = POSTER_AT;
export const NEW_TOTAL = TOTAL;
export const NEW_FLASH_AT = FLASH_AT;
export const SALE_UNTIL_OLD = -1;
function interp(p: [number, number][], n: number) {
  if (n <= p[0][0]) { const [a, b] = [p[0], p[1]]; return a[1] + ((n - a[0]) * (b[1] - a[1])) / (b[0] - a[0]); }
  for (let i = 1; i < p.length; i++) if (n <= p[i][0]) { const a = p[i - 1], b = p[i]; return a[1] + ((n - a[0]) * (b[1] - a[1])) / (b[0] - a[0] || 1); }
  const a = p[p.length - 2], b = p[p.length - 1]; return b[1] + ((n - b[0]) * (b[1] - a[1])) / (b[0] - a[0]);
}
export const segAt = (n: number) => { for (let i = 0; i < SEGS.length; i++) if (n < SEGS[i].pts[SEGS[i].pts.length - 1][0] || i === SEGS.length - 1) return i; return SEGS.length - 1; };
export const oldOf = (i: number, n: number) => interp(SEGS[i].pts, n);
export const DISSOLVE = 10;
export const segLayers = (n: number): { seg: number; old: number; alpha: number }[] => {
  const i = segAt(n), start = SEGS[i].pts[0][0];
  if (i > 0 && n < start + DISSOLVE / 2 + 0.5 && n >= start - DISSOLVE / 2 && Math.round(start) !== NEW_FLASH_AT) {
    const a = (n - (start - DISSOLVE / 2) + 1) / (DISSOLVE + 1);
    return [{ seg: i - 1, old: n, alpha: 1 }, { seg: i, old: n, alpha: a }];
  }
  const end = SEGS[i].pts[SEGS[i].pts.length - 1][0];
  if (i + 1 < SEGS.length && n >= end - DISSOLVE / 2 && Math.round(end) !== NEW_FLASH_AT) {
    const a = (n - (end - DISSOLVE / 2) + 1) / (DISSOLVE + 1);
    return [{ seg: i, old: n, alpha: 1 }, { seg: i + 1, old: n, alpha: a }];
  }
  return [{ seg: i, old: n, alpha: 1 }];
};
