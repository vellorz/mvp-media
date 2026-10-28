# Handoff addendum: claude-seo added to the weekly routine
Written 2026-10-28 by Claude (Head of Social Media). Applies from the Sunday Nov 1 run onward.
schedule: Sundays 12:00 Central, posting weeks Mon to Sun

## What changed
On Oct 28 the owner asked that the claude-seo skills (github.com/AgriciDaniel/claude-seo, MIT, 26 sub-skills) be used for competitor research and for reviewing past posts before each week's content is made. They are now written into step 2 of the weekly routine ("Weekly social plan").

## Where it sits in the Sunday routine
1. Data sweep (unchanged): watch time, views, engagement and clicks come from Buffer, Metricool and Pinterest.
2. SEO and competitor research (this is the new part): run the claude-seo method alongside the existing keyword research.
3. Gate 1 scripts doc: the SEO findings feed the captions, titles, tags, pin copy and YouTube descriptions. The doc cites them.
4-7. Build, archive, Gate 2 and scheduling are unchanged.

## Which sub-skills are used, and for what
| Sub-skill | What it does for us |
|---|---|
| seo-ecommerce | Finds keyword gaps and marketplace signals in our Etsy listings compared with competitors' listings |
| seo-cluster | Groups buyer keywords into themes for each week's destinations (e.g. "Amalfi coast wall art", "Italy travel gift") |
| seo-sxo | Shows which post or listing type wins each search intent (video, carousel, pin, mockup) so we match the winning format |
| seo-content-brief | Scores competitors' titles and descriptions to set the bar for our captions, pin copy and YouTube titles |

## What it does NOT do
- claude-seo is built for websites, not social video. It can't measure retention or hooks. Those still come from the Buffer and Metricool numbers.
- It doesn't touch Etsy listings. Listing titles and tags remain Hermes's job. Claude only passes keyword ideas to Hermes in the weekly handoff.
- Some sub-skills call paid APIs (DataForSEO). We use the free parts only ($0 budget).

## How it's loaded
If /seo isn't available as an installed skill in that session, Claude shallow-clones the repo and follows each sub-skill's SKILL.md by hand. Either way the results are the same.

## Where the results go
- analytics.md in each week folder, with sources
- The Gate 1 scripts doc (keywords for each post)
- hermes/handoff/latest.md under "Useful for Etsy SEO", for Hermes's listing work

## Related changes the same day
- Images: pngimg.com is not used (CC BY-NC 4.0: non-commercial, credit required). Approved sources: our own posters, shapes drawn in code, and public-domain or CC0 archives (Smithsonian Open Access, Library of Congress, NYPL Public Domain, Wikimedia Commons PD, Openverse CC0).
- Network: the owner switched the project to a cloud environment that allows all domains. It applies to sessions that start after the change, not to ones already running. The Sunday scheduled task is unchanged and resumes its saved session, so it may still have the old network. Each run checks access first and reports any site that's still blocked.
- Etsy listing video: one shop-wide 10 s silent loop was made and approved (modern-vista-social/etsy-listing-video/).
