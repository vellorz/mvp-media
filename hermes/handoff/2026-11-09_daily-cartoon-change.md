# Handoff for the Hermes Dashboard chats (Claude + Codex) — Nov 9 2026

From: Claude, Head of Social Media for Modern Vista Prints. Context only: this does not authorize Hermes to change social schedules, publish, or edit Etsy listings.

## What changed (owner decision, Nov 8-9)
1. **One video format now: cartoon-3d story shorts.** ~60-70 s, a true and sourced surprising story about the poster's place, told with flat cartoon characters in a painted 3D world, Drew voice-over, 1-3 word captions, original music. It ends on the whole poster. The old formats (paper collage, map route, Mr. Hale, carousels, etc.) are retired unless the owner asks.
2. **Volume: 1 video per day per platform** (Instagram Reel, Facebook Reel, TikTok, YouTube Short, Pinterest video pin). This replaces "2 posts/day/platform".
   - Dashboard rule (c) should now expect **1 post/day/platform** in Buffer, not 2.
3. **Pinterest is maximized.** Every day gets the video pin plus 3-4 fresh static poster pins across keyword boards. New boards are created as needed (by country/region and by room/gift).
4. **Scheduled tasks rewritten** (same IDs, both fire into the main thread):
   - Sunday 12:00 CT `trig_01VkpfBg45X4spiEHUTVnMmh` "Daily cartoon videos (Sunday run, Mon-Thu)": 4 videos. It is ENABLED again; next run Sun Nov 15.
   - Thursday 12:00 CT `trig_018PXZtrJSxXjakazT8kkHbZ` "Daily cartoon videos (Thursday run, Fri-Sun)": 3 videos. Next run Thu Nov 12.
   - Both still do: brain read, data check-in, SEO/trends, Gate 1 (scripts doc), then Part B on "finish this run" (build, Gate 2 per video, schedule).
   - Full prompts: handoff/2026-11-09_daily-cartoon/{sunday,thursday}-task-prompt.txt.
5. **Engine in the repo.** The cartoon engine (Remotion + three.js project, audio scripts, owner-correction checklist) is in vellorz/mvp-media `engine/cartoon-3d/`, so any run can rebuild it. Renders take ~3 h per video on the cloud box.

## Week 03 status (Mon Nov 9 - Sun Nov 15)

| Day | Video | Poster | Status |
|---|---|---|---|
| Mon | London Bridge → Arizona | 0245 London | SCHEDULED |
| Tue | The tower Paris tried to tear down | 0495 Paris | rendering, Gate 2 pending |
| Wed | Pisa: fix it without fixing it | 0351 Pisa | queued, Gate 2 pending |
| Thu Nov 12 | not planned | | |
| Fri-Sun | planned by the Thursday run | | |

Monday post times (Central):
- YouTube 16:00, via Metricool (post 421343968).
- TikTok 18:00 (Buffer 6af1465a2f1ff83d4513fcf5).
- Pinterest 18:00 (video pin, board Architecture & City Travel Prints).
- Instagram 19:00 (Buffer 6af14658796ccae2668143d7).
- Facebook 19:00 (Buffer 6af14659e29b1359f0ca150d).
- Times came from Metricool best-time data (Monday peaks: TikTok 18:00, YouTube 16:00).

Approvals: Tue + Wed scripts approved Nov 8 (Gate 1). Monday's video was approved at Gate 2 on Nov 9.

## What Hermes can help with
- Keep posting-times.md / social-daily.md updating hourly. The new format is 60-70 s, so **watch time and completion %** are the key numbers to log per video.
- Wednesday 20:00 research: send **true, sourced, surprising stories** for poster places (engineering failures, odd purchases, near-demolitions, famous mistakes). Those feed the Thursday run.
- Saturday brief: the most-visited listings, with **listing URLs**, so each video and pin can link the exact listing instead of a shop search.
- Etsy listing SEO stays with Hermes. Social never edits listings.
