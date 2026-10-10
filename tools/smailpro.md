# SmailPro — temporary Gmail & Outlook inboxes

- **Site**: https://smailpro.com/temporary-email
- **API docs (overview)**: https://smailpro.com/api
- **Full API reference**: https://sonjj.com/docs/?brand=smailpro.com
- **Owner**: SONJJ / Sonjj ecosystem
- **Logged**: 2026-10-10
- **Summary**: Disposable inboxes on **real Gmail and Outlook addresses**, which clears the domain blocklists that silently kill ordinary temp-mail verification.
- **Category**: temporary email / signup verification

## What it is

A disposable-email service that hands out **real Gmail and Outlook addresses** instead of addresses on throwaway domains. It is part of the SONJJ product family (which also includes YChecker, UGener, SMSer, StoreGmail, CardGener) sharing one credit wallet.

## Why it matters

The usual reason a "temp mail" address fails on a signup form is a **domain blocklist**. Temp-mail.com, Guerrilla Mail and Maildrop issue addresses on generic disposable domains, and signup forms blocklist those domains — so the verification mail is dropped before it is even sent. The failure is silent: no error, no bounce, just a form that never verifies. *(The examples of which platforms do this — Salesforce and HubSpot — come from the vendor's own page: (vendor claim — unverified).)*

Because SmailPro issues `@gmail.com` and `@outlook.com` addresses, it clears domain-based blocklists that kill ordinary temp mail. That is the entire value proposition, and it is a real mechanism. *(The pool size and acceptance rates the vendor quotes are (vendor claim — unverified); see Limits & risks.)*

## How to use

### Free path (browser, manual)

1. Open https://smailpro.com/temporary-email
2. Create an inbox — pick the provider (Gmail / Outlook / other).
3. The page gives you the address; keep the tab open.
4. Paste the address into the signup form, then read the code from the SmailPro inbox.

The Cloudflare Turnstile challenge is solved by you in the browser. There is also a Chrome/Firefox/Edge extension and an Android app.

### Automation path (API)

Auth is a single `X-Api-Key` header (key from the my.sonjj.com dashboard). No OAuth, no SDK, no session cookie.

Three calls:

| Step | Call |
|---|---|
| 1 | **Create** an inbox → returns a Gmail or Outlook address |
| 2 | **Poll** the inbox for new messages (IMAP-synced every 5–10s) |
| 3 | **Read** a message → full body, or extract the OTP directly |

The API is **receive-only by design** — it cannot send mail. Cost per call: create 1 credit, poll 0.05 credits, read 1–2 credits. Base rate $1.00 / 1,000 credits, down to $0.30 / 1,000 at scale (vendor claim — unverified); credits never expire and are only charged on an HTTP 200 (vendor claim — unverified).

### Python wrapper (unofficial)

`pip install smailpro-api` — community wrapper by AsmSafone ([PyPI](https://pypi.org/project/smailpro-api/), [GitHub](https://github.com/AsmSafone/smailpro-api)).

```python
from smailpro_api import SmailProAPI, Provider

api = SmailProAPI(provider=Provider.GOOGLE, solver_url="http://localhost:8000")
email_info = api.create_email()
inbox = api.fetch_inbox(email_info)          # after a short sleep
msg = api.fetch_message(email_info, inbox["messages"][0]["mid"])
```

**Caveat**: the wrapper's headline feature is "automated CAPTCHA bypass", but it does no bypassing itself — it **requires** an external Cloudflare Turnstile solver service (it recommends Boterdrop-Solver) running at `solver_url`. So it is not a pure-Python install; budget for a Dockerized solver.

Providers the wrapper exposes:

| Provider | Default domain | Other domains |
|---|---|---|
| `google` | gmail.com | googlemail.com |
| `microsoft` | outlook.com | hotmail.com, outlook.kr, outlook.fr, outlook.com.vn, outlook.co.id, outlook.co.th, outlook.com.ar, outlook.co.il |
| `other` | melbourne.edu.pl | sydney.edu.pl, tokyo.edu.pl, storegmail.net |

## Limits & risks

- **These inboxes are not private.** A "temporary Gmail" is a credential for a mailbox the vendor created and can also access. Never use it where the mail contains anything sensitive or where account recovery matters — the address is shared infrastructure and could be reassigned.
- **Vendor metrics are marketing.** ~14,000 accounts in rotation (~3,000 Gmail + ~11,000 Outlook), "400,000+ messages received", "sub-10 second OTP delivery", "high observed acceptance" — all from SmailPro's own page (vendor claim — unverified), self-described as *operational metrics, not hard guarantees*. No independent verification. Treat acceptance as unknown until you test it on your actual target form.
- **Receive-only.** No sending, no attachments. It cannot be used for outbound mail or to test attachment handling.
- **Acceptance is still not guaranteed.** Real Gmail/Outlook clears *domain* blocklists, but forms also use behavioral checks, phone verification, IP reputation and risk scoring. A provider-domain address does not defeat those.
- **Terms-of-service risk.** Many platforms prohibit disposable addresses for account creation. Using this to mass-create or verify accounts is a ToS violation and, depending on the service and intent, potentially fraud. This is documented here for legitimately permitted uses: QA/testing of your own signup flows, and one-off signups where the platform allows it.
- **Paid and metered.** The free browser flow is rate-limited ("Limit /" on the tool page); anything programmatic costs credits and needs an account on a second domain (`my.sonjj.com`).
- **The docs live off-site.** The `/api` page on smailpro.com deliberately contains no endpoints or code samples — the real reference is on `sonjj.com`, a different domain. Documentation, pricing and pool status can change there without notice on the page you bookmarked.

## Verdict

**Genuinely useful, but for one specific job**: getting a verification mail through a form that rejects disposable domains, in cases where you are allowed to do so. The real-Gmail/Outlook mechanism is the differentiator and it solves a real, otherwise-confusing failure (silently dropped verification mail).

**Not** a privacy tool, not an anonymity tool, and not a production email provider. For automation, budget for a paid credit balance plus a separate CAPTCHA solver; if you only need an occasional code, the free browser flow is the cheaper path.

## Sources

- [SmailPro temporary email tool](https://smailpro.com/temporary-email) — https://smailpro.com/temporary-email
- [SmailPro API overview](https://smailpro.com/api) — https://smailpro.com/api
- [smailpro-api on PyPI](https://pypi.org/project/smailpro-api/) — https://pypi.org/project/smailpro-api/
- [smailpro-api on GitHub](https://github.com/AsmSafone/smailpro-api) — https://github.com/AsmSafone/smailpro-api
- [Temp Mail by SmailPro — Chrome Web Store](https://chromewebstore.google.com/detail/temp-mail-by-smailpro/hpjiofbbhffhfeiioadkedhalpijppnk) — https://chromewebstore.google.com/detail/temp-mail-by-smailpro/hpjiofbbhffhfeiioadkedhalpijppnk
