# Editorial and implementation notes

## Narrative structure

The user requested an incremental account, including invented intermediate steps if useful for teaching. The notebook reconstructs dependencies while preserving recorded outcomes:

1. Reconstruct the pre-race decision: declaration, outcome, deadline and availability.
2. Try an agent that researches and predicts; observe separate retrieval and probability-output failures.
3. Move probability estimation into a statistical model and define three cumulative forecasts: A history, B history + printed form, C history + printed form + articles.
4. Test a narrow article-reading task, preserve missingness, and explain the earlier training-population correction.
5. Define the evaluation criteria before showing matched results, uncertainty, calibration and the separate market comparison.
6. State what has been learned and what the next experiment must resolve.

No experiments or performance statistics are invented. Explicit teaching constructions: the three-clock timeline and the ALPHA/BETA current-recommendation quotation. The earlier decorative gentleman-horse portrait has been removed. The synthetic three-runner fixture is actually present in the private test source; the displayed test matrix summarizes existing checks rather than asserting one complete synthetic population dataset.

## Distinguish the two November 12 releases

`runs/research_release_20261112` corrects cohort coverage using earlier accepted outputs whose semantic columns are all zero. The article/form difference is effectively numerical noise.

`runs/article_component_evaluation_20261112` evaluates a new single-horse article adapter on preserved sources. It adds 26 nonzero feature rows and has different scores. These must not be described as one unchanged agent arm. The latter tests controlled extraction, not the quality of the full shared-engine search process.

## Public boundary

The sibling private project is read-only for this website task. There is no copy of its hidden hosting identity, Git history, raw sources, SQLite files, full source paragraphs, model traces or runner-level evaluation records. The static build copies an explicit allowlist of public assets and curated aggregate files only. Public provenance paths identify evidence in the local research workspace; they are references, not downloadable source files.

The removed website in the private folder remains removed. Current user instructions authorize this separate local notebook. Future Cloudflare publication remains a later step.

## Verification

- `npm run build` and `npm run check` pass.
- Local HTTP endpoint and both aggregate downloads return 200.
- Browser review at 1440, 768, 390 and 320 px checks page overflow, chapter anchors, expandable policy note and downloads.
- Desktop/mobile hero, architecture and interval chart screenshots are inspected during development.
- Print rendering is generated as a PDF for review.

Browser tooling is environment-local (`/tmp/chaos-browser`), not a dependency of this website. The website uses one local, dependency-free script for the illustrative forecast sliders and live Brier calculation. It has no remote fonts, remote visual assets or runtime services. No private research tests or GPU jobs are run by the site.

## Country-club visual edition

The local redesign replaces the original dark science-lab appearance with an intentionally exaggerated English sporting-journal style. Cream paper, green and burgundy ink, brass-colored ornaments, a heraldic horseshoe and a top-hatted horse in tweed establish the visual theme. The horse illustration is an original inline SVG, not a real person, institution or historical plate.

The research narrative, aggregate facts, cohorts and uncertainty calculations are preserved. The generated interval figure uses burgundy ink; diagram panels, tables, equation plates, chapter dividers, notes, downloads and mobile/print layouts share the new palette and typography. Decorative country-club language stays in the editorial frame.

Build and static checks pass. Browser checks at 1440/768/390/320 px pass with no page overflow, broken anchors, browser exceptions or HTTP errors. Hero, portrait and architecture screenshots were inspected. The existing local preview remains at port 8080; no tunnel or hosting configuration changed.

## Research-first introduction

The opening now explains the experimental playground from first principles: repeated observable events, accessible public records, a relatively efficient market as a demanding working reference, and calibration as a testable research objective. The 20% / one-in-five explanation is illustrative, not an observed result. No market-efficiency estimate or achieved calibration is claimed for the study. A direct link to Snowberg & Wolfers (2010) supplies external context on departures from ideal market probability estimates; it does not validate our historical price proxies.

The horse portrait, rosette, captions and comic motto have been removed from the page, and humorous masthead/footer copy has been replaced. The cream/green/burgundy design, crest, diagrams, narrative and evaluation remain. The hero's right column now states the research question and motivation. This is still a local-only website update.

Editorial tone: keep occasional dry humor that reinforces the explanation. The market introduction retains one aside, “The market has read the form book too.” Avoid comic slogans across the masthead, hero and footer.

## Argument and reading order

The main narrative follows one experimental question: does adding source-grounded article information improve a history-and-form forecast? Each chapter explains the decision, the observation and the question motivating the next chapter. Terms such as declaration, benchmark, agent, calibration and feature are defined before use. A small invented three-horse example illustrates probabilities without pretending to be a saved model result.

Detailed dataset counts and splits, source chronology, the full original agent architecture, synthetic fixtures, model-fitting settings, equations and the earlier cohort-control experiment are available in expandable method notes. They remain grounded in their original experiments, but do not interrupt the main argument. The direct-agent engine and later controlled article-extraction test are explicitly distinct. Metrics are explained before the result table. A/B/C forecast names are consistent across the model explanation and dynamic table; original architecture role letters were removed to avoid a competing A/B/C notation.

