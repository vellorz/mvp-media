const P = new Proxy(function () {}, { get: (_t, k) => (k === Symbol.toPrimitive ? () => 0 : k === "length" ? 0 : P), apply: () => P, construct: () => P, set: () => true });
globalThis.document = { createElement: () => ({ width: 1, height: 1, getContext: () => P, style: {}, addEventListener(){} }), createElementNS: () => ({ style: {}, addEventListener(){} }) };
globalThis.window = globalThis; globalThis.Image = function () { return P; }; globalThis.OffscreenCanvas = function(){ return { getContext: () => P }; };
globalThis.addEventListener=()=>{}; globalThis.removeEventListener=()=>{}; globalThis.dispatchEvent=()=>{};
