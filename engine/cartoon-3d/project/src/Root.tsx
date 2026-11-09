// Lists every composition. Add one <Composition> per short (copy src/videos/bridge to src/videos/<name>).
import React from "react";
import { Composition } from "remotion";
import { BridgeShort, BRIDGE_FRAMES } from "./videos/bridge/Bridge";
import { HavasuShort, HAVASU_FRAMES } from "./videos/havasu/Havasu";
import { EiffelShort, EIFFEL_FRAMES } from "./videos/eiffel/Eiffel";
import { PisaShort, PISA_FRAMES } from "./videos/pisa/Pisa";

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="BridgeShort" component={BridgeShort} durationInFrames={BRIDGE_FRAMES} fps={30} width={1080} height={1920} />
    <Composition id="HavasuShort" component={HavasuShort} durationInFrames={HAVASU_FRAMES} fps={30} width={1080} height={1920} />
    <Composition id="EiffelShort" component={EiffelShort} durationInFrames={EIFFEL_FRAMES} fps={30} width={1080} height={1920} />
    <Composition id="PisaShort" component={PisaShort} durationInFrames={PISA_FRAMES} fps={30} width={1080} height={1920} />
  </>
);
