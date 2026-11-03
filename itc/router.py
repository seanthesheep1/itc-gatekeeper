"""Stage D - Router. Decides what a human must look at. Biased towards review: auto-accept is the exception."""
import re

AUTO, REVIEW = "AUTO", "REVIEW"
CONFIDENCE_FLOOR = 0.8


def hsn_hint(hsn: str, hints: dict):
    """Longest-prefix match of HSN/SAC against the hint table."""
    if not hsn:
        return None
    best = max((p for p in hints if hsn.startswith(p)), key=len, default=None)
    return hints[best] if best else None


def route(line, cls, s16, rule, blocked_cats, cfg) -> tuple[str, list]:
    reasons = []
    if s16["s16_status"] != "PASS":
        reasons.append(f"s.16: {s16['s16_status']}")
    if cls["category"] in blocked_cats:
        reasons.append("touches a s.17(5) clause - human sign-off required")
    if rule["recommendation"] in ("NEEDS_FACT", "NEEDS_REVIEW"):
        reasons.append(rule["recommendation"])
    if cls["category"] in cfg["review_always"]:
        reasons.append(cfg["review_always"][cls["category"]])
    if cls["confidence"] < CONFIDENCE_FLOOR:
        reasons.append(f"LLM confidence {cls['confidence']:.2f} < {CONFIDENCE_FLOOR}")
    if cls.get("llm_problems"):
        reasons.append("LLM output failed validation: " + "; ".join(cls["llm_problems"]))

    hint = hsn_hint(line["hsn_sac"], cfg["hsn_hints"])
    if hint:
        ok = cfg["hsn_equivalents"].get(hint, [hint])
        if cls["category"] not in ok:
            reasons.append(f"HSN/SAC {line['hsn_sac']} suggests '{hint}' but LLM said '{cls['category']}'")

    if cls["category"] not in blocked_cats:
        words = [w for w in cfg["tripwires"] if re.search(rf"\b{re.escape(w)}\b", line["description"], re.I)]
        if words:
            reasons.append(f"tripwire words {words} but LLM placed it outside s.17(5)")

    return (REVIEW if reasons else AUTO), reasons
