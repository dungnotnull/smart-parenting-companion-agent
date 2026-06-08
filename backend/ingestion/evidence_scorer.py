import logging

logger = logging.getLogger(__name__)

EVIDENCE_CLASSIFICATION_RULES: list[tuple[list[str], str, int]] = [
    (["randomized controlled trial", "randomized clinical trial", "rct", "double-blind", "placebo-controlled"], "RCT", 1),
    (["meta-analysis", "meta analysis", "systematic review and meta-analysis", "pooled analysis"], "meta-analysis", 1),
    (["systematic review", "systematic literature review"], "systematic-review", 2),
    (["clinical practice guideline", "practice guideline", "consensus guideline", "guideline", "recommendations"], "guideline", 2),
    (["cohort study", "longitudinal study", "prospective study", "retrospective study", "case-control"], "observational", 3),
    (["cross-sectional", "survey", "registry"], "observational", 3),
    (["case series", "case report", "case study"], "case-study", 4),
    (["expert opinion", "editorial", "commentary", "narrative review", "review article"], "expert-opinion", 5),
]


def classify_evidence_level(abstract: str, title: str = "") -> tuple[str, int, float]:
    text = f"{title} {abstract}".lower()

    for keywords, label, rank in EVIDENCE_CLASSIFICATION_RULES:
        for kw in keywords:
            if kw in text:
                confidence = 0.9 if len([k for k in keywords if k in text]) >= 2 else 0.7
                return label, rank, confidence

    return "expert-opinion", 5, 0.5


def score_evidence_quality(abstract: str, title: str = "") -> dict:
    evidence_level, rank, confidence = classify_evidence_level(abstract, title)

    quality_score = (6 - rank) * confidence

    has_sample_size = any(w in abstract.lower() for w in ["n=", "n =", "sample", "participants", "subjects", "patients"])
    has_statistics = any(w in abstract.lower() for w in ["p<", "p <", "p=", "p =", "95% ci", "odds ratio", "hazard ratio", "relative risk", "confidence interval", "statistically significant"])
    has_methods = any(w in abstract.lower() for w in ["method", "design", "protocol", "inclusion criteria", "exclusion criteria"])

    richness = 0.0
    if has_sample_size:
        richness += 0.1
    if has_statistics:
        richness += 0.15
    if has_methods:
        richness += 0.05

    final_score = min(1.0, quality_score + richness)

    return {
        "evidence_level": evidence_level,
        "evidence_rank": rank,
        "confidence": round(confidence, 3),
        "quality_score": round(final_score, 3),
        "has_sample_size": has_sample_size,
        "has_statistics": has_statistics,
        "has_methods": has_methods,
    }
