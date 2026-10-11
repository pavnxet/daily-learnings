# WhatsMyName — username enumeration dataset (and whatsmyname.app)

- **Web tool**: https://whatsmyname.app/
- **Dataset repo**: https://github.com/WebBreacher/WhatsMyName
- **Raw data**: https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json
- **Creator**: Micah "WebBreacher" Hoffman (2015); web UI by Chris Poulter
- **Logged**: 2026-10-10
- **Summary**: A community-maintained JSON dataset of 700+ sites that answers "does this username exist?" — the data behind most username-checker tools, and the reason their false positives are low.
- **Category**: OSINT / digital footprint

## What it is

WhatsMyName (WMN) is **a dataset, not an application.** It is a single JSON file — `wmn-data.json` — where each entry describes how to check one website for a username: what URL to request, and what a hit versus a miss looks like. Tools read the file and do the actual checking.

That split is the whole design. Anyone can write a checker; the data stays accurate independently of which tool you use. Started in 2015 as a fix for the creator's frustration that existing username checkers were full of **false positives**, it has grown into one of the most widely used username-enumeration datasets in OSINT.

The web interface at [whatsmyname.app](https://whatsmyname.app/) (built by Chris Poulter, OSINT Combine) runs the dataset in the browser: filter by category, export to CSV, always pulls the latest data.

A site only qualifies for inclusion if it:

1. Is **publicly accessible** — paywalls and login walls can't be checked
2. **Contains the username in the URL** — the profile URL must include it directly
3. **Does not transform the username** — sites mapping usernames to numeric IDs won't work

## Why it matters

One username, run once, tells you which of hundreds of services a person uses. That is the single highest-yield move in a digital-footprint investigation, because a reused handle is the strongest and cheapest link between separate accounts.

It is also worth knowing *because it is infrastructure*. Judging by the consumer tools that embed it — Blackbird, SpiderFoot's `sfp_account` module, Maltego transforms, Sherlock-style checkers — WMN is closer to the data layer of this corner of OSINT than a tool you use directly.

## How to use

### Web (no install)

Open https://whatsmyname.app/, enter a username, filter by category, export CSV.

### Command line

The bundled checker scripts were **removed in May 2023** — the project maintains data only. Use a third-party checker against the JSON:

| Tool | Type | Notes |
|---|---|---|
| [Naminter](https://github.com/3xp0rt/Naminter) | Python | Built specifically for this dataset; Cloudflare bypass, browser impersonation, concurrent checking |
| [Blackbird](https://github.com/p1ngul1n0/blackbird) | Python | Fast username/email search |
| [WhatsMyName-Python](https://github.com/C3n7ral051nt4g3ncy/WhatsMyName-Python) | Python | Simple script |
| [Reveal My Name](https://github.com/yooper/reveal-my-name) | Python | The original bundled checker, maintained separately |
| [sn0int](https://github.com/kpcyrd/sn0int) | Rust | Uses WMN in the `kpcyrd/whatsmyname` module |
| [NameSeeker](https://github.com/funnyzak/name-seeker) | Electron | Desktop app; exports PDF, CSV, JSON |
| [SpiderFoot](https://github.com/smicallef/spiderfoot) | Python | `sfp_account` module |

### Roll your own

Because it is just JSON with `url` and `response codes` per site, a minimal checker is a loop over `sites`:

```python
import json, requests

data = json.load(open("wmn-data.json", encoding="utf-8"))
username = "target"

for site in data["sites"]:
    url = site["uri_check"].format(account=username)
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        found = r.status_code == site["e_code"] and site["e_string"] in r.text
        if found:
            print(f"FOUND  {site['name']}: {site['uri_pretty'].format(account=username)}")
    except requests.RequestException:
        pass  # a network error is not a "not found"
```

**Keep the error path distinct from the miss path.** The single most common bug in home-made checkers is treating a timeout, a 403 or a Cloudflare challenge as "user does not exist" — which silently produces the false negatives the dataset exists to prevent.

## Limits & risks

- **Cloudflare and bot protection break checkers constantly.** Many target sites challenge automated requests. That is why Naminter advertises Cloudflare bypass and browser impersonation — without them, results are wrong rather than missing. **A 403 is not a negative result.**
- **False positives and negatives still happen.** The dataset encodes expected status code *and* an expected string per site. Sites change their markup, response codes and URL shapes continuously, which is why the project actively asks for contributions to repair broken detections. Verify hits manually before relying on them.
- **The dataset is inaccurate by decay, not by design.** Any given detection has a shelf life. Pull the JSON fresh rather than vendoring an old copy — the web tool always fetches the latest.
- **Sites that transform usernames are excluded**, so absence of a hit proves nothing about those platforms.
- **`whatsmyname.app` blocks automated fetching.** Fetching it returned **HTTP 403** during research on 2026-10-10, so do not build a pipeline against the web UI — use the JSON or a CLI checker. The JSON is the supported integration point.
- **This is personal-data processing.** Enumerating a real person's accounts across hundreds of services is surveillance-adjacent even when every individual request is to a public page. Depending on your role, jurisdiction and purpose you may need a lawful basis, and many sites' terms prohibit automated querying regardless of the data being public.
- **Do not use it to harass, stalk, or compile dossiers on people who have not consented.** The tool cannot tell you the difference; you have to.
- **Licence is CC BY-SA 4.0** — attribution required, and derivatives must carry the same licence. If you ship a tool embedding `wmn-data.json`, honour that.

## Verdict

**The reference dataset for username enumeration, and still the best starting point for digital-footprint work — as long as you respect that it is data with a shelf life.**

**Use it for**: finding which services a handle is registered on, checking your own footprint, feeding an existing OSINT tool, and building a checker without having to first solve per-site detection rules.

**Do not use it for**: automated scraping of the web UI (it 403s), treating a lone negative as proof of absence, or compiling profiles of people without a lawful basis.

**The honest framing**: its value is curation, not cleverness. The idea is trivial and the maintenance is the product — which is exactly why the false-positive rate is the selling point and why a stale copy of the file is worse than useless.

## Sources

- [WhatsMyName on GitHub](https://github.com/WebBreacher/WhatsMyName) — https://github.com/WebBreacher/WhatsMyName
- [WhatsMyName README (raw)](https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/README.md) — https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/README.md
- **[whatsmyname.app](https://whatsmyname.app/)** — https://whatsmyname.app/ *(returned HTTP 403 to automated fetching)*
- [Bellingcat's Online Investigation Toolkit — WhatsMyName](https://bellingcat.gitbook.io/toolkit/more/all-tools/whats-my-name) — https://bellingcat.gitbook.io/toolkit/more/all-tools/whats-my-name
- [Naminter](https://github.com/3xp0rt/Naminter) — https://github.com/3xp0rt/Naminter
- [Blackbird](https://github.com/p1ngul1n0/blackbird) — https://github.com/p1ngul1n0/blackbird
- [Reveal My Name](https://github.com/yooper/reveal-my-name) — https://github.com/yooper/reveal-my-name
- [SpiderFoot](https://github.com/smicallef/spiderfoot) — https://github.com/smicallef/spiderfoot

*Verification note: the dataset README and licence were fetched from the repo, and `whatsmyname.app` genuinely returned HTTP 403 to automated access (confirmed, not assumed) — recorded above as a real limitation. The requester-count claim "700+ sites" comes from the repo's own description; the live count is in `wmn-data.json` (`$.sites.length`) and is worth reading directly rather than trusting the badge. No username search was run.*
