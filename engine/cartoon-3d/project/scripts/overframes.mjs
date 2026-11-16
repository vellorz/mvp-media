// renders the second ("over") layer of every dissolve frame as PNGs: node overframes.mjs <proj> <Comp> <dissolves.json> <outDir> [conc]
import { bundle } from "@remotion/bundler";
import { selectComposition, renderFrames } from "@remotion/renderer";
import fs from "fs"; import path from "path";
const [proj, comp, dj, outDir, conc = "1"] = process.argv.slice(2);
const D = JSON.parse(fs.readFileSync(dj, "utf8")).map((x) => x[0]).filter((n) => !fs.existsSync(path.join(outDir, `over_${String(n).padStart(4, "0")}.png`)));
if (!D.length) { console.log("RENDERED"); process.exit(0); }
fs.mkdirSync(outDir, { recursive: true });
const serveUrl = await bundle({ entryPoint: path.join(proj, "src/index.ts") });
const chromiumOptions = { gl: "swangle" };
const tmp = outDir + "/tmp";
for (let c = 0; c < D.length; c += 20) {
  const F = D.slice(c, c + 20), ip = { only: "over", frames: F };
  fs.rmSync(tmp, { recursive: true, force: true }); fs.mkdirSync(tmp, { recursive: true });
  const composition = await selectComposition({ serveUrl, id: comp, inputProps: ip, chromiumOptions, timeoutInMilliseconds: 1500000 });
  await renderFrames({ serveUrl, composition, inputProps: ip, outputDir: tmp, imageFormat: "png", frameRange: [0, F.length - 1], scale: Number(process.env.SCALE || 1), concurrency: Number(conc), chromiumOptions, timeoutInMilliseconds: 1500000,
    onStart: () => {}, onFrameUpdate: () => {}, logLevel: "error" });
  for (const f of fs.readdirSync(tmp).sort()) { const i = Number(f.match(/(\d+)\.png$/)[1]); fs.renameSync(path.join(tmp, f), path.join(outDir, `over_${String(F[i]).padStart(4, "0")}.png`)); }
  console.log("chunk", F[0], F[F.length - 1]);
}
console.log("RENDERED", D.length);
