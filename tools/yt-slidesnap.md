# yt-slidesnap — turn a lecture video into a PDF of its slides

- **Site**: https://github.com/pavnxet/yt-slidesnap
- **Logged**: 2026-10-10
- **Category**: video tooling / study automation

## What it is

A Python CLI (and a small local web UI) that takes a video URL plus the timestamps where slides appear, and returns **a clean PDF with one slide per page**. It does not download the video — it resolves the stream and extracts only the frames it needs.

Built for a specific tedious case: a 2.5-hour recorded class with 40 questions in it, where you want the question slides as a document instead of scrubbing a timeline by hand. Output is captioned (`[Q22 at 1:34:21]`) and the tool prints exactly how it interpreted your timestamps, so a misread shows up in the log rather than silently in the PDF.

## Why it matters

The interesting part is not the PDF — it is **how the frames come out clean without any ML**.

Naively grabbing a frame at a timestamp usually catches the presenter standing in front of the slide. The fix here is a statistical trick that costs nothing:

- Each slide window is sampled **8 times** by one ffmpeg pass.
- The 8 frames are stacked and a **per-pixel median** is computed.
- The slide is static; the presenter is not. So the median **is the slide with the presenter erased**.
- The candidate closest to that median (lowest mean absolute deviation) is the frame where they cover it least.

No machine learning, no face detection — just `numpy.median` over the stack. That is the whole idea, and it is a genuinely reusable pattern for any "remove the moving thing from a static background" problem.

Two other design decisions are worth stealing:

- **Sampling is bounded by the *earliest* later timestamp**, not the next row. `min(later)` in the parser means the window can never extend past the answer's appearance, so an answer cannot leak into the PDF and the window cannot drift across the next question. A negative constraint enforced by the arithmetic rather than by hope.
- **Every candidate frame is kept**, so re-picking costs nothing — `--override Q22=5` pins a specific candidate without re-running extraction.

## How to use

### Install

```bash
pipx install git+https://github.com/pavnxet/yt-slidesnap   # gives the yt-slidesnap command
# or
pip install git+https://github.com/pavnxet/yt-slidesnap
```

From a clone instead: `pip install -r requirements.txt`, then run `python slidesnap.py ...` — **the `yt-slidesnap` command does not exist on that path** unless you also run `pip install -e .`. The README calls this the single most common trip-up.

You do **not** need ffmpeg installed. A full build ships inside `imageio-ffmpeg` and the tool always uses that one (`FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()`). `yt-dlp` resolves the stream.

### Run it

Timestamps can be pasted almost however you already have them:

```
Q22: Question 01:34:21 | Answer 01:34:53 (C)
Q23: Question 01:38:45 | Answer 01:39:16 (D)
```

Markdown tables work too, including several later timestamps per row. Then:

```bash
yt-slidesnap run "<video-url>" --file timestamps.txt
yt-slidesnap run "<video-url>" --text "Q22: Question 01:34:21 | Answer 01:34:53 (C)"
cat timestamps.txt | yt-slidesnap run "<video-url>"
```

**Check before spending a run:**

```bash
yt-slidesnap run "<url>" --file timestamps.txt --dry-run
```

This prints the parsed windows (`Q19  1:41:04 -> 1:41:27  23s`) and exits without extracting. Every real extraction also prints the window it understood.

### Web UI

```bash
yt-slidesnap serve      # opens http://127.0.0.1:8765
```

Paste URL + timestamps, click Extract, watch progress, then get a PDF link and a contact-sheet preview. Binds to `127.0.0.1` by default; one run at a time (a second click is rejected with 409, not queued).

### Flags worth knowing

| Flag | Default | Use |
|---|---|---|
| `--frames N` | `8` | candidates per slide — raise it if picks look dirty |
| `--override ID=N` | — | pin candidate N for one slide, repeatable |
| `--workers N` | `4` | concurrent slide extraction |
| `--dry-run` | off | show parsed timestamps, extract nothing |
| `--no-label` / `--no-watermark` | off | drop the caption / footer strip |
| `--client NAME` | `android` | yt-dlp `player_client` for YouTube |

### Output

```
slidesnap-out/<video-id>/
├── Q22-Q37.pdf        one captioned slide per page
├── auto_picked.png    contact sheet of every pick — eyeball this first
├── frames/Q22.png     the chosen slides
└── candidates/        all 8 candidates per slide, for re-picking
```

