# Independent market calibration baseline

Source: Betfair's official public CSV listing at https://betfair-datascientists.github.io/data/dataListing/, linking ANZ_Thoroughbreds_2024.zip. SHA-256: effe8d4183ffe6dfd410467561f788d199fc6164dd874610a93cb95e93765fef. The archive contains 193,342 runner rows in 19,550 markets. Local source bytes are retained under /tmp/horse-market-calibration, outside the served directory and Git.

Price field: BEST_AVAIL_BACK_AT_SCHEDULED_OFF, paired with WIN_RESULT. This is an exchange back-price study, not bookmaker fixed odds or BSP. It retains 19,485 races / 192,643 runner records / 2,513 meetings. Exclusions: duplicate runner identity (8 markets), not exactly one winner (24), and scheduled clock not strictly before reported actual clock (33). Whole races require valid prices for all recorded runners.

Both probability conventions use the same full cohort. Ten fixed 10-percentage-point bins describe reliability. The separate near-40% band is [37.5%,42.5%): raw probabilities yield 837 wins / 2,123 records, normalized probabilities 824 / 2,043. Normalization can change bin membership. Mean assigned probabilities are 39.84% / 39.83%; observed wins 39.43% / 40.33%. Both observed-minus-predicted intervals include zero.

Raw probabilities are assessed as binary marginal predictions, without asserting their sum is one. Race-summed squared error averages 0.77807256 raw versus 0.77792319 normalized. The paired difference is -0.00014937 with 95% interval [-0.00028876,-0.00001103]. Mean runner binary Brier is a distinct scaling (0.07869865 / 0.07868354).

Uncertainty: 4,000 paired whole-meeting percentile-bootstrap draws, seed 20261113. Scores weight races equally; reliability fractions weight runner records. No recalibration is fitted and no new forecast model is evaluated. Later calibration fitting needs an earlier fitting period and a separate later evaluation period.

Provider snapshot timing, public dissemination, complete contemporaneous fields and subsequent withdrawals are not independently certified. The population is the recorded settled field. Raw probability totals average 101.64%, ranging from 35.72% to 130.86%; extreme under-rounds warrant data/liquidity review and are not executable opportunities. No post-hoc filter was applied to improve reported scores. Exchange commission, depth, executable price size and returns are not evaluated. This is a descriptive study, not a market-edge finding or a T-60 study. Its scores cannot be compared directly with a different country/year/field cohort.

Verification: aggregate exclusions, winner counts, bin counts, normalized probability mass, near-40% fractions and score weightings were independently checked. Static build checks pass; browser QA covers 1440/768/390/320 px, expanded method notes, downloads and no page overflow or runtime errors. Curves and 40% cards were visually inspected.

## Scenario inspection after the pooled calibration result

The scenario extension reuses the same 19,485-race cohort. It publishes the three highest realized normalized Brier losses among 19,037 cases with raw price totals between 0.95 and 1.10. This additional quote-quality screen applies to case selection only; it does not change the original calibration curves. Ballina R4 on 5 January, Gold Coast R1 on 29 June and Balaklava R2 on 5 February are retrospective surprises. No independent ANZ model probabilities exist here, so they must not be described as model-market disagreements or known mispricing. The favorite and winner source rows were also checked against their separate recorded BSP fields as an audit, without changing the scheduled-start prediction convention.

Fourteen overlapping groups use field size, distance, literal race-type codes and the favorite probability range. First-half absolute calibration gaps rank candidates, minimum 250 discovery races; the top three receive a later-period descriptive check. Tied favorites are excluded from the subgroup study (339 races). Missing or alternative race-type codes stay in the other category.

The largest first-half gaps were 1,601–2,200 m races, above-2,200 m races and fields of 12+ runners. Both distance signals weakened substantially later. The larger-field favorite gap was +2.02 percentage points in January–June and +1.51 in July–December, whose 95% meeting interval [-0.16,+3.28] percentage points includes zero. Four thousand later-period meeting-bootstrap draws are pointwise, without multiple-testing adjustment. The discovery ranking is selection-biased, and pooled-year inspection prevents calling the later check independent blind evidence. This is a research lead only.

The narrative connects these diagnostics to planned pre-race model-market comparisons using committed predictions, frozen hypotheses and a new evaluation period. It does not equate a rare winning outsider with an identifiable pre-race opportunity, and no fitted correction or profitability experiment is claimed.
