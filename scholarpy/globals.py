# ===============================================================
# ScholarPy - Global variables
# ===============================================================
# Author: Ricardo Costa (rcosta@dep.uminho.pt)
# License: MIT License (see LICENSE file for details)
# Repository: https://github.com/ricardodpcosta/ScholarPy
# Description: Core functionalities for ScholarPy.
# ===============================================================

# Stop words
STOPWORDS = set([
    "abstract", "academic", "acta", "annual", "approach", "apply", "article",
    "base", "case", "center", "centre", "change", "congress", "conference", "contributor",
    "decrease", "education",
    "effect", "european",
    "high",
    "ieee", "increase", "international",
    "journal",
    "load", "low",
    "meeting",
    "national",
    "path", "portugal", "portuguese", "procedia", "proceeding", "profile", "project",
    "property", "publications",
    "reduce", "reduction", "report", "research", "researcher", "review",
    "self", "strategy", "student", "study", "symposium",
    "techma",
    "university", "user",
    "works", "workshop"
])

# Compound words
COMPWORDS = {
    "additive manufacturing": "additive_manufacturing",
    "artificial intelligence": "artificial_intelligence",
    "finite difference": "finite_difference",
    "finite element": "finite_element",
    "finite volume": "finite_volume",
    "machine learning": "machine_learning",
    "multi layered": "multilayered",
    "multi material": "multimaterial",
    "multi modal": "multimodal",
    "multi objective": "multiobjective",
    "multi physics": "multiphysics",
    "multi scale": "multiscale",
    "multi sensor": "multisensor",
    "multi variate": "multivariate",
    "neural networks": "neural_networks",
}

# Lemma words
LEMMAWORDS = {
    "additive_manufacture": "additive_manufacturing",
    "analyses": "analyse",
    "analyze": "analyse",
    "analyzes": "analyse",
    "behavior": "behaviour",
    "computation": "computational",
    "computer": "computational",
    "computing": "computational",
    "efficient": "efficiency",
    "engineer": "engineering",
    "fiber": "fibre",
    "form": "forming",
    "innovative": "innovation",
    "inovate": "innovation",
    "manufacture": "manufacturing",
    "model": "modelling",
    "modeling": "modelling",
    "mold": "moulding",
    "molding": "moulding",
    "optimal": "optimisation",
    "optimization": "optimisation",
    "optimise": "optimisation",
    "optimize": "optimisation",
    "sustainable": "sustainability"
}

# End of file
