# Before the off

An English static lab notebook for the sibling `horse-race-forecast-private` study. The six-chapter narrative follows one question: does source-grounded article information improve a statistical forecast? It explains failed checkpoints, the separation of reading from prediction, the cohort correction and the matched article experiment. Expandable method notes retain implementation and audit details. The current design uses a dark bottle-green journal palette, cream typography, brass and muted rose accents, a heraldic horseshoe and formal race-programme typography. An odds-first introduction uses one invented race to explain decimal odds, implied probabilities, overround, calibration and a worked multiclass Brier score before the six implementation chapters. A short glossary defines racing and forecasting terms. Diagrams, tables and print styles follow the same sporting-journal treatment.

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
- `src/forecast.js`: browser-local probability sliders, winner selection and live Brier calculation. The three probabilities always sum to 100%; the example remains readable without JavaScript.
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

## Independent historical market calibration

The site includes a separate market-only study of Betfair's public 2024 Australia & New Zealand thoroughbred archive. It compares raw inverse scheduled-off exchange back prices with proportional normalization on identical retained races. It is independent of the Spanish model cohort. Only aggregates are served in `data/market_calibration.json`; the source archive stays outside the site.

Reproduce explicitly, using the 13.3 MB publisher archive (network download is opt-in):

```bash
python3 scripts/analyze_market_calibration.py --archive /tmp/horse-market-calibration/ANZ_Thoroughbreds_2024.zip --download
npm run build
npm run check
```

The script verifies a frozen SHA-256 and resamples whole meetings 4,000 times. No account, payment, model fitting or GPU job is required. The static build uses saved aggregates and does not fetch sources or rerun analysis. Method and limitations: [market calibration](docs/MARKET_CALIBRATION.md).

## Market surprise cases and conditional scenarios

The market study also shows three retrospective high-Brier races and an exploratory subgroup search. These are diagnostics and hypothesis leads, not measured model-market disagreement or established betting opportunities. The cases are outcome-selected. Fourteen pre-race group definitions are ranked on January–June favorite calibration gaps; the three largest are checked descriptively in July–December. The pooled year had already been inspected, so the later check is not a fresh blind test.

```bash
python3 scripts/analyze_market_scenarios.py --archive /tmp/horse-market-calibration/ANZ_Thoroughbreds_2024.zip
npm run build
npm run check
```

The site serves `data/market_scenarios.json`, containing three case extracts from the public Betfair source and subgroup aggregates. It includes the source and analysis-code hashes, selection rules, later meeting-bootstrap intervals and limitations. No private model labels or traces are exported.