## Limits & risks

- **YouTube output is capped at 640×360, and that is a hard constraint, not a bug.** The README and a code comment both note that YouTube's `android` client is the only one that hands ffmpeg a URL it can actually fetch, and that client caps at 360p. Going higher needs a JS runtime for yt-dlp's `nsig` handling, and that client's URL may still return **HTTP 403** (the stream URL is locked to the client that requested it). The tool upscales 2× when writing the PDF. Fine for slide text; not fine for a diagram with small labels.
- **It downloads frames of someone else's video.** The README says this plainly: fine for study notes and fair-use quotation, not fine for republishing a lecture. The output folder is gitignored by default — keep it that way, and check the platform's terms and the rights holder before sharing. This is the main thing to get right; the tool cannot enforce it for you.
- **Age-restricted or members-only videos need cookies** exported and passed to yt-dlp, or stream resolution fails outright (`could not resolve a stream URL`).
- **One frame per timestamp.** If a slide is built up with animation, you get whatever is on screen at that instant — there is no "find the completed slide" logic.
- **The median trick fails if the slide itself changes inside the window.** Then the median is a blend of two slides and *every* candidate scores badly. This is detectable rather than silent: the `error X vs worst Y` output shows it — if `X` is close to `Y`, every candidate was dirty and you should raise `--frames`. Blindly trusting a low-confidence pick is the realistic failure mode.
- **Only YouTube is tested end to end**, though it works with anything `yt-dlp` supports.
- **The web UI has no authentication.** It serves the current run's output folder and nothing else, is single-user by design, and binds to loopback. Do not expose it to a network you do not trust — `--host 0.0.0.0` on a shared network hands out your extracted frames. The 409-on-second-click means no queuing, so it is not built for multiple users.
- **The speed figure is a self-reported claim.** "16 slides in ~25 seconds" comes from the project's own README and was not independently measured here. Treat it as an indication, not a benchmark.

## Verdict

**Small, sharply-scoped, and unusually well-argued for a utility — the kind of tool where the README explains *why* it works rather than just what to type.**

**Use it for**: turning recorded lectures or webinars into a slide document you can search and annotate, pulling the question slides out of an exam-review recording, and as a reference implementation of the median trick for removing a moving person from a static scene.

**Do not use it for**: republishing someone else's lecture, anything needing better than 360p detail, or animated builds where you need the completed state of a slide.

**The honest framing**: the value is in two decisions, not the code volume — the per-pixel median (clean frames with no ML) and the earliest-ceiling window rule (answers structurally cannot leak). Both are the kind of thing that is obvious in hindsight and easy to get wrong, and the tool's own logging (`error X vs worst Y`, the printed window) is what makes the wrong cases visible instead of silent.

## Sources

- [yt-slidesnap on GitHub](https://github.com/pavnxet/yt-slidesnap) — https://github.com/pavnxet/yt-slidesnap
- [README](https://github.com/pavnxet/yt-slidesnap/blob/main/README.md) — https://github.com/pavnxet/yt-slidesnap/blob/main/README.md
- [slidesnap.py source](https://github.com/pavnxet/yt-slidesnap/blob/main/slidesnap.py) — https://github.com/pavnxet/yt-slidesnap/blob/main/slidesnap.py
- [examples/timestamps.txt](https://github.com/pavnxet/yt-slidesnap/blob/main/examples/timestamps.txt) — https://github.com/pavnxet/yt-slidesnap/blob/main/examples/timestamps.txt
- [imageio-ffmpeg (bundled ffmpeg build)](https://pypi.org/project/imageio-ffmpeg/) — https://pypi.org/project/imageio-ffmpeg/
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — https://github.com/yt-dlp/yt-dlp

*Verification note: the README, `slidesnap.py` and the examples file were read from the repository. The mechanism claims were checked against the source rather than taken from the README: `autopick()` stacks the candidate frames and returns `argmin` of the mean absolute deviation from `np.median(stack, axis=0)`; `extract_window()` samples with ffmpeg's `-vf fps=k/span`; and the parser sets the window end to `min(later)` — the earliest later timestamp — confirming that an answer cannot be reached. No run was performed, so output quality, the ~25-second figure and PDF layout are unverified.*
