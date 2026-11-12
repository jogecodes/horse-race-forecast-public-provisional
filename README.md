# Before the off

An English static lab notebook for the sibling `horse-race-forecast-private` study. The narrative explains how the system evolved, including failed checkpoints, cohort correction and the later isolated article experiment. Design follows the dark, lime-accented editorial language of `../chaos-public`, with explanatory diagrams instead of interactive simulations.

## Local preview

Node 22+ and Python 3 are sufficient. No dependency installation is required.

```bash
cd /app/more_studies/horse-race-forecast-public
npm run build
npm run check
npm run preview
```

Open **http://localhost:8080**. The preview listens on all interfaces to support a forwarded workspace port. If browsing from a different machine, forward TCP port 8080; its localhost is not the execution host. Stop the foreground server with Ctrl+C. Rebuild after source edits, then refresh the browser. The HTTP server serves **only `dist/`**, not the private study or project root.

## Edit the notebook

- `index.html`: narrative, conceptual SVG and HTML/CSS diagrams, source references.
- `src/styles.css`: layout, responsive behavior, print styles.
- `data/facts.json`: explicitly selected aggregate results.
- `data/provenance.json`: research source paths and SHA-256 receipts.
- `scripts/build.mjs`: deterministic static build; inserts result rows and interval chart from saved aggregate facts.
- `scripts/export_evidence.py`: optional, explicit refresh from the sibling private study.

The build works without the private folder. `npm run refresh:evidence` needs it and rewrites only the two curated JSON exports. It deliberately excludes article quotations, runner-level predictions/labels, raw model responses, databases and credentials. A refresh is not an automatic editorial update: verify the prose, counts, interpretation and chart accessibility text whenever results change.

`npm run check` verifies emitted links, unique anchors, the intended file set, expected evaluation cohorts and aggregate-only exports. No research experiment is launched by any website command. New research evidence should receive a new documented snapshot rather than silently changing the meaning of the existing experiment.

## Editorial contract

The journey is a didactic reconstruction, not a claim that every conceptual step happened in exactly the displayed order. Actual findings remain tied to the documented experiments. Invented examples are visibly marked “Illustration.” The main data is historical/reconstructed; synthetic fixtures test the pipeline and are not evidence of forecasting skill.

The latest article experiment is distinct from the earlier corrected zero-signal release. Both are explained. The latest evaluation is January-fitted / February development, with no claimed March–June evaluation, certified T−60 backtest, verified closing prices or demonstrated betting edge. See [editorial notes](docs/EDITORIAL.md).

## Cloudflare later

This task prepares a local site only. No hosting project was registered, repository pushed, or cloud deployment performed. The older withdrawn website inside the private project is separate and remains untouched.

`wrangler.jsonc` declares a static Worker with `assets.directory: ./dist`. To publish later, use an authenticated Cloudflare Wrangler installation and explicitly choose the intended account/name:

```bash
npm run build
npm run check
wrangler deploy
```

Wrangler is not installed by this project. The proposed Worker name is `horse-race-forecast-notebook`; change it before deployment if needed. Alternatively, Cloudflare Pages can serve the generated `dist/` directory. The `_headers` file declares response headers for platforms that support it; Python's development server does not apply those headers.

## Verification of this version

Static build and asset/anchor checks pass. Browser verification uses an existing local Playwright installation outside the project; no browser or dependency downloads are required. Tested widths and observations are recorded in [editorial notes](docs/EDITORIAL.md). Print styles support saving the notebook to PDF.
