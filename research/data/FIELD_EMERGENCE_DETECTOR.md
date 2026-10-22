# Channel B detector: method, simulation, results on the 35 section pairs (2026-10-16)

Code: [`scripts/field-emergence/detect.py`](../../scripts/field-emergence/detect.py) (`python3 -I detect.py sim | apply | all`; needs numpy and scipy, both installed here). Inputs and the naive baseline are described in [FIELD_EMERGENCE_SPIKE.md](FIELD_EMERGENCE_SPIKE.md).

## Bottom line

1. The new detector is **far stricter than the naive one and is calibrated by simulation**: 0 of 10 control pairs flagged, against 7 of 10 (30% of transitions) for the naive rule; on synthetic nulls the naive rule fires for 25-85% of pairs at any count scale of 3 or more, ours for 0-3%.
2. It **recovers almost none of the seed events at section level** (0 of 40 event-pair tests with the default thresholds; 6 of 40 with a deliberately relaxed rule, all of them the single pair 11x37: 4 in the expected decade, 2 about three decades late). That is a statement about the data as much as about the detector: the seed pairs mostly rise by a factor of 1.2 to 2 per decade, from a deficit, to about the level of a typical pair; the simulation says a step needs a factor of about 3 to 5 at 10 or more expected documents to be seen. **The 35 pairs cannot validate recall.** They validate only that the false-positive control is not obviously broken.
3. Section-pair lift against plain independence is the wrong yardstick (see "Normalisation" below); the detector measures lift against a per-window "typical pair" level.
4. For the class-level run the parametric p-value is not enough (it is too liberal, FDR 3-20% at nominal 5%); the size-matched empirical null is needed and, with BH over about 140k pairs, needs thousands of neighbours (rule of thumb below).

## Method

Notation: `n_ab[p,t]` documents carrying both classes of pair p in window t, `n_a`, `n_b` class totals, `N[t]` all documents in the window.

**1. Expectation.** `E = n_a n_b / N` (independence given margins), then `E' = kappa[t] * E`. `kappa[t]` is the typical pair lift in window t (median of `n_ab/E` over pairs with `E >= 1`; `'mass'` = `sum n_ab / sum E` is the exact multiplicity correction once the full class matrix is supplied). Reason: documents carry few codes and before about 1970 most documents carry none, so the typical pair has lift far from 1 and the factor moves with time (median lift over the 35 pairs: 1.08 in 1960-69, 0.78 in the 1970s-80s, 0.72 in the 1990s, 0.97 in 2020-24). Against raw independence, nearly every seed pair is below lift 1 even at its peak (11x37 reaches 1.0, 05x14 1.0, 14x81 1.5), so "exceeds independence" would reject them all. "Exceeds independence" is therefore implemented as lift `>= l_min` (default 1) relative to the typical pair; an optional NB-significance test against it (`indep_test`) is available and costs 7-8 points of power for under 1 point less false positives.

**2. Count model.** `Var(n) = psi * mu + nu * mu^2`, a negative binomial on the scale `n/psi`. NB rather than quasi-Poisson because (a) the lift of a pair genuinely drifts between windows, which makes variance quadratic in the mean (a quasi-Poisson `phi * mu` would let a 3-fold change at 1,000 documents look significant), while at small counts the variance must stay linear; (b) NB gives exact tails, which matter at counts of 0-20, where a quasi-likelihood has no distribution. `psi >= 1` absorbs clustering of documents (series by one author coded alike); `nu` is the extra-Poisson variance of the log-lift change between adjacent windows (`nu = 2/k` for iid gamma noise on the lift, the step variance for a random-walk lift). Both are estimated from the pooled data by moments: conditioning on `s = n1 + n2` in adjacent windows, `r = n2 - s p` (with `p = e2/(e1+e2)`) has `E[r^2 / (s p (1-p))] = psi + nu * s p (1-p)`; bin means are fitted by a weighted line, intercept `psi`, slope `nu`. On synthetic data with known values this recovers `nu` 0.09-0.10 (true 0.10) and `psi` 1.0, 1.0, 2.7-2.8 (true 1, 1, 3). On the real 35 pairs: `nu = 0.083`, `psi = 3.3` (212 transitions).

