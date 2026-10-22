#!/usr/bin/env python3
"""Detector for 'a pair of MSC classes started to be co-assigned far more than expected'.

Needs numpy and scipy (both present in this environment). Run with `python3 -I detect.py`:

    python3 -I detect.py sim      # simulation study (false positives and power by count scale)
    python3 -I detect.py apply    # the 35 section-level pairs, scored against the seed events
    python3 -I detect.py all

Library use (the interface for the class-level run):

    from detect import detect, Params
    res = detect(n_ab, n_a, n_b, N, pair_index=None, params=Params())

    n_ab[P, T]   documents carrying both classes of pair p in window t (NaN = not observed)
    n_a, n_b     either [P, T] (already expanded per pair) or [C, T] per class together with
                 pair_index[P, 2] giving the rows of the two classes of each pair
    N[T]         all documents in window t

What the method does, in short (full write-up and simulation tables in
data/collection/FIELD_EMERGENCE_DETECTOR.md):

 1. Expectation under independence E = n_a * n_b / N, rescaled by kappa[t], the typical pair lift
    in window t (documents carry few codes and coverage changes over time, so raw independence is
    not the right yardstick). lift = n_ab / (kappa * E).
 2. Count model Var(n) = psi * mu + nu * mu^2 (negative binomial on the scale n / psi); psi
    (clustering) and nu (lift drift between windows) estimated from the pooled data.
 3. Burst rule: window t is an eligible onset if the count is >= min_count, the lift is >= r_min
    times the pair's own baseline (previous m_base windows) and >= l_min, and, if observable, the
    next window stays above the baseline. Evidence = NB upper-tail p-value against the baseline
    expectation (optionally also against the independence expectation: indep_test). The onset is
    the first eligible window with pair-level p <= alpha_date.
 4. Pair statistic S = max over windows of the evidence; parametric pair p-value = Bonferroni over
    the windows scanned. Empirical p-value: rank of the pair's ungated evidence among its M
    nearest pairs in (log expected count, log smaller margin) trajectory, with an exponential tail
    fitted to the 80th-95th percentile of those neighbours so the p-value is not stuck at 1/(M+1).
    p_final = max(p_param, p_emp).
 5. Benjamini-Hochberg over all pairs (q_param, q_emp, q_final).

detect() returns a dict: onset (window index or -1), S, p_param, p_emp, p_final, q_*, nu, psi,
kappa, E (kappa-adjusted expectation), scan (per-window lift, baseline lift, eligibility).
"""
from __future__ import annotations

import json
import math
import os
import sys
from dataclasses import dataclass, field

import numpy as np
from scipy.spatial import cKDTree
from scipy.stats import nbinom

LN10 = math.log(10.0)


# --------------------------------------------------------------------------------------------
# parameters
# --------------------------------------------------------------------------------------------
@dataclass
class Params:
    min_count: int = 20        # minimum co-assigned documents in the onset window
    r_min: float = 2.0         # lift must be >= r_min x own baseline lift
    l_min: float = 1.0         # and lift must be >= l_min (independence is lift 1; significance vs 1 is tested separately)
    m_base: int = 2            # baseline = previous m_base observed windows
    prior_weight: float = 1.0  # baseline lift shrunk to 1 with this many expected documents
    sustain: bool = True       # next window (if observable) must keep lift >= sqrt(r_min) x baseline
    alpha_date: float = 0.01   # pair-level (Bonferroni over windows) level for dating an onset
    disp_wmin: float = 1.0     # transitions need binomial variance s*p*(1-p) >= this to enter the dispersion estimate
    disp_trim: float = 0.005   # trimmed share of the largest squared residuals per bin
    nu_default: float = 0.15   # used only if fewer than 80 usable transitions
    nu_floor: float = 0.01
    n_neighbors: int = 200     # M for the size-matched empirical null
    emp_tail: bool = True      # exponential tail smoothing of the empirical p-value
    fdr: float = 0.05
    indep_test: bool = False   # if True, also require NB-significance against the (kappa-adjusted) independence expectation, not just lift >= l_min
    kappa: str = "median"      # 'median' | 'mass' | 'none': per-window multiplicity / coverage normalisation
    kappa_min_e: float = 1.0   # pairs need E >= this to enter the kappa estimate


# --------------------------------------------------------------------------------------------
# step 1-2: expectation and dispersion
# --------------------------------------------------------------------------------------------
def expected(n_a, n_b, N):
    """E[p, t] = n_a * n_b / N: expected co-assignment if documents carried classes independently."""
    return np.asarray(n_a, float) * np.asarray(n_b, float) / np.asarray(N, float)[None, :]