The main path has six chapters, with a question linking each chapter to the next. Browser checks cover both the reading view and expanded method notes. Research aggregate JSON and source hashes remain unchanged.

## Dark-green, odds-first edition

Dark bottle-green now covers the journal frame and all reading sections, with slightly lighter green diagram plates, cream text and brass/rose accents. Contrast colors in the generated interval chart were updated without changing any values. Print rendering retains its plain light-paper treatment.

The primer starts with prices rather than implementation. One invented three-horse race has decimal odds 2, 3 and 4: raw implied probabilities total 108.33%, and proportional normalization gives 46.15%, 30.77% and 23.08%. These rows are calculated at build time, not stored as research observations. A separate illustrative model distribution (50%, 30%, 20%) is used throughout the calibration and Brier explanation. With GAMMA winning its summed multiclass Brier loss is 0.98; with ALPHA winning it is 0.38. The distinction between normalization, calibration, informative predictions and evaluation uncertainty is explicit.

A glossary defines declarations, fields (in the primer), form, meetings, baselines, benchmarks, features and held-out evaluation. Definitions cite primary market documentation and Gneiting & Raftery (2007). These external sources are general context, not a replacement for the local research receipts. The later evaluation links back to the same Brier convention and odds normalization. No recorded predictions, score aggregates or source hashes were changed.

Verification: build and static checks pass; browser checks at 1440/768/390/320 px pass for both closed and expanded notes, anchors and downloads. Hero, odds table, worked Brier plate and research diagram were visually inspected.

## Market reference before model building

The independent market-calibration section follows the odds/Brier primer and precedes the six model-building chapters. It contains two reliability curves, exact probability-bin counts, wins/losses around 40%, paired raw-versus-normalized scores and meeting-cluster uncertainty. It uses ANZ exchange back prices from 2024 and is explicitly separate from the Spanish 2026 model experiments. The original model facts and research receipts are unchanged. See MARKET_CALIBRATION.md for the source, protocol and interpretation.

## Where to look after a strong calibration result

The market section now continues with “Good on average. What can the average hide?” It presents actual outcome-selected high-Brier case studies, then a chronological subgroup check and a concrete plan for identifying pre-race model-market disagreement. The optimistic thread is about a research target, supported by a tentative larger-field lead. It explicitly distinguishes surprising outcomes, conditional calibration gaps and independent model-market disagreement. No positive finding is manufactured to provide a silver lining. Source/selection rules and uncertainty remain visible.

### Interactive illustrative forecast

The three fictional horses have gold, blue and rose silks, displayed as compact race-programme rows. Sliders and winner buttons have explicit cross-browser styling rather than native browser controls. The stylesheet URL is versioned so returning browsers fetch the redesign. Sliders redistribute the remaining integer percentage points proportionally between the other two horses (split evenly when their previous total is zero), keeping the total at 100%. Winner selection and reset update both the compact score and the full squared-error calculation. Scores use four decimal places, summing unrounded terms. The caption joke uses Posterior Favourite’s live assigned probability and changes its punchline depending on whether that horse wins or loses. Without JavaScript, disabled controls and the original worked example remain readable. One same-origin script is allowed by CSP and the explicit build allowlist; there are no runtime data requests.

Verified in a browser at 1440/768/390/320 px: initial scores, different winners, perfect (0) and maximally wrong (2) forecasts, repeated slider changes, 100% totals, keyboard adjustment, reset, no horizontal overflow, no-JavaScript fallback and deployment CSP. Desktop and mobile cards were visually inspected.

The primer now progresses from odds to calibration to forecasting and scoring. The probability controls, outcome vector, per-horse squared errors and Brier total live in one callout under point 3; calibration is point 2.

The calibration introduction now explains probability as uncertainty conditional on available information, then uses an illustrative 1,000 forecasts at 20% (roughly 200 realized events for a calibrated forecaster). Predictions are grouped by assigned probability across distinct events, with sampling variation and subgroup caveats. Scott Alexander’s essay on non-frequentist probabilities is cited for the conceptual framing, separately from the statistical scoring-rule reference.

Horse forecast rows now match the historical 40% comparison cards: bottle-green panels, muted borders, cream labels and brass percentages. Small muted left-edge accents identify the horses. Slider tracks and winner controls use the restrained shared palette. The confidence footnote has been removed; the live Posterior Favourite caption remains.

### Resume point — 13 November 2026

The local horse-racing preview on port 8080 was stopped at the user's request. Continue editing the standalone section headed “Now, finally: the forecasting experiment.” (`#experiment-plan`), immediately after the odds/calibration/interactive Brier primer. Its opening now reads: “Our goal is to identify disagreements between the probabilities implied by betting odds and our own estimates.” This is the current storytelling review position; the later chapters have not yet been reviewed in this pass.

The section describes forming our own probabilities, locating disagreements with market odds, and testing whether those disagreements are meaningful. Keep the English prose, dark-green restrained styling and dynamic Posterior Favourite caption. All edits remain local; no deployment or new commit was requested in this session. Restart with `npm run preview` from the public project when requested (port 8080, serving only `dist/`).
