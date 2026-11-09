// The ONLY file that calls registerRoot(). Never call registerRoot() anywhere else (that causes the "registerRoot() was called more than once" error).
import { registerRoot } from "remotion";
import { RemotionRoot } from "./Root";
registerRoot(RemotionRoot);