def estimate_kappa(n_ab, E, params: Params = Params()):
    """Per-window normalisation kappa[t]: the typical lift of a pair in window t.

    Documents carry only a few codes and, before the 1970s, most documents carry none, so
    n_a * n_b / N is not the right yardstick: the typical pair has lift far from 1 and the factor
    moves with time (coverage). kappa[t] is the median lift over pairs with E >= kappa_min_e
    ('median', robust to the minority of emerging pairs) or sum(n_ab) / sum(E) ('mass', exact
    document-multiplicity correction when the full class matrix is supplied). A pair's 'excess over
    independence' is then lift / kappa. Windows with fewer than 10 usable pairs borrow the nearest
    estimated window."""
    T = n_ab.shape[1]
    kap = np.full(T, np.nan)
    if params.kappa == "none":
        return np.ones(T)
    for t in range(T):
        m = np.isfinite(n_ab[:, t]) & np.isfinite(E[:, t]) & (E[:, t] >= params.kappa_min_e)
        if m.sum() < 10:
            continue
        if params.kappa == "mass":
            kap[t] = n_ab[m, t].sum() / E[m, t].sum()
        else:
            kap[t] = np.median(n_ab[m, t] / E[m, t])
    good = np.where(np.isfinite(kap) & (kap > 0))[0]
    if len(good) == 0:
        return np.ones(T)
    for t in range(T):
        if not (np.isfinite(kap[t]) and kap[t] > 0):
            kap[t] = kap[good[np.argmin(np.abs(good - t))]]
    return kap