**3. Burst rule.** For window t >= 1, the baseline is the previous `m_base = 2` observed windows pooled, shrunk to independence with one pseudo-document: `L0 = (B + 1)/(E_B + 1)`. The count is tested (NB upper tail) against `L0 * E'_t`, with size `1/(psi/(B+1) + nu * c_m)` so that baseline uncertainty and a random-walk lift (`c_m = 1.25` for two windows) are priced in. Window t is an *eligible onset* if: `n_ab >= min_count (20)`, `lift >= r_min (2) x baseline`, `lift >= l_min (1)`, and, when observable, the next window's lift stays `>= sqrt(r_min) x baseline` (sustained). Pair statistic: `S = max_t` of `-log10 p` over eligible windows; parametric pair p-value = Bonferroni over the windows scanned. The **onset** is the first eligible window with pair-level `p <= alpha_date (0.01)`.

**4. Size-matched empirical null.** Each pair is described by the trajectory `log(1+E'_t)` and `log(1+min(n_a,n_b)_t)` (size and growth of the margins; it contains no information on the pair's own lift). Its ungated evidence `S_free` is ranked among the same statistic of its `M` nearest pairs (k-d tree, self excluded). The rank p-value cannot go below `1/(M+1)`, so an exponential tail is fitted through the neighbours' 80th and 95th percentiles (robust to up to 5% true events among them) and used beyond the 95th. Reported: `p_emp_rank`, `p_emp`. The final p-value is `max(p_param, p_emp)`.

**5. BH** over all pairs on `p_final` (also reported on `p_param` and `p_emp` separately).

## Simulation study

Synthetic series use the real window totals `N[t]` (so realistic growth), pair-specific lognormal affinity, a coverage drift shared by all pairs, growth of the pair's expected size, margin imbalance, integer margins, and three null families: **iid** (constant lift, NB k = 20), **drift** (random-walk lift, step sd 0.25, plus NB k = 50) and **drift+cluster** (as drift, plus documents in clusters of mean size 2, so variance/mean = 3). Injected take-offs multiply the lift by x2...x30 from a random window in 1970s..2010s, as a **step** or a **ramp** (square root of the factor in the first window). The scale is `mu0`: expected co-assigned documents in the take-off window before the take-off. 1,500 pairs per cell, seed 7; reproduce with `python3 -I detect.py sim` (about 35 s).

### A. False positive rate per pair (any window), unadjusted

Rule = default `detect` thresholds, pair-level p <= 0.01. Naive = any window-to-window lift jump >= 1.5 with n_ab >= 10.

| mu0 | iid rule | iid naive | drift rule | drift naive | drift+cluster rule | drift+cluster naive |
|---|---|---|---|---|---|---|
| 0.3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.003 |
| 1 | 0.000 | 0.013 | 0.000 | 0.027 | 0.001 | 0.069 |
| 3 | 0.003 | 0.274 | 0.003 | 0.272 | 0.005 | 0.405 |
| 10 | 0.007 | 0.705 | 0.014 | 0.682 | 0.019 | 0.830 |
| 30 | 0.007 | 0.667 | 0.027 | 0.665 | 0.033 | 0.842 |
| 100 | 0.008 | 0.509 | 0.021 | 0.535 | 0.031 | 0.701 |
| 300 | 0.007 | 0.473 | 0.022 | 0.453 | 0.024 | 0.538 |

The naive rule's rate on real controls (7 of 10 pairs; 17 of 56 transitions = 30%) is what it does on pure noise. The rule's FPR is above the nominal 0.01 by a factor 2-3 under drift (it is a per-pair rate and the lift drifts as a random walk), which is why BH on the parametric p alone is not enough (table D). Without the count/ratio/sustain gates the FPR is 1-7%.

### B. Power: % dated in the right window / % in the right window or one late (drift+cluster null)

Step:

| mu0 | x2 | x3 | x5 | x10 | x30 |
|---|---|---|---|---|---|
| 0.3 | 0/0 | 0/0 | 0/0 | 0/1 | 5/19 |
| 1 | 0/0 | 0/1 | 0/2 | 6/15 | 82/91 |
| 3 | 0/2 | 1/4 | 16/21 | 68/73 | 100/100 |
| 10 | 6/8 | 20/23 | 55/58 | 95/95 | 100/100 |
| 30 | 10/12 | 37/39 | 80/81 | 96/96 | 98/98 |
| 100 | 17/19 | 51/53 | 90/91 | 97/98 | 98/98 |
| 300 | 18/20 | 60/61 | 91/92 | 97/97 | 99/99 |

Ramp (gradual, reaching the full factor one window later):

| mu0 | x2 | x3 | x5 | x10 | x30 |
|---|---|---|---|---|---|
| 3 | 0/2 | 0/5 | 1/19 | 2/56 | 21/98 |
| 10 | 2/6 | 3/17 | 8/40 | 24/82 | 63/99 |
| 30 | 3/10 | 8/24 | 16/59 | 41/91 | 88/99 |
| 100 | 3/9 | 9/31 | 24/67 | 57/95 | 93/98 |
| 300 | 4/11 | 11/33 | 30/72 | 67/96 | 94/99 |

(The drift-only tables are within a few points of these; the full output is printed by `python3 -I detect.py sim`.) Reading: a x5 step is found 55-90% of the time from 10 expected documents upward and almost never below 3; x10 from about 3 (68% at mu0 = 3, 95% at 10); x3 reaches 50% only at about mu0 = 100; x2 is found at most 20% of the time at any scale. A gradual rise is dated correctly (right window or one late) only if it is large: x5 ramps reach 59-72% at mu0 >= 30, and the exact window only 16-30%. Below mu0 of about 3 nothing short of a 30-fold jump is detectable: **at small counts this is a data limit, not a tuning choice.**

### C. Thresholds (drift+cluster null, unadjusted, pooled mu0 1-100)

| min_count | l_min | indep_test | FPR | power x5, mu0=10 | power x5, mu0=30 |
|---|---|---|---|---|---|
| 5 | 1.0 | no | 0.036 | 0.553 | 0.792 |
| 10 | 1.0 | no | 0.029 | 0.559 | 0.792 |
| **20** | **1.0** | **no** | **0.017** | **0.565** | **0.799** |
| 30 | 1.0 | no | 0.011 | 0.561 | 0.804 |
| 20 | 1.5 | no | 0.016 | 0.547 | 0.775 |
| 20 | 1.0 | yes | 0.013 | 0.495 | 0.715 |

Raising `min_count` from 5 to 20 halves the FPR at no cost in power (the NB test already refuses small counts; the gate removes the clustered-noise cases the Poisson-inflation estimate misses). `r_min` between 1.5 and 3 changes nothing for the same reason. Chosen: `min_count = 20, r_min = 2, l_min = 1, m_base = 2, sustain, alpha_date = 0.01, indep_test off`.

### D. Mixed population with BH at q = 0.05

Events: 4% of pairs, factor in {3,5,10}, mu0 log-uniform 0.3-300 (so about a quarter of the events are below mu0 = 1.5 and essentially undetectable). FDR = flagged pairs that are null; power = event flagged and dated in the true window or one late; "hi" = events with mu0 >= 10.

| pool | M | null | param FDR | param power (hi) | emp FDR | emp power (hi) | final FDR | final power (hi) |
|---|---|---|---|---|---|---|---|---|
| 2000 | 100 | iid | 0.027 | 0.45 (0.74) | 0.054 | 0.44 (0.71) | 0.030 | 0.40 (0.66) |
| 2000 | 100 | drift | 0.196 | 0.50 (0.79) | 0.067 | 0.35 (0.55) | 0.069 | 0.34 (0.52) |
| 2000 | 100 | drift+cluster | 0.135 | 0.39 (0.62) | 0.000 | 0.31 (0.54) | 0.000 | 0.31 (0.54) |
| 10000 | 500 | iid | 0.059 | 0.48 (0.71) | 0.018 | 0.40 (0.61) | 0.019 | 0.40 (0.61) |
| 10000 | 500 | drift | 0.116 | 0.45 (0.67) | 0.014 | 0.34 (0.52) | 0.007 | 0.33 (0.51) |
| 10000 | 500 | drift+cluster | 0.195 | 0.37 (0.64) | 0.028 | 0.26 (0.49) | 0.028 | 0.26 (0.49) |
| 10000 | 2000 | iid | 0.063 | 0.44 (0.68) | 0.000 | 0.30 (0.49) | 0.000 | 0.30 (0.49) |
| 10000 | 2000 | drift | 0.121 | 0.44 (0.68) | 0.034 | 0.35 (0.58) | 0.028 | 0.34 (0.58) |
| 10000 | 2000 | drift+cluster | 0.138 | 0.38 (0.63) | 0.018 | 0.27 (0.47) | 0.009 | 0.27 (0.47) |

The parametric p-value controls FDR only under iid noise; with lift drift or clustering it is 12-20% at nominal 5%. The empirical null brings FDR to 0-7% (conservative) at a cost of roughly 10 points of power. Use `p_final` (or `p_emp`).

Two cautions on D. (i) Resolution: BH with m tests can only reject a p-value of at most `q * R / m` for R rejections, so an empirical p-value with floor `1/(M+1)` supports at most `R >= m / (q (M+1))` rejections unless the tail is extrapolated. The exponential tail fit is what makes D work with M of 100-2000; it is an extrapolation, not a measurement. (ii) The simulated lift model is mine: if real lifts drift or cluster differently, D's numbers move. D checks internal consistency, not truth.

### E. All-null check at class-level size

140,000 simulated pairs, no events, mu0 log-uniform 0.05-300, M = 500 (one run each; not in `detect.py sim`, which would take minutes: call `simulate` and `detect` as in the module). Pairs flagged:

| null | unadjusted rule (onset only) | BH on p_param | BH on p_emp | BH on p_final |
|---|---|---|---|---|
| iid | 484 | 11 | 10 | 3 |
| drift | 1,590 | 116 | 13 | 11 |
| drift+cluster | 1,989 | 67 | 0 | 0 |

With no real events BH at q = 0.05 should report anything in at most 5% of runs; 3 and 11 false flags out of 140,000 (0.002-0.008%) show the empirical layer is slightly anti-conservative in the extreme tail under drift, a negligible rate here but a reason to treat q-values as approximate. The unadjusted rule alone would flag 0.3-1.4% of all pairs: the case for BH plus the empirical null at this scale. 140,000 pairs take about 45 s (M = 500); M in the thousands is slow (minutes per run) and would need chunking or size strata.

## Results on the 35 section pairs

Data: `zbmath_counts.jsonl`, 9 windows. The 1931-49 pair counts are missing (query timeouts), so those windows serve only as margins. 25 event pairs + 10 controls. Run `python3 -I detect.py apply` for the full table (40 event-pair tests, reasons for every miss).

**Dispersion and normalisation:** `nu = 0.083`, `psi = 3.3`; `kappa` = 1.08, 1.08, 1.08, 0.78, 0.78, 0.72, 0.73, 0.78, 0.97 by window. (kappa here is the median over a hand-picked set of pairs; 25 of the 35 were selected for being event pairs, so it is somewhat high, which makes the detector slightly stricter.)

**Controls.** Default rule: 0 of 10 flagged (and 0 of 10 at the relaxed setting below). Naive rule: 7 of 10 pairs have at least one jump >= 1.5, 17 of 56 transitions (30%). The exact upper 95% bound for 0 of 10 is 26%, so this shows the rule is not wildly liberal, not that its false positive rate is 1%; the simulation (table A) is the better guide. Caveat: the "controls" are random pairs from the same sections, not verified non-events (46x81 operator algebras x quantum theory, for instance, is a real field relation), so the control rate is an upper bound on the false positive rate if anything.

**Seed events (default rule).** 40 event-pair tests (22 hand-mapped from `analyze_spike.py`'s EV table, which mixes seed A and B events, 18 derived from `mscSections` of seed B, anchored on the start of the conceptual interval if at most 10 years wide, else the start of the methodological interval; 20 distinct pairs; B18 wavelets 42x94 was never queried): **exact 0, one window late 0, missed 40.** The naive rule "hits" in 16 of the 38 scoreable tests (42%), about what it does on controls.

Why the misses, from the per-test diagnostics:
- **Rise too gradual, or not above a typical pair**: most tests (e.g. 17x81 moonshine: lift 5.1 to 8.0, x1.6, then x1.4 in the next decade; 14x81 mirror symmetry x1.9; 05x14 Huh x1.3; 58x81 x1.8; 46x57 Jones x1.9 but lift 0.39 vs a typical pair 1). The lift of these pairs grows by 20-90% per decade; a step detector with a two-window baseline and a ratio gate of 2 rejects that by design.
- **Counts too small in the expected decade**: Furstenberg 11x37 (7 documents in the 1970s), Atiyah-Singer 55x58 (5 in the 1960s), 11x22 Langlands (26 in the 1960s: gates pass, but pair-level p = 0.26).
- **Insufficient evidence given overdispersion**: 57x81 Donaldson (137 documents, x2.2, p_pair = 0.39), 11x37 in the 2000s (n = 1120, x2.2 on 0.51, p_pair = 0.017: just misses 0.01).
- **Decline or flat at the event date**: SLE 60x81 (x0.5), 05x94, 05x68 (x1.5 in the 1970s only), 32x35 D-modules, the 11x14 pairs (lift 10 in 1931-60, falling to 4-7).
- **Blind**: B17 entropy 37x94 (section 37 and 94 empty before 1970; zero documents).
- **Not visible at section level** (known from the spike): SLE, the polynomial method.

**Detected:** with the default rule only 14x52 (algebraic geometry x convex geometry) in the 1990s (q = 0.024 after BH over 35, p_emp = 0.04); it is on the pair list but no seed event is attached to it in the EV table, so it is unscored. With a relaxed rule (`m_base = 1, min_count = 10, alpha_date = 0.05`, shown for sensitivity only and not recommended because it is chosen after seeing the seeds) 11x37 also fires in the 2000s: exact for E50 (Green-Tao ergodic route, 2004), B13 (2006), B13 measure rigidity (2003) and B41 (2006); "late" for E38 Furstenberg 1977 and B30 1974 (the MSC curve rises decades after those dates; part of this is the new section 37 in the 2000 MSC edition rather than mathematics). **All six hits are one pair with several events attached**, so this is one observation, not six.

## What 35 pairs can and cannot tell us

Can: the false-positive behaviour is not obviously broken (0 of 10); the dispersion parameters are estimable from 212 transitions and are in the range the simulation assumes; the failure of the naive rule is real; the seeds' section-level signature is gradual and mostly sub-threshold; the blind period before 1970 is real.

Cannot:
- **Recall.** Twenty distinct pairs, most with a mild rise, tested against a threshold the simulation says needs a x3-5 step. A miss tells us the signal is not step-like or not large, not that the detector is wrong. No seed event was chosen because it should produce a step in the section-pair series, and the event-to-pair mapping is mine.
- **False discovery rate.** Ten controls cannot resolve anything below about 25%.
- **The empirical null.** With 34 other pairs available, M <= 15 and the p-value floor is 0.06; BH on it cannot reject anything with 35 tests. The `p_emp` column is a rank, not a calibrated p-value.
- **Dating accuracy.** Windows are a decade wide; the 1931-49 and 2020-24 windows have different widths; the first window has no pair counts.
- **kappa and the dispersion** are estimated from a non-random set of pairs.
- **Independence across events.** Several events share a pair (11x37 appears six times); counting tests as independent overstates both hits and misses.

## Limitations of the method

- It is a step detector. Slow growth (the typical shape of a maturing field), a decline-then-recovery, or a rise that straddles two windows is under-detected (table B, ramps).
- Window-scale dating: the onset is a window, not a year, and a rise during a window is attributed to it only if the previous windows were low.
- Classification artefacts are not modelled: new sections (37 in MSC 2000, 94 earlier), retroactive coding, and the coverage jump around 1970 (shares of every section jump 3-10-fold between the 1960s and 1970s) make "take-offs" that are relabelling. `kappa[t]` removes the common part of this; section-specific relabelling stays.
- The null is document-level independence adjusted by one scalar per window. A degree-preserving null (document by document, from the dump) is stronger and is the natural next step.
- Simulation assumptions (lognormal affinity, random-walk drift, cluster size) are plausible but unvalidated; the overdispersion estimator is the main link to reality and is estimated on contaminated data (events inflate it, which is conservative).

## Recommendation for the class-level run

1. Work from the zbMATH dump so that `N[t]` is the number of **classified** documents and so that document-level degree-preserving permutation is possible; use `kappa = 'mass'` on the full matrix.
2. Use 5-year windows from 1970 only if counts allow; the simulation says detection needs about 10 expected documents in the take-off window (about 3 for a x10 jump). Most of the ~140k pairs have far fewer, so **expect to test a small fraction of pairs at all**; report the number of pairs that clear `min_count` before reporting discoveries, and run BH over the testable pairs.
3. Use `p_final` with M in the thousands (BH over 140k pairs rejecting R pairs needs a p-value floor below `q R / m`; at m = 140,000, R = 500 that is 1.8e-4, so M >= 5,600 for rank p-values, or the tail-fitted version with M of about 500-2,000 as in table D). Stratify the neighbours by size so the pool is homogeneous.
4. Treat `onset` as a candidate date to be checked against channel A, not as a finding; the recoverable class of events is large, sustained jumps in well-populated pairs.
5. Do not tune thresholds on the 35 pairs or on the seeds; if tuning is wanted, hold out half of seed set B.
6. Before running: simulate once more with a lift-drift and cluster structure measured from the real class-level transitions (`estimate_dispersion` prints `nu`, `psi`).
