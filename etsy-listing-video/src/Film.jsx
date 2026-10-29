import React from 'react';
import { AbsoluteFill, Img, staticFile, useCurrentFrame, interpolate, Easing } from 'remotion';

const FPS = 30, DUR = 300;
const POSTERS = [
  ['cefalu', 'Cefalù', 'Italy'],
  ['palm-springs', 'Palm Springs', 'California'],
  ['menton', 'Menton', 'France'],
  ['annapurna', 'Annapurna', 'Nepal'],
  ['porto', 'Porto', 'Portugal'],
  ['grand-canyon', 'Grand Canyon', 'Arizona'],
  ['zermatt', 'Zermatt', 'Switzerland'],
];
const SLOT = 36, XF = 9;           // frames per poster, crossfade length
const CARD_IN = 250, CARD_OUT = 286, CARD_LEN = 14;
const TAU = Math.PI * 2;
const loop = (f, periods = 1) => Math.sin((f / DUR) * TAU * periods);

const FONTS = `
@font-face{font-family:CG;src:url(${staticFile('fonts/cg.woff2')}) format('woff2');font-weight:300 700;}
@font-face{font-family:CGi;src:url(${staticFile('fonts/cg-italic.woff2')}) format('woff2');font-style:italic;}
`;

// seeded jagged edge for torn paper
function tornEdge(seed, h, amp, step) {
  let s = seed, pts = [];
  const rnd = () => ((s = (s * 9301 + 49297) % 233280) / 233280);
  for (let y = -20; y <= h + 20; y += step) pts.push([amp * (rnd() - 0.5) * 2 + (rnd() < 0.15 ? amp * 0.8 : 0), y]);
  return pts;
}
const LEFT = tornEdge(7, 1080, 14, 9), RIGHT = tornEdge(31, 1080, 14, 9);
const W = 1180; // card width incl. both torn edges
const cardPath = () => {
  const l = LEFT.map(([x, y]) => `${x + 40},${y}`).join(' ');
  const r = RIGHT.slice().reverse().map(([x, y]) => `${W - 40 + x},${y}`).join(' ');
  return `M ${l} L ${r} Z`.replace(/ (\d)/, ' $1');
};

const Wall = ({ f }) => (
  <AbsoluteFill style={{ background: 'linear-gradient(170deg,#efe3cf 0%,#e8d9c1 55%,#dcc9ad 100%)' }}>
    <svg width="1080" height="1080" style={{ position: 'absolute', inset: 0, opacity: 0.55, mixBlendMode: 'multiply' }}>
      <filter id="plaster"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="4" /><feColorMatrix values="0 0 0 0 0.55  0 0 0 0 0.47  0 0 0 0 0.38  0 0 0 0.22 0" /></filter>
      <rect width="1080" height="1080" filter="url(#plaster)" />
      <filter id="blotch"><feTurbulence type="fractalNoise" baseFrequency="0.006" numOctaves="2" seed="9" /><feColorMatrix values="0 0 0 0 0.6  0 0 0 0 0.5  0 0 0 0 0.4  0 0 0 0.25 0" /></filter>
      <rect width="1080" height="1080" filter="url(#blotch)" />
    </svg>
  </AbsoluteFill>
);

// window light: four warm panes thrown diagonally across the wall
const WindowLight = ({ f }) => {
  const dx = loop(f) * 26, dy = loop(f) * 8;
  return (
    <svg width="1080" height="1080" style={{ position: 'absolute', inset: 0, mixBlendMode: 'soft-light', opacity: 1 }}>
      <g opacity="1">
      <defs>
        <filter id="soft"><feGaussianBlur stdDeviation="14" /></filter>
        <linearGradient id="beam" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#fff6dc" stopOpacity="1" />
          <stop offset="1" stopColor="#ffd9a0" stopOpacity="0.85" />
        </linearGradient>
      </defs>
      <g transform={`translate(${520 + dx} ${-60 + dy}) skewX(-22)`} filter="url(#soft)">
        {[[0, 0], [250, 0], [0, 360], [250, 360]].map(([x, y], i) => <rect key={i} x={x} y={y} width="232" height="342" fill="url(#beam)" />)}
      </g>
      <g transform={`translate(${520 + dx} ${-60 + dy}) skewX(-22)`} filter="url(#soft)" style={{ mixBlendMode: 'screen' }} opacity="0.22">
        {[[0, 0], [250, 0], [0, 360], [250, 360]].map(([x, y], i) => <rect key={i} x={x} y={y} width="232" height="342" fill="#fff1d6" />)}
      </g>
      </g>
    </svg>
  );
};

