# Research board: file format for the agents

Mission Control's **Research** screen reads two folders in the shared brain (`hermes/` in vellorz/mvp-media). Any agent can write to them; the dashboard only reads.

The north star is **Etsy orders**. Every insight should say how it could move orders, and every experiment should measure something on the way to them.

## Insights: `hermes/insights/YYYY-MM-DD_short-slug.md`

A finding with evidence. Header lines (`key: value`), one blank line, then the body.

```
from: research
title: Lyon listings lose to 861 competitors on "lyon poster"
metric: etsy.visits
evidence: https://www.etsy.com/search?q=lyon+poster; 861 matching listings; 3 of our 4 Lyon tags unused by top 20

Two to four sentences: what you saw, why it matters for orders, what to try.
```

- `from`: `chief`, `marketing` or `research`.
- `title`: one line, the finding itself (not "Research notes").
- `metric` (optional): one of the metric keys below. It's used when the owner turns the insight into an experiment.
- `evidence`: links or numbers, separated by `;`.

## Experiment proposals: `hermes/experiments/YYYY-MM-DD_short-slug.md`

Usually written by the Chief of staff. A proposal shows in the **Proposed** column and in the owner's **Approvals** inbox. Nothing runs until the owner approves it and presses Start. Start captures the baseline (the 14 days before); Finish records the result.

```
from: chief
title: Gift-angle captions for the next two weeks
metric: etsy.orders
target: 20
days: 14
status: proposed

Hypothesis: captions framed as gifts ("for the one who still talks about Porto") raise orders before the holidays. Marketing writes them; Research picks the destinations.
```

- `target`: the % improvement that counts as a win (default 10).
- `days`: 7, 14, 21 or 28 (default 14).
- `status`: leave as `proposed`. The dashboard records approval, start and finish in its own log, so an approved proposal isn't shown twice.

## Weekly targets: `hermes/targets/YYYY-MM-DD.md` (the Monday of the week)

Written by the Chief of staff every Monday for the week starting that day. They show in the owner's Approvals inbox; the owner approves or edits them on the Today or Research screen.

```
week: 2026-11-02
etsy.orders: 3
etsy.visits: 110
social.views: 2400

One or two sentences: why these numbers (last 4 weeks' pace, what's planned this week).
```

## Lessons: `hermes/lessons.md`

The team's running memory of what works: what was tried, the result with numbers and source, keep/drop/retest, and confidence. Every agent reads it before planning and updates it when a result comes in (format at the top of the file).

## SEO scoreboard: `hermes/insights/seo-scoreboard.md`

Written by the hourly brain sync from Mission Control's SEO lab: which edited listings did better or worse than untouched listings, and what kind of edit they had. Research and the Chief read it to learn which SEO changes help.

## Metric keys

| Key | Measures |
|---|---|
| `etsy.orders` | Etsy orders per week (captured days only) |
| `etsy.visits` | Etsy visits per week |
| `etsy.conversion` | orders ÷ visits, % |
| `social.views` | views per week, all platforms (posts published in the window) |
| `views.tiktok`, `views.instagram`, `views.facebook`, `views.youtube`, `views.pinterest` | that platform's views per week |
| `avg.tiktok`, `avg.instagram`, … | that platform's views per post |

## Who writes what

- **Research:** insights after each research run (keywords, competitors, destinations that sell).
- **Marketing:** insights after the Thursday run (what the week's data showed). Experiment ideas go to the Chief as a handoff note, not straight into `experiments/`.
- **Chief of staff:** reads all insights each morning and proposes at most two experiments a week. It also proposes the weekly targets, which go to the owner's Approvals inbox.
- **Everyone:** reads `hermes/lessons.md` before planning, and adds a lesson when an experiment finishes or a week's results come in.
