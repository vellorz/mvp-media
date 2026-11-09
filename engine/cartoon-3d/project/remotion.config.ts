import { Config } from "@remotion/cli/config";
// three.js needs WebGL in headless Chrome: "angle" uses the GPU on Windows/macOS; Linux/cloud boxes without a GPU need
// "swangle" (software). Software rendering is slow, so the delayRender timeout is raised to 4 min.
Config.setChromiumOpenGlRenderer(process.platform === "linux" ? "swangle" : "angle");
Config.setDelayRenderTimeoutInMilliseconds(240000);
Config.setVideoImageFormat("jpeg");
