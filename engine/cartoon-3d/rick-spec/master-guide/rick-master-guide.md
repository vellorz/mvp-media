# Rick Master Guide — the spec every Modern Vista cartoon short is built from
Version 1.0, 2026-11-17. Private (contains reference measurements; never publish reference frames). Built from evidence, not from our old checklists; where they conflict, this guide wins.
Evidence keys: `#10` = "What the Grave Bell Really Meant" (bell, 1,785 f), `#14` = "The Ancient Jar That Warned an Empire" (dragon, 1,945 f), `fNNN` = frame number at 30 fps (t = (f−1)/30 s). Full frame logs: frame-logs/. Test results: phase4/04_rubric-and-test.md. [derived] = follows from Rick evidence but Rick has no direct example (our poster). [unverified] = no evidence; not counted toward the 95 % bar.

---
## a. Quick card — the 20 rules that matter most
| # | rule | number | evidence |
|---|---|---|---|
| 1 | Open on the strange act, spoken from frame 1 | first word at t ≤ 0.2 s; hook sentence 9-21 words, oddity stated in sentence 1 | 20/20 transcripts; #14 f1-92 |
| 2 | Narration speed | **3.4-4.1 words/s** (target 3.75); ≤ 3 gaps > 0.8 s; none > 1.2 s | 20/20; ours 2.5-2.7 |
| 3 | Story beats | hook → "You see," world rule (3-8 s) → doubter mocks (quoted line) → 2-3 escalations with time markers → turn → reveal at **50-85 %** → payoff on the last word | 19/20 reveal window |
| 4 | Joins | dissolve **4-14 f (default 6-12 f)**, or a fast join ≤ 3 f; ≤ 5 fast joins per video | 241/248 unseen, 35/35 primaries |
| 5 | Join count | **2-4.5 joins per 10 s** (primaries 3.0); shots 1.5-8.5 s | 19/19 |
| 6 | Bridge object | ≥ 50 % of dissolves put a matching shape (round→round, window→window, head→bell) at the same screen spot | #10 14/17, #14 10/18 |
| 7 | Camera never stops | no static hold > 1.5 s; motion median ≥ **4.5** (ours 2.5-3.3) | 19/19 |
| 8 | Camera hits | eased moves arrive on the spoken noun (±3 f); crash push 9 f on the punch word | #14 f1419-1427 "pile"; #10 f1041 "bell" |
| 9 | Characters | flat 2D drawn round head + bean/stick body, monoline dark outline **6-10 px @1080** in MS (2.5 % of head width), one costume cue | 101/101 sampled frames |
| 10 | Head size | **30-39 % frame width in MS**, 45-85 % in CU, 8-23 % in wides | #10, #14 logs |
| 11 | Faces act | a face change every **0.3-2 s** (0.5-3.4 swaps/s), 5-14 expressions per 12 s, blinks 1-3 f; lips move only on quoted lines | 10/10 logs |
| 12 | Captions | heavy rounded sans, white #FFFFFF, black outline 4-6 px, shadow +3 px; cap **54 px @1920** (2.8 % H); box bottom **71.7 % H**; centred; **1-3 words**; hard swap **0-3 f before** the word | 19/19 videos |
| 13 | Tracking/leading | tracking **0 %** (default sidebearings), kerning default, single line (leading n/a), word space ≈ 26 px | all logs |
| 14 | Grade | mean luma 0.33-0.56, sat 0.37-0.66, blacks lifted **p2 ≥ 0.05**, whites **p98 ≥ 0.84** | 19/19 (Salzburg p2 0.004, p98 0.67) |
| 15 | Palette per beat | each time/mood change flips the palette across a join (cool ext ↔ warm int; night blue-violet → dawn peach in 7-18 f) | #10 f394-722, #14 f1380-1386 |
| 16 | Set density | dense, textured, lit sets with props, signage and joke details; facts shown as in-world props/documents, never overlays/arrows | #14 dragon addendum; 19/19 grids |
| 17 | Mix | **−14 LUFS**, TP −2 dBTP, LRA ≤ 3.2; music bed ≈ **20 dB under** the VO, constant, no ducking | 19/19 loudness; 5/5 stems |
| 18 | Music | light loopy plucked/pizzicato bed + soft pulse, 81-157 BPM, frame 0 to last frame, no intro/outro | 5/5 stems |
| 19 | Ending | payoff image on the last word; video ends **≤ 1.2 s** after the last word starts; no end card, logo, CTA | 19/19 |
| 20 | Poster | [derived] the poster lives inside the payoff shot as an in-world object, whole poster visible, no "X, on your wall" line | owner rules + rule 19 |

