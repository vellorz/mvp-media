# @RicksClips3000 — frame-by-frame + audio style study (videos 01–05)

Private reference only. Sources: 01 "This Shape Saved Roller Coasters" (QlDPMzGmYac), 02 "The Pink Prison Cell Experiment" (HxqtHI62otM), 03 "Why Perfect Railroads Don't Work" (7xS87iActkU), 04 "Why Sailors Carried Storm Oil" (Mz72MuPgnGY), 05 "How a Mirror Rigged a Horse Race" (5WMQhPObNqQ).
Method: every frame (~9,800) viewed on labelled contact sheets by 10 agents (one per half-video); full-res zooms in `NN/zoom/`; per-video data in `NN/data.md`; audio separated with Demucs (htdemucs) and measured per stem in `audio/*.audio.md` (+ spectrogram/level PNGs).
OBSERVED = seen/measured. INFERRED = best guess at tool/method.

## 1. Format (OBSERVED, all 5)
1080x1920, 30 fps, 63–65 s, ~240 spoken words. No title card, no logo, no outro/CTA, no end card. Video starts mid-action on frame 0 and ends hard on the payoff frame.

## 2. Story template (OBSERVED, all 5)
1. **0–3 s hook:** a strange action already happening ("He bent the loop out of shape", "He sawed gaps into a railroad", "He poured cooking oil into the sea", "They painted the jail cell pink", "He bet his life savings on the slowest horse").
2. **Stakes + antagonist** (rival, boss, captain, mocking crowd) who thinks the hero is an idiot.
3. **Escalation by repetition**; hero stays calm or smug.
4. **"You see," / "Wait, what?"** pivot ~36–47 s, into a science/history explanation told through an everyday analogy (car on hairpin, blowing on soup, coin/paper in the gap, telegraph wire).
5. **Payoff + comeuppance** in the last 3–5 s (explosion, wave on pirates, money avalanche, rage reveal) on the very last word.
6. **Loop:** last line grammatically runs into the first ("…that perfect circle." → "He bent the roller coaster's loop…"). Visual loop is via same character, not pixel-match.
Key term often never said; picture explains it.

## 3. Picture (OBSERVED unless marked)
- **Worlds:** stylised toon-shaded 3D with ink outlines, bloom, DOF, volumetric light/dust, particles. 01 looks like Planet Coaster 2 (+ BeamNG-like crash insert); 02–05 look like purpose-built Unreal/Unity/Blender sets (INFERRED). One reviewer flagged possible AI image-to-video in 02 (garbled truck lettering, cube debris, morphing limbs) — unresolved; treat as "custom 3D or AI-assisted".
- **Characters:** Cyanide-&-Happiness-style bean people: round white head, thick dark-brown/black outline (~6–8 px at 1080 w), stick limbs, one costume cue per role. They live *inside* the 3D: cast shadows, take scene light/colour, get DOF blur, occluded by foreground objects. Mostly flat 2D cards (they flatten in a top-down view in 02; back-view sprite swap on orbit in 05); 04 reviewers saw 3D-like perspective on hats — either 3D toon models or cards; both read the same.
- **Animation:** puppet/cut-out. Expression swaps every 0.3–0.7 s landing on stressed words (wink, sweat drop, purple face-fill, swirl eyes, smug 3/4 smirk). No narrator lip-sync; mouth flaps only when a character speaks a quoted line (05 teller properly lip-synced).
- **Camera never stops.** Continuous spline moves: push-ins that accelerate, orbits, cranes, fly-throughs, "follow the object" (oil stream → hook; telegraph pulse through 3 locations). Holds >1.5 s are rare and always have animation inside.
- **Transitions:** almost no hard cuts (01: 1, 03: 0 in first half, 04: 0). Default = **crossfade 6–10 frames placed on sentence starts**. Specials: match-dissolve on rhyming shapes (bucket→cell, soup→sea, milk bottle→milk bottle, porthole), push *through* an object (mirror, telescope lens, CRT screen), iris POV, cuts hidden in motion/white flash.
- **Explanation visuals:** no arrows, diagrams, text cards. Instead: glow stroke traced on the relevant 3D part (01), heat-map recolour of rails (03), measuring props (coin, paper, calendar), in-world signage carrying all text (banners, newspaper headline, can labels, odds boards, chalk tally).
- **Gags:** one literal sight gag per metaphor (wallet + moth for "cost him everything", twig snap, tears wiped with a dollar). Background joke signs for re-watchers.
- **Change rate:** a new setup every ~2–4 s; something new (expression/prop/FX/reveal) every 0.5–1 s. Pictures land on the noun being spoken.
- **Colour:** time-of-day / mood grade per act (day → dusk → night storm; pink saturation tracks tension).

## 4. Captions (OBSERVED, all 5 identical)
- Font: white heavy rounded geometric sans (Montserrat ExtraBold/Black or Poppins Bold look), sentence case, punctuation kept, numerals as digits.
- Thin black stroke (~3–4 px) + small soft/hard drop shadow. No highlight colour, no box, no emoji.
- **Small:** cap height ≈2.5–3% of frame (~45–60 px). Centred, baseline ≈70% down (y≈1350). Never moves.
- 1–2 words (max 3); hard swap, no animation; on screen continuously; stay on top during crossfades.
- Timing: 0–6 frames *ahead* of the word. Text comes from the script, not raw ASR (corrected words; final word present where ASR dropped it).

