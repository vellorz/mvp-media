# Round 2 fix plan (from round-1 verifier reports, Nov 18 ~02:50Z). Reports kept in verify/round1/.
CRITICAL
- P3/R21 line-ups facing camera: S08 f900 (4 side by side), S11 f1056-1114 (frontal facade, row). Restage: angled camera, staggered depth, overlap.
- R07/C3 medium-shot heads 30-39 % W: fails f390 S03, f630 S05, f690-780 S06, f780 S07, f960/990 S09, f1140/1170 S12. Tighten cameras/lens.
- R22/L8 interior vignette (corner/centre 0.33-0.42) + depth of field: post vignette on interiors; fstop down (cam dof already on, fs 5.6 -> ~1.4 medium).
- G1 S15 newspaper floats (no hands) f1488-1554: add mitten hands gripping the edges.
OTHER FAILS
- L9 S07/S08 no foreground layer, flat blue facade.
- C8 S13 arm pops in 1262/1306: slide in from frame edge.
- K8 eased landings on nouns: only 1/10 within +-3 f; retime keys to noun onsets.
- T1 box bottom 72.24 > 72.2: baseline 0.717->0.7125 (DONE in post.py).
- Safe area: faces in bottom 20 % S07 816-834, S08 870-932, S09 939-948. Faces must sit above caption band (y_cam >= 0.36).
- E2 poster partly hidden f1608-1693 (bay post + heads). Keep poster clear once visible.
- G5: 498 thief behind woman (S04); 620-624 writer behind sergeant (S05); 892-896 owner behind fan (S08); sergeant cut right edge 528-606 (S05); owner out of bottom 822-834 (S07); exec head cut top 1404-1422 (S14).
- G6: pole cuts DINER f942 (S09); sergeant head over BLACK FRIDAY 630-642 (S05); signs cropped: TOYS/DRUGS 330-426, DINER 504-522, NOV 1961 cal 720-768, HARTWELL 792-834/918-930, newsstand 1074-1116, banner 1708-1712.
- 155/166: chalk grows while writer hidden 622-628; black entries before pen 1302<1306; red pen over pre-printed figures 1266-1300 -> reveal mask follows pen.
- rule 54: pennant tips on faces 366-426 (S03).
SOFT / NOTES
- Props out of story order: framed BLACK FRIDAY paper in precinct (pph2 paper66); BIG FRIDAY register tag in S06; 1981 bay banner reads BIG FRIDAY 1961; 1981 paper 5 CENTS.
- White flat doorway 1644-1662: give interior.
- S02 podium empty: add cop.
- S10 washed out (luma .64 sat .22); captions over headlines S10 1014-1026, S15 1512-1558.
- Empty sky S01 top 28 %; S15 cop merges with blue skyline; luma spread 0.051 vs Rick 0.11.
- Captions slower than Rick (17 f mean vs 9-12); f0 no caption.
- Final push 9 f lands on "show"; poster sharpness 0.28 of source.
- Script critique (S6 irony, S9 "worked so well" overclaim, Big Friday issuer disputed): VO is owner-approved; propose, don't change.
