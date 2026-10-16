#!/usr/bin/env python3
"""Rebuild every figure of The AI Crawler Identity Report, round one, from the
published rows.

Run it in this folder:  python3 analyze.py
It reads rows/*.json and bing-daily-citations.csv, writes the four tables to
tables/ and results.json, and prints the main counts quoted in the article.

The rows are Cloudflare GraphQL Analytics API groups (httpRequestsAdaptiveGroups)
for 3 to 9 September 2026, UTC. They contain only requests that claimed an AI
crawler's name or asked for a secret file, so they do not show how much
ordinary traffic either site receives. Every crawler figure in the article is built
from those two kinds of request and is fully reproducible here.
"""
import collections
import csv
import json
import os
import re

import rules

HERE = os.path.dirname(os.path.abspath(__file__))
SITES = ["ismybrandinai.com", "vouchaitools.com"]
WAVE_DAY = "2026-09-08"


def rows(site, shape):
    with open(os.path.join(HERE, "rows", "%s-%s.json" % (site, shape)), encoding="utf-8") as fh:
        return json.load(fh)["rows"]


def main():
    results = {"sites": {}}
    rows_identity, rows_daily, rows_targets = [], [], []
    for site in SITES:
        ver = collections.Counter(); imp = collections.Counter(); imp_probe = collections.Counter()
        ver_probe = collections.Counter()
        unv = collections.Counter(); verified_by_operator = collections.Counter()
        probe_by_disguise = collections.Counter(); probe_codes = collections.Counter()
        probe_targets = collections.Counter(); vite = 0
        daily = collections.OrderedDict()
        for r in sorted(rows(site, "ua_path"), key=lambda r: r["day"]):
            d = daily.setdefault(r["day"], {"ua_counted": 0, "verified": 0, "impersonation": 0,
                                            "impersonation_probe": 0, "perplexity_unverifiable": 0,
                                            "probes_all": 0, "probes_2xx": 0, "microsoft_verified": 0})
            dims, n = r["dimensions"], r["count"]
            agent = dims.get("userAgent") or ""
            crawler, operator = rules.classify(agent)
            code = int(dims.get("edgeResponseStatus") or 0)
            path = dims.get("clientRequestPath") or "/"
            verified = bool(dims.get("verifiedBotCategory"))
            probe = rules.is_probe(path)
            if probe:
                d["probes_all"] += n
                probe_by_disguise[rules.disguise(agent, crawler)] += n
                probe_codes[str(code)] += n
                probe_targets[rules.target(path)] += n
                vite += n if rules.VITE_FS.search(path) else 0
                if 200 <= code < 300:
                    d["probes_2xx"] += n
            if not crawler:
                continue
            d["ua_counted"] += n
            if verified:
                d["verified"] += n
                ver[crawler] += n
                verified_by_operator[operator] += n
                if probe:
                    ver_probe[crawler] += n
                if operator == "Microsoft":
                    d["microsoft_verified"] += n
            elif crawler in rules.UNVERIFIABLE and not probe:
                d["perplexity_unverifiable"] += n
                unv[crawler] += n
            else:
                d["impersonation"] += n
                imp[crawler] += n
                if probe:
                    d["impersonation_probe"] += n
                    imp_probe[crawler] += n
        for day, d in daily.items():
            rows_daily.append({"site": site, "day": day, **d})
        names = sorted(set(ver) | set(imp), key=lambda k: -(ver[k] + imp[k]))
        for name in names:
            rows_identity.append({"site": site, "claimed_crawler": name, "verified": ver[name],
                                  "verified_to_secret_paths": ver_probe[name],
                                  "unverified": imp[name], "unverified_to_secret_paths": imp_probe[name],
                                  "verified_share": round(ver[name] / (ver[name] + imp[name]), 3) if ver[name] + imp[name] else ""})
        for name, n in unv.items():
            rows_identity.append({"site": site, "claimed_crawler": name + " (cannot be verified, no hidden-file request)",
                                  "verified": 0, "verified_to_secret_paths": 0, "unverified": n,
                                  "unverified_to_secret_paths": 0, "verified_share": ""})
        total_probes = sum(probe_targets.values())
        for name, n in probe_targets.most_common():
            rows_targets.append({"site": site, "target": name, "requests": n,
                                 "share": round(n / total_probes, 3) if total_probes else ""})

        by_hour_imp = collections.Counter(); by_hour_probe = collections.Counter()
        for r in rows(site, "hour_ua"):
            dims = r["dimensions"]
            crawler, _ = rules.classify(dims.get("userAgent") or "")
            if r["day"] == WAVE_DAY and crawler and not dims.get("verifiedBotCategory") and crawler not in rules.UNVERIFIABLE:
                by_hour_imp[dims["datetimeHour"][11:13]] += r["count"]
        for r in rows(site, "hour_path"):
            if r["day"] == WAVE_DAY and rules.is_probe(r["dimensions"].get("clientRequestPath") or "/"):
                by_hour_probe[r["dimensions"]["datetimeHour"][11:13]] += r["count"]
        countries = collections.Counter(); nl_by_day = collections.Counter()
        for r in rows(site, "country_ua"):
            dims = r["dimensions"]
            crawler, _ = rules.classify(dims.get("userAgent") or "")
            if crawler and not dims.get("verifiedBotCategory") and crawler not in rules.UNVERIFIABLE:
                countries[dims.get("clientCountryName") or "?"] += r["count"]
                if dims.get("clientCountryName") == "NL":
                    nl_by_day[r["day"]] += r["count"]

        week = {k: sum(d[k] for d in daily.values()) for k in
                ("ua_counted", "verified", "impersonation", "impersonation_probe",
                 "perplexity_unverifiable", "probes_all", "probes_2xx")}
        week["days_with_probes"] = sum(1 for d in daily.values() if d["probes_all"])
        results["sites"][site] = {
            "week": week, "daily": daily,
            "claimed_vs_verified": {n: {"verified": ver[n], "verified_to_secret_paths": ver_probe[n], "unverified": imp[n], "unverified_to_secret_paths": imp_probe[n]} for n in names},
            "verified_by_operator": dict(verified_by_operator.most_common()),
            "perplexity_unverifiable": dict(unv),
            "probes_by_disguise": dict(probe_by_disguise.most_common()),
            "probe_status_codes": dict(sorted(probe_codes.items())),
            "probe_targets": dict(probe_targets.most_common()),
            "probes_via_vite_fs": vite,
            "wave_2026_09_08": {"impersonation_by_hour_utc": dict(sorted(by_hour_imp.items())),
                                "probes_by_hour_utc": dict(sorted(by_hour_probe.items()))},
            "countries_unverified_ai_named": dict(countries.most_common(10)),
            "nl_unverified_ai_named_by_day": dict(sorted(nl_by_day.items())),
        }

    bing = {}
    with open(os.path.join(HERE, "bing-daily-citations.csv"), encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            bing[row["day"]] = int(row["bing_ai_citations"])
    ib = results["sites"]["ismybrandinai.com"]["daily"]
    rows_bing = [{"day": day, "bing_ai_citations": bing[day], "microsoft_verified_requests": ib[day]["microsoft_verified"]}
                 for day in sorted(ib) if day in bing]
    results["bing_vs_microsoft_visits"] = rows_bing

    out = os.path.join(HERE, "tables")
    os.makedirs(out, exist_ok=True)
    for name, table in [("claimed-identity-vs-cloudflare-verification.csv", rows_identity),
                        ("daily-ai-named-requests.csv", rows_daily),
                        ("secret-file-probe-targets.csv", rows_targets),
                        ("bing-citations-vs-microsoft-requests.csv", rows_bing)]:
        with open(os.path.join(out, name), "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(table[0].keys()))
            w.writeheader(); w.writerows(table)
    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)

    for site, s in results["sites"].items():
        print("\n==", site)
        print("week:", s["week"])
        print("verified requests by operator:", s["verified_by_operator"])
        print("verified requests that asked for a hidden file:",
              sum(v["verified_to_secret_paths"] for v in s["claimed_vs_verified"].values()))
        print("probes by disguise:", s["probes_by_disguise"])
        print("probe targets:", s["probe_targets"], "| via /@fs/:", s["probes_via_vite_fs"])
        print("probe status codes:", s["probe_status_codes"])
        print("8 Sept, unverified AI-named requests by hour (UTC):", s["wave_2026_09_08"]["impersonation_by_hour_utc"])
        print("unverified AI-named requests from NL, by day:", s["nl_unverified_ai_named_by_day"])
    print("\nBing citations vs Microsoft verified requests:", rows_bing)


if __name__ == "__main__":
    main()
