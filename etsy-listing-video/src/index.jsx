import { registerRoot, Composition } from 'remotion';
import { Film } from './Film';
const Root = () => <Composition id="Film" component={Film} durationInFrames={300} fps={30} width={1080} height={1080} />;
registerRoot(Root);
