# Change log: Rick Master Guide merge into the cartoon checklist (Nov 17 2026)
Owner approval (Nov 17 2026, relayed in the "Build 99% Rick-style test video" thread): all new rules, the fixes to contradicting older rules, and the renumbering are approved. Backups taken before any edit, byte-identical (sha256 checked): CHECKLIST_backup-2026-11-17_pre-rick-merge.md (4ff9caf2…), DETAIL_STANDARD_backup-2026-11-17_pre-rick-merge.md (705e7c13…).

## A. New rules: old (proposal) number → new number
The master-guide thread first drafted them as 154-173, then renumbered them 172-191 because the live checklist already ended at 171 (rules 153-171 were added by the Salzburg thread). Numbers 144-152 were never assigned in any checklist (gap between rule 143 and 153); left empty so no existing number changes.
| proposal draft # | final # | rule | why |
|---|---|---|---|
| 154 | 172 | Rick Master Guide is the build spec | guide k |
| 155 | 173 | Script template | 20/20 transcripts; gap: Dresden/Salzburg had no doubter/reveal |
| 156 | 174 | No date-/place-first openings | Dresden opened "In 1730…" |
| 157 | 175 | Roles, not names | Rick never names; ours used 3 names |
| 158 | 176 | 1-4 numbers, no stat lists | Dresden had 9 numbers |
| 159 | 177 | No "on your wall"/CTA | 19/19 Rick endings; owner Nov 17 |
| 160 | 178 | Poster inside the payoff scene | owner Nov 17 approval |
| 161 | 179 | VO pace 3.4-4.1 w/s, pause limits | ours 2.5-2.7 w/s |
| 162 | 180 | Join grammar 4-14 f varied | ours all 5 f |
| 163 | 181 | Bridge objects ≥ 50 % | ours rare |
| 164 | 182 | Camera never static > 1.5 s, motion ≥ 4.5 | ours 2.5-3.3, holds 35-36 f |
| 165 | 183 | Camera hits on nouns, crash push | #14 f1419-1427 |
| 166 | 184 | Character construction (flat head, 6-10 px outline, head 30-39 % W) | ours 3D figurines |
| 167 | 185 | Faces act every 0.3-2 s | ours static faces |
| 168 | 186 | Caption spec | ours 11-22 % too big |
| 169 | 187 | Grade window | Salzburg p2 0.004 |
| 170 | 188 | Mix and music | owner: wrong music (Dresden) |
| 171 | 189 | Facts in-world | agrees with 2A |
| 172 | 190 | Rubric gate before Gate 2 | guide k |
| 173 | 191 | Dynamic angles ≥ 4 types | ours frontal |

## B. Older rules fixed in place (number unchanged; old text kept inside the rule as "Was: …")
| rule | file | change | why (master guide wins) |
|---|---|---|---|
| 5 | CHECKLIST | "no zoom/push into a character on a narration beat" → no push into a torso; pushes land on face/prop | Rick's most common move is the push-in; camera never stops (182-183) |
| 8 | CHECKLIST | bed "~15-20 dB under" → ≈ 20 dB under, -14 LUFS, -2 dBTP, LRA ≤ 3.2, Drew on eleven_v4 | rule 188 |
| 9 | CHECKLIST | "Montserrat 800, lower third" → full rule 186 spec | captions 11-22 % too big |
| 10 | CHECKLIST | "end on the poster shown whole" → poster inside the payoff scene, end ≤ 1.2 s after last word | rules 177-178 |
| 55 | CHECKLIST | outline 6-8 px, motion median 1.2-1.5 px/f, "big moves become soft dissolves" → outline 6-10 px, head 30-39 % W, motion median ≥ 4.5, no static > 1.5 s | rules 182, 184 (old motion cap caused static camera) |
| 57 | CHECKLIST | "focus blur only indoors" → FG/MG/BG + DOF + haze in every shot | guide e Depth |
| 134 | CHECKLIST | kept the 4 s shot rule, added camera never static > 1.5 s | rule 182 |
| 137 | CHECKLIST | "follow the references and Chicago" → Rick's join grammar; Chicago v21 no longer the benchmark | rules 180-181 |
| Reference-first para | CHECKLIST | Chicago v21 benchmark removed; the master guide is the written spec | owner Nov 17 |
| 141 A | CHECKLIST | read RESUME + guide + ledger + RULES_CONSOLIDATED first; Chicago v21 removed | owner Nov 17 |
| A table saturation | DETAIL_STANDARD | 0.40-0.48 → 0.37-0.66 | rule 187 (Rick 0.376-0.653) |
| A table edge | DETAIL_STANDARD | ≥ 32 % → average ≥ 28 % (edge.py) + 0.20-0.35 (metrics.py) | rule 72 already set 28 %; guide e |
| A table motion | DETAIL_STANDARD | added rick-spec diff ≥ 4.5 | rule 182 |
| D7 / Q4 | DETAIL_STANDARD | head 18-22 % → 30-39 % W in MS | rule 184 |
| D8 / Q5 | DETAIL_STANDARD | face every 8-15 f → every 0.3-2 s | rule 185 |
| T2 | DETAIL_STANDARD | whip arc → not a default, max one | guide b "Never" |
| T3, G2 | DETAIL_STANDARD | dissolves 4-6 f / 4-8 f → 4-14 f, default 6-12 f, varied | rule 180 |
| Q7, 3A | DETAIL_STANDARD | saturation 0.40-0.48 → 0.37-0.66 | rule 187 |
| G3 outline | DETAIL_STANDARD | 6-8 px → 6-10 px | rule 184 |
| memory: VO tags | mvp-vo-delivery-tags | kept; pace + pause limits of 179 added (memory checklist-12) | Salzburg failed on pace too |
| memory: music taste | MEMORY.md | kept; expressed inside rule 188 (plucked melodic loop over soft pulse) | resolves house/garage vs plucked bed |

## C. Not changed (checked, no conflict)
Rules 1-4, 6-7, 11-54, 56, 58-133, 135-136, 138-143, 153-171 (stricter or orthogonal to the guide). Rule 52 "at most 1 hard cut" is stricter than Rick (0-2) and stays. Rule 72 (edge ≥ 28 %) stays as the critical owner metric.
