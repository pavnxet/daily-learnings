# Intelligence X (intelx.io) — OSINT search engine for leaks and historical web data

- **Site**: https://intelx.io/
- **Product / pricing**: https://intelx.io/product
- **Help docs**: https://help.intelx.io/get-started/
- **Related**: https://phonebook.cz
- **Logged**: 2026-10-10
- **Summary**: Freemium OSINT search engine over 200 billion+ records — breach dumps, stealer logs, pastes, darknet, and historical web copies — searched by **selector** (email, domain, IP, wallet), not by keyword.
- **Category**: OSINT / breach data search

## What it is

A search engine for leaked, archived and historical data, run by Intelligence X. It indexes more than **200 billion records** across paste sites (including historical ones), darknet (Tor and I2P), WikiLeaks and Cryptome, government sites of North Korea and Russia, data leaks, WHOIS, and a "Dumpster" bucket for everything else.

The important thing to understand is that **it does not do full-text search**. You cannot search "John Doe" or "American Airlines" — those return an error. You search by **selector**, and it supports an unusually wide set: email address, domain (with wildcards like `*.example.com`), URL, IP/CIDR (IPv4 and IPv6), phone number, Bitcoin and Ethereum addresses, MAC address, IPFS hash, credit card number, SSN, IBAN, and internal types like UUID and SimHash.

## Why it matters

Two features make it more than a breach-lookup site:

- **The Phonebook.** When you only have a domain, Phonebook expands it into the underlying email addresses, URLs and domains — the classic "I have a company, I need a person" step. It runs at `phonebook.cz` and is a paid-tier feature.
- **Historical copies.** Like a Wayback Machine for leaked and archived documents, you can go back in time on a site or document, which is what makes it useful for investigating content that has since been taken down.

It also handles the practical side: inline preview of archived HTML, PDFs and Word files (viewable without leaving the site, including darknet content), statistics filters by bucket/type/date, CSV/ZIP export, and email alerts.

**The Identity Portal** is the separate product for serious work — it lists every line where a search term appears rather than previewing whole files, exports leaked accounts as CSV with password-type/hash analysis, and adds reverse lookup and stealer-log export.

## How to use

1. **Sign up** at https://intelx.io/signup. Unregistered visitors get only a couple of searches a day and cannot see most data, so an account is the real starting point.
2. **Pick a strong selector.** Reconnaissance first. A domain, email, IP or crypto address works; a person's name does not.
3. **Use Phonebook** when you have a domain but not an address.
4. **Filter with the statistics panel** (top-left after searching) or the Advanced menu, rather than scrolling results.
5. **Automate or alert.** There is a documented [Search API](https://help.intelx.io/api/) — but note the licence terms below before building on it. Alerts arrive daily/weekly/monthly; monthly is recommended because newly indexed results are backdated.

### Tiers

| Tier | Selector searches | Phonebook | Notes |
|---|---|---|---|
| Public (not logged in) | 2 / day | — | Much data hidden |
| **Free (signed up)** | **50 / day** | — | No download, no export, no API access |
| Academia | 50 / day | 25 / day | For universities and schools |
| Free Trial (7 days) | 50 / day | — | 20 exports/day, download enabled; **downgrades to Free after 7 days** |
| Researcher | 200 / day | 25 / day | €2,500 / year |
| API | 500 / day | 100 / day | €7,000 / year |
| Identity Portal | 500 / day | 100 / day | €10,000 / year — the only tier with line-by-line results, reverse lookup, stealer-log export |
| Enterprise | 5000+ / day | 2500+ / day | €20,000 / year, multiple users |

*(Figures read from the vendor's product page on 2026-10-10 — verify before budgeting, as tiers change.)*

### Free-tier gotchas

- The **Free** tier has **no download and no export** — you can look, but getting results out is the paid feature. For most real workflows the free tier is a triage tool, not a data source.
- **Free trial does not grant API access.** The API tiers are separate licences entirely.
- A "license key" may be required; an account without one shows *"Invalid License Key"* on searches.

## Limits & risks

- **Legal and ethical exposure is real.** This indexes **breach data and stealer logs** — credentials and personal data of people who never consented. Querying is not the same as being entitled to the contents. Many jurisdictions restrict knowingly possessing or processing unlawfully obtained personal data, and "I found it in a search engine" is not a defence. Treat results as *indicators for verification*, and get legal advice before acting on leaked credentials — including before *testing* a leaked password, which can itself be unauthorised access.
- **Do not test credentials you find.** Logging into an account with a leaked password is typically a crime, regardless of how you got the password.
- **The API is fair-use and licence-restricted.** The product page defines fair use as *"the user shall not engage in usage of the API that goes against our Terms of Service such as mass scraping"*, and states explicitly that **only API, Identity Portal and Enterprise licences grant the right to integrate the API into third-party products**. The Researcher and Free tiers do not. Building a product on the free tier's API is a licence breach.
- **Free tier cannot export, so it cannot be automated meaningfully** — that is by design, not an oversight.
- **Data can be stale, duplicated or misattributed.** Breach dumps are messy: records are backdated on indexing, entries repeat across buckets, and a match on an email does not prove the person used the service or that the data is current. The vendor itself recommends monthly alert cycles precisely because indexing lags.
- **Searching a person's email or domain is a privacy-sensitive act.** Depending on your role and jurisdiction this may require a lawful basis — it is not automatically fine because the tool is public.
- **Free tier is browse-only and small.** 50 selectors/day sounds generous until you realise no export means hand-copying; plan around that rather than being surprised.

## Verdict

**The strongest free-tier OSINT starting point for selector-based investigation, with a hard ceiling at "look but don't take".**

**Use it for**: verifying whether an email or domain appears in known breaches, expanding a domain into email addresses via Phonebook, checking your own exposure, finding historical copies of removed content, and academic/security research where you understand the legal basis.

**Do not use it for**: harvesting credentials, testing found passwords, bulk-collecting personal data, or building any product on the free/Researcher API — those are unlawful or licence-breaching respectively.

**The honest framing**: the free tier is a genuine research tool for *looking up specific selectors*, and the moment you need volume or export you are into €2,500/year territory. Budget or downgrade your expectations accordingly.

## Sources

- [Intelligence X](https://intelx.io/) — https://intelx.io/
- [Intelligence X — Product tiers and pricing](https://intelx.io/product) — https://intelx.io/product
- [Intelligence X — Get started](https://help.intelx.io/get-started/) — https://help.intelx.io/get-started/
- [Intelligence X — API limits](https://help.intelx.io/api/limits/) — https://help.intelx.io/api/limits/
- [Intelligence X — Selectors](https://help.intelx.io/get-started/selector/) — https://help.intelx.io/get-started/selector/
- [Phonebook](https://phonebook.cz) — https://phonebook.cz

*Verification note: the tool and pricing pages were fetched directly from the vendor on 2026-10-10 and the tier figures above are transcribed from their comparison table, so they are vendor-published facts rather than marketing claims. No account was created and no search was run, so behaviour on the free tier (rate limiting, what data is visible) is described from the vendor's own documentation, not from testing.*
