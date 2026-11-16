// which 3D layers a frame shows: segment dissolves from the timeline, and inside one segment the in-shot camera cut
// dissolves (base layer frozen on the pre-cut camera, over layer fading in). Pure, so the 2K split render can use it.
import { cutPre } from "./story";
import { NEW_POSTER_AT, SEGS, segLayers, oldOf } from "./remap";
export type Layer = { id: number; of: number; alpha: number; pre?: number };
export const layersFor = (n: number): Layer[] => {
  const segs = segLayers(Math.min(n, NEW_POSTER_AT + 13));
  let layers: Layer[] = segs.map((l) => ({ id: SEGS[l.seg].shot, of: l.old, alpha: l.alpha }));
  if (layers.length === 1) {
    const { id, of } = layers[0], si = segs[0].seg;
    // cut dissolve lasts 6 new frames whatever the local speed of the old timeline
    const rate = Math.max(0.2, oldOf(si, n + 1) - oldOf(si, n)), pre = cutPre(id, of, 9 * rate);
    if (pre !== undefined) layers = [{ id, of, alpha: 1, pre }, { id, of, alpha: Math.min(1, (of - pre) / (9 * rate) + 1 / 10) }];
  }
  return layers;
};
