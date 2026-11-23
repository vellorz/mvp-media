# ==== ROUND 6 (Nov 23 2026): COORDINATED MOTION, Rick's way (owner: face turn, arms, legs and posture are ONE movement) ====
# Pure Python (no bpy): the combo catalogue and a per-frame evaluator. lib.combo() bakes it into Blender keys; m6sheet.py draws the
# same frames in 2D for the owner page, so the preview and the render come from one plan.
# Evidence and agreement rates: research/rick-style-spec/motion-library/ (project files) and motion_combos.json next to this file.
# Opt-in: nothing here runs unless a scene calls lib.combo(); characters need cast.json "turns" and "poses" for the full drawings
# (missing turn variants fall back to the base face, missing pose cards are generated on first use).
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
def _load():
    p = os.path.join(HERE, 'motion_combos.json')
    return json.load(open(p)) if os.path.exists(p) else {'combos': {}}
LIB = _load()
COMBOS = LIB['combos']

def _side(v, d):
    return v * d if isinstance(v, (int, float)) else v

def plan(name, side=1, face='smug', frm=0, face2=None):
    """Events for combo `name` toward screen side `side` (+1 right, -1 left) starting at offset 0.
    Returns a list of (offset, channel, value) with the side applied. Channels:
      'face'  : face key (base name before turn variants)
      'look'  : head level -3..3 (snap to it)
      'turn'  : (frm, to) stepped turn (lib.turn grammar, 353a)
      'arm'   : (sx, pose or 'hang', inb, settle, anticip)       sx is the SCREEN side of the arm (-1 left, +1 right)
      'lean'  : degrees toward `side` (positive = top of the body moves toward `side`), applied as drawn steps
      'squash': scale delta (+ = squash down and wider, - = stretch up), about the feet
      'hdy'   : head drop in metres (nod / flinch), 'htilt': head tilt in degrees toward `side`
      'legs'  : 'body' | 'bodyw1' | 'bodyw2' (stride drawings used as a step or weight shift) | 'hop' (root lift in metres)
    """
    C = COMBOS[name]; out = []
    lv0 = frm
    for ev in C['events']:
        o, ch, v = ev['at'], ev['ch'], ev.get('v')
        if ch == 'face':
            k = v.replace('$face', face).replace('$face2', face2 or face)
            out.append((o, 'face', k))
        elif ch == 'look':
            out.append((o, 'look', 0 if v == 0 else (v * side if v != 'from' else lv0)))
        elif ch == 'turn':
            a, b = v
            a = lv0 if a == 'from' else a * side
            b = lv0 if b == 'from' else b * side
            out.append((o, 'turn', (a, b)))
        elif ch == 'arm':
            which, pose = v[0], v[1]; opts = v[2] if len(v) > 2 else {}
            sx = side if which == 'near' else (-side if which == 'far' else (1 if which == 'right' else -1))
            out.append((o, 'arm', (sx, pose, opts.get('inb', True), opts.get('settle', 0), opts.get('anticip', 0))))
        elif ch in ('lean', 'htilt'):
            out.append((o, ch, [v[0] * side, v[1]] if isinstance(v, (list, tuple)) else v * side))
        else:
            out.append((o, ch, v))
    return sorted(out, key=lambda e: e[0])

def turn_plan(frm, to, holds=None):   # same grammar as lib.turn_plan (353a)
    if frm == to: return []
    if abs(to - frm) == 1: return [(0, to)]
    if frm * to < 0: return [(0, 0), (2 if abs(frm) + abs(to) >= 4 else 1, to)]
    step = 1 if to > frm else -1; lv = list(range(frm + step, to + step, step)); out = []; o = 0
    for i, l in enumerate(lv):
        out.append((o, l)); o += (holds[i] if holds and i < len(holds) else (2 if i == len(lv) - 2 else 1))
    return out

def frames(name, side=1, face='smug', frm=0, face2=None, pre=3, post=8):
    """Per-frame state, frame 0 = combo start. Used by the 2D sheet and by the probe (rule 357 'nothing frozen')."""
    P = plan(name, side, face, frm, face2)
    end = max(o for o, _, _ in P) + post
    st = dict(face=face, lv=frm, arms={-1: 'hang', 1: 'hang'}, lean=0.0, squash=0.0, hdy=0.0, htilt=0.0, legs='body', hop=0.0)
    keyed = {}   # frame -> list of (channel, value) after expanding turns/arm sequences/ramps
    def put(f, k, v): keyed.setdefault(f, []).append((k, v))
    for o, ch, v in P:
        if ch == 'turn':
            for oo, l in turn_plan(*v): put(o + oo, 'lv', l)
        elif ch == 'look': put(o, 'lv', v)
        elif ch == 'arm':
            sx, pose, inb, settle, anticip = v; g = o
            if pose == 'hang':
                if inb: put(g, 'arm', (sx, '_m_back')); g += 1
                put(g, 'arm', (sx, 'hang'))
            else:
                if anticip: put(g, 'arm', (sx, 'dip')); g += anticip
                if inb: put(g, 'arm', (sx, pose + '_m')); g += 1
                if settle: put(g, 'arm', (sx, pose + '_o')); g += settle
                put(g, 'arm', (sx, pose))
        elif ch in ('lean', 'squash', 'hdy', 'htilt', 'hop'):
            # v may be a number (snap) or [target, frames] (drawn steps, one per frame, Rick redraws each frame)
            tgt, n = (v, 1) if not isinstance(v, (list, tuple)) else (v[0], max(1, int(v[1])))
            put(o, ch + '_ramp', (tgt, n))
        else:
            put(o, ch, v)
    seq = []; ramps = {}
    prev_arm = {-1: 'hang', 1: 'hang'}
    for f in range(-pre, end + 1):
        for k, v in keyed.get(f, []):
            if k == 'lv': st['lv'] = v
            elif k == 'face': st['face'] = v
            elif k == 'arm':
                sx, card = v
                if card == '_m_back': card = (st['arms'][sx] + '_m') if st['arms'][sx] not in ('hang',) else 'hang'
                st['arms'] = dict(st['arms']); st['arms'][sx] = card
            elif k == 'legs': st['legs'] = v
            elif k.endswith('_ramp'):
                c = k[:-5]; ramps[c] = (f, st[c], v[0], v[1])
        for c, (f0, a, b, n) in list(ramps.items()):
            t = min(1.0, (f - f0 + 1) / n); st[c] = a + (b - a) * t
            if t >= 1.0: del ramps[c]
        seq.append(dict(f=f, face=st['face'], lv=st['lv'], arms=dict(st['arms']), lean=round(st['lean'], 2), squash=round(st['squash'], 3),
                        hdy=round(st['hdy'], 4), htilt=round(st['htilt'], 2), legs=st['legs'], hop=round(st['hop'], 4)))
    return seq

def moving_parts(seq):
    """For the 'nothing frozen' probe: per frame, which parts changed versus the frame before (head, arms, torso, legs)."""
    out = []
    for a, b in zip(seq, seq[1:]):
        m = set()
        if a['lv'] != b['lv'] or a['face'] != b['face'] or a['hdy'] != b['hdy'] or a['htilt'] != b['htilt']: m.add('head')
        if a['arms'] != b['arms']: m.add('arms')
        if a['lean'] != b['lean'] or a['squash'] != b['squash']: m.add('torso')
        if a['legs'] != b['legs'] or a['hop'] != b['hop']: m.add('legs')
        out.append((b['f'], m))
    return out
