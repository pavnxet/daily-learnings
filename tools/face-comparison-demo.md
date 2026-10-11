# Face Detection & Comparison (CodeSandbox demo) — compare two uploaded faces

- **Demo**: https://6mzld2.csb.app/
- **Host**: CodeSandbox (`.csb.app` preview URL)
- **Logged**: 2026-10-10
- **Summary**: A browser-only demo that takes two uploaded photos and reports whether they show the same person — face detection plus descriptor comparison, with no server round-trip.
- **Category**: computer vision / face matching

## What it is

A single-page demo, hosted on CodeSandbox, whose job is narrow: you upload two images, it detects the face in each and compares them, telling you whether they are the same person.

The URL is a CodeSandbox preview (`6mzld2.csb.app`) — an ephemeral sandbox hostname, not a product with a domain, docs, or a support channel.

## Why it matters

**Because the technique is what you actually want to learn here, not the app.** Face comparison in the browser is a solved, small problem, and every implementation follows the same four steps:

1. **Detect** the face and its landmarks in each image (bounding box + feature points).
2. **Align and normalise** — crops, resizes and squares the face so pose and scale do not dominate.
3. **Embed** — run the crop through a neural network to get a face descriptor: a fixed-length vector (commonly 128 numbers) representing that face.
4. **Compare** descriptors with a distance metric, typically Euclidean distance, and threshold it.

The threshold is the entire decision. In the widely used `face-api.js` implementation the accepted convention is **distance < 0.6 means a match**, and 0.4–0.5 is a confident one. A distance near 0.6 is a coin-flip, not an answer — which is exactly the failure mode people misunderstand when they treat this class of demo as a verdict.

That matters because the same four steps power passport e-gates, phone unlock, and photo-app "is this the same person" grouping. Once you have seen the pipeline in a 30-line demo, the big systems stop being magic and become threshold tuning plus a much larger, curated model.

## How to use

1. Open https://6mzld2.csb.app/
2. Upload two photos — one face per image works best, front-on, decent lighting.
3. It reports a comparison result, typically a similarity/distance figure with a match verdict.
4. Read the **distance**, not the verdict. If the tool prints a number, judge it yourself against the 0.6 convention rather than trusting a label.

### If you want to build it yourself

The canonical route is `face-api.js` (TensorFlow.js under the hood), which runs entirely client-side:

```js
// after faceapi.loadSsdMobilenetv1Model(...) and loadFaceLandmarkModel(...)
const a = await faceapi
  .detectSingleFace(imgA).withFaceLandmarks().withFaceDescriptor();
const b = await faceapi
  .detectSingleFace(imgB).withFaceLandmarks().withFaceDescriptor();

// < 0.6 is the usual match threshold; 0.4-0.5 is confident
const distance = faceapi.euclideanDistance(a.descriptor, b.descriptor);
console.log(distance, distance < 0.6 ? "likely same person" : "different");
```

Alternatives: **MediaPipe** (faster, lighter, better mobile support) or **InsightFace / ArcFace** models (much more accurate, but usually server-side and heavier).

## Limits & risks

- **I could not verify this specific demo.** Fetching the URL returned an **HTTP 400 CodeSandbox trust gate** — an interstitial asking *"You are opening a CodeSandbox preview, do you want to continue?"* that requires a browser cookie to pass. So I cannot confirm which library it uses, whether it is client-side or calls an API, what it uploads, or what it reports. **Everything above about the technique is standard and sourceable; nothing above should be read as a verified description of this app's behaviour.**
- **Privacy is the first question and it is unanswered.** If it is client-side (the norm for `face-api.js`), images never leave your machine. If it posts them anywhere, you have just uploaded two photos of a face to an anonymous, ephemeral sandbox of unknown provenance. **Assume the worst until you check the network tab** — open DevTools → Network, then upload, and see whether a request carries your image. Facial images are special-category biometric data under regimes like GDPR, so "it was probably local" is not good enough.
- **The hostname can vanish.** `.csb.app` previews are ephemeral sandboxes tied to someone's account. They get deleted, and this link will 404 with no notice. Do not build anything on it and do not bookmark it as a tool.
- **Face comparison is not identification.** This tells you whether two *given* images match. It cannot find a person from a photo, and it cannot search a database. Treat any tool that blurs that line with suspicion.
- **Accuracy is demographic-uneven and threshold-sensitive.** Published work on face recognition consistently finds higher error rates for darker skin tones and for women, and accuracy degrades with pose, lighting, occlusion, age gap, and low resolution. A demo with no confidence reporting hides all of this.
- **Never use it for a decision that matters to a person** — access, employment, verification, moderation, or a claim about someone's identity. This class of demo has no calibration, no audit trail, and no appeal path.
- **Consent.** Comparing two photos of a real person to determine identity is processing their biometric data. Having the photos is not the same as being allowed to do that.

## Verdict

**Useful as a teaching example of the detect → align → embed → compare pipeline. Not a tool, and not verifiable as it stands.**

**Use it for**: understanding how face matching works, and as a sanity check on your intuition about thresholds before you use a real library.

**Do not use it for**: any real identification claim, anything involving a third party's biometric data without consent, or anything you need to still exist next month.

**The honest framing**: the interesting content is the four-step pipeline and the 0.6 threshold — those transfer to every real system. The app itself is an anonymous, unverifiable, disposable sandbox, and it should be treated as a demo you look at, not a service you rely on. If you want this capability, build it with `face-api.js` locally in an afternoon; you will get the same result with privacy you actually control.

## Sources

- [Demo under test](https://6mzld2.csb.app/) — https://6mzld2.csb.app/ *(returned HTTP 400 CodeSandbox trust-gate interstitial to automated fetching)*
- [`face-api.js`](https://github.com/justadudewhohacks/face-api.js) — https://github.com/justadudewhohacks/face-api.js
- [face-api.js — face recognition docs (descriptors, `euclideanDistance`, 0.6 threshold)](https://github.com/justadudewhohacks/face-api.js#face-recognition) — https://github.com/justadudewhohacks/face-api.js#face-recognition
- [MediaPipe Face Detection](https://ai.google.dev/edge/mediapipe/solutions/vision/face_detector) — https://ai.google.dev/edge/mediapipe/solutions/vision/face_detector
- [InsightFace (ArcFace models)](https://github.com/deepinsight/insightface) — https://github.com/deepinsight/insightface
- [face-comparison-api (reference implementation)](https://github.com/spiffgreen/face-comparison-api) — https://github.com/spiffgreen/face-comparison-api

*Verification note: the demo could not be reached — CodeSandbox served a trust-gate page requiring user interaction and a cookie. Its library, upload behaviour and output format are therefore **unknown and unverified**. The pipeline description and the 0.6 threshold are general knowledge taken from the `face-api.js` documentation, not from this app, and are labelled as such above. The claim that face recognition error rates vary by demographic group is well established in the literature but was not re-verified against a specific study for this entry.*