## 5. AUDIO — measured spec (Demucs stems, EBU R128). This is the target.
| measure | 01 | 02 | 03 | 04 | 05 | **target** |
|---|---|---|---|---|---|---|
| Mix integrated | −14.0 | −14.2 | −14.1 | −14.0 | −14.0 | **−14 LUFS** |
| Mix true peak | −2.1 | −1.9 | −2.2 | −2.1 | −2.1 | **−2 dBTP** |
| Mix LRA | 1.7 | 2.2 | 3.2 | 2.4 | 2.6 | **2–3 LU** (very dense) |
| Voice stem | −14.2 | −14.4 | −14.1 | −14.1 | −14.1 | voice ≈ whole mix |
| Bed (music+SFX) | −29.7 | −28.7 | −32.9 | −34.2 | −34.7 | **≈ −30 to −35 LUFS** |
| Voice over bed (median, speaking) | 19.9 | 20.7 | 20.3 | 21.4 | 21.3 | **≈ 20 dB** (p10 ≈ 11–17) |
| Voice/bed level correlation | −0.10 | 0.07 | −0.01 | −0.03 | 0.10 | **no sidechain ducking**; bed just sits low and constant |
| Words/s | 3.77 | 3.70 | 3.35 | 3.86 | 3.85 | **3.4–3.9 w/s (~200–230 wpm)** |
| Longest gap between words | 0.68 | 0.80 | 0.72 | 0.64 | 0.72 | **never > 0.8 s**; speech 100% of runtime |
| Narrator median F0 / range | 197 Hz / 12.7 st | 211 / 14.0 | 208 / 14.3 | 210 / 13.3 | 207 / 14.7 | same voice in all 5; very animated (≈13–15 semitone swing) |
| Voice centroid | 2.79 kHz | 2.83 | 2.87 | 2.85 | 2.73 | bright, present |
| Voice <80 Hz vs 150–300 Hz | −23.6 dB | −17.8 | −22.9 | −22.4 | −20.1 | **high-passed ~80–100 Hz** |
| Voice stereo | mono (corr 1.000) | mono | mono | mono | mono | **dead-centre mono VO** |
| Bed stereo corr | 0.67 | 0.91 | 0.70 | 0.82 | 0.92 | stereo music/SFX |
| Music tempo / key | 118 BPM E min | 157 E min | 118 E min | 81 D min | 152 D maj | light, loopy, plucky/pizzicato-style bed with soft kick/sub pulse |

**Reading of it:**
- The narration *is* the mix: voice alone already hits −14 LUFS; music+SFX add almost nothing to loudness. Bed is ~20 dB under the voice the whole time, never swells, never ducks — it is simply mixed low and left alone.
- Voice is compressed/limited hard into a narrow loudness range (LRA 2–3 LU, 50 ms RMS spread ~14 dB, crest ~14 dB), high-passed, bright (~2.8 kHz centroid), mono, true-peak capped at −2 dBTP.
- Delivery: one consistent, highly expressive storyteller voice (≈205 Hz median, wide pitch swings), wall-to-wall with breaths/pauses trimmed so no gap exceeds ~0.8 s. Quoted character lines are done by the same narrator in a character voice, sometimes slightly quieter (05). INFERRED: either a heavily edited human read or an expressive AI voice (e.g. ElevenLabs-class) — the uniformity across 5 videos fits either.
- SFX: sparse, short and *in the bed bus* — they poke ~8–12 dB above the bed (e.g. 03: hammer 25.5 s, clacks 29–31 s, spikes 52–53 s, boom 61–64 s) but stay well under the voice; no SFX spikes the mix. Whooshes on fast camera moves, impacts on gags, a bigger boom on the payoff.
- Music runs from 0.0 s to the last frame with no intro/outro, no drop-outs.

**Reproduction chain (INFERRED from measurements; ffmpeg terms):**
1. VO: `highpass=f=90, (de-ess), acompressor=threshold=-20dB:ratio=4:attack=5:release=60, alimiter` → normalise VO alone to ≈ −14.5 LUFS short-term-stable. Trim every pause to ≤ 0.6 s. Mono, centred.
2. Music: light looped track, set to ≈ −34 LUFS integrated (≈ 20 dB under VO). No sidechain.
3. SFX: short whoosh/impact/pop on camera moves and gags, peaking ≈ −25 to −28 LUFS momentary (≈ 10 dB over the bed, ≈ 10 dB under VO); one bigger hit on the payoff.
4. Master: `loudnorm=I=-14:TP=-2:LRA=3` (two-pass) on the full mix; AAC 128k+ 44.1 kHz stereo.
5. QC targets: mix −14 ±0.3 LUFS, TP ≤ −2 dBTP, LRA ≤ 3, voice−bed ≈ 20 dB, no word gap > 0.8 s.

## 6. Distinctive ideas worth borrowing
- The camera move *is* the edit — 10–12 s single takes carry whole setups.
- Exposition lives in props/signage; captions stay small and plain.
- Science is shown with a material/colour change on the real object, never a diagram.
- Every metaphor gets a literal sight gag; comedy lands via expression swaps on stressed words.
- Ending: payoff on the last word, no outro, last line feeds the first.

Per-video detail: `NN/data.md`, `NN/zoom/*.jpg`, `03/report_A.md`, `audio/NN_*.audio.md`, `audio/NN_*_spectrogram.png`, `audio/NN_*_levels.png`. Full shot logs from all 10 agents were relayed to the coordinator.
