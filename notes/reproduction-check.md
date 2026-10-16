# Reproduction check

Date: 17 October 2026. Machine: macOS 26.6.2, Python 3.9.6, no extra packages.

## 1. The repository holds the published package unchanged

The source is the download published on the site,
`https://ismybrandinai.com/data/ai-crawler-identity/ai-crawler-identity-round1.zip`
(SHA-256 `c2abd3dfff5d96058c4a84157507869d9c54eb9a2ca322c2848858a81afcb185`).
It was unzipped, and every file in it was compared with `cmp` against the
loose copy of the same file published next to it on the site. All 16 files are
identical. The layout here is the zip's, with the four table CSVs moved into
`tables/`, which is where `analyze.py` writes them. The zip's README is kept as
`notes/package-readme.md`. No file content was edited.

| File | SHA-256 |
|---|---|
| `rules.py` | `4bcedc60a5b590620ddf88b239dddeb6c0bf45e6169df78fa15c7c55d0f9d0cf` |
| `analyze.py` | `8398e8fd66d7fe7300861ab30a6592f516370b2be15e3f023ef477f15f7803ff` |
| `bing-daily-citations.csv` | `51d05c9e48e061a8c437b799069887aa9f129391dbebaf1cd5450ffcedc5e2f4` |
| `rows/ismybrandinai.com-country_ua.json` | `614d4cc5cbcf06542a2e8ad957d18e729484c467e3187944ea19fb3c572b8d90` |
| `rows/ismybrandinai.com-hour_path.json` | `f50d8440422b41d9a54110d0d9324a230f31636b0dc633fe3c84f502dc901167` |
| `rows/ismybrandinai.com-hour_ua.json` | `0b7519559c8efc94091c4820f2e68a923c2a18211fbe37f1fc5130b6661dd32e` |
| `rows/ismybrandinai.com-ua_path.json` | `a389afb024c6a82f3ea973deb580adb94618eaed19dda8fe44402de10a184172` |
| `rows/vouchaitools.com-country_ua.json` | `425b248145f145d8586743ca9569e52a9fad6fda7da3920ce90db33b8301eae1` |
| `rows/vouchaitools.com-hour_path.json` | `90a1c0f53d6633d3b2db03ec201e94f4113dd9836f1e7c90e0d4e220fc3a7e86` |
| `rows/vouchaitools.com-hour_ua.json` | `34e1cb54116b10e64e94dcc6358e460d66372d868f6cfee2fbf563114f8946fe` |
| `rows/vouchaitools.com-ua_path.json` | `5ffc12932e2fe2fda3c3487e3f4e2277576829dd22d808f88fe30e006cede8d8` |

## 2. The script rebuilds the published tables byte for byte

`analyze.py` was run unchanged, in a separate copy of `rules.py`, `analyze.py`,
`bing-daily-citations.csv` and `rows/`, so that the published tables could not be
overwritten before the comparison. Each table it wrote was compared with `cmp`
against the published file.

| Table | SHA-256 (published = rebuilt) | Result |
|---|---|---|
| `claimed-identity-vs-cloudflare-verification.csv` | `eb2d1becfe09086a7fecb9b9d95efe05df5bf77af476af76df5c6d644ca434b5` | identical |
| `daily-ai-named-requests.csv` | `755669a951324be8d74ca7357e3a8ecfdb2210f72ea9ab0866eb18e182c62b72` | identical |
| `secret-file-probe-targets.csv` | `89e4efd7ae2e666a9322aec7e7d98a37409b245da108eb66d6a1b50aa1b8c7e3` | identical |
| `bing-citations-vs-microsoft-requests.csv` | `6e8d4fbe7a1f176521bf164457ffa5da2213caff17c82f46ba533e708ab8df1a` | identical |

