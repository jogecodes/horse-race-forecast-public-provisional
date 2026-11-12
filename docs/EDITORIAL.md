# Editorial and implementation notes

## Narrative structure

The user requested an incremental account, including invented intermediate steps if useful for teaching. The notebook reconstructs dependencies while preserving recorded outcomes:

1. Historical records and provider identity.
2. Declaration recovery and temporal availability.
3. Bounded research, admission and observed bottlenecks.
4. Synthetic fixtures for deterministic behavior and separate local-model probes.
5. Statistical estimation separated from feature extraction.
6. Training-cohort confound and same-cohort correction.
7. Later isolated article experiment, including semantic errors and unsupported opposition effects.
8. Matched evaluation, cluster uncertainty, reliability and market provenance.
9. Prospective next experiment.

No experiments or performance statistics are invented. Explicit teaching constructions: hero racetrack, the three-clock timeline, and the ALPHA/BETA current-recommendation quotation. The synthetic three-runner fixture is actually present in the private test source; the displayed test matrix summarizes existing checks rather than asserting one complete synthetic population dataset.

## Distinguish the two November 12 releases

`runs/research_release_20261112` corrects cohort coverage using earlier accepted outputs whose semantic columns are all zero. The article/form difference is effectively numerical noise.

`runs/article_component_evaluation_20261112` evaluates a new single-horse article adapter on preserved sources. It adds 26 nonzero feature rows and has different scores. These must not be described as one unchanged agent arm. The latter tests controlled extraction, not the quality of the full shared-engine search process.

## Public boundary

The sibling private project is read-only for this website task. There is no copy of its hidden hosting identity, Git history, raw sources, SQLite files, full source paragraphs, model traces or runner-level evaluation records. The static build copies six explicitly allowed files only. Public provenance paths identify evidence in the local research workspace; they are references, not downloadable source files.

The removed website in the private folder remains removed. Current user instructions authorize this separate local notebook. Future Cloudflare publication remains a later step.

## Verification

- `npm run build` and `npm run check` pass.
- Local HTTP endpoint and both aggregate downloads return 200.
- Browser review at 1440, 768, 390 and 320 px checks page overflow, chapter anchors, expandable policy note and downloads.
- Desktop/mobile hero, architecture and interval chart screenshots are inspected during development.
- Print rendering is generated as a PDF for review.

Browser tooling is environment-local (`/tmp/chaos-browser`), not a dependency of this website. The website itself has no client-side JavaScript, remote fonts, remote visual assets or runtime services. No private research tests or GPU jobs are run by the site.
