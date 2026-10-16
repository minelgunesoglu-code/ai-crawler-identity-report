# The AI Crawler Identity Report, round one

**Which requests that carry an AI crawler's name are really that crawler, checked against Cloudflare's bot verification on two websites**

| | |
|---|---|
| **Article** | https://ismybrandinai.com/ai-visibility-case-study |
| **Repository** | https://github.com/minelgunesoglu-code/ai-crawler-identity-report |
| **Archive** | DOI: to be added after the Zenodo release |
| **Collected** | 3 to 9 September 2026 (UTC), read from Cloudflare on 10 September 2026 |
| **Sites** | ismybrandinai.com and vouchaitools.com, both run by the author |
| **Source** | Cloudflare GraphQL Analytics API, dataset `httpRequestsAdaptiveGroups`; Bing Webmaster Tools AI Performance for ismybrandinai.com |
| **Headline** | Not one of the **3,234** verified requests from AI and search crawlers to the two sites asked for a hidden file. In the same week, **476** unverified requests to ismybrandinai.com carrying 13 crawler names, among them GPTBot, ClaudeBot and ChatGPT-User, asked for hidden files. |
| **Licence** | CC BY 4.0 (`LICENSE`); see `LICENCE-NOTES.md` for what it does and does not cover |

A server log records whatever name a request gives, and a name costs nothing to
type. This dataset holds one week of requests to two websites that either claimed
one of 20 AI or search crawler names, or asked for a secret file, together with
Cloudflare's verdict on whether each request really came from the crawler it
named.

**What is measured:** the user agent a request claimed, whether Cloudflare placed
it in a verified bot category, the path it asked for and the response status.
**What is NOT measured:** how much ordinary traffic either site receives, who sent
any unverified request, and whether any crawler's visit led to a citation. The
rows contain no IP addresses.

---

## 1. Findings

All figures below are the ones published in the article and are rebuilt exactly
by `analyze.py` (see `notes/reproduction-check.md`).

### The real crawlers never asked for a hidden file

Across both sites, Cloudflare verified 3,234 requests from AI and search
crawlers in the week. None of them asked for a hidden file.

Verified requests to ismybrandinai.com, by company:

| Company | Crawlers | Verified requests |
|---|---|---:|
| OpenAI | ChatGPT-User, OAI-SearchBot, GPTBot | 396 |
| Meta | Meta-ExternalAgent | 314 |
| Microsoft | BingBot | 168 |
| Amazon | Amazonbot | 142 |
| Google | Googlebot | 136 |
| Anthropic | ClaudeBot | 49 |
| Baidu | Baiduspider | 42 |
| Apple | Applebot | 35 |

The OpenAI figure includes 240 requests from ChatGPT-User.

### Requests that borrowed the names went straight for secret files

That week, 476 unverified requests to ismybrandinai.com carrying 13 crawler
names asked for hidden files: environment files, cloud credentials such as
`/.aws/credentials`, and the credential and config files of AI coding tools,
such as `/.claude/.credentials.json` and `/.cursor/config.json`. Per-name counts
are in `tables/claimed-identity-vs-cloudflare-verification.csv`, and what the
hidden-file requests asked for is in `tables/secret-file-probe-targets.csv`.

Counting AI crawlers by name counts the impostors too, which is why the company
table above counts verified requests only.

### Crawler requests and citations measure different things

In the five days both sources cover, 3 to 7 September, Microsoft's verified
crawlers made 113 requests to ismybrandinai.com, while Bing Webmaster Tools
counted about 4,150 AI citations of the site: 37 citations for every request.
Citations outnumbered requests on each of the five days, by 12 to 216 times. A log
shows the crawl; the citation happens inside the AI answer, where the site's own
log cannot see it. The daily pairs are in
`tables/bing-citations-vs-microsoft-requests.csv`.

---

## 2. What is in this repository

```
rules.py                   the classification rules: 20 crawler names, the secret-file rule, the Perplexity rule
analyze.py                 rebuilds the four tables and prints the main counts from the rows
rows/<site>-ua_path.json     requests grouped by user agent, path, response status and verified bot category
rows/<site>-hour_ua.json     grouped by hour (UTC), user agent and verified bot category
rows/<site>-hour_path.json   grouped by hour (UTC), path and response status
rows/<site>-country_ua.json  grouped by country of the requesting address, user agent and verified bot category
bing-daily-citations.csv   Bing AI Performance daily citations for ismybrandinai.com, 3 to 7 September 2026
tables/                    the four published tables, as on the site
notes/
  reproduction-check.md    the byte-for-byte check of the tables and the printed counts
  package-readme.md        the README shipped in the original download on the site
  zenodo-release-steps.md  how this repository is archived on Zenodo
```

| File | What it is |
|---|---|
| `tables/claimed-identity-vs-cloudflare-verification.csv` | Per site and crawler name: verified requests, unverified ones, and how many of each asked for a hidden file |
| `tables/daily-ai-named-requests.csv` | Per site and day: crawler requests by name, verified, and hidden-file attempts |
| `tables/secret-file-probe-targets.csv` | Per site: what the hidden-file attempts asked for |
| `tables/bing-citations-vs-microsoft-requests.csv` | Per day, 3 to 7 September: Bing AI citations and Microsoft's verified crawler requests |

### What the rows include and leave out

Only requests that claimed an AI crawler's name or asked for a secret file are
included. Ordinary visits to ordinary pages are not, so these files do not show
how much traffic either site receives. Every crawler figure in the article is
built from the two kinds of request that are included.

Not included: IP addresses, query strings, cookies or request headers other than
the user agent (Cloudflare's grouped analytics do not return them at this level),
and the rest of the article's Bing data (the 91-day citation series, the page and
phrase exports). Only the five Bing daily values needed for the crawler comparison
are here.

### Definitions

- A request counts as **verified** when Cloudflare places it in a verified bot
  category.
- A request counts as **asking for a hidden file** when its path has a segment
  that starts with a dot, other than the public `/.well-known/`, or matches a short
  list of well-known secret files. The exact patterns are in `rules.py`.
- Cloudflare verified none of the PerplexityBot or Perplexity-User requests in
  this data. Unverified requests under those two names are kept on their own line
  unless they ask for a hidden file, in which case they count as impersonation.
- Bing's report displays daily values of 1,000 or more rounded to the hundred. In
  this window that affects one day, 3 September (1,200). The values are used as
  displayed.

---

## 3. Rebuilding the tables

```bash
python3 analyze.py
git status --short tables/   # prints nothing: the rebuilt tables are byte-identical
```

Python 3.8 or later, standard library only. Run it from the repository root. The
script reads `rows/` and `bing-daily-citations.csv`, overwrites the four files in
`tables/`, writes `results.json` (gitignored) and prints the main counts quoted in
the article.

Run it as shown. `analyze.py` imports `rules.py` from its own folder, so
`python3 -I analyze.py` (isolated mode, which leaves the script's folder off the
import path) stops with `ModuleNotFoundError: No module named 'rules'`.

---

## 4. Citing this

> Gunesoglu, M. (2026). *The AI Crawler Identity Report, round one* [Data set].
> Is My Brand in AI. https://ismybrandinai.com/ai-visibility-case-study

If a count here does not match what you get from the files, open an issue and a
correction will be published saying what changed.