// soft leaf shadows swaying, from a plant out of frame upper-left
const LEAVES = Array.from({ length: 26 }, (_, i) => {
  const a = i * 2.39996, r = 40 + (i % 9) * 34;
  return { x: Math.cos(a) * r * 1.3, y: Math.sin(a) * r, rot: (a * 57) % 180, s: 0.7 + ((i * 37) % 10) / 14, ph: i * 0.7 };
});
const LeafShadows = ({ f }) => {
  const sway = loop(f, 2) * 3.2;
  return (
    <svg width="1080" height="1080" style={{ position: 'absolute', inset: 0, mixBlendMode: 'multiply', opacity: 0.32 }}>
      <filter id="lblur"><feGaussianBlur stdDeviation="7" /></filter>
      <g filter="url(#lblur)" transform={`translate(70 110) rotate(${sway} -120 -160)`}>
        <path d="M -200 -200 Q 40 30 180 300" stroke="#4a3a28" strokeWidth="7" fill="none" />
        <path d="M -40 40 Q 120 80 260 60" stroke="#4a3a28" strokeWidth="5" fill="none" />
        {LEAVES.map((l, i) => (
          <ellipse key={i} cx={l.x + 40} cy={l.y + 60} rx={38 * l.s} ry={13 * l.s} fill="#4a3a28"
            transform={`rotate(${l.rot + Math.sin((f / DUR) * TAU * 2 + l.ph) * 6} ${l.x + 40} ${l.y + 60})`} />
        ))}
      </g>
    </svg>
  );
};

// frame geometry: matches the shop's real frames (walnut / black / white flat moulding,
// mitred corners, print runs edge to edge with no mat)
const PW = 470, PH = 705, M = 36;
const FW = PW + 2 * M, FH = PH + 2 * M;
const FX = (1080 - FW) / 2, FY = 80;
// sampled from the owner's "Poster Frame Colors" listing slide: [top, right, bottom, left]
const FRAMES = [
  ['#46362d', '#3a2c25', '#3b2e26', '#433329'], // walnut
  ['#262626', '#353535', '#2a2a2a', '#242424'], // black
  ['#ececec', '#dedede', '#e2e2e2', '#f1f1f1'], // white
];
const frameOf = (i) => i % FRAMES.length;

const Moulding = ({ c, opacity }) => {
  const o = M, w = FW, h = FH;
  const sides = [
    `0,0 ${w},0 ${w - o},${o} ${o},${o}`,
    `${w},0 ${w},${h} ${w - o},${h - o} ${w - o},${o}`,
    `0,${h} ${w},${h} ${w - o},${h - o} ${o},${h - o}`,
    `0,0 0,${h} ${o},${h - o} ${o},${o}`,
  ];
  return (
    <svg width={w} height={h} style={{ position: 'absolute', inset: 0, opacity }}>
      {sides.map((pts, i) => <polygon key={i} points={pts} fill={c[i]} />)}
      {/* mitre seams, outer edge highlight, inner lip shadow */}
      {[[0, 0, o, o], [w, 0, w - o, o], [0, h, o, h - o], [w, h, w - o, h - o]].map(([a, b, x, y], i) =>
        <line key={i} x1={a} y1={b} x2={x} y2={y} stroke="rgba(0,0,0,0.18)" strokeWidth="1" />)}
      <rect x="0.5" y="0.5" width={w - 1} height={h - 1} fill="none" stroke="rgba(255,255,255,0.10)" />
      <rect x={o - 1} y={o - 1} width={w - 2 * o + 2} height={h - 2 * o + 2} fill="none" stroke="rgba(0,0,0,0.28)" strokeWidth="2" />
    </svg>
  );
};

