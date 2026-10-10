# lucky-cat-api + radio-house-api — free AI backend via OpenAI-compatible bridges

- **Sites**: [lucky-cat-api](https://github.com/khrotu/lucky-cat-api) · [radio-house-api](https://github.com/khrotu/radio-house-api)
- **Owner**: KHROTU (own repos)
- **Logged**: 2026-10-10
- **Summary**: Two local FastAPI bridges that wrap free AI chat sites (Proton Lumo, TryingOpen) into one OpenAI-compatible endpoint — point any AI client at `localhost` and use current frontier models for free.
- **Category**: AI API bridge / OpenAI-compatible proxy

## What it is

Two standalone Python servers that each present a **free upstream AI chat site as an OpenAI-compatible REST API**, so any tool that speaks the OpenAI protocol can use it with a `baseURL` change and no API key.

| Repo | Free upstream it wraps | Default port |
|---|---|---|
| `lucky-cat-api` | Proton Lumo guest sessions (`lumo.proton.me`) | 8000 |
| `radio-house-api` | TryingOpen (`tryingopen.com`, by Offline Base) | 8002 |

Both are FastAPI/Uvicorn apps with the same shape and the same endpoint surface, so one client config can point at either — and the two ports run side by side, giving a combined pool of ~24 models.

## Why it matters

This is the practical answer to "how do I get an AI backend for free". Both are **drop-in OpenAI replacements** rather than toys: they implement streaming SSE, `tools` / `tool_choice`, and `reasoning_effort`, which is the hard part of bridging a chat website. Because they speak the standard protocol, they work with existing clients with no wrapper code:

- **OpenCode** — via `@ai-sdk/openai-compatible`, `baseURL: http://127.0.0.1:8002/v1` (documented and working in this setup).
- Anything else accepting a custom OpenAI `baseURL` — LangChain, the `openai` SDK, Continue, Cline, LibreChat, and so on.

The mechanisms differ, and both are worth understanding:

- **`lucky-cat-api` harvests anonymous guest credentials.** `lc_credentials.py` drives headless Edge/Chrome through Selenium to load the Lumo guest page, waits for an `AUTH-*` cookie, and stores the full cookie header. It auto-downloads the matching `msedgedriver` if missing, keeps up to 8 credentials, and the router rotates them and marks one depleted when its rate limit is hit. Upstream is `https://lumo.proton.me/api/ai/v1/chat/completions` with an app-version header (`web-lumo@2.0.2.9`).
- **`radio-house-api` reverse-engineers a Next.js app.** It scrapes model metadata out of the site's JS chunks (`/_next/static/chunks/`) with regexes for id/name/context/price, then calls the site's private endpoints. It manages route cooldowns and failure counts, and **emulates tool calls** for upstreams that do not support them.

## How to use

### 1. Run a bridge

```powershell
cd lucky-cat-api          # or radio-house-api
pip install -r requirements.txt
python lc_server.py       # radio-house-api: python rh_server.py
```

Or explicitly: `uvicorn lc_server:app --host 127.0.0.1 --port 8000` (radio-house-api uses port **8002**).

### 2. Confirm it is alive

`GET /health` returns liveness **plus live credential-pool stats** — check this first, since an empty pool is the usual cause of failures.

### 3. Point a client at it

```python
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="not-needed")
resp = client.chat.completions.create(
    model="glm-5.3",
    messages=[{"role": "user", "content": "hello"}],
    stream=True,
)
for chunk in resp:
    print(chunk.choices[0].delta.content or "", end="")
```

### Endpoints (identical on both)

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/v1/chat/completions` | Chat completions; `stream: true` for SSE. Supports `tools`, `tool_choice`, `reasoning_effort` |
| `GET` | `/v1/models` | List models |
| `GET` | `/v1/models/{id}` | Retrieve one model |
| `GET` | `/health` | Liveness + credential-pool stats |
| `POST` | `/admin/reload` | Reload `credentials.json` from disk without a restart |

`/chat/completions` and `/api/v1/chat/completions` are accepted as aliases of `/v1/chat/completions`, which covers clients that hardcode a different path.

### Models

**lucky-cat-api** (context reported as 130k in the README; `lc_router.py` declares 128000):

| ID | Upstream model | Aliases |
|---|---|---|
| `qwen3.5-122b-a10b` | `lumo-lite` | `qwen3.5`, `qwen` |
| `glm-5.3` | `lumo-max` | `glm5.3` |
| `apertus-1.5` | `apertus-15` | `apertus` |

**radio-house-api** — 21 models, including `claude-sonnet-5` (977k), `gpt-5.6-terra` (1025k), `deepseek-v4-flash-0731` / `deepseek-v4-pro-0813` / `deepseek-v4.1-flash` (1M), `kimi-k3` (1M), `glm-5.3` / `glm-5.3-flash` (1M), `mimo-v2.6-flash` / `mimo-v2.6-pro` (1M), `qwen3.8-2.4t-a95b` (1M), `qwen3.8-flash` (1M), `nemotron-3-ultra-550b-a55b` (262k), `qwen3.8-27b`, `gemma-4-26b-a4b-it`, `gemma-4-31b-it`, `gpt-oss-120b`, `inkling` / `inkling-small`, `muse-glimmer-30b`, `ling-3.0-flash-vl`, `nemotron-3.5-lightning`. The README warns the list is not finalised.

*(These model lists, the context windows, and the rate limits quoted below are read from the repos' own READMEs and source, not independently tested. Context windows in particular are copied from the upstream sites and do not all match the code — lucky-cat-api's README says 130k while `lc_router.py` declares 128000. Verify against `/v1/models` on a running server before relying on any of them.)*

## Limits & risks

This section matters more than the rest, because the "free" part is not the stable part.

- **The upstream terms of service prohibit exactly this.** TryingOpen's terms (effective 2026-10-03) state you must not *"get around the service's limits, for example with automated requests, scraping, or rotating addresses to avoid rate limits"* — and its service description explicitly promises *"free, with no account"* for humans. **`radio-house-api` is, by construction, automated requests plus credential rotation** (`ROUTE_COOLDOWN_S`, failure-based route suspension, a credential pool). The terms add: *"We may block access from anyone who does [this], without notice."* So expect breakage by design, not by accident. `lucky-cat-api` takes the same approach to Proton Lumo's anonymous guest tier, and Proton sells Lumo plans where guest mode is the free limited tier.
- **No auth on your own server.** `/health` exposes credential-pool stats and `/admin/reload` reloads credentials — neither is protected. Safe bound to `127.0.0.1`, **dangerous if you expose it** (LAN, port-forward, tunnel, container on `0.0.0.0`): anyone reaching it gets a free model backend and your pool stats. Keep it on loopback.
- **`credentials.json` is plaintext session cookies.** Treat it as a secret. It is gitignored in both repos — keep it that way, and remember a leaked `AUTH-*` cookie is an impersonatable session.
- **Undocumented private endpoints.** Both call APIs the sites never published (Lumo's `/api/ai/v1/...`, TryingOpen's internal routes). They can change or vanish with any deploy, and the browser automation can break whenever the driver or site markup changes. The Selenium path also launches a browser with `--ignore-certificate-errors` and `--disable-web-security`.
- **Hard upstream size limits.** `radio-house-api` had to enforce `PROMPT_CHAR_CAP = 18000` and compact tool schemas (`max_spec_len=3000`) because TryingOpen returns **HTTP 413 above ~22,000 characters**. lucky-cat-api reportedly handles 500,000+ characters via `lumo-max`.
- **Some models are heavily throttled or degraded.** `claude-sonnet-5` and `gpt-5.6-terra` are limited to roughly **5 requests per 30–40 minutes** and support **only emulated tool calls** — emulated tool calls are prompt-level impersonation, not real function calling, so reliability differs from a native tool-use API.
- **Not for anything that matters.** No SLA, no uptime guarantee, no data-handling guarantee, and free-tier models change without notice. Using this for production, commercial, or user-facing traffic is not defensible; using it to experiment locally is what it is for.
- **Copyright/licence of the model weights is a separate matter** from the site's terms, and TryingOpen's terms explicitly require you to comply with *"the terms or usage policies of the companies that serve the models"*.

## Verdict

**Genuinely useful as a free, local, OpenAI-compatible AI backend — with a clear and honest ceiling.**

The engineering is the valuable part: both repos solve the genuinely fiddly problems (SSE streaming, tool-call translation, credential rotation, OpenAI-compatible surface) so that a client makes one config change instead of being rewritten. Together they expose ~24 current models on two localhost ports, and `radio-house-api` in particular offers 1M-context frontier models through nothing but a `baseURL` swap.

**Use it for**: local experimentation, prototyping an AI feature before paying for an API, personal tooling, and learning how OpenAI-compatible bridging works.

**Do not use it for**: anything production, commercial, user-facing, or dependent on staying up. The upstream sites' terms forbid automated access and rate-limit circumvention, and TryingOpen reserves the right to block without notice. Treat the upstream as something that will break, never as a free tier you are entitled to.

**The honest framing**: this is not "free AI" — it is a free *client-side bridge* to free-tier upstream services that do not permit automated access. The cost is that the dependency can be blocked at any time, so build nothing you would be upset to lose.

## Sources

- [lucky-cat-api on GitHub](https://github.com/khrotu/lucky-cat-api) — https://github.com/khrotu/lucky-cat-api
- [radio-house-api on GitHub](https://github.com/khrotu/radio-house-api) — https://github.com/khrotu/radio-house-api
- [TryingOpen — Try any open model](https://www.tryingopen.com/) — https://www.tryingopen.com/
- [TryingOpen Terms of Service (effective 2026-10-03)](https://www.tryingopen.com/terms) — https://www.tryingopen.com/terms
- [Proton Lumo — guest mode](https://lumo.proton.me/guest/) — https://lumo.proton.me/guest/
- [Proton Lumo pricing (Free vs Plus)](https://proton.me/lumo/pricing) — https://proton.me/lumo/pricing
- Local source read for verification: `lc_router.py`, `lc_credentials.py`, `rh_router.py`, `rh_models.py`, `rh_credentials.py`, `README.md`, `requirements.txt` in both repos.

*Verification note: at the time of writing, neither server was running (`/health` refused connection on ports 8000 and 8002), so every claim above comes from reading the source and the upstream sites rather than from a live request. The behaviours attributing limits (credential rotation, the 18,000-char cap, emulated tool calls) are read from the code and repo READMEs.*
