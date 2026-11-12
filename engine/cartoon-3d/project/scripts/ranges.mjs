// usage: node ranges.mjs <projDir> <Comp> <ranges.json> <outDir> [concurrency]
import { bundle } from "@remotion/bundler";
import { selectComposition, renderMedia } from "@remotion/renderer";
import fs from "fs"; import path from "path";
const [proj, comp, rj, outDir, conc = "3"] = process.argv.slice(2);
const R = JSON.parse(fs.readFileSync(rj, "utf8"));
const serveUrl = await bundle({ entryPoint: path.join(proj, "src/index.ts") });
const chromiumOptions = { gl: "swangle" };
const inputProps = process.env.ONLY ? { only: process.env.ONLY } : {};
const composition = await selectComposition({ serveUrl, id: comp, inputProps, chromiumOptions, timeoutInMilliseconds: 1500000 });
for (const [a, b] of R) {
  const out = path.join(outDir, `seg_${String(a).padStart(4, "0")}.mp4`);
  if (fs.existsSync(out) && fs.statSync(out).size > 0) continue;
  const t0 = Date.now();
  await renderMedia({ serveUrl, composition, inputProps, codec: "h264", crf: 16, outputLocation: out + ".tmp.mp4", frameRange: [a, b], scale: Number(process.env.SCALE || 1), concurrency: Number(conc), chromiumOptions, logLevel: "error", timeoutInMilliseconds: 1500000 });
  fs.renameSync(out + ".tmp.mp4", out);
  console.log("seg", a, b, ((Date.now() - t0) / 1000).toFixed(0) + "s");
}
console.log("RENDERED");