const Frame = ({ f, idx, mix }) => {
  const glare = interpolate((f % 150) / 150, [0, 1], [-60, 160]);
  const lightOnFrame = 0.04 + 0.03 * loop(f);
  const cur = frameOf(idx), prev = mix.prev >= 0 ? frameOf(mix.prev) : -1;
  return (
    <div style={{ position: 'absolute', left: FX, top: FY, width: FW, height: FH }}>
      {/* cast shadow on wall */}
      <div style={{ position: 'absolute', inset: 0, transform: 'translate(-14px, 20px)', background: 'rgba(60,40,20,0.36)', filter: 'blur(20px)' }} />
      <div style={{ position: 'absolute', inset: 0, transform: 'translate(-3px, 5px)', background: 'rgba(50,32,16,0.35)', filter: 'blur(4px)' }} />
      {/* frame finish switches cleanly halfway through the art crossfade (no muddy blend) */}
      <Moulding c={FRAMES[prev >= 0 && mix.t < 0.5 ? prev : cur]} opacity={1} />
      {/* print sits directly against the moulding */}
      <div style={{ position: 'absolute', left: M, top: M, width: PW, height: PH, overflow: 'hidden', boxShadow: 'inset 2px 2px 4px rgba(0,0,0,0.25)' }}>
        {POSTERS.map(([file], i) => {
          const o = i === idx ? 1 : i === mix.prev ? 1 - mix.t : 0;
          if (o <= 0) return null;
          return <Img key={file} src={staticFile(`posters/${file}.png`)} style={{ position: 'absolute', width: PW, height: PH, objectFit: 'cover', opacity: i === idx ? 1 : o, zIndex: i === idx ? 1 : 2 }} />;
        })}
        <div style={{ position: 'absolute', inset: 0, zIndex: 3, boxShadow: 'inset 3px 3px 5px rgba(0,0,0,0.22)' }} />
      </div>
      {/* faint glass sheen + window light */}
      <div style={{ position: 'absolute', left: M, top: M, width: PW, height: PH, overflow: 'hidden', pointerEvents: 'none' }}>
        <div style={{ position: 'absolute', top: -200, left: `${glare}%`, width: 120, height: FH + 400, transform: 'rotate(24deg)', background: 'linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,0.09),rgba(255,255,255,0))' }} />
        <div style={{ position: 'absolute', inset: 0, background: `linear-gradient(160deg, rgba(255,250,235,${lightOnFrame}), rgba(255,250,235,0) 60%)` }} />
      </div>
    </div>
  );
};

const Placard = ({ idx, mix }) => (
  <div style={{ position: 'absolute', top: FY + FH + 34, left: 0, width: 1080, height: 60, textAlign: 'center' }}>
    {POSTERS.map(([file, place, region], i) => {
      const o = i === idx ? (mix.prev === -1 ? 1 : Math.max(0, mix.t * 2 - 1)) : i === mix.prev ? Math.max(0, 1 - mix.t * 2) : 0;
      if (o <= 0) return null;
      return (
        <div key={file} style={{ position: 'absolute', width: '100%', opacity: o, fontFamily: 'CG', color: '#4b3d2e' }}>
          <span style={{ fontSize: 30, fontWeight: 600, letterSpacing: '0.2em', textTransform: 'uppercase' }}>{place}</span>
          <span style={{ fontSize: 30, fontWeight: 500, letterSpacing: '0.08em', fontFamily: 'CGi', fontStyle: 'italic', marginLeft: 14, color: '#7a6650' }}>{region}</span>
        </div>
      );
    })}
  </div>
);

