# Licence notes

The licence itself is in [`LICENSE`](LICENSE): Creative Commons Attribution 4.0
International (CC BY 4.0). This file holds the things a bare licence text cannot
say, and it is the file to read before reusing anything here.

  Full legal code: https://creativecommons.org/licenses/by/4.0/legalcode
  Summary:         https://creativecommons.org/licenses/by/4.0/

## What is covered

The material produced by the author in this repository: the grouped request
data in `rows/`, the derived tables in `tables/`, `bing-daily-citations.csv`, the
code (`rules.py`, `analyze.py`), and the supporting documents in `notes/`.

You may share and adapt it, including commercially, provided you give appropriate
credit, link to the licence, and indicate whether changes were made.

Suggested attribution:

    Gunesoglu, M. (2026). The AI Crawler Identity Report, round one.
    Is My Brand in AI.
    https://ismybrandinai.com/ai-visibility-case-study

## Where the data comes from

**Cloudflare.** The rows were read from Cloudflare's GraphQL Analytics API,
dataset `httpRequestsAdaptiveGroups`, for the author's own two websites,
ismybrandinai.com and vouchaitools.com, on 10 September 2026. They are aggregate
counts grouped by the dimensions named in each file. They contain no IP
addresses, query strings or cookies. The country field is the country Cloudflare
assigns to the requesting address, and it is published only as part of a grouped
count.

**Bing Webmaster Tools.** `bing-daily-citations.csv` holds five daily values from
the AI Performance report for the author's own site, ismybrandinai.com, as the
report displays them.

## What this licence does NOT cover

**Strings sent by third parties.** Every user agent and every requested path in
`rows/` is text that a requesting client chose to send. They are reproduced
verbatim because the study is about what those strings claim. Some user agents
carry a crawler operator's published contact address or URL, for example
`claudebot@anthropic.com`. The author makes no claim of ownership over any of
these strings and does not license them.

**Names and marks.** Crawler names such as GPTBot, ClaudeBot, Googlebot or
BingBot, and the names of the companies that operate them, belong to their
owners. Their appearance here describes what a request claimed, and an
unverified request carrying a name was, by definition, not shown to come from
that company.

**Paths requested by probing clients.** Many paths in `rows/` name secret files
(`/.env`, `/.aws/credentials` and similar). They are the requests that were
made, not files that exist on either site. No such request received a file.
