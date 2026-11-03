"""Stage C - Rules engine. Deterministic: category + client profile + clause cards -> recommendation.

Outputs one of ELIGIBLE / BLOCKED / NEEDS_FACT / NEEDS_REVIEW, with the clause and the path taken.
"""
import operator

ELIGIBLE, BLOCKED, NEEDS_FACT, NEEDS_REVIEW = "ELIGIBLE", "BLOCKED", "NEEDS_FACT", "NEEDS_REVIEW"
OPS = {"<=": operator.le, "<": operator.lt, ">=": operator.ge, ">": operator.gt, "==": operator.eq}

FACT_QUESTIONS = {
    "seating_capacity": "What is the approved seating capacity (incl. driver) on the vehicle's RC?",
}


def blocked_categories(cards: list) -> set:
    return {c for card in cards for c in card["categories"]}


def _exception_applies(exc: dict, category: str, profile: dict):
    """Return the evidence string if this exception applies, else None."""
    if exc["type"] == "profile_flag":
        for f in profile.get("flags", []):
            if f["flag"] == exc["flag"]:
                return f["evidence"]
    elif exc["type"] == "outward_same_category":
        for o in profile.get("outward_categories", []):
            if o["category"] == category:
                return o["evidence"]
    elif exc["type"] == "statutory_obligation":
        for ob in profile.get("statutory_obligations", []):
            if category in ob["categories"]:
                return f'{ob["law"]} | {ob["evidence"]}'
    return None


def decide(category: str, facts: dict, profile: dict, cards: list) -> dict:
    if category == "unclear":
        return {"recommendation": NEEDS_REVIEW, "clause": "", "rule_path": ["category unclear"], "question": ""}

    card = next((c for c in cards if category in c["categories"]), None)
    if card is None:
        return {"recommendation": ELIGIBLE, "clause": "",
                "rule_path": [f"'{category}' not covered by in-scope s.17(5) clauses"], "question": ""}

    path = [f"'{category}' falls under {card['id']}"]
    if card.get("requires_fact"):
        fact = card["requires_fact"]
        if facts.get(fact) is None:
            path.append(f"required fact '{fact}' not on invoice")
            return {"recommendation": NEEDS_FACT, "clause": card["citation"], "rule_path": path,
                    "question": FACT_QUESTIONS.get(fact, f"Provide {fact}")}
    cond = card.get("blocked_if")
    if cond:
        val = facts.get(cond["fact"])
        if not OPS[cond["op"]](val, cond["value"]):
            path.append(f"{cond['fact']}={val} is not {cond['op']} {cond['value']} -> clause does not bite")
            return {"recommendation": ELIGIBLE, "clause": card["citation"], "rule_path": path, "question": ""}
        path.append(f"{cond['fact']}={val} {cond['op']} {cond['value']}")

    for exc in card.get("exceptions", []):
        ev = _exception_applies(exc, category, profile)
        if ev:
            path.append(f"exception: {exc['text']} [profile evidence: {ev}]")
            return {"recommendation": ELIGIBLE, "clause": card["citation"], "rule_path": path, "question": ""}

    path.append("no exception in client profile")
    return {"recommendation": BLOCKED, "clause": card["citation"], "rule_path": path, "question": ""}