const EndCard = ({ f }) => {
  const ease = Easing.bezier(0.7, 0, 0.25, 1);
  let x;
  if (f < CARD_IN || f > CARD_OUT + CARD_LEN) return null;
  if (f <= CARD_IN + CARD_LEN) x = interpolate(f, [CARD_IN, CARD_IN + CARD_LEN], [1100, -50], { easing: ease });
  else if (f < CARD_OUT) x = -50;
  else x = interpolate(f, [CARD_OUT, CARD_OUT + CARD_LEN], [-50, -1200], { easing: ease, extrapolateRight: 'clamp' });
  const inner = interpolate(f, [CARD_IN + 8, CARD_IN + 20], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return (
    <div style={{ position: 'absolute', top: 0, left: x, width: W, height: 1080 }}>
      <svg width={W} height="1080" style={{ position: 'absolute', inset: 0, overflow: 'visible' }}>
        <defs>
          <filter id="paper"><feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="3" seed="2" /><feColorMatrix values="0 0 0 0 0.5  0 0 0 0 0.45  0 0 0 0 0.38  0 0 0 0.12 0" /><feComposite in2="SourceGraphic" operator="in" /></filter>
          <filter id="cshadow"><feGaussianBlur stdDeviation="10" /></filter>
        </defs>
        <path d={cardPath()} fill="rgba(40,25,10,0.35)" filter="url(#cshadow)" transform="translate(-8 0)" />
        <path d={cardPath()} fill="#f7f3ea" />
        <path d={cardPath()} fill="#f7f3ea" filter="url(#paper)" />
        {/* exposed paper fibres along torn edges */}
        <path d={cardPath()} fill="none" stroke="#fffdf8" strokeWidth="5" opacity="0.9" />
      </svg>
      <div style={{ position: 'absolute', left: 50, top: 0, width: 1080, height: 1080, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', opacity: inner }}>
        <Img src={staticFile('logo.png')} style={{ width: 380, height: 380 }} />
        <div style={{ fontFamily: 'CGi', fontStyle: 'italic', fontSize: 50, color: '#2c3a33', marginTop: 34 }}>Vintage travel posters</div>
        <div style={{ fontFamily: 'CG', fontWeight: 600, fontSize: 24, letterSpacing: '0.28em', color: '#6d5c48', marginTop: 16, textTransform: 'uppercase', fontVariantNumeric: 'lining-nums' }}>600+ destinations · several sizes</div>
      </div>
    </div>
  );
};

export const Film = () => {
  const f = useCurrentFrame();
  // poster schedule; the card covers the jump back to poster 0 so the loop is seamless
  let idx, mix;
  if (f >= CARD_IN + CARD_LEN) { idx = 0; mix = { prev: -1, t: 1 }; }
  else {
    idx = Math.min(POSTERS.length - 1, Math.floor(f / SLOT));
    const local = f - idx * SLOT;
    mix = idx > 0 && local < XF ? { prev: idx - 1, t: interpolate(local, [0, XF], [0, 1], { easing: Easing.inOut(Easing.cubic) }) } : { prev: -1, t: 1 };
  }
  const push = 1.025 + 0.02 * loop(f);
  return (
    <AbsoluteFill style={{ overflow: 'hidden', background: '#e8d9c1' }}>
      <style>{FONTS}</style>
      <AbsoluteFill style={{ transform: `scale(${push})`, transformOrigin: '50% 45%' }}>
        <Wall f={f} />
        <WindowLight f={f} />
        <Frame f={f} idx={idx} mix={mix} />
        <LeafShadows f={f} />
        <Placard idx={idx} mix={mix} />
      </AbsoluteFill>
      <EndCard f={f} />
      {/* gentle vignette */}
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(60,40,20,0.22) 100%)', pointerEvents: 'none' }} />
    </AbsoluteFill>
  );
};