---
## b. Shot and transition grammar
**Takes, not cuts.** Rick builds 18-22 takes per minute. A take is one continuous camera move that may contain 2-5 beats (drift → push → crane → settle). The camera move is the edit: #14 f1-92 (snap push 10 f, crane-over-the-lid reveal 22 f, hold 12 f) and #10 f1586-1785 (200 f one-take with 5 eased moves).

| type | share | length (frames) | curve | when Rick uses it | evidence |
|---|---|---|---|---|---|
| Cross-dissolve during motion | ~85 % of joins | 4-14 (median 9; #10 median 11, #14 median 7) | linear core with soft shoulders: incoming weight .08 .17 .32 .47 .61 .75 .85 .92 .96 | default for every scene change; both shots moving; placed on a phrase onset | #14 f404-412; 248 joins on 17 videos |
| Shape/position-matched dissolve | ~50 % of dissolves | same | same; the bridge object sits at the same x,y ±5 % | new scene shares a round/rectangular hero object | head→bell #10 f1578-1585; window→window #10 f869-881; frog mouth→wine bowl #14 f609-617; coin→head #16 f998; face→clock #12 f284 |
| Time/mood dissolve | at each day/night change | 6-12, grade ramp 7-18 | — | "next morning", "until sunrise" | #14 f1380-1386; #10 f1558-1576 (in-shot ramp 18 f) |
| Iris / lens POV mask | 0-3 round trips, only in POV stories | in/out 3-5 | — | a character looks through a telescope/peephole | #05 f553-615; #13 f660-706 |
| Push-through | 0-2 | 2 f micro-mix after a 20-30 f ease-in push | ease-in into the glass | entering a building/window/lens | #10 f1176-1183; #05 f395 |
| Foreground wipe | 0-3 | 2-4 f of FG object filling frame | camera truck | busy, comic montage | #16 f111, f162, f191 |
| Hard cut | 0-2 | 0 | — | comic snap, bookend, same-setup jump | #14 f92/93; #10 f368/369; #16 f893, f942 |
| In-shot move transition | 2-4 per video | 10-35 | ease-in-out | going inside/under/over to a new space without a join | #14 f59-80, f1496-1530, f1857-1866 |
**Never**: whip pans as a default, full-frame slide wipes, zoom-blur, flash-to-white, glitch, page curls, star/shape wipes (not seen in 19 videos).
**Bridging a scene change**: (1) start the outgoing camera move 10-30 f before the join (ease-in); (2) put the next scene's hero object where the old one is; (3) place the join on a phrase onset ("He", "So", "Then", "The next morning"); (4) keep the caption on top at full opacity; (5) incoming camera already moving (ease-out).

---
## c. Character build sheet
- **Construction**: flat, drawn (2D) round or bean head, white/cream fill (#FFFFFF, emperor #FDE1CC #14 f385-768); stick or tube limbs; simple bean body with one flat costume colour block and one costume cue (crown, nightcap, helmet, chef hat). Characters stand inside 3D/2.5D lit sets: they take scene tint, cast contact shadows and get DOF blur (STYLE_STUDY §3; #10 f1081-1440). Our own designs are allowed (owner Nov 16) as long as they follow this construction; no shaded 3D figurine heads (Dresden/Salzburg gap).
- **Proportions**: head:body 1:2 in close/medium, 1:3 in wides (#14 f806-889). Head width: CU 45-85 % W, MS 30-39 % W, wide 8-23 % W (#10 f361-720, f1441-1785; #14 f1-384).
- **Outline**: monoline, no taper, dark warm brown/black (#573423 on the emperor, #121635 on night scenes); 6-10 px @1080 in MS (≈ 2-2.5 % of head width), 14-22 px in CU, 3-4 px in wides. Set lines thinner: 2-4 px. 3D props may have no outline or a 6 px toon outline (#14 f1561-1945).
- **Face**: dot or oval eyes, simple brows, small mouth. Expression set seen (≥ 14 per video): neutral half-lid, smug smirk, wide O-eyes, swirl/startle, laugh ^^ with open grin, cry-laugh tears, sweat drop, angry purple face-fill, asleep "= =", snore "o", gritted teeth, one-eye-open, dazed, deadpan.
- **Face-swap cadence**: hard swaps, no in-betweens: 0.5-3.4 swaps/s on screen; bursts of 12 swaps in 14 f for shock (#14 f571-584); typical 8-15 f per face. Blinks 1-3 f, rare (≈ 1 per 4-6 s).
- **Lip-sync**: only when the narrator quotes a character; mouth shapes every 2-4 f (4-6 visemes: closed, small o, open, wide, teeth, smile) (#10 f562-667 "You go check"; #14 f721-805). The narrator is never lip-synced.
- **Pose language**: pose-to-pose with 1-4 f snaps, anticipation 3 f → travel 8 f → settle 1 f; reaction cascades staggered 2-7 f between characters (#14 f179-196); no squash/stretch/smear on characters.
- **Prop scale**: hero props oversized (bronze ball, bell, shovel ~ head size); props held in hand; documents readable in close-up.

---
## d. Typography and lettering spec
| property | value | evidence |
|---|---|---|
| Typeface | heavy geometric/rounded sans, Montserrat Black/ExtraBold or Arial Black class (agents disagree on exact face; all agree on class) | 10/10 logs |
| Classification / weight / width | sans, 800-900, normal width, roman (no italic) | logs |
| Case | sentence case as spoken, punctuation kept, numerals as digits ("2:00", "39 ft", "15") | transcripts vs captions |
| Size | cap height 53-55 px @1920 (2.8 % H) → **72 px @2560**; x-height 38-41 px; font ≈ 74-77 px | 19/19 auto (box 53-63 px) |
| Hierarchy | one level only; no emphasis colour/size | logs |
| Tracking | ≈ 0 % (default sidebearings; one measure +3 %); does not animate | logs |
| Kerning | default (no manual pairs seen) | logs |
| Leading | n/a — always one line | logs |
| Word spacing | 23-30 px @1080 (≈ 0.33 em) | logs |
| Baseline | y = 1376 px @1920 = **71.7 % H**; no baseline shift | 19/19 |
| Alignment / line length | centred at x 50 %; 1-3 words; median width 24-49 % W, widest ~62 % W | 19/19 |
| Rag / orphans / widows / ligatures / glyph variants | n/a single line / none / none / none | logs |
| Fill / gradient / glow | #FFFFFF / none / none | logs |
| Stroke | 4-6 px #000000 outside stroke @1080 | logs |
| Drop shadow | offset +2…+3 px x, +3…+4 px y, blur 0-6 px, black ~60 % | logs (C8) |
| Bevel, extrusion, text-on-path, warp, mask | none | logs |
| Reveal | hard swap on one frame; no pop/slide/scale/typewriter | 10/10 logs |
| Timing | on 0-3 f before the word (range −3…+4 f), hold 3-21 f (mean 9.4-12.4 f), 2.7 captions/s, no gaps between captions | logs |
| Layering | above every dissolve, never fades, can span a join | #14 f405-723 |
| Safe area | centred, 71.7 % baseline: lower-third band kept clear of faces | 136/136 sampled |
| In-world text | separate system: signs, epitaphs ("S. HOLT 1849-1894"), certificates, boards, labels in serif or hand-lettered styles matching the period; carries the facts | #10 f77+, f1208-1244 |
| Reading time | ≈ 0.3 s per word, set by the VO, not by reading | logs |

---
## e. Look spec
- **Palette** (sampled hex): day exterior #d2bda3 stone, #c19d61 road, #fbead1 light, sky #2f7eb7; warm interior #24153a/#452048 violet + #eab48b lantern; night #071660 sky, #5070F9 snow, #4E5FAF/#322846; golden hour #F6C28D/#FCE2B5, bell gold #C3912D; diagram #114267/#DF6524/#EDA42C (#10, #14 logs). Split ~55 % dominant / 25 % secondary / 5-10 % accent (#14 f806-889).
- **Harmony**: complementary blue-violet vs orange in night stories, analogous warm in day/court; one warm emitter in night shots.
- **Grade**: luma 0.33-0.56, sat 0.37-0.66, lifted blacks p2 0.05-0.19, bright highlights p98 0.85-0.98, soft highlight roll-off, no crushed blacks. Temperature follows the beat: warm hook, cool warning, saturated payoff (#14 f1-384, f1561-1945).
- **Lighting**: motivated key (sun, moon, candle, lantern), soft shadows, contact shadows and AO under every character/prop, bloom on emitters, rim light on backlit metal, god rays/volumetrics in interiors; vignette in interiors (corners 33-42 % of centre luma), none in daylight.
- **Depth**: FG/MG/BG layers in every shot; FG elements blurred 8-12 px @540; rack focus to the clue (#10 f897-940); aerial haze in far shots; parallax FG ≈ 2× BG.
- **Composition**: one focal subject; symmetric centre-axis framing for authority (throne, gate); thirds for action; leading lines (carpet, road, rails, string); look-room toward the next beat; lower 30 % calm for the caption.
- **Set density**: 20-30 props in a wide set, joke details for rewatchers (epitaphs, signs), no repeating tiles; sets are 3D boxes with painted/drawn textures, hero props true 3D (#14 addendum; DETAIL_STANDARD).
- **Edge density** 0.21-0.34 (ours Salzburg 0.197).
- **Texture**: smooth render, painted surfaces, hatching/stipple only on illustrated inserts; no film grain.
- **Camera**: eye-level or slightly high, 24-35 mm feel; macro/tele for prop close-ups; moves: push-in (most common), pull-out reveal (up to 10× in 32 f), crane up/down, orbit, truck, dive top-down; no handheld, no roll except a slight roll on dives; no zoom (dolly only); speed ramps into joins.
- **Motion tracking**: none for graphics — captions are screen-locked; the camera follows objects (oil stream, pulse, falling ball) instead.

---
## f. Audio spec
- **Narrator (our Drew, eleven_v4)**: one energetic storyteller voice for every line; 3.4-4.1 words/s (target 3.75); trim breaths so ≤ 3 gaps exceed 0.8 s and none exceeds 1.2 s; pitch swing ≥ 12 semitones; quoted character lines read by the same narrator in a character voice, slightly quieter. Tags: open `[energetic, playful storytelling]`; `[amused]` on the doubter's line; `[brisk]` on escalations; `[curious, building excitement]` before the reveal; `[impressed]` on the payoff. Never `[warm, intrigued]`, `[cozy]`, `[soft]` (Salzburg failure).
- **Per line type**: hook = fast and declarative, stress on the strange object; "You see," = conversational; doubter quote = mocking character voice; escalation = quicker, rising; turn ("Wait, what?") = a beat of surprise; reveal = clear and slower by ~10 %; payoff = punchy, last word stressed.
- **Mix**: VO high-passed ~90 Hz, mono centre, compressed; whole mix −14 LUFS integrated, −2 dBTP, LRA 1.7-3.2.
- **Music**: light, loopy, plucked/pizzicato/mallet bed with a soft kick/sub pulse; 81-157 BPM; minor keys common; starts frame 0, runs to the last frame, constant level ≈ 20 dB under the VO (bed −30…−35 LUFS), no sidechain ducking, no swells (owner rule "no pumping" agrees). Owner taste and cleared-music rule still apply.
- **SFX**: sparse, in the bed bus, 8-12 dB above the bed and well under the VO: whoosh on fast camera moves, thud/clank on impacts, a bigger hit on the payoff; no silence moments.

---
## g. Script and narration playbook
**Fill-in template (≈ 225 words, 58-64 s at 3.75 w/s)**
1. HOOK (0-3 s, 9-21 words): "[He/They] [did a strange concrete thing] [to/with odd object] [and said/told doubter X]."
2. WORLD RULE (3-8 s): "You see, [how this world/time worked, one image]."
3. DOUBTER (8-15 s): "[Rival/boss/crowd] [laughs/mocks]: "[short funny quoted line]"."
4. ESCALATION ×2-3 (15-35 s): "[Time marker], [it gets worse / he doubles down]." Each with a concrete number or object.
5. TURN (35-45 s): "Then, one [night/morning]…" / "Wait, what?"
6. REVEAL (50-85 % of runtime): "You see, [mechanism] — like [everyday analogy]."
7. PAYOFF (last sentence): the consequence lands on the LAST word. For us [derived]: the payoff happens in the poster's place, and the camera's final move lands on the poster inside that scene. No "on your wall", no CTA.
Style: roles not names ("a young priest", "the king"); 1-4 concrete numbers, never a list of statistics; dates only inside the story; casual spoken English; one joke line every 10-15 s; mix 2-5-word punches with long run-ons (mean 15 words/sentence).

**Example 1 — #14 dragon (top views, 32.7 M)**
| t (s) | line | beat |
|---|---|---|
| 0.0 | He put a bronze ball in a dragon's mouth and told the emperor if this ever falls out, run. | hook: strange act + warning |
| 5.2 | The whole court burst out laughing. | doubter |
| 7.2 | You see, there were eight dragons coiled around a giant bronze jar, each holding a ball over a frog's open mouth. | world rule (object shown) |
| 13.4 | But the emperor had the biggest army in the world and he wasn't about to run from a jar. | stakes |
| 17.6-22.2 | Weeks later, a ball fell, but nothing happened. Not even a ripple… Now they laughed even harder. | escalation 1 + punch lines |
| 24.1-29.5 | The emperor called it the world's most expensive toy and threw the inventor out… So, he dragged it up a hill… | escalation 2 (exile) |
| 32.8-37.0 | Then, one night, a ball dropped. Then another. Then all eight at once. He ran to the city gates… | turn, 2-word punches |
| 40.4 | "Hey, it's the toy guy. Did your frogs get hungry again?" | quoted mockery |
| 45.8 | The next morning, the palace was a pile of rubble. | consequence (crash push on "pile", f1423) |
| 48.5-58.2 | Inside the jar hung a heavy pendulum… | reveal at 75 % |
| 60.3 | All eight meant the biggest earthquake the empire had ever seen was right underneath them. | payoff on last word; ends 0.34 s later |

**Example 2 — #10 bell (12.2 M)**
| t | line | beat |
|---|---|---|
| 0.0 | They buried a man alive with a bell tied to his finger. | hook |
| 3.1 | You see, people were so scared of waking up in a coffin that graves came with a little bell… | world rule |
| 10.0 | Except when his bell starts ringing at 2:00 in the morning, the guy next door decides it's probably the wind. | complication + palette flip to night |
| 15.2-25.7 | "You go check. No, you go check." … "Bodies twitch. He's dead. I signed the paper myself." | doubters (two quoted lines) |
| 27.0-32.6 | But his wife isn't on her porch… Three short, one long, the exact signal they practiced. | turn |
| 35.8 | Wait, practiced? Well, he was never dead. | reveal at 59 % |
| 38.4-45.9 | He owed money… Instead, she just sits there all night… | twist |
| 53.9 | You see, with him in the ground, every debt got buried right along with him, and the house was all hers. | payoff on "hers" (smirk f1771) |

**Example 3 — #03 railroad (26.9 M)**
| t | line | beat |
|---|---|---|
| 0.1 | He saw gaps into a railroad every 39 ft. | hook with one concrete number |
| 3.4-8.6 | You see, two companies are racing… whoever finishes first gets the whole country's business. | world rule + stakes |
| 11.7-18.2 | …his face goes purple. "You're wrecking my railroad." | doubter |
| 21.7-31.2 | The other company… finishes first… everyone switches to the quiet trains. | escalation (he loses) |
| 36.1-45.8 | Then summer comes… In May… By July… "See, even your gaps know you were wrong." | turn + time markers + mockery |
| 47.9-54.4 | Meanwhile… the rails have started groaning… his gaps finally close. | reveal through the picture (heat) |
| 59.4 | …the perfect railroad kicks sideways like a snake, right as a train rolls onto | payoff, cut mid-sentence → loops to "He saw gaps" |

---
## h. Index of reference videos studied (19 videos + 1 transcript-only = 20)
| # | title | role in this guide | what it teaches |
|---|---|---|---|
| 01 | This Shape Saved Roller Coasters | script + loudness/stem study + test set | science reveal through a rival story; glow stroke on the real part |
| 02 | The Pink Prison Cell Experiment | script + stems + test | escalation by timed steps (15 → 20 min) |
| 03 | Why Perfect Railroads Don't Work | script example 3 + stems + test | mid-sentence loop ending; heat-map recolour |
| 04 | Why Sailors Carried Storm Oil | script + stems + test | soup analogy; storm grade |
| 05 | How a Mirror Rigged a Horse Race | **Phase 2 transitions** + stems + test | iris/telescope POV joins |
| 06 | The Town Built Around a Button | script + test | mystery loop twist |
| 07 | Why the Second Draw Always Wins | script + test | "imagine you" hook |
| 08 | Every Memory Has a Price | script + test | what fails: 78 s sad fiction, lowest story views |
| 09 | He Could Spot Winning Tickets Just by Looking | script + test | "look at" hook |
| 10 | What the Grave Bell Really Meant | **PRIMARY, every frame** | long dissolves for an eerie night story, colour flip per beat, smirk ending |
| 11 | Why Cashiers Keep Winning The Lottery | script + test | sting twist |
| 12 | The Job Nobody Wants in Japan | **Phase 2 transitions** + test | shape-matched round-object dissolves |
| 13 | The Burglar Who Only Moved Furniture | **Phase 2 transitions** + test | peephole POV, repeated top-down setup to show change |
| 14 | The Ancient Jar That Warned an Empire | **PRIMARY, every frame** | short dissolves for a busy story, mechanism taught close then wide, crash push on the key word |
| 15 | Levels of Pirate Cannonballs | script + test | list format (lower fit) |
| 16 | This Knight Found the Ultimate Loophole | **Phase 2 transitions** + test | FG wipes, punchline hard cuts |
| 17 | An Unstoppable Spear vs an Unbreakable Shield | script + test | 45 s paradox story |
| 18 | How Painkillers Actually Work | script + test | weak format: question hook, early reveal |
| 19 | The Window That Breaks Japan's Gambling Law | script + test | paradox + "you" walk-through |
| 20 | The Science Behind Slot Machines | script only (no video file) | weakest format: pure explainer |

---
## i. Design-vocabulary coverage table (every term × every video studied)
Columns: **#10** and **#14** = every-frame logs; **P2** = #05, #12, #13, #16 (transition strips + grids + metrics); **Rest** = #01-04, 06-09, 11, 15, 17-19 (metrics on every frame, captions on every 10th frame, 8-frame grids, transcripts). A value in Rest/P2 marked "=" means checked and the same as the primaries.
| group | term | #10 | #14 | P2 (05,12,13,16) | Rest (13 videos) |
|---|---|---|---|---|---|
| T | typeface/family | heavy sans (Verdana/Arial Black-like) | Montserrat Black-class | = (visual) | = (visual) |
| T | classification | sans | sans | = | = |
| T | weight | 800-900 | 800-900 | = | = |
| T | width | normal | normal | = | = |
| T | italic/oblique | none | none | = | = |
| T | case | sentence | sentence | = | = |
| T | size + hierarchy | cap 53-55 px, 1 level | cap 54 px, 1 level | box 54-55 px | box 53-63 px |
| T | tracking | ≈0 % | ≈0 % (+3 % one measure) | = | = |
| T | kerning | default | default | = | = |
| T | leading | n/a 1 line | n/a | = | = |
| T | word spacing | 23-30 px | ≈26 px | = | = |
| T | baseline/shift | 71.7 % H / none | 71.7 % / none | 71.7 (12: 72.1) | 71.7 % |
| T | alignment | centre | centre | 49.9-50 % | 49.9-50 % |
| T | line length/breaks | 1-3 words, 1 line | 1-3 words | width 26-44 % W | 24-49 % W |
| T | rag | n/a | n/a | n/a | n/a |
| T | orphans/widows | none | none | none | none |
| T | ligatures | none | none | none | none |
| T | glyph variants | none | none | none | none |
| T | stroke | 4-6 px #000 | 4-6 px #000 | = | = |
| T | fill | #FFFFFF | #FFFFFF | = | = |
| T | gradient fill | none | none | none | none |
| T | inner/outer glow | none | none | none | none |
| T | drop shadow | +3,+3/4 px, blur 0-4 | +2..3,+4, blur 0-8 | = | = |
| T | bevel/emboss | none | none | none | none |
| T | extrusion/3D text | none (in-world signs are 3D props) | none | none | none |
| T | text on path | none | none | none | none |
| T | distortion/warp | none | none | none | none |
| T | mask/knockout | none | none | none | none |
| T | word emphasis | none (VO carries it) | none | none | none |
| LM | reveal style | hard swap | hard swap | hard swap | hard swap |
| LM | entrance/exit | 1 f / 1 f | 1 f / 1 f | = | = |
| LM | easing | none | none | none | none |
| LM | overshoot | none | none | none | none |
| LM | stagger | none | none | none | none |
| LM | hold | 3-21 f, mean 9.4-11.3 | 3-18 f, mean 10.2-12.4 | ≈ similar (strips) | caption on 79-100 % of frames |
| LM | VO sync | −3…+3 f, mean ≈0 | −2.6…+4 f, mean ≈+0.3 | [primaries only] | [primaries only] |
| LM | safe-area placement | x 50 %, y 71.7 % | same | same | same |
| LM | reading time/word | ≈0.27-0.37 s | ≈0.3 s | 3.6-4.1 w/s | 3.4-4.1 w/s |
| C | palette hex | #071660 #5070F9 #C3912D #24153a #eab48b #F8E9CF | #d2bda3 #c19d61 #4E5FAF #F6C28D #b2272a #FDE1CC | grids: office greens/blues (#12), pinks/blue night (#13), medieval primaries (#16), racetrack ochre (#05) | per-video in grids |
| C | dominant/secondary/accent | ≈60/30/10 (blue/violet/gold) | ≈55/25/5-10 | [estimated from grids] ≈60/30/10 | same |
| C | hue | blue-violet + orange | warm beige/red + navy | varies per story | varies |
| C | saturation | 0.524 | 0.416 | 0.442-0.457 | 0.376-0.653 |
| C | value | luma 0.417 | 0.439 | 0.455-0.548 | 0.338-0.528 |
| C | contrast ratio | p98/p2 ≈ 8.8:1; caption 21:1 | ≈ 7.2:1; caption 21:1 | 5.3-9:1 | 4.8-17.8:1 |
| C | temperature | cool night, warm interiors | warm day/court, cool night | mixed | lab_b −14.6…+15.5 |
| C | harmony | complementary | analogous + complementary | complementary mostly | = |
| C | grade/LUT feel | clean toon, lifted blacks | warm pastel day, lifted blacks | = | = |
| C | black level | p2 0.098 | 0.125 | 0.094-0.180 | 0.051-0.192 |
| C | highlight rolloff | soft, p98 0.863 | soft, 0.902 | 0.847-0.945 | 0.871-0.980 |
| C | tint | blue-violet nights | warm gold day | = | = |
| C | vibrance | moderate | moderate | moderate | moderate |
| C | per-scene shift | every join (cool↔warm) | every time change | yes (strips) | yes (grids) |
| C | gradients | sky purple→pink | sky + sun bloom | skies | skies |
| S | shape language | round (heads, bell, arches) | round + ornate | round | round |
| S | line weight/consistency | 6-10 px MS, consistent | 8-16 px MS, consistent | = | = |
| S | outline colour | #121635 / dark brown | #573423 / #5B2E1C | dark | dark |
| S | outline variation | scales with shot | scales | = | = |
| S | stroke taper | none | none | none | none |
| S | corner radius | soft/rounded | rounded | rounded | rounded |
| S | silhouette | clear | clear, small in wides | clear | clear |
| S | negative space | lower 35 % calm | floor/sky areas | = | = |
| S | texture | painted, low-poly snow, stipple strata | painted stone, hatched mountain | painted | painted; no grain |
| CL | frame/aspect | 1080×1920 9:16 | same | same | same |
| CL | grid | thirds + centre axis | centre axis + thirds | = | = |
| CL | margins/safe areas | caption band clear | clear | = | = |
| CL | rule of thirds | yes | yes | yes | yes |
| CL | golden ratio | not used deliberately | not used | — | — |
| CL | focal point | one per shot | one | one | one |
| CL | hierarchy | face > prop > set | same | = | = |
| CL | balance | asymmetric scenes, symmetric authority | symmetric throne/gate | mixed | mixed |
| CL | alignment | subject on thirds/centre | same | = | = |
| CL | proximity | groups clustered | clustered court | = | = |
| CL | repetition | tally marks, lanterns | 8 dragons/8 frogs | repeated top-down bed (#13) | = |
| CL | rhythm | beat every 0.5-1 s | same | = | = |
| CL | white space | low (dense sets) | low | low | low |
| CL | scale/proportion | oversized hero props | oversized jar | = | = |
| CL | depth layering | FG/MG/BG always | always | always | always |
| CL | overlap | yes | yes | yes | yes |
| CL | framing | window/door frames | arches, portcullis | telescope ring, peephole | = |
| CL | leading lines | bell string, street | carpet, road, crack | rails/aisles | rails, roads |
| CL | cropping | tight CU crops faces at chin | same | same | same |
| CL | bleed | sets bleed off all edges | same | same | same |
| CL | head-room/look-room | small head-room, look-room toward action | same | = | = |
| DL | key/fill/rim | moon/candle key, cool fill, warm rim | sun key, warm rim on metal | motivated | motivated |
| DL | falloff | candle falloff in interiors | lamp falloff | = | = |
| DL | shadow shape/softness | soft | soft | soft | soft |
| DL | contact shadows | yes | yes | yes | yes |
| DL | AO | light | yes at bases | = | = |
| DL | highlights/specular | bell gold specular | gold/wine specular | = | = |
| DL | bloom/glow | candles, windows | sun, lamps, lens dots | yes | yes |
| DL | vignette | interiors | interiors 33-42 % | interiors | interiors |
| DL | DOF/focal plane | rack focus f897-940 | FG blur 8-12 px @540 | yes | yes |
| DL | blur type | gaussian DOF + motion blur on fast moves | same | = | = |
| DL | haze | night snow haze | aerial haze f1760 | = | = |
| DL | parallax | FG ≈2× BG | treadmill parallax f897-951 | = | = |
| DL | film grain | none/faint | none | none | none |
| CM | position/lens | eye-level, 28-35 mm; top-down diagram | eye-level 24-35 mm; macro | = | = |
| CM | push-in/pull-out | yes both | yes both (10× pull) | yes | yes |
| CM | pan/tilt | tilt up string | tilt down ball | = | = |
| CM | truck/dolly/crane | all | all | all | all |
| CM | orbit | final orbit | jar orbit f223-404 | yes | yes |
| CM | handheld | none | none | none | none |
| CM | roll | none | slight on dive | none | none |
| CM | tracking shot | doctor dragged f655-722 | walk-back f1309 | yes | yes |
| CM | motion tracking (graphic) | none | none | none | none |
| CM | speed ramp | ease-in pushes into joins | crash push 9 f | = | = |
| CM | zoom | none (dolly) | none | none | none |
| CM | punch-in | f481-513 | f21-30, f1419-1427 | yes | yes |
| MD | keyframe spacing | pose holds 8-15 f | same | = | = |
| MD | easing | ease-in-out camera | same | = | = |
| MD | anticipation | 3 f | 3 f | = | = |
| MD | follow-through | dust/snow settle | dust lingers | = | = |
| MD | overshoot | none | 1 f glint bounce | none | none |
| MD | squash/stretch | none | none | none | none |
| MD | secondary motion | snow, lantern sway | crows, dust | = | = |
| MD | smear/motion blur | camera only | camera only | camera only | camera only |
| MD | hold | ≤ 1.5 s static | ≤ 1.5 s | still frames 1.1-4.7 % | 0.4-11.1 % |
| MD | loop | none | none | none | #02-04 audio loop |
| MD | stagger | lights on house by house f533-550 | laugh cascade 2-7 f | = | = |
| MD | mask reveal | none | lid as FG wipe f59-80 | iris masks (#05, #13) | none |
| MD | wipe | none | none | FG wipes (#16) | none |
| MD | match cut | shape dissolves | shape dissolves | yes | yes |
| MD | morph | none | none | none | none |
| MD | dissolve | 5-14 f, median 11 | 5-13 f, median 7 | 2-15 f | 0-19 f (97 % ≤ 14) |
| MD | whip | none | 1 whip with hidden cut f158-165 (8 f) | none | none |
| MD | shape-matched transition | 14/17 | ≈10/18 | yes | yes |
| CH | head-to-body | 1:2-1:3 | 1:2-1:3 | = | = |
| CH | face shape | round | round/oval | round | round |
| CH | eye size/spacing | dots/ovals, ~1 eye-width apart | same | = | = |
| CH | brow | single strokes | same | = | = |
| CH | mouth/visemes | 4-6 shapes, quotes only | same | = | = |
| CH | face-swap cadence | 0.5-2.3/s | 2-4.7/s | [visual only] | [visual only] |
| CH | blink timing | 1-2 f | 2-3 f | — | — |
| CH | pose language | pose-to-pose | pose-to-pose | = | = |
| CH | outline weight | 6-10 px MS | 8-16 px MS | = | = |
| CH | costume colour-blocking | 1-2 flat blocks | same | = | = |
| CH | prop scale | oversized bell/shovel | oversized jar/ball | = | = |
| IA | illustration/photo/3D | 3D sets + 2D characters | same | same | same (01 game-engine look) |
| IA | painted backdrops | yes (night sky, town) | yes (army painting) | yes | yes |
| IA | texture maps | painted | painted | = | = |
| IA | icons/pictograms | none on screen | crest pictogram | none | none |
| IA | maps | none | none | none | none |
| IA | documents/props in-world | death certificate, tally wall | none (mechanism shown) | pardon (#16), calendar (#12) | newspapers, boards |
| IA | logos/marks | none | none | none | none |
| IA | poster treatment | none (Rick has no product) | none | none | none |
| IA | mockup/frame style | none | none | none | none |
| AV | cut-to-beat | joins on phrase onsets | same | = | [not measured] |
| AV | hit points | dirt burst on "up" f1336 | crash push on "pile" f1423 | = | = |
| AV | SFX-to-motion | snow puff on "buried" | thud f830 | = | 5/5 stems: SFX 8-12 dB over bed |
| AV | music swells/ducking | none | none | none | none (5/5) |
| AV | silence | none | none | none | none |
| EXTRA | sight gag per metaphor | $20 bribe under certificate f788-799 | cobwebs + sleeping guard for "weeks later" | yes | yes |
| EXTRA | time shown in-world | dawn ramp in one shot | cobweb/pigeon/stubble | = | = |

---
## j. Do / Don't (Rick vs what we have been doing)
| Rick does | we did (Dresden/Salzburg, measured) |
|---|---|
| Strange act or paradox in sentence 1, from t = 0 | "In 1730, a king ordered…" date first (Dresden) |
| A person with a goal and a doubter who mocks him in a quoted line | no conflict, no doubter |
| 2-3 escalations with time markers | a list of quantities and names |
| Reveal at 50-85 % ("You see,…") | no reveal |
| Payoff on the last word, end ≤ 1.2 s later | "Dresden, on your wall." tag line |
| 3.75 words/s, ≤ 3 pauses > 0.8 s | 2.54-2.66 words/s, 15-16 pauses > 0.8 s |
| Camera always moving, motion median 4.5-11.3 | 2.45-3.34, still frames 10-15 % |
| Flat drawn heads, dark monoline outline, big faces (30-39 % W in MS) | shaded 3D figurines, no outline, small faces |
| Captions 1-3 words, median width 24-49 % W | 2-4 words, median width 52-55 % W, numbers spelled out ("three thousand six hundred eggs") |
| Lifted blacks p2 ≥ 0.05, bright p98 ≥ 0.85 | Salzburg p2 0.004, p98 0.67; Dresden p98 0.77 |
| Dense sets, dynamic angles (low, high, top-down, through objects) | eye-level frontal stage shots, sparse walls and grass |
| Dissolves 4-14 f on phrase onsets with bridge objects | similar lengths but few bridge objects and long static holds |
| Music bed constant ~20 dB under VO | (owner: wrong style in Dresden) |

## k. Scored rubric and pre-render checklist
The full rubric with pass lines, evidence and the fix-and-retest log is phase4/04_rubric-and-test.md (sections A-D). Summary: 14 dimensions, each ≥ 95 % on Rick (overall 99.4 %). The pre-render checklist (16 binary items) is section D of that file and must be all YES before any 2K render; Gate 2 still applies.