def estimate_dispersion(n_ab, E, params: Params = Params()):
    """Two overdispersion parameters, estimated from the pooled data (quasi-likelihood moments).

    Count model: Var(n) = psi * mu + nu * mu^2, i.e. a negative binomial on the scale n / psi.
      psi >= 1  Poisson inflation: documents arrive in clusters (one author's series, a book of
                surveys coded the same way); psi = 1 is plain Poisson.
      nu        the NB term: how much a pair's lift moves between windows beyond count noise
                (iid gamma noise on the lift gives nu = 2/k for NB size k; a random-walk lift gives
                nu = the step variance). It is what makes the tests refuse small ratios at large counts.
    Estimation: for every pair and adjacent windows (1, 2) with expectations e1, e2, condition on
    s = n1 + n2 and put p = e2 / (e1 + e2). If the lift were constant, n2 | s would be binomial(s, p)
    with variance s p (1-p) = w. So r = n2 - s p has E[r^2 / w] = psi + nu * w. Transitions with
    w >= disp_wmin are binned by w, the (2%-trimmed, to resist genuine take-offs) mean of r^2 / w is
    taken per bin, and a line is fitted through the bin means: intercept psi, slope nu. On synthetic
    data with known psi and nu this recovers both to within about 10%. Returns (nu, psi, n_used)."""
    n1, n2 = n_ab[:, :-1], n_ab[:, 1:]
    e1, e2 = E[:, :-1], E[:, 1:]
    m = (e1 > 0) & (e2 > 0) & np.isfinite(n1) & np.isfinite(n2)
    n1, n2, e1, e2 = n1[m], n2[m], e1[m], e2[m]
    p = e2 / (e1 + e2)
    s = n1 + n2
    w = s * p * (1 - p)
    r = n2 - s * p
    k = w >= params.disp_wmin
    r, w = r[k], w[k]
    if len(w) < 80:
        return params.nu_default, 1.0, int(len(w))
    order = np.argsort(w)
    nb = int(min(10, len(w) // 40))
    W, V = [], []
    for ch in np.array_split(order, nb):
        x = np.sort(r[ch] ** 2 / w[ch])
        x = x[: max(1, int(len(x) * (1 - params.disp_trim)))]
        W.append(float(w[ch].mean()))
        V.append(float(x.mean()))
    W_, V_ = np.array(W), np.array(V)
    # relative-error weights: a bin mean of r^2/w has sd proportional to its mean, so weight by 1/mean^2
    slope, icpt = np.polyfit(W_, V_, 1, w=1.0 / V_)
    psi = max(float(icpt), 1.0)
    nu = float(slope)
    if icpt < 1.0:                       # intercept cannot be below Poisson: refit slope with psi = 1
        wt = 1.0 / V_ ** 2
        nu = float(np.sum(wt * W_ * (V_ - 1.0)) / np.sum(wt * W_ * W_))
    return max(nu, params.nu_floor), min(psi, 10.0), int(len(w))


# --------------------------------------------------------------------------------------------
# step 3-4: burst scan for every pair
# --------------------------------------------------------------------------------------------
def _nb_logsf(x, mean, size):
    """log P(X >= x) for X ~ NB with given mean and size (variance = mean + mean^2 / size)."""
    mean = np.maximum(mean, 1e-12)
    return nbinom.logsf(x - 1.0, size, size / (size + mean))


def scan(n_ab, E, nu, params: Params = Params(), psi=1.0):
    """Window-by-window evidence for each pair. Returns dict of [P, T] arrays (window 0 has no baseline)."""
    P, T = n_ab.shape
    valid = np.isfinite(n_ab) & np.isfinite(E) & (E > 0)
    n = np.where(valid, n_ab, 0.0)
    e = np.where(valid, E, 0.0)
    v = valid.astype(float)
    S_raw = np.zeros((P, T))        # -log10 of the weaker of the two p-values
    lift = np.where(valid, n / np.where(valid, e, 1.0), np.nan)
    base_lift = np.full((P, T), np.nan)
    tested = np.zeros((P, T), bool)  # has a baseline and an observed count
    mb = params.m_base
    drift_c = (mb + 1) * (2 * mb + 1) / (6.0 * mb)   # variance of x_t - mean(previous mb) for a random-walk lift, in units of nu
    for t in range(1, T):
        lo = max(0, t - params.m_base)
        B = n[:, lo:t].sum(1)
        EB = e[:, lo:t].sum(1)
        m_eff = v[:, lo:t].sum(1)
        ok = valid[:, t] & (m_eff >= 1)
        w = params.prior_weight
        L0 = (B + w) / (EB + w)                       # baseline lift shrunk towards independence
        base_lift[:, t] = np.where(ok, L0, np.nan)
        mean0 = L0 * e[:, t]
        size_b = 1.0 / (psi / (B + w) + nu * drift_c)  # baseline uncertainty + lift drift
        # counts are tested on the n/psi scale (Var = psi*mu + nu*mu^2)
        x = np.ceil(n[:, t] / psi - 1e-9)
        lp_base = _nb_logsf(x, mean0 / psi, size_b)
        lp_ind = _nb_logsf(x, e[:, t] / psi, 1.0 / nu)
        lp = np.maximum(lp_base, lp_ind) if params.indep_test else lp_base
        S_raw[:, t] = np.where(ok, -lp / LN10, 0.0)
        tested[:, t] = ok
    ratio = lift / base_lift
    gate = tested & (n >= params.min_count) & (ratio >= params.r_min) & (lift >= params.l_min)
    sustained = np.ones((P, T), bool)
    if params.sustain:
        nxt_lift = np.full((P, T), np.nan)
        nxt_lift[:, :-1] = lift[:, 1:]
        sustained = ~np.isfinite(nxt_lift) | (nxt_lift >= math.sqrt(params.r_min) * np.nan_to_num(base_lift, nan=0.0))
    eligible = gate & sustained
    S = np.where(eligible, S_raw, 0.0)
    return dict(lift=lift, base_lift=base_lift, ratio=ratio, S_raw=S_raw, S=S, eligible=eligible,
                tested=tested, valid=valid)


def pair_summary(sc, params: Params = Params()):
    """Pair-level statistic S, parametric p (Bonferroni over scanned windows) and dated onset."""
    S = sc["S"].max(1)
    nwin = np.maximum(sc["tested"].sum(1), 1)
    p_param = np.minimum(1.0, nwin * 10.0 ** (-S))
    p_param = np.where(S > 0, p_param, 1.0)
    thr = -np.log10(params.alpha_date / nwin)                  # per-pair threshold on S_t
    hit = sc["eligible"] & (sc["S_raw"] >= thr[:, None])
    onset = np.where(hit.any(1), hit.argmax(1), -1)
    return S, p_param, onset


# --------------------------------------------------------------------------------------------
# step 5: size-matched empirical null
# --------------------------------------------------------------------------------------------
def match_features(n_a, n_b, E):
    """Trajectory of expected size and of the smaller margin: what 'size and growth' means here."""
    f1 = np.log1p(np.nan_to_num(E, nan=0.0))
    f2 = np.log1p(np.nan_to_num(np.minimum(n_a, n_b), nan=0.0))
    return np.hstack([f1, f2])


def empirical_null_p(S, feats, params: Params = Params(), chunk=20000):
    """For each pair, p-value of its S against the S of its M nearest pairs in feature space (self
    excluded). Returns (p_rank, p_smooth, M). p_rank >= 1/(M+1). p_smooth fits an exponential tail
    through the neighbours' 80th and 95th percentiles (robust to up to 5% true events among them),
    so that it can go below 1/(M+1) when there is something to extrapolate from."""
    P = len(S)
    M = int(min(params.n_neighbors, P - 1))
    if M < 5:
        return np.ones(P), np.ones(P), M
    tree = cKDTree(feats)
    p_rank = np.ones(P)
    p_smooth = np.ones(P)
    for s in range(0, P, chunk):
        idx = np.arange(s, min(P, s + chunk))
        _, nb = tree.query(feats[idx], k=M + 1)
        ref = S[nb]                                         # [chunk, M+1], first is usually self
        selfmask = nb == idx[:, None]
        # drop self wherever it appears; if it does not appear (ties), drop the farthest
        drop = np.where(selfmask.any(1), selfmask.argmax(1), M)
        keep = np.ones(ref.shape, bool)
        keep[np.arange(len(idx)), drop] = False
        ref = ref[keep].reshape(len(idx), M)
        ge = (ref >= S[idx][:, None]).sum(1)
        pr = (1.0 + ge) / (M + 1.0)
        p_rank[idx] = pr
        if params.emp_tail:
            q80 = np.quantile(ref, 0.80, axis=1)
            q95 = np.quantile(ref, 0.95, axis=1)
            beta = (q95 - q80) / math.log(4.0)
            tail = (S[idx] > q95) & (beta > 1e-9)
            ps = 0.05 * np.exp(-(S[idx] - q95) / np.where(beta > 1e-9, beta, 1.0))
            p_smooth[idx] = np.where(tail, np.minimum(pr, ps), pr)
        else:
            p_smooth[idx] = pr
    return p_rank, p_smooth, M


def benjamini_hochberg(p):
    """BH adjusted p-values (q-values), NaN-safe (NaN -> 1)."""
    p = np.nan_to_num(np.asarray(p, float), nan=1.0)
    m = len(p)
    order = np.argsort(p)
    q = p[order] * m / (np.arange(m) + 1.0)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(m)
    out[order] = np.minimum(q, 1.0)
    return out


# --------------------------------------------------------------------------------------------
# the one-call interface
# --------------------------------------------------------------------------------------------
def detect(n_ab, n_a, n_b, N, pair_index=None, params: Params = Params(), nu=None):
    n_ab = np.asarray(n_ab, float)
    n_a = np.asarray(n_a, float)
    n_b = np.asarray(n_b, float)
    if pair_index is not None:
        pair_index = np.asarray(pair_index)
        n_a, n_b = n_a[pair_index[:, 0]], n_b[pair_index[:, 1]]
    E0 = expected(n_a, n_b, N)
    E0 = np.where((n_a > 0) & (n_b > 0), E0, np.nan)
    kap = estimate_kappa(n_ab, E0, params)
    E = E0 * kap[None, :]
    n_used = None
    psi = 1.0
    if nu is None:
        nu, psi, n_used = estimate_dispersion(n_ab, E, params)
    sc = scan(n_ab, E, nu, params, psi)
    S, p_param, onset = pair_summary(sc, params)
    feats = match_features(n_a, n_b, E)
    S_free = sc["S_raw"].max(1)                  # ungated evidence: continuous, so the empirical tail can be fitted
    p_rank, p_smooth, M = empirical_null_p(S_free, feats, params)
    return dict(
        E=E, E_indep=E0, kappa=kap, nu=nu, psi=psi, nu_transitions=n_used, scan=sc, S=S, onset=onset,
        p_param=p_param, p_emp_rank=p_rank, p_emp=p_smooth, n_neighbors=M,
        p_final=np.maximum(p_param, p_smooth),
        q_param=benjamini_hochberg(p_param),
        q_emp=benjamini_hochberg(p_smooth),
        q_final=benjamini_hochberg(np.maximum(p_param, p_smooth)),
    )


# --------------------------------------------------------------------------------------------
# naive detector (as in analyze_spike.py), for comparison on simulated and real data
# --------------------------------------------------------------------------------------------
def naive_jumps(n_ab, E, min_n=10):
    """lift(t)/lift(t-1) where n_ab(t) >= min_n, as in analyze_spike.py; NaN elsewhere."""
    with np.errstate(divide="ignore", invalid="ignore"):
        lift = n_ab / E
    with np.errstate(divide="ignore", invalid="ignore"):
        j = lift[:, 1:] / lift[:, :-1]
    ok = (n_ab[:, 1:] >= min_n) & np.isfinite(j) & (lift[:, :-1] > 0)
    return np.where(ok, j, np.nan)


# --------------------------------------------------------------------------------------------
# step 6: simulation study
# --------------------------------------------------------------------------------------------
# real window totals (zbMATH Open documents per window), used to give simulated series realistic growth
N_REAL = np.array([132597, 87786, 171636, 349798, 484095, 675889, 1019172, 1213675, 634584], float)
T_REAL = len(N_REAL)
NULL_KINDS = ("iid", "drift", "drift+cluster")


def _draw_counts(rng, lam, kind):
    """lam: expected counts [P, T] (already including lift path). Adds NB noise (+ clustering)."""
    k = 20.0 if kind == "iid" else 50.0
    g = rng.gamma(k, 1.0 / k, size=lam.shape)
    mu = lam * g
    if kind == "drift+cluster":
        c = rng.poisson(mu / 2.0)                    # clusters of mean size 2 (e.g. one author's series)
        extra = np.where(c > 0, rng.negative_binomial(np.maximum(c, 1), 0.5), 0)
        return (c + extra).astype(float)
    return rng.poisson(mu).astype(float)


KAPPA_TRUE = np.array([4.0, 3.0, 1.5, 1.0, 1.0, 0.8, 0.7, 0.7, 0.8])  # coverage / multiplicity drift shared by all pairs


def simulate(rng, P, scale, kind, factor=None, t_star=None, shape="step", T=T_REAL, N=N_REAL):
    """Synthetic pairs. scale = baseline expected count mu0 = (typical lift x E) in the reference
    window (the take-off window t_star for injected series, window 5 for null series); may be an
    array of length P. A take-off multiplies the lift by `factor` from t_star on ('step'), or by
    sqrt(factor) at t_star and by factor afterwards ('ramp'); factor may be an array (1 = no event).
    Lifts: pair-specific lognormal level x shared coverage drift KAPPA_TRUE x (iid or random-walk
    drift). Returns n_ab, n_a, n_b [P, T]."""
    scale = np.broadcast_to(np.asarray(scale, float), (P,))
    gamma = rng.uniform(-0.2, 0.6, size=(P, 1))                 # growth of the pair's expected size
    tt = np.arange(T)[None, :]
    shape_E = N[None, :] * np.exp(gamma * tt)
    log_L0 = rng.normal(math.log(1.5), 1.0, size=(P, 1))        # pairs differ widely in natural affinity
    if kind == "iid":
        logL = np.repeat(log_L0, T, axis=1)
    else:
        steps = rng.normal(0.0, 0.25, size=(P, T))
        steps[:, 0] = 0.0
        logL = log_L0 + np.cumsum(steps, axis=1)               # random-walk drift of the lift
    logL = logL + np.log(KAPPA_TRUE)[None, :]
    ref = np.full(P, 5) if t_star is None else np.broadcast_to(np.asarray(t_star), (P,)).astype(int)
    rows = np.arange(P)
    mu_ref = np.exp(logL[rows, ref]) * shape_E[rows, ref]
    shape_E = shape_E * (scale / mu_ref)[:, None]               # baseline mu0 at ref == scale
    if factor is not None:
        f = np.broadcast_to(np.asarray(factor, float), (P,))
        lf = np.log(f)
        cols = np.arange(T)[None, :]
        after = cols >= ref[:, None]
        if shape == "ramp":
            bump = np.where(cols == ref[:, None], 0.5 * lf[:, None], np.where(after, lf[:, None], 0.0))
        else:
            bump = np.where(after, lf[:, None], 0.0)
        logL = logL + bump
    rho = np.exp(rng.uniform(math.log(1 / 30), math.log(30), size=(P, 1)))   # margin imbalance
    n_a = np.maximum(np.round(np.sqrt(shape_E * N[None, :] * rho)), 1)
    n_b = np.maximum(np.round(np.sqrt(shape_E * N[None, :] / rho)), 1)
    E_int = n_a * n_b / N[None, :]                              # expectation exactly as the detector computes it
    n_ab = _draw_counts(rng, E_int * np.exp(logL), kind)
    return n_ab, n_a, n_b


def _fmt(x, w=6, nd=3):
    return f"{x:{w}.{nd}f}"


def calibrate(n_ab, a, b, prm):
    """kappa and nu as `detect` would estimate them from a pooled population."""
    E0 = expected(a, b, N_REAL)
    kap = estimate_kappa(n_ab, E0, prm)
    nu, psi, _ = estimate_dispersion(n_ab, E0 * kap[None, :], prm)
    return kap, (nu, psi)


def rule(n_ab, a, b, kap, nupsi, prm):
    E = expected(a, b, N_REAL) * kap[None, :]
    sc = scan(n_ab, E, nupsi[0], prm, nupsi[1])
    S, pp, onset = pair_summary(sc, prm)
    return E, S, pp, onset


def _pool(rng, nrep, scales, kind):
    x = [simulate(rng, nrep, s, kind) for s in scales]
    return tuple(np.vstack([y[i] for y in x]) for i in range(3))


def run_simulation(seed=7, quick=False, out=sys.stdout):
    rng = np.random.default_rng(seed)
    nrep = 1500 if not quick else 300
    scales = [0.3, 1, 3, 10, 30, 100, 300]
    pr = lambda *a: print(*a, file=out)
    P0 = Params()
    Pn = Params(min_count=0, r_min=1.0, l_min=0.0, sustain=False)

    # --- A. false positives under the null, by count scale, three null families
    pr("## A. False positives under the null (per pair, any window), by baseline expected count mu0\n")
    pr("Rule = onset dated by `detect` defaults (gates + pair-level p <= 0.01). 'No gates' = same test without min_count, ratio, sustain gates.")
    pr("Naive = any window-to-window lift jump >= 1.5 with n_ab >= 10 (analyze_spike.py). Last column: pair-level parametric p <= 0.05.\n")
    pr("| null | nu, psi | mu0 | rule FPR | no-gates FPR | naive FPR | param p<=.05 |")
    pr("|---|---|---|---|---|---|---|")
    for kind in NULL_KINDS:
        pn, pa, pb = _pool(rng, nrep, scales, kind)
        kap, nu = calibrate(pn, pa, pb, P0)
        for si, s in enumerate(scales):
            sl = slice(si * nrep, (si + 1) * nrep)
            E, S, pp, onset = rule(pn[sl], pa[sl], pb[sl], kap, nu, P0)
            _, _, pp2, onset2 = rule(pn[sl], pa[sl], pb[sl], kap, nu, Pn)
            nj = naive_jumps(pn[sl], expected(pa[sl], pb[sl], N_REAL))
            naive = (np.nan_to_num(nj, nan=0.0) >= 1.5).any(1)
            pr(f"| {kind} | {nu[0]:.2f}, {nu[1]:.1f} | {s} | {_fmt((onset >= 0).mean())} | {_fmt((onset2 >= 0).mean())} | {_fmt(naive.mean())} | {_fmt((pp <= 0.05).mean())} |")
    pr()

    # --- B. power by scale and factor
    facs = [2, 3, 5, 10, 30]
    for kind in ("drift", "drift+cluster"):
        pn, pa, pb = _pool(rng, nrep, scales, kind)
        kap, nu = calibrate(pn, pa, pb, P0)
        for shape in ("step", "ramp"):
            pr(f"## B. Power [{kind}, {shape}]: % dated in the right window / % right window or one late\n")
            pr("Take-off at a random window in 3..7 (1970s..2010s); unadjusted, rule with pair-level p <= 0.01. Rows: baseline expected count mu0 in the take-off window. Columns: lift multiplier.\n")
            pr("| mu0 | " + " | ".join(f"x{f}" for f in facs) + " |")
            pr("|---|" + "---|" * len(facs))
            for s in scales:
                cells = []
                for f in facs:
                    ts = rng.integers(3, 8, size=nrep)
                    n_ab, a, b = simulate(rng, nrep, s, kind, factor=f, t_star=ts, shape=shape)
                    _, _, _, onset = rule(n_ab, a, b, kap, nu, P0)
                    cells.append(f"{100 * (onset == ts).mean():.0f}/{100 * ((onset == ts) | (onset == ts + 1)).mean():.0f}")
                pr(f"| {s} | " + " | ".join(cells) + " |")
            pr()

    # --- C. threshold grid
    pr("## C. Threshold choice (drift+cluster null; FPR pooled over mu0 in 1,3,10,30,100; power = x5 step at mu0=10 / 30, right window or one late)\n")
    pr("Unadjusted pair-level rule at p <= 0.01. r_min = 2 throughout (r_min between 1.5 and 3 changes nothing: the NB test already demands a larger ratio).\n")
    pr("| min_count | l_min | indep_test | sustain | FPR | power mu0=10 | power mu0=30 |")
    pr("|---|---|---|---|---|---|---|")
    kind = "drift+cluster"
    pn, pa, pb = _pool(rng, nrep, [1, 3, 10, 30, 100], kind)
    kap, nupsi = calibrate(pn, pa, pb, P0)
    ts = rng.integers(3, 8, size=nrep)
    ev = {s: simulate(rng, nrep, s, kind, factor=5, t_star=ts) for s in (10, 30)}
    for mc in (5, 10, 20, 30):
        for lm in (1.0, 1.5, 2.0):
            for it in (False, True):
                for su in ((True, False) if (mc, lm, it) == (10, 1.0, False) else (True,)):
                    prm = Params(min_count=mc, l_min=lm, sustain=su, indep_test=it)
                    _, _, _, onset = rule(pn, pa, pb, kap, nupsi, prm)
                    pw = []
                    for s in (10, 30):
                        _, _, _, o = rule(*ev[s], kap, nupsi, prm)
                        pw.append(((o == ts) | (o == ts + 1)).mean())
                    pr(f"| {mc} | {lm} | {it} | {su} | {_fmt((onset >= 0).mean())} | {_fmt(pw[0])} | {_fmt(pw[1])} |")
    pr()

    # --- D. mixed population with BH
    pr("## D. Mixed population + Benjamini-Hochberg at q = 0.05\n")
    pr("Events: 4% of pairs, lift multiplier in {3,5,10}, mu0 log-uniform 0.3..300, take-off window 3..7. FDR = share of flagged pairs that are nulls; "
       "power = events flagged and dated in t* or t*+1, over all events / over events with mu0 >= 10. 'param' = BH on the NB scan p-value; 'emp' = BH on the "
       "size-matched empirical p-value (M neighbours); 'final' = BH on max of the two.\n")
    pr("| pool | M | null kind | param FDR | param pow | param pow(mu0>=10) | emp FDR | emp pow | emp pow(mu0>=10) | final FDR | final pow | final pow(mu0>=10) |")
    pr("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for Ptot, M in ((2000, 100), (10000, 500), (10000, 2000)):
        for kind in NULL_KINDS:
            nev = int(0.04 * Ptot)
            sc_all = np.exp(rng.uniform(math.log(0.3), math.log(300), size=Ptot))
            is_ev = np.arange(Ptot) < nev
            ts_all = np.where(is_ev, rng.integers(3, 8, size=Ptot), 5)
            fac_all = np.where(is_ev, rng.choice([3.0, 5.0, 10.0], size=Ptot), 1.0)
            n_ab, a, b = simulate(rng, Ptot, sc_all, kind, factor=fac_all, t_star=ts_all)
            r = detect(n_ab, a, b, N_REAL, params=Params(n_neighbors=M))
            row = []
            hi = is_ev & (sc_all >= 10)
            for key in ("q_param", "q_emp", "q_final"):
                flag = (r[key] <= 0.05) & (r["onset"] >= 0)
                good = is_ev & ((r["onset"] == ts_all) | (r["onset"] == ts_all + 1))
                row += [(flag & ~is_ev).sum() / max(flag.sum(), 1), (flag & good).sum() / nev, (flag & good & hi).sum() / hi.sum()]
            pr(f"| {Ptot} | {M} | {kind} | " + " | ".join(_fmt(x) for x in row) + " |")
    pr()


# --------------------------------------------------------------------------------------------
# step 6b: the 35 section-level pairs and the seed events
# --------------------------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WINDOWS = [(1931, 1949), (1950, 1959), (1960, 1969), (1970, 1979), (1980, 1989), (1990, 1999),
           (2000, 2009), (2010, 2019), (2020, 2024)]
WLAB = [f"{a}-{b}" for a, b in WINDOWS]

# hand-mapped events of seed set A (same table as analyze_spike.py): name -> (sectionA, sectionB, year)
EV_A = {
    "E38 Furstenberg ergodic Szemeredi": ("11", "37", 1977),
    "E50 Green-Tao": ("05", "11", 2004),
    "E50 Green-Tao ergodic route": ("11", "37", 2004),
    "E41 Donaldson gauge theory": ("57", "81", 1983),
    "E41 Donaldson gauge theory (58x81)": ("58", "81", 1983),
    "E42 Jones polynomial": ("46", "57", 1985),
    "E44 moonshine / vertex algebras": ("17", "81", 1988),
    "E47 mirror symmetry": ("14", "81", 1991),
    "E49 SLE": ("60", "81", 2000),
    "E49 SLE (30x60)": ("30", "60", 2000),
    "E52 expansion in groups": ("05", "20", 2008),
    "E51 polynomial method": ("05", "14", 2008),
    "E56 Huh Hodge theory": ("05", "14", 2012),
    "E57 regularity structures": ("35", "60", 2014),
    "E59 PFR entropy": ("05", "94", 2023),
    "E73 computer proof": ("05", "68", 1976),
    "E36 topological combinatorics": ("05", "55", 1978),
    "E33 index theorem": ("55", "58", 1963),
    "B13 arithmetic QUE": ("11", "37", 2006),
    "B17 entropy": ("37", "94", 1958),
    "B18 wavelets": ("42", "94", 1988),
    "B24 D-modules": ("32", "35", 1984),
    "E34/E65 Langlands": ("11", "22", 1967),
}


def window_of(year):
    for i, (a, b) in enumerate(WINDOWS):
        if a <= year <= b:
            return i
    return None


def b_anchor_year(ev):
    """Anchor year of a seed-B event: start of the conceptual interval if it is <= 10 years wide,
    else start of the methodological interval, else the conceptual midpoint."""
    c, m = ev["dates"].get("conceptual"), ev["dates"].get("methodological")
    if c and c[1] - c[0] <= 10:
        return c[0]
    if m:
        return m[0]
    return (c[0] + c[1]) // 2 if c else None


def load_counts():
    rows = {}
    with open(os.path.join(HERE, "zbmath_counts.jsonl")) as fh:
        for line in fh:
            r = json.loads(line)
            if r["n"] is not None:
                rows[r["q"]] = r["n"]
    meta = json.load(open(os.path.join(HERE, "zb_spike_meta.json")))
    return rows, meta


def build_arrays(rows, meta):
    secs = meta["sections"]
    pairs = [tuple(p) for p in meta["pairs"]] + [tuple(p) for p in meta["control"]]
    N = np.array([rows[f"py:{a}-{b}"] for a, b in WINDOWS], float)
    sec_idx = {s: i for i, s in enumerate(secs)}
    n_cls = np.full((len(secs), len(WINDOWS)), np.nan)
    for s in secs:
        for t, (a, b) in enumerate(WINDOWS):
            n_cls[sec_idx[s], t] = rows.get(f"cc:{s} py:{a}-{b}", np.nan)
    n_ab = np.full((len(pairs), len(WINDOWS)), np.nan)
    for i, (x, y) in enumerate(pairs):
        for t, (a, b) in enumerate(WINDOWS):
            q = f"cc:{x} cc:{y} py:{a}-{b}"
            n_ab[i, t] = rows.get(q, rows.get(f"cc:{y} cc:{x} py:{a}-{b}", np.nan))
    pidx = np.array([[sec_idx[x], sec_idx[y]] for x, y in pairs])
    return pairs, secs, N, n_cls, n_ab, pidx


def why_not(res, i, w, prm):
    """Plain-language reason a pair has no eligible onset in expected window w or the next."""
    sc = res["scan"]
    out = []
    for t in (w, w + 1):
        if t >= sc["lift"].shape[1]:
            continue
        if not sc["tested"][i, t]:
            out.append(f"{WLAB[t]}: no baseline/obs")
            continue
        r = []
        n = sc["lift"][i, t] * res["E"][i, t]
        if n < prm.min_count:
            r.append(f"n={n:.0f}<{prm.min_count}")
        if sc["ratio"][i, t] < prm.r_min:
            r.append(f"x{sc['ratio'][i, t]:.1f} vs baseline")
        if sc["lift"][i, t] < prm.l_min:
            r.append(f"lift {sc['lift'][i, t]:.2f}")
        if not r and not sc["eligible"][i, t]:
            r.append("not sustained")
        if not r:
            r.append(f"gates pass, p_pair={min(1, sc['tested'][i].sum() * 10 ** -sc['S_raw'][i, t]):.2g}>{prm.alpha_date}")
        out.append(f"{WLAB[t]}: " + ", ".join(r))
    return "; ".join(out)


def apply_to_data(out=sys.stdout, prm=None, full=True):
    pr = lambda *a: print(*a, file=out)
    rows, meta = load_counts()
    pairs, secs, N, n_cls, n_ab, pidx = build_arrays(rows, meta)
    prm = prm or Params(n_neighbors=15)  # only 34 other pairs exist: M must be small, see note
    res = detect(n_ab, n_cls, n_cls, N, pair_index=pidx, params=prm)
    npair = len(meta["pairs"])
    sc = res["scan"]
    is_ctrl = np.arange(len(pairs)) >= npair
    pr(f"dispersion nu = {res['nu']:.3f} (iid-NB size k = 2/nu = {2 / res['nu']:.1f}), Poisson inflation psi = {res['psi']:.2f}, "
       f"from {res['nu_transitions']} adjacent-window transitions")
    pr("kappa (typical pair lift, median over pairs with E>=1) by window: " + " ".join(f"{v:.2f}" for v in res["kappa"]))
    pr(f"M neighbours for empirical null = {res['n_neighbors']} (p_emp floor {1 / (res['n_neighbors'] + 1):.3f})\n")
    if full:
        pr("| pair | kind | lift/kappa by window (1931-49 .. 2020-24) | onset | S | p_param | p_emp | q_param |")
        pr("|---|---|---|---|---|---|---|---|")
    for i, (x, y) in enumerate(pairs if full else []):
        L = " ".join("-" if not np.isfinite(v) else f"{v:.1f}" for v in sc["lift"][i])
        # window 0 pair counts are missing in the data; show lift from window 1
        on = "none" if res["onset"][i] < 0 else WLAB[res["onset"][i]]
        pr(f"| {x}x{y} | {'control' if is_ctrl[i] else 'event'} | {L} | {on} | {res['S'][i]:.1f} | "
           f"{res['p_param'][i]:.3g} | {res['p_emp'][i]:.3g} | {res['q_param'][i]:.3g} |")
    pr()

    # naive detector at pair level (same rule as analyze_spike.py)
    nj = naive_jumps(n_ab, res["E_indep"])
    naive_pair = (np.nan_to_num(nj, nan=0.0) >= 1.5).any(1)
    ctrl_tr = nj[is_ctrl]
    ctrl_tr = ctrl_tr[np.isfinite(ctrl_tr)]
    pr(f"controls: naive transition rate {np.mean(ctrl_tr >= 1.5):.3f} ({int((ctrl_tr >= 1.5).sum())}/{len(ctrl_tr)}); "
       f"naive per-pair 'any jump' {int(naive_pair[is_ctrl].sum())}/{int(is_ctrl.sum())}; "
       f"new rule per-pair onset {int((res['onset'][is_ctrl] >= 0).sum())}/{int(is_ctrl.sum())}; "
       f"BH q_param<=.05 {int((res['q_param'][is_ctrl] <= 0.05).sum())}/{int(is_ctrl.sum())}")
    pr(f"listed event pairs: naive per-pair {int(naive_pair[~is_ctrl].sum())}/{int((~is_ctrl).sum())}; "
       f"new rule onset {int((res['onset'][~is_ctrl] >= 0).sum())}/{int((~is_ctrl).sum())}; "
       f"BH q_param<=.05 {int((res['q_param'][~is_ctrl] <= 0.05).sum())}/{int((~is_ctrl).sum())}\n")

    # event table
    pair_row = {tuple(sorted(p)): i for i, p in enumerate(pairs)}
    tests = []
    not_queried = []
    for name, (x, y, yr) in EV_A.items():
        if tuple(sorted((x, y))) not in pair_row:
            not_queried.append(name)
            continue
        tests.append(("A", name, tuple(sorted((x, y))), yr))
    sb = json.load(open(os.path.join(REPO, "data/collection/field-events-seed-b.json")))
    for ev in sb["events"]:
        yr = b_anchor_year(ev)
        ms = ev.get("mscSections") or []
        if yr is None:
            continue
        for i in range(len(ms)):
            for j in range(i + 1, len(ms)):
                k = tuple(sorted((ms[i], ms[j])))
                if k in pair_row:
                    tests.append(("B", f"{ev['id']} {ev['name'][:48]}", k, yr))
    if full:
        pr("| id/name | pair | event year | expected window | n_ab there | lift there / baseline | detected onset | verdict | why not (if missed) | naive jump>=1.5 (window or next) | q_param |")
        pr("|---|---|---|---|---|---|---|---|---|---|---|")
    tally = {}
    rows_out = []
    for src, name, k, yr in tests:
        i = pair_row[k]
        w = window_of(yr)
        on = int(res["onset"][i])
        nvj = [nj[i, w - 1] if w >= 1 else np.nan, nj[i, w] if w < nj.shape[1] else np.nan]
        nvj = [v for v in nvj if np.isfinite(v)]
        naive_hit = (max(nvj) >= 1.5) if nvj else None
        if w == 0:
            v = "unscorable"
        elif on < 0:
            v = "missed"
        elif on == w:
            v = "exact"
        elif on == w + 1:
            v = "one window late"
        elif on > w + 1:
            v = f"late"
        else:
            v = f"early"
        why = "" if on >= 0 else why_not(res, i, w, prm)
        tally[v] = tally.get(v, 0) + 1
        nw = n_ab[i, w]
        bl = sc["base_lift"][i, w]
        if on >= 0 and not full:
            pr(f"detected: {name} {k[0]}x{k[1]} anchor {yr} ({WLAB[w]}) onset {WLAB[on]} -> {v}")
        if full:
          pr(f"| {name} | {k[0]}x{k[1]} | {yr} | {WLAB[w]} | {nw:.0f} | {sc['lift'][i, w]:.2f} / {bl:.2f} | {'none' if on < 0 else WLAB[on]} | {v} | {why} | "
             f"{'n/a' if naive_hit is None else ('yes' if naive_hit else 'no')} | {res['q_param'][i]:.2g} |")
    pr(f"\ntally over {len(tests)} event-pair tests: {tally}")
    if not_queried:
        pr("seed events whose pair was not among the 35 queried (cannot be scored): " + "; ".join(not_queried))
    return res


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("sim", "all"):
        run_simulation(quick="--quick" in sys.argv)
    if cmd in ("apply", "all"):
        apply_to_data()
        print("\n## Sensitivity: relaxed rule (m_base=1, min_count=10, alpha_date=0.05); NOT a recommended setting\n")
        apply_to_data(prm=Params(n_neighbors=15, m_base=1, min_count=10, alpha_date=0.05), full=False)
