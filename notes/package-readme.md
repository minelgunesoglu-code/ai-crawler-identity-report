# The AI Crawler Identity Report, round one: data and code

Requests to two websites, ismybrandinai.com and vouchaitools.com, that claimed to be an AI crawler or
asked for a secret file, from 3 to 9 September 2026 (UTC). Source: Cloudflare's GraphQL Analytics
API, dataset `httpRequestsAdaptiveGroups`, read on 10 September 2026.

Article: https://ismybrandinai.com/ai-visibility-case-study

## Rebuild the tables

```
python3 analyze.py
```

Python 3.8 or later, no extra packages. The script reads `rows/` and `bing-daily-citations.csv`,
writes the four tables to `tables/`, and prints the main counts quoted in the article. The tables
it writes are identical to the published ones.

## Files

| File | What it is |
|---|---|
| `rules.py` | The classification rules: crawler names, the secret-file rule, the Perplexity rule |
| `analyze.py` | The script that builds the four tables and the main counts from the rows |
| `rows/<site>-ua_path.json` | Grouped requests by user agent, path, response status and Cloudflare's verified bot category |
| `rows/<site>-hour_ua.json` | Grouped by hour (UTC), user agent and verified bot category |
| `rows/<site>-hour_path.json` | Grouped by hour (UTC), path and response status |
| `rows/<site>-country_ua.json` | Grouped by country of the requesting address, user agent and verified bot category |
| `bing-daily-citations.csv` | Bing Webmaster Tools AI Performance, daily citations for ismybrandinai.com, 3 to 7 September 2026, as the report displays them |
| `*.csv` (four tables) | The published tables |

Bing's report displays daily values of 1,000 or more rounded to the hundred. In this window that
affects one day: 3 September (1,200).

## What the rows leave out

Only requests that claimed an AI crawler's name or asked for a secret file are included. Ordinary
visits to ordinary pages are not, so these files do not show how much traffic either site receives.
Every crawler figure in the article is built from the two kinds of request that are included.

## Licence

CC BY 4.0. Cite as: Gunesoglu, M. (2026). *The AI Crawler Identity Report, round one.* Is My Brand in AI.
https://ismybrandinai.com/ai-visibility-case-study
