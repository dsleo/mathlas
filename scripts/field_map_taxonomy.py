"""Stable, readable lanes for the Field Emergence Map.

Catalogue output names are deliberately fine grained and inconsistently
capitalized. Map lanes group those labels without changing the source data.
The order matters: a specialist field wins before its broader parent.
"""

import re
import unicodedata


LANES = (
    "Astronomy & trigonometry",
    "Number theory",
    "Algebraic geometry",
    "Geometry",
    "Differential geometry",
    "Topology",
    "Algebraic topology",
    "Algebra",
    "Group & representation theory",
    "Category & homological algebra",
    "Analysis",
    "Approximation theory",
    "Functional & harmonic analysis",
    "Complex analysis",
    "Differential equations",
    "Functional equations",
    "Fluid mechanics",
    "Solid mechanics",
    "Probability",
    "Statistics & decision theory",
    "Combinatorics",
    "Graph theory",
    "Logic & foundations",
    "Computer science",
    "Algorithms & complexity",
    "Numerical analysis",
    "Game theory & economics",
    "Dynamics",
    "Mathematical physics",
    "Geophysics & geodesy",
    "Optimization & control",
    "Information & cryptography",
    "Applied mathematics",
    "Other fields",
)


def _key(value):
    value = unicodedata.normalize("NFKD", value or "").casefold()
    value = "".join(c for c in value if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def map_lane(event):
    """Classify an event by its first stated output, with a title fallback."""
    label = _key((event.get("to") or event.get("from") or [""])[0])
    title = _key(event.get("name"))

    def has(*terms):
        return any(re.search(r"\b" + re.escape(term), label) for term in terms)

    # Some early catalogue passes used only a broad output label even when the
    # event headline states a more specific field unambiguously.
    if label in {"geometry", "analysis", "topology", "algebra", "combinatorics", "number theory", "probability"}:
        if title.startswith("graph theory") or title.startswith("random graph theory"):
            return "Graph theory"
        if title.startswith(("algebraic topology", "a 1 homotopy", "higher algebraic k theory")):
            return "Algebraic topology"
        if title.startswith(("functional analysis", "fourier series", "wavelets", "fourier integral operators")):
            return "Functional & harmonic analysis"
        if title.startswith(("complex analysis", "real variable methods in complex analysis")):
            return "Complex analysis"
        if title.startswith(("riemannian geometry", "symplectic topology")):
            return "Differential geometry"
        if title.startswith(("scheme theory", "sheaf theory", "geometric langlands", "geometric invariant theory", "mirror symmetry")):
            return "Algebraic geometry"
        if title.startswith(("viscosity solutions", "landau damping")):
            return "Differential equations"
        if title.startswith(("game theory", "nash equilibrium")):
            return "Game theory & economics"

    if has("astronom", "trigonom", "celestial", "planetary", "spherical"):
        return "Astronomy & trigonometry"
    if has("langlands", "automorphic", "diophantine", "number theory", "number fields", "arithmetic", "modular form", "zeta", "l function", "p adic", "class group", "transcenden", "irrational"):
        if has("arithmetic geometry", "algebraic geometry"):
            return "Algebraic geometry"
        return "Number theory"
    if has("algebraic geometry", "birational", "scheme", "moduli", "hodge", "kahler", "calabi yau", "mirror symmetry", "brill noether", "enumerative geometry", "topological recursion", "variet", "positive geometry", "intersection theory"):
        return "Algebraic geometry"
    if has("homotopy type theory"):
        return "Logic & foundations"
    if has("algebraic topology", "homotopy", "homology", "cohomology", "cobordism", "k theory", "fibre bundle", "characteristic class", "tqft", "floer theory", "fukaya"):
        return "Algebraic topology"
    if has("differential geometry", "riemannian", "lorentzian", "symplectic", "contact geometry", "curvature", "geodesic", "manifold theory", "singularity theory"):
        return "Differential geometry"
    if has("topology", "knot", "manifold", "dimension theory", "triangulation conjecture"):
        return "Topology"
    if re.search(r"\b(graph|graphs|graphon|graphons|network|networks|matroid|matroids)\b", label) and not has("feynman"):
        return "Graph theory"
    if has("group theory", "cubulated group", "lie algebra", "lie theory", "representation", "burnside", "moonshine", "vertex operator", "operator algebra", "voa", "cluster algebra"):
        return "Group & representation theory"
    if has("categor", "homological", "derived functor", "deformation theory", "condensed mathematics"):
        return "Category & homological algebra"
    if has("complex analysis", "complex dynamics", "riemann surface", "several complex", "holomorphic", "elliptic function"):
        return "Complex analysis"
    if has("approximation theory", "best uniform approximation", "best approximation"):
        return "Approximation theory"
    if has("functional analysis", "harmonic analysis", "banach", "hilbert space", "sobolev", "microlocal", "distribution theory", "spectral theory", "spectral gap", "operator theory"):
        return "Functional & harmonic analysis"
    if has("functional equation", "difference equation"):
        return "Functional equations"
    if has("fluid mechanics", "fluid pde", "hydrodynamics", "navier stokes"):
        return "Fluid mechanics"
    if has("elasticity of solids", "solid mechanics", "elastic solids"):
        return "Solid mechanics"
    if has("geophys", "geodesy", "figure of the earth"):
        return "Geophysics & geodesy"
    if has("differential equation", "pde", "spde", "fluid", "soliton", "integrable", "potential theory", "global analysis"):
        return "Differential equations"
    if has("statistic", "inference", "bayesian", "decision theory", "demography", "economics", "social choice", "general equilibrium"):
        return "Statistics & decision theory"
    if has("probabil", "stochastic", "brownian", "random walk", "large deviation", "random planar", "random geometry", "scaling limits"):
        return "Probability"
    if has("logic", "foundation", "set theory", "type theory", "model theory", "proof theory", "theorem proving", "computability", "axiom", "undecidab", "forcing"):
        return "Logic & foundations"
    if has("cryptograph", "information", "coding", "signal", "privacy"):
        return "Information & cryptography"
    if has("game theory", "combinatorial games", "social choice", "general equilibrium", "mathematical economics"):
        return "Game theory & economics"
    if has("numerical analysis", "numerical method", "finite element"):
        return "Numerical analysis"
    if has("complexity", "algorithm", "automata", "formal language", "program verification", "semantics of programming", "term rewriting", "hardness", "switching theory"):
        return "Algorithms & complexity"
    if has("computer", "computational", "machine learning", "ml guided", "learning theory", "data analysis", "discovery of matrix"):
        return "Computer science"
    if has("optim", "control", "variational", "calculus of variations", "filtering"):
        return "Optimization & control"
    if has("dynam", "ergodic", "stability theory", "chaos", "catastrophe"):
        return "Dynamics"
    if has("physics", "quantum", "mechanic", "relativity", "gauge", "spin glass", "statistical mechanics", "feynman", "gravity", "twistor"):
        return "Mathematical physics"
    if has("combinator", "ramsey", "discrepancy", "design theory", "partition identit", "game theory"):
        return "Combinatorics"
    if has("algebra", "ring", "field theory", "theory of equations", "theory of cubic", "elimination", "determinant", "matrix", "linear algebra", "boolean", "complex numbers"):
        return "Algebra"
    if has("geometry", "geometric", "distance set", "grassmannian"):
        return "Geometry"
    if has("analysis", "calculus", "integral", "integration", "logarithm", "measure theory", "real number", "series", "quadrature", "ratio"):
        return "Analysis"
    if has("applied", "image", "population", "stati", "engineering"):
        return "Applied mathematics"
    if title.startswith(("euclid", "pythagor", "archimed")) or label == "mathematics":
        return "Geometry"
    return "Other fields"