A note on the command. `python3 -I analyze.py` stops with
`ModuleNotFoundError: No module named 'rules'`: isolated mode leaves the script's
own folder off the import path, and `analyze.py` imports `rules.py` from there.
This is expected behaviour of `-I`, not a defect in the code. The check was run as
`python3 -E -s analyze.py`, which ignores environment variables and user site
packages but keeps the script's folder, so only standard-library modules and
`rules.py` were loaded. Plain `python3 analyze.py`, as the README says, gives the
same result.

## 3. The printed counts match the article

| Article statement | Printed by `analyze.py` | Match |
|---|---|---|
| Verified requests to ismybrandinai.com: OpenAI 396, Meta 314, Microsoft 168, Amazon 142, Google 136, Anthropic 49, Baidu 42, Apple 35 | `verified requests by operator` for ismybrandinai.com: the same eight values | yes |
| 240 ChatGPT-User requests within the OpenAI figure | `ChatGPT-User` verified = 240 in the identity table | yes |
| None of the 3,234 verified requests to the two sites asked for a hidden file | verified 1,282 + 1,952 = 3,234; verified requests that asked for a hidden file: 0 and 0 | yes |
| 476 unverified requests to ismybrandinai.com asked for hidden files | `impersonation_probe` = 476 | yes |
| ... carrying 13 crawler names | 13 names with `unverified_to_secret_paths` above 0 for ismybrandinai.com, summing to 476 | yes |
| Microsoft verified requests 3 to 7 September: 113 | 14 + 30 + 47 + 3 + 19 = 113 | yes |
| About 4,150 Bing citations in those days | 1,200 + 926 + 586 + 649 + 788 = 4,149 | yes |
| 37 citations per request | 4,149 / 113 = 36.7 | yes |
| Citations outnumbered requests each day by 12 to 216 times | daily ratios 85.7, 30.9, 12.5, 216.3, 41.5 | yes |
| 20 crawler names tracked | 20 entries in `rules.CRAWLERS` | yes |

Other counts printed by the script, for the record (not quoted in the article):

| | ismybrandinai.com | vouchaitools.com |
|---|---:|---:|
| Requests claiming a tracked crawler name | 2,349 | 2,146 |
| of which verified | 1,282 | 1,952 |
| of which unverified, counted as impersonation | 851 | 17 |
| of which Perplexity, unverifiable, no hidden-file request | 216 | 177 |
| Hidden-file requests, any user agent | 1,910 | 3,003 |
| Hidden-file requests answered with a 2xx status | 0 | 0 |

## 4. Privacy check

Every value in `rows/` and every line of the tables was scanned for IPv4 and IPv6
addresses, email addresses, query strings, API key and token formats (`sk-`,
`AKIA`, `ghp_`, `xox`, `AIza`, JWT), long opaque strings, and words such as
token, password, secret, cookie, session and auth.

- The rows have six dimensions only: `userAgent`, `clientRequestPath`,
  `edgeResponseStatus`, `verifiedBotCategory`, `datetimeHour` and
  `clientCountryName`. There is no IP address field and no query-string field.
  No requested path contains `?` or `=`.
- Address-shaped matches are all browser version numbers inside user agents,
  such as `Chrome/131.0.0.0`.
- Email-shaped matches are crawler operators' published contact addresses inside
  user agents (`claudebot@anthropic.com`, `claude-user@anthropic.com`,
  `spider-feedback@bytedance.com`). Other `@` matches are `/@fs/` and `/@vite/`
  path prefixes used by probing clients.
- Matches for secret words are requested paths such as `/secrets.json` or
  `/.azure/accessTokens.json`: names of files that were asked for, carrying no
  value. Home-folder names in probe paths are generic defaults (`ubuntu`, `node`,
  `ec2-user`, `azureuser`, `admin`, `debian`, `www-data`).
- Long strings are the sites' own page slugs and build asset names.
- No personal name, real credential or secret value was found.

One observation for the owner: 30 requests carry the user agent
`Claude-User (claude-code/<version>; +https://support.anthropic.com/)`, which
Claude Code sends when it fetches a page. Some of them may be the author's own
tooling. They identify no person and are kept as published.
